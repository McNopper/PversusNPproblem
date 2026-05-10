"""
Set Cover Decision
==================
Given a universe U, a family of subsets of U, and an integer k, decide
whether at most k sets cover the whole universe.

Why it is in NP:
A certificate is a list of at most k set indices. We can verify in polynomial
time that their union is exactly the universe.

Special status:
SET COVER is NP-Complete.
"""

from __future__ import annotations

from itertools import combinations


def verify_set_cover(universe: set[int], subsets: list[set[int]], chosen: list[int], k: int) -> bool:
    """Verify that chosen identifies at most k subsets whose union covers universe."""
    if len(chosen) != len(set(chosen)) or len(chosen) > k:
        return False
    if any(index < 0 or index >= len(subsets) for index in chosen):
        return False
    covered: set[int] = set()
    for index in chosen:
        covered |= subsets[index]
    return universe <= covered


def solve_brute_force(universe: set[int], subsets: list[set[int]], k: int) -> list[int] | None:
    """Try every collection of at most k subsets."""
    indices = list(range(len(subsets)))
    for size in range(k + 1):
        for choice in combinations(indices, size):
            candidate = list(choice)
            if verify_set_cover(universe, subsets, candidate, k):
                return candidate
    return None


if __name__ == "__main__":
    universe = {1, 2, 3, 4, 5}
    subsets = [
        {1, 2},
        {2, 3, 4},
        {4, 5},
        {1, 5},
    ]
    k = 2
    solution = solve_brute_force(universe, subsets, k)
    print(f"Universe: {sorted(universe)}")
    print(f"k = {k}")
    print(f"Chosen set indices: {solution}")
    print(f"Verified: {verify_set_cover(universe, subsets, solution, k) if solution is not None else False}")
