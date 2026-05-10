"""
Feedback Arc Set (FAS) -- NP-Complete
=======================================
Given a directed graph G and integer k, does there exist a set of at most k
directed edges whose removal makes G acyclic (a DAG)?

Equivalent to finding the minimum number of edges to reverse to make a
tournament a DAG. Used in scheduling with cyclic dependencies.

Verifier:  Remove edges, check DAG with DFS -- O(V+E).
Solver:    Brute-force over all C(E, k) edge subsets.
"""

from itertools import combinations


def has_cycle(graph: dict) -> bool:
    """Detect cycle in directed graph using DFS coloring -- O(V+E)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}

    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(dfs(u) for u in graph if color[u] == 0)


def remove_edges(graph: dict, edges_to_remove: set) -> dict:
    result = {}
    for u, neighbors in graph.items():
        result[u] = [v for v in neighbors if (u, v) not in edges_to_remove]
    return result


def all_edges(graph: dict) -> list:
    return [(u, v) for u, neighbors in graph.items() for v in neighbors]


def verify(graph: dict, fas: set, k: int) -> bool:
    if len(fas) > k:
        return False
    return not has_cycle(remove_edges(graph, fas))


def solve(graph: dict, k: int) -> set | None:
    edges = all_edges(graph)
    for size in range(k + 1):
        for combo in combinations(edges, size):
            fas = set(combo)
            if verify(graph, fas, size):
                return fas
    return None


if __name__ == "__main__":
    # Directed graph with multiple cycles
    graph = {
        "A": ["B"],
        "B": ["C", "D"],
        "C": ["A"],        # Cycle: A->B->C->A
        "D": ["E"],
        "E": ["B"],        # Cycle: B->D->E->B
    }

    edges = all_edges(graph)
    print("Directed graph edges:")
    for u, v in edges:
        print(f"  {u} -> {v}")
    print(f"Has cycle: {has_cycle(graph)}")

    for k in range(len(edges) + 1):
        fas = solve(graph, k)
        if fas is not None:
            print(f"\nMinimum FAS (size {k}): {sorted(fas)}")
            clean = remove_edges(graph, fas)
            print(f"Remaining graph has cycle: {has_cycle(clean)}")
            print(f"Verification: {verify(graph, fas, k)}")
            break
