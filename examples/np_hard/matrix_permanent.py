"""
Matrix Permanent -- #P-hard
===========================
For an n x n matrix A, the permanent is

perm(A) = sum over all permutations p of product_i A[i][p(i)]

This looks like the determinant, except every term has a plus sign.

Why #P-hard:
- Computing the permanent of a 0/1 matrix counts perfect matchings in a
  bipartite graph.
- That counting problem is #P-complete.
- Therefore, exact permanent computation is #P-hard.

Is it in NP?
- No. Permanent is a function problem, not a decision language.
- The associated threshold decision versions live in counting complexity, not NP.

Key properties:
- The determinant is easy because signs cancel; the permanent keeps every term.
- The naive formula takes O(n! * n) time.
- Ryser's formula improves this to O(2^n * n^2), or O(2^n * n) with careful
  updates.

This module includes:
- A brute-force permutation formula.
- Ryser's inclusion-exclusion formula.
"""

from itertools import permutations


def permanent_bruteforce(matrix):
    n = len(matrix)
    total = 0
    for perm in permutations(range(n)):
        product = 1
        for i in range(n):
            product *= matrix[i][perm[i]]
        total += product
    return total


def permanent_ryser(matrix):
    n = len(matrix)
    total = 0
    for mask in range(1, 1 << n):
        bits = 0
        row_product = 1
        for j in range(n):
            if mask & (1 << j):
                bits += 1
        sign = -1 if (n - bits) % 2 else 1
        for i in range(n):
            row_sum = 0
            for j in range(n):
                if mask & (1 << j):
                    row_sum += matrix[i][j]
            row_product *= row_sum
        total += sign * row_product
    return total


if __name__ == "__main__":
    matrix = [
        [1, 2, 1],
        [0, 3, 4],
        [2, 1, 5],
    ]

    brute_force_value = permanent_bruteforce(matrix)
    ryser_value = permanent_ryser(matrix)

    print("Matrix Permanent (#P-hard)")
    print(f"Matrix: {matrix}")
    print(f"Brute-force permanent: {brute_force_value}")
    print(f"Ryser permanent:       {ryser_value}")
