from pathlib import Path

from pydantic import BaseModel

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)


class Instruction(BaseModel):
    action: str
    start: tuple[int, int]
    end: tuple[int, int]


def transform_data(data: list[str]) -> list[Instruction]:
    instructions: list[Instruction] = []

    for line in data:
        parts = line.split()

        end_coords = parts[-1].split(",")
        start_coords = parts[-3].split(",")
        action = "toggle" if parts[0] == "toggle" else parts[1]

        instructions.append(
            Instruction(
                action=action,
                start=(int(start_coords[0]), int(start_coords[1])),
                end=(int(end_coords[0]), int(end_coords[1])),
            )
        )

    return instructions


instructions = transform_data(data)


def get_light_states():
    light_states = [[0 for _ in range(1000)] for _ in range(1000)]
    return light_states


def q1():
    light_states = get_light_states()
    for instruction in instructions:
        for i in range(instruction.start[0], instruction.end[0] + 1):
            for j in range(instruction.start[1], instruction.end[1] + 1):
                if instruction.action == "toggle":
                    light_states[i][j] = 1 - light_states[i][j]
                elif instruction.action == "on":
                    light_states[i][j] = 1
                elif instruction.action == "off":
                    light_states[i][j] = 0

    return sum(sum(row) for row in light_states)


def q2():
    light_states = get_light_states()
    for instruction in instructions:
        for i in range(instruction.start[0], instruction.end[0] + 1):
            for j in range(instruction.start[1], instruction.end[1] + 1):
                if instruction.action == "toggle":
                    light_states[i][j] += 2
                elif instruction.action == "on":
                    light_states[i][j] += 1
                elif instruction.action == "off":
                    light_states[i][j] = max(0, light_states[i][j] - 1)

    return sum(sum(row) for row in light_states)


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
