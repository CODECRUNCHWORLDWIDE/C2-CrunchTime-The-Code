# Challenge 2 — Consist Reconstruction

> **Topic:** deriving an ordering from partial observations, then topologically sorting it — and saying whether the answer is forced or merely possible
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Hard
> **Target time:** 90 minutes
> **Why this one:** the sorting half is Kahn's algorithm, which you already own by now. The hard half is everything around it. You have to notice that the input is not a graph yet and build one; you have to work out which constraints you actually need, because the obvious answer is a hundred times too many; and you have to answer a question most versions of this problem never ask — *is this the only answer?* An order that happens to be legal and an order that is forced are worth very different things to whoever asked you, and telling them apart costs one line of code and a clear head.

## The Brief

A freight train is a line of wagons hooked together, front to back. Railway
people call that line the train's **consist** — the word just means "which
wagons, in which order". Every wagon carries a painted **mark**, a short code
like `HOP-11`, and no two wagons in one train carry the same mark.

A train ran across the country last night. It had one fixed order the whole
way — wagons do not swap places while the train is moving. But no single rail
yard saw the whole thing. A yard sees the part of the train that passes its
window, in the dark, and writes down what it could read.

Each yard files a **sighting**: the marks it did see, written front to back,
with nothing at all where the wagons it could not read would have been. So a
sighting is the true order with gaps in it. It is never *wrong*; it is only
ever *incomplete*.

Here is the job. Given every yard's sighting, rebuild the train.

Think about what one sighting actually tells you. If a yard writes down
`HOP-11`, `BOX-27`, `CAB-09`, then you know `HOP-11` is somewhere in front of
`BOX-27`, and `BOX-27` is somewhere in front of `CAB-09`. You do **not** know
whether anything sat between them — that is what the gaps mean. Put enough
sightings together and the overlaps pin the whole train down.

Or they do not, and that is the second half of the job. Three things can
happen, and your answer says which:

- **`"unique"`** — the sightings pin the train down completely. At every point
  there was exactly one wagon that could come next. This is the answer the
  yardmaster wants.
- **`"ambiguous"`** — more than one train fits everything the yards filed. You
  still hand back a real, legal order, so there is something to work with; the
  verdict is what tells the yardmaster not to trust it. Two wagons that no
  single yard ever saw together are the usual cause: nothing on paper says
  which of them is in front.
- **`"impossible"`** — no train fits. Either two yards contradict each other,
  or one yard's own sighting lists the same mark twice, which cannot happen in
  a train where every wagon appears once. On `"impossible"` you hand back an
  empty order, because there is nothing honest to hand back.

When more than one order fits, you must still be *predictable* about which one
you return, or two people running your program get two different trains. The
rule is: at every step, of all the wagons that could legally come next, take
the **alphabetically smallest mark**.

And one strange-looking case that is not strange at all: a train with no
wagons. No sightings at all, or a couple of blank ones, is an empty train — and
there is exactly one way to arrange no wagons, so the verdict is `"unique"`.

## Starter

Create `challenge-02-consist-reconstruction.py` in your practice repo and paste
this in. Fill in every `TODO`.

```python
"""challenge-02-consist-reconstruction.py — rebuild a train from sightings.

Each rail yard filed the wagons it saw, front to back, with gaps where wagons
it could not read would have been. Put the sightings together, rebuild the
train, and say whether the sightings force that train or merely allow it.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import heapq


def reconstruct_consist(sightings: list[list[str]]) -> tuple[list[str], str]:
    """Rebuild the train's wagon order from the yards' sightings.

    Args:
        sightings: One list per yard, holding the wagon marks that yard saw,
            written front to back. A yard may have seen one wagon, or none.

    Returns:
        (order, verdict). verdict is "unique" when exactly one train fits the
        sightings, "ambiguous" when more than one does, and "impossible" when
        none does. On "impossible" the order is []. On "ambiguous" the order
        is one train that really does fit: at every step the alphabetically
        smallest wagon that could come next.

    Raises:
        ValueError: a sighting holds a wagon mark that is not a non-empty
            string.
    """
    # TODO 1: collect every wagon mark that appears anywhere. A yard that saw
    #         exactly one wagon adds no ordering, but the wagon is still real
    #         and must appear in the order.
    # TODO 2: refuse a mark that is not a non-empty string.
    # TODO 3: a sighting that lists the same mark twice is "impossible".
    # TODO 4: one constraint per NEIGHBOURING pair in each sighting, and no
    #         others. Keep them in a set, not a list.
    # TODO 5: count how many wagons are ahead of each wagon, and start the
    #         ready heap with the ones that have none.
    # TODO 6: pop the smallest ready wagon, release its followers, repeat.
    #         If the heap ever holds more than one wagon, the answer is not
    #         forced.
    # TODO 7: fewer wagons in the order than exist means a loop: "impossible".
    ...


def _constraints_every_pair(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the wasteful way, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        A constraint for every pair of wagons in every sighting, not only the
        neighbouring ones.
    """
    # TODO 8: every wagon against every later wagon in the same sighting.
    ...


def _constraints_neighbours(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the way the answer does, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        One constraint per neighbouring pair in each sighting.
    """
    # TODO 9: zip(sighting, sighting[1:]) walks the neighbouring pairs.
    ...


if __name__ == "__main__":
    assert reconstruct_consist([]) == ([], "unique")
    assert reconstruct_consist([[], []]) == ([], "unique")
    assert reconstruct_consist([["HOP-11"], ["TNK-04"]]) == (
        ["HOP-11", "TNK-04"],
        "ambiguous",
    )
    assert reconstruct_consist(
        [
            ["HOP-11", "BOX-27", "CAB-09"],
            ["HOP-11", "TNK-04", "BOX-27"],
            ["BOX-27", "GON-52", "CAB-09"],
        ]
    ) == (["HOP-11", "TNK-04", "BOX-27", "GON-52", "CAB-09"], "unique")
    assert reconstruct_consist([["FLT-03", "CAB-09"], ["REF-08", "CAB-09"]]) == (
        ["FLT-03", "REF-08", "CAB-09"],
        "ambiguous",
    )
    assert reconstruct_consist([["TNK-04", "BOX-27"], ["BOX-27", "TNK-04"]]) == (
        [],
        "impossible",
    )
    assert reconstruct_consist([["HOP-11", "TNK-04", "HOP-11"]]) == ([], "impossible")

    long_train = [[f"WAG-{number:04d}" for number in range(200)]]
    assert len(_constraints_neighbours(long_train)) == 199
    assert len(_constraints_every_pair(long_train)) == 19_900

    print("All checks passed.")
```

Four words you need before you start.

**Constraint.** One fact of the form "this wagon is in front of that one". It
is written here as the pair `(front, back)`. The whole train is rebuilt from
nothing but a pile of these.

**Ready.** A wagon is **ready** when every wagon known to be in front of it has
already been placed. At the very start, the ready wagons are the ones no
sighting ever put behind anything.

**Kahn's algorithm.** The method from Lecture 3 §4, in one sentence: keep a
pool of ready wagons, take one out and place it, and every time you place a
wagon, tick down the count of wagons still ahead of each of its followers —
when a follower's count hits zero it joins the pool. When the pool empties, if
you placed every wagon you have an order; if you did not, the leftovers are
stuck behind each other in a loop.

**Heap.** A `heapq` is a pool that always hands you the smallest thing in it,
for `log n` work per push and pop rather than the `n` work of scanning a list.
It is how "take the alphabetically smallest ready wagon" costs almost nothing.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/challenges/challenge-02-consist-reconstruction.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `reconstruct_consist(sightings)` returns `(order, verdict)`, and `verdict`
   is exactly one of `"unique"`, `"ambiguous"`, `"impossible"`.
2. Each sighting contributes **one constraint per neighbouring pair** and no
   others.
3. `"impossible"` when the sightings contradict each other, and `"impossible"`
   when any single sighting lists the same mark twice. In both cases the order
   is `[]`.
4. `"ambiguous"` when at any step more than one wagon could legally come next.
   The order returned is still a legal one.
5. `"unique"` when exactly one wagon is ready at every step.
6. When more than one wagon is ready, the alphabetically smallest mark goes
   next — Python's ordinary `<` on strings.
7. `reconstruct_consist([])` returns `([], "unique")`, and so does
   `reconstruct_consist([[], []])`.
8. A wagon seen by a yard that saw nothing else still appears in the order.
9. A mark that is not a non-empty string raises `ValueError` naming the
   sighting it was in.
10. Every function keeps its type hints and its docstring.

## Constraints

- **At most 2,000 wagons and at most 2,000 sightings, together listing at most
  20,000 positions.** Those three numbers exist so that the whole job stays
  linear in what you were actually given: one pass over the listed positions
  to build the constraints, then one pass over the wagons and the constraints
  to place them. A real freight train tops out in the low hundreds of wagons,
  and a yard files one sighting per train, so these bounds are generous rather
  than tight — they are here to tell you what *not* to worry about. Nothing in
  this problem needs a clever data structure, and nothing in it justifies an
  approach whose cost grows faster than the input does.

- **Only neighbouring pairs, which is what keeps that promise.** A sighting of
  `n` wagons has `n - 1` neighbouring pairs and `n * (n - 1) / 2` pairs
  altogether. For a single yard that read 200 wagons that is **199 constraints
  against 19,900** — the shipped file prints both numbers so you can see the
  gap rather than take it on faith. Across the whole 20,000-position budget,
  neighbouring pairs give you at most 20,000 constraints; every-pair, from one
  long sighting, heads towards two million. And the extra ones buy nothing:
  if the sighting says `A`, `B`, `C`, then "A in front of B" and "B in front of
  C" already force "A in front of C". Adding it is not a different answer, it
  is the same answer paid for twice.

- **Wagon marks are compared as plain strings, so the tie-break is Python's
  `<`.** That means code point by code point: `"BOX-27" < "CAB-09"`, and also
  `"WAG-9" > "WAG-10"`, because `9` beats `1` at the first character that
  differs. This is stated rather than left to chance because "alphabetically
  smallest" has to mean exactly one thing or two correct-looking programs
  disagree. If you want numeric-looking marks to sort numerically, that is a
  different contract and it belongs in the Stretch, not here.

- **A yard's sighting is never wrong, only incomplete.** You are not being
  asked to weigh evidence or discard an outlier. Every constraint is true, so
  a contradiction between two of them is not a mistake to smooth over — it is
  proof that no train fits, and the honest answer is `"impossible"` with an
  empty order.

- **An empty train is one train, not zero.** There is exactly one way to
  arrange no wagons, so `[]` with `"unique"` is not a special case bolted on;
  it is what the general rule says when you run it on nothing. A program that
  hard-codes it has probably got the general rule wrong.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-consist-reconstruction-solution.py
sightings            verdict     order
nothing filed        unique      []
two blank sightings  unique      []
one wagon each       ambiguous   ['HOP-11', 'TNK-04']
overlapping yards    unique      ['HOP-11', 'TNK-04', 'BOX-27', 'GON-52', 'CAB-09']
never seen together  ambiguous   ['FLT-03', 'REF-08', 'CAB-09']
yards disagree       impossible  []
wagon listed twice   impossible  []
200-wagon sighting : 199 neighbouring constraints
                     19900 if you write every pair
blank wagon mark   : sighting 0 holds '', which is not a wagon mark
All checks passed.
```

Two rows are worth staring at. **overlapping yards** is the payoff: three
yards, none of which saw more than three wagons, and between them they force
all five into one order — including `TNK-04`, which only one yard ever saw.
**never seen together** returns an order that is perfectly legal and a verdict
that says do not trust it: no yard ever saw `FLT-03` and `REF-08` in the same
sighting, so nothing on paper decides which is in front, and `FLT-03` goes
first only because `F` comes before `R`.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python challenge-02-consist-reconstruction.py`. The first assert fails,
   because the stub returns `None`. That is the correct starting point.
2. **Frame it.** In, a list of partial front-to-back sightings. Out, one order
   and one verdict from three. Say the three verdicts out loud in your own
   words before writing code — most of the wrong answers on this page come
   from a fuzzy idea of what `"ambiguous"` means.
3. Draw the `overlapping yards` case on paper. Five wagons, three sightings,
   six constraints. Place the wagons by hand and notice what you are actually
   doing: at each step you look for a wagon with nothing left in front of it.
   That hand method *is* Kahn's algorithm; the code is only bookkeeping.
4. **Research the constraints.** Convince yourself, on that paper drawing,
   that adding `HOP-11` in front of `CAB-09` — true, but not a neighbouring
   pair — changes nothing about which wagon is ready when. Then count the
   pairs for a 200-wagon sighting both ways. That comparison is the reason
   this page has a `_constraints_every_pair` at all.
5. **Assess your options.** Kahn or DFS post-order? Both topologically sort.
   Take Kahn, for two reasons that matter here: it is a loop, so no recursion
   limit to think about; and the ready pool is a thing you can *look at*, which
   is what makes the ambiguity check a one-liner. A DFS post-order version can
   be made to answer the same question, but not nearly as directly.
6. **Make it.** Build the wagon set and the constraint set first, and print
   both for the small cases before writing any of the sorting. Most bugs on
   this page are already present at that point.
7. Add the counts and the heap. Get `"unique"` and `"impossible"` working,
   and leave the verdict as a two-way choice for now.
8. Add the ambiguity check: **before** you pop, if the heap holds more than
   one wagon, the answer is not forced. Before, not after — checking after the
   pop misses the last step and is a real bug with a real wrong answer; it is
   in *Common bugs to catch* below.
9. **Examine.** Run all seven named cases. Then feed it a sighting of your own
   with a wagon repeated in the middle, and satisfy yourself that the answer
   would still be `"impossible"` even if you deleted the explicit check —
   working out why is a good five minutes.
10. Last, make the 200-wagon sighting and print the two constraint counts.
    Seeing 199 next to 19,900 is the part of this page you will still remember
    in a month.

## The Solution

```python
"""challenge-02-consist-reconstruction-solution.py — rebuild a train from sightings.

A freight train's wagons sit in one fixed front-to-back order. No single yard
saw the whole train, so each yard filed a sighting: the wagons it did see,
front to back, with gaps where wagons it never saw would have been.

Every sighting says the same small thing over and over: this wagon is in front
of the next one. Collect those neighbouring pairs, run Kahn's algorithm over
them, and the train comes back — or the sightings contradict each other and
nothing can.

The verdict is the second half of the answer. "unique" means the sightings pin
the train down. "ambiguous" means more than one train fits, and the order
handed back is only one of them. "impossible" means no train fits at all.

`_constraints_every_pair` is here to be measured, not used: it is the common
wrong move of writing a constraint between every pair of wagons in a sighting
instead of only the neighbouring ones. It gets the same answer for far more
work, and the self-checks print both counts so the gap is visible.
"""

from __future__ import annotations

import heapq


def reconstruct_consist(sightings: list[list[str]]) -> tuple[list[str], str]:
    """Rebuild the train's wagon order from the yards' sightings.

    Args:
        sightings: One list per yard, holding the wagon marks that yard saw,
            written front to back. A yard may have seen one wagon, or none.

    Returns:
        (order, verdict). verdict is "unique" when exactly one train fits the
        sightings, "ambiguous" when more than one does, and "impossible" when
        none does. On "impossible" the order is []. On "ambiguous" the order
        is one train that really does fit: at every step the alphabetically
        smallest wagon that could come next.

    Raises:
        ValueError: a sighting holds a wagon mark that is not a non-empty
            string.
    """
    wagons: set[str] = set()
    for index, sighting in enumerate(sightings):
        for mark in sighting:
            if not isinstance(mark, str) or not mark:
                raise ValueError(
                    f"sighting {index} holds {mark!r}, which is not a wagon mark"
                )
            wagons.add(mark)
        if len(set(sighting)) != len(sighting):
            # One wagon cannot stand in two places in one train.
            return [], "impossible"

    # Only neighbouring pairs. A > B and B > C already say A > C.
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for front, back in zip(sighting, sighting[1:]):
            constraints.add((front, back))

    behind: dict[str, list[str]] = {wagon: [] for wagon in wagons}
    ahead_count: dict[str, int] = {wagon: 0 for wagon in wagons}
    for front, back in constraints:
        behind[front].append(back)
        ahead_count[back] += 1

    ready = [wagon for wagon in wagons if ahead_count[wagon] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    forced = True
    while ready:
        if len(ready) > 1:
            # More than one wagon could legally come next, so the train the
            # sightings describe is not the only one that fits.
            forced = False
        wagon = heapq.heappop(ready)
        order.append(wagon)
        for follower in behind[wagon]:
            ahead_count[follower] -= 1
            if ahead_count[follower] == 0:
                heapq.heappush(ready, follower)

    if len(order) != len(wagons):
        # Whatever is left is stuck behind itself: the sightings loop.
        return [], "impossible"
    return order, "unique" if forced else "ambiguous"


def _constraints_every_pair(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the wasteful way, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        A constraint for every pair of wagons in every sighting, not only the
        neighbouring ones.
    """
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for i, front in enumerate(sighting):
            for back in sighting[i + 1 :]:
                constraints.add((front, back))
    return constraints


def _constraints_neighbours(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the way the answer does, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        One constraint per neighbouring pair in each sighting.
    """
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for front, back in zip(sighting, sighting[1:]):
            constraints.add((front, back))
    return constraints


def _order_from_constraints(
    wagons: set[str], constraints: set[tuple[str, str]]
) -> list[str]:
    """Run the same Kahn walk over a constraint set someone else built.

    Args:
        wagons: Every wagon that must appear in the order.
        constraints: (front, back) pairs, each meaning front is ahead of back.

    Returns:
        The alphabetically smallest legal order, or [] when none exists.
    """
    behind: dict[str, list[str]] = {wagon: [] for wagon in wagons}
    ahead_count: dict[str, int] = {wagon: 0 for wagon in wagons}
    for front, back in constraints:
        behind[front].append(back)
        ahead_count[back] += 1
    ready = [wagon for wagon in wagons if ahead_count[wagon] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        wagon = heapq.heappop(ready)
        order.append(wagon)
        for follower in behind[wagon]:
            ahead_count[follower] -= 1
            if ahead_count[follower] == 0:
                heapq.heappush(ready, follower)
    return order if len(order) == len(wagons) else []


if __name__ == "__main__":
    cases: list[tuple[str, list[list[str]]]] = [
        ("nothing filed", []),
        ("two blank sightings", [[], []]),
        ("one wagon each", [["HOP-11"], ["TNK-04"]]),
        (
            "overlapping yards",
            [
                ["HOP-11", "BOX-27", "CAB-09"],
                ["HOP-11", "TNK-04", "BOX-27"],
                ["BOX-27", "GON-52", "CAB-09"],
            ],
        ),
        ("never seen together", [["FLT-03", "CAB-09"], ["REF-08", "CAB-09"]]),
        ("yards disagree", [["TNK-04", "BOX-27"], ["BOX-27", "TNK-04"]]),
        ("wagon listed twice", [["HOP-11", "TNK-04", "HOP-11"]]),
    ]
    print(f"{'sightings':<21}{'verdict':<12}order")
    for name, sightings in cases:
        order, verdict = reconstruct_consist(sightings)
        print(f"{name:<21}{verdict:<12}{order}")

    assert reconstruct_consist([]) == ([], "unique")
    assert reconstruct_consist([[], []]) == ([], "unique")
    assert reconstruct_consist([["HOP-11"], ["TNK-04"]]) == (
        ["HOP-11", "TNK-04"],
        "ambiguous",
    )
    assert reconstruct_consist(
        [
            ["HOP-11", "BOX-27", "CAB-09"],
            ["HOP-11", "TNK-04", "BOX-27"],
            ["BOX-27", "GON-52", "CAB-09"],
        ]
    ) == (["HOP-11", "TNK-04", "BOX-27", "GON-52", "CAB-09"], "unique")
    assert reconstruct_consist([["FLT-03", "CAB-09"], ["REF-08", "CAB-09"]]) == (
        ["FLT-03", "REF-08", "CAB-09"],
        "ambiguous",
    )
    assert reconstruct_consist([["TNK-04", "BOX-27"], ["BOX-27", "TNK-04"]]) == (
        [],
        "impossible",
    )
    assert reconstruct_consist([["HOP-11", "TNK-04", "HOP-11"]]) == ([], "impossible")

    # One yard that saw the whole train. Both ways of reading it agree; only
    # one of them stays linear in the wagons it was given.
    long_train = [[f"WAG-{number:04d}" for number in range(200)]]
    wagons = {mark for sighting in long_train for mark in sighting}
    neighbours = _constraints_neighbours(long_train)
    every_pair = _constraints_every_pair(long_train)
    assert _order_from_constraints(wagons, neighbours) == long_train[0]
    assert _order_from_constraints(wagons, every_pair) == long_train[0]
    print(f"200-wagon sighting : {len(neighbours)} neighbouring constraints")
    print(f"                     {len(every_pair)} if you write every pair")
    assert len(neighbours) == 199
    assert len(every_pair) == 19_900

    try:
        reconstruct_consist([["HOP-11", ""]])
    except ValueError as error:
        print(f"blank wagon mark   : {error}")
    else:  # pragma: no cover - the call above always raises
        raise AssertionError("a blank wagon mark must be refused")

    print("All checks passed.")
```

**The input is not a graph, so the first job is building one.** Every wagon
mark is a node. Every neighbouring pair in every sighting is one edge, pointing
from the wagon in front to the wagon behind it. That is the whole modelling
step, and it is three lines:

```python
for sighting in sightings:
    for front, back in zip(sighting, sighting[1:]):
        constraints.add((front, back))
```

`zip(sighting, sighting[1:])` is the idiom for "walk the neighbouring pairs".
It stops when the shorter side runs out, so a sighting of one wagon yields no
pairs and a sighting of none yields no pairs, with no length checks anywhere.

**Neighbouring pairs are enough because ordering is transitive.** If `A` is in
front of `B` and `B` is in front of `C`, then `A` is in front of `C` — that
fact is already carried by the two constraints you have, so writing the third
one down adds no information. It does add work: `n - 1` constraints become
`n * (n - 1) / 2`, which for one 200-wagon sighting is 199 against 19,900, and
for the biggest single sighting the bounds allow is 1,999 against nearly two
million. The answer would be identical — the shipped file asserts exactly that
by running the same walk over both constraint sets — which is what makes this
such a good trap. It does not fail; it just costs a hundred times more, and in
an interview you will be asked why.

**The constraints live in a set for a plainer reason: two yards can file the
same pair.** If three yards all saw `HOP-11` directly in front of `TNK-04`,
that is one fact, not three. A set says so once. Nothing downstream has to
know or care how many yards agreed.

**The ready pool is a heap because the tie-break is a rule, not a mood.**
`heapq` always hands back the smallest item, so "the alphabetically smallest
wagon that could come next" is `heapq.heappop(ready)` and nothing else.
Reach for a plain list and `pop()` instead and you get the *last* item, which
is a legal order but not the one the contract asks for — and worse, reach for
a `set` and the order depends on string hashing, which changes between runs.

**Ambiguity is the size of the ready pool, checked before the pop.**

```python
while ready:
    if len(ready) > 1:
        forced = False
```

If two wagons are both ready, then both could legally be placed next, so at
least two different trains fit the sightings — that is the definition of
ambiguous, and the pool size is that definition made mechanical. It must be
read *before* popping, because the pool is at its largest right then. Check it
after the pop and you miss the final step entirely: with two lone wagons and
no constraints at all, the pool holds two, you take one, and a check made
afterwards sees a pool of one and calls a genuinely ambiguous train forced.

**Two different failures both come out as `"impossible"`, and only one of them
needs its own code.** A loop in the constraints — two yards insisting each way
round — leaves wagons that are never ready, so the order comes up short and
`len(order) != len(wagons)` catches it. A mark repeated inside one sighting is
caught up front by comparing `len(set(sighting))` to `len(sighting)`. Here is
the thing worth noticing: the second check is not strictly necessary. A mark
at two places in one sighting builds a chain of constraints that leads from
that mark back to itself, which is a loop, which the length check would catch
anyway. The explicit check is kept because it says *why* in the code, and it
answers before doing any work. Knowing that it is a convenience rather than a
correctness fix is the kind of thing an interviewer will probe.

**The empty train falls out; it is not special-cased.** With no sightings there
are no wagons, the heap starts empty, the loop never runs, `forced` is still
`True`, and `len(order) == len(wagons) == 0`. The function returns
`([], "unique")` by the general rule, which is the right answer: there is
exactly one way to arrange nothing.

## Download and run

Download
[challenge-02-consist-reconstruction-solution.py](./challenge-02-consist-reconstruction-solution.py)
and run it:

```bash
python challenge-02-consist-reconstruction-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-02-consist-reconstruction.py`.

## Common bugs to catch

- **`KeyError: 'CAB-09'`.** You built the followers dictionary from the
  constraints instead of from the wagons:

  ```text
  Traceback (most recent call last):
    File "consist.py", line 29, in <module>
      for follower in behind[wagon]:
                      ~~~~~~^^^^^^^
  KeyError: 'CAB-09'
  ```

  `{front: [] for front, _ in constraints}` has a key for every wagon that is
  in front of something, and no key for the wagon at the very back of the
  train — which is the one wagon guaranteed to exist. Build both dictionaries
  from the wagon set, so that every wagon has an entry from the start.

- **`(['REF-08', 'FLT-03', 'CAB-09'], 'ambiguous')` instead of
  `(['FLT-03', 'REF-08', 'CAB-09'], 'ambiguous')`.** You used a list and
  `pop()` where the contract asks for the smallest:

  ```text
  >>> reconstruct_consist([['FLT-03', 'CAB-09'], ['REF-08', 'CAB-09']])
  (['REF-08', 'FLT-03', 'CAB-09'], 'ambiguous')
  ```

  `list.pop()` takes from the end. Both orders are legal trains and the verdict
  is right, which is exactly why this survives casual testing — the contract
  fixes the tie-break so that "legal" is not good enough. Use `heapq`.

- **`(['HOP-11', 'TNK-04'], 'unique')` for `[['HOP-11'], ['TNK-04']]`.** You
  checked the pool size after the pop instead of before:

  ```text
  >>> reconstruct_consist([['HOP-11'], ['TNK-04']])
  (['HOP-11', 'TNK-04'], 'unique')
  ```

  Two wagons, no constraints between them, so either could be in front — that
  is `"ambiguous"` by definition. The pool held two right up until you took one
  out. Move the check above the pop.

- **`([], 'unique')` for `[['HOP-11'], ['TNK-04']]`.** You collected the wagons
  from the constraints rather than from the sightings:

  ```text
  >>> reconstruct_consist([['HOP-11'], ['TNK-04']])
  ([], 'unique')
  ```

  Neither yard filed an ordering, so there are no constraints, so a wagon set
  built out of the constraints is empty — and the program cheerfully reports a
  train with no wagons in it. A sighting of one wagon carries no ordering but
  it does carry an existence claim, and Requirement 8 exists for this.

- **`(['FLT-03'], 'unique')` where the answer is `([], 'impossible')`.** You
  ran Kahn and returned whatever came out, with no length check:

  ```text
  >>> reconstruct_consist([['TNK-04', 'BOX-27'], ['BOX-27', 'GON-52'], ['GON-52', 'TNK-04']])
  (['FLT-03'], 'unique')
  ```

  Three yards insisting on a circle leave those three wagons stuck forever, so
  they never make it into the order — but the unrelated wagon does, and a
  partial answer looks like an answer. `len(order) != len(wagons)` is the
  entire cycle detector, and it costs one line.

- **`([], 'impossible')` for a perfectly good train.** You passed a flat list
  of marks instead of a list of sightings:

  ```text
  >>> reconstruct_consist(['HOP-11', 'TNK-04'])
  ([], 'impossible')
  ```

  Python iterates a string one character at a time, so `"HOP-11"` became a
  "sighting" of `H`, `O`, `P`, `-`, `1`, `1` — and it lists `1` twice, so your
  own duplicate rule fired. The type hint says `list[list[str]]` and the
  outer list really does have to be a list of lists.

- **The 200-wagon sighting is slow and everything else is fine.** You wrote a
  constraint between every pair. Nothing fails, no test goes red, and the
  answer is right. Count the constraints — 19,900 where 199 will do — and read
  the Constraints section again.

## Under the hood

<details>
<summary>Under the hood — what the verdict really asks, and what it costs</summary>

**"Unique" has a much sharper name.** A directed graph with no loops has
exactly one topological order if and only if there is an edge between every
consecutive pair of that order — that is, the graph contains a **Hamiltonian
path**, a path visiting every node once. The reasoning is short. If some
consecutive pair `x`, `y` in your order has no edge between them, nothing
forces `x` before `y`, so swapping them gives a second legal order. And if
every consecutive pair does have an edge, the whole order is one chain and
nothing can move. So "the ready pool never held two" and "the order is a chain
of constraints" are two ways of saying the same thing, and the second gives you
a completely independent way to test the first — which is exactly the second
stretch below.

Finding a Hamiltonian path in a general graph is famously hard. It is easy here
only because a topological order hands you the one candidate to check, so
there is nothing to search for.

**"Ambiguous" is hiding a much harder question.** Your verdict says whether
more than one train fits. It does not say **how many** do, and that is a
genuinely difficult question: counting the linear extensions of a partial order
is `#P`-complete, proved by Brightwell and Winkler in 1991. The brute-force
count in the third stretch below is fine on five wagons and hopeless on fifty.
Be glad the contract only asks "more than one?" — the boundary between an easy
question and an intractable one is often exactly that thin, and noticing where
it sits is worth saying out loud in an interview.

**The cost, said honestly.** Building the constraints is one pass over the
listed positions. Kahn's algorithm is one look at every wagon and one look at
every constraint, and then it is done. The heap adds a `log` factor to the
wagon half: every wagon is pushed once and popped once, at `log W` each, so the
total is `O(P + C + W log W)` where `P` is the listed positions, `C` the
constraints and `W` the wagons. With a plain queue instead of a heap it would
be flatly linear — the `log W` is the price of the deterministic tie-break, and
at 2,000 wagons `log W` is about 11, so the price is nothing.

**Why Kahn and not DFS post-order here.** Both produce a topological order in
linear time, and Lecture 3 §5 lays out the general choice. This problem tips it
for two specific reasons. First, Kahn is a loop, so the recursion depth that
haunts the rest of this week never comes up — see
[exercise-02-conveyor-reachability.md](../exercises/exercise-02-conveyor-reachability.md)
for why that matters. Second, and more importantly, Kahn keeps an explicit pool
of everything that could come next, and this problem's whole second half is a
question about that pool. DFS post-order never materialises it, so the same
verdict would have to be reconstructed afterwards from the Hamiltonian-path
property. Pick the algorithm whose internal state is the thing you were asked
about.

**Three colours, and where they went.** Lecture 3 §2 detects a directed loop by
painting nodes white, grey and black during a depth-first walk, and calling any
edge into a grey node a loop. There is no trace of that here, and it is worth
knowing why: Kahn detects the same loops by arithmetic. Anything in a loop can
never have its count of wagons-in-front reach zero — each one is waiting on the
next — so it never enters the pool, so the order comes up short. Same fact,
found two ways. If you ever need to *report* the loop rather than merely notice
it, the three-colour walk is the one that can, because the grey nodes on the
stack are the loop; that is the first stretch.

</details>

## Acceptance checklist

- [ ] `python challenge-02-consist-reconstruction.py` prints `All checks passed.`
- [ ] `reconstruct_consist([])` and `reconstruct_consist([[], []])` both return
      `([], "unique")`.
- [ ] The three overlapping yards return all five wagons with verdict
      `"unique"`.
- [ ] Two wagons never seen in the same sighting return a legal order with
      verdict `"ambiguous"`.
- [ ] Contradicting yards, and a mark repeated inside one sighting, both return
      `([], "impossible")`.
- [ ] The tie-break is the alphabetically smallest ready mark, taken from a
      heap.
- [ ] The ambiguity check reads the pool size **before** the pop.
- [ ] A wagon seen alone by one yard still appears in the order.
- [ ] Constraints come from neighbouring pairs only, and the file prints 199
      against 19,900 to prove it.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like
      `Add Week 7 challenge 2: consist reconstruction`.

## Stretch

- **Name the loop, do not just detect it.** `"impossible"` tells the yardmaster
  there is a contradiction; it does not tell them which yards to go and ask
  about. Kahn cannot say, because the wagons in the loop are exactly the ones
  it never touched. The three-colour walk from Lecture 3 §2 can: when it finds
  an edge into a grey wagon, the grey wagons still on the path *are* the loop.

  ```python
  def name_the_loop(sightings: list[list[str]]) -> list[str]:
      """Return one loop of wagons the sightings insist on, or []."""
      constraints = _constraints_neighbours(sightings)
      behind: dict[str, list[str]] = {}
      for front, back in constraints:
          behind.setdefault(front, []).append(back)
          behind.setdefault(back, [])
      colour = {wagon: "white" for wagon in behind}
      path: list[str] = []

      def walk(wagon: str) -> list[str]:
          colour[wagon] = "grey"
          path.append(wagon)
          for follower in sorted(behind[wagon]):
              if colour[follower] == "grey":
                  return path[path.index(follower):] + [follower]
              if colour[follower] == "white":
                  found = walk(follower)
                  if found:
                      return found
          colour[wagon] = "black"
          path.pop()
          return []

      for wagon in sorted(behind):
          if colour[wagon] == "white":
              found = walk(wagon)
              if found:
                  return found
      return []
  ```

  ```text
  yards disagree : ['BOX-27', 'GON-52', 'TNK-04', 'BOX-27']
  overlapping    : []
  ```

  Read the first line as a sentence: `BOX-27` is in front of `GON-52` is in
  front of `TNK-04` is in front of `BOX-27`. Now go and ask those yards. Note
  that this version recurses, so put a bound on it or rewrite it with a stack
  before you point it at anything large.

- **Check the verdict a second, independent way.** By the Hamiltonian-path
  argument in *Under the hood*, an order is forced exactly when every
  consecutive pair in it is a constraint you were actually given.

  ```python
  def every_step_forced(sightings: list[list[str]]) -> bool:
      """True when each wagon in the order is directly in front of the next."""
      order, verdict = reconstruct_consist(sightings)
      if verdict == "impossible":
          return False
      constraints = _constraints_neighbours(sightings)
      return all(pair in constraints for pair in zip(order, order[1:]))
  ```

  ```text
  overlapping    : True (unique)
  never together : False (ambiguous)
  ```

  Two computations that share no code and must always agree is the cheapest
  strong test there is — the same move Challenge 1 makes with its slow
  reference. Wire it into your self-checks and it will catch any future edit
  that breaks the pool-size logic.

- **Count the trains that fit, and prove the verdict on small cases.** Try
  every arrangement of the wagons and keep the ones that break no constraint.

  ```python
  def count_trains(sightings: list[list[str]]) -> int:
      """Count every wagon order that fits, by trying all of them."""
      _, verdict = reconstruct_consist(sightings)
      if verdict == "impossible":
          return 0
      wagons = sorted({mark for sighting in sightings for mark in sighting})
      constraints = _constraints_neighbours(sightings)
      fitting = 0
      for candidate in permutations(wagons):
          place = {wagon: at for at, wagon in enumerate(candidate)}
          if all(place[front] < place[back] for front, back in constraints):
              fitting += 1
      return fitting
  ```

  ```text
  overlapping    : 1 trains fit, verdict unique
  never together : 2 trains fit, verdict ambiguous
  yards disagree : 0 trains fit, verdict impossible
  nothing filed  : 1 trains fit, verdict unique
  ```

  Three verdicts, three counts, and they line up exactly: `"unique"` is one,
  `"ambiguous"` is more than one, `"impossible"` is none. Look at the last row
  as well — no sightings at all counts as **one** train, the empty one, which
  is the same claim the contract makes and now you have it from an independent
  direction. Do not run this past about nine wagons: `permutations` is
  factorial, and 12 wagons is already half a billion arrangements.

**Practice elsewhere.** The same "derive the edges, then topologically sort"
move appears as
[LeetCode 269 · Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)
if you want a judge to run against — ours differs in that the evidence is many
partial sightings rather than one fully sorted list, there is no prefix rule to
trip over, and the answer carries a verdict separating a forced order from a
merely possible one.

That is the week's problem set. Take the [quiz](../quiz.md), work through the
[homework](../homework/README.md), then ship the
[mini-project](../mini-project/README.md).
