# Exercise 4 — Cable Pull

> **Topic:** the same search on a network big enough to punish the wrong queue
> **Lecture:** [01 — The BFS Template](../lecture-notes/01-the-bfs-template.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** every page so far has been small enough that a list used as a queue would have worked fine. That is exactly why nobody learns the lesson on small pages. Twenty thousand junction boxes is where `list.pop(0)` starts costing real time, and this page makes you count the cost instead of taking it on trust.

## The Brief

A tower block has cable trays running between junction boxes. An electrician
standing at the head end wants to know two things before ordering cable: how
many trays the longest pull has to cross, and which box is on the end of it.

The network is a dictionary, the same shape as Exercise 1's mesh, except
trays run both ways — if box A shares a tray with box B, then B shares one
with A. Twenty thousand boxes, labelled `J00000` upward.

You are not asked to invent the network. `tray_manifest` is given to you and
builds it from the as-built drawings: two trays leave every box, feeding the
boxes numbered `2n + 1` and `2n + 2`, and on top of that the electricians ran
a **cross tie** from every thirteenth box to the box seven along. The cross
ties are what turn a tidy branching riser into a real graph with loops in it,
and they are why `J00007` is one tray from the head rather than three.

Now the part this page is really about.

A queue is a line at a counter. `collections.deque` is Python's queue, and
taking the front item off is one operation however long the line is. A plain
list can be used as a queue with `pop(0)`, and it will give you the same
answer — but a list keeps its items in a row in memory, so removing the front
one means **sliding every other item one place left**. A queue of five
thousand costs five thousand slides. Do that twenty thousand times and the
slides are the program.

So the survey reports a fifth number: **how many element shifts a list-backed
queue would have performed**. You compute it without ever doing them, by
adding up the length of the queue behind each box as it comes off the front.
That number is the reason for the rule, written down.

The rest of the contract:

- `tray_hops` returns a dictionary of label to tray count, `head` at `0`.
  Boxes on another island of the network — there are none in this manifest,
  but the function must not assume that — are simply absent.
- `survey` returns a `Survey` record: how many boxes were reached, the
  largest tray count, the furthest box, how many boxes share that count, and
  the shift figure.
- Two boxes can tie for furthest. Twelve hundred and fifty-seven of them do.
  The **lowest label wins**, so two people running the survey get the same
  answer.
- A `head` that is not in the manifest raises `ValueError`.

## Starter

Create `exercise-04-cable-pull.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""exercise-04-cable-pull.py — surveying twenty thousand junction boxes.

A tower's cable trays run between junction boxes. An electrician standing at
the head end wants to know how many trays a pull has to cross to reach the
furthest box, and which box that is. Twenty thousand boxes is enough that the
choice of queue stops being a matter of taste.

The survey also reports how many times a list-backed queue would have shifted
an element along, which is the work `deque` does not do.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
BOX_COUNT = 20_000
HEAD = "J00000"


class Survey(NamedTuple):
    """What a completed survey of the tray network reports."""

    boxes: int
    deepest: int
    furthest: str
    at_deepest: int
    list_shifts: int


def label(number: int) -> str:
    """Return the stencilled label for a junction box.

    Args:
        number: The box's number, counting from zero at the head end.

    Returns:
        The label as it is painted on the box, e.g. `J00042`.
    """
    return f"J{number:05d}"


def tray_manifest(count: int = BOX_COUNT) -> dict[str, list[str]]:
    """Build the as-built tray manifest for a riser of `count` boxes.

    Two trays leave every box, feeding boxes `2n+1` and `2n+2`. On top of
    that the electricians ran a cross tie from every thirteenth box to the
    box seven along, which is what turns the riser from a tree into a graph.

    Args:
        count: How many junction boxes the riser has.

    Returns:
        The manifest: each label mapped to the labels it shares a tray with.
        Trays run both ways, so every tie appears in both entries.
    """
    trays: dict[str, list[str]] = {label(n): [] for n in range(count)}

    def tie(one: int, other: int) -> None:
        trays[label(one)].append(label(other))
        trays[label(other)].append(label(one))

    for number in range(count):
        for onward in (2 * number + 1, 2 * number + 2):
            if onward < count:
                tie(number, onward)
        if number % 13 == 0 and number + 7 < count:
            tie(number, number + 7)
    return trays


# ---- Your task ----
def tray_hops(trays: dict[str, list[str]], head: str) -> dict[str, int]:
    """Return how many trays a pull crosses from `head` to every box it reaches.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        A dict mapping each reachable label to its tray count. `head` maps
        to 0.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    # TODO: raise ValueError when head is not in the manifest
    # TODO: hops = {head: 0} — this dict is also the reached set
    # TODO: the usual loop, with a deque
    ...


def list_queue_shifts(trays: dict[str, list[str]], head: str) -> int:
    """Return the element shifts a list-backed queue would perform.

    `list.pop(0)` has to slide every remaining element one place to the left.
    This counts those slides without ever doing them, by adding up the length
    of the queue behind each box as it comes off the front.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        The total number of element shifts. A `deque` performs none of them.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    # TODO: the same walk, with `shifts += len(queue) - 1` before each pop
    ...


def survey(trays: dict[str, list[str]], head: str) -> Survey:
    """Return the full survey of the riser from `head`.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        A `Survey`: how many boxes were reached, the largest tray count, the
        furthest box (lowest label wins a tie), how many boxes share that
        count, and the shifts a list-backed queue would have performed.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    # TODO: one call to tray_hops, then max / count / min over its items
    ...


# ---- Self-check ----
if __name__ == "__main__":
    trays = tray_manifest()
    report = survey(trays, HEAD)
    print(f"boxes reached      : {report.boxes}")
    print(f"deepest tray count : {report.deepest}")
    print(f"furthest box       : {report.furthest}")
    print(f"boxes that deep    : {report.at_deepest}")
    print(f"list pop(0) shifts : {report.list_shifts:,}")
    print(f"deque popleft shifts: 0")

    assert report.boxes == BOX_COUNT  # every box is reachable from the head
    assert report.deepest == 14
    assert report.furthest == "J18447"
    assert report.at_deepest == 1257
    assert report.list_shifts == 97_108_042

    hops = tray_hops(trays, HEAD)
    assert hops[HEAD] == 0
    assert hops["J00001"] == 1 and hops["J00002"] == 1
    assert hops["J00007"] == 1  # the cross tie from box 0, not three trays down
    assert hops["J00008"] == 3  # no cross tie helps here: 0 - 1 - 3 - 8

    try:
        tray_hops(trays, "J99999")
    except ValueError as error:
        assert "not a box on this riser" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("All checks passed.")
```

Two ideas before you start.

**Why `pop(0)` is slow and `pop()` is not.** A list keeps its items in one
unbroken run of memory. Removing the *last* one is free — nothing else moves.
Removing the *first* one means every remaining item has to shuffle down one
place to close the gap. A `deque` is built differently: it is a chain of
small blocks, and it keeps a handle on both ends, so taking from either end
touches nothing else.

**One dictionary, two jobs.** `hops` maps a label to its tray count, and a
label is in it exactly when it has been queued. So `if neighbour not in hops`
is the reached check, and there is no separate `set`. Fewer structures, fewer
ways to disagree.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/exercises/exercise-04-cable-pull.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `tray_hops` returns a `dict[str, int]` with `head` mapped to `0`.
2. Every box in the manifest that a pull can reach appears exactly once in
   that dict, with the smallest number of trays it takes to reach it.
3. `tray_hops` and `list_queue_shifts` both raise `ValueError` for a head
   that is not in the manifest, and the message contains
   `not a box on this riser`.
4. `list_queue_shifts` returns the total of `len(queue) - 1` measured
   immediately before each removal, over the same walk.
5. `survey` returns a `Survey` with all five fields filled in.
6. `survey(...).furthest` is the **lowest** label among the boxes at the
   deepest count.
7. `survey` walks the network with `tray_hops` rather than repeating the
   search inside itself.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Use `collections.deque`. This is the page where it stops being advice.**
  Twenty thousand removals from the front of a list would move roughly
  ninety-seven million elements. The `deque` moves none. Both give the same
  answer; only one of them does it in a time you would sit through.

- **Do not build the network yourself.** `tray_manifest` is given. If your
  numbers do not match the expected output, the bug is in your search, and
  editing the manifest to make the numbers agree is how a broken search gets
  shipped.

- **Use `hops` as the reached set.** A second `set` holding the same labels
  is a second copy of the same fact and doubles the memory for nothing.
  `label in hops` is exactly as fast as `label in seen`, because a dict and a
  set are the same lookup underneath.

- **Break the tie with `min`, not by sorting.** `min(...)` walks the
  candidates once holding the best so far. Sorting twelve hundred labels to
  read the first and throw away the rest does about ten times the work for
  the same answer, and it says something untrue about what you wanted.

- **`survey` calls `tray_hops`; it does not re-implement it.** The moment two
  functions both claim to know how the walk works, one of them will
  eventually be wrong, and it will be the one nobody is looking at.

- **`list_queue_shifts` must not actually perform the shifts.** Counting
  `len(queue) - 1` before each removal is exact and instant. Running a real
  list-backed search to measure it would take about fifty times as long and
  tell you the same number — which is the point of the page, but it is a
  thing to demonstrate in the stretch, not to leave in the shipped program.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
@@OUTPUT@@
```

Ninety-seven million shifts. That is the work a list-backed queue would have
done and a `deque` did not, on a network you can hold in your head.

Here is the same walk timed both ways on the same machine, same Python,
same manifest — the only difference is `deque` and `popleft` against `list`
and `pop(0)`:

```text
deque: 4.8 ms
list : 216.4 ms
```

Forty-five times slower for an identical answer. And that ratio is not
fixed — it grows with the size of the network, because the shifts grow with
the square of the number of boxes while the useful work grows only in step
with it. Double the riser and the gap roughly doubles again.

Look at `J00007` too, which is one tray from the head. On the branching
pattern alone it would be three: 0 to 1, 1 to 3, 3 to 7. The cross tie from
box 0 is what makes it one, and it is the reason this network is worth
searching rather than calculating.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first use
   of a result.
2. Write `tray_hops` with a `deque`. Run it against a small manifest first:
   `tray_manifest(15)`, then print the whole dict. Fifteen entries, counts
   from 0 to 3, and you can check every one by hand against the rule.
3. Move up to the full twenty thousand. It should finish in well under a
   second. If it does not, look at your queue's type.
4. Write `list_queue_shifts`. It is `tray_hops` with the answer thrown away
   and one extra line. Resist the urge to merge them: they measure different
   things and one of them is a teaching aid.
5. Write `survey`. Three one-line expressions over `hops.items()` and a
   fourth call for the shifts.
6. Get the tie-break right. Print
   `sorted(box for box, n in hops.items() if n == 14)[:5]` and check that the
   first of those is what `survey` returned.
7. Now do the experiment. Copy `tray_hops` into a scratch file, change
   `deque` to a list and `popleft()` to `pop(0)`, and time both with
   `timeit`. The stretch section has the code. Write your own two numbers in
   your notes — the ones from your machine, not the ones on this page.

## The Solution

```python
@@CODE@@
```

**The walk itself is Exercise 1's walk, with the hops carried in a dict.**

```python
if neighbour not in hops:
    hops[neighbour] = hops[box] + 1
    queue.append(neighbour)
```

Three lines that always travel together, in that order. The dict entry is
written at the moment of queueing, which is what makes `not in hops` the
reached check as well as the answer. Write it after the pop instead and boxes
go into the queue several times over — a box in this manifest has up to four
trays, so up to four copies.

**Why `hops` is also the reached set, and why that is safe.** The only thing
that ever writes to `hops` is the line above, and it only runs when the label
is absent. So a box's count is written once, at the moment it is first
reached, and the queue's order guarantees that first reach is the shortest
pull. Nothing later can overwrite it, because nothing later passes the test.

**The shift count is the definition of `pop(0)`, not a simulation of it.**

```python
shifts += len(queue) - 1  # what pop(0) would have had to slide
```

When a list has `n` items and you remove the first, the other `n - 1` slide
down one place. Measuring `len(queue)` immediately before the removal and
subtracting one gives that number exactly, for that removal. Sum it over the
walk and you have the total. No timing, no variance, no machine dependence:
the same number every run, on any computer.

Ninety-seven million is not an estimate. It is a count.

**Where ninety-seven million comes from.** The queue in this walk holds one
level of the riser at a time, and the levels roughly double in size. The
biggest level holds several thousand boxes, and every box popped while the
queue is that long pays several thousand shifts. Roughly, a search over `n`
boxes on a wide network does work in step with `n²` when the queue is a list,
and in step with `n` when it is a `deque`. That is why the ratio grows: at
twenty thousand it is forty-five times; at two hundred thousand it would be
several hundred.

**`min` and `max` are one pass each, and `min` is doing the tie-break.**

```python
furthest = min(box for box, count in hops.items() if count == deepest)
```

`min` over strings compares them alphabetically, and the labels are
zero-padded to five digits on purpose, so alphabetical order and numeric
order are the same thing. That padding is not decoration; without it
`J9` would sort before `J10` and the tie-break would be nonsense.

**`Survey` is a `NamedTuple`, not five loose values.** The caller writes
`report.deepest` rather than `report[1]`, and a field added later does not
silently shift everything after it. It is also self-documenting at the point
of use, which matters more the more numbers a function hands back.

## Download and run

Download
[exercise-04-cable-pull-solution.py](./exercise-04-cable-pull-solution.py)
and run it:

```bash
python exercise-04-cable-pull-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-04-cable-pull.py`.

## Common bugs to catch

- **The program takes several seconds instead of a fraction of one.** No
  exception; it finishes and the answer is right. Your queue is a list. Time
  it and compare against the two numbers in the expected output section. This
  is the whole page: the wrong data structure does not fail, it just costs.

- **`AttributeError: 'list' object has no attribute 'popleft'`.**

  ```text
  Traceback (most recent call last):
      queue.popleft()
      ^^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  You changed the queue's type and not the method. This is the *good* version
  of the bug, because it stops you.

- **`TypeError: deque.pop() takes no arguments (1 given)`.** The mirror
  image — a `deque` asked for `pop(0)`:

  ```text
  Traceback (most recent call last):
      q.pop(0)
      ~~~~~^^^
  TypeError: deque.pop() takes no arguments (1 given)
  ```

  `deque.pop()` takes from the *right*. The left-hand one is `popleft()`, and
  the fact that it refuses an index at all is the library telling you that
  indexing into a queue is not a thing you want.

- **The program never finishes and memory climbs.** You wrote
  `hops[neighbour] = ...` after popping rather than before queueing, or you
  left the reached check out entirely. The cross ties make loops, and a walk
  with no reached check on a graph with a loop in it does not terminate.

- **`report.at_deepest` is 1 when it should be 1257.** You counted the boxes
  whose label equals `furthest` instead of the boxes whose count equals
  `deepest`. Two different questions, one letter apart in the code.

- **`furthest` comes back as `J9999` or similar on your own test manifest.**
  You built labels without padding. `min` on strings is alphabetical, so
  `"J10"` sorts before `"J9"`. Keep the `:05d`.

- **`KeyError: 'J00003'`.**

  ```text
  Traceback (most recent call last):
      print(hops["b"])
          ~~~~^^^^^
  KeyError: 'b'
  ```

  You read `hops[label]` for a box the walk never reached. On this manifest
  every box is reachable so it cannot happen — but the function does not
  promise that, and a manifest with an island in it would produce exactly
  this. Use `.get` when you are asking about a box you have not proved is
  there.

## Under the hood

<details>
<summary>Under the hood — what a deque actually is, and where the quadratic comes from</summary>

**A list is one block; a deque is a chain of blocks.**

CPython's `list` is an array of pointers in one contiguous run of memory.
`pop(0)` calls `memmove` to shift the remaining pointers down one slot.
`memmove` is written in C and is genuinely fast per byte — which is precisely
why the bug survives so long. A single `pop(0)` on a five-thousand-item list
takes a few microseconds. It feels free. Twenty thousand of them do not.

`collections.deque` is a doubly linked list of fixed-size blocks, each
holding up to 64 pointers, with the head and tail blocks tracked directly.
`popleft` reads one pointer and advances an index; when a block empties it is
unlinked. Nothing else moves, ever. Both ends are cheap and the middle is
not — `some_deque[5000]` has to walk the chain, which is the trade you accept
in return.

**Where the `n²` comes from.** Say the walk pops `n` boxes, and the queue
averages `q` items while that happens. The shifts total about `n × q`. On a
network whose levels grow — a riser, a tree, most real graphs — the last few
levels hold a constant fraction of every box, so `q` is itself in step with
`n`. That makes the shifts in step with `n²`. Twenty thousand boxes gives
ninety-seven million, and `20000²` is four hundred million, so the constant
here is about a quarter. Close enough to feel the shape.

**The other `pop(0)` in disguise.** `list.insert(0, x)` has the same cost for
the same reason, and `del some_list[0]` and `some_list[1:]` do too. Any
operation that changes the front of a list is linear in the list's length.
The rule that covers all of them: *lists are cheap at the end and expensive
at the start.*

**When a list really is fine.** Depth-first search uses a stack, not a queue,
and a stack takes from the end — `append` and `pop()` with no argument. Those
are both cheap on a list, and a `deque` would buy nothing. So the advice is
not "always use `deque`"; it is "match the structure to the end you take
from". Next week's search is the one where a list is the right answer.

**Why the shift count is worth reporting at all.** Timings vary by machine,
by Python build, by what else is running. A count does not. When you want to
prove a complexity claim to somebody — or to yourself, six months later — a
deterministic operation count is stronger evidence than a stopwatch, and it
does not need the slow version to exist.

</details>

## Acceptance checklist

- [ ] `python exercise-04-cable-pull.py` prints six lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] It finishes in well under a second.
- [ ] `collections.deque` is used; there is no `pop(0)` anywhere in the file.
- [ ] `hops` is the only reached-tracking structure — no separate `set`.
- [ ] `survey` calls `tray_hops` rather than searching again.
- [ ] The tie for furthest box is broken with `min`, not by sorting.
- [ ] `tray_hops(trays, "J99999")` raises `ValueError`.
- [ ] Every function has type hints and a docstring.
- [ ] You have timed both queues yourself and written down your own numbers.
- [ ] Committed to Git with a message like `Add Week 6 exercise 4: cable pull`.

## Stretch

- **Time both queues yourself.** Do not take the page's word for it.

  ```python
  import timeit
  from collections import deque

  def with_list(trays: dict[str, list[str]], head: str) -> dict[str, int]:
      """The same walk, with the wrong queue."""
      hops = {head: 0}
      queue = [head]
      while queue:
          box = queue.pop(0)
          for neighbour in trays[box]:
              if neighbour not in hops:
                  hops[neighbour] = hops[box] + 1
                  queue.append(neighbour)
      return hops

  trays = tray_manifest()
  for name, fn in (("deque", tray_hops), ("list ", with_list)):
      best = min(timeit.repeat(lambda: fn(trays, HEAD), number=1, repeat=5))
      print(f"{name}: {best * 1000:.1f} ms")
  ```

  ```text
  deque: 4.8 ms
  list : 216.4 ms
  ```

  Then assert the two agree — `with_list(trays, HEAD) == tray_hops(trays, HEAD)`
  — because the whole point is that the slow one is *not* wrong.

- **Watch the ratio grow.** Run the pair at four sizes and look at the shape.

  ```python
  for size in (2_500, 5_000, 10_000, 20_000):
      trays = tray_manifest(size)
      print(f"{size:>6}: {list_queue_shifts(trays, HEAD):>12,} shifts")
  ```

  ```text
    2500:    1,516,020 shifts
    5000:    6,067,018 shifts
   10000:   24,274,018 shifts
   20000:   97,108,042 shifts
  ```

  Double the network, quadruple the shifts. That is what "in step with `n²`"
  looks like when you can see it rather than being told it.

- **Find the widest level.** The largest number of boxes the queue ever holds
  at once, which is the memory the search really costs.

  ```python
  def widest_level(trays: dict[str, list[str]], head: str) -> tuple[int, int]:
      """Return the deepest queue length and the tray count where it happened."""
      hops = {head: 0}
      queue = deque([head])
      widest, at_count = 1, 0
      while queue:
          if len(queue) > widest:
              widest, at_count = len(queue), hops[queue[0]]
          box = queue.popleft()
          for neighbour in trays[box]:
              if neighbour not in hops:
                  hops[neighbour] = hops[box] + 1
                  queue.append(neighbour)
      return widest, at_count
  ```

  ```text
  (9216, 12)
  ```

  Nine thousand boxes in the queue at once, twelve trays from the head. That is the number a list-backed queue was sliding, over and over.

When your survey is right, move on to
[Exercise 5 — Feeder Tier Load](./exercise-05-feeder-tier-load.md).
