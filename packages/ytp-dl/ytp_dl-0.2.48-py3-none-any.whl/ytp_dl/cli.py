#!/usr/bin/env python3
# ytp_dl/cli.py — v0.2.48
#  • credentials are never written to logs
#  • get_available_heights uses proxies again
#  • fetch_pair already proxies every call

import sys
import argparse
import asyncio
import subprocess
import shutil
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urlsplit

import requests
import yt_dlp
from PIL import Image

from config import (              # ← if you are in a package use “from .config”
    TMP_DIR, CONNS, SPLITS, MIN_SPLIT,
    MAX_WORKERS, TIMEOUT, ensure_aria2c, ensure_ffmpeg,
)

# ────────────────────────── logging ────────────────────────────
LOG_FMT = "%(asctime)s  [%(levelname)s]  %(name)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger("ytp_dl")


def setup_logging(verbose: bool) -> None:
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("yt_dlp").setLevel(logging.ERROR)


def _sanitize_proxy(uri: str) -> str:
    """strip user:pass@ from proxy URI for safe logging"""
    try:
        parts = urlsplit(uri)
        host = parts.hostname or ""
        port = f":{parts.port}" if parts.port else ""
        return f"{parts.scheme}://{host}{port}"
    except Exception:
        return uri.split("@")[-1] if "@" in uri else uri


def _log_signin_error(where: str, proxy: str, vid: str, exc: Exception) -> None:
    msg = str(exc).lower()
    if any(k in msg for k in ("sign in", "sign‑in", "login required", "http error 403")):
        logger.error("[%s] sign‑in required (proxy=%s, id=%s)",
                     where, _sanitize_proxy(proxy), vid)
        logger.debug("traceback follows", exc_info=exc)


# ────────────────────────── helpers ────────────────────────────
def run_stream(cmd: list[str], outfile_name: str | None = None) -> int:
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1,
    )
    assert proc.stdout
    for line in proc.stdout:
        text = line.rstrip()
        if text:
            print(f"[download] {text}")
            sys.stdout.flush()
    proc.stdout.close()
    code = proc.wait()
    if outfile_name:
        print(f"[download_complete] {outfile_name}")
        sys.stdout.flush()
    return code


def parse_video_id(url: str) -> str | None:
    u = urlparse(url)
    if u.hostname == "youtu.be":
        return u.path.lstrip("/")
    return parse_qs(u.query).get("v", [None])[0]


def get_available_heights(vid: str, proxies: list[str]) -> list[int]:
    """
    Try each proxy until yt metadata is returned.
    """
    for proxy in proxies:
        opts = {
            "quiet": True, "no_warnings": True, "skip_download": True,
            "proxy": proxy,
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f"https://youtu.be/{vid}", download=False)
            return sorted(
                f["height"] for f in info.get("formats", [])
                if isinstance(f.get("height"), int)
            )
        except Exception as e:
            _log_signin_error("get_available_heights", proxy, vid, e)
            logger.info("proxy %s failed (%s). next…",
                        _sanitize_proxy(proxy), e.__class__.__name__)
    sys.exit("Error: all proxies failed to fetch metadata.")


def resize_image(image_path: Path, size=(640, 640)) -> None:
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")
            w, h = img.size
            if w > h:
                img = img.crop(((w - h) // 2, 0, (w + h) // 2, h))
            elif h > w:
                img = img.crop((0, (h - w) // 2, w, (h + w) // 2))
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(image_path, "JPEG", quality=95)
            logger.info("resized cover to %s: %s", size, image_path)
    except Exception:
        logger.exception("failed to resize cover %s", image_path)


def head_ok(url: str) -> bool:
    try:
        return requests.head(url, allow_redirects=True, timeout=TIMEOUT).status_code == 200
    except Exception:
        return False


def parse_args():
    p = argparse.ArgumentParser(
        prog="ytp-dl",
        usage="ytp-dl -o OUTDIR -p PROXY [--audio] [--verbose] URL [HEIGHT]",
    )
    p.add_argument("-o", "--output-dir", dest="outdir", required=True,
                   help="Directory to save the final file")
    p.add_argument("-p", "--proxy", dest="proxy", required=True,
                   help="Comma‑separated proxy URIs")
    p.add_argument("-a", "--audio", action="store_true",
                   help="Download audio-only MP3 (cover embedded)")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Enable DEBUG logging")
    p.add_argument("url", help="YouTube URL")
    p.add_argument("height", nargs="?", default="1080p",
                   help="Desired video height (e.g. 1080p)")
    return p.parse_args()


async def fetch_pair(vid: str, height: str, proxies: list[str]) -> dict:
    loop = asyncio.get_running_loop()
    exe = ThreadPoolExecutor(min(MAX_WORKERS, len(proxies)))
    future: asyncio.Future[dict] = loop.create_future()

    def schedule():
        if not future.done():
            loop.run_in_executor(exe, worker)

    def worker():
        proxy = proxies.pop(0); proxies.append(proxy)
        ydl_opts = {
            "format": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]",
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "proxy": proxy if proxy.startswith("socks") else None,
            "all-proxy": None if proxy.startswith("socks") else proxy,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://youtu.be/{vid}", download=False)
        except Exception as e:
            _log_signin_error("fetch_pair", proxy, vid, e)
            return schedule()

        fmts = info.get("requested_formats") or info.get("formats") or []
        vids = [f for f in fmts if isinstance(f.get("height"), int)
                and f["height"] <= int(height)]
        if not vids:
            return schedule()

        vfmt = max(vids, key=lambda f: f["height"])
        afmt = next((f for f in fmts if f.get("acodec", "") != "none"), None)
        if not afmt:
            return schedule()

        if head_ok(afmt["url"]) and head_ok(vfmt["url"]):
            if not future.done():
                loop.call_soon_threadsafe(future.set_result, {
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "video_url": vfmt["url"],
                    "audio_url": afmt["url"],
                    "video_ext": vfmt.get("ext", "mp4").lower(),
                    "thumbnail": info.get("thumbnail"),
                })
        else:
            return schedule()

    for _ in range(min(MAX_WORKERS, len(proxies))):
        schedule()

    return await future


async def _amain():
    args = parse_args()
    setup_logging(args.verbose)

    vid = parse_video_id(args.url) or sys.exit("Error: could not parse video ID")
    h = args.height.rstrip("p")
    proxies = [p.strip() for p in args.proxy.split(",") if p.strip()]
    if not proxies:
        sys.exit("Error: no proxies provided via -p")

    heights = get_available_heights(vid, proxies)
    if not heights or int(h) > max(heights):
        sys.exit(f"Error: requested {h}p but only up to {max(heights)}p available")

    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir()

    aria2c = ensure_aria2c()
    ffmpeg = ensure_ffmpeg()

    try:
        pair = await fetch_pair(vid, h, proxies)
        safe = ("".join(c for c in pair["title"] if c.isalnum() or c.isspace())
                .strip()[:150] or f"media_{vid}")
        outdir = Path(args.outdir).expanduser()
        outdir.mkdir(parents=True, exist_ok=True)

        # ─── audio only ──────────────────────────────────────────
        if args.audio:
            atmp = TMP_DIR / f"{vid}_audio.tmp"
            run_stream(
                [str(aria2c), "-x", str(CONNS), "-s", str(SPLITS),
                 f"--min-split-size={MIN_SPLIT}", "--file-allocation=none",
                 "--continue", "--max-tries=1", "--retry-wait=5",
                 "-o", str(atmp), pair["audio_url"]],
                outfile_name=f"{safe}.mp3",
            )

            cover_args: list[str] = []
            thumb = pair.get("thumbnail")
            if thumb and head_ok(thumb):
                cover_path = TMP_DIR / "cover.jpg"
                resp = requests.get(thumb, timeout=TIMEOUT); resp.raise_for_status()
                cover_path.write_bytes(resp.content)
                resize_image(cover_path)
                cover_args = [
                    "-i", str(cover_path), "-map", "1:v",
                    "-metadata:s:v", "title=Cover",
                    "-metadata:s:v", "comment=Cover (front)",
                ]

            mp3_out = outdir / f"{safe}.mp3"
            cmd = [str(ffmpeg), "-i", str(atmp)] + cover_args + [
                "-map", "0:a", "-c:a", "libmp3lame", "-qscale:a", "2",
                "-y", str(mp3_out),
            ]
            run_stream(cmd, outfile_name=mp3_out.name)
            return

        # ─── full video ─────────────────────────────────────────
        ext = "mkv" if pair["video_ext"] in ("webm", "mkv") else "mp4"
        vtmp = TMP_DIR / f"{vid}_video.{pair['video_ext']}"
        atmp = TMP_DIR / f"{vid}_audio.tmp"

        await asyncio.gather(
            asyncio.to_thread(
                run_stream,
                [str(aria2c), "-x", str(CONNS), "-s", str(SPLITS),
                 f"--min-split-size={MIN_SPLIT}", "--file-allocation=none",
                 "--continue", "--max-tries=1", "--retry-wait=5",
                 "-o", str(vtmp), pair["video_url"]],
                vtmp.name,
            ),
            asyncio.to_thread(
                run_stream,
                [str(aria2c), "-x", str(CONNS), "-s", str(SPLITS),
                 f"--min-split-size={MIN_SPLIT}", "--file-allocation=none",
                 "--continue", "--max-tries=1", "--retry-wait=5",
                 "-o", str(atmp), pair["audio_url"]],
                atmp.name,
            ),
        )

        final = outdir / f"{safe}.{ext}"
        run_stream(
            [str(ffmpeg), "-i", str(vtmp), "-i", str(atmp),
             "-c", "copy", "-y", str(final)],
            outfile_name=final.name,
        )

    except subprocess.CalledProcessError as e:
        sys.exit(f"Error during download/merge: {e}")

    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)


def main() -> None:
    asyncio.run(_amain())


if __name__ == "__main__":
    main()