from collections import deque
from functools import cache
from pathlib import Path
from typing import Any

from src.utils.input import DayInput

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

KEYPAD = ["789", "456", "123", " 0A"]
DIR_KEYPAD = [" ^A", "<v>"]
KEYPAD_START_XY = (2, 3)
DIR_KEYPAD_START_XY = (2, 0)

DIR_TO_ARROW = {
    (-1, 0): "<",
    (1, 0): ">",
    (0, -1): "^",
    (0, 1): "v",
}


# @cache
def get_target_xy(grid, target):
    return [
        (x, y)
        for y, row in enumerate(grid)
        for x, pos in enumerate(row)
        if pos == target
    ][0]


def path_to_arrows(path):
    arrows = []
    for d_x, d_y in path:
        if (d_x, d_y) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            arrows.append(DIR_TO_ARROW[(d_x, d_y)])
        else:
            arrows.append("A")

    return arrows

    # return [DIR_TO_ARROW[(d_x, d_y)] for d_x, d_y in path]


def shortest_path_in_grid(grid, start, targets):
    rows, cols = len(grid[0]), len(grid)

    # Helper function for BFS
    def bfs(start, end):
        queue = deque([(start[0], start[1], 0, [])])  # (x, y, steps, path)
        visited = set()
        visited.add((start[0], start[1]))

        while queue:
            x, y, steps, path = queue.popleft()

            # If we reach the target, return steps and path
            if (x, y) == end:
                steps += 1
                path.append((99, 99))
                return steps, path

            # Check all 4 directions
            for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + d_x, y + d_y
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and grid[ny][nx] in "1234567890A^v<> "
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1, path + [(d_x, d_y)]))

        return float("inf"), []  # Return infinity if the target is unreachable

    # Start traversing the sequence
    total_steps = 0
    full_path = []
    current_position = start

    for target in targets:
        target_position = get_target_xy(grid, target)  # Find the (x, y) of the target
        steps, path = bfs(current_position, target_position)
        if steps == float("inf"):
            return -1, []  # Return -1 if any target is unreachable
        total_steps += steps
        full_path.extend(path)  # Append the path to the full path
        current_position = target_position

    return total_steps, full_path


def q1():
    sums = 0
    for row in input:
        print(row)
        n_steps, path = shortest_path_in_grid(KEYPAD, KEYPAD_START_XY, [c for c in row])
        print(n_steps, path)

        arrow_path = path_to_arrows(path)
        print(arrow_path)

        for _ in range(2):
            _, path = shortest_path_in_grid(DIR_KEYPAD, DIR_KEYPAD_START_XY, arrow_path)
            arrow_path = path_to_arrows(path)
            print(arrow_path)

        row_int = int(row.replace("A", ""))
        print(
            f"Target {row}: {row_int} * {len(arrow_path)} = {row_int * len(arrow_path)}"
        )
        sums += row_int * len(arrow_path)

    ans = sums
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
