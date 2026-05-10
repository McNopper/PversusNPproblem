"""
Travelling Salesman -- Optimization Version -- NP-Hard
======================================================
Given a weighted graph, find the *shortest* possible tour that visits every
city exactly once and returns to the starting city.

This is the *optimization* version of TSP. Unlike the decision version (NP),
this isn't in NP itself (a solution can't be "verified" as optimal in poly-time
without solving the problem) -- making it NP-Hard but not NP-Complete.

Solvers:
  - Brute-force: O((n-1)!) -- exact but exponential
  - Nearest-neighbor heuristic: O(n²) -- fast but not always optimal
"""

from itertools import permutations


def tour_length(tour: list, dist: dict) -> float:
    total = 0
    n = len(tour)
    for i in range(n):
        u, v = tour[i], tour[(i + 1) % n]
        edge = (u, v) if (u, v) in dist else (v, u)
        total += dist.get(edge, float("inf"))
    return total


def solve_brute_force(cities: list, dist: dict) -> tuple:
    """Exact solution: try all (n-1)! permutations. O((n-1)!)."""
    start = cities[0]
    rest = cities[1:]
    best_tour = None
    best_length = float("inf")
    for perm in permutations(rest):
        tour = [start] + list(perm)
        length = tour_length(tour, dist)
        if length < best_length:
            best_length = length
            best_tour = tour
    return best_tour, best_length


def solve_nearest_neighbor(cities: list, dist: dict) -> tuple:
    """
    Greedy heuristic: always go to the nearest unvisited city. O(n²).
    Not guaranteed to be optimal, but fast in practice.
    """
    def edge_dist(u, v):
        return dist.get((u, v), dist.get((v, u), float("inf")))

    unvisited = set(cities[1:])
    tour = [cities[0]]
    while unvisited:
        current = tour[-1]
        nearest = min(unvisited, key=lambda c: edge_dist(current, c))
        tour.append(nearest)
        unvisited.remove(nearest)
    return tour, tour_length(tour, dist)


if __name__ == "__main__":
    cities = ["A", "B", "C", "D", "E"]
    dist = {
        ("A", "B"): 10, ("A", "C"): 15, ("A", "D"): 20, ("A", "E"): 25,
        ("B", "C"): 35, ("B", "D"): 25, ("B", "E"): 30,
        ("C", "D"): 30, ("C", "E"): 10,
        ("D", "E"): 15,
    }

    optimal_tour, optimal_len = solve_brute_force(cities, dist)
    greedy_tour,  greedy_len  = solve_nearest_neighbor(cities, dist)

    route_str = lambda t: " -> ".join(t) + f" -> {t[0]}"

    print("TSP Optimization (NP-Hard)")
    print(f"\n  Optimal (brute-force):        {route_str(optimal_tour)}")
    print(f"  Length: {optimal_len}")
    print(f"  Heuristic (nearest-neighbor): {route_str(greedy_tour)}")
    print(f"  Length: {greedy_len}")
    ratio = greedy_len / optimal_len
    print(f"\n  Heuristic is {ratio:.2f}× the optimal length.")
