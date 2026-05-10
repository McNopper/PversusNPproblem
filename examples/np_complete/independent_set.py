"""
Independent Set -- NP-Complete
================================
Given a graph G and integer k, does G contain an independent set of size >= k?
An independent set is a set of vertices with NO edges between any two of them.

Complement of Clique: S is an independent set in G iff S is a clique in G_complement.

Verifier:  Check all pairs in S share no edge -- O(k^2), polynomial.
Solver:    Brute-force over all C(V, k) subsets.
"""

from itertools import combinations


def verify(graph: dict, independent_set: list, k: int) -> bool:
    if len(independent_set) < k:
        return False
    for u, v in combinations(independent_set, 2):
        if v in graph.get(u, []):
            return False
    return True


def solve(graph: dict, k: int) -> list | None:
    nodes = list(graph.keys())
    for subset in combinations(nodes, k):
        if verify(graph, list(subset), k):
            return list(subset)
    return None


def find_maximum(graph: dict) -> list:
    nodes = list(graph.keys())
    for k in range(len(nodes), 0, -1):
        result = solve(graph, k)
        if result:
            return result
    return []


if __name__ == "__main__":
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3, 4],
        3: [1, 2, 4],
        4: [2, 3],
    }

    max_is = find_maximum(graph)
    print(f"Maximum independent set: {max_is}  (size {len(max_is)})")
    print(f"Verification: {verify(graph, max_is, len(max_is))}")

    # Check: no edge exists between any two members
    for u, v in combinations(max_is, 2):
        print(f"  Edge {u}-{v} exists: {v in graph[u]}")
