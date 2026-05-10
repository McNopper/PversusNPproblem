"""
Selection Algorithm - Class P
=============================
The selection problem asks for the k-th smallest element of an unsorted list.
The median-of-medians algorithm gives a deterministic worst-case linear-time
solution by using carefully chosen pivots.

This problem is in P because the algorithm runs in O(n) time in the worst case,
which is polynomial in the input size.
"""


def median_of_medians(values: list[int]) -> int:
    """Return a good pivot value using groups of five."""
    if len(values) <= 5:
        return sorted(values)[len(values) // 2]

    groups = [values[index:index + 5] for index in range(0, len(values), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]
    return median_of_medians(medians)



def select_kth(values: list[int], k: int) -> int:
    """Return the element that would appear at index k in sorted order."""
    if not 0 <= k < len(values):
        raise IndexError("k is out of range")
    if len(values) == 1:
        return values[0]

    pivot = median_of_medians(values)
    lows = [value for value in values if value < pivot]
    highs = [value for value in values if value > pivot]
    pivots = [value for value in values if value == pivot]

    if k < len(lows):
        return select_kth(lows, k)
    if k < len(lows) + len(pivots):
        return pivot
    return select_kth(highs, k - len(lows) - len(pivots))


if __name__ == "__main__":
    data = [29, 10, 14, 37, 14, 5, 18, 22, 31]
    k = 4
    answer = select_kth(data, k)

    print(f"Data: {data}")
    print(f"Element at sorted index {k}: {answer}")
    print(f"Sorted data for verification: {sorted(data)}")
