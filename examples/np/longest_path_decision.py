"""
Longest Path Decision
=====================
Given a graph and an integer k, decide whether the graph contains a simple
path of length at least k, where length means number of edges.

Why it is in NP:
A certificate is a path. We can verify in polynomial time that all vertices on
it are distinct, each consecutive pair is adjacent, and the path length is at
least k.

Special status:
LONGEST PATH in decision form is NP-Complete.
"""

from __future__ import annotations

from typing import Dict, Set

Graph = Dict[int, Set[int]]


def verify_longest_path(graph: Graph, path: list[int], k: int) -> bool:
    """Verify that path is simple and has at least k edges."""
    if len(path) < 1 or len(set(path)) != len(path):
        return False
    if any(vertex not in graph for vertex in path):
        return False
    for index in range(len(path) - 1):
        if path[index + 1] not in graph[path[index]]:
            return False
    return len(path) - 1 >= k


def solve_dfs(graph: Graph, k: int) -> list[int] | None:
    """Try all simple paths using DFS backtracking."""
    best: list[int] | None = None

    def dfs(node: int, path: list[int], used: set[int]) -> bool:
        nonlocal best
        if len(path) - 1 >= k:
            best = path[:]
            return True
        for neighbor in sorted(graph[node]):
            if neighbor in used:
                continue
            used.add(neighbor)
            path.append(neighbor)
            if dfs(neighbor, path, used):
                return True
            path.pop()
            used.remove(neighbor)
        return False

    for start in graph:
        if dfs(start, [start], {start}):
            return best
    return best


if __name__ == "__main__":
    graph = {
        1: {2},
        2: {1, 3, 5},
        3: {2, 4},
        4: {3, 5},
        5: {2, 4},
    }
    k = 4
    path = solve_dfs(graph, k)
    print(f"Need path length >= {k}")
    print(f"Path found: {path}")
    print(f"Verified: {verify_longest_path(graph, path, k) if path is not None else False}")
