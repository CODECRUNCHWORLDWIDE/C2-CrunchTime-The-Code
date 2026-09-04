# Exercise 5 — Feeder Tier Load

> **Topic:** summarising each level while it is still one batch, and what a repeated node does to a level
> **Lecture:** [01 — The BFS Template](../lecture-notes/01-the-bfs-template.md)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** Exercise 1 listed each level. This one *reduces* each level to a couple of numbers, which is what real reports actually ask for, and it is only easy if the level is still in one piece when you do it. The page also carries the trap that catches people on their first real network: a node wired to two parents, which is one node and belongs to one tier, however many times it is mentioned.

## The Brief

A substation feeds transformers. Those transformers feed more transformers.
Draw it and you get a fan spreading outward from the substation, and each
ring of the fan is a **tier**.

The planners want one row per tier:

- the **tier number**, counting the substation as tier 0,
- the **total amps** that whole tier draws,
- the **heaviest** single transformer on it, with the earlier name A to Z
  winning if two draw the same.

Two pieces of data. `FEEDER` says who feeds whom. `LOADS` says what each
transformer draws.

Three details that are decisions, and each of them is a decision somebody
made because the alternative was worse.

**GRANGE is listed twice.** BRINDLE feeds it and COLTON feeds it — that is
what the as-built drawing says, and it happens, because somebody ran a second
spur years later. GRANGE is still one transformer. It belongs to the first
tier that reaches it, and its amps are counted once. If you count it twice
your tier total is wrong by 45 amps and nothing tells you.

**IRTON has no entry in `LOADS`.** It was commissioned last week and nobody
has been out to meter it. It counts as 0 amps. Not "unknown", not an error —
an unmetered site is a site with no reading, and a reading of nothing is the
honest thing to put in the total. Say so on the page so the planner reading
the report knows what the number means.

**An unknown head raises `ValueError`.** `tier_report(FEEDER, LOADS, "MARSTON")`
is a question about a transformer that does not exist, and so is
`tier_report({}, LOADS, "SUBSTATION")`. Both are the same mistake and get the
same answer.

## Starter

Create `exercise-05-feeder-tier-load.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""exercise-05-feeder-tier-load.py — load on a distribution feeder, tier by tier.

A substation feeds transformers; those transformers feed more transformers.
The planners want one row per tier: how much current that whole tier draws,
and which single transformer on it draws the most. That is a level-by-level
walk with a sum and a maximum taken while the level is still in one piece.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Who feeds whom. GRANGE appears twice on purpose: the as-built has it
# spurred off two different transformers.
FEEDER: dict[str, list[str]] = {
    "SUBSTATION": ["ASHLEY", "BRINDLE", "COLTON"],
    "ASHLEY": ["DEEPING", "ELVASTON"],
    "BRINDLE": ["FRAMPTON", "GRANGE"],
    "COLTON": ["GRANGE", "HALLOW"],
    "DEEPING": [],
    "ELVASTON": ["IRTON"],
    "FRAMPTON": [],
    "GRANGE": ["JUNIPER"],
    "HALLOW": [],
    "IRTON": [],
    "JUNIPER": [],
}

# Amps drawn at each transformer. IRTON is not listed: it was commissioned
# last week and nobody has metered it yet.
LOADS: dict[str, int] = {
    "SUBSTATION": 0,
    "ASHLEY": 120,
    "BRINDLE": 95,
    "COLTON": 140,
    "DEEPING": 60,
    "ELVASTON": 75,
    "FRAMPTON": 210,
    "GRANGE": 45,
    "HALLOW": 210,
    "JUNIPER": 30,
}


class Tier(NamedTuple):
    """One row of the tier report."""

    depth: int
    total: int
    heaviest: str


# ---- Your task ----
def tier_report(
    feeder: dict[str, list[str]], loads: dict[str, int], head: str
) -> list[Tier]:
    """Return one row per tier of the feeder, working outward from `head`.

    Args:
        feeder: Each transformer mapped to the transformers it feeds.
        loads: Each transformer mapped to the amps it draws. A transformer
            with no entry counts as 0 amps, because an unmetered site is not
            a site drawing an unknown amount — it is a site with no reading.
        head: The substation the report starts from, at tier 0.

    Returns:
        A list of `Tier` rows, tier 0 first. `total` is the tier's combined
        amps; `heaviest` is the single largest draw on that tier, with the
        earlier name A to Z winning a tie.

    Raises:
        ValueError: If `head` is not a key in `feeder`.
    """
    # TODO: raise ValueError when head is not a key of feeder
    # TODO: deque seeded with head, a `seen` set holding head
    # TODO: each turn of the outer loop is one tier:
    #         snapshot len(queue), pop that many, collect their names
    #         then build one Tier row from the names you collected
    # TODO: sum with loads.get(name, 0); pick the heaviest with min() and a
    #       key that sorts by -amps first, then by name
    ...


# ---- Self-check ----
if __name__ == "__main__":
    report = tier_report(FEEDER, LOADS, "SUBSTATION")
    for row in report:
        print(f"tier {row.depth}: {row.total:>4} A   heaviest {row.heaviest}")

    assert [row.depth for row in report] == [0, 1, 2, 3]
    assert [row.total for row in report] == [0, 355, 600, 30]
    assert [row.heaviest for row in report] == [
        "SUBSTATION",
        "COLTON",
        "FRAMPTON",
        "JUNIPER",
    ]

    # FRAMPTON and HALLOW both draw 210 A on tier 2. The earlier name wins.
    assert LOADS["FRAMPTON"] == LOADS["HALLOW"] == 210
    assert report[2].heaviest == "FRAMPTON"

    # GRANGE is spurred off two transformers but belongs to one tier: the
    # first one that reaches it. Counting it twice would inflate tier 2.
    assert 60 + 75 + 210 + 45 + 210 == report[2].total  # GRANGE counted once

    # IRTON has no meter reading, so it adds nothing and never wins a tier.
    assert "IRTON" not in LOADS
    assert report[3].total == 30 and report[3].heaviest == "JUNIPER"

    # A leaf is a one-tier report all by itself.
    assert tier_report(FEEDER, LOADS, "DEEPING") == [Tier(0, 60, "DEEPING")]

    for feeder, head in ((FEEDER, "MARSTON"), ({}, "SUBSTATION")):
        try:
            tier_report(feeder, LOADS, head)
        except ValueError as error:
            assert "is not on this feeder" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
```

Two ideas before you start.

**A tie-break written as a sort key.** You want the biggest load, and where
two are equal, the earlier name. Write that as one key:
`key=lambda name: (-loads.get(name, 0), name)` and then take the `min`.
Negating the amps turns "biggest first" into "smallest first", so a single
`min` handles both rules in one pass. It reads oddly the first time and then
never again — you will use it for the rest of your career.

**`min` with a key, not `sorted(...)[0]`.** `min` walks the tier once holding
the best so far. Sorting the whole tier to read its first entry does more
work for the same answer, and says something untrue about what you asked for.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/exercises/exercise-05-feeder-tier-load.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `tier_report` returns a list of `Tier` records, tier 0 first, with no
   gaps in the tier numbers.
2. Tier 0 holds `head` alone.
3. `total` is the sum of the amps of every transformer on that tier, each
   counted once.
4. A transformer missing from `loads` contributes `0`.
5. `heaviest` is the transformer on that tier with the largest load; where
   two tie, the earlier name A to Z.
6. A transformer reachable by more than one route appears on exactly one
   tier — the first one that reaches it.
7. A `head` that is not a key of `feeder` raises `ValueError` whose message
   contains `is not on this feeder`.
8. `tier_report` keeps its type hints and its docstring.

## Constraints

- **Build the whole tier before you summarise it.** Collect the names first,
  then sum and pick. Trying to keep a running total and a running best inside
  the pop loop works here and stops working the moment the summary needs two
  passes — a median, a spread, a ratio. A tier is a batch; treat it as one.

- **Take the snapshot before you pop.** `for _ in range(len(queue))` reads
  the length once. This is the same line as Exercise 1 and the same reason:
  the queue grows while you are working through the tier, and the snapshot is
  what stops tomorrow's tier joining today's.

- **Mark a transformer seen when you queue it.** GRANGE is the reason. BRINDLE
  and COLTON are both on tier 1 and both feed GRANGE. Marking on the way out
  of the queue puts GRANGE in twice, so tier 2 lists it twice, so the total is
  45 amps too high and the report is quietly wrong. Nothing raises.

- **Read the loads with `loads.get(name, 0)`, never `loads[name]`.** IRTON has
  no reading. `loads[name]` raises `KeyError` and takes the whole report down
  because one meter has not been read yet, which is the wrong response to a
  perfectly ordinary situation.

- **Break the tie inside the key, not with an `if`.** One key expression says
  the whole rule in the order you would say it aloud: heaviest first, earlier
  name on a tie. A hand-rolled comparison spreads that rule over three lines
  and two of them are where the bug goes.

- **Use `min` with a negated first field rather than `max`.** `max` also
  works for the amps, but it would need `reverse`-style thinking for the name
  half — you want amps descending and names ascending in the same pass, and
  negating the number is the only part of a tuple key you can flip on its own.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
tier 0:    0 A   heaviest SUBSTATION
tier 1:  355 A   heaviest COLTON
tier 2:  600 A   heaviest FRAMPTON
tier 3:   30 A   heaviest JUNIPER
All checks passed.
```

Tier 2 is the row worth staring at. Six hundred amps across five
transformers — DEEPING, ELVASTON, FRAMPTON, GRANGE and HALLOW. FRAMPTON and
HALLOW both draw 210, and FRAMPTON is named because F comes before H. If
yours says HALLOW, your key has one part where it needs two: the tie fell
wherever the queue happened to leave it.

If your tier 2 total is 645 rather than 600, GRANGE is in there twice.

Tier 3 is IRTON and JUNIPER. IRTON contributes nothing, so the total is 30,
and JUNIPER is the heaviest by default. A tier of nothing but unmetered sites
would report `0` and name the alphabetically first of them, which is the
right thing for the report to say.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first use
   of the result.
2. Write the `ValueError` guard first and get those two self-checks passing.
3. Write the walk, collecting names per tier, and print the raw name lists
   before you summarise anything. Four lists: one, three, five, two. If tier
   2 has six names, GRANGE is in there twice and the fix is *where* you mark
   seen, not what you do afterwards.
4. Add the sum. Check tier 2 is 600 by adding the five numbers on paper.
5. Add the heaviest. Test it by temporarily raising HALLOW to 211 and
   confirming the answer moves — a tie-break you never watch change is a
   tie-break you have not tested.
6. Run the leaf case, `tier_report(FEEDER, LOADS, "DEEPING")`. One row. No
   special code should have been needed for it.
7. When `All checks passed.` prints, add a transformer to `FEEDER` that feeds
   something already on an earlier tier — say `"JUNIPER": ["ASHLEY"]` — and
   confirm the report does not change at all. That is the `seen` set earning
   its keep on a loop.

## The Solution

```python
"""exercise-05-feeder-tier-load-solution.py — load on a distribution feeder, tier by tier.

A substation feeds transformers; those transformers feed more transformers.
The planners want one row per tier: how much current that whole tier draws,
and which single transformer on it draws the most. That is a level-by-level
walk with a sum and a maximum taken while the level is still in one piece.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Who feeds whom. GRANGE appears twice on purpose: the as-built has it
# spurred off two different transformers.
FEEDER: dict[str, list[str]] = {
    "SUBSTATION": ["ASHLEY", "BRINDLE", "COLTON"],
    "ASHLEY": ["DEEPING", "ELVASTON"],
    "BRINDLE": ["FRAMPTON", "GRANGE"],
    "COLTON": ["GRANGE", "HALLOW"],
    "DEEPING": [],
    "ELVASTON": ["IRTON"],
    "FRAMPTON": [],
    "GRANGE": ["JUNIPER"],
    "HALLOW": [],
    "IRTON": [],
    "JUNIPER": [],
}

# Amps drawn at each transformer. IRTON is not listed: it was commissioned
# last week and nobody has metered it yet.
LOADS: dict[str, int] = {
    "SUBSTATION": 0,
    "ASHLEY": 120,
    "BRINDLE": 95,
    "COLTON": 140,
    "DEEPING": 60,
    "ELVASTON": 75,
    "FRAMPTON": 210,
    "GRANGE": 45,
    "HALLOW": 210,
    "JUNIPER": 30,
}


class Tier(NamedTuple):
    """One row of the tier report."""

    depth: int
    total: int
    heaviest: str


# ---- Your task ----
def tier_report(
    feeder: dict[str, list[str]], loads: dict[str, int], head: str
) -> list[Tier]:
    """Return one row per tier of the feeder, working outward from `head`.

    Args:
        feeder: Each transformer mapped to the transformers it feeds.
        loads: Each transformer mapped to the amps it draws. A transformer
            with no entry counts as 0 amps, because an unmetered site is not
            a site drawing an unknown amount — it is a site with no reading.
        head: The substation the report starts from, at tier 0.

    Returns:
        A list of `Tier` rows, tier 0 first. `total` is the tier's combined
        amps; `heaviest` is the single largest draw on that tier, with the
        earlier name A to Z winning a tie.

    Raises:
        ValueError: If `head` is not a key in `feeder`.
    """
    if head not in feeder:
        raise ValueError(f"{head!r} is not on this feeder")

    queue = deque([head])
    seen = {head}
    report: list[Tier] = []
    depth = 0
    while queue:
        names: list[str] = []
        for _ in range(len(queue)):  # this tier only — the queue grows below
            name = queue.popleft()
            names.append(name)
            for fed in feeder.get(name, ()):
                if fed not in seen:
                    seen.add(fed)
                    queue.append(fed)
        report.append(
            Tier(
                depth=depth,
                total=sum(loads.get(name, 0) for name in names),
                heaviest=min(names, key=lambda name: (-loads.get(name, 0), name)),
            )
        )
        depth += 1
    return report


# ---- Self-check ----
if __name__ == "__main__":
    report = tier_report(FEEDER, LOADS, "SUBSTATION")
    for row in report:
        print(f"tier {row.depth}: {row.total:>4} A   heaviest {row.heaviest}")

    assert [row.depth for row in report] == [0, 1, 2, 3]
    assert [row.total for row in report] == [0, 355, 600, 30]
    assert [row.heaviest for row in report] == [
        "SUBSTATION",
        "COLTON",
        "FRAMPTON",
        "JUNIPER",
    ]

    # FRAMPTON and HALLOW both draw 210 A on tier 2. The earlier name wins.
    assert LOADS["FRAMPTON"] == LOADS["HALLOW"] == 210
    assert report[2].heaviest == "FRAMPTON"

    # GRANGE is spurred off two transformers but belongs to one tier: the
    # first one that reaches it. Counting it twice would inflate tier 2.
    assert 60 + 75 + 210 + 45 + 210 == report[2].total  # GRANGE counted once

    # IRTON has no meter reading, so it adds nothing and never wins a tier.
    assert "IRTON" not in LOADS
    assert report[3].total == 30 and report[3].heaviest == "JUNIPER"

    # A leaf is a one-tier report all by itself.
    assert tier_report(FEEDER, LOADS, "DEEPING") == [Tier(0, 60, "DEEPING")]

    for feeder, head in ((FEEDER, "MARSTON"), ({}, "SUBSTATION")):
        try:
            tier_report(feeder, LOADS, head)
        except ValueError as error:
            assert "is not on this feeder" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
```

**The tier is collected first and summarised second.**

```python
names: list[str] = []
for _ in range(len(queue)):
    ...
    names.append(name)
    ...
report.append(Tier(depth=depth, total=..., heaviest=...))
```

The inner loop's only job is to produce `names`. The `Tier` is built
afterwards, from a list that is complete. That separation is why adding a
third column later — a count, an average, the spread between heaviest and
lightest — is one more line rather than a rewrite of the loop.

**The key says the whole rule, in the order you would say it.**

```python
key=lambda name: (-loads.get(name, 0), name)
```

Read it aloud: *most amps first, and where two tie, the earlier name.* Python
compares tuples left to right and stops at the first difference. FRAMPTON and
HALLOW both give `-210` in the first slot, so it moves to the second, and
`"FRAMPTON" < "HALLOW"` settles it.

The minus sign is the direction switch, and it only works on numbers — which
is exactly right here, because the name half genuinely wants to go A to Z. If
you reached for `reverse=True` instead you would flip *both* halves and the
tie would come out backwards.

**`seen` is marked at the door.**

```python
if fed not in seen:
    seen.add(fed)
    queue.append(fed)
```

BRINDLE and COLTON are both on tier 1. BRINDLE reaches GRANGE, marks it and
queues it. COLTON looks, finds it marked, and moves on. GRANGE lands on tier
2 exactly once, with its 45 amps counted exactly once.

Move `seen.add` down to where a name comes off the queue and both BRINDLE and
COLTON queue GRANGE before either copy is popped. The report still prints.
The total is just wrong. This is the single most valuable habit in the week,
and this page is where the cost of getting it wrong is a number on a
planner's desk rather than an exception on yours.

**`loads.get(name, 0)` is a statement about the world, not a safety net.** It
says: a site with no reading draws nothing as far as this report is
concerned. That is a claim you can defend to the planner. `loads[name]` makes
a different claim — that every site must have been metered — and the feeder
does not agree.

**Nothing here knows the feeder is a tree.** It is one, as it happens, apart
from GRANGE's double spur. But the code never assumes it: the `seen` set
handles a loop, a double spur and a plain branch identically. Add
`"JUNIPER": ["ASHLEY"]` and the report is unchanged, because ASHLEY was seen
on tier 1 and a second mention does not un-see it.

## Run it

Copy the worked answer on this page into `exercise-05-feeder-tier-load.py` and run it:

```bash
python exercise-05-feeder-tier-load.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-05-feeder-tier-load.py`.

## Common bugs to catch

- **Tier 2 totals 645.** No exception. GRANGE is counted twice because you
  mark `seen` when a name leaves the queue rather than when it joins:

  ```text
  tier 2:  645 A   heaviest FRAMPTON
  ```

  BRINDLE and COLTON both feed GRANGE and both are on tier 1. Move the
  `seen.add` up next to the `queue.append`.

- **`heaviest` on tier 2 is HALLOW.** Also no exception:

  ```text
  tier 2:  600 A   heaviest HALLOW
  ```

  Your key is the amps alone, so the tie fell wherever the queue left it. Add
  the name as the second part of the tuple.

- **`KeyError: 'IRTON'`.**

  ```text
  Traceback (most recent call last):
      print(hops["b"])
          ~~~~^^^^^
  KeyError: 'b'
  ```

  You read `loads[name]`. IRTON is on the feeder and not in the load table,
  which is the ordinary state of a newly commissioned site. `loads.get(name, 0)`.

- **`KeyError: 'JUNIPER'` from the *feeder*, not the loads.** You read
  `feeder[name]` for a transformer that is only ever mentioned as somebody's
  child. It does not happen with this data because every name is also a key,
  but it will the first time somebody edits the file. `feeder.get(name, ())`.

- **Every transformer lands on tier 1.** Your inner loop is `while queue:`
  instead of `for _ in range(len(queue))`, so the tiers ran together:

  ```text
  tier 0:    0 A   heaviest SUBSTATION
  tier 1:  985 A   heaviest FRAMPTON
  ```

  The snapshot is what separates one tier from the next.

- **`ValueError: min() iterable argument is empty`.**

  ```text
  Traceback (most recent call last):
      m = min(x for x in d if False)
  ValueError: min() iterable argument is empty
  ```

  You appended a `Tier` row for a tier with no names in it — usually because
  the outer loop keeps going one turn past the end. `while queue:` already
  stops at the right moment; nothing extra is needed.

- **The tiers come out in the wrong order.** You built the list and reversed
  it, or you sorted it. A queue produces tiers in order by construction. If
  you felt the need to sort them, something earlier is wrong.

## Under the hood

<details>
<summary>Under the hood — reducing a level, and what changes when the graph is not a tree</summary>

**Cost.** Every transformer is queued at most once, so with `T` transformers
and `S` spur entries the walk is `O(T + S)`. The summarising is another
single pass over each tier, and the tiers together hold every transformer
once, so that is `O(T)` on top. Total `O(T + S)` — linear in the size of the
feeder. Memory is `O(T)` for the `seen` set plus the widest tier in the
queue.

**Why "collect then reduce" scales and "accumulate as you go" does not.**
Running totals work for anything you can fold one item at a time: a sum, a
count, a maximum, a minimum. They stop working the moment the summary needs
to see the whole batch — a median needs the tier sorted, a standard deviation
needs the mean first, "the two heaviest" needs a comparison against something
you have not met yet. Collecting the tier costs one list per tier and buys
you every summary there is. At this size the memory is nothing; at any size,
the list is at most one tier wide.

**What the `seen` set is really claiming.** Not "this feeder has no loops" —
the code does not know that and does not need to. It claims something
narrower: *the first tier that reaches a transformer is the only tier it
belongs to.* On a feeder that is a genuine tree, every transformer has one
parent and the claim is trivially true. On a feeder with a double spur, like
GRANGE, the claim is a decision: GRANGE is one transformer at one depth, and
the depth is the shorter of the two routes to it. That is the right answer
for a load report, because the load is drawn once whatever the drawing says.

Worth noticing that this is the *same* claim as every other page this week,
wearing different clothes. "First reach wins" is what makes the hop counts
shortest in Exercise 1, the moves fewest in Exercise 2, and the seconds
smallest in Exercise 3. Here it makes the tier the shallowest. One property,
four uses.

**Where this breaks and what replaces it.** If a transformer genuinely
belonged to several tiers — if the report wanted GRANGE counted under BRINDLE
*and* under COLTON — this is the wrong algorithm entirely, because the
answer is no longer a walk over a graph but an enumeration of paths through
it, and there can be exponentially many of those. The tell is a spec that
says "for each route" rather than "for each transformer". Next week's search
is the one that enumerates routes.

</details>

## Acceptance checklist

- [ ] `python exercise-05-feeder-tier-load.py` prints four tier lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] Tier 2 totals 600, not 645.
- [ ] Tier 2's heaviest is FRAMPTON, and you have watched it change to
      HALLOW by editing a load.
- [ ] The tie-break lives in one `key` expression.
- [ ] `seen.add` sits immediately beside `queue.append`.
- [ ] Both dictionaries are read with `.get`.
- [ ] `tier_report(FEEDER, LOADS, "MARSTON")` raises `ValueError`.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 exercise 5: feeder tier load`.

## Stretch

- **Add the tier's width and its lightest transformer.** Two more fields, no
  change to the walk.

  ```python
  class WideTier(NamedTuple):
      """A tier row with the spread as well as the peak."""

      depth: int
      count: int
      total: int
      heaviest: str
      lightest: str
  ```

  ```text
  tier 0: 1 sites,    0 A   SUBSTATION .. SUBSTATION
  tier 1: 3 sites,  355 A   COLTON .. BRINDLE
  tier 2: 5 sites,  600 A   FRAMPTON .. GRANGE
  tier 3: 2 sites,   30 A   JUNIPER .. IRTON
  ```

  `lightest` uses `min` with `(loads.get(name, 0), name)` — the same key with
  the minus sign taken off. Note that IRTON wins tier 3's lightest at 0 amps,
  which is the unmetered rule showing up where you can see it.

- **Find the tier that would hurt most to lose.** Which single tier carries
  the largest share of the feeder's total load?

  ```python
  def worst_tier(report: list[Tier]) -> tuple[int, float]:
      """Return the tier drawing the largest share, and that share."""
      whole = sum(row.total for row in report) or 1
      worst = max(report, key=lambda row: row.total)
      return worst.depth, worst.total / whole
  ```

  ```text
  (2, 0.6091370558375635)
  ```

  Tier 2 is 61% of the feeder. That is the sort of number a planner acts on,
  and it came out of one walk and two lines of arithmetic.

- **Report the depth of every transformer instead of the tiers.** The other
  shape of the same walk.

  ```python
  def depth_of(feeder: dict[str, list[str]], loads: dict[str, int], head: str) -> dict[str, int]:
      """Return each reachable transformer's tier number."""
      return {
          name: row.depth
          for row in tier_report(feeder, loads, head)
          for name in ()  # a Tier row keeps totals, not names — see below
      }
  ```

  That does not work, and finding out why is the exercise: `Tier` threw the
  names away. Decide whether to widen `Tier` with a `names` field or to write
  a second, plainer walk, and be able to say which you picked and why. There
  is no single right answer — there is only the one you can defend.

When your report is right, move on to
[Challenge 1 — Trunk Splice](../challenges/challenge-01-trunk-splice.md).
