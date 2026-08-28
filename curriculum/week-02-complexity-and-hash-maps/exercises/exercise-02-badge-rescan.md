# Exercise 2 — The Repeated Badge

> **Topic:** set membership — the hash map with the payload taken away, and the first problem where the *best* case is worth saying out loud
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Easy
> **Target time:** 40 minutes
> **Why this one:** Exercise 1's map carried a payload — where each amount was seen. This one carries nothing but the fact that something *was* seen, which is what a `set` is. It is the shortest solution in the week and the one where all the marks are in the discussion around it: why `None` and not `-1`, why a set and not a flag array, and why the honest best case here is `O(1)`.

## The Brief

A data centre has one front door with a badge reader on it. Every time somebody
taps a badge, the reader writes down the badge number. By the end of the day
you have a long list of numbers, in the order the taps happened.

Security cares about one thing: **tailgating**. If the same badge is tapped
twice in a day, it usually means somebody handed their badge to a colleague in
the car park so that two people could get in on one card. The camera footage
would show it — but the footage is hours long, and somebody has to know where
to start watching.

So the question is not *"did a badge repeat?"* and it is not *"which badge
repeated?"* It is **"at which tap should the guard start the footage?"**

Return the **index of the first tap whose badge had already been tapped
earlier that day**. If every tap in the log is a distinct badge, return `None`.

Notice what that rules out. You are not returning the badge number, not
returning a count, and not returning true-or-false. You are returning a
position in the log.

The tool is a **set**. A set is a hash map that only remembers the labels on
the pigeonholes and never puts anything inside them — it answers exactly one
question, *have I seen this before*, and it answers it in the same tiny amount
of time however many things it holds. That is the entire problem: walk the log
once, and at each tap ask the set that one question.

## Starter

Create `exercise-02-badge-rescan.py` in your practice repo and paste this in.
Fill in the `TODO`.

```python
"""exercise-02-badge-rescan.py — the first repeated badge tap.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""


def first_repeated_scan(badge_ids: list[int]) -> int | None:
    """Return the index of the first tap whose badge was already tapped.

    Args:
        badge_ids: Badge numbers in the order they were tapped.

    Returns:
        The smallest index i such that badge_ids[i] appears in badge_ids[:i],
        or None if every badge in the log is distinct.
    """
    # TODO: one pass with a set. Ask before you add.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int | None]] = [
        ([4820, 1173, 4820, 9002], 2),
        ([4820, 1173, 9002], None),
        ([], None),
        ([7715], None),
        ([3301, 3301, 3301], 1),
        ([5, 9, 12, 9, 5], 3),
    ]

    for log, expected in cases:
        found = first_repeated_scan(log)
        assert found == expected, (log, found, expected)
        verdict = "clean" if found is None else f"review from tap {found}"
        counted = f"{len(log)} tap" + ("" if len(log) == 1 else "s")
        print(f"{counted:<7} ->  {verdict:<20}  {log}")

    print("All checks passed.")
```

Two words before you start.

**Set.** `seen = set()` makes an empty one. `seen.add(4820)` puts a badge in it.
`4820 in seen` asks whether it is there. There is no value to fetch, because a
set stores no values — only membership. `{}` makes an empty *dict*, not an empty
set, which is a genuine Python trap worth knowing once.

**Early return.** The moment you find the answer, `return` it. Do not keep
scanning to the end "to be safe". On this problem, returning early is not a
micro-optimisation — it is the difference between the best case being `O(1)` and
being `O(n)`, and this page grades you on being able to say which.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/exercises/exercise-02-badge-rescan.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `first_repeated_scan` returns an **index into the log**, not a badge number
   and not a count.
2. It returns the index of the **first** repeat, not the last. On
   `[3301, 3301, 3301]` the answer is `1`.
3. It returns `None` — not `-1`, not `False`, not `0` — when every badge is
   distinct.
4. An empty log and a single-tap log both return `None`.
5. It runs in `O(n)` time and `O(n)` space, with a single pass.
6. It returns as soon as it has the answer, so the best case really is `O(1)`.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(badge_ids) <= 500_000`.** A large campus taps roughly half a
  million badges in a day. The bound is chosen to reject the obvious first
  instinct — for each tap, look back over every earlier tap — which is about
  `1.25 x 10^11` comparisons. That is the number to name out loud when somebody
  asks why you did not just use a nested loop.

- **`1 <= badge_ids[i] <= 10_000_000`.** Badge numbers are seven digits and are
  issued sparsely: a site might have four hundred staff holding numbers
  scattered anywhere in that range. This is the bound that rules out the other
  obvious answer, a list of ten million true/false flags indexed by badge
  number. That list costs the same ten million slots on a day when four people
  came in. A set costs one entry per badge *actually tapped*. Space proportional
  to the data, not to the range — that is the space half of your cost sentence,
  and it is the reason a hash structure exists at all.

- **The log is in tap order and carries no other guarantee.** It is not sorted
  and cannot be sorted, because sorting renumbers the taps and the answer *is* a
  tap number. This is the constraint that makes the sorting alternative not
  merely slower but incapable of answering the question.

- **The answer must be distinguishable from "no answer".** Index `0` can never
  itself be the answer — the first tap of a badge is innocent — but `-1` forces
  every caller to remember a magic number, and `False` collides with `0` under
  `if result:`. `None` is the one value that means absence and cannot be
  confused with a position.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-badge-rescan-solution.py
4 taps  ->  review from tap 2     [4820, 1173, 4820, 9002]
3 taps  ->  clean                 [4820, 1173, 9002]
0 taps  ->  clean                 []
1 tap   ->  clean                 [7715]
3 taps  ->  review from tap 1     [3301, 3301, 3301]
5 taps  ->  review from tap 3     [5, 9, 12, 9, 5]
All checks passed.
```

Look at the last row. Two badges repeat in `[5, 9, 12, 9, 5]`: badge 9 first at
index 1 and again at index 3, and badge 5 first at index 0 and again at index 4.
The earliest *repeat* is at index 3. That row punishes two wrong approaches at
once — sorting the log, which destroys the positions, and "find the badge that
appears most often", which would pick 5 or 9 arbitrarily and say nothing about
when.

## Steps

1. Create the file, paste the starter, and run it. The first case fails
   immediately, which is the correct starting point.
2. Write the loop with `seen.add(badge)` **only**, and print the set at the end.
   Convince yourself it contains six badges for the last case and that the order
   you see is not the order you added them in. Sets do not keep order, and it
   does not matter here, because you never iterate one.
3. Now add the membership test **above** the add, and return the index.
4. Run it. All six cases should pass.
5. Break it on purpose: move `seen.add(badge)` above the `if`. Run again and
   read the failure. Every non-empty log now answers `0`, because the very first
   tap finds itself. Put it back. Deliberately introducing a bug and reading its
   signature is worth more than avoiding it.
6. Say the cost sentence out loud, including the best case: *"one pass, each set
   operation O(1) average, so O(n) time worst case and O(n) space; but it
   returns on the first repeat, so if the second tap repeats the first it is
   O(1) and touches two elements."*

## The Solution

```python
"""exercise-02-badge-rescan-solution.py — the first repeated badge tap.

One pass over the tap log, carrying a set of the badges seen so far. At every
tap we ask one question: have I seen this badge already? The first time the
answer is yes, that tap's index is the answer.

Time: O(n) worst case, O(1) best case when the second tap repeats the first.
Space: O(n) — one entry per distinct badge, never O(10_000_000).

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def first_repeated_scan(badge_ids: list[int]) -> int | None:
    """Return the index of the first tap whose badge was already tapped.

    Args:
        badge_ids: Badge numbers in the order they were tapped.

    Returns:
        The smallest index i such that badge_ids[i] appears in badge_ids[:i],
        or None if every badge in the log is distinct.
    """
    seen: set[int] = set()
    for index, badge in enumerate(badge_ids):
        if badge in seen:
            return index
        seen.add(badge)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int | None]] = [
        ([4820, 1173, 4820, 9002], 2),
        ([4820, 1173, 9002], None),
        ([], None),
        ([7715], None),
        ([3301, 3301, 3301], 1),
        ([5, 9, 12, 9, 5], 3),
    ]

    for log, expected in cases:
        found = first_repeated_scan(log)
        assert found == expected, (log, found, expected)
        verdict = "clean" if found is None else f"review from tap {found}"
        counted = f"{len(log)} tap" + ("" if len(log) == 1 else "s")
        print(f"{counted:<7} ->  {verdict:<20}  {log}")

    print("All checks passed.")
```

**The set is the whole algorithm.**

```python
seen: set[int] = set()
for index, badge in enumerate(badge_ids):
    if badge in seen:
        return index
    seen.add(badge)
return None
```

Five lines. The interesting part of this exercise is not writing them; it is
being able to defend every choice inside them.

**A set, not a dict, because there is no payload.** Exercise 1's map needed to
remember *where* each amount was seen, because it had to return that position.
Here the position you return is the one you are standing on, so nothing needs
remembering except the bare fact of having seen a badge. A `set` is exactly a
dict with the values thrown away; using one says "I only need membership" in the
type itself, and it saves the memory the values would have taken.

**Check first, add second.** If you add before you check, the first tap of every
log finds itself in the set and the function returns `0` on any non-empty input.
The rule generalises: when a structure is both the question and the record, ask
before you record.

**`return index`, immediately.** The loop stops at the first repeat, so the
index it returns is the smallest index that qualifies. Just as in Exercise 1, a
requirement — "the *first* repeat" — dissolved into the shape of the loop
instead of turning into a comparison. On `[3301, 3301, 3301]` this is the
difference between the answer `1` and the answer `2`.

**Why `None` and not `-1`, and why the difference is real.** Return `-1` and
every caller has to know that `-1` is special. Return `False` and a caller
writing `if result:` mishandles a real index of `0`. Neither of those is a
hypothetical: index `0` really is falsy, and in this codebase there will be
other functions that legitimately return it. `None` cannot be mistaken for a
position, and testing for it requires `is None`, which nobody writes by mistake.

**The best case is `O(1)` and you must say so.** On a log whose second tap
repeats the first, the function does one membership test, one add, one more
membership test, and returns — two elements touched, regardless of whether the
log has ten entries or five hundred thousand. That is a genuine best case, not a
technicality, because it is the case security most wants to hear about. Worst
case is `O(n)`, when the log is clean and the loop has to reach the end.

**The alternative here is not slower — it is wrong.** Sorting the log and
scanning for adjacent equal values is `O(n log n)` time and, sorted in place,
`O(1)` extra space. It genuinely beats this solution on memory. It also
*renumbers the taps*, and the answer to this question is a tap number, so the
sorted version cannot answer it at all. That is a much stronger sentence than
"mine is faster", and this exercise exists partly so you have one to say.

**The one-liner answers a different question.**
`len(badge_ids) != len(set(badge_ids))` is short, correct, and returns a
boolean. It throws away the position, and it always builds the whole set even
when the repeat is at index 1. It is the right answer to the yes-or-no version
of this problem and the wrong answer to ours. Knowing which question a neat
one-liner answers is a skill; reaching for it because it is neat is not.

**The cost, said properly.** *Time*: `O(n)` worst case, `O(1)` best case, one
pass with `O(1)`-average set operations. *Space*: `O(n)` auxiliary — at most one
entry per distinct badge, which is at most `n`. Pointedly **not** `O(10^7)`,
which is what the flag-array design would cost regardless of input size.
*Tradeoff*: sort-then-scan is cheaper in memory and cannot answer the question;
the flag array is `O(1)` per check and wastes ten million slots.
*Improvement*: none. The answer may be the very last tap, so every tap may have
to be read, and `O(n)` is the floor.

## Download and run

Download
[exercise-02-badge-rescan-solution.py](./exercise-02-badge-rescan-solution.py)
and run it:

```bash
python exercise-02-badge-rescan-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-badge-rescan.py`.

## Common bugs to catch

- **Every non-empty log answers `0`.** You added before you checked:

  ```text
  Traceback (most recent call last):
      assert found == expected, (log, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([4820, 1173, 4820, 9002], 0, 2)
  ```

  There is no exception from the set itself, because adding and then finding is
  perfectly legal — it is just not the question. Swap the two lines.

- **`AssertionError` on `([3301, 3301, 3301], ...)`, got `2`.** You collected
  every repeat and returned the last one, or you kept scanning after finding the
  answer. Return the moment you find it. As a bonus, that is what makes the best
  case `O(1)`.

- **`AttributeError: 'dict' object has no attribute 'add'`.** You wrote
  `seen = {}` thinking it made an empty set:

  ```text
  Traceback (most recent call last):
      seen.add(badge)
      ^^^^^^^^
  AttributeError: 'dict' object has no attribute 'add'
  ```

  `{}` is an empty dict. `set()` is an empty set. `{1, 2}` is a set with two
  things in it, so the braces only mean "set" once there is something between
  them. This is the one piece of Python syntax that bites everybody exactly
  once.

- **`TypeError: unhashable type: 'list'`.** You added the whole log instead of
  one badge:

  ```text
  Traceback (most recent call last):
      seen.add(badge_ids)
      ^^^^^^^^^^^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  A set holds hashable things, and a list is not hashable because it can change
  after you put it in.

- **Returning the badge, not the index.** `[4820, 1173, 4820, 9002]` answers
  `2`, not `4820`. Read the return annotation, and re-read the brief: the guard
  wants to know where to start the footage.

- **Assuming the repeat is adjacent.** A solution built on
  `badge_ids[i] == badge_ids[i + 1]` gets `[3301, 3301, 3301]` right and
  `[5, 9, 12, 9, 5]` wrong. Adjacent-comparison solutions are sorted-input
  solutions in disguise, and this input is not sorted.

- **`return len(badge_ids) != len(set(badge_ids))`.** Correct answer to a
  different question. It gives a boolean, loses the position, and always builds
  the whole set. Keep it in your notes as the answer to give when somebody
  changes the contract to a yes-or-no.

## Under the hood

<details>
<summary>Under the hood — a set is a dict with the values removed, and what that saves</summary>

**Same table, no values.** CPython implements `set` with the same open-address
hash table as `dict`, minus the value slot. An entry in a set stores the cached
hash and the key; an entry in a dict stores the hash, the key and the value.
Everything you know about dict lookups — hashing the key, probing on collision,
resizing at about two-thirds full, `O(1)` average and `O(n)` adversarial worst
case — is true of sets word for word.

The saving is real but modest: you are dropping one pointer per entry, not
changing the complexity. The better argument for `set` is that it *says* what
you are doing. A reader who sees `seen: set[int]` knows immediately that no
payload is involved. A reader who sees `seen: dict[int, bool]` has to check
whether the `bool` ever gets read.

**Why not a list of flags?** For a badge range of 1 to 10,000,000 the flag array
is genuinely faster per check — no hashing at all, just an index — and it is a
completely reasonable design when the key range is small and dense. Here the
range is huge and the data is sparse, so the array wastes 10,000,000 slots to
record 400 facts. The rule to carry away: **direct addressing beats hashing when
the key range is small and dense; hashing beats direct addressing when the key
range is large and sparse.** Interviewers ask this. Having the sentence ready is
worth more than having the code ready.

**What "distinct" costs you.** The set's size is the number of *distinct*
badges, `d`, not the number of taps, `n`. So the honest space bound is `O(d)`,
and `d <= n`. Saying `O(n)` is correct because it is an upper bound, and saying
`O(d)` is more informative. On a log where forty people tapped ten thousand
times, that difference is two hundred and fifty times the memory. Say `O(n)`
first, then refine to `O(d)` — the refinement is the part that sounds like
someone who has thought about it.

**Sets are unordered, and that is not a bug.** Iterating a set gives you its
elements in whatever order the hash table lays them out, which depends on the
values, on the insertion history, and on the table's size. Nothing in this
solution iterates the set, so nothing here depends on the order — but
Exercise 5 *does* iterate a set, and its tie-break rule exists precisely because
that order cannot be relied on.

</details>

## Acceptance checklist

- [ ] `python exercise-02-badge-rescan.py` prints six rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] The membership test comes **before** the add.
- [ ] The function returns the moment it finds the answer.
- [ ] The absent answer is `None`, and you can say in one sentence why not `-1`.
- [ ] You used `set`, not `dict`, and can say why the payload is not needed.
- [ ] You can name the rejected alternative and say why it is *wrong*, not just
      slower.
- [ ] You stated the best case out loud, with the input that triggers it.
- [ ] Committed to Git with a message like `Add Week 2 exercise 2: badge rescan`.

## Stretch

- **Report every tailgating incident, not just the first.**

  ```python
  def all_repeated_scans(badge_ids: list[int]) -> list[tuple[int, int]]:
      """Return (first_index, repeat_index) for every repeated tap, in tap order."""
      first_at: dict[int, int] = {}
      incidents: list[tuple[int, int]] = []
      for index, badge in enumerate(badge_ids):
          if badge in first_at:
              incidents.append((first_at[badge], index))
          else:
              first_at[badge] = index
      return incidents

  print(all_repeated_scans([5, 9, 12, 9, 5]))
  print(all_repeated_scans([3301, 3301, 3301]))
  ```

  ```text
  [(1, 3), (0, 4)]
  [(0, 1), (0, 2)]
  ```

  The set became a dict again the moment the answer needed a payload — the guard
  now wants to see both taps, so you have to remember where the first one was.
  That is the whole distinction between this exercise and Exercise 1, in one
  edit. Note also that the early return had to go, and with it the `O(1)` best
  case: a full report needs the full log.

- **Answer the yes-or-no version, and time both.**

  ```python
  def has_repeat_scan(badge_ids: list[int]) -> bool:
      """Return True if any badge was tapped more than once."""
      return len(badge_ids) != len(set(badge_ids))

  print(has_repeat_scan([5, 9, 12, 9, 5]))
  print(has_repeat_scan([4820, 1173, 9002]))
  ```

  ```text
  True
  False
  ```

  Both are `O(n)`, and on a log whose repeat sits at index 1 the loop version
  finishes after two taps while this one builds a set of all five hundred
  thousand. Same complexity class, wildly different work. Being able to say
  "same big-O, different constant, and here is when the constant matters" is a
  more useful thing to be able to say than the big-O alone.

- **Find the busiest badge instead.**

  ```python
  from collections import Counter

  def busiest_badge(badge_ids: list[int]) -> int | None:
      """Return the badge tapped most often, ties broken toward the lower number."""
      if not badge_ids:
          return None
      tally = Counter(badge_ids)
      return min(tally, key=lambda badge: (-tally[badge], badge))

  print(busiest_badge([5, 9, 12, 9, 5, 9]))
  print(busiest_badge([]))
  ```

  ```text
  9
  None
  ```

  Third structure, third question. Set answers *have I seen it*, dict answers
  *where did I see it*, `Counter` answers *how many times*. Exercise 3 is built
  on the third one.

**Practice elsewhere.** The same pattern appears as [LeetCode 217 · Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) if you want a judge to run against. The contract there returns a boolean, so it never forces you to keep the index or to tell "no repeat" apart from a falsy zero — which is where most of this page's marks live.

Next: [Exercise 3 — Stage Twins](./exercise-03-stage-twins.md).
