"""
Linear Programming (P) vs Integer Linear Programming (NP-Hard)
===============================================================
LP: optimize a linear objective over a CONTINUOUS feasible region.
    Solvable in polynomial time (Ellipsoid 1979, Interior Point 1984).

ILP: same problem but variables must be INTEGERS.
     NP-Hard -- the integer constraint shatters the nice geometry of LP.

The LP relaxation of an ILP provides a lower bound and is the basis
of Branch and Bound, the dominant exact ILP algorithm.
"""

from itertools import combinations


# ── LP Relaxation (Polynomial -- corner point method for 2D) ──────────────────

def solve_lp_2d(constraints, objective, bounds=None):
    """
    Solve a 2-variable LP by evaluating all corner points.
    constraints: list of (a, b, c) meaning ax + by <= c
    objective: (cx, cy) -- maximize cx*x + cy*y
    bounds: (x_max, y_max) defaults to (100, 100)
    """
    if bounds is None:
        bounds = (100, 100)

    def intersect(a1, b1, c1, a2, b2, c2):
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-10:
            return None
        return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det

    lines = list(constraints) + [(1, 0, bounds[0]), (0, 1, bounds[1]), (-1, 0, 0), (0, -1, 0)]
    candidates = [(0, 0)]
    for (a1, b1, c1), (a2, b2, c2) in combinations(lines, 2):
        pt = intersect(a1, b1, c1, a2, b2, c2)
        if pt:
            candidates.append(pt)

    feasible = [
        (x, y) for x, y in candidates
        if x >= -1e-9 and y >= -1e-9
        and all(a * x + b * y <= c + 1e-9 for a, b, c in constraints)
    ]
    if not feasible:
        return None, None
    cx, cy = objective
    best = max(feasible, key=lambda p: cx * p[0] + cy * p[1])
    return best, cx * best[0] + cy * best[1]


# ── ILP Solver (NP-Hard -- Grid enumeration for 2D demo) ─────────────────────

def solve_ilp_grid(constraints, objective, x_max: int, y_max: int):
    """
    Enumerate all integer (x, y) in [0..x_max] x [0..y_max] and
    return the feasible point maximizing the objective.
    """
    cx, cy = objective
    best_val = float("-inf")
    best_pt = None
    for x in range(x_max + 1):
        for y in range(y_max + 1):
            if all(a * x + b * y <= c for a, b, c in constraints):
                val = cx * x + cy * y
                if val > best_val:
                    best_val = val
                    best_pt = (x, y)
    return best_pt, best_val


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Maximize 5x + 4y subject to: 6x+4y<=24, x+2y<=6, x,y>=0
    constraints = [(6, 4, 24), (1, 2, 6)]
    objective   = (5, 4)

    lp_pt, lp_val = solve_lp_2d(constraints, objective)
    ilp_pt, ilp_val = solve_ilp_grid(constraints, objective, x_max=4, y_max=3)

    print("Maximize: 5x + 4y")
    print("Subject to: 6x+4y<=24, x+2y<=6, x,y>=0")
    print()
    print(f"LP  (continuous, polynomial):  x={lp_pt[0]:.4f}, y={lp_pt[1]:.4f}  -> value={lp_val:.4f}")
    print(f"ILP (integer,   NP-Hard):      x={ilp_pt[0]},      y={ilp_pt[1]}       -> value={ilp_val}")
    print(f"\nIntegrality gap: {lp_val - ilp_val:.4f}")
    print("\nKey insight:")
    print("  LP  (continuous variables) -- polynomial time, in P")
    print("  ILP (integer variables)    -- NP-Hard, no known poly algorithm")
