from copy import deepcopy
from functools import cache
from pathlib import Path
from typing import Any

from devtools import pprint

from src.utils.input import DayInput
from src.utils.solutions import assert_answer

TESTING = False
ASSERT_Q1_TESTING = None
ASSERT_Q2_TESTING = None

ASSERT_Q1 = None
ASSERT_Q2 = None


def clean_input(input: list[Any]) -> list[Any]:
    return input


year, day = map(int, str(Path(__file__).parent).split("/")[-2:])
input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)


def q1():
    ans = None
    assert_answer(ans, ASSERT_Q1_TESTING if TESTING else ASSERT_Q1)
    return ans


def q2():
    ans = None
    assert_answer(ans, ASSERT_Q2_TESTING if TESTING else ASSERT_Q2)
    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
