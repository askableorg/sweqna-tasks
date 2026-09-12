#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Portable across bash 3.2 (macOS) and 5.x — no mapfile.
TASKS=()
while IFS= read -r task; do
  TASKS+=("$task")
done < <(find tasks -mindepth 1 -maxdepth 1 -type d | sort)

if [[ ${#TASKS[@]} -eq 0 ]]; then
  echo "No tasks found under tasks/." >&2
  exit 1
fi

python3 scripts/validate_task.py "${TASKS[@]}"
