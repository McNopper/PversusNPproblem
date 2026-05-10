"""
Euler Path - Class P
====================
An Euler path in an undirected graph uses every edge exactly once. Hierholzer's
algorithm constructs such a path or circuit by following unused edges and then
backtracking when it gets stuck.

The problem is in P because Hierholzer's algorithm runs in O(E) time after the
initial degree and connectivity checks, which is polynomial in the graph size.
"""


def find_euler_path(graph: dict[str, list[str]]) -> list[str] | None:
    """Return an Euler path or circuit for a simple undirected graph, or None."""
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    non_isolated = [node for node, degree in degrees.items() if degree > 0]
    if not non_isolated:
        return []

    odd_vertices = [node for node, degree in degrees.items() if degree % 2 == 1]
    if len(odd_vertices) not in (0, 2):
        return None

    start = odd_vertices[0] if odd_vertices else non_isolated[0]

    # Check that every non-isolated vertex lies in one connected component.
    stack = [start]
    connected: set[str] = set()
    while stack:
        node = stack.pop()
        if node in connected:
            continue
        connected.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in connected:
                stack.append(neighbor)

    if any(node not in connected for node in non_isolated):
        return None

    # Give each undirected edge a shared id on both endpoints.
    adjacency: dict[str, list[tuple[str, int]]] = {node: [] for node in graph}
    edge_id = 0
    seen_edges: set[tuple[str, str]] = set()

    for u, neighbors in graph.items():
        for v in neighbors:
            edge_key = (u, v) if u <= v else (v, u)
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)
            adjacency[u].append((v, edge_id))
            adjacency[v].append((u, edge_id))
            edge_id += 1

    traversal_stack = [start]
    used_edges: set[int] = set()
    path: list[str] = []

    while traversal_stack:
        node = traversal_stack[-1]
        while adjacency[node] and adjacency[node][-1][1] in used_edges:
            adjacency[node].pop()

        if adjacency[node]:
            neighbor, current_edge = adjacency[node].pop()
            used_edges.add(current_edge)
            traversal_stack.append(neighbor)
        else:
            path.append(traversal_stack.pop())

    if len(path) != edge_id + 1:
        return None

    path.reverse()
    return path


if __name__ == "__main__":
    graph = {
        "A": ["B", "D"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["A", "C"],
    }

    euler_walk = find_euler_path(graph)
    print(f"Euler path or circuit: {euler_walk}")
