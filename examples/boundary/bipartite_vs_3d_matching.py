"""
Bipartite Matching (P) vs 3-Dimensional Matching (NP-Complete)
===============================================================
Maximum Bipartite Matching: match vertices across two sets to maximise pairs.
                            Solvable in O(sqrt(V)*E) via Hopcroft-Karp -- in P.

3-Dimensional Matching (3DM): match across THREE sets simultaneously.
                               NP-Complete -- the third dimension adds hardness.

This is one of the cleanest examples of how dimension drives complexity.
  2D matching: P
  3D matching: NP-Complete
  k-Dimensional matching (k>=3): NP-Complete
"""

from collections import defaultdict, deque
from itertools import combinations


# ── Bipartite Matching -- Hopcroft-Karp (Polynomial) ─────────────────────────

def hopcroft_karp(left, right, edges):
    """O(sqrt(V)*E) maximum bipartite matching."""
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    match_l, match_r = {}, {}
    INF = float("inf")

    def bfs():
        dist = {}
        q = deque()
        for u in left:
            if u not in match_l:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = match_r.get(v)
                if w is None:
                    found = True
                elif dist.get(w, INF) == INF:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return found, dist

    def dfs(u, dist):
        for v in adj[u]:
            w = match_r.get(v)
            if w is None or (dist.get(w, INF) == dist[u] + 1 and dfs(w, dist)):
                match_l[u] = v
                match_r[v] = u
                return True
        dist[u] = INF
        return False

    while True:
        found, dist = bfs()
        if not found:
            break
        for u in left:
            if u not in match_l:
                dfs(u, dist)

    return match_l


# ── 3D Matching (NP-Complete, backtracking) ───────────────────────────────────

def three_d_matching(X, Y, Z, triples):
    """
    Find a perfect 3D matching: n disjoint triples covering all of X, Y, Z.
    Backtracking -- exponential worst case.
    """
    n = len(X)
    X, Y, Z = set(X), set(Y), set(Z)

    def backtrack(used_x, used_y, used_z, chosen):
        if len(chosen) == n:
            return chosen if used_x == X and used_y == Y and used_z == Z else None
        for xi, yi, zi in triples:
            if xi not in used_x and yi not in used_y and zi not in used_z:
                result = backtrack(
                    used_x | {xi}, used_y | {yi}, used_z | {zi},
                    chosen + [(xi, yi, zi)]
                )
                if result:
                    return result
        return None

    return backtrack(set(), set(), set(), [])


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Bipartite matching
    left  = [1, 2, 3, 4]
    right = ["a", "b", "c", "d"]
    bi_edges = [(1,"a"),(1,"b"),(2,"b"),(2,"c"),(3,"c"),(3,"d"),(4,"a"),(4,"d")]

    matching = hopcroft_karp(left, right, bi_edges)
    print("Maximum Bipartite Matching (Hopcroft-Karp, O(sqrt(V)*E)):")
    for u, v in sorted(matching.items()):
        print(f"  {u} <-> {v}")
    print(f"  Size: {len(matching)}")

    # 3D matching
    X = {1, 2, 3}
    Y = {"a", "b", "c"}
    Z = {"p", "q", "r"}
    triples = [
        (1,"a","p"),(1,"b","q"),(2,"b","r"),
        (2,"c","p"),(3,"a","q"),(3,"c","r"),
    ]

    result = three_d_matching(X, Y, Z, triples)
    print("\n3-Dimensional Matching (backtracking, NP-Complete):")
    if result:
        for t in result:
            print(f"  {t}")
        print(f"  Size: {len(result)} (perfect matching)")
    else:
        print("  No perfect 3D matching found.")

    print("\nKey insight:")
    print("  2D bipartite matching -- O(sqrt(V)*E), in P")
    print("  3D matching           -- NP-Complete, no known poly algorithm")
    print("  k-D matching (k>=3)   -- NP-Complete")
