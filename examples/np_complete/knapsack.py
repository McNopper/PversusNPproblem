"""
0/1 Knapsack Problem — NP-Complete
====================================
Given items with weights and values, and a knapsack with a weight capacity,
find the subset of items that maximizes total value without exceeding capacity.

- Verifier: Given a subset, check weight ≤ capacity in O(n) — polynomial.
- Solver (DP): O(n × W) pseudo-polynomial dynamic programming.
- Solver (Brute-force): O(2^n) — exponential.

Note: NP-Completeness refers to the *decision* version:
"Is there a selection with value ≥ V and weight ≤ W?"
"""

from itertools import combinations


def verify(items: list, selected_indices: list, capacity: int, min_value: int) -> bool:
    """Verifier: checks weight ≤ capacity and value ≥ min_value."""
    total_weight = sum(items[i]["weight"] for i in selected_indices)
    total_value  = sum(items[i]["value"]  for i in selected_indices)
    return total_weight <= capacity and total_value >= min_value


def solve_dp(items: list, capacity: int) -> tuple:
    """
    Dynamic programming knapsack solver — O(n × W).
    Returns (max_value, selected_item_indices).
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = items[i - 1]["weight"]
        v = items[i - 1]["value"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # Backtrack to find selected items
    selected = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(i - 1)
            c -= items[i - 1]["weight"]

    return dp[n][capacity], selected


def solve_brute_force(items: list, capacity: int) -> tuple:
    """Brute-force: tries all 2^n subsets — O(2^n)."""
    best_value = 0
    best_subset = []
    n = len(items)
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            w = sum(items[i]["weight"] for i in subset)
            v = sum(items[i]["value"]  for i in subset)
            if w <= capacity and v > best_value:
                best_value = v
                best_subset = list(subset)
    return best_value, best_subset


if __name__ == "__main__":
    items = [
        {"name": "Laptop",   "weight": 3, "value": 4},
        {"name": "Phone",    "weight": 1, "value": 3},
        {"name": "Book",     "weight": 2, "value": 1},
        {"name": "Camera",   "weight": 2, "value": 2},
        {"name": "Headphones","weight": 1, "value": 2},
    ]
    capacity = 5

    print(f"Knapsack capacity: {capacity} kg")
    print(f"{'Item':<12} {'Weight':>6} {'Value':>6}")
    for item in items:
        print(f"  {item['name']:<10} {item['weight']:>6} {item['value']:>6}")

    value_dp, selected_dp = solve_dp(items, capacity)
    print(f"\nDP solution (max value): {value_dp}")
    print("Selected items:")
    for i in selected_dp:
        print(f"  {items[i]['name']} (weight {items[i]['weight']}, value {items[i]['value']})")

    total_w = sum(items[i]["weight"] for i in selected_dp)
    print(f"Total weight: {total_w}/{capacity}")
    print(f"Verification: {verify(items, selected_dp, capacity, value_dp)}")
