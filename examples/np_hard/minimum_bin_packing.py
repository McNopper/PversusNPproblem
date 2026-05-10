"""
Minimum Bin Packing -- NP-Hard optimization
===========================================
Given item sizes and a bin capacity, pack all items using as few bins as
possible.

Why NP-Hard:
- The decision version asks whether the items can be packed into at most k bins.
- That decision problem is NP-Complete.
- Therefore, minimizing the number of bins is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because a proposed packing can be checked in
  polynomial time.

Key properties:
- The problem stays hard even for simple one-dimensional bins.
- First Fit Decreasing is a widely used heuristic with proven bounds.
- Exact search is exponential.

This module includes:
- A brute-force branch-and-bound exact solver.
- The First Fit Decreasing heuristic.
"""


def first_fit_decreasing(items, capacity):
    bins = []
    for item in sorted(items, reverse=True):
        placed = False
        for bin_items in bins:
            if sum(bin_items) + item <= capacity:
                bin_items.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins


def brute_force_bin_packing(items, capacity):
    items = sorted(items, reverse=True)
    best = {"bins": first_fit_decreasing(items, capacity)}

    def search(index, bins):
        if len(bins) >= len(best["bins"]):
            return
        if index == len(items):
            best["bins"] = [list(bin_items) for bin_items in bins]
            return

        item = items[index]
        used_loads = set()
        for bin_items in bins:
            load = sum(bin_items)
            if load in used_loads:
                continue
            if load + item <= capacity:
                used_loads.add(load)
                bin_items.append(item)
                search(index + 1, bins)
                bin_items.pop()
        bins.append([item])
        search(index + 1, bins)
        bins.pop()

    search(0, [])
    return best["bins"]


if __name__ == "__main__":
    items = [8, 7, 6, 5, 4, 3, 2, 2]
    capacity = 10

    exact = brute_force_bin_packing(items, capacity)
    heuristic = first_fit_decreasing(items, capacity)

    print("Minimum Bin Packing (NP-Hard)")
    print(f"Items: {items}")
    print(f"Capacity: {capacity}")
    print(f"Exact packing uses {len(exact)} bins: {exact}")
    print(f"FFD packing uses   {len(heuristic)} bins: {heuristic}")
