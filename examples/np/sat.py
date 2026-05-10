"""
Boolean Satisfiability (SAT) — Class NP
=========================================
Given a boolean formula, decide if there exists an assignment of variables
that makes the formula TRUE.

- Verifier: Given a candidate assignment, check it in O(n) — polynomial.
- Solver:   Brute-force tries all 2^n assignments — exponential.

SAT was the first problem proven NP-Complete (Cook's theorem, 1971).
"""

from itertools import product


def evaluate(formula, assignment: dict) -> bool:
    """
    Evaluate a CNF formula under the given assignment.
    formula: list of clauses, each clause is a list of literals.
    A literal is a variable name (str) or its negation ("NOT var").
    """
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            if literal.startswith("NOT "):
                var = literal[4:]
                if not assignment[var]:
                    clause_satisfied = True
                    break
            else:
                if assignment[literal]:
                    clause_satisfied = True
                    break
        if not clause_satisfied:
            return False
    return True


def verify(formula, assignment: dict) -> bool:
    """Polynomial-time verifier: checks a proposed solution in O(clauses × literals)."""
    return evaluate(formula, assignment)


def solve_sat(variables: list, formula) -> dict | None:
    """Brute-force SAT solver: tries all 2^n assignments."""
    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if evaluate(formula, assignment):
            return assignment
    return None  # Unsatisfiable


if __name__ == "__main__":
    # Formula: (A OR B) AND (NOT A OR C) AND (NOT B OR NOT C)
    variables = ["A", "B", "C"]
    formula = [
        ["A", "B"],
        ["NOT A", "C"],
        ["NOT B", "NOT C"],
    ]

    print("Formula: (A OR B) AND (NOT A OR C) AND (NOT B OR NOT C)")
    solution = solve_sat(variables, formula)

    if solution:
        print(f"Satisfying assignment found: {solution}")
        print(f"Verification: {verify(formula, solution)}")
    else:
        print("Formula is UNSATISFIABLE")

    # Unsatisfiable example: (A) AND (NOT A)
    formula2 = [["A"], ["NOT A"]]
    print("\nFormula: (A) ∧ (¬A)")
    result2 = solve_sat(["A"], formula2)
    print(f"Result: {'UNSATISFIABLE' if result2 is None else result2}")
