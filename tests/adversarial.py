"""
Adversarial test harness for tsp.

We construct city configurations specifically designed to defeat fixed
geometric bisection:

  1. zig-zag across the bisection axis
  2. interleaved clusters straddling the splitting axis
  3. near-collinear "comb" patterns
  4. concentric rings (no preferred axis)
  5. random Euclidean instances (control)

For each, we compare tsp against:
  - Held-Karp (exact, ground truth)
  - Nearest-Neighbor (NN)
  - 2-opt (NN + 2-opt)
  - tsp with depth in {1, 2, 3} and bf_threshold = 6

A failure of tsp to match the Held-Karp optimum on any instance
constitutes a counterexample to its claimed exactness.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tsp import tsp_adaptive  # noqa: E402
from tests.baselines import (  # noqa: E402
    held_karp,
    nearest_neighbor,
    two_opt,
    tour_length,
)


# ---------- adversarial instance generators ---------- #

def zigzag_across_axis(n, amp=5.0, span=10.0, seed=0):
    """
    n points zig-zagging across the y-axis at x = span/2.
    Optimal tour follows the zig-zag; vertical bisection at x = span/2
    splits it into ~n/2 left points and ~n/2 right points, forcing
    cross-section edges that are easy to mis-route.
    """
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        y = i * (span / n)
        x = (span / 2) + (amp if i % 2 == 0 else -amp)
        x += rng.uniform(-0.05, 0.05)
        y += rng.uniform(-0.05, 0.05)
        pts.append((x, y))
    return pts


def interleaved_clusters(n, seed=1):
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        side = i % 2
        cx = 2.0 if side == 0 else 8.0
        pts.append((cx + rng.uniform(-0.3, 0.3),
                    i * (10.0 / n) + rng.uniform(-0.1, 0.1)))
    return pts


def comb_pattern(n, seed=2):
    rng = random.Random(seed)
    pts = []
    teeth = max(2, n // 2)
    for k in range(teeth):
        x = k * (10.0 / max(1, teeth - 1))
        pts.append((x + rng.uniform(-0.05, 0.05), 0.0 + rng.uniform(-0.05, 0.05)))
        if len(pts) < n:
            pts.append((x + rng.uniform(-0.05, 0.05), 3.0 + rng.uniform(-0.05, 0.05)))
    return pts[:n]


def concentric_rings(n, seed=3):
    rng = random.Random(seed)
    pts = []
    half = n // 2
    for i in range(half):
        a = 2 * math.pi * i / half
        pts.append((5 + 2 * math.cos(a) + rng.uniform(-0.05, 0.05),
                    5 + 2 * math.sin(a) + rng.uniform(-0.05, 0.05)))
    for i in range(n - half):
        a = 2 * math.pi * i / (n - half) + math.pi / (n - half)
        pts.append((5 + 4 * math.cos(a) + rng.uniform(-0.05, 0.05),
                    5 + 4 * math.sin(a) + rng.uniform(-0.05, 0.05)))
    return pts


def uniform_random(n, seed=42):
    rng = random.Random(seed)
    return [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]


# ---------- evaluation ---------- #

def gap(length, opt):
    if opt <= 0:
        return 0.0
    return (length / opt - 1.0) * 100.0


def evaluate(name, cities):
    opt_tour = held_karp(cities)
    opt = tour_length(opt_tour)
    nn_len = tour_length(nearest_neighbor(cities))
    two_opt_len = tour_length(two_opt(cities))
    rows = []
    for d in (1, 2, 3):
        tour = tsp_adaptive(list(cities), depth=d, bf_threshold=6)
        rows.append((d, tour_length(tour)))
    print(f"\n=== {name}  (n={len(cities)}) ===")
    print(f"  Held-Karp optimum : {opt:.4f}")
    print(f"  Nearest-Neighbor  : {nn_len:.4f}   gap {gap(nn_len, opt):+.2f}%")
    print(f"  NN + 2-opt        : {two_opt_len:.4f}   gap {gap(two_opt_len, opt):+.2f}%")
    failures = []
    for d, l in rows:
        g = gap(l, opt)
        marker = " EXACT" if g < 1e-6 else " *** FAIL ***"
        print(f"  SiftTSP d={d}, t=6  : {l:.4f}   gap {g:+.2f}%{marker}")
        if g > 1e-6:
            failures.append((d, l, g))
    return opt, failures


def main():
    random.seed(0)
    cases = [
        ("zigzag-12",        zigzag_across_axis(12)),
        ("zigzag-14",        zigzag_across_axis(14)),
        ("zigzag-16",        zigzag_across_axis(16)),
        ("zigzag-tight-12",  zigzag_across_axis(12, amp=2.0)),
        ("zigzag-wide-14",   zigzag_across_axis(14, amp=8.0)),
        ("interleaved-12",   interleaved_clusters(12)),
        ("interleaved-14",   interleaved_clusters(14)),
        ("comb-12",          comb_pattern(12)),
        ("comb-14",          comb_pattern(14)),
        ("rings-12",         concentric_rings(12)),
        ("rings-14",         concentric_rings(14)),
        ("uniform-12",       uniform_random(12, seed=42)),
        ("uniform-14",       uniform_random(14, seed=43)),
        ("uniform-16",       uniform_random(16, seed=44)),
    ]
    total_failures = 0
    failure_log = []
    for name, cities in cases:
        opt, fails = evaluate(name, cities)
        if fails:
            total_failures += 1
            failure_log.append((name, len(cities), opt, fails))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total adversarial cases  : {len(cases)}")
    print(f"Cases where tsp missed: {total_failures}")
    if failure_log:
        print("\nCounterexamples found:")
        for name, n, opt, fails in failure_log:
            for d, l, g in fails:
                print(f"  {name:22s} n={n:2d}  d={d}  opt={opt:.4f}  got={l:.4f}  gap={g:+.2f}%")
    else:
        print("No counterexamples found in this battery.")


if __name__ == "__main__":
    main()
