"""
Knapsack Decision
=================
Given items with weights and values, a weight limit W, and a target value V,
decide whether some selection has total value at least V and total weight at
most W.

Why it is in NP:
A certificate is a list of chosen item indices. We can verify in polynomial
time that the indices are valid and that the total weight and value satisfy
the bounds.

Special status:
0/1 KNAPSACK is NP-Complete in decision form. It also has a pseudo-polynomial
DP algorithm, so it is weakly NP-Complete.

This file includes both a brute-force solver and a DP solver.
"""

from __future__ import annotations

from itertools import combinations

Item = tuple[int, int, str]


def verify_knapsack(items: list[Item], chosen: list[int], min_value: int, max_weight: int) -> bool:
    """Verify a proposed selection of item indices."""
    if len(chosen) != len(set(chosen)):
        return False
    if any(index < 0 or index >= len(items) for index in chosen):
        return False
    total_weight = sum(items[index][0] for index in chosen)
    total_value = sum(items[index][1] for index in chosen)
    return total_weight <= max_weight and total_value >= min_value


def solve_brute_force(items: list[Item], min_value: int, max_weight: int) -> list[int] | None:
    """Try every subset of items."""
    indices = range(len(items))
    for size in range(len(items) + 1):
        for subset in combinations(indices, size):
            candidate = list(subset)
            if verify_knapsack(items, candidate, min_value, max_weight):
                return candidate
    return None


def solve_dp(items: list[Item], min_value: int, max_weight: int) -> list[int] | None:
    """Use dynamic programming by weight to find a feasible selection."""
    best_value = [-1] * (max_weight + 1)
    chosen_sets: list[list[int] | None] = [None] * (max_weight + 1)
    best_value[0] = 0
    chosen_sets[0] = []

    for index, (weight, value, _name) in enumerate(items):
        for current_weight in range(max_weight - weight, -1, -1):
            if best_value[current_weight] < 0:
                continue
            new_weight = current_weight + weight
            new_value = best_value[current_weight] + value
            if new_value > best_value[new_weight]:
                best_value[new_weight] = new_value
                chosen_sets[new_weight] = chosen_sets[current_weight] + [index]

    for weight in range(max_weight + 1):
        if best_value[weight] >= min_value:
            return chosen_sets[weight]
    return None


if __name__ == "__main__":
    items = [
        (2, 6, "map"),
        (2, 10, "water"),
        (3, 12, "food"),
        (1, 7, "flashlight"),
    ]
    min_value = 19
    max_weight = 5

    solution = solve_dp(items, min_value, max_weight)
    print(f"Need value >= {min_value} with weight <= {max_weight}")
    print(f"Chosen item indices: {solution}")
    if solution is not None:
        names = [items[index][2] for index in solution]
        print(f"Chosen items: {names}")
    print(f"Verified: {verify_knapsack(items, solution, min_value, max_weight) if solution is not None else False}")
