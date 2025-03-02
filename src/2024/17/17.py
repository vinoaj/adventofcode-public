from pathlib import Path
from typing import Any

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = None
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])

registers = {}
program = []


def clean_input(input: list[Any]) -> list[Any]:
    global registers, program

    registers = {k[-1]: int(n) for reg in input[0] for k, n in [reg.split(": ")]}
    program = list(map(int, [n for n in input[1][0].split(": ")[1].split(",")]))
    return input


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)
print(program)
print(registers)


def set_register(key, value):
    global registers
    registers[key] = value


def adv(operand: int):
    numerator = registers["A"]
    denominator = operand**2
    val = int(numerator // denominator)
    set_register("A", val)


def bxl(operand: int):
    val = 0
    set_register("B", val)


def jnz(operand: int):
    if registers["A"] == 0:
        return

    # TODO


def bxc(operand: int):
    b = registers["B"]
    c = registers["C"]

    # TODO
    val = 0
    set_register("B", val)


opcode_to_function = {
    0: adv,
    1: bxl,
    3: jnz,
    4: bxc,
}


def q1():
    ans = None
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    ans = None
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
    print(adv(2))
