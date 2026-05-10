"""
Set Cover -- NP-Complete
=========================
Given a universe U and a collection of subsets S, find the smallest
sub-collection of S whose union equals U.

Decision version: Is there a sub-collection of size <= k covering U?

Verifier:  Check union of chosen sets == U -- O(k * |U|), polynomial.
Solver:    Brute-force over all 2^|S| sub-collections.
Greedy:    O(|U| * |S|) approximation with ln(|U|) + 1 factor guarantee.
"""

from itertools import combinations


def verify(universe: set, chosen_sets: list, k: int) -> bool:
    if len(chosen_sets) > k:
        return False
    covered = set()
    for s in chosen_sets:
        covered |= set(s)
    return covered >= universe


def solve_brute(universe: set, sets: list, k: int) -> list | None:
    for size in range(1, k + 1):
        for combo in combinations(sets, size):
            if verify(universe, list(combo), size):
                return list(combo)
    return None


def solve_greedy(universe: set, sets: list) -> list:
    """ln(|U|)+1 approximation: always pick the set covering the most uncovered elements."""
    uncovered = set(universe)
    chosen = []
    remaining = [set(s) for s in sets]
    while uncovered:
        best = max(remaining, key=lambda s: len(s & uncovered))
        chosen.append(best)
        uncovered -= best
        remaining.remove(best)
    return chosen


if __name__ == "__main__":
    universe = {1, 2, 3, 4, 5, 6, 7, 8}
    sets = [
        {1, 2, 3},
        {2, 4, 5},
        {3, 6},
        {4, 7},
        {5, 6, 8},
        {1, 7, 8},
    ]

    print(f"Universe: {sorted(universe)}")
    print(f"Available sets: {[sorted(s) for s in sets]}")

    # Find minimum k
    for k in range(1, len(sets) + 1):
        result = solve_brute(universe, sets, k)
        if result:
            print(f"\nMinimum cover (k={k}): {[sorted(s) for s in result]}")
            print(f"Verification: {verify(universe, result, k)}")
            break

    greedy = solve_greedy(universe, sets)
    print(f"\nGreedy cover ({len(greedy)} sets): {[sorted(s) for s in greedy]}")
