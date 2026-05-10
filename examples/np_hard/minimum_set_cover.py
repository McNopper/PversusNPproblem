"""
Minimum Set Cover -- NP-Hard optimization
=========================================
Given a universe U and a family of subsets, choose as few subsets as possible
so that their union equals U.

Why NP-Hard:
- The decision version asks whether U can be covered using at most k sets.
- That problem is NP-Complete.
- Therefore, the optimization problem is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because a proposed family can be checked in
  polynomial time.

Key properties:
- Greedy set cover has an approximation ratio of H_n, which is at most 1 + ln n.
- Set cover is fundamental in approximation algorithms.
- Exact search is exponential in the number of sets.

This module includes:
- A brute-force exact solver.
- The standard greedy approximation.
"""

from itertools import combinations


def brute_force_minimum_set_cover(universe, family):
    names = list(family)
    for size in range(len(names) + 1):
        for subset in combinations(names, size):
            covered = set()
            for name in subset:
                covered.update(family[name])
            if covered >= universe:
                return list(subset)
    return None


def greedy_set_cover(universe, family):
    uncovered = set(universe)
    chosen = []
    while uncovered:
        best_name = max(
            family,
            key=lambda name: (len(family[name] & uncovered), -len(chosen), str(name)),
        )
        gain = family[best_name] & uncovered
        if not gain:
            return None
        chosen.append(best_name)
        uncovered -= gain
    return chosen


if __name__ == "__main__":
    universe = {1, 2, 3, 4, 5, 6, 7}
    family = {
        "S1": {1, 2, 3},
        "S2": {2, 4, 5},
        "S3": {3, 5, 6},
        "S4": {4, 7},
        "S5": {6, 7},
        "S6": {1, 4, 6},
    }

    exact = brute_force_minimum_set_cover(universe, family)
    greedy = greedy_set_cover(universe, family)

    print("Minimum Set Cover (NP-Hard)")
    print(f"Universe: {sorted(universe)}")
    print(f"Exact cover:    {exact} (size {len(exact)})")
    print(f"Greedy cover:   {greedy} (size {len(greedy)})")
