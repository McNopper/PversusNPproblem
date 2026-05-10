"""
XOR-SAT (P) vs 3-SAT (NP-Complete)
=====================================
SAT variants differ dramatically in complexity based on clause structure:

XOR-SAT: Each clause is an XOR of literals (exactly one must be true).
         Solvable in O(n^3) via Gaussian elimination over GF(2) -- in P.

3-SAT:   Each clause is an OR of exactly 3 literals -- NP-Complete.

XOR-SAT is a special case of SAT solvable in polynomial time, demonstrating
how the logical connective used determines tractability.
"""

from itertools import product


# ── XOR-SAT (Polynomial -- Gaussian Elimination over GF(2)) ──────────────────

def solve_xor_sat(n_vars: int, xor_clauses: list) -> dict | None:
    """
    Solve XOR-SAT via Gaussian elimination over GF(2).
    Each clause is a list of variable indices that must XOR to 1.
    Returns assignment dict or None if inconsistent.
    """
    # Build augmented matrix [A | b] over GF(2)
    # Each row: coefficients for each variable, plus RHS
    rows = []
    for clause in xor_clauses:
        row = [0] * (n_vars + 1)
        for var in clause:
            row[var] ^= 1
        row[n_vars] = 1  # XOR must equal 1
        rows.append(row)

    # Gaussian elimination
    pivot_col = [None] * n_vars
    row_idx = 0
    for col in range(n_vars):
        # Find pivot
        pivot = None
        for r in range(row_idx, len(rows)):
            if rows[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue  # Free variable
        rows[row_idx], rows[pivot] = rows[pivot], rows[row_idx]
        pivot_col[col] = row_idx
        # Eliminate column
        for r in range(len(rows)):
            if r != row_idx and rows[r][col] == 1:
                rows[r] = [rows[r][j] ^ rows[row_idx][j] for j in range(n_vars + 1)]
        row_idx += 1

    # Check consistency
    for row in rows:
        if all(row[j] == 0 for j in range(n_vars)) and row[n_vars] == 1:
            return None  # 0 = 1 -- inconsistent

    # Back-substitute (free variables set to 0)
    assignment = [0] * n_vars
    for col in range(n_vars - 1, -1, -1):
        if pivot_col[col] is not None:
            r = pivot_col[col]
            assignment[col] = rows[r][n_vars]
            for c2 in range(col + 1, n_vars):
                if rows[r][c2]:
                    assignment[col] ^= assignment[c2]

    return {i: bool(assignment[i]) for i in range(n_vars)}


def verify_xor(assignment: dict, xor_clauses: list) -> bool:
    for clause in xor_clauses:
        xor_val = 0
        for var in clause:
            xor_val ^= int(assignment[var])
        if xor_val != 1:
            return False
    return True


# ── 3-SAT (NP-Complete -- brute force) ───────────────────────────────────────

def solve_3sat(n_vars: int, clauses: list) -> dict | None:
    """Brute force 3-SAT. Clause: list of (var_idx, negated_bool)."""
    for vals in product([False, True], repeat=n_vars):
        if all(
            any((not vals[v] if neg else vals[v]) for v, neg in clause)
            for clause in clauses
        ):
            return {i: vals[i] for i in range(n_vars)}
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # XOR-SAT: x0 XOR x1 = 1, x1 XOR x2 = 1, x0 XOR x2 = 1
    n = 3
    xor_clauses = [[0, 1], [1, 2], [0, 2]]

    print("XOR-SAT (Gaussian elimination over GF(2), O(n^3) -- in P):")
    print("  x0 XOR x1 = 1")
    print("  x1 XOR x2 = 1")
    print("  x0 XOR x2 = 1")
    xor_result = solve_xor_sat(n, xor_clauses)
    if xor_result:
        print(f"  Solution: {xor_result}")
        print(f"  Verification: {verify_xor(xor_result, xor_clauses)}")
    else:
        print("  UNSATISFIABLE")

    # 3-SAT: (x0 OR x1 OR x2) AND (NOT x0 OR x1 OR NOT x2) AND (x0 OR NOT x1 OR x2)
    n3 = 3
    # Each literal: (var_index, is_negated)
    clauses_3 = [
        [(0, False), (1, False), (2, False)],
        [(0, True),  (1, False), (2, True)],
        [(0, False), (1, True),  (2, False)],
    ]

    print("\n3-SAT (brute force O(2^n) -- NP-Complete):")
    print("  (x0 OR x1 OR x2) AND (NOT x0 OR x1 OR NOT x2) AND (x0 OR NOT x1 OR x2)")
    result_3sat = solve_3sat(n3, clauses_3)
    print(f"  Solution: {result_3sat}")

    print("\nKey insight:")
    print("  XOR-SAT  (XOR clauses) -- O(n^3) Gaussian elimination, in P")
    print("  Horn-SAT (<=1 pos lit) -- O(n*m) unit propagation, in P")
    print("  2-SAT    (2 lits/clause)-- O(V+E) SCC, in P")
    print("  3-SAT    (OR clauses)  -- NP-Complete, O(2^n) brute force")
