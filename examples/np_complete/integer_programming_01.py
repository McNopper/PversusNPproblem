"""
Integer Programming (0-1) -- NP-Complete
==========================================
Given an integer matrix A, integer vectors b and c, and integer k, does there
exist a binary vector x in {0,1}^n such that Ax <= b and c^T x >= k?

0-1 Integer Programming is NP-Complete (one of Karp's original 21).
It is the decision version of Binary Integer Linear Programming.
Many NP-Complete problems (Knapsack, Set Cover, Vertex Cover, etc.) reduce to it.

Verifier:  Check Ax <= b and c^T x >= k -- O(m*n), polynomial.
Solver:    Brute-force over all 2^n binary vectors.
"""

from itertools import product


def matrix_vec(A: list[list], x: list) -> list:
    """Compute Ax."""
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def verify(A: list[list], b: list, c: list, x: list, k: int) -> bool:
    """Check all constraints Ax <= b and objective c^T x >= k."""
    if not all(v in (0, 1) for v in x):
        return False
    Ax = matrix_vec(A, x)
    if any(Ax[i] > b[i] for i in range(len(b))):
        return False
    return sum(c[j] * x[j] for j in range(len(c))) >= k


def solve(A: list[list], b: list, c: list, k: int, n: int) -> list | None:
    """Brute-force over all 2^n binary vectors."""
    for x in product([0, 1], repeat=n):
        x = list(x)
        if verify(A, b, c, x, k):
            return x
    return None


if __name__ == "__main__":
    # Example: select items to maximize value subject to weight constraint
    # Variables: x0=laptop, x1=phone, x2=book, x3=camera
    # Constraint: 3x0 + 1x1 + 2x2 + 2x3 <= 5  (weight capacity)
    # Objective: 4x0 + 3x1 + 1x2 + 2x3 >= k   (minimum value)

    A = [[3, 1, 2, 2]]   # Weight constraint
    b = [5]              # Capacity
    c = [4, 3, 1, 2]     # Values
    n = 4
    items = ["Laptop", "Phone", "Book", "Camera"]

    print("0-1 Integer Programming")
    print("Constraints: 3x0 + x1 + 2x2 + 2x3 <= 5")
    print("Objective:   4x0 + 3x1 + x2 + 2x3 >= k")

    # Find maximum achievable k
    best_val = 0
    best_x = None
    for x in product([0, 1], repeat=n):
        x = list(x)
        Ax = matrix_vec(A, x)
        if all(Ax[i] <= b[i] for i in range(len(b))):
            val = sum(c[j] * x[j] for j in range(n))
            if val > best_val:
                best_val = val
                best_x = x

    print(f"\nMaximum objective value: {best_val}")
    print(f"Solution vector: {best_x}")
    for i, xi in enumerate(best_x):
        if xi:
            print(f"  Selected: {items[i]}")

    # Decision: is there a solution with value >= 6?
    k = 6
    result = solve(A, b, c, k, n)
    print(f"\nIs there a selection with value >= {k}?")
    if result:
        print(f"  Yes: {result}  (value={sum(c[j]*result[j] for j in range(n))})")
        print(f"  Verification: {verify(A, b, c, result, k)}")
    else:
        print(f"  No feasible solution with value >= {k}.")
