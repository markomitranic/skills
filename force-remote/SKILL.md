---
name: force-remote
description: Spin up a fresh Claude Code instance with --remote-control in a new Terminal window on macOS, so the user can attach to it from the Claude phone/web app. Use whenever the user says "force-remote", "/force-remote", "spin up a remote claude", "start a new remote session", "I need a new chat I can connect to from my phone", or any variant of wanting a fresh remote-controllable Claude session running on their desktop. Also use proactively when the user mentions the remote app doesn't have a "new chat" command.
---

# force-remote

Start a fresh `claude --remote-control` session in a new Terminal window so the user can attach to it from the Claude phone or web app.

## Why this exists

The Claude phone/web app can **attach** to existing remote-controllable Claude Code sessions but cannot **create** new ones. The user occasionally needs a way to spawn a fresh session on their desktop that the remote app can then pick up. This skill automates that — picking a sensible session name, choosing a working directory, opening the right kind of process so it actually starts, and reporting back so the user can verify it's live before they walk away from the desk.

## How it works (load-bearing — read before deviating)

`claude --remote-control NAME` requires a real PTY. Two obvious-looking approaches fail:

- **`nohup claude --remote-control NAME &` / backgrounded with `&`** — claude sees no TTY on stdin and silently degrades to `--print` mode, then dies with: `Input must be provided either through stdin or as a prompt argument when using --print`. The session never registers.
- **`osascript -e 'tell application "Terminal" to do script "..."'`** — frequently times out with AppleEvent error `-1712`, especially if Terminal.app isn't already foregrounded. Even when it works it's slow.

The reliable path: write a temp `.command` file, `chmod +x` it, and `open` it. macOS Launch Services treats `.command` files as Terminal-launchable, opens a fresh window with a real PTY, and runs the script inside.

The bundled helper `scripts/spawn.sh` does this for you and handles the edge cases (macOS-only check, `claude` binary path resolution, duplicate-name check, PID verification). Prefer it over inlining the bash unless the user wants something custom.

## Workflow

### 1. Pick a session name

Order of preference:

1. **Explicit name from the user.** If they said "call it `foo`" or passed an argument, use it verbatim.
2. **Derive from context.** Strong defaults:
   - Current git branch — `git rev-parse --abbrev-ref HEAD` (slugify if it has slashes).
   - Current task being worked on — e.g., a PR number, a Jira key, or a short descriptor from recent conversation.
3. **Ask.** If you can't derive a meaningful name from context, ask the user with one short question. Don't invent generic names like `claude-remote-1` — names show up in the remote app picker and the user will be looking for something recognizable.

### 2. Pick a working directory

Default to the parent session's `cwd`. If the user mentioned a different project, switch to that path. The working directory matters because the spawned session reads `CLAUDE.md`, `.mcp.json`, and settings from there.

### 3. Check for duplicates

```bash
pgrep -af 'claude --remote-control' | grep -- "<chosen-name>"
```

If a session with that name is already running, surface the PID and ask whether the user wants a new one anyway (different name) or to attach to the existing one. Multiple identically-named sessions in the remote app picker are confusing.

### 4. Spawn it

Run the bundled helper:

```bash
bash <skill-dir>/scripts/spawn.sh "<session-name>" "<working-directory>"
```

The script writes a temp `.command` file, opens it (which spawns a new Terminal window with a real PTY), waits a few seconds, then verifies via `pgrep` that the session actually started. It prints `spawned: pid=<PID> name=<NAME> cwd=<DIR>` on success, or a warning if no process was detected.

### 5. Brief the user on what's next

After successful spawn, tell the user:

- **Where to attach**: the Claude phone or web app — look for a session named `<session-name>` in the picker.
- **The session is fresh** — it has no memory of this conversation. It only knows the codebase via `CLAUDE.md` and any settings/skills available in that working directory.
- **Suggest a one-line brief** they can paste when they connect, derived from current context. Examples:
  - *"I'm continuing RFC-001 PR 3 follow-up — PR #741 is open, awaiting human review."*
  - *"Working on the Keycloak migration on branch `feat/keycloak-rollout`. We're mid-investigation on token refresh."*
  - The brief should pick up where the parent session is roughly. One sentence is enough.
- **Lifecycle**: the new session runs in its own Terminal window. Closing the parent Claude session doesn't kill it. To shut it down, the user types `/exit` in the remote app or closes that Terminal window.

## Common failure modes

- **`claude` not found by the spawned shell.** `.command` files run a non-login shell that may not source `~/.zshrc`, so PATH can differ from the parent. The bundled script resolves `claude`'s absolute path before writing the temp file, which sidesteps this. If you inline your own version, use `command -v claude` and bake the absolute path in.
- **Terminal.app not the user's default terminal.** `open <.command>` routes to whichever app owns the `.command` extension — usually Terminal. iTerm2 users can right-click "Open With..." once to remap, but that's a system-settings concern, not something to fix per-spawn.
- **Stale session with the same name.** Step 3 covers this — always check before spawning.
- **Permissions / Gatekeeper warnings.** If the user runs this for the first time, macOS may prompt "Allow Terminal to open .command files from /tmp?". A normal one-time approval — surface this if the spawn appears to hang.

## What NOT to do

- Don't `nohup claude --remote-control NAME &` or `claude --remote-control NAME &` — `--print`-mode fallback (see "How it works").
- Don't `osascript ... do script` — flaky, slow, AppleEvent timeouts.
- Don't drop into `--print` mode and pretend it's the same — it's a one-shot non-interactive mode, not a remote-controllable session.
- Don't tell the user to type `! claude --remote-control NAME` themselves — that runs inside the parent Claude session and blocks it.
- Don't run formal eval loops "just to be safe" — this is a deterministic spawn, not a generative task. Either the new Terminal window appears with claude running or it doesn't.
