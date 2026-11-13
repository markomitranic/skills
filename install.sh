#!/bin/sh
# Bootstraps this repo into Claude Code: hooks, symlink, and a first sync.
# Safe to re-run; every step is idempotent.
set -eu

repo_root=$(cd "$(dirname "$0")" && pwd)
skills_link="$HOME/.claude/skills"

git -C "$repo_root" config core.hooksPath .githooks
echo "🪝 Git hooks enabled — global config now syncs on commit, checkout, merge and push."

if [ "$repo_root" = "$skills_link" ]; then
  echo "🔗 Repo already lives at $skills_link, no symlink needed."
elif [ -L "$skills_link" ]; then
  ln -sfn "$repo_root" "$skills_link"
  echo "🔗 Symlink repointed: $skills_link -> $repo_root"
elif [ -e "$skills_link" ]; then
  echo "⚠️  $skills_link exists and is not a symlink. Move it aside and re-run." >&2
  exit 1
else
  mkdir -p "$HOME/.claude"
  ln -s "$repo_root" "$skills_link"
  echo "🔗 Symlinked $skills_link -> $repo_root"
fi

"$repo_root/.githooks/sync-global.sh"

echo "✅ Done. Skills load on the next session or after /clear."
