# Exercise 3 — Batch Loop Audit

> **Topic:** the three colours — white, grey, black — and finding a circular wait in a one-way graph
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** a visited set answers "have I been here?". That is the wrong question for finding a loop, and answering the wrong question here does not raise anything — it reports circles that are not there, on any plan where two paths split and meet again. This page swaps the visited set for three colours, which answer "am I standing on it right now?", and then asks for the loop itself rather than a yes or no, because "your plan has a loop" is not something anybody can act on.

## The Brief

A cannery turns fruit into tins. The work happens in **stages** — wash, blanch,
fill, seal, retort — and the plant's plan says which stage **feeds** which
other stages. If washing feeds blanching, then whatever comes out of the wash
goes into the blancher.

The plan is a dictionary. Each key is a stage, and the list beside it is the
stages it feeds:

```python
feeds = {
    "wash": ["blanch", "cook"],
    "blanch": ["fill"],
    "cook": ["fill"],
    "fill": ["seal"],
}
```

Read the arrows as one-way. Wash feeds blanch; blanch does not feed wash.

Sometimes somebody types a plan where the arrows come back round on
themselves — fill feeds seal, seal feeds retort, and retort feeds fill again.
That is a **loop**, and a plant with a loop in its plan cannot start, because
each of those three stages is waiting for one of the others.

Your job is to find one, and to **name it**. Not `True`. Not "yes, there is a
loop". The actual stages, in feed order:

```python
["fill", "seal", "retort"]
```

which reads as *fill feeds seal feeds retort feeds fill*.

### Why a visited set is not enough

The natural instinct is a set of stages you have already been to. Try it on
this plan:

```text
wash ──> blanch ──┐
  │               ├──> fill ──> seal
  └──> cook ──────┘
```

Walk from wash. Go down through blanch to fill, then seal. Come back up. Now
try cook, and cook feeds fill — which you have visited. A visited set says
"been there", so a naive check shouts *loop!* And there is no loop. Blanch and
cook both feed the same stage, which is a **diamond**, and diamonds are how
most real plants are built.

The fix is to keep more than one kind of "been there":

- **White** — a stage nobody has started looking at.
- **Grey** — a stage you are standing on *right now*. You walked into it and
  you have not walked back out. Every grey stage is on the path under your
  feet, in order.
- **Black** — a stage you finished. You walked in, you followed everything it
  feeds all the way down, and you came back out.

Now the rule is exact. **An arrow into a grey stage is a loop**, because grey
means "on my current path", so you have arrived somewhere you never left. **An
arrow into a black stage is nothing at all** — that part of the plant is
finished and already proved clean. In the diamond above, `fill` is black by the
time cook reaches it, so nothing is reported. Correct.

That is the entire idea. The rest is bookkeeping.

### The contract, precisely

`find_feed_loop(feeds)` returns the stages of **one** loop, in feed order,
rotated so the list begins at the alphabetically smallest stage in that loop,
without repeating that stage at the end. It returns `None` when the plan has no
loop.

Two details that keep the answer the same on every machine and every run:

- Start stages are tried **in sorted order**, and each stage's fed stages are
  walked **in sorted order**. The first loop found under that rule is the one
  returned. Without a rule like this, a plan with two loops in it could
  honestly report either, and no test could check it.
- A stage that appears only as a target and never as a key is still a stage.
  `{"wash": ["blanch"]}` has two stages in it, not one.

A stage that feeds itself is a loop of one: `{"retort": ["retort"]}` returns
`["retort"]`.

## Starter

Create `exercise-03-batch-loop-audit.py` in your practice repo and paste this
in. Fill in the one `TODO`.

```python
"""exercise-03-batch-loop-audit.py — find a loop in a cannery's batch plan.

Three colours: white for untouched, grey for on-the-path-right-now, black for
finished. An arrow into a grey stage is a loop. An arrow into a black stage is
not.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

from collections.abc import Iterator

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
CLEAN_DIAMOND: dict[str, list[str]] = {
    "wash": ["blanch", "cook"],
    "blanch": ["fill"],
    "cook": ["fill"],
    "fill": ["seal"],
}

SELF_FEED: dict[str, list[str]] = {
    "retort": ["retort"],
}

SIMPLE_LOOP: dict[str, list[str]] = {
    "wash": ["fill"],
    "fill": ["seal"],
    "seal": ["retort"],
    "retort": ["fill"],
}

ROTATED_LOOP: dict[str, list[str]] = {
    "intake": ["press"],
    "press": ["soak"],
    "soak": ["mash"],
    "mash": ["press"],
}


def long_plan(stages: int, loop_back: bool) -> dict[str, list[str]]:
    """Build a plan that is one straight chain of `stages` stages.

    Args:
        stages: How many stages the chain holds.
        loop_back: When True the last stage feeds the first, closing the chain
            into one enormous loop.

    Returns:
        A feed table keyed by zero-padded stage names, so alphabetical order
        and chain order agree.
    """
    plan: dict[str, list[str]] = {}
    for index in range(stages - 1):
        plan[f"stage-{index:05d}"] = [f"stage-{index + 1:05d}"]
    if loop_back:
        plan[f"stage-{stages - 1:05d}"] = ["stage-00000"]
    return plan


# ---- Your task ----
def find_feed_loop(feeds: dict[str, list[str]]) -> list[str] | None:
    """Return the stages of one feed loop, or None when the plan has none.

    Args:
        feeds: Maps a stage name to the stages it feeds. A stage that appears
            only as a target and never as a key is still a stage.

    Returns:
        The stages of one loop in feed order, rotated so the list starts at the
        alphabetically smallest stage in that loop, with that stage not
        repeated at the end. None when no loop exists. Start stages are tried
        in sorted order and each stage's fed stages are walked in sorted order;
        the first loop found under that rule is the one returned.
    """
    # TODO: collect every stage, colour them all white, then walk from each
    # white stage in sorted order. Keep the grey stages in a `path` list so a
    # loop can be sliced straight out of it, and keep the pending work on an
    # explicit stack of (stage, iterator over its fed stages).
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty plan     : {find_feed_loop({})}")
    print(f"clean diamond  : {find_feed_loop(CLEAN_DIAMOND)}")
    print(f"self feed      : {find_feed_loop(SELF_FEED)}")
    print(f"simple loop    : {find_feed_loop(SIMPLE_LOOP)}")
    print(f"rotated loop   : {find_feed_loop(ROTATED_LOOP)}")

    clean_chain = find_feed_loop(long_plan(5_000, loop_back=False))
    closed_chain = find_feed_loop(long_plan(5_000, loop_back=True))
    print(f"5000 clean     : {clean_chain}")
    assert closed_chain is not None
    print(
        f"5000 looped    : {len(closed_chain)} stages, "
        f"{closed_chain[0]} .. {closed_chain[-1]}"
    )

    assert find_feed_loop({}) is None
    assert find_feed_loop({"wash": []}) is None
    assert find_feed_loop(CLEAN_DIAMOND) is None
    assert find_feed_loop(SELF_FEED) == ["retort"]
    assert find_feed_loop(SIMPLE_LOOP) == ["fill", "seal", "retort"]
    assert find_feed_loop(ROTATED_LOOP) == ["mash", "press", "soak"]
    assert clean_chain is None
    assert len(closed_chain) == 5_000
    assert closed_chain[0] == "stage-00000"
    assert closed_chain[-1] == "stage-04999"
    print("All checks passed.")
```

Four words you need before you start.

**Directed.** The arrows go one way. Week 6's graphs let you walk back down any
edge you came up; here you cannot, and that one-way-ness is exactly what makes
a loop possible.

**Path.** The list of grey stages, in the order you walked into them. It is the
route from wherever you started to wherever you are standing. When you meet a
grey stage, the loop is the tail of this list starting at that stage — one
slice, no searching.

**Iterator.** An object that hands out the items of a list one at a time and
remembers where it got to. `iter(["a", "b", "c"])` gives you one. Recursion
remembers "which fed stage was I up to" for free; an explicit stack has to
remember it on purpose, and holding an iterator in the stack entry is how.

**Rotate.** Turning `["seal", "retort", "fill"]` into `["fill", "seal",
"retort"]` — same ring, different starting point. Two slices and a `+`. It is
what makes two people auditing the same broken plan get the same answer.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/exercises/exercise-03-batch-loop-audit.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_feed_loop(feeds)` returns `None` when the plan has no loop, and a list
   of stage names when it has one.
2. The returned list is in feed order — each stage feeds the next, and the last
   feeds the first.
3. It is rotated to begin at the alphabetically smallest stage in the loop, and
   that stage is **not** repeated at the end.
4. `find_feed_loop({"retort": ["retort"]})` returns `["retort"]`.
5. `find_feed_loop({})` returns `None`.
6. A stage that appears only as a target counts as a stage. The walk must not
   raise `KeyError` on one.
7. Start stages are tried in sorted order, and fed stages in sorted order, so
   the answer is one specific loop rather than any of them.
8. No function in your answer calls itself, and nothing touches
   `sys.setrecursionlimit`.
9. The function keeps its type hints and its docstring.

## Constraints

- **Up to 5,000 stages, and the chain can use all of them.** A cannery does not
  have five thousand stages; a plan generated by a scheduling system for a
  whole site does. Five thousand is five times CPython's default recursion
  limit of 1,000, so the recursive spelling of this walk raises
  `RecursionError` on the self-check's long chain. That is why the answer
  carries its pending work on an explicit stack.
  [Exercise 2](./exercise-02-conveyor-reachability.md) argues that case in
  full, including why raising the limit is not the fix.

- **Three colours, not a visited set.** This is the load-bearing constraint.
  Grey is a claim about *where you are*; a visited set is a claim about *where
  you have been*. Only the first can distinguish a loop from a diamond, and
  `CLEAN_DIAMOND` in the starter is there to fail loudly if you use the second.

- **Do not treat an arrow into a black stage as a loop.** Black means finished
  and proved clean. Every plant with two paths that meet has these arrows, and
  reporting them is the single most common wrong answer to this problem.

- **Keep the grey stages in an ordered list, not only in a set.** A set can
  tell you that a stage is grey. It cannot tell you what the loop *is*, because
  it has no order in it. The `path` list is what turns the yes-or-no into an
  answer somebody can act on, and slicing it costs nothing you were not already
  paying.

- **Sort at the two places where a choice exists**, and nowhere else. Sorting
  the start stages and each stage's fed stages is what makes the result one
  specific loop. That costs `O(E log E)` across the whole walk, which is more
  than the `O(V + E)` floor — one look at every stage and one at every arrow —
  and it is worth it, because an answer a test can check is worth more here
  than a constant factor.

- **The stage list comes from the keys *and* the values.** A plan can name a
  stage that never gets a key of its own, and it usually does — the last stage
  in the plant feeds nothing, so nobody writes a line for it. Missing those is
  a quiet bug: nothing raises, the walk just never looks at part of the plan.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-batch-loop-audit-solution.py
empty plan     : None
clean diamond  : None
self feed      : ['retort']
simple loop    : ['fill', 'seal', 'retort']
rotated loop   : ['mash', 'press', 'soak']
5000 clean     : None
5000 looped    : 5000 stages, stage-00000 .. stage-04999
All checks passed.
```

Two lines deserve a second look.

`clean diamond : None` is the one that matters. Two paths out of `wash` meet
again at `fill`, and the audit says nothing, because by the time `cook` reaches
`fill` it is black. Any answer that prints a loop on this line has confused
"been there" with "standing on it".

`rotated loop : ['mash', 'press', 'soak']` shows the rotation doing its job.
The walk finds that loop by arriving at `press` from `intake`, so it meets the
circle at `press` — but `mash` sorts first, so the answer starts there. Read it
out: mash feeds press, press feeds soak, soak feeds mash. Same ring, one
agreed starting point.

## Steps

1. Create the file, paste the starter, and run it. Five lines print `None`, and
   then it stops at `assert closed_chain is not None`. That is the correct
   first run — a stub returns `None` and the first assert that cares says so.
2. Collect every stage before you walk anything: the keys, union everything
   inside every value. Print the set for `CLEAN_DIAMOND` and check `seal` is in
   it, because `seal` has no key of its own.
3. Write the walk **recursively first**, with the three colours. It is about
   twelve lines and it is much easier to see. Grey on the way in, black on the
   way out, and a `path` list you append to and pop from at the same moments.
   Get `SIMPLE_LOOP`, `SELF_FEED` and `CLEAN_DIAMOND` right this way before you
   change anything.
4. Now run it on `long_plan(5_000, loop_back=True)` and watch it raise
   `RecursionError`. That is the reason for step 5, and it is worth seeing
   rather than being told.
5. Convert the recursion to an explicit stack. The stack entry is a pair:
   the stage, and an **iterator** over its sorted fed stages. The `while` loop
   looks at the top entry, tries to step down into one more fed stage, and if
   it cannot, colours the stage black and pops it.
6. Get the rotation right last. `path[path.index(fed):]` is the loop; then find
   the position of the smallest name in it and re-join the two slices.
7. Run the whole file. When `All checks passed.` prints, invent a plan with two
   separate loops in it and satisfy yourself that you can predict which one
   comes back before you run it. If you cannot, the sorted-order rule is not
   yet clear to you.

## The Solution

```python
"""exercise-03-batch-loop-audit-solution.py — find a loop in a cannery's batch plan.

Three-colour depth-first search, carried on an explicit stack so a five
thousand stage plan cannot overflow CPython's thousand-frame recursion limit.
White is a stage nobody has started, grey is a stage on the path you are
standing on right now, black is a stage that is finished and proved clean. A
hop to a grey stage is a loop. A hop to a black stage is not.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

from collections.abc import Iterator

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
CLEAN_DIAMOND: dict[str, list[str]] = {
    "wash": ["blanch", "cook"],
    "blanch": ["fill"],
    "cook": ["fill"],
    "fill": ["seal"],
}

SELF_FEED: dict[str, list[str]] = {
    "retort": ["retort"],
}

SIMPLE_LOOP: dict[str, list[str]] = {
    "wash": ["fill"],
    "fill": ["seal"],
    "seal": ["retort"],
    "retort": ["fill"],
}

ROTATED_LOOP: dict[str, list[str]] = {
    "intake": ["press"],
    "press": ["soak"],
    "soak": ["mash"],
    "mash": ["press"],
}


def long_plan(stages: int, loop_back: bool) -> dict[str, list[str]]:
    """Build a plan that is one straight chain of `stages` stages.

    Args:
        stages: How many stages the chain holds.
        loop_back: When True the last stage feeds the first, closing the chain
            into one enormous loop.

    Returns:
        A feed table keyed by zero-padded stage names, so alphabetical order
        and chain order agree.
    """
    plan: dict[str, list[str]] = {}
    for index in range(stages - 1):
        plan[f"stage-{index:05d}"] = [f"stage-{index + 1:05d}"]
    if loop_back:
        plan[f"stage-{stages - 1:05d}"] = ["stage-00000"]
    return plan


# ---- Your task ----
def find_feed_loop(feeds: dict[str, list[str]]) -> list[str] | None:
    """Return the stages of one feed loop, or None when the plan has none.

    Args:
        feeds: Maps a stage name to the stages it feeds. A stage that appears
            only as a target and never as a key is still a stage.

    Returns:
        The stages of one loop in feed order, rotated so the list starts at the
        alphabetically smallest stage in that loop, with that stage not
        repeated at the end. None when no loop exists. Start stages are tried
        in sorted order and each stage's fed stages are walked in sorted order;
        the first loop found under that rule is the one returned.
    """
    stages: set[str] = set(feeds)
    for targets in feeds.values():
        stages.update(targets)
    colour: dict[str, int] = {stage: WHITE for stage in stages}

    for root in sorted(stages):
        if colour[root] != WHITE:
            continue
        colour[root] = GREY
        path: list[str] = [root]
        pending: list[tuple[str, Iterator[str]]] = [
            (root, iter(sorted(feeds.get(root, []))))
        ]
        while pending:
            stage, targets = pending[-1]
            descended = False
            for fed in targets:
                if colour[fed] == GREY:
                    loop = path[path.index(fed) :]
                    pivot = min(range(len(loop)), key=lambda spot: loop[spot])
                    return loop[pivot:] + loop[:pivot]
                if colour[fed] == WHITE:
                    colour[fed] = GREY
                    path.append(fed)
                    pending.append((fed, iter(sorted(feeds.get(fed, [])))))
                    descended = True
                    break
                # colour[fed] == BLACK: finished elsewhere, already proved clean.
            if not descended:
                colour[stage] = BLACK
                path.pop()
                pending.pop()
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty plan     : {find_feed_loop({})}")
    print(f"clean diamond  : {find_feed_loop(CLEAN_DIAMOND)}")
    print(f"self feed      : {find_feed_loop(SELF_FEED)}")
    print(f"simple loop    : {find_feed_loop(SIMPLE_LOOP)}")
    print(f"rotated loop   : {find_feed_loop(ROTATED_LOOP)}")

    clean_chain = find_feed_loop(long_plan(5_000, loop_back=False))
    closed_chain = find_feed_loop(long_plan(5_000, loop_back=True))
    print(f"5000 clean     : {clean_chain}")
    assert closed_chain is not None
    print(
        f"5000 looped    : {len(closed_chain)} stages, "
        f"{closed_chain[0]} .. {closed_chain[-1]}"
    )

    assert find_feed_loop({}) is None
    assert find_feed_loop({"wash": []}) is None
    assert find_feed_loop(CLEAN_DIAMOND) is None
    assert find_feed_loop(SELF_FEED) == ["retort"]
    assert find_feed_loop(SIMPLE_LOOP) == ["fill", "seal", "retort"]
    assert find_feed_loop(ROTATED_LOOP) == ["mash", "press", "soak"]
    assert clean_chain is None
    assert len(closed_chain) == 5_000
    assert closed_chain[0] == "stage-00000"
    assert closed_chain[-1] == "stage-04999"
    print("All checks passed.")
```

**The colours are three answers to one question, and the middle one is the
whole point.** White, grey, black is not a visited set with extra steps. A
visited set has two states, and it merges two completely different situations:
"I am standing on this" and "I finished this ages ago". The first is a loop.
The second is a diamond. Separating them is the entire content of this
exercise, and it is why `colour` is a `dict[str, int]` rather than a `set[str]`.

**`path` and grey are the same thing, seen two ways.** Every stage in `path` is
grey, and every grey stage is in `path`, in the order it was entered. They are
appended and popped at exactly the same moments as the colour changes, which is
why the loop is a slice:

```python
loop = path[path.index(fed) :]
```

`path.index(fed)` finds where on the current route you first stepped into the
stage you have just arrived back at. Everything from there to the end is the
circle. You do not have to search for it; you were standing on it the whole
time.

**The rotation is what makes the answer reproducible.** Two people running the
same audit on the same broken plan must get the same list, or the answer is not
useful in a conversation. `min(range(len(loop)), key=...)` finds the position of
the alphabetically smallest stage, and `loop[pivot:] + loop[:pivot]` turns the
ring so that stage is first. It changes nothing about which stages are in the
loop, only where the list starts.

**The stack holds an iterator, and that is the trick that makes this loop-shaped
instead of recursive.** A recursive walk gets "which fed stage was I up to?"
free — it is the `for` loop's own state, kept in the frame. Written as a loop,
that state has to be stored somewhere, and the somewhere is the stack entry:

```python
pending.append((fed, iter(sorted(feeds.get(fed, [])))))
```

`iter(...)` is made once, when the stage is entered. Coming back to that stage
later, `for fed in targets` resumes at the next unexamined fed stage rather
than starting over. Rebuild the iterator each time round and the walk restarts
that stage's fed list at the beginning on every visit, which either never ends
or ends short — and raises nothing either way.

**`descended` is how a `while` loop says "I went deeper".** The inner `for`
either finds a loop and returns, or steps into a white stage and breaks, or
runs out. Only in the last case is the stage finished, so only then does it
turn black and come off the stack. The flag is doing what a recursive call
would have done by simply returning.

**`feeds.get(stage, [])`, not `feeds[stage]`.** The last stage in the plant
feeds nothing and nobody wrote a line for it, so it has no key. `.get` with a
default is one character longer than the `KeyError` and one bug shorter.

**Every stage is walked once, and every arrow is followed once.** A stage is
coloured grey exactly once, because only white stages are entered, and it turns
black exactly once. So the whole audit is `O(V + E)` steps plus the sorting —
one look at each stage, one look at each arrow. Five thousand stages is nothing;
the reason the file is careful is depth, not size.

## Download and run

Download
[exercise-03-batch-loop-audit-solution.py](./exercise-03-batch-loop-audit-solution.py)
and run it:

```bash
python exercise-03-batch-loop-audit-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-batch-loop-audit.py`.

## Common bugs to catch

- **`CLEAN_DIAMOND` reports a loop.** You used a visited set instead of three
  colours. The self-check catches it with a bare `AssertionError`:

  ```text
  Traceback (most recent call last):
      assert find_feed_loop(CLEAN_DIAMOND) is None
             ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  AssertionError
  ```

  `wash` feeds both `blanch` and `cook`, and both feed `fill`. Whichever gets
  there first finishes `fill`; the second arrives at a **black** stage, which is
  not a loop. Two states cannot express that. Three can.

- **`RecursionError: maximum recursion depth exceeded`** on the five-thousand
  chain, from the recursive version:

  ```text
    File "batch.py", line 31, in walk
      walk(fed)
      ~~~~^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Expected, and worth producing on purpose at step 4. The limit is 1,000 by
  default —

  ```bash
  python -c "import sys; print(sys.getrecursionlimit())"
  ```

  ```text
  1000
  ```

  — and the plan has five thousand stages in a line. Move the pending work onto
  an explicit stack; do not raise the limit.

- **`KeyError` on a stage with no key of its own.**

  ```text
  Traceback (most recent call last):
      for fed in sorted(feeds[stage]):
                        ~~~~~^^^^^^^
  KeyError: 'seal'
  ```

  `seal` is fed by `fill` and feeds nothing, so nobody wrote a line for it. Use
  `feeds.get(stage, [])`. The same oversight in the *stage collection* step is
  quieter: no exception at all, just a walk that never starts from part of the
  plan.

- **The walk never finishes.** You rebuilt the iterator on every pass:

  ```python
  stage, _ = pending[-1]
  for fed in sorted(feeds.get(stage, [])):   # wrong: starts over every time
  ```

  Nothing raises. The process sits there while the same stage is re-entered
  forever. Press Ctrl+C:

  ```text
  KeyboardInterrupt
  ```

  Build the iterator once, when the stage goes on the stack, and read from the
  one in the stack entry.

- **The loop comes back rotated to the wrong place**, or with the first stage
  repeated at the end:

  ```text
  Traceback (most recent call last):
      assert find_feed_loop(ROTATED_LOOP) == ["mash", "press", "soak"]
             ~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  AssertionError
  ```

  Two separate mistakes give the same failure. Either you returned
  `path[path.index(fed):]` without rotating — which starts wherever the walk
  happened to enter the circle — or you appended the first stage again to
  "close" it. The contract asks for the ring exactly once, starting at its
  smallest name.

- **A stage that feeds itself is missed.** You wrote `if fed != stage and
  colour[fed] == GREY`, guarding against something that is not a problem here.
  A self-feed is a real loop of length one, and `{"retort": ["retort"]}` must
  return `["retort"]`. That guard belongs to *undirected* graphs, where you have
  to ignore the edge you came in on — a different problem, covered in
  [Lecture 1 §12](../lecture-notes/01-recursive-dfs.md).

- **Five lines of `None`, then an `AssertionError` from the long chain.** You
  ran the starter before filling in the `TODO`:

  ```text
  empty plan     : None
  clean diamond  : None
  self feed      : None
  simple loop    : None
  rotated loop   : None
  5000 clean     : None
  Traceback (most recent call last):
      assert closed_chain is not None
             ^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  The correct first run. Notice that five of the six report lines were *right*
  by accident — an unfinished function that returns `None` agrees with every
  loop-free plan you show it. Tests that only use clean input cannot tell a
  correct audit from no audit at all.

## Under the hood

<details>
<summary>Under the hood — why "grey" is the same idea as a back edge, and what the other two edge kinds are</summary>

Textbooks describe this walk by classifying every arrow it follows into one of
four kinds, and the three colours are how the classification is computed.

- **Tree edge** — an arrow into a **white** stage. You have just discovered
  something new; this arrow becomes part of the walk's own tree.
- **Back edge** — an arrow into a **grey** stage. It points back up your own
  current path. This is a loop, and it is the only kind that is.
- **Forward edge** — an arrow into a **black** stage that is a descendant of
  where you are. `wash -> fill` in a plan that also has `wash -> blanch ->
  fill`.
- **Cross edge** — an arrow into a **black** stage that is not a descendant.
  `cook -> fill` in the diamond, once `fill` finished under `blanch`.

The last two are both black, and telling them apart needs discovery and finish
times, which this exercise does not need — because for loop detection they are
identical: neither is a loop. That is the whole reason two colours are not
enough and four numbers are more than you need.

**A theorem worth carrying:** a directed graph has a loop **if and only if** a
depth-first walk of it finds a back edge. The "only if" half is the interesting
one. Suppose there is a loop. Consider the stage on that loop that the walk
turns grey first. Every other stage on the loop is reachable from it, so every
one of them gets entered before it turns black — so at the moment the walk
follows the loop's last arrow back into it, it is still grey. The back edge is
found. Nothing about which stage you started from, or in what order, changes
that.

That is why the defence sentence is short and total: *"a directed graph has a
loop exactly when a depth-first walk finds an arrow into a grey node, so one
`O(V + E)` pass settles it — one look at every stage and one at every arrow."*

</details>

<details>
<summary>Under the hood — the other way to ask the same question, and when to prefer it</summary>

There is a second, completely different way to find out whether a plan has a
loop, and you will write it in [Exercise 4](./exercise-04-refit-order.md).

Count how many stages each stage is waiting on. Release the ones waiting on
nothing. Every time a stage is released, lower the count of everything it feeds
and release anything that reaches zero. When you run out of releasable stages,
compare how many you released against how many there were. Short means loop.

That is Kahn's algorithm, it is a loop rather than a recursion, and it needs no
colours at all. Three lines of it are a complete loop detector. So why does this
page do it the harder way?

**Because Kahn's leftovers are not the loop.** They are the stages inside a
loop *plus everything downstream of one*, which on a real plant is most of the
graph. If the question is "yes or no", Kahn is simpler and cheaper to think
about. If the question is "which stages, in what order", only the grey path can
answer it, because only the grey path is a *route* rather than a set.

**The other real difference is early exit.** The colour walk returns the moment
it meets its first grey stage. Kahn always runs to completion, because it
cannot know it is finished until it has tried everything. On a plan whose very
first stage feeds itself, the colour walk does two steps and Kahn does all of
them. On a plan with no loop at all, they do the same work.

**And a third, which is what the mini-project ends up using: both.** Run Kahn,
because it is cheap and it also gives you the order you actually wanted. If it
comes up short, *then* run the colour walk to name the loop for the error
message. Neither tool is a compromise, and using each for what it is good at
costs one extra pass on the only input where anybody is going to be reading an
error message anyway.

</details>

## Acceptance checklist

- [ ] `python exercise-03-batch-loop-audit.py` prints seven report lines and
      then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `find_feed_loop(CLEAN_DIAMOND)` is `None`.
- [ ] `find_feed_loop(SELF_FEED)` is `["retort"]`.
- [ ] `find_feed_loop(SIMPLE_LOOP)` is `["fill", "seal", "retort"]` — rotated,
      and not closed by repeating `"fill"`.
- [ ] `find_feed_loop({})` is `None` and raises nothing.
- [ ] The five-thousand-stage chain is audited without a `RecursionError`.
- [ ] No function in your file calls itself, and the file does not import `sys`.
- [ ] You can say out loud, without notes, what grey means and why black is not
      a loop.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 3: batch loop audit`.

## Stretch

- **Report every loop, not just the first one.** Once a loop is found, the
  cheapest honest thing to do is record it, break the arrow that closed it, and
  keep walking.

  ```python
  def all_feed_loops(feeds: dict[str, list[str]]) -> list[list[str]]:
      """Every loop found by cutting the closing arrow and auditing again."""
      working = {stage: list(fed) for stage, fed in feeds.items()}
      found: list[list[str]] = []
      while (loop := find_feed_loop(working)) is not None:
          found.append(loop)
          working.setdefault(loop[-1], []).remove(loop[0])
      return found
  ```

  On `{**SIMPLE_LOOP, **ROTATED_LOOP}` — the two broken plans from the starter,
  merged into one plant:

  ```text
  [['fill', 'seal', 'retort'], ['mash', 'press', 'soak']]
  ```

  Say plainly what this does and does not promise: it returns enough loops that
  cutting one arrow from each makes the plan sound, which is what a plant
  engineer wants. It is **not** every circular route in the graph — that number
  can be astronomically large on a graph this size, and asking for it is almost
  always the wrong question.

- **Say how deep the walk went.** Track the high-water mark of `len(path)`.

  ```text
  clean diamond : deepest path 4
  5000 chain    : deepest path 5000
  ```

  Four against five thousand, on the same code. That number is the one the
  recursive version would have had to hold in frames, and it is the reason for
  the explicit stack in a single line of output.

- **Show that starting order does not change the verdict, only the loop.** Walk
  the start stages in reverse-sorted order instead, and confirm the answer is
  still `None` on every clean plan and still a loop on every broken one.

  ```python
  def audit_reversed(feeds: dict[str, list[str]]) -> list[str] | None:
      """Same audit, start stages tried Z to A. Same verdict, maybe another loop."""
      flipped = {stage: sorted(fed, reverse=True) for stage, fed in feeds.items()}
      return find_feed_loop(flipped)
  ```

  ```text
  simple loop, A to Z : ['fill', 'seal', 'retort']
  simple loop, Z to A : ['fill', 'seal', 'retort']
  ```

  Same loop here, because there is only one. The point is the verdict: *has a
  loop* is a property of the plan, and no walk order can disagree about it. The
  proof is in the first Under the hood block.

**Practice elsewhere.** The same question, asked as a yes or no, appears as
[LeetCode 207 · Course Schedule](https://leetcode.com/problems/course-schedule/)
if you want a judge to run against — though that contract wants a boolean, where
ours wants the loop itself, in a fixed rotation, which is what forces the grey
path to be a list rather than a set.

When your audit is right, move on to
[Exercise 4 — Refit Order](./exercise-04-refit-order.md), where the same
machinery stops asking whether the work can be done and starts saying in what
order.
