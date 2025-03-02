from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"
# input_file = Path(__file__).parent / "test.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
DIRECTIONS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
    "NE": (1, 1),
    "SE": (1, -1),
    "SW": (-1, -1),
    "NW": (-1, 1),
}
LETTERS = "XMAS"
NEXT_LETTERS = {"X": "M", "M": "A", "A": "S", "S": None}

A_CHECK_COORDS = [
    # Check above
    (-1, -1),
    (1, -1),
    # Check below
    (-1, 1),
    (1, 1),
]


def get_letter_coords(letter: str) -> list[tuple[int, int]]:
    return [
        (x, y)
        for y, row in enumerate(data)
        for x, ltr in enumerate(row)
        if ltr == letter
    ]


def get_x_coords():
    return get_letter_coords("X")


def get_a_coords():
    return get_letter_coords("A")


def grid_fetch(grid: list[list[str]], x: int, y: int) -> str:
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return grid[y][x]

    return None


def trace_path(x: int, y: int, next_letter: str, direction: str = None) -> int:
    if next_letter is None:
        return 1

    if direction is None:
        for direction, (d_x, d_y) in DIRECTIONS.items():
            new_x, new_y = x + d_x, y + d_y

            if grid_fetch(data, new_x, new_y) == next_letter:
                return trace_path(
                    new_x, new_y, NEXT_LETTERS[next_letter], direction=direction
                )
    else:
        d_x, d_y = DIRECTIONS[direction]
        new_x, new_y = x + d_x, y + d_y
        if grid_fetch(data, new_x, new_y) == next_letter:
            return trace_path(
                new_x, new_y, NEXT_LETTERS[next_letter], direction=direction
            )

    return 0


def q1():
    x_coords = get_x_coords()
    count = 0
    next_letter = NEXT_LETTERS["X"]

    for x, y in x_coords:
        for direction, (d_x, d_y) in DIRECTIONS.items():
            new_x, new_y = x + d_x, y + d_y
            if grid_fetch(data, new_x, new_y) == next_letter:
                count += trace_path(
                    new_x, new_y, NEXT_LETTERS[next_letter], direction=direction
                )

    return count


def q2():
    a_coords = get_a_coords()
    count = 0

    for x, y in a_coords:
        oob = False
        for d_x, d_y in A_CHECK_COORDS:
            new_x, new_y = x + d_x, y + d_y
            if grid_fetch(data, new_x, new_y) is None:
                oob = True
                break

        if oob:
            continue

        next_chars = [data[y + d_y][x + d_x] for d_x, d_y in A_CHECK_COORDS]
        if next_chars.count("M") != 2 or next_chars.count("S") != 2:
            continue

        if (next_chars[0] == next_chars[1]) or (next_chars[0] == next_chars[2]):
            count += 1

    return count


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 2483
    print(f"Q2: {q2()}")  # 1925
