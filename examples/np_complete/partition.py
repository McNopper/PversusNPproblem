"""
Partition Problem -- NP-Complete
==================================
Given a multiset of integers, can it be partitioned into two subsets with
equal sum? Special case of Subset Sum (target = total_sum / 2).

Verifier:  Check both subsets sum to total/2 -- O(n), polynomial.
Solver DP: O(n * S) pseudo-polynomial, where S = total sum.
"""


def verify(numbers: list, part1: list, part2: list) -> bool:
    if sorted(part1 + part2) != sorted(numbers):
        return False
    return sum(part1) == sum(part2)


def solve_dp(numbers: list) -> tuple | None:
    total = sum(numbers)
    if total % 2 != 0:
        return None  # Odd total -- impossible

    target = total // 2
    n = len(numbers)

    # dp[i][s] = True if a subset of numbers[:i] sums to s
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

    # Backtrack to find partition
    part1 = []
    s = target
    for i in range(n, 0, -1):
        if not dp[i - 1][s]:
            part1.append(numbers[i - 1])
            s -= numbers[i - 1]

    part2 = list(numbers)
    for x in part1:
        part2.remove(x)

    return part1, part2


if __name__ == "__main__":
    examples = [
        [3, 1, 1, 2, 2, 1],   # Partitionable
        [1, 5, 11, 5],         # Partitionable (1+5+5 = 11)
        [1, 2, 3, 5],          # Not partitionable
    ]

    for nums in examples:
        print(f"\nNumbers: {nums}  (sum={sum(nums)})")
        result = solve_dp(nums)
        if result:
            p1, p2 = result
            print(f"  Part 1: {p1}  sum={sum(p1)}")
            print(f"  Part 2: {p2}  sum={sum(p2)}")
            print(f"  Verification: {verify(nums, p1, p2)}")
        else:
            print("  Cannot be partitioned into equal halves.")
