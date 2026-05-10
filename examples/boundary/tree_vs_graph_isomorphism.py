"""
Tree Isomorphism (P) vs Graph Isomorphism (Unknown complexity)
===============================================================
Graph Isomorphism asks: are two graphs structurally identical (up to relabeling)?

Tree Isomorphism:   O(n) -- canonical form via AHU algorithm. Clearly in P.
General Graph ISO:  Status UNKNOWN -- believed not NP-Complete, not in P.
                    It is GI-complete (its own complexity class).
                    Best known algorithm: quasi-polynomial O(n^polylog(n)) -- Babai 2015.

Graph Isomorphism is one of the few natural problems in NP whose complexity
is unresolved -- a rare "island" between P and NP-Complete.
"""


# ── Tree Isomorphism -- AHU Canonical Form (Polynomial O(n)) ──────────────────

def tree_canonical(adj: dict, root, parent=None) -> str:
    """
    Compute a canonical string for a rooted tree (AHU algorithm).
    Two trees are isomorphic iff their canonical strings match.
    """
    children_codes = sorted(
        tree_canonical(adj, child, root)
        for child in adj.get(root, [])
        if child != parent
    )
    return "(" + "".join(children_codes) + ")"


def trees_isomorphic(adj1: dict, root1, adj2: dict, root2) -> bool:
    """O(n) tree isomorphism check via canonical form."""
    return tree_canonical(adj1, root1) == tree_canonical(adj2, root2)


def unrooted_tree_isomorphic(adj1: dict, adj2: dict) -> bool:
    """Find center(s) of each tree, compare canonical forms."""
    def find_centers(adj):
        leaves = [v for v in adj if len(adj[v]) == 1]
        remaining = set(adj.keys())
        while len(remaining) > 2:
            remaining -= set(leaves)
            leaves = [v for v in remaining if sum(1 for nb in adj[v] if nb in remaining) == 1]
        return list(remaining)

    centers1 = find_centers(adj1)
    centers2 = find_centers(adj2)
    for c1 in centers1:
        for c2 in centers2:
            if trees_isomorphic(adj1, c1, adj2, c2):
                return True
    return False


# ── General Graph Isomorphism (brute force -- O(n! * n^2)) ────────────────────

from itertools import permutations


def graph_isomorphic_brute(adj1: dict, adj2: dict) -> dict | None:
    """
    Brute-force graph isomorphism -- O(n! * n^2).
    Returns a mapping {v1: v2} or None.
    """
    nodes1 = sorted(adj1.keys())
    nodes2 = sorted(adj2.keys())
    if len(nodes1) != len(nodes2):
        return None

    for perm in permutations(nodes2):
        mapping = dict(zip(nodes1, perm))
        valid = True
        for u in nodes1:
            mapped_neighbors = {mapping[v] for v in adj1[u]}
            if mapped_neighbors != set(adj2[mapping[u]]):
                valid = False
                break
        if valid:
            return mapping
    return None


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Two isomorphic trees (same structure, different labels)
    tree1 = {1: [2, 3], 2: [1, 4, 5], 3: [1], 4: [2], 5: [2]}
    tree2 = {10: [20, 30], 20: [10], 30: [10, 40, 50], 40: [30], 50: [30]}

    print("Tree Isomorphism (AHU canonical form, O(n)):")
    iso = unrooted_tree_isomorphic(tree1, tree2)
    print(f"  Tree 1 edges: {[(u,v) for u in tree1 for v in tree1[u] if u<v]}")
    print(f"  Tree 2 edges: {[(u,v) for u in tree2 for v in tree2[u] if u<v]}")
    print(f"  Isomorphic: {iso}")

    # General graph isomorphism
    g1 = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    g2 = {"a": ["b", "c"], "b": ["a", "d"], "c": ["a", "b"], "d": ["b", "c"]}
    # Fix g2 to make it isomorphic to g1
    g2 = {"a": ["b","c"], "b": ["a","c","d"], "c": ["a","b"], "d": ["b"]}

    print("\nGeneral Graph Isomorphism (brute force, O(n!)):")
    mapping = graph_isomorphic_brute(g1, g2)
    print(f"  G1 adjacency: {g1}")
    print(f"  G2 adjacency: {g2}")
    print(f"  Isomorphic: {mapping is not None}")
    if mapping:
        print(f"  Mapping: {mapping}")

    print("\nKey insight:")
    print("  Tree isomorphism      -- O(n),         clearly in P")
    print("  Graph isomorphism     -- O(n^polylog n), complexity UNKNOWN (GI-complete)")
    print("  NOT known to be NP-Complete, NOT known to be in P")
    print("  Babai (2015): quasi-polynomial time -- the biggest complexity breakthrough in decades")
