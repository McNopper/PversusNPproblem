"""
Depth-First Search - Class P
============================
Depth-first search (DFS) explores a graph by following one branch as far as
possible before backtracking. DFS can also detect cycles in a directed graph
by tracking the recursion stack.

DFS is in P because it runs in O(V + E) time, which is polynomial in the size
of the graph. Each vertex and edge is processed only a constant number of
times.
"""


def dfs_traversal(graph: dict[str, list[str]], start: str) -> list[str]:
    """Return vertices in a DFS preorder traversal from start."""
    visited: set[str] = set()
    order: list[str] = []

    def visit(node: str) -> None:
        visited.add(node)
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def has_cycle_directed(graph: dict[str, list[str]]) -> bool:
    """Detect whether a directed graph contains a cycle."""
    visited: set[str] = set()
    active: set[str] = set()

    def visit(node: str) -> bool:
        visited.add(node)
        active.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if visit(neighbor):
                    return True
            elif neighbor in active:
                return True

        active.remove(node)
        return False

    for vertex in graph:
        if vertex not in visited and visit(vertex):
            return True

    return False


if __name__ == "__main__":
    traversal_graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": [],
        "F": [],
    }
    cycle_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A", "D"],
        "D": [],
    }

    order = dfs_traversal(traversal_graph, "A")
    cycle_found = has_cycle_directed(cycle_graph)

    print(f"DFS preorder from A: {order}")
    print(f"Cycle detected in directed graph: {cycle_found}")
