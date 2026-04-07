#!/bin/bash
# PreToolUse hook: intercept Bash commands that should use dedicated tools
# This hook is declared in the analyzing-codebase SKILL.md frontmatter
# and activates automatically during skill execution.

# Read tool input from stdin
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Fast-fail: no command means nothing to check
[ -z "$COMMAND" ] && exit 0

# Allow ctags and cp (the only permitted Bash commands for this skill)
echo "$COMMAND" | grep -qE '^\s*(ctags|cp)\b' && exit 0

# Block file operations that should use dedicated tools
# Pattern matches command names at word boundaries to avoid false positives
# (e.g., don't block "catalog" when looking for "cat")
if echo "$COMMAND" | grep -qE '\b(cat|head|tail|less|more)\b.*[/.]'; then
  echo '{"decision":"deny","reason":"Use the Read tool instead of '"$( echo "$COMMAND" | grep -oE '\b(cat|head|tail|less|more)\b' | head -1)"' for reading files."}'
  exit 0
fi

if echo "$COMMAND" | grep -qE '^\s*(find|ls|tree|du|stat|file)\b'; then
  echo '{"decision":"deny","reason":"Use the Glob tool to find files instead of '"$(echo "$COMMAND" | grep -oE '^\s*(find|ls|tree|du|stat|file)\b' | head -1 | tr -d ' ')"'."}'
  exit 0
fi

if echo "$COMMAND" | grep -qE '^\s*(grep|rg|ag|ack)\b'; then
  echo '{"decision":"deny","reason":"Use the Grep tool instead of shell grep for searching file contents."}'
  exit 0
fi

if echo "$COMMAND" | grep -qE '\b(awk|sed|cut|sort|uniq|wc|tr)\b'; then
  echo '{"decision":"deny","reason":"Use dedicated tools (Glob, Grep, Read) instead of '"$(echo "$COMMAND" | grep -oE '\b(awk|sed|cut|sort|uniq|wc|tr)\b' | head -1)"' for file analysis."}'
  exit 0
fi

if echo "$COMMAND" | grep -qE '^\s*(mkdir)\b'; then
  echo '{"decision":"deny","reason":"The Write tool creates directories automatically. Do not use mkdir."}'
  exit 0
fi

# Allow everything else (git, npm, docker, etc.)
exit 0
