"""D-LOC-01: blank coordinates row-major, 1-index (FR-LOC-01)."""

import pytest

from entity.loc import find_blank_coords


@pytest.mark.entity
def test_d_loc_01_blank_coords_row_major(grid_g1: list[list[int]]) -> None:
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    result = find_blank_coords(grid_g1)
    # Then: [(2,2),(3,3)] 반환 (1-index, row-major)
    assert result == [(2, 2), (3, 3)]
