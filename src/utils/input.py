from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field


class DayInput(BaseModel):
    year: int = Field(default=2024, alias="y")
    day: int = Field(default=1, alias="d")
    test_mode: bool = False
    input: list[Any] = None

    split_characters: ClassVar[list[str]] = [",", ":", "|"]

    class Config:
        populate_by_name = True

    @property
    def day_str(self):
        return f"{self.day:02}"

    def _get_path(self):
        filename = "test.txt" if self.test_mode else f"{self.day_str}.txt"
        return Path(__file__).parent.parent / str(self.year) / self.day_str / filename

    def _get_lines(self, input_str: str):
        lines = None
        if "\n\n" in input_str:
            # lines = input_str.split("\n\n")
            lines = [line.splitlines() for line in input_str.split("\n\n")]
        else:
            lines = input_str.splitlines()

        return lines

    def _split_line_item(self, line: str):
        # TODO
        pass

    def read(self):
        print(f"Reading input from {self._get_path()}")
        with open(self._get_path(), "r") as file:
            input = file.read().strip()

        self.input = self._get_lines(input)

        if len(self.input) == 1:
            self.input = self.input[0]

        return self.input
