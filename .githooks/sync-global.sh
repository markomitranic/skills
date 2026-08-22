#!/bin/sh
# Copies this repo's global config out to ~/.claude, called by every hook in this directory.
repo_root=$(git rev-parse --show-toplevel)

cp -f "$repo_root/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
echo "💿 Global CLAUDE.md synced with this version."

mkdir -p "$HOME/.claude/output-styles"
cp -f "$repo_root"/output-styles/*.md "$HOME/.claude/output-styles/"
echo "💿 Global /output-styles/ synced with this version."