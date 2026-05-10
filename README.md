# SiftTSP — A Geometric Sandclock-Sift Heuristic for Euclidean TSP

A deterministic, polynomial-time **heuristic** for the Euclidean Travelling
Salesman Problem (TSP), built around recursive geometric bisection with a
*sandclock* depth schedule and a *mill + sieve* angular search.

> **Status.** SiftTSP runs in $O(n \log n)$ time for fixed parameters (proven,
> paper §1.5). It is **not exact**: an explicit 12-point Euclidean
> counterexample is shipped in [`counterexample.py`](counterexample.py). This
> work makes **no claim** of resolving $\mathcal{P}$ versus $\mathcal{NP}$ in
> either direction.

## What is in this repository

- The TSP heuristic itself — current implementation:
  **[`tsp.py`](tsp.py)** (entry point: `sift_tsp`).
- **[`ALGORITHM.md`](ALGORITHM.md)** — the essence of the algorithm in one
  page (what it does, parameters, complexity).
- **[`paper/`](paper)** — the full scientific write-up (definitions,
  pseudocode, complexity proof, experimental battery, discussion).
- **[`counterexample.py`](counterexample.py)** — the canonical 12-point
  instance on which the algorithm misses the optimum, with literal
  coordinates and a self-contained verification harness.
- **[`tests/`](tests)** — Held–Karp / nearest-neighbor / 2-opt baselines and
  the adversarial test battery used in paper §5.
- **[`examples/`](examples)** — 110 reference Python implementations of
  problems across the complexity hierarchy ($\mathcal{P}$, $\mathcal{NP}$,
  NP-Complete, NP-Hard). These are **not** part of the TSP algorithm; they
  were collected as a contextual reference for the broader complexity
  landscape this work is embedded in. They can be read independently.

## How to run

```powershell
$env:PYTHONIOENCODING="utf-8"

# The algorithm itself, with verbose phase 4 trace
python tsp.py

# The counterexample, with side-by-side Held-Karp comparison
python counterexample.py

# The full adversarial battery (Held-Karp / NN / 2-opt / ours)
python -m tests.adversarial
```

## The paper

A compact write-up in Springer LNCS style lives in [`paper/`](paper):

| Section | Content |
|---|---|
| [Abstract](paper/00-abstract.md) | Title, abstract, keywords |
| [1 · Algorithm & Complexity](paper/01-algorithm.md) | Setting, parameters, four phases, pseudocode, $O(n \log n)$ / $O(n^2)$ proof |
| [2 · Experiments](paper/02-experiments.md) | Battery, counterexample, iteration history, discussion |
| [References](paper/03-references.md) | Bibliography |

## Design history

SiftTSP is the consolidation of 17 incremental design iterations. The
individual iteration files (`tsp_p.py`, `tsp_p2.py`, ..., `tsp_p17.py`)
are no longer carried in the repository; their full source is preserved
in the git history. A short narrative summary of the design milestones
is in paper §2.5.

## License

See [LICENSE](LICENSE).
