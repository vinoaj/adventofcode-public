from copy import deepcopy
from typing import Any

from pydantic import BaseModel


class GridHelper(BaseModel):
    grid: list[list[Any] | str]

    def __init__(self, grid: list[list[Any] | str]):
        super().__init__(grid=grid)

        if not isinstance(grid[0], list):
            if isinstance(grid[0], str):
                self.grid = [list(row) for row in grid]

    @property
    def unique_values(self) -> set[Any]:
        return set([value for row in self.grid for value in row])

    def get_coordinate_value(self, x: int, y: int) -> Any | bool:
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x]

        return False

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        return self.get_coordinate_value(x, y) is not False

    def get_adjacent_coordinates(self, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (x + d_x, y + d_y)
            for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if self.get_coordinate_value(x + d_x, y + d_y)
        ]

    def get_coordinates_for(self, value: Any) -> list[tuple[int, int]]:
        return [
            (x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val == value
        ]

    def draw_grid(self, chars: dict[str, list[tuple[int, int]]]) -> None:
        tmp_grid = deepcopy(self.grid)

        for char, coordinates in chars.items():
            for x, y in coordinates:
                tmp_grid[y][x] = char

        print("\n".join(["".join(row) for row in tmp_grid]))
