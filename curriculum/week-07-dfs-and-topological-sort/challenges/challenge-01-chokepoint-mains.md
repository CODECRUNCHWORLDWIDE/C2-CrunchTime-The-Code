# Challenge 1 — Chokepoint Mains

> **Topic:** finding the single pipes a network cannot lose — discovery times and low-links, in one iterative depth-first pass
> **Lecture:** [01 — Recursive DFS](../lecture-notes/01-recursive-dfs.md), then [02 — Iterative DFS](../lecture-notes/02-iterative-dfs.md)
> **Difficulty:** Hard
> **Target time:** 120 minutes
> **Why this one:** it is the first problem this week where the answer is not "walk the graph and collect what you touched". The walk has to *remember something on the way back up*, and that memory — the earliest place this station's side of the network can still reach — is what turns a global question ("would the city split?") into a local test you can run at every step. On top of that, the input is a real maintenance log rather than a tidy edge list, so the obvious way of ignoring the pipe you arrived on is wrong here, and the size of the input rules out recursion. Three separate lessons, one program.

## The Brief

A city's water comes from **pumping stations**, and the stations are joined to
each other by **mains** — big pipes. Water can travel either way along a main,
so a main is a two-way link between two stations.

Here is the question the city's engineers ask every year.

> If exactly one main broke, is there a main whose breaking would leave some
> station with no route at all to a station it can reach today?

A main like that is a **chokepoint**. Picture six houses joined by footbridges.
If two groups of three are each joined in a triangle, and one single bridge
joins the two triangles, then that middle bridge is a chokepoint: lose it and
nobody can get across. None of the six triangle bridges is a chokepoint,
because a triangle always offers you the long way round.

You are given the number of stations and the maintenance log of mains, and you
have to hand back two things:

1. **Every chokepoint**, written in a fixed shape so two people who solve this
   get the same list: each one as `(a, b)` with the smaller station number
   first, and the whole list sorted from smallest to largest.
2. **How many pieces** the network would be in if every chokepoint failed on
   the same bad day. If the city is already in two halves — and networks that
   have grown over a century often are — then that number starts at two, not
   at one.

The log is where this gets interesting. It is a **real** log, written by people
doing maintenance, so two things are true of it that are not true of a tidy
diagram:

- **The same pair can be listed twice.** That is not a typo. It means two
  pipes really were laid side by side between those two stations. And that
  changes the answer: if one of the two breaks, the other still carries the
  water, so neither of them is a chokepoint.
- **Either station can be written first.** `(4, 9)` and `(9, 4)` are the same
  main written by two different people.

There are no mains from a station to itself.

That first bullet is the whole trap of this page, and it is worth saying out
loud now, because you will write the bug otherwise. When your walk arrives at
a station, it must not turn straight round and walk back the way it came —
that would look like a loop when it is not one. The obvious way to prevent it
is to remember *which station you came from* and skip that station. That is
wrong here. When two pipes join the same two stations, the second pipe is a
genuine way back, and skipping by station number throws it away. What you must
remember is **which pipe you came in by**, not which station.

## Starter

Create `challenge-01-chokepoint-mains.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""challenge-01-chokepoint-mains.py — the mains a city cannot lose.

Find every main whose failure would cut some pumping station off from a
station it can reach today, and say how many pieces the network would be in
if all of them failed at once.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import random

UNSEEN = -1


def survey_chokepoints(
    stations: int, mains: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], int]:
    """Find every chokepoint main, and the pieces left if they all failed.

    Args:
        stations: How many pumping stations the network has. They are
            numbered 0 to stations - 1.
        mains: The maintenance log, one (a, b) pair per pipe. The same pair
            may be listed twice, and either station may be written first.

    Returns:
        (chokepoints, pieces). chokepoints holds every chokepoint main,
        each written (a, b) with a < b, the whole list sorted ascending.
        pieces is how many separate networks would be left if every
        chokepoint failed at once.

    Raises:
        ValueError: a main names a station this network does not have.
    """
    # TODO 1: refuse a main that names a station outside 0..stations - 1.
    # TODO 2: stations == 0 is ([], 0), and there is nothing else to do.
    # TODO 3: build the pipe lists. Number every pipe, and store the pipe
    #         number beside the station at each end.
    # TODO 4: walk, iteratively. Each stack entry is (station, the pipe you
    #         came in by, an iterator over that station's untried pipes).
    # TODO 5: on the way back up, carry the lowest reachable time to the
    #         station behind you, and test it for a chokepoint.
    ...


def _piece_count(stations: int, mains: list[tuple[int, int]]) -> int:
    """Count the separate pieces of a network, the plain way.

    This one is written for you. It is an ordinary iterative walk: start
    somewhere unseen, mark everything you can reach, then look for the next
    station nobody has reached yet.

    Args:
        stations: How many pumping stations the network has.
        mains: The pipes that are still standing.

    Returns:
        How many groups of stations there are, where two stations are in the
        same group when water can get from one to the other.
    """
    linked: list[list[int]] = [[] for _ in range(stations)]
    for a, b in mains:
        linked[a].append(b)
        linked[b].append(a)
    seen = [False] * stations
    pieces = 0
    for start in range(stations):
        if seen[start]:
            continue
        pieces += 1
        seen[start] = True
        stack = [start]
        while stack:
            station = stack.pop()
            for nxt in linked[station]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return pieces


def _chokepoints_the_slow_way(
    stations: int, mains: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Find chokepoints by shutting off one main at a time and looking.

    Args:
        stations: How many pumping stations the network has.
        mains: The maintenance log.

    Returns:
        The chokepoints, each (a, b) with a < b, sorted ascending.
    """
    # TODO 6: count the pieces of the whole network. Then, for every main in
    #         turn, count the pieces of the network without that one main.
    #         More pieces than before means that main was a chokepoint.
    ...


def _random_network(rng: random.Random) -> tuple[int, list[tuple[int, int]]]:
    """Build one small network to test with, duplicates and all.

    This one is written for you.

    Args:
        rng: The seeded source of randomness, so every run is the same run.

    Returns:
        (stations, mains) — between one and seven stations, up to ten pipes,
        no pipe from a station to itself.
    """
    stations = rng.randint(1, 7)
    mains: list[tuple[int, int]] = []
    for _ in range(rng.randint(0, 10)):
        a = rng.randrange(stations)
        b = rng.randrange(stations)
        if a != b:
            mains.append((a, b))
    return stations, mains


if __name__ == "__main__":
    assert survey_chokepoints(0, []) == ([], 0)
    assert survey_chokepoints(1, []) == ([], 1)
    assert survey_chokepoints(3, []) == ([], 3)
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3)]) == (
        [(0, 1), (1, 2), (2, 3)],
        4,
    )
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) == ([], 1)
    assert survey_chokepoints(2, [(0, 1), (1, 0)]) == ([], 1)
    assert survey_chokepoints(5, [(0, 1), (2, 3), (3, 4), (4, 2)]) == ([(0, 1)], 3)

    rng = random.Random(20260826)
    for _ in range(300):
        stations, mains = _random_network(rng)
        fast, _ = survey_chokepoints(stations, mains)
        assert fast == _chokepoints_the_slow_way(stations, mains), (stations, mains)

    long_chain = [(i, i + 1) for i in range(49_999)]
    assert survey_chokepoints(50_000, long_chain) == (long_chain, 50_000)

    print("All checks passed.")
```

Four words you need before you start.

**Discovery time.** Give the walk a clock that ticks up by one every time it
stands on a station it has never stood on before. The number on the clock at
that moment is that station's **discovery time**. Station 0 might be time 0,
the next station you step to is time 1, and so on. It is just "how early did I
get here".

**Low-link.** For a station, the **low-link** is the earliest discovery time
that station's side of the walk can still reach — either by carrying on
downwards, or by taking one pipe back up to somewhere the walk has already
been. If a station's low-link is smaller than its own discovery time, there is
a way round. If it is not, there is no way round.

**Back main.** A main that leads to a station the walk has already stood on is
a **back main**. It is the "long way round" made visible: it proves a loop
exists, so it lowers the low-link.

**Bridge.** A chokepoint has a textbook name: it is a **bridge** of the graph.
Say "bridge" out loud in an interview and the interviewer knows exactly what
you are about to compute.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/challenges/challenge-01-chokepoint-mains.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `survey_chokepoints(stations, mains)` returns a tuple
   `(chokepoints, pieces)`.
2. Each chokepoint is a tuple `(a, b)` with `a < b`, and the list is sorted
   ascending. Two people who solve this correctly get identical lists.
3. A main whose pair appears twice in the log is **never** a chokepoint,
   whichever way round each copy is written.
4. `pieces` is the number of separate networks left when every chokepoint has
   failed. It is never smaller than the number of pieces the network is in
   today.
5. `survey_chokepoints(0, [])` returns `([], 0)`.
6. A network with no mains at all is `stations` pieces.
7. A main naming a station outside `0` to `stations - 1` raises `ValueError`,
   and the message names the offending station.
8. The walk is **iterative**. No recursion, and no call to
   `sys.setrecursionlimit`.
9. `_chokepoints_the_slow_way` is written too, and the self-checks run both it
   and the real answer over the seeded random networks and assert they agree.
10. Every function keeps its type hints and its docstring.

## Constraints

- **`0 <= stations <= 50000`, so the walk must be iterative.** Fifty thousand
  stations laid in a straight line is a walk fifty thousand steps deep.
  CPython's default recursion limit is `1000` — check it yourself with
  `sys.getrecursionlimit()` — so a recursive walk dies at about station 995
  with a `RecursionError`, and the real text of that error is in *Common bugs
  to catch* below. Raising the limit with `sys.setrecursionlimit(10 ** 6)` is
  not the fix, and this is worth being precise about: that call raises
  Python's own counter, but each Python frame still sits on the **C stack** the
  interpreter actually runs on, and that stack has a fixed size the call does
  not touch. So you trade a clean `RecursionError` you can catch for a hard
  process crash you cannot — and either way you are betting on an input size
  you do not control. The exercise
  [exercise-02-conveyor-reachability.md](../exercises/exercise-02-conveyor-reachability.md)
  owns this argument in full, with the captured error text; read it if this is
  the first time you have met it. The fix is an explicit stack holding, for
  each station, the pipe you entered it by and an iterator over its remaining
  pipes.

- **`0 <= len(mains) <= 200000`, so the answer must be `O(V + E)`.** Said in
  words: one look at every station and one look at every main, and then it is
  done. That is roughly 250,000 steps here, which finishes instantly. Now
  price the tempting alternative — pull out one main, re-walk the whole
  network, ask whether it still hangs together, put the main back, repeat.
  That is `O(E * (V + E))`: 200,000 removals times a 250,000-step walk is
  **fifty billion** steps. At even ten million simple steps a second that is
  well over an hour for one answer. You will still write that version, because
  it is the reference implementation the self-checks measure against — but you
  will only ever run it on networks of seven stations.

- **Station numbers are `0` to `stations - 1`, and a main outside that range
  is refused.** A log naming station 7 in a four-station network is not a
  puzzle to solve, it is a broken input, and silently indexing a list with it
  either lands on the wrong station or raises `IndexError` from deep inside
  your walk where the message tells the caller nothing. Refuse it at the door,
  in a message that names the station and the range.

- **No self-loops, so you never have to think about them.** A pipe from a
  station to itself can never be a chokepoint — nothing crosses it — but it
  would need its own line of code in the walk. The log has none, and the
  contract says so, so the walk stays short.

- **Pairs may repeat, and either order is allowed, so the answer must not
  care.** This is not a nuisance clause; it is the point of the page. Handle
  it by numbering the pipes and remembering pipe numbers rather than station
  numbers.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-chokepoint-mains-solution.py
network         chokepoints               pieces
empty city      []                        0
single station  []                        1
no mains at all []                        3
short chain     [(0, 1), (1, 2), (2, 3)]  4
one ring        []                        1
twin mains      []                        1
barbell         [(2, 3)]                  2
already split   [(0, 1)]                  3
random cross-check : 300 networks, fast answer matches the slow one
50000-station chain: 49999 chokepoints, 50000 pieces
out-of-range main  : main (0, 7) names station 7, but the network's stations are 0..3
All checks passed.
```

Read the table from the bottom up, because the last three rows are the ones
that break wrong programs. **twin mains** is two stations joined by two pipes:
no chokepoints, one piece. A program that skips the station it came from
instead of the pipe it came in by prints `[(0, 1)]` and `2` there.
**barbell** is two triangles joined by a single main, and exactly that main is
the chokepoint. **already split** is a network that is in two pieces before
anything breaks — one lone pair and one triangle — so its answer starts from
two and the one chokepoint takes it to three.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python challenge-01-chokepoint-mains.py`. The first assert fails
   immediately, because the stub returns `None`. That is the correct starting
   point.
2. **Frame it.** Write the contract down in your own words before any code:
   in, a station count and a log of pipes; out, a sorted list of pipes and a
   count of pieces. Say out loud what "chokepoint" means without using the
   word graph. Ask the clarifying questions the log forces —
   *can a pair repeat?* yes; *can the order flip?* yes; *is the network
   guaranteed to be in one piece?* no.
3. **Research the constraints.** Fifty thousand stations rules out recursion.
   Two hundred thousand mains rules out removing them one at a time. Write
   both numbers in the margin; they are the two facts that pick the algorithm.
4. Fill in `_chokepoints_the_slow_way` first, using the `_piece_count` you
   were given. It is six lines and it is the definition typed out. Doing it
   first means that from now on you have something to be right *against*.
5. **Assess your options** for the fast answer. The slow one is `O(E * (V +
   E))` and out. Union-find tells you what is connected, but not what is
   critical, because it has no idea in which order things were joined. One
   depth-first walk that remembers a discovery time and a low-link per station
   is `O(V + E)` and is the answer.
6. **Make it, in two sittings.** First write the iterative walk with no
   chokepoint logic at all: push the start, loop while the stack is not empty,
   take the next untried pipe, descend if the far station is unseen, pop when
   the iterator runs dry. Check it visits every station exactly once and
   counts pieces correctly. Only then add the two arrays.
7. Add the clock and the discovery times. Then add the two updates: a back
   main lowers your own low-link to the far station's **discovery time**; a
   pop carries the popped station's low-link up to the station behind it.
8. Add the test. When you pop a station and the station behind it is `behind`,
   the pipe between them is a chokepoint exactly when
   `lowest[station] > reached_at[behind]` — read it as "nothing under here can
   reach as far back as the station behind me, so this pipe is the only way
   in". Strictly greater. `>=` is a different, wrong test.
9. **Examine.** Run the seeded random cross-check. If it disagrees, print the
   network it disagreed on — it will be small enough to draw on paper, which
   is the entire reason the generator makes tiny networks.
10. Last, run the fifty-thousand chain. If you have a recursive version lying
    around, run that too, once, so that you have seen the `RecursionError` with
    your own eyes rather than taking this page's word for it.

## The Solution

```python
"""challenge-01-chokepoint-mains-solution.py — the mains a city cannot lose.

A chokepoint is a water main whose failure would cut some pumping station off
from a station it can reach today. One depth-first walk over the network finds
every one of them: one look at every station and one look at every main, and
then it is done.

The walk is iterative on purpose. Fifty thousand stations laid in a line is
fifty times CPython's default recursion limit, so a recursive version dies
before it answers.

Beside the real answer sits `_chokepoints_the_slow_way`, which pulls out one
main at a time and counts how many pieces the network falls into. It is far
too slow for a real network and it is obviously correct, which is exactly what
a reference implementation is for. The self-checks run both over seeded random
networks and demand that they agree.
"""

from __future__ import annotations

import random
from collections.abc import Iterator

UNSEEN = -1


def survey_chokepoints(
    stations: int, mains: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], int]:
    """Find every chokepoint main, and the pieces left if they all failed.

    Args:
        stations: How many pumping stations the network has. They are
            numbered 0 to stations - 1.
        mains: The maintenance log, one (a, b) pair per pipe. The same pair
            may be listed twice, because two pipes really were laid side by
            side, and either station may be written first.

    Returns:
        (chokepoints, pieces). chokepoints holds every main whose failure
        would cut some station off from a station it can currently reach,
        each written (a, b) with a < b, the whole list sorted ascending.
        pieces is how many separate networks would be left if every
        chokepoint failed at once.

    Raises:
        ValueError: a main names a station this network does not have.
    """
    for a, b in mains:
        for station in (a, b):
            if not 0 <= station < stations:
                if stations == 0:
                    raise ValueError(
                        f"main {(a, b)} names station {station}, "
                        "but the network has no stations"
                    )
                raise ValueError(
                    f"main {(a, b)} names station {station}, "
                    f"but the network's stations are 0..{stations - 1}"
                )
    if stations == 0:
        return [], 0

    # Every pipe gets a number. Both ends of pipe 7 remember that they are
    # pipe 7, which is how a pair listed twice stays two pipes.
    pipes_at: list[list[tuple[int, int]]] = [[] for _ in range(stations)]
    for pipe, (a, b) in enumerate(mains):
        pipes_at[a].append((b, pipe))
        pipes_at[b].append((a, pipe))

    reached_at = [UNSEEN] * stations  # when the walk first stood here
    lowest = [0] * stations  # the earliest time this station's side can reach
    clock = 0
    pieces_today = 0
    chokepoints: list[tuple[int, int]] = []

    for start in range(stations):
        if reached_at[start] != UNSEEN:
            continue
        pieces_today += 1
        reached_at[start] = lowest[start] = clock
        clock += 1
        # Each stack entry is: the station, the pipe we walked in by, and an
        # iterator over the pipes at that station we have not tried yet.
        walk: list[tuple[int, int, Iterator[tuple[int, int]]]] = [
            (start, -1, iter(pipes_at[start]))
        ]
        while walk:
            station, came_in_by, untried = walk[-1]
            went_deeper = False
            for nxt, pipe in untried:
                if pipe == came_in_by:
                    continue  # the one pipe we arrived on, not a way back
                if reached_at[nxt] == UNSEEN:
                    reached_at[nxt] = lowest[nxt] = clock
                    clock += 1
                    walk.append((nxt, pipe, iter(pipes_at[nxt])))
                    went_deeper = True
                    break
                if reached_at[nxt] < lowest[station]:
                    lowest[station] = reached_at[nxt]
            if went_deeper:
                continue
            walk.pop()
            if walk:
                behind = walk[-1][0]
                if lowest[station] < lowest[behind]:
                    lowest[behind] = lowest[station]
                if lowest[station] > reached_at[behind]:
                    ends = (behind, station) if behind < station else (station, behind)
                    chokepoints.append(ends)

    chokepoints.sort()
    # Pulling one chokepoint out splits exactly one piece in two, so the
    # network today plus one piece per chokepoint is the whole answer.
    return chokepoints, pieces_today + len(chokepoints)


def _piece_count(stations: int, mains: list[tuple[int, int]]) -> int:
    """Count the separate pieces of a network, the plain way.

    Args:
        stations: How many pumping stations the network has.
        mains: The pipes that are still standing.

    Returns:
        How many groups of stations there are, where two stations are in the
        same group when water can get from one to the other.
    """
    linked: list[list[int]] = [[] for _ in range(stations)]
    for a, b in mains:
        linked[a].append(b)
        linked[b].append(a)
    seen = [False] * stations
    pieces = 0
    for start in range(stations):
        if seen[start]:
            continue
        pieces += 1
        seen[start] = True
        stack = [start]
        while stack:
            station = stack.pop()
            for nxt in linked[station]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return pieces


def _chokepoints_the_slow_way(
    stations: int, mains: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Find chokepoints by shutting off one main at a time and looking.

    This is the definition typed out. It re-walks the whole network once per
    main, so it is hopeless on a real one — and unarguable on a small one,
    which is why the self-checks measure the fast answer against it.

    Args:
        stations: How many pumping stations the network has.
        mains: The maintenance log.

    Returns:
        The chokepoints, each (a, b) with a < b, sorted ascending.
    """
    whole = _piece_count(stations, mains)
    found: list[tuple[int, int]] = []
    for index, (a, b) in enumerate(mains):
        without = mains[:index] + mains[index + 1 :]
        if _piece_count(stations, without) > whole:
            found.append((a, b) if a < b else (b, a))
    return sorted(found)


def _random_network(rng: random.Random) -> tuple[int, list[tuple[int, int]]]:
    """Build one small network to test with, duplicates and all.

    Args:
        rng: The seeded source of randomness, so every run is the same run.

    Returns:
        (stations, mains) — between one and seven stations, up to ten pipes,
        no pipe from a station to itself.
    """
    stations = rng.randint(1, 7)
    mains: list[tuple[int, int]] = []
    for _ in range(rng.randint(0, 10)):
        a = rng.randrange(stations)
        b = rng.randrange(stations)
        if a != b:
            mains.append((a, b))
    return stations, mains


if __name__ == "__main__":
    cases: list[tuple[str, int, list[tuple[int, int]]]] = [
        ("empty city", 0, []),
        ("single station", 1, []),
        ("no mains at all", 3, []),
        ("short chain", 4, [(0, 1), (1, 2), (2, 3)]),
        ("one ring", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("twin mains", 2, [(0, 1), (1, 0)]),
        ("barbell", 6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]),
        ("already split", 5, [(0, 1), (2, 3), (3, 4), (4, 2)]),
    ]
    print(f"{'network':<16}{'chokepoints':<26}pieces")
    for name, stations, mains in cases:
        chokepoints, pieces = survey_chokepoints(stations, mains)
        print(f"{name:<16}{str(chokepoints):<26}{pieces}")

    assert survey_chokepoints(0, []) == ([], 0)
    assert survey_chokepoints(1, []) == ([], 1)
    assert survey_chokepoints(3, []) == ([], 3)
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3)]) == (
        [(0, 1), (1, 2), (2, 3)],
        4,
    )
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) == ([], 1)
    assert survey_chokepoints(2, [(0, 1), (1, 0)]) == ([], 1)
    assert survey_chokepoints(
        6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]
    ) == ([(2, 3)], 2)
    assert survey_chokepoints(5, [(0, 1), (2, 3), (3, 4), (4, 2)]) == ([(0, 1)], 3)

    rng = random.Random(20260826)
    trials = 300
    for _ in range(trials):
        stations, mains = _random_network(rng)
        fast, pieces = survey_chokepoints(stations, mains)
        slow = _chokepoints_the_slow_way(stations, mains)
        assert fast == slow, (stations, mains, fast, slow)
        standing = [
            (a, b) for a, b in mains if (min(a, b), max(a, b)) not in set(slow)
        ]
        assert pieces == _piece_count(stations, standing), (stations, mains)
    print(f"random cross-check : {trials} networks, fast answer matches the slow one")

    long_chain = [(i, i + 1) for i in range(49_999)]
    chokepoints, pieces = survey_chokepoints(50_000, long_chain)
    assert len(chokepoints) == 49_999
    assert pieces == 50_000
    print(f"50000-station chain: {len(chokepoints)} chokepoints, {pieces} pieces")

    try:
        survey_chokepoints(4, [(0, 1), (0, 7)])
    except ValueError as error:
        print(f"out-of-range main  : {error}")
    else:  # pragma: no cover - the call above always raises
        raise AssertionError("a main outside the station numbers must be refused")

    print("All checks passed.")
```

**Number the pipes, and the duplicate-main problem disappears.** The adjacency
list holds `(far station, pipe number)` rather than a bare station number:

```python
for pipe, (a, b) in enumerate(mains):
    pipes_at[a].append((b, pipe))
    pipes_at[b].append((a, pipe))
```

Now "do not walk straight back the way you came" is `if pipe == came_in_by`,
which skips exactly one pipe — the one you arrived on. When the same pair is
listed twice, the second copy has a different number, so it is not skipped, it
is seen as a back main, it lowers the low-link, and the pair is correctly
reported as no chokepoint at all. The version that writes `if nxt == came_from`
throws both copies away and reports a chokepoint that is not there.

**The clock and the two arrays are the whole algorithm.** `reached_at[station]`
is when the walk first stood there. `lowest[station]` starts equal to it and
only ever goes down. Two updates keep it true. A back main to an already-seen
station pulls it down to that station's *discovery* time,
`reached_at[nxt]` — not that station's low-link, because what you have proved
is that you can reach *that station*, and its own low-link is a claim about a
different part of the walk. And when a station is finished and popped, its
low-link is carried up to the station behind it, because whatever the child
can reach, the parent can reach through the child.

**The chokepoint test is one strict comparison.** After popping `station` back
to `behind`:

```python
if lowest[station] > reached_at[behind]:
```

Everything reachable from `station` was discovered *after* `behind` was. That
means no pipe anywhere under `station` climbs back to `behind` or above it, so
the single pipe you walked down is the only connection, so it is a chokepoint.
Change the `>` to `>=` and the test also fires when the subtree can reach
`behind` itself — which is exactly the case where there *is* a way round — and
you start reporting chokepoints inside rings.

**The stack entry has three parts, and the iterator is the important one.**
`(station, came_in_by, untried)` — and `untried` is an *iterator*, made once
with `iter(pipes_at[nxt])` when the station is pushed. That is what makes the
whole walk `O(V + E)`. Each pipe is handed out by that iterator exactly once
from each end, so the total work across all the resuming and re-resuming is two
passes over the log and no more. If instead you re-looped over
`pipes_at[station]` from the beginning every time you came back to a station,
you would re-examine pipes you had already dealt with, and a station with a
thousand pipes would cost a thousand times more than it should.

**`pieces` is arithmetic, not a second algorithm.** Count the pieces the
network is in today — that is just how many times the outer loop had to start a
fresh walk. Then notice that pulling out one chokepoint splits exactly one
piece into exactly two, by the definition of a chokepoint, and that removing
one chokepoint never turns another one into a non-chokepoint. So the answer is
`pieces_today + len(chokepoints)`, and the seeded cross-check confirms it
against a network that really has had all its chokepoints deleted.

**The slow reference is a testing tool, not cheating.** It is worth being
blunt about this, because it feels like it should be against the rules. It is
not, for two reasons. First, it computes the answer from the *definition* —
"remove it and see whether the network falls apart" — while the fast version
computes it from a clever invariant, so the two programs can only agree by
both being right; there is no shared assumption for a single bug to hide in.
Second, you would never ship it: it is `O(E * (V + E))`, and the constraints
make it useless on real input. That combination — obviously correct, far too
slow — is precisely what a reference implementation is for, and pairing it
with a seeded generator is how anyone sane tests a hand-written low-link
routine. Seeding matters: `random.Random(20260826)` means a failure you see
today is a failure you can still reproduce tomorrow.

## Download and run

Download
[challenge-01-chokepoint-mains-solution.py](./challenge-01-chokepoint-mains-solution.py)
and run it:

```bash
python challenge-01-chokepoint-mains-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-01-chokepoint-mains.py`.

## Common bugs to catch

- **`RecursionError: maximum recursion depth exceeded`.** You wrote the walk
  as a function that calls itself, and then ran the fifty-thousand-station
  chain:

  ```text
  recursion limit: 1000
  Traceback (most recent call last):
    File "chokepoints.py", line 41, in <module>
      print(survey_chokepoints(50_000, chain)[1])
            ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
    File "chokepoints.py", line 35, in survey_chokepoints
      walk(start, -1)
      ~~~~^^^^^^^^^^^
    File "chokepoints.py", line 24, in walk
      walk(nxt, pipe)
      ~~~~^^^^^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Note *995*, not 49,999 — it stopped a thousandth of the way in. The fix is
  the explicit stack, not `sys.setrecursionlimit`; see the Constraints above
  and [exercise-02-conveyor-reachability.md](../exercises/exercise-02-conveyor-reachability.md).

- **`survey_chokepoints(2, [(0, 1), (1, 0)])` returns `([(0, 1)], 2)`.** You
  skipped the station you came from instead of the pipe you came in by:

  ```text
  >>> survey_chokepoints(2, [(0, 1), (1, 0)])
  ([(0, 1)], 2)
  >>> survey_chokepoints(4, [(0, 1), (1, 2), (2, 1), (2, 3)])
  ([(0, 1), (1, 2), (2, 3)], 4)
  ```

  The right answers are `([], 1)` and `([(0, 1), (2, 3)], 3)`. Both copies of
  the doubled pair got thrown away, so the walk never saw the way round, so it
  reported a pipe that has a twin as critical. This is the single most common
  wrong answer on this page, it passes every test that has no doubled pair in
  it, and it is why the `twin mains` row exists.

- **`TypeError: cannot unpack non-iterable int object`.** You built the pipe
  lists holding bare station numbers and then tried to read a pipe number back
  out of them:

  ```text
  Traceback (most recent call last):
    File "chokepoints.py", line 4, in <module>
      for nxt, pipe in untried:
          ^^^^^^^^^
  TypeError: cannot unpack non-iterable int object
  ```

  The adjacency entry has to be the pair `(far station, pipe number)`. If you
  find yourself wanting to recover the pipe number from the two station
  numbers, stop — that is the doubled-pair bug wearing a different hat, since
  the two copies have the same two station numbers and different pipe numbers.

- **A ring reports a chokepoint.** You wrote `>=` where the test is `>`:

  ```text
  >>> survey_chokepoints(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
  ([(0, 1)], 2)
  ```

  Four stations in a ring have no chokepoints at all — you can lose any one
  pipe and still walk round the other way. `lowest[station] == reached_at[behind]`
  means the subtree can climb back to exactly the station behind you, which is
  the definition of a way round, so it must *not* count.

- **The list comes back in walk order.** Every pair is right and the order is
  not, because you returned `chokepoints` without sorting it. The walk emits
  chokepoints as it pops, which is deepest-first, and that order depends on
  which station happened to be listed first in the log. Requirement 2 asks for
  a fixed shape precisely so that this cannot be a matter of taste: sort the
  list, and normalise each pair to `a < b` when you append it.

- **`pieces` is right on connected networks and one too small on split ones.**
  You returned `len(chokepoints) + 1`. That says "the network is one piece
  today", which the `already split` row disproves. Count how many times the
  outer loop starts a fresh walk and add that instead.

- **The random cross-check passes and the barbell fails.** Look at the
  generator before you look at your walk. `_random_network` makes networks of
  at most seven stations, so if your bug needs two rings joined by a single
  pipe to show up, tiny networks may never build one. This is the honest
  limitation of random testing, and the answer is the fixed hand-written cases
  above the loop — the random networks catch the bugs you did not think of,
  and the named cases catch the ones you did.

## Under the hood

<details>
<summary>Under the hood — where low-links come from, and what else they buy you</summary>

**The name.** This is Tarjan's bridge-finding algorithm, from Robert Tarjan's
work on depth-first search in the early 1970s. The same `low` array, computed
the same way, is the engine of three other algorithms you will meet: finding
**articulation points** (stations whose failure splits the network, rather
than mains), finding **strongly connected components** in a directed graph,
and **biconnected components**. If you ever wondered why depth-first search is
treated as more fundamental than breadth-first search despite being no faster,
this is the reason: the depth-first tree has a property breadth-first does not,
and every one of those algorithms leans on it.

**The property.** In an undirected graph, a depth-first walk classifies every
main into exactly two kinds: **tree mains**, the ones you walked down, and
**back mains**, the ones that lead to a station already on your current path.
There is no third kind. In particular there is no "cross main" joining two
branches that have no ancestor relationship — if there were, the walk would
have gone down it when it first arrived, and it would have been a tree main.
That is the fact that makes the whole thing work, because it means a way round
a tree main can only ever be a back main, and a back main is exactly what the
low-link is watching for.

**Why the low-link is enough.** Take the pipe from `behind` down to `station`.
Removing it splits the network if and only if nothing in the part of the walk
below `station` has any other route back to `behind` or higher. "Any other
route" has to end in a back main, by the paragraph above. `lowest[station]` is
the earliest discovery time anything down there can reach. So
`lowest[station] > reached_at[behind]` says "the earliest thing anybody down
there can reach was still discovered after `behind`", which says "nobody down
there can reach `behind` or above it". That is not a heuristic and it is not
approximate — it is an if-and-only-if, which is why the seeded cross-check
against the definition never disagrees.

**The `pieces` count has a name too.** The pieces you are left with after all
the chokepoints fail are the graph's **two-edge-connected components**: the
maximal groups of stations where you would have to cut at least two pipes to
separate any of them. Contract each of those groups to a single point and the
chokepoints between them form a forest — the *bridge tree*. That is a genuinely
useful object: once you have it, questions like "which single pipe would cut
the most customers off" become one pass over a tree instead of a fresh search.

**Iterators as saved state.** The stack entry holds `iter(pipes_at[nxt])`, and
that iterator *is* the "where was I up to" that a recursive version keeps in its
frame. This is the general shape of turning any recursion into a loop: find
what the frame was remembering, and store it on your own stack. Here the frame
remembered three things — which station, which pipe it arrived on, and how far
through the neighbour loop it had got — so the stack entry is a three-tuple.
Nothing about the algorithm changed; only where the bookkeeping lives.

**A note on the C stack.** `sys.setrecursionlimit(10 ** 6)` is a promise Python
cannot keep. The limit it raises is a counter CPython checks; the memory that
actually runs out is the operating system's stack for the interpreter's own C
frames, which is fixed when the process starts and typically around 1 MB on
Windows and 8 MB on Linux. Raise the counter high enough and you do not get a
`RecursionError`, you get a segmentation fault or a Windows access violation:
the process dies with no traceback and no chance to catch anything. Python 3.12
onwards makes many pure-Python calls cheaper in C-stack terms, which changes
how far you get, not whether the cliff exists. Write the loop.

</details>

## Acceptance checklist

- [ ] `python challenge-01-chokepoint-mains.py` prints `All checks passed.`
- [ ] `survey_chokepoints(2, [(0, 1), (1, 0)])` is `([], 1)` — the doubled pair
      is not a chokepoint.
- [ ] `survey_chokepoints(4, [(0, 1), (1, 2), (2, 3), (3, 0)])` is `([], 1)` —
      a ring has none.
- [ ] `survey_chokepoints(5, [(0, 1), (2, 3), (3, 4), (4, 2)])` is
      `([(0, 1)], 3)` — an already-split network starts from two.
- [ ] Every returned pair has the smaller station first, and the list is
      sorted.
- [ ] The fifty-thousand-station chain finishes and returns 49,999
      chokepoints. No `RecursionError`, no `sys.setrecursionlimit`.
- [ ] The seeded random cross-check runs the slow reference and asserts
      agreement.
- [ ] A main naming a station outside the range raises `ValueError` with the
      station in the message.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like
      `Add Week 7 challenge 1: chokepoint mains`.

## Stretch

- **Report the chokepoint that would cut off the most stations.** Each
  chokepoint splits one piece in two, and the number the engineers actually
  care about is the size of the smaller half, because that is who loses their
  water.

  ```python
  def _reachable(stations: int, mains: list[tuple[int, int]], start: int) -> int:
      """How many stations you can get to from start."""
      linked: list[list[int]] = [[] for _ in range(stations)]
      for a, b in mains:
          linked[a].append(b)
          linked[b].append(a)
      seen = {start}
      stack = [start]
      while stack:
          station = stack.pop()
          for nxt in linked[station]:
              if nxt not in seen:
                  seen.add(nxt)
                  stack.append(nxt)
      return len(seen)


  def worst_chokepoint(
      stations: int, mains: list[tuple[int, int]]
  ) -> tuple[tuple[int, int], int] | None:
      """Return the chokepoint cutting off the most stations, and how many."""
      chokepoints, _ = survey_chokepoints(stations, mains)
      if not chokepoints:
          return None
      worst, cut_off = None, -1
      for a, b in chokepoints:
          standing = [m for m in mains if (min(m), max(m)) != (a, b)]
          here = min(
              _reachable(stations, standing, a), _reachable(stations, standing, b)
          )
          if here > cut_off:
              worst, cut_off = (a, b), here
      return worst, cut_off
  ```

  ```text
  barbell     : ((2, 3), 3)
  short chain : ((1, 2), 2)
  ring        : None
  ```

  Written that way it is slow on purpose — it re-walks the network once per
  chokepoint. Now write the linear version: count, in the same pass, how many
  stations finish under each station, and the smaller half of the pipe from
  `behind` down to `station` is exactly that count. Then check the two agree
  over the seeded networks. That is this page's own discipline, applied to your
  own extension.

- **Find articulation stations instead of chokepoint mains.** A **station** is
  an articulation station when its own failure splits the network. It is
  almost the same walk: for a station that is not where a walk started, it is
  an articulation station when some station popped back into it has
  `lowest[child] >= reached_at[station]` — note `>=` here, where the mains
  wanted `>`. Where a walk started is special: it is an articulation station
  when two or more stations were pushed from it directly.

  ```text
  barbell     : [2, 3]
  ring        : []
  short chain : [1, 2]
  ```

  Work out for yourself why the comparison flips, using the definition of the
  low-link. Cutting the *station* also cuts the pipe you arrived on, and that
  is the whole difference. Note the short chain: stations 1 and 2 are
  articulation stations, but the two ends are not — losing an end cuts off
  nobody but itself.

- **Return the pieces themselves, not just how many.** `pieces` is a count;
  the engineers will want the lists. Delete every chokepoint, then group what
  is left.

  ```python
  def pieces_of(stations: int, mains: list[tuple[int, int]]) -> list[list[int]]:
      """The groups of stations left when every chokepoint has failed."""
      chokepoints, _ = survey_chokepoints(stations, mains)
      gone = set(chokepoints)
      standing = [m for m in mains if (min(m), max(m)) not in gone]
      linked: list[list[int]] = [[] for _ in range(stations)]
      for a, b in standing:
          linked[a].append(b)
          linked[b].append(a)
      seen = [False] * stations
      groups: list[list[int]] = []
      for start in range(stations):
          if seen[start]:
              continue
          seen[start] = True
          stack = [start]
          group: list[int] = []
          while stack:
              station = stack.pop()
              group.append(station)
              for nxt in linked[station]:
                  if not seen[nxt]:
                      seen[nxt] = True
                      stack.append(nxt)
          groups.append(sorted(group))
      return groups
  ```

  ```text
  barbell       : [[0, 1, 2], [3, 4, 5]]
  already split : [[0], [1], [2, 3, 4]]
  ```

  Then assert `len(pieces_of(...)) == survey_chokepoints(...)[1]` over the
  seeded networks. Two ways of computing the same number, one of them
  arithmetic and one of them a walk, is a cheap and very effective test.

**Practice elsewhere.** The same pattern appears as
[LeetCode 1192 · Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/)
if you want a judge to run against — ours differs in that it tolerates a pair
listed twice, fixes the shape of the reported pairs instead of accepting any
order, and also asks how many pieces the network falls into.

When your survey is right, the optional stretch is
[Challenge 2 — Consist Reconstruction](./challenge-02-consist-reconstruction.md).
