"""
Subset Sum — Class NP
======================
Given a set of integers and a target value, decide whether any subset
sums to exactly the target.

- Verifier: Given a candidate subset, sum it and compare — O(n).
- Solver:   Brute-force tries all 2^n subsets — exponential.
            (A pseudo-polynomial DP solution also exists: O(n × target).)
"""

from itertools import combinations


def verify(numbers: list, subset: list, target: int) -> bool:
    """Polynomial-time verifier: checks that subset ⊆ numbers and sums to target."""
    subset_counts = {}
    for x in subset:
        subset_counts[x] = subset_counts.get(x, 0) + 1

    pool = list(numbers)
    for x in subset:
        if x in pool:
            pool.remove(x)
        else:
            return False  # Element not in original set

    return sum(subset) == target


def solve_brute_force(numbers: list, target: int) -> list | None:
    """Brute-force: tries all 2^n subsets."""
    for size in range(1, len(numbers) + 1):
        for subset in combinations(numbers, size):
            if sum(subset) == target:
                return list(subset)
    return None


def solve_dp(numbers: list, target: int) -> list | None:
    """
    Dynamic programming solver — pseudo-polynomial O(n × target).
    Returns a subset that sums to target, or None.
    """
    n = len(numbers)
    # dp[i][s] = True if subset of numbers[:i] sums to s
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(1, n + 1):
        num = numbers[i - 1]
        for s in range(target + 1):
            dp[i][s] = dp[i - 1][s]
            if s >= num and dp[i - 1][s - num]:
                dp[i][s] = True

    if not dp[n][target]:
        return None

    # Backtrack to find the subset
    subset = []
    s = target
    for i in range(n, 0, -1):
        if not dp[i - 1][s]:
            subset.append(numbers[i - 1])
            s -= numbers[i - 1]
    return subset


if __name__ == "__main__":
    numbers = [3, 1, 4, 2, 2, 9, 6]
    target = 10

    print(f"Numbers: {numbers}")
    print(f"Target:  {target}")

    result = solve_dp(numbers, target)
    if result:
        print(f"\nSubset found (DP):         {result}  ->  sum = {sum(result)}")
        print(f"Verification:              {verify(numbers, result, target)}")
    else:
        print("No subset sums to target.")

    # No-solution example
    numbers2 = [3, 7, 1, 2]
    target2 = 100
    print(f"\nNumbers: {numbers2}, Target: {target2}")
    print(f"Result: {'No solution' if solve_dp(numbers2, target2) is None else 'Found'}")
