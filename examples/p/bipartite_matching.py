"""
Maximum Bipartite Matching - Class P
====================================
In a bipartite graph, the maximum matching problem asks for the largest set of
pairwise disjoint edges. The augmenting-path method used below repeatedly
improves the current matching.

This implementation runs in O(VE) time, which is polynomial in the size of the
graph, so the problem lies in P.
"""


def maximum_bipartite_matching(
    graph: dict[str, list[str]], left_vertices: list[str]
) -> tuple[int, dict[str, str]]:
    """Return the matching size and a map from right vertices to left vertices."""
    match_right: dict[str, str] = {}

    def try_augment(left: str, seen: set[str]) -> bool:
        for right in graph.get(left, []):
            if right in seen:
                continue
            seen.add(right)

            if right not in match_right or try_augment(match_right[right], seen):
                match_right[right] = left
                return True

        return False

    match_count = 0
    for left in left_vertices:
        if try_augment(left, set()):
            match_count += 1

    return match_count, match_right


if __name__ == "__main__":
    graph = {
        "applicant_1": ["job_a", "job_b"],
        "applicant_2": ["job_a"],
        "applicant_3": ["job_b", "job_c"],
        "applicant_4": ["job_c"],
    }
    left = ["applicant_1", "applicant_2", "applicant_3", "applicant_4"]

    size, matching = maximum_bipartite_matching(graph, left)
    assignment = {worker: job for job, worker in matching.items()}

    print(f"Maximum matching size: {size}")
    print(f"Assignments: {assignment}")
