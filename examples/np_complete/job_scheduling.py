"""
Job Scheduling -- NP-Complete
==============================
Given n jobs each with a processing time and deadline, and m identical machines,
can all jobs be completed by their deadlines?

More specifically: Preemptive scheduling on identical machines is in P,
but many scheduling variants are NP-Complete, including:
- Minimizing weighted completion time on unrelated machines
- 3-machine job shop scheduling
- Minimizing makespan on m >= 3 identical machines (Partition reduction)

This implements the classic Makespan Minimization:
Given n jobs and m machines, can we assign jobs to machines such that
the maximum completion time (makespan) <= T?

This reduces directly from Partition (2 machines) and is NP-Complete for m >= 2.

Verifier:  Check every job assigned, each machine load <= T -- O(n).
Solver:    Brute-force assigns jobs to machines -- O(m^n).
Approx:    LPT (Longest Processing Time first) gives 4/3 - 1/(3m) approximation.
"""

from itertools import product


def makespan(assignment: list, times: list, m: int) -> float:
    loads = [0.0] * m
    for job, machine in enumerate(assignment):
        loads[machine] += times[job]
    return max(loads)


def verify(assignment: list, times: list, m: int, T: float) -> bool:
    if len(assignment) != len(times):
        return False
    if any(a < 0 or a >= m for a in assignment):
        return False
    return makespan(assignment, times, m) <= T


def solve_brute(times: list, m: int, T: float) -> list | None:
    """Try all m^n assignments."""
    for assignment in product(range(m), repeat=len(times)):
        if makespan(list(assignment), times, m) <= T:
            return list(assignment)
    return None


def solve_lpt(times: list, m: int) -> tuple:
    """
    Longest Processing Time (LPT) heuristic -- O(n log n).
    Sort jobs by decreasing time, assign each to least loaded machine.
    """
    order = sorted(range(len(times)), key=lambda i: -times[i])
    loads = [0.0] * m
    assignment = [0] * len(times)

    for job in order:
        least = min(range(m), key=lambda i: loads[i])
        assignment[job] = least
        loads[least] += times[job]

    return assignment, max(loads)


if __name__ == "__main__":
    import math

    jobs = [6, 5, 4, 4, 3, 3, 2, 2, 1]
    m = 3
    optimal_lower = math.ceil(sum(jobs) / m)

    print(f"Jobs (processing times): {jobs}")
    print(f"Machines: {m}")
    print(f"Sum of jobs: {sum(jobs)}, Lower bound on makespan: {optimal_lower}")

    # LPT heuristic
    lpt_assign, lpt_make = solve_lpt(jobs, m)
    print(f"\nLPT makespan: {lpt_make}")
    for machine in range(m):
        machine_jobs = [jobs[j] for j, a in enumerate(lpt_assign) if a == machine]
        print(f"  Machine {machine+1}: jobs {machine_jobs}  load={sum(machine_jobs)}")

    # Brute force for small instance
    small_jobs = [4, 5, 3, 2, 6]
    small_m = 2
    T = 10
    print(f"\nSmall example -- Jobs: {small_jobs}, m={small_m}, T={T}")
    result = solve_brute(small_jobs, small_m, T)
    if result:
        print(f"Feasible assignment found (makespan={makespan(result, small_jobs, small_m)}):")
        for machine in range(small_m):
            load = [small_jobs[j] for j, a in enumerate(result) if a == machine]
            print(f"  Machine {machine+1}: {load}  sum={sum(load)}")
        print(f"Verification: {verify(result, small_jobs, small_m, T)}")
    else:
        print(f"No feasible schedule with makespan <= {T}")
