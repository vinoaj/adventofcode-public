from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]

    print(data)

DIRECTIONS = {
    "^": (0, 1),
    "v": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
}


def get_visited_houses(directions: list[str]) -> list[tuple[int, int]]:
    visited_houses: list[tuple[int, int]] = [(0, 0)]

    for direction in directions:
        current_house = visited_houses[-1]
        dx, dy = DIRECTIONS[direction]
        visited_houses.append((current_house[0] + dx, current_house[1] + dy))

    return visited_houses


def q1():
    visited_houses = get_visited_houses(data)
    return len(set(visited_houses))


def q2():
    santa_directions = data[::2]
    robo_santa_directions = data[1::2]

    visited_houses = get_visited_houses(santa_directions) + get_visited_houses(
        robo_santa_directions
    )
    return len(set(visited_houses))


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
