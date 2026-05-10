"""
Max Cut Decision
================
Given an undirected graph and an integer k, decide whether there exists a
partition of the vertices that cuts at least k edges.

Why it is in NP:
A certificate is one side of the partition. We can verify in polynomial time
by counting how many edges cross from the chosen side to its complement.

Special status:
MAX CUT in decision form is NP-Complete.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Set

Graph = Dict[int, Set[int]]


def edge_list(graph: Graph) -> list[tuple[int, int]]:
    """Return undirected edges without duplicates."""
    return [(u, v) for u, neighbors in graph.items() for v in neighbors if u < v]


def cut_size(graph: Graph, left_side: set[int]) -> int:
    """Return the number of crossing edges."""
    size = 0
    for u, v in edge_list(graph):
        if (u in left_side) != (v in left_side):
            size += 1
    return size


def verify_max_cut(graph: Graph, left_vertices: list[int], k: int) -> bool:
    """Verify that the proposed partition cuts at least k edges."""
    left_side = set(left_vertices)
    if len(left_side) != len(left_vertices):
        return False
    if not left_side <= set(graph.keys()):
        return False
    return cut_size(graph, left_side) >= k


def solve_brute_force(graph: Graph, k: int) -> list[int] | None:
    """Try all partitions, fixing one vertex to remove symmetry."""
    vertices = sorted(graph.keys())
    if not vertices:
        return [] if k <= 0 else None
    anchor = vertices[0]
    others = vertices[1:]
    for size in range(len(others) + 1):
        for subset in combinations(others, size):
            candidate = [anchor] + list(subset)
            if verify_max_cut(graph, candidate, k):
                return candidate
    return None


if __name__ == "__main__":
    graph = {
        1: {2, 3, 4},
        2: {1, 3, 4},
        3: {1, 2, 4},
        4: {1, 2, 3},
    }
    k = 4
    left_side = solve_brute_force(graph, k)
    print(f"Need cut size >= {k}")
    print(f"Left side of partition: {left_side}")
    if left_side is not None:
        print(f"Cut size: {cut_size(graph, set(left_side))}")
    print(f"Verified: {verify_max_cut(graph, left_side, k) if left_side is not None else False}")
