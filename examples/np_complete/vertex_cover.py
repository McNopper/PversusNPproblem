"""
Vertex Cover — NP-Complete
===========================
Given a graph and integer k, decide whether there exists a set of at most k
vertices such that every edge has at least one endpoint in the set.

- Verifier: Given a candidate cover, check all edges in O(E) — polynomial.
- Solver:   Brute-force tries all C(V, k) subsets — exponential in worst case.

A 2-approximation is achievable greedily (pick both endpoints of any uncovered
edge, repeat), but finding the *minimum* vertex cover is NP-Complete.
"""

from itertools import combinations


def verify(graph: dict, cover: set, k: int) -> bool:
    """Verifier: checks every edge has at least one endpoint in cover."""
    if len(cover) > k:
        return False
    for u, neighbors in graph.items():
        for v in neighbors:
            if u not in cover and v not in cover:
                return False
    return True


def solve_vertex_cover(graph: dict, k: int) -> set | None:
    """Brute-force: tries all subsets of size ≤ k."""
    nodes = list(graph.keys())
    for size in range(k + 1):
        for subset in combinations(nodes, size):
            candidate = set(subset)
            if verify(graph, candidate, size):
                return candidate
    return None


def greedy_approx(graph: dict) -> set:
    """
    2-approximation: repeatedly pick both endpoints of an uncovered edge.
    Guaranteed to find a cover ≤ 2 × optimal.
    """
    cover = set()
    edges_remaining = {(u, v) for u, neighbors in graph.items() for v in neighbors if u < v}
    while edges_remaining:
        u, v = next(iter(edges_remaining))
        cover.add(u)
        cover.add(v)
        edges_remaining = {(a, b) for a, b in edges_remaining if a not in cover and b not in cover}
    return cover


if __name__ == "__main__":
    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 4],
        3: [1, 4],
        4: [2, 3],
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"  {node}: {neighbors}")

    # Find minimum vertex cover
    for k in range(len(graph) + 1):
        cover = solve_vertex_cover(graph, k)
        if cover:
            print(f"\nMinimum vertex cover (size {k}): {cover}")
            print(f"Verification: {verify(graph, cover, k)}")
            break

    approx = greedy_approx(graph)
    print(f"\n2-approximation cover: {approx}  (size {len(approx)})")
