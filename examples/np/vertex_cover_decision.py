"""
Vertex Cover Decision
=====================
Given an undirected graph and an integer k, decide whether there exists a
vertex cover of size at most k.

Why it is in NP:
A certificate is a set of at most k vertices. We can verify in polynomial time
that every edge has at least one endpoint in the certificate.

Special status:
VERTEX COVER is NP-Complete.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Set

Graph = Dict[int, Set[int]]


def edge_list(graph: Graph) -> list[tuple[int, int]]:
    """Return undirected edges without duplicates."""
    edges = []
    for u, neighbors in graph.items():
        for v in neighbors:
            if u < v:
                edges.append((u, v))
    return edges


def verify_vertex_cover(graph: Graph, cover: list[int], k: int) -> bool:
    """Verify that cover has size at most k and touches every edge."""
    cover_set = set(cover)
    if len(cover) != len(cover_set) or len(cover_set) > k:
        return False
    if any(v not in graph for v in cover_set):
        return False
    for u, v in edge_list(graph):
        if u not in cover_set and v not in cover_set:
            return False
    return True


def solve_brute_force(graph: Graph, k: int) -> list[int] | None:
    """Try every subset of size up to k."""
    vertices = list(graph.keys())
    for size in range(k + 1):
        for subset in combinations(vertices, size):
            candidate = list(subset)
            if verify_vertex_cover(graph, candidate, k):
                return candidate
    return None


if __name__ == "__main__":
    graph = {
        1: {2, 3},
        2: {1, 3, 4},
        3: {1, 2, 4},
        4: {2, 3},
    }
    k = 2
    cover = solve_brute_force(graph, k)
    print(f"k = {k}")
    print(f"Vertex cover found: {cover}")
    print(f"Verified: {verify_vertex_cover(graph, cover, k) if cover is not None else False}")
