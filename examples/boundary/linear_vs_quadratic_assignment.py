"""
Linear Assignment (P) vs Quadratic Assignment (NP-Hard)
========================================================
Assignment Problem (Linear):    Assign n workers to n jobs minimizing total cost.
                                 Solved optimally by the Hungarian algorithm O(n^3).

Quadratic Assignment Problem (QAP): Assign n facilities to n locations minimizing
                                     flow * distance interactions (quadratic objective).
                                     NP-Hard -- one of the hardest combinatorial problems.

Real-world QAP: hospital layout, keyboard key placement, circuit board design,
                typewriter key arrangement (the QWERTY keyboard was a QAP solution).
"""

from itertools import permutations


# ── Hungarian Algorithm for Linear Assignment (Polynomial O(n^3)) ─────────────

def hungarian(cost: list[list]) -> tuple:
    """
    Hungarian algorithm for minimum-cost linear assignment.
    Returns (min_cost, assignment list where assignment[i] = job for worker i).
    """
    n = len(cost)
    # Pad to square if needed
    inf = float("inf")

    # Simple O(n^3) implementation using the shortest augmenting path method
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)   # p[j] = worker assigned to job j
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minval = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = -1
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minval[j]:
                        minval[j] = cur
                        way[j] = j0
                    if minval[j] < delta:
                        delta = minval[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minval[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            p[j0] = p[way[j0]]
            j0 = way[j0]

    assignment = [0] * n
    for j in range(1, n + 1):
        if p[j]:
            assignment[p[j] - 1] = j - 1

    total = sum(cost[i][assignment[i]] for i in range(n))
    return total, assignment


# ── Quadratic Assignment (NP-Hard -- brute force) ─────────────────────────────

def qap_brute(flow: list[list], dist: list[list]) -> tuple:
    """
    QAP: minimize sum_{i,j} flow[i][j] * dist[perm[i]][perm[j]].
    Brute force over all n! permutations -- exponential.
    Returns (min_cost, best_permutation).
    """
    n = len(flow)
    best_cost = float("inf")
    best_perm = None

    for perm in permutations(range(n)):
        cost = sum(
            flow[i][j] * dist[perm[i]][perm[j]]
            for i in range(n) for j in range(n)
        )
        if cost < best_cost:
            best_cost = cost
            best_perm = perm

    return best_cost, list(best_perm)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Linear assignment: 4 workers x 4 jobs cost matrix
    cost = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]

    la_cost, la_assign = hungarian(cost)
    print("Linear Assignment (Hungarian O(n^3)):")
    for worker, job in enumerate(la_assign):
        print(f"  Worker {worker} -> Job {job}  (cost {cost[worker][job]})")
    print(f"  Total cost: {la_cost}")

    # Quadratic assignment: 4 facilities, 4 locations
    # flow[i][j] = traffic between facilities i and j
    # dist[k][l] = distance between locations k and l
    flow = [
        [0, 5, 2, 4],
        [5, 0, 3, 1],
        [2, 3, 0, 6],
        [4, 1, 6, 0],
    ]
    dist = [
        [0, 3, 5, 9],
        [3, 0, 2, 7],
        [5, 2, 0, 4],
        [9, 7, 4, 0],
    ]

    qap_cost, qap_perm = qap_brute(flow, dist)
    print("\nQuadratic Assignment (brute force O(n!)):")
    for facility, location in enumerate(qap_perm):
        print(f"  Facility {facility} -> Location {location}")
    print(f"  Total interaction cost: {qap_cost}")

    print("\nKey insight:")
    print("  Linear Assignment (worker-job)  -- O(n^3) Hungarian, in P")
    print("  Quadratic Assignment (QAP)      -- NP-Hard, no known poly algorithm")
    print("  QAP hardness: QWERTY keyboard layout, hospital floor plans, chip design")
