# Claude Skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. Each subfolder is a self-contained skill defined by a `SKILL.md` with frontmatter (`name`, `description`) that Claude auto-loads when the description matches the user's intent.

Alongside the skills, `output-styles/` holds custom output styles. An output style is appended to Claude Code's system prompt for every turn, so it fits rules that must apply to everything Claude writes rather than to one task.

## Output styles

`**output-styles/unslop.md`.** Writing style rules, applied to every response. Turn it on with `/config` → Output style → `unslop`, or set it in `~/.claude/settings.json`:

```json
"outputStyle": "unslop"
```

It takes effect on `/clear` or the next session, since Claude Code reads the system prompt once at startup. Note that output styles apply to the main conversation only, not to subagents.

> **💡 Pro tip: hard-enforce it with a hook.** Claude drifts back to its default voice on long conversations. Anthropic solves this by having a `turnReminder` hook that  re-injects their rules on every turn: *"Concise output style is active. Be concise: lead with the result, skip preamble and narration, keep only what the user needs."*
>
> Custom styles have no such luxury, but it is possible to register our own hook to constantly pester the agent to follow the rules.

## Other tooling

- `**status-line/**` — Bash script that renders the Claude Code status line (branch, model, context window usage with rot warnings, session cost). Wire it up in `~/.claude/settings.json`:
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
├── [[ORCA_RICH_MD:151c3b64cd8ca0b60383e855cd1dbc12:inline-html:%3Cskill-name%3E]]/
│   └── SKILL.md
└── output-styles/
    └── [[ORCA_RICH_MD:151c3b64cd8ca0b60383e855cd1dbc12:inline-html:%3Cstyle-name%3E]].md
```

Claude Code reads output styles from `~/.claude/output-styles/`, not from this folder, so the git hooks in `.githooks/` copy `output-styles/*.md` out on every commit, checkout, merge and push. Same trick they already use for `CLAUDE.md`.

The `SKILL.md` frontmatter `description` is what Claude matches against to decide whether to invoke the skill — keep it specific and trigger-rich.