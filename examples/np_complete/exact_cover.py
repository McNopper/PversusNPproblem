"""
Exact Cover -- NP-Complete
===========================
Given a universe U and a collection S of subsets of U, find a sub-collection
S* subset of S such that every element of U is covered by exactly one set in S*.

Generalises: Sudoku, N-Queens, Pentomino tiling, and Exact 3-Cover all reduce to Exact Cover.
Donald Knuth's Algorithm X with Dancing Links (DLX) solves it efficiently in practice.

Verifier:  Check every element appears exactly once across chosen sets -- O(|U| * |S*|).
Solver:    Algorithm X (recursive backtracking with constraint propagation).
"""


def verify(universe: set, chosen: list) -> bool:
    covered = []
    for s in chosen:
        covered.extend(s)
    return sorted(covered) == sorted(universe) and len(covered) == len(universe)


def algorithm_x(universe: set, sets: list) -> list | None:
    """
    Knuth's Algorithm X: recursively select a set, remove covered elements,
    recurse on the reduced problem.
    """
    if not universe:
        return []  # All elements covered -- success

    # Choose element with fewest covering sets (MRV heuristic)
    elem = min(universe, key=lambda e: sum(1 for s in sets if e in s))

    for s in [s for s in sets if elem in s]:
        # Select s: remove all elements it covers and all conflicting sets
        new_universe = universe - set(s)
        new_sets = [t for t in sets if not (set(t) & set(s))]
        result = algorithm_x(new_universe, new_sets)
        if result is not None:
            return [s] + result

    return None  # No solution with this branch


if __name__ == "__main__":
    universe = {1, 2, 3, 4, 5, 6, 7}
    sets = [
        frozenset([1, 4, 7]),
        frozenset([1, 4]),
        frozenset([4, 5, 7]),
        frozenset([3, 5, 6]),
        frozenset([2, 3, 6, 7]),
        frozenset([2, 7]),
    ]

    print(f"Universe: {sorted(universe)}")
    print("Available sets:")
    for i, s in enumerate(sets):
        print(f"  S{i}: {sorted(s)}")

    result = algorithm_x(universe, sets)
    if result:
        print(f"\nExact cover found ({len(result)} sets):")
        for s in result:
            print(f"  {sorted(s)}")
        print(f"Verification: {verify(universe, result)}")
    else:
        print("\nNo exact cover exists.")

    # Sudoku-style example: 4x4 mini Sudoku encoded as exact cover
    print("\nNote: Sudoku, N-Queens, and Pentomino tiling all reduce to Exact Cover.")
    print("Algorithm X (with Dancing Links) is the basis of the world's fastest Sudoku solvers.")
