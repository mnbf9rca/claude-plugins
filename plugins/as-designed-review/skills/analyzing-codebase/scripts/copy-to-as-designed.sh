#!/bin/bash
# Copy as-built analysis to as-designed for user editing
# Usage: copy-to-as-designed.sh <project-root>
# Example: copy-to-as-designed.sh /Users/rob/Downloads/git/my-project

ROOT="${1:-.}"
SRC="$ROOT/docs/codebase-analysis/as-built/"
DST="$ROOT/docs/codebase-analysis/as-designed/"

if [ ! -d "$SRC" ]; then
  echo "Error: $SRC does not exist"
  exit 1
fi

cp -r "$SRC" "$DST"
echo "Copied as-built/ to as-designed/"
