"""
Edit Distance - Class P
=======================
The Levenshtein edit distance between two strings is the minimum number of
insertions, deletions, and substitutions needed to transform one string into
the other. Dynamic programming solves it by filling an m by n table of
subproblems.

The problem is in P because the standard dynamic programming algorithm runs in
O(mn) time, which is polynomial in the input lengths.
"""


def levenshtein_distance(first: str, second: str) -> int:
    """Return the Levenshtein edit distance between two strings."""
    rows = len(first) + 1
    cols = len(second) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            substitution_cost = 0 if first[i - 1] == second[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + substitution_cost,
            )

    return dp[-1][-1]


if __name__ == "__main__":
    source = "kitten"
    target = "sitting"
    distance = levenshtein_distance(source, target)

    print(f"First string: {source}")
    print(f"Second string: {target}")
    print(f"Edit distance: {distance}")
