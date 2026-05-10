"""
Feedback Vertex Set (FVS) -- NP-Complete
==========================================
Given an undirected graph G and integer k, does there exist a set of at most
k vertices whose removal makes G acyclic (a forest)?

Also called "Cycle Vertex Cover". FVS is NP-Complete for general graphs
but solvable in polynomial time for planar graphs (P).

Verifier:  Remove FVS vertices, check remaining graph is acyclic -- O(V+E).
Solver:    Brute-force over all C(V, k) subsets.
"""

from itertools import combinations


def is_acyclic(graph: dict) -> bool:
    """DFS-based cycle detection -- O(V+E)."""
    visited = set()
    rec_stack = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor == parent:
                continue
            if neighbor in visited:
                return True  # Cycle found
            if dfs(neighbor, node):
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return False
    return True


def remove_vertices(graph: dict, vertices: set) -> dict:
    return {u: [v for v in neighbors if v not in vertices]
            for u, neighbors in graph.items()
            if u not in vertices}


def verify(graph: dict, fvs: set, k: int) -> bool:
    if len(fvs) > k:
        return False
    return is_acyclic(remove_vertices(graph, fvs))


def solve(graph: dict, k: int) -> set | None:
    nodes = list(graph.keys())
    for size in range(k + 1):
        for combo in combinations(nodes, size):
            fvs = set(combo)
            if verify(graph, fvs, size):
                return fvs
    return None


if __name__ == "__main__":
    # Graph with multiple cycles
    graph = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 3],
        3: [0, 2, 5],
        4: [1, 5],
        5: [3, 4],
    }

    print("Graph (has cycles):")
    print(f"  Acyclic: {is_acyclic(graph)}")

    for k in range(len(graph)):
        fvs = solve(graph, k)
        if fvs is not None:
            print(f"\nMinimum FVS (size {k}): {sorted(fvs)}")
            remaining = remove_vertices(graph, fvs)
            print(f"Remaining graph acyclic: {is_acyclic(remaining)}")
            print(f"Verification: {verify(graph, fvs, k)}")
            break
