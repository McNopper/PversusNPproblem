"""
Hamiltonian Path — Class NP
============================
Given a graph, decide whether there exists a path that visits every node
exactly once (Hamiltonian path).

- Verifier: Given a candidate path, check it visits all nodes once
            and all edges exist — O(V), polynomial.
- Solver:   Backtracking — exponential worst case (O(V!)).
"""


def verify(graph: dict, path: list) -> bool:
    """Verifier: checks path visits each node exactly once, using valid edges."""
    nodes = set(graph.keys())
    if set(path) != nodes or len(path) != len(nodes):
        return False
    for i in range(len(path) - 1):
        if path[i + 1] not in graph[path[i]]:
            return False
    return True


def solve_hamiltonian_path(graph: dict) -> list | None:
    """
    Backtracking solver. Tries every possible starting node.
    Returns a Hamiltonian path or None.
    """
    nodes = list(graph.keys())
    n = len(nodes)

    def backtrack(path, visited):
        if len(path) == n:
            return path
        current = path[-1]
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                result = backtrack(path, visited)
                if result:
                    return result
                path.pop()
                visited.remove(neighbor)
        return None

    for start in nodes:
        result = backtrack([start], {start})
        if result:
            return result
    return None


if __name__ == "__main__":
    # Graph WITH a Hamiltonian path
    graph_with = {
        "A": ["B", "C"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D", "E"],
        "D": ["B", "C", "E"],
        "E": ["C", "D"],
    }

    print("Graph with Hamiltonian path:")
    path = solve_hamiltonian_path(graph_with)
    if path:
        print(f"  Path: {' -> '.join(path)}")
        print(f"  Valid: {verify(graph_with, path)}")
    else:
        print("  No Hamiltonian path exists.")

    # Graph WITHOUT a Hamiltonian path (disconnected)
    graph_without = {
        "A": ["B"],
        "B": ["A"],
        "C": ["D"],
        "D": ["C"],
    }

    print("\nDisconnected graph (no Hamiltonian path):")
    path2 = solve_hamiltonian_path(graph_without)
    print(f"  Result: {'No path found' if path2 is None else path2}")
