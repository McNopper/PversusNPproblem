"""
Graph Isomorphism
=================
Given two graphs G and H, decide whether there exists a bijection between
their vertices that preserves adjacency.

Why it is in NP:
A certificate is a vertex mapping. We can verify in polynomial time that the
mapping is a bijection and that every edge in G maps to an edge in H and vice
versa.

Special status:
Graph Isomorphism is in NP, but it is not known to be NP-Complete and it is
not known to be in P. Problems with this status are often described as
GI-complete under reductions tailored to graph isomorphism.

This file uses a brute-force permutation search for small graphs.
"""

from __future__ import annotations

from itertools import permutations
from typing import Dict, Iterable, Set

Graph = Dict[str, Set[str]]


def edge_set(graph: Graph) -> set[tuple[str, str]]:
    """Return undirected edges with endpoints stored in sorted order."""
    edges = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if u == v:
                edges.add((u, v))
            else:
                edges.add(tuple(sorted((u, v))))
    return edges


def verify_isomorphism(graph_a: Graph, graph_b: Graph, mapping: Dict[str, str]) -> bool:
    """Verify that mapping is a graph isomorphism from graph_a to graph_b."""
    if set(mapping.keys()) != set(graph_a.keys()):
        return False
    if set(mapping.values()) != set(graph_b.keys()):
        return False
    edges_a = edge_set(graph_a)
    edges_b = edge_set(graph_b)
    mapped_edges = {
        tuple(sorted((mapping[u], mapping[v])))
        for (u, v) in edges_a
    }
    return mapped_edges == edges_b


def solve_brute_force(graph_a: Graph, graph_b: Graph) -> Dict[str, str] | None:
    """Try every vertex permutation until an isomorphism is found."""
    if len(graph_a) != len(graph_b):
        return None
    degrees_a = sorted(len(graph_a[v]) for v in graph_a)
    degrees_b = sorted(len(graph_b[v]) for v in graph_b)
    if degrees_a != degrees_b:
        return None

    vertices_a = list(graph_a.keys())
    vertices_b = list(graph_b.keys())
    for perm in permutations(vertices_b):
        mapping = dict(zip(vertices_a, perm))
        if verify_isomorphism(graph_a, graph_b, mapping):
            return mapping
    return None


if __name__ == "__main__":
    graph_1 = {
        "a": {"b", "d"},
        "b": {"a", "c"},
        "c": {"b", "d"},
        "d": {"a", "c"},
    }
    graph_2 = {
        "w": {"x", "z"},
        "x": {"w", "y"},
        "y": {"x", "z"},
        "z": {"w", "y"},
    }

    mapping = solve_brute_force(graph_1, graph_2)
    print(f"Graphs are isomorphic: {mapping is not None}")
    if mapping is not None:
        print(f"Mapping found: {mapping}")
        print(f"Verified: {verify_isomorphism(graph_1, graph_2, mapping)}")
