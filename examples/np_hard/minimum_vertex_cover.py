"""
Minimum Vertex Cover -- NP-Hard optimization
===========================================
Given an undirected graph, find the smallest set of vertices that touches every
edge.

Why NP-Hard:
- The decision version asks whether there exists a vertex cover of size at most
  k.
- That problem is NP-Complete.
- Therefore, minimizing the size of the cover is NP-Hard.

Is it in NP?
- The optimization problem is not itself a decision language.
- The decision version is in NP because we can verify that every edge is
  covered in polynomial time.

Key properties:
- Vertex cover is the complement of independent set: V minus C is independent.
- There is a classic 2-approximation using any maximal matching.
- Exact search is exponential.

This module includes:
- A brute-force exact solver.
- A 2-approximation built from a greedy maximal matching.
"""

from itertools import combinations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def edge_list(graph):
    edges = []
    for u in graph:
        for v in graph[u]:
            if str(u) < str(v):
                edges.append((u, v))
    return edges


def is_vertex_cover(vertices, edges):
    chosen = set(vertices)
    return all(u in chosen or v in chosen for u, v in edges)


def brute_force_minimum_vertex_cover(graph):
    edges = edge_list(graph)
    vertices = list(graph)
    for size in range(len(vertices) + 1):
        for subset in combinations(vertices, size):
            if is_vertex_cover(subset, edges):
                return list(subset)
    return vertices


def maximal_matching_2_approx(graph):
    uncovered = set(edge_list(graph))
    cover = set()
    while uncovered:
        u, v = next(iter(uncovered))
        cover.add(u)
        cover.add(v)
        uncovered = {
            edge for edge in uncovered if u not in edge and v not in edge
        }
    return sorted(cover)


def format_set(items):
    return "{" + ", ".join(str(x) for x in items) + "}"


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C"},
            "B": {"A", "C", "D"},
            "C": {"A", "B", "E"},
            "D": {"B", "E"},
            "E": {"C", "D", "F"},
            "F": {"E"},
        }
    )

    exact = brute_force_minimum_vertex_cover(graph)
    approx = maximal_matching_2_approx(graph)

    print("Minimum Vertex Cover (NP-Hard)")
    print(f"Exact cover:      {format_set(exact)} (size {len(exact)})")
    print(f"2-approx cover:   {format_set(approx)} (size {len(approx)})")
