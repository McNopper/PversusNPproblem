"""
Hitting Set -- NP-Complete
===========================
Given a collection of sets S over universe U and integer k, find a set H
of size <= k that intersects (hits) every set in S.

Dual of Set Cover: S hits every set <=> S is a set cover of the hypergraph.

Verifier:  For each set in S, check it has at least one element in H -- O(|S|*k).
Solver:    Brute-force over all C(|U|, k) subsets of the universe.
"""

from itertools import combinations


def verify(collection: list, hitting_set: set, k: int) -> bool:
    if len(hitting_set) > k:
        return False
    return all(hitting_set & set(s) for s in collection)


def solve(universe: set, collection: list, k: int) -> set | None:
    for size in range(1, k + 1):
        for combo in combinations(universe, size):
            h = set(combo)
            if verify(collection, h, size):
                return h
    return None


if __name__ == "__main__":
    universe = {1, 2, 3, 4, 5, 6}
    collection = [
        {1, 2, 3},
        {2, 4},
        {3, 5, 6},
        {1, 4, 6},
    ]

    print("Collection of sets:")
    for i, s in enumerate(collection):
        print(f"  S{i}: {sorted(s)}")

    for k in range(1, len(universe) + 1):
        result = solve(universe, collection, k)
        if result:
            print(f"\nMinimum hitting set (size {k}): {sorted(result)}")
            print(f"Verification: {verify(collection, result, k)}")
            # Show which element hits each set
            for s in collection:
                hit = sorted(result & set(s))
                print(f"  {sorted(s)} hit by: {hit}")
            break
