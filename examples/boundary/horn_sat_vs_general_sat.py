"""
Horn-SAT (P) vs General SAT (NP-Complete)
==========================================
SAT asks: can a boolean formula be satisfied?

Horn-SAT:    Every clause has AT MOST ONE positive literal.
             Solvable in O(n) via unit propagation -- in P.
             Used in logic programming (Prolog), databases, expert systems.

General SAT: No restriction on positive literals -- NP-Complete.
2-SAT:       At most 2 literals per clause -- in P (via SCC).
3-SAT:       Exactly 3 literals -- NP-Complete.

This file shows all three solvers side by side.
"""

from itertools import product


# ── Horn-SAT (Polynomial -- unit propagation) ─────────────────────────────────

def solve_horn_sat(variables: list, clauses: list) -> dict | None:
    """
    Unit propagation for Horn-SAT -- O(n * m).
    Each clause is a list of literals; at most one is positive (no NOT prefix).
    Literals: variable name (positive) or '~var' (negative).
    Returns assignment or None if UNSAT.
    """
    assignment = {v: False for v in variables}
    changed = True

    while changed:
        changed = False
        for clause in clauses:
            pos = [lit for lit in clause if not lit.startswith("~")]
            neg = [lit[1:] for lit in clause if lit.startswith("~")]

            # If all negative literals are True (their vars are False), clause forces pos var
            if len(pos) == 1 and all(not assignment[v] for v in neg):
                if not assignment[pos[0]]:
                    assignment[pos[0]] = True
                    changed = True

    # Verify
    for clause in clauses:
        satisfied = False
        for lit in clause:
            if lit.startswith("~"):
                if not assignment[lit[1:]]:
                    satisfied = True
            else:
                if assignment[lit]:
                    satisfied = True
        if not satisfied:
            return None

    return assignment


# ── General SAT (NP-Complete -- brute force) ──────────────────────────────────

def solve_general_sat(variables: list, clauses: list) -> dict | None:
    """Brute force: O(2^n * m)."""
    for vals in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, vals))
        if all(
            any(
                (not assignment[lit[1:]] if lit.startswith("~") else assignment[lit])
                for lit in clause
            )
            for clause in clauses
        ):
            return assignment
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    variables = ["A", "B", "C", "D"]

    # Horn-SAT: at most 1 positive literal per clause
    # (~A OR ~B OR C) = if A and B then C
    # (~C OR D)       = if C then D
    # (A)             = A is true
    # (B)             = B is true
    horn_clauses = [
        ["~A", "~B", "C"],
        ["~C", "D"],
        ["A"],
        ["B"],
    ]

    print("Horn-SAT (unit propagation -- O(n*m), in P):")
    print("  Clauses: (~A OR ~B OR C), (~C OR D), (A), (B)")
    result = solve_horn_sat(variables, horn_clauses)
    print(f"  Result: {result}")

    # General SAT: multiple positive literals per clause (NOT Horn)
    general_clauses = [
        ["A", "B", "~C"],
        ["~A", "C", "D"],
        ["~B", "~D"],
        ["~A", "~B", "~C", "~D"],
    ]

    print("\nGeneral SAT (brute force -- O(2^n * m), NP-Complete):")
    print("  Clauses: (A OR B OR ~C), (~A OR C OR D), (~B OR ~D), (~A OR ~B OR ~C OR ~D)")
    result2 = solve_general_sat(variables, general_clauses)
    print(f"  Result: {result2}")

    print("\nKey insight:")
    print("  Horn-SAT    (<=1 positive literal/clause) -- O(n*m),    in P")
    print("  2-SAT       (<=2 literals/clause)         -- O(V+E),    in P")
    print("  General SAT (no restriction)              -- NP-Complete")
