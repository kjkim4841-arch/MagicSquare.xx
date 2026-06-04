"""D-SOL-01: solver step A success — G1 int[6] (D-SOLVE-INT6-1INDEX / FR-SOL)."""

import pytest

from _approval import assert_matches_golden, format_int6_success
from entity.constants import MagicConstant
from entity.solve import solve_step_a


@pytest.mark.entity
def test_d_sol_01_step_a_success(grid_g1: list[list[int]]) -> None:
    # Given: G1 (0×2, row-major blanks at (2,2) and (3,3))
    # When: solve_step_a(grid_g1)
    result = solve_step_a(grid_g1)
    # Then: int[6] [r1,c1,n1,r2,c2,n2], 1-index, missing numbers 6 and 11
    assert len(result) == 6
    assert result == [2, 2, 6, 3, 3, 11]
    r1, c1, _n1, r2, c2, _n2 = result
    lo = MagicConstant.COORD_INDEX_BASE
    hi = MagicConstant.GRID_SIZE
    for row, col in ((r1, c1), (r2, c2)):
        assert lo <= row <= hi
        assert lo <= col <= hi
    # Golden Master regression (fixed text format)
    assert_matches_golden(
        format_int6_success(result),
        "d_sol_01_g1_step_a.approved.txt",
    )
