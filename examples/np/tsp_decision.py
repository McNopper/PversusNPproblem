"""
Travelling Salesman — Decision Version — Class NP
==================================================
Given a weighted graph and a bound B, decide whether there exists a tour
(a path visiting every city exactly once and returning to start) with total
distance ≤ B.

- Verifier: Given a candidate tour, compute its length and check ≤ B — O(n).
- Solver:   Brute-force over all (n-1)! permutations — exponential.

The *optimization* version (find the shortest tour) is NP-Hard.
"""

from itertools import permutations


def tour_length(tour: list, dist: dict) -> float:
    """Compute the total length of a tour (including return to start)."""
    total = 0
    n = len(tour)
    for i in range(n):
        u, v = tour[i], tour[(i + 1) % n]
        edge = (u, v) if (u, v) in dist else (v, u)
        total += dist.get(edge, float("inf"))
    return total


def verify(tour: list, cities: list, dist: dict, bound: float) -> bool:
    """Verifier: checks the tour visits all cities once and length ≤ bound."""
    if sorted(tour) != sorted(cities):
        return False
    return tour_length(tour, dist) <= bound


def solve_tsp_decision(cities: list, dist: dict, bound: float) -> list | None:
    """Brute-force: tries all permutations to find a tour within the bound."""
    start = cities[0]
    rest = cities[1:]
    for perm in permutations(rest):
        tour = [start] + list(perm)
        if tour_length(tour, dist) <= bound:
            return tour
    return None


if __name__ == "__main__":
    cities = ["A", "B", "C", "D"]
    dist = {
        ("A", "B"): 10,
        ("A", "C"): 15,
        ("A", "D"): 20,
        ("B", "C"): 35,
        ("B", "D"): 25,
        ("C", "D"): 30,
    }

    print("Cities:", cities)
    print("Distances:", {f"{u}-{v}": w for (u, v), w in dist.items()})

    for bound in [80, 60]:
        print(f"\nIs there a tour with total distance <= {bound}?")
        tour = solve_tsp_decision(cities, dist, bound)
        if tour:
            length = tour_length(tour, dist)
            print(f"  Yes! Tour: {' → '.join(tour)} → {tour[0]}  (length {length})")
            print(f"  Verification: {verify(tour, cities, dist, bound)}")
        else:
            print("  No such tour exists.")
