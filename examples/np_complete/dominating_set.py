"""
Dominating Set -- NP-Complete
==============================
Given a graph G and integer k, does there exist a set D of at most k vertices
such that every vertex is either in D or adjacent to a vertex in D?

Applications: facility location (place k facilities so every city is covered),
              wireless network base station placement, social network influence.

Verifier:  For every vertex, check it is in D or has a neighbor in D -- O(V+E).
Solver:    Brute-force over all C(V, k) subsets.
Greedy:    O(V+E) ln(V)-approximation.
"""

from itertools import combinations


def verify(graph: dict, dominating_set: set, k: int) -> bool:
    if len(dominating_set) > k:
        return False
    for v in graph:
        if v in dominating_set:
            continue
        if not any(nb in dominating_set for nb in graph[v]):
            return False
    return True


def solve(graph: dict, k: int) -> set | None:
    nodes = list(graph.keys())
    for size in range(1, k + 1):
        for combo in combinations(nodes, size):
            d = set(combo)
            if verify(graph, d, size):
                return d
    return None


def greedy_dominating_set(graph: dict) -> set:
    """Greedy: pick the vertex that dominates the most uncovered vertices."""
    uncovered = set(graph.keys())
    dominating = set()

    while uncovered:
        # Score each vertex by how many uncovered vertices it dominates (itself + neighbors)
        best = max(graph, key=lambda v: len((uncovered & (set(graph[v]) | {v}))))
        dominating.add(best)
        uncovered -= {best} | set(graph[best])

    return dominating


if __name__ == "__main__":
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 5, 6],
        5: [2, 4],
        6: [4],
    }

    print("Graph:")
    for v, nb in graph.items():
        print(f"  {v}: {nb}")

    for k in range(1, len(graph) + 1):
        result = solve(graph, k)
        if result:
            print(f"\nMinimum dominating set (size {k}): {sorted(result)}")
            print(f"Verification: {verify(graph, result, k)}")
            # Show coverage
            for v in sorted(graph):
                covered_by = "self" if v in result else f"neighbor {next(nb for nb in graph[v] if nb in result)}"
                print(f"  Vertex {v} covered by: {covered_by}")
            break

    greedy = greedy_dominating_set(graph)
    print(f"\nGreedy dominating set: {sorted(greedy)}  (size {len(greedy)})")
