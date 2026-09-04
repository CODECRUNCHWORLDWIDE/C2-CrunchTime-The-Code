# Problem 3 — When the Window Fails

> **Topic:** pattern rejection — recognising a problem that looks like a sliding window, proving it is not, and reaching for the right tool instead
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** pattern matching is what you do; pattern *rejection* is what you decline to do, and it is invisible in a portfolio unless you make it visible. This page makes it visible by having you write both solutions — the one that is right and the one that looks right — and print the log where they disagree. A pattern you have watched fail is a pattern you will not misapply.

## The Brief

A pallet loader logs the weight of every crate as it comes off the truck, in
kilograms, in unloading order. A pallet takes exactly **two crates**, and their
weights must add up to the pallet allowance.

**Your job.** Find two crates whose weights sum to the allowance and return
their positions.

Now read that again and count the sliding-window signals. There is a list. It
is in order. You are looking for something inside it. The word "two" is even
there, and windows have two edges.

None of that is the signal. The signal for a sliding window is **contiguity** —
the thing you are looking for has to be a run of neighbouring elements. And
this problem says the opposite: the two crates *may sit anywhere in the log*,
with any number of other crates between them. Crate 0 can pair with crate 40.

Here is the test to apply, and it is worth memorising because it takes five
seconds:

> A sliding window can only ever produce three kinds of answer about a
> **contiguous** run: how long the best one is, how many there are, or an
> extreme value over them. If what you want is not one of those three things
> about a contiguous run, the pattern does not fit.

This problem wants a **pair of positions**, and the pair is not a run. Two
strikes. It is a hash-map problem — Week 2's pattern — and the right move is to
walk the list once, remembering every weight you have seen and where you first
saw it, and at each new crate ask whether the weight that would complete the
pallet has already gone past.

On this page you will write both. The correct lookup, and a two-wide window
that only ever compares neighbouring crates. Then you run them side by side and
print the logs where they disagree, so the rejection is something you can point
at rather than a claim you have to take on trust.

**The contract.** Return `(i, j)` with `i < j`. Where several pairs work, return
the one that **completes earliest** — the smallest `j` — and among pairs sharing
that `j`, the smallest `i`. A crate is never paired with itself. If no two
crates fill the pallet, return `None`.

That tie-break is chosen to match how the loader actually works: the pallet is
finished the moment the second crate arrives, so the earliest completion is the
first pallet that can physically be built.

## Starter

Create `problem-03-when-the-window-fails.py` and paste this in. Fill in every
`TODO`.

```python
"""problem-03-when-the-window-fails.py — the pattern that does not fit.

Find two crates, anywhere in the log, whose weights fill the pallet. Then
watch a sliding window fail at the same job, on purpose.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def pallet_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """Return the positions of two crates whose weights fill the allowance.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        (i, j) with i < j, choosing the pair that completes earliest — the
        smallest j — and, among pairs sharing that j, the smallest i. None
        when no two crates add up to the allowance. A crate is never paired
        with itself.
    """
    # TODO: a dict from weight to the FIRST index it appeared at.
    # TODO: walk j over the log. Work out the partner weight this crate needs.
    #       If that partner is already in the dict, you are done — and because
    #       you are walking forward, this j is the earliest possible.
    # TODO: record this weight, but only if it is not already recorded. Keeping
    #       the FIRST sighting is what makes the second tie-break rule true.
    ...


def neighbouring_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """The wrong pattern, kept so you can watch it fail.

    A two-wide sliding window can only ever compare crates that touch, so it
    answers "are there two ADJACENT crates that fill the pallet?" — a
    different question from the one the loader asked.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        The first adjacent pair that fills the allowance, or None.
    """
    # TODO: slide a two-wide window and return the first pair that sums right.
    #       Write it. It is correct code answering the wrong question, and
    #       seeing that distinction on your own screen is the point of the page.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int]] = [
        ([310, 240, 90, 150, 260], 400),
        ([200, 100, 200], 400),
        ([120, 280, 200, 200], 400),
        ([200, 200, 200], 400),
        ([10, 20], 100),
        ([400], 400),
        ([], 400),
    ]

    print(f"{'log':<28} {'allowance':>9}  {'lookup':>10}  {'window':>10}  agree")
    for weights, allowance in cases:
        right = pallet_pair(weights, allowance)
        wrong = neighbouring_pair(weights, allowance)
        print(f"{str(weights):<28} {allowance:>9}  {str(right):>10}  {str(wrong):>10}  {'yes' if right == wrong else 'NO'}")
    print()

    weights, allowance = cases[0]
    i, j = pallet_pair(weights, allowance)
    print(f"the window misses {weights[i]} at index {i} plus {weights[j]} at index {j},")
    print(f"because {weights[i + 1]} sits between them and a window cannot skip it.")
    print()

    assert pallet_pair([310, 240, 90, 150, 260], 400) == (0, 2)
    assert pallet_pair([200, 100, 200], 400) == (0, 2)
    assert pallet_pair([120, 280, 200, 200], 400) == (0, 1)
    assert pallet_pair([200, 200, 200], 400) == (0, 1)
    assert pallet_pair([10, 20], 100) is None
    assert pallet_pair([400], 400) is None
    assert pallet_pair([], 400) is None

    assert neighbouring_pair([310, 240, 90, 150, 260], 400) is None
    assert neighbouring_pair([200, 100, 200], 400) is None

    # Whatever the lookup returns is a real pair, and nothing completes sooner.
    for weights, allowance in cases:
        found = pallet_pair(weights, allowance)
        pairs = [
            (j, i)
            for j in range(len(weights))
            for i in range(j)
            if weights[i] + weights[j] == allowance
        ]
        if not pairs:
            assert found is None
            continue
        second, first = min(pairs)
        assert found == (first, second)

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/homework/problem-03-when-the-window-fails.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `pallet_pair(weights, allowance)` returns `(i, j)` with `i < j`, or `None`.
2. The pair completing earliest wins — the smallest `j`.
3. Among pairs sharing that `j`, the smallest `i` wins.
4. A crate is never paired with itself. `pallet_pair([400], 400)` is `None`.
5. `pallet_pair` makes exactly one pass and never compares a crate against
   every other.
6. `neighbouring_pair` is implemented as a genuine two-wide window and returns
   the first adjacent pair.
7. The two disagree on at least two of the seven logs, and the program prints
   which.
8. Every function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(weights) <= 150_000`.** A container ship's manifest. The bound
  rejects comparing every crate against every other, which is about
  `1.1 x 10^10` comparisons here. This is the same bound that rejects brute
  force in the window problems, and it is worth noticing that the *reason* is
  identical while the *solution* is from a different family entirely.

- **`1 <= weights[i] <= 2_000` and `2 <= allowance <= 4_000`.** Crates are real
  objects with positive mass, and a pallet takes two of them. Positivity is not
  load-bearing here the way it was in Exercise 4 — the lookup works fine with
  negative numbers, which is itself a useful contrast. Ask yourself why: the
  hash map never assumes anything is monotone, because it never shrinks
  anything.

- **A crate cannot pair with itself.** So a log of `[400]` with an allowance of
  `400` returns `None`, not `(0, 0)`. This is the case that decides *where* in
  the loop you record each weight: record before you look up, and every crate
  becomes its own partner whenever the allowance is exactly double its weight.

- **Weights repeat, and that is normal.** Identical crates are the common case
  in a warehouse, so `[200, 200, 200]` with an allowance of `400` is real
  input, not an edge case. It is also the case that makes the "first sighting"
  rule matter.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-when-the-window-fails.py
log                          allowance      lookup      window  agree
[310, 240, 90, 150, 260]           400      (0, 2)        None  NO
[200, 100, 200]                    400      (0, 2)        None  NO
[120, 280, 200, 200]               400      (0, 1)      (0, 1)  yes
[200, 200, 200]                    400      (0, 1)      (0, 1)  yes
[10, 20]                           100        None        None  yes
[400]                              400        None        None  yes
[]                                 400        None        None  yes

the window misses 310 at index 0 plus 90 at index 2,
because 240 sits between them and a window cannot skip it.

All checks passed.
```

Two rows say `NO`, and those two rows are the deliverable. In the first log the
correct pair is 310 at index 0 and 90 at index 2 — a crate apart. The window
never compares them, because 240 sits between them and a window has no way to
skip it. The window is not buggy. It is correct code answering a question
nobody asked.

Note that the other five rows agree, and that is exactly why this bug survives
in the wild: on any log where the answer happens to be adjacent, the wrong
pattern looks right.

## Steps

1. Create the file, paste the starter, and run it. Correct starting point.
2. Write `pallet_pair`. One dict, one pass.
3. Get the order inside the loop right: **look up first, then record**. Test it
   against `[400]` with an allowance of `400` — if you get `(0, 0)`, your record
   is above your lookup.
4. Get the record right: only store a weight if it is not already stored. Test
   it against `[200, 200, 200]` with an allowance of `400` — you want `(0, 1)`,
   and overwriting would give you `(1, 2)`.
5. Write `neighbouring_pair`. It is four lines and it is deliberately the wrong
   tool. Do not skip it; the printed disagreement is the point of the page.
6. Run it and read the two `NO` rows.
7. Now write the rejection down, in your own words, somewhere you will keep it.
   Two to four sentences covering: (a) why "two crates summing to the
   allowance" is not a contiguous-run question, and (b) why, even if you could
   phrase it as a window, a pair of positions is not one of the three things a
   window naturally produces.

## The Solution

```python
"""problem-03-when-the-window-fails-solution.py — the pattern that does not fit.

A pallet loader logs crate weights in the order they come off the truck. A
pallet takes exactly two crates, and their weights must add up to the pallet
allowance. The two crates may sit anywhere in the log, with any number of
other crates between them.

That "anywhere" is the whole point. A sliding window only ever looks at a
contiguous stretch, so a window that checks neighbouring crates answers a
different question and misses real pairs. This file implements both — the
lookup that is right, and the window that is wrong — and prints the log where
they disagree, so the rejection is something you can run rather than a claim
you have to take on trust.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def pallet_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """Return the positions of two crates whose weights fill the allowance.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        (i, j) with i < j, choosing the pair that completes earliest — the
        smallest j — and, among pairs sharing that j, the smallest i. None
        when no two crates add up to the allowance. A crate is never paired
        with itself.
    """
    first_seen: dict[int, int] = {}

    for j, weight in enumerate(weights):
        partner = allowance - weight
        if partner in first_seen:
            return (first_seen[partner], j)
        if weight not in first_seen:
            first_seen[weight] = j

    return None


def neighbouring_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """The wrong pattern, kept so you can watch it fail.

    A two-wide sliding window can only ever compare crates that touch, so it
    answers "are there two ADJACENT crates that fill the pallet?" — a
    different question from the one the loader asked.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        The first adjacent pair that fills the allowance, or None.
    """
    for i in range(len(weights) - 1):
        if weights[i] + weights[i + 1] == allowance:
            return (i, i + 1)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int]] = [
        ([310, 240, 90, 150, 260], 400),
        ([200, 100, 200], 400),
        ([120, 280, 200, 200], 400),
        ([200, 200, 200], 400),
        ([10, 20], 100),
        ([400], 400),
        ([], 400),
    ]

    print(f"{'log':<28} {'allowance':>9}  {'lookup':>10}  {'window':>10}  agree")
    for weights, allowance in cases:
        right = pallet_pair(weights, allowance)
        wrong = neighbouring_pair(weights, allowance)
        print(f"{str(weights):<28} {allowance:>9}  {str(right):>10}  {str(wrong):>10}  {'yes' if right == wrong else 'NO'}")
    print()

    weights, allowance = cases[0]
    i, j = pallet_pair(weights, allowance)
    print(f"the window misses {weights[i]} at index {i} plus {weights[j]} at index {j},")
    print(f"because {weights[i + 1]} sits between them and a window cannot skip it.")
    print()

    assert pallet_pair([310, 240, 90, 150, 260], 400) == (0, 2)
    assert pallet_pair([200, 100, 200], 400) == (0, 2)
    assert pallet_pair([120, 280, 200, 200], 400) == (0, 1)
    assert pallet_pair([200, 200, 200], 400) == (0, 1)
    assert pallet_pair([10, 20], 100) is None
    assert pallet_pair([400], 400) is None
    assert pallet_pair([], 400) is None

    assert neighbouring_pair([310, 240, 90, 150, 260], 400) is None
    assert neighbouring_pair([200, 100, 200], 400) is None

    # Whatever the lookup returns is a real pair, and nothing completes sooner.
    for weights, allowance in cases:
        found = pallet_pair(weights, allowance)
        pairs = [
            (j, i)
            for j in range(len(weights))
            for i in range(j)
            if weights[i] + weights[j] == allowance
        ]
        if not pairs:
            assert found is None
            continue
        second, first = min(pairs)
        assert found == (first, second)

    print("All checks passed.")
```

**Look up before you record, and that ordering is the self-pairing rule.**

```python
partner = allowance - weight
if partner in first_seen:
    return (first_seen[partner], j)
if weight not in first_seen:
    first_seen[weight] = j
```

At the moment of the lookup, `first_seen` holds only crates at positions
strictly before `j`. So any hit is a genuine partner at an earlier index, and
`i < j` is guaranteed by construction rather than by a check. Record first
instead and a crate weighing exactly half the allowance finds itself, returning
`(0, 0)` on a single-crate log.

**Record the first sighting only, and that is the second tie-break.**

`if weight not in first_seen` keeps the earliest index for each weight. On
`[200, 200, 200]` with an allowance of `400`, the crate at index 1 looks up
`200` and finds index 0, giving `(0, 1)`. Overwrite on every sighting and index
2 would be the one recorded by then — except the function has already returned,
which is exactly the kind of accident that makes this bug hard to see. Build a
log where the pair is found later and it bites.

**Returning inside the loop is what makes the first tie-break true.** The walk
goes forward, so the first `j` at which any partner exists is the smallest such
`j`. There is nothing to compare and no incumbent to beat — the loop structure
delivers the tie-break for free. Compare that with the window problems, where
the tie-break had to be encoded in a comparison operator; here it falls out of
the traversal order. Noticing which of the two situations you are in saves a
lot of unnecessary bookkeeping.

**Why the window cannot be repaired.** The obvious patch is to widen it — three
crates, four, all of them. But a window of width `w` compares crates at most
`w - 1` apart, and the answer may be `n - 1` apart, so the only width that
works is `n`, at which point it is not a window and the cost is `O(n^2)`
comparisons. The pattern is not slightly wrong here; it is aimed at a different
question.

The single sentence to keep: **a window can only see a contiguous run, so if
the answer's parts do not have to be neighbours, the window is the wrong
tool.**

**What replaces it, and why.** The hash map turns "is the partner anywhere
behind me?" from a search into a lookup. That is Week 2's move and it composes
happily with windows — Exercises 3 and 5 both keep dictionaries *inside* a
window. The two patterns are not rivals. What they answer is different: a
window answers questions about *runs*, a map answers questions about
*membership*, and this problem is entirely a membership question.

**Cost.** One pass, one dictionary operation per crate, so `O(n)` time and
`O(min(n, 2000))` space — the second bound from the weight range, since there
are only so many distinct weights to remember. The brute force is `O(n^2)` time
and `O(1)` space; the size bound rejects it. `neighbouring_pair` is `O(n)` and
answers a different question, which is a useful reminder that being fast is not
the same as being right.

## Run it

Copy the worked answer on this page into `problem-03-when-the-window-fails.py` and run it:

```bash
python problem-03-when-the-window-fails.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-03-when-the-window-fails.py`.

## Common bugs to catch

- **`pallet_pair([400], 400)` returns `(0, 0)`.** You recorded the weight
  before looking its partner up, so the crate found itself. Move the lookup
  above the record.

- **`TypeError: cannot unpack non-sequence NoneType object`.**

  ```text
  Traceback (most recent call last):
      i, j = pallet_pair(weights, allowance)
      ^^^^
  TypeError: cannot unpack non-sequence NoneType object
  ```

  The self-check unpacks the first case's answer, so this means `pallet_pair`
  returned `None` on a log that has a pair in it. Usually the lookup is
  checking the wrong dictionary — `if weight in first_seen` rather than
  `if partner in first_seen`.

- **`pallet_pair` returns a later pair than it should.** You overwrote the
  index on every sighting instead of keeping the first. On logs with repeated
  weights the returned `i` is too large.

- **`KeyError`.**

  ```text
  Traceback (most recent call last):
      return (first_seen[partner], j)
              ~~~~~~~~~~^^^^^^^^^
  KeyError: 310
  ```

  You looked up a key you had not tested for, usually by restructuring the
  `if`. The membership test and the read have to agree about which key they are
  talking about.

- **`neighbouring_pair` finds the right answer on every log.** Then it is not a
  two-wide window — you probably wrote a nested loop by accident. Check that
  its inner expression only ever touches `weights[i]` and `weights[i + 1]`. The
  page needs it to fail; a version that succeeds teaches nothing.

- **Comparing every crate against every other.** Correct, `O(n^2)`, and
  rejected by the size bound. It also hides the lesson, because it does not
  fail on the interesting logs — it just takes a week.

- **Concluding that sliding window is a bad pattern.** It is an excellent
  pattern for the questions it answers. The skill being built here is telling
  which questions those are, not developing a suspicion of windows.

## Under the hood

<details>
<summary>Under the hood — a rejection checklist, and the near-miss problems that really are windows</summary>

**The three-question rejection test.**

Before reaching for a window, ask:

1. **Does the answer have to be contiguous?** If the thing you are looking for
   can have gaps, stop. This is the fastest and most reliable signal, and it
   rejects this problem in about two seconds.
2. **Is the answer one of: a length, a count of windows, or an extreme over
   windows?** Those are the only three shapes a window naturally produces. A
   pair of unrelated positions is none of them.
3. **Is the property monotone under shrinking?** If removing an element from
   the left can *break* something that was true, the shrink loop has no
   boundary to find, and even a contiguous problem will not yield. This is the
   question Exercise 4's non-negativity requirement was really about, and it is
   the one people skip.

Any single "no" is a rejection. All three "yes" and you almost certainly have a
window.

**Near misses worth knowing, because they invert the answer.**

*Two crates that sum to the allowance, but they must be adjacent.* Now it is a
window — a trivial one, width 2 — and `neighbouring_pair` is the correct
solution. One word in the prompt flips which of the two functions on this page
is right.

*The longest run of crates whose total weight is at most the allowance.*
Contiguous, and the answer is a length, and the property is monotone under
shrinking because weights are positive. All three questions pass. That is
Exercise 4's family.

*Two crates that sum to the allowance, in a log that is already sorted by
weight.* Not a window either — but not a hash map, and the reason is worth
sitting with. Sorted order means two pointers moving *toward each other* from
the ends, which is Week 1's converging two-pointer and looks superficially like
a window because it also uses two indices. The difference is direction: a
window's indices both move forward and never cross; a converging pair moves
inward and meets. Same number of variables, entirely different invariant.

**Why the negative space belongs in a portfolio.**

An interviewer learns more from thirty seconds of *"this looks like a sliding
window and it is not, because the two crates need not be neighbours — I'd
reach for a hash map"* than from three minutes of a correct window solution to
a window problem. The first demonstrates judgement; the second demonstrates
recall.

That signal is only available if you practise saying it. It does not appear on
its own during a solve, because when the pattern is right nobody asks you to
justify rejecting the alternatives. Writing it down deliberately, on a page
built for it, is how it becomes something you can produce under pressure.

**A footnote on the hash map's indifference to sign.** The lookup on this page
works unchanged on negative weights, zero, floats, whatever — because it never
assumes anything about ordering or monotonicity. It only ever asks "have I seen
this exact value". That robustness is the flip side of its limitation: it knows
nothing about neighbours, which is precisely why it cannot answer the questions
a window answers.

</details>

## Acceptance checklist

- [ ] `python problem-03-when-the-window-fails.py` prints the table, the two explanation lines, then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] Exactly two rows of the table say `NO`.
- [ ] `pallet_pair([400], 400)` returns `None`, and you can say which line makes that true.
- [ ] `pallet_pair([200, 200, 200], 400)` returns `(0, 1)`, not `(1, 2)`.
- [ ] `pallet_pair` makes one pass and never compares a crate against every other.
- [ ] `neighbouring_pair` is a genuine two-wide window and genuinely fails on two logs.
- [ ] You have written the rejection down in two to four sentences, covering both the contiguity point and the return-shape point.
- [ ] You can recite the three-question rejection test from *Under the hood*.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 homework 3: when the window fails`.

## Stretch

- **Flip the prompt so the window becomes right.** *"Find two **adjacent**
  crates that fill the pallet."* Now `neighbouring_pair` is the answer and the
  hash map is overkill. Write both prompts side by side in your notes with the
  word that differs underlined. One word, opposite conclusions.

- **Return every pair, not just the earliest.** The tie-break disappears, and
  so does the early return — which means the "first sighting only" rule has to
  become a list of sightings.

  ```python
  def all_pallet_pairs(weights: list[int], allowance: int) -> list[tuple[int, int]]:
      """Return every (i, j) with i < j whose weights fill the allowance."""
      seen: dict[int, list[int]] = {}
      found: list[tuple[int, int]] = []
      for j, weight in enumerate(weights):
          for i in seen.get(allowance - weight, []):
              found.append((i, j))
          seen.setdefault(weight, []).append(j)
      return found
  ```

  ```text
  ([200, 200, 200], 400) -> [(0, 1), (0, 2), (1, 2)]
  ([310, 240, 90, 150, 260], 400) -> [(0, 2)]
  ```

  Note that this is no longer `O(n)` — it cannot be, because the output itself
  can be quadratic. When the answer is big, the algorithm cannot be small, and
  saying so is a better response than trying to optimise it.

- **Audit your own Week 1 and Week 2 write-ups.** Pick one and add a short
  paragraph: *"why this is not a sliding-window problem."* You now have the
  three-question test to structure it. Doing this once per pattern, as you
  learn each new one, is how the negative space accumulates.

Next: [Problem 4 — Behavioral Story 3](./problem-04-behavioral-story-03.md).
