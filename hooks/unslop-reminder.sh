#!/bin/sh
# UserPromptSubmit hook: stands in for the `turnReminder` field that custom
# output styles cannot set, re-injecting the unslop thesis on every turn.
# Always exits 0, so it can only ever append context, never block a prompt.
cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"Unslop output style is active. Remember to follow the specific guidelines for this style."}}
JSON
