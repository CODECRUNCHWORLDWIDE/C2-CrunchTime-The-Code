# Exercise 3 — The Rota Window

> **Topic:** a fixed-size window whose state is a frequency table, compared against a target table
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** back to a fixed-width window, but the thing being carried across the slide is no longer a single number — it is a whole table of counts. Hold a target mix, slide a window of exactly that size, ask whether the two match. That shape turns up constantly, and it is the direct bridge to this week's first challenge.

## The Brief

A hospital ward publishes its roster as a plain list of role codes, one per
shift, in the order the shifts happen. `"RN"` is a registered nurse, `"LPN"` a
licensed practical nurse, `"NA"` a nursing assistant, and there are a handful of
others.

Regulation says a **staffing block** — any run of consecutive shifts as long as
the requirement — must be covered by exactly the mix the requirement names.
Order inside the block does not matter at all. A block staffed
`["NA", "RN"]` satisfies a requirement of `["RN", "NA"]`, because it has the
same one nurse and the same one assistant, just in the other order.

The word for "a collection where the counts matter but the order does not" is a
**multiset**. A set would tell you *which* roles are present; a multiset tells
you *how many of each*. That difference is the entire problem. If the
requirement is two nurses and one assistant, a block with one nurse and two
assistants has the same roles in it and is not compliant.

**Your job.** Return **how many** staffing blocks in the roster are compliant.

Blocks overlap, and they all count. Shifts 0–1 and shifts 1–2 are two different
blocks, they share a shift, and each is checked on its own. So a roster of six
shifts with a two-shift requirement has five blocks in it, not three.

The technique is the fixed window again, but with a table instead of a running
total. Build one table for the requirement, once, before the loop. Build a
second for the first block. Then, at each slide, one shift joins the window and
one leaves — so exactly two counts change, and everything else in the table is
already right.

There is one detail that will cost you the whole exercise if you miss it. When
a count drops to zero, **delete the key**. In Python, a table that says
`{"RN": 1, "NA": 0}` is not equal to a table that says `{"RN": 1}`, even
though a human reading them would say the ward has one nurse and no assistants
either way. Python compares the keys as well as the values. Leave the zeros in
and your window will never match anything.

**The contract.** Return the count as an integer. If `required` is empty,
return `0` — an empty requirement is a caller mistake, not a roster in which
every block is trivially compliant. If the roster is shorter than the
requirement, return `0` as well.

## Starter

Create `exercise-03-rota-window.py` and paste this in. Fill in every `TODO`.

```python
"""exercise-03-rota-window.py — counting compliant staffing blocks.

Slide a fixed-size window across a roster and count how many blocks match the
required role mix exactly, ignoring order.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import Counter


def count_compliant_blocks(roster: list[str], required: list[str]) -> int:
    """Return how many staffing blocks in the roster are compliant.

    Args:
        roster: Role codes, one per shift, in chronological order.
        required: The role mix a block must be covered by. Repeats are real
            requirements: two "RN" entries mean two registered nurses.

    Returns:
        The number of contiguous blocks of len(required) shifts whose role
        counts equal the requirement's. Overlapping blocks count separately.
        Zero when the requirement is empty or longer than the roster.
    """
    # TODO: guard both zero cases before touching a window.
    # TODO: build `wanted` from `required`, and the first window from the
    #       first `size` shifts. Seed the count from whether they already match.
    # TODO: slide. Each step: add the arriving shift, drop the leaving one,
    #       DELETE the leaving key if its count reaches zero, then compare.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]),
        (["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]),
        (["RN", "RN", "RN", "LPN"], ["RN", "RN"]),
        (["RN", "RN"], ["LPN"]),
        (["RN"], ["RN", "NA"]),
        (["RN"], []),
        ([], ["RN"]),
    ]
    for roster, required in cases:
        found = count_compliant_blocks(roster, required)
        print(f"required {str(required):<22} roster {str(roster):<44} -> {found}")
    print()

    assert count_compliant_blocks(["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]) == 3
    assert count_compliant_blocks(["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]) == 2
    assert count_compliant_blocks(["RN", "RN", "RN", "LPN"], ["RN", "RN"]) == 2
    assert count_compliant_blocks(["RN", "RN"], ["LPN"]) == 0
    assert count_compliant_blocks(["RN"], ["RN", "NA"]) == 0
    assert count_compliant_blocks(["RN"], []) == 0
    assert count_compliant_blocks([], ["RN"]) == 0

    # The incremental table must agree with rebuilding one per block.
    for roster, required in cases:
        size = len(required)
        if size == 0 or size > len(roster):
            continue
        slow = sum(
            Counter(roster[i : i + size]) == Counter(required)
            for i in range(len(roster) - size + 1)
        )
        assert count_compliant_blocks(roster, required) == slow

    print("All checks passed.")
```

Two things you need before you start.

**`Counter`.** A dictionary that counts. `Counter(["RN", "NA", "RN"])` gives
you `Counter({'RN': 2, 'NA': 1})`. It has one convenience that matters here:
`window[shift] += 1` works even when `shift` has never been seen, because a
missing key reads as `0` instead of raising. It also has one trap, and it is
the one this page is about — reading a missing key *creates nothing*, but
writing a zero *does* leave a key behind.

**Multiset equality.** `Counter(a) == Counter(b)` is `True` when both tables
have the same keys with the same values. It is plain dictionary equality
underneath, which is why a key sitting at zero breaks it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/exercises/exercise-03-rota-window.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `count_compliant_blocks(roster, required)` returns an **integer count**, not
   a boolean and not a list of positions.
2. Overlapping blocks count separately.
   `count_compliant_blocks(["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"])`
   is `3`.
3. Duplicates in `required` are real requirements. Two `"RN"` entries mean two
   nurses, and a block with one nurse and two assistants is not compliant.
4. An empty `required` returns `0`. A `required` longer than the roster returns
   `0`.
5. The window table is updated incrementally. Nothing inside the loop may build
   a `Counter` from a slice.
6. Every count that reaches zero has its key deleted.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(roster) <= 200_000`.** A decade of three-shift days is about
  11,000 entries, so this covers any real ward with a wide margin. The size is
  chosen to reject the naive check: sorting each block and comparing the sorted
  lists costs `O(m log m)` per block, so with a requirement near the roster's
  own length you are at roughly `2 x 10^5 x 2 x 10^5 x log(2 x 10^5)`
  operations. That is not a slow program; it is a program that does not
  terminate on a working day.

- **`0 <= len(required)`, and a requirement longer than the roster is legal
  input.** It returns `0`. Saying so in the contract costs one sentence and
  saves a guard argument later — and note that Python will *not* stop you:
  `roster[:5]` on a three-element roster quietly gives you three elements
  rather than raising, so an unguarded solution ends up comparing a three-shift
  window against a five-shift requirement and gets a plausible wrong answer.

- **Role codes come from a fixed vocabulary of at most 12 codes.** A ward has a
  finite set of job titles. This bound is load-bearing and it is the sentence
  to say out loud: it makes a whole-table comparison at most 12 key probes, so
  the comparison is a constant rather than something that grows, and that is
  what lets the whole scan be linear. Say what would break without it: with an
  unbounded vocabulary each comparison costs `O(vocabulary)` and the algorithm
  degrades. That is exactly the situation Challenge 1 puts you in, and it is
  why the matched-count trick exists.

- **Update the table, do not rebuild it.** Two key changes per slide. Building
  a fresh `Counter` from `roster[i:i + size]` is `O(m)` per step, which is the
  rescan from Exercise 1 wearing different clothes.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-rota-window.py
required ['RN', 'NA']           roster ['RN', 'NA', 'RN', 'LPN', 'RN', 'NA']        -> 3
required ['RN', 'RN', 'NA']     roster ['RN', 'NA', 'NA', 'RN', 'RN', 'NA']         -> 2
required ['RN', 'RN']           roster ['RN', 'RN', 'RN', 'LPN']                    -> 2
required ['LPN']                roster ['RN', 'RN']                                 -> 0
required ['RN', 'NA']           roster ['RN']                                       -> 0
required []                     roster ['RN']                                       -> 0
required ['RN']                 roster []                                           -> 0

All checks passed.
```

The second row is the one to study. Both the roster and the requirement are
built from nothing but `"RN"` and `"NA"`, so every one of the four blocks
contains exactly the same two *roles*. Only two of them contain the right
*numbers*. A solution comparing `set(block) == set(required)` answers `4` here,
confidently and instantly.

## Steps

1. Create the file, paste the starter, and run it. Every row prints `None` and
   the first assert fails. Correct starting point.
2. Write the two guards. `size == 0` and `size > len(roster)` both return `0`,
   and they can share a line.
3. Build `wanted = Counter(required)` once, above the loop. It never changes.
4. Build the first window with `Counter(roster[:size])`. This is the one place a
   `Counter` may be built from a slice, because there is no previous table to
   adjust.
5. Seed the answer. The first block is a real block and might already be
   compliant, so the count starts at `1` or `0` depending on the comparison —
   not always at `0`.
6. Write the slide. Add `roster[right]`. Then decrement `roster[right - size]`.
   Then, if that count is now zero, `del` the key.
7. Compare the two tables and increment. No early return: the contract asks for
   a count, so you must see every block.
8. Trace the second case by hand, four blocks, writing out the window's table
   at each step. It is the fastest way to feel why the deletion matters.

## The Solution

```python
"""exercise-03-rota-window-solution.py — counting compliant staffing blocks.

A ward publishes its roster as one role code per shift. Regulation says any
run of len(required) consecutive shifts must be covered by exactly the mix in
`required` — same roles, same counts, order irrelevant.

The window is a fixed size and the state inside it is a frequency table. One
Counter is built once from the requirement; the other is nudged by two keys
per slide. The graded line is the deletion: a key sitting at zero is not the
same as a key that is absent, and Counter equality knows the difference.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def count_compliant_blocks(roster: list[str], required: list[str]) -> int:
    """Return how many staffing blocks in the roster are compliant.

    Args:
        roster: Role codes, one per shift, in chronological order.
        required: The role mix a block must be covered by. Repeats are real
            requirements: two "RN" entries mean two registered nurses.

    Returns:
        The number of contiguous blocks of len(required) shifts whose role
        counts equal the requirement's. Overlapping blocks count separately.
        Zero when the requirement is empty or longer than the roster.
    """
    size = len(required)
    if size == 0 or size > len(roster):
        return 0

    wanted = Counter(required)
    window = Counter(roster[:size])
    compliant = 1 if window == wanted else 0

    for right in range(size, len(roster)):
        window[roster[right]] += 1
        leaving = roster[right - size]
        window[leaving] -= 1
        if window[leaving] == 0:
            del window[leaving]
        if window == wanted:
            compliant += 1

    return compliant


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]),
        (["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]),
        (["RN", "RN", "RN", "LPN"], ["RN", "RN"]),
        (["RN", "RN"], ["LPN"]),
        (["RN"], ["RN", "NA"]),
        (["RN"], []),
        ([], ["RN"]),
    ]
    for roster, required in cases:
        found = count_compliant_blocks(roster, required)
        print(f"required {str(required):<22} roster {str(roster):<44} -> {found}")
    print()

    assert count_compliant_blocks(["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]) == 3
    assert count_compliant_blocks(["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]) == 2
    assert count_compliant_blocks(["RN", "RN", "RN", "LPN"], ["RN", "RN"]) == 2
    assert count_compliant_blocks(["RN", "RN"], ["LPN"]) == 0
    assert count_compliant_blocks(["RN"], ["RN", "NA"]) == 0
    assert count_compliant_blocks(["RN"], []) == 0
    assert count_compliant_blocks([], ["RN"]) == 0

    # The incremental table must agree with rebuilding one per block.
    for roster, required in cases:
        size = len(required)
        if size == 0 or size > len(roster):
            continue
        slow = sum(
            Counter(roster[i : i + size]) == Counter(required)
            for i in range(len(roster) - size + 1)
        )
        assert count_compliant_blocks(roster, required) == slow

    print("All checks passed.")
```

**Both guards live in one line, and both are contract decisions rather than
defensive coding.**

```python
if size == 0 or size > len(roster):
    return 0
```

The first says an empty requirement is a caller error. It would have been
equally consistent to define an empty requirement as matching every position —
the empty multiset really is a sub-multiset of anything — and the contract
simply chooses not to. That is the point: it is a decision that gets *made*, in
the brief, rather than discovered in the loop. The second guard exists because
Python's slicing will not protect you: `roster[:size]` truncates silently, so
without the guard you would compare a short window against a long requirement
forever.

**`wanted` is built once and never touched again.** It is the target, and the
window is the thing that moves. Rebuilding `Counter(required)` inside the loop
is a surprisingly common reflex and adds `O(m)` to every step for no reason at
all.

**The seed is a real comparison, not a zero.**

```python
window = Counter(roster[:size])
compliant = 1 if window == wanted else 0
```

The first block is a block. Starting the count at `0` and entering the loop
skips it, and the loop starts at `right = size`, which is the *second* block.
This is the same family of bug as Exercise 1's `best_total = 0`: the first
window is easy to forget precisely because it is handled outside the loop.

**The three lines of the slide, and the third one is the exercise.**

```python
window[roster[right]] += 1
leaving = roster[right - size]
window[leaving] -= 1
if window[leaving] == 0:
    del window[leaving]
```

Adding is easy — `Counter` treats a missing key as zero, so `+= 1` works
whether or not the role has been seen before. Removing is where the trap is.
After the decrement the count may be zero, and a zero-valued key is still a
key. `Counter({'RN': 1, 'NA': 0})` and `Counter({'RN': 1})` are different
dictionaries and compare unequal, so a window carrying zero entries will never
match anything, and your function returns 0 on rosters that obviously have
matches. Delete the key and the two tables can be compared directly.

Worth knowing for later: `Counter` has a `+` operator that drops non-positive
counts, so `window + Counter()` cleans the table up — but it also copies the
whole thing, which turns an `O(1)` slide into an `O(vocabulary)` one. The
explicit `del` is both cheaper and clearer about what it is protecting.

**The element that leaves is `roster[right - size]`.** After the addition the
window covers `roster[right - size + 1 : right + 1]`, so the shift that has just
fallen out the back is the one at `right - size`. Off-by-one here shifts the
whole window by a position and produces answers that are wrong in a way no
single test makes obvious.

**No early return.** The contract asks how many, and the only way to know how
many is to look at all of them. The sister problem — *is there at least one
compliant block?* — can stop at the first match, and a solution written for
that one will pass two of these tests and fail the rest.

**Why this is `O(n + m)` and not `O(n · vocabulary)`.** Building `wanted` and
the first window is `O(m)`. Each of the `n - m` slides does two constant-time
dictionary updates and one table comparison. That comparison touches at most 12
keys by the vocabulary bound, and 12 is a constant, so the whole loop is
linear. State the bound before you make the claim; the claim depends on it.

## Run it

Copy the worked answer on this page into `exercise-03-rota-window.py` and run it:

```bash
python exercise-03-rota-window.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-rota-window.py`.

## Common bugs to catch

- **Every answer is `0`, or nearly.** You left zero counts in the window table.
  No traceback — the code runs, the comparison just never succeeds. Reproduce
  it in a REPL so you recognise the shape:

  ```text
  >>> from collections import Counter
  >>> window = Counter(["RN", "NA"])
  >>> window["NA"] -= 1
  >>> window
  Counter({'RN': 1, 'NA': 0})
  >>> window == Counter(["RN"])
  False
  ```

  That `False` is the whole bug. Two tables a human would call the same, and
  Python calls different, because one has a key the other does not.

- **`count_compliant_blocks(["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"])`
  returns `4` instead of `2`.** You compared sets rather than multisets. All
  four blocks contain the roles `{"RN", "NA"}`; only two contain two nurses and
  one assistant. The requirement is a mix, not a menu.

- **The answer is one too low on rosters whose first block is compliant.** You
  seeded `compliant = 0` and let the loop find everything. The loop starts at
  the second block; the first one is yours to check before it.

- **`IndexError: list index out of range`.**

  ```text
  Traceback (most recent call last):
      leaving = roster[right - size]
                ~~~~~~^^^^^^^^^^^^^^
  IndexError: list index out of range
  ```

  You dropped the guard on `size > len(roster)` and the loop ran with a window
  wider than the data. Note that the *first* symptom of that missing guard is
  usually not this exception at all — it is a silently wrong comparison,
  because `roster[:size]` truncated without complaint.

- **`KeyError` on the delete.**

  ```text
  Traceback (most recent call last):
      del window[leaving]
      ^^^^^^^^^^^^^^^^^^^
  KeyError: 'NA'
  ```

  You deleted unconditionally instead of only when the count reached zero, and
  the second time the same role left the window there was nothing there.

- **Returning `True` at the first match.** You solved the sister problem. The
  contract says count; there is no early exit that is compatible with counting.

- **Rebuilding the window table each step.** `Counter(roster[i:i + size])` per
  iteration is `O(m)` per step and `O(n · m)` overall — Exercise 1's rescan in a
  new outfit. No exception, right answers, wrong solution.

- **Treating an empty `required` as "everything matches".** Defensible in the
  abstract and not what the contract says. Read Requirement 4.

## Under the hood

<details>
<summary>Under the hood — what Counter equality really compares, and the trick this exercise is setting up</summary>

**`Counter.__eq__` is `dict.__eq__`, and that is the whole story.**

`Counter` subclasses `dict` and does not override equality, so two counters are
equal exactly when they are equal as dictionaries: same keys, same values. The
"missing key reads as zero" convenience belongs to `__missing__`, which is only
consulted on a *read* of a key that is absent. It has no say in equality.

Python 3.10 added `<=` and `>=` to `Counter` for multiset containment, which is
genuinely useful — `Counter(block) >= Counter(required)` asks "does the block
cover the requirement, ignoring surplus?" and that is precisely the question
Challenge 1 asks. It is worth knowing it exists, and worth knowing it costs one
probe per key in the smaller counter, so it does not rescue you from a per-step
scan.

**Three ways to compare a block against a requirement, and their costs.**

| Approach | Per block | Whole roster |
| --- | --- | --- |
| Sort both and compare lists | `O(m log m)` | `O(n · m log m)` |
| Build a fresh `Counter` per block | `O(m)` | `O(n · m)` |
| Slide the table, compare tables | `O(vocabulary)` | `O(n · vocabulary)` |
| Slide the table, keep a matched count | `O(1)` | `O(n + m)` |

The page's solution is the third row, and the vocabulary bound is what makes
that row honest here: 12 is a constant, so `O(n · 12)` is `O(n)`. The fourth
row is what you do when the vocabulary is *not* small.

**The fourth row, since you will need it on Thursday.**

Instead of comparing whole tables, carry one integer: how many distinct role
codes currently have exactly the right count in the window. Call it `matched`,
and let `distinct_wanted` be the number of distinct codes in the requirement.
Then `matched == distinct_wanted` is the compliance test, and it is a single
comparison.

The bookkeeping is two `if`s, and both are one character wide:

- when a count changes *to* its target, `matched += 1`;
- when a count changes *away from* its target, `matched -= 1`.

Every slide changes exactly two counts, so `matched` changes at most twice per
step. That is the trick that makes [Challenge 1](../challenges/challenge-01-shortest-kit-span.md)
work at a catalogue of 500 codes rather than 12, and practising it here — where
you already have a correct answer to check against — is much easier than
meeting it cold.

**Why `sum(...)` over a generator of booleans works in the self-check.** `True`
is `1` and `False` is `0` in Python, because `bool` subclasses `int`. So
`sum(condition for x in xs)` counts how many times the condition held. It reads
cleanly and it is a genuine idiom, not a trick — though `sum(1 for x in xs if
condition)` is clearer when the condition is long.

</details>

## Acceptance checklist

- [ ] `python exercise-03-rota-window.py` prints seven rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] Every count that reaches zero has its key deleted.
- [ ] The first block is checked before the loop starts.
- [ ] No `Counter(...)` of a slice appears inside the loop.
- [ ] Your solution has no early return.
- [ ] You can state the vocabulary bound and say what breaks without it.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 exercise 3: the rota window`.

## Stretch

- **Return the positions instead of the count.** The window is identical; only
  the combine step changes.

  ```python
  def compliant_block_starts(roster: list[str], required: list[str]) -> list[int]:
      """Return, ascending, the start index of every compliant staffing block."""
      size = len(required)
      if size == 0 or size > len(roster):
          return []
      wanted = Counter(required)
      window = Counter(roster[:size])
      starts = [0] if window == wanted else []
      for right in range(size, len(roster)):
          window[roster[right]] += 1
          leaving = roster[right - size]
          window[leaving] -= 1
          if window[leaving] == 0:
              del window[leaving]
          if window == wanted:
              starts.append(right - size + 1)
      return starts
  ```

  ```text
  ["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"] -> [0, 1, 4]
  ```

  Being able to say "same window, same invariant, different combine step" — and
  be right about it — is the sort of structural observation that reads as
  senior. The [mini-project's Problem 3](../mini-project/README.md) is this
  exact change in another domain.

- **Rewrite it with a matched count instead of a table comparison.** Use the
  recipe in *Under the hood*. Check it against the version you already have on
  all seven cases; the whole value of doing it now is that you have a correct
  answer to disagree with.

- **Allow surplus.** Change the question from "the block is exactly this mix"
  to "the block contains at least this mix", which is what a ward would
  actually ask if extra staff turned up. One operator changes in the
  comparison, and the window size stops being forced — which is a much bigger
  change than it sounds, and it is what Challenge 1 is about.
Next: [Exercise 4 — The Shortest Catchment](./exercise-04-shortest-catchment.md).
