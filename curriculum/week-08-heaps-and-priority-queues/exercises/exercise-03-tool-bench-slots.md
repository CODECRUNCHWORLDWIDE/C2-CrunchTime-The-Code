# Exercise 3 — The Tool Bench Rota

> **Topic:** a max-heap out of `heapq`, by negation, doing real scheduling work
> **Lecture:** [02 — Heaps of Tuples and the k-Closest Shape](../lecture-notes/02-heap-of-tuples-and-k-closest.md)
> **Difficulty:** Beginner-Medium
> **Target time:** 35 minutes
> **Why this one:** `heapq` has no max-heap, and every scheduling problem this week wants one. This is the page where negation stops being a trick you half-remember and becomes something you can explain in a sentence.

## The Brief

The tool library's repair bench works in **fifteen-minute slots**. At the start
of every slot it picks the tool with the **most repair time still outstanding**,
works one slot on it, and puts what is left back in the queue. A tool with ten
minutes left still gets a whole slot; the bench does not split slots.

That rule — biggest first, one slot at a time — spreads the bench across the big
jobs instead of finishing them one by one, which is what the library wants: no
member waits all afternoon while a bandsaw is rebuilt.

`heapq` only ever hands back the **smallest** item. Getting "biggest first" out
of it is the exercise.

## Starter

`exercise-03-tool-bench-slots-solution.py` sits beside this page with the day's
jobs and the self-checks.

```text
tool             outstanding
bandsaw                70 min
chain hoist            25 min
hedge trimmer          45 min
mitre saw              70 min
router                 10 min
sander                 30 min
```

Two tools are tied at 70. Decide what that means *before* you write the loop —
the tie is the first thing your heap will hit.

## Requirements

1. `build_bench(jobs)` returns a heap of `(-minutes, tool)` entries.
2. `biggest_job(bench)` reads the front without disturbing it, and returns the
   tool and its **positive** outstanding minutes — or `None` on an empty bench.
3. `bench_log(bench, slot_minutes)` returns one row per slot: the tool worked and
   what it has left afterwards.
4. `finish_order(jobs, slot_minutes)` returns the tools in the order they reach
   zero.
5. `slots_per_tool(jobs, slot_minutes)` returns how many slots each tool got.

## Constraints

- **Store the negation, return the positive.** The minus sign lives inside the
  heap and nowhere else. A function that hands a caller `-70` has leaked the
  implementation.
- **Ties break by name**, because the tuple's second element is the tool, and
  that is what `heapq` compares when the first elements match. Say so in the memo
  rather than discovering it in the output.
- **A tool that reaches zero is done** and does not go back on the heap.
- **Reading the front is `bench[0]`,** not a pop and a push. Popping to look is
  the bug this page exists to prevent.
- The last slot of a job is still a full slot, even if the job needs five minutes
  of it. That is the bench's rule.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-03-tool-bench-slots.py
front of the bench: ('bandsaw', 70)
raw entry at the front: (-70, 'bandsaw')
slot log:
  slot  1  bandsaw        55 min left
  slot  2  mitre saw      55 min left
  slot  3  bandsaw        40 min left
  slot  4  mitre saw      40 min left
  slot  5  hedge trimmer  30 min left
  slot  6  bandsaw        25 min left
  slot  7  mitre saw      25 min left
  slot  8  hedge trimmer  15 min left
  slot  9  sander         15 min left
  slot 10  bandsaw        10 min left
  slot 11  chain hoist    10 min left
  slot 12  mitre saw      10 min left
  slot 13  hedge trimmer   0 min left
  slot 14  sander          0 min left
  slot 15  bandsaw         0 min left
  slot 16  chain hoist     0 min left
  slot 17  mitre saw       0 min left
  slot 18  router          0 min left
finish order: ['hedge trimmer', 'sander', 'bandsaw', 'chain hoist', 'mitre saw', 'router']
slots per tool: {'bandsaw': 5, 'mitre saw': 5, 'hedge trimmer': 3, 'sander': 2, 'chain hoist': 2, 'router': 1}
front of an empty bench: None
All checks passed.
```

Look at the finish order against the outstanding minutes. The **hedge trimmer**
finishes first at 45 minutes, before either 70-minute job — and the **router**,
the smallest job on the bench at 10 minutes, finishes *last*. Biggest-first is
not shortest-first, and the price of spreading the bench is that the small jobs
wait. That is the trade-off the write-up has to name.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: min-heap, negated key, and the one sentence that makes it a
   max-heap.
3. Build the bench and print the raw front entry once, so you have seen the
   `(-70, 'bandsaw')` shape with your own eyes.
4. Write the slot loop. Pop, subtract one slot, push back only if something is
   left.
5. Derive `finish_order` and `slots_per_tool` from the log rather than
   re-simulating. If they disagree with the log, one of the three is wrong.
6. Handle the empty bench, then write the FRAME pass.

## The Solution

```python
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
```

`biggest_job` returning the positive number is the whole discipline of this page
in one function: the negation is a storage decision, and no caller should have
to know about it.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-03-tool-bench-slots.py
```

No third-party packages, no arguments, no input. It prints the front of the
bench, the raw heap entry behind it, the slot log, the finish order, the slots
per tool, and then `All checks passed.`

## Common bugs to catch

- **Negating on the way in and forgetting on the way out.** Symptom: a report
  full of negative minutes.
- **Popping to read the front.** Symptom: the front job silently vanishes from
  the rota.
- **Pushing a finished tool back with zero minutes.** Symptom: a slot spent on a
  tool that needed nothing, and a log two rows too long.
- **Subtracting the slot from the negated value in the wrong direction.**
  Symptom: outstanding minutes that grow. Negate, do the arithmetic in positive
  numbers, negate back.
- **Assuming the tie order.** Symptom: a log that is right today and wrong when a
  tool is renamed. The tuple decides, and you should say what it decides.
- **Splitting the last slot.** Symptom: 18 slots become 17.5, and the bench does
  not work that way.

## Acceptance checklist

- [ ] The front of the bench is `('bandsaw', 70)` — positive, not negated.
- [ ] The slot log is 18 rows for the shipped jobs.
- [ ] The hedge trimmer finishes first; the router finishes last.
- [ ] `slots_per_tool` sums to the number of rows in the log.
- [ ] `biggest_job` on an empty bench returns `None` rather than raising.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Change the rule to shortest-first and re-run. The finish order inverts; say in
  one sentence which rule the library should actually use and for whom.
- Report the longest a member waits under each rule. That is the number the two
  rules are really trading against each other.
- Add a second bench and say what changes. The heap does not; the loop does.
