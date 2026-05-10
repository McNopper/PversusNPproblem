"""
Linear Programming -- Class P
=============================
Linear programming (LP) optimizes a linear objective function subject to
linear inequality constraints. The Ellipsoid method (1979) and Interior
Point methods prove LP is in P.

This example solves a simple 2-variable LP by finding and evaluating all
corner points (vertices) of the feasible region -- correct for 2D LPs.

Problem (production planning):
  Maximize:  5x + 4y          (profit)
  Subject to:
    6x + 4y <= 24              (machine hours)
    x  + 2y <= 6               (labor hours)
    x >= 0, y >= 0
"""

from itertools import combinations


def solve_2x2(a1, b1, c1, a2, b2, c2):
    """Solve 2×2 linear system: a1x+b1y=c1, a2x+b2y=c2. Returns (x,y) or None."""
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-10:
        return None
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return x, y


def lp_2d(constraints, objective):
    """
    Solve a 2-variable LP by enumerating corner points.
    constraints: list of (a, b, c) meaning ax + by <= c
    objective: (cx, cy) -- maximize cx*x + cy*y
    """
    # Include non-negativity constraints as lines: x=0, y=0
    lines = [(a, b, c) for a, b, c in constraints] + [(1, 0, 0), (0, 1, 0)]

    candidates = [(0, 0)]  # Origin is always a candidate

    # Find all pairwise intersections of constraint boundary lines
    for (a1, b1, c1), (a2, b2, c2) in combinations(lines, 2):
        pt = solve_2x2(a1, b1, c1, a2, b2, c2)
        if pt:
            candidates.append(pt)

    # Filter feasible points (satisfy all constraints including x,y >= 0)
    feasible = []
    for x, y in candidates:
        if x < -1e-9 or y < -1e-9:
            continue
        if all(a * x + b * y <= c + 1e-9 for a, b, c in constraints):
            feasible.append((x, y))

    if not feasible:
        return None, None

    cx, cy = objective
    best_pt = max(feasible, key=lambda p: cx * p[0] + cy * p[1])
    best_val = cx * best_pt[0] + cy * best_pt[1]
    return best_pt, best_val


if __name__ == "__main__":
    constraints = [
        (6, 4, 24),  # 6x + 4y <= 24
        (1, 2, 6),   # x + 2y <= 6
    ]
    objective = (5, 4)  # maximize 5x + 4y

    point, value = lp_2d(constraints, objective)
    x, y = point

    print("Linear Programming -- Production Planning")
    print("  Maximize: 5x + 4y")
    print("  Subject to: 6x + 4y <= 24, x + 2y <= 6, x,y >= 0")
    print()
    print(f"  Optimal point:  x = {x:.4f}, y = {y:.4f}")
    print(f"  Optimal value:  {value:.4f}")
