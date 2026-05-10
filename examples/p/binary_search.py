"""
Binary Search - Class P
=======================
Binary search locates a target value in a sorted list by repeatedly halving
the search interval. Because each step discards half of the remaining input,
it runs in O(log n) time.

This problem is in P because logarithmic time is polynomially bounded and the
algorithm is deterministic.
"""


def binary_search(values: list[int], target: int) -> int:
    """Return the index of target in a sorted list, or -1 if absent."""
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = (left + right) // 2
        guess = values[mid]

        if guess == target:
            return mid
        if guess < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    numbers = [3, 8, 12, 21, 34, 55, 89]
    target = 34
    index = binary_search(numbers, target)

    print(f"Sorted data: {numbers}")
    print(f"Target: {target}")
    print(f"Index found: {index}")
