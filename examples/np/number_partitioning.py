"""
Number Partitioning Decision
============================
Given a list of numbers and a threshold d, decide whether the numbers can be
split into two groups whose sums differ by at most d.

Why it is in NP:
A certificate is one of the two groups. We can verify in polynomial time that
its elements come from the input and that the resulting difference is at most
d.

Special status:
This threshold decision version is in NP. The related optimization problem of
minimizing the difference is NP-hard, while pseudo-polynomial DP algorithms are
available for integer inputs.

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


def partition_difference(numbers: list[int], subset: list[int]) -> int:
    """Return the absolute difference between the two group sums."""
    return abs(sum(numbers) - 2 * sum(subset))


def verify_number_partitioning(numbers: list[int], subset: list[int], max_difference: int) -> bool:
    """Verify that subset gives a partition with difference at most max_difference."""
    return _multiset_contains(numbers, subset) and partition_difference(numbers, subset) <= max_difference


def solve_brute_force(numbers: list[int], max_difference: int) -> list[int] | None:
    """Try every subset."""
    for size in range(len(numbers) + 1):
        for subset in combinations(numbers, size):
            candidate = list(subset)
            if verify_number_partitioning(numbers, candidate, max_difference):
                return candidate
    return None


def solve_dp(numbers: list[int], max_difference: int) -> list[int] | None:
    """Use subset-sum style DP to find a near-balanced partition."""
    total = sum(numbers)
    reachable = {0: []}
    for value in numbers:
        updates = dict(reachable)
        for current_sum, subset in reachable.items():
            new_sum = current_sum + value
            if new_sum not in updates:
                updates[new_sum] = subset + [value]
        reachable = updates
    for subset_sum, subset in sorted(reachable.items(), key=lambda entry: abs(total - 2 * entry[0])):
        if abs(total - 2 * subset_sum) <= max_difference:
            return subset
    return None


if __name__ == "__main__":
    numbers = [10, 8, 7, 6, 5]
    max_difference = 2
    subset = solve_dp(numbers, max_difference)
    print(f"Numbers: {numbers}")
    print(f"Need difference <= {max_difference}")
    print(f"One group: {subset}")
    if subset is not None:
        print(f"Difference: {partition_difference(numbers, subset)}")
    print(f"Verified: {verify_number_partitioning(numbers, subset, max_difference) if subset is not None else False}")
