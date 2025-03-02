from pathlib import Path

TESTING = True

folder_day = str(Path(__file__).parent).split("/")[-1]
filename = "test.txt" if TESTING else f"{folder_day}.txt"
input_file = Path(__file__).parent / filename

data = None
with open(input_file, "r") as file:
    data = file.read().strip().splitlines()
    if len(data) == 1:
        data = data[0]
    # print(data)


def build_layout():
    layout = []
    layout_metadata = []
    layout_str = ""
    for i, v in enumerate(data):
        components = []
        metadata = None
        if i % 2 == 0:
            components = [i // 2 for _ in range(int(v))]
            metadata = (i // 2, int(v))
        else:
            components = ["." for _ in range(int(v))]
            metadata = (".", int(v))

        if len(components) == 0:
            continue

        layout.extend(components)
        layout_metadata.append(metadata)
        # layout_str += "".join([str(x) for x in components])

    return layout, layout_metadata


def q1():
    layout, _ = build_layout()

    str_array = [int(c) if c != "." else c for c in layout]
    # print(str_array[:-100])

    num_ixs = [i for i, c in enumerate(str_array) if isinstance(c, int)]
    empty_ixs = [i for i, c in enumerate(str_array) if not isinstance(c, int)]
    # print(empty_ixs[:100])

    while num_ixs and empty_ixs and empty_ixs[0] < num_ixs[-1]:
        num_ix = num_ixs.pop()
        ix = empty_ixs.pop(0)

        str_array[ix] = str_array[num_ix]
        str_array[num_ix] = "."

    checksum_parts = [n * i for i, n in enumerate(str_array) if isinstance(n, int)]

    ans = sum(checksum_parts)
    # assert ans == 6398252054886

    return ans


def q2():
    layout, layout_metadata = build_layout()

    files = layout_metadata[::2]
    blanks = layout_metadata[1::2]

    new_layout = [files.pop(0)]

    for filename, file_length in files[::-1]:
        _, free_length = blanks.pop(0)
        if file_length <= free_length:
            diff = free_length - file_length
            new_layout.append((filename, file_length))
            if diff > 0:
                new_layout.append((".", diff))
        else:
            new_layout.append((".", free_length))

    checksum_parts = []
    ix = 0
    for n, length in new_layout:
        if n == ".":
            n = 0

        for _ in range(length):
            checksum_parts.append(n * ix)
            ix += 1

    # 784922763557 too low
    return sum(checksum_parts)


if __name__ == "__main__":
    print(f"Q1: {q1()}")  # 6398252054886
    print(f"Q2: {q2()}")
