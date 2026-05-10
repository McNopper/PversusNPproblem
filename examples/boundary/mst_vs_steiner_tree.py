"""
Minimum Spanning Tree (P) vs Steiner Tree (NP-Complete)
========================================================
MST:         Connect ALL vertices with minimum total edge weight.
             Solvable in O(E log E) via Kruskal's algorithm -- in P.

Steiner Tree: Connect a SUBSET of terminal vertices with minimum weight,
             using optional Steiner points (non-terminals).
             NP-Complete -- reducing the set of required nodes adds hardness.

When terminals = all vertices: Steiner Tree = MST (reduces to P).
When terminals is a strict subset: NP-Complete.
"""

from itertools import combinations


# ── MST via Kruskal (Polynomial) ─────────────────────────────────────────────

class UnionFind:
    def __init__(self, nodes):
        self.p = {n: n for n in nodes}
        self.r = {n: 0 for n in nodes}

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.r[rx] < self.r[ry]:
            rx, ry = ry, rx
        self.p[ry] = rx
        if self.r[rx] == self.r[ry]:
            self.r[rx] += 1
        return True


def kruskal_mst(nodes, edges):
    """O(E log E) MST. edges: list of (weight, u, v)."""
    uf = UnionFind(nodes)
    mst, total = [], 0
    for w, u, v in sorted(edges):
        if uf.union(u, v):
            mst.append((w, u, v))
            total += w
    return mst, total


# ── Steiner Tree (NP-Complete, brute force) ───────────────────────────────────

def prim_on_subset(nodes_subset, adj):
    """Prim's MST restricted to a node subset."""
    nodes = list(nodes_subset)
    if not nodes:
        return 0, []
    in_tree = {nodes[0]}
    edges, total = [], 0
    while len(in_tree) < len(nodes):
        best = (float("inf"), None, None)
        for u in in_tree:
            for v, w in adj.get(u, {}).items():
                if v in nodes_subset and v not in in_tree and w < best[0]:
                    best = (w, u, v)
        if best[1] is None:
            return float("inf"), []
        w, u, v = best
        in_tree.add(v)
        edges.append((w, u, v))
        total += w
    return total, edges


def steiner_tree_brute(terminals, all_nodes, adj):
    """
    Brute force: try all subsets of non-terminal (Steiner) nodes.
    For each subset S, compute MST on terminals UNION S.
    """
    steiner_pts = [n for n in all_nodes if n not in terminals]
    best_w, best_edges, best_extra = float("inf"), [], []

    for size in range(len(steiner_pts) + 1):
        for extra in combinations(steiner_pts, size):
            node_set = set(terminals) | set(extra)
            w, edges = prim_on_subset(node_set, adj)
            if w < best_w:
                best_w = w
                best_edges = edges
                best_extra = list(extra)

    return best_w, best_edges, best_extra


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    all_nodes = list("ABCDE")
    edges = [(1,"A","B"),(4,"A","C"),(3,"B","C"),(2,"B","D"),(5,"C","D"),(1,"C","E"),(3,"D","E")]
    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, {})[v] = w
        adj.setdefault(v, {})[u] = w

    # MST: connect ALL nodes
    mst, mst_w = kruskal_mst(all_nodes, edges)
    print("MST (connect ALL nodes -- Kruskal O(E log E)):")
    for w, u, v in mst:
        print(f"  {u}--{v} (w={w})")
    print(f"  Total weight: {mst_w}")

    # Steiner Tree: connect only terminals {A, D, E}
    terminals = {"A", "D", "E"}
    st_w, st_edges, st_extra = steiner_tree_brute(terminals, all_nodes, adj)
    print(f"\nSteiner Tree (terminals={sorted(terminals)}, brute force):")
    for w, u, v in st_edges:
        print(f"  {u}--{v} (w={w})")
    if st_extra:
        print(f"  Steiner points used: {st_extra}")
    print(f"  Total weight: {st_w}")

    print("\nKey insight:")
    print("  MST (all vertices required)       -- O(E log E), in P")
    print("  Steiner Tree (subset of vertices) -- NP-Complete, O(2^|S|) brute force")
