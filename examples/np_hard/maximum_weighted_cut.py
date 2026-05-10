"""
Maximum Weighted Cut -- NP-Hard optimization
============================================
Given a weighted undirected graph, partition the vertices into two sides so that
the total weight of edges crossing the partition is as large as possible.

Why NP-Hard:
- The decision version asks whether there is a cut of weight at least K.
- That decision problem is NP-Complete.
- Therefore, maximizing cut weight is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because a cut value can be checked in
  polynomial time.

Key properties:
- MAX-CUT has strong approximation algorithms; random assignment gives a 1/2
  approximation in expectation.
- Local search is often effective in practice.
- Exact search is exponential.

This module includes:
- A brute-force exact solver.
- A greedy local-search heuristic.
"""

from itertools import product


def cut_weight(vertices, edges, side_a):
    side_a = set(side_a)
    total = 0
    for u, v, w in edges:
        if (u in side_a) != (v in side_a):
            total += w
    return total


def brute_force_max_cut(vertices, edges):
    vertices = list(vertices)
    anchor = vertices[0]
    best_side = {anchor}
    best_value = -1
    for bits in product([0, 1], repeat=len(vertices) - 1):
        side_a = {anchor}
        for bit, vertex in zip(bits, vertices[1:]):
            if bit:
                side_a.add(vertex)
        value = cut_weight(vertices, edges, side_a)
        if value > best_value:
            best_value = value
            best_side = side_a
    return best_side, best_value


def greedy_local_search(vertices, edges):
    vertices = list(vertices)
    side_a = set(vertices[::2])
    improved = True
    while improved:
        improved = False
        for v in vertices:
            current = cut_weight(vertices, edges, side_a)
            if v in side_a:
                candidate = set(side_a)
                candidate.remove(v)
            else:
                candidate = set(side_a)
                candidate.add(v)
            new_value = cut_weight(vertices, edges, candidate)
            if new_value > current:
                side_a = candidate
                improved = True
    return side_a, cut_weight(vertices, edges, side_a)


def side_b(vertices, side_a):
    return sorted(set(vertices) - set(side_a))


if __name__ == "__main__":
    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 6),
        ("C", "D", 3),
        ("C", "E", 5),
        ("D", "E", 2),
    ]

    exact_side, exact_value = brute_force_max_cut(vertices, edges)
    heuristic_side, heuristic_value = greedy_local_search(vertices, edges)

    print("Maximum Weighted Cut (NP-Hard)")
    print(f"Exact cut:     A={sorted(exact_side)}, B={side_b(vertices, exact_side)}, weight={exact_value}")
    print(f"Heuristic cut: A={sorted(heuristic_side)}, B={side_b(vertices, heuristic_side)}, weight={heuristic_value}")
