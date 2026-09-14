#!/bin/sh
# Copies this repo's global config out to ~/.claude and ~/.codex, called by every hook in this directory.
repo_root=$(git rev-parse --show-toplevel)

# Prints a markdown file without its leading YAML frontmatter block.
strip_frontmatter() {
  awk 'NR == 1 && $0 == "---" { inside = 1; next } inside && $0 == "---" { inside = 0; next } !inside' "$1"
}

cp -f "$repo_root/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
echo "💿 Global CLAUDE.md synced with this version."

mkdir -p "$HOME/.claude/output-styles"
cp -f "$repo_root"/output-styles/*.md "$HOME/.claude/output-styles/"
echo "💿 Global /output-styles/ synced with this version."

if [ -d "$HOME/.codex" ]; then
  {
    cat "$repo_root/CLAUDE.md"
    strip_frontmatter "$repo_root/output-styles/unslop.md"
  } > "$HOME/.codex/AGENTS.md"
  echo "💿 Codex AGENTS.md synced — same rules, unslop style inlined."
fi
