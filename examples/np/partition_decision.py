"""
Partition Decision
==================
Given a multiset of integers, decide whether it can be split into two subsets
with equal sum.

Why it is in NP:
A certificate is one side of the partition. We can verify in polynomial time
that the selected numbers come from the input and that their sum is exactly
half of the total.

Special status:
PARTITION is NP-Complete, but only weakly so because a pseudo-polynomial DP
algorithm exists.

This file includes both a brute-force solver and a DP solver.
"""

from __future__ import annotations

from itertools import combinations


def _multiset_contains(numbers: list[int], subset: list[int]) -> bool:
    pool = list(numbers)
    for value in subset:
        if value in pool:
            pool.remove(value)
        else:
            return False
    return True


def verify_partition(numbers: list[int], subset: list[int]) -> bool:
    """Verify that subset forms one side of an equal-sum partition."""
    total = sum(numbers)
    if total % 2 != 0:
        return False
    return _multiset_contains(numbers, subset) and sum(subset) == total // 2


def solve_brute_force(numbers: list[int]) -> list[int] | None:
    """Try every subset."""
    target = sum(numbers)
    if target % 2 != 0:
        return None
    target //= 2
    for size in range(len(numbers) + 1):
        for subset in combinations(numbers, size):
            candidate = list(subset)
            if sum(candidate) == target:
                return candidate
    return None


def solve_dp(numbers: list[int]) -> list[int] | None:
    """Use subset-sum style DP to find one side of an equal partition."""
    total = sum(numbers)
    if total % 2 != 0:
        return None
    target = total // 2
    reachable = {0: []}
    for value in numbers:
        updates = dict(reachable)
        for current_sum, subset in reachable.items():
            new_sum = current_sum + value
            if new_sum <= target and new_sum not in updates:
                updates[new_sum] = subset + [value]
        reachable = updates
    return reachable.get(target)


if __name__ == "__main__":
    numbers = [3, 1, 1, 2, 2, 1]
    solution = solve_dp(numbers)
    print(f"Numbers: {numbers}")
    print(f"Equal partition subset: {solution}")
    print(f"Verified: {verify_partition(numbers, solution) if solution is not None else False}")
