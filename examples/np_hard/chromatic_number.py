"""
Chromatic Number -- NP-Hard optimization
========================================
Given an undirected graph, find the minimum number of colors needed so that
adjacent vertices receive different colors.

Why NP-Hard:
- The decision version asks whether a graph is k-colorable.
- For k >= 3, that decision problem is NP-Complete.
- Therefore, computing the chromatic number is NP-Hard.

Is it in NP?
- The optimization problem itself is not a decision language.
- The decision version is in NP because a coloring can be checked quickly.

Key properties:
- Bipartite graphs have chromatic number 2 unless edgeless.
- Complete graphs on n vertices need n colors.
- Exact graph coloring is usually attacked with backtracking and pruning.

This module includes:
- An exact backtracking search for the chromatic number.
- A greedy coloring that provides a fast upper bound.
"""


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def greedy_coloring(graph):
    order = sorted(graph, key=lambda v: (-len(graph[v]), str(v)))
    coloring = {}
    for v in order:
        used = {coloring[u] for u in graph[v] if u in coloring}
        color = 0
        while color in used:
            color += 1
        coloring[v] = color
    return coloring


def can_color_with_k(graph, k):
    order = sorted(graph, key=lambda v: (-len(graph[v]), str(v)))
    coloring = {}

    def backtrack(index):
        if index == len(order):
            return True
        v = order[index]
        forbidden = {coloring[u] for u in graph[v] if u in coloring}
        for color in range(k):
            if color not in forbidden:
                coloring[v] = color
                if backtrack(index + 1):
                    return True
                del coloring[v]
        return False

    success = backtrack(0)
    return success, dict(coloring)


def exact_chromatic_number(graph):
    upper = 1 + max((len(neighbors) for neighbors in graph.values()), default=0)
    upper = min(upper, len(graph))
    greedy = greedy_coloring(graph)
    upper = min(upper, 1 + max(greedy.values(), default=-1))
    best_coloring = greedy
    for k in range(1, upper + 1):
        success, coloring = can_color_with_k(graph, k)
        if success:
            return k, coloring
    return 1 + max(greedy.values(), default=-1), greedy


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C", "D"},
            "B": {"A", "C", "E"},
            "C": {"A", "B", "D", "E"},
            "D": {"A", "C", "E"},
            "E": {"B", "C", "D"},
        }
    )

    greedy = greedy_coloring(graph)
    exact_value, exact_coloring = exact_chromatic_number(graph)

    print("Chromatic Number (NP-Hard)")
    print(f"Greedy colors used: {1 + max(greedy.values())}")
    print(f"Greedy coloring:    {greedy}")
    print(f"Exact value:        {exact_value}")
    print(f"Exact coloring:     {exact_coloring}")
