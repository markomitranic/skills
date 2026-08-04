#!/bin/sh
# Copies the global CLAUDE.md into the repo root, called by every hook in this directory.
repo_root=$(git rev-parse --show-toplevel)
cp -f "$HOME/.claude/CLAUDE.md" "$repo_root/CLAUDE.md"
