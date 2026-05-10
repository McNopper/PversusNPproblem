"""
Steiner Tree Decision
=====================
Given a weighted undirected graph, a set of terminal vertices, and a budget B,
decide whether there exists a tree of total weight at most B that connects all
terminals. The tree may include extra non-terminal Steiner vertices.

Why it is in NP:
A certificate is a set of graph edges. We can verify in polynomial time that
these edges exist in the graph, form a tree, connect all terminals, and have
total weight at most B.

Special status:
The decision version of STEINER TREE is NP-Complete.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict

WeightedGraph = Dict[str, Dict[str, int]]


def unique_edges(graph: WeightedGraph) -> list[tuple[str, str, int]]:
    """Return each undirected weighted edge once."""
    edges = []
    for u, neighbors in graph.items():
        for v, weight in neighbors.items():
            if u < v:
                edges.append((u, v, weight))
    return edges


def verify_steiner_tree(graph: WeightedGraph, terminals: set[str], chosen_edges: list[tuple[str, str]], budget: int) -> bool:
    """Verify that chosen_edges forms a Steiner tree within the given budget."""
    seen = set()
    adjacency: dict[str, set[str]] = {}
    total_weight = 0
    for u, v in chosen_edges:
        edge = tuple(sorted((u, v)))
        if edge in seen:
            return False
        seen.add(edge)
        if u not in graph or v not in graph[u]:
            return False
        total_weight += graph[u][v]
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    if total_weight > budget:
        return False
    if not terminals:
        return True
    if not terminals <= set(adjacency.keys()):
        return False
    vertices = set(adjacency.keys())
    if len(chosen_edges) != len(vertices) - 1:
        return False
    start = next(iter(terminals))
    stack = [start]
    seen_vertices = set()
    while stack:
        node = stack.pop()
        if node in seen_vertices:
            continue
        seen_vertices.add(node)
        stack.extend(adjacency.get(node, ()))
    return terminals <= seen_vertices and seen_vertices == vertices


def solve_brute_force(graph: WeightedGraph, terminals: set[str], budget: int) -> list[tuple[str, str]] | None:
    """Try every edge subset until a valid Steiner tree is found."""
    edges = unique_edges(graph)
    for size in range(max(0, len(terminals) - 1), len(edges) + 1):
        for subset in combinations(edges, size):
            chosen = [(u, v) for u, v, _weight in subset]
            if verify_steiner_tree(graph, terminals, chosen, budget):
                return chosen
    return None


if __name__ == "__main__":
    graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "C": 2, "D": 5},
        "C": {"A": 4, "B": 2, "D": 1},
        "D": {"B": 5, "C": 1},
    }
    terminals = {"A", "D"}
    budget = 4
    tree = solve_brute_force(graph, terminals, budget)
    print(f"Terminals: {sorted(terminals)}")
    print(f"Budget: {budget}")
    print(f"Chosen edges: {tree}")
    print(f"Verified: {verify_steiner_tree(graph, terminals, tree, budget) if tree is not None else False}")
