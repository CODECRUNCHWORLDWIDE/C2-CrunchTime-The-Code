# Problem 4 — Cairn Routes

> **Topic:** two searches, one from each end, and the arithmetic that reads the answer out of them
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Medium-Hard
> **Target time:** 60 minutes
> **Why this one:** it is the first page where the answer is not produced by the search at all. Both searches finish, and then one line of arithmetic decides which cairns matter. That separation — search, then read — is the thing to carry into [Challenge 1](../challenges/challenge-01-trunk-splice.md).

## The Brief

A mountain rescue team keeps a map of cairns and the paths between them. Before a
search they want two things about the quickest way from one cairn to another:

1. **how many different quickest ways there are**, and
2. **which cairns lie on at least one of them** — that is where the spotters go.

One breadth-first search from each end answers both. A cairn is on a quickest
route exactly when its distance from one end **plus** its distance from the other
adds up to the length of the whole route. Any cairn where the sum is larger is on
a detour, however close it looks on the map.

## Starter

`problem-04-cairn-routes-solution.py` sits beside this page with the map and the
self-checks.

```text
ALDER  — BIRCH, DAMSON          GORSE   — DAMSON, HOLLY
BIRCH  — ALDER, CEDAR, ELDER    HOLLY   — ELDER, GORSE, IVY
CEDAR  — BIRCH, FIRTH           IVY     — FIRTH, HOLLY
DAMSON — ALDER, ELDER, GORSE
ELDER  — BIRCH, DAMSON, FIRTH, HOLLY    JUNIPER — KELD
FIRTH  — CEDAR, ELDER, IVY              KELD    — JUNIPER
```

Nine cairns three by three on the open fell, plus **Juniper and Keld on the far
side of a river with no crossing**. They are not a mistake in the data — they are
the unreachable case, and a route to them has to come back `None` rather than
zero or an empty list.

## Requirements

1. `steps_from(paths, start)` returns the distance to every cairn reachable from
   `start`, and omits the ones that are not.
2. `route_spread(paths, start, finish)` returns the number of quickest routes and
   the cairns lying on at least one of them.
3. An unreachable finish returns `None`, not an empty answer.
4. `start == finish` is one route over one cairn.
5. The spotter list is in a stable order, so two runs agree.

## Constraints

- **Two searches, not one.** One from the start, one from the finish. Trying to
  count routes inside a single search is possible and much harder to get right;
  name it as the rejected alternative.
- **The membership test is arithmetic, not search.** `from_start[c] +
  from_finish[c] == shortest` and nothing else. If you find yourself walking the
  graph again to decide, you have missed the point of running the second search.
- **Counting routes needs the count carried along**, level by level: a cairn's
  route count is the sum of the counts of the cairns one step closer to the
  start. It is not the number of neighbours.
- **Unreachable is a real answer.** Juniper and Keld exist and are not reachable,
  and the two searches must both simply not mention them.
- **The graph is undirected here**, but the code should not assume it — the
  second search walks the same dictionary, so an undirected map is what makes
  running it "from the finish" meaningful at all. Say so.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python problem-04-cairn-routes-solution.py
ALDER to IVY: 6 quickest routes over 9 cairns
  spotters at: ALDER, BIRCH, CEDAR, DAMSON, ELDER, FIRTH, GORSE, HOLLY, IVY
ALDER to FIRTH: 3 quickest routes over 6 cairns
  spotters at: ALDER, BIRCH, CEDAR, DAMSON, ELDER, FIRTH
ALDER to ALDER: 1 quickest routes over 1 cairns
  spotters at: ALDER
ALDER to KELD: None
All checks passed.
```

Alder to Firth has **three** quickest routes across **six** cairns. Six of nine
cairns are on some shortest route — which is the finding the team wants, because
it means spotters cover two thirds of the fell and the remaining three cairns can
be left alone.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: two searches, and the one-line test that reads the answer out
   of them.
3. Write `steps_from` and check it by hand on Alder — three cairns at distance 1,
   and so on.
4. Run it from both ends and write down `shortest = from_start[finish]`.
5. Apply the arithmetic test to every cairn. Check by hand that a cairn you
   expect to be excluded really is.
6. Add the route count, level by level, and check it against a hand enumeration
   of the three Alder-to-Firth routes.
7. Handle the unreachable case and `start == finish`, then write the FRAME pass.

## The Solution

```python
"""problem-04-cairn-routes-solution.py — every shortest way across the fell.

A mountain rescue team keeps a map of cairns and the paths between them.
Before a search they want two things about the quickest way from one cairn to
another: how many different quickest ways there are, and which cairns lie on
at least one of them. The second list is where they post spotters.

One BFS from each end answers both. A cairn is on a quickest route exactly
when its distance from one end plus its distance from the other adds up to
the length of the whole route.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# Nine cairns on the open fell, laid out three by three, plus two on the far
# side of a river with no crossing.
PATHS: dict[str, list[str]] = {
    "ALDER": ["BIRCH", "DAMSON"],
    "BIRCH": ["ALDER", "CEDAR", "ELDER"],
    "CEDAR": ["BIRCH", "FIRTH"],
    "DAMSON": ["ALDER", "ELDER", "GORSE"],
    "ELDER": ["BIRCH", "DAMSON", "FIRTH", "HOLLY"],
    "FIRTH": ["CEDAR", "ELDER", "IVY"],
    "GORSE": ["DAMSON", "HOLLY"],
    "HOLLY": ["ELDER", "GORSE", "IVY"],
    "IVY": ["FIRTH", "HOLLY"],
    "JUNIPER": ["KELD"],
    "KELD": ["JUNIPER"],
}


# ---- Your task ----
def steps_from(paths: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return the path count from `start` to every cairn it can reach.

    Args:
        paths: The map. Each cairn maps to the cairns a path joins it to.
        start: The cairn to measure from.

    Returns:
        A dict mapping each reachable cairn to its path count. `start` maps
        to 0. Cairns on the far side of the river are simply absent.
    """
    steps = {start: 0}
    queue = deque([start])
    while queue:
        cairn = queue.popleft()
        for neighbour in paths.get(cairn, ()):
            if neighbour not in steps:
                steps[neighbour] = steps[cairn] + 1
                queue.append(neighbour)
    return steps


def route_spread(
    paths: dict[str, list[str]], start: str, finish: str
) -> tuple[int, list[str]] | None:
    """Return how many quickest routes there are, and which cairns they use.

    Args:
        paths: The map.
        start: The cairn the team sets off from.
        finish: The cairn they are heading for.

    Returns:
        A pair: the number of different quickest routes, and every cairn
        lying on at least one of them, sorted A to Z. When `start` and
        `finish` are the same cairn there is one route of no steps and it
        uses that cairn alone. None when no path joins the two.

    Raises:
        KeyError: If either cairn is missing from the map.
    """
    for role, cairn in (("start", start), ("finish", finish)):
        if cairn not in paths:
            raise KeyError(f"{role} cairn {cairn!r} is not on the map")

    from_start = steps_from(paths, start)
    if finish not in from_start:
        return None
    from_finish = steps_from(paths, finish)
    length = from_start[finish]

    routes = {start: 1}
    queue = deque([start])
    seen = {start}
    while queue:
        cairn = queue.popleft()
        for neighbour in paths[cairn]:
            if from_start[neighbour] != from_start[cairn] + 1:
                continue
            routes[neighbour] = routes.get(neighbour, 0) + routes[cairn]
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)

    on_route = sorted(
        cairn
        for cairn, out in from_start.items()
        if out + from_finish.get(cairn, length + 1) == length
    )
    return routes[finish], on_route


# ---- Self-check ----
if __name__ == "__main__":
    for start, finish in (("ALDER", "IVY"), ("ALDER", "FIRTH"), ("ALDER", "ALDER")):
        spread = route_spread(PATHS, start, finish)
        print(f"{start} to {finish}: {spread[0]} quickest routes over {len(spread[1])} cairns")
        print(f"  spotters at: {', '.join(spread[1])}")
    print(f"ALDER to KELD: {route_spread(PATHS, 'ALDER', 'KELD')}")

    # Corner to opposite corner on a three-by-three lattice: four steps, and
    # every one of the six orders of two easts and two souths is quickest.
    assert route_spread(PATHS, "ALDER", "IVY") == (
        6,
        [
            "ALDER",
            "BIRCH",
            "CEDAR",
            "DAMSON",
            "ELDER",
            "FIRTH",
            "GORSE",
            "HOLLY",
            "IVY",
        ],
    )

    # Three steps to FIRTH, three ways to order them, and the three cairns
    # in the far corner are not on any of them.
    count, spotters = route_spread(PATHS, "ALDER", "FIRTH")
    assert count == 3
    assert spotters == ["ALDER", "BIRCH", "CEDAR", "DAMSON", "ELDER", "FIRTH"]
    assert "GORSE" not in spotters and "HOLLY" not in spotters

    # Standing still is one route over one cairn.
    assert route_spread(PATHS, "ALDER", "ALDER") == (1, ["ALDER"])
    # Neighbours: one route, two cairns.
    assert route_spread(PATHS, "ALDER", "BIRCH") == (1, ["ALDER", "BIRCH"])
    # The river has no crossing.
    assert route_spread(PATHS, "ALDER", "KELD") is None

    try:
        route_spread(PATHS, "ALDER", "LARCH")
    except KeyError as error:
        assert "is not on the map" in str(error)
    else:
        raise AssertionError("expected KeyError")

    print("All checks passed.")
```

The route count and the spotter list come out of the same two distance maps. That
is worth stating explicitly in the write-up: the expensive part ran twice, total,
and both answers are reads off the result rather than further searching.

## Download and run

Download the solution beside this page and run it:

```bash
python problem-04-cairn-routes-solution.py
```

No third-party packages, no arguments, no input. It prints the three cases and
then `All checks passed.`

## Common bugs to catch

- **Testing `<=` instead of `==`.** Symptom: every cairn is a spotter. The sum is
  never less than the shortest route, so `<=` is the same as "always".
- **Counting neighbours instead of routes.** Symptom: a plausible number that is
  wrong as soon as two routes merge and split again.
- **One search, and counting inside it.** Symptom: correct on a fell with no
  branching and wrong on this one.
- **Returning an empty list for Juniper.** Symptom: "no spotters needed", which
  reads as an answer and is not one. `None` says unreachable.
- **A spotter list built from a set.** Symptom: a different order every run, and a
  test that passes intermittently.
- **`start == finish` returning zero routes.** Symptom: off by one on the
  degenerate case. Standing still is one route.

## Acceptance checklist

- [ ] Alder to Firth is 3 quickest routes over 6 cairns.
- [ ] Alder to Alder is 1 route over 1 cairn.
- [ ] Alder to Keld returns `None`.
- [ ] `steps_from` omits unreachable cairns rather than giving them a distance.
- [ ] The spotter list is in a stable order across runs.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report which single cairn, if a spotter were placed there alone, would cover
  the most quickest routes. It is a count over the same two maps.
- Add the river crossing and re-run. Two cairns join the fell and the numbers
  change; predict them before running it.
- Return the routes themselves rather than the count. It needs a parent map and
  it grows fast — which is the reason the team asked for a count and a list in
  the first place.
