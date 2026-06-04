"""Blank-cell location helpers (FR-LOC-01)."""

from entity.constants import MagicConstant


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return blank (0) cell coordinates in row-major order, 1-index (row, col)."""
    coords: list[tuple[int, int]] = []
    base = MagicConstant.COORD_INDEX_BASE
    for row in range(MagicConstant.GRID_SIZE):
        for col in range(MagicConstant.GRID_SIZE):
            if grid[row][col] == MagicConstant.BLANK_CELL:
                coords.append((row + base, col + base))
    return coords
