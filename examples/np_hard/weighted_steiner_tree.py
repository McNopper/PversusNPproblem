"""
Weighted Steiner Tree -- NP-Hard optimization
=============================================
Given a weighted undirected graph and a required set of terminal vertices, find
a minimum-weight connected subgraph that spans all terminals. The solution may
include extra non-terminal vertices called Steiner vertices.

Why NP-Hard:
- The decision version asks whether there is a Steiner tree of weight at most K.
- That decision problem is NP-Complete.
- Therefore, the optimization version is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- The decision version is in NP because a proposed tree can be checked in
  polynomial time.

Key properties:
- Steiner tree generalizes minimum spanning tree.
- When every vertex is a terminal, the problem becomes MST and is easy.
- Exact search is exponential.

This module includes:
- A brute-force exact solver over edge subsets for small graphs.
- A metric-closure MST heuristic followed by pruning.
"""

from heapq import heappop, heappush
from itertools import combinations


def normalize_edges(edges):
    result = {}
    for u, v, w in edges:
        key = tuple(sorted((u, v)))
        result[key] = min(w, result.get(key, float("inf")))
    return [(u, v, w) for (u, v), w in result.items()]


def vertices_from_edges(edges):
    vertices = set()
    for u, v, _ in edges:
        vertices.add(u)
        vertices.add(v)
    return sorted(vertices)


def adjacency_from_edges(edges):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
    return graph


def is_tree_spanning_terminals(edge_subset, terminals):
    if not edge_subset:
        return len(terminals) <= 1
    vertices = set()
    for u, v, _ in edge_subset:
        vertices.add(u)
        vertices.add(v)
    if not set(terminals) <= vertices:
        return False
    if len(edge_subset) != len(vertices) - 1:
        return False
    graph = adjacency_from_edges(edge_subset)
    start = next(iter(vertices))
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor, _ in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen == vertices


def brute_force_steiner_tree(edges, terminals):
    edges = normalize_edges(edges)
    best_edges = None
    best_weight = float("inf")
    for size in range(len(terminals) - 1, len(edges) + 1):
        for subset in combinations(edges, size):
            total = sum(weight for _, _, weight in subset)
            if total >= best_weight:
                continue
            if is_tree_spanning_terminals(subset, terminals):
                best_weight = total
                best_edges = list(subset)
    return best_edges, best_weight


def shortest_path(graph, source, target):
    heap = [(0, source, [])]
    best = {source: 0}
    while heap:
        distance, node, path = heappop(heap)
        if node == target:
            return distance, path
        if distance > best[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            next_distance = distance + weight
            if next_distance < best.get(neighbor, float("inf")):
                best[neighbor] = next_distance
                heappush(heap, (next_distance, neighbor, path + [(node, neighbor, weight)]))
    return float("inf"), []


def mst_complete_graph(vertices, weight_lookup):
    chosen = {vertices[0]}
    tree_edges = []
    while len(chosen) < len(vertices):
        best_edge = None
        best_weight = float("inf")
        for u in chosen:
            for v in vertices:
                if v in chosen or u == v:
                    continue
                weight = weight_lookup[(u, v)]
                if weight < best_weight:
                    best_weight = weight
                    best_edge = (u, v)
        tree_edges.append(best_edge)
        chosen.add(best_edge[1])
    return tree_edges


def prune_steiner_leaves(edges, terminals):
    edges = [tuple(sorted((u, v))) + (w,) for u, v, w in edges]
    changed = True
    while changed:
        changed = False
        degree = {}
        for u, v, _ in edges:
            degree[u] = degree.get(u, 0) + 1
            degree[v] = degree.get(v, 0) + 1
        for edge in list(edges):
            u, v, w = edge
            leaf = None
            if degree.get(u, 0) == 1 and u not in terminals:
                leaf = u
            elif degree.get(v, 0) == 1 and v not in terminals:
                leaf = v
            if leaf is not None:
                edges.remove(edge)
                changed = True
                break
    dedup = {}
    for u, v, w in edges:
        key = tuple(sorted((u, v)))
        dedup[key] = min(w, dedup.get(key, float("inf")))
    return [(u, v, w) for (u, v), w in dedup.items()]


def steiner_tree_mst_heuristic(edges, terminals):
    graph = adjacency_from_edges(normalize_edges(edges))
    terminals = sorted(terminals)
    weight_lookup = {}
    path_lookup = {}
    for u in terminals:
        for v in terminals:
            if u == v:
                continue
            distance, path = shortest_path(graph, u, v)
            weight_lookup[(u, v)] = distance
            path_lookup[(u, v)] = path
    metric_tree = mst_complete_graph(terminals, weight_lookup)
    expanded = []
    for u, v in metric_tree:
        expanded.extend(path_lookup[(u, v)])
    pruned = prune_steiner_leaves(expanded, set(terminals))
    weight = sum(w for _, _, w in pruned)
    return pruned, weight


if __name__ == "__main__":
    edges = [
        ("A", "B", 1),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 2),
        ("C", "E", 2),
        ("D", "E", 1),
        ("D", "F", 3),
        ("E", "F", 2),
        ("C", "D", 2),
    ]
    terminals = {"A", "D", "F"}

    exact_edges, exact_weight = brute_force_steiner_tree(edges, terminals)
    heuristic_edges, heuristic_weight = steiner_tree_mst_heuristic(edges, terminals)

    print("Weighted Steiner Tree (NP-Hard)")
    print(f"Terminals: {sorted(terminals)}")
    print(f"Exact tree weight:     {exact_weight}, edges = {exact_edges}")
    print(f"Heuristic tree weight: {heuristic_weight}, edges = {heuristic_edges}")
