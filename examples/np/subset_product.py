"""
Subset Product Decision
=======================
Given a list of integers and a target T, decide whether some subset has
product exactly T.

Why it is in NP:
A certificate is a subset of the input. We can verify in polynomial time that
all chosen numbers come from the input and that their product is exactly T.

Special status:
This multiplicative analogue of SUBSET SUM is in NP. For suitably encoded
integer inputs, related decision versions are NP-Complete.
"""

from __future__ import annotations

from itertools import combinations
from math import prod


def _multiset_contains(numbers: list[int], subset: list[int]) -> bool:
    pool = list(numbers)
    for value in subset:
        if value in pool:
            pool.remove(value)
        else:
            return False
    return True


def verify_subset_product(numbers: list[int], subset: list[int], target: int) -> bool:
    """Verify that subset is drawn from numbers and multiplies to target."""
    return _multiset_contains(numbers, subset) and prod(subset, start=1) == target


def solve_brute_force(numbers: list[int], target: int) -> list[int] | None:
    """Try every subset."""
    for size in range(len(numbers) + 1):
        for subset in combinations(numbers, size):
            candidate = list(subset)
            if prod(candidate, start=1) == target:
                return candidate
    return None


if __name__ == "__main__":
    numbers = [2, 3, 5, 7, 11]
    target = 30
    subset = solve_brute_force(numbers, target)
    print(f"Numbers: {numbers}")
    print(f"Target product: {target}")
    print(f"Subset found: {subset}")
    print(f"Verified: {verify_subset_product(numbers, subset, target) if subset is not None else False}")
