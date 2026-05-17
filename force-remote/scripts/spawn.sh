#!/bin/bash
# Spawn a `claude --remote-control` session in a fresh Terminal window.
#
# Usage: spawn.sh <session-name> [working-directory]
#
# Why this dance:
#   `claude --remote-control` needs a real PTY. Backgrounding it (`nohup ... &`,
#   `... & disown`) makes claude fall into --print mode and die with
#   "Input must be provided either through stdin or as a prompt argument".
#   `osascript tell Terminal do script ...` times out with AppleEvent -1712.
#   Writing a `.command` file and `open`-ing it makes macOS Launch Services
#   open a fresh Terminal window with a real PTY and run the script inside.
#   That works reliably.

set -euo pipefail

NAME="${1:?usage: spawn.sh <session-name> [working-directory]}"
CWD="${2:-$(pwd)}"

if [[ "$(uname)" != "Darwin" ]]; then
  echo "force-remote: macOS only (uname=$(uname))" >&2
  exit 2
fi

CLAUDE_BIN="$(command -v claude || true)"
if [[ -z "$CLAUDE_BIN" ]]; then
  echo "force-remote: 'claude' not found on PATH" >&2
  exit 3
fi

if [[ ! -d "$CWD" ]]; then
  echo "force-remote: working directory does not exist: $CWD" >&2
  exit 4
fi

CMD_FILE="$(mktemp -t force-remote).command"
cat > "$CMD_FILE" <<EOF
#!/bin/bash
cd "$CWD"
exec "$CLAUDE_BIN" --remote-control '$NAME'
EOF
chmod +x "$CMD_FILE"

open "$CMD_FILE"

# Give the new Terminal a moment to start the child process.
sleep 3

# Verify. Match on the full flag value so we don't catch other claude invocations.
PID="$(pgrep -af "claude --remote-control $NAME" | grep -v pgrep | awk '{print $1}' | head -1 || true)"

if [[ -n "$PID" ]]; then
  echo "spawned: pid=$PID name=$NAME cwd=$CWD command-file=$CMD_FILE"
  exit 0
else
  echo "force-remote: no claude --remote-control process detected after 3s." >&2
  echo "force-remote: check the new Terminal window for errors (PATH? Gatekeeper prompt?)." >&2
  echo "force-remote: command-file kept for inspection: $CMD_FILE" >&2
  exit 5
fi
