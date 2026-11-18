#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["aiohttp>=3.10", "faster-whisper>=1.1", "numpy"]
# ///
"""Voice call into a T3 thread: speech is transcribed here, posted to the thread, voice notes play back.

Runs only as a descendant of the T3 server and dies with its parent. Ends itself after two minutes of
silence (time spent waiting on the agent doesn't count) or thirty minutes in total. Prints the call
link once the tailnet HTTPS address is up, and the reason when the call ends.

@example call.py --thread "$T3CODE_THREAD_ID"  # CALL https://host.tailnet.ts.net:8451/?t=…
"""

import argparse
import asyncio
import ctypes
import json
import os
import re
import secrets
import signal
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from aiohttp import WSMsgType, web

IDLE_LIMIT = 120
IDLE_WARNING = 90
CALL_LIMIT = 30 * 60
CALL_WARNING = CALL_LIMIT - 60

HTTPS_PORTS = range(8451, 8480)
PAGE = Path(__file__).with_name("call.html")
VOICE_DIR = Path(tempfile.gettempdir()) / "claude-voice"
VOICE_EMBED = re.compile(r"!\[[^\]]*\]\(([^)\s]+\.mp3)\)")
AUDIO_NAME = re.compile(r"^[\w.-]+\.mp3$")

NOISE_PHRASES = {"you", "thank you", "thanks", "thanks for watching", "bye", "okay", "uh", "um", "hmm"}
PR_SET_PDEATHSIG = 1


@dataclass
class Call:
    t3: str
    t3_pid: int
    thread: str
    title: str
    token: str
    whisper: asyncio.Task
    started: float = field(default_factory=time.monotonic)
    last_activity: float = field(default_factory=time.monotonic)
    turns: int = 0
    speaking: bool = False
    playing: bool = False
    warned_idle: bool = False
    warned_limit: bool = False
    socket: web.WebSocketResponse | None = None
    outbox: list = field(default_factory=list)
    ended: asyncio.Future = field(default_factory=lambda: asyncio.get_running_loop().create_future())



def ancestors(pid: int):
    """Yield (pid, argv) for each ancestor of a process, nearest first.

    @example next(ancestors(os.getpid()))  # (4211, ["/bin/bash", "-c", "…"])
    """
    while pid > 1:
        try:
            stat = Path(f"/proc/{pid}/stat").read_text()
            pid = int(stat.rsplit(")", 1)[1].split()[1])
            argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0") if pid > 1 else []
        except OSError:
            return

        if pid <= 1:
            return

        yield pid, [arg.decode(errors="replace") for arg in argv if arg]


def find_t3_server() -> tuple[int, str] | None:
    """Find the `t3 serve` process this one runs under, as (pid, binary).

    @example find_t3_server()  # (1361900, "/home/me/.t3/runtime/versions/0.1.11/t3")
    """
    for pid, argv in ancestors(os.getpid()):
        if len(argv) >= 2 and Path(argv[0]).name == "t3" and argv[1] == "serve":
            return pid, argv[0]

    return None


def die_with_parent() -> None:
    """Ask the kernel to send SIGTERM to this process when its parent dies."""
    ctypes.CDLL(None).prctl(PR_SET_PDEATHSIG, signal.SIGTERM)


def still_under_t3(call: Call) -> bool:
    """True while the original T3 server is alive and still an ancestor of this process."""
    return any(pid == call.t3_pid for pid, _ in ancestors(os.getpid()))



async def run_t3(call_t3: str, *args: str, stdin: str = "") -> tuple[int, str, str]:
    """Run the T3 CLI and return (exit code, stdout, stderr)."""
    process = await asyncio.create_subprocess_exec(
        call_t3, *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await process.communicate(stdin.encode())

    return process.returncode, out.decode(), err.decode().strip()


async def thread_title(t3: str, thread: str) -> str:
    """Title of a thread, or an empty string when T3 can't say.

    @example await thread_title(t3, thread)  # "Checkout headers"
    """
    code, out, _ = await run_t3(t3, "thread", "show", thread, "--messages", "1", "--json")
    if code != 0:
        return ""

    return json.loads(out)["thread"].get("title") or ""


async def ask_thread(call: Call, text: str) -> dict:
    """Post a message to the thread and wait for the agent's run to finish.

    @example await ask_thread(call, "Run the tests")  # {"status": "completed", "reply": "…", "error": None}
    """
    code, out, err = await run_t3(call.t3, "thread", "send", call.thread, "-", "--wait", "--json", stdin=text)

    try:
        return json.loads(out)
    except ValueError:
        return {"status": "failed", "reply": None, "error": err or f"t3 exited with {code}"}


def voice_note(reply: str | None) -> tuple[str, str] | None:
    """Find the voice note at the end of a reply, as (audio file name, caption).

    @example voice_note("Done.\\n\\n![Listen](/tmp/claude-voice/a.mp3)")  # ("a.mp3", "Done, all green.")
    """
    embeds = VOICE_EMBED.findall(reply or "")
    if not embeds:
        return None

    audio = Path(embeds[-1])
    if audio.parent.resolve() != VOICE_DIR.resolve() or not audio.exists():
        return None

    caption = audio.with_suffix(".txt")

    return audio.name, caption.read_text().strip() if caption.exists() else ""



def load_whisper(name: str):
    """Load a faster-whisper model for CPU inference; downloads it on first use."""
    from faster_whisper import WhisperModel

    return WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)


def transcribe(model, pcm: bytes) -> str:
    """Turn 16 kHz mono 16-bit PCM into text, skipping segments Whisper thinks are not speech.

    @example transcribe(model, pcm)  # "Can you check why the header test fails?"
    """
    audio = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
    segments, _ = model.transcribe(audio, beam_size=1, vad_filter=True, condition_on_previous_text=False)

    return " ".join(segment.text.strip() for segment in segments if segment.no_speech_prob < 0.6).strip()


def is_noise(text: str) -> bool:
    """True for empty transcripts and the phrases Whisper tends to invent from background noise.

    @example is_noise("Thank you.")  # True
    """
    words = re.sub(r"[^a-z' ]", "", text.lower()).strip()

    return len(words) < 2 or words in NOISE_PHRASES



async def send(call: Call, **event) -> None:
    """Send an event to the phone, or keep it until the phone reconnects."""
    if call.socket is None or call.socket.closed:
        call.outbox.append(event)
        return

    await call.socket.send_json(event)


async def send_phase(call: Call) -> None:
    """Tell the phone whether the agent is working on something."""
    await send(call, type="phase", phase="working" if call.turns else "listening")


def log(message: str) -> None:
    """Print a timestamped line to the call's output, which the agent reads when the call ends."""
    print(f"{time.strftime('%H:%M:%S')} {message}", flush=True)


def touch(call: Call) -> None:
    """Reset the silence timer."""
    call.last_activity = time.monotonic()
    call.warned_idle = False


def end(call: Call, reason: str) -> None:
    """End the call once, with a reason for the phone and the agent."""
    if not call.ended.done():
        call.ended.set_result(reason)


async def handle_utterance(call: Call, pcm: bytes) -> None:
    """Transcribe one utterance, post it to the thread, and deliver the agent's voice note."""
    call.turns += 1
    await send_phase(call)

    try:
        text = await asyncio.to_thread(transcribe, await call.whisper, pcm)
        if is_noise(text):
            log(f"dropped as noise: {text!r}")
            await send(call, type="dropped")
            return

        log(f"heard: {text}")
        await send(call, type="heard", text=text)
        result = await ask_thread(call, text)
        await deliver(call, result)
    except Exception as error:
        log(f"failed: {error!r}")
        await send(call, type="problem", message=f"Something broke: {error}")
    finally:
        call.turns -= 1
        touch(call)
        await send_phase(call)


async def deliver(call: Call, result: dict) -> None:
    """Pass the agent's reply to the phone as a voice note, or explain why there isn't one."""
    status = result.get("status")
    log(f"run {status}")

    if status == "waiting":
        await send(call, type="problem", message="Claude is waiting for an answer in T3.")
        return

    if status != "completed":
        await send(call, type="problem", message=result.get("error") or f"The run ended: {status}.")
        return

    note = voice_note(result.get("reply"))
    if note is None:
        await send(call, type="problem", message="That reply had no voice note. It's in T3.")
        return

    audio, caption = note
    await send(call, type="reply", audio=f"/audio/{audio}?t={call.token}", caption=caption)


async def watch(call: Call) -> None:
    """Enforce the silence and length limits, and end the call if T3 goes away."""
    while not call.ended.done():
        await asyncio.sleep(1)
        now = time.monotonic()

        if not still_under_t3(call):
            end(call, "T3 stopped")
            return

        if call.turns or call.speaking or call.playing:
            touch(call)

        idle = now - call.last_activity
        length = now - call.started

        if length >= CALL_LIMIT:
            end(call, "The 30 minute limit")
        elif idle >= IDLE_LIMIT:
            end(call, "Two minutes of silence")
        elif length >= CALL_WARNING and not call.warned_limit:
            call.warned_limit = True
            await send(call, type="warning", message="One minute left on this call.")
        elif idle >= IDLE_WARNING and not call.warned_idle:
            call.warned_idle = True
            await send(call, type="warning", message="Hanging up in 30 seconds unless you say something.")



def authorized(call: Call, request: web.Request) -> bool:
    return secrets.compare_digest(request.query.get("t", ""), call.token)


async def page(request: web.Request) -> web.StreamResponse:
    call = request.app["call"]
    if not authorized(call, request):
        raise web.HTTPNotFound()

    return web.FileResponse(PAGE, headers={"Cache-Control": "no-store"})


async def audio(request: web.Request) -> web.StreamResponse:
    call = request.app["call"]
    name = request.match_info["name"]
    if not authorized(call, request) or not AUDIO_NAME.match(name) or not (VOICE_DIR / name).exists():
        raise web.HTTPNotFound()

    log(f"phone fetched {name}")

    return web.FileResponse(VOICE_DIR / name)


async def hangup(request: web.Request) -> web.Response:
    call = request.app["call"]
    if not authorized(call, request):
        raise web.HTTPNotFound()

    end(call, "You declined")

    return web.Response(status=204)


async def socket(request: web.Request) -> web.StreamResponse:
    """One live connection per call; a reconnect replaces the old one and gets missed events."""
    call = request.app["call"]
    if not authorized(call, request):
        raise web.HTTPNotFound()

    ws = web.WebSocketResponse(heartbeat=15, max_msg_size=32 * 1024 * 1024)
    await ws.prepare(request)

    if call.socket is not None and not call.socket.closed:
        await call.socket.close()

    call.socket = ws
    log("phone connected")
    touch(call)
    await ws.send_json({"type": "hello", "title": call.title})
    await send_phase(call)

    while call.outbox:
        await ws.send_json(call.outbox.pop(0))

    async for message in ws:
        if message.type == WSMsgType.BINARY:
            call.speaking = False
            asyncio.create_task(handle_utterance(call, message.data))
            continue

        if message.type != WSMsgType.TEXT:
            continue

        event = json.loads(message.data)
        match event.get("type"):
            case "ignored":
                call.speaking = False
                log(f"ignored quiet speech, level {event['level']:.3f}, background {event['floor']:.3f}")
            case "level":
                log(f"speech level {event['level']:.3f}, background {event['floor']:.3f}")
            case "speaking":
                call.speaking = True
            case "quiet":
                call.speaking = False
            case "playing":
                call.playing = True
            case "played":
                call.playing = False
            case "hangup":
                end(call, "You hung up")

        touch(call)

    if call.socket is ws:
        log("phone disconnected")
        call.speaking = call.playing = False

    return ws



async def publish(local_port: int) -> tuple[asyncio.subprocess.Process, str]:
    """Expose the local server on the tailnet over HTTPS, in the foreground, on the first free port.

    @example await publish(41234)  # (process, "https://host.tailnet.ts.net:8451")
    """
    for https_port in HTTPS_PORTS:
        process = await asyncio.create_subprocess_exec(
            "tailscale", "serve", f"--https={https_port}", f"http://127.0.0.1:{local_port}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            preexec_fn=die_with_parent,
        )
        url = await first_url(process)
        if url:
            asyncio.create_task(process.stdout.read())
            return process, url.rstrip("/")

        await process.wait()

    sys.exit("call: no free tailnet HTTPS port between 8451 and 8479")


async def first_url(process: asyncio.subprocess.Process) -> str | None:
    """Read `tailscale serve` output until it prints its URL, or give up when it exits or stalls."""
    try:
        async with asyncio.timeout(15):
            async for raw in process.stdout:
                line = raw.decode().strip()
                if line.startswith("https://"):
                    return line
    except TimeoutError:
        process.terminate()

    return None



async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--thread", default=os.environ.get("T3CODE_THREAD_ID"))
    parser.add_argument("--model", default="small.en", help="faster-whisper model name")
    args = parser.parse_args()

    if not args.thread:
        sys.exit("call: no thread; pass --thread or run it from a T3 thread")

    server = find_t3_server()
    if server is None:
        sys.exit("call: must run under the T3 server, started from a T3 thread")

    die_with_parent()
    t3_pid, t3 = server

    call = Call(
        t3=t3,
        t3_pid=t3_pid,
        thread=args.thread,
        title=await thread_title(t3, args.thread),
        token=secrets.token_urlsafe(18),
        whisper=asyncio.create_task(asyncio.to_thread(load_whisper, args.model)),
    )

    loop = asyncio.get_running_loop()
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        loop.add_signal_handler(signum, end, call, "Stopped")

    app = web.Application()
    app["call"] = call
    app.add_routes([
        web.get("/", page),
        web.get("/ws", socket),
        web.get("/audio/{name}", audio),
        web.post("/hangup", hangup),
    ])

    runner = web.AppRunner(app, handle_signals=False)
    await runner.setup()
    await web.TCPSite(runner, "127.0.0.1", 0).start()
    local_port = runner.addresses[0][1]

    tailscale, url = await publish(local_port)
    print(f"CALL {url}/?t={call.token}", flush=True)

    watcher = asyncio.create_task(watch(call))
    reason = await call.ended

    await send(call, type="ended", reason=reason)
    if call.socket is not None:
        await call.socket.close()

    watcher.cancel()
    tailscale.terminate()
    await tailscale.wait()
    await runner.cleanup()

    print(f"CALL ENDED: {reason}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
