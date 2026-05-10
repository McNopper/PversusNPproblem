"""
Clique Cover -- NP-Complete
=============================
Given a graph G and integer k, can the vertices of G be partitioned into at
most k cliques (complete subgraphs)?

Equivalent to k-coloring the *complement* graph:
  - A clique in G is an independent set in complement(G)
  - Covering G with k cliques = coloring complement(G) with k colors

So Clique Cover is NP-Complete by reduction from Graph Coloring.

Verifier:  Check every group is a clique and all vertices are assigned -- O(k * V^2).
Solver:    Brute-force partition using backtracking.
"""

from itertools import combinations


def is_clique(graph: dict, nodes: list) -> bool:
    for u, v in combinations(nodes, 2):
        if v not in graph.get(u, []):
            return False
    return True


def verify(graph: dict, cover: list[list], k: int) -> bool:
    if len(cover) > k:
        return False
    all_nodes = sorted(v for group in cover for v in group)
    if all_nodes != sorted(graph.keys()):
        return False
    return all(is_clique(graph, group) for group in cover)


def solve(graph: dict, k: int) -> list[list] | None:
    nodes = list(graph.keys())

    def backtrack(remaining, groups):
        if not remaining:
            return groups
        node = remaining[0]
        rest = remaining[1:]
        # Try adding node to each existing group (if it forms a clique)
        for i, group in enumerate(groups):
            if all(node in graph.get(v, []) for v in group):
                groups[i].append(node)
                result = backtrack(rest, groups)
                if result is not None:
                    return result
                groups[i].pop()
        # Start a new group (if we still have room)
        if len(groups) < k:
            groups.append([node])
            result = backtrack(rest, groups)
            if result is not None:
                return result
            groups.pop()
        return None

    return backtrack(nodes, [])


if __name__ == "__main__":
    # Graph where complement is 3-colorable => clique cover with 3 groups
    graph = {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 5],
        3: [0, 4, 5],
        4: [1, 3, 5],
        5: [2, 3, 4],
    }

    print("Graph:")
    for v, nb in graph.items():
        print(f"  {v}: {nb}")

    for k in range(1, len(graph) + 1):
        result = solve(graph, k)
        if result:
            print(f"\nMinimum clique cover (k={k}):")
            for i, group in enumerate(result):
                print(f"  Clique {i+1}: {group}  (is_clique: {is_clique(graph, group)})")
            print(f"Verification: {verify(graph, result, k)}")
            break
