"""
Clique Decision
===============
Given an undirected graph and an integer k, decide whether the graph contains
a clique of size k.

Why it is in NP:
A certificate is a set of k vertices. We can verify in polynomial time that
all pairs of distinct certificate vertices are adjacent.

Special status:
CLIQUE is one of Karp's classic NP-Complete problems.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Set

Graph = Dict[int, Set[int]]


def verify_clique(graph: Graph, vertices: list[int], k: int) -> bool:
    """Verify that vertices describes a clique of size k."""
    if len(vertices) != k or len(set(vertices)) != k:
        return False
    if any(v not in graph for v in vertices):
        return False
    for u, v in combinations(vertices, 2):
        if v not in graph[u] or u not in graph[v]:
            return False
    return True


def solve_brute_force(graph: Graph, k: int) -> list[int] | None:
    """Try every k-vertex subset."""
    for subset in combinations(graph.keys(), k):
        candidate = list(subset)
        if verify_clique(graph, candidate, k):
            return candidate
    return None


if __name__ == "__main__":
    graph = {
        1: {2, 3, 4},
        2: {1, 3, 4},
        3: {1, 2, 4, 5},
        4: {1, 2, 3},
        5: {3},
    }
    k = 4
    clique = solve_brute_force(graph, k)
    print(f"k = {k}")
    print(f"Clique found: {clique}")
    print(f"Verified: {verify_clique(graph, clique, k) if clique else False}")
