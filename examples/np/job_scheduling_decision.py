"""
Job Scheduling Decision
=======================
Given jobs with processing times and deadlines, and a number of identical
machines m, decide whether all jobs can be scheduled non-preemptively so that
every job finishes by its deadline.

Why it is in NP:
A certificate is a sequence of jobs for each machine. We can verify in
polynomial time by simulating each machine timeline and checking that every
job appears exactly once and meets its deadline.

Special status:
This parallel-machine deadline scheduling decision problem is NP-Complete when
m is part of the input.
"""

from __future__ import annotations

Job = tuple[str, int, int]


def verify_schedule(jobs: list[Job], schedule: list[list[int]], machine_count: int) -> bool:
    """Verify that the schedule meets all deadlines on at most machine_count machines."""
    if len(schedule) > machine_count:
        return False
    seen: list[int] = []
    for machine_jobs in schedule:
        current_time = 0
        for index in machine_jobs:
            if index < 0 or index >= len(jobs):
                return False
            current_time += jobs[index][1]
            if current_time > jobs[index][2]:
                return False
            seen.append(index)
    return sorted(seen) == list(range(len(jobs)))


def solve_brute_force(jobs: list[Job], machine_count: int) -> list[list[int]] | None:
    """Try schedules by recursively appending jobs to machine queues."""
    schedule: list[list[int]] = [[] for _ in range(machine_count)]
    loads = [0] * machine_count
    order = sorted(range(len(jobs)), key=lambda i: jobs[i][2])

    def backtrack(pos: int) -> bool:
        if pos == len(order):
            return True
        job_index = order[pos]
        _name, duration, deadline = jobs[job_index]
        seen_loads = set()
        for machine in range(machine_count):
            if loads[machine] in seen_loads:
                continue
            if loads[machine] + duration > deadline:
                continue
            seen_loads.add(loads[machine])
            schedule[machine].append(job_index)
            loads[machine] += duration
            if backtrack(pos + 1):
                return True
            loads[machine] -= duration
            schedule[machine].pop()
            if loads[machine] == 0:
                break
        return False

    if backtrack(0):
        return [machine_jobs[:] for machine_jobs in schedule if machine_jobs]
    return None


if __name__ == "__main__":
    jobs = [
        ("A", 2, 2),
        ("B", 1, 2),
        ("C", 2, 3),
        ("D", 1, 4),
    ]
    machine_count = 2
    schedule = solve_brute_force(jobs, machine_count)
    print(f"Jobs: {jobs}")
    print(f"Machines: {machine_count}")
    print(f"Schedule found: {schedule}")
    print(f"Verified: {verify_schedule(jobs, schedule, machine_count) if schedule is not None else False}")
