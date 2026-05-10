"""
Steiner Tree -- NP-Complete
============================
Given a weighted graph G, a set of required terminal vertices T, and a bound B,
does there exist a subtree of G that connects all terminals with total weight <= B?

Steiner Tree generalises Minimum Spanning Tree (T = all vertices => MST, in P),
but when T is a proper subset of vertices it becomes NP-Complete.

Applications: network design, VLSI routing, phylogenetic trees.

Verifier:  Check tree connects all terminals and total weight <= B -- O(V+E).
Solver:    Brute-force over all subsets of Steiner vertices (non-terminals).
"""

from itertools import combinations


def prim_mst(nodes: set, graph: dict) -> tuple:
    """Compute MST weight over the given node subset using Prim's algorithm."""
    if not nodes:
        return 0, []
    nodes = list(nodes)
    in_tree = {nodes[0]}
    edges = []
    total = 0

    while len(in_tree) < len(nodes):
        best = (float("inf"), None, None)
        for u in in_tree:
            for v, w in graph.get(u, {}).items():
                if v in nodes and v not in in_tree:
                    if w < best[0]:
                        best = (w, u, v)
        if best[1] is None:
            return float("inf"), []  # Disconnected subgraph
        w, u, v = best
        in_tree.add(v)
        edges.append((w, u, v))
        total += w

    return total, edges


def verify(graph: dict, tree_edges: list, terminals: set, bound: float) -> bool:
    connected = set()
    for w, u, v in tree_edges:
        connected.add(u)
        connected.add(v)
    if not terminals <= connected:
        return False
    return sum(w for w, _, _ in tree_edges) <= bound


def solve(graph: dict, terminals: set, bound: float) -> tuple | None:
    all_nodes = set(graph.keys())
    steiner_candidates = all_nodes - terminals

    best_weight = float("inf")
    best_edges = None

    # Try all subsets of Steiner (non-terminal) nodes
    for size in range(len(steiner_candidates) + 1):
        for extra in combinations(steiner_candidates, size):
            node_set = terminals | set(extra)
            weight, edges = prim_mst(node_set, graph)
            if weight < best_weight:
                best_weight = weight
                best_edges = edges

    if best_weight <= bound:
        return best_edges, best_weight
    return None


if __name__ == "__main__":
    # Graph as adjacency dict: graph[u] = {v: weight}
    graph = {
        "A": {"B": 1, "C": 4, "D": 8},
        "B": {"A": 1, "C": 2, "E": 6},
        "C": {"A": 4, "B": 2, "D": 3, "E": 1},
        "D": {"A": 8, "C": 3, "E": 5},
        "E": {"B": 6, "C": 1, "D": 5},
    }

    terminals = {"A", "D", "E"}
    bound = 10

    print(f"Terminals: {sorted(terminals)}")
    print(f"All nodes: {sorted(graph.keys())}")
    print(f"Weight bound: {bound}")

    result = solve(graph, terminals, bound)
    if result:
        edges, weight = result
        print(f"\nSteiner tree found (weight {weight}):")
        for w, u, v in sorted(edges):
            print(f"  {u} -- {v}  (weight {w})")
        print(f"Verification: {verify(graph, edges, terminals, bound)}")
    else:
        print(f"\nNo Steiner tree with weight <= {bound} found.")
