"""Shared pytest fixtures — grid data only (no domain scan logic)."""

import pytest

# G1: valid partial 4×4 — two blanks (0), 1..16 each at most once.
# SSOT 상수(34/16/4)는 GREEN 시 entity.constants import 예정.
_G1_ROWS: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 0, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 16],
]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 partial grid: 0×2, row-major blank order (2,2) then (3,3) at 1-index."""
    return [row[:] for row in _G1_ROWS]
