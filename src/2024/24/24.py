from functools import cache
from pathlib import Path
from typing import Any

import networkx as nx
import pydot

from src.utils.input import DayInput

TESTING = False

ASSERT_Q1 = None
ASSERT_Q2 = None

year, day = map(int, str(Path(__file__).parent).split("/")[-2:])


def clean_input(input: list[Any]) -> list[Any]:
    connections = []
    nodes = []
    edges = []

    initial_wire_values = {k: int(v) for s in input[0] for k, v in [s.split(": ")]}

    for conn in input[1]:
        aeb, c = conn.split(" -> ")
        a, e, b = aeb.split(" ")

        if a in initial_wire_values:
            a = (a, initial_wire_values[a])
        if b in initial_wire_values:
            b = (b, initial_wire_values[b])
        if c in initial_wire_values:
            c = (c, initial_wire_values[c])

        connections.append((a, e, b, c))
        nodes.append(a)
        nodes.append(e)
        nodes.append(b)
        nodes.append(c)
        edges.extend([(a, e), (b, e), (e, c)])

    return initial_wire_values, connections, nodes, edges


input_parser = DayInput(year=year, day=day, test_mode=TESTING)
input = input_parser.read()
initial_wire_values, connections, nodes, edges = clean_input(input)

print(initial_wire_values)
print(connections)
print(nodes)
print(len(nodes))
print(edges)
print(len(edges))

z_nodes = sorted([n for n in nodes if isinstance(n, str) and n.startswith("z")])
print(z_nodes)

# Create a directed graph
g = nx.DiGraph()
g.add_edges_from(edges)
print(g)


@cache
def AND(a: int, b: int) -> int:
    return 1 if bool(a and b) else 0


@cache
def OR(a: int, b: int) -> int:
    return 1 if bool(a or b) else 0


@cache
def XOR(a: int, b: int) -> int:
    return 1 if a != b else 0


def q1():
    ans = None
    if ASSERT_Q1 and not TESTING:
        assert ans == ASSERT_Q1

    return ans


def q2():
    ans = None
    if ASSERT_Q2 and not TESTING:
        assert ans == ASSERT_Q2

    return ans


if __name__ == "__main__":
    print(f"Q1: {q1()}")
    print(f"Q2: {q2()}")
