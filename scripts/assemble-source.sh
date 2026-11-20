#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_ROOT="${1:-${REPO_ROOT}/.nexora-build/source}"
PART_DIR="${REPO_ROOT}/bundle/parts"
ARCHIVE="${REPO_ROOT}/.nexora-build/NEXORA_Godot_source.tar.gz"

if [[ ! -d "$PART_DIR" ]] || ! compgen -G "${PART_DIR}/part-*.b64" >/dev/null; then
  echo "ERROR: source archive fragments are missing: ${PART_DIR}" >&2
  exit 2
fi

mkdir -p "$(dirname "$ARCHIVE")" "$DEST_ROOT"
cat "${PART_DIR}"/part-*.b64 | tr -d '\r\n' | base64 --decode > "$ARCHIVE"
gzip -t "$ARCHIVE"

tar -tzf "$ARCHIVE" > "${ARCHIVE}.contents.txt"
grep -qx 'NEXORA_Godot/project.godot' "${ARCHIVE}.contents.txt"
grep -qx 'NEXORA_Godot/tests/static_contract_check.py' "${ARCHIVE}.contents.txt"

tar -xzf "$ARCHIVE" -C "$DEST_ROOT"
PROJECT_DIR="${DEST_ROOT}/NEXORA_Godot"
python3 "${REPO_ROOT}/patches/apply_source_fixes.py" "$PROJECT_DIR"
for required in project.godot scenes/main.tscn scripts/ui/main.gd tests/run_tests.gd tests/static_contract_check.py; do
  [[ -f "${PROJECT_DIR}/${required}" ]] || { echo "ERROR: extracted source is missing ${required}" >&2; exit 3; }
done

printf '%s\n' "$PROJECT_DIR"
