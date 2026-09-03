# Exercise 1 — Sluice Gate Order

> **Topic:** `heapq.heapify`, `heappush`, `heappop`, and reading the front of a heap without disturbing it
> **Lecture:** [01 — `heapq` and the Top-k Template](../lecture-notes/01-heapq-and-top-k.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** every other page this week is this page with more on top. If `heapify`, `heappop` and `queue[0]` are not automatic, the two-heap and k-way-merge pages will feel like magic instead of like arithmetic. This one also gets the first surprise out of the way early: a heap is **not** a sorted list, and printing it will prove that to you before anybody tells you.

## The Brief

Picture a flat piece of farmland that sits below the level of the river beside
it. The only reason it is not a lake is a ring of banks and a row of **sluice
gates** — doors in the bank that let water out when the river is low enough.
Somebody has to open them, one at a time, and the order matters.

The rule the drainage board uses is simple: **open the gate with the least
water pressed against it first.** The pressure is measured as the **head** —
how many centimetres higher the water is on one side than the other. Open a
gate with a big head first and the rush can undercut the bank; work up from
the smallest and the flow stays gentle.

So you have a pile of gates, each with a number, and you keep wanting the
smallest number. You could sort the whole pile every time. There is a cheaper
tool.

A **heap** is a pile of things arranged so that **the smallest one is always
on top**, and nothing else is promised. Think of a pile of stones where you
only ever care about the lightest one. Keeping the whole pile in order is a
lot of work. Keeping the lightest on top is much less work, and it is all you
ever asked for.

Python's `heapq` module turns an ordinary list into that pile. Three moves are
the whole toolkit for this page:

- **`heapq.heapify(items)`** — rearrange a list, in place, so the smallest
  thing is at position 0.
- **`heapq.heappop(items)`** — take that smallest thing out and shuffle the
  next-smallest up into its place.
- **`items[0]`** — look at the smallest thing without taking it. There is no
  `heappeek`; reading position 0 *is* the peek, and it costs nothing.

Two gates can have the same head, so the board wrote down a full rule: **least
head first; if two gates tie, the one that takes fewer turns of the handwheel;
if they still tie, the earlier name, A to Z.** You will say that whole rule in
one line, because a heap of **tuples** compares box by box and stops at the
first difference — exactly the way you would read the rule out loud.

You are writing four small functions for the pump crew's tablet: build the
queue, look at what is next, drain the whole queue in order, and answer "which
gates come before the head reaches 25 cm?" without touching the ones behind.

## Starter

Create `exercise-01-sluice-gate-order.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""exercise-01-sluice-gate-order.py — the drainage board's opening order.

Build a queue of sluice gates that always hands back the one with the least
water head, then read from it four different ways.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

import heapq

# ---- Given data ----
# (gate name, water head in centimetres, turns of the handwheel to open it)
GATES: list[tuple[str, int, int]] = [
    ("Molenkade", 41, 6),
    ("Zwarte Sloot", 17, 3),
    ("Kruisweg", 41, 2),
    ("Oude Dijk", 8, 9),
    ("Vaartbrug", 23, 4),
    ("Noordkil", 17, 3),
    ("Boezemsluis", 62, 1),
]


# ---- Your task ----
def build_queue(gates: list[tuple[str, int, int]]) -> list[tuple[int, int, str]]:
    """Return a NEW heapified list of (head, turns, name) entries.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        A list rearranged so that entry 0 is the smallest by
        (head, turns, name). The rest of the list is heap order, not
        sorted order.
    """
    # TODO: reorder each row into (head, turns, name), then heapify the new list
    ...


def peek_next(queue: list[tuple[int, int, str]]) -> str | None:
    """Return the name of the gate at the front of the queue, without removing it.

    Args:
        queue: A heapified queue from build_queue.

    Returns:
        The gate's name, or None when the queue is empty.
    """
    # TODO: guard the empty case, then read position 0. No pop.
    ...


def drain_order(gates: list[tuple[str, int, int]]) -> list[str]:
    """Return every gate's name in the order the crew opens them.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        Names, lowest head first; ties by fewer turns, then by name A to Z.
    """
    # TODO: build the queue, then heappop until it is empty
    ...


def gates_below(gates: list[tuple[str, int, int]], limit_cm: int) -> list[str]:
    """Return the names of the gates whose head is under limit_cm, in service order.

    Stops as soon as the front of the queue reaches the limit, so the gates
    behind it are never removed.

    Args:
        gates: (name, head, turns) rows. This list is not modified.
        limit_cm: The head, in centimetres, at which the crew stops.

    Returns:
        Names in service order. Empty when the shallowest gate is already at
        or above the limit.
    """
    # TODO: pop while the queue is non-empty AND its front is under the limit
    ...


# ---- Self-check ----
if __name__ == "__main__":
    queue = build_queue(GATES)
    print("heap layout:")
    for head, turns, name in queue:
        print(f"  {head:3d} cm  {turns} turns  {name}")

    print(f"front of the queue: {peek_next(queue)}")
    print(f"queue length after peeking: {len(queue)}")

    print("service order:")
    for position, name in enumerate(drain_order(GATES), 1):
        print(f"  {position}. {name}")

    print(f"under 25 cm: {gates_below(GATES, 25)}")
    print(f"under 5 cm: {gates_below(GATES, 5)}")
    print(f"front of an empty queue: {peek_next([])}")

    assert queue[0] == (8, 9, "Oude Dijk")
    assert len(queue) == 7
    assert peek_next(queue) == "Oude Dijk"
    assert drain_order(GATES)[:3] == ["Oude Dijk", "Noordkil", "Zwarte Sloot"]
    assert drain_order(GATES)[-1] == "Boezemsluis"
    assert drain_order(GATES).index("Kruisweg") < drain_order(GATES).index("Molenkade")
    assert gates_below(GATES, 25) == ["Oude Dijk", "Noordkil", "Zwarte Sloot", "Vaartbrug"]
    assert gates_below(GATES, 5) == []
    assert peek_next([]) is None
    assert GATES[0] == ("Molenkade", 41, 6)  # original rows untouched
    print("All checks passed.")
```

Four words you need before you start.

**Heap.** A list that `heapq` has arranged so position 0 holds the smallest
item. Nothing else about the order is promised, and the printout in the
expected output shows you exactly that.

**In place.** `heapq.heapify(items)` rearranges the list you handed it and
returns `None`. It does not build you a new one. That is why `build_queue`
makes a fresh list first — the rows the board gave you must come out
unchanged.

**Tuple comparison.** Python compares two tuples box by box, left to right,
and stops at the first box where they differ. `(17, 3, "Noordkil")` is smaller
than `(17, 3, "Zwarte Sloot")` because the first two boxes match and `"N"`
comes before `"Z"`. That single fact is what lets one tuple carry a three-part
rule.

**Peek.** Looking at the front without removing it. `queue[0]` is the peek.
There is no `heapq.heappeek`, and you do not need one.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-08-heaps-and-priority-queues/exercises/exercise-01-sluice-gate-order.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `build_queue` returns a **new** list of `(head, turns, name)` tuples with
   `heapq.heapify` applied. `GATES` is unchanged afterwards.
2. `peek_next` returns a name string, never a tuple, and never removes
   anything. `len(queue)` is the same before and after.
3. `peek_next([])` returns `None` rather than raising.
4. `drain_order` returns all seven names in service order: least head first,
   then fewer turns, then name A to Z.
5. `gates_below(GATES, 25)` returns exactly
   `["Oude Dijk", "Noordkil", "Zwarte Sloot", "Vaartbrug"]`, and stops popping
   as soon as the front of the queue is at or above the limit.
6. `gates_below(GATES, 5)` returns `[]`.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Use `heapq`, not `sorted`, for `gates_below`.** Sorting puts all seven
  gates in order so you can read the first four and throw three away. The heap
  answers "which are under the limit" by looking at the front and stopping.
  With seven gates you cannot feel it. With a hundred thousand river assets and
  a limit that only four of them pass, sorting does about 1.7 million
  comparisons for four answers, and the heap does about a hundred thousand to
  build plus a handful per answer.

- **Copy before you heapify.** `heapq.heapify` rearranges the list you pass it.
  `build_queue` is handed the board's own `GATES`, and the rest of the program
  is still reading it, so shuffling it behind their back is a bug even when
  your return value looks right. The last assert on the page exists only to
  catch this.

- **Put the numbers you sort by first in the tuple.** The rows arrive as
  `(name, head, turns)` and the rule reads "head, then turns, then name", so
  the entries you push must be `(head, turns, name)`. Heaping the rows as they
  arrive compares names first and gives you a perfectly ordered answer to a
  question nobody asked.

- **Peek with `queue[0]`, never with `heappop` followed by `heappush`.** Pop
  and push again is two rearrangements of the pile to answer a question that a
  single list index already answers. It also briefly changes the queue, which
  matters the moment anything else is looking at it.

- **Do not sort the heap and do not trust its printed order.** A heap promises
  one thing: the smallest item is at position 0. The expected output below
  prints the whole layout so you can see for yourself that positions 1 to 6
  are not in order. Code that reads `queue[1]` expecting the second-smallest is
  reading a number that happens to be there.

- **Guard the empty queue before you index it.** `queue[0]` on an empty list
  raises `IndexError`, and so does `heapq.heappop` on one. An empty queue is a
  normal state for a pump crew at the end of a shift, not an error, so
  `peek_next` returns `None`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
heap layout:
    8 cm  9 turns  Oude Dijk
   17 cm  3 turns  Zwarte Sloot
   17 cm  3 turns  Noordkil
   41 cm  6 turns  Molenkade
   23 cm  4 turns  Vaartbrug
   41 cm  2 turns  Kruisweg
   62 cm  1 turns  Boezemsluis
front of the queue: Oude Dijk
queue length after peeking: 7
service order:
  1. Oude Dijk
  2. Noordkil
  3. Zwarte Sloot
  4. Vaartbrug
  5. Kruisweg
  6. Molenkade
  7. Boezemsluis
under 25 cm: ['Oude Dijk', 'Noordkil', 'Zwarte Sloot', 'Vaartbrug']
under 5 cm: []
front of an empty queue: None
All checks passed.
```

Look at the heap layout. Position 0 is the smallest, and after that the order
is 17, 17, 41, 23, 41, 62 — not sorted, and not meant to be. Now look at the
service order underneath: 8, 17, 17, 23, 41, 41, 62. The sorted answer comes
out of *popping*, one at a time, never out of reading the list as it stands.

Two gates read 17 cm at three turns each. `Noordkil` comes out first because
`"N"` beats `"Z"`, and that is the third box of the tuple doing its job.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-sluice-gate-order.py`. You get a `TypeError` on the
   first line that loops over `queue`. That is the correct starting point — it
   proves the self-check is real.
2. Fill in `build_queue`. One comprehension to reshape the rows, one
   `heapq.heapify` call, one `return`. Watch out: `heapify` returns `None`, so
   `return heapq.heapify(queue)` gives you nothing.
3. Run again and read the printed layout before anything else. Position 0
   should be `Oude Dijk`. If the first row is `Boezemsluis` you heaped the rows
   in their original `(name, head, turns)` shape and are ordering by name.
4. Fill in `peek_next`. Guard the empty case first, then return `queue[0][2]`.
   Confirm on screen that the queue length is still 7 afterwards.
5. Fill in `drain_order`: build the queue, then `while queue:` and
   `heapq.heappop`. Read the service order out loud against the rule.
6. Fill in `gates_below`. The loop condition has two halves and both matter:
   `while queue and queue[0][0] < limit_cm`. Swap them around and an empty
   queue raises `IndexError` on the last turn.
7. When `All checks passed.` prints, open a REPL with
   `python -i exercise-01-sluice-gate-order.py` and try
   `gates_below(GATES, 100)` and `gates_below(GATES, 0)`. Both should behave
   without a special case anywhere in your code.

## The Solution

```python
"""exercise-01-sluice-gate-order-solution.py — the drainage board's opening order.

A polder's sluice gates are opened lowest water head first. This file builds
the queue with `heapq`, reads the front of it without disturbing it, drains it
in service order, and answers a prefix question — "which gates come before the
head reaches 25 cm?" — without draining the rest.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (gate name, water head in centimetres, turns of the handwheel to open it)
GATES: list[tuple[str, int, int]] = [
    ("Molenkade", 41, 6),
    ("Zwarte Sloot", 17, 3),
    ("Kruisweg", 41, 2),
    ("Oude Dijk", 8, 9),
    ("Vaartbrug", 23, 4),
    ("Noordkil", 17, 3),
    ("Boezemsluis", 62, 1),
]


# ---- Your task ----
def build_queue(gates: list[tuple[str, int, int]]) -> list[tuple[int, int, str]]:
    """Return a NEW heapified list of (head, turns, name) entries.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        A list rearranged so that entry 0 is the smallest by
        (head, turns, name). The rest of the list is heap order, not
        sorted order.
    """
    queue = [(head, turns, name) for name, head, turns in gates]
    heapq.heapify(queue)
    return queue


def peek_next(queue: list[tuple[int, int, str]]) -> str | None:
    """Return the name of the gate at the front of the queue, without removing it.

    Args:
        queue: A heapified queue from build_queue.

    Returns:
        The gate's name, or None when the queue is empty.
    """
    if not queue:
        return None
    return queue[0][2]


def drain_order(gates: list[tuple[str, int, int]]) -> list[str]:
    """Return every gate's name in the order the crew opens them.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        Names, lowest head first; ties by fewer turns, then by name A to Z.
    """
    queue = build_queue(gates)
    order = []
    while queue:
        _, _, name = heapq.heappop(queue)
        order.append(name)
    return order


def gates_below(gates: list[tuple[str, int, int]], limit_cm: int) -> list[str]:
    """Return the names of the gates whose head is under limit_cm, in service order.

    Stops as soon as the front of the queue reaches the limit, so the gates
    behind it are never removed.

    Args:
        gates: (name, head, turns) rows. This list is not modified.
        limit_cm: The head, in centimetres, at which the crew stops.

    Returns:
        Names in service order. Empty when the shallowest gate is already at
        or above the limit.
    """
    queue = build_queue(gates)
    picked = []
    while queue and queue[0][0] < limit_cm:
        _, _, name = heapq.heappop(queue)
        picked.append(name)
    return picked


# ---- Self-check ----
if __name__ == "__main__":
    queue = build_queue(GATES)
    print("heap layout:")
    for head, turns, name in queue:
        print(f"  {head:3d} cm  {turns} turns  {name}")

    print(f"front of the queue: {peek_next(queue)}")
    print(f"queue length after peeking: {len(queue)}")

    print("service order:")
    for position, name in enumerate(drain_order(GATES), 1):
        print(f"  {position}. {name}")

    print(f"under 25 cm: {gates_below(GATES, 25)}")
    print(f"under 5 cm: {gates_below(GATES, 5)}")
    print(f"front of an empty queue: {peek_next([])}")

    assert queue[0] == (8, 9, "Oude Dijk")
    assert len(queue) == 7
    assert peek_next(queue) == "Oude Dijk"
    assert drain_order(GATES)[:3] == ["Oude Dijk", "Noordkil", "Zwarte Sloot"]
    assert drain_order(GATES)[-1] == "Boezemsluis"
    assert drain_order(GATES).index("Kruisweg") < drain_order(GATES).index("Molenkade")
    assert gates_below(GATES, 25) == ["Oude Dijk", "Noordkil", "Zwarte Sloot", "Vaartbrug"]
    assert gates_below(GATES, 5) == []
    assert peek_next([]) is None
    assert GATES[0] == ("Molenkade", 41, 6)  # original rows untouched
    print("All checks passed.")
```

**The tuple is the rule, written down once.**

```python
queue = [(head, turns, name) for name, head, turns in gates]
```

Read the entry out loud and you get the board's rule: least head, then fewest
turns, then earliest name. Python compares two of these box by box and stops
at the first difference, so a three-part rule costs one comprehension and no
comparison function at all. Reshaping the row is the whole design decision on
this page — everything after it is three `heapq` calls.

**`heapify` is one pass, not a sort.** It walks the list from the middle
backwards, letting each item sink until its children are both larger. That is
`O(n)` work — cheaper than the `O(n log n)` a sort costs — and it buys you
exactly one promise: position 0 is the smallest. Pushing seven items one at a
time with `heappush` would cost `O(n log n)` and end up at the same place, so
when you already hold the whole list, `heapify` is the cheaper door in.

**The copy is not politeness, it is correctness.** `heapq.heapify` rearranges
the list object it is given. `build_queue` receives `GATES` itself, not a copy
of it. The comprehension makes a new list before `heapify` ever sees one, so
the board's rows survive. Notice that this falls out of the reshaping for
free: because the entries have to change shape anyway, the copy costs nothing
extra.

**`peek_next` reads, `drain_order` removes, and the difference is the point.**
`queue[0]` is a list index — instant, and it changes nothing. `heapq.heappop`
takes the front item out, moves the last item into the hole, and sinks it back
down to where it belongs, which costs one walk down the tree. Use the first
when you want to *ask*, the second when you want to *take*.

**`gates_below` is why a heap beats a sort here.** The loop stops the moment
the front of the queue reaches the limit. Four pops answered the question, and
the three deeper gates were never removed, never compared against each other,
never looked at. A sorted list would have put all seven in order first. That is
the shape of almost every heap problem: *the answer needs a prefix, so pay for
a prefix.*

**Both halves of `while queue and queue[0][0] < limit_cm` are load-bearing.**
Python stops evaluating an `and` as soon as the left half is false, so when the
queue empties, `queue[0][0]` is never reached. Write the halves the other way
round and the last turn of the loop raises `IndexError: list index out of
range` — on the run where every single gate was under the limit, which is
exactly the run a hurried tester does not try.

## Download and run

Download
[exercise-01-sluice-gate-order-solution.py](./exercise-01-sluice-gate-order-solution.py)
and run it:

```bash
python exercise-01-sluice-gate-order-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-sluice-gate-order.py`.

## Common bugs to catch

- **The service order comes out alphabetical.** You heaped the rows in the
  shape they arrived in:

  ```python
  queue = list(gates)
  heapq.heapify(queue)
  ```

  No exception — a tuple of `(name, head, turns)` compares perfectly well, it
  just compares the name first. In a REPL:

  ```text
  >>> heapq.heappop(queue)
  ('Boezemsluis', 62, 1)
  ```

  Sixty-two centimetres is the *deepest* gate there is. Any time a heap hands
  you an answer that looks alphabetical, look at box zero of your tuple.

- **`TypeError: 'NoneType' object is not iterable`.** You returned the result
  of `heapify`:

  ```text
  Traceback (most recent call last):
      for head, turns, name in queue:
                               ^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  `heapq.heapify` rearranges in place and hands back `None`, the same way
  `list.sort()` does. Heapify the list on one line, `return` it on the next.

- **`IndexError: index out of range` from inside `heapq`.** You popped an
  empty queue:

  ```text
  Traceback (most recent call last):
      _, _, name = heapq.heappop(queue)
                   ^^^^^^^^^^^^^^^^^^^^
  IndexError: index out of range
  ```

  Note the wording: `heapq` says `index out of range`, while indexing an empty
  list yourself says `list index out of range`. The extra word tells you which
  of the two you hit. Both mean the same thing here — check `if queue:` first.

- **`gates_below` returns every gate.** Your loop condition tests the wrong
  box, usually `queue[0] < limit_cm` instead of `queue[0][0] < limit_cm`.
  Comparing a whole tuple against an integer does raise, and the message names
  both types:

  ```text
  TypeError: '<' not supported between instances of 'tuple' and 'int'
  ```

  If instead you compared `queue[0][1] < limit_cm` you get no exception at all
  and a silently wrong answer, because box 1 is the number of turns and every
  gate turns fewer than 25 times.

- **`GATES` comes out reordered.** You wrote `heapq.heapify(gates)` on the
  argument itself. The function's return value can still look right, and every
  assert above the last one still passes — which is what makes this bug
  expensive. The row order the board gave you is now gone for every other
  function in the program.

- **You read `queue[1]` for the second gate.** There is no second-smallest at
  position 1. A heap of seven items promises exactly one thing, and this is the
  bug the printed layout in the expected output exists to inoculate you
  against. The second-smallest comes out of the second `heappop`, and nowhere
  else.

## Under the hood

<details>
<summary>Under the hood — how a list becomes a tree, and why heapify is cheaper than sorting</summary>

**The tree is imaginary; the list is real.**

There are no node objects in `heapq` and no pointers. The list *is* the tree,
by arithmetic: the children of position `i` live at `2i + 1` and `2i + 2`, and
the parent of position `i` lives at `(i - 1) // 2`. Position 0 is the root, so
position 0 is the smallest.

Draw the expected output's layout that way and it stops looking random:

```text
                (8, Oude Dijk)
           /                      \
   (17, Zwarte Sloot)        (17, Noordkil)
     /          \              /         \
(41, Molenkade) (23, Vaartbrug) (41, Kruisweg) (62, Boezemsluis)
```

Every parent is smaller than both of its children. That is the entire
invariant, and it says nothing at all about left-to-right order — which is why
`Zwarte Sloot` at 17 sits to the left of `Vaartbrug` at 23 while `Noordkil`,
also 17, sits over on the right.

**Why `heapify` costs `O(n)` and a sort costs `O(n log n)`.**

`heapify` starts at the last item that has children and works backwards,
sinking each one down until both its children are larger. The important detail
is that most items are near the bottom and barely sink at all. Half the items
are leaves and move zero steps; a quarter can move at most one step; an eighth
at most two. Add that up — `n/2 · 0 + n/4 · 1 + n/8 · 2 + …` — and the series
converges to less than `n`. Sorting cannot do that, because a sort has to place
every item relative to every other, not just relative to its own two children.

CPython's `heapq` is written in Python in `Lib/heapq.py` and then, on the
usual builds, quietly replaced by a C version from `_heapq` at the bottom of
the file. The Python one is worth reading precisely because it is short: the
whole module is about a page of real logic.

**Why the pop is `O(log n)`.**

`heappop` takes position 0, moves the *last* item of the list into the hole,
and sinks it back down. Sinking follows one root-to-leaf path, and a complete
binary tree of `n` items is `log₂ n` levels deep. Seven gates is three levels;
a million items is twenty. That is the whole reason the structure exists: the
cost of "give me the smallest, then keep the rest usable" barely grows.

**Where the wasted work in `sorted` actually goes.**

For `gates_below` with seven gates and a limit that four of them pass, sorting
does roughly `7 · log₂ 7 ≈ 20` comparisons, and the heap does about seven to
build plus a few per pop. At this size the difference is noise, and it is
honest to say so. Change the numbers to a hundred thousand assets with four
answers and the sort does about 1.7 million comparisons while the heap does
about a hundred thousand plus a handful. The pattern is worth learning at seven
so that you already have it at a hundred thousand.

**`heapq` has no `heappeek`, and that is deliberate.**

Reading `queue[0]` is a list index: one bounds check and one pointer fetch,
with no function call at all. A `heappeek` function would be slower than the
thing it wrapped. Some other languages' priority queues hide the array, so they
have to provide a `peek`; Python leaves the list in your hands and lets you
index it.

</details>

## Acceptance checklist

- [ ] `python exercise-01-sluice-gate-order.py` prints the layout, the service
      order, both prefix answers, then `All checks passed.`
- [ ] The printed heap layout matches the expected output line for line.
- [ ] `GATES` is in its original order after every function has run.
- [ ] `peek_next` never calls `heappop`, and the queue length is unchanged
      after it runs.
- [ ] `gates_below` stops early — it does not drain the queue and filter
      afterwards.
- [ ] Neither `sorted` nor `.sort()` appears anywhere in your four functions.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like
      `Add Week 8 exercise 1: sluice gate order`.

## Stretch

- **Add a gate to a queue that is already built.**

  ```python
  def add_gate(queue: list[tuple[int, int, str]], name: str, head: int, turns: int) -> None:
      """Push one more gate into an existing queue, keeping the heap valid."""
      heapq.heappush(queue, (head, turns, name))
  ```

  ```text
  before: Oude Dijk
  after adding Kleine Kil at 3 cm: Kleine Kil
  queue length: 8
  ```

  One push, one sift up the tree, and the front changes. This is the move that
  makes a heap a *queue* rather than a one-off ranking: things can arrive after
  you have started.

- **Answer "which is the worst gate?" and notice what it costs.**

  ```python
  def deepest_gate(gates: list[tuple[str, int, int]]) -> str:
      """Return the name of the gate with the greatest head."""
      return max(gates, key=lambda row: row[1])[0]
  ```

  ```text
  deepest: Boezemsluis
  ```

  A min-heap is the wrong tool for this and `max` is the right one. The heap
  knows where its smallest item is and genuinely does not know where its
  largest one is — it could be anywhere in the bottom half of the list.
  Exercise 3 is about what to do when the *largest* is the one you keep asking
  for.

- **Count the pops that `gates_below` saves.**

  ```python
  def pops_used(gates: list[tuple[str, int, int]], limit_cm: int) -> tuple[int, int]:
      """Return (pops made, pops a full drain would have made)."""
      return len(gates_below(gates, limit_cm)), len(gates)
  ```

  ```text
  limit  25 cm: 4 pops instead of 7
  limit   5 cm: 0 pops instead of 7
  limit 100 cm: 7 pops instead of 7
  ```

  The third line is the honest one. When the limit lets everything through, the
  heap saves nothing and the sort would have been just as good. Knowing when
  your tool stops helping is worth as much as knowing when it helps.

---
When your queue drains in the right order, move on to
[Exercise 2 — Crest Watch Shortlist](./exercise-02-crest-watch-shortlist.md).
