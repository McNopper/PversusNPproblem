"""
All-Pairs Shortest Path - Class P
=================================
The Floyd-Warshall algorithm computes shortest path distances between every
pair of vertices by considering intermediate vertices one by one.

This problem is in P because Floyd-Warshall runs in O(V^3) time, which is
polynomial in the number of vertices.
"""


def floyd_warshall(graph: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """Return all-pairs shortest path distances."""
    vertices = sorted(graph)
    dist = {
        u: {v: float("inf") for v in vertices}
        for u in vertices
    }

    for vertex in vertices:
        dist[vertex][vertex] = 0.0

    for u, edges in graph.items():
        for v, weight in edges.items():
            dist[u][v] = min(dist[u][v], float(weight))

    for k in vertices:
        for i in vertices:
            for j in vertices:
                through_k = dist[i][k] + dist[k][j]
                if through_k < dist[i][j]:
                    dist[i][j] = through_k

    return dist


if __name__ == "__main__":
    graph = {
        "A": {"B": 3, "C": 8, "E": -4},
        "B": {"D": 1, "E": 7},
        "C": {"B": 4},
        "D": {"A": 2, "C": -5},
        "E": {"D": 6},
    }

    distances = floyd_warshall(graph)
    print("Shortest distances from Floyd-Warshall:")
    for source in sorted(distances):
        print(f"  {source}: {distances[source]}")
