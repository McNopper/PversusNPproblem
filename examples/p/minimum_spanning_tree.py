"""
Minimum Spanning Tree — Class P
================================
Kruskal's algorithm finds the minimum spanning tree (MST) of a weighted
undirected graph in O(E log E) time — polynomial, so it is in P.

A spanning tree connects all nodes with no cycles. The MST is the one
with minimum total edge weight.
"""


class UnionFind:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # Already in same component — would form a cycle
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(nodes: list, edges: list) -> tuple:
    """
    Returns (mst_edges, total_weight).
    edges: list of (weight, u, v)
    """
    uf = UnionFind(nodes)
    mst_edges = []
    total_weight = 0

    for weight, u, v in sorted(edges):
        if uf.union(u, v):
            mst_edges.append((weight, u, v))
            total_weight += weight
            if len(mst_edges) == len(nodes) - 1:
                break  # MST is complete

    return mst_edges, total_weight


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D", "E"]
    edges = [
        (2, "A", "B"),
        (3, "A", "C"),
        (3, "B", "C"),
        (6, "B", "D"),
        (5, "C", "D"),
        (4, "C", "E"),
        (2, "D", "E"),
    ]

    mst, total = kruskal(nodes, edges)

    print("Minimum Spanning Tree (Kruskal's algorithm):")
    for weight, u, v in mst:
        print(f"  {u} — {v}  (weight {weight})")
    print(f"\nTotal MST weight: {total}")
