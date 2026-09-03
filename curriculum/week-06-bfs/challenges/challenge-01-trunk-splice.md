# Challenge 1 — Trunk Splice

> **Topic:** searching from both ends, and the arithmetic that says whether a node is on a shortest route
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Hard
> **Target time:** 75 minutes
> **Why this one:** one search answers "how far". Two searches, one from each end, answer a whole family of questions one search cannot touch — which nodes are on a shortest route, where the middle is, what would happen if a node were removed. The identity `distance_from_west + distance_from_east == route_length` is the entire idea, it is two lines of code, and almost nobody derives it under pressure without having met it first.

## The Brief

A telephone network is a set of street cabinets with trunk cables between
them. Trunks carry both ways: if a trunk joins ABBOT to BEDE, then it joins
BEDE to ABBOT.

There is a fault somewhere between the west end and the east end. A crew is
going to trace it, and tracing takes a whole day if you start at one end and
walk. So they do the sensible thing: they cut in at the **middle** of the
route, test both ways from there, and throw away half the network in one
morning.

Your job is to tell them two things: how long the shortest route is, and
which cabinet is at its middle.

"The middle" needs pinning down, because a route of three hops has no exact
centre. Here is the rule, and it is chosen so two crews reading the same map
pick the same cabinet:

> The midpoint is a cabinet that sits `hops // 2` trunks from the **west**
> end and the remaining `hops - hops // 2` from the **east** end, on some
> shortest route. Where several cabinets qualify, take the earlier name A to
> Z.

Two consequences worth saying out loud before you write anything.

**On an odd route, swapping the ends changes the answer.** Three hops means
`3 // 2 == 1`, so the midpoint is one hop from whichever end you called west.
Call the other end west and you get a different cabinet. That is not a bug —
it is what "the middle of an odd number of steps" means, and the spec names
which end the rounding favours so that the answer is at least *decided*.

**On an even route it does not.** Four hops puts the midpoint two from each
end, and two from each end is the same set of cabinets whichever way round
you ask.

The rest of the contract:

- `trunk_splice` returns a `Splice(hops, midpoint)`, or `None` when no run of
  trunks joins the two ends. Not `-1`, not an exception: two cabinets on
  separate islands is an ordinary state for a network to be in.
- The two ends being the same cabinet is a route of `0` hops, and that
  cabinet is its own midpoint.
- A cabinet missing from the map raises `ValueError`, and the message says
  which end was wrong.
- `on_a_shortest_route` returns every cabinet lying on at least one shortest
  route, sorted. Empty list when the ends are not joined.

## Starter

Create `challenge-01-trunk-splice.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""challenge-01-trunk-splice.py — where to cut a trunk cable in half.

A telephone trunk network of street cabinets. A fault has to be traced from
the west end to the east end, and the crew wants to start at the cabinet in
the middle of the shortest route: whichever cabinet sits exactly half the
hops from the west end and the rest of the way to the east end.

Two searches do it. One from each end. A cabinet is on some shortest route
exactly when its two distances add up to the length of the whole route.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Cabinets and the trunks between them. Trunks carry both ways.
TRUNKS: dict[str, list[str]] = {
    "ABBOT": ["BEDE", "CULVER"],
    "BEDE": ["ABBOT", "DRAYTON", "ELMET"],
    "CULVER": ["ABBOT", "ELMET", "FENWICK"],
    "DRAYTON": ["BEDE", "GARROW"],
    "ELMET": ["BEDE", "CULVER", "GARROW", "HORNBY"],
    "FENWICK": ["CULVER", "HORNBY"],
    "GARROW": ["DRAYTON", "ELMET", "IVEGATE"],
    "HORNBY": ["ELMET", "FENWICK", "IVEGATE"],
    "IVEGATE": ["GARROW", "HORNBY"],
    "KEELBY": ["LOWTHER"],
    "LOWTHER": ["KEELBY"],
}


class Splice(NamedTuple):
    """Where to cut, and how long the route is."""

    hops: int
    midpoint: str


# ---- Your task ----
def hops_from(trunks: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return the trunk count from `start` to every cabinet it can reach.

    Args:
        trunks: The trunk map. Each cabinet maps to the cabinets it is
            joined to.
        start: The cabinet to measure from.

    Returns:
        A dict mapping each reachable cabinet to its trunk count. `start`
        maps to 0. Cabinets on another island of the network are absent.
    """
    # TODO: the plain walk from Exercise 4, with the dict as the reached set
    ...


def trunk_splice(trunks: dict[str, list[str]], west: str, east: str) -> Splice | None:
    """Return the shortest route's length and the cabinet at its midpoint.

    The midpoint is the cabinet sitting `hops // 2` trunks from `west` and
    the remaining `hops - hops // 2` from `east`, on some shortest route. If
    more than one cabinet qualifies, the earlier name A to Z is chosen, so
    two crews reading the same map pick the same cabinet.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end of the trace.
        east: The cabinet at the east end.

    Returns:
        A `Splice`, or None when no run of trunks joins the two ends. When
        `west` and `east` are the same cabinet the route is 0 hops long and
        that cabinet is its own midpoint.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    # TODO: raise ValueError for either end missing, naming which
    # TODO: walk from west; if east is not in the result, return None
    # TODO: walk from east too; hops is from_west[east]; half is hops // 2
    # TODO: the midpoint is the smallest name whose west distance is `half`
    #       AND whose east distance is `hops - half`
    ...


def on_a_shortest_route(
    trunks: dict[str, list[str]], west: str, east: str
) -> list[str]:
    """Return every cabinet lying on at least one shortest route, sorted.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end.
        east: The cabinet at the east end.

    Returns:
        The cabinets whose two distances add up to the route length, A to Z.
        An empty list when the two ends are not joined.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    # TODO: same two walks; keep every cabinet where west + east == hops
    ...


# ---- Self-check ----
if __name__ == "__main__":
    splice = trunk_splice(TRUNKS, "ABBOT", "IVEGATE")
    print(f"ABBOT to IVEGATE : {splice.hops} hops, splice at {splice.midpoint}")
    print(f"on a shortest route: {', '.join(on_a_shortest_route(TRUNKS, 'ABBOT', 'IVEGATE'))}")
    print(f"ABBOT to KEELBY  : {trunk_splice(TRUNKS, 'ABBOT', 'KEELBY')}")
    print(f"ABBOT to ABBOT   : {trunk_splice(TRUNKS, 'ABBOT', 'ABBOT')}")

    assert splice == Splice(hops=4, midpoint="DRAYTON")
    assert on_a_shortest_route(TRUNKS, "ABBOT", "IVEGATE") == [
        "ABBOT",
        "BEDE",
        "CULVER",
        "DRAYTON",
        "ELMET",
        "FENWICK",
        "GARROW",
        "HORNBY",
        "IVEGATE",
    ]

    # An even route has a true middle, so turning the trace around finds the
    # same cabinet. DRAYTON and ELMET are both two hops from either end;
    # DRAYTON wins because D comes before E.
    assert trunk_splice(TRUNKS, "IVEGATE", "ABBOT") == Splice(4, "DRAYTON")

    # An odd route does not. 3 // 2 == 1, so the midpoint sits one hop from
    # the west end and two from the east — and that depends on which end is
    # called west.
    assert trunk_splice(TRUNKS, "ABBOT", "GARROW") == Splice(3, "BEDE")
    assert trunk_splice(TRUNKS, "GARROW", "ABBOT") == Splice(3, "DRAYTON")

    # No route at all: the second island is not joined to the first.
    assert trunk_splice(TRUNKS, "ABBOT", "KEELBY") is None
    assert on_a_shortest_route(TRUNKS, "ABBOT", "KEELBY") == []

    # A cabinet is its own midpoint over a route of no hops.
    assert trunk_splice(TRUNKS, "ABBOT", "ABBOT") == Splice(0, "ABBOT")
    assert trunk_splice(TRUNKS, "KEELBY", "LOWTHER") == Splice(1, "KEELBY")

    try:
        trunk_splice(TRUNKS, "ABBOT", "MERRION")
    except ValueError as error:
        assert "is not on the trunk map" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("All checks passed.")
```

The one idea you need, and it is worth stopping over.

**A cabinet is on a shortest route exactly when its two distances add up.**
Write `w(c)` for the hops from the west end to cabinet `c`, and `e(c)` for
the hops from the east end. Let `D` be the whole route's length.

Then `w(c) + e(c) >= D` for every cabinet — you cannot get from west to east
via `c` in fewer hops than the shortest route, or the shortest route would be
shorter. And `w(c) + e(c) == D` exactly when going *through* `c` costs no
more than the best route, which is what "`c` is on a shortest route" means.

So the test for "is this cabinet on a shortest route?" is one addition and
one comparison. No path-finding, no backtracking, no storing of routes. Two
searches and a sum.

## Requirements

1. `hops_from` returns a `dict[str, int]` with `start` at `0` and every
   reachable cabinet at its trunk count. Unreachable cabinets are absent.
2. `trunk_splice` returns a `Splice` or `None`.
3. `Splice.hops` is the number of trunks on a shortest route.
4. `Splice.midpoint` is the alphabetically earliest cabinet at exactly
   `hops // 2` from `west` and `hops - hops // 2` from `east`.
5. `trunk_splice(TRUNKS, x, x)` returns `Splice(0, x)` for any cabinet on the
   map.
6. Both public functions raise `ValueError` naming `west` or `east` when that
   end is not on the map.
7. `on_a_shortest_route` returns a sorted list, and `[]` when the two ends
   are not joined.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Run two searches, not one search and a route reconstruction.** You could
  record a `came_from` link at every cabinet, walk it back from the east end
  and read the middle off the route. That finds *one* shortest route and
  cannot answer which cabinets are on *any* of them — and the tie-break then
  depends on which route the search happened to find, which is exactly the
  instability the spec is written to avoid.

- **Do not enumerate the routes.** There can be a great many. On a lattice of
  `n` by `n` cabinets the number of shortest routes across it grows faster
  than any polynomial, so a program that lists them cannot finish on a real
  network. The two-distance test never touches a route at all.

- **Compute the midpoint with `min`, not by sorting the candidates.** One
  pass holding the best so far, rather than ordering everything to read the
  first.

- **Reach for `from_east.get(cabinet)` rather than `from_east[cabinet]`.**
  On a connected network every cabinet the west search reached is also
  reachable from the east, so the lookup would succeed — but only because the
  trunks run both ways, which is a property of *this* map and not something
  the function is told. `.get` keeps the function honest and costs nothing.

- **Check the ends before searching.** A missing cabinet is a broken
  question, and answering `None` to it would tell the crew "no route" when
  the truth is "you typed it wrong". Those are different problems with
  different fixes.

- **`hops // 2`, not `hops / 2`.** `/` gives a float, and `w(c) == 1.5` is
  never true for any cabinet, so the midpoint search silently finds nothing
  and `min` raises on an empty sequence. Integer division is not a
  micro-optimisation here; it is the difference between working and not.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
ABBOT to IVEGATE : 4 hops, splice at DRAYTON
on a shortest route: ABBOT, BEDE, CULVER, DRAYTON, ELMET, FENWICK, GARROW, HORNBY, IVEGATE
ABBOT to KEELBY  : None
ABBOT to ABBOT   : Splice(hops=0, midpoint='ABBOT')
All checks passed.
```

Four hops from ABBOT to IVEGATE, and every one of the nine cabinets on the
main island is on some shortest route. That is worth a second look, because
it is not obvious: the network is dense enough that there is no cabinet you
can leave out of every shortest route. On a sparser map the list would be
much shorter, and the cabinets *missing* from it are the ones a crew can
safely ignore.

DRAYTON is the splice point. So is ELMET — both sit two hops from ABBOT and
two from IVEGATE — and DRAYTON is named because D comes before E. Nothing
about the search decides that. The spec does.

The `None` on line three is a real `None`, printed as the word. The crew
reading that report needs to know the two ends are not joined at all, which
is a different day's work from a long route.

## Steps

1. Create the file, paste the starter, and run it. It fails immediately.
2. Write `hops_from` first — it is Exercise 4's walk with nothing added — and
   check it by hand. `hops_from(TRUNKS, "ABBOT")` should have nine entries
   and no KEELBY.
3. Print `hops_from(TRUNKS, "ABBOT")` and `hops_from(TRUNKS, "IVEGATE")` side
   by side, then add the pairs up by eye. Every sum should be 4 or more, and
   the ones equal to 4 are the answer to `on_a_shortest_route`. Confirm that
   before you write a line of it.
4. Write `on_a_shortest_route`. It is one comprehension over one of the two
   dicts.
5. Write `trunk_splice`. The midpoint condition is two equalities joined by
   `and` — resist the urge to combine them into one, because
   `w + e == hops and w == half` is the same thing and reads worse.
6. Get the odd-route asserts passing. If both directions give you the same
   cabinet on a three-hop route, your `half` is being computed from the wrong
   end.
7. Handle the `None` and the same-cabinet cases. Both should need no special
   code beyond the early return for "east not reached".
8. When `All checks passed.` prints, try `trunk_splice(TRUNKS, "KEELBY",
   "LOWTHER")`. One hop, `half` is 0, and the midpoint is the west end
   itself. Convince yourself that is right rather than a bug.

## The Solution

```python
"""challenge-01-trunk-splice-solution.py — where to cut a trunk cable in half.

A telephone trunk network of street cabinets. A fault has to be traced from
the west end to the east end, and the crew wants to start at the cabinet in
the middle of the shortest route: whichever cabinet sits exactly half the
hops from the west end and the rest of the way to the east end.

Two searches do it. One from each end. A cabinet is on some shortest route
exactly when its two distances add up to the length of the whole route.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Cabinets and the trunks between them. Trunks carry both ways.
TRUNKS: dict[str, list[str]] = {
    "ABBOT": ["BEDE", "CULVER"],
    "BEDE": ["ABBOT", "DRAYTON", "ELMET"],
    "CULVER": ["ABBOT", "ELMET", "FENWICK"],
    "DRAYTON": ["BEDE", "GARROW"],
    "ELMET": ["BEDE", "CULVER", "GARROW", "HORNBY"],
    "FENWICK": ["CULVER", "HORNBY"],
    "GARROW": ["DRAYTON", "ELMET", "IVEGATE"],
    "HORNBY": ["ELMET", "FENWICK", "IVEGATE"],
    "IVEGATE": ["GARROW", "HORNBY"],
    "KEELBY": ["LOWTHER"],
    "LOWTHER": ["KEELBY"],
}


class Splice(NamedTuple):
    """Where to cut, and how long the route is."""

    hops: int
    midpoint: str


# ---- Your task ----
def hops_from(trunks: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return the trunk count from `start` to every cabinet it can reach.

    Args:
        trunks: The trunk map. Each cabinet maps to the cabinets it is
            joined to.
        start: The cabinet to measure from.

    Returns:
        A dict mapping each reachable cabinet to its trunk count. `start`
        maps to 0. Cabinets on another island of the network are absent.
    """
    hops = {start: 0}
    queue = deque([start])
    while queue:
        cabinet = queue.popleft()
        for neighbour in trunks.get(cabinet, ()):
            if neighbour not in hops:
                hops[neighbour] = hops[cabinet] + 1
                queue.append(neighbour)
    return hops


def trunk_splice(trunks: dict[str, list[str]], west: str, east: str) -> Splice | None:
    """Return the shortest route's length and the cabinet at its midpoint.

    The midpoint is the cabinet sitting `hops // 2` trunks from `west` and
    the remaining `hops - hops // 2` from `east`, on some shortest route. If
    more than one cabinet qualifies, the earlier name A to Z is chosen, so
    two crews reading the same map pick the same cabinet.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end of the trace.
        east: The cabinet at the east end.

    Returns:
        A `Splice`, or None when no run of trunks joins the two ends. When
        `west` and `east` are the same cabinet the route is 0 hops long and
        that cabinet is its own midpoint.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    for name, cabinet in (("west", west), ("east", east)):
        if cabinet not in trunks:
            raise ValueError(f"{name} end {cabinet!r} is not on the trunk map")

    from_west = hops_from(trunks, west)
    if east not in from_west:
        return None
    from_east = hops_from(trunks, east)
    hops = from_west[east]
    half = hops // 2

    midpoint = min(
        cabinet
        for cabinet, west_hops in from_west.items()
        if west_hops == half and from_east.get(cabinet) == hops - half
    )
    return Splice(hops=hops, midpoint=midpoint)


def on_a_shortest_route(
    trunks: dict[str, list[str]], west: str, east: str
) -> list[str]:
    """Return every cabinet lying on at least one shortest route, sorted.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end.
        east: The cabinet at the east end.

    Returns:
        The cabinets whose two distances add up to the route length, A to Z.
        An empty list when the two ends are not joined.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    for name, cabinet in (("west", west), ("east", east)):
        if cabinet not in trunks:
            raise ValueError(f"{name} end {cabinet!r} is not on the trunk map")

    from_west = hops_from(trunks, west)
    if east not in from_west:
        return []
    from_east = hops_from(trunks, east)
    hops = from_west[east]
    return sorted(
        cabinet
        for cabinet, west_hops in from_west.items()
        if west_hops + from_east.get(cabinet, hops + 1) == hops
    )


# ---- Self-check ----
if __name__ == "__main__":
    splice = trunk_splice(TRUNKS, "ABBOT", "IVEGATE")
    print(f"ABBOT to IVEGATE : {splice.hops} hops, splice at {splice.midpoint}")
    print(f"on a shortest route: {', '.join(on_a_shortest_route(TRUNKS, 'ABBOT', 'IVEGATE'))}")
    print(f"ABBOT to KEELBY  : {trunk_splice(TRUNKS, 'ABBOT', 'KEELBY')}")
    print(f"ABBOT to ABBOT   : {trunk_splice(TRUNKS, 'ABBOT', 'ABBOT')}")

    assert splice == Splice(hops=4, midpoint="DRAYTON")
    assert on_a_shortest_route(TRUNKS, "ABBOT", "IVEGATE") == [
        "ABBOT",
        "BEDE",
        "CULVER",
        "DRAYTON",
        "ELMET",
        "FENWICK",
        "GARROW",
        "HORNBY",
        "IVEGATE",
    ]

    # An even route has a true middle, so turning the trace around finds the
    # same cabinet. DRAYTON and ELMET are both two hops from either end;
    # DRAYTON wins because D comes before E.
    assert trunk_splice(TRUNKS, "IVEGATE", "ABBOT") == Splice(4, "DRAYTON")

    # An odd route does not. 3 // 2 == 1, so the midpoint sits one hop from
    # the west end and two from the east — and that depends on which end is
    # called west.
    assert trunk_splice(TRUNKS, "ABBOT", "GARROW") == Splice(3, "BEDE")
    assert trunk_splice(TRUNKS, "GARROW", "ABBOT") == Splice(3, "DRAYTON")

    # No route at all: the second island is not joined to the first.
    assert trunk_splice(TRUNKS, "ABBOT", "KEELBY") is None
    assert on_a_shortest_route(TRUNKS, "ABBOT", "KEELBY") == []

    # A cabinet is its own midpoint over a route of no hops.
    assert trunk_splice(TRUNKS, "ABBOT", "ABBOT") == Splice(0, "ABBOT")
    assert trunk_splice(TRUNKS, "KEELBY", "LOWTHER") == Splice(1, "KEELBY")

    try:
        trunk_splice(TRUNKS, "ABBOT", "MERRION")
    except ValueError as error:
        assert "is not on the trunk map" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("All checks passed.")
```

**Two dictionaries, and everything else is arithmetic.**

```python
from_west = hops_from(trunks, west)
from_east = hops_from(trunks, east)
hops = from_west[east]
```

After those three lines you know, for every cabinet, how far it is from each
end and how long the whole route is. No routes have been stored, none have
been enumerated, and nothing that follows needs to search again.

**The midpoint condition is the spec, transcribed.**

```python
if west_hops == half and from_east.get(cabinet) == hops - half
```

Read the two halves against the brief: *`hops // 2` trunks from the west end*
and *the remaining `hops - hops // 2` from the east end*. The second test is
what makes it a point on a shortest route rather than merely a cabinet at the
right distance from one end — a cabinet can be two hops west of ABBOT and
five hops from IVEGATE, and that cabinet is on no shortest route at all.

**Why the east check cannot be dropped.** It is tempting: surely anything
`half` hops from the west and on the route is fine? But "on the route" is
precisely what the east distance establishes. Take the test away and the
midpoint can be a cabinet down a dead end that happens to be the right
distance from one side. The two-distance sum is the only cheap way to know
you are still on a shortest route, and it is why this problem needs two
searches rather than one.

**`min` over a generator does the tie-break and the search in one pass.**

```python
midpoint = min(
    cabinet
    for cabinet, west_hops in from_west.items()
    if west_hops == half and from_east.get(cabinet) == hops - half
)
```

There is no list built. `min` pulls candidates one at a time and holds the
smallest name it has seen. On this map that is DRAYTON and ELMET, and D wins.

**The two early exits carry the whole edge-case burden.** `east not in
from_west` is the no-route case, and it is checked before the second search
so an unconnected pair costs one walk instead of two. The same-cabinet case
needs nothing at all: `hops` is 0, `half` is 0, and the only cabinet at zero
hops from both ends is the cabinet itself.

**The `for name, cabinet in (("west", west), ("east", east))` guard.**
Writing the check once and running it twice keeps the two messages
identical in shape and different in content. Two copy-pasted blocks stay in
step until the first time somebody edits one of them.

**A word on what this is not.** A true bidirectional search advances the two
frontiers alternately and stops the instant they touch, which visits far
fewer cabinets on a large network. That is the right tool when you want only
`hops` and the network is enormous. It is the *wrong* tool here, because the
answer depends on distances to cabinets the meeting-in-the-middle version
never settles. Two complete searches cost more and tell you more. Being able
to say which of those you need is the senior half of this problem.

## Download and run

Download
[challenge-01-trunk-splice-solution.py](./challenge-01-trunk-splice-solution.py)
and run it:

```bash
python challenge-01-trunk-splice-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-01-trunk-splice.py`.

## Common bugs to catch

- **`ValueError: min() iterable argument is empty`.**

  ```text
  Traceback (most recent call last):
      m = min(x for x in d if False)
  ValueError: min() iterable argument is empty
  ```

  Nothing matched your midpoint condition. Two usual causes: you used
  `hops / 2` and are comparing an integer to `2.0`, or your east-side test
  says `== half` when it should say `== hops - half`. Print the two dicts and
  find a cabinet by hand that ought to qualify.

- **The odd-route asserts both give the same cabinet.** You computed `half`
  from the east distance, or you tested `from_east[cabinet] == half` as well.
  On an even route that is the same condition and it passes; on an odd one it
  cannot ever be satisfied, or it picks from the wrong side.

- **`on_a_shortest_route` returns every cabinet on the island.** You wrote
  `>=` instead of `==`. Every cabinet satisfies `w + e >= D`; only the ones
  on a shortest route satisfy equality.

- **`KeyError: 'KEELBY'`.**

  ```text
  Traceback (most recent call last):
      print(hops["b"])
          ~~~~^^^^^
  KeyError: 'b'
  ```

  You read `from_east[cabinet]` for a cabinet the east search never reached.
  With trunks running both ways it cannot happen on a connected pair — but
  swap in a one-way map and it will. `.get` with a default that can never
  equal the target is the safe form, which is why the solution passes
  `hops + 1`.

- **`trunk_splice(TRUNKS, "ABBOT", "KEELBY")` raises instead of returning
  `None`.** You looked up `from_west[east]` before checking membership.
  Check first, then read.

- **`AttributeError: 'list' object has no attribute 'popleft'`.**

  ```text
  Traceback (most recent call last):
      queue.popleft()
      ^^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  The queue in `hops_from` is a list. Exercise 4 has the numbers.

- **The same-cabinet case returns `None`.** You special-cased it with an
  early `return None` for "no hops", or your loop never runs because the
  queue is seeded empty. `Splice(0, west)` should fall out of the general
  code with nothing added.

## Under the hood

<details>
<summary>Under the hood — why the two-distance identity is true, and what else it unlocks</summary>

**The proof, in full, and it is short.**

Write `w(c)` for the shortest number of trunks from the west end to `c`, and
`e(c)` for the shortest from `c` to the east end. Let `D = w(east)`.

*Lower bound.* Any route from west to east through `c` has at least `w(c)`
trunks to reach `c` and at least `e(c)` after it, so it has at least
`w(c) + e(c)` trunks. It is also at least `D` long, since `D` is the shortest
of all west-to-east routes. So `w(c) + e(c) >= D`, always.

*The equality case.* Suppose `w(c) + e(c) == D`. Take a shortest route from
west to `c` and a shortest route from `c` to east, and join them. The result
is a west-to-east route of exactly `D` trunks — a shortest one — and `c` is
on it. Conversely, if `c` is on some shortest route, then that route splits
at `c` into a west part of at least `w(c)` and an east part of at least
`e(c)`, and the two together are exactly `D`, which forces both parts to be
exactly minimal.

So: **`c` is on a shortest route if and only if `w(c) + e(c) == D`.** Two
dictionaries and one addition.

**Cost.** Two searches over a network of `C` cabinets and `T` trunks is
`O(C + T)` — the constant is two, and constants do not appear in the
notation. Memory is `O(C)` for the two dictionaries. Compare against
enumerating routes: the number of shortest routes across an `n × n` lattice
is the central binomial coefficient, which is about `4ⁿ / √n`. For a
twenty-by-twenty lattice that is over a hundred billion. The identity turns
an impossible enumeration into a linear scan.

**What else the two dictionaries buy you.** Once you have `w` and `e`:

- *How many shortest routes are there?* Count them with a second pass in
  distance order — Homework Problem 4 does exactly this.
- *Which cabinets, if they failed, would lengthen the route?* The ones on
  **every** shortest route. A cabinet is on all of them if it is the only one
  at its west distance among the on-route set.
- *Is cabinet `c` a detour, and by how much?* `w(c) + e(c) - D` is the extra
  cost of routing through it. Zero means free.
- *What is the network's diameter through this pair?* Not directly, but the
  same two-search trick applied to every pair gives it in `O(C × (C + T))`.

All four are questions a single search cannot answer, and none of them needs
a route to be stored.

**Where the true bidirectional search belongs.** If all you want is `D`, and
the network is large with a moderate branching factor, advancing both
frontiers a level at a time and stopping when they touch visits roughly the
square root of the cabinets a single search would. The catch is that it
settles distances only for the cabinets it reached before the meeting, so
`w(c)` and `e(c)` are unknown for most of the network — and every question in
the list above needs them. Pick the meeting-in-the-middle version when the
answer is one number; pick two full searches when the answer is about the
cabinets.

</details>

## Acceptance checklist

- [ ] `python challenge-01-trunk-splice.py` prints four lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] `hops_from` is called exactly twice per public call, and never inside a
      loop.
- [ ] No routes are stored and none are enumerated anywhere in the file.
- [ ] `hops // 2`, not `hops / 2`.
- [ ] Both directions of a three-hop trace give different midpoints, and you
      can say why.
- [ ] `trunk_splice(TRUNKS, "ABBOT", "KEELBY")` returns `None` without
      raising.
- [ ] `trunk_splice(TRUNKS, "ABBOT", "MERRION")` raises `ValueError` naming
      the east end.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 challenge 1: trunk splice`.

## Stretch

- **Find the cabinets on *every* shortest route.** Those are the ones a
  failure would genuinely lengthen the trace, and they are the on-route
  cabinets that are alone at their west distance.

  ```python
  def unavoidable(trunks: dict[str, list[str]], west: str, east: str) -> list[str]:
      """Return the cabinets every shortest route has to pass through."""
      route_set = on_a_shortest_route(trunks, west, east)
      if not route_set:
          return []
      from_west = hops_from(trunks, west)
      at_depth: dict[int, list[str]] = {}
      for cabinet in route_set:
          at_depth.setdefault(from_west[cabinet], []).append(cabinet)
      return sorted(only[0] for only in at_depth.values() if len(only) == 1)
  ```

  ```text
  ['ABBOT', 'IVEGATE']
  ```

  Only the two ends. Every cabinet in between has an alternative at the same
  depth, which is what a well-built network looks like — and telling the crew
  that is itself useful.

- **Measure the detour cost of every cabinet.** How much longer the trace
  gets if you insist on routing through it.

  ```python
  def detour_cost(trunks: dict[str, list[str]], west: str, east: str) -> dict[str, int]:
      """Return the extra hops incurred by routing through each cabinet."""
      from_west = hops_from(trunks, west)
      from_east = hops_from(trunks, east)
      hops = from_west[east]
      return {
          cabinet: out + from_east[cabinet] - hops
          for cabinet, out in from_west.items()
          if cabinet in from_east
      }
  ```

  ```text
  {'ABBOT': 0, 'BEDE': 0, 'CULVER': 0, 'DRAYTON': 0, 'ELMET': 0,
   'FENWICK': 0, 'GARROW': 0, 'HORNBY': 0, 'IVEGATE': 0}
  ```

  All zeros on this map, because every cabinet is on a shortest route. Add a
  dead-end cabinet — `"MOORGATE": ["FENWICK"]` and `FENWICK` back to it — and
  MOORGATE reports 2, because going out to it and back costs two extra hops.

- **Do it properly bidirectionally, and count what you saved.** Advance both
  frontiers a level at a time, stop when they touch, and count how many
  cabinet distances each version settled.

  ```python
  def meet_in_middle(trunks: dict[str, list[str]], west: str, east: str) -> tuple[int | None, int]:
      """Return the route length and how many cabinets were settled to find it."""
      if west == east:
          return 0, 1
      near, far = {west}, {east}
      settled = {west, east}
      hops = 0
      while near and far:
          hops += 1
          if len(near) > len(far):
              near, far = far, near
          nxt = set()
          for cabinet in near:
              for neighbour in trunks.get(cabinet, ()):
                  if neighbour in far:
                      return hops, len(settled)
                  if neighbour not in settled:
                      settled.add(neighbour)
                      nxt.add(neighbour)
          near = nxt
      return None, len(settled)
  ```

  ```text
  two full searches: 18 cabinet distances settled
  meeting in the middle: (4, 9)
  ```

  Same four hops, half the settling — and no midpoint, because the cabinets
  it never settled are the ones the midpoint test needs. On eleven cabinets
  the saving is a rounding error anyway. Build a lattice of a thousand and
  run it again: that is where the technique earns its name, and where you
  find out it no longer answers the question this page asked.

When your splice point is right, move on to
[Challenge 2 — Tide Gate](./challenge-02-tide-gate.md).
