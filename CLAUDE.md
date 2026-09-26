## AI work

- Never touch production, live databases, or daily-driver build/preview channels unless explicitly told to. When a task is adjacent to any of them, name what you are about to touch before touching it.
- If the user names a model, use the latest version of that model family for the work they describe. "Use Opus" means the latest Opus. This applies to the main session, subagents, and any tool that takes a model parameter.
- When a step doesn't need my input, keep going. Put status notes in the same message as your next action. Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository.

## Visual and design work

- Make UI, layout, and copy changes directly. Create mocks only when explicitly requested.
- Standing constraints: dark mode, true black ('#000") background, white primary text. Information-dense, no decorative card/pill chrome, no light-gray subtitle lines above sections. Minimal copy. No em dashes.
- No sloppy UX work that looks like it belongs in 2003, not even in POCs. I expect polished, well executed UX experiences that feel native.
- Avoid continuously repainting CSS animations (pulse, shimmer, blur, spinners); they peg the GPU high-refresh displays.

## Coding preferences

Code should be named pragmatically and broken down in logical colocated chunks, with space to breathe. If your code looks like a Python or Java dev wrote it, it is bad code. In any language, we strive for visual readability and less cognitive load - the artisan style Laravel or Elixir would be proud of.

We prefer simplistic implementations of well-known design patterns, as you can often get all the benefits without the OOP overhead.

This usually means writing simple, flat, and functional code, namespacing and colocating related concepts.

- Prefer simple repetitive statements over magic, generation and loops.
- Typesafety is useful, so take advantage of it.
- Inferred types are better than annotations. `any` is the enemy.
- Avoid one-line functions that are just casting wrappers.
- Proactively remove unused code, tests and dependencies, we don't want to leave dead code around unless we have a good reason for it (fx. public api or future plans)
- Don't run production build commands unless asked. Dev servers are fine, see below.

### Dev servers

You may start dev servers. Other worktrees and agents share this machine, so check before you start and clean up when you are done.

- Before starting, look for a server this worktree already runs and reuse it. `ss -ltnp` lists listeners; `readlink /proc/<pid>/cwd` shows which worktree owns one.
- If the default port is taken by another worktree, pick a free port with the project's `--port` flag or `PORT` env var.
- If changing the port needs more than that (monorepos with ports wired through several configs), stop and ask. Say why you need the server, then offer three options: change the config, kill the other worktree's process, or skip the dev server.
- Start servers only with your harness's own background option (e.g. `run_in_background`), so the process dies with your session. Never detach it: no `nohup`, `setsid`, `disown`, trailing `&`, `tmux`, `screen` or `pm2`. A detached server outlives the thread and nobody cleans it up.
- Every server gets a `timeout` TTL, as a backstop in case the harness doesn't kill it:
  - Temporary (a screenshot, a quick check): `timeout 5m bun run dev --port 3001`. Kill it as soon as you have what you need.
  - Long-lived (testing, iterating, brainstorming with me): `timeout 30m bun run dev --port 3001`. Restart it the same way if it expires while still needed.
- When the work ends with a PR, kill every server you started.

### Keep It Simple, Stupid

- Actively search for and suggest code-judo moves, simplify and remove the problem from the equasion, rather than solving it at a cost of extra complexity.
- How often does this actually happen, for the people who will actually use this?
- What happens if we do nothing? An error message shown to the user is usually an acceptable outcome. Silent corruption is not.
- Would a senior dev who owns this feature bother, or would they say "if it fails we show an error, boo hoo"?

### Testing

You are allowed and encouraged to run test/lint/typecheck scripts to validate your work. You are also encouraged to use the browser for development on Storybook or the dev server. Please attach screenshots or videos when you want to show the user how your implementation looks.

Stop yourself from spamming unit tests:

- Only cover functions with unit tests if they actually contain business logic.
- Avoid overtesting and prefer type safety and static checks over unit tests.
- Skip compiler or linter guarantees, trivial forwarding, and assertions that merely repeat mock values or implementation details.
- Test should only cover requirements, observed bugs, or documented behavior. Do not invent hypothetical requirements or edge cases to justify coverage.
- Slim down or remove existing unit tests that exhibit these problems when you see them.

### Code comments

- Do not make inline-comments. If you make or see an inline-comment, it signals that the code is not clear enough. Fix the code instead. Inline comments are a bad smell. If the code isn't telling a story on its own, it means you failed to write good, readable, visually structured code.
- Function and Module comments are the bomb. Add or update JSDoc for every exported (or non-trivial private) function, specify inputs and outputs:
  1. Headline line - explains the purpose/intent in under 100 characters
  2. (optional, rare) 1 short paragraph, max 250 characters - concisely describe complexity or side effects or edge cases
  3. @example - short 1-line usage examples (e.g., `myFunc(); // false`)), especially important for pure functions
- Your comments must not have references to other files or concepts, they must be self-standing and understandable on their own.

## Browser access

Default: `agent-browser`, which runs on this machine. Use it for all browser work,
including screenshots and videos you attach to your replies.

Use the T3 Code `preview_*` tools only when the user explicitly asks for a preview
or asks you to share the screen. Wanting to show the user a result is not a request
for preview.

The `preview_*` tools are listed even when no client is attached. Only when the user
asked for preview, call `preview_status` first. No answer within 10s means no client
is attached: tell the user and use `agent-browser` instead.

When delegating browser work to a subagent, tell it to use `agent-browser`, unless
the user asked for preview.

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
