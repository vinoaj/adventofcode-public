from functools import cached_property
from pathlib import Path
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field, field_validator

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = None
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    return input


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)

start = [
    (x, y) for x, row in enumerate(input) for y, pos in enumerate(row) if pos == "S"
][0]
end = [
    (x, y) for x, row in enumerate(input) for y, pos in enumerate(row) if pos == "E"
][0]
walls = [
    (x, y) for x, row in enumerate(input) for y, pos in enumerate(row) if pos == "#"
]

MAX_X, MAX_Y = len(input[0]) - 1, len(input) - 1

START_DIRECTION = (1, 0)

NEXT_DIRECTIONS = {
    (1, 0): [(0, 1), (0, -1)],
    (-1, 0): [(0, 1), (0, -1)],
    (0, 1): [(1, 0), (-1, 0)],
    (0, -1): [(1, 0), (-1, 0)],
}

print(walls)
print(start, end)

paths = []
scores = []


class Coordinate(BaseModel):
    x: int = 0
    y: Annotated[int, Field(validate_default=True)] = 0

    @field_validator("x", "y")
    @classmethod
    def check_non_negative(cls, v, field):
        if v < 0:
            raise ValueError(f"{field.name} must be >= 0")
        return v


class DepthFirstSearch(BaseModel):
    grid: list[list[str]]
    obstacles: Optional[list[Coordinate]] = None

    start_x: Optional[int] = None
    start_y: Optional[int] = None
    start_xy: Optional[Coordinate] = None
    end_x: Optional[int] = None
    end_y: Optional[int] = None
    end_xy: Optional[Coordinate] = None

    start_direction: tuple[int, int] = (0, 1)
    next_directions: dict[tuple[int, int], list[tuple[int, int]]] = {
        (1, 0): [(0, 1), (0, -1)],
        (-1, 0): [(0, 1), (0, -1)],
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)],
    }

    paths: list[list[Coordinate]] = []
    visited: set[Coordinate] = set()
    scores: list[int] = []

    @cached_property
    def max_x(self):
        return len(self.grid[0]) - 1

    @cached_property
    def max_y(self):
        return len(self.grid) - 1

    def _xy_in_range(self, x, y):
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

    def search(self):
        if not self.start_x:
            self.start_x = self.start_xy.x
            self.start_y = self.start_xy.y

        if not self.end_x:
            self.end_x = self.end_xy.x
            self.end_y = self.end_xy.y

        self.traverse_path(self.start_xy, START_DIRECTION, 0)

    def traverse_path(self, x, y, direction, score, path):
        if (x, y) in self.visited:
            return

        if (x, y) == (self.end_x, self.end_y):
            self.paths.append(self.path)

        self.visited.add((x, y))
        path.append((x, y))

        d_x, d_y = direction
        nx, ny = x + d_x, y + d_y

        if not self._xy_in_range(nx, ny):
            return

        pass

    pass


def traverse_path(xy, direction, visited, path, score):
    if xy in visited:
        return

    if xy == end:
        scores.append(score)
        paths.append(path)

    visited.add(xy)
    path.append(xy)

    x, y = xy
    d_x, d_y = direction
    nx, ny = x + d_x, y + d_y
    # nx, ny = xy + direction

    if not (0 <= nx <= MAX_X and 0 <= ny <= MAX_Y):
        return

    if (nx, ny) not in walls:
        score += 1
        traverse_path((nx, ny), direction, visited, path, score)

    for d_x, d_y in NEXT_DIRECTIONS[direction]:
        new_x, new_y = x + d_x, y + d_y
        if (new_x, new_y) not in walls and (new_x, new_y) not in visited:
            score += 1000
            traverse_path((new_x, new_y), (d_x, d_y), visited, path, score)

    visited.remove(xy)
    path.pop()

    return scores


def q1():
    ans = sum(traverse_path(start, START_DIRECTION, set(), [], 0))
    print(paths)
    print(scores)
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    ans = None
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
