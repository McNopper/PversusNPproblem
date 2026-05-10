"""
Greatest Common Divisor and Extended Euclid - Class P
====================================================
The Euclidean algorithm computes gcd(a, b) by repeatedly replacing the larger
problem with a smaller remainder problem. The extended version also finds
Bezout coefficients x and y such that ax + by = gcd(a, b).

These problems are in P because the number of remainder steps is O(log n),
where n is the smaller input magnitude. That is polynomial time.
"""


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor using Euclid's algorithm."""
    a = abs(a)
    b = abs(b)

    while b != 0:
        a, b = b, a % b

    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with g = gcd(a, b) and ax + by = g."""
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0

    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


if __name__ == "__main__":
    a = 252
    b = 198
    g = gcd(a, b)
    g2, x, y = extended_gcd(a, b)

    print(f"gcd({a}, {b}) = {g}")
    print(f"Extended result: gcd = {g2}, x = {x}, y = {y}")
    print(f"Check: {a} * {x} + {b} * {y} = {a * x + b * y}")
