"""
Minimum Makespan Scheduling -- NP-Hard optimization
===================================================
Given jobs with processing times and m identical machines, assign jobs to
machines so that the maximum machine load (the makespan) is as small as
possible.

Why NP-Hard:
- The decision version asks whether there is a schedule with makespan at most T.
- That problem is NP-Complete when the number of machines is part of the input.
- Therefore, minimizing makespan is NP-Hard.

Is it in NP?
- The optimization problem is not itself a decision language.
- The decision version is in NP because a schedule can be checked quickly.

Key properties:
- Even the two-machine case captures the PARTITION problem.
- Exact search is exponential.
- LPT (Longest Processing Time first) is a standard practical heuristic.

This module includes:
- A brute-force branch-and-bound exact solver.
- The LPT heuristic.
"""


def lpt_schedule(jobs, machine_count):
    loads = [0] * machine_count
    assignment = [[] for _ in range(machine_count)]
    for job in sorted(jobs, reverse=True):
        machine = min(range(machine_count), key=lambda i: (loads[i], i))
        assignment[machine].append(job)
        loads[machine] += job
    return assignment, max(loads, default=0)


def brute_force_minimum_makespan(jobs, machine_count):
    jobs = sorted(jobs, reverse=True)
    heuristic_assignment, heuristic_value = lpt_schedule(jobs, machine_count)
    best = {"assignment": heuristic_assignment, "value": heuristic_value}
    loads = [0] * machine_count
    assignment = [[] for _ in range(machine_count)]

    def search(index):
        if max(loads, default=0) >= best["value"]:
            return
        if index == len(jobs):
            best["value"] = max(loads, default=0)
            best["assignment"] = [list(machine_jobs) for machine_jobs in assignment]
            return
        job = jobs[index]
        seen_loads = set()
        for machine in range(machine_count):
            if loads[machine] in seen_loads:
                continue
            seen_loads.add(loads[machine])
            loads[machine] += job
            assignment[machine].append(job)
            search(index + 1)
            assignment[machine].pop()
            loads[machine] -= job

    search(0)
    return best["assignment"], best["value"]


if __name__ == "__main__":
    jobs = [9, 8, 7, 6, 5, 4]
    machines = 3

    exact_assignment, exact_value = brute_force_minimum_makespan(jobs, machines)
    heuristic_assignment, heuristic_value = lpt_schedule(jobs, machines)

    print("Minimum Makespan Scheduling (NP-Hard)")
    print(f"Jobs: {jobs}")
    print(f"Machines: {machines}")
    print(f"Exact makespan: {exact_value} with assignment {exact_assignment}")
    print(f"LPT makespan:   {heuristic_value} with assignment {heuristic_assignment}")
