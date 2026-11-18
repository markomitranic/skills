---
name: call
description: Start a voice call with the user in this thread. Only when the user types /call.
disable-model-invocation: true
---

# Call

The user wants to talk to you hands-free. They get a link that opens a call screen on their phone.
Their speech is transcribed on this machine and arrives in this thread as normal messages, and
each of your replies plays back to them as a voice note. The thread stays the record; the call
only carries voice.

1. Load the `voice` skill with the Skill tool, so every reply during the call has a voice note.
2. Start the call server with your harness's background option, never detached:

   ```bash
   ~/.claude/skills/call/call.py
   ```

   It needs `uv` and Tailscale with HTTPS certificates, reads the thread from `T3CODE_THREAD_ID`,
   and downloads a Whisper model (about 500 MB) on first run. It refuses to run outside T3, dies
   with its parent, and ends itself after two minutes of silence or thirty minutes in total.
3. Read its output until the `CALL <url>` line, then reply with a short message that says Claude
   is calling and links the URL as `[Answer](<url>)`.

When the server exits, it prints why the call ended. Carry on in text.
