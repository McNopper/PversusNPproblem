## SiftTSP: A Geometric Sandclock-Sift Heuristic for Euclidean TSP

---

## Abstract

We present **SiftTSP**, a deterministic polynomial-time heuristic for the
Euclidean Travelling Salesman Problem. The algorithm partitions the city
set by recursive geometric bisection into $2^d$ sections, solves small
sections by brute force and larger ones by a complementary pair of greedy
rules (min-max / max-min), and reconnects the section paths by exhaustive
search over orderings and orientations. The angular dimension of the
search is covered by two complementary sweeps — a uniform *mill*
(breadth) and a damped fan-shaped *sieve* (depth) — coordinated by a
*sandclock* depth schedule $1\to d_{\max}\to 1$ and an 8-state Phase 4
loop over (section-mode, mill-direction, ordering).

For any fixed parameters the algorithm runs in $O(n^2)$ time
(Theorem 1). SiftTSP is **not exact**: we exhibit an explicit 12-point
Euclidean instance (`counterexample.py`, `rings-12`) on which the
algorithm misses the Held–Karp optimum at every tested depth, with gap
$+3.24\%$ at $d=3$. The structural reason is identified as
*decomposition irrecoverability* (§2.3): no fixed family of geometric
decompositions can recover an optimal tour that interleaves cities
across components of every decomposition in the family.Consequently this work makes **no claim**
of resolving $\mathcal{P}$ versus $\mathcal{NP}$.

On a battery of 14 instances ($n \in \{12, 14, 16\}$) including zigzag,
comb, interleaved, concentric-ring, and uniform configurations, SiftTSP
matches Held–Karp on most structured inputs and beats 2-opt on the
rotationally symmetric `rings-12` and `rings-14` instances despite not
being exact.

**Keywords:** Travelling Salesman Problem, Polynomial-Time Heuristic,
Euclidean TSP, Geometric Subdivision, Mill-Sieve Search.
