import operator
from pathlib import Path
from typing import Any

from src.utils.input import DayInput
from src.utils.solutions import assert_answer

TESTING = False
ASSERT_Q1_TESTING = 3749
ASSERT_Q2_TESTING = 11387

ASSERT_Q1 = 3351424677624
ASSERT_Q2 = 204976636995111


def clean_input(input: list[Any]) -> list[Any]:
    # Storing as a list, as there are some duplicate results
    return [
        (int(result), list(map(int, nums.split())))
        for line in input
        for result, nums in [line.split(": ")]
    ]


year, day = map(int, str(Path(__file__).parent).split("/")[-2:])
input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
equations = clean_input(input)

OPERATIONS = [operator.mul, operator.add]


def is_valid_combo(
    target: int, remaining_nums: list[int], do_concat: bool = False
) -> bool:
    if len(remaining_nums) == 1:
        return target == remaining_nums[0]

    n1, n2 = remaining_nums[:2]
    add_next_two = [n1 + n2]
    mult_next_two = [n1 * n2]
    concat_next_two = [int(str(n1) + str(n2))]

    if is_valid_combo(target, add_next_two + remaining_nums[2:], do_concat):
        return True
    if is_valid_combo(target, mult_next_two + remaining_nums[2:], do_concat):
        return True

    if do_concat and is_valid_combo(
        target, concat_next_two + remaining_nums[2:], do_concat
    ):
        return True

    return False


def q1():
    good_test_values = [
        target for target, nums in equations if is_valid_combo(target, nums)
    ]

    ans = sum(good_test_values)
    assert_answer(ans, ASSERT_Q1_TESTING if TESTING else ASSERT_Q1)
    return ans


def q2():
    good_test_values = [
        target
        for target, nums in equations
        if is_valid_combo(target, nums, do_concat=True)
    ]

    ans = sum(good_test_values)
    assert_answer(ans, ASSERT_Q2_TESTING if TESTING else ASSERT_Q2)
    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
