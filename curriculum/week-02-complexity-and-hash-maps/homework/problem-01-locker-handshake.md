# Homework Problem 1 — The Locker Handshake

> **Topic:** the two-way mapping — two hash maps that have to agree with each other, and the first problem this week where a `set` is one payload short of being able to answer at all
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Medium
> **Target time:** 90 minutes
> **Why this one:** the week's five exercises covered complement lookup, set membership, canonical keys and one-set-per-axis. This is the fourth sub-shape they did not cover, and it is the one that teaches the difference between *have I seen this* and *what did I see it with*. Solve it cold, with FRAME, recorder running.

## The Brief

Think of a cloakroom where every coat gets a ticket. One coat, one ticket. If
the same ticket number turns up on two different coats, somebody has made a
mistake — and so has the attendant who gave one coat two tickets.

Notice that this is **two** rules, not one, and they can break independently.

A courier depot assigns every arriving parcel to a locker. Over one shift the
depot logs the pairs `(route_code, locker_id)` in the order the parcels were
processed.

The depot's rule is a **one-to-one correspondence within a shift**: a route code
always goes to the same locker, and a locker only ever receives one route code.
Re-logging a pair the depot has already recorded is fine — a parcel gets
rescanned sometimes — and breaks nothing.

Scan the log in order and return the index of the **first entry that breaks the
rule**, together with which half of the correspondence broke:

- `"route"` — this route code was already logged against a *different* locker.
- `"locker"` — this locker was already logged against a *different* route code.

An entry can break both halves at once. When it does, report `"route"`.

Return `None` if the whole shift is consistent.

Here is the thing that makes this different from Exercise 2. A `set` of route
codes you have seen answers "have I seen `QRT` before?" — and that is the wrong
question. Seeing `QRT` before is *normal*; the depot rescans parcels all day.
The question is "have I seen `QRT` before **with a different locker**?" and that
needs the payload: which locker the route went to. Membership is not enough.
You need a map.

And you need two of them, one per direction, because the two halves of the rule
are about different things and can break separately.

## Starter

Create `problem-01-locker-handshake.py` in your practice repo and paste this in.
Fill in the `TODO`.

```python
"""problem-01-locker-handshake.py — the first broken handshake.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""


def first_handshake_break(
    assignments: list[tuple[str, int]],
) -> tuple[int, str] | None:
    """Return the first entry that breaks the one-to-one correspondence.

    Args:
        assignments: (route_code, locker_id) pairs in the order the parcels
            were processed.

    Returns:
        (index, side) for the first offending entry, where side is 'route'
        when the route was already logged against a different locker and
        'locker' when the locker was already logged against a different
        route. 'route' wins when both are true. None when the whole shift
        is consistent.
    """
    # TODO: two dicts, route -> locker and locker -> route. Per entry, test
    # BOTH halves in precedence order before recording anything, then record
    # the pair in both maps.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[tuple[str, int]], tuple[int, str] | None]] = [
        ([("QRT", 14), ("BLM", 9), ("QRT", 14)], None),
        ([("QRT", 14), ("QRT", 21)], (1, "route")),
        ([("QRT", 14), ("BLM", 14)], (1, "locker")),
        ([("QRT", 14), ("BLM", 21), ("QRT", 21)], (2, "route")),
        ([("QRT", 14), ("BLM", 9), ("ZED", 9), ("QRT", 30)], (2, "locker")),
        ([("QRT", 14), ("BLM", 9), ("QRT", 14), ("BLM", 9)], None),
        ([("QRT", 14)], None),
        ([], None),
    ]

    for log, expected in cases:
        found = first_handshake_break(log)
        assert found == expected, (log, found, expected)
        verdict = "consistent" if found is None else f"{found[1]} break at {found[0]}"
        pairs = " ".join(f"{route}->{locker}" for route, locker in log) or "(no parcels)"
        print(f"{verdict:<20}  {pairs}")

    print("All checks passed.")
```

Two words before you start.

**Bijection.** A one-to-one correspondence in both directions: every route has
exactly one locker and every locker has exactly one route. Two maps is the
straightforward way to enforce one, because each map guards one direction.

**Payload.** The value a map stores next to its key. Exercise 2 needed no
payload and used a `set`. This problem's whole difficulty is that it does need
one, and the sixth self-check is there to make that cost you if you forget.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/homework/problem-01-locker-handshake.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `first_handshake_break` returns `(index, side)` for the first offending
   entry, or `None` when the shift is consistent.
2. `side` is `"route"` or `"locker"`, and `"route"` wins when both halves break
   at the same entry.
3. Re-logging a pair already on record is legal and returns nothing.
4. The function returns at the **first** break and never reads later entries.
5. Absence is `None` — not `-1`, not `False`. Index `0` is a legal answer and
   `0` is falsy.
6. It runs in `O(n)` time and `O(n)` space, in one pass.
7. A pair that survives both checks is recorded in **both** maps.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(assignments) <= 400_000`.** A large depot processes roughly four
  hundred thousand parcels across a twenty-four hour shift. Checking each entry
  against every earlier entry is about `8 x 10^10` comparisons and will not
  finish, so the bound itself rejects the nested look-back. Name it out loud
  before you write anything.

- **Route codes are 2 to 5 uppercase ASCII letters, from an open catalogue of up
  to 50,000 codes.** Because they are **strings from an open catalogue**, you
  cannot index a flag array by them; the lookup has to be hashed. That is the
  "why a hash map at all" half of the argument, and it is the same reasoning as
  Exercise 2's badge range, with the key space being non-numeric rather than
  merely sparse.

- **`1 <= locker_id <= 30_000`.** The two key spaces are different types and
  different widths. That is the bound that pushes you toward **two** maps rather
  than one: a single map would need every key tagged with which side it came
  from, or a route code and a locker id could collide as keys. (Exercise 4's
  one-set-with-tagged-tuples trick is the alternative, and it works here too —
  name it.)

- **The log carries no ordering guarantee at all.** The same pair may recur at
  any distance, with anything in between. So you cannot compare adjacent entries
  and you cannot sort — sorting would renumber the entries, and the answer is an
  entry number.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-locker-handshake-solution.py
consistent            QRT->14 BLM->9 QRT->14
route break at 1      QRT->14 QRT->21
locker break at 1     QRT->14 BLM->14
route break at 2      QRT->14 BLM->21 QRT->21
locker break at 2     QRT->14 BLM->9 ZED->9 QRT->30
consistent            QRT->14 BLM->9 QRT->14 BLM->9
consistent            QRT->14
consistent            (no parcels)
All checks passed.
```

Two rows carry most of the teaching.

**Row four**, `QRT->14 BLM->21 QRT->21`, answers `route break at 2`. Both halves
break at index 2: `QRT` was on locker 14, and locker 21 belonged to `BLM`. Both
statements are true. The spec says `"route"` wins, so the order your two checks
are written in *is* the precedence rule — exactly as in Exercise 4.

**Row six**, `QRT->14 BLM->9 QRT->14 BLM->9`, answers `consistent`, and it is
the row that punishes reaching for a `set`. A set of seen route codes reports a
break at index 2, because `QRT` has indeed been seen. It has been seen *with the
same locker*, which is a rescan, not a contradiction. Only the payload can tell
those apart.

## Steps

1. Create the file, paste the starter, and run it. Cases two through five fail;
   the consistent ones pass by accident, because a stub that returns `None`
   answers them correctly. That is worth noticing: **a broken function can pass
   half your tests**, and it is why the failing cases matter more than the
   passing ones.
2. Write down what each map holds, in one sentence each. `locker_of` maps a
   route code to the locker it went to. `route_of` maps a locker to the route it
   received.
3. Write the loop with only the route check. Run. Case three still fails, which
   is correct — you have not written the locker half yet.
4. Add the locker check *below* the route check, then the two writes below both.
   Run. All eight should pass.
5. Break it on purpose three times, and read each failure: swap the two checks
   (row four answers `locker`); write to the maps before checking them (row one
   answers a break at index 2); record in only one map (row five answers
   `None`). Put each back before trying the next.
6. Write a generator: a consistent log of a few thousand pairs, then exactly one
   break injected at a known index. It is the fastest way to find an off-by-one
   in the early return.

## The Solution

```python
"""problem-01-locker-handshake-solution.py — the first broken handshake.

Two maps that have to agree with each other: route code to locker, and locker
to route code. A set cannot answer this problem at all, because the question is
never "have I seen this route" — it is "have I seen this route paired with a
*different* locker", and that needs the payload.

Time: O(n) — one pass, two lookups and two writes per entry, each O(1) average.
Space: O(n) — at most one entry per distinct route and one per distinct locker.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def first_handshake_break(
    assignments: list[tuple[str, int]],
) -> tuple[int, str] | None:
    """Return the first entry that breaks the one-to-one correspondence.

    Args:
        assignments: (route_code, locker_id) pairs in the order the parcels
            were processed.

    Returns:
        (index, side) for the first offending entry, where side is 'route'
        when the route was already logged against a different locker and
        'locker' when the locker was already logged against a different
        route. 'route' wins when both are true. None when the whole shift
        is consistent.
    """
    locker_of: dict[str, int] = {}
    route_of: dict[int, str] = {}

    for index, (route, locker) in enumerate(assignments):
        if route in locker_of and locker_of[route] != locker:
            return (index, "route")
        if locker in route_of and route_of[locker] != route:
            return (index, "locker")
        locker_of[route] = locker
        route_of[locker] = route

    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[tuple[str, int]], tuple[int, str] | None]] = [
        ([("QRT", 14), ("BLM", 9), ("QRT", 14)], None),
        ([("QRT", 14), ("QRT", 21)], (1, "route")),
        ([("QRT", 14), ("BLM", 14)], (1, "locker")),
        ([("QRT", 14), ("BLM", 21), ("QRT", 21)], (2, "route")),
        ([("QRT", 14), ("BLM", 9), ("ZED", 9), ("QRT", 30)], (2, "locker")),
        ([("QRT", 14), ("BLM", 9), ("QRT", 14), ("BLM", 9)], None),
        ([("QRT", 14)], None),
        ([], None),
    ]

    for log, expected in cases:
        found = first_handshake_break(log)
        assert found == expected, (log, found, expected)
        verdict = "consistent" if found is None else f"{found[1]} break at {found[0]}"
        pairs = " ".join(f"{route}->{locker}" for route, locker in log) or "(no parcels)"
        print(f"{verdict:<20}  {pairs}")

    print("All checks passed.")
```

**Two maps, because there are two rules.**

```python
locker_of: dict[str, int] = {}
route_of: dict[int, str] = {}
```

Each map guards one direction of the correspondence. `locker_of` catches "this
route has been somewhere else"; `route_of` catches "this locker has had
somebody else". Neither can catch the other's failure, which is why one map is
not enough and why the return value has to say *which*.

**The test is "seen with something different", not "seen".**

```python
if route in locker_of and locker_of[route] != locker:
```

Read it as English: *I have a record for this route, and the record disagrees
with what I am looking at now.* Two conditions, and dropping either one breaks a
different case. Drop `route in locker_of` and you get a `KeyError` on the first
occurrence of any route. Drop the inequality and every rescan becomes a
violation — which is exactly the bug a `set` forces on you, because a set has no
second half to compare.

That is the sentence to be able to say in one breath when asked why a set is
insufficient here: **a set can tell you a route has appeared before, and this
problem needs to know what it appeared with.**

**Both checks come before either write.** If you record the pair first, the
entry contradicts itself: `locker_of[route]` is now `locker`, so the inequality
is false and no break is ever reported. Same rule as every other page this week
— ask the structure before you tell it anything — and it is the third time the
ordering has been load-bearing.

**The checks are in precedence order, and that is all the precedence rule is.**
The route check returns first, so an entry that breaks both halves reports
`"route"` and never reaches the locker check. Row four is the test that pins it
down. Encoding a spec rule as statement order is cheap and completely invisible
to a reader, which is why it deserves the test rather than a comment.

**Both writes, or neither.**

```python
locker_of[route] = locker
route_of[locker] = route
```

A pair that survives both checks has to go into both maps. Record it in only one
and a later entry slips through the half you never populated — row five is the
case, and it fails by returning `None` on a log that really does contain a
break. Silent false negatives again, the same failure mode as Exercise 4's
missing insert.

**Returning at the first break is part of the contract, not an optimisation.**
Row five has two breaks in it — locker 9 at index 2 and route `QRT` at index 3 —
and the function must report index 2 and never read index 3. A solution that
sweeps the whole log collecting violations and then picks one out of the pile
gets this wrong whenever the pile is not in log order.

**Why `None` and not `-1` or `False`.** Index `0` is a legal answer, and `0` is
falsy, so a caller writing `if result:` would mishandle a break on the very
first entry. `-1` forces every caller to remember a magic number. `None` means
absence and nothing else. Third time this week; it is a house rule for a reason.

**The cost, said properly.** *Time `O(n)`*: one pass, and each entry does two
lookups and two writes, each `O(1)` average — with the caveat that hashing a
route code reads the string, which the 5-character cap makes a constant.
*Space `O(n)`*: at most one entry per distinct route in one map and one per
distinct locker in the other, so `O(r + l)` where both are at most `n`. *Best
case `O(1)`*: a break at index 1 returns after two entries. *Worst case*: a
consistent shift, which reads everything. *Tradeoff*: one set of tagged tuples —
Exercise 4's trick — replaces the two maps at the same complexity, but it stores
only membership, so it can tell you a route has appeared and not what it
appeared with; it would need the tag to carry the locker too, at which point it
is two maps wearing a costume. Sorting is not merely slower here but wrong: it
renumbers the entries, and the answer is an entry number. *Improvement*: none;
every entry must be read in the worst case, so `O(n)` is the floor.

## Download and run

Download
[problem-01-locker-handshake-solution.py](./problem-01-locker-handshake-solution.py)
and run it:

```bash
python problem-01-locker-handshake-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-01-locker-handshake.py`.

## Common bugs to catch

- **`KeyError` on the first entry.** You looked up before checking that the key
  exists:

  ```text
  Traceback (most recent call last):
      if locker_of[route] != locker:
         ~~~~~~~~~^^^^^^^
  KeyError: 'QRT'
  ```

  The first time a route appears there is nothing to disagree with. Guard with
  `route in locker_of and ...`, or use `locker_of.get(route, locker) != locker`
  — though the explicit version reads better and is what the shipped answer
  uses.

- **`AssertionError` on the rescan case, got `(2, 'route')`.** You treated
  "seen this route" as the failure condition:

  ```text
  Traceback (most recent call last):
      assert found == expected, (log, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([('QRT', 14), ('BLM', 9), ('QRT', 14)], (2, 'route'), None)
  ```

  Almost always this means you reached for a `set`. A repeat is a rescan; a
  repeat *with a different locker* is a contradiction. The test is on the
  payload.

- **`AssertionError` on row four, got `(2, 'locker')`.** Your two checks are in
  the wrong order. Correct arithmetic, wrong precedence — which is why the
  precedence rule belongs in your restatement of the problem, not in your
  debugging.

- **Every case answers `None`.** You wrote to the maps before you checked them,
  so every entry agrees with the record you just made of it. Move both writes
  below both checks.

- **`AssertionError` on row five, got `None`.** You updated only one map. The
  locker half was never populated, so locker 9's second appearance sailed
  through. Both maps, every time.

- **`TypeError: unhashable type: 'list'`.** You unpacked the entry wrongly and
  used the whole pair, or a list, as a key:

  ```text
  Traceback (most recent call last):
      locker_of[assignments] = locker
      ~~~~~~~~~^^^^^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  `for index, (route, locker) in enumerate(assignments)` unpacks the tuple in
  the loop header, which is the tidiest way to avoid this entirely.

- **Collecting every violation and then picking one.** Row five has two breaks,
  and the answer is the first one in log order. A sweep-then-choose solution
  reports whichever came out of your collection first, which is not the same
  thing and is not always wrong — which is what makes it dangerous.

- **`O(n^2)` instead of `O(n)`.** A nested look-back over `assignments[:index]`
  is the natural first instinct and the 400,000 bound exists to kill it. All
  eight self-checks pass with it in place, because eight entries cannot tell the
  difference.

## Under the hood

<details>
<summary>Under the hood — the four hash-map sub-shapes side by side, and when two maps beat one</summary>

**The four sub-shapes of this week, in one table.**

| Shape | Question it answers | Structure | Where you met it |
|---|---|---|---|
| Membership | *have I seen this?* | `set` | Exercise 2, Exercise 5 |
| Complement lookup | *have I seen the thing that completes this?* | `dict` value = position | Exercise 1 |
| Canonical key | *is this the same as that, by the problem's definition?* | `dict` key = computed form | Exercise 3 |
| Frequency | *how many times?* | `dict` value = count | Challenge 1 |
| Two-way mapping | *what did I see it **with**?* | two `dict`s, one per direction | this problem |

The pattern-matching skill this week is really about running down that list.
Every hash-map problem you will meet is one of those five, or two of them at
once — Challenge 1 is complement lookup and frequency in the same map.

**Why not one map keyed by both?** You could store one dict keyed by a tagged
tuple: `("route", "QRT") -> 14` and `("locker", 14) -> "QRT"`. That works, it is
one structure instead of two, and it is exactly Exercise 4's trick. It costs you
a slightly heavier key to hash and a reader who has to decode the tag. Two maps
cost you two names and read straight off the specification. Neither is wrong; be
able to say why you picked yours.

What *does not* work is one untagged map holding both directions. Route codes
are strings and locker ids are integers, so today they cannot collide — but that
is an accident of the types, not a property of the design. The day somebody
introduces numeric route codes, a route and a locker share a key and the two
rules silently merge. A design that is only correct because of a coincidence in
the input types is a design that will break during a refactor nobody thought was
risky.

**Bijections show up everywhere once you have the shape.** Pattern matching
(does this pattern of letters map one-to-one onto these words?), isomorphic
strings, schema mapping between two systems, bidirectional caches, symbol tables
with reverse lookup. All of them are two maps that must agree, and all of them
have the same three bugs: forgetting one direction, checking before existence,
and treating a legal repeat as a violation.

**The cost of the second map, honestly.** Two maps is roughly twice the memory
of one, and both are `O(n)`, so the complexity class does not change. What does
change is the constant, and on four hundred thousand entries that is real memory
— a few tens of megabytes. Worth knowing; not worth optimising away here, since
the alternative is the tagged single map, which stores exactly the same number
of facts in a slightly different shape.

**Why the string-key caveat matters.** Hashing `"QRT"` reads three characters,
so a dict operation here is `O(len(route))` rather than truly `O(1)`. With a
5-character cap that is a constant and folds in. Say the caveat anyway. "It's a
dict so it's O(1)" is the answer of somebody who has not thought about what gets
hashed, and this is a problem where the keys are strings and the interviewer
knows it.

</details>

## Acceptance checklist

- [ ] `python problem-01-locker-handshake.py` prints eight rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] Two maps, one per direction.
- [ ] Both checks come before either write.
- [ ] The route check comes before the locker check.
- [ ] A surviving pair is recorded in both maps.
- [ ] The function returns at the first break and reads nothing after it.
- [ ] You can answer, in one sentence, why a `set` is insufficient here.
- [ ] A FRAME write-up exists at
      `frame-writeups/c2-week-02/homework-01-locker-handshake.md`, with the cost
      section in the five-piece structure.
- [ ] Your write-up says how long the *Assess options* step took, and what made
      you certain the two-map shape was right.
- [ ] Recording is at least 15 minutes.
- [ ] Committed to Git with a message like `Add Week 2 homework 1: locker handshake`.

## Stretch

- **Report every break, not just the first.** The depot supervisor would rather
  fix a shift in one pass.

  ```python
  def all_handshake_breaks(
      assignments: list[tuple[str, int]],
  ) -> list[tuple[int, str]]:
      """Return every offending entry in log order. Offenders are not recorded."""
      locker_of: dict[str, int] = {}
      route_of: dict[int, str] = {}
      breaks: list[tuple[int, str]] = []
      for index, (route, locker) in enumerate(assignments):
          if route in locker_of and locker_of[route] != locker:
              breaks.append((index, "route"))
          elif locker in route_of and route_of[locker] != route:
              breaks.append((index, "locker"))
          else:
              locker_of[route] = locker
              route_of[locker] = route
      return breaks

  print(all_handshake_breaks([("QRT", 14), ("BLM", 9), ("ZED", 9), ("QRT", 30)]))
  print(all_handshake_breaks([("QRT", 14), ("BLM", 9), ("QRT", 14)]))
  ```

  ```text
  [(2, 'locker'), (3, 'route')]
  []
  ```

  Note the design decision hiding in the `else`: an offending entry is **not**
  recorded, so the maps keep describing the shift as the depot intended it
  rather than as it was mis-scanned. Recording offenders instead would suppress
  every later break involving the same route. Say which you chose and why —
  that is a product question, not a coding one.

- **Return the conflicting record, so the supervisor knows what to look at.**

  ```python
  def first_break_detail(
      assignments: list[tuple[str, int]],
  ) -> tuple[int, str, str, int] | None:
      """Return (index, side, route, the locker already on record) at the first break."""
      locker_of: dict[str, int] = {}
      route_of: dict[int, str] = {}
      for index, (route, locker) in enumerate(assignments):
          if route in locker_of and locker_of[route] != locker:
              return (index, "route", route, locker_of[route])
          if locker in route_of and route_of[locker] != route:
              return (index, "locker", route_of[locker], locker)
          locker_of[route] = locker
          route_of[locker] = route
      return None

  print(first_break_detail([("QRT", 14), ("QRT", 21)]))
  print(first_break_detail([("QRT", 14), ("BLM", 14)]))
  ```

  ```text
  (1, 'route', 'QRT', 14)
  (1, 'locker', 'QRT', 14)
  ```

  The map already held the answer; the original contract just threw it away.
  That is worth noticing generally — when a structure knows more than the
  contract returns, widening the contract is usually free.

- **Cross-check with a generator, which is how you should have tested it.**

  ```python
  import random

  def make_shift(size: int, break_at: int | None, seed: int) -> list[tuple[str, int]]:
      """A consistent shift of `size` pairs, with one route break injected."""
      rng = random.Random(seed)
      routes = [f"R{n:03d}" for n in range(size)]
      log = [(routes[n], n + 1) for n in range(size)]
      for _ in range(size // 2):
          log.append(rng.choice(log))
      rng.shuffle(log)
      if break_at is not None:
          route, locker = log[break_at]
          log[break_at] = (route, locker + 100_000)
      return log

  clean = make_shift(500, None, 20260227)
  print(first_handshake_break(clean))
  hurt = make_shift(500, 300, 20260227)
  print(first_handshake_break(hurt))
  ```

  ```text
  None
  (300, 'route')
  ```

  The generator builds a genuinely consistent shift, adds rescans, shuffles, and
  then injects exactly one break at a known index. If your early return is off
  by one, this catches it and hand-written cases do not — because you would have
  written the hand case with the same off-by-one in your head.

**Practice elsewhere.** The same pattern appears as [LeetCode 290 · Word Pattern](https://leetcode.com/problems/word-pattern/) if you want a judge to run against. The contract there returns a boolean, so it never forces you to carry the index, to name which side broke, or to tell a legal repeat apart from a contradiction — which are three of the four things this page is grading.

Next: [Homework Problem 2 — Time the Gap](./problem-02-time-the-gap.md).
