# Claude Skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. Each subfolder is a self-contained skill defined by a `SKILL.md` with frontmatter (`name`, `description`) that Claude auto-loads when the description matches the user's intent.

## Install

```sh
git clone https://github.com/markomitranic/skills.git ~/skills
~/skills/install.sh
```

`install.sh` symlinks it to `~/.claude/skills`, where Claude Code looks for user-level skills, and to `~/.agents/skills` when Codex is installed.

## Other tooling

- `**status-line/**` — Bash script that renders the Claude Code status line (branch, model, context window usage with rot warnings, session cost). Wire it up in `~/.claude/settings.json`:
  ```json
  "statusLine": {
    "type": "command",
    "command": "~/.claude/skills/status-line/statusline.sh"
  }
  ```

### opencode

Skills and `CLAUDE.md` work with no setup. opencode's global search paths already include `~/.claude/skills/<name>/SKILL.md` and it falls back to `~/.claude/CLAUDE.md` for global instructions.
