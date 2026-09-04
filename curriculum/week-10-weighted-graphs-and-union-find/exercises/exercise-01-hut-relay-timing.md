# Exercise 1 — The Hut Relay Timing

> **Topic:** the shortest-path picker at its plainest — a frontier ordered by cost, and a settled answer per node
> **Lecture:** [01 — Dijkstra and the Shortest-Path Picker](../lecture-notes/01-dijkstra-and-the-shortest-path-picker.md)
> **Difficulty:** Easy
> **Target time:** 35 minutes
> **Why this one:** every weighted-graph page this week is this page with something added. It also settles the thing beginners get wrong first — a link is one-way unless the data says otherwise — and it does it with an unreachable hut you can see on the map.

## The Brief

A row of mountain huts passes one snow-depth reading along by radio. Each link
takes a whole number of seconds, and **every link points one way**, because a
hut's aerial is aimed at the next hut and not back.

Two questions: how many seconds until each hut has heard the reading, and which
hut hears it last.

## Starter

The worked answer on this page carries the huts, the links and the
self-checks.

```text
Ash Col   -> Bell Tarn      4s      Cairn Gap -> Dun Force     5s
Ash Col   -> Cairn Gap      9s      Cairn Gap -> Elder Scree  12s
Bell Tarn -> Cairn Gap      3s      Cairn Gap -> Fell Hause    9s
Bell Tarn -> Dun Force      8s      Dun Force -> Elder Scree   4s
```

Ash Col reaches Cairn Gap directly in 9 seconds, and via Bell Tarn in 7. That is
the whole shape of the problem on one pair of huts, and it is worth having on
paper before you write anything.

Notice also that **nothing points back to Ash Col**. Release the reading from
Bell Tarn instead and Ash Col never hears it at all.

## Requirements

1. `build_aerials(links)` turns the link list into a map from hut to
   `(hut, seconds)` pairs.
2. `relay_seconds(links, start)` returns the seconds to each hut that hears the
   reading. Huts that never hear it are **absent**, not infinite.
3. `slowest_hut(links, huts, start)` returns the last hut and its time — or
   `None` when some hut never hears it at all.
4. `relay_table(links, start)` formats the result for printing.
5. The start hut is at 0 seconds.

## Constraints

- **Links are one-way.** The data lists each direction separately, and adding the
  reverse edge "to be helpful" changes every answer.
- **The frontier is ordered by total seconds so far**, not by the length of the
  next link. That distinction is the algorithm.
- **A hut is settled once**, and its answer never changes afterwards. If you find
  yourself lowering a settled hut's time, either the graph has a negative link —
  it does not here — or the settled set is not being respected.
- **Unreachable is absent, not a large number.** A hut with no answer must not
  quietly acquire one through arithmetic later on.
- **`slowest_hut` returns `None` when any hut is unreachable**, rather than the
  slowest of the ones that did hear. Reporting the slowest of a partial set as if
  it were the whole answer is the failure this return type exists to prevent.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-01-hut-relay-timing.py
Reading released at Ash Col
   0s  Ash Col
   4s  Bell Tarn
   7s  Cairn Gap
  12s  Dun Force
  16s  Elder Scree
  16s  Fell Hause
last to hear: ('Elder Scree', 16)

Reading released at Bell Tarn
   0s  Bell Tarn
   3s  Cairn Gap
   8s  Dun Force
  12s  Elder Scree
  12s  Fell Hause
last to hear: None
All checks passed.
```

Two things to read. From Ash Col, **Cairn Gap is at 7 seconds, not 9** — the
route through Bell Tarn beats the direct link, which is the entire reason this is
a search and not a lookup.

And from Bell Tarn, `slowest_hut` is **`None`**: Ash Col never hears the reading,
so there is no "last hut". Elder Scree at 12 seconds would be a plausible answer
and it would be wrong.

## Steps

1. Read the self-checks. They are the spec.
2. Work out Ash Col to Cairn Gap by hand, both ways. It takes thirty seconds and
   it is the whole idea.
3. Write the memo: a frontier ordered by total cost, a settled set, one answer per
   hut.
4. Build the aerial map, then the search. Keep the settled set explicit rather
   than implied — it is the subject of [Exercise 2](./exercise-02-sluice-gate-settling.md).
5. Handle the unreachable case in `relay_seconds` first, then in `slowest_hut`.
6. Release from Bell Tarn and confirm the `None`. Then write the FRAME pass.

## The Solution

```python
"""exercise-01-hut-relay-timing-solution.py — how fast a snow reading crosses a ridge.

A row of mountain huts passes one snow-depth reading along by radio. Each
radio link takes a whole number of seconds, and every link points one way,
because a hut's aerial is aimed at the next hut and not back.

Two questions, two functions:

  relay_seconds  — how many seconds until each hut has heard the reading
  slowest_hut    — which hut hears it last, and when

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (sending hut, receiving hut, seconds on that link)
Link = tuple[str, str, int]

HUTS: list[str] = [
    "Ash Col",
    "Bell Tarn",
    "Cairn Gap",
    "Dun Force",
    "Elder Scree",
    "Fell Hause",
]

LINKS: list[Link] = [
    ("Ash Col", "Bell Tarn", 4),
    ("Ash Col", "Cairn Gap", 9),
    ("Bell Tarn", "Cairn Gap", 3),
    ("Bell Tarn", "Dun Force", 8),
    ("Cairn Gap", "Dun Force", 5),
    ("Cairn Gap", "Elder Scree", 12),
    ("Cairn Gap", "Fell Hause", 9),
    ("Dun Force", "Elder Scree", 4),
]


# ---- Your task ----
def build_aerials(links: list[Link]) -> dict[str, list[tuple[str, int]]]:
    """Return the one-way link list keyed by sending hut.

    Args:
        links: Every radio link, as (sender, receiver, seconds).

    Returns:
        A dict where aerials[hut] is a list of (receiver, seconds) pairs.
        Every hut named anywhere in links is a key, even one that only
        receives, so a later lookup never has to guess.
    """
    aerials: dict[str, list[tuple[str, int]]] = {}
    for sender, receiver, seconds in links:
        aerials.setdefault(sender, []).append((receiver, seconds))
        aerials.setdefault(receiver, [])
    return aerials


def relay_seconds(links: list[Link], start: str) -> dict[str, int]:
    """Return the earliest second at which each reachable hut hears the reading.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        start: The hut that reads the snow gauge and starts the relay.

    Returns:
        A dict of hut -> seconds. A hut that can never hear the reading is
        left out of the dict entirely, so `in` is the reachability test.
    """
    aerials = build_aerials(links)
    heard: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]

    while queue:
        so_far, hut = heapq.heappop(queue)
        if hut in settled:
            continue
        settled.add(hut)
        for receiver, seconds in aerials.get(hut, []):
            total = so_far + seconds
            if total < heard.get(receiver, float("inf")):
                heard[receiver] = total
                heapq.heappush(queue, (total, receiver))

    return heard


def slowest_hut(links: list[Link], huts: list[str], start: str) -> tuple[str, int] | None:
    """Return the hut that hears the reading last, and the second it hears it.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        huts: Every hut that must hear the reading.
        start: The hut that starts the relay.

    Returns:
        (hut, seconds) for the last hut to hear it, ties broken by name A to
        Z. None when even one hut in `huts` never hears it at all.
    """
    heard = relay_seconds(links, start)
    if any(hut not in heard for hut in huts):
        return None
    latest, name = min((-heard[hut], hut) for hut in huts)
    return name, -latest


def relay_table(links: list[Link], start: str) -> list[str]:
    """Return one printable row per hut that hears the reading.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        start: The hut that starts the relay.

    Returns:
        Rows sorted by seconds, ties broken by hut name A to Z.
    """
    heard = relay_seconds(links, start)
    ordered = sorted((seconds, hut) for hut, seconds in heard.items())
    return [f"{seconds:4d}s  {hut}" for seconds, hut in ordered]


# ---- Self-check ----
if __name__ == "__main__":
    print("Reading released at Ash Col")
    for row in relay_table(LINKS, "Ash Col"):
        print(row)
    print(f"last to hear: {slowest_hut(LINKS, HUTS, 'Ash Col')}")

    print()
    print("Reading released at Bell Tarn")
    for row in relay_table(LINKS, "Bell Tarn"):
        print(row)
    print(f"last to hear: {slowest_hut(LINKS, HUTS, 'Bell Tarn')}")

    from_ash = relay_seconds(LINKS, "Ash Col")
    assert from_ash["Ash Col"] == 0
    assert from_ash["Cairn Gap"] == 7          # 4 + 3 beats the direct 9
    assert from_ash["Dun Force"] == 12         # 7 + 5 ties 4 + 8; both are 12
    assert from_ash["Elder Scree"] == 16
    assert from_ash["Fell Hause"] == 16
    assert slowest_hut(LINKS, HUTS, "Ash Col") == ("Elder Scree", 16)

    from_bell = relay_seconds(LINKS, "Bell Tarn")
    assert "Ash Col" not in from_bell          # no link points back up the ridge
    assert slowest_hut(LINKS, HUTS, "Bell Tarn") is None
    assert slowest_hut(LINKS, ["Bell Tarn", "Cairn Gap"], "Bell Tarn") == ("Cairn Gap", 3)
    print("All checks passed.")
```

`relay_seconds` returning a dict that simply omits unreachable huts is a
deliberate choice over returning infinity for them. Infinity reads as a number,
survives comparisons, and eventually gets printed to somebody as if it meant
something. Absence has to be handled.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-01-hut-relay-timing.py
```

No third-party packages, no arguments, no input. It prints both releases with
their timings, and then `All checks passed.`

## Common bugs to catch

- **Treating links as two-way.** Symptom: Ash Col hears a reading released from
  Bell Tarn, which the aerials make impossible.
- **Ordering the frontier by the next link's cost.** Symptom: right on this data
  and wrong as soon as a cheap link leads somewhere expensive.
- **Infinity for unreachable huts.** Symptom: a table with `inf` in it, or
  arithmetic on a number that was never real.
- **`slowest_hut` ignoring unreachable huts.** Symptom: a confident answer where
  `None` is the truth.
- **Settling a hut twice.** Symptom: correct answers and wasted work — and a
  habit that becomes a real bug in [Exercise 5](./exercise-05-shunting-rebate-legs.md).
- **Forgetting the start hut is at zero.** Symptom: every time off by the first
  link.

## Acceptance checklist

- [ ] From Ash Col, Cairn Gap is 7 seconds, not 9.
- [ ] From Ash Col, Elder Scree and Fell Hause are both 16.
- [ ] From Bell Tarn, `slowest_hut` returns `None`.
- [ ] Unreachable huts are absent from `relay_seconds`, not infinite.
- [ ] The start hut is at 0 seconds.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return the **route** to each hut, not just the time. It needs one extra map and
  it is what a radio operator would actually want.
- Add the reverse of every link and re-run. Some answers fall; say which and why,
  and note that this is now a different problem the aerials do not support.
- Report which single link, if it were made instant, would help the most huts.
  It is one re-run per link and the answer is not the longest link.
