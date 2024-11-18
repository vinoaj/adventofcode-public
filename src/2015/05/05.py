from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]

strings = data
EXCLUDE_STRINGS = ["ab", "cd", "pq", "xy"]


def vowel_count(string: str) -> int:
    return sum(1 for c in string if c in "aeiou")


def has_double_characters(string: str) -> bool:
    return any(string[i] == string[i + 1] for i in range(len(string) - 1))


def has_xyx(string: str) -> bool:
    return any(string[i] == string[i + 2] for i in range(len(string) - 2))


def count_repeating_pairs(string: str) -> int:
    return sum(
        1 for i in range(len(string) - 1) if string[i : i + 2] in string[i + 2 :]
    )


def q1():
    reduced_strings = [s for s in strings if not any(es in s for es in EXCLUDE_STRINGS)]
    reduced_strings = [s for s in reduced_strings if vowel_count(s) >= 3]
    reduced_strings = [s for s in reduced_strings if has_double_characters(s)]
    return len(reduced_strings)


def q2():
    reduced_strings = [s for s in strings if has_xyx(s)]
    reduced_strings = [s for s in reduced_strings if count_repeating_pairs(s) > 0]
    return len(reduced_strings)


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
