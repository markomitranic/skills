---
name: voice
description: Use when the user asks you to answer with voice messages, or invokes /voice. Keep answering with voice for as long as the conversation is active.
---

# Voice

The user listens to your final reply as well as reading it. Long voice notes are dry, and nobody
wants to listen to verbose ones, so the voice note is a significantly shorter, succinct spoken
version of the reply. A speech engine reads it literally. The written reply stays as it would be
without this skill.

Generate the audio. The script needs `uv`. It speaks with ElevenLabs when `ELEVENLABS_API_KEY` or
`~/.config/claude-voice/elevenlabs-key` holds an API key, and otherwise falls back to the local
Kokoro voice, which needs `ffmpeg` and downloads its model (about 350 MB) on first use. It prints
the MP3 path:

```bash
~/.claude/skills/voice/speak.py <<'EOF'
<voice note>
EOF
```

End the final reply with the embed, after a blank line, so the player sits right where the user
stops reading:

```markdown
![Listen](<mp3 path>)
```

If the script fails, send the reply without audio and say so in one line. When the user turns
voice off, stop until they turn it back on.
