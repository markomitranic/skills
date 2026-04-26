# Claude Skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. Each subfolder is a self-contained skill defined by a `SKILL.md` with frontmatter (`name`, `description`) that Claude auto-loads when the description matches the user's intent.

## Skills

- **`ddd/`** — Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms.
- **`grill-me/`** — Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree.
- **`pr-triage/`** — Walk through unresolved review comments on the current branch's PR one at a time, separating real bugs from confident-sounding nonsense (especially useful with Greptile/Codex/Coderabbit).
- **`to-prd/`** — Turn the current conversation context into a PRD and submit it as a GitHub issue.

## Layout

This repo lives at `~/.claude/skills/`, which is where Claude Code looks for user-level skills. Each skill is a folder containing at least a `SKILL.md`:

```
skills/
├── <skill-name>/
│   └── SKILL.md
```

The `SKILL.md` frontmatter `description` is what Claude matches against to decide whether to invoke the skill — keep it specific and trigger-rich.

## Adding a skill

1. Create a new folder: `mkdir ~/.claude/skills/<skill-name>`
2. Add `SKILL.md` with frontmatter:
   ```markdown
   ---
   name: <skill-name>
   description: <when to use this skill, with concrete trigger phrases>
   ---

   <skill body — instructions Claude follows when invoked>
   ```
3. Skills become available in new Claude Code sessions automatically.
