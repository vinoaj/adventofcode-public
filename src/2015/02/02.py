from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    # Sort each gift's dimensions, so that first area's calculations is shortest area
    data = [sorted([int(x) for x in line.strip().split("x")]) for line in file]


def q1():
    areas = [[a * b, a * c, b * c] for a, b, c in data]
    totals = [(2 * sum(area)) + area[0] for area in areas]

    return sum(totals)


def q2():
    lengths = [(2 * (a + b)) + (a * b * c) for a, b, c in data]
    return sum(lengths)


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
