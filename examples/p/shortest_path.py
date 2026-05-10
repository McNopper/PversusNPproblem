"""
Shortest Path -- Class P
=======================
Dijkstra's algorithm finds the shortest path from a source node to all
other nodes in a weighted graph with non-negative edge weights.

Time complexity: O((V + E) log V) with a min-heap -- polynomial in the
size of the graph, so it belongs to P.
"""

import heapq


def dijkstra(graph: dict, source: str) -> dict:
    """
    Returns a dict of shortest distances from source to every reachable node.
    graph[u] = [(weight, v), ...] adjacency list with weights.
    """
    dist = {node: float("inf") for node in graph}
    dist[source] = 0
    heap = [(0, source)]  # (distance, node)

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for weight, v in graph.get(u, []):
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist


if __name__ == "__main__":
    # Example graph (city map)
    graph = {
        "A": [(1, "B"), (4, "C")],
        "B": [(1, "A"), (2, "C"), (5, "D")],
        "C": [(4, "A"), (2, "B"), (1, "D")],
        "D": [(5, "B"), (1, "C")],
    }

    source = "A"
    distances = dijkstra(graph, source)
    print(f"Shortest distances from '{source}':")
    for node, dist in sorted(distances.items()):
        print(f"  {source} -> {node}: {dist}")
