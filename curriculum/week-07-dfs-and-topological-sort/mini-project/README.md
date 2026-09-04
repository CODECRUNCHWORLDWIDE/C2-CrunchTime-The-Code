# Mini-Project — The Restart Planner

> **Topic:** one directed graph, four questions — is it startable, in what order, what can run at once, and what is holding everything up
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** no single function here is hard; making four passes over one graph agree with each other is the whole project
> **Target time:** 10 hours, spread across Thursday to Saturday
> **Why this one:** the exercises each drill one pass over a graph. Real work is never one pass. A supervisor with a cold plant does not want a topological order — they want to know whether the plan is sound, what to switch on first, how many people they need on shift, and which chain of stages decides how long the whole restart takes. Four questions, one graph, and every answer has to be the same shape of true. This is also the week's portfolio piece: two FRAME write-ups come out of it, one on the depth-first half and one on the topological-sort half.

<!-- no-runnable-file: what you hand in is a program in your own repository together with two FRAME write-ups and a recording of yourself delivering them, which is not something a script can produce. The runnable answer ships beside this page as restart-planner-solution.py, named after the project rather than after the page because a file called README.py would be a strange thing to ask anybody to download. It is linked from Download and run, and its output is the Expected output block below. -->

## The Brief

A dairy line has been shut down for its annual clean. Now it has to come back
up, and it cannot all come up at once.

Think of the plant as a room full of switches, except the switches argue. You
cannot start the boiler until the water softener is running, because the boiler
would scale up in an hour on raw water. You cannot start the softener until the
well pump is running, because there is nothing to soften. Every stage in the
plant is like that: it has a short list of other stages that must already be
running before anybody is allowed to switch it on.

Write that down and you have a **directed graph**. A graph is just dots and
arrows. The dots are stages. An arrow from the well pump to the softener means
"the well pump has to be going first". Nothing more mysterious than that.

Here is the plan you are given, as a dictionary. Each key is a stage, and the
list beside it is what that stage needs already running:

```python
NEEDS = {
    "air-compressor": [],
    "boiler": ["softener"],
    "capper": ["filler", "air-compressor"],
    "case-packer": ["capper", "labeller"],
    "chiller": ["well-pump"],
    "cip-loop": ["steam-header", "softener"],
    "filler": ["pasteuriser", "cip-loop", "air-compressor"],
    "glycol-loop": ["chiller"],
    "homogeniser": ["pasteuriser"],
    "labeller": ["filler"],
    "pasteuriser": ["steam-header", "glycol-loop", "cip-loop"],
    "silo-agitator": ["well-pump"],
    "softener": ["well-pump"],
    "steam-header": ["boiler"],
    "well-pump": [],
}
```

The shift supervisor wants four things out of it, and they want them in this
order, because each one is useless if the one before it came back wrong.

**One — is the plan startable at all?** If two stages each wait on the other,
nothing in that group can ever be switched on, and no amount of ordering will
help. This is the **loop question**, and it is answered with a depth-first walk
and three colours. A stage is *white* while you have not started looking at it,
*grey* while you are standing on it — that is, it is on the path you walked in
on — and *black* once you have finished it and everything under it. Walking into
a grey stage means you have arrived somewhere you never left. That is a loop.
Walking into a black stage means nothing at all: that part of the plant is
already proved clean.

If there is a loop, say what it is. "The plan has a loop" is a useless answer to
somebody standing in front of fifteen switches. `chiller -> well-pump ->
glycol-loop -> chiller` is an answer they can act on.

**Two — one legal start order, single file.** One stage at a time, each one
started only after everything it needs. There are usually many legal orders, so
the plan pins one down: at every step, start the **alphabetically smallest stage
that is ready**. That turns "any valid order" into one specific answer a test
can check exactly.

**Three — the crew waves.** Single file is safe and slow. In practice several
stages become startable at the same moment, and a crew can do them together. A
**wave** is every stage that is ready at once. The number of waves is how many
rounds the restart takes, which is how the supervisor works out how long the
line has to be down.

**Four — what is holding each stage up.** For every stage, how many distinct
stages must already be running underneath it — counting stages further down the
chain, not just the ones it names directly. And then the single longest run of
stages that have to be started one after another, because *that* chain is the
restart's real length. Shortening anything else buys you nothing.

Four questions, one graph, one program.

## Starter

Create `restart-planner.py` in your practice repo and paste this in. Fill in
every `TODO`. The file runs as pasted: `...` on its own line is a real Python
statement that does nothing, so every unfinished function quietly hands back
`None` and nothing explodes until something tries to use the result.

```python
"""restart-planner.py - the plant restart planner.

Four passes over one directed graph:
  1. find a loop, or prove there is none
  2. one legal single-file start order
  3. the crew waves
  4. what is holding each stage up, and the longest chain

Fill in every TODO, then run the file.
"""

from __future__ import annotations

import heapq

WHITE, GREY, BLACK = 0, 1, 2

NEEDS: dict[str, list[str]] = {
    "air-compressor": [],
    "boiler": ["softener"],
    "capper": ["filler", "air-compressor"],
    "case-packer": ["capper", "labeller"],
    "chiller": ["well-pump"],
    "cip-loop": ["steam-header", "softener"],
    "filler": ["pasteuriser", "cip-loop", "air-compressor"],
    "glycol-loop": ["chiller"],
    "homogeniser": ["pasteuriser"],
    "labeller": ["filler"],
    "pasteuriser": ["steam-header", "glycol-loop", "cip-loop"],
    "silo-agitator": ["well-pump"],
    "softener": ["well-pump"],
    "steam-header": ["boiler"],
    "well-pump": [],
}

BROKEN_NEEDS: dict[str, list[str]] = {**NEEDS, "well-pump": ["glycol-loop"]}


def every_stage(needs: dict[str, list[str]]) -> list[str]:
    """Every stage named anywhere in the plan, sorted."""
    # TODO: the keys, plus everything named in any needs list
    ...


def tidy_plan(needs: dict[str, list[str]]) -> dict[str, list[str]]:
    """The plan with every stage present as a key and no repeated needs."""
    # TODO: build a dict keyed by every_stage(); sort and de-duplicate each list
    ...


def find_need_loop(needs: dict[str, list[str]]) -> list[str] | None:
    """One circular wait, or None when the plan is sound."""
    # TODO: three colours, an explicit stack, and a path list you can slice
    ...


def restart_order(needs: dict[str, list[str]]) -> list[str]:
    """One legal single-file start order: smallest ready stage first."""
    # TODO: count what each stage waits on, then run the ready heap down
    ...


def restart_waves(needs: dict[str, list[str]]) -> list[list[str]]:
    """The same start order, grouped into waves the crew can run at once."""
    # TODO: the same counts, but drained one whole wave at a time
    ...


def stages_underneath(needs: dict[str, list[str]]) -> dict[str, int]:
    """How many distinct stages must already be running under each stage."""
    # TODO: walk the start order, union each stage's needs with theirs
    ...


def longest_chain(needs: dict[str, list[str]]) -> list[str]:
    """The longest run of stages that must be started one after another."""
    # TODO: walk the start order carrying a depth and a back-pointer
    ...


def print_report(needs: dict[str, list[str]]) -> None:
    """The whole restart report, in the order the supervisor reads it."""
    # TODO: the loop first; if there is one, say so and stop
    ...


if __name__ == "__main__":
    print("=== restart plan: line 2, after the annual clean ===")
    print_report(NEEDS)
    print()
    print("=== the same audit on last year's typed-in-wrong plan ===")
    print_report(BROKEN_NEEDS)
```

Four words you need before you start.

**Directed.** An arrow points one way. The well pump helps the softener; the
softener does not help the well pump. Week 6's undirected graphs let you walk
back down every edge you came up. Here you cannot, and that is what makes loops
possible in the first place.

**Waiting count.** For each stage, how many of its needs are still not running.
A stage whose waiting count is zero is *ready*. Starting a stage lowers the
waiting count of everything that named it. That is the whole of Kahn's
algorithm, and it never looks for a loop — it just notices when it has run out
of ready work with stages left over.

**Ready heap.** A heap is a list that always hands you its smallest item first,
for far less work than sorting the whole thing every time. `heapq.heappop` is
how "the alphabetically smallest ready stage" gets picked without re-sorting.

**Post-order.** Doing the work on the way back *up* out of a walk instead of on
the way down. Question four is post-order: you cannot say what is holding a
stage up until you have finished everything under it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/mini-project/README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `every_stage(needs)` returns every stage named anywhere, sorted — including
   stages that only ever appear inside somebody else's needs list.
2. `tidy_plan(needs)` returns a plan where every stage is a key, every needs list
   is sorted, and no need is listed twice.
3. `find_need_loop(needs)` returns one loop in "needs" order, rotated to begin at
   the alphabetically smallest stage in it and not repeating that stage at the
   end, or `None` when the plan is sound. `{"a": ["a"]}` returns `["a"]`.
4. `restart_order(needs)` returns every stage exactly once, each one after
   everything it needs, taking the alphabetically smallest ready stage at every
   step. On a plan with a loop it raises `ValueError` whose message spells the
   loop out.
5. `restart_waves(needs)` returns a list of waves, each wave sorted, every stage
   in exactly one wave, and the waves in start order.
6. `stages_underneath(needs)` returns `{stage: count}` where the count is the
   number of **distinct** stages anywhere below it, not the number of arrows out
   of it.
7. `longest_chain(needs)` returns the stages of one longest run, in start order.
   Ties go to the alphabetically smallest stage at every choice.
8. `print_report(needs)` prints the loop verdict first and stops there when there
   is a loop. On a sound plan it prints all four sections.
9. Empty input works everywhere: `restart_order({})` is `[]`,
   `restart_waves({})` is `[]`, `find_need_loop({})` is `None`.
10. Every function keeps its type hints and its docstring.

## Constraints

- **Keep the pending work in a list, not on the call stack.** Every walk in the
  shipped answer holds its unfinished stages in a Python list. The dairy line is
  fifteen stages deep, so a recursive version would be perfectly safe on it — and
  that is exactly why this constraint has to be stated rather than discovered.
  The scale check at the bottom of the file runs the same planner over a chain of
  twenty thousand stages, which is twenty times CPython's default limit of one
  thousand frames. A recursive version dies there with `RecursionError`.
  [Exercise 2](../exercises/exercise-02-conveyor-reachability.md) is the page
  that argues this out in full, including why raising the limit is not the fix.

- **De-duplicate the needs before counting them.** The maintenance system emits
  the same dependency from two different forms, so `["softener", "softener"]` is
  ordinary input. Count it twice and the boiler believes it is waiting on two
  things when it is waiting on one, its waiting count never reaches zero, and it
  silently lands in the "never started" pile. Nothing raises. The order just
  comes out short.

- **A stage that is only ever named as a need is still a stage.** `well-pump`
  would still be one even if nobody had given it a key of its own. Build the
  stage list from the keys *and* the values. Skipping this is the same bug as
  the one above wearing a different hat: the answer is short and nothing
  complains.

- **Report the loop, not just its existence.** A boolean is not an answer a
  supervisor can act on. Rotating the loop to start at its smallest stage costs
  two lines and makes the report reproducible, which matters the moment two
  people compare notes on the same broken plan.

- **Answer the loop question first, and stop if the answer is yes.** The other
  three passes are only meaningful on a sound plan, and running them anyway
  produces a confident, wrong, partial order. Order the report the way the
  supervisor reads it.

- **Do not compute the same thing twice in two ways.** `restart_waves` and
  `restart_order` both count what each stage is waiting on. They have to agree,
  so the shape of the plan is settled once, in `tidy_plan`, and both build on
  that. The day two functions each claim to know the plan, one of them is wrong
  and nobody knows which.

- **Plan sizes to expect: at most 20,000 stages and 60,000 dependencies.** That
  is the size of a real build graph, which is this same problem wearing overalls
  — see [Homework Problem 6](../homework/README.md#problem-6--system-design-warm-up-7).
  At that size only `O(V + E)` finishes: one look at every stage and one look at
  every dependency, and then it is done. The tempting alternative — for each
  stage, walk everything below it to find out what is holding it up — is
  `O(V x (V + E))`, which at twenty thousand stages is well over a billion steps
  for an answer that one pass already has.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python restart-planner.py
=== restart plan: line 2, after the annual clean ===
audit          : 15 stages, 20 dependencies, no loops

start order    : smallest ready stage first
   1  air-compressor
   2  well-pump
   3  chiller
   4  glycol-loop
   5  silo-agitator
   6  softener
   7  boiler
   8  steam-header
   9  cip-loop
  10  pasteuriser
  11  filler
  12  capper
  13  homogeniser
  14  labeller
  15  case-packer

crew waves     : 9 waves, every stage in a wave starts at once
  wave 1  air-compressor, well-pump
  wave 2  chiller, silo-agitator, softener
  wave 3  boiler, glycol-loop
  wave 4  steam-header
  wave 5  cip-loop
  wave 6  pasteuriser
  wave 7  filler, homogeniser
  wave 8  capper, labeller
  wave 9  case-packer

holding up     : distinct stages that must already be running
  12  case-packer
  10  capper
  10  labeller
   9  filler
   8  homogeniser
   7  pasteuriser
   4  cip-loop
   3  steam-header
   2  boiler
   2  glycol-loop
   1  chiller
   1  silo-agitator
   1  softener
   0  air-compressor
   0  well-pump

longest chain  : 9 stages, one after another
  well-pump -> softener -> boiler -> steam-header -> cip-loop -> pasteuriser -> filler -> capper -> case-packer

=== the same audit on last year's typed-in-wrong plan ===
audit          : loop found - chiller -> well-pump -> glycol-loop -> chiller
                 nothing can start; fix the loop, then re-plan

=== scale check ===
20000-stage chain: audited, ordered, waved, measured - no recursion used

all checks passed
```

Look at the crew waves against the longest chain. Nine waves, and the longest
chain is nine stages. That is not a coincidence, and it is worth a minute: a
wave number *is* the length of the longest chain ending at that stage, so the
number of waves can never be smaller than the longest chain, and the greedy wave
rule never makes it bigger. If your wave count comes out higher than your
longest chain, one of the two passes is wrong.

Look also at `labeller` and `capper`, both holding up ten stages while `filler`
holds up nine. Each of them sits directly on top of `filler`, so each holds up
everything `filler` does, plus `filler` itself. Counting arrows instead of
counting the stages underneath gives `labeller` a score of one, and the whole
column becomes meaningless.

## Steps

1. Create the file, paste the starter, and run it before writing anything. You
   get an `AttributeError` from the first line of `print_report` that tries to
   use a result. That is the correct starting point, not a problem.
2. Write `every_stage` and `tidy_plan` first. Everything else is built on them,
   and both are five lines. Check that `every_stage({"filler": ["capper"]})`
   returns `["capper", "filler"]` — the stage that has no key of its own is the
   one to watch.
3. Write `find_need_loop`. Get the recursive shape clear in your head first —
   colour grey on the way in, colour black on the way out — then move it onto an
   explicit stack. The stack holds pairs of `(stage, iterator over its needs)`,
   and the trick is that leaving the iterator in the stack is what lets you pick
   a stage back up where you left it.
4. Test the loop finder on `BROKEN_NEEDS` before you write anything else. If it
   cannot find a loop you know is there, nothing later will save you.
5. Write `restart_order`. Waiting counts, a heap of ready stages, pop, append,
   decrement. Then check the leftover count — that is your second, independent
   loop detector, and the two must agree on every plan you try.
6. Write `restart_waves` by copying `restart_order` and draining a whole wave at
   a time instead of one stage. Then go back and notice how much of the two
   functions is the same, and decide honestly what to share.
7. Write `stages_underneath`. It walks the start order, so every stage's needs
   are already computed by the time you reach it. No recursion required, and no
   memo table either — the order *is* the memo.
8. Write `longest_chain` the same way, carrying a depth and a back-pointer, then
   walk the back-pointers home and reverse.
9. Write `print_report` last. Loop verdict first.
10. Then write it a second way. Re-do question one with Kahn's leftover count
    instead of three colours, or re-do question two with a depth-first
    post-order instead of Kahn. Check that both spellings agree on both plans.
    That comparison is the material for your two FRAME write-ups.

## The Solution

```python
"""restart-planner-solution.py - the plant restart planner.

A dairy line has been shut down for its annual clean. Every stage in the plant
needs some other stages running before it can be started, and the shift
supervisor needs four things before anyone touches a switch:

  1. Is the plan even startable, or do two stages each wait on the other?
  2. One legal order to start everything in, single file.
  3. The crew waves - which stages can be started at the same moment.
  4. How much of the plant is holding up each stage, and which chain is
     longest, because that chain is how long the restart takes.

Every walk in this file keeps its pending work in a list on the heap rather
than on Python's call stack, so the same planner runs on a fifteen-stage dairy
line and on a twenty-thousand-stage chain without changing a line. The scale
check at the bottom proves it.

Run it:  python restart-planner-solution.py
"""

from __future__ import annotations

import heapq

# Three colours, and they mean exactly what Lecture 3 says they mean.
# WHITE: not started. GREY: on the path I am standing on right now.
# BLACK: finished, and everything under it is proved clean.
WHITE, GREY, BLACK = 0, 1, 2

# ---- The plant ----
# stage -> the stages that must already be running before it can start.
NEEDS: dict[str, list[str]] = {
    "air-compressor": [],
    "boiler": ["softener"],
    "capper": ["filler", "air-compressor"],
    "case-packer": ["capper", "labeller"],
    "chiller": ["well-pump"],
    "cip-loop": ["steam-header", "softener"],
    "filler": ["pasteuriser", "cip-loop", "air-compressor"],
    "glycol-loop": ["chiller"],
    "homogeniser": ["pasteuriser"],
    "labeller": ["filler"],
    "pasteuriser": ["steam-header", "glycol-loop", "cip-loop"],
    "silo-agitator": ["well-pump"],
    "softener": ["well-pump"],
    "steam-header": ["boiler"],
    "well-pump": [],
}

# Last year somebody typed the glycol loop into the well pump's needs. The
# plant would not start, and nobody could say why. This is that plan.
BROKEN_NEEDS: dict[str, list[str]] = {**NEEDS, "well-pump": ["glycol-loop"]}


def every_stage(needs: dict[str, list[str]]) -> list[str]:
    """Every stage named anywhere in the plan, sorted.

    A stage that only ever appears in somebody else's needs list is still a
    stage. Missing them is the quietest bug in this whole family of problems:
    the plan looks fine and the order comes out short.
    """
    seen = set(needs)
    for wants in needs.values():
        seen.update(wants)
    return sorted(seen)


def tidy_plan(needs: dict[str, list[str]]) -> dict[str, list[str]]:
    """The plan with every stage present as a key and no repeated needs.

    The maintenance system emits the same dependency from two different forms,
    so `["softener", "softener"]` is normal input. Counting it twice would tell
    the planner that the boiler is waiting on two things when it is waiting on
    one, and the boiler would never be released.
    """
    tidy = {stage: [] for stage in every_stage(needs)}
    for stage, wants in needs.items():
        tidy[stage] = sorted(dict.fromkeys(wants))
    return tidy


def find_need_loop(needs: dict[str, list[str]]) -> list[str] | None:
    """One circular wait, or None when the plan is sound.

    The loop is returned in "needs" order and rotated so it begins at the
    alphabetically smallest stage in it, so the same plan always reports the
    same loop the same way round.
    """
    plan = tidy_plan(needs)
    colour = {stage: WHITE for stage in plan}

    for start in sorted(plan):
        if colour[start] != WHITE:
            continue
        colour[start] = GREY
        path = [start]
        stack = [(start, iter(plan[start]))]

        while stack:
            stage, pending = stack[-1]
            stepped_down = False
            for nxt in pending:
                if colour[nxt] == GREY:
                    loop = path[path.index(nxt) :]
                    spin = loop.index(min(loop))
                    return loop[spin:] + loop[:spin]
                if colour[nxt] == WHITE:
                    colour[nxt] = GREY
                    path.append(nxt)
                    stack.append((nxt, iter(plan[nxt])))
                    stepped_down = True
                    break
            if not stepped_down:
                colour[stage] = BLACK
                path.pop()
                stack.pop()
    return None


def restart_order(needs: dict[str, list[str]]) -> list[str]:
    """One legal single-file start order: smallest ready stage first."""
    plan = tidy_plan(needs)
    waiting_on = {stage: len(plan[stage]) for stage in plan}
    unlocks: dict[str, list[str]] = {stage: [] for stage in plan}
    for stage, wants in plan.items():
        for want in wants:
            unlocks[want].append(stage)

    ready = [stage for stage in plan if waiting_on[stage] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        stage = heapq.heappop(ready)
        order.append(stage)
        for later in unlocks[stage]:
            waiting_on[later] -= 1
            if waiting_on[later] == 0:
                heapq.heappush(ready, later)

    if len(order) != len(plan):
        loop = find_need_loop(needs) or []
        raise ValueError("restart plan has a loop: " + " -> ".join(loop + loop[:1]))
    return order


def restart_waves(needs: dict[str, list[str]]) -> list[list[str]]:
    """The same start order, grouped into waves the crew can run at once."""
    plan = tidy_plan(needs)
    waiting_on = {stage: len(plan[stage]) for stage in plan}
    unlocks: dict[str, list[str]] = {stage: [] for stage in plan}
    for stage, wants in plan.items():
        for want in wants:
            unlocks[want].append(stage)

    wave = sorted(stage for stage in plan if waiting_on[stage] == 0)
    waves: list[list[str]] = []
    started = 0
    while wave:
        waves.append(wave)
        started += len(wave)
        freed: list[str] = []
        for stage in wave:
            for later in unlocks[stage]:
                waiting_on[later] -= 1
                if waiting_on[later] == 0:
                    freed.append(later)
        wave = sorted(freed)

    if started != len(plan):
        loop = find_need_loop(needs) or []
        raise ValueError("restart plan has a loop: " + " -> ".join(loop + loop[:1]))
    return waves


def stages_underneath(needs: dict[str, list[str]]) -> dict[str, int]:
    """How many distinct stages must already be running under each stage."""
    plan = tidy_plan(needs)
    beneath: dict[str, set[str]] = {}
    for stage in restart_order(needs):
        pool: set[str] = set()
        for want in plan[stage]:
            pool.add(want)
            pool |= beneath[want]
        beneath[stage] = pool
    return {stage: len(pool) for stage, pool in beneath.items()}


def longest_chain(needs: dict[str, list[str]]) -> list[str]:
    """The longest run of stages that must be started one after another."""
    plan = tidy_plan(needs)
    order = restart_order(needs)
    depth: dict[str, int] = {}
    beneath: dict[str, str | None] = {}
    for stage in order:
        best, best_from = 0, None
        for want in plan[stage]:
            if depth[want] > best:
                best, best_from = depth[want], want
        depth[stage] = best + 1
        beneath[stage] = best_from

    last = min(order, key=lambda stage: (-depth[stage], stage))
    chain: list[str] = []
    walker: str | None = last
    while walker is not None:
        chain.append(walker)
        walker = beneath[walker]
    chain.reverse()
    return chain


def print_report(needs: dict[str, list[str]]) -> None:
    """The whole restart report, in the order the supervisor reads it."""
    plan = tidy_plan(needs)
    links = sum(len(wants) for wants in plan.values())
    loop = find_need_loop(needs)

    if loop is not None:
        print(f"audit          : loop found - {' -> '.join(loop + loop[:1])}")
        print("                 nothing can start; fix the loop, then re-plan")
        return

    print(f"audit          : {len(plan)} stages, {links} dependencies, no loops")
    print()

    print("start order    : smallest ready stage first")
    for position, stage in enumerate(restart_order(needs), 1):
        print(f"  {position:2d}  {stage}")
    print()

    waves = restart_waves(needs)
    print(f"crew waves     : {len(waves)} waves, every stage in a wave starts at once")
    for number, wave in enumerate(waves, 1):
        print(f"  wave {number}  {', '.join(wave)}")
    print()

    underneath = stages_underneath(needs)
    print("holding up     : distinct stages that must already be running")
    for stage in sorted(underneath, key=lambda s: (-underneath[s], s)):
        print(f"  {underneath[stage]:2d}  {stage}")
    print()

    chain = longest_chain(needs)
    print(f"longest chain  : {len(chain)} stages, one after another")
    print(f"  {' -> '.join(chain)}")


def _straight_chain(length: int) -> dict[str, list[str]]:
    """A plan that is one stage deep, `length` stages long."""
    plan = {"stage-00000": []}
    for index in range(1, length):
        plan[f"stage-{index:05d}"] = [f"stage-{index - 1:05d}"]
    return plan


if __name__ == "__main__":
    print("=== restart plan: line 2, after the annual clean ===")
    print_report(NEEDS)
    print()

    print("=== the same audit on last year's typed-in-wrong plan ===")
    print_report(BROKEN_NEEDS)
    print()

    # The plant is fifteen stages deep at most. The scale check is the reason
    # every walk above uses an explicit stack anyway: twenty thousand stages in
    # a straight line is twenty times CPython's default 1000-frame limit, and a
    # recursive version of any of these functions dies on it.
    deep = _straight_chain(20_000)
    assert find_need_loop(deep) is None
    assert restart_order(deep)[:2] == ["stage-00000", "stage-00001"]
    assert len(restart_order(deep)) == 20_000
    assert len(restart_waves(deep)) == 20_000
    assert longest_chain(deep)[-1] == "stage-19999"

    assert find_need_loop({"a": ["a"]}) == ["a"]
    assert find_need_loop({}) is None
    assert restart_order({}) == []
    assert restart_waves({}) == []
    assert restart_order({"boiler": ["softener", "softener"]}) == ["softener", "boiler"]
    assert every_stage({"filler": ["capper"]}) == ["capper", "filler"]

    print("=== scale check ===")
    print("20000-stage chain: audited, ordered, waved, measured - no recursion used")
    print()
    print("all checks passed")
```

**Four passes, one tidy plan underneath.** `tidy_plan` is doing more work than
it looks like. It fills in the stages that had no key of their own, it sorts
every needs list so that "alphabetically smallest" is decided once rather than
in four places, and it drops duplicate needs so the waiting counts are honest.
Every other function starts by calling it. That is not tidiness for its own
sake: it is the only way the four answers can be guaranteed to be about the same
graph.

**The three colours are a claim about *where you are*, not about *what you have
seen*.** A visited set answers "have I been here?". The colours answer a sharper
question: grey means "I am standing on this stage right now — I walked in and I
have not walked back out". So an arrow into a grey stage is an arrow into your
own path, which is a loop by definition. An arrow into a *black* stage is
completely ordinary: that stage is finished, everything under it is finished,
and arriving there a second time proves nothing. Treating black as a loop is the
single most common wrong answer in this family, and it fires on any diamond —
two paths that split and meet again.

**The path list is what turns "there is a loop" into "here is the loop".**
`path` holds exactly the grey stages, in the order you walked into them. When
you meet a grey stage, everything from that stage to the end of `path` is the
loop, which is one slice. Rotating it to begin at its smallest member costs two
more lines and makes the report the same every time, which matters as soon as
two people compare notes on the same broken plan.

**The explicit stack holds an iterator, and that is the whole trick.**
Recursion remembers where it had got to in the `for` loop for free. An explicit
stack has to remember it on purpose, and `iter(plan[stage])` is how: the
iterator sits inside the stack entry, so when you come back to a stage the next
`for nxt in pending` picks up at the need you had not tried yet. Without that,
returning to a stage restarts its needs list from the beginning, and the walk
either never ends or ends short.

**Kahn's algorithm never looks for a loop.** `restart_order` counts what each
stage is waiting on, releases the ones waiting on nothing, and lowers the counts
as it goes. If a group of stages is in a loop, every one of them is waiting on
another one in the group forever, so none of them is ever released and the order
comes out short. The check is `len(order) != len(plan)` — one comparison, at the
end, and it is exact. Only then does it call the colour walk, to *name* the
loop, because the count knows there is one but not which stages are in it.

**The heap is what makes the answer single-valued.** Any order that respects the
arrows is legal, and there are hundreds of them here. `heapq` costs `O(log V)`
per push and pop where a `deque` costs `O(1)`, which at twenty thousand stages
is about fourteen extra comparisons each — nothing you can feel — and it buys a
result a test can check character for character. Choosing determinism you can
test over a constant factor you cannot measure is nearly always right.

**Waves are Kahn's algorithm with the draining done in rounds.** Same counts,
same releases; the only change is that a whole wave comes off before any of the
stages it frees goes on. The number of waves that comes out is the length of the
longest chain, because a stage cannot be in wave `k` unless something in wave
`k-1` was holding it up, all the way back to wave one.

**`stages_underneath` and `longest_chain` are post-order without recursion.**
Both need every stage below them finished before they can answer. Walking
`restart_order` gives them that for free: the order's whole promise is that
everything a stage needs comes earlier in it. So a plain `for` loop over the
order is a post-order traversal wearing different clothes — no stack, no memo
table, no risk of depth at all. When you already have a topological order, reach
for it before you reach for recursion.

**`stages_underneath` unions sets rather than adding numbers.** Adding the
counts of `filler` and `air-compressor` would count everything they share twice.
`capper` sits on both, and both sit on `air-compressor`, so the plant underneath
`capper` overlaps, and the only honest way to size it is to hold the actual
stages and let the set do the de-duplicating. It is the same reason the answer
to "how many people are in these two rooms" is not the sum of the two rooms.

## Run it

Copy the worked answer on this page into `restart-planner.py` and run it:

```bash
python restart-planner.py
```

It is the same program you are writing, under a name that will not collide with
your own `restart-planner.py`.

The scale check at the bottom is worth running on purpose. It builds a chain of
twenty thousand stages and puts all four passes through it. If you want to feel
why the constraint about the call stack is there, write `find_need_loop` the
recursive way in a scratch file and point it at the same chain.

## Common bugs to catch

- **The order comes out short, and the error is about the wrong thing.** You
  counted a duplicated need twice:

  ```text
  Traceback (most recent call last):
      raise ValueError("restart plan has a loop: " + " -> ".join(loop + loop[:1]))
                                                                        ~~~~^^^^
  TypeError: 'NoneType' object is not subscriptable
  ```

  Read that carefully. `restart_order` noticed its order was short and asked
  `find_need_loop` to name the loop. There is no loop, so it got `None` back,
  and slicing `None` blew up. The real bug is two stops earlier:
  `["softener", "softener"]` made the boiler's waiting count 2 when only one
  need was ever going to arrive. Fix it in `tidy_plan` with `dict.fromkeys`,
  which drops duplicates — and note the shipped code sorts afterwards, because
  "alphabetically smallest" has to be true of the needs lists too. The shipped
  code also writes `find_need_loop(needs) or []` for exactly this reason: a
  defensive `or []` turns a confusing `TypeError` into a message that at least
  names the right function.

- **`KeyError` on a stage that has no key of its own.**

  ```text
  Traceback (most recent call last):
      for want in plan[stage]:
                  ~~~~^^^^^^^
  KeyError: 'well-pump'
  ```

  `every_stage` only looked at `needs.keys()`. Any stage that nothing needs to
  say anything about — the ones at the very bottom of the plant, which are
  exactly the ones you start first — never got a key. Union the keys with every
  name inside every list.

- **Every diamond reports a loop.** You treated a black stage as a back-edge.
  `pasteuriser` and `cip-loop` both sit on `steam-header`; whichever one you
  finish first turns `steam-header` black, and then the second one walks into
  it. That is not a loop, it is a shared foundation. Only **grey** means loop.
  The fix is one comparison, and the bug survives every test whose graph happens
  to be a tree.

- **The walk never finishes, or finishes with stages missing.** You rebuilt the
  iterator each time round instead of keeping it in the stack:

  ```python
  stack.append((nxt, iter(plan[nxt])))     # right: made once, kept
  stage, pending = stack[-1]               # right: the same iterator, resumed
  ```

  If instead you write `for nxt in plan[stage]` at the top of the `while`, you
  start that stage's needs from the beginning every time you come back to it.
  Nothing raises. You just get a walk that does not terminate, or an answer that
  is quietly short.

- **`AttributeError: 'NoneType' object has no attribute 'values'`.** You ran the
  starter before filling a `TODO` in. That is the correct first run, and it
  proves the report is really calling your code:

  ```text
  Traceback (most recent call last):
      links = sum(len(wants) for wants in plan.values())
                                          ^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'values'
  ```

  A function whose whole body is `...` does not return `...`. It runs a
  statement that does nothing and falls off the end, and falling off the end of
  a Python function hands back `None`. That is why an unfinished stub is quiet
  until its result is used, and why the traceback points at the *user* of the
  value rather than at the function that never produced one.

- **The waves are right but there are more of them than the longest chain.** You
  released a freed stage into the *current* wave rather than the next one.
  Collect everything a wave frees into a separate list, and only make that list
  the next wave once the whole current wave has been drained. Mixing them turns
  the wave count back into the single-file order, one stage per wave, and the
  two answers stop agreeing.

- **`longest_chain` returns the chain backwards.** The back-pointers run
  downwards — each stage points at whichever of its needs sits deepest — so the
  list you build by following them starts at the top of the plant. Reverse it
  before returning, or the supervisor starts with the case packer.

## Under the hood

<details>
<summary>Under the hood — why the wave count and the longest chain are the same number</summary>

The report prints nine waves and a nine-stage longest chain, and that is a
theorem rather than a coincidence.

Give every stage a number: `level(s) = 1` if it needs nothing, and otherwise
`1 + max(level(n))` over everything `s` needs. That is exactly what
`longest_chain` computes, and the longest chain in the plan is the biggest level
in it.

Now watch the wave rule. Wave one is every stage of level 1, because a stage is
ready at the start precisely when it needs nothing. Suppose every stage of level
`k` or less has gone in waves 1 to `k`. A stage of level `k+1` has all its needs
at level `k` or below, so all of them have started, so it is ready — and it was
not ready any earlier, because one of its needs is at level exactly `k` and only
started in wave `k`. So it goes in wave `k+1`, and no earlier.

By induction, wave number equals level, and the number of waves equals the
biggest level, which is the length of the longest chain.

This is worth more than the trivia. It says the restart cannot be made shorter
by adding people. Nine waves means nine rounds, whether the crew is two or two
hundred, because the ninth stage genuinely cannot begin until the eighth has.
The longest chain has a name — the **critical path** — and every
project-scheduling tool you will ever meet is computing it. Adding capacity
shortens a plan only up to the critical path, and not one round further.

</details>

<details>
<summary>Under the hood — the other spelling of each half, and what each one gives you free</summary>

Both halves of this project can be written the other way round, and that pair of
comparisons is the material for your two write-ups.

**Question one, Kahn's way.** Run `restart_order` and check whether it came out
short. That is a loop detector, it is three lines, and it needs no colours at
all. What it will not tell you is *which* stages are in the loop: the leftovers
are the stages in the loop **plus everything downstream of one**, which on a big
plant is most of the graph. The colour walk names the loop exactly. So: Kahn for
the yes-or-no, colours for the report — which is why the shipped code uses both,
and calls the colour walk only once the count has already said there is
something to find.

**Question two, depth-first.** Walk the plan depth-first and append each stage
when you *finish* it. Because a stage is only finished once everything under it
is already on the list, the list comes out in start order with no waiting counts
and no heap. It is shorter code. It gives you loop detection free, if you carry
the colours while you walk. What it does not give you is waves — a depth-first
order has no notion of "at the same time" in it — and it cannot easily be made
to pick the alphabetically smallest *ready* stage, because "ready" is not
something it ever computes. That is the honest trade, and it is the answer to
"why Kahn here?".

**The one-sentence versions, worth having ready to say out loud.**

> *Kahn's algorithm releases every stage whose needs have all started, so
> running out of ready work with stages left over is exactly a loop; it costs
> `O(V + E)` — one look at every stage and one at every dependency — and it
> hands me the waves for free.*

> *The three colours say where I am rather than where I have been: grey is the
> path under my feet, so an arrow into grey is an arrow into my own path, and
> that is a loop; black is finished, and proves nothing.*

**Two named algorithms, and neither name is required.** Kahn's algorithm is from
Arthur Kahn's 1962 paper on topological sorting, and the depth-first post-order
version is usually credited to Robert Tarjan's graph work in the early 1970s.
You will meet both names in the reading. Nobody in an interview needs you to say
them; they need you to say what the algorithm does and what it costs. Names are
for finding the paper later.

</details>

## Acceptance checklist

- [ ] `python restart-planner.py` prints the four sections for `NEEDS`, then the
      loop verdict for `BROKEN_NEEDS`.
- [ ] The output matches the Expected output block character for character.
- [ ] `find_need_loop(BROKEN_NEEDS)` returns
      `['chiller', 'well-pump', 'glycol-loop']`.
- [ ] `find_need_loop({"a": ["a"]})` returns `["a"]`.
- [ ] `restart_order({"boiler": ["softener", "softener"]})` returns
      `["softener", "boiler"]`.
- [ ] `restart_order({})`, `restart_waves({})` and `find_need_loop({})` all
      return the empty answer rather than raising.
- [ ] The number of waves equals the length of the longest chain.
- [ ] No function in your file recurses. The planner runs on a 20,000-stage
      chain without anybody touching `sys.setrecursionlimit`.
- [ ] Every function has type hints and a docstring.
- [ ] Two FRAME write-ups pushed under `frame-writeups/c2-week-07/mini-project/`
      — see *What you hand in*, below.
- [ ] Committed to Git with a message like
      `Add Week 7 mini-project: the restart planner`.

### What you hand in

The program is half of it. The other half is the portfolio piece, and it is what
Mock #2 actually grades:

```text
frame-writeups/c2-week-07/mini-project/
├── README.md                        short overview, index, what you would do differently
├── problem-01-the-loop-audit.md     the depth-first half: three colours, the path slice
└── problem-02-the-restart-order.md  the topological half: waiting counts, waves, critical path
```

Each write-up is the full FRAME narration — Frame, Research constraints, Assess
options, Make the solution, Examine — on its half of this project, recorded at
ten minutes or more. Two rules make the pair worth more than two singles:

- **Each one must reject the other out loud.** Write-up one says why the colour
  walk is the right tool for naming a loop, and what Kahn's leftover count would
  have given instead. Write-up two says why Kahn is the right tool for the order
  and the waves, and what a depth-first post-order would have cost. Both
  arguments are in the second Under the hood block above, in one-sentence form.
- **Each one must link the other.** A reader arriving at either should be able
  to reach the whole picture in one click.

The recognition sentence at the top of each write-up is the thing to rehearse.
Two lines, said in under thirty seconds: what pattern this is, and what
invariant makes it correct.

## Stretch

- **Which dependency would help most if you could argue it away?** The restart
  is as long as its critical path, so the only dependencies worth arguing with
  are the ones on it.

  ```python
  def critical_pairs(needs: dict[str, list[str]]) -> list[tuple[str, str]]:
      """The (need, stage) pairs that lie on the longest chain."""
      chain = longest_chain(needs)
      return list(zip(chain, chain[1:]))
  ```

  ```text
  ('well-pump', 'softener')
  ('softener', 'boiler')
  ('boiler', 'steam-header')
  ('steam-header', 'cip-loop')
  ('cip-loop', 'pasteuriser')
  ('pasteuriser', 'filler')
  ('filler', 'capper')
  ('capper', 'case-packer')
  ```

  Eight pairs out of twenty dependencies. The other twelve can be argued about
  all day without the restart getting one minute shorter.

- **Count the crew you would need.** The widest wave is the largest number of
  people who can usefully be working at once.

  ```python
  def crew_needed(needs: dict[str, list[str]]) -> int:
      """The largest number of stages that can be started simultaneously."""
      return max((len(wave) for wave in restart_waves(needs)), default=0)
  ```

  ```text
  crew needed: 3
  ```

  Three, from wave two. Sending five people costs the same nine waves, which is
  the critical-path result from the first Under the hood block turned into a
  staffing decision.

- **Make the planner answer questions instead of printing a report.** Add
  `must_start_before(needs, a, b)` — is `a` anywhere underneath `b`? — and
  answer it from the sets `stages_underneath` already builds, rather than by
  walking the graph again for every question.

  ```python
  def build_lookup(needs: dict[str, list[str]]) -> dict[str, set[str]]:
      """Every stage's full set of stages underneath it, ready to query."""
      plan = tidy_plan(needs)
      beneath: dict[str, set[str]] = {}
      for stage in restart_order(needs):
          pool: set[str] = set()
          for want in plan[stage]:
              pool.add(want)
              pool |= beneath[want]
          beneath[stage] = pool
      return beneath
  ```

  ```text
  well-pump before case-packer?   True
  homogeniser before case-packer? False
  ```

  One pass up front, then every question is a set lookup. That is the shape of
  nearly every "answer many questions about one fixed structure" problem you
  will meet, and it is why the report builds the sets and only then throws away
  everything but their sizes.

---
When both write-ups are pushed, Week 7 is closed. Next:
[Week 8 — Heaps and Priority Queues](../../week-08-heaps-and-priority-queues/).
