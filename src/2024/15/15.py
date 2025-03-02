from pathlib import Path
from typing import Any

from src.utils.input import DayInput

TESTING = True

ASSERT_Q1 = 1514353
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])

DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def clean_input(input: list[Any]) -> list[Any]:
    return input


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
# print(input)

grid, moves = input

MAX_X, MAX_Y = len(grid[0]), len(grid)

moves = "".join(moves)
wall_coords = [
    (x, y) for y, row in enumerate(grid) for x, pos in enumerate(row) if pos == "#"
]
box_coords = [
    (x, y) for y, row in enumerate(grid) for x, pos in enumerate(row) if pos == "O"
]
start_pos = [
    (x, y) for y, row in enumerate(grid) for x, pos in enumerate(row) if pos == "@"
][0]
s_x, s_y = start_pos

print(moves)
print(
    f"Starting at {start_pos} robot will make {len(moves)} moves and may encounter up to {len(box_coords)} boxes"
)


def draw_grid(coords):
    grid = [["." for _ in range(MAX_X + 1)] for _ in range(MAX_Y + 1)]

    for x, y in coords:
        grid[y][x] = "O"

    for row in grid:
        print("".join(row))


def get_box_pair_coords(x, y, coords):
    return sorted(
        list(
            set(
                [
                    (cx, cy)
                    for cx, cy in coords
                    if (cx, cy) == (x, y)
                    or (cx, cy) == (x + 1, y)
                    or (cx, cy) == (x - 1, y)
                ]
            )
        )
    )


def move_box_wh2(box_coords, box_xy, direction, max_x, max_y):
    x, y = box_xy
    d_x, d_y = DIRECTIONS[direction]

    box_xy_pair = get_box_pair_coords(x, y, box_coords)
    print(f"Box pair: {box_xy_pair} (from {box_xy})")

    can_move_box = False
    boxes = box_xy_pair

    while 0 <= x < max_x and 0 <= y < max_y:
        x, y = x + d_x, y + d_y
        if (x, y) in box_coords:
            boxes.extend(get_box_pair_coords(x, y, box_coords))
        elif (x, y) in wall_coords:
            break
        else:
            can_move_box = True
            break

    if can_move_box:
        boxes = set(boxes)
        print(f"Can move boxes in direction {direction} -> {boxes}")
        for x, y in boxes:
            box_coords.remove((x, y))
            box_coords.append((x + d_x, y + d_y))
        draw_grid(box_coords)

    print(
        f"For box at {box_xy} moving {direction} to {x, y} is {can_move_box} | {boxes}"
    )

    return can_move_box, box_coords


def move_box(coords, box_xy, direction):
    x, y = box_xy
    d_x, d_y = DIRECTIONS[direction]

    can_move_box = False
    boxes = [box_xy]

    # draw_grid(coords)

    while 0 <= x < MAX_X and 0 <= y < MAX_Y:
        x, y = x + d_x, y + d_y
        if (x, y) in coords:
            boxes.append((x, y))
        elif (x, y) in wall_coords:
            break
        else:
            can_move_box = True
            break

    if can_move_box:
        # print(f"Can move boxes in direction {direction} -> {boxes}")
        for x, y in boxes:
            coords.remove((x, y))
            coords.append((x + d_x, y + d_y))

    # print(
    #     f"For box at {box_xy} moving {direction} to {x, y} is {can_move_box} | {boxes}"
    # )
    # draw_grid(coords)
    return can_move_box, coords


def q1():
    box_state = box_coords.copy()

    x, y = start_pos
    for move in moves:
        d_x, d_y = DIRECTIONS[move]
        # print(f"Moving {move} from {x, y} to {x + d_x, y + d_y} (delta {d_x, d_y})")
        x, y = x + d_x, y + d_y
        # print(x, y)
        if (x, y) in wall_coords:
            x, y = x - d_x, y - d_y
            continue
        if (x, y) in box_state:
            # print(f"Found box at {x, y}")
            can_move, box_state = move_box(box_state, (x, y), move)
            if not can_move:
                x, y = x - d_x, y - d_y
                continue

    # draw_grid(box_state)

    # 7668005
    # 7835425
    ans = sum([(y * 100) + x for x, y in box_state])
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    wall_coords_wh2 = list(set(wall_coords + [(x + 1, y) for x, y in wall_coords]))
    box_coords_wh2 = [((x, y), (x + 1, y)) for x, y in box_coords]
    box_coords_wh2_singles = list(set(box_coords + [(x + 1, y) for x, y in box_coords]))

    start_x, start_y = start_pos
    max_x = max([x for x, _ in wall_coords_wh2])

    start_x += int(
        (
            len([x for x, y in wall_coords if y == start_y and x < start_x])
            + len(
                [x for x, y in box_coords_wh2_singles if y == start_y and x < start_x]
            )
        )
        / 2
    )

    # print(box_coords_wh2)
    print(f"Start at {start_x, start_y}")

    x, y = start_x, start_y
    for move in moves:
        d_x, d_y = DIRECTIONS[move]
        x, y = x + d_x, y + d_y
        if (x, y) in wall_coords:
            x, y = x - d_x, y - d_y
            continue
        if (x, y) in box_coords_wh2_singles:
            # can_move, box_coords_wh2 = move_box(box_coords_wh2, (x, y), move)
            can_move, box_coords_wh2_singles = move_box_wh2(
                box_coords_wh2_singles, (x, y), move, max_x, MAX_Y
            )
            if not can_move:
                x, y = x - d_x, y - d_y
                continue

    score = 0
    print(box_coords_wh2_singles)
    for x, y in box_coords_wh2_singles:
        box_parts = get_box_pair_coords(x, y, box_coords_wh2_singles)
        print(box_parts)

        bx, by = box_parts[0]
        score += by * 100 + bx

        box_coords_wh2_singles.remove(box_parts[0])
        box_coords_wh2_singles.remove(box_parts[1])

    # 809527 too low
    ans = score
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
