from functools import cache
from pathlib import Path
from typing import Any

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = 3525
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    return (
        [tuple(pattern) for pattern in input if set(pattern[-1]) == {"#"}],
        [tuple(pattern) for pattern in input if set(pattern[0]) == {"#"}],
    )


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
keys, locks = clean_input(input)

MAX_X, MAX_Y = len(keys[0][0]) - 1, len(keys[0]) - 1


def get_key_or_lock_heights(object_type: str, object_grid: tuple[str]):
    object_grid = object_grid[:-1] if object_type == "key" else object_grid[1:]

    filled = [
        (x, y)
        for y in range(MAX_Y)
        for x in range(MAX_X + 1)
        if object_grid[y][x] == "#"
    ]

    heights = [0 for _ in range(MAX_X + 1)]
    for x, _ in filled:
        heights[x] += 1

    return tuple(heights)


@cache
def get_key_heights(key):
    return get_key_or_lock_heights("key", key)


@cache
def get_lock_heights(lock):
    return get_key_or_lock_heights("lock", lock)


@cache
def is_valid_combination(key_heights, lock_heights):
    return all(
        [(key_heights[i] + lock_heights[i] <= MAX_Y - 1) for i in range(MAX_X + 1)]
    )


def q1():
    key_heights = [get_key_heights(key) for key in keys]
    lock_heights = [get_lock_heights(lock) for lock in locks]

    n_valid_combinations = sum(
        is_valid_combination(key_height, lock_height)
        for key_height in key_heights
        for lock_height in lock_heights
    )

    ans = n_valid_combinations
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    ans = None
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    # print(get_key_heights("abc"))
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
