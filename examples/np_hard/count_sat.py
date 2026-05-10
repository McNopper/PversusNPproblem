"""
#SAT -- counting satisfying assignments (#P-hard)
=================================================
Given a Boolean formula, count how many assignments satisfy it.

Why #P-hard:
- SAT asks whether at least one satisfying assignment exists.
- #SAT asks for the exact number of satisfying assignments.
- If we could solve #SAT efficiently, then we could solve SAT by checking
  whether the count is nonzero.
- In fact, #SAT is complete for #P under standard reductions.

Is it in NP?
- No. #SAT is a counting problem, not a yes/no language.
- The related decision problem SAT is in NP.

Key properties:
- Counting is usually harder than deciding existence.
- Exact counting by brute force takes time exponential in the number of
  variables.

This module includes:
- A brute-force exact counter.
"""

from itertools import product


def variables_in_formula(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(literal[1:] if literal.startswith("!") else literal)
    return sorted(variables)


def clause_satisfied(clause, assignment):
    for literal in clause:
        if literal.startswith("!") and not assignment[literal[1:]]:
            return True
        if not literal.startswith("!") and assignment[literal]:
            return True
    return False


def count_satisfying_assignments(clauses):
    variables = variables_in_formula(clauses)
    count = 0
    witnesses = []
    for bits in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        if all(clause_satisfied(clause, assignment) for clause in clauses):
            count += 1
            witnesses.append(assignment)
    return count, witnesses


if __name__ == "__main__":
    clauses = [
        ["x1", "x2"],
        ["!x1", "x3"],
        ["!x2", "!x3"],
    ]

    count, witnesses = count_satisfying_assignments(clauses)

    print("#SAT (#P-hard)")
    print(f"Formula: {clauses}")
    print(f"Number of satisfying assignments: {count}")
    print("Satisfying assignments:")
    for witness in witnesses:
        print(f"  {witness}")
