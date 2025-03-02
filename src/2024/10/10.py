from functools import cache
from pathlib import Path
from typing import Any

from src.utils.grids import GridHelper
from src.utils.input import DayInput
from src.utils.solutions import assert_answer

TESTING = False
ASSERT_Q1_TESTING = None
ASSERT_Q2_TESTING = None

ASSERT_Q1 = 538
ASSERT_Q2 = 1110


def clean_input(input: list[Any]) -> list[Any]:
    return [
        (x, y)
        for y, row in enumerate(input)
        for x, pos in enumerate(row)
        if int(pos) == 0
    ], [
        (x, y)
        for y, row in enumerate(input)
        for x, pos in enumerate(row)
        if int(pos) == 9
    ]


year, day = map(int, str(Path(__file__).parent).split("/")[-2:])
input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()

trailheads, trailends = clean_input(input)
input = tuple(input)

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

grid = GridHelper(grid=input)


def traverse(
    x: int, y: int, visited: set[tuple[int, int]], track_paths: bool = False
) -> int:
    if (x, y) in visited:
        return 0

    visited.add((x, y))

    if (x, y) in trailends:
        return 1

    if track_paths:
        visited = visited.copy()

    current_height = int(grid.get_coordinate_value[y][x])
    score = 0

    for dx, dy in DIRECTIONS:
        new_x, new_y = x + dx, y + dy

        if (new_x, new_y) in visited:
            continue

        new_height = int(grid.get_coordinate_value(new_x, new_y))
        if not new_height or new_height - current_height != 1:
            continue

        score += traverse(new_x, new_y, visited, track_paths)

    return score


def q1():
    scores = [traverse(*th, set(), False) for th in trailheads]
    ans = sum(scores)
    assert_answer(ans, ASSERT_Q1_TESTING if TESTING else ASSERT_Q1)
    return ans


def q2():
    n_paths = [traverse(*th, set(), True) for th in trailheads]
    ans = sum(n_paths)
    assert_answer(ans, ASSERT_Q2_TESTING if TESTING else ASSERT_Q2)
    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 538
    print(f"Q2: {q2()}")  # 1110
