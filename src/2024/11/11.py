import math
from functools import cache
from pathlib import Path

TESTING = False

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    print(data)

stones = list(map(int, data.split()))
BLINKS = 25
MULTIPLIER = 2024


@cache
def split_stone(stone: int) -> int | tuple[int, int]:
    if stone == 0:
        return 1

    n_digits = math.floor(math.log10(abs(stone))) + 1
    if n_digits % 2 == 0:
        stone_str = str(stone)
        split_point = n_digits // 2
        left, right = (
            stone_str[:split_point],
            stone_str[split_point:],
        )
        return (int(left), int(right))
    else:
        return stone * MULTIPLIER


@cache
def blink_stone(stone: int, blinks: int) -> int:
    """Take one stone and recursively count the number of stones after `blinks` blinks"""
    if blinks == 0:
        return 1

    split = split_stone(stone)
    if isinstance(split, int):
        return blink_stone(split, blinks - 1)
    else:
        return sum([blink_stone(s, blinks - 1) for s in split])


def q1(blinks: int = BLINKS):
    counts = [blink_stone(stone, blinks) for stone in stones]
    return sum(counts)


def q2():
    return q1(blinks=75)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 193899
    print(f"Q2: {q2()}")  # 229682160383225
