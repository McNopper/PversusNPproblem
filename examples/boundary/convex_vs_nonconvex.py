"""
Convex Optimization (P) vs Non-Convex Optimization (NP-Hard)
=============================================================
Convex Optimization: minimize f(x) subject to convex constraints,
                     where f is a convex function.
                     Solvable in polynomial time (interior point methods).
                     Includes LP, QP with positive-definite Q, SDP.

Non-Convex Optimization: same structure but f or constraints are non-convex.
                          Generally NP-Hard -- local minima != global minimum.
                          Examples: MaxSAT, Max-Cut, training neural networks.

This file demonstrates gradient descent on both and shows how convexity
guarantees global optimality while non-convexity can trap you in local minima.
"""


# ── Convex Optimization -- Gradient Descent (converges to global min) ─────────

def gradient_descent(grad_f, x0: float, lr: float = 0.1, steps: int = 100) -> tuple:
    """
    Gradient descent on a 1D function.
    For convex f: guaranteed to find global minimum.
    """
    x = x0
    history = [x]
    for _ in range(steps):
        x = x - lr * grad_f(x)
        history.append(x)
    return x, history


# ── Convex function: f(x) = (x-3)^2 (parabola, one global minimum) ───────────

def convex_f(x):
    return (x - 3) ** 2

def grad_convex(x):
    return 2 * (x - 3)


# ── Non-convex function: f(x) = sin(x) + 0.1*x^2 (multiple local minima) ─────

import math


def nonconvex_f(x):
    return math.sin(x) + 0.1 * x ** 2

def grad_nonconvex(x):
    return math.cos(x) + 0.2 * x


# ── Global optimizer for non-convex (brute force grid search) ─────────────────

def global_minimize(f, lo: float, hi: float, steps: int = 10000) -> tuple:
    """Exhaustive grid search -- exponential in higher dimensions."""
    best_x = lo
    best_f = f(lo)
    step = (hi - lo) / steps
    x = lo
    while x <= hi:
        val = f(x)
        if val < best_f:
            best_f = val
            best_x = x
        x += step
    return best_x, best_f


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("Convex function: f(x) = (x-3)^2")
    print("=" * 55)
    for x0 in [-5.0, 0.0, 10.0]:
        x_min, _ = gradient_descent(grad_convex, x0)
        print(f"  Start x={x0:5.1f} -> converged to x={x_min:.6f} (f={convex_f(x_min):.8f})")
    print("  All starting points converge to global min x=3.0")

    print()
    print("=" * 55)
    print("Non-convex function: f(x) = sin(x) + 0.1*x^2")
    print("=" * 55)
    for x0 in [-5.0, 0.0, 3.0, 6.0, 10.0]:
        x_loc, _ = gradient_descent(grad_nonconvex, x0, lr=0.05, steps=500)
        print(f"  Start x={x0:5.1f} -> stuck at local min x={x_loc:.4f} (f={nonconvex_f(x_loc):.6f})")

    x_global, f_global = global_minimize(nonconvex_f, -10, 10)
    print(f"\n  Global min (grid search, O(1/eps)): x={x_global:.4f} (f={f_global:.6f})")
    print("  Gradient descent misses it from most starting points!")

    print("\nKey insight:")
    print("  Convex optimization     -- polynomial time (interior point), in P")
    print("  Non-convex optimization -- generally NP-Hard (local != global min)")
    print("  Includes: neural network training, MaxSAT, Max-Cut, protein folding")
