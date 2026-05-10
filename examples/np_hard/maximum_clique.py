"""
Maximum Clique -- NP-Hard optimization
=====================================
Given an undirected graph, find the largest subset of vertices such that every
pair in the subset is connected by an edge.

Why NP-Hard:
- The decision version asks whether there is a clique of size at least k.
- That decision problem is NP-Complete.
- Therefore, the optimization problem of finding the largest clique is NP-Hard.

Is it in NP?
- The optimization problem itself is not usually classified as a language in NP.
- Its associated decision version is in NP because a proposed clique can be
  checked in polynomial time.

Key properties:
- A clique in G is an independent set in the complement of G.
- Clique is one of Karp's original NP-Complete problems.
- Exact algorithms are exponential in the worst case.

This module includes:
- A brute-force exact solver.
- A simple greedy heuristic based on high-degree vertices.
"""

from itertools import combinations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def is_clique(vertices, graph):
    for u, v in combinations(vertices, 2):
        if v not in graph[u]:
            return False
    return True


def brute_force_maximum_clique(graph):
    """Exact exponential solver: try all subsets from largest to smallest."""
    vertices = list(graph)
    for size in range(len(vertices), 0, -1):
        for subset in combinations(vertices, size):
            if is_clique(subset, graph):
                return list(subset)
    return []


def greedy_maximum_clique(graph):
    """Greedy heuristic: build a clique from each high-degree starting point."""
    vertices = sorted(graph, key=lambda v: (-len(graph[v]), str(v)))
    best = []
    for start in vertices:
        clique = [start]
        candidates = sorted(graph[start], key=lambda v: (-len(graph[v]), str(v)))
        for v in candidates:
            if all(v in graph[u] for u in clique):
                clique.append(v)
        if len(clique) > len(best):
            best = clique
    return best


def format_set(items):
    return "{" + ", ".join(str(x) for x in items) + "}"


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C", "D"},
            "B": {"A", "C", "D", "E"},
            "C": {"A", "B", "D", "F"},
            "D": {"A", "B", "C", "E"},
            "E": {"B", "D", "F"},
            "F": {"C", "E"},
        }
    )

    exact = brute_force_maximum_clique(graph)
    heuristic = greedy_maximum_clique(graph)

    print("Maximum Clique (NP-Hard)")
    print(f"Exact clique:     {format_set(exact)} (size {len(exact)})")
    print(f"Greedy heuristic: {format_set(heuristic)} (size {len(heuristic)})")
