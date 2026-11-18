#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["kokoro-onnx>=0.4"]
# ///
"""Turn a spoken script from stdin into an MP3 and print its path.

Speaks with ElevenLabs when an API key is set, and falls back to the local Kokoro voice when there
is no key or ElevenLabs fails, for example when the credits run out. The script text is saved next
to the MP3 with a .txt suffix, for captions. Replies go to the system temp folder, which the OS
clears on its own.

@example echo "Done, the tests pass." | speak.py  # /tmp/claude-voice/2026-11-18-184501-3fa2.mp3
"""

import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPLIES = Path(tempfile.gettempdir()) / "claude-voice"

ELEVENLABS_KEY_FILE = Path.home() / ".config" / "claude-voice" / "elevenlabs-key"
ELEVENLABS_VOICE = "cjVigY5qzO86Huf0OWal"
ELEVENLABS_MODEL = "eleven_flash_v2_5"
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"

KOKORO_MODELS = Path.home() / ".cache" / "claude-voice" / "models"
KOKORO_RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
KOKORO_FILES = ["kokoro-v1.0.onnx", "voices-v1.0.bin"]
KOKORO_VOICE = "am_michael"


def elevenlabs_key() -> str | None:
    """The ElevenLabs API key from ELEVENLABS_API_KEY or the key file, if either is set."""
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]

    if ELEVENLABS_KEY_FILE.exists():
        return ELEVENLABS_KEY_FILE.read_text().strip() or None

    return None


def elevenlabs(text: str, key: str) -> bytes:
    """Speak text with ElevenLabs and return the MP3 bytes.

    @example elevenlabs("Hi there.", key)  # b"ID3…"
    """
    request = urllib.request.Request(
        ELEVENLABS_URL.format(voice=ELEVENLABS_VOICE),
        data=json.dumps({"text": text, "model_id": ELEVENLABS_MODEL}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def ensure_kokoro() -> None:
    """Download the Kokoro model and voice pack once, about 350 MB."""
    KOKORO_MODELS.mkdir(parents=True, exist_ok=True)

    for name in KOKORO_FILES:
        target = KOKORO_MODELS / name
        if target.exists():
            continue

        print(f"voice: downloading {name}", file=sys.stderr)
        partial = target.with_suffix(".part")
        urllib.request.urlretrieve(f"{KOKORO_RELEASE}/{name}", partial)
        partial.rename(target)


def kokoro(text: str) -> bytes:
    """Speak text with the local Kokoro model and return MP3 bytes, encoded by ffmpeg.

    @example kokoro("Hi there.")  # b"ID3…"
    """
    from kokoro_onnx import Kokoro

    ensure_kokoro()
    model = Kokoro(str(KOKORO_MODELS / KOKORO_FILES[0]), str(KOKORO_MODELS / KOKORO_FILES[1]))
    samples, rate = model.create(text, voice=KOKORO_VOICE, lang="en-us")

    return subprocess.run(
        [
            "ffmpeg", "-loglevel", "error",
            "-f", "f32le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0",
            "-b:a", "64k", "-f", "mp3", "pipe:1",
        ],
        input=samples.astype("float32").tobytes(),
        capture_output=True,
        check=True,
    ).stdout


def speak(text: str) -> tuple[bytes, str]:
    """Speak text with ElevenLabs if possible, otherwise Kokoro, and name the engine used.

    @example speak("Hi there.")  # (b"ID3…", "elevenlabs")
    """
    key = elevenlabs_key()
    if key is None:
        return kokoro(text), "kokoro"

    try:
        return elevenlabs(text, key), "elevenlabs"
    except (urllib.error.URLError, TimeoutError) as error:
        detail = error.read().decode()[:200] if isinstance(error, urllib.error.HTTPError) else error
        print(f"voice: ElevenLabs failed ({detail}), using Kokoro", file=sys.stderr)

        return kokoro(text), "kokoro"


def reply_path() -> Path:
    """Fresh, sortable file name for one reply.

    @example reply_path()  # /tmp/claude-voice/2026-11-18-184501-3fa2.mp3
    """
    stamp = time.strftime("%Y-%m-%d-%H%M%S")

    return REPLIES / f"{stamp}-{secrets.token_hex(2)}.mp3"


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        sys.exit("voice: nothing to say")

    started = time.time()
    audio, engine = speak(text)

    REPLIES.mkdir(parents=True, exist_ok=True)
    target = reply_path()
    target.write_bytes(audio)
    target.with_suffix(".txt").write_text(text)

    print(target)
    print(f"voice: {engine}, {len(text)} characters in {time.time() - started:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
