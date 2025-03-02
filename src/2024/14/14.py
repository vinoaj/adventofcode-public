import math
from pathlib import Path

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = 228457125
ASSERT_Q2 = 6493

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])

# 101 wide x 103 tall
MAX_X = 100
MAX_Y = 102
SECONDS = 100

if TESTING:
    MAX_X = 10
    MAX_Y = 6


def clean_input():
    robots = [
        [
            tuple(map(int, line.split()[0].split("=")[1].split(","))),
            tuple(map(int, line.split()[1].split("=")[1].split(","))),
        ]
        for line in input
    ]

    return robots


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input()
print(input)


def calculate_end_position(start_xy, velocity_xy, time):
    vx, vy = velocity_xy
    tx, ty = start_xy

    tx = (tx + vx * time) % (MAX_X + 1)
    ty = (ty + vy * time) % (MAX_Y + 1)

    return tx, ty


def get_quadrant_counts(coords):
    quadrant_width = MAX_X // 2
    quadrant_height = MAX_Y // 2

    quadrants = [
        [(0, 0), (quadrant_width - 1, quadrant_height - 1)],
        [(quadrant_width + 1, 0), (MAX_X, quadrant_height - 1)],
        [(0, quadrant_height + 1), (quadrant_width - 1, MAX_Y)],
        [(quadrant_width + 1, quadrant_height + 1), (MAX_X, MAX_Y)],
    ]

    counts = []
    for quadrant in quadrants:
        q_coords = [
            (x, y)
            for x, y in coords
            if quadrant[0][0] <= x <= quadrant[1][0]
            and quadrant[0][1] <= y <= quadrant[1][1]
        ]

        counts.append(len(q_coords))

    return counts


def all_unique_coords(coords):
    return len(set(coords)) == len(coords)


def draw_grid(coords):
    grid = [["." for _ in range(MAX_X + 1)] for _ in range(MAX_Y + 1)]

    for x, y in coords:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))


def q1():
    end_coords = [
        calculate_end_position(start, velocity, SECONDS) for start, velocity in input
    ]
    draw_grid(end_coords)

    ans = math.prod(get_quadrant_counts(end_coords))

    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    target_secs = None
    for s in range(1, SECONDS * 1000):
        end_coords = [calculate_end_position(start, v, s) for start, v in input]
        if all_unique_coords(end_coords):
            target_secs = s
            break

    if ASSERT_Q2 and not TESTING:
        assert target_secs == ASSERT_Q2

    draw_grid(end_coords)
    return target_secs


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
