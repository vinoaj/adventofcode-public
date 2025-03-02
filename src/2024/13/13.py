from pathlib import Path

TESTING = False

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

ASSERT_Q1 = 29877
ASSERT_Q2 = 99423413811305


def parse_input():
    with open(input_file, "r") as file:
        input = file.read().strip()

    if "\n\n" in input:
        input = input.split("\n\n")
        input = [line.strip().splitlines() for line in input]
    else:
        input = input.strip().splitlines()
    if len(input) == 1:
        input = input[0]

    return input


input = parse_input()
# print(input)

A_TOKEN_COST = 3
B_TOKEN_COST = 1
ADD_TO_PRIZE = 10000000000000


def process_input():
    machines = []
    for machine in input:
        machine_data = {}
        for metadata in machine:
            key, xy = metadata.split(": ")
            if key[-1] in ["A", "B"]:
                key = key[-1]
            else:
                key = "P"

            x, y = xy.split(", ")

            split_sign = "+" if "+" in x else "="
            x = int(x.split(split_sign)[1])
            y = int(y.split(split_sign)[1])

            machine_data[key] = (x, y)

        machines.append(machine_data)

    return machines


input = process_input()
# print(input)


def calculate_tokens(add_to_prize: int = 0):
    tokens = 0
    for machine in input:
        x1, y1 = machine["A"]
        x2, y2 = machine["B"]
        xp, yp = machine["P"]
        xp, yp = xp + add_to_prize, yp + add_to_prize

        # Solving a simultaneous equation based on a 2x2 matrix of x & y's
        # a*x1 + b*x2 = xp
        # a*y1 + b*y2 = yp
        a = (xp * y2 - yp * x2) / (x1 * y2 - y1 * x2)
        b = (xp * y1 - yp * x1) / (x2 * y1 - y2 * x1)

        if a.is_integer() and b.is_integer():
            tokens += A_TOKEN_COST * a + B_TOKEN_COST * b

    return int(tokens)


def q1():
    tokens = calculate_tokens()
    if ASSERT_Q1:
        assert tokens == ASSERT_Q1

    return tokens


def q2():
    tokens = calculate_tokens(add_to_prize=ADD_TO_PRIZE)
    if ASSERT_Q2:
        assert tokens == ASSERT_Q2

    return tokens


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
