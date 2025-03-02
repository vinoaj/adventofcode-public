from functools import cache
from pathlib import Path
from typing import Any

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = 13022553808
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    return list(map(int, input))


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)


PRUNE_MOD = 16777216


@cache
def mix(a, b):
    return a ^ b


@cache
def prune(secret_num: int):
    return secret_num % PRUNE_MOD


@cache
def step_1(secret_num: int):
    return prune(mix(secret_num * 64, secret_num))


@cache
def step_2(secret_num: int):
    return prune(mix(secret_num // 32, secret_num))


@cache
def step_3(secret_num: int):
    return prune(mix(secret_num * 2048, secret_num))


@cache
def steps_short_circuit(secret_num: int):
    reduced = secret_num % PRUNE_MOD
    return ((((reduced * 64) ^ reduced) // 32 ^ reduced) * 2048 ^ reduced) % PRUNE_MOD


@cache
def get_next_secret_nums(secret_num: int, n: int):
    for _ in range(n):
        # secret_num = step_1(secret_num)
        # secret_num = step_2(secret_num)
        # secret_num = step_3(secret_num)
        secret_num = steps_short_circuit(secret_num)

    return secret_num


@cache
def get_last_digit(num: int):
    return num % 10


secret_numbers = []


def q1():
    global secret_numbers

    n = 2000
    secret_numbers = [get_next_secret_nums(num, n) for num in input]

    ans = sum(secret_numbers)
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    # prices = []

    ans = None
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(get_next_secret_nums(123, 10))
    # print(f"Q1: {q1()}")
    # print(f"Q2: {q2()}")
