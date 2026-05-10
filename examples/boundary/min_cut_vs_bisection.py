"""
Minimum Cut (P) vs Minimum Bisection (NP-Hard)
===============================================
Minimum Cut: find a partition of vertices minimizing the number of crossing
             edges, with NO constraint on partition sizes.
             Solvable in O(VE log(V^2/E)) via max-flow/min-cut (P).

Minimum Bisection: same goal but BOTH halves must have equal size n/2.
             Adding the balance constraint makes it NP-Hard.

This is a striking example of how a single constraint can change a P problem
into an NP-Hard one.
"""

from collections import defaultdict, deque


# ── Min Cut via Max Flow (Polynomial) ────────────────────────────────────────

def bfs_path(graph, source, sink, parent):
    """BFS to find augmenting path in residual graph."""
    visited = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited and graph[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False


def edmonds_karp(graph: dict, source, sink) -> tuple:
    """
    Edmonds-Karp max flow O(VE^2), then find min cut via BFS on residual.
    Returns (max_flow, set of source-side vertices in min cut).
    """
    # Deep copy graph as residual
    residual = {u: dict(v_cap) for u, v_cap in graph.items()}
    for u in list(residual):
        for v in list(residual[u]):
            if v not in residual:
                residual[v] = {}
            residual[v].setdefault(u, 0)

    max_flow = 0
    while True:
        parent = {}
        if not bfs_path(residual, source, sink, parent):
            break
        # Find min capacity along path
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        # Update residual
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        max_flow += path_flow

    # Find source side via BFS on residual
    visited = set()
    queue = deque([source])
    visited.add(source)
    while queue:
        u = queue.popleft()
        for v, cap in residual[u].items():
            if v not in visited and cap > 0:
                visited.add(v)
                queue.append(v)

    return max_flow, visited


# ── Minimum Bisection (NP-Hard, brute force) ──────────────────────────────────

from itertools import combinations


def min_bisection_brute(graph: dict) -> tuple:
    """
    Find the equal partition minimizing cut edges -- O(C(V, V/2)).
    NP-Hard: no known polynomial algorithm for general graphs.
    """
    nodes = list(graph.keys())
    n = len(nodes)
    half = n // 2
    best_cut = float("inf")
    best_partition = None

    for subset in combinations(nodes, half):
        s = set(subset)
        cut = sum(1 for u in s for v in graph[u] if v not in s)
        if cut < best_cut:
            best_cut = cut
            best_partition = s

    return best_cut, best_partition


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Graph with capacities for max-flow
    flow_graph = {
        "S": {"A": 10, "B": 10},
        "A": {"C": 10, "B": 2},
        "B": {"D": 10},
        "C": {"T": 10},
        "D": {"T": 10},
        "T": {},
    }

    flow, source_side = edmonds_karp(flow_graph, "S", "T")
    sink_side = set(flow_graph) - source_side
    print("Min Cut (Polynomial -- max-flow/min-cut theorem):")
    print(f"  Max flow = min cut = {flow}")
    print(f"  Source side: {sorted(source_side)}")
    print(f"  Sink side:   {sorted(sink_side)}")

    # Unweighted graph for bisection
    graph = {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 5],
        3: [0, 4, 5],
        4: [1, 3, 5],
        5: [2, 3, 4],
    }

    cut, partition = min_bisection_brute(graph)
    complement = set(graph) - partition
    print("\nMin Bisection (NP-Hard -- brute force):")
    print(f"  Cut size: {cut}")
    print(f"  Partition A: {sorted(partition)}")
    print(f"  Partition B: {sorted(complement)}")

    print("\nKey insight:")
    print("  Min Cut (unconstrained)   -- O(VE^2), in P via max-flow")
    print("  Min Bisection (equal size) -- NP-Hard, no known poly algorithm")
