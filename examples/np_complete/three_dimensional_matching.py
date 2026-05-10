"""
3-Dimensional Matching (3DM) -- NP-Complete
=============================================
Given three disjoint sets X, Y, Z each of size n, and a set of triples
T subset of X x Y x Z, does there exist a perfect matching -- a set of n
disjoint triples that together cover every element of X, Y, and Z exactly once?

Generalizes bipartite matching (which is in P) to three dimensions.

Verifier:  Check n triples cover all elements exactly once -- O(n^2).
Solver:    Backtracking over compatible triples.
"""


def verify(x: set, y: set, z: set, matching: list) -> bool:
    if len(matching) != len(x):
        return False
    used_x, used_y, used_z = set(), set(), set()
    for (xi, yi, zi) in matching:
        if xi in used_x or yi in used_y or zi in used_z:
            return False
        used_x.add(xi)
        used_y.add(yi)
        used_z.add(zi)
    return used_x == x and used_y == y and used_z == z


def solve(x: set, y: set, z: set, triples: list) -> list | None:
    x, y, z = set(x), set(y), set(z)
    n = len(x)

    def backtrack(used_x, used_y, used_z, matching):
        if len(matching) == n:
            return matching if (used_x == x and used_y == y and used_z == z) else None
        for (xi, yi, zi) in triples:
            if xi not in used_x and yi not in used_y and zi not in used_z:
                result = backtrack(
                    used_x | {xi}, used_y | {yi}, used_z | {zi},
                    matching + [(xi, yi, zi)]
                )
                if result:
                    return result
        return None

    return backtrack(set(), set(), set(), [])


if __name__ == "__main__":
    X = {1, 2, 3}
    Y = {"a", "b", "c"}
    Z = {"p", "q", "r"}

    triples = [
        (1, "a", "p"),
        (1, "b", "q"),
        (2, "b", "r"),
        (2, "c", "p"),
        (3, "a", "q"),
        (3, "c", "r"),
    ]

    print(f"X = {sorted(X)}")
    print(f"Y = {sorted(Y)}")
    print(f"Z = {sorted(Z)}")
    print(f"Triples: {triples}")

    matching = solve(X, Y, Z, triples)
    if matching:
        print(f"\nPerfect 3D matching found:")
        for t in matching:
            print(f"  {t}")
        print(f"Verification: {verify(X, Y, Z, matching)}")
    else:
        print("\nNo perfect 3D matching exists.")

    # Impossible case
    triples2 = [(1, "a", "p"), (2, "a", "q"), (3, "b", "r")]
    print(f"\nWith triples {triples2}:")
    print(f"Result: {'No matching' if solve(X, Y, Z, triples2) is None else 'Found'}")
