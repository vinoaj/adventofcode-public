import string
from pathlib import Path

# from src.utils.grids import

TESTING = True

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    print(data)

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
PLANT_TYPES = list(string.ascii_uppercase)


def explore_plot(x, y, coords: list[tuple[int, int]], current_plot: set):
    # if (x, y) in coords:
    current_plot.add((x, y))
    if (x, y) in coords:
        coords.remove((x, y))

    for dx, dy in DIRECTIONS:
        next_x, next_y = x + dx, y + dy
        if (next_x, next_y) not in coords:
            continue

        current_plot.update(explore_plot(next_x, next_y, coords, current_plot))

    return current_plot


def count_perimeter(plot: set[tuple[int, int]]):
    if len(plot) == 1:
        return 4

    perimeter = 0
    for x, y in plot:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in plot:
                perimeter += 1

    return perimeter


def count_sides(plot: set[tuple[int, int]]):
    original_plot = plot.copy()
    if len(plot) == 1:
        return 4

    sides = 0
    side_coords = set()

    for x, y in plot:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in plot:
                side_coords.add((x, y))

    print("SIDES: ", side_coords)

    xs, ys = [x for x, _ in side_coords], [y for _, y in side_coords]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    while side_coords:
        x, y = side_coords.pop()
        h_plane = [(nx, ny) for nx, ny in side_coords if ny == y]
        v_plane = [(nx, ny) for nx, ny in side_coords if nx == x]

        if len(h_plane) == 0 and len(v_plane) == 0:
            sides += 4
            continue

        if len(h_plane) > 0:
            nx = x + 1
            first_x, last_x = None, None
            while (nx, y) in h_plane:
                side_coords.remove((nx, y))
                last_x = nx
                nx += 1
            nx = x - 1
            while (nx, y) in h_plane:
                side_coords.remove((nx, y))
                first_x = nx
                nx -= 1

    # while plot:
    #     x, y = plot.pop()
    #     new_xy = [
    #         (x + dx, y + dy)
    #         for dx, dy in DIRECTIONS
    #         if 0 <= x + dx < len(data[0]) and 0 <= y + dy < len(data)
    #     ]
    #     all_in_plot = all([(x, y) in plot for x, y in new_xy])
    #     if all_in_plot:
    #         # Surrounded by plots, so not on an edge
    #         continue

    #     for new_x, new_y in new_xy:
    #         # Must be on an edge
    #         if (new_x, new_y) in plot:
    #             side_coords.add((new_x, new_y))
    #             plot.remove((new_x, new_y))  # Don't reprocess this plant

    # print(f"{original_plot=} -> {side_coords=}")

    # while side_coords:
    #     x, y = side_coords.pop()
    #     # Look at horizontal plane
    #     horizontal_plane = [(nx, ny) for nx, ny in side_coords if ny == y]
    #     vertical_plane = [(nx, ny) for nx, ny in side_coords if nx == x]

    #     if len(horizontal_plane) == 0 and len(vertical_plane) == 0:
    #         # This is a lone plant in its own plot of 1.
    #         # Theoretically this case should have been picked up at the top.
    #         sides += 4
    #         continue

    #     if len(horizontal_plane) > 0:
    #         t_x = x

    #         while True:
    #             t_x -= 1
    #             if (t_x, y) not in horizontal_plane:
    #                 break
    #             else:
    #                 side_coords.remove((t_x, y))

    #         t_x = x
    #         while True:
    #             t_x += 1
    #             if (t_x, y) not in horizontal_plane:
    #                 break
    #             else:
    #                 side_coords.remove((t_x, y))

    #         sides += 3

    #     if len(vertical_plane) > 0:
    #         t_y = y

    #         while True:
    #             t_y -= 1
    #             if (x, t_y) not in vertical_plane:
    #                 # sides += 1
    #                 break
    #             else:
    #                 side_coords.remove((x, t_y))

    #         t_y = y
    #         while True:
    #             t_y += 1
    #             if (x, t_y) not in vertical_plane:
    #                 # sides += 1
    #                 break
    #             else:
    #                 side_coords.remove((x, t_y))

    #         sides += 3

    #     # Look at vertical plane

    # # for dx, dy in DIRECTIONS:
    # #     if (x + dx, y + dy) not in plot:
    # #         side_coords.add((x + dx, y + dy))

    return sides


def calculate_price_for_plant_type(plant_type: str, do_count_sides: bool = False):
    coords = list(
        {
            (x, y)
            for y, row in enumerate(data)
            for x, pos in enumerate(row)
            if pos == plant_type
        }
    )

    plots = []
    while coords:
        x, y = coords.pop()
        plot = explore_plot(x, y, coords, {(x, y)})
        plots.append(plot)

    if do_count_sides:
        areas = [(len(plot), count_sides(plot)) for plot in plots]
    else:
        areas = [(len(plot), count_perimeter(plot)) for plot in plots]
    prices = [area * perimeter for area, perimeter in areas]

    return sum(prices)


def q1():
    prices = [calculate_price_for_plant_type(plant_type) for plant_type in PLANT_TYPES]
    return sum(prices)


def q2():
    prices = [
        calculate_price_for_plant_type(plant_type, do_count_sides=True)
        for plant_type in PLANT_TYPES
    ]

    # 2594624 too high
    # 1731 too low
    return sum(prices)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 1377008
    print(f"Q2: {q2()}")
