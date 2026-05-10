"""
Clique Problem — NP-Complete
==============================
Given a graph and integer k, decide whether the graph contains a clique
(a complete subgraph) of size k — a set of k nodes all mutually connected.

- Verifier: Given a candidate clique, check all pairs in O(k²) — polynomial.
- Solver:   Backtracking over all subsets — exponential worst case.

Applications: social network analysis (finding tightly-knit groups),
bioinformatics (finding common subsequences), and VLSI design.
"""

from itertools import combinations


def verify(graph: dict, clique: list, k: int) -> bool:
    """Verifier: checks that all pairs in clique are connected and size ≥ k."""
    if len(clique) < k:
        return False
    for u, v in combinations(clique, 2):
        if v not in graph.get(u, []):
            return False
    return True


def solve_clique(graph: dict, k: int) -> list | None:
    """Brute-force: tries all C(V, k) subsets of size k."""
    nodes = list(graph.keys())
    for subset in combinations(nodes, k):
        if verify(graph, list(subset), k):
            return list(subset)
    return None


def find_max_clique(graph: dict) -> list:
    """Finds the maximum clique by trying decreasing sizes."""
    nodes = list(graph.keys())
    for k in range(len(nodes), 0, -1):
        result = solve_clique(graph, k)
        if result:
            return result
    return []


if __name__ == "__main__":
    # Graph with a known 4-clique: {0, 1, 2, 3}
    graph = {
        0: [1, 2, 3, 4],
        1: [0, 2, 3],
        2: [0, 1, 3, 5],
        3: [0, 1, 2],
        4: [0, 5],
        5: [2, 4],
    }

    print("Graph adjacency list:")
    for node, neighbors in sorted(graph.items()):
        print(f"  {node}: {neighbors}")

    max_clique = find_max_clique(graph)
    print(f"\nMaximum clique: {max_clique}  (size {len(max_clique)})")
    print(f"Verification:  {verify(graph, max_clique, len(max_clique))}")

    print("\nSearching for cliques of specific sizes:")
    for k in [3, 4, 5]:
        result = solve_clique(graph, k)
        status = f"Found: {result}" if result else "None"
        print(f"  k={k}: {status}")
