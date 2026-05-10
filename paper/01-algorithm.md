## 1  Algorithm

### 1.1  Setting

Given $n$ cities $C = \{c_1, \dots, c_n\} \subset \mathbb{R}^2$, a *tour*
is a cyclic permutation $\pi$ of $C$, and its length is
$L(\pi) = \sum_i \|c_{\pi(i)} - c_{\pi(i+1)}\|_2$ (indices mod $n$).
Euclidean TSP asks for an $L$-minimum tour. The decision form is
NP-Complete [5]; the optimization form is NP-Hard. The exact Held–Karp
DP [6] runs in $O(n^2 \cdot 2^n)$ timeand is feasible only for small
$n$. SiftTSP is a polynomial-time *heuristic* — it is not exact, see
§2.3.

### 1.2  Parameters and Phases

SiftTSP is controlled by four constants treated as fixed:

| Symbol | Meaning |
|---|---|
| $d_{\text{ceiling}}$ | Maximum recursive subdivision depth |
| $m_{\text{ceiling}}$ | Mill (breadth) cap: third-steps per direction |
| $s_{\text{ceiling}}$ | Sieve (depth) cap: damped halvings around mill best |
| $\tau$ | Brute-force threshold: sections with $\leq \tau$ cities are solved exactly |

The algorithm is structured in four phases:

- **Phase 1 (max).** A worst-case greedy-longest tour, computed once,
  fixes a length floor $B_0$ that the rest only lowers.
- **Phase 2 (sift).** At each depth $d$ on the sandclock schedule
  $1, 2, \dots, d_{\max}, \dots, 2, 1$ and at each angle $\theta$ in the
  current mill+sieve schedule, the city set is partitioned by recursive
  bisection along four rotated axes (vertical, $/$, horizontal,
  $\backslash$) into $2^d$ sections. Sections of size $> \tau$ are
  solved by a greedy section solver in one of two complementary modes
  (selected per sweep by Phase 4):
  - **min-max**: at each step, append the city minimising the running
    *maximum* edge (favouring smooth paths);
  - **max-min**: at each step, append the city maximising the running
    *minimum* edge (a complementary ordering).
- **Phase 3 (min).** Sections of size $\leq \tau$ are solved exactly by
  brute force. The $2^d$ section paths are reconnected by exhaustive
  search over $(2^d - 1)! \cdot 2^{2^d - 1}$ orderings and
  orientations.
- **Phase 4 (loop).** An 8-state super-cycle drives the angular search.

The angular dimension uses two complementary sweeps. The **mill** is a
uniform third-step rotation across $[0, \pi/2)$ in both directions
(breadth). The **sieve** is a damped forth-and-back oscillation around
the best $(\theta^*, d^*)$ found by the mill, with amplitudes
$\tfrac{s_0}{2}, \tfrac{s_0}{4}, \dots, \tfrac{s_0}{2^{s}}$ where
$s_0 = (\pi / 2^{d^*}) / 3$ (depth). Mill and sieve refine the
*same* angular axis at different scales; together they sift the search
through both wide and narrow neighbourhoods of every depth.

### 1.3  The Phase 4 Super-Cycle

Each sandclock sweep is parameterised by a quadruple
$(d_{\max}, m, s, \mu, \delta)$, where $\mu$ is the section-solver mode
(min-max / max-min) and $\delta$ is the angular-sweep direction
(CW / CCW). The four configurations $(\mu, \delta)$ may be visited in
two orderings — *mode-first* (MD) or *direction-first* (DM) — giving an
8-state super-cycle:

| $k$ | $\mu$ | $\delta$ | ordering |
|:---:|:---:|:---:|:---:|
| 0 | max-min | CW  | MD |
| 1 | min-max | CW  | MD |
| 2 | max-min | CCW | MD |
| 3 | min-max | CCW | MD |
| 4 | max-min | CW  | DM |
| 5 | max-min | CCW | DM |
| 6 | min-max | CW  | DM |
| 7 | min-max | CCW | DM |

The order of visitation matters because the mill cap $m$ and sieve cap
$s$ double *only on improvement*; the sequence of $(config, m, s)$
triples ever evaluated depends on the order.

**Transition rule.** After a sweep at position $k$:
1. If the *mill* improved the running best, $m \leftarrow 2m$.
2. If the *sieve* improved the running best, $s \leftarrow 2s$.
3. Advance $k \leftarrow (k+1) \bmod 8$.
4. If 8 consecutive sweeps at the same $(d_{\max}, m, s)$ all fail,
   bump $d_{\max} \leftarrow d_{\max} + 1$, reset $m, s, k$ to $1, 1, 0$,
   and restart Phase 2.

The loop terminates when $d_{\max}$ reaches $d_{\text{ceiling}}$ and the
super-cycle converges. Tour length is bounded below by OPT and is
monotone non-increasing across the loop, so termination is guaranteed.

### 1.4  Pseudocode

```
SUPERCYCLE := concat(
    [(MaxMin,CW), (MinMax,CW), (MaxMin,CCW), (MinMax,CCW)],   # ordering MD
    [(MaxMin,CW), (MaxMin,CCW), (MinMax,CW), (MinMax,CCW)]    # ordering DM
)                                                              # length 8

procedure SiftTSP(C, d_ceiling, m_ceiling, s_ceiling, tau):
    best <- WorstCaseTour(C); best_len <- Length(best)         # PHASE 1
    for d_max = 1 .. d_ceiling do                              # PHASE 4
        m, s, k, no_improve <- 1, 1, 0, 0
        while m <= m_ceiling or s <= s_ceiling do
            (mode, dir) <- SUPERCYCLE[k]
            (best, best_len, mill_imp, sieve_imp)
              <- SandclockSweep(C, d_max, min(m,m_ceiling),
                                min(s,s_ceiling), tau, mode, dir,
                                best, best_len)
            k <- (k+1) mod 8
            if mill_imp or sieve_imp then
                no_improve <- 0
                if mill_imp  and m <= m_ceiling then m <- 2*m
                if sieve_imp and s <= s_ceiling then s <- 2*s
            else
                no_improve <- no_improve + 1
                if no_improve >= 8 then break
    return best

procedure SandclockSweep(C, d_max, m, s, tau, mode, dir, best, best_len):
    mill_imp, sieve_imp, theta*, d* <- false, false, 0, d_max
    for d in [1,2,..,d_max,..,2,1] do                          # PHASE 2 mill
        for theta in MillAngles(d, m, dir) do
            (best, best_len, hit) <- EvalAt(C, d, theta, tau, mode, ...)
            if hit then mill_imp, theta*, d* <- true, theta, d
    s0 <- (pi / 2^d*) / 3                                      # PHASE 2 sieve
    for j = 0 .. s-1 do
        delta <- s0 / 2^(j+1)
        for sigma in (+1, -1) do
            (best, best_len, hit) <- EvalAt(C, d*, theta* + sigma*delta, ...)
            if hit then sieve_imp, theta* <- true, theta* + sigma*delta
    return (best, best_len, mill_imp, sieve_imp)

procedure EvalAt(C, d, theta, tau, mode, best, best_len):
    hit <- false
    for (axis_p, axis_s) in AxisPairs(theta) do                # 4 pairs
        sections <- Subdivide(C, [axis_p, axis_s], d)
        paths <- []
        for S in sections do
            if |S| <= tau then paths <- paths + [BruteForce(S)]      # PHASE 3
            elif mode = MinMax then paths <- paths + [MinMax(S)]     # PHASE 2
            else                    paths <- paths + [MaxMin(S)]
        T <- BruteForceConnect(paths)
        if Length(T) < best_len then
            best_len, best, hit <- Length(T), T, true
    return (best, best_len, hit)
```

The reference implementation is `SiftTSP.py`; entry point `sift_tsp`.

### 1.5  Complexity

Treat $d_{\text{ceiling}}, m_{\text{ceiling}}, s_{\text{ceiling}}, \tau$
as fixed.

**Lemma 1 (Subdivide).** Algorithm `Subdivide` runs in $O(n \log n)$
time and produces at most $2^d$ sections.
*Proof.* The recursion has depth $d$; at each level the cities are
sorted once along the current axis at cost $O(n \log n)$. With $d$
fixed, total work is $O(n \log n)$. $\square$

**Lemma 2 (Section solving).** With $k = 2^d$, processing all sections
takes $O(1)$ in the all-brute-force regime ($\lceil n/k \rceil \leq
\tau$) and $O(n^2 / k)$ in the all-greedy regime; the mixed regime is
bounded by the larger.
*Proof.* Brute force on a section of $\leq \tau$ cities is $O(\tau!) =
O(1)$, and there are at most $k = O(1)$ such sections. For the greedy
branch, each section costs $O(s_i^2)$ with $\sum_i s_i = n$ and at most
$k$ non-empty sections, so $\sum_i s_i^2 \leq k \cdot (n/k)^2 = n^2/k$
by Cauchy–Schwarz. $\square$

**Lemma 3 (Connection).** `BruteForceConnect` runs in
$O(n \cdot (k-1)! \cdot 2^{k-1}) = O(n)$ for fixed $d$, since there are
$(k-1)!$ orderings and $2^{k-1}$ flip vectors and each tour is scored
in $O(n)$ time. $\square$

**Theorem 2 (Time complexity of SiftTSP).** *For fixed parameters,
SiftTSP runs in $O(n \log n)$ time when $n \leq \tau \cdot
2^{d_{\text{ceiling}}}$ (all-exact regime) and in $O(n^2)$ time
otherwise.*

*Proof.* Phase 1 costs $O(n^2)$. Each `EvalAt` invocation costs
$O(n \log n)$ for `Subdivide` (Lemma 1), $O(1)$ or $O(n^2/2^d)$ for
section solving (Lemma 2), and $O(n)$ for `BruteForceConnect`
(Lemma 3). The number of `EvalAt` invocations per `SandclockSweep` is
$O(d_{\max} \cdot m_{\text{ceiling}} + s_{\text{ceiling}}) \cdot 4 =
O(1)$. The total number of sweeps in Phase 4 is bounded by
$d_{\text{ceiling}} \cdot 8 \cdot
(\log m_{\text{ceiling}} + \log s_{\text{ceiling}} + 1) = O(1)$
because both ceilings double on improvement and at most 8 consecutive
non-improving sweeps occur. Multiplying gives the stated bounds.
$\square$

**Corollary 1.** *SiftTSP is a polynomial-time algorithm for all fixed
parameters.* The polynomiality is a property of a *heuristic*: §2.3
shows it is not exact in general.
