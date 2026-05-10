"""
Minimum Bisection -- NP-Hard optimization
=========================================
Given an undirected graph with an even number of vertices, split the vertices
into two equal-size parts while minimizing the number of crossing edges.

Why NP-Hard:
- The decision version asks whether there is an equal split with cut size at
  most K.
- That problem is NP-Complete.
- Therefore, finding the minimum bisection is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because a proposed bisection can be checked in
  polynomial time.

Key properties:
- Balance makes the problem much harder than unconstrained cut minimization.
- Spectral methods use the graph Laplacian and the Fiedler vector to suggest a
  good partition.
- Exact search is exponential.

This module includes:
- A brute-force exact solver.
- A small pure-Python spectral heuristic based on Jacobi eigenvalue iteration.
"""

from itertools import combinations


def normalize_graph(graph):
    normalized = {v: set(neighbors) for v, neighbors in graph.items()}
    for v in list(normalized):
        for u in normalized[v]:
            normalized.setdefault(u, set()).add(v)
    return normalized


def cut_size(graph, side_a):
    side_a = set(side_a)
    total = 0
    for u in graph:
        for v in graph[u]:
            if str(u) < str(v) and ((u in side_a) != (v in side_a)):
                total += 1
    return total


def brute_force_minimum_bisection(graph):
    vertices = list(graph)
    n = len(vertices)
    if n % 2 != 0:
        raise ValueError("Minimum bisection requires an even number of vertices.")
    anchor = vertices[0]
    best_side = None
    best_value = float("inf")
    for subset in combinations(vertices[1:], n // 2 - 1):
        side_a = {anchor, *subset}
        value = cut_size(graph, side_a)
        if value < best_value:
            best_value = value
            best_side = side_a
    return sorted(best_side), best_value


def jacobi_eigendecomposition(matrix, tolerance=1e-10, max_iterations=100):
    n = len(matrix)
    a = [row[:] for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iterations):
        p, q = 0, 1
        max_off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > max_off:
                    max_off = abs(a[i][j])
                    p, q = i, j
        if max_off < tolerance:
            break
        if a[p][p] == a[q][q]:
            angle = 0.7853981633974483
        else:
            angle = 0.5 * __import__("math").atan2(2 * a[p][q], a[q][q] - a[p][p])
        c = __import__("math").cos(angle)
        s = __import__("math").sin(angle)
        app = c * c * a[p][p] - 2 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2 * s * c * a[p][q] + c * c * a[q][q]
        a[p][q] = 0.0
        a[q][p] = 0.0
        a[p][p] = app
        a[q][q] = aqq
        for r in range(n):
            if r not in (p, q):
                arp = c * a[r][p] - s * a[r][q]
                arq = s * a[r][p] + c * a[r][q]
                a[r][p] = a[p][r] = arp
                a[r][q] = a[q][r] = arq
        for r in range(n):
            vrp = c * v[r][p] - s * v[r][q]
            vrq = s * v[r][p] + c * v[r][q]
            v[r][p] = vrp
            v[r][q] = vrq
    eigenpairs = []
    for i in range(n):
        vector = [v[r][i] for r in range(n)]
        eigenpairs.append((a[i][i], vector))
    eigenpairs.sort(key=lambda item: item[0])
    return eigenpairs


def spectral_bisection(graph):
    vertices = list(graph)
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    laplacian = [[0.0 for _ in range(n)] for _ in range(n)]
    for u in vertices:
        i = index[u]
        laplacian[i][i] = float(len(graph[u]))
        for v in graph[u]:
            if u != v:
                laplacian[i][index[v]] = -1.0
    eigenpairs = jacobi_eigendecomposition(laplacian)
    fiedler_vector = eigenpairs[1][1]
    ordered = sorted(zip(fiedler_vector, vertices))
    side_a = [vertex for _, vertex in ordered[: n // 2]]
    return side_a, cut_size(graph, side_a)


if __name__ == "__main__":
    graph = normalize_graph(
        {
            "A": {"B", "C", "D"},
            "B": {"A", "C", "E"},
            "C": {"A", "B", "F"},
            "D": {"A", "E", "F"},
            "E": {"B", "D", "F"},
            "F": {"C", "D", "E"},
        }
    )

    exact_side, exact_value = brute_force_minimum_bisection(graph)
    spectral_side, spectral_value = spectral_bisection(graph)

    print("Minimum Bisection (NP-Hard)")
    print(f"Exact side A:     {exact_side}, cut size = {exact_value}")
    print(f"Spectral side A:  {sorted(spectral_side)}, cut size = {spectral_value}")
