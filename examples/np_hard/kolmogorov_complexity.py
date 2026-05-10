"""
Kolmogorov Complexity -- NP-Hard (uncomputable)
===============================================
The Kolmogorov complexity K(s) of a string s is the length of the shortest
program that outputs s. It measures the intrinsic information content of s.

Like the Halting Problem, Kolmogorov complexity is *uncomputable* -- no
algorithm can calculate K(s) for all strings. It is even harder than
NP-Hard in the computability hierarchy.

Key properties:
  - K(s) <= |s| + c  (trivial program: just print s)
  - Strings where K(s) ≈ |s| are called *incompressible* (random-looking)
  - Most strings are incompressible (there aren't enough short programs)

This file demonstrates the concept using compression as an approximation.
"""

import zlib
import sys


def compression_approximation(s: str) -> dict:
    """
    Use compression ratio as a practical approximation of Kolmogorov complexity.
    A highly compressible string has low K(s); incompressible strings have K(s) ≈ |s|.
    Note: This is only an upper bound -- true K(s) may be even smaller.
    """
    encoded = s.encode("utf-8")
    compressed = zlib.compress(encoded, level=9)
    return {
        "original_bytes": len(encoded),
        "compressed_bytes": len(compressed),
        "ratio": len(compressed) / len(encoded),
    }


def why_uncomputable():
    print("=" * 60)
    print("Why Kolmogorov Complexity is Uncomputable")
    print("=" * 60)
    print("""
Suppose a function K(s) existed that computed the shortest program length.

Define: find the first string s of length n such that K(s) >= n.
        (This string exists -- most strings are incompressible.)

The program to find and print that string has some fixed size c.
But for large enough n, the program is shorter than n -> K(s) < n.
CONTRADICTION.

This is a variant of Berry's paradox:
  "The smallest number not definable in fewer than twelve words"
  -- that definition itself uses eleven words!

Therefore, K(s) is uncomputable.
""")


EXAMPLES = [
    ("Repetitive",   "abababababababababababababababababababababababababababab"),
    ("Structured",   "".join(str(i % 10) for i in range(50))),
    ("Pi digits",    "31415926535897932384626433832795028841971693993751058"),
    ("Pseudo-random","a3f9bc12de78f1a0c5b4e72d9810fe36c7a2591b84d063e7f2c1"),
]


if __name__ == "__main__":
    why_uncomputable()

    print("Compression-based approximation of Kolmogorov Complexity:\n")
    print(f"  {'String type':<16} {'Original':>8} {'Compressed':>10} {'Ratio':>7}  {'Interpretation'}")
    print("  " + "-" * 65)

    for label, s in EXAMPLES:
        info = compression_approximation(s)
        interp = "Low K(s) -- highly regular" if info["ratio"] < 0.8 else "High K(s) -- complex/random"
        print(f"  {label:<16} {info['original_bytes']:>8} {info['compressed_bytes']:>10} "
              f"{info['ratio']:>7.2f}  {interp}")

    print("""
Note: compression gives an *upper bound* on K(s) -- the true minimum
program may be shorter than any compressor can find. The exact K(s)
is always unknowable in general.
""")
