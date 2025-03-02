from collections import defaultdict
from pathlib import Path

TESTING = False

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)


break_point = data.index("")
orders, page_updates = data[:break_point], data[break_point + 1 :]

orders = [tuple(map(int, o.split("|"))) for o in orders]
page_updates = [tuple(map(int, u.split(","))) for u in page_updates]

page_orders = defaultdict(list)
for page, next_page in orders:
    page_orders[page].append(next_page)

invalid_updates = []


def q1():
    global invalid_updates

    valid_updates = []
    for i, update in enumerate(page_updates):
        valid = True
        for p, page in enumerate(update):
            next_pages = page_updates[i][p + 1 :]
            valid_next_pages = []

            if page in page_orders:
                valid_next_pages = page_orders[page]

            all_valid = all([next_page in valid_next_pages for next_page in next_pages])

            if not all_valid:
                invalid_updates.append(update)
                valid = False
                break

        if valid:
            valid_updates.append(update)

    middle_pages = [update[len(update) // 2] for update in valid_updates]
    return sum(middle_pages)


def custom_sort(page, next_page):
    if next_page not in page_orders or next_page in page_orders[page]:
        return -1
    elif page == next_page:
        return 0
    else:
        return 1


def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if custom_sort(arr[j], arr[j + 1]) > 0:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def q2():
    new_updates = []
    for invalid_update in invalid_updates:
        new_update = bubble_sort(list(invalid_update))
        new_updates.append(new_update)

    middle_pages = [update[len(update) // 2] for update in new_updates]
    return sum(middle_pages)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 4609
    print(f"Q2: {q2()}")  # 5723
