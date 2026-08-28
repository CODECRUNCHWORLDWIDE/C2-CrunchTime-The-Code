# Exercise 3 — Stage Twins

> **Topic:** the canonical key — inventing a label that is the same for two things exactly when the problem says they are the same
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** Exercises 1 and 2 handed you the key — an amount, a badge number. Here you have to invent one. That is the step where hash maps stop being a data structure you use and start being a technique you apply, and the wrong key on this page is wrong in a way that still returns plausible groups.

## The Brief

Two boxes of Lego are the same box if they hold the same bricks in the same
numbers. It does not matter which order you pull them out in. It *does* matter
how many of each there are: a box with two red bricks is not the same as a box
with one.

That is this whole problem, with amplifiers instead of bricks.

A festival stage manager is planning changeovers. Each act has sent in a
**load-out**: the list of backline gear they bring on stage, one entry per
physical item. An act that brings two guitar amps lists `"gtr"` twice.

Two acts are **stage twins** when their load-outs hold the same items in the
same numbers, in any order. Twins can follow each other on stage with no
changeover crew at all, which is what the manager is trying to schedule.

Now, how do you find them without comparing every act against every other act?

The move is a **canonical key**. A canonical key is a label you compute from a
thing, chosen so that two things get the *same* label exactly when the problem
calls them equal. Once you have one, "are these two acts twins?" becomes "are
these two labels equal?", and grouping by an equal label is what a hash map does
for free. You never compare two load-outs against each other at all.

For load-outs the label almost writes itself: **sort the items and freeze them
into a tuple.** `["gtr", "kit", "bass"]` and `["bass", "gtr", "kit"]` both
become `("bass", "gtr", "kit")`. Order is gone, counts survive, and a tuple can
be a dict key because it cannot change afterwards.

The contract, and there are four rules in it that are easy to skim:

Return the twin groups as **submission indices**, subject to:

1. A group is reported only if it has **at least two** acts in it. An act with a
   unique load-out is not a group of one; it is simply absent.
2. Groups are ordered by their **smallest index**, ascending.
3. Within a group, indices are ascending.
4. If no two acts are twins, return `[]`.

## Starter

Create `exercise-03-stage-twins.py` in your practice repo and paste this in.
Fill in the `TODO`.

```python
"""exercise-03-stage-twins.py — grouping acts by their load-out.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""

from collections import defaultdict


def stage_twins(loadouts: list[list[str]]) -> list[list[int]]:
    """Group the submission indices of acts with identical load-outs.

    Args:
        loadouts: One list of backline item codes per act, in submission
            order. An act that brings two of an item lists it twice.

    Returns:
        Groups of at least two indices, each group ascending, the groups
        themselves ordered by their smallest index. Acts with a unique
        load-out are absent.
    """
    # TODO: build a canonical key per act, bucket the INDEX under that key,
    # then drop every bucket with fewer than two acts in it.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[list[str]], list[list[int]]]] = [
        (
            [
                ["gtr", "kit", "bass"],
                ["bass", "gtr", "kit"],
                ["kit", "kit"],
                ["gtr", "gtr", "kit"],
                ["kit", "kit"],
            ],
            [[0, 1], [2, 4]],
        ),
        ([["gtr", "gtr"], ["gtr"]], []),
        ([["kit"], ["kit"], ["kit"]], [[0, 1, 2]]),
        ([[], []], [[0, 1]]),
        ([], []),
        ([["snare", "hat"], ["hat", "snare"], ["gtr"], ["hat", "hat"]], [[0, 1]]),
    ]

    for loadouts, expected in cases:
        found = stage_twins(loadouts)
        assert found == expected, (loadouts, found, expected)
        print(f"{len(loadouts)} acts  ->  {found}")

    print("All checks passed.")
```

Three words before you start.

**Canonical.** A canonical form is the one agreed-on spelling of a thing.
`("bass", "gtr", "kit")` is the canonical form of every ordering of those three
items. Canonicalising turns "are these equivalent?" into "are these identical?",
which is a much cheaper question.

**Hashable.** A dict key has to be hashable, which in practice means it must
not be able to change after you file it. `tuple` is hashable; `list` is not.
`sorted()` gives you a list, so it needs wrapping in `tuple(...)`.

**`defaultdict(list)`.** A dict that invents an empty list the first time you
touch a missing key, so `groups[key].append(i)` works without a "is this key
here yet?" branch. It is `from collections import defaultdict`.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/exercises/exercise-03-stage-twins.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `stage_twins` returns a list of lists of **submission indices**, not
   load-outs.
2. Equality is **multiset** equality: same items, same counts, order irrelevant.
   `["gtr", "gtr"]` and `["gtr"]` are not twins.
3. Groups with fewer than two acts are omitted entirely.
4. Groups appear in order of their smallest index; indices within a group
   ascend.
5. Two acts that bring nothing are twins. `[[], []]` returns `[[0, 1]]`.
6. It makes one pass over the acts. No act is ever compared against another act.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(loadouts) <= 20_000`.** A large festival across a weekend really
  does book that many acts. The bound rejects the pairwise comparison: checking
  every act against every other is two hundred million pairs *before* you look
  inside a single load-out, and each of those comparisons is itself work. One
  pass that computes a key per act does twenty thousand small sorts instead.

- **`0 <= len(loadouts[i]) <= 40`.** A stage plot is small. This bound is chosen
  so that **both** sensible key constructions pass comfortably — sorting a
  load-out is `O(k log k)` and counting it is `O(k)`, and at `k = 40` neither is
  the bottleneck. The bound exists so you can *discuss* the difference honestly
  instead of having one of them time out and make the choice for you. An
  interview answer that says "these two are equivalent at this size, and here is
  the size where they stop being" is worth more than one that picks the clever
  option and cannot say why.

- **Item codes are lowercase ASCII strings of 1 to 6 characters, from an open
  catalogue of at most 300 distinct codes.** This is the bound that matters
  most. The catalogue is open-ended and far bigger than the 26 letters, so the
  classic trick of counting into a fixed 26-slot array does not apply. Your
  canonical key has to work over an alphabet you do not know in advance, which
  is exactly why it is a hash key and not an array index.

- **The output ordering is specified, not arbitrary.** Two acts can be twins in
  either order, so without a stated rule the same input could produce different
  correct outputs and no test could pin it down. Specifying "by smallest index"
  makes the answer unique — and, as it turns out, makes it free. See the
  solution.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-stage-twins-solution.py
5 acts  ->  [[0, 1], [2, 4]]
2 acts  ->  []
3 acts  ->  [[0, 1, 2]]
2 acts  ->  [[0, 1]]
0 acts  ->  []
4 acts  ->  [[0, 1]]
All checks passed.
```

Read the second row. `[["gtr", "gtr"], ["gtr"]]` gives `[]`, and that row is the
whole reason this exercise exists. Two guitars is not one guitar. If your key is
`set(items)` or `frozenset(items)`, both acts collapse to `{"gtr"}` and you
report `[[0, 1]]` — a group of two acts that cannot follow each other, because
one of them has to strike an amp. A canonical form that loses counts is not
canonical for this problem.

## Steps

1. Create the file, paste the starter, and run it. The first case fails
   immediately.
2. Before writing the function, write the six keys out by hand for the first
   case. You should get `("bass","gtr","kit")`, `("bass","gtr","kit")`,
   `("kit","kit")`, `("gtr","gtr","kit")`, `("kit","kit")`. Notice that acts 0
   and 1 already match and act 3 already does not. The algorithm is now obvious;
   what remains is typing.
3. Write the loop that fills a `defaultdict(list)` with `key -> [indices]`.
   Print the dict. Read it against your hand-written keys.
4. Add the `len(indices) >= 2` filter and return.
5. Run. All six cases should pass — including the ordering, which you did not
   write any code for. Work out why before you read the solution; it is the most
   interesting thing on this page.
6. Break it on purpose: change the key to `frozenset(items)` and run again. Case
   two now fails. Change it back. That failure is the one you want to be able to
   describe from memory.

## The Solution

```python
"""exercise-03-stage-twins-solution.py — grouping acts by their load-out.

Every act gets one canonical key: its load-out sorted into a tuple. Two acts
are stage twins exactly when their keys are equal, so grouping the acts becomes
bucketing their indices under that key.

Time: O(n * k log k) — one sort per act, k items in the largest load-out.
Space: O(n * k) — the keys and the buckets.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from collections import defaultdict


def stage_twins(loadouts: list[list[str]]) -> list[list[int]]:
    """Group the submission indices of acts with identical load-outs.

    Args:
        loadouts: One list of backline item codes per act, in submission
            order. An act that brings two of an item lists it twice.

    Returns:
        Groups of at least two indices, each group ascending, the groups
        themselves ordered by their smallest index. Acts with a unique
        load-out are absent.
    """
    groups: defaultdict[tuple[str, ...], list[int]] = defaultdict(list)
    for index, items in enumerate(loadouts):
        groups[tuple(sorted(items))].append(index)
    return [indices for indices in groups.values() if len(indices) >= 2]


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[list[str]], list[list[int]]]] = [
        (
            [
                ["gtr", "kit", "bass"],
                ["bass", "gtr", "kit"],
                ["kit", "kit"],
                ["gtr", "gtr", "kit"],
                ["kit", "kit"],
            ],
            [[0, 1], [2, 4]],
        ),
        ([["gtr", "gtr"], ["gtr"]], []),
        ([["kit"], ["kit"], ["kit"]], [[0, 1, 2]]),
        ([[], []], [[0, 1]]),
        ([], []),
        ([["snare", "hat"], ["hat", "snare"], ["gtr"], ["hat", "hat"]], [[0, 1]]),
    ]

    for loadouts, expected in cases:
        found = stage_twins(loadouts)
        assert found == expected, (loadouts, found, expected)
        print(f"{len(loadouts)} acts  ->  {found}")

    print("All checks passed.")
```

**One key per act, and the problem dissolves.**

```python
groups[tuple(sorted(items))].append(index)
```

Everything hard about this problem is in that line, and none of it is code.
"Which acts are twins?" is a question about pairs, and pairs are quadratic.
"What is this act's canonical form?" is a question about one act, and there are
only `n` acts. Rephrasing a pairwise question as a per-item question is *the*
hash-map move, and it is the same move Exercise 1 made when it turned "which
line pairs with this one" into "have I seen the complement".

**`sorted` throws away order and keeps counts, which is exactly the equivalence
the problem defines.** Two load-outs are twins when they are equal as multisets.
Sorting is the standard way to canonicalise a multiset: two multisets are equal
if and only if their sorted sequences are identical. `["gtr", "gtr"]` sorts to
`["gtr", "gtr"]` and `["gtr"]` sorts to `["gtr"]`, and those are different, as
they should be.

**`tuple(...)` is not decoration.** `sorted()` hands back a list, and a list
cannot be a dict key, because Python cannot promise the key will still be the
same key tomorrow. A tuple cannot change, so its hash is stable, so it can be a
key. Try it without the `tuple` once and read the `TypeError` — it is in Common
bugs to catch below.

**The empty load-out needs no special case.** Two acts that bring nothing both
produce the key `()`, which is a perfectly ordinary hashable tuple, so they
group like anything else. Degenerate inputs that need no special handling are a
sign the design is right; if `[[], []]` had forced an `if`, the key would have
been the wrong shape.

**The required ordering comes free, and this is the part worth saying out loud
in an interview.** Look at what the loop does. A bucket is created the first
time any member of its group is seen — which is at that group's *smallest*
index. Python dictionaries have preserved insertion order since 3.7, and it is a
language guarantee, not a CPython accident. A list comprehension preserves
order. So `[indices for indices in groups.values() if len(indices) >= 2]` is
already ordered by smallest index, and every group's indices already ascend
because you appended them in increasing `index`. There is no sort anywhere in
this solution.

Say both halves of that out loud: *"insertion order gives me the required
ordering for free, so I do not pay an `O(g log g)` sort"* — and then the honest
half — *"in a language whose maps do not guarantee order I would have to sort by
`min(group)`, and the complexity would gain a log factor."* Knowing which of
your guarantees come from your algorithm and which come from your runtime is the
judgment signal this exercise is really grading.

**The size filter goes at the end, not during the loop.** You cannot know a
bucket is a singleton until every act has been read — the twin might be the last
submission. Filtering at the end costs one pass over the buckets, which is
`O(n)` in total across all of them.

**The cost, said properly.** *Time `O(n * k log k)`*, where `n` is the number of
acts and `k` the largest load-out: each act pays `O(k log k)` for its sort, and
hashing the resulting tuple costs `O(k)` because a hash has to read the whole
key. *Space `O(n * k)`*: every key is a copy of a load-out, and there are up to
`n` of them, plus one index per act in the buckets. *Best, average and worst are
the same*: there is no early exit, because a group's last member could be the
last act submitted. *Tradeoff*: see the stretch — keying on counts instead of on
a sort trades `O(k log k)` for `O(k + d log d)` on `d` distinct codes, which
wins only when items repeat heavily, and at `k <= 40` is invisible. *Improvement*:
none meaningful. Every item of every load-out has to be read, so `O(n * k)` is
the floor, and the sort's log factor is the only thing above it.

## Download and run

Download
[exercise-03-stage-twins-solution.py](./exercise-03-stage-twins-solution.py)
and run it:

```bash
python exercise-03-stage-twins-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-stage-twins.py`.

## Common bugs to catch

- **`TypeError: unhashable type: 'list'`.** You used `sorted(items)` directly as
  the key:

  ```text
  Traceback (most recent call last):
      groups[sorted(items)].append(index)
      ~~~~~~^^^^^^^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  `sorted()` returns a list. Wrap it: `tuple(sorted(items))`. The error message
  is telling you the exact truth — the thing you offered as a key has no
  usable hash, because it could change underneath the dict.

- **`AssertionError` on `([['gtr', 'gtr'], ['gtr']], ...)`, got `[[0, 1]]`.**
  Your key is `frozenset(items)`, or `set(items)` wrapped somehow. A set
  discards duplicates, so both acts collapse to the same key:

  ```text
  Traceback (most recent call last):
      assert found == expected, (loadouts, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([['gtr', 'gtr'], ['gtr']], [[0, 1]], [])
  ```

  `frozenset` is hashable and therefore *looks* like a valid key, which is what
  makes this the dangerous mistake on this page. Hashable is not the same as
  correct. The key must preserve everything the equivalence cares about, and
  this one cares about counts.

- **Singleton groups in the output.** You returned `list(groups.values())` and
  forgot the filter. The first case then answers
  `[[0, 1], [2, 4], [3]]`. An act with a unique load-out is not a group of one;
  it has nobody to change over with.

- **`AttributeError: 'NoneType' object has no attribute 'append'`.** You used a
  plain `dict` and wrote `groups.get(key).append(index)`:

  ```text
  Traceback (most recent call last):
      groups.get(key).append(index)
      ^^^^^^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'append'
  ```

  `.get` returns `None` for a missing key rather than raising. Either use
  `defaultdict(list)`, or `groups.setdefault(key, []).append(index)`, which does
  the same thing on a plain dict.

- **Returning the load-outs instead of the indices.** The return annotation says
  `list[list[int]]`. The manager schedules by submission number, not by gear
  list.

- **Returning the dict.** `return groups` gives a mapping, not a list of lists,
  and the assert fails with a message that looks nothing like the others.

- **Sorting the output by something.** Sorting groups by size, or by key, or
  "just to be safe", produces output the checks reject. The insertion order is
  already the required order. Adding a sort here is not a harmless extra; it is
  a change of answer.

- **Comparing acts to each other.** If your solution contains a loop inside a
  loop over `loadouts`, you wrote the `O(n^2 * k)` version. It passes all six
  self-checks, because six acts cannot tell the difference. Twenty thousand can.

## Under the hood

<details>
<summary>Under the hood — the two reasonable keys, and what hashing a tuple actually costs</summary>

**Key A — the sorted tuple.** What the solution uses.

```python
key = tuple(sorted(items))
```

Per act: `O(k log k)` for the sort, then `O(k)` to hash the resulting tuple.
Total `O(n * k log k)` time and `O(n * k)` space.

**Key B — the counted tuple.**

```python
from collections import Counter

key = tuple(sorted(Counter(items).items()))
```

Per act: `O(k)` to count, then `O(d log d)` to sort the `d` distinct codes,
where `d <= k`. When an act brings forty copies of one item, `d = 1` and Key B
is effectively `O(k)` while Key A is `O(k log k)`. When every item is distinct,
`d = k` and the two are the same, with Key B carrying a slightly heavier
constant because it builds a `Counter` first.

In an interview, present **Key A** first — it is one line and obviously correct
— then say: *"if load-outs were long and repetitive I would key on the counts
instead, which drops the per-act sort from k items to d distinct items."* That
sentence is the "I can do better, and I know exactly when it matters" move. Do
not claim Key B is faster in general; at `k <= 40` it is not measurably faster
at all, and claiming a win you cannot defend is worse than not mentioning one.

**Hashing a tuple is not free, and the page's cost sentence quietly assumed it.**
`hash(("bass", "gtr", "kit"))` combines the hashes of all three strings, and
each string's hash reads the whole string. So a dict operation on a `k`-item key
is `O(k)`, not `O(1)`. That is fine here — it is dominated by the sort — but it
matters as a habit. "Dict operations are O(1)" always means "O(1) in the number
of entries". The size of the key is a separate cost, and on a page where keys
are big it is the cost that dominates.

Python caches a string's hash inside the string object after the first
computation, so re-hashing the same item code in a later load-out is free. That
is why twenty thousand acts drawing on a 300-code catalogue do far less hashing
work than the arithmetic above suggests.

**Why not hash the load-out into a single number yourself?** You could add up
the hashes of the items, or multiply primes, and get a fixed-size key. Two
problems. First, addition and multiplication are commutative, so a hand-rolled
combination usually loses information the sort keeps, and two genuinely
different load-outs can collide *as keys that compare equal* — which is not a
hash collision the table can resolve, it is a wrong answer. Second, Python's
tuple hashing already does this properly, order-sensitively, with a
well-tested mixing function. Canonicalise, then let the language hash.

</details>

## Acceptance checklist

- [ ] `python exercise-03-stage-twins.py` prints six rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] Your key preserves counts, and you can say in one sentence why `frozenset`
      does not.
- [ ] No act is ever compared against another act.
- [ ] There is no `sort` anywhere except inside the key construction.
- [ ] Groups of one are filtered out at the end, not skipped during the loop.
- [ ] You can explain where the required output ordering came from.
- [ ] You can name the counted-tuple alternative and say when it would win.
- [ ] Committed to Git with a message like `Add Week 2 exercise 3: stage twins`.

## Stretch

- **Build the counted key and check it agrees.**

  ```python
  from collections import Counter, defaultdict

  def stage_twins_counted(loadouts: list[list[str]]) -> list[list[int]]:
      """Same contract, keyed on (item, count) pairs instead of on a sorted list."""
      groups: defaultdict[tuple[tuple[str, int], ...], list[int]] = defaultdict(list)
      for index, items in enumerate(loadouts):
          groups[tuple(sorted(Counter(items).items()))].append(index)
      return [indices for indices in groups.values() if len(indices) >= 2]

  sample = [["gtr", "kit", "bass"], ["bass", "gtr", "kit"], ["kit", "kit"],
            ["gtr", "gtr", "kit"], ["kit", "kit"]]
  print(stage_twins_counted(sample))
  print(stage_twins_counted([["gtr", "gtr"], ["gtr"]]))
  ```

  ```text
  [[0, 1], [2, 4]]
  []
  ```

  Same answers, different key. Now say which you would ship and why — and note
  that "they agree on these inputs" is evidence, not proof. The proof is that
  both keys are injective on multisets.

- **Return the group's shared load-out alongside its indices.**

  ```python
  from collections import defaultdict

  def stage_twin_plans(loadouts: list[list[str]]) -> list[tuple[list[int], list[str]]]:
      """Return (indices, shared load-out) for every twin group."""
      groups: defaultdict[tuple[str, ...], list[int]] = defaultdict(list)
      for index, items in enumerate(loadouts):
          groups[tuple(sorted(items))].append(index)
      return [(indices, list(key)) for key, indices in groups.items() if len(indices) >= 2]

  for indices, gear in stage_twin_plans(sample):
      print(indices, gear)
  ```

  ```text
  [0, 1] ['bass', 'gtr', 'kit']
  [2, 4] ['kit', 'kit']
  ```

  The canonical key turned out to be useful output, not just an internal label —
  it is the gear the whole group shares, which is exactly what the crew needs on
  a clipboard. Canonical forms often have that property, and it is worth
  noticing when they do.

- **Find the largest twin group.**

  ```python
  def biggest_twin_group(loadouts: list[list[str]]) -> list[int]:
      """Return the largest twin group, ties broken toward the smaller first index."""
      groups = stage_twins(loadouts)
      if not groups:
          return []
      return max(groups, key=lambda indices: (len(indices), -indices[0]))

  print(biggest_twin_group(sample))
  print(biggest_twin_group([["kit"], ["kit"], ["kit"], ["gtr"], ["gtr"]]))
  ```

  ```text
  [0, 1]
  [0, 1, 2]
  ```

  `max` with a tuple key again, exactly as in Week 1 — negate the field you want
  to break ties *downwards*. The scheduling value is real: the biggest twin
  group is the longest run of acts the manager can put back to back with no crew
  at all.

**Practice elsewhere.** The same pattern appears as [LeetCode 49 · Group Anagrams](https://leetcode.com/problems/group-anagrams/) if you want a judge to run against. The contract there returns the strings in any order and keeps singleton groups, so it never forces the index mapping, the size filter, or a deterministic ordering — which is where three of this page's four ordering rules live.

Next: [Exercise 4 — The On-Call Grid](./exercise-04-on-call-grid.md).
