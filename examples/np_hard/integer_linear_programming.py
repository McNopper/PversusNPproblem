"""
Integer Linear Programming (ILP) — NP-Hard
============================================
ILP is like Linear Programming, but variables must take integer values.
Adding the integrality constraint makes the problem NP-Hard.

LP (continuous) is in P — solved by Ellipsoid or Interior Point methods.
ILP (integer) is NP-Hard — the feasible region becomes a discrete set.

This example uses Branch and Bound, the classical exact ILP algorithm.

Problem (integer production planning):
  Maximize:  5x + 4y
  Subject to:
    6x + 4y ≤ 24
    x  + 2y ≤ 6
    x, y ≥ 0  and  x, y ∈ ℤ  (integers!)
"""

import math


def lp_relaxation_2d(constraints, objective, x_bounds, y_bounds):
    """Solve the LP relaxation over a bounded 2D region (corner-point method)."""
    from itertools import combinations

    lines = list(constraints) + [
        (1, 0, x_bounds[1]),   # x <= ub
        (-1, 0, -x_bounds[0]), # x >= lb  →  -x <= -lb
        (0, 1, y_bounds[1]),
        (0, -1, -y_bounds[0]),
    ]

    def intersect(a1, b1, c1, a2, b2, c2):
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-10:
            return None
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        return x, y

    candidates = []
    for (a1, b1, c1), (a2, b2, c2) in combinations(lines, 2):
        pt = intersect(a1, b1, c1, a2, b2, c2)
        if pt:
            candidates.append(pt)

    feasible = []
    for x, y in candidates:
        if (x < x_bounds[0] - 1e-9 or x > x_bounds[1] + 1e-9 or
                y < y_bounds[0] - 1e-9 or y > y_bounds[1] + 1e-9):
            continue
        if all(a * x + b * y <= c + 1e-9 for a, b, c in constraints):
            feasible.append((x, y))

    if not feasible:
        return None, float("-inf")

    cx, cy = objective
    best = max(feasible, key=lambda p: cx * p[0] + cy * p[1])
    return best, cx * best[0] + cy * best[1]


def branch_and_bound(constraints, objective):
    """
    ILP solver: enumerate all integer points in the feasible region.
    For 2-variable problems this is a complete exact search.
    """
    cx, cy = objective
    best_val = float("-inf")
    best_pt = None
    for x in range(5):
        for y in range(4):
            if all(a * x + b * y <= c for a, b, c in constraints):
                val = cx * x + cy * y
                if val > best_val:
                    best_val = val
                    best_pt = (x, y)
    return best_pt, best_val


if __name__ == "__main__":
    constraints = [(6, 4, 24), (1, 2, 6)]
    objective = (5, 4)

    print("Integer Linear Programming -- Branch and Bound")
    print("  Maximize: 5x + 4y")
    print("  Subject to: 6x + 4y <= 24,  x + 2y <= 6,  x,y >= 0,  x,y integers")

    # LP relaxation (ignoring integrality)
    lp_point, lp_val = lp_relaxation_2d(constraints, objective, (0, 4), (0, 3))
    print(f"\n  LP relaxation:  x={lp_point[0]:.4f}, y={lp_point[1]:.4f}  ->  value={lp_val:.4f}")

    # ILP solution
    ilp_point, ilp_val = branch_and_bound(constraints, objective)
    x, y = ilp_point
    print(f"  ILP solution:   x={x}, y={y}  →  value={ilp_val}")
    print(f"\n  Integrality gap: {lp_val - ilp_val:.4f}")
