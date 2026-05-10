"""
2-SAT - Class P
===============
In 2-SAT, each clause contains exactly two literals, and we ask whether there
is a truth assignment satisfying all clauses. The classic linear-time solution
builds an implication graph and computes strongly connected components.

2-SAT is in P because SCC decomposition on the implication graph runs in
O(V + E) time, which is polynomial in the number of variables and clauses.
"""


def negate(literal: str) -> str:
    """Return the opposite literal."""
    return literal[1:] if literal.startswith("!") else f"!{literal}"



def reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Return the graph with all implication directions reversed."""
    reversed_graph = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph.setdefault(neighbor, []).append(node)
    return reversed_graph



def kosaraju_components(graph: dict[str, list[str]]) -> list[list[str]]:
    """Return SCCs in reverse topological order of the component graph."""
    visited: set[str] = set()
    order: list[str] = []

    def dfs_first(node: str) -> None:
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_first(neighbor)
        order.append(node)

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

    for node in reversed(order):
        if node not in visited:
            component: list[str] = []
            dfs_second(node, component)
            components.append(component)

    return components



def solve_two_sat(variables: list[str], clauses: list[tuple[str, str]]) -> dict[str, bool] | None:
    """Return a satisfying assignment, or None if the formula is unsatisfiable."""
    graph: dict[str, list[str]] = {}

    for variable in variables:
        graph.setdefault(variable, [])
        graph.setdefault(negate(variable), [])

    for left, right in clauses:
        graph.setdefault(left, [])
        graph.setdefault(right, [])
        graph.setdefault(negate(left), []).append(right)
        graph.setdefault(negate(right), []).append(left)

    components = kosaraju_components(graph)
    component_index: dict[str, int] = {}
    for index, component in enumerate(components):
        for literal in component:
            component_index[literal] = index

    for variable in variables:
        if component_index[variable] == component_index[negate(variable)]:
            return None

    assignment: dict[str, bool] = {}
    for variable in variables:
        assignment[variable] = component_index[variable] > component_index[negate(variable)]

    return assignment


if __name__ == "__main__":
    variables = ["x1", "x2", "x3"]
    clauses = [
        ("x1", "x2"),
        ("!x1", "x3"),
        ("!x2", "!x3"),
    ]

    solution = solve_two_sat(variables, clauses)
    print(f"Variables: {variables}")
    print(f"Clauses: {clauses}")
    print(f"Satisfying assignment: {solution}")
