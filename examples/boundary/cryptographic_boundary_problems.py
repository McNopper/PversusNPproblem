"""
Discrete Log & Integer Factoring -- Cryptographic Boundary Problems
====================================================================
Both are in NP (solutions are efficiently verifiable), but neither is known
to be NP-Complete or proven to be in P. They sit in a fascinating "grey zone".

Integer Factoring:   Given n, find a non-trivial factor. In NP and co-NP.
                     RSA encryption relies on its hardness.
                     Best classical algorithm: General Number Field Sieve O(e^(n^1/3)).
                     Shor's quantum algorithm: O((log n)^3) -- quantum polynomial time!

Discrete Logarithm:  Given g, h, p, find x such that g^x = h (mod p).
                     Basis of Diffie-Hellman, ElGamal, Elliptic Curve Crypto.
                     Also in NP and co-NP; also broken by Shor's algorithm.

These are not known to be NP-Complete -- if they were, NP = co-NP (unlikely).
"""

import math
import random


# ── Integer Factoring (classical algorithms) ──────────────────────────────────

def trial_division_factor(n: int) -> int | None:
    """O(sqrt(n)) trial division. Returns a factor or None if prime."""
    if n % 2 == 0:
        return 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    return None


def pollard_rho(n: int) -> int:
    """
    Pollard's rho algorithm -- O(n^1/4) expected.
    Much faster than trial division for large composites.
    """
    if n % 2 == 0:
        return 2
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
    return d if d != n else None


def full_factorize(n: int) -> list:
    """Fully factorize n using trial division + Pollard's rho."""
    if n <= 1:
        return []
    factors = []
    queue = [n]
    while queue:
        num = queue.pop()
        if num == 1:
            continue
        # Check if prime (Miller-Rabin)
        if is_prime(num):
            factors.append(num)
            continue
        # Try to factor
        f = trial_division_factor(num)
        if f is None:
            for _ in range(50):
                f = pollard_rho(num)
                if f and f != num:
                    break
        if f and f != num:
            queue.append(f)
            queue.append(num // f)
        else:
            factors.append(num)  # Give up
    return sorted(factors)


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n: continue
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True


# ── Discrete Logarithm (Baby-step Giant-step, O(sqrt(p))) ────────────────────

def baby_step_giant_step(g: int, h: int, p: int) -> int | None:
    """
    Solve g^x = h (mod p) using BSGS -- O(sqrt(p)) time and space.
    Better than brute force O(p) but still exponential in input size.
    """
    m = math.isqrt(p) + 1
    # Baby steps: table[g^j mod p] = j
    table = {}
    val = 1
    for j in range(m):
        table[val] = j
        val = val * g % p

    # Giant steps: find i such that g^(im) * h^(-1) is in table
    gm = pow(g, m, p)
    inv_h = pow(h, p - 2, p)  # Fermat's little theorem (p prime)
    curr = inv_h
    for i in range(1, m + 1):
        curr = curr * gm % p
        if curr in table:
            x = i * m + table[curr]
            if pow(g, x, p) == h:
                return x
    return None


# ── Verify (polynomial -- just exponentiation) ────────────────────────────────

def verify_dlog(g: int, x: int, h: int, p: int) -> bool:
    return pow(g, x, p) == h


def verify_factor(n: int, factors: list) -> bool:
    result = 1
    for f in factors:
        result *= f
    return result == n


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Integer Factoring (classical -- exponential in bit-length):")
    numbers = [12, 77, 561, 1234567, 999999937 * 1000000007]
    for n in numbers:
        factors = full_factorize(n)
        valid = verify_factor(n, factors)
        print(f"  {n} = {' * '.join(map(str, factors))}  (verify: {valid})")

    print("\nDiscrete Logarithm (Baby-step Giant-step, O(sqrt(p))):")
    # Find x such that g^x = h (mod p)
    cases = [(2, 22, 29), (3, 13, 17), (5, 3, 23)]
    for g, h, p in cases:
        x = baby_step_giant_step(g, h, p)
        if x is not None:
            print(f"  {g}^x = {h} (mod {p}): x = {x}  verify: {verify_dlog(g, x, h, p)}")

    print("\nKey insight:")
    print("  Integer factoring  -- in NP and co-NP, NOT known NP-Complete")
    print("  Discrete logarithm -- in NP and co-NP, NOT known NP-Complete")
    print("  Both: RSA/DH cryptography relies on their classical hardness")
    print("  Both: Shor's quantum algorithm solves them in polynomial time!")
    print("  => Quantum computers would break RSA and Diffie-Hellman")
