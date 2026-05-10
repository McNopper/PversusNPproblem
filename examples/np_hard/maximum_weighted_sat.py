"""
Maximum Weighted SAT -- NP-Hard optimization
============================================
Given a CNF formula with clause weights, assign truth values to maximize the
sum of weights of satisfied clauses.

Why NP-Hard:
- The decision version asks whether there is an assignment satisfying clauses of
  total weight at least K.
- That problem is NP-Complete.
- Therefore, the optimization problem MAX-SAT is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because we can evaluate all clauses under a
  proposed assignment in polynomial time.

Key properties:
- If all weights are 1, this is the usual MAX-SAT problem.
- A uniformly random assignment satisfies at least half of the total clause
  weight in expectation for clauses with at least one literal.
- Exact search is exponential in the number of variables.

This module includes:
- A brute-force exact solver.
- A randomized heuristic illustrating the 1/2-approximation idea.
"""

import random
from itertools import product


def variables_in_formula(clauses):
    names = set()
    for clause in clauses:
        for literal in clause:
            names.add(literal[1:] if literal.startswith("!") else literal)
    return sorted(names)


def literal_value(literal, assignment):
    if literal.startswith("!"):
        return not assignment[literal[1:]]
    return assignment[literal]


def weighted_satisfied_value(clauses, weights, assignment):
    total = 0
    for clause, weight in zip(clauses, weights):
        if any(literal_value(literal, assignment) for literal in clause):
            total += weight
    return total


def brute_force_max_weighted_sat(clauses, weights):
    variables = variables_in_formula(clauses)
    best_assignment = None
    best_value = -1
    for bits in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        value = weighted_satisfied_value(clauses, weights, assignment)
        if value > best_value:
            best_value = value
            best_assignment = assignment
    return best_assignment, best_value


def randomized_half_approximation(clauses, weights, trials=200, seed=0):
    random.seed(seed)
    variables = variables_in_formula(clauses)
    best_assignment = None
    best_value = -1
    for _ in range(trials):
        assignment = {var: bool(random.getrandbits(1)) for var in variables}
        value = weighted_satisfied_value(clauses, weights, assignment)
        if value > best_value:
            best_value = value
            best_assignment = assignment
    return best_assignment, best_value


if __name__ == "__main__":
    clauses = [
        ["x1", "x2"],
        ["!x1", "x3"],
        ["x2", "!x3"],
        ["!x2", "!x3"],
        ["x1", "!x2", "x3"],
    ]
    weights = [3, 4, 2, 5, 6]

    exact_assignment, exact_value = brute_force_max_weighted_sat(clauses, weights)
    heuristic_assignment, heuristic_value = randomized_half_approximation(clauses, weights)

    print("Maximum Weighted SAT (NP-Hard)")
    print(f"Exact value:     {exact_value} with assignment {exact_assignment}")
    print(f"Randomized best: {heuristic_value} with assignment {heuristic_assignment}")
