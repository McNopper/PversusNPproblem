"""
Convex Hull - Class P
=====================
The convex hull of a set of planar points is the smallest convex polygon that
contains them. Graham scan builds the hull by sorting points by polar angle and
then removing turns that would bend inward.

The problem is in P because Graham scan runs in O(n log n) time, dominated by
the sorting step.
"""

from math import atan2


Point = tuple[int, int]


def cross(o: Point, a: Point, b: Point) -> int:
    """Return the cross product of OA x OB."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def distance_sq(a: Point, b: Point) -> int:
    """Return squared Euclidean distance."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def graham_scan(points: list[Point]) -> list[Point]:
    """Return the convex hull in counterclockwise order."""
    unique_points = sorted(set(points))
    if len(unique_points) <= 1:
        return unique_points

    pivot = min(unique_points, key=lambda p: (p[1], p[0]))
    others = [p for p in unique_points if p != pivot]
    others.sort(key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), distance_sq(pivot, p)))

    # Remove closer points that share the same angle so the farthest one survives.
    filtered: list[Point] = []
    for point in others:
        while filtered and cross(pivot, filtered[-1], point) == 0:
            if distance_sq(pivot, point) >= distance_sq(pivot, filtered[-1]):
                filtered.pop()
            else:
                break
        else:
            filtered.append(point)
            continue

        if not filtered or filtered[-1] != point:
            if cross(pivot, filtered[-1], point) != 0:
                filtered.append(point)

    hull = [pivot]
    for point in filtered:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    return hull


if __name__ == "__main__":
    sample_points = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 0),
        (2, 1),
        (1, 2),
        (0, 3),
        (3, 3),
    ]

    hull = graham_scan(sample_points)
    print(f"Input points: {sample_points}")
    print(f"Convex hull: {hull}")
