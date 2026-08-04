# Claude Skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. Each subfolder is a self-contained skill defined by a `SKILL.md` with frontmatter (`name`, `description`) that Claude auto-loads when the description matches the user's intent.

## Other tooling

- **`status-line/`** — Bash script that renders the Claude Code status line (branch, model, context window usage with rot warnings, session cost). Wire it up in `~/.claude/settings.json`:
  ```json
  "statusLine": {
    "type": "command",
    "command": "~/.claude/skills/status-line/statusline.sh"
  }
  ```

## Layout

This repo lives at `~/.claude/skills/`, which is where Claude Code looks for user-level skills. Each skill is a folder containing at least a `SKILL.md`:

```
skills/
├── <skill-name>/
│   └── SKILL.md
```

The `SKILL.md` frontmatter `description` is what Claude matches against to decide whether to invoke the skill — keep it specific and trigger-rich.