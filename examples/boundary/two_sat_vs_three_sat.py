"""
2-SAT (P) vs 3-SAT (NP-Complete)
==================================
2-SAT: each clause has exactly 2 literals -- solvable in O(V+E) using
       strongly connected components on the implication graph.

3-SAT: each clause has exactly 3 literals -- NP-Complete.

This file shows BOTH algorithms side by side, illustrating why adding
just one literal per clause jumps from P to NP-Complete.
"""

# ── 2-SAT (Polynomial) ────────────────────────────────────────────────────────

def build_implication_graph(n_vars: int, clauses_2sat: list) -> dict:
    """
    For clause (a OR b), add implications (~a => b) and (~b => a).
    Variables are 0..n-1; negation of var i is i+n.
    """
    graph = {i: [] for i in range(2 * n_vars)}
    def neg(x): return x + n_vars if x < n_vars else x - n_vars
    for a, b in clauses_2sat:
        graph[neg(a)].append(b)
        graph[neg(b)].append(a)
    return graph


def kosaraju_scc(graph: dict) -> list:
    """Returns list mapping node -> SCC id (Kosaraju's algorithm)."""
    n = len(graph)
    visited = set()
    finish_order = []

    def dfs1(u):
        stack = [(u, iter(graph[u]))]
        visited.add(u)
        while stack:
            node, it = stack[-1]
            try:
                v = next(it)
                if v not in visited:
                    visited.add(v)
                    stack.append((v, iter(graph[v])))
            except StopIteration:
                finish_order.append(node)
                stack.pop()

    for u in graph:
        if u not in visited:
            dfs1(u)

    rev = {i: [] for i in range(n)}
    for u in graph:
        for v in graph[u]:
            rev[v].append(u)

    comp = [-1] * n
    comp_id = 0
    visited2 = set()

    def dfs2(start, cid):
        stack = [start]
        visited2.add(start)
        while stack:
            u = stack.pop()
            comp[u] = cid
            for v in rev[u]:
                if v not in visited2:
                    visited2.add(v)
                    stack.append(v)

    for u in reversed(finish_order):
        if u not in visited2:
            dfs2(u, comp_id)
            comp_id += 1

    return comp


def solve_2sat(n_vars: int, clauses: list) -> dict | None:
    """
    Solve 2-SAT in O(V+E).
    clauses: list of (a, b) where a,b are variable indices (negated if >= n_vars).
    Returns assignment dict or None if unsatisfiable.
    """
    graph = build_implication_graph(n_vars, clauses)
    comp = kosaraju_scc(graph)
    assignment = {}
    for i in range(n_vars):
        if comp[i] == comp[i + n_vars]:
            return None  # Variable and its negation in same SCC -> UNSAT
        assignment[i] = comp[i] < comp[i + n_vars]
    return assignment


# ── 3-SAT (NP-Complete, brute force) ─────────────────────────────────────────

from itertools import product as iproduct


def solve_3sat_brute(n_vars: int, clauses: list) -> dict | None:
    """Brute-force 3-SAT: O(2^n). clauses: list of 3-literal tuples."""
    for vals in iproduct([False, True], repeat=n_vars):
        ok = True
        for clause in clauses:
            if not any(vals[abs(lit)] ^ (lit < 0) for lit in clause):
                ok = False
                break
        if ok:
            return {i: vals[i] for i in range(n_vars)}
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 2-SAT example: (x0 OR x1) AND (NOT x0 OR x2) AND (NOT x1 OR NOT x2)
    # Encoding: var i, negation = i + n_vars
    n = 3
    # Clause (a OR b) stored as (a, b) with negation = index + n
    clauses_2 = [(0, 1), (0 + n, 2), (1 + n, 2 + n)]

    result = solve_2sat(n, clauses_2)
    print("2-SAT (solvable in polynomial time O(V+E)):")
    print("  Formula: (x0 OR x1) AND (NOT x0 OR x2) AND (NOT x1 OR NOT x2)")
    if result:
        print(f"  Solution: { {f'x{k}': v for k, v in result.items()} }")
    else:
        print("  UNSATISFIABLE")

    # 3-SAT example (same structure, now NP-Complete)
    # Using signed literals: positive = var index, negative = negated
    clauses_3 = [(0, 1, 2), (-1, 2, -3), (-2, -3, 0)]  # vars 0-based, negative = negated
    # Reformat for solver: abs(lit) = var idx, sign determines polarity
    def eval_clause(vals, clause):
        return any((vals[abs(l)] if l > 0 else not vals[abs(l)]) for l in clause)

    print("\n3-SAT (NP-Complete, brute force O(2^n)):")
    print("  Formula: (x0 OR x1 OR x2) AND (NOT x1 OR x2 OR NOT x3) AND (NOT x2 OR NOT x3 OR x0)")
    n3 = 4
    for vals in iproduct([False, True], repeat=n3):
        mapping = {i: vals[i] for i in range(n3)}
        if all(any((mapping[abs(l)] if l >= 0 else not mapping[abs(l)]) for l in c) for c in clauses_3):
            print(f"  Solution: { {f'x{k}': v for k, v in mapping.items()} }")
            break
    else:
        print("  UNSATISFIABLE")

    print("\nKey insight:")
    print("  2-SAT: O(V+E) -- polynomial => in P")
    print("  3-SAT: O(2^n) brute force -- NP-Complete, no known poly-time algorithm")
