"""
Primality Testing — Class P
===========================
The Miller-Rabin primality test is a probabilistic algorithm that runs in
O(k log² n) time. The deterministic AKS algorithm (2002) proved primality
testing is in P, but Miller-Rabin is practical and used widely in cryptography.

With enough witnesses (k rounds), the probability of a false positive is
negligibly small (< 4^(-k)).
"""


def miller_rabin(n: int, rounds: int = 20) -> bool:
    """Returns True if n is (very likely) prime, False if definitely composite."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Use fixed set of witnesses — deterministically correct for n < 3,317,044,064,679,887,385,961,981
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
            return False  # Definitely composite
    return True  # Almost certainly prime


if __name__ == "__main__":
    test_numbers = [2, 3, 4, 17, 561, 1009, 7919, 104729, 999983, 1_000_003]
    print(f"{'Number':<12} {'Prime?'}")
    print("-" * 20)
    for n in test_numbers:
        print(f"{n:<12} {miller_rabin(n)}")
