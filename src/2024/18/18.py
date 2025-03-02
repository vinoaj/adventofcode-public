import sys
from heapq import heappop, heappush
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from src.utils.input import DayInput

sys.setrecursionlimit(10000)

TESTING = False

ASSERT_Q1 = None
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    input = [(int(x), int(y)) for xy in input for x, y in [xy.split(",")]]
    return input


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)
print(len(input))

sx, sy = (0, 0)
ex, ey = (70, 70)


class AStarSearch(BaseModel):
    start_xy: tuple[int, int] = (0, 0)
    end_xy: tuple[int, int] = (70, 70)
    obstacles: list[tuple[int, int]] = input
    visited: set[tuple[int, int]] = None

    def _manhattan_distance(self, xy1: tuple[int, int], xy2: tuple[int, int]) -> int:
        x1, y1 = xy1
        x2, y2 = xy2
        return abs(x1 - x2) + abs(y1 - y2)

    def find_path(self):
        queue = [(0, self.start_xy, [])]  # (distance, coord, path)


class DepthFirstSearch(BaseModel):
    start_xy: tuple[int, int] = (0, 0)
    end_xy: tuple[int, int] = (70, 70)
    obstacles: list[tuple[int, int]] = input

    paths: list[tuple[int, int]] = []
    visited: set[tuple[int, int]] = None

    def collect_paths(self, xy: tuple[int, int], path=None):
        print(f"Collecting paths from {xy}")
        if path is None:  # Fix mutable default argument
            path = []

        x, y = xy
        ex, ey = self.end_xy

        if self.visited is None:
            self.visited = set()

        # Base cases
        if xy in self.visited or xy in self.obstacles:
            return
        if not (0 <= x <= ex and 0 <= y <= ey):
            return
        if xy in self.obstacles or xy in self.visited:
            return
        if xy == self.end_xy:
            # Reached the end
            self.paths.append(path[:])
            return

        # Add current position
        self.visited.add(xy)
        # path.append(xy)
        current_path = path + [xy]

        # Try all valid directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x <= ex
                and 0 <= new_y <= ey
                and (new_x, new_y) not in self.obstacles
            ):
                self.collect_paths((new_x, new_y), current_path)

        # path.pop()
        self.visited.remove(xy)
        return self.paths


def q1():
    byte_coords = input[:1024]

    dfs = DepthFirstSearch(obstacles=byte_coords)
    paths = dfs.collect_paths((0, 0))
    print(paths)

    smallest_path = min(paths, key=lambda x: len(x))

    ans = len(smallest_path)
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
