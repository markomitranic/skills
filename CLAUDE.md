## Tone of voice

> **IMPORTANT!!!** Writing style rules live in the `unslop` skill.  
> YOU MUST APPLY IT TO everything you write for me - chat, PRs, Jira tickets, reports, code, document whatever.  
> ALWAYS LOAD THE UNSLOP SKILL! DO NOT FORGET THIS RULE!

- Keep things simple. Channel "YAGNI" energy and help me find ways to simplify problems.
- Don't be reluctant to propose bold ideas or change of direction, if they can meaningfully benefit our work.
- A question is a request for an answer, not for changes. If I ask you a question, don't rush into implementation, instead, research it and answer - i usually just want your critical opinion.

## Coding preferences

Code should be named pragmatically and broken down in logical colocated chunks, with space to breathe. If your  code looks like a Python or Java dev wrote it, it is bad code. In any language, we strive for visual readability and less cognitive load - the artisan style Laravel or Elixir would be proud of.

We prefer simplistic implementations of well-known design patterns, as you can often get all the benefits without the OOP overhead.

This usually means writing simple, flat, and functional code, namespacing and colocating related concepts.

- Typesafety is useful, so take advantage of it.
- Complexity belongs at the adapter boundary, orchestration stays pure, UI stays dumb.
- Inferred types are better than annotations. `any` is the enemy.
- Tests are great, but endless smoke tests, or exhaustive tests, or "regression tests" for feature deletions etc are overwhelming, much less good. Tests should be small and focused, not filler slop.
- Avoid one-line functions that are just casting wrappers.
- Proactively remove unused code and dependencies, we don't want to leave dead code around unless we have a good reason for it (fx. public api or future plans)
- Don't run dev server or build commands (e.g., `bun run dev`) - assume it's already running or ask.

### A word on code comments

- Comments are a great way to explain how a thing is used, but please don't make inline-comments. If you make or see an inline-comment, it signals that the code is not clear enough. Fix the code instead.
- Keep comments up to date, when making changes, its important to keep things in sync.
- Function and module comments are the bomb. Add or update JSDoc for every exported (or non-trivial private) function, specify inputs and outputs:
  1. Single short line - explains the purpose
  2. (optional) short paragraphs - concisely describe usage, or complexity or  side effects or edge cases
  3. @example - short 1-line usage examples (e.g., `myFunc(); // false`))

## Rules for Teams and Sub-Agents

Match ceremony to the task, don't spawn subagents or multi-agent panels for work that can be finished in a single pass.

Computer use and Browser use MUST be delegated to Sonnet sub-agents.

Never use Fable in sub-agents or teams! Always pick Opus or Sonnet for subagent in workflows.

- Opus is good for most tasks that require taste and creativity - reasoning, thinking, design, decisions, critique, debugging.
- Sonnet is much less expensive, only good for tightly specced mechanical grunt-work - searching, reading, running commands, parsing files, computer use, mechanical operations.

