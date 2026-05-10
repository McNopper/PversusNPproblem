"""
Breadth-First Search - Class P
==============================
Breadth-first search (BFS) explores a graph level by level. In an unweighted
graph, the first time BFS reaches a vertex, it has found a shortest path in
number of edges.

BFS is in P because it runs in O(V + E) time, which is polynomial in the size
of the graph. Each vertex is processed at most once and each edge is examined
at most once.
"""

from collections import deque


def bfs_traversal(graph: dict[str, list[str]], start: str) -> list[str]:
    """Return vertices in the order visited by BFS."""
    visited = {start}
    queue = deque([start])
    order: list[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def shortest_path_unweighted(
    graph: dict[str, list[str]], start: str, goal: str
) -> list[str] | None:
    """Return one shortest path from start to goal, or None if unreachable."""
    if start == goal:
        return [start]

    visited = {start}
    parent: dict[str, str | None] = {start: None}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            parent[neighbor] = node

            if neighbor == goal:
                path = [goal]
                current = goal
                while parent[current] is not None:
                    current = parent[current]
                    path.append(current)
                path.reverse()
                return path

            queue.append(neighbor)

    return None


if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }

    order = bfs_traversal(graph, "A")
    path = shortest_path_unweighted(graph, "A", "F")

    print(f"BFS order from A: {order}")
    print(f"Shortest path from A to F: {path}")
