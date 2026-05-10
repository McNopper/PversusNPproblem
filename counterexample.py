"""
Canonical counterexample to exactness of the geometric-subdivision
heuristic (`tsp.py`, Algorithm 4).

The 12-point concentric-rings instance below is solved sub-optimally
by the algorithm at every tested depth d in {1, 2, 3} with bf_threshold = 6.

Held-Karp optimum (verified by O(n^2 * 2^n) DP) : 29.7823
SiftTSP d=1, t=6                                : 31.7503  (+6.61%)
SiftTSP d=2, t=6                                : 31.7503  (+6.61%)
SiftTSP d=3, t=6                                : 30.7478  (+3.24%)

This refutes the empirical claim that the algorithm is exact for all
tested small instances, and supports the structural argument of
Section 6.2 (Proposition 2) that fixed geometric bisection cannot, in
general, recover an optimal Euclidean tour.

Run:
    python counterexample.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from SiftTSP import tsp_adaptive
from tests.baselines import held_karp, tour_length


# Materialised concentric_rings(12, seed=3) coordinates -- self-contained.
RINGS_12 = [
    (6.973796, 5.004423),
    (5.986996, 6.742443),
    (4.012572, 6.688604),
    (2.951317, 5.033747),
    (3.975935, 3.241382),
    (6.049564, 3.264976),
    (8.497748, 6.997635),
    (5.013907, 8.965062),
    (1.549384, 7.036805),
    (1.538217, 3.024125),
    (5.017141, 0.956403),
    (8.489925, 3.009110),
]


def main():
    print("Counterexample to exactness of the geometric-subdivision heuristic")
    print("=" * 66)
    opt = tour_length(held_karp(RINGS_12))
    print(f"Held-Karp optimum  : {opt:.4f}")
    for d in (1, 2, 3):
        l = tour_length(tsp_adaptive(list(RINGS_12), depth=d, bf_threshold=6))
        gap = (l / opt - 1) * 100
        marker = " EXACT" if gap < 1e-6 else " *** FAIL ***"
        print(f"SiftTSP d={d}, t=6  : {l:.4f}   gap {gap:+.2f}%{marker}")


if __name__ == "__main__":
    main()
