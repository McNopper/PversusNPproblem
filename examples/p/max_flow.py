"""
Maximum Flow - Class P
======================
The Edmonds-Karp algorithm solves the maximum flow problem by repeatedly using
BFS to find the shortest augmenting path in the residual network. It is a
specific implementation of Ford-Fulkerson.

This problem is in P because Edmonds-Karp runs in O(VE^2) time, which is
polynomial in the size of the graph.
"""

from collections import deque


Graph = dict[str, dict[str, int]]


def _build_residual(capacity: Graph) -> Graph:
    """Create a residual graph with forward and reverse edges."""
    residual: Graph = {}

    for u, edges in capacity.items():
        residual.setdefault(u, {})
        for v, cap in edges.items():
            residual.setdefault(v, {})
            residual[u][v] = cap
            residual[v].setdefault(u, 0)

    return residual


def _bfs_augmenting_path(residual: Graph, source: str, sink: str) -> dict[str, str] | None:
    """Find a shortest augmenting path in the residual graph."""
    queue = deque([source])
    parent: dict[str, str | None] = {source: None}

    while queue:
        u = queue.popleft()
        for v, remaining in residual[u].items():
            if remaining <= 0 or v in parent:
                continue
            parent[v] = u
            if v == sink:
                return {node: prev for node, prev in parent.items() if prev is not None}
            queue.append(v)

    return None


def edmonds_karp(capacity: Graph, source: str, sink: str) -> tuple[int, Graph]:
    """Return the maximum flow value and the final residual network."""
    residual = _build_residual(capacity)
    max_flow_value = 0

    while True:
        parent = _bfs_augmenting_path(residual, source, sink)
        if parent is None:
            break

        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u

        max_flow_value += int(path_flow)

    return max_flow_value, residual


if __name__ == "__main__":
    capacity_graph = {
        "s": {"a": 10, "c": 10},
        "a": {"b": 4, "c": 2, "d": 8},
        "b": {"t": 10},
        "c": {"d": 9},
        "d": {"b": 6, "t": 10},
        "t": {},
    }

    value, residual_graph = edmonds_karp(capacity_graph, "s", "t")
    print(f"Maximum flow from s to t: {value}")
    print(f"Residual capacity on edge d -> t: {residual_graph['d']['t']}")
