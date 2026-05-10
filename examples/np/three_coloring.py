"""
Three Coloring
==============
Given an undirected graph, decide whether it has a proper coloring that uses
exactly three colors.

Why it is in NP:
A certificate is a color assigned to each vertex. We can verify in polynomial
time that adjacent vertices receive different colors and that the coloring uses
exactly the three allowed colors.

Special status:
3-COLORING is NP-Complete. More generally, k-COLORING is NP-Complete for every
fixed k >= 3.
"""

from __future__ import annotations

from typing import Dict, Set

Graph = Dict[int, Set[int]]


def verify_three_coloring(graph: Graph, coloring: dict[int, int]) -> bool:
    """Verify that coloring is proper and uses exactly colors 0, 1, and 2."""
    if set(coloring.keys()) != set(graph.keys()):
        return False
    used_colors = set(coloring.values())
    if used_colors != {0, 1, 2}:
        return False
    for node, neighbors in graph.items():
        color = coloring.get(node)
        if color not in {0, 1, 2}:
            return False
        for neighbor in neighbors:
            if coloring.get(neighbor) == color:
                return False
    return True


def solve_backtracking(graph: Graph) -> dict[int, int] | None:
    """Backtracking solver for exact 3-colorability."""
    nodes = sorted(graph.keys(), key=lambda node: len(graph[node]), reverse=True)
    coloring: dict[int, int] = {}

    def backtrack(index: int) -> bool:
        if index == len(nodes):
            return set(coloring.values()) == {0, 1, 2}
        node = nodes[index]
        for color in range(3):
            if all(coloring.get(neighbor) != color for neighbor in graph[node]):
                coloring[node] = color
                if backtrack(index + 1):
                    return True
                del coloring[node]
        return False

    return coloring if backtrack(0) else None


if __name__ == "__main__":
    graph = {
        1: {2, 3},
        2: {1, 3},
        3: {1, 2, 4},
        4: {3},
    }
    coloring = solve_backtracking(graph)
    print(f"3-coloring found: {coloring}")
    print(f"Verified: {verify_three_coloring(graph, coloring) if coloring is not None else False}")
