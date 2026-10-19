#!/bin/sh
# grep one provider's snapshots: scripts/lines.sh <slug> <extended-regex> [max]
# prints matching lines with the snapshot name as prefix
slug="$1"; pat="$2"; max="${3:-40}"
cd "$(dirname "$0")/.." || exit 1
for f in data/snapshots/"$slug"/*.txt; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .txt)
  grep -iE "$pat" "$f" 2>/dev/null | head -"$max" | sed "s|^|[$name] |"
done
