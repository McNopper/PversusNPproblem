"""
Topological Sort - Class P
==========================
A topological ordering of a directed acyclic graph (DAG) lists vertices so
that every directed edge u -> v places u before v. Kahn's algorithm repeatedly
removes vertices with indegree zero.

The algorithm is in P because it runs in O(V + E) time, which is polynomial in
the size of the graph. Every vertex enters the queue at most once and every
edge is considered once when indegrees are updated.
"""

from collections import deque


def kahn_topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Return a topological ordering, or raise ValueError if a cycle exists."""
    indegree = {node: 0 for node in graph}

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            indegree.setdefault(neighbor, 0)
            indegree[neighbor] += 1

    queue = deque(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(indegree):
        raise ValueError("Graph contains a cycle, so no topological ordering exists.")

    return order


if __name__ == "__main__":
    dag = {
        "plan": ["shop", "cook"],
        "shop": ["cook"],
        "cook": ["eat"],
        "eat": [],
    }

    ordering = kahn_topological_sort(dag)
    print(f"Topological order: {ordering}")
