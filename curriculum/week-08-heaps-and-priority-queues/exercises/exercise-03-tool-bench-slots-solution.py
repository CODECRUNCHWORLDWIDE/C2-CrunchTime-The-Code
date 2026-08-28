"""exercise-03-tool-bench-slots-solution.py — the repair bench's biggest-job-first rota.

The tool library's repair bench works in fifteen-minute slots. At the start of
every slot it picks the tool with the most repair time still outstanding, works
one slot on it, and puts what is left back in the queue.

`heapq` only ever hands back the smallest item, so the biggest-first rule is
built by storing minus the outstanding minutes and negating them again on the
way out.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (tool, outstanding repair minutes)
JOBS: list[tuple[str, int]] = [
    ("bandsaw", 70),
    ("chain hoist", 25),
    ("hedge trimmer", 45),
    ("mitre saw", 70),
    ("router", 10),
    ("sander", 30),
]

SLOT_MINUTES = 15


# ---- Your task ----
def build_bench(jobs: list[tuple[str, int]]) -> list[tuple[int, str]]:
    """Return a NEW heapified queue whose front is the largest outstanding job.

    Args:
        jobs: (tool, outstanding minutes) rows. This list is not modified.

    Returns:
        A heapified list of (minus outstanding, tool) entries. Entry 0 is the
        tool with the most work left; ties go to the earlier name, A to Z.
    """
    bench = [(-minutes, tool) for tool, minutes in jobs]
    heapq.heapify(bench)
    return bench


def biggest_job(bench: list[tuple[int, str]]) -> tuple[str, int] | None:
    """Return the front job as (tool, outstanding minutes), without removing it.

    Args:
        bench: A queue from build_bench.

    Returns:
        (tool, a positive minute count), or None when the bench is empty. The
        minus sign the queue stores is undone here, so callers never see it.
    """
    if not bench:
        return None
    stored, tool = bench[0]
    return tool, -stored


def bench_log(
    jobs: list[tuple[str, int]], slot_minutes: int
) -> list[tuple[int, str, int]]:
    """Return one row per worked slot.

    Args:
        jobs: (tool, outstanding minutes) rows. This list is not modified.
        slot_minutes: How many minutes one slot covers.

    Returns:
        (slot number starting at 1, tool worked, minutes still outstanding
        after the slot). A tool that reaches zero is not queued again.
    """
    bench = build_bench(jobs)
    log = []
    slot = 0
    while bench:
        stored, tool = heapq.heappop(bench)
        slot += 1
        left = max(-stored - slot_minutes, 0)
        log.append((slot, tool, left))
        if left:
            heapq.heappush(bench, (-left, tool))
    return log


def finish_order(jobs: list[tuple[str, int]], slot_minutes: int) -> list[str]:
    """Return the tools in the order their last slot was worked.

    Args:
        jobs: (tool, outstanding minutes) rows. This list is not modified.
        slot_minutes: How many minutes one slot covers.

    Returns:
        Tool names, first finished first.
    """
    return [tool for _, tool, left in bench_log(jobs, slot_minutes) if left == 0]


def slots_per_tool(jobs: list[tuple[str, int]], slot_minutes: int) -> dict[str, int]:
    """Return how many slots each tool took.

    Args:
        jobs: (tool, outstanding minutes) rows. This list is not modified.
        slot_minutes: How many minutes one slot covers.

    Returns:
        A dict of tool to slot count.
    """
    counts: dict[str, int] = {}
    for _, tool, _ in bench_log(jobs, slot_minutes):
        counts[tool] = counts.get(tool, 0) + 1
    return counts


# ---- Self-check ----
if __name__ == "__main__":
    bench = build_bench(JOBS)
    print(f"front of the bench: {biggest_job(bench)}")
    print(f"raw entry at the front: {bench[0]}")

    print("slot log:")
    for slot, tool, left in bench_log(JOBS, SLOT_MINUTES):
        print(f"  slot {slot:2d}  {tool:<13} {left:3d} min left")

    print(f"finish order: {finish_order(JOBS, SLOT_MINUTES)}")
    print(f"slots per tool: {slots_per_tool(JOBS, SLOT_MINUTES)}")
    print(f"front of an empty bench: {biggest_job([])}")

    log = bench_log(JOBS, SLOT_MINUTES)
    assert biggest_job(bench) == ("bandsaw", 70)
    assert bench[0] == (-70, "bandsaw")
    assert log[0] == (1, "bandsaw", 55)
    assert log[1] == (2, "mitre saw", 55)
    assert log[-1][1] == "router"
    assert len(log) == 18
    assert finish_order(JOBS, SLOT_MINUTES)[0] == "hedge trimmer"
    assert finish_order(JOBS, SLOT_MINUTES)[-1] == "router"
    assert slots_per_tool(JOBS, SLOT_MINUTES)["bandsaw"] == 5
    assert slots_per_tool(JOBS, SLOT_MINUTES)["router"] == 1
    assert sum(slots_per_tool(JOBS, SLOT_MINUTES).values()) == 18
    assert biggest_job([]) is None
    assert JOBS[0] == ("bandsaw", 70)  # original rows untouched
    print("All checks passed.")
