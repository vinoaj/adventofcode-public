from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)

string_literals = data


def q1(string_literals: list[str]) -> int:
    string_literal_count = 0
    string_memory_count = 0

    for string_literal in string_literals:
        string_literal_count += len(string_literal)
        string_memory_count += len(eval(string_literal))

    return string_literal_count - string_memory_count


def q2() -> int:
    transformed_strings = []
    for string_literal in string_literals:
        transformed_string = string_literal.replace("\\", "\\\\").replace('"', '\\"')
        transformed_strings.append(f'"{transformed_string}"')

    return q1(string_literals=transformed_strings)


if __name__ == "__main__":
    print(f"Q1: {q1(string_literals=string_literals)}")
    print(f"Q2: {q2()}")
