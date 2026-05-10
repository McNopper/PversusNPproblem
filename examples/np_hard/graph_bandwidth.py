"""
Graph Bandwidth -- NP-Hard optimization
=======================================
Given an undirected graph, assign distinct labels 1..n to the vertices so that
max |label(u) - label(v)| over all edges is as small as possible.

Why NP-Hard:
- The decision version asks whether a labeling exists with bandwidth at most B.
- That problem is NP-Complete.
- Therefore, computing the minimum bandwidth is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because we can check the maximum edge span of a
  proposed labeling in polynomial time.

Key properties:
- Bandwidth models placing related items close together on a line.
- Exact search tries all n! labelings in the worst case.
- BFS-based orderings often do well on sparse graphs.

This module includes:
- A brute-force exact solver.
- A greedy BFS heuristic that tries all start vertices.
"""

from collections import deque
from itertools import permutations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def bandwidth_of_order(order, graph):
    position = {vertex: i for i, vertex in enumerate(order)}
    best = 0
    for u in graph:
        for v in graph[u]:
            if str(u) < str(v):
                best = max(best, abs(position[u] - position[v]))
    return best


def brute_force_graph_bandwidth(graph):
    vertices = list(graph)
    best_order = None
    best_value = float("inf")
    for order in permutations(vertices):
        value = bandwidth_of_order(order, graph)
        if value < best_value:
            best_value = value
            best_order = list(order)
    return best_order, best_value


def bfs_order_from_start(graph, start):
    seen = {start}
    order = []
    queue = deque([start])
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in sorted(graph[v], key=lambda node: (len(graph[node]), str(node))):
            if u not in seen:
                seen.add(u)
                queue.append(u)
    for v in sorted(graph):
        if v not in seen:
            order.append(v)
    return order


def bfs_bandwidth_heuristic(graph):
    best_order = None
    best_value = float("inf")
    for start in graph:
        order = bfs_order_from_start(graph, start)
        value = bandwidth_of_order(order, graph)
        if value < best_value:
            best_value = value
            best_order = order
    return best_order, best_value


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C"},
            "B": {"A", "D", "E"},
            "C": {"A", "F"},
            "D": {"B", "G"},
            "E": {"B", "H"},
            "F": {"C", "I"},
            "G": {"D"},
            "H": {"E"},
            "I": {"F"},
        }
    )

    exact_order, exact_value = brute_force_graph_bandwidth(graph)
    heuristic_order, heuristic_value = bfs_bandwidth_heuristic(graph)

    print("Graph Bandwidth (NP-Hard)")
    print(f"Exact order:      {exact_order}, bandwidth = {exact_value}")
    print(f"BFS heuristic:    {heuristic_order}, bandwidth = {heuristic_value}")
