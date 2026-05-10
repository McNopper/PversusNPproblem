"""
Integer Factorization
=====================
Given an integer n >= 2, find its prime factorization.

Why it is in NP:
A certificate is a list of prime factors. We can verify in polynomial time
that every listed factor is prime and that their product is exactly n.

Special status:
Integer factorization is in NP, but it is not known to be NP-Complete.
It is also not known to be solvable in deterministic polynomial time on a
classical computer.

This file includes:
- verify_factorization: polynomial-time verifier for a proposed factor list
- solve_trial_division: simple brute-force style trial division
- solve_pollards_rho: a faster search procedure based on Pollard's rho
"""

from __future__ import annotations

import math
import random
from typing import List


def is_prime(n: int) -> bool:
    """Return True if n is prime."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def verify_factorization(n: int, factors: List[int]) -> bool:
    """Verify that factors is a valid prime factorization of n."""
    if n < 2:
        return factors == [n]
    product = 1
    for factor in factors:
        if factor < 2 or not is_prime(factor):
            return False
        product *= factor
    return product == n


def solve_trial_division(n: int) -> List[int]:
    """Find prime factors by repeated trial division."""
    if n < 2:
        return [n]
    factors: List[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2
    if n > 1:
        factors.append(n)
    return factors


def pollards_rho(n: int, rng: random.Random) -> int:
    """Return a non-trivial factor of n using Pollard's rho."""
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        x = rng.randrange(2, n - 1)
        y = x
        c = rng.randrange(1, n - 1)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def _factor_with_rho(n: int, rng: random.Random, out: List[int]) -> None:
    if n == 1:
        return
    if is_prime(n):
        out.append(n)
        return
    d = pollards_rho(n, rng)
    _factor_with_rho(d, rng, out)
    _factor_with_rho(n // d, rng, out)


def solve_pollards_rho(n: int) -> List[int]:
    """Find prime factors using small trial division plus Pollard's rho."""
    if n < 2:
        return [n]
    factors: List[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    divisor = 3
    while divisor * divisor <= n and divisor <= 101:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2
    if n > 1:
        rng = random.Random(n)
        rho_factors: List[int] = []
        _factor_with_rho(n, rng, rho_factors)
        factors.extend(sorted(rho_factors))
    return sorted(factors)


if __name__ == "__main__":
    n = 8051
    print(f"n = {n}")

    factors_trial = solve_trial_division(n)
    print(f"Trial division factors: {factors_trial}")
    print(f"Trial division verified: {verify_factorization(n, factors_trial)}")

    factors_rho = solve_pollards_rho(n)
    print(f"Pollard rho factors: {factors_rho}")
    print(f"Pollard rho verified: {verify_factorization(n, factors_rho)}")
