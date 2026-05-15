# SiftTSP

*by Norbert Nopper*

A geometric sandclock-sift heuristic for the Euclidean Travelling Salesman
Problem.

## Overview

**SiftTSP** is a deterministic polynomial-time heuristic for the Euclidean
TSP in the partitioning lineage of Karp (1977). The algorithm partitions the
city set by recursive geometric bisection into $2^d$ sections, solves small
sections by brute force and larger ones by a complementary pair of greedy
rules (min-max / max-min), and reconnects the section paths by exhaustive
search over orderings and orientations. The angular dimension of the search
is covered by two complementary sweeps — a uniform *mill* (breadth) and a
damped fan-shaped *sieve* (depth) — coordinated by a *sandclock* depth
schedule $1 \to d_{\max} \to 1$ and an 8-state Phase 4 loop over
(section-mode, mill-direction, ordering). The contribution is the specific
orchestration of these primitives, not a new theoretical guarantee.

- **Runtime:** $O(n^2)$ for fixed parameters.
- **Not exact.** [`counterexample.py`](counterexample.py) is a canonical
  12-point witness (`rings-12`) on which the algorithm misses the Held–Karp
  optimum at every tested depth, with gap $+3.24\%$ at $d=3$. The structural
  reason is identified in the paper as *decomposition irrecoverability*: no
  fixed family of geometric decompositions can recover an optimal tour that
  interleaves cities across components of every decomposition in the
  family. Consequently this work makes **no claim** of resolving $\mathcal{P}$
  versus $\mathcal{NP}$, and offers no approximation ratio (unlike
  Christofides 1976 for metric TSP or Arora 1998 for Euclidean TSP).
- **Empirically.** On a battery of 14 instances ($n \in \{12, 14, 16\}$)
  SiftTSP matches Held–Karp on most structured inputs and beats 2-opt on
  the rotationally symmetric `rings-12` / `rings-14` instances despite not
  being exact.

## The paper

- 📄 **[SiftTSP.pdf](SiftTSP.pdf)** — typeset PDF
- 📝 **[SiftTSP.tex](SiftTSP.tex)** — LaTeX source

Rebuild with any standard LaTeX engine:

```sh
latexmk -pdf SiftTSP.tex
```

## Repository layout

- **[`SiftTSP.py`](SiftTSP.py)** — the algorithm (entry point: `sift_tsp`).
- **[`SiftTSP.pdf`](SiftTSP.pdf) / [`SiftTSP.tex`](SiftTSP.tex)** — the
  scientific write-up and its LaTeX source.
- **[`counterexample.py`](counterexample.py)** — the canonical 12-point
  instance on which the algorithm misses the optimum, with literal
  coordinates and a self-contained verification harness.
- **[`tests/`](tests)** — Held–Karp / nearest-neighbour / 2-opt baselines
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

## License

Code: MIT. Paper text and figures: CC BY 4.0. See [LICENSE](LICENSE).
