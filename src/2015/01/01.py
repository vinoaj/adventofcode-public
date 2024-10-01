from pathlib import Path

# get folder this script is in, then look for {folder_name}.txt
folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip()
    print(data)


def q1():
    ups = data.count("(")
    downs = data.count(")")

    target_floor = ups - downs
    return target_floor


def q2():
    floor = 0
    target = -1

    for i, c in enumerate(data):
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1

        if floor == target:
            return i + 1

    return None


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
