## 2  Experiments

### 2.1  Setup

All experiments use the Euclidean distance metric. Optimal tours are
computed by the exact Held–Karp DP [7] (feasible up to $n \approx 20$).
We compare SiftTSP (`tsp.py`, entry point `sift_tsp`) against:

- **Held–Karp**: exact $O(n^2 \cdot 2^n)$ DP — ground-truth optimum.
- **Nearest-Neighbor (NN)**: classic $O(n^2)$ greedy construction.
- **2-opt**: 2-opt local search starting from the NN tour.

SiftTSP is run with $\tau = 6$ and $d_{\max} \in \{1, 2, 3\}$.
The optimality gap is $(L / L^* - 1) \times 100\%$ where $L^*$ is the
Held–Karp optimum.

Reproduce with:
```bash
$env:PYTHONIOENCODING="utf-8"; python -m tests.adversarial   # full battery
$env:PYTHONIOENCODING="utf-8"; python counterexample.py      # canonical counterexample
```

### 2.2  Adversarial Battery

Instance families designed to probe geometric-bisection weaknesses:

- **zigzag-$n$**: $n$ points alternating across a vertical axis.
- **interleaved-$n$**: two clusters with interleaved indices.
- **comb-$n$**: a spine with vertical teeth.
- **rings-$n$**: two concentric rings — no axis is preferred.
- **uniform-$n$**: uniform random control.

**Table 1.** Optimality gap (%) — **bold = exact**, *italic = sub-optimal*.

| Instance | $n$ | NN | NN+2-opt | $d{=}1$ | $d{=}2$ | $d{=}3$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| zigzag-12        | 12 | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| zigzag-14        | 14 | 28.84    | **0.00** | **0.00** | **0.00** | **0.00** |
| zigzag-16        | 16 | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| zigzag-tight-12  | 12 | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| zigzag-wide-14   | 14 | 19.52    | **0.00** | **0.00** | **0.00** | **0.00** |
| interleaved-12   | 12 | 38.09    | **0.00** | **0.00** | **0.00** | **0.00** |
| interleaved-14   | 14 | **0.00** | **0.00** | *31.41*  | **0.00** | **0.00** |
| comb-12          | 12 | **0.00** | **0.00** | **0.00** | **0.00** | **0.00** |
| comb-14          | 14 | **0.00** | **0.00** | *25.98*  | **0.00** | **0.00** |
| **rings-12**     | 12 | 17.63    | 17.63    | *6.82*   | *6.73*   | *3.24*   |
| **rings-14**     | 14 | 8.58     | 8.58     | *26.06*  | *3.82*   | *1.52*   |
| uniform-12       | 12 | 12.20    | **0.00** | **0.00** | *5.46*   | **0.00** |
| uniform-14       | 14 | 30.36    | **0.00** | *15.32*  | *1.47*   | *1.47*   |
| uniform-16       | 16 | 12.01    | 1.01     | *9.78*   | *7.60*   | *0.31*   |

### 2.3  Counterexample to Exactness — `rings-12`

We exhibit an explicit 12-point Euclidean instance on which SiftTSP
fails to recover the optimum at every tested depth. The instance, an
inner ring of 6 points of radius $\approx 2$ and an outer ring of 6
points of radius $\approx 4$ both centred at $(5,5)$, is materialised
verbatim in `counterexample.py`.

**Table 2.** Counterexample `rings-12` — Held–Karp optimum
$L^* = 29.7823$.

| Algorithm | Length $L$ | Gap |
|:---|:---:|:---:|
| Held–Karp (exact)            | 29.7823 | — |
| SiftTSP, $d=1$, $\tau=6$ | 31.7503 | $+6.61\%$ |
| SiftTSP, $d=2$, $\tau=6$ | 31.7503 | $+6.61\%$ |
| SiftTSP, $d=3$, $\tau=6$ | 30.7478 | $+3.24\%$ |

**Proposition 1.** *SiftTSP with $\tau = 6$ and any
$d \in \{1, 2, 3\}$ is not exact on the Euclidean TSP.*

The structural reason is captured by:

**Proposition 2 (Decomposition irrecoverability).**
*Any algorithm that (i) commits to a fixed geometric decomposition $D$
of the city set before seeing the optimal tour, (ii) solves each
component of $D$ optimally as an open path, and (iii) optimally chains
those paths into a closed tour, can return a tour strictly longer than
the global optimum.*

*Justification.* The closed tour returned by such an algorithm is the
shortest among those that visit each component contiguously. The global
optimum is not constrained to do so; if the optimum interleaves cities
across components, no chaining can recover it. The `rings-12`
Held–Karp optimum interleaves inner-ring and outer-ring vertices in a
way no bisection along any of the four axes respects. $\square$

The mill+sieve refinement of iteration 17 (§2.5) adds finer angular
resolution but does not change the decomposition primitive, so it
cannot break Proposition 2.

### 2.4  Observations

1. **Structured inputs are matched.** On zigzag, comb, and interleaved
   instances, SiftTSP at $d \geq 2$ matches Held–Karp in every case,
   including instances where NN has gaps up to $+38\%$.
2. **Rotationally symmetric inputs are not matched, but 2-opt is
   beaten.** On `rings-12` and `rings-14`, NN and 2-opt are stuck at
   $+17.63\%$ and $+8.58\%$; SiftTSP at $d=3$ achieves $+3.24\%$ and
   $+1.52\%$.
3. **Increasing depth is not monotone.** On `uniform-12`, $d{=}2$ gives
   $+5.46\%$ while $d \in \{1, 3\}$ are exact. Finer subdivision can
   split clusters that the optimum traverses contiguously.

### 2.5  Iteration History

The current `tsp.py` is the consolidation of 17 design iterations.
The intermediate files (`tsp_p.py`, `tsp_p2.py`, ..., `tsp_p17.py`) are
no longer carried in the repository; their full source is preserved in
the git history.

**Table 3.** Iteration milestones — gap on a fixed 10-city instance
$C_{10}$, $L^* = 32.9296$.

| Iteration | Key Design Change | Gap on $C_{10}$ |
|---|---|:---:|
| 1   | Global min-max heuristic only | ~23% |
| 2   | Divide & conquer + edge-swap merge | 5.4% |
| 3   | Iterative vertical/horizontal + min-max | ~19–25% |
| 4   | Four-direction axis rotation | 0% (n=8), variable |
| 5   | Four sections, 48-combination brute-force join | 0% (n ≤ 11) |
| 6   | Depth $d$ as parameter; greedy chain join | Degraded at $d \geq 3$ |
| 7   | $d=3$; brute-force join (645 K combinations) | 0% (limited tests) |
| 8   | Brute-force threshold $\tau$ as parameter | 0% on $C_{10}$ at $d{\geq}2$ |
| 9   | Worst-case greedy-longest start added | 0% on $C_{10}$ at $d{\geq}2$ |
| 10  | Progressive sift + bidirectional mill rotation | 0% on $C_{10}$ at $d{\geq}2$ |
| 11  | Sandclock depth schedule $1\to d_{\max}\to 1$ | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| 12  | Convergence-driven Phase 4 loop over $(d_{\max}, m)$ | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| 13  | Section solver evaluates min-max and max-min | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| 14  | Phase 4 alternates section mode (2-state cycle) | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| 15  | Phase 4 cycles mode × mill-direction (4-state) | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| 16  | Phase 4 8-state super-cycle (mode × dir × ordering) | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |
| **17 (`tsp.py`)** | **SiftTSP**: adds sieve (depth) sweep alongside mill (breadth) | 0% on $C_{10}$ at $d_{\max}{\geq}2$ |

**Caveat.** The 0%-gap entries on $C_{10}$ in earlier drafts were
treated as evidence of exactness; the broader battery in Table 1, and
the `rings-12` counterexample, show that this was an artefact of a
small unrepresentative test set.

### 2.6  Discussion

**Where SiftTSP is useful.** Determinism (reproducible given
$(C, d, \tau, m, s)$); strong performance on inputs with a clear
geometric scan order (zigzag/comb/interleaved); and a useful regime on
rotationally symmetric inputs where 2-opt is trapped.

**Limits.** Decomposition irrecoverability (Proposition 2) is the hard
structural ceiling of *any* algorithm of this shape. The
`rings-12` $+3.24\%$ wall is unmoved by the mill+sieve refinement of
iteration 17, confirming that the obstruction is structural, not
angular-resolution-limited. The connection step's
$(2^d - 1)! \cdot 2^{2^d - 1}$ growth blocks $d \geq 4$ unless replaced
by a smarter chaining primitive.

**Open directions.**
- *Adaptive decomposition* (axes that depend on local geometry).
- *Recursive connection* (replace the brute-force chain by a
  recursive SiftTSP application on the path endpoints).
- *Hybridisation* with 2-opt or Lin–Kernighan-Helsgaun [9] using
  SiftTSP as an initial-tour generator.
- *Characterisation of exactness regimes* — a sufficient geometric
  condition on $C$ guaranteeing exactness would clarify the value of
  the algorithm as a conditional exact solver.

None of these are claimed to break Proposition 2. SiftTSP is and will
remain a heuristic; this work makes **no claim** of resolving
$\mathcal{P}$ versus $\mathcal{NP}$.
