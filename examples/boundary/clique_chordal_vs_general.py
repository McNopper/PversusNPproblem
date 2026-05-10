"""
Clique in Chordal Graphs (P) vs General Graphs (NP-Complete)
=============================================================
A graph is CHORDAL if every cycle of length >= 4 has a chord (extra edge).

Maximum Clique in chordal graphs: O(n + m) via perfect elimination ordering.
Maximum Clique in general graphs:  NP-Hard.

Chordal graphs arise naturally in: sparse matrix factorization, Bayesian
networks, perfect phylogeny, and interval graph models.
"""


# ── Chordal Graph Check + Perfect Elimination Ordering (O(n + m)) ────────────

def maximum_cardinality_search(adj: dict) -> list:
    """
    Maximum Cardinality Search -- produces a PEO if graph is chordal.
    O(n + m).
    """
    nodes = list(adj.keys())
    n = len(nodes)
    weight = {v: 0 for v in nodes}
    visited = set()
    order = []

    for _ in range(n):
        v = max((nd for nd in nodes if nd not in visited), key=lambda x: weight[x])
        visited.add(v)
        order.append(v)
        for nb in adj[v]:
            if nb not in visited:
                weight[nb] += 1

    return list(reversed(order))  # Perfect elimination ordering (if chordal)


def is_chordal(adj: dict) -> bool:
    """Verify chordality using PEO -- O(n + m)."""
    peo = maximum_cardinality_search(adj)
    pos = {v: i for i, v in enumerate(peo)}
    for v in peo:
        later_neighbors = [nb for nb in adj[v] if pos[nb] > pos[v]]
        if not later_neighbors:
            continue
        w = min(later_neighbors, key=lambda x: pos[x])
        later_w = set(nb for nb in adj[w] if pos[nb] > pos[w])
        for nb in later_neighbors:
            if nb != w and nb not in later_w:
                return False
    return True


def max_clique_chordal(adj: dict) -> list:
    """
    Find maximum clique in a chordal graph via PEO -- O(n + m).
    The maximum clique is the largest 'simplicial clique' in the PEO.
    """
    peo = maximum_cardinality_search(adj)
    pos = {v: i for i, v in enumerate(peo)}
    best = []
    for i, v in enumerate(peo):
        clique = [v] + [nb for nb in adj[v] if pos[nb] > pos[v]]
        if len(clique) > len(best):
            best = clique
    return best


# ── General Max Clique (NP-Hard, brute force) ─────────────────────────────────

from itertools import combinations


def max_clique_general(adj: dict) -> list:
    """Brute force maximum clique -- O(2^n * n^2)."""
    nodes = list(adj.keys())
    best = []
    for k in range(len(nodes), 0, -1):
        if k <= len(best):
            break
        for subset in combinations(nodes, k):
            if all(v in adj[u] for u, v in combinations(subset, 2)):
                if len(subset) > len(best):
                    best = list(subset)
                break
    return best


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Chordal graph (interval graph -- always chordal)
    chordal = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 4],
        3: [0, 1, 4],
        4: [2, 3, 5],
        5: [4],
    }

    print(f"Chordal graph check: {is_chordal(chordal)}")
    clique_c = max_clique_chordal(chordal)
    print(f"Max clique (chordal, O(n+m)):    {clique_c}  (size {len(clique_c)})")

    # General (non-chordal) graph: 5-cycle has no chord
    general = {
        0: [1, 4],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3, 0],
    }
    print(f"\nGeneral graph (5-cycle) chordal: {is_chordal(general)}")
    clique_g = max_clique_general(general)
    print(f"Max clique (general, O(2^n)):     {clique_g}  (size {len(clique_g)})")

    print("\nKey insight:")
    print("  Max clique in chordal graphs -- O(n+m),  in P")
    print("  Max clique in general graphs -- NP-Hard, O(2^n) brute force")
    print("  Other special P cases: perfect graphs, bipartite graphs (trivially 2)")
