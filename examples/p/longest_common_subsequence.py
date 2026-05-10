"""
Longest Common Subsequence - Class P
====================================
The longest common subsequence (LCS) problem asks for the longest sequence of
characters that appears in two strings in the same relative order, not
necessarily contiguously. Dynamic programming computes optimal answers for all
prefix pairs and then backtracks to recover one optimal subsequence.

The problem is in P because this dynamic programming solution runs in O(mn)
time, which is polynomial in the input lengths.
"""


def longest_common_subsequence(first: str, second: str) -> tuple[int, str]:
    """Return the LCS length and one longest common subsequence."""
    rows = len(first) + 1
    cols = len(second) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        for j in range(1, cols):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    sequence: list[str] = []
    i = len(first)
    j = len(second)

    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            sequence.append(first[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    sequence.reverse()
    return dp[-1][-1], "".join(sequence)


if __name__ == "__main__":
    first = "ABCBDAB"
    second = "BDCABA"
    length, sequence = longest_common_subsequence(first, second)

    print(f"First string: {first}")
    print(f"Second string: {second}")
    print(f"LCS length: {length}")
    print(f"One LCS: {sequence}")
