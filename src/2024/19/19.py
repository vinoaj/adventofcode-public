from functools import cache
from pathlib import Path

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = 247
ASSERT_Q2 = 692596560138745

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])
input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()

PATTERNS = input[0][0].split(", ")
DESIGNS = input[1]


@cache
def get_pattern_candidates(design: str) -> list[str]:
    """Given a design, find all patterns that could start the design"""
    return [pattern for pattern in PATTERNS if design.startswith(pattern)]


@cache
def count_design_patterns(design: str) -> int:
    if design == "":
        # Reached the end of the design
        return 1

    # Iterate through next sections of the design
    next_designs = [
        design[len(pattern) :]
        for pattern in get_pattern_candidates(design)
        if design.startswith(pattern)
    ]

    total_possibilities = sum(count_design_patterns(d) for d in next_designs)
    return total_possibilities


def q1() -> int:
    possibilities = [count_design_patterns(design) for design in DESIGNS]

    ans = sum([1 for p in possibilities if p > 0])
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2() -> int:
    n_ways = [count_design_patterns(design) for design in DESIGNS]

    ans = sum(n_ways)
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
