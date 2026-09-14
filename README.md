# Claude Skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. Each subfolder is a self-contained skill defined by a `SKILL.md` with frontmatter (`name`, `description`) that Claude auto-loads when the description matches the user's intent.

Alongside the skills, `output-styles/` holds custom output styles. An output style is appended to Claude Code's system prompt for every turn, so it fits rules that must apply to everything Claude writes rather than to one task.

## Install

```sh
git clone https://github.com/markomitranic/skills.git ~/skills
~/skills/install.sh
```

Clone anywhere you like — `install.sh` symlinks it to `~/.claude/skills`, where Claude Code looks for user-level skills, and to `~/.agents/skills` when Codex is installed. Cloning straight to `~/.claude/skills` works too; the script detects that and skips the symlink.

Re-run it any time; every step is idempotent.

## Output styles

`**output-styles/unslop.md`.** Writing style rules, applied to every response. Turn it on with `/config` → Output style → `unslop`, or set it in `~/.claude/settings.json`:

```json
"outputStyle": "unslop"
```

It takes effect on `/clear` or the next session, since Claude Code reads the system prompt once at startup. Note that output styles apply to the main conversation only, not to subagents.

### Which settings file wins

Three files can carry the `outputStyle` key, and the most specific one wins:

```
.claude/settings.local.json   beats   .claude/settings.json   beats   ~/.claude/settings.json
  (this repo, gitignored)             (this repo, committed)          (every project)
```

Picking a style from `/config` writes it to the project's `.claude/settings.local.json`, not to the global file. So a style chosen once inside a repo keeps overriding the global choice in that repo forever, and every other project falls back to Claude's default voice. Put the key in `~/.claude/settings.json` to make it the default everywhere.

When a project answers in the wrong voice, find the key before changing anything:

```bash
grep -rn outputStyle ~/.claude/settings.json .claude/settings*.json
```

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

Claude Code reads user-level skills from `~/.claude/skills/`, which `install.sh` points at this repo. Each skill is a folder containing at least a `SKILL.md`:

```
skills/
├── [[ORCA_RICH_MD:151c3b64cd8ca0b60383e855cd1dbc12:inline-html:%3Cskill-name%3E]]/
│   └── SKILL.md
└── output-styles/
    └── [[ORCA_RICH_MD:151c3b64cd8ca0b60383e855cd1dbc12:inline-html:%3Cstyle-name%3E]].md
```

Claude Code reads output styles from `~/.claude/output-styles/`, not from this folder, so the git hooks in `.githooks/` copy `output-styles/*.md` out on every commit, checkout, merge and push. Same trick they already use for `CLAUDE.md`.

Those hooks need `core.hooksPath` pointed at `.githooks`, and **git never carries that setting across a clone** — it is repo-local config, not tracked content. A fresh clone therefore looks correct and silently syncs nothing. `install.sh` sets it, which is the main reason to run the script rather than just symlinking by hand.

The `SKILL.md` frontmatter `description` is what Claude matches against to decide whether to invoke the skill — keep it specific and trigger-rich.

## Other coding agents

Claude Code is the source of truth: this repo is the skills folder, `CLAUDE.md` is the instructions, `output-styles/` is the voice. Every other agent gets pointed back at those same files.

Codex is the worked example. Three things have to travel, each a different trick:

- **Skills** — Codex reads `~/.agents/skills`, so it gets a symlink to this repo and both agents stay live on one folder.
- **Instructions** — Codex reads `~/.codex/AGENTS.md`, which has no include syntax. `sync-global.sh` copies `CLAUDE.md` into it on every commit, checkout, merge and push.
- **Output style** — Codex has no equivalent concept, so that same sync appends `unslop.md` below the instructions, frontmatter stripped. `~/.codex/AGENTS.md` is generated output; edit the sources instead.

`install.sh` wires all three, and skips the Codex half when `~/.codex` is absent:

```sh
~/skills/install.sh
```

By hand, the same thing:

```sh
mkdir -p ~/.agents
ln -s ~/skills ~/.claude/skills            # Claude Code skills
ln -s ~/skills ~/.agents/skills            # Codex skills
sh ~/skills/.githooks/sync-global.sh       # CLAUDE.md + unslop -> ~/.codex/AGENTS.md
```

### opencode

Skills and `CLAUDE.md` work with no setup. opencode's global search paths already include `~/.claude/skills/<name>/SKILL.md` and it falls back to `~/.claude/CLAUDE.md` for global instructions.

Only the output style needs wiring, since opencode has no equivalent concept:

```diff
  // ~/.config/opencode/opencode.json
  {
    "$schema": "https://opencode.ai/config.json",
+   "instructions": ["~/.claude/skills/output-styles/unslop.md"]
  }
```

> **⚠️ Careful with `AGENTS.md`.** opencode picks the first match per category rather than merging, and `~/.config/opencode/AGENTS.md` beats `~/.claude/CLAUDE.md`. A global `AGENTS.md` silently shadows your `CLAUDE.md`. Leave it absent.
