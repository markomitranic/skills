---
name: voice
description: Always on. Attach a voice note to every final reply to the user. Skip it when the user has turned voice off, or when your reply goes to another agent.
---

# Voice

The user listens to your final reply as well as reading it. Long voice notes are dry, and nobody
wants to listen to verbose ones, so the voice note is a significantly shorter, succinct spoken
version of the reply. A speech engine reads it literally. The written reply stays as it would be
without this skill.

Generate the audio with the local Kokoro voice. The script needs `uv` and `ffmpeg` on the PATH,
installs its own Python packages, and downloads the voice model (about 350 MB) on first run. It
prints the MP3 path:

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
