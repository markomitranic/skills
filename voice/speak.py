#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pocket-tts>=4.0", "torch"]
#
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
#
# [tool.uv.sources]
# torch = [{ index = "pytorch-cpu", marker = "sys_platform == 'linux'" }]
# ///
"""Turn a spoken script from stdin into an MP3 with Kyutai's Pocket TTS, and print its path.

Runs locally on the CPU with the built-in Alba voice. The model downloads from Hugging Face on
first use. The script text is saved next to the MP3 with a .txt suffix, for captions. Replies go to
the system temp folder, which the OS clears on its own.

@example echo "Done, the tests pass." | speak.py  # /tmp/claude-voice/2026-11-18-184501-3fa2.mp3
"""

import secrets
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPLIES = Path(tempfile.gettempdir()) / "claude-voice"
VOICE = "alba"


def synthesize(text: str) -> tuple[bytes, int]:
    """Render text to raw float32 PCM with Pocket TTS, as (samples, sample rate).

    @example synthesize("Hi there.")  # (b"\\x00…", 24000)
    """
    from pocket_tts import TTSModel

    model = TTSModel.load_model()
    audio = model.generate_audio(model.get_state_for_audio_prompt(VOICE), text)

    return audio.numpy().astype("float32").tobytes(), model.sample_rate


def encode_mp3(pcm: bytes, rate: int, target: Path) -> None:
    """Pipe raw float32 samples through ffmpeg into a compact mono MP3."""
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-y",
            "-f", "f32le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0",
            "-b:a", "64k", str(target),
        ],
        input=pcm,
        check=True,
    )


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
    pcm, rate = synthesize(text)

    REPLIES.mkdir(parents=True, exist_ok=True)
    target = reply_path()
    encode_mp3(pcm, rate, target)
    target.with_suffix(".txt").write_text(text)

    print(target)
    print(f"voice: {VOICE}, {len(pcm) / 4 / rate:.0f}s of audio in {time.time() - started:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
