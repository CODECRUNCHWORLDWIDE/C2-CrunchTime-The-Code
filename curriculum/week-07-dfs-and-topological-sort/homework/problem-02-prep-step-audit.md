# Problem 2 — Prep Step Audit

> **Topic:** directed cycle detection — the three-colour walk against Kahn's counting, and choosing between them out loud
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** this is the cheapest question in the whole scheduling family — not *what order*, just *is there one*. Cheap questions have more than one right answer, which is why this page is really about the choice rather than the code. An interviewer who asks "can all of these be done?" is waiting to hear you name two algorithms, say what each is actually computing, and pick one for a reason. Writing Kahn's and returning a bool without saying any of that gets the tick and loses the point.

## The Brief

A pastry kitchen keeps two lists on the wall.

The first is the **prep steps** — every job that has to happen before service.
Chill the dough. Roll the dough. Cut the shapes. Proof them. Bake. Glaze. Box.

The second is the **rules**, and each rule is a pair of steps. The pair
`("chill dough", "roll dough")` means: *chill the dough before you roll it.* It
does not say when to roll, or that rolling has to happen immediately after. It
says only that one comes before the other.

Your job is to answer one question, and only that question:

> **Can every step on the list be done, in some order that keeps every rule?**

Yes or no. You are not asked for the order. That comes later in the week, in
[Exercise 4 — Refit Order](../exercises/exercise-04-refit-order.md).

### When the answer is no

The answer is no when the rules chase each other round in a circle. Temper the
chocolate before you dip. Dip before it sets. And — somebody wrote this down
without thinking — let it set before you temper. Now there is no first step.
Whichever one you try, a rule says something else had to happen first, and
following those rules leads you back to where you started. Nothing can begin, so
nothing can be done.

That is the only way the answer is no. Everything else is schedulable.

### The trap: two branches that meet again

Here is a rule set that is perfectly fine, and that a great many first attempts
call a circle:

```
measure  ->  mix wet   ->  combine
measure  ->  mix dry   ->  combine
```

Walk it. Start at `measure`. Go down through `mix wet` to `combine`, and
`combine` has nothing after it, so that branch is finished. Come back up. Now go
down through `mix dry`, and you arrive at `combine` **again**.

You have been here before. That is not the same as being in a circle.

Being in a circle means arriving somewhere you are *still standing* — a step
further up the very path you are walking right now. `combine` is not that. You
finished with `combine` and walked away from it. Reaching it a second time from a
different branch is just two jobs that both feed the same next job, which is what
a kitchen looks like.

Telling those two situations apart is exactly what the three colours are for, and
it is the reason this problem is Medium rather than Easy.

## Starter

Create `problem-02-prep-step-audit.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""problem-02-prep-step-audit.py -- can the prep list be scheduled at all?

Build the rules into an "unblocks" map, then answer yes or no. Write both
routes -- the three-colour walk and Kahn's counting -- so you can compare them
on the same inputs and defend the one you ship.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

from collections import deque

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
BISCUIT_STEPS = [
    "chill dough",
    "roll dough",
    "cut shapes",
    "proof",
    "bake",
    "glaze",
    "box",
]
BISCUIT_RULES = [
    ("chill dough", "roll dough"),
    ("roll dough", "cut shapes"),
    ("cut shapes", "proof"),
    ("proof", "bake"),
    ("bake", "glaze"),
    ("glaze", "box"),
]

DIAMOND_STEPS = ["measure", "mix wet", "mix dry", "combine"]
DIAMOND_RULES = [
    ("measure", "mix wet"),
    ("measure", "mix dry"),
    ("mix wet", "combine"),
    ("mix dry", "combine"),
]

CIRCLE_STEPS = ["temper chocolate", "dip", "set", "wrap"]
CIRCLE_RULES = [
    ("temper chocolate", "dip"),
    ("dip", "set"),
    ("set", "temper chocolate"),
    ("set", "wrap"),
]


# ---- Your task ----
def _rules_by_step(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> dict[str, list[str]]:
    """Turn the rule list into "once this step is done, these become possible"."""
    # TODO 1: start every step with an empty list of things it unblocks.
    # TODO 2: reject a rule naming a step that is not on the list, by name.
    ...


def can_schedule(steps: list[str], must_precede: list[tuple[str, str]]) -> bool:
    """Say whether every prep step can be done in some legal order."""
    # TODO 3: the three-colour walk. Grey means "on the path I am standing on
    #         right now". A rule pointing at grey is the circle. A rule pointing
    #         at black is a branch already finished, and is fine.
    ...


def can_schedule_by_counting(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> bool:
    """The same answer, reached by Kahn's counting instead."""
    # TODO 4: tally how many rules hold each step back, peel off the zeroes,
    #         and see whether every step came off in the end.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for label, steps, rules in [
        ("biscuit line", BISCUIT_STEPS, BISCUIT_RULES),
        ("two branches that meet", DIAMOND_STEPS, DIAMOND_RULES),
        ("rules in a circle", CIRCLE_STEPS, CIRCLE_RULES),
        ("nothing on the list", [], []),
    ]:
        print(f"{label:24s} -> {can_schedule(steps, rules)}")
        assert can_schedule(steps, rules) == can_schedule_by_counting(steps, rules)

    assert can_schedule(BISCUIT_STEPS, BISCUIT_RULES) is True
    assert can_schedule(DIAMOND_STEPS, DIAMOND_RULES) is True
    assert can_schedule(CIRCLE_STEPS, CIRCLE_RULES) is False
    assert can_schedule([], []) is True
    assert can_schedule(["proof"], [("proof", "proof")]) is False

    try:
        can_schedule(BISCUIT_STEPS, [("bake", "wash up")])
    except ValueError as err:
        assert "wash up" in str(err)
    else:
        raise AssertionError("a rule naming an unlisted step should raise ValueError")

    print("All checks passed.")
```

Three words you need before you start.

**Unblocks map.** A dict from each step to the steps that become possible once it
is done. You build it by walking the rules once: rule `(a, b)` appends `b` to
`a`'s list. It is the adjacency list from Problem 1, with the arrows now pointing
one way only.

**The three colours.** White is a step you have not looked at. Grey is a step you
have walked into and are still inside — it is on the path under your feet right
now. Black is a step whose every branch you have followed to the end and come
back from. The whole algorithm is those three words plus one rule: *an arrow onto
grey is a circle; an arrow onto black is not*.

**In-degree, or "waiting on".** For each step, how many rules still stand between
it and being allowed to start. A step waiting on nothing is ready. Doing a ready
step lowers the count of everything it unblocks. That is Kahn's, in two sentences.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/homework/problem-02-prep-step-audit.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `can_schedule(steps, must_precede)` returns `True` when a legal order exists
   and `False` when the rules form a circle. It never returns an order.
2. `can_schedule([], [])` is `True`. Nothing to do is trivially doable.
3. `can_schedule(["proof"], [("proof", "proof")])` is `False`. A step cannot come
   before itself.
4. `can_schedule(DIAMOND_STEPS, DIAMOND_RULES)` is `True`. Two branches meeting
   at the same later step is not a circle.
5. A rule naming a step that is not in `steps` raises `ValueError`, and the
   message contains that step's name.
6. You implement **both** routes and assert they agree on every case in the
   self-check. Shipping one is the deliverable; writing both is the assignment.
7. Your FRAME write-up names both, says what each is computing, and defends the
   one you shipped. "I used Kahn's because I remember Kahn's" is not a defense.
8. Type hints and a docstring on every function.

## Constraints

- **At most 5,000 prep steps and 20,000 rules.** Those numbers are picked so that
  `O(V + E)` finishes instantly and anything quadratic does not. A rebuild of the
  unblocks map inside the loop — "for each step, scan the rules to see which ones
  point at it" — is 5,000 × 20,000 = 100 million reads for an answer that needs
  25,000.

- **The recursive colour walk is only safe while the longest chain of rules stays
  under about 900 steps.** 5,000 steps in a single chain is 5,000 frames, and
  CPython stops at 1,000. If you ship the recursive colour walk you must say that
  out loud and say what you would do instead — the explicit stack from
  [Exercise 2 — Conveyor Reachability](../exercises/exercise-02-conveyor-reachability.md),
  which the Stretch below writes. Kahn's has no such ceiling because it is a loop.

- **Step names are strings and are compared exactly.** `"bake"` and `"Bake"` are
  two different steps. Nothing about this problem needs case-folding, and adding
  it invents a rule the kitchen never asked for.

- **A step may appear in `steps` more than once.** Building the map with
  `{step: [] for step in steps}` collapses the repeat into one entry, which is
  the sane reading: the list is a set of jobs, written down casually.

- **Do not answer by producing an order and then throwing it away.** You may
  *use* Kahn's, whose counting happens to build an order — that is fine, and the
  order falls out for free. What is not fine is writing the topological sort from
  Exercise 4, returning `len(order) == len(steps)`, and calling it a design. The
  design is the sentence you say about why.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-prep-step-audit-solution.py
biscuit line             -> True
two branches that meet   -> True
rules in a circle        -> False
nothing on the list      -> True
a 502-step list whose circle is in the first two steps
  colour walk   : False, after entering 2 steps
  Kahn counting : False, after reading 502 steps
All checks passed.
```

The last two lines are the whole argument on this page, measured rather than
asserted. Both routes answer `False`. The colour walk answers it having stepped
into **two** of the 502 prep steps: it walked into `swap pans`, walked into
`clear rack`, saw a rule pointing straight back at the grey step under its feet,
and stopped. Kahn's cannot stop early, because before it can find a single ready
step it has to build a waiting-on tally for **every** step on the list.

Both are `O(V + E)` in the worst case. The difference is what happens in the
lucky case, and the lucky case is common — a circle is usually a small mistake in
a big file.

## Steps

1. Create the file, paste the starter, and run it. The first `print` blows up
   because `can_schedule` still returns `...` and an f-string is happy to print
   `Ellipsis` — so actually you get a *wrong-looking line*, not a crash, until
   the first `assert`. Read that carefully: a stub that returns `...` fails
   *quietly* here. Note it.
2. Write `_rules_by_step` first, with the validation inside it. Both routes need
   it, and putting the check in one place means neither route can forget it.
3. Print the map for `DIAMOND_RULES` before you go further. Four steps,
   `combine` unblocking nothing. Trace the walk on paper: which step is grey
   when you reach `combine` the second time?
4. Write the colour walk. Colour grey on entry, loop the unblocked steps, colour
   black on the way out. Three branches inside the loop: grey means return
   `False`; white means recurse; black means do nothing at all. **That third
   branch being empty is the answer to the diamond.**
5. Write the outer loop over every step, so a rule set in two disconnected halves
   still gets both halves looked at.
6. Write Kahn's counting beside it and assert the two agree on all four cases.
   When they disagree, the diamond is the one to look at first.
7. Build the front-loaded case from the Expected output — a circle in the first
   two steps and a long chain after it — and count what each route touches. Now
   you have a number to put in your write-up instead of an adjective.

## The Solution

```python
"""problem-02-prep-step-audit-solution.py -- can the prep list be scheduled at all?

A pastry kitchen writes down its prep steps and the rules between them. A rule
(a, b) means step a has to be finished before step b can start. This page asks
the cheapest question in the family: is there a legal order at all, yes or no?
No order is produced.

Two routes answer it, both O(V + E) -- one look at every step and one look at
every rule, and then it is done:

  * the three-colour walk, which can stop the instant it meets a step that is
    already on the path it is standing on, and
  * Kahn's counting, which reads every step to build its waiting-on table
    before it can start, and so always pays for the whole list.

This file ships the colour walk and keeps the counting version beside it so the
two can be run against the same inputs and compared.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

from collections import deque

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
BISCUIT_STEPS = [
    "chill dough",
    "roll dough",
    "cut shapes",
    "proof",
    "bake",
    "glaze",
    "box",
]
BISCUIT_RULES = [
    ("chill dough", "roll dough"),
    ("roll dough", "cut shapes"),
    ("cut shapes", "proof"),
    ("proof", "bake"),
    ("bake", "glaze"),
    ("glaze", "box"),
]

# Two branches that meet again. "combine" is reached down both, and the second
# arrival lands on a step that is already finished -- not a circle.
DIAMOND_STEPS = ["measure", "mix wet", "mix dry", "combine"]
DIAMOND_RULES = [
    ("measure", "mix wet"),
    ("measure", "mix dry"),
    ("mix wet", "combine"),
    ("mix dry", "combine"),
]

# The rules chase each other: temper before dip, dip before set, set before
# temper.
CIRCLE_STEPS = ["temper chocolate", "dip", "set", "wrap"]
CIRCLE_RULES = [
    ("temper chocolate", "dip"),
    ("dip", "set"),
    ("set", "temper chocolate"),
    ("set", "wrap"),
]

# A long list whose circle sits in the first two steps. The colour walk finds it
# without reading the rest; the counting version reads all of it first.
BUSY_STEPS = ["swap pans", "clear rack"] + [f"tray {slot:03d}" for slot in range(500)]
BUSY_RULES = [("swap pans", "clear rack"), ("clear rack", "swap pans")] + [
    (f"tray {slot:03d}", f"tray {slot + 1:03d}") for slot in range(499)
]


def _rules_by_step(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> dict[str, list[str]]:
    """Turn the rule list into "once this step is done, these become possible".

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        A dict from each step to the steps it unblocks.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    after: dict[str, list[str]] = {step: [] for step in steps}
    for earlier, later in must_precede:
        for name in (earlier, later):
            if name not in after:
                raise ValueError(
                    f"rule names prep step {name!r}, which is not on the list"
                )
        after[earlier].append(later)
    return after


def _audit_by_colour(after: dict[str, list[str]]) -> tuple[bool, int]:
    """The three-colour walk.

    White is a step not looked at yet, grey is a step on the path we are
    standing on right now, black is a step whose whole branch is finished. A
    rule that points at a grey step is the circle. A rule that points at a black
    step is a branch we already cleared, and is fine.

    Args:
        after: The unblocks-map from _rules_by_step.

    Returns:
        (schedulable, steps_entered). The second number is how many prep steps
        the walk actually stepped into before it could answer.
    """
    colour: dict[str, int] = {step: WHITE for step in after}
    entered = 0

    def walk(step: str) -> bool:
        nonlocal entered
        entered += 1
        colour[step] = GREY
        for later in after[step]:
            if colour[later] == GREY:
                return False
            if colour[later] == WHITE and not walk(later):
                return False
        colour[step] = BLACK
        return True

    for step in after:
        if colour[step] == WHITE and not walk(step):
            return (False, entered)
    return (True, entered)


def _audit_by_counting(after: dict[str, list[str]]) -> tuple[bool, int]:
    """Kahn's counting.

    Every step gets a tally of how many rules are still holding it back. Steps
    on zero are ready; doing one lowers the tally of everything it unblocks. If
    the ready pile runs dry before every step has been done, the leftovers are
    holding each other back in a circle.

    Args:
        after: The unblocks-map from _rules_by_step.

    Returns:
        (schedulable, steps_read). The second number is how many prep steps had
        to be read to build the waiting-on table, which is all of them.
    """
    waiting_on: dict[str, int] = {}
    steps_read = 0
    for step in after:
        waiting_on[step] = 0
        steps_read += 1
    for laters in after.values():
        for later in laters:
            waiting_on[later] += 1

    ready: deque[str] = deque(step for step in after if waiting_on[step] == 0)
    done = 0
    while ready:
        step = ready.popleft()
        done += 1
        for later in after[step]:
            waiting_on[later] -= 1
            if waiting_on[later] == 0:
                ready.append(later)
    return (done == len(after), steps_read)


def can_schedule(steps: list[str], must_precede: list[tuple[str, str]]) -> bool:
    """Say whether every prep step can be done in some legal order.

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        True when a legal order exists, False when the rules chase each other in
        a circle. An empty list with no rules is True -- nothing to do is
        trivially doable.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    return _audit_by_colour(_rules_by_step(steps, must_precede))[0]


def can_schedule_by_counting(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> bool:
    """The same answer, reached by Kahn's counting instead. Kept for comparison.

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        The same bool can_schedule returns, on every input.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    return _audit_by_counting(_rules_by_step(steps, must_precede))[0]


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[str, list[str], list[tuple[str, str]]]] = [
        ("biscuit line", BISCUIT_STEPS, BISCUIT_RULES),
        ("two branches that meet", DIAMOND_STEPS, DIAMOND_RULES),
        ("rules in a circle", CIRCLE_STEPS, CIRCLE_RULES),
        ("nothing on the list", [], []),
    ]
    for label, steps, rules in cases:
        print(f"{label:24s} -> {can_schedule(steps, rules)}")

    colour_answer, entered = _audit_by_colour(_rules_by_step(BUSY_STEPS, BUSY_RULES))
    counting_answer, steps_read = _audit_by_counting(
        _rules_by_step(BUSY_STEPS, BUSY_RULES)
    )
    print(f"a {len(BUSY_STEPS)}-step list whose circle is in the first two steps")
    print(f"  colour walk   : {colour_answer}, after entering {entered} steps")
    print(f"  Kahn counting : {counting_answer}, after reading {steps_read} steps")

    assert can_schedule(BISCUIT_STEPS, BISCUIT_RULES) is True
    assert can_schedule(DIAMOND_STEPS, DIAMOND_RULES) is True
    assert can_schedule(CIRCLE_STEPS, CIRCLE_RULES) is False
    assert can_schedule([], []) is True
    assert can_schedule(["proof"], []) is True
    assert can_schedule(["proof"], [("proof", "proof")]) is False
    assert can_schedule(BUSY_STEPS, BUSY_RULES) is False

    for _, steps, rules in cases:
        assert can_schedule(steps, rules) == can_schedule_by_counting(steps, rules)
    assert can_schedule_by_counting(BUSY_STEPS, BUSY_RULES) is False

    try:
        can_schedule(BISCUIT_STEPS, [("bake", "wash up")])
    except ValueError as err:
        assert "wash up" in str(err)
    else:
        raise AssertionError("a rule naming an unlisted step should raise ValueError")

    print("All checks passed.")
```

**What was shipped, and why.** `can_schedule` runs the three-colour walk. The
question is yes-or-no and nothing else, and the colour walk is the route that can
answer *no* the moment it is sure, without reading the rest of the file. On the
502-step case that is 2 steps against 502. Both routes are `O(V + E)` — one look
at every step and one look at every rule, and then it is done — so this is not an
asymptotic claim. It is a claim about the common case, and it is the right kind
of claim to be able to make.

**The counter-argument, said fairly.** Kahn's counting is a loop, so it does not
care how long the longest chain of rules is; the colour walk is a recursion, and
recursion in CPython stops at about a thousand frames. On this page the shipped
route is the recursive one *because the page tells you the input is small enough*
— and that is a promise the page makes, not a property of the algorithm. Change
the bound and the answer changes with it. The Stretch below writes the colour
walk with an explicit stack, which is the version that has neither weakness, and
that is what production code would carry.

**The three branches in the loop, and the one that is empty.**

```python
for later in after[step]:
    if colour[later] == GREY:
        return False
    if colour[later] == WHITE and not walk(later):
        return False
```

Grey means the step is on the path beneath your feet — you entered it, you have
not left it, and here is a rule pointing back at it. That is the circle. White
means unexplored, so go and explore. Black — finished — matches neither `if`, so
nothing happens and the loop moves on.

That silent third case is the diamond. `combine` is black by the time `mix dry`
looks at it, so `mix dry` walks past it without a word. A version that says
"anything I have seen before is a circle" cannot tell grey from black, and reports
`False` on a kitchen that works perfectly well.

**Grey goes on at entry, black goes on at exit.** Not the other way round, and
not both at once. The gap between the two is precisely the time this step spends
on the current path, which is precisely what grey is supposed to mean. Setting
black at entry would make every step look finished immediately and hide every
circle; never setting black at all would leave finished branches grey and invent
circles out of the diamond.

**Kahn's counts nothing but arrivals.** `waiting_on[later] += 1` once per rule.
A step on zero has nothing left to wait for, so it goes in the ready pile.
Taking one out of the pile is "doing" it, which lets you knock one off the tally
of everything it unblocks — and anything that hits zero joins the pile. When the
pile runs dry, either everything came off (`done == len(after)`, no circle) or
some steps never reached zero, and the only way that happens is that they are
holding each other up.

**The outer loop matters more than it looks.** `for step in after` is not
decoration. A rule set can be two unconnected halves — the bread station and the
chocolate station — and a walk that starts only from the first step ever
mentioned would never look at the second half at all. Every step gets its turn;
the colour check makes the turns that were already covered free.

**The empty case, and why `True` is the right answer rather than a special
case.** With no steps, the colour dict is empty, the outer loop runs zero times,
and the function falls through to `return (True, entered)`. Nothing to schedule
is schedulable. It costs no code, and stating it in the contract is what stops a
caller wondering.

## Download and run

Download
[problem-02-prep-step-audit-solution.py](./problem-02-prep-step-audit-solution.py)
and run it:

```bash
python problem-02-prep-step-audit-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-02-prep-step-audit.py`.

## Common bugs to catch

- **`KeyError: 'wash up'`.** You built the unblocks map without checking that
  both ends of each rule are on the list:

  ```text
  Traceback (most recent call last):
      can_schedule(STEPS, [("bake", "wash up"), ("wash up", "chill dough")])
      ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      after[earlier].append(later)
      ~~~~~^^^^^^^^^
  KeyError: 'wash up'
  ```

  This one is *lucky*. The rule that broke was `("wash up", "chill dough")`,
  where the unknown name is on the left, so the dict lookup failed loudly. The
  earlier rule `("bake", "wash up")` put the unknown name on the *right*, and
  that one sailed through — `after["bake"].append("wash up")` is perfectly legal.
  A rule pointing at a step that does not exist would then either crash later,
  deep in the walk, or quietly not exist. Check **both** ends, at build time.

- **The diamond comes back `False`.** You used one visited set instead of three
  colours:

  ```text
  Traceback (most recent call last):
      assert can_schedule(DIAMOND_STEPS, DIAMOND_RULES) is True
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  The printed answer just above it is `False`. There is no traceback from the
  walk itself, because nothing illegal happened — you asked a slightly different
  question and got its correct answer. "Have I seen this before" and "am I
  standing on this right now" are not the same question, and the gap between them
  is exactly one extra colour.

- **`RecursionError: maximum recursion depth exceeded`.** You ran the recursive
  colour walk on a 5,000-step chain, which the constraints allow and the
  recursion does not:

  ```text
  Traceback (most recent call last):
      if colour[later] == WHITE and not walk(later):
                                        ~~~~^^^^^^^
      if colour[later] == WHITE and not walk(later):
                                        ~~~~^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Notice this fires on a rule set with **no circle in it at all** — it is a
  straight chain, the healthiest possible input. The recursion depth follows the
  longest chain, not the difficulty of the question. Either ship Kahn's, or ship
  the explicit stack from the Stretch, or say the bound out loud. Do not reach
  for `sys.setrecursionlimit`;
  [Exercise 2](../exercises/exercise-02-conveyor-reachability.md) explains why.

- **The circle is found but the diamond is slow.** You wrote the colour walk and
  never set anything to black. Every finished step stays grey, so later branches
  keep re-entering steps that are already done — and on a rule set shaped like a
  fan, the same subtree gets re-walked once per route into it. There is no
  exception and, on the four small cases, no wrong answer either. It shows up as
  a program that stops finishing on the 5,000-step input.

- **`can_schedule` returns something that is not a bool.** You returned the
  tuple from the audit helper instead of its first item, and `assert ... is True`
  fails with a bare `AssertionError` while the printed line reads
  `(True, 7)`. The `is True` in the checks is deliberate: `if (True, 7):` is
  truthy, so a looser check would have let this through.

## Under the hood

<details>
<summary>Under the hood — what each route is really computing, and where the extra information is</summary>

Both routes answer the yes-or-no. They compute rather different things on the
way there, and knowing what falls out for free is how you pick under pressure.

**The colour walk computes a classification of every rule.** In the language of
the textbook, it labels each edge as a tree edge, a back edge, a forward edge or
a cross edge — and "back edge" is the one that means circle. That labelling is
the raw material for Tarjan's algorithms: bridges, articulation points, strongly
connected components. If a follow-up question is going to be "which steps are
tangled *together*", the colour walk is already most of the way there. The
week's [Challenge 1 — Chokepoint Mains](../challenges/challenge-01-chokepoint-mains.md)
is that follow-up.

**Kahn's counting computes a layering.** Each time you drain the ready pile
completely and refill it, you have a set of steps with no rules between them —
steps that could all be done *at the same time*. Kahn's is therefore already an
answer to "how long does this take with unlimited hands", and to "how many hands
can I usefully keep busy". Problem 6 is about a build system, and that is
precisely the question a build system is asking.

**Two facts that surprise people.**

The first: Kahn's tells you *which* steps are in the tangle, and the colour walk
tells you *one* tangle it found. When Kahn's stops early, everything not yet
done is involved in some circle, and you get that set for free by subtraction.
The colour walk, by contrast, returns the moment it finds a back edge, so it
knows one circle and nothing about the others.

The second: neither route needs the graph to be connected, and neither needs a
sensible starting point. Both loop over every step. That is the same
disconnected-components handling as Problem 1, and it is the single most commonly
dropped line in both algorithms.

**A note on the constants.** `WHITE, GREY, BLACK = 0, 1, 2` is a tuple unpack of
three module-level names, and CPython looks a module global up in a dict every
time it is used. Inside a hot loop, `from enum import IntEnum` would be slower
still, because an `IntEnum` member is an object with `__eq__`. None of that
matters at 5,000 steps. It is worth knowing which of the two you reached for and
why, since "I used an enum for readability" and "I used ints because this is the
inner loop" are both good answers and "I did not think about it" is not.

</details>

## Acceptance checklist

- [ ] `python problem-02-prep-step-audit.py` prints four verdicts, the two
      touch-counts, then `All checks passed.`
- [ ] The diamond returns `True`, and you can say in one sentence why a naive
      visited set returns `False`.
- [ ] Both routes are implemented, and the self-check asserts they agree.
- [ ] Grey is set at entry and black at exit, in that order.
- [ ] The outer loop covers every step, so a rule set in two halves works.
- [ ] A rule naming an unknown step raises `ValueError` naming it, and both ends
      of the rule are checked.
- [ ] `can_schedule([], [])` is `True`.
- [ ] Your FRAME write-up names both routes, says what each computes, and
      defends the one you shipped with a reason that is not "habit".
- [ ] Committed to Git with a message like
      `feat(week-07): homework problem 2, prep step audit`.

## Stretch

- **Do not just say no — say which steps are chasing each other.** Keep the grey
  path in a list as you walk, and slice it when the back edge fires.

  ```python
  def circular_steps(steps: list[str], must_precede: list[tuple[str, str]]) -> list[str]:
      """Return one circle of steps, first step repeated at the end. [] if there is none."""
      after = _rules_by_step(steps, must_precede)
      colour: dict[str, int] = {step: WHITE for step in after}
      path: list[str] = []

      def walk(step: str) -> list[str]:
          colour[step] = GREY
          path.append(step)
          for later in after[step]:
              if colour[later] == GREY:
                  return path[path.index(later):] + [later]
              if colour[later] == WHITE:
                  found = walk(later)
                  if found:
                      return found
          colour[step] = BLACK
          path.pop()
          return []

      for step in after:
          if colour[step] == WHITE:
              found = walk(step)
              if found:
                  return found
      return []
  ```

  ```text
  circle: ['temper chocolate', 'dip', 'set', 'temper chocolate']
  no circle: []
  ```

  `path` is the grey steps, in order, and it is popped on the way back out — so
  it always holds exactly the path under your feet. That is the invariant grey
  was describing all along, now written down as a list you can print. A bug
  report saying *"set → temper chocolate closes the loop"* is worth ten saying
  *"not schedulable"*.

- **Ask for the order after all.** One line changes in Kahn's: keep the steps you
  take off the ready pile.

  ```python
  def one_order(steps: list[str], must_precede: list[tuple[str, str]]) -> list[str]:
      """Return one legal order, or [] when the rules form a circle."""
      after = _rules_by_step(steps, must_precede)
      waiting_on = {step: 0 for step in after}
      for laters in after.values():
          for later in laters:
              waiting_on[later] += 1
      ready: deque[str] = deque(s for s in after if waiting_on[s] == 0)
      order: list[str] = []
      while ready:
          step = ready.popleft()
          order.append(step)
          for later in after[step]:
              waiting_on[later] -= 1
              if waiting_on[later] == 0:
                  ready.append(later)
      return order if len(order) == len(after) else []
  ```

  ```text
  order: ['chill dough', 'roll dough', 'cut shapes', 'proof', 'bake', 'glaze', 'box']
  order for the circle: []
  ```

  The order was always there — this page just threw it away. That is worth
  noticing before you get to
  [Exercise 4 — Refit Order](../exercises/exercise-04-refit-order.md), which
  keeps it.

- **Take the depth limit off the colour walk.** An explicit stack, each entry
  holding the step and an iterator over what it unblocks.

  ```python
  def can_schedule_iteratively(steps: list[str], must_precede: list[tuple[str, str]]) -> bool:
      """The three-colour walk with the recursion replaced by a list."""
      after = _rules_by_step(steps, must_precede)
      colour: dict[str, int] = {step: WHITE for step in after}
      for start in after:
          if colour[start] != WHITE:
              continue
          stack = [(start, iter(after[start]))]
          colour[start] = GREY
          while stack:
              step, remaining = stack[-1]
              later = next(remaining, None)
              if later is None:
                  colour[step] = BLACK
                  stack.pop()
                  continue
              if colour[later] == GREY:
                  return False
              if colour[later] == WHITE:
                  colour[later] = GREY
                  stack.append((later, iter(after[later])))
      return True
  ```

  ```text
  5000-step chain, iterative: True
  5000-step chain plus a circle: False
  ```

  The iterator in each stack entry is the part worth studying. A recursive call
  remembers, for free, how far through the neighbour loop it had got; an explicit
  stack has to remember that itself, and an iterator is how. Popping when
  `next` runs dry is where black gets set — the exact moment the recursion would
  have returned.
When both routes agree, move on to
[Problem 3 — Safe Forwarding](./problem-03-safe-forwarding.md).
