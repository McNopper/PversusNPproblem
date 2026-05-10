"""
Vertex Cover: Bipartite (P) vs General (NP-Complete)
======================================================
Vertex Cover asks: find a minimum set of vertices that touches every edge.

Bipartite graphs: solvable in O(sqrt(V) * E) via Konig's theorem
                  (min vertex cover = max matching in bipartite graphs).
General graphs:   NP-Complete -- no known polynomial algorithm.

Konig's theorem (1931) is one of the most beautiful results in graph theory.
"""

from collections import defaultdict, deque


# ── Maximum Bipartite Matching (Hopcroft-Karp, O(sqrt(V)*E)) ─────────────────

def hopcroft_karp(left: list, right: list, edges: list) -> dict:
    """
    Hopcroft-Karp maximum bipartite matching.
    edges: list of (u, v) with u in left, v in right.
    Returns match_left: {u: v} and match_right: {v: u}.
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    match_l = {}  # left -> right
    match_r = {}  # right -> left
    INF = float("inf")

    def bfs():
        dist = {}
        queue = deque()
        for u in left:
            if u not in match_l:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        found = False
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                w = match_r.get(v)
                if w is None:
                    found = True
                elif w not in dist or dist[w] == INF:
                    dist[w] = dist[u] + 1
                    queue.append(w)
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

    return match_l, match_r


def konig_vertex_cover(left, right, edges):
    """
    Konig's theorem: min vertex cover of bipartite graph = max matching.
    Returns the minimum vertex cover.
    """
    match_l, match_r = hopcroft_karp(left, right, edges)
    unmatched_left = set(left) - set(match_l)

    # Alternating BFS from unmatched left vertices
    reachable_l = set()
    reachable_r = set()
    adj_l = defaultdict(list)
    adj_r = defaultdict(list)
    for u, v in edges:
        adj_l[u].append(v)
    for u, v in match_l.items():
        adj_r[v].append(u)

    queue = deque(unmatched_left)
    reachable_l = set(unmatched_left)
    while queue:
        u = queue.popleft()
        for v in adj_l[u]:
            if v not in reachable_r:
                reachable_r.add(v)
                w = match_r.get(v)
                if w and w not in reachable_l:
                    reachable_l.add(w)
                    queue.append(w)

    # Cover = (left NOT reachable) UNION (right reachable)
    cover = (set(left) - reachable_l) | reachable_r
    return cover


# ── General Vertex Cover (NP-Complete, brute force) ───────────────────────────

from itertools import combinations


def vertex_cover_brute(graph: dict, k: int) -> set | None:
    nodes = list(graph.keys())
    for subset in combinations(nodes, k):
        s = set(subset)
        if all(u in s or v in s for u in graph for v in graph[u]):
            return s
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Bipartite graph
    left  = ["L1", "L2", "L3"]
    right = ["R1", "R2", "R3"]
    bi_edges = [("L1","R1"),("L1","R2"),("L2","R2"),("L2","R3"),("L3","R3")]

    cover = konig_vertex_cover(left, right, bi_edges)
    print("Bipartite vertex cover (Konig's theorem, O(sqrt(V)*E)):")
    print(f"  Edges:          {bi_edges}")
    print(f"  Minimum cover:  {sorted(cover)}  (size {len(cover)})")

    # General (non-bipartite) graph
    general = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2],
    }
    for k in range(len(general) + 1):
        result = vertex_cover_brute(general, k)
        if result:
            print(f"\nGeneral graph vertex cover (brute force O(C(V,k))):")
            print(f"  Minimum cover: {sorted(result)}  (size {k})")
            break

    print("\nKey insight:")
    print("  Bipartite vertex cover -- O(sqrt(V)*E), in P (Konig's theorem)")
    print("  General vertex cover   -- NP-Complete, no known poly algorithm")
