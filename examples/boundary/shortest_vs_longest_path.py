"""
Shortest Path (P) vs Longest Path (NP-Hard)
============================================
Shortest path between two vertices: solvable in O((V+E) log V) -- in P.
Longest SIMPLE path: NP-Hard for general graphs.

Exception: in a DAG (Directed Acyclic Graph), BOTH shortest and longest
paths are solvable in O(V+E) via dynamic programming -- because there are
no cycles to worry about.

This file shows all three algorithms side by side.
"""

import heapq


# ── Shortest Path -- Dijkstra (Polynomial) ────────────────────────────────────

def dijkstra(graph: dict, src) -> dict:
    """Dijkstra's O((V+E) log V) shortest path from src."""
    dist = {v: float("inf") for v in graph}
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist


# ── DAG Longest Path (Polynomial for DAGs only) ───────────────────────────────

def dag_longest_path(graph: dict, src) -> dict:
    """Longest path in a DAG via DP + topological sort -- O(V+E)."""
    # Kahn's topological sort
    in_degree = {v: 0 for v in graph}
    for u in graph:
        for v, _ in graph[u]:
            in_degree[v] += 1
    from collections import deque
    queue = deque(v for v in in_degree if in_degree[v] == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, _ in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    dist = {v: float("-inf") for v in graph}
    dist[src] = 0
    for u in topo:
        if dist[u] == float("-inf"):
            continue
        for v, w in graph[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
    return dist


# ── Longest Path in General Graph (NP-Hard, brute force) ─────────────────────

def longest_path_general(adj: dict, src, dst) -> tuple:
    """
    Brute-force longest simple path via backtracking -- O(V!).
    Returns (length, path).
    """
    best = {"len": -1, "path": []}

    def dfs(node, path, visited, length):
        if node == dst and length > best["len"]:
            best["len"] = length
            best["path"] = list(path)
        for nb, w in adj[node]:
            if nb not in visited:
                visited.add(nb)
                path.append(nb)
                dfs(nb, path, visited, length + w)
                path.pop()
                visited.remove(nb)

    dfs(src, [src], {src}, 0)
    return best["len"], best["path"]


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # DAG (directed, no cycles)
    dag = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }

    print("=== DAG: both shortest and longest path in O(V+E) ===")
    short = dijkstra(dag, "A")
    long_ = dag_longest_path(dag, "A")
    print(f"  Shortest from A: { {k: v for k, v in short.items()} }")
    print(f"  Longest  from A: { {k: v for k, v in long_.items() if v != float('-inf')} }")

    # General graph (undirected, has cycles)
    general = {
        "A": [("B", 1), ("C", 4), ("D", 2)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 1)],
        "D": [("A", 2), ("B", 5), ("C", 1)],
    }

    print("\n=== General graph: shortest in P, longest NP-Hard ===")
    short2 = dijkstra(general, "A")
    print(f"  Shortest from A (Dijkstra, O((V+E)logV)): { {k: v for k, v in short2.items()} }")

    length, path = longest_path_general(general, "A", "D")
    print(f"  Longest A->D (brute force O(V!)): length={length}, path={' -> '.join(path)}")

    print("\nKey insight:")
    print("  Shortest path (general graph) -- O((V+E)logV), in P")
    print("  Longest  path (DAG only)      -- O(V+E), in P")
    print("  Longest  path (general graph) -- NP-Hard, no known poly algorithm")
