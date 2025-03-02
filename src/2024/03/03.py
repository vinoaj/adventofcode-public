import re
from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]

instructions = "".join(data)
# print(instructions)

RE_MUL = re.compile(r"(mul\(\d+\,\d+\))")
RE_NUMS = re.compile(r"\d+")
RE_DONT = re.compile(r"don't\(\)")
RE_DO = re.compile(r"do\(\)")


def calculate_result(input_instructions: str) -> int:
    matches = RE_MUL.findall(input_instructions)
    operation_sums = 0

    for match in matches:
        nums = list(map(int, RE_NUMS.findall(match)))
        operation_sums += nums[0] * nums[1]

    return operation_sums


def find_next_dont(current_ix_end: int, dont_ix_pairs: list[tuple[int, int]]):
    return next((pair for pair in dont_ix_pairs if pair[0] > current_ix_end), None)


def q1() -> int:
    return calculate_result(instructions)


def q2() -> int:
    dont_ix_pairs = [(m.start(0), m.end(0)) for m in RE_DONT.finditer(instructions)]
    do_ix_pairs = [(0, 0)] + [
        (m.start(0), m.end(0)) for m in RE_DO.finditer(instructions)
    ]

    new_instructions = ""
    seen_dont_ix_pairs = set()

    for do_ix_pair in do_ix_pairs:
        next_dont_ix_pair = find_next_dont(do_ix_pair[1], dont_ix_pairs)
        if next_dont_ix_pair and next_dont_ix_pair not in seen_dont_ix_pairs:
            new_instructions += instructions[do_ix_pair[0] : next_dont_ix_pair[0]]
            seen_dont_ix_pairs.add(next_dont_ix_pair)

    return calculate_result(new_instructions)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 175700056
    print(f"Q2: {q2()}")  # 71668682
