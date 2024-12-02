from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    print(data)


def get_init_ints() -> list[int]:
    ints = [int(c) for c in data]
    print(ints)
    return ints


def advance_sequence(seq: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pass


def q1():
    ints = get_init_ints()
    seqs = []

    count = 0
    current_int = None
    for ix, n in enumerate(ints):
        if ix == 0 or count == 0:
            current_int = n
            count += 1
            continue

        if n == current_int:
            count += 1
            continue
        else:
            seqs.append((count, current_int))
            count = 1
            current_int = n

    seqs.append((count, current_int))
    print(seqs)

    return None


def q2():
    return None


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
