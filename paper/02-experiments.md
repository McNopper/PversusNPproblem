## 2  Experiments

### 2.1  Setup

All experiments use the Euclidean distance metric. Optimal tours are
computed by the exact Held–Karp DP [6] (feasible up to $n \approx 20$).
We compare SiftTSP (`SiftTSP.py`, entry point `sift_tsp`) against:

- **Held–Karp**: exact $O(n^2 \cdot 2^n)$ DP — ground-truth optimum.
- **Nearest-Neighbor (NN)**: classic $O(n^2)$ greedy construction.
- **2-opt**: 2-opt local search starting from the NN tour.

SiftTSP is run with $\tau = 6$ and $d_{\max} \in \lbrace 1, 2, 3 \rbrace$.
The optimality gap is $(L / L^{\star} - 1) \times 100\%$ where $L^{\star}$ is the
Held–Karp optimum.

Reproduce with:
```powershell
$env:PYTHONIOENCODING="utf-8"; python -m tests.adversarial   # full battery
$env:PYTHONIOENCODING="utf-8"; python counterexample.py      # canonical counterexample
```

### 2.2  Adversarial Battery

Instance families designed to probe geometric-bisection weaknesses:

- **zigzag**-*n*: $n$ points alternating across a vertical axis.
- **interleaved**-*n*: two clusters with interleaved indices.
- **comb**-*n*: a spine with vertical teeth.
- **rings**-*n*: two concentric rings — no axis is preferred.
- **uniform**-*n*: uniform random control.

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
| **rings-12**     | 12 | 17.63    | 17.63    | *6.61*   | *6.61*   | *3.24*   |
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
$L^{\star} = 29.7823$.

| Algorithm | Length $L$ | Gap |
|:---|:---:|:---:|
| Held–Karp (exact)            | 29.7823 | — |
| SiftTSP, $d=1$, $\tau=6$ | 31.7503 | $+6.61\%$ |
| SiftTSP, $d=2$, $\tau=6$ | 31.7503 | $+6.61\%$ |
| SiftTSP, $d=3$, $\tau=6$ | 30.7478 | $+3.24\%$ |

**Proposition 1 (Non-exactness).** *SiftTSP with $\tau = 6$ and any
$d \in \lbrace 1, 2, 3 \rbrace$ is not exact on the Euclidean TSP.*
*Proof.* The 12-point instance `RINGS_12` in `counterexample.py` is a
witness: Held–Karp's optimum has length $29.7823$, while SiftTSP at
$d=1,2$ returns $31.7503$ and at $d=3$ returns $30.7478$, all strictly
greater. Values are reproducible by `python counterexample.py`. $\square$

The following is the structural intuition for *why* rings-12 defeats
the algorithm; it is an argument, not a formal proof of non-exactness
(Proposition 1 above does that).

**Argument (Decomposition irrecoverability).**
*Fix a finite family $\mathcal{D}$ of geometric decompositions of a
point set $C$, each partitioning $C$ into components, and consider any
algorithm that, for each $D \in \mathcal{D}$, solves every component
optimally as an open path and then optimally chains those paths into a
closed tour, finally returning the shortest tour across all
$D \in \mathcal{D}$. If the global optimum $\pi^{\star}$ is not
"component-contiguous" for any $D \in \mathcal{D}$ — that is, for every
$D$, some component of $D$ is entered and left more than once by
$\pi^{\star}$ — then no chaining can recover $\pi^{\star}$, and the algorithm's
output is strictly longer than $L(\pi^{\star})$.*

This applies to SiftTSP because the family $\mathcal{D}$ it explores
(median bisections at depths $1, \dots, d_{\max}$ along finitely many
rotated axes and four axis-pairs) is *fixed* and does not depend on
$\pi^{\star}$. The `rings-12` Held–Karp optimum is empirically
non-contiguous with respect to every $D$ tried at $d \leq 3$ (any
straight-line bisection separates the two rings or cuts them in two
diametrically opposed half-rings, while the optimum alternates between
inner and outer rings). Finer angular search adds resolution but does
not change the decomposition primitive, so it cannot defeat the
obstruction.

### 2.4  Observations

The following are observations from the 14-instance battery (Table 1).
Each instance is run on a single fixed seed; we report descriptive
findings, not statistical claims.

1. **Structured inputs are matched.** On zigzag, comb, and interleaved
   instances ($n \in \lbrace 12, 14, 16 \rbrace$), SiftTSP at $d \geq 2$ matches
   Held–Karp in every tested case, including instances where NN has
   gaps up to $+38\%$.
2. **Two rotationally symmetric inputs are not matched, but 2-opt is
   beaten on both.** On `rings-12` and `rings-14`, NN and 2-opt are
   stuck at $+17.63\%$ and $+8.58\%$; SiftTSP at $d=3$ achieves
   $+3.24\%$ and $+1.52\%$. Sample size is two; we do not claim this
   pattern holds on a wider population of rotationally symmetric
   instances.
3. **Increasing depth is not monotone.** On `uniform-12`, $d{=}2$ gives
   $+5.46\%$ while $d \in \lbrace 1, 3 \rbrace$ are exact. Finer subdivision can
   split clusters that the optimum traverses contiguously.

### 2.5  Discussion

**Where SiftTSP appears useful (on this battery).** Determinism
(reproducible given $(C, d, \tau, m, s)$); strong performance on inputs
with a clear geometric scan order (zigzag/comb/interleaved); and a
suggestive regime on the two rotationally symmetric instances tested,
where 2-opt is trapped. A larger study would be needed to claim this
generalises.

**Limits.** Decomposition irrecoverability (§2.3) is the structural
ceiling of *any* algorithm that explores only a fixed-in-advance
family of geometric decompositions and then optimally chains the
resulting component paths. The `rings-12` $+3.24\%$ wall is unmoved by
the mill+sieve refinement, consistent with the
obstruction being structural rather than angular-resolution-limited.
The connection step's $(2^d - 1)! \cdot 2^{2^d - 1}$ growth blocks
$d \geq 4$ unless replaced by a smarter chaining primitive.

**Open directions.**
- *Adaptive decomposition* (axes that depend on local geometry).
- *Recursive connection* (replace the brute-force chain by a
  recursive SiftTSP application on the path endpoints).
- *Hybridisation* with 2-opt or Lin–Kernighan [9] (LKH [10])
  using SiftTSP as an initial-tour generator.
- *Characterisation of exactness regimes* — a sufficient geometric
  condition on $C$ guaranteeing exactness would clarify the value of
  the algorithm as a conditional exact solver.

None of these are claimed to defeat the decomposition-irrecoverability
obstruction. SiftTSP is and will remain a heuristic; this work makes
**no claim** of resolving $\mathcal{P}$ versus $\mathcal{NP}$.
