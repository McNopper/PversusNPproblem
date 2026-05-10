"""
Max Flow (P) vs Multi-Commodity Flow (NP-Hard)
==============================================
Max Flow:            Find maximum flow from source to sink in a network.
                     Solvable in O(VE^2) via Edmonds-Karp -- in P.

Multi-Commodity Flow: Multiple source-sink pairs sharing the same network.
                     The FRACTIONAL version is in P (LP), but the INTEGER
                     version (each unit of flow is indivisible) is NP-Hard.

Used in: telecommunications, logistics, VLSI routing, airline scheduling.
"""

from collections import defaultdict, deque


# ── Single Commodity Max Flow -- Edmonds-Karp (Polynomial) ────────────────────

def edmonds_karp(capacity: dict, source, sink) -> tuple:
    """
    O(VE^2) max flow.
    capacity: {u: {v: cap}} dict.
    Returns (max_flow, flow_dict).
    """
    flow = defaultdict(lambda: defaultdict(int))
    max_flow = 0

    while True:
        # BFS for augmenting path
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, cap in capacity.get(u, {}).items():
                if v not in parent and cap - flow[u][v] > 0:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break

        # Find bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u].get(v, 0) - flow[u][v])
            v = u

        # Augment
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
        max_flow += path_flow

    return max_flow, flow


# ── Integer Multi-Commodity Flow (NP-Hard -- brute force for tiny instances) ──

def integer_multicommodity_brute(graph: dict, commodities: list) -> list | None:
    """
    Each commodity is (source, sink, demand).
    Try to route each demand as indivisible integer units.
    Brute force over simple paths -- exponential.
    """
    from itertools import product as iproduct

    def find_paths(graph, src, dst, visited=None):
        if visited is None:
            visited = set()
        if src == dst:
            return [[dst]]
        visited = visited | {src}
        paths = []
        for nb in graph.get(src, []):
            if nb not in visited:
                for p in find_paths(graph, nb, dst, visited):
                    paths.append([src] + p)
        return paths

    # Collect all simple paths for each commodity
    all_paths = []
    for src, dst, demand in commodities:
        paths = find_paths(graph, src, dst)
        if not paths:
            return None
        all_paths.append((demand, paths))

    # Try all combinations of paths
    path_combinations = iproduct(*[p[1] for p in all_paths])
    for combo in path_combinations:
        # Check edge capacity constraints
        edge_use = defaultdict(int)
        for path in combo:
            for i in range(len(path) - 1):
                edge_use[(path[i], path[i+1])] += 1
        cap = graph.get("_capacity", {})
        if all(edge_use[e] <= cap.get(e, float("inf")) for e in edge_use):
            return [{"path": p, "commodity": i} for i, p in enumerate(combo)]

    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Single commodity max flow
    capacity = {
        "S": {"A": 10, "B": 10},
        "A": {"C":  8, "D":  5},
        "B": {"C":  5, "D":  8},
        "C": {"T": 10},
        "D": {"T": 10},
        "T": {},
    }

    flow_val, _ = edmonds_karp(capacity, "S", "T")
    print("Single-commodity max flow (Edmonds-Karp, O(VE^2)):")
    print(f"  Max flow S -> T: {flow_val}")

    # Multi-commodity: two flows sharing edges, integer routing
    # Simple network: A-B-C-D, edges A-B, A-C, B-D, C-D with capacity 1 each
    network = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C"],
        "_capacity": {("A","B"):1, ("A","C"):1, ("B","D"):1, ("C","D"):1}
    }
    commodities = [
        ("A", "D", 1),  # Route 1 unit from A to D
        ("A", "D", 1),  # Route another unit from A to D (must use different path)
    ]

    result = integer_multicommodity_brute(network, commodities)
    print("\nInteger multi-commodity flow (NP-Hard, brute force):")
    if result:
        for r in result:
            print(f"  Commodity {r['commodity']}: {' -> '.join(r['path'])}")
    else:
        print("  No feasible integer routing found.")

    print("\nKey insight:")
    print("  Max flow (single commodity)              -- O(VE^2), in P")
    print("  Multi-commodity flow (fractional)        -- LP-based, in P")
    print("  Multi-commodity flow (integer units)     -- NP-Hard")
