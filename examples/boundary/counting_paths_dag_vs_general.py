"""
Counting Paths in DAG (P) vs Counting Hamiltonian Paths (#P-Hard)
===================================================================
Counting problems are often much harder than their decision counterparts.

Count paths in a DAG (source to sink): O(V+E) via topological DP.
Count ALL simple paths in a general graph: #P-Hard.
Count Hamiltonian paths: #P-Hard (even though the decision problem is NP-Complete).

#P (sharp-P) is the class of counting problems. #P-Hard problems are at least
as hard as any #P problem -- believed harder than NP.
Famous result: Toda's theorem (1991) -- P^#P contains the entire polynomial hierarchy.
"""


# ── Count Paths in DAG (Polynomial -- O(V+E)) ─────────────────────────────────

def count_dag_paths(adj: dict, src, dst) -> int:
    """
    Count all paths from src to dst in a DAG using DP.
    Requires topological ordering -- O(V+E).
    """
    from collections import deque

    # Kahn's topological sort
    in_deg = {v: 0 for v in adj}
    for u in adj:
        for v in adj[u]:
            in_deg[v] += 1

    queue = deque(v for v in in_deg if in_deg[v] == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    dp = {v: 0 for v in adj}
    dp[src] = 1
    for u in topo:
        for v in adj[u]:
            dp[v] += dp[u]

    return dp[dst]


# ── Count All Simple Paths in General Graph (#P-Hard, brute force) ────────────

def count_simple_paths(adj: dict, src, dst) -> int:
    """
    Count all simple paths from src to dst -- exponential worst case.
    For general graphs this is #P-Hard.
    """
    count = [0]

    def dfs(node, visited):
        if node == dst:
            count[0] += 1
            return
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                dfs(nb, visited)
                visited.remove(nb)

    dfs(src, {src})
    return count[0]


# ── Count Hamiltonian Paths (#P-Hard, inclusion-exclusion DP O(2^n * n^2)) ────

def count_hamiltonian_paths(adj: dict) -> int:
    """
    Count Hamiltonian paths using Held-Karp DP: O(2^n * n^2).
    dp[S][v] = number of paths visiting exactly the set S of vertices, ending at v.
    """
    nodes = list(adj.keys())
    n = len(nodes)
    idx = {v: i for i, v in enumerate(nodes)}

    # Bitmask DP
    dp = [[0] * n for _ in range(1 << n)]
    for i, v in enumerate(nodes):
        dp[1 << i][i] = 1  # Path consisting of single vertex

    for mask in range(1, 1 << n):
        for last in range(n):
            if not dp[mask][last]:
                continue
            if not (mask >> last & 1):
                continue
            for nb in adj[nodes[last]]:
                ni = idx[nb]
                if mask >> ni & 1:
                    continue
                dp[mask | (1 << ni)][ni] += dp[mask][last]

    full_mask = (1 << n) - 1
    return sum(dp[full_mask][i] for i in range(n))


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # DAG: count paths from A to E
    dag = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["D"],
        "D": ["E"],
        "E": [],
    }

    print("Count paths in DAG A -> E (O(V+E) DP):")
    count = count_dag_paths(dag, "A", "E")
    print(f"  Number of paths: {count}")

    # General graph: count simple paths
    general = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D", "E"],
        "D": ["A", "C"],
        "E": ["B", "C"],
    }

    print("\nCount simple paths A -> E in general graph (brute force, #P-Hard):")
    sp = count_simple_paths(general, "A", "E")
    print(f"  Number of simple paths: {sp}")

    # Count Hamiltonian paths
    small = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2],
    }

    print("\nCount Hamiltonian paths in graph (Held-Karp O(2^n * n^2), #P-Hard):")
    hp = count_hamiltonian_paths(small)
    print(f"  Number of Hamiltonian paths: {hp}")

    print("\nKey insight:")
    print("  Count paths in DAG            -- O(V+E),        in P")
    print("  Count simple paths (general)  -- #P-Hard,       exponential brute force")
    print("  Count Hamiltonian paths       -- #P-Hard,       O(2^n * n^2) Held-Karp")
    print("  #P is believed strictly harder than NP (Toda's theorem, 1991)")
