"""
Hamiltonian Cycle Decision
==========================
Given an undirected graph, decide whether it contains a Hamiltonian cycle,
meaning a cycle that visits every vertex exactly once and returns to the
start.

Why it is in NP:
A certificate is an ordering of all vertices around the cycle. We can verify
in polynomial time that each vertex appears exactly once and each consecutive
pair, including the last and first, forms an edge.

Special status:
HAMILTONIAN CYCLE is NP-Complete.
"""

from __future__ import annotations

from typing import Dict, Set

Graph = Dict[int, Set[int]]


def verify_hamiltonian_cycle(graph: Graph, cycle: list[int]) -> bool:
    """Verify that cycle is a Hamiltonian cycle written without repeating the start."""
    if len(cycle) != len(graph) or len(set(cycle)) != len(graph):
        return False
    if set(cycle) != set(graph.keys()):
        return False
    for index, u in enumerate(cycle):
        v = cycle[(index + 1) % len(cycle)]
        if v not in graph[u]:
            return False
    return True


def solve_backtracking(graph: Graph) -> list[int] | None:
    """Search for a Hamiltonian cycle by backtracking."""
    if not graph:
        return []
    start = next(iter(graph))
    path = [start]
    used = {start}

    def backtrack() -> bool:
        if len(path) == len(graph):
            return start in graph[path[-1]]
        current = path[-1]
        for neighbor in sorted(graph[current]):
            if neighbor in used:
                continue
            used.add(neighbor)
            path.append(neighbor)
            if backtrack():
                return True
            path.pop()
            used.remove(neighbor)
        return False

    return path[:] if backtrack() else None


if __name__ == "__main__":
    graph = {
        1: {2, 4},
        2: {1, 3, 4},
        3: {2, 4},
        4: {1, 2, 3},
    }
    cycle = solve_backtracking(graph)
    print(f"Hamiltonian cycle found: {cycle}")
    print(f"Verified: {verify_hamiltonian_cycle(graph, cycle) if cycle else False}")
