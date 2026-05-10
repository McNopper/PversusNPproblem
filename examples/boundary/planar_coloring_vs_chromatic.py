"""
Planar Graph 4-Coloring (P) vs Chromatic Number (NP-Hard)
===========================================================
Four Color Theorem (1976, Appel & Haken): every planar graph is 4-colorable.
A constructive proof gives a polynomial-time algorithm for 4-coloring planar graphs.

Chromatic number (general): finding the MINIMUM colors for any graph is NP-Hard.

Deciding if a graph needs exactly k colors:
  k=1: trivial (no edges)
  k=2: P (bipartite check)
  k=3: NP-Complete
  k>=4: NP-Complete
  k=4 for PLANAR graphs: P (Four Color Theorem)

This file shows: greedy coloring (fast approximation) + exact chromatic number search.
"""

from collections import deque
from itertools import combinations


# ── Planarity Check (Simplified -- cycle + edge count heuristic) ──────────────

def is_likely_planar(adj: dict) -> bool:
    """
    Necessary condition for planarity: |E| <= 3|V| - 6 (Euler's formula).
    Not sufficient -- full planarity testing needs O(n) LR-planarity algorithm.
    """
    v = len(adj)
    e = sum(len(nb) for nb in adj.values()) // 2
    if v < 3:
        return True
    return e <= 3 * v - 6


# ── Greedy Coloring (O(V + E) -- gives upper bound) ───────────────────────────

def greedy_color(adj: dict) -> dict:
    """
    Greedy coloring: assign each vertex the smallest color not used by its neighbors.
    Not optimal in general, but O(V+E).
    """
    coloring = {}
    for v in adj:
        used = {coloring[nb] for nb in adj[v] if nb in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[v] = c
    return coloring


# ── Exact Chromatic Number (NP-Hard -- brute force) ───────────────────────────

def chromatic_number(adj: dict) -> int:
    """Find minimum k such that graph is k-colorable -- O(k * 3^n)."""
    nodes = list(adj.keys())
    n = len(nodes)

    def is_k_colorable(k):
        coloring = {}
        def backtrack(idx):
            if idx == n:
                return True
            v = nodes[idx]
            for c in range(k):
                if all(coloring.get(nb) != c for nb in adj[v]):
                    coloring[v] = c
                    if backtrack(idx + 1):
                        return True
                    del coloring[v]
            return False
        return backtrack(0)

    for k in range(1, n + 1):
        if is_k_colorable(k):
            return k
    return n


# ── 4-Coloring for Planar Graphs (demonstration via DSATUR) ───────────────────

def dsatur_coloring(adj: dict) -> dict:
    """
    DSATUR: color vertex with highest 'saturation' (most distinct neighbor colors).
    Exact for many graph classes; always produces <= Delta+1 colors.
    For planar graphs, always finds a 4-coloring (by Four Color Theorem).
    """
    coloring = {}
    saturation = {v: 0 for v in adj}
    degree = {v: len(adj[v]) for v in adj}

    for _ in range(len(adj)):
        # Pick uncolored vertex with max saturation (break ties by degree)
        v = max((u for u in adj if u not in coloring),
                key=lambda u: (saturation[u], degree[u]))
        used = {coloring[nb] for nb in adj[v] if nb in coloring}
        c = 0
        while c in used:
            c += 1
        coloring[v] = c
        for nb in adj[v]:
            if nb not in coloring:
                nb_colors = {coloring[x] for x in adj[nb] if x in coloring}
                saturation[nb] = len(nb_colors)

    return coloring


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Planar graph (dodecahedron-like, planar)
    planar = {
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

    print(f"Likely planar: {is_likely_planar(planar)}")

    dsatur = dsatur_coloring(planar)
    colors_used = len(set(dsatur.values()))
    print(f"\nDSATUR 4-coloring (planar, polynomial):")
    for v, c in sorted(dsatur.items()):
        print(f"  Vertex {v}: color {c}")
    print(f"  Colors used: {colors_used} (<= 4 by Four Color Theorem)")

    # Small non-planar graph: K5 (complete graph on 5 vertices)
    k5 = {i: [j for j in range(5) if j != i] for i in range(5)}
    chi = chromatic_number(k5)
    print(f"\nK5 (complete graph, non-planar):")
    print(f"  Chromatic number (exact, NP-Hard): {chi}")
    print(f"  Expected: 5 (all vertices must differ)")

    print("\nKey insight:")
    print("  4-coloring planar graphs      -- polynomial (Four Color Theorem, 1976)")
    print("  3-coloring general graphs     -- NP-Complete")
    print("  Chromatic number (general)    -- NP-Hard")
    print("  2-coloring (bipartite check)  -- O(V+E), in P")
