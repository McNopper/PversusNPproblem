"""
Baseline TSP algorithms for honest comparison against `tsp.py`.

Includes:
  - held_karp: exact O(n^2 * 2^n) DP, feasible to n ~= 20
  - nearest_neighbor: classic O(n^2) heuristic
  - two_opt: 2-opt local search starting from NN
"""

import math
import itertools


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def tour_length(tour):
    n = len(tour)
    return sum(dist(tour[i], tour[(i + 1) % n]) for i in range(n))


def held_karp(cities):
    """Exact TSP via Bellman-Held-Karp DP. O(n^2 * 2^n)."""
    n = len(cities)
    if n <= 1:
        return list(cities)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0.0
    for mask in range(1 << n):
        if not (mask & 1):
            continue
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            if dp[mask][i] == INF:
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                new_mask = mask | (1 << j)
                cand = dp[mask][i] + dist(cities[i], cities[j])
                if cand < dp[new_mask][j]:
                    dp[new_mask][j] = cand
                    parent[new_mask][j] = i
    full = (1 << n) - 1
    best_cost = INF
    best_end = -1
    for i in range(1, n):
        c = dp[full][i] + dist(cities[i], cities[0])
        if c < best_cost:
            best_cost = c
            best_end = i
    tour = []
    mask = full
    cur = best_end
    while cur != -1:
        tour.append(cities[cur])
        prev = parent[mask][cur]
        mask ^= 1 << cur
        cur = prev
    tour.reverse()
    return tour


def nearest_neighbor(cities):
    if not cities:
        return []
    unvisited = list(cities[1:])
    tour = [cities[0]]
    while unvisited:
        cur = tour[-1]
        nxt = min(unvisited, key=lambda c: dist(cur, c))
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour


def two_opt(cities, max_passes=100):
    tour = nearest_neighbor(cities)
    n = len(tour)
    if n < 4:
        return tour
    improved = True
    passes = 0
    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = (dist(a, c) + dist(b, d)) - (dist(a, b) + dist(c, d))
                if delta < -1e-12:
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    improved = True
    return tour


def brute_force_exact(cities):
    """Exact via permutation enumeration. Only feasible for n <= 11."""
    if len(cities) <= 1:
        return list(cities)
    best, best_len = None, float("inf")
    fixed = cities[0]
    for perm in itertools.permutations(cities[1:]):
        tour = [fixed] + list(perm)
        l = tour_length(tour)
        if l < best_len:
            best_len, best = l, tour
    return best
