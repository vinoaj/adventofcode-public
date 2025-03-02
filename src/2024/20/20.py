import sys
from pathlib import Path
from typing import Any

from src.utils.input import DayInput

sys.recursionlimit = 10000

TESTING = True

ASSERT_Q1 = None
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    return input


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)

start_xy = [
    (x, y) for y, row in enumerate(input) for x, pos in enumerate(row) if pos == "S"
][0]
end_xy = [
    (x, y) for y, row in enumerate(input) for x, pos in enumerate(row) if pos == "E"
][0]
walls = [
    (x, y) for x, row in enumerate(input) for y, pos in enumerate(row) if pos == "#"
]

MAX_X, MAX_Y = len(input[0]) - 1, len(input) - 1

print(start_xy, end_xy)


def count_steps(xy, walls, visited: set, steps: int = 0) -> int:
    if xy == end_xy:
        return 0

    if xy in visited:
        return 0

    visited.add(xy)
    x, y = xy

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for d_x, d_y in directions:
        new_x, new_y = x + d_x, y + d_y
        new_xy = (new_x, new_y)
        if (
            new_xy in walls
            or new_xy in visited
            or not (0 <= new_x <= MAX_X and 0 <= new_y <= MAX_Y)
        ):
            continue

        steps += count_steps((new_x, new_y), walls, visited)

    return steps + 1


def q1():
    base_steps = count_steps(start_xy, walls, set())
    print(base_steps)

    ans = None
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
