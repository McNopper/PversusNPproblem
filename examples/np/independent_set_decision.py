"""
Independent Set Decision
========================
Given an undirected graph and an integer k, decide whether the graph contains
an independent set of size k.

Why it is in NP:
A certificate is a set of k vertices. We can verify in polynomial time that
no two selected vertices are adjacent.

Special status:
INDEPENDENT SET is NP-Complete. It is the complement-style counterpart of
CLIQUE in graph complements.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Set

Graph = Dict[int, Set[int]]


def verify_independent_set(graph: Graph, vertices: list[int], k: int) -> bool:
    """Verify that vertices is an independent set of size k."""
    if len(vertices) != k or len(set(vertices)) != k:
        return False
    if any(v not in graph for v in vertices):
        return False
    for u, v in combinations(vertices, 2):
        if v in graph[u] or u in graph[v]:
            return False
    return True


def solve_brute_force(graph: Graph, k: int) -> list[int] | None:
    """Try every k-vertex subset."""
    for subset in combinations(graph.keys(), k):
        candidate = list(subset)
        if verify_independent_set(graph, candidate, k):
            return candidate
    return None


if __name__ == "__main__":
    graph = {
        1: {2, 3},
        2: {1, 3},
        3: {1, 2, 4},
        4: {3, 5},
        5: {4},
    }
    k = 2
    solution = solve_brute_force(graph, k)
    print(f"k = {k}")
    print(f"Independent set found: {solution}")
    print(f"Verified: {verify_independent_set(graph, solution, k) if solution else False}")
