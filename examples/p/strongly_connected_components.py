"""
Strongly Connected Components - Class P
=======================================
A strongly connected component (SCC) in a directed graph is a maximal set of
vertices where every vertex can reach every other. Kosaraju's algorithm finds
all SCCs using two depth-first search passes: one on the original graph and
one on the reversed graph.

The algorithm is in P because it runs in O(V + E) time, which is polynomial in
the size of the graph.
"""


def reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Return the graph with all edges reversed."""
    reversed_graph = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph.setdefault(neighbor, []).append(node)
    return reversed_graph



def kosaraju_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    """Return all strongly connected components."""
    visited: set[str] = set()
    finish_order: list[str] = []

    def dfs_first(node: str) -> None:
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_first(neighbor)
        finish_order.append(node)

    for node in graph:
        if node not in visited:
            dfs_first(node)

    reversed_graph = reverse_graph(graph)
    visited.clear()
    components: list[list[str]] = []

    def dfs_second(node: str, component: list[str]) -> None:
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                dfs_second(neighbor, component)

    for node in reversed(finish_order):
        if node not in visited:
            component: list[str] = []
            dfs_second(node, component)
            components.append(component)

    return components


if __name__ == "__main__":
    graph = {
        "A": ["B"],
        "B": ["C", "E", "F"],
        "C": ["D", "G"],
        "D": ["C", "H"],
        "E": ["A", "F"],
        "F": ["G"],
        "G": ["F"],
        "H": ["D", "G"],
    }

    components = kosaraju_scc(graph)
    print(f"Strongly connected components: {components}")
