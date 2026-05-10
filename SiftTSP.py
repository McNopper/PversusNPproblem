"""
SiftTSP - A Geometric Sandclock-Sift Heuristic for Euclidean TSP
================================================================

A deterministic, polynomial-time **heuristic** for the Euclidean
Travelling Salesman Problem, based on recursive geometric bisection.
Entry point: `sift_tsp`.

Architecture (full prose: paper/):

    Phase 1  max         worst-case greedy-longest start (once)
    Phase 2  sift        sandclock depth schedule + mill (breadth)
                         + sieve (depth) angular search
    Phase 3  min         exact brute force on sections of size <= tau
    Phase 4  loop        8-state (mode, direction, ordering) super-cycle;
                         mill and sieve ceilings grow independently

The 17 incremental design iterations that produced this file
(`tsp_p.py`, `tsp_p2.py`, ..., `tsp_p17.py`) have been removed; their
source is preserved in the git history.
"""

import math
import itertools


# --------------------------------------------------------------------
# Basic geometry
# --------------------------------------------------------------------

def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def tour_length(tour):
    n = len(tour)
    return sum(dist(tour[i], tour[(i + 1) % n]) for i in range(n))


# --------------------------------------------------------------------
# Phase 1: worst-case greedy-longest start
# --------------------------------------------------------------------

def greedy_longest_path(cities):
    """At each step move to the FARTHEST unvisited city."""
    if len(cities) <= 1:
        return list(cities)
    unvisited = list(cities)
    path = [unvisited.pop(0)]
    while unvisited:
        cur = path[-1]
        nxt = max(unvisited, key=lambda c: dist(cur, c))
        path.append(nxt)
        unvisited.remove(nxt)
    return path


def worst_case_tour(cities):
    return greedy_longest_path(cities)


# --------------------------------------------------------------------
# Axis pairs (four canonical pairs in a rotated frame)
# --------------------------------------------------------------------

def make_axis_pairs(theta):
    c, s = math.cos(theta), math.sin(theta)
    rx = lambda p: p[0] * c + p[1] * s
    ry = lambda p: -p[0] * s + p[1] * c
    return [
        (rx,                              ry),
        (lambda p: rx(p) + ry(p),         lambda p: rx(p) - ry(p)),
        (ry,                              rx),
        (lambda p: rx(p) - ry(p),         lambda p: rx(p) + ry(p)),
    ]


# --------------------------------------------------------------------
# Section solvers
# --------------------------------------------------------------------

def brute_force_path(cities):
    if len(cities) <= 1:
        return list(cities)
    best, best_len = None, float("inf")
    for perm in itertools.permutations(cities):
        l = sum(dist(perm[i], perm[i + 1]) for i in range(len(perm) - 1))
        if l < best_len:
            best_len, best = l, list(perm)
    return best


def minmax_path(cities):
    """Greedy: at each step, minimise the running MAXIMUM edge."""
    if len(cities) <= 1:
        return list(cities)
    unvisited = list(cities)
    path = [unvisited.pop(0)]
    current_max = 0.0
    while unvisited:
        current = path[-1]
        best_city, best_max = None, float("inf")
        for c in unvisited:
            cm = max(current_max, dist(current, c))
            if cm < best_max:
                best_max, best_city = cm, c
        path.append(best_city)
        current_max = max(current_max, dist(path[-2], best_city))
        unvisited.remove(best_city)
    return path


def maxmin_path(cities):
    """Greedy: at each step, maximise the running MINIMUM edge."""
    if len(cities) <= 1:
        return list(cities)
    unvisited = list(cities)
    path = [unvisited.pop(0)]
    current_min = float("inf")
    while unvisited:
        current = path[-1]
        best_city, best_min = None, float("-inf")
        for c in unvisited:
            cm = min(current_min, dist(current, c))
            if cm > best_min:
                best_min, best_city = cm, c
        new_edge = dist(path[-1], best_city)
        path.append(best_city)
        current_min = min(current_min, new_edge)
        unvisited.remove(best_city)
    return path


def solve_section(cities, bf_threshold, mode):
    if len(cities) <= bf_threshold:
        return brute_force_path(cities)
    if mode == "minmax":
        return minmax_path(cities)
    if mode == "maxmin":
        return maxmin_path(cities)
    raise ValueError(f"unknown mode {mode!r}")


# --------------------------------------------------------------------
# Subdivision and connection
# --------------------------------------------------------------------

def subdivide(cities, axes, depth):
    if depth == 0 or len(cities) <= 1:
        return [cities]
    axis_fn = axes[0]
    sorted_cities = sorted(cities, key=axis_fn)
    mid = len(sorted_cities) // 2
    left = subdivide(sorted_cities[:mid], axes[1:] + axes[:1], depth - 1)
    right = subdivide(sorted_cities[mid:], axes[1:] + axes[:1], depth - 1)
    return left + right


def brute_force_connect(paths):
    if len(paths) == 1:
        return paths[0]
    first = paths[0]
    rest = paths[1:]
    best_tour, best_len = None, float("inf")
    for ordering in itertools.permutations(range(len(rest))):
        for flips in itertools.product([False, True], repeat=len(rest)):
            tour = list(first)
            for idx, flip in zip(ordering, flips):
                tour += rest[idx][::-1] if flip else rest[idx]
            l = tour_length(tour)
            if l < best_len:
                best_len, best_tour = l, tour
    return best_tour


# --------------------------------------------------------------------
# Depth and angle schedules
# --------------------------------------------------------------------

def sandclock_depths(d_max):
    """Depth schedule 1, 2, ..., d_max, d_max-1, ..., 1."""
    if d_max <= 0:
        return []
    up = list(range(1, d_max + 1))
    down = list(range(d_max - 1, 0, -1))
    return up + down


def mill_angles_for_depth(d, max_n_per_direction=None, cw_first=True):
    """
    Bidirectional mill (BREADTH) at depth d.

    Step is one third of the section angle alpha_d = pi / 2^d, so three
    consecutive same-direction steps cover one full section. Within
    [0, pi/2) we interleave forward and backward third-steps:

        cw_first=True  -> [0, +s, -s, +2s, -2s, ...]
        cw_first=False -> [0, -s, +s, -2s, +2s, ...]
    """
    segment = math.pi / (2 ** d)
    step = segment / 3.0
    n_per_direction = max(1, int(round((math.pi / 2.0) / step)))
    if max_n_per_direction is not None:
        n_per_direction = min(n_per_direction, max_n_per_direction)
    sign = +1.0 if cw_first else -1.0
    angles = [0.0]
    for k in range(1, n_per_direction):
        angles.append(+sign * k * step)
        angles.append(-sign * k * step)
    return angles


def sieve_amplitudes(d, n_sift_cap):
    """
    Damped fan amplitudes (DEPTH) around a centre angle, at depth d.

        amplitudes = [step/2, step/4, step/8, ..., step/2^n_sift_cap]
    """
    segment = math.pi / (2 ** d)
    step = segment / 3.0
    return [step / (2 ** (k + 1)) for k in range(n_sift_cap)]


# --------------------------------------------------------------------
# Per-(depth, angle) evaluation
# --------------------------------------------------------------------

def _eval_at(cities, theta, depth, bf_threshold, mode, best, best_len):
    """Try all 4 axis pairs at this (theta, depth); update best."""
    hit = False
    for primary, secondary in make_axis_pairs(theta):
        sections = subdivide(cities, [primary, secondary], depth)
        paths = [solve_section(s, bf_threshold, mode) for s in sections if s]
        tour = brute_force_connect(paths)
        l = tour_length(tour)
        if l + 1e-12 < best_len:
            best_len, best = l, tour
            hit = True
    return best, best_len, hit


# --------------------------------------------------------------------
# Mill sweep (breadth) and sieve sweep (depth)
# --------------------------------------------------------------------

def _mill_sweep(cities, d_max, n_rot_cap, bf_threshold, mode, cw_first,
                best, best_len):
    improved = False
    best_theta = 0.0
    best_d = d_max
    for d in sandclock_depths(d_max):
        for theta in mill_angles_for_depth(d, max_n_per_direction=n_rot_cap,
                                           cw_first=cw_first):
            best, best_len, hit = _eval_at(cities, theta, d, bf_threshold,
                                           mode, best, best_len)
            if hit:
                improved = True
                best_theta, best_d = theta, d
    return best, best_len, improved, best_theta, best_d


def _sieve_sweep(cities, d, theta_center, n_sift_cap, bf_threshold, mode,
                 cw_first, best, best_len):
    improved = False
    sign_first = +1.0 if cw_first else -1.0
    theta = theta_center
    for delta in sieve_amplitudes(d, n_sift_cap):
        for sign in (sign_first, -sign_first):
            t = theta + sign * delta
            best, best_len, hit = _eval_at(cities, t, d, bf_threshold,
                                           mode, best, best_len)
            if hit:
                improved = True
                theta = t
    return best, best_len, improved


def _sandclock_sweep(cities, d_max, n_rot_cap, n_sift_cap, bf_threshold,
                     mode, cw_first, best, best_len):
    best, best_len, mill_imp, theta_star, d_star = _mill_sweep(
        cities, d_max, n_rot_cap, bf_threshold, mode, cw_first,
        best, best_len,
    )
    best, best_len, sieve_imp = _sieve_sweep(
        cities, d_star, theta_star, n_sift_cap, bf_threshold, mode,
        cw_first, best, best_len,
    )
    return best, best_len, mill_imp, sieve_imp


# --------------------------------------------------------------------
# Phase 4: 8-state super-cycle (mode, direction, ordering)
# --------------------------------------------------------------------

_CYCLE_MD = [
    ("maxmin", True),
    ("minmax", True),
    ("maxmin", False),
    ("minmax", False),
]
_CYCLE_DM = [
    ("maxmin", True),
    ("maxmin", False),
    ("minmax", True),
    ("minmax", False),
]
_SUPERCYCLE = _CYCLE_MD + _CYCLE_DM   # length 8


def sift_tsp(cities, d_ceiling=3, n_rot_ceiling=8, n_sift_ceiling=4,
             bf_threshold=6, verbose=False):
    """
    SiftTSP main entry point. Phases:

        1. Worst-case start (once).
        2. Mill (breadth) + sieve (depth) sweep at current
           (d_max, m_rot, s_sift) for the current super-cycle config.
        3. Brute-force exact at sections of size <= bf_threshold.
        4. 8-state super-cycle over (mode, direction, ordering). Mill
           and sieve ceilings double independently on their own
           improvements. d_max is bumped after 8 consecutive
           non-improving super-steps at the same rung.
    """
    best = worst_case_tour(list(cities))
    best_len = tour_length(best)
    if verbose:
        print(f"[init] worst-case length = {best_len:.4f}")

    for d_max in range(1, d_ceiling + 1):
        m_rot = 1
        s_sift = 1
        k = 0
        consec_no_improve = 0

        while m_rot <= n_rot_ceiling or s_sift <= n_sift_ceiling:
            mode, cw_first = _SUPERCYCLE[k % len(_SUPERCYCLE)]
            ordering = "MD" if (k % len(_SUPERCYCLE)) < 4 else "DM"

            m_eff = min(m_rot, n_rot_ceiling)
            s_eff = min(s_sift, n_sift_ceiling)

            best, best_len, mill_imp, sieve_imp = _sandclock_sweep(
                cities, d_max, m_eff, s_eff,
                bf_threshold, mode, cw_first, best, best_len,
            )
            improved = mill_imp or sieve_imp

            if verbose:
                tag = ("mill+sieve" if mill_imp and sieve_imp
                       else "mill" if mill_imp
                       else "sieve" if sieve_imp
                       else "converged")
                dir_lbl = "CW " if cw_first else "CCW"
                print(f"[d_max={d_max}, m={m_eff:>2}, s={s_eff:>2}, "
                      f"k={k % 8}, ord={ordering}, "
                      f"cfg=({mode},{dir_lbl})] "
                      f"best={best_len:.4f} ({tag})")

            k += 1
            if improved:
                consec_no_improve = 0
                if mill_imp and m_rot <= n_rot_ceiling:
                    m_rot *= 2
                if sieve_imp and s_sift <= n_sift_ceiling:
                    s_sift *= 2
            else:
                consec_no_improve += 1
                if consec_no_improve >= len(_SUPERCYCLE):
                    break

    return best


def tsp_adaptive(cities, depth=3, bf_threshold=6, max_rounds=20):
    """Backwards-compatible alias used by counterexample.py and tests."""
    return sift_tsp(cities, d_ceiling=depth, bf_threshold=bf_threshold)


# Backwards-compatible alias for the iteration-17 name.
tsp_progressive = sift_tsp


def tsp_exact(cities):
    """Brute-force exact TSP. Used only for n <= ~10 sanity checks."""
    best, best_len = None, float("inf")
    for perm in itertools.permutations(cities[1:]):
        tour = [cities[0]] + list(perm)
        l = tour_length(tour)
        if l < best_len:
            best_len, best = l, tour
    return best


if __name__ == "__main__":
    cities_10 = [
        (0, 0), (2, 4), (5, 2), (6, 7), (1, 9),
        (8, 1), (9, 5), (4, 8), (7, 3), (3, 6),
    ]

    opt_len = tour_length(tsp_exact(list(cities_10)))
    worst_len = tour_length(worst_case_tour(list(cities_10)))
    print("=" * 65)
    print("SiftTSP - Geometric Sandclock-Sift Heuristic")
    print("=" * 65)
    print(f"Optimal     : {opt_len:.4f}")
    print(f"Worst case  : {worst_len:.4f}  "
          f"({(worst_len/opt_len-1)*100:+.1f}%)")
    print()
    tour = sift_tsp(list(cities_10), d_ceiling=2,
                    n_rot_ceiling=4, n_sift_ceiling=2,
                    bf_threshold=6, verbose=False)
    final = tour_length(tour)
    gap = ((final / opt_len) - 1) * 100
    marker = " EXACT" if gap < 0.001 else ""
    print(f"Heuristic   : {final:.4f}  gap = {gap:+.2f}%{marker}")
