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

- Function and Module comments are the bomb.  Add or update JSDoc for every exported (or non-trivial private) function, specify inputs and outputs:
  1. Headline line - explains the purpose/intent in under 100 characters
  2. (optional, rare) 1 short paragraph, max 250 characters - concisely describe complexity or  side effects or edge cases
  3. @example - short 1-line usage examples (e.g., `myFunc(); // false`)), especially important for pure functions
- Do not make inline-comments. If you make or see an inline-comment, it signals that the code is not clear enough. Fix the code instead. Inline comments are a bad smell. If the code isn't telling a story on its own, it means you failed to write good, readable, visually structured code.
- Your comments must not have references to other files or concepts, they must be self-standing and understandable on their own.

## Rules for Teams and Sub-Agents

- Never use Fable in sub-agents! Use Opus/Sol instead.
- Computer use and Browser use can ONLY EVER BE RAN BY Sonnet/Terra model. If you are not Sonnet/Terra you must spin up a sub-agent.

## Browser access

Two browser stacks may exist on a machine: the T3 Code `preview_*` tools, which
run in the attached client's browser, and `agent-browser`, which runs on the
machine itself.

1. Does the task require sharing the screen with the human?
2. If yes (or human asked for it) use `preview_*` tools.
3. If no (most tasks), use `agent-browser`.
4. Delegating browser work to a subagent -> explicitly tell it which one to use.

The `preview_*` tools are always listed whether or not a client
is attached, so their presence in the tool list proves nothing. 
You must probe - call `preview_status`. No answer within 10s counts as a no.

### Using Agent Browser

Run `agent-browser skills get core` before the first browser command in a
session. The skills ship with the CLI and are version-matched, so they beat
guessing from `agent-browser --help`.

Export a named session first, or you risk conflicts with other agents:

```sh
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix task)"
```

Core workflow:

1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
3. `agent-browser click @e1` / `fill @e2 "text"` - Interact using refs
4. Re-snapshot after page changes



&nbsp;