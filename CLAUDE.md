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

- Do not make inline-comments. If you make or see an inline-comment, it signals that the code is not clear enough. Fix the code instead. Inline comments are a bad smell.
- Function and Module comments are the bomb.  Add or update JSDoc for every exported (or non-trivial private) function, specify inputs and outputs:
  1. Single short line - explains the purpose/intent
  2. (optional, rare) 1 short paragraph, max 120 words - concisely describe complexity or  side effects or edge cases
  3. @example - short 1-line usage examples (e.g., `myFunc(); // false`)), especially important for pure functions

## Rules for Teams and Sub-Agents

Computer use and Browser use can ONLY EVER BE RAN BY GPT Terra model. If you are not GPT you must spin up a GPT Terra sub-agent.

Never use Fable in sub-agents or teams! Always pick Opus or Sonnet for subagent in workflows.

- Opus is good for most tasks that require taste and creativity - reasoning, thinking, design, decisions, critique, debugging.
- Sonnet is much less expensive, only good for tightly specced mechanical grunt-work - searching, reading, running commands, parsing files, computer use, mechanical operations.

