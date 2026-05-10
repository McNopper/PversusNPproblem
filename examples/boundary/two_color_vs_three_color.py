"""
2-Coloring (P) vs 3-Coloring (NP-Complete)
===========================================
Graph coloring assigns colors to vertices so no two adjacent vertices share one.

2-Coloring: solvable in O(V+E) -- a graph is 2-colorable iff it is bipartite.
3-Coloring: NP-Complete -- no known polynomial-time algorithm.

This file shows both algorithms and explains the boundary.
"""

from collections import deque


# ── 2-Coloring / Bipartite Check (Polynomial) ────────────────────────────────

def two_color(graph: dict) -> dict | None:
    """
    BFS 2-coloring -- O(V+E).
    Returns coloring dict or None if graph is not bipartite (not 2-colorable).
    """
    color = {}
    for start in graph:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return None  # Odd cycle found -- not bipartite
    return color


# ── 3-Coloring (NP-Complete, backtracking) ────────────────────────────────────

def three_color(graph: dict) -> dict | None:
    """
    Backtracking 3-coloring -- O(3^V) worst case.
    """
    nodes = list(graph.keys())
    coloring = {}

    def backtrack(idx):
        if idx == len(nodes):
            return True
        v = nodes[idx]
        for c in range(3):
            if all(coloring.get(nb) != c for nb in graph[v]):
                coloring[v] = c
                if backtrack(idx + 1):
                    return True
                del coloring[v]
        return False

    return coloring if backtrack(0) else None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Bipartite graph (2-colorable)
    bipartite = {
        "A": ["C", "D"],
        "B": ["C", "D"],
        "C": ["A", "B"],
        "D": ["A", "B"],
    }

    # Non-bipartite but 3-colorable (triangle)
    triangle = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
    }

    # Petersen graph (3-colorable, NOT 2-colorable)
    petersen = {
        i: [] for i in range(10)
    }
    for u, v in [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]:
        petersen[u].append(v)
        petersen[v].append(u)

    for name, g in [("Bipartite graph", bipartite), ("Triangle (K3)", triangle), ("Petersen graph", petersen)]:
        print(f"\n{name}:")
        result2 = two_color(g)
        if result2:
            print(f"  2-colorable (O(V+E)): YES -- {result2}")
        else:
            print(f"  2-colorable (O(V+E)): NO")
            result3 = three_color(g)
            if result3:
                print(f"  3-colorable (O(3^V)): YES -- {result3}")
            else:
                print(f"  3-colorable (O(3^V)): NO")

    print("\nKey insight:")
    print("  2-coloring (bipartite check) -- O(V+E), in P")
    print("  3-coloring (general)         -- NP-Complete, O(3^V) brute force")
