#!/usr/bin/env python3
"""Apply reviewed, fail-closed compatibility fixes to the packaged NEXORA source."""
from __future__ import annotations

import sys
from pathlib import Path


def _replace_once_or_already_patched(source: str, original: str, replacement: str, label: str) -> str:
    original_count = source.count(original)
    replacement_count = source.count(replacement)
    if replacement_count == 1 and original_count == 0:
        return source
    if original_count != 1 or replacement_count != 0:
        raise ValueError(f"Unexpected source shape for patch: {label}")
    return source.replace(original, replacement, 1)


def apply_fixes(project_dir: Path) -> None:
    test_file = project_dir / "tests" / "run_tests.gd"
    if not test_file.is_file():
        raise FileNotFoundError(f"NEXORA GDScript tests not found: {test_file}")

    source = test_file.read_text(encoding="utf-8")
    source = _replace_once_or_already_patched(
        source,
        '\tstate["run"] = {"stage": 3, "wave": 1, "started_at": 1000.0, "session": session}\n\tvar save_manager = GameStateScript.new()',
        '\tstate["run"] = {"stage": 3, "wave": 1, "started_at": 1000.0, "session": session}\n'
        '\tstate["run"]["session"]["node_type"] = "boss" # Simulate untrusted/tampered save data.\n'
        '\tvar save_manager = GameStateScript.new()',
        "tampered checkpoint node type fixture",
    )
    source = _replace_once_or_already_patched(
        source,
        '\t_expect(str(normalized["run"]["session"]["node_type"]) == "puzzle", "نوع العقدة المستعادة يجب أن يطابق المرحلة")',
        '\t_expect(str(normalized["run"]["session"]["node_type"]) == WorldMap.get_node_type(3), "نوع العقدة المستعادة يجب أن يُشتق من المرحلة لا من بيانات الحفظ")',
        "canonical checkpoint node type assertion",
    )
    test_file.write_text(source, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: apply_source_fixes.py <NEXORA_Godot project directory>", file=sys.stderr)
        return 2
    try:
        apply_fixes(Path(sys.argv[1]).resolve())
    except (OSError, ValueError) as exc:
        print(f"Source patch failed safely: {exc}", file=sys.stderr)
        return 1
    # Keep stdout reserved for the extracted project path consumed by GitHub Actions.
    print("NEXORA source overlays: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
