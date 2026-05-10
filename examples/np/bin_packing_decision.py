"""
Bin Packing Decision
====================
Given item sizes, a bin capacity C, and a number of bins k, decide whether all
items can be packed into at most k bins without exceeding capacity in any bin.

Why it is in NP:
A certificate is an assignment of each item to a bin. We can verify in
polynomial time that every item is assigned exactly once and that each bin's
load is at most C.

Special status:
The decision version of BIN PACKING is NP-Complete.
"""

from __future__ import annotations


def verify_bin_packing(items: list[int], bins: list[list[int]], k: int, capacity: int) -> bool:
    """Verify that bins describes a valid packing using at most k bins."""
    if len(bins) > k:
        return False
    seen: list[int] = []
    for bin_items in bins:
        total = 0
        for index in bin_items:
            if index < 0 or index >= len(items):
                return False
            total += items[index]
            seen.append(index)
        if total > capacity:
            return False
    return sorted(seen) == list(range(len(items)))


def solve_brute_force(items: list[int], k: int, capacity: int) -> list[list[int]] | None:
    """Assign items to bins with recursive brute force."""
    bins: list[list[int]] = [[] for _ in range(k)]
    loads = [0] * k
    order = sorted(range(len(items)), key=lambda i: items[i], reverse=True)

    def backtrack(pos: int) -> bool:
        if pos == len(order):
            return True
        item_index = order[pos]
        size = items[item_index]
        used_loads = set()
        for bin_index in range(k):
            if loads[bin_index] in used_loads:
                continue
            if loads[bin_index] + size > capacity:
                continue
            used_loads.add(loads[bin_index])
            bins[bin_index].append(item_index)
            loads[bin_index] += size
            if backtrack(pos + 1):
                return True
            loads[bin_index] -= size
            bins[bin_index].pop()
            if loads[bin_index] == 0:
                break
        return False

    if backtrack(0):
        return [bin_items[:] for bin_items in bins if bin_items]
    return None


if __name__ == "__main__":
    items = [4, 3, 3, 2, 2]
    k = 2
    capacity = 7
    packing = solve_brute_force(items, k, capacity)
    print(f"Items: {items}")
    print(f"Need <= {k} bins of capacity {capacity}")
    print(f"Packing found: {packing}")
    print(f"Verified: {verify_bin_packing(items, packing, k, capacity) if packing is not None else False}")
