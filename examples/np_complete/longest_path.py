"""
Longest Path -- NP-Complete
=============================
Given a graph G, two vertices s and t, and integer k, does there exist a
simple path (no repeated vertices) from s to t of length >= k?

NB: Shortest Path is in P (Dijkstra), but Longest Simple Path is NP-Complete.
(Longest path in a DAG is in P via dynamic programming.)

Verifier:  Check the path is simple, connects s to t, and length >= k -- O(k).
Solver:    Backtracking DFS -- O(V!) worst case.
"""


def verify(graph: dict, path: list, s, t, k: int) -> bool:
    if path[0] != s or path[-1] != t:
        return False
    if len(set(path)) != len(path):  # Not simple
        return False
    for i in range(len(path) - 1):
        if path[i + 1] not in graph.get(path[i], []):
            return False
    return len(path) - 1 >= k


def solve(graph: dict, s, t, k: int) -> list | None:
    best = [None]

    def dfs(node, path, visited):
        if node == t:
            if len(path) - 1 >= k:
                best[0] = list(path)
            return
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                if best[0]:
                    return  # Found a valid path
                path.pop()
                visited.remove(neighbor)

    dfs(s, [s], {s})
    return best[0]


def find_longest_path(graph: dict, s, t) -> list:
    """Find the actual longest simple path from s to t."""
    best = {"path": [], "length": -1}

    def dfs(node, path, visited):
        if node == t:
            if len(path) - 1 > best["length"]:
                best["path"] = list(path)
                best["length"] = len(path) - 1
            return
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

    dfs(s, [s], {s})
    return best["path"]


if __name__ == "__main__":
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D", "E", "F"],
        "D": ["A", "C", "F"],
        "E": ["B", "C", "F"],
        "F": ["C", "D", "E"],
    }

    s, t = "A", "F"
    longest = find_longest_path(graph, s, t)
    print(f"Longest simple path from {s} to {t}:")
    print(f"  Path: {' -> '.join(longest)}")
    print(f"  Length: {len(longest) - 1} edges")

    for k in [3, 4, 5]:
        result = solve(graph, s, t, k)
        found = f"{' -> '.join(result)}" if result else "None"
        print(f"\nPath of length >= {k}: {found}")
        if result:
            print(f"  Verification: {verify(graph, result, s, t, k)}")
