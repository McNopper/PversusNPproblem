"""
Bin Packing -- NP-Complete
===========================
Given n items with sizes and k bins each of capacity C, can all items fit?

Decision: Can n items fit into k bins of capacity C?
Optimization: What is the minimum number of bins needed?

Verifier:  Check each bin's load <= C and all items assigned -- O(n).
Solver:    Brute-force assigns each item to each bin -- O(k^n).
Heuristics: First Fit Decreasing (FFD) gives a good approximation.
"""

from itertools import product


def verify(items: list, bins: list[list], capacity: int) -> bool:
    assigned = sorted(item for b in bins for item in b)
    if assigned != sorted(items):
        return False
    return all(sum(b) <= capacity for b in bins)


def solve_brute(items: list, k: int, capacity: int) -> list[list] | None:
    """Try all k^n assignments of n items into k bins."""
    n = len(items)
    for assignment in product(range(k), repeat=n):
        bins = [[] for _ in range(k)]
        for item, bin_idx in zip(items, assignment):
            bins[bin_idx].append(item)
        if all(sum(b) <= capacity for b in bins):
            return [b for b in bins if b]  # Remove empty bins
    return None


def first_fit_decreasing(items: list, capacity: int) -> list[list]:
    """FFD heuristic: sort descending, place each item in first bin that fits."""
    bins = []
    for item in sorted(items, reverse=True):
        placed = False
        for b in bins:
            if sum(b) + item <= capacity:
                b.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins


if __name__ == "__main__":
    items = [0.5, 0.7, 0.3, 0.8, 0.2, 0.6, 0.4, 0.1]
    capacity = 1.0

    print(f"Items: {items}")
    print(f"Bin capacity: {capacity}")

    # Find minimum number of bins (brute force, small example)
    small_items = [4, 3, 3, 2, 2, 1]
    small_cap = 5
    print(f"\nSmall example -- Items: {small_items}, Capacity: {small_cap}")
    for k in range(1, len(small_items) + 1):
        result = solve_brute(small_items, k, small_cap)
        if result:
            print(f"Minimum bins needed: {k}")
            for i, b in enumerate(result):
                print(f"  Bin {i+1}: {b}  (load {sum(b)}/{small_cap})")
            print(f"Verification: {verify(small_items, result, small_cap)}")
            break

    print(f"\nFFD heuristic on original items (capacity {capacity}):")
    ffd_bins = first_fit_decreasing(items, capacity)
    for i, b in enumerate(ffd_bins):
        print(f"  Bin {i+1}: {b}  (load {sum(b):.1f}/{capacity})")
    print(f"Bins used: {len(ffd_bins)}")
