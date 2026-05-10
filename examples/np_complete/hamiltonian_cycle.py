"""
Hamiltonian Cycle -- NP-Complete
==================================
Given a graph, does it contain a cycle that visits every vertex exactly once
and returns to the starting vertex?

Differs from Hamiltonian Path: the last node must connect back to the first.

Verifier:  Check cycle visits all nodes once and all edges exist -- O(V).
Solver:    Backtracking -- O(V!) worst case.
"""


def verify(graph: dict, cycle: list) -> bool:
    nodes = set(graph.keys())
    if set(cycle) != nodes or len(cycle) != len(nodes):
        return False
    for i in range(len(cycle)):
        u = cycle[i]
        v = cycle[(i + 1) % len(cycle)]
        if v not in graph[u]:
            return False
    return True


def solve(graph: dict) -> list | None:
    nodes = list(graph.keys())
    n = len(nodes)

    def backtrack(path, visited):
        if len(path) == n:
            # Check if last node connects back to start
            return path[0] in graph[path[-1]]
        current = path[-1]
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                if backtrack(path, visited):
                    return True
                path.pop()
                visited.remove(neighbor)
        return False

    for start in nodes:
        path = [start]
        if backtrack(path, {start}):
            return path
    return None


if __name__ == "__main__":
    # Graph with a Hamiltonian cycle
    graph_yes = {
        "A": ["B", "E"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C", "E"],
        "E": ["D", "A"],
    }

    # Graph without a Hamiltonian cycle (bridge node)
    graph_no = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C", "E"],
        "E": ["D"],
    }

    for label, graph in [("Cycle graph (yes)", graph_yes), ("Bridge graph (no)", graph_no)]:
        cycle = solve(graph)
        print(f"\n{label}:")
        if cycle:
            route = " -> ".join(cycle) + f" -> {cycle[0]}"
            print(f"  Hamiltonian cycle: {route}")
            print(f"  Verification: {verify(graph, cycle)}")
        else:
            print("  No Hamiltonian cycle exists.")
