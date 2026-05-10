"""
Protein Folding in the 2D HP model -- NP-Hard optimization
==========================================================
Given a string over {H, P}, embed it as a self-avoiding walk on the 2D grid.
The objective is to maximize the number of non-consecutive H-H contacts, where
hydrophobic residues prefer to sit next to each other.

Why NP-Hard:
- Even simplified lattice versions of protein folding capture hard combinatorial
  structure.
- The optimization problem of maximizing H-H contacts is NP-Hard.

Is it in NP?
- The optimization problem is not a decision language.
- Natural bounded decision versions are in NP because a proposed fold can be
  checked in polynomial time.

Key properties:
- A fold is a self-avoiding walk.
- Contacts count only for adjacent H residues that are not consecutive in the
  chain.
- Exact search explodes quickly, so exhaustive search is practical only for
  short sequences.

This module includes:
- An exhaustive exact solver for short sequences.
- A greedy heuristic.
"""

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def add_point(point, direction):
    return point[0] + direction[0], point[1] + direction[1]


def hh_contacts(sequence, positions):
    total = 0
    index_of = {pos: i for i, pos in enumerate(positions)}
    for i, amino in enumerate(sequence):
        if amino != "H":
            continue
        x, y = positions[i]
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)
            j = index_of.get(neighbor)
            if j is None:
                continue
            if sequence[j] == "H" and abs(i - j) > 1:
                total += 1
    return total // 2


def greedy_fold(sequence):
    positions = [(0, 0), (1, 0)]
    used = set(positions)
    for i in range(2, len(sequence)):
        best_pos = None
        best_score = None
        for direction in DIRECTIONS:
            candidate = add_point(positions[-1], direction)
            if candidate in used:
                continue
            trial = positions + [candidate]
            score = hh_contacts(sequence[: i + 1], trial)
            openness = sum(1 for d in DIRECTIONS if add_point(candidate, d) not in used)
            key = (score, openness)
            if best_score is None or key > best_score:
                best_score = key
                best_pos = candidate
        if best_pos is None:
            return positions, hh_contacts(sequence[: len(positions)], positions)
        positions.append(best_pos)
        used.add(best_pos)
    return positions, hh_contacts(sequence, positions)


def exhaustive_fold(sequence):
    if len(sequence) <= 1:
        return [(0, 0)], 0
    best = {"positions": [(0, 0), (1, 0)], "score": -1}
    used = {(0, 0), (1, 0)}
    positions = [(0, 0), (1, 0)]

    def search(index):
        if index == len(sequence):
            score = hh_contacts(sequence, positions)
            if score > best["score"]:
                best["score"] = score
                best["positions"] = list(positions)
            return
        for direction in DIRECTIONS:
            candidate = add_point(positions[-1], direction)
            if candidate in used:
                continue
            positions.append(candidate)
            used.add(candidate)
            search(index + 1)
            used.remove(candidate)
            positions.pop()

    search(2)
    return best["positions"], best["score"]


if __name__ == "__main__":
    sequence = "HHPHHHPH"

    exact_positions, exact_score = exhaustive_fold(sequence)
    greedy_positions, greedy_score = greedy_fold(sequence)

    print("Protein Folding in the 2D HP model (NP-Hard)")
    print(f"Sequence: {sequence}")
    print(f"Exact score:   {exact_score} with positions {exact_positions}")
    print(f"Greedy score:  {greedy_score} with positions {greedy_positions}")
