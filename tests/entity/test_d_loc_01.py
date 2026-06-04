"""RED — D-LOC-01: blank coordinates row-major, 1-index (FR-LOC-01)."""

import pytest


@pytest.mark.entity
def test_d_loc_01_blank_coords_row_major(grid_g1: list[list[int]]) -> None:
    # Given: G1 격자 (0이 2개)
    _ = grid_g1
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(2,2),(3,3)] 반환 (1-index, row-major)
    pytest.fail("RED: D-LOC-01 — 구현 없음, 의도적 실패")
