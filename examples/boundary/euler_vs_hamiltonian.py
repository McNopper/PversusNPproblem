"""
Euler Path (P) vs Hamiltonian Path (NP-Complete)
=================================================
Both ask for a special traversal of a graph, but the complexity differs radically:

Euler Path:      Visit every EDGE exactly once. Decidable in O(E) and solvable
                 in O(E) via Hierholzer's algorithm.

Hamiltonian Path: Visit every VERTEX exactly once. NP-Complete -- no known
                  polynomial-time algorithm.

The difference: edges vs vertices. Euler (1736) -- first graph theory result.
"""

from collections import defaultdict, deque


# ── Euler Path (Polynomial) ───────────────────────────────────────────────────

def has_euler_path(graph: dict) -> str:
    """
    Euler path/circuit existence conditions (O(V+E)):
    - Euler CIRCUIT:  all vertices have even degree.
    - Euler PATH:     exactly 2 vertices have odd degree.
    """
    odd = sum(1 for v in graph if len(graph[v]) % 2 != 0)
    if odd == 0:
        return "circuit"
    if odd == 2:
        return "path"
    return "none"


def hierholzer(graph: dict, start) -> list | None:
    """Find Euler circuit/path using Hierholzer's algorithm -- O(E)."""
    kind = has_euler_path(graph)
    if kind == "none":
        return None

    adj = {v: list(neighbors) for v, neighbors in graph.items()}

    if kind == "path":
        # Start from an odd-degree vertex
        start = next(v for v in adj if len(adj[v]) % 2 != 0)

    stack = [start]
    path = []

    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            adj[u].remove(v)  # Undirected: remove reverse edge too
            stack.append(u)
        else:
            path.append(stack.pop())

    return path if len(path) == sum(len(nb) for nb in graph.values()) // 2 + 1 else None


# ── Hamiltonian Path (NP-Complete) ────────────────────────────────────────────

def solve_hamiltonian(graph: dict) -> list | None:
    """Backtracking Hamiltonian path -- O(V!) worst case."""
    nodes = list(graph.keys())
    n = len(nodes)

    def backtrack(path, visited):
        if len(path) == n:
            return path
        for nb in graph[path[-1]]:
            if nb not in visited:
                visited.add(nb)
                path.append(nb)
                if backtrack(path, visited):
                    return path
                path.pop()
                visited.remove(nb)
        return None

    for start in nodes:
        result = backtrack([start], {start})
        if result:
            return result
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Graph with BOTH an Euler circuit and a Hamiltonian path
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["A", "C"],
    }

    print("Graph:", {k: v for k, v in graph.items()})

    # Euler
    kind = has_euler_path(graph)
    euler = hierholzer(graph, "A")
    print(f"\nEuler {kind} (O(E) -- Polynomial):")
    print(f"  {' -> '.join(euler) if euler else 'None'}")

    # Hamiltonian
    ham = solve_hamiltonian(graph)
    print(f"\nHamiltonian path (O(V!) -- NP-Complete):")
    print(f"  {' -> '.join(ham) if ham else 'None'}")

    print("\nKey insight:")
    print("  Euler path  (every EDGE once)   -- solvable in O(E), in P")
    print("  Hamiltonian (every VERTEX once) -- NP-Complete, O(V!) brute force")
