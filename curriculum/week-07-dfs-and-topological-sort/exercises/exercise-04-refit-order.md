# Exercise 4 — Refit Order

> **Topic:** Kahn's algorithm — waiting counts, a ready pile, and what the leftovers mean
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** "in what order can these be done?" is the most common graph question in the whole interview repertoire, and this is the shape that answers it. There is no recursion in it, it detects an impossible plan without ever looking for one, and the leftovers it produces are more useful than a boolean. The tie-break in this contract also forces you to swap the queue for a heap, which is the difference between "any valid order" and one answer a test can check.

## The Brief

A ship is in dry dock for a refit. There is a list of **jobs** — dock in, hull
survey, blast, weld, paint, float out, sea trial — and a list of rules saying
which job has to finish before which other job can start.

Each rule is a pair. `("blast", "weld")` means *blast has to finish before weld
starts*. Read it left to right: the first one comes first.

```python
jobs = ["blast", "dock-in", "hull-survey", "weld"]
must_follow = [
    ("dock-in", "hull-survey"),
    ("hull-survey", "blast"),
    ("blast", "weld"),
]
```

You are writing the planner. It returns two things:

```python
(order, blocked)
```

**`order`** is a running order that never breaks a rule: every job appears
after everything that has to finish before it. There are usually many such
orders, so the contract pins one down — **at every step, start the
alphabetically smallest job that is ready**. "Ready" means every job that had
to finish before it already has. That turns "any valid order" into one specific
answer, which is the difference between a test that checks your work and a test
that shrugs.

**`blocked`** is the sorted list of jobs that never became ready at all. That
happens when the rules chase each other round in a circle: pressure test cannot
start until the valve is fitted, sign-off cannot start until the pressure test
is done, and — because somebody typed it wrong — the valve cannot be fitted
until sign-off. None of those three will ever start, and neither will anything
waiting on them.

So `blocked` is not just "the circle". It is *the circle plus everything
downstream of it*, which is exactly the list a yard superintendent wants: these
are the jobs that will not happen today.

### How it works, in one picture

For every job, count how many jobs it is **waiting on**. Jobs waiting on
nothing can start immediately — put them in a pile called *ready*.

Then repeat: take the alphabetically smallest job out of the ready pile, write
it down, and for every job it was holding up, lower that job's waiting count by
one. Any count that reaches zero goes into the ready pile.

Stop when the ready pile is empty. If you wrote down every job, the plan works.
If you wrote down fewer, the ones you did not write down are `blocked`.

Notice what is *not* in that description: at no point does anything go looking
for a circle. The algorithm finds one by noticing it ran out of work with jobs
left over. That is the elegant part, and it is the thing to be able to say out
loud.

### One trap, deliberately planted

The yard's maintenance system emits the same dependency from two different
forms, so `("dock-in", "hull-survey")` arrives **twice** in the starter's rule
list. The danger is not the duplicate itself. It is **counting it on one side and
not the other**. Keep the "who does this job hold up" list as a `set` — which
is the natural choice — and the second copy vanishes from it. Raise the waiting
count anyway and the hull survey now waits for two things when only one is ever
coming. Its count never reaches zero, it lands in `blocked`, everything behind
it follows, and nothing raises. You get a confident, wrong, two-job plan.

Note what does *not* break: if you keep plain lists on both sides and count
twice, the second copy also decrements twice and the two mistakes cancel. That
is worth knowing, because it means the bug hides from the obvious spelling and
only appears in the tidier one.

The rule that is always safe: decide once whether a pair is new, and let that
one decision drive both tables.

## Starter

Create `exercise-04-refit-order.py` in your practice repo and paste this in.
Fill in the one `TODO`.

```python
"""exercise-04-refit-order.py — a legal running order for a dry-dock refit.

Kahn's algorithm: count what each job is waiting on, start with the jobs
waiting on nothing, and release the rest as their counts fall to zero. The
ready pile is a heap, because the tie rule is "alphabetically smallest".

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import heapq

# ---- Given data ----
REFIT_JOBS: list[str] = [
    "anode-swap",
    "bilge-clean",
    "blast",
    "dock-in",
    "float-out",
    "hull-survey",
    "paint",
    "prop-shaft",
    "sea-trial",
    "weld",
]

# The maintenance system emits ("dock-in", "hull-survey") from two different
# forms, so the same dependency arrives twice. Counting it twice would leave
# hull-survey waiting forever.
REFIT_RULES: list[tuple[str, str]] = [
    ("dock-in", "hull-survey"),
    ("hull-survey", "blast"),
    ("blast", "weld"),
    ("weld", "paint"),
    ("paint", "float-out"),
    ("float-out", "sea-trial"),
    ("dock-in", "bilge-clean"),
    ("bilge-clean", "paint"),
    ("hull-survey", "prop-shaft"),
    ("prop-shaft", "float-out"),
    ("prop-shaft", "anode-swap"),
    ("dock-in", "hull-survey"),
]

VALVE_JOBS: list[str] = ["fit-valve", "handover", "pressure-test", "sign-off"]

VALVE_RULES: list[tuple[str, str]] = [
    ("fit-valve", "pressure-test"),
    ("pressure-test", "sign-off"),
    ("sign-off", "fit-valve"),
    ("sign-off", "handover"),
]


# ---- Your task ----
def plan_refit(
    jobs: list[str], must_follow: list[tuple[str, str]]
) -> tuple[list[str], list[str]]:
    """Return a legal running order for the refit, and the jobs that never ran.

    Args:
        jobs: Every job in the refit. Names are unique.
        must_follow: Pairs (a, b) meaning job a must finish before job b
            starts. The same pair may arrive more than once; it still counts
            once.

    Returns:
        A pair (order, blocked). `order` takes the alphabetically smallest
        ready job at every step. `blocked` is the sorted list of jobs that
        never became ready — the jobs inside a loop, plus everything
        downstream of one.

    Raises:
        ValueError: If a pair names a job that is not in `jobs`.
    """
    # TODO: build "what does this job hold up" and "how many is it waiting on",
    # counting each distinct pair once. Then run the ready heap down.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    refit_order, refit_blocked = plan_refit(REFIT_JOBS, REFIT_RULES)
    print(f"refit order   : {refit_order}")
    print(f"refit blocked : {refit_blocked}")

    valve_order, valve_blocked = plan_refit(VALVE_JOBS, VALVE_RULES)
    print(f"valve order   : {valve_order}")
    print(f"valve blocked : {valve_blocked}")

    print(f"nothing to do : {plan_refit([], [])}")
    print(f"no rules      : {plan_refit(['zinc-check', 'scrub'], [])}")
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        print(f"unknown job   : {refusal}")

    assert refit_order == [
        "dock-in",
        "bilge-clean",
        "hull-survey",
        "blast",
        "prop-shaft",
        "anode-swap",
        "weld",
        "paint",
        "float-out",
        "sea-trial",
    ]
    assert refit_blocked == []
    assert valve_order == []
    assert valve_blocked == ["fit-valve", "handover", "pressure-test", "sign-off"]
    assert plan_refit([], []) == ([], [])
    assert plan_refit(["zinc-check", "scrub"], []) == (["scrub", "zinc-check"], [])
    assert plan_refit(["weld"], [("weld", "weld")]) == ([], ["weld"])
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        assert "'grind'" in str(refusal)
    else:
        raise AssertionError("an unknown job should have been refused")
    print("All checks passed.")
```

Four words you need before you start.

**Waiting count.** For one job, how many other jobs must finish before it can
start. Sometimes called the *in-degree* — the number of arrows pointing at it.
Both names mean the same number; the first one says what it is for.

**Ready.** A job whose waiting count is zero. Nothing is in its way.

**Heap.** A pile that always hands you its smallest item first, and does it in
`O(log n)` rather than by sorting the whole pile again. `heapq.heappush(pile,
x)` puts one in; `heapq.heappop(pile)` takes the smallest out. It works
directly on an ordinary list, which is why there is no `Heap` class to import.

**Topological order.** The formal name for what `order` is: an arrangement of
the jobs in which every arrow points forwards. Every graph with no circle in it
has at least one; a graph with a circle has none at all.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/exercises/exercise-04-refit-order.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `plan_refit(jobs, must_follow)` returns a tuple `(order, blocked)`.
2. Every job in `order` appears after everything that must finish before it.
3. At every step the **alphabetically smallest ready job** is taken, so the
   order is one specific list.
4. `blocked` is sorted, and holds exactly the jobs that never became ready.
5. `order` and `blocked` together contain every job exactly once.
6. A duplicated pair counts once. The refit plan in the starter has one, and it
   must not change the answer.
7. `plan_refit([], [])` returns `([], [])`.
8. A pair naming a job that is not in `jobs` raises `ValueError`, and the
   message names the offending job.
9. A job that must follow itself is impossible, so it goes in `blocked`:
   `plan_refit(["weld"], [("weld", "weld")])` is `([], ["weld"])`.
10. The function keeps its type hints and its docstring.

## Constraints

- **Count each distinct pair once, and let one decision drive both tables.**
  The duplicated rule in `REFIT_RULES` is there to catch the tidy-looking
  version of this code: a `set` for what a job holds up, and an unguarded `+= 1`
  for the waiting count. The set swallows the second copy; the counter does not;
  the hull survey then waits on a job that is never coming. The failure is
  entirely silent — a shorter plan, a longer `blocked` list, no exception. (Two
  plain lists and an unguarded `+= 1` happen to survive, because the extra
  decrement cancels the extra increment. Do not rely on that; it is luck, not
  design.)

- **Check every job name before counting anything.** `("dock-in", "grind")`
  where `grind` is not a job is a typo in the yard's data, and the honest
  response is a `ValueError` naming `grind`. The alternative — quietly
  inventing a job called `grind` — produces a plan for work nobody scheduled.

- **Use a heap for the ready pile, not a `deque`.** With a `deque` you get *a*
  valid order, and which one depends on the order the rules happened to arrive
  in. That is fine for a judge that accepts any answer and useless for a test
  that has to check yours. `heapq` costs `O(log V)` per push and pop instead of
  `O(1)`; with ten jobs that is unmeasurable, and with a hundred thousand it is
  about seventeen comparisons each. Determinism you can test is worth far more
  than a constant factor you cannot feel.

- **Do not go looking for a circle.** The whole point of this shape is that it
  finds one for free. If the order comes out shorter than the job list, the
  jobs you did not write down are the circle plus everything downstream. Adding
  a separate loop-detection pass duplicates work you have already done and
  gives you a worse answer — a boolean instead of the actual list.

- **`O(V + E)`.** One look at every job and one look at every rule, plus the
  heap's `log` factor: every job enters the ready pile at most once and every
  rule lowers exactly one count. Nothing here re-reads the rules, which is
  what the `holds_up` table is for. The alternative you may be tempted by —
  scan all jobs each round looking for one that is ready — is `O(V²)` and is
  the standard way this gets written badly.

- **Job names are short strings and there are at most 100,000 of them.** A real
  refit has dozens; a build system's job list, which is the same problem in
  different overalls, has that many. The bound matters because it rules out
  anything quadratic and because it makes the heap's `log` factor worth naming.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-refit-order.py
refit order   : ['dock-in', 'bilge-clean', 'hull-survey', 'blast', 'prop-shaft', 'anode-swap', 'weld', 'paint', 'float-out', 'sea-trial']
refit blocked : []
valve order   : []
valve blocked : ['fit-valve', 'handover', 'pressure-test', 'sign-off']
nothing to do : ([], [])
no rules      : (['scrub', 'zinc-check'], [])
unknown job   : must_follow names a job that is not in jobs: 'grind'
All checks passed.
```

Look at the first two entries of the refit order: `dock-in`, then
`bilge-clean`. Both are legal at that moment — once the ship is docked, the
bilge clean and the hull survey are both ready — and `bilge-clean` sorts before
`hull-survey`, so it goes first. That is the tie rule doing visible work. With a
`deque` instead of a heap you would very likely get `hull-survey` there
instead, and it would be equally correct and completely untestable.

Then look at the valve plan. All four jobs are blocked, including `handover`,
which is not in the circle at all — it is merely waiting on `sign-off`, which
is. That is what "the circle plus everything downstream" means, and it is why
`blocked` is more useful than `False`.

## Steps

1. Create the file, paste the starter, and run it. It stops immediately with
   `TypeError: cannot unpack non-iterable NoneType object`, because an
   unfinished function hands back `None` and the first line tries to open it
   into two names. Correct first run.
2. Build the two tables before you plan anything. `holds_up[job]` is the set of
   jobs this one is blocking; `waiting_on[job]` is a count. Use a **set** for
   `holds_up` and the duplicate rule handles itself: adding the same job twice
   to a set changes nothing, so guard the count increment on whether the set
   actually grew.
3. Add the name check as you read each pair, before you touch either table.
   Test it with `("dock-in", "grind")` right away.
4. Seed the ready pile with every job whose count is zero, and `heapq.heapify`
   it. Heapify in one go is `O(V)`; pushing them one at a time is `O(V log V)`
   for the same pile.
5. Write the drain loop: pop the smallest, append it to `order`, and lower the
   count of everything it holds up.
6. Compute `blocked` at the end as the sorted difference between all the jobs
   and the ones in `order`. Do not try to track it as you go — you cannot know
   a job is blocked until you have run out of everything else.
7. Run it. Then delete the duplicate-handling and run it again, so you see the
   failure this page is built around with your own eyes. Then put it back.

## The Solution

```python
"""exercise-04-refit-order-solution.py — a legal running order for a dry-dock refit.

Kahn's algorithm. Count how many jobs each job is waiting on, start with the
jobs waiting on nothing, and every time a job finishes, take one off the count
of the jobs it was holding up. The ready pile is a heap because the tie rule is
"alphabetically smallest ready job", so the answer is one specific order rather
than any legal one.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

import heapq

# ---- Given data ----
REFIT_JOBS: list[str] = [
    "anode-swap",
    "bilge-clean",
    "blast",
    "dock-in",
    "float-out",
    "hull-survey",
    "paint",
    "prop-shaft",
    "sea-trial",
    "weld",
]

# The maintenance system emits ("dock-in", "hull-survey") from two different
# forms, so the same dependency arrives twice. Counting it twice would leave
# hull-survey waiting forever.
REFIT_RULES: list[tuple[str, str]] = [
    ("dock-in", "hull-survey"),
    ("hull-survey", "blast"),
    ("blast", "weld"),
    ("weld", "paint"),
    ("paint", "float-out"),
    ("float-out", "sea-trial"),
    ("dock-in", "bilge-clean"),
    ("bilge-clean", "paint"),
    ("hull-survey", "prop-shaft"),
    ("prop-shaft", "float-out"),
    ("prop-shaft", "anode-swap"),
    ("dock-in", "hull-survey"),
]

VALVE_JOBS: list[str] = ["fit-valve", "handover", "pressure-test", "sign-off"]

VALVE_RULES: list[tuple[str, str]] = [
    ("fit-valve", "pressure-test"),
    ("pressure-test", "sign-off"),
    ("sign-off", "fit-valve"),
    ("sign-off", "handover"),
]


# ---- Your task ----
def plan_refit(
    jobs: list[str], must_follow: list[tuple[str, str]]
) -> tuple[list[str], list[str]]:
    """Return a legal running order for the refit, and the jobs that never ran.

    Args:
        jobs: Every job in the refit. Names are unique.
        must_follow: Pairs (a, b) meaning job a must finish before job b
            starts. The same pair may arrive more than once; it still counts
            once.

    Returns:
        A pair (order, blocked). `order` takes the alphabetically smallest
        ready job at every step. `blocked` is the sorted list of jobs that
        never became ready — the jobs inside a loop, plus everything
        downstream of one.

    Raises:
        ValueError: If a pair names a job that is not in `jobs`.
    """
    known = set(jobs)
    holds_up: dict[str, set[str]] = {job: set() for job in jobs}
    waiting_on: dict[str, int] = {job: 0 for job in jobs}

    for before, after in must_follow:
        for name in (before, after):
            if name not in known:
                raise ValueError(f"must_follow names a job that is not in jobs: {name!r}")
        if after in holds_up[before]:
            continue  # the same dependency, said twice
        holds_up[before].add(after)
        waiting_on[after] += 1

    ready = [job for job in jobs if waiting_on[job] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        job = heapq.heappop(ready)
        order.append(job)
        for held in sorted(holds_up[job]):
            waiting_on[held] -= 1
            if waiting_on[held] == 0:
                heapq.heappush(ready, held)

    blocked = sorted(known - set(order))
    return order, blocked


# ---- Self-check ----
if __name__ == "__main__":
    refit_order, refit_blocked = plan_refit(REFIT_JOBS, REFIT_RULES)
    print(f"refit order   : {refit_order}")
    print(f"refit blocked : {refit_blocked}")

    valve_order, valve_blocked = plan_refit(VALVE_JOBS, VALVE_RULES)
    print(f"valve order   : {valve_order}")
    print(f"valve blocked : {valve_blocked}")

    print(f"nothing to do : {plan_refit([], [])}")
    print(f"no rules      : {plan_refit(['zinc-check', 'scrub'], [])}")
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        print(f"unknown job   : {refusal}")

    assert refit_order == [
        "dock-in",
        "bilge-clean",
        "hull-survey",
        "blast",
        "prop-shaft",
        "anode-swap",
        "weld",
        "paint",
        "float-out",
        "sea-trial",
    ]
    assert refit_blocked == []
    assert valve_order == []
    assert valve_blocked == ["fit-valve", "handover", "pressure-test", "sign-off"]
    assert plan_refit([], []) == ([], [])
    assert plan_refit(["zinc-check", "scrub"], []) == (["scrub", "zinc-check"], [])
    assert plan_refit(["weld"], [("weld", "weld")]) == ([], ["weld"])
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        assert "'grind'" in str(refusal)
    else:
        raise AssertionError("an unknown job should have been refused")
    print("All checks passed.")
```

**Two tables, built in one pass over the rules.** `waiting_on` answers "can
this job start yet?" and `holds_up` answers "who do I unblock when I finish?".
Every topological sort of this shape needs both, and building them together
means the rule list is read exactly once.

**The duplicate is handled by a set, not by a check.**

```python
if after in holds_up[before]:
    continue  # the same dependency, said twice
holds_up[before].add(after)
waiting_on[after] += 1
```

Because `holds_up[before]` is a `set`, membership is a single hash lookup, and
the count is only raised for a pair that is genuinely new. This is worth
noticing as a general move: when duplicates in the input would corrupt a
counter, keep the thing you are counting in a set and let the set be the
authority.

**The heap is the tie rule made mechanical.** `heapq.heapify(ready)` turns the
list of initially-ready jobs into a heap in one linear pass, and every
`heappop` after that hands back the alphabetically smallest job available *at
that moment*. Note the "at that moment": the answer is not the sorted job list,
and it is not the sorted list of any fixed group. It is a running choice, and
jobs join the pile as the plan unfolds.

**`for held in sorted(holds_up[job])` — the sort is not load-bearing, and it is
still worth writing.** The heap decides the order jobs come *out*, so the order
they go *in* cannot change the answer. Sorting here makes the program's
behaviour identical on any Python whose set iteration order differs, which is
one less thing to wonder about when a test fails on somebody else's machine.

**Nothing ever looks for a circle.** There is no colour, no path, no grey set.
The loop drains until the ready pile is empty, and then:

```python
blocked = sorted(known - set(order))
```

Anything not in `order` never reached a waiting count of zero, which means
something it was waiting on never finished, which — following that chain
backwards through a finite set of jobs — means it eventually leads back to a
job waiting on itself. That is a circle, proved, without a single line of code
that mentions one.

**`blocked` is deliberately more than the circle.** `handover` is not in the
valve plan's circle; it simply waits on `sign-off`, which is. The yard cannot
do `handover` today either, so it belongs in the list. If you ever need the
circle itself — for an error message somebody has to act on — that is
[Exercise 3](./exercise-03-batch-loop-audit.md)'s grey path, and the honest
design is to run this first and only reach for the colours when this comes up
short.

**Empty input needs no special case.** With no jobs, both tables are empty, the
ready pile is empty, the loop does not run, and `sorted(set() - set())` is
`[]`. Code that handles the empty case by not being surprised by it is better
than code that handles it with an `if`.

## Run it

Copy the worked answer on this page into `exercise-04-refit-order.py` and run it:

```bash
python exercise-04-refit-order.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-04-refit-order.py`.

## Common bugs to catch

- **The duplicate rule silently shortens the plan.** You used a `set` for
  `holds_up` and raised `waiting_on` without checking whether the pair was new:

  ```text
  refit order   : ['dock-in', 'bilge-clean']
  refit blocked : ['anode-swap', 'blast', 'float-out', 'hull-survey', 'paint', 'prop-shaft', 'sea-trial', 'weld']
  Traceback (most recent call last):
      assert refit_order == [
             ^^^^^^^^^^^^^^^
  AssertionError
  ```

  Eight jobs blocked and not one of them is in a circle. `hull-survey` is
  waiting on two copies of a dependency that only arrives once, because the set
  kept one copy and the counter kept two — and everything behind it inherits
  the wait. Nothing raised until the assert. This is the failure mode the
  exercise is built around: wrong, quiet, and entirely plausible on a first
  read of the output. Guard the increment on whether the set actually grew, and
  the two tables can never disagree again.

- **`TypeError: cannot unpack non-iterable NoneType object`** on the very first line:

  ```text
  Traceback (most recent call last):
      refit_order, refit_blocked = plan_refit(REFIT_JOBS, REFIT_RULES)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  The correct first run of the starter. A function whose body is `...` returns
  `None`, and `a, b = None` is what that message is complaining about.

- **`KeyError` instead of your `ValueError`.**

  ```text
  Traceback (most recent call last):
      holds_up[before].add(after)
      ~~~~~~~~^^^^^^^^
  KeyError: 'grind'
  ```

  You used the name before checking it. `KeyError: 'grind'` is a message about
  a dictionary; `must_follow names a job that is not in jobs: 'grind'` is a
  message about the yard's data. Check both halves of the pair at the top of
  the loop, before either table is touched.

- **The order is valid but not the one asked for.** You used a `deque`:

  ```text
  refit order   : ['dock-in', 'hull-survey', 'bilge-clean', 'blast', ...]
  Traceback (most recent call last):
      assert refit_order == [
             ^^^^^^^^^^^^^^^
  AssertionError
  ```

  Nothing about that order breaks a rule. It is a perfectly good plan. It is
  just not *the* plan, because a queue hands back whatever went in first, and
  what went in first depends on the order the rules were listed. If you find
  yourself arguing that your answer is also correct — it is, and the contract
  asked for a specific one precisely so that this argument cannot happen.

- **`blocked` contains jobs that did run**, or `order` and `blocked` overlap.
  You built `blocked` from the jobs with a non-zero count *during* the loop
  rather than by subtracting at the end. A job's count is non-zero for most of
  the run and zero later; only when the ready pile is finally empty does a
  non-zero count mean anything.

- **`ValueError: heap argument must be a list`,** or a heap that does not
  behave:

  ```text
  Traceback (most recent call last):
      heapq.heapify(ready)
      ~~~~~~~~~~~~~^^^^^^^
  TypeError: heap argument must be a list
  ```

  You built `ready` as a set or a generator. `heapq` works *on* a list, in
  place; it is a set of functions, not a container. `heapify` on a list is
  `O(V)`, which is why the shipped code builds the list first and heapifies it
  once, rather than pushing `V` times.

- **A self-following job crashes instead of blocking.** `("weld", "weld")` is a
  legal pair naming a real job, and it means weld must finish before weld
  starts. There is nothing to raise about — it is simply impossible, so `weld`
  ends up in `blocked`. If you special-cased it, you added a branch the
  algorithm did not need: its waiting count starts at one and nothing ever
  lowers it, which is exactly right without any help.

## Under the hood

<details>
<summary>Under the hood — why the leftovers are exactly the circle and its downstream, proved</summary>

The claim the whole algorithm rests on is this: **when the ready pile empties,
every job not yet written down is either in a circle or waiting on something
that is.**

Here is why. Take any leftover job. Its waiting count is above zero, so at
least one job it is waiting on was never written down — call that one its
*blamed* predecessor. That predecessor is also a leftover, so it has a blamed
predecessor of its own. Keep following the blame backwards.

There are finitely many jobs, so this walk must eventually revisit one. The
moment it does, you have followed a run of "waits on" arrows from a job back to
itself. That is a circle.

So every leftover is connected backwards to a circle. And the converse is
obvious: nothing in a circle can ever reach a waiting count of zero, because
every member is waiting on another member.

The contrapositive is the useful half in an interview: **if the order contains
every job, the plan has no circle in it.** One `O(V + E)` pass answers both
"give me an order" and "is this possible", and the second answer is free.

**Why the number of orders can be enormous.** With no rules at all, `n` jobs
have `n!` legal orders. Ten jobs is 3,628,800. That is why "return any valid
order" is the usual contract on a judge, and why this page adds a tie rule
instead: a specific answer is testable, and testable beats general when you are
learning the shape.

</details>

<details>
<summary>Under the hood — Kahn against the depth-first version, and what each gives you free</summary>

The next exercise answers the same question by walking the graph depth-first
and appending each job when it *finishes*. Both are `O(V + E)`. Both are
correct. Here is the honest comparison, which is what an interviewer is
actually asking for when they say "why this one?".

**Kahn gives you three things free.**

*The waves.* Drain the ready pile a whole round at a time instead of one job at
a time and each round is a set of jobs that can run **at the same moment**. That
is what `make -j` does, and the number of rounds is the shortest the plan can
possibly be, however many people you put on it. The mini-project builds on this.

*The leftovers.* Already discussed, and they arrive without a second pass.

*No depth at all.* It is a loop over a heap. There is no recursion to overflow
and nothing to move onto an explicit stack. On a hundred-thousand-job build
graph that is not a small thing.

**The depth-first version gives you two things free.**

*Shorter code.* No counts, no `holds_up` table. Walk, and append on the way
back out.

*The circle itself*, if you carry the three colours — the grey path names it,
where Kahn's leftovers only bound it.

**What each finds awkward.** Kahn cannot easily name the circle. The
depth-first version cannot easily produce waves, because it has no notion of
"at the same time" anywhere in it, and it cannot easily honour a
smallest-ready-first tie rule, because it never computes "ready" at all.

**The sentence worth memorising:** *"Kahn releases every job whose
prerequisites are done, so running out of ready work with jobs left over is
exactly a circle; it is iterative, it costs `O(V + E)`, and it hands me the
parallel waves for free — I would switch to the depth-first post-order if I
needed the circle itself rather than just its existence."*

</details>

## Acceptance checklist

- [ ] `python exercise-04-refit-order.py` prints seven report lines and then
      `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] The refit order begins `dock-in`, `bilge-clean`, `hull-survey`.
- [ ] `refit_blocked` is `[]` — the duplicated rule changed nothing.
- [ ] The valve plan returns `([], [...all four jobs...])`.
- [ ] `plan_refit([], [])` is `([], [])`.
- [ ] `plan_refit(REFIT_JOBS, [("dock-in", "grind")])` raises `ValueError`
      naming `grind`.
- [ ] Nothing in your file looks for a circle.
- [ ] You can say out loud why the leftovers are the circle plus its
      downstream.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 4: refit order`.

## Stretch

- **Return the waves instead of the single-file order.** Drain a whole round at
  a time, and each round is a set of jobs the yard can put separate gangs on.

  ```python
  def refit_waves(
      jobs: list[str], must_follow: list[tuple[str, str]]
  ) -> list[list[str]]:
      """Group the plan into rounds; every job in a round can start at once."""
      order, blocked = plan_refit(jobs, must_follow)
      if blocked:
          return []
      earliest: dict[str, int] = {}
      after: dict[str, list[str]] = {job: [] for job in jobs}
      for before, later in set(must_follow):
          after[before].append(later)
      for job in order:
          earliest.setdefault(job, 0)
          for later in after[job]:
              earliest[later] = max(earliest.get(later, 0), earliest[job] + 1)
      waves: list[list[str]] = [[] for _ in range(max(earliest.values(), default=-1) + 1)]
      for job in sorted(earliest):
          waves[earliest[job]].append(job)
      return waves
  ```

  ```text
  wave 1: ['dock-in']
  wave 2: ['bilge-clean', 'hull-survey']
  wave 3: ['blast', 'prop-shaft']
  wave 4: ['anode-swap', 'weld']
  wave 5: ['paint']
  wave 6: ['float-out']
  wave 7: ['sea-trial']
  ```

  Ten jobs, seven rounds. Seven is the shortest the refit can be even with
  unlimited gangs, because `sea-trial` genuinely cannot start until six other
  jobs have happened in sequence.

- **Count how many valid orders there are.** For a small plan, brute force it
  and be surprised.

  ```python
  from itertools import permutations

  def count_valid_orders(
      jobs: list[str], must_follow: list[tuple[str, str]]
  ) -> int:
      """How many arrangements of `jobs` break no rule. Small inputs only."""
      rules = set(must_follow)
      return sum(
          all(guess.index(a) < guess.index(b) for a, b in rules)
          for guess in permutations(jobs)
      )
  ```

  ```text
  4 jobs, 2 rules : 6 valid orders
  ```

  Six, out of twenty-four arrangements. Now imagine the refit's ten jobs and
  3,628,800 arrangements, and you can see why the contract picks one rather
  than asking you to describe them all. Do not run this past about eight jobs.

- **Find the jobs that could go anywhere.** A job with no rules attached to it
  at all is free to happen at any point, and spotting those is how a
  superintendent finds slack in a plan.

  ```python
  def unconstrained(jobs: list[str], must_follow: list[tuple[str, str]]) -> list[str]:
      """Jobs that neither wait on anything nor hold anything up."""
      named = {name for pair in must_follow for name in pair}
      return sorted(set(jobs) - named)
  ```

  ```text
  refit : []
  yard  : ['scrub', 'zinc-check']
  ```

  Nothing in the refit is free — every job is tied to something. That is itself
  a finding, and it is the kind of thing worth saying in a Examine step.
When your plan is right, move on to
[Exercise 5 — Firmware Install Order](./exercise-05-firmware-install-order.md),
which answers the same question from the other end.
