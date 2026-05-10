"""
Interval Scheduling (P) vs Weighted Interval Scheduling (P via DP) vs Job Shop (NP-Hard)
==========================================================================================
Interval Scheduling:          Select maximum non-overlapping intervals.
                              Greedy O(n log n) -- in P.

Weighted Interval Scheduling: Select non-overlapping intervals maximizing total weight.
                              DP O(n log n) -- still in P.

Job Shop Scheduling:          n jobs, m machines, each job has ordered operations.
                              Minimize makespan -- NP-Hard for m >= 3 machines.

A striking progression: adding weights keeps it in P, but adding machine ordering
constraints and minimizing makespan jumps to NP-Hard.
"""

import bisect


# ── Interval Scheduling (Polynomial -- Greedy) ────────────────────────────────

def interval_scheduling(intervals: list) -> list:
    """
    Greedy: sort by finish time, greedily pick compatible intervals.
    O(n log n). Returns list of selected interval indices.
    """
    sorted_idx = sorted(range(len(intervals)), key=lambda i: intervals[i][1])
    selected = []
    last_finish = float("-inf")
    for i in sorted_idx:
        start, finish = intervals[i]
        if start >= last_finish:
            selected.append(i)
            last_finish = finish
    return selected


# ── Weighted Interval Scheduling (Polynomial -- DP) ───────────────────────────

def weighted_interval_scheduling(intervals: list) -> tuple:
    """
    DP: O(n log n). intervals: list of (start, finish, weight).
    Returns (max_weight, selected_indices).
    """
    n = len(intervals)
    sorted_idx = sorted(range(n), key=lambda i: intervals[i][1])
    intervals_sorted = [intervals[i] for i in sorted_idx]

    finish_times = [iv[1] for iv in intervals_sorted]

    def latest_compatible(j):
        """Find last interval that finishes before intervals_sorted[j] starts."""
        return bisect.bisect_right(finish_times, intervals_sorted[j][0]) - 1

    dp = [0] * (n + 1)
    for j in range(1, n + 1):
        iv = intervals_sorted[j - 1]
        p = latest_compatible(j - 1)
        dp[j] = max(dp[j - 1], dp[p + 1] + iv[2])

    # Backtrack
    selected = []
    j = n
    while j > 0:
        iv = intervals_sorted[j - 1]
        p = latest_compatible(j - 1)
        if dp[p + 1] + iv[2] > dp[j - 1]:
            selected.append(sorted_idx[j - 1])
            j = p + 1
        else:
            j -= 1

    return dp[n], selected


# ── Job Shop Scheduling (NP-Hard -- brute force for tiny instances) ────────────

def job_shop_brute(jobs: list, n_machines: int) -> int:
    """
    Each job is a list of (machine, duration) operations in order.
    Find the schedule (start times) minimizing makespan.
    Brute force over all permutations of jobs on each machine -- O((n!)^m).
    Only feasible for tiny instances.
    """
    from itertools import permutations

    n_jobs = len(jobs)
    best_makespan = float("inf")

    # Try all orderings of jobs on each machine
    for perm in permutations(range(n_jobs)):
        # Simulate this ordering
        job_end = [0] * n_jobs       # When each job finishes its last operation
        machine_free = [0] * n_machines  # When each machine is free

        op_idx = [0] * n_jobs  # Next operation index for each job
        job_order = list(perm)

        # Simple simulation: process operations in job order
        start = [[] for _ in range(n_jobs)]
        job_end2 = [0] * n_jobs
        machine_free2 = [0] * n_machines
        op_done = [0] * n_jobs

        for _ in range(sum(len(j) for j in jobs)):
            # Find next ready job (respects machine and job precedence)
            for job in job_order:
                if op_done[job] < len(jobs[job]):
                    mach, dur = jobs[job][op_done[job]]
                    ready = max(job_end2[job], machine_free2[mach])
                    job_end2[job] = ready + dur
                    machine_free2[mach] = ready + dur
                    op_done[job] += 1

        makespan = max(job_end2)
        best_makespan = min(best_makespan, makespan)

    return best_makespan


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Interval scheduling (unweighted)
    intervals_uw = [(1,4),(2,6),(3,5),(5,7),(6,9),(8,10)]
    selected = interval_scheduling(intervals_uw)
    print("Interval Scheduling (greedy, O(n log n) -- in P):")
    for i in selected:
        print(f"  Interval {i}: [{intervals_uw[i][0]}, {intervals_uw[i][1]}]")
    print(f"  Count: {len(selected)}")

    # Weighted interval scheduling
    intervals_w = [(1,4,3),(2,6,5),(3,5,2),(5,7,4),(6,9,6),(8,10,3)]
    weight, selected_w = weighted_interval_scheduling(intervals_w)
    print(f"\nWeighted Interval Scheduling (DP, O(n log n) -- in P):")
    for i in selected_w:
        s,f,w = intervals_w[i]
        print(f"  Interval {i}: [{s},{f}] weight={w}")
    print(f"  Total weight: {weight}")

    # Job shop (NP-Hard)
    # 2 jobs, 2 machines
    jobs = [
        [(0, 3), (1, 2)],  # Job 0: machine 0 then machine 1
        [(1, 2), (0, 3)],  # Job 1: machine 1 then machine 0
    ]
    makespan = job_shop_brute(jobs, 2)
    print(f"\nJob Shop Scheduling (brute force -- NP-Hard for m>=3):")
    print(f"  Minimum makespan: {makespan}")

    print("\nKey insight:")
    print("  Interval scheduling (unweighted) -- O(n log n), in P")
    print("  Interval scheduling (weighted)   -- O(n log n), in P")
    print("  Job shop scheduling (m>=3 mach.) -- NP-Hard")
