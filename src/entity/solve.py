"""Partial-grid solver — step A: fill blanks with missing 1..16 (row-major)."""

from entity.constants import MagicConstant
from entity.loc import find_blank_coords


def solve_step_a(grid: list[list[int]]) -> list[int]:
    """Return int[6] [r1,c1,n1,r2,c2,n2] for valid partial grid (0×2)."""
    coords = find_blank_coords(grid)
    used = {
        value
        for row in grid
        for value in row
        if value != MagicConstant.BLANK_CELL
    }
    missing = [
        n
        for n in range(1, MagicConstant.CELL_MAX + 1)
        if n not in used
    ]
    if len(coords) != 2 or len(missing) != 2:
        raise ValueError("expected exactly two blanks and two missing numbers")
    return [
        coords[0][0],
        coords[0][1],
        missing[0],
        coords[1][0],
        coords[1][1],
        missing[1],
    ]
