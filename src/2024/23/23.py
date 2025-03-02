from pathlib import Path
from typing import Any

import networkx as nx

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = 1054
ASSERT_Q2 = "ch,cz,di,gb,ht,ku,lu,tw,vf,vt,wo,xz,zk"

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    return [(c1, c2) for pair in input for c1, c2 in [pair.split("-")]]


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
input = clean_input(input)
print(input)

g = nx.Graph()
g.add_edges_from(input)


def q1():
    connections = [list(x) for x in nx.enumerate_all_cliques(g) if len(x) == 3]
    connections = [c for c in connections if any([comp.startswith("t") for comp in c])]
    print(connections)

    ans = len(connections)
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    connections = list(nx.find_cliques(g))
    largest_group = max(connections, key=len)

    ans = ",".join(sorted(largest_group))
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
