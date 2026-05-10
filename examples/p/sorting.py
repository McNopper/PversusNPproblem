"""
Sorting — Class P
=================
Merge Sort runs in O(n log n) time, placing it firmly in P.

The algorithm recursively splits the list in half, sorts each half,
then merges the sorted halves back together.
"""


def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]
    print(f"Input:  {data}")
    sorted_data = merge_sort(data)
    print(f"Sorted: {sorted_data}")
