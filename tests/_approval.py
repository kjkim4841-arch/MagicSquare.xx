"""Golden master approval — fixed text format for int[6] success and error codes."""

from __future__ import annotations

import os
from pathlib import Path

_GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"


def _update_golden_enabled() -> bool:
    value = os.environ.get("UPDATE_GOLDEN", "").strip().lower()
    return value in ("1", "true", "yes")


def format_int6_success(solution: list[int]) -> str:
    """Solver success: int[6] as [r1,c1,n1,r2,c2,n2], 1-index coords."""
    if len(solution) != 6:
        raise ValueError(f"expected int[6], got len={len(solution)}")
    body = ",".join(str(x) for x in solution)
    return f"kind: success\nint6: {body}\n"


def format_error_code(code: str) -> str:
    """Boundary-style error golden (e.g. E002 INVALID_BLANKS)."""
    return f"kind: error\nerror: {code}\n"


def _normalize(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual text to tests/golden/<relative>, or update when UPDATE_GOLDEN=1."""
    relative_path = Path(relative.replace("\\", "/"))
    golden_path = _GOLDEN_ROOT / relative_path
    actual_norm = _normalize(actual)

    if _update_golden_enabled():
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual_norm, encoding="utf-8", newline="\n")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"Golden missing: {golden_path}. "
            "Run: UPDATE_GOLDEN=1 python -m pytest <test> -v"
        )

    expected_norm = _normalize(golden_path.read_text(encoding="utf-8"))
    if expected_norm == actual_norm:
        return

    import difflib

    diff = "\n".join(
        difflib.unified_diff(
            expected_norm.splitlines(),
            actual_norm.splitlines(),
            fromfile=f"golden/{relative_path.as_posix()}",
            tofile="actual",
            lineterm="",
        )
    )
    raise AssertionError(f"Golden mismatch for {relative_path}:\n{diff}")
