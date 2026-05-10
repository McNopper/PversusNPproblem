"""
Non-convex Quadratic Programming -- NP-Hard in general
======================================================
Optimize an objective of the form

    x^T Q x + c^T x

subject to linear constraints.

Why NP-Hard:
- When Q is indefinite, the objective is non-convex.
- General non-convex quadratic programs can encode hard combinatorial problems,
  so global optimization is NP-Hard.

Is it in NP?
- The optimization problem is not itself a decision language.
- Natural threshold decision versions can be NP-Hard; certificates are delicate
  over real numbers because representation and precision matter.

Key properties:
- Convex quadratic programming is polynomial-time solvable.
- Non-convex quadratic programming is fundamentally different because local
  optima may not be global optima.
- Exact global optimization is hard even in small dimensions when discretized.

This module includes:
- A brute-force exhaustive grid search over a bounded region.
- A simple local-search heuristic.
"""

from itertools import product


def quadratic_objective(x, q, c):
    total = 0.0
    n = len(x)
    for i in range(n):
        for j in range(n):
            total += x[i] * q[i][j] * x[j]
    for i in range(n):
        total += c[i] * x[i]
    return total


def is_feasible(x, constraints):
    for coeffs, bound in constraints:
        lhs = sum(a * b for a, b in zip(coeffs, x))
        if lhs > bound + 1e-9:
            return False
    return True


def exhaustive_grid_search(q, c, constraints, grid_values):
    best_x = None
    best_value = float("-inf")
    for x in product(grid_values, repeat=len(c)):
        if not is_feasible(x, constraints):
            continue
        value = quadratic_objective(x, q, c)
        if value > best_value:
            best_value = value
            best_x = x
    return best_x, best_value


def local_search_heuristic(q, c, constraints, grid_values, start):
    current = start
    if not is_feasible(current, constraints):
        raise ValueError("Start point must be feasible.")
    current_value = quadratic_objective(current, q, c)
    improved = True
    while improved:
        improved = False
        for i in range(len(current)):
            for candidate_value in grid_values:
                if candidate_value == current[i]:
                    continue
                candidate = list(current)
                candidate[i] = candidate_value
                candidate = tuple(candidate)
                if not is_feasible(candidate, constraints):
                    continue
                value = quadratic_objective(candidate, q, c)
                if value > current_value + 1e-9:
                    current = candidate
                    current_value = value
                    improved = True
    return current, current_value


if __name__ == "__main__":
    q = [
        [-1.0, 2.0],
        [2.0, -1.5],
    ]
    c = [0.5, 0.25]
    constraints = [
        ([1.0, 1.0], 2.0),
        ([-1.0, 0.0], 0.0),
        ([0.0, -1.0], 0.0),
    ]
    grid_values = [0.0, 0.5, 1.0, 1.5, 2.0]

    exact_x, exact_value = exhaustive_grid_search(q, c, constraints, grid_values)
    heuristic_x, heuristic_value = local_search_heuristic(
        q, c, constraints, grid_values, start=(0.0, 0.0)
    )

    print("Non-convex Quadratic Programming (NP-Hard in general)")
    print(f"Exact grid optimum: {exact_x} with value {exact_value:.3f}")
    print(f"Local heuristic:    {heuristic_x} with value {heuristic_value:.3f}")
