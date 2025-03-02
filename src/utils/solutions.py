from typing import Any, Optional


def assert_answer(answer: Any, expected_result: Optional[Any] = None) -> None:
    if expected_result is None:
        return

    assert answer == expected_result, f"Expected {expected_result}, but got {answer}"
