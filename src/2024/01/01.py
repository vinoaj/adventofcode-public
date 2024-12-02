from collections import Counter
from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]

data = [tuple(map(int, line.split())) for line in data]
left = [pair[0] for pair in data]
right = [pair[1] for pair in data]


def q1():
    distances = [
        abs(left_n - right_n) for left_n, right_n in zip(sorted(left), sorted(right))
    ]
    return sum(distances)


def q2():
    # Pre-compute counts of right values to speed up repeated lookups
    right_counts = Counter(right)
    scores = [(left_n * right_counts[left_n]) for left_n in left]
    return sum(scores)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 2756096
    print(f"Q2: {q2()}")  # 23117829
