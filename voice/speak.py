#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["kokoro-onnx>=0.4"]
# ///
"""Turn a spoken script from stdin into an MP3 with the local Kokoro voice, and print its path.

Model files download on first use. Replies older than two weeks are pruned on every run.

@example echo "Done, the tests pass." | speak.py  # /home/me/.cache/claude-voice/replies/2026-11-18-184501-3fa2.mp3
"""

import argparse
import secrets
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

CACHE = Path.home() / ".cache" / "claude-voice"
MODELS = CACHE / "models"
REPLIES = CACHE / "replies"

MODEL_RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
MODEL_FILES = ["kokoro-v1.0.onnx", "voices-v1.0.bin"]

REPLY_TTL = 14 * 86400


def ensure_models() -> None:
    """Download the Kokoro model and voice pack once, about 350 MB."""
    MODELS.mkdir(parents=True, exist_ok=True)

    for name in MODEL_FILES:
        target = MODELS / name
        if target.exists():
            continue

        print(f"voice: downloading {name}", file=sys.stderr)
        partial = target.with_suffix(".part")
        urllib.request.urlretrieve(f"{MODEL_RELEASE}/{name}", partial)
        partial.rename(target)


def prune_replies() -> None:
    """Delete reply audio older than the retention window."""
    cutoff = time.time() - REPLY_TTL

    for old in REPLIES.glob("*.mp3"):
        if old.stat().st_mtime < cutoff:
            old.unlink()


def synthesize(text: str, voice: str, speed: float):
    """Render text to float32 samples with Kokoro.

    @example synthesize("Hi there.", "af_heart", 1.0)  # (array([...]), 24000)
    """
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(str(MODELS / MODEL_FILES[0]), str(MODELS / MODEL_FILES[1]))
    lang = "en-gb" if voice.startswith("b") else "en-us"

    return kokoro.create(text, voice=voice, speed=speed, lang=lang)


def encode_mp3(samples, rate: int, target: Path) -> None:
    """Pipe raw float32 samples through ffmpeg into a compact mono MP3."""
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-y",
            "-f", "f32le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0",
            "-b:a", "64k", str(target),
        ],
        input=samples.astype("float32").tobytes(),
        check=True,
    )


def reply_path() -> Path:
    """Fresh, sortable file name for one reply.

    @example reply_path()  # .../replies/2026-11-18-184501-3fa2.mp3
    """
    stamp = time.strftime("%Y-%m-%d-%H%M%S")

    return REPLIES / f"{stamp}-{secrets.token_hex(2)}.mp3"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--speed", type=float, default=1.0)
    args = parser.parse_args()

    text = sys.stdin.read().strip()
    if not text:
        sys.exit("voice: nothing to say")

    started = time.time()
    ensure_models()
    REPLIES.mkdir(parents=True, exist_ok=True)
    prune_replies()

    samples, rate = synthesize(text, args.voice, args.speed)
    target = reply_path()
    encode_mp3(samples, rate, target)

    print(target)
    print(
        f"voice: {args.voice}, {len(samples) / rate:.0f}s of audio in {time.time() - started:.1f}s",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
