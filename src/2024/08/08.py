from functools import cache
from pathlib import Path
from typing import Any

from src.utils.grids import GridHelper
from src.utils.input import DayInput
from src.utils.solutions import assert_answer

TESTING = False
ASSERT_Q1_TESTING = 14
ASSERT_Q2_TESTING = 34

ASSERT_Q1 = 359
ASSERT_Q2 = 1293


def clean_input(input: list[Any]) -> list[Any]:
    return input


year, day = map(int, str(Path(__file__).parent).split("/")[-2:])
input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
# print(input)


grid = GridHelper(grid=input)
antennas = grid.unique_values
antennas.remove(".")
# print(antennas)


@cache
def get_antinode_locations(
    location_1: tuple[int], location_2: tuple[int], part_2: bool = False
):
    x1, y1 = location_1
    x2, y2 = location_2

    x_diff = (x1 - x2) * -1
    y_diff = (y1 - y2) * -1

    locations = [location_1, location_2]
    tmp_locations = []

    for xc, yc in locations:
        for multiplier in [-1, 1]:
            nx = xc + x_diff * multiplier
            ny = yc + y_diff * multiplier
            tmp_locations.append((nx, ny))

            if part_2:
                while grid.is_valid_coordinate(nx, ny):
                    tmp_locations.append((nx, ny))
                    nx += x_diff * multiplier
                    ny += y_diff * multiplier

    tmp_locations = [
        loc
        for loc in tmp_locations
        if grid.is_valid_coordinate(*loc) and loc not in locations
    ]

    antenna_locations = set(tmp_locations)
    if part_2:
        antenna_locations.update(locations)

    return antenna_locations


def count_antinodes(part_2: bool = False):
    antinodes = set()

    for antenna in antennas:
        antenna_coords = grid.get_coordinates_for(antenna)
        coord_pairs = [
            (c1, c2) for c1 in antenna_coords for c2 in antenna_coords if c1 != c2
        ]

        for pair in coord_pairs:
            antinodes.update(get_antinode_locations(*pair, part_2=part_2))

    grid.draw_grid({"#": antinodes})
    return len(antinodes)


def q1():
    ans = count_antinodes()
    assert_answer(ans, ASSERT_Q1_TESTING if TESTING else ASSERT_Q1)
    return ans


def q2():
    ans = count_antinodes(part_2=True)
    assert_answer(ans, ASSERT_Q2_TESTING if TESTING else ASSERT_Q2)
    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
