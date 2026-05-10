"""
Graph Coloring — Class NP
==========================
Given a graph and k colors, decide whether the graph can be colored such
that no two adjacent nodes share the same color.

- Verifier: Given a coloring, check all edges — O(V + E), polynomial.
- Solver:   Backtracking with constraint propagation — exponential worst case.

3-coloring is NP-Complete. 2-coloring (bipartite check) is in P.
"""


def verify(graph: dict, coloring: dict, k: int) -> bool:
    """Verifier: checks that no two adjacent nodes share a color."""
    for node, neighbors in graph.items():
        color = coloring.get(node)
        if color is None or color < 0 or color >= k:
            return False
        for neighbor in neighbors:
            if coloring.get(neighbor) == color:
                return False
    return True


def solve_coloring(graph: dict, k: int) -> dict | None:
    """
    Backtracking k-coloring solver.
    Returns a valid coloring dict {node: color} or None if impossible.
    """
    nodes = list(graph.keys())
    coloring = {}

    def is_safe(node, color):
        return all(coloring.get(nb) != color for nb in graph[node])

    def backtrack(idx):
        if idx == len(nodes):
            return True
        node = nodes[idx]
        for color in range(k):
            if is_safe(node, color):
                coloring[node] = color
                if backtrack(idx + 1):
                    return True
                del coloring[node]
        return False

    return coloring if backtrack(0) else None


if __name__ == "__main__":
    # Petersen graph (needs 3 colors)
    graph = {
        0: [1, 4, 5],
        1: [0, 2, 6],
        2: [1, 3, 7],
        3: [2, 4, 8],
        4: [3, 0, 9],
        5: [0, 7, 8],
        6: [1, 8, 9],
        7: [2, 9, 5],
        8: [3, 5, 6],
        9: [4, 6, 7],
    }

    for k in [2, 3]:
        result = solve_coloring(graph, k)
        print(f"\n{k}-coloring of Petersen graph:")
        if result:
            for node, color in sorted(result.items()):
                print(f"  Node {node}: color {color}")
            print(f"  Valid: {verify(graph, result, k)}")
        else:
            print(f"  Not {k}-colorable.")
