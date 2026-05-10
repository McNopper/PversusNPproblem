"""
Set Packing -- NP-Complete
===========================
Given a collection of sets and integer k, do there exist k sets in the
collection that are pairwise disjoint (no element shared between any two)?

Complement of Set Cover / dual of Hitting Set.

Verifier:  Check all pairs of chosen sets are disjoint -- O(k^2 * |max_set|).
Solver:    Brute-force over all C(|S|, k) combinations.
"""

from itertools import combinations


def verify(sets: list, chosen_indices: list, k: int) -> bool:
    if len(chosen_indices) < k:
        return False
    chosen = [sets[i] for i in chosen_indices]
    for s1, s2 in combinations(chosen, 2):
        if set(s1) & set(s2):  # Non-empty intersection
            return False
    return True


def solve(sets: list, k: int) -> list | None:
    n = len(sets)
    for combo in combinations(range(n), k):
        if verify(sets, list(combo), k):
            return list(combo)
    return None


def find_maximum_packing(sets: list) -> list:
    for k in range(len(sets), 0, -1):
        result = solve(sets, k)
        if result:
            return result
    return []


if __name__ == "__main__":
    sets = [
        {1, 2, 3},
        {3, 4, 5},
        {1, 6, 7},
        {2, 8, 9},
        {6, 10, 11},
        {4, 8, 12},
    ]

    print("Sets:")
    for i, s in enumerate(sets):
        print(f"  S{i}: {sorted(s)}")

    max_pack = find_maximum_packing(sets)
    print(f"\nMaximum packing indices: {max_pack}")
    print(f"Packing ({len(max_pack)} sets):")
    for i in max_pack:
        print(f"  S{i}: {sorted(sets[i])}")
    print(f"Verification: {verify(sets, max_pack, len(max_pack))}")
