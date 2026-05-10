"""
Post Correspondence Problem -- undecidable
==========================================
Input: a finite list of dominoes (top_i, bottom_i), each with two strings.
Question: is there a non-empty sequence of indices i1, i2, ..., ik such that

top_i1 + top_i2 + ... + top_ik == bottom_i1 + bottom_i2 + ... + bottom_ik ?

Why it is not merely NP-Hard:
- PCP is undecidable. There is no algorithm that always determines the answer
  for every instance.
- PCP is therefore outside NP and outside all decidable complexity classes.
- It is often used as a source problem in undecidability reductions.

Proof sketch idea:
- One can encode a Turing machine computation history as a sequence of tiles.
- Matching top and bottom strings forces a legal accepting computation.
- If PCP were decidable, we could decide whether a Turing machine accepts,
  contradicting standard undecidability results.

This module includes:
- A proof-sketch printer.
- A bounded search procedure. It can find short witnesses when they exist, but
  failure within the bound does not prove there is no solution.
"""


def proof_sketch():
    print("Post Correspondence Problem (undecidable)")
    print("Proof sketch:")
    print("1. Encode machine configurations as strings.")
    print("2. Build tiles so matching concatenations simulate legal steps.")
    print("3. A PCP match exists exactly when the encoded machine reaches acceptance.")
    print("4. Therefore a general PCP solver would decide an undecidable problem.")
    print()


def bounded_search(tiles, max_length):
    def compatible(a, b):
        return a.startswith(b) or b.startswith(a)

    frontier = [([], "", "")]
    for _ in range(max_length):
        new_frontier = []
        for sequence, top, bottom in frontier:
            for index, (top_piece, bottom_piece) in enumerate(tiles):
                next_top = top + top_piece
                next_bottom = bottom + bottom_piece
                if not compatible(next_top, next_bottom):
                    continue
                next_sequence = sequence + [index]
                if next_top == next_bottom and next_sequence:
                    return next_sequence, next_top
                new_frontier.append((next_sequence, next_top, next_bottom))
        frontier = new_frontier
    return None, None


if __name__ == "__main__":
    proof_sketch()
    print()

    solvable_tiles = [("ab", "a"), ("b", "bb")]
    solution, word = bounded_search(solvable_tiles, max_length=6)
    print(f"Bounded search on solvable tiles: {solvable_tiles}")
    if solution is not None:
        print(f"Found sequence: {solution}")
        print(f"Matching word:  {word}")
    else:
        print("No solution found within the bound.")

    second_tiles = [("a", "ab"), ("ba", "a")]
    solution, _ = bounded_search(second_tiles, max_length=1)
    print(f"Bounded search on second instance with a small bound: {second_tiles}")
    if solution is None:
        print("No solution found within the bound. This is not a proof of impossibility.")
    else:
        print(f"Found sequence within the bound: {solution}")
