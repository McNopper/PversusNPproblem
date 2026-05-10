"""
Max Cut -- NP-Complete
=======================
Given a graph G and integer k, does there exist a partition of vertices into
two sets S and V-S such that the number of edges crossing the cut is >= k?

Applications: VLSI circuit design, statistical physics (Ising model),
              clustering, and network design.

Verifier:  Count crossing edges for a given partition -- O(E), polynomial.
Solver:    Brute-force over all 2^(V-1) partitions (fix one vertex to break symmetry).
Approx:    Randomized 1/2-approximation, Goemans-Williamson gives 0.878 approximation.
"""

from itertools import product


def cut_size(graph: dict, partition_s: set) -> int:
    """Count edges with one endpoint in S and one in V-S."""
    count = 0
    for u in partition_s:
        for v in graph.get(u, []):
            if v not in partition_s:
                count += 1
    return count


def verify(graph: dict, partition_s: set, k: int) -> bool:
    return cut_size(graph, partition_s) >= k


def solve_brute(graph: dict) -> tuple:
    """Find the maximum cut by trying all 2^(V-1) partitions."""
    nodes = list(graph.keys())
    n = len(nodes)
    best_cut = 0
    best_partition = set()

    # Fix nodes[0] in S to eliminate symmetric solutions
    for bits in product([0, 1], repeat=n - 1):
        s = {nodes[0]} | {nodes[i + 1] for i, b in enumerate(bits) if b}
        size = cut_size(graph, s)
        if size > best_cut:
            best_cut = size
            best_partition = s

    return best_partition, best_cut


def random_cut(graph: dict) -> tuple:
    """
    Randomized 1/2-approximation: assign each vertex to S or V-S uniformly at random.
    Expected cut >= |E| / 2.
    """
    import random
    nodes = list(graph.keys())
    s = {v for v in nodes if random.random() < 0.5}
    return s, cut_size(graph, s)


if __name__ == "__main__":
    graph = {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 3, 4],
        3: [0, 2, 4],
        4: [1, 2, 3],
    }

    total_edges = sum(len(v) for v in graph.values()) // 2
    print(f"Graph has {len(graph)} vertices and {total_edges} edges.")

    best_s, best_k = solve_brute(graph)
    complement = set(graph.keys()) - best_s
    print(f"\nMaximum cut: {best_k} edges")
    print(f"  S  = {sorted(best_s)}")
    print(f"  V-S = {sorted(complement)}")
    print(f"Verification: {verify(graph, best_s, best_k)}")

    # Randomized approximation (run 5 trials)
    print("\nRandomized 1/2-approximation (5 trials):")
    for trial in range(5):
        s, size = random_cut(graph)
        print(f"  Trial {trial+1}: cut = {size}  (S = {sorted(s)})")
