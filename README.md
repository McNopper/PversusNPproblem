# SiftTSP — A Geometric Sandclock-Sift Heuristic for Euclidean TSP

A deterministic, polynomial-time **heuristic** for the Euclidean Travelling
Salesman Problem (TSP), built around recursive geometric bisection with a
*sandclock* depth schedule and a *mill + sieve* angular search.

> **Status.** SiftTSP runs in $O(n^2)$ time for fixed parameters
> (proven, paper §1.5). It is **not exact**: an explicit 12-point
> Euclidean counterexample is shipped in
> [`counterexample.py`](counterexample.py). This work makes **no claim**
> of resolving $\mathcal{P}$ versus $\mathcal{NP}$ in either direction.

## What is in this repository

- **[`SiftTSP.py`](SiftTSP.py)** — the algorithm (entry point: `sift_tsp`).
- **[`paper/`](paper)** — the full scientific write-up (definitions,
  pseudocode, complexity proof, experimental battery, discussion).
- **[`counterexample.py`](counterexample.py)** — the canonical 12-point
  instance on which the algorithm misses the optimum, with literal
  coordinates and a self-contained verification harness.
- **[`tests/`](tests)** — Held–Karp / nearest-neighbor / 2-opt baselines and
  the adversarial test battery used in paper §2.

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

## Algorithm

Entry point: `sift_tsp(cities, d_ceiling, n_rot_ceiling, n_sift_ceiling, bf_threshold)`.

### Inputs

| Input | Paper symbol | Meaning |
|---|---|---|
| `cities` | $C$ | List of $n$ points $(x, y) \in \mathbb{R}^2$ |
| `d_ceiling` | $d_{\text{ceiling}}$ | Maximum recursive subdivision depth (sections at depth $d$: $2^d$) |
| `n_rot_ceiling` | $m_{\text{ceiling}}$ | Mill (breadth) cap: third-steps per direction in the uniform sweep |
| `n_sift_ceiling` | $s_{\text{ceiling}}$ | Sieve (depth) cap: halvings of the damped fan around the mill's best angle |
| `bf_threshold` | $\tau$ | Section size at or below which we solve exactly by brute force |

### Four phases

The criterion used to pick the next city tightens monotonically across the
phases:

$$
\text{max} \;\longrightarrow\; \{\text{min-max} \mid \text{max-min}\}
\;\longrightarrow\; \text{min} \;\longrightarrow\; \text{loop}
$$

**Phase 1 — Max (worst-case start, once).**
Construct a deliberately bad initial tour by greedy *farthest*-next
insertion. The resulting length is a guaranteed upper-bound floor that the
rest of the algorithm only ever lowers.

**Phase 2 — Sift (one sandclock sweep, mill + sieve).**
At depths $d = 1, 2, \ldots, d_{\max}, \ldots, 2, 1$ (the *sandclock*
schedule) the angular axis is searched with two complementary sweeps:

- **Mill (breadth).** Uniform third-segment sweep at angles
  $0, \pm\alpha_d/3, \pm 2\alpha_d/3, \ldots$ where
  $\alpha_d = \pi / 2^d$, capped at $m$ third-steps per direction.
- **Sieve (depth).** Damped forth-and-back oscillation around the best
  angle $\theta^*$ found by the mill, with amplitudes
  $\alpha_{d^*}/6, \alpha_{d^*}/12, \alpha_{d^*}/24, \ldots$ — a
  hand-fan rather than a full revolution — capped at $s$ halvings.

For each evaluated $(d, \theta)$ and for each of the four axis pairs
(vertical, $/$, horizontal, $\backslash$):

1. **Subdivide** the city set into $2^d$ sections by recursive bisection.
2. **Solve each section** by an open Hamiltonian path:
   - if $|S| \leq \tau$: exact brute-force enumeration (Phase 3);
   - else: a greedy rule (`min-max` *or* `max-min`, chosen by Phase 4):
     - `min-max` picks at each step the city that minimises the largest
       edge so far on the path;
     - `max-min` picks at each step the city that maximises the smallest
       edge so far.
3. **Reconnect** the $2^d$ section paths into a closed tour by exhaustive
   $(k{-}1)! \cdot 2^{k-1}$ search over orderings and orientations.

The shortest tour seen across the sweep is kept.

**Phase 3 — Min (exact local solve).**
As $d$ grows, sections shrink. Once a section has at most $\tau$ cities it
is solved *exactly* by brute force — the true minimum on that section.

**Phase 4 — Loop (convergence-driven outer schedule).**
Phase 2 sweeps are repeated at increasing parameters. Each sweep is
configured by a triple $(\text{mode}, \text{direction}, \text{ordering})$
giving an 8-state super-cycle:

| $k$ | mode | direction-first | cycle ordering |
|---|---|---|---|
| 0 | max-min | CW | MD |
| 1 | min-max | CW | MD |
| 2 | max-min | CCW | MD |
| 3 | min-max | CCW | MD |
| 4 | max-min | CW | DM |
| 5 | max-min | CCW | DM |
| 6 | min-max | CW | DM |
| 7 | min-max | CCW | DM |

Transition rule between sweeps:

- *Mill improvement:* double the mill cap, $m \leftarrow 2m$.
- *Sieve improvement:* double the sieve cap, $s \leftarrow 2s$.
- After each sweep, advance $k$ to the next super-cycle position.
- *No improvement:* advance $k$ and retry.
- *Eight consecutive non-improving sweeps:* bump $d_{\max} \leftarrow d_{\max} + 1$,
  reset $m \leftarrow 1$, $s \leftarrow 1$, $k \leftarrow 0$, return to Phase 2.

Termination: when $d_{\max}$ reaches `d_ceiling` and the super-cycle
converges again. Tour length is monotone non-increasing, so termination is
guaranteed.

### Complexity

For fixed `d_ceiling`, `n_rot_ceiling`, `n_sift_ceiling`, `bf_threshold`:

| Component | Worst-case cost |
|---|---|
| Phase 1 (worst-case greedy-longest start) | $O(n^2)$ |
| Per `EvalAt` (subdivide + section solve + connect) | $O(n^2)$ |
| Number of `EvalAt` calls | $O(1)$ |
| **Total** | **$O(n^2)$** |

Polynomial in all regimes. The dominant cost is Phase 1's pairwise
farthest-point scans; a $k$-d-tree implementation would reduce this to
$O(n \log n)$. See [`paper/01-algorithm.md`](paper/01-algorithm.md) §1.5
for the proof (Theorem 1).

### Limitation

The algorithm is not exact. The 12-point instance in
[`counterexample.py`](counterexample.py) is the canonical witness. See
[`paper/02-experiments.md`](paper/02-experiments.md) §2.3 for the
structural reason (decomposition irrecoverability: a fixed family of
geometric bisections cannot recover an optimum that interleaves cities
across components of every member of the family).

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
