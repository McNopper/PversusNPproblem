"""
Maximum Independent Set -- NP-Hard optimization
===============================================
Given an undirected graph, find the largest subset of vertices such that no two
chosen vertices are adjacent.

Why NP-Hard:
- The decision version asks whether there is an independent set of size at
  least k.
- That problem is NP-Complete.
- Therefore, the optimization version is NP-Hard.

Is it in NP?
- The optimization problem is not itself a decision language.
- The decision version is in NP because a proposed set can be verified quickly.

Key properties:
- An independent set in G is a clique in the complement graph.
- Maximum independent set is a canonical hard graph optimization problem.
- Exact algorithms are exponential in the worst case.

This module includes:
- A brute-force exact solver.
- A greedy heuristic that repeatedly picks a low-degree vertex.
"""

from itertools import combinations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def is_independent_set(vertices, graph):
    for u, v in combinations(vertices, 2):
        if v in graph[u]:
            return False
    return True


def brute_force_maximum_independent_set(graph):
    vertices = list(graph)
    for size in range(len(vertices), 0, -1):
        for subset in combinations(vertices, size):
            if is_independent_set(subset, graph):
                return list(subset)
    return []


def greedy_independent_set(graph):
    remaining = {v: set(neighbors) for v, neighbors in graph.items()}
    chosen = []
    while remaining:
        v = min(remaining, key=lambda node: (len(remaining[node]), str(node)))
        chosen.append(v)
        forbidden = remaining[v] | {v}
        for node in list(forbidden):
            if node in remaining:
                del remaining[node]
        for neighbors in remaining.values():
            neighbors.difference_update(forbidden)
    return chosen


def format_set(items):
    return "{" + ", ".join(str(x) for x in items) + "}"


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C"},
            "B": {"A", "D", "E"},
            "C": {"A", "D"},
            "D": {"B", "C", "F"},
            "E": {"B", "F"},
            "F": {"D", "E"},
        }
    )

    exact = brute_force_maximum_independent_set(graph)
    heuristic = greedy_independent_set(graph)

    print("Maximum Independent Set (NP-Hard)")
    print(f"Exact set:        {format_set(exact)} (size {len(exact)})")
    print(f"Greedy heuristic: {format_set(heuristic)} (size {len(heuristic)})")
