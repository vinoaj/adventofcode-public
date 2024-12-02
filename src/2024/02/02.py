from pathlib import Path

folder_day = str(Path(__file__).parent).split("/")[-1]
input_file = Path(__file__).parent / f"{folder_day}.txt"

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]


data = [list(map(int, line.split())) for line in data]

SHIFTS = [1, 0]

safe_reports = []
unsafe_reports = []


def is_safe_report(report: list[int]) -> tuple[bool, list[int]]:
    increments = [b - a for a, b in zip(report, report[1:])]
    if any(abs(increment) < 1 or abs(increment) > 3 for increment in increments):
        return (False, increments)

    signs = {increment > 0 for increment in increments if increment != 0}
    return (True, increments) if len(signs) == 1 else (False, increments)


def is_fixed_report_safe(report: list[int], ix: int) -> bool:
    for shift in SHIFTS:
        new_report = report[: ix + shift] + report[ix + 1 + shift :]
        new_report_safe, _ = is_safe_report(new_report)
        if new_report_safe:
            return True

    return False


def q1():
    global safe_reports, unsafe_reports

    assessments = [(report, is_safe_report(report)) for report in data]
    safe_reports = [report for report, (is_safe, _) in assessments if is_safe]
    unsafe_reports = [
        [report, increments]
        for report, (is_safe, increments) in assessments
        if not is_safe
    ]

    return len(safe_reports)


def q2():
    n_safer_reports = 0

    for report, increments in unsafe_reports:
        bad_entries = [
            increment
            for increment in increments
            if abs(increment) < 1 or abs(increment) > 3
        ]

        n_bad_entries = len(bad_entries)
        if n_bad_entries > 1:
            continue

        elif n_bad_entries == 0:
            # No fluctuations; only issue will be they're not increasing or decreasing
            negatives = [increment for increment in increments if increment < 0]
            positives = [increment for increment in increments if increment > 0]

            if not (len(negatives) == 1 or len(positives) == 1):
                continue

            lookup_val = negatives[0] if len(negatives) == 1 else positives[0]
            ix = increments.index(lookup_val)

            n_safer_reports += 1 if is_fixed_report_safe(report, ix) else 0

        elif n_bad_entries == 1:
            # If there's only one bad fluctuation, there is potential for a fix
            ix = increments.index(bad_entries[0])
            n_safer_reports += 1 if is_fixed_report_safe(report, ix) else 0
        else:
            continue

    return n_safer_reports + len(safe_reports)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 472
    print(f"Q2: {q2()}")  # 520
