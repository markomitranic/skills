#!/bin/sh
# Copies the repo's CLAUDE.md out to the global ~/.claude/CLAUDE.md, called by every hook in this directory.
repo_root=$(git rev-parse --show-toplevel)
cp -f "$repo_root/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
