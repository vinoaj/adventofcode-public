from collections import Counter
from functools import cache
from pathlib import Path
from typing import Optional

TESTING = False

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

next_directions = {}
for i, direction in enumerate(DIRECTIONS):
    next_ix = i + 1
    if i == len(DIRECTIONS) - 1:
        next_ix = 0

    next_directions[direction] = DIRECTIONS[next_ix]

MAX_Y = len(data)
MAX_X = len(data[0])

obstacle_coords = [
    (x, y) for y, row in enumerate(data) for x, pos in enumerate(row) if pos == "#"
]
start_pos = [
    (x, y) for y, row in enumerate(data) for x, pos in enumerate(row) if pos == "^"
][0]

# print(obstacle_coords)
# print(start_pos)
# print(next_directions)


@cache
def get_next_obstacle(start_pos: tuple[int, int], direction: tuple[int, int]):
    dx, dy = direction

    next_obstacle = None
    nx, ny = start_pos

    while not next_obstacle:
        nx, ny = nx + dx, ny + dy
        if (nx, ny) in obstacle_coords:
            next_obstacle = (nx, ny)

        if not (0 <= nx < MAX_X and 0 <= ny < MAX_Y):
            break

    return next_obstacle


@cache
def get_visited_steps(
    start_pos: tuple[int, int],
    direction: Optional[tuple[int, int]],
    end_pos: Optional[tuple[int, int]],
):
    sx, sy = start_pos
    dir_x, dir_y = direction

    if end_pos is None:
        ex = sx if dir_x == 0 else MAX_X if dir_x == 1 else 0
        ey = sy if dir_y == 0 else MAX_Y if dir_y == 1 else 0
        end_pos = (ex, ey)
        print(f"EndPOS was NONE -> end_pos: {end_pos} ({start_pos=}, {direction=})")
        return get_visited_steps(start_pos, direction, end_pos)

    ex, ey = end_pos
    dx, dy = sx - ex, sy - ey

    n_steps = abs(dx) if dx != 0 else abs(dy)

    steps = [start_pos]
    steps.extend(
        [(sx + (dir_x * step), sy + (dir_y * step)) for step in range(n_steps)]
    )

    return steps


def print_grid(grid, coords, fill="X"):
    new_grid = grid
    for x, y in coords:
        new_grid[y] = new_grid[y][:x] + fill + new_grid[y][x + 1 :]

    print("\n".join(new_grid))


@cache
def get_visited_coords():
    current_pos = start_pos
    direction = DIRECTIONS[0]

    visited_coords = {current_pos}
    visited_coords_list = [current_pos]
    tmp_obstacle_coords = set()
    seen_count = 0

    while True:
        print(f"current_pos: {current_pos}; direction: {direction}")
        obstacle = get_next_obstacle(current_pos, direction)

        if obstacle is not None:
            tmp_obstacle_coords.add(obstacle)

        steps = get_visited_steps(
            start_pos=current_pos, end_pos=obstacle, direction=direction
        )
        print(current_pos, steps, obstacle)

        # for step in steps:
        #     if step in visited_coords:
        #         seen_count += 1

        visited_coords.update(steps)
        visited_coords_list.extend(steps)
        current_pos = steps[-1]
        direction = next_directions[direction]

        if obstacle is None:
            break

    counter = Counter(visited_coords_list)
    seen_count = sum([1 for v in counter.values() if v > 1])

    return visited_coords, seen_count


def q1():
    visited_coords, _ = get_visited_coords()
    print_grid(data, visited_coords)

    return len(visited_coords)


def q2():
    _, seen_count = get_visited_coords()

    # 798 too low
    # 643 too low
    return seen_count


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 4890
    print(f"Q2: {q2()}")
