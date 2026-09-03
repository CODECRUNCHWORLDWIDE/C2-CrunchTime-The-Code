# Exercise 2 — The Sluice Gate Settling

> **Topic:** what the settled set is actually for, demonstrated by taking it out
> **Lecture:** [01 — Dijkstra and the Shortest-Path Picker](../lecture-notes/01-dijkstra-and-the-shortest-path-picker.md)
> **Difficulty:** Easy-Medium
> **Target time:** 40 minutes
> **Why this one:** every explanation of the settled set says "once a node is settled its answer never changes". This page runs the same algorithm without it, on data chosen so that exactly one gate comes out wrong, and prints both tables side by side. One wrong row is more convincing than a paragraph.

## The Brief

An irrigation district opens its head gate and water runs downhill through a web
of channels. Each channel takes a whole number of minutes.

Report two things: the **order** the gates get their final answer in, with the
minute each is settled, and the same answer as a plain lookup table.

Then run the identical algorithm **with the settled set removed** and compare.

## Starter

`exercise-02-sluice-gate-settling-solution.py` sits beside this page with the
channels and the self-checks.

```text
Head Gate  -> Bywash       1 min      Cut Sluice -> Tail Weir   1 min
Head Gate  -> Cut Sluice   4 min      Cut Sluice -> Fold Drain  6 min
Bywash     -> Cut Sluice   1 min      Tail Weir  -> Fold Drain  5 min
```

The channels are chosen so that Cut Sluice can be reached two ways — directly in
4 minutes, or via Bywash in 2. Which of those the algorithm keeps is the entire
exercise.

## Requirements

1. `settling_order(channels, head)` returns `(gate, minute)` pairs in the order
   the gates settle.
2. `arrival_minutes(channels, head)` returns the same information as a dict.
3. `arrival_minutes_no_settled(channels, head)` is the identical algorithm with
   the settled set removed — shipped on purpose, to be run and compared.
4. `compare_tables(channels, head)` prints the two side by side and marks the
   difference.
5. The two tables differ in **exactly one** gate on this data.

## Constraints

- **A gate settles once**, at the moment it comes off the frontier, and its
  answer is final from then on.
- **The broken version must be the same algorithm minus one thing.** If it
  differs in any other way, the comparison proves nothing about the settled set.
- **The settling order is not the gate order and not the minute order.** It is
  the order the frontier hands them over, and printing it is what makes the
  mechanism visible.
- **The difference is marked in the output**, not left for the reader to spot.
  A comparison table nobody reads carefully is a table that proves nothing.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-02-sluice-gate-settling-solution.py
Settling order from Head Gate
  1. Head Gate at 0 min
  2. Bywash at 1 min
  3. Cut Sluice at 2 min
  4. Tail Weir at 3 min
  5. Fold Drain at 8 min

gate        with   without
Head Gate     0      0
Bywash        1      1
Cut Sluice    2      4   <- wrong
Tail Weir     3      3
Fold Drain    8      8
All checks passed.
```

**Cut Sluice: 2 minutes with the settled set, 4 without.**

That is the whole page. Without the settled set the algorithm accepts the direct
4-minute channel when it first sees it and never revisits the gate, so the
2-minute route through Bywash is found too late to matter. Every other gate
agrees, which is exactly what makes the one disagreement worth looking at — a
version that got everything wrong would be obviously broken and would teach
nothing.

Note also that Fold Drain is 8, not 7: via Cut Sluice and Tail Weir it is
2 + 1 + 5 = 8, and via Cut Sluice directly it is 2 + 6 = 8. A tie, and both
versions agree on it.

## Steps

1. Read the self-checks. They are the spec.
2. Work out both routes to Cut Sluice by hand. Two minutes, not four.
3. Write the memo: settle on removal from the frontier, and never touch a settled
   gate again.
4. Write `settling_order` and print it. Look at the order — it is by minute, and
   seeing that is what makes the next step make sense.
5. Write `arrival_minutes_no_settled` by copying the first and deleting the
   settled check. Nothing else.
6. Run them side by side. Find the one wrong row before reading the answer above.
7. Write the FRAME pass, and put the wrong row in it.

## The Solution

```python
"""exercise-02-sluice-gate-settling-solution.py — the settled set, and what it is for.

An irrigation district opens its head gate and water runs downhill through a
web of channels. Each channel takes a whole number of minutes. Two functions
answer two questions:

  settling_order  — the order the gates get their final answer, and when
  arrival_minutes — the same answer as a plain dict of gate -> minutes

A third function, arrival_minutes_no_settled, is the same algorithm with the
settled set taken out. It is shipped on purpose: running the two side by side
is the whole point of the exercise. One gate, and only one, comes out wrong.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (upstream gate, downstream gate, minutes for water to travel)
Channel = tuple[str, str, int]

CHANNELS: list[Channel] = [
    ("Head Gate", "Bywash", 1),
    ("Head Gate", "Cut Sluice", 4),
    ("Bywash", "Cut Sluice", 1),
    ("Cut Sluice", "Tail Weir", 1),
    ("Cut Sluice", "Fold Drain", 6),
    ("Tail Weir", "Fold Drain", 5),
]


# ---- Your task ----
def build_channels(channels: list[Channel]) -> dict[str, list[tuple[str, int]]]:
    """Return the downhill channels keyed by the gate they leave from.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).

    Returns:
        A dict where downhill[gate] is a list of (downstream gate, minutes).
        Every gate named anywhere is a key, including the ones nothing
        leaves from.
    """
    downhill: dict[str, list[tuple[str, int]]] = {}
    for upstream, downstream, minutes in channels:
        downhill.setdefault(upstream, []).append((downstream, minutes))
        downhill.setdefault(downstream, [])
    return downhill


def settling_order(channels: list[Channel], head: str) -> list[tuple[str, int]]:
    """Return the gates in the order their arrival time is settled.

    A gate is settled the first time it comes off the queue. That is the
    moment its answer is final and can never improve again.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A list of (gate, minutes) in settling order. Water that never
        reaches a gate leaves that gate out of the list entirely.
    """
    downhill = build_channels(channels)
    best: dict[str, int] = {head: 0}
    settled: set[str] = set()
    order: list[tuple[str, int]] = []
    queue: list[tuple[int, str]] = [(0, head)]

    while queue:
        so_far, gate = heapq.heappop(queue)
        if gate in settled:
            continue
        settled.add(gate)
        order.append((gate, so_far))
        for downstream, minutes in downhill.get(gate, []):
            total = so_far + minutes
            if total < best.get(downstream, float("inf")):
                best[downstream] = total
                heapq.heappush(queue, (total, downstream))

    return order


def arrival_minutes(channels: list[Channel], head: str) -> dict[str, int]:
    """Return the minute the water reaches each gate it can reach.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A dict of gate -> minutes, built from the settling order so the two
        functions can never disagree.
    """
    return dict(settling_order(channels, head))


# ---- Given: the same algorithm with the settled set removed ----
def arrival_minutes_no_settled(channels: list[Channel], head: str) -> dict[str, int]:
    """The broken version. Do not fix it; run it and read the difference.

    Every pop writes its own number straight into the answer, with nothing
    checking whether that gate was already settled. A stale copy of a gate
    that is still sitting in the queue will pop later, carrying a larger
    number, and overwrite the correct one.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A dict of gate -> minutes that is wrong for at least one gate.
    """
    downhill = build_channels(channels)
    best: dict[str, int] = {head: 0}
    answer: dict[str, int] = {}
    queue: list[tuple[int, str]] = [(0, head)]

    while queue:
        so_far, gate = heapq.heappop(queue)
        answer[gate] = so_far          # <- no settled set, so this can be undone
        for downstream, minutes in downhill.get(gate, []):
            total = so_far + minutes
            if total < best.get(downstream, float("inf")):
                best[downstream] = total
                heapq.heappush(queue, (total, downstream))

    return answer


def compare_tables(channels: list[Channel], head: str) -> list[str]:
    """Return one printable row per gate, correct beside broken.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        Rows sorted by the correct arrival time, then by gate name. A row
        whose two numbers disagree is marked "<- wrong".
    """
    right = arrival_minutes(channels, head)
    wrong = arrival_minutes_no_settled(channels, head)
    rows = []
    for minutes, gate in sorted((m, g) for g, m in right.items()):
        flag = "" if wrong[gate] == minutes else "   <- wrong"
        rows.append(f"{gate:<11}{minutes:4d}{wrong[gate]:7d}{flag}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("Settling order from Head Gate")
    for place, (gate, minutes) in enumerate(settling_order(CHANNELS, "Head Gate"), 1):
        print(f"  {place}. {gate} at {minutes} min")

    print()
    print("gate        with   without")
    for row in compare_tables(CHANNELS, "Head Gate"):
        print(row)

    right = arrival_minutes(CHANNELS, "Head Gate")
    assert right == {
        "Head Gate": 0,
        "Bywash": 1,
        "Cut Sluice": 2,
        "Tail Weir": 3,
        "Fold Drain": 8,
    }
    assert [gate for gate, _ in settling_order(CHANNELS, "Head Gate")] == [
        "Head Gate",
        "Bywash",
        "Cut Sluice",
        "Tail Weir",
        "Fold Drain",
    ]

    wrong = arrival_minutes_no_settled(CHANNELS, "Head Gate")
    assert wrong["Cut Sluice"] == 4            # the stale 4 popped last and won
    assert wrong["Fold Drain"] == 8            # every other gate is still right
    assert sum(1 for gate in right if right[gate] != wrong[gate]) == 1

    from_bywash = arrival_minutes(CHANNELS, "Bywash")
    assert "Head Gate" not in from_bywash      # water does not run uphill
    assert from_bywash["Fold Drain"] == 7
    print("All checks passed.")
```

Shipping the broken version alongside the correct one is unusual and deliberate.
An invariant you have only read about is a thing you will drop under time
pressure; an invariant you have watched fail on a five-gate district is one you
remember.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-02-sluice-gate-settling-solution.py
```

No third-party packages, no arguments, no input. It prints the settling order,
the two tables side by side with the difference marked, and then
`All checks passed.`

## Common bugs to catch

- **Settling on insertion rather than on removal.** Symptom: this exercise's bug,
  in the version that was meant to be correct.
- **A "broken" version that differs in more than the settled set.** Symptom: two
  tables that differ everywhere, and a comparison that shows nothing.
- **Reporting the settling order as sorted by gate name.** Symptom: a tidy list
  that hides the mechanism.
- **Not marking the difference.** Symptom: two tables and a reader who takes your
  word for it.
- **Assuming ties break the same way in both versions.** They need not, and Fold
  Drain is the tie here. Check it rather than assuming.

## Acceptance checklist

- [ ] Cut Sluice is 2 minutes with the settled set and 4 without.
- [ ] Every other gate agrees between the two versions.
- [ ] The settling order is Head Gate, Bywash, Cut Sluice, Tail Weir, Fold Drain.
- [ ] Fold Drain is 8 minutes in both versions.
- [ ] The output marks the differing row.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a channel that makes a **second** gate disagree, and say what property the
  new channel needed to have. It is a specific shape, and naming it is the real
  understanding.
- Count how many times each version pushes to the frontier. The broken one does
  less work and gets a worse answer, which is the trade nobody would take
  knowingly.
- Make every channel cost 1 minute and re-run. Both versions now agree
  everywhere; say why, and what that tells you about when the settled set is
  load-bearing.
