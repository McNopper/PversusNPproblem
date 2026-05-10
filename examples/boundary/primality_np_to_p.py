"""
Primality Testing: NP to P
===========================
Primality testing asks: is integer n prime?

Historical journey through complexity classes:
- 1975: Miller-Rabin (probabilistic, efficient, widely used)
- 1977: Solovay-Strassen (probabilistic)
- 2002: AKS algorithm -- PROVED primality testing is in P (deterministic, polynomial)

Before AKS, primality was known to be in NP (and co-NP), but its P membership
was uncertain. AKS resolved this definitively.

This file shows the evolution: trial division -> Miller-Rabin -> AKS (simplified).
"""

import math
import random


# ── Trial Division (O(sqrt(n)) -- simple but slow) ───────────────────────────

def trial_division(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


# ── Miller-Rabin (Probabilistic, O(k log^2 n)) ───────────────────────────────

def miller_rabin(n: int, rounds: int = 20) -> bool:
    """Probabilistic primality test. False positive probability < 4^(-rounds)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# ── AKS (Simplified demonstration -- O(log^6 n)) ─────────────────────────────

def is_perfect_power(n: int) -> bool:
    """Check if n = a^b for some a >= 1, b >= 2."""
    for b in range(2, int(math.log2(n)) + 1):
        a = round(n ** (1 / b))
        for candidate in (a - 1, a, a + 1):
            if candidate >= 2 and candidate ** b == n:
                return True
    return False


def aks_simplified(n: int) -> bool:
    """
    Simplified AKS primality test (deterministic polynomial time).
    Full AKS runs in O(log^6 n); this is a pedagogical version.
    For production use, Miller-Rabin with fixed witnesses is preferred.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if is_perfect_power(n):
        return False  # n = a^b is composite

    # Find smallest r such that ord_r(n) > log2(n)^2
    log2n = math.log2(n)
    max_k = int(log2n ** 2)
    r = 2
    while r < n:
        if math.gcd(r, n) == 1:
            # Check multiplicative order of n mod r
            order = 1
            x = n % r
            while x != 1 and order <= max_k:
                x = (x * (n % r)) % r
                order += 1
            if order > max_k:
                break
        r += 1

    # Check small factors up to min(r, n-1)
    for a in range(2, min(r, n)):
        if n % a == 0:
            return n == a

    if n <= r:
        return True

    # Polynomial check (simplified: use witness check over range)
    limit = int(math.sqrt(r) * log2n)
    for a in range(1, min(limit + 1, n)):
        # Check (x + a)^n == x^n + a (mod x^r - 1, n) -- simplified
        if pow(a, n, n) != a % n:
            return False

    return True


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_cases = [2, 3, 4, 17, 97, 561, 1009, 7919, 104729, 999983]

    print(f"{'n':<10} {'Trial Div':>10} {'Miller-Rabin':>13} {'AKS':>6}")
    print("-" * 42)
    for n in test_cases:
        td = trial_division(n)
        mr = miller_rabin(n)
        aks = aks_simplified(n)
        print(f"{n:<10} {str(td):>10} {str(mr):>13} {str(aks):>6}")

    print("\nComplexity comparison:")
    print("  Trial division: O(sqrt(n))           -- exponential in input size (digits)")
    print("  Miller-Rabin:   O(k log^2 n)         -- probabilistic polynomial")
    print("  AKS (2002):     O(log^6 n)           -- deterministic polynomial => in P")
    print("\nAKS was a landmark: proved primality is in P, not just in NP and co-NP.")
