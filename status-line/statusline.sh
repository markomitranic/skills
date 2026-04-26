#!/usr/bin/env bash

# Status line script for Claude Code
# Receives JSON on stdin from Claude Code and prints a formatted status line.
#
# Displays: Branch, Model, Context window usage, Session cost
# Location: ~/.claude/skills/status-line/statusline.sh
#
# Installation: ~/.claude/settings.json
# "statusLine": {
#   "type": "command",
#   "command": "~/.claude/skills/status-line/statusline.sh"
# }

input=$(cat)

# ---------- helpers ----------

# Classify context-window fill, a.k.a. "context rot".
# Models degrade as context fills, regardless of the model's max window.
# Thresholds are calibrated against MRCRV2 (Google DeepMind's Multi-Round
# Coreference Resolution v2 long-context benchmark). Recurve every couple
# of model generations as frontier capabilities shift.
#
# < 60k   Perfect    — Full recall. Attention undiluted. Zero rot.
# < 200k  Optimal    — Peak working range. MRCRv2 93%+. No degradation.
# < 400k  Nominal    — Linear ~2%/100k drop. Compact above 300k.
# < 700k  Degraded   — Middle-context undertended. Iterative use breaks.
# ≥ 700k  Unreliable — ~25% retrieval failure at 1M. Use RAG / sub-agents.
context_emoji() {
  local tokens=$1
  if   [ "$tokens" -lt 60000  ]; then echo "😀"
  elif [ "$tokens" -lt 200000 ]; then echo "🤓"
  elif [ "$tokens" -lt 400000 ]; then echo "😐"
  elif [ "$tokens" -lt 700000 ]; then echo "😣"
  else                                echo "😡"
  fi
}

# Format a raw token count as e.g. "28k" / "950".
format_tokens() {
  local tokens=$1
  if [ "$tokens" -ge 1000 ]; then
    awk "BEGIN { printf \"%.0fk\", $tokens / 1000 }"
  else
    echo "$tokens"
  fi
}

# ---------- gather data ----------

# Git branch
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
branch=""
if [ -n "$cwd" ]; then
  branch=$(git -C "$cwd" branch --show-current 2>/dev/null)
fi

# Model
model=$(echo "$input" | jq -r '.model.display_name // empty')
model_id=$(echo "$input" | jq -r '.model.id // empty')

# Context window usage
total_input=$(echo "$input"  | jq -r '.context_window.current_usage.input_tokens // 0')
total_output=$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // 0')
cache_read=$(echo "$input"   | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
cache_create=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
total_tokens=$(( total_input + total_output + cache_read + cache_create ))

if echo "$model_id" | grep -qi "1m"; then
  ctx_size=1000000
else
  ctx_size=200000
fi

ctx_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -z "$ctx_pct" ] && [ "$total_tokens" -gt 0 ]; then
  ctx_pct=$(awk "BEGIN { printf \"%.0f\", ($total_tokens / $ctx_size) * 100 }")
fi

ctx_display=$(format_tokens "$total_tokens")
ctx_emoji=$(context_emoji "$total_tokens")

# Session cost
cost=$(echo "$input" | jq -r '.cost.total_cost_usd // empty')

# ---------- assemble segments ----------

segments=()

if [ -n "$branch" ]; then
  segments+=("🌿 ${branch}")
fi

if [ -n "$model" ]; then
  segments+=("🤖 ${model}")
fi

if [ "$total_tokens" -gt 0 ] && [ -n "$ctx_pct" ]; then
  segments+=("${ctx_emoji} Context: ${ctx_display} (${ctx_pct}%)")
elif [ "$total_tokens" -gt 0 ]; then
  segments+=("${ctx_emoji} Context: ${ctx_display}")
fi

if [ -n "$cost" ] && [ "$cost" != "0" ] && [ "$cost" != "null" ]; then
  cost_fmt=$(printf "%.4f" "$cost")
  segments+=("💰 Session: \$${cost_fmt}")
fi

# ---------- output ----------

output=""
for seg in "${segments[@]}"; do
  if [ -z "$output" ]; then
    output="$seg"
  else
    output="${output} | ${seg}"
  fi
done

echo "$output"