# Exercise 2 — Conveyor Reachability

> **Topic:** depth-first search with the pending work held in a list you can see, instead of on Python's call stack
> **Lecture:** [02 — Iterative DFS](../lecture-notes/02-iterative-dfs.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** this is the page where recursion stops being free. CPython lets a function call itself about a thousand times deep and then refuses, and a depot's belt run is far longer than a thousand. You will see the real exception, you will see what happens when you try to buy your way out of it by raising the limit, and you will write the version that has no limit to raise. Everything after this — the loop audit, both challenges, the mini-project — keeps its pending work in a list because of what this page shows you.

## The Brief

A parcel depot is a building full of chutes and belts.

A **chute** is a hole a parcel drops through. A **belt** is a one-way conveyor
from one chute to another. One-way matters: a belt from chute 3 to chute 7
carries parcels from 3 to 7 and never the other way, the same way a slide only
goes down.

The chutes are numbered `0`, `1`, `2` and so on. The depot's wiring is written
as a list of lists called `belts`, where `belts[i]` is the chutes a parcel can
drop to directly from chute `i`:

```python
belts = [
    [1, 2],   # from chute 0 a parcel can drop to chute 1 or chute 2
    [3],      # from chute 1 it can only drop to chute 3
    [3, 4],   # from chute 2 it can drop to chute 3 or chute 4
    [],       # chute 3 is a dead end - nothing leaves it
    [],       # so is chute 4
]
```

The night supervisor wants one thing: **release a parcel at chute `start` and
tell me every chute it could possibly end up at.** Not the route. Not the
shortest way. Just the full set of places it could get to, sorted smallest
first.

That is a graph walk, and depth-first search is the natural tool. Depth-first
means: take one belt, follow it as far as it goes, and only when that arm runs
out come back and try the next one. A **visited set** — a set of chute numbers
you have already been to — is what stops the walk going round forever, because
depots really do have re-sort loops in them, where a parcel that misses its
gate is put back on an earlier belt to go round again.

One detail in the contract is chosen to catch a lazy answer. **The starting
chute is in the answer only if some belt path actually leads back to it.** Drop
a parcel into chute 0 of the depot above and it can never return to chute 0, so
`0` is not in the answer. Drop one into a re-sort loop and it can, so it is.
The obvious wrong implementation — put `start` in the visited set, walk, then
return the visited set — gets this wrong every single time and looks completely
reasonable while doing it.

And one detail is chosen to break recursion. A real depot's longest single belt
run is tens of thousands of chutes. The self-check on this page uses sixty
thousand. Python's ordinary way of writing this walk — a function that calls
itself — gives up at about a thousand.

## Starter

Create `exercise-02-conveyor-reachability.py` in your practice repo and paste
this in. Fill in the one `TODO`.

```python
"""exercise-02-conveyor-reachability.py — where a parcel can end up.

Walk the belts out of one chute and report everywhere a parcel could land.
The walk must survive a belt run sixty thousand chutes long, so the pending
work goes in a list, not on the call stack.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

# ---- Given data ----
FAN_OUT: list[list[int]] = [
    [1, 2],
    [3],
    [3, 4],
    [],
    [],
]

RESORT_LOOP: list[list[int]] = [
    [1],
    [2],
    [0],
]

DEAD_ENDS: list[list[int]] = [
    [1],
    [],
    [1],
]


def straight_run(chutes: int) -> list[list[int]]:
    """Build a depot that is one straight belt run, chute 0 down to the last.

    Args:
        chutes: How many chutes the run holds.

    Returns:
        A belt table where chute i drops to chute i + 1 and the last is a
        dead end.
    """
    belts: list[list[int]] = [[index + 1] for index in range(chutes - 1)]
    belts.append([])
    return belts


# ---- Your task ----
def reachable_chutes(belts: list[list[int]], start: int) -> list[int]:
    """Return every chute a parcel released at `start` can end up at.

    Args:
        belts: `belts[i]` lists the chutes a parcel drops to directly from
            chute i. One-way: a belt from i to j says nothing about j to i.
        start: The chute the parcel is released into.

    Returns:
        The reachable chute numbers, sorted ascending. `start` is in the list
        only when some belt path leads back to it. An empty depot gives an
        empty list.

    Raises:
        ValueError: If `start` is not a chute in this depot.
    """
    # TODO: refuse an impossible start, then walk with an explicit stack.
    # Seed the stack with the chutes leaving `start` - not with `start`.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty depot         : {reachable_chutes([], 0)}")
    print(f"fan-out from 0      : {reachable_chutes(FAN_OUT, 0)}")
    print(f"fan-out from 2      : {reachable_chutes(FAN_OUT, 2)}")
    print(f"dead end at chute 1 : {reachable_chutes(DEAD_ENDS, 1)}")
    print(f"re-sort loop from 0 : {reachable_chutes(RESORT_LOOP, 0)}")
    try:
        reachable_chutes(FAN_OUT, 9)
    except ValueError as refusal:
        print(f"chute 9 refused     : {refusal}")

    long_depot = straight_run(60_000)
    far = reachable_chutes(long_depot, 0)
    print(f"60000-chute run     : {len(far)} chutes, first {far[0]}, last {far[-1]}")

    assert reachable_chutes([], 0) == []
    assert reachable_chutes(FAN_OUT, 0) == [1, 2, 3, 4]
    assert reachable_chutes(FAN_OUT, 2) == [3, 4]
    assert reachable_chutes(FAN_OUT, 3) == []
    assert reachable_chutes(DEAD_ENDS, 1) == []
    assert reachable_chutes(DEAD_ENDS, 2) == [1]
    assert reachable_chutes(RESORT_LOOP, 0) == [0, 1, 2]
    assert reachable_chutes(RESORT_LOOP, 1) == [0, 1, 2]
    assert far == list(range(1, 60_000))
    assert reachable_chutes(long_depot, 59_999) == []
    for bad_start in (-1, 5):
        try:
            reachable_chutes(FAN_OUT, bad_start)
        except ValueError as refusal:
            assert str(refusal).startswith(f"no such chute: {bad_start}")
        else:
            raise AssertionError(f"chute {bad_start} should have been refused")
    print("All checks passed.")
```

Four words you need before you start.

**Stack.** A stack is a pile you add to and take from at the same end — the
last thing in is the first thing out. A Python list is already a stack:
`.append(x)` puts one on top, `.pop()` takes the top one off. That is all the
data structure this exercise needs.

**Call stack.** When a function calls another function, Python has to remember
where to come back to. It keeps those notes in a pile of its own, called the
call stack, and each note is a **frame**. Recursion is a function calling
itself, so a recursion a thousand deep means a thousand frames. Python puts a
ceiling on that pile on purpose, and the ceiling is the whole subject of this
page.

**Explicit stack.** "Explicit" here just means *written down where you can see
it*. Instead of letting Python keep the pile of unfinished work for you, you
keep it yourself in an ordinary list. Same walk, same answer, same cost — but
now the pile is data in memory rather than frames in the interpreter, and there
is no ceiling on it.

**Reachable.** Chute `b` is reachable from chute `a` if there is some run of
belts leading from `a` to `b`. One belt or twenty, it makes no difference to
the question.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/exercises/exercise-02-conveyor-reachability.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `reachable_chutes(belts, start)` returns a sorted list of every chute
   reachable from `start` by one or more belts.
2. `start` appears in that list **only** when some belt path returns to it.
   `reachable_chutes(FAN_OUT, 0)` is `[1, 2, 3, 4]`, with no `0`.
   `reachable_chutes(RESORT_LOOP, 0)` is `[0, 1, 2]`, with a `0`.
3. `reachable_chutes([], 0)` returns `[]` and raises nothing. An empty depot
   has no chutes to complain about.
4. A `start` outside `0` to `len(belts) - 1` raises `ValueError`, and the
   message names the offending chute — `no such chute: 9 (this depot has
   chutes 0 to 4)`.
5. The walk keeps its pending work in a list. No function in your answer calls
   itself, and nothing touches `sys.setrecursionlimit`.
6. A dead-end chute returns `[]`, not `None`.
7. The function keeps its type hints and its docstring.

## Constraints

- **Up to 60,000 chutes, and the longest belt run can use all of them.** That
  number is not decoration. CPython's default recursion limit is 1,000 frames,
  so a run of 60,000 is sixty times past the point where the recursive spelling
  of this walk stops working. The bound is here to make the recursive answer
  fail, loudly, on a case the self-check actually runs.

- **Belts may lead back to chutes you have already left.** A re-sort loop —
  where a parcel that missed its gate is put back on an earlier belt — is
  ordinary depot equipment, not a corner case. So the visited set is not an
  optimisation you add for speed. Without it the walk never ends.

- **Check `start` before you use it, and say what was wrong.** `belts[9]` on a
  five-chute depot raises `IndexError: list index out of range`, which tells
  the caller nothing about chutes. A `ValueError` naming the chute and the
  legal range is the difference between an error somebody can fix and an error
  somebody has to debug.

- **Seed the stack with `belts[start]`, never with `start`.** This is the whole
  of requirement 2, and it is one line. Push the chutes *leaving* the start and
  the start only ever gets marked if a belt genuinely arrives back at it.

- **Mark a chute as reached when you pop it, not when you push it — or check
  for it when you pop.** Both disciplines work; what does not work is neither.
  The shipped answer pushes freely and skips already-reached chutes on the way
  out, which costs a little more memory in the stack and is much harder to get
  wrong. Lecture 2 §6 walks through the version that marks on push.

- **`O(V + E)`.** One look at every chute and one look at every belt, and then
  it is done — 60,000 chutes and their belts, once each. There is no cheaper
  answer, because you cannot know a chute is unreachable without having failed
  to reach it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-conveyor-reachability-solution.py
empty depot         : []
fan-out from 0      : [1, 2, 3, 4]
fan-out from 2      : [3, 4]
dead end at chute 1 : []
re-sort loop from 0 : [0, 1, 2]
chute 9 refused     : no such chute: 9 (this depot has chutes 0 to 4)
60000-chute run     : 59999 chutes, first 1, last 59999
All checks passed.
```

Read the third line and the fifth line together. Starting at chute 2 of the
fan-out depot gives `[3, 4]` with no `2` in it, and starting at chute 0 of the
re-sort loop gives `[0, 1, 2]` *with* the `0`. Same function, same rule: the
start is in the answer when a belt gets back to it, and only then.

The last line is the one that matters most. Fifty-nine thousand nine hundred
and ninety-nine chutes reached from a single release, in a fraction of a
second, on a walk that would need sixty thousand nested function calls if you
had written it the ordinary way.

## Steps

1. Create the file, paste the starter, and run it. Five report lines print
   `None`, and then the run stops with
   `TypeError: object of type 'NoneType' has no len()`. That is the correct
   starting point, not a problem — an unfinished function hands back `None`,
   an f-slot will happily print `None`, and the first line that does real work
   with the result is where it falls over.
2. **Write the recursive version first, on purpose.** Six lines: a helper that
   takes a chute, loops over `belts[chute]`, and calls itself for any chute not
   yet in `reached`. Run it. Everything passes until the 60,000-chute check,
   and then you get the exception in *Common bugs to catch*. Read it before you
   read anything else on this page.
3. Now try to buy your way out. Put `sys.setrecursionlimit(200_000)` at the top
   and run it again. On a recent CPython it will very probably work — and that
   is the trap, not the fix. *Common bugs to catch* explains why.
4. Delete both and write the explicit-stack version. Start with a list holding
   the chutes leaving `start`. While it is not empty: pop one, skip it if it is
   already reached, mark it, and push everything leaving it.
5. Run the small cases and check requirement 2 by hand. `FAN_OUT` from `0` must
   not contain `0`; `RESORT_LOOP` from `0` must.
6. Add the `start` check. Test both `-1` and a number too big — `-1` is the one
   people forget, because `belts[-1]` is perfectly legal Python and silently
   walks from the *last* chute.
7. Run the whole file. When `All checks passed.` prints, open a REPL with
   `python -i exercise-02-conveyor-reachability.py` and print the stack's length
   inside the loop on a depot you invent. Watching it grow and shrink is the
   fastest way to believe that the list really is doing what the frames did.

## The Solution

```python
"""exercise-02-conveyor-reachability-solution.py — where a parcel can end up.

Iterative depth-first search with an explicit stack. The pending work lives in
a plain list on the heap, so the depot's longest belt run — sixty thousand
chutes in the self-check below — costs memory and nothing else. The recursive
spelling of the same walk dies at about a thousand chutes with RecursionError.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
FAN_OUT: list[list[int]] = [
    [1, 2],
    [3],
    [3, 4],
    [],
    [],
]

RESORT_LOOP: list[list[int]] = [
    [1],
    [2],
    [0],
]

DEAD_ENDS: list[list[int]] = [
    [1],
    [],
    [1],
]


def straight_run(chutes: int) -> list[list[int]]:
    """Build a depot that is one straight belt run, chute 0 down to the last.

    Args:
        chutes: How many chutes the run holds.

    Returns:
        A belt table where chute i drops to chute i + 1 and the last is a
        dead end.
    """
    belts: list[list[int]] = [[index + 1] for index in range(chutes - 1)]
    belts.append([])
    return belts


# ---- Your task ----
def reachable_chutes(belts: list[list[int]], start: int) -> list[int]:
    """Return every chute a parcel released at `start` can end up at.

    Args:
        belts: `belts[i]` lists the chutes a parcel drops to directly from
            chute i. One-way: a belt from i to j says nothing about j to i.
        start: The chute the parcel is released into.

    Returns:
        The reachable chute numbers, sorted ascending. `start` is in the list
        only when some belt path leads back to it. An empty depot gives an
        empty list.

    Raises:
        ValueError: If `start` is not a chute in this depot.
    """
    if not belts:
        return []
    if not 0 <= start < len(belts):
        raise ValueError(
            f"no such chute: {start} (this depot has chutes 0 to {len(belts) - 1})"
        )

    reached: set[int] = set()
    stack: list[int] = list(belts[start])
    while stack:
        chute = stack.pop()
        if chute in reached:
            continue
        reached.add(chute)
        stack.extend(belts[chute])
    return sorted(reached)


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty depot         : {reachable_chutes([], 0)}")
    print(f"fan-out from 0      : {reachable_chutes(FAN_OUT, 0)}")
    print(f"fan-out from 2      : {reachable_chutes(FAN_OUT, 2)}")
    print(f"dead end at chute 1 : {reachable_chutes(DEAD_ENDS, 1)}")
    print(f"re-sort loop from 0 : {reachable_chutes(RESORT_LOOP, 0)}")
    try:
        reachable_chutes(FAN_OUT, 9)
    except ValueError as refusal:
        print(f"chute 9 refused     : {refusal}")

    long_depot = straight_run(60_000)
    far = reachable_chutes(long_depot, 0)
    print(f"60000-chute run     : {len(far)} chutes, first {far[0]}, last {far[-1]}")

    assert reachable_chutes([], 0) == []
    assert reachable_chutes(FAN_OUT, 0) == [1, 2, 3, 4]
    assert reachable_chutes(FAN_OUT, 2) == [3, 4]
    assert reachable_chutes(FAN_OUT, 3) == []
    assert reachable_chutes(DEAD_ENDS, 1) == []
    assert reachable_chutes(DEAD_ENDS, 2) == [1]
    assert reachable_chutes(RESORT_LOOP, 0) == [0, 1, 2]
    assert reachable_chutes(RESORT_LOOP, 1) == [0, 1, 2]
    assert far == list(range(1, 60_000))
    assert reachable_chutes(long_depot, 59_999) == []
    for bad_start in (-1, 5):
        try:
            reachable_chutes(FAN_OUT, bad_start)
        except ValueError as refusal:
            assert str(refusal).startswith(f"no such chute: {bad_start}")
        else:
            raise AssertionError(f"chute {bad_start} should have been refused")
    print("All checks passed.")
```

**The stack is the recursion, written down.** A recursive walk keeps its
unfinished work in Python's call stack: each nested call is a frame holding
"which chute am I on, and which belt was I up to". The loop version keeps the
same information in `stack`, a plain list of chutes still to look at. Nothing
about the algorithm changed. What changed is *where the pending work lives* —
in a list on the heap instead of in frames the interpreter counts and caps.

**`stack.pop()` takes from the end, and that is what makes it depth-first.**
The last chute pushed is the first one examined, so the walk dives down one arm
before it comes back for the others. Swap `pop()` for `pop(0)` and you have
breadth-first search instead — a different traversal order, the same set of
chutes at the end, and a quiet performance bug, because `pop(0)` on a list has
to shuffle every remaining item down one place. That is what `collections.deque`
exists for, and it is Week 6's tool.

**Seeding with `belts[start]` is the whole of the start-is-special rule.**

```python
stack: list[int] = list(belts[start])
```

The start chute is never marked by hand. It gets marked if — and only if — some
belt pushes it onto the stack, which is exactly the question "can a parcel get
back here?". Compare the tempting version, `stack = [start]` with `reached =
{start}`: it answers a different question, "which chutes are on some path
beginning at start", and the two questions agree on every depot except the ones
you were asked about.

**`if chute in reached: continue` is doing two jobs at once.** It is what makes
the walk terminate on a depot with a loop in it, and it is what stops a chute
being processed twice when two belts arrive at it. Both jobs need a set rather
than a list: `in` on a set is one hash lookup whatever the size, while `in` on
a list of 60,000 chutes reads through the list. With this input the list version
would do around a billion comparisons and take minutes; the set version takes
under a second.

**The same chute can sit on the stack more than once, and that is fine.** Two
belts into chute 3 push `3` twice. The first pop marks it; the second pop finds
it already marked and skips. The alternative — check before pushing — keeps the
stack smaller and is what Lecture 2 §6 calls marking on push. Both are correct.
What is not correct is doing neither, which is the most common way this walk
turns into an infinite loop.

**`sorted(reached)` at the end, not a sorted structure all the way through.**
The walk does not care about order, so paying for order during the walk buys
nothing. One sort of `V` items at the end is `O(V log V)`, which is cheaper than
the walk itself for any depot where the belts outnumber the chutes.

**The `ValueError` is written before any work happens.** Refusing bad input at
the top of a function, in one place, is worth more than it looks: everything
below that point can then assume `start` is a real chute, and the error the
caller sees names their mistake instead of exposing an `IndexError` from three
lines into a walk they cannot see.

## Download and run

Download
[exercise-02-conveyor-reachability-solution.py](./exercise-02-conveyor-reachability-solution.py)
and run it:

```bash
python exercise-02-conveyor-reachability-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-conveyor-reachability.py`.

## Common bugs to catch

- **`RecursionError: maximum recursion depth exceeded`.** You wrote the walk as
  a function that calls itself, and pointed it at the 60,000-chute run. This is
  the exception this whole page exists for. Real output, trimmed in the middle
  where it repeats:

  ```text
  Traceback (most recent call last):
    File "conveyor.py", line 19, in <module>
      print(len(reachable_chutes(straight_run(60_000), 0)))
                ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
    File "conveyor.py", line 16, in reachable_chutes
      walk(start)
      ~~~~^^^^^^^
    File "conveyor.py", line 15, in walk
      walk(nxt)
      ~~~~^^^^^
    File "conveyor.py", line 15, in walk
      walk(nxt)
      ~~~~^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  `[Previous line repeated 995 more times]` is Python being kind — the real
  traceback is a thousand copies of the same two lines. Check the ceiling for
  yourself:

  ```bash
  python -c "import sys; print(sys.getrecursionlimit())"
  ```

  ```text
  1000
  ```

  A thousand. Your depot has sixty times that in one straight line.

- **You raised the limit, it worked, and you shipped it.** This is the
  dangerous one, because it *does* work:

  ```python
  import sys
  sys.setrecursionlimit(200_000)
  ```

  ```text
  59999
  ```

  On CPython 3.12 and later, a deep run of ordinary Python calls no longer
  needs one C stack frame per Python call, so raising the limit really can let
  a walk this deep finish. Three reasons not to be pleased with that.

  First, **the number is a guess about input you do not control.** You picked
  200,000 because the depot has 60,000 chutes today. Nothing in the code
  notices the day it has 400,000.

  Second, **you do not choose the interpreter your code runs on.** On CPython
  3.11 and earlier each Python call really does consume a C stack frame, and
  raising the limit past what that stack can hold does not give you a
  `RecursionError` — it overflows the operating system's stack and kills the
  process outright, with no traceback and nothing to catch. The same is true on
  any version for a recursion that passes through C on its way round, which
  includes comparisons, `__repr__`, and sorting with a key.

  Third, **every frame costs memory** whether or not it costs C stack. A
  million frames is a real number of megabytes for a walk whose answer is a
  set of integers.

  The explicit stack has none of these problems, not because it is clever but
  because it never asks the question. Its pending work is a list, lists grow
  until memory runs out, and there is no limit to tune, no version to worry
  about and nothing to guess.

- **The answer contains `start` when it should not.** You wrote:

  ```python
  reached = {start}
  stack = [start]
  ```

  Every test passes except the two that this exercise is about. `FAN_OUT` from
  `0` comes back as `[0, 1, 2, 3, 4]`:

  ```text
  AssertionError
  ```

  A bare `AssertionError` with no message, because `assert` says nothing when
  it fails beyond which line failed. Seed the stack from `belts[start]` and mark
  nothing by hand.

- **The program never finishes.** You dropped the visited check and pointed it
  at `RESORT_LOOP`. There is no exception and no traceback — the process simply
  sits there, and `stack` grows without limit until the machine runs out of
  memory. Press Ctrl+C and you will see where it was:

  ```text
  KeyboardInterrupt
  ```

  Any graph that can lead back to somewhere you have been needs the set. In this
  domain, that is any depot with a re-sort loop, which is most of them.

- **`IndexError: list index out of range`** instead of your `ValueError`:

  ```text
  Traceback (most recent call last):
      stack = list(belts[start])
                   ~~~~~^^^^^^^
  IndexError: list index out of range
  ```

  You used `start` before checking it. Move the check above the first use.

- **`reachable_chutes(FAN_OUT, -1)` quietly returns an answer.** No exception,
  because `belts[-1]` is legal Python and means the last chute. You checked
  `start >= len(belts)` and forgot the other end. `0 <= start < len(belts)`
  says both halves in one expression, and reads as the sentence you meant.

- **Five lines of `None`, then `TypeError: object of type 'NoneType' has no
  len()`.** Your function walked, marked, and forgot to `return`:

  ```text
  empty depot         : None
  fan-out from 0      : None
  fan-out from 2      : None
  dead end at chute 1 : None
  re-sort loop from 0 : None
  Traceback (most recent call last):
      print(f"60000-chute run     : {len(far)} chutes, first {far[0]}, last {far[-1]}")
                                     ~~~^^^^^
  TypeError: object of type 'NoneType' has no len()
  ```

  A function that falls off its end hands back `None`. Notice how far the
  damage travelled before anything complained: five lines printed the word
  `None` quite happily, because an f-string will format anything. The traceback
  points at the first place somebody asked `None` a real question — not at the
  missing `return`, which is five functions and sixty thousand chutes away.

## Under the hood

<details>
<summary>Under the hood — what a frame actually is, and what changed in CPython 3.12</summary>

**A frame is an object.** Every time a Python function is called, the
interpreter makes a frame object holding the local variables, the position in
the bytecode, and a link back to the caller's frame. That is what the traceback
prints when it says `File "...", line 15, in walk` a thousand times: it is
walking the chain of frames from the exception back to the start.

You can see one:

```python
import sys
def show():
    frame = sys._getframe()
    print(frame.f_code.co_name, frame.f_lineno)
show()
```

```text
show 4
```

**The limit is a guard rail, not a law of physics.** `sys.setrecursionlimit`
sets a counter. The interpreter increments it on entry to a Python call and
raises `RecursionError` when it crosses the number. Nothing about the machine
enforces a thousand — it is a chosen default, and it was chosen to be small
enough that a runaway recursion raises a catchable exception well before it
overflows the real, operating-system stack underneath.

**What changed in 3.11 and 3.12.** Older CPythons implemented a Python function
call by making a C function call — `_PyEval_EvalFrame` calling itself — so every
Python frame sat on a C frame. Raise the recursion limit past what the C stack
could hold and you did not get an exception; the process died. CPython 3.11
started storing frames in a chunked stack of its own, and 3.12 finished the job
for ordinary Python-to-Python calls, so a deep pure-Python recursion now mostly
consumes heap memory instead of C stack.

That is a real improvement and it is the reason your raised limit worked. It is
not a reason to depend on it. A recursion that passes through C at any point —
a `__lt__` called by `sorted`, a `__repr__` called by `print`, a generator
resumed by a built-in — is back on the C stack for that hop, and the failure
there is still an abrupt one. And "mostly consumes heap memory" is a phrase
about your memory budget, not about safety.

**The cost comparison, straight.** Recursive: one frame per chute, plus the
visited set. Explicit stack: one integer per pending chute, plus the visited
set. A frame is a Python object with a dozen fields; an integer in a list is
eight bytes and a pointer. For a walk 60,000 deep, that is the difference
between tens of megabytes and well under one.

**The time is identical.** Both are `O(V + E)` — one look at each chute, one
look at each belt. Function calls in CPython are not free, so the loop version
is usually somewhat *faster*, but that is a constant factor and not the reason
to prefer it. The reason to prefer it is that it has no ceiling to think about.

</details>

<details>
<summary>Under the hood — the two disciplines for marking visited, and why the answer here picks the lazy one</summary>

There are two places you can mark a chute as reached, and the choice changes
the size of the stack but not the answer.

**Mark on pop** — what this page ships:

```python
while stack:
    chute = stack.pop()
    if chute in reached:
        continue
    reached.add(chute)
    stack.extend(belts[chute])
```

A chute can be pushed several times before it is popped, so the stack can hold
up to `E` entries. In exchange, there is exactly one place where marking
happens, which is very hard to get wrong.

**Mark on push** — the tighter one:

```python
for nxt in belts[chute]:
    if nxt not in reached:
        reached.add(nxt)
        stack.append(nxt)
```

Now a chute is never on the stack twice, so the stack holds at most `V`
entries. The cost is that the marking is spread over two places — the seeding
and the loop — and forgetting the seed half is a bug that only appears on
inputs where the start is reachable from itself.

**Which to write in an interview?** Mark on pop, then say the sentence: *"this
can queue a node twice, so the stack is `O(E)` rather than `O(V)`; if the edges
massively outnumber the nodes I would mark on push instead."* Saying that is
worth more than silently writing the tighter one, because it shows you know
there was a choice.

**One thing neither version does is find shortest paths.** Depth-first search
dives down one arm to the end before touching the second belt out of the start,
so the first time it arrives at a chute is very often not by the shortest run of
belts. If the supervisor ever asks "how many belts away is chute 900?", this is
the wrong tool and Week 6's queue is the right one. Recognising that in one
sentence is Q7 of this week's [quiz](../quiz.md).

</details>

## Acceptance checklist

- [ ] `python exercise-02-conveyor-reachability.py` prints the seven report
      lines and then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `reachable_chutes(FAN_OUT, 0)` does **not** contain `0`.
- [ ] `reachable_chutes(RESORT_LOOP, 0)` **does** contain `0`.
- [ ] `reachable_chutes([], 0)` returns `[]` without raising.
- [ ] `reachable_chutes(FAN_OUT, -1)` and `reachable_chutes(FAN_OUT, 5)` both
      raise `ValueError` naming the chute.
- [ ] No function in your file calls itself, and the file does not import `sys`.
- [ ] You ran the recursive version once, on purpose, and read the
      `RecursionError` it produced.
- [ ] The function keeps its type hints and its docstring.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 2: conveyor reachability`.

## Stretch

- **Report the route, not just the destinations.** Carry the path alongside the
  chute on the stack.

  ```python
  def a_route_to(belts: list[list[int]], start: int, target: int) -> list[int] | None:
      """Return one belt route from start to target, or None if there is none."""
      stack: list[tuple[int, list[int]]] = [(nxt, [start, nxt]) for nxt in belts[start]]
      reached: set[int] = set()
      while stack:
          chute, route = stack.pop()
          if chute in reached:
              continue
          reached.add(chute)
          if chute == target:
              return route
          stack.extend((nxt, route + [nxt]) for nxt in belts[chute])
      return None
  ```

  ```text
  route 0 -> 4: [0, 2, 4]
  route 3 -> 0: None
  ```

  Note what this costs: each stack entry now holds a whole list, so the memory
  is `O(V²)` in the worst case rather than `O(V)`. The cheaper version keeps a
  `came_from` dictionary and rebuilds the route once at the end — worth writing
  as a second pass.

- **Turn the walk round: which chutes can reach a given one?** Build the
  reversed depot first, then run the same function on it, unchanged.

  ```python
  def reversed_belts(belts: list[list[int]]) -> list[list[int]]:
      """Every belt turned round: reversed[j] lists the chutes that drop into j."""
      backwards: list[list[int]] = [[] for _ in belts]
      for chute, targets in enumerate(belts):
          for target in targets:
              backwards[target].append(chute)
      return backwards
  ```

  ```text
  chutes that can reach 3: [0, 1, 2]
  ```

  Reversing the arrows and reusing the walk is one of the highest-value moves in
  the whole graph repertoire. [Homework Problem 3](../homework/problem-03-safe-forwarding.md)
  is built on it.

- **Count how deep the stack ever gets.** Add a `high_water` variable that
  tracks `max(high_water, len(stack))` inside the loop, and run it on the
  60,000-chute straight run and on `FAN_OUT`.

  ```text
  straight run: high water 1
  fan-out     : high water 3
  ```

  One. A straight belt run never has more than a single chute pending, because
  each chute leads to exactly one other. So the recursion that died at a
  thousand frames was not holding a thousand *chutes* of pending work — it was
  holding one chute of work and 999 frames of bookkeeping. That is the clearest
  possible statement of what the explicit stack buys you.
When your depot survives sixty thousand chutes, move on to
[Exercise 3 — Batch Loop Audit](./exercise-03-batch-loop-audit.md), where the
walk has to notice it has arrived somewhere it never left.
