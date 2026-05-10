"""
Matrix Multiplication — Class P
================================
Standard matrix multiplication runs in O(n³) time and is in P.
Strassen's algorithm improves this to O(n^2.807).

This example implements both the naive O(n³) approach and Strassen's
divide-and-conquer algorithm for 2×2 blocks.
"""


def naive_multiply(A: list[list], B: list[list]) -> list[list]:
    """Standard O(n³) matrix multiplication."""
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C


def strassen(A: list[list], B: list[list]) -> list[list]:
    """Strassen's O(n^2.807) matrix multiplication (2×2 base case demo)."""
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    def split(M):
        top_left  = [row[:mid] for row in M[:mid]]
        top_right = [row[mid:] for row in M[:mid]]
        bot_left  = [row[:mid] for row in M[mid:]]
        bot_right = [row[mid:] for row in M[mid:]]
        return top_left, top_right, bot_left, bot_right

    def add(X, Y):
        return [[X[i][j] + Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

    def sub(X, Y):
        return [[X[i][j] - Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))

    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)

    top = [C11[i] + C12[i] for i in range(mid)]
    bot = [C21[i] + C22[i] for i in range(mid)]
    return top + bot


def print_matrix(M, label):
    print(f"{label}:")
    for row in M:
        print(" ", row)


if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    naive = naive_multiply(A, B)
    fast  = strassen(A, B)

    print_matrix(A, "A")
    print_matrix(B, "B")
    print_matrix(naive, "A × B (naive)")
    print_matrix(fast,  "A × B (Strassen)")
    print(f"\nResults match: {naive == fast}")
