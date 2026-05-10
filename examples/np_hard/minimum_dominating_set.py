"""
Minimum Dominating Set -- NP-Hard optimization
==============================================
Given an undirected graph, find the smallest set of vertices such that every
vertex is either in the set or adjacent to a vertex in the set.

Why NP-Hard:
- The decision version asks whether there exists a dominating set of size at
  most k.
- That decision problem is NP-Complete.
- Therefore, the optimization version is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because domination can be checked in
  polynomial time.

Key properties:
- Dominating set generalizes many facility-location style tasks.
- Greedy algorithms give logarithmic-factor approximations for the equivalent
  set cover view.
- Exact search is exponential.

This module includes:
- A brute-force exact solver.
- A greedy approximation inspired by set cover.
"""

from itertools import combinations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def dominates(graph, subset):
    dominated = set(subset)
    for v in subset:
        dominated.update(graph[v])
    return dominated >= set(graph)


def brute_force_minimum_dominating_set(graph):
    vertices = list(graph)
    for size in range(len(vertices) + 1):
        for subset in combinations(vertices, size):
            if dominates(graph, subset):
                return list(subset)
    return vertices


def greedy_dominating_set(graph):
    undominated = set(graph)
    chosen = []
    while undominated:
        best = max(
            graph,
            key=lambda v: (len(({v} | graph[v]) & undominated), -len(chosen), str(v)),
        )
        chosen.append(best)
        undominated -= {best} | graph[best]
    return chosen


def format_set(items):
    return "{" + ", ".join(str(x) for x in items) + "}"


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C"},
            "B": {"A", "D", "E"},
            "C": {"A", "F"},
            "D": {"B"},
            "E": {"B", "F", "G"},
            "F": {"C", "E", "H"},
            "G": {"E"},
            "H": {"F"},
        }
    )

    exact = brute_force_minimum_dominating_set(graph)
    greedy = greedy_dominating_set(graph)

    print("Minimum Dominating Set (NP-Hard)")
    print(f"Exact set:        {format_set(exact)} (size {len(exact)})")
    print(f"Greedy heuristic: {format_set(greedy)} (size {len(greedy)})")
