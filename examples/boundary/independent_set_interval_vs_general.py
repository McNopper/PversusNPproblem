"""
Independent Set on Interval Graphs (P) vs General Graphs (NP-Hard)
====================================================================
An interval graph represents intervals on a line: vertices are intervals,
edges connect overlapping intervals.

Independent Set on interval graphs: O(n log n) -- greedy by finish time.
Independent Set on general graphs:  NP-Hard.

This is the same algorithm as interval scheduling! Max independent set in an
interval graph = maximum non-overlapping set of intervals.
"""

from itertools import combinations


# ── Independent Set on Interval Graphs (Polynomial -- Greedy) ────────────────

def build_interval_graph(intervals: list) -> dict:
    """Build graph from intervals: edge if they overlap."""
    n = len(intervals)
    adj = {i: [] for i in range(n)}
    for i, j in combinations(range(n), 2):
        s1, e1 = intervals[i]
        s2, e2 = intervals[j]
        if s1 < e2 and s2 < e1:  # Overlap
            adj[i].append(j)
            adj[j].append(i)
    return adj


def max_independent_set_interval(intervals: list) -> list:
    """
    Greedy by finish time -- O(n log n).
    Equivalent to interval scheduling maximization.
    """
    order = sorted(range(len(intervals)), key=lambda i: intervals[i][1])
    selected = []
    last_end = float("-inf")
    for i in order:
        start, end = intervals[i]
        if start >= last_end:
            selected.append(i)
            last_end = end
    return selected


# ── Independent Set on General Graphs (NP-Hard, brute force) ──────────────────

def max_independent_set_general(adj: dict) -> list:
    """Brute force maximum independent set -- O(2^n * n^2)."""
    nodes = list(adj.keys())
    best = []
    for k in range(len(nodes), 0, -1):
        if k <= len(best):
            break
        for subset in combinations(nodes, k):
            s = set(subset)
            if not any(v in adj[u] for u, v in combinations(subset, 2)):
                best = list(subset)
                break
    return best


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    intervals = [(1, 4), (2, 6), (3, 5), (5, 8), (6, 9), (7, 10), (9, 11)]
    labels = [f"I{i}[{s},{e}]" for i, (s, e) in enumerate(intervals)]

    adj = build_interval_graph(intervals)

    print("Intervals:", [f"[{s},{e}]" for s, e in intervals])
    print(f"Interval graph edges: {[(i,j) for i in adj for j in adj[i] if i<j]}")

    # Interval graph IS (greedy)
    greedy_is = max_independent_set_interval(intervals)
    print(f"\nMax independent set (interval graph, O(n log n)):")
    for i in greedy_is:
        print(f"  {labels[i]}")
    print(f"  Size: {len(greedy_is)}")

    # General graph IS (brute force, same graph)
    general_is = max_independent_set_general(adj)
    print(f"\nMax independent set (general brute force, O(2^n)):")
    for i in general_is:
        print(f"  {labels[i]}")
    print(f"  Size: {len(general_is)}")

    assert sorted(greedy_is) == sorted(general_is), "Results should match on interval graphs!"
    print(f"\nBoth methods agree: {sorted(greedy_is) == sorted(general_is)}")

    print("\nKey insight:")
    print("  Max independent set on interval graphs -- O(n log n), in P")
    print("  Max independent set on general graphs  -- NP-Hard, O(2^n) brute force")
    print("  Other P special cases: bipartite graphs (complement of max matching),")
    print("    perfect graphs, chordal graphs, planar graphs (PTAS only)")
