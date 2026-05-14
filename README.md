# SiftTSP — A Geometric Sandclock-Sift Heuristic for Euclidean TSP

A deterministic, polynomial-time **heuristic** for the Euclidean Travelling
Salesman Problem (TSP), built around recursive geometric bisection with a
*sandclock* depth schedule and a *mill + sieve* angular search.

## Overview

SiftTSP partitions the city set by recursive geometric bisection into $2^d$
sections, solves small sections by brute force and larger ones by a
complementary pair of greedy rules (min-max / max-min), and reconnects the
section paths by exhaustive search over orderings and orientations. The
angular dimension of the search is covered by two complementary sweeps — a
uniform *mill* (breadth) and a damped fan-shaped *sieve* (depth) —
coordinated by a *sandclock* depth schedule $1 \to d_{\max} \to 1$ and an
8-state super-cycle over (section-mode, mill-direction, ordering).

- **Runtime:** $O(n^2)$ for fixed parameters.
- **Not exact:** [`counterexample.py`](counterexample.py) is a canonical
  12-point witness (`rings-12`) on which the algorithm misses the
  Held–Karp optimum at every tested depth.
- **Empirically:** matches Held–Karp on most structured inputs in the
  adversarial battery (zigzag, comb, interleaved) and beats 2-opt on the
  rotationally symmetric `rings-12` / `rings-14` instances.

## Paper

The full scientific write-up — definitions, pseudocode, complexity proof
(Theorem 1), experimental battery, counterexample and discussion of
*decomposition irrecoverability* — is available as a single PDF:

**📄 [`SiftTSP.pdf`](SiftTSP.pdf)** — LaTeX source: [`SiftTSP.tex`](SiftTSP.tex).

## Repository layout

- **[`SiftTSP.py`](SiftTSP.py)** — the algorithm (entry point: `sift_tsp`).
- **[`SiftTSP.pdf`](SiftTSP.pdf)** / **[`SiftTSP.tex`](SiftTSP.tex)** —
  the scientific write-up and its LaTeX source.
- **[`counterexample.py`](counterexample.py)** — the canonical 12-point
  instance on which the algorithm misses the optimum, with literal
  coordinates and a self-contained verification harness.
- **[`tests/`](tests)** — Held–Karp / nearest-neighbor / 2-opt baselines
  and the adversarial test battery used in paper §2.

## How to run

```powershell
$env:PYTHONIOENCODING="utf-8"

# The algorithm itself
python SiftTSP.py

# The counterexample, with side-by-side Held-Karp comparison
python counterexample.py

# The full adversarial battery (Held-Karp / NN / 2-opt / ours)
python -m tests.adversarial
```

## Entry point

`sift_tsp(cities, d_ceiling, n_rot_ceiling, n_sift_ceiling, bf_threshold)`

| Input | Paper symbol | Meaning |
|---|---|---|
| `cities` | $C$ | List of $n$ points $(x, y) \in \mathbb{R}^2$ |
| `d_ceiling` | $d_{\text{ceiling}}$ | Maximum recursive subdivision depth (sections at depth $d$: $2^d$) |
| `n_rot_ceiling` | $m_{\text{ceiling}}$ | Mill (breadth) cap: third-steps per direction in the uniform sweep |
| `n_sift_ceiling` | $s_{\text{ceiling}}$ | Sieve (depth) cap: halvings of the damped fan around the mill's best angle |
| `bf_threshold` | $\tau$ | Section size at or below which we solve exactly by brute force |

For the algorithm's four phases, the 8-state super-cycle, the $O(n^2)$
complexity proof, and the structural counterexample, see
[`SiftTSP.pdf`](SiftTSP.pdf).

## License

See [LICENSE](LICENSE).
