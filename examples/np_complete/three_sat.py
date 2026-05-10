"""
3-SAT -- NP-Complete
=====================
3-SAT is a restricted form of SAT where every clause has exactly 3 literals.
It is one of the most fundamental NP-Complete problems.

Cook's theorem proves SAT is NP-Complete. Karp (1972) showed 3-SAT is
NP-Complete by reduction from SAT. Every NP problem reduces to 3-SAT.

- Verifier: Check each clause in O(n) -- polynomial.
- Solver:   Brute-force over all 2^n truth assignments.
"""

from itertools import product


def evaluate_clause(clause: tuple, assignment: dict) -> bool:
    """A clause (l1, l2, l3) is True if at least one literal is True."""
    for literal in clause:
        negated = literal.startswith("~")
        var = literal[1:] if negated else literal
        value = assignment[var]
        if negated:
            value = not value
        if value:
            return True
    return False


def verify(clauses: list, assignment: dict) -> bool:
    """Polynomial-time verifier: all clauses must be satisfied."""
    return all(evaluate_clause(clause, assignment) for clause in clauses)


def solve_3sat(variables: list, clauses: list) -> dict | None:
    """Brute-force 3-SAT solver: tries all 2^n assignments."""
    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if verify(clauses, assignment):
            return assignment
    return None


if __name__ == "__main__":
    # Example: (A OR B OR C) AND (NOT A OR B OR D) AND (NOT B OR NOT C OR D) AND (A OR NOT C OR NOT D)
    variables = ["A", "B", "C", "D"]
    clauses = [
        ("A",  "B",  "C"),
        ("~A", "B",  "D"),
        ("~B", "~C", "D"),
        ("A",  "~C", "~D"),
    ]

    print("3-SAT Formula:")
    for c in clauses:
        print(f"  ({' OR '.join(c)})")

    solution = solve_3sat(variables, clauses)
    if solution:
        print(f"\nSatisfying assignment: {solution}")
        print(f"Verification: {verify(clauses, solution)}")
    else:
        print("\nUNSATISFIABLE")

    # Unsatisfiable: (A OR A OR A) AND (NOT A OR NOT A OR NOT A)
    clauses2 = [("A", "A", "A"), ("~A", "~A", "~A")]
    print("\nContradictory formula:")
    for c in clauses2:
        print(f"  ({' OR '.join(c)})")
    print(f"Result: {'UNSATISFIABLE' if solve_3sat(['A'], clauses2) is None else 'SAT'}")
