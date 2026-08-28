# Challenge 1 — The Settlement Trio

> **Topic:** pinning one element and running converging pointers over the rest, with three separate duplicate suppressions
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Medium
> **Target time:** 90 minutes
> **Why this one:** "find three of something" is one of the most commonly asked interview shapes, and the pin-plus-converging structure generalises — four of something is two pins around the same inner scan. It is also the first problem this week where the hard part is not the algorithm. It is the deduplication, and most candidates lose the points there rather than on the search.

## The Brief

A food co-op's treasurer is closing out the **suspense account**. That is the
holding bucket where every transaction the bookkeeping software could not
classify has been parked all year. Each entry is an amount in cents. Credits
are negative, debits are positive.

The auditor's rule is that a suspense balance may be written off only if it
can be **accounted for by exactly three parked entries that sum to it.** The
treasurer needs *every* way that can be done, so the board can pick the
explanation that actually makes sense.

Now the part that makes this a real problem rather than a search.

**Two write-offs that use the same three amounts are the same explanation.**
`(-200, -200, 400)` is one explanation whether the two 200-cent credits came
from March or from August — the board is being asked to approve "two
two-hundred-cent credits and a four-hundred-cent debit," and where they sat
in the ledger is not part of that sentence. So the answer is a set of
distinct **amount** triples, not a set of index triples.

But the entries still have to be real and separate. **Each triple must be
drawable from three distinct positions in the ledger.** A single entry cannot
pay for itself twice. So `[3, 3]` with a balance of `9` has no answer, even
though `3 + 3 + 3` lands on it exactly.

Return every distinct triple of amounts summing to the balance. Each triple
is sorted ascending. The list of triples is itself sorted ascending. Return
`[]` when nothing works.

```python
def settlement_trios(amounts: list[int], suspense: int) -> list[tuple[int, int, int]]:
    """Return every distinct (a, b, c) with a <= b <= c summing to `suspense`."""
```

The suspense balance is a real ledger figure and is very often **not zero**.
A solution with a zero hard-coded anywhere in it is answering a different
question.

## Starter

Save this as `challenge-01-settlement-trio.py` and fill in the `TODO`s.

```python
"""challenge-01-settlement-trio.py — explaining a suspense balance.

Sort the ledger, pin each amount in turn, and converge two pointers over the
tail for the pair that completes the trio.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def settlement_trios(amounts: list[int], suspense: int) -> list[tuple[int, int, int]]:
    """Find every distinct way three parked entries explain the balance.

    Args:
        amounts: The suspense account in ledger order, cents. Credits are
            negative. The caller's list is not modified.
        suspense: The balance the three amounts must sum to. Rarely zero.

    Returns:
        Every distinct (a, b, c) with a <= b <= c, drawn from three distinct
        ledger positions, summing to `suspense`. Sorted within each triple
        and across triples. Empty list when nothing works.
    """
    # TODO: sort a COPY of the ledger — the caller still needs theirs in
    #       ledger order
    # TODO: pin each position in turn, stopping early enough that two entries
    #       remain in the tail
    # TODO: skip a pin whose amount equals the previous pin's amount, because
    #       every triple it could find was already found
    # TODO: converging pointers over the tail, hunting for the pair that
    #       makes up the difference
    # TODO: after recording a match, step BOTH pointers past any repeat of
    #       the amount just used — that is two more suppressions, and each
    #       one protects a different example
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(settlement_trios([-2, -2, 0, 2, 2, 4], 0))

    assert settlement_trios([1, 3, 5, 7, 9], 15) == [(1, 5, 9), (3, 5, 7)]
    assert settlement_trios([2, 2, 2, 2], 6) == [(2, 2, 2)]
    assert settlement_trios([3, 3], 9) == []
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/challenges/challenge-01-settlement-trio.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `settlement_trios` returns a `list[tuple[int, int, int]]`.
2. Each triple is sorted ascending: `a <= b <= c`.
3. The list of triples is sorted ascending, and the tests compare it
   **exactly** — not up to reordering.
4. No triple appears twice, however much repetition the ledger holds.
5. Every triple is drawable from three **distinct** ledger positions.
6. The target is arbitrary. Nothing in the solution assumes it is zero.
7. `amounts` is unchanged after the call.
8. `O(n²)` time. An `O(n³)` triple loop does not pass inside the bound.
9. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(amounts) <= 4_000`.** Four thousand is chosen precisely, and it
  is the hint. The `O(n³)` triple loop is about `6.4 × 10¹⁰` operations and
  will not finish. The `O(n²)` pin-plus-converging solution is about
  `1.6 × 10⁷` and runs in well under a second. Read the bound and say what it
  rules out *before* you plan anything — a constraint that eliminates one
  approach and admits another is the interviewer telling you what they want.

- **`amounts` is not sorted.** It arrives in ledger order, which is
  chronological. You will sort it yourself at `O(n log n)`, which is
  dominated by the `O(n²)` scan and is therefore free. Contrast this with
  [Exercise 3](../exercises/exercise-03-widest-ballast-pair.md), where
  sortedness was handed to you and the positions had to be preserved. Here
  the positions are irrelevant to the answer, which is exactly what makes
  sorting allowed.

- **`-1_000_000 <= amounts[i] <= 1_000_000`, in cents.** Both signs are real:
  a credit is a negative entry. A solution that assumes positive amounts
  cannot find `(-500, -100, 600)`, and a solution that prunes on "this amount
  already exceeds the target, so stop" is wrong for the same reason — a
  large debit can still be part of a valid trio once a credit joins it.

- **`suspense` is any integer three amounts in that range could sum to.** It
  is not guaranteed to be zero, and the third example is built to punish
  assuming it is.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python challenge-01-settlement-trio-solution.py
suspense    0  3 explanation(s)  [(-5, -1, 6), (-5, 1, 4), (-1, 0, 1)]
suspense    0  2 explanation(s)  [(-2, -2, 4), (-2, 0, 2)]
suspense   15  2 explanation(s)  [(1, 5, 9), (3, 5, 7)]
suspense    0  2 explanation(s)  [(-7, -3, 10), (-3, -3, 6)]
suspense   15  2 explanation(s)  [(1, 5, 9), (5, 5, 5)]
suspense    6  1 explanation(s)  [(2, 2, 2)]
suspense    9  0 explanation(s)  []
suspense    0  0 explanation(s)  []
suspense  100  0 explanation(s)  []
All checks passed.
```

Five of these are worth stopping on.

**Line 1**, from `[-5, -1, 0, 1, 4, 6]`. Three explanations, and note the
required output order: sorted within each triple, and the list of triples
sorted too. Produce the right three in a different order and you have solved
the algorithm and failed the contract — and in a real system an unordered
answer means the board sees a different list every time it refreshes the
page.

**Line 2**, from `[-2, -2, 0, 2, 2, 4]`. This is the deduplication example
and it is the discriminating one. There is one way to build `(-2, -2, 4)`
and **four** ways to build `(-2, 0, 2)` — two choices of which `-2`, two
choices of which `2`. A solution without duplicate suppression emits five
triples where the answer has two.

**Line 3**, from `[1, 3, 5, 7, 9]` with a balance of `15`. The non-zero
target. Nothing about this problem is about summing to zero. If you wrote
`-amounts[i]` anywhere, this is the line where it shows.

**Line 4**, from `[-7, -3, -3, 10, 6]`. Unsorted input, a repeated credit,
and a triple that legitimately uses that credit twice — because there really
are two entries of `-3` at two distinct positions.

**Line 6**, from `[2, 2, 2, 2]` with a balance of `6`. Four identical
entries, four ways to choose three of them, one distinct explanation. This is
the case that catches deduplication logic which only guards the outer pin.

## Steps

1. Save the starter and run it. `AssertionError`.
2. Sort a **copy**: `ledger = sorted(amounts)`. The caller's list stays in
   ledger order. Say out loud that this costs `O(n)` space and that you chose
   to pay it.
3. Loop the pin over `range(len(ledger) - 2)`. Stopping two short leaves at
   least two entries in the tail, and it also handles the empty and
   two-entry ledgers without a special case — `range(-2)` and `range(0)` are
   both empty.
4. Skip a repeated pin: `if pin > 0 and ledger[pin] == ledger[pin - 1]:
   continue`. The `pin > 0` matters — without it, the first iteration
   compares against `ledger[-1]`, the largest amount in the sorted ledger.
5. Set `pair_target = suspense - ledger[pin]` and put converging pointers on
   `pin + 1` and the last position.
6. Run the Exercise 3 loop. Too small, move left up. Too big, move right
   down. Equal, record the triple.
7. **After recording**, step both pointers inward by one, then walk each of
   them past any repeat of the amount it just used. That is suppressions two
   and three. Write them as you go and say which example each protects.
8. Return the list. Do not sort it at the end — trace the loop and convince
   yourself it already comes out sorted.

## The Solution

```python
"""challenge-01-settlement-trio-solution.py — explaining a suspense balance.

Sort the ledger, pin each amount in turn, and converge two pointers over the
tail for the pair that completes the trio. Three duplicate suppressions —
one on the pin, one on each pointer after a match — turn index triples into
distinct amount triples.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def settlement_trios(amounts: list[int], suspense: int) -> list[tuple[int, int, int]]:
    """Find every distinct way three parked entries explain the balance.

    Args:
        amounts: The suspense account in ledger order, cents. Credits are
            negative. The caller's list is not modified.
        suspense: The balance the three amounts must sum to. Rarely zero.

    Returns:
        Every distinct (a, b, c) with a <= b <= c, drawn from three distinct
        ledger positions, summing to `suspense`. Sorted within each triple
        and across triples. Empty list when nothing works.
    """
    ledger = sorted(amounts)
    results: list[tuple[int, int, int]] = []

    for pin in range(len(ledger) - 2):
        if pin > 0 and ledger[pin] == ledger[pin - 1]:
            continue

        pair_target = suspense - ledger[pin]
        left, right = pin + 1, len(ledger) - 1
        while left < right:
            total = ledger[left] + ledger[right]
            if total < pair_target:
                left += 1
            elif total > pair_target:
                right -= 1
            else:
                results.append((ledger[pin], ledger[left], ledger[right]))
                left += 1
                right -= 1
                while left < right and ledger[left] == ledger[left - 1]:
                    left += 1
                while left < right and ledger[right] == ledger[right + 1]:
                    right -= 1

    return results


# ---- Self-check ----
if __name__ == "__main__":
    books = [
        ([-5, -1, 0, 1, 4, 6], 0),
        ([-2, -2, 0, 2, 2, 4], 0),
        ([1, 3, 5, 7, 9], 15),
        ([-7, -3, -3, 10, 6], 0),
        ([5, 5, 5, 1, 1, 9], 15),
        ([2, 2, 2, 2], 6),
        ([3, 3], 9),
        ([], 0),
        ([1, 2, 4, 8], 100),
    ]
    for amounts, suspense in books:
        trios = settlement_trios(amounts, suspense)
        print(f"suspense {suspense:>4}  {len(trios)} explanation(s)  {trios}")

    assert settlement_trios([-5, -1, 0, 1, 4, 6], 0) == [(-5, -1, 6), (-5, 1, 4), (-1, 0, 1)]
    assert settlement_trios([-2, -2, 0, 2, 2, 4], 0) == [(-2, -2, 4), (-2, 0, 2)]
    assert settlement_trios([1, 3, 5, 7, 9], 15) == [(1, 5, 9), (3, 5, 7)]
    assert settlement_trios([-7, -3, -3, 10, 6], 0) == [(-7, -3, 10), (-3, -3, 6)]
    assert settlement_trios([5, 5, 5, 1, 1, 9], 15) == [(1, 5, 9), (5, 5, 5)]
    assert settlement_trios([2, 2, 2, 2], 6) == [(2, 2, 2)]
    assert settlement_trios([0, 0, 0, 0], 0) == [(0, 0, 0)]
    assert settlement_trios([3, 3, 3], 9) == [(3, 3, 3)]
    assert settlement_trios([3, 3], 9) == []
    assert settlement_trios([], 0) == []
    assert settlement_trios([1, 2, 4, 8], 100) == []

    ledger_order = [-7, -3, -3, 10, 6]
    settlement_trios(ledger_order, 0)
    assert ledger_order == [-7, -3, -3, 10, 6]  # the caller's ledger is not sorted
    print("All checks passed.")
```

**Sorting turns "find three" into "pin one, find two."** Once the ledger is
in order, fixing the smallest member of the triple leaves a sorted tail, and
finding two numbers in a sorted list that hit a target is Exercise 3. That is
the whole idea: the outer loop costs a factor of `n`, and the inner scan is
the linear one you already know. A triple loop would be a factor of `n` on
top of a factor of `n` on top of a factor of `n`, which the bound forbids.

**There are three duplicate suppressions and each one protects a different
example.**

The **pin skip** protects `[-2, -2, 0, 2, 2, 4]`. Without it the second `-2`
pins as well and rediscovers every triple the first `-2` already found.

The **left-pointer skip after a match** protects `[-2, -2, 0, 0, 2, 2]`. After
recording `(-2, 0, 2)` from the first `0` and the last `2`, stepping `left`
by exactly one lands it on the second `0`, and `right` on the first `2`, and
the same triple comes out again. The suppression walks `left` past the
repeated `0`.

The **right-pointer skip after a match** is the mirror image, and it is the
one people leave out because the other two feel like enough. Leave it out and
a ledger with repeats on the *right* side of the pair emits duplicates in
exactly the same way.

**The `pin > 0` guard is not decoration.** `if ledger[pin] == ledger[pin - 1]`
on the very first iteration compares `ledger[0]` against `ledger[-1]`, the
*largest* amount in the sorted ledger. On `[3, 3, 3]` with a target of `9`
those are equal, so the only pin is skipped and the function returns `[]`
instead of `[(3, 3, 3)]`. Silently wrong, from a missing three-character
condition.

**The output is sorted for free, and that is a design choice worth
naming.** The pin walks the sorted ledger upward, so the first member of each
triple comes out ascending. Within one pin, `left` only ever moves upward, so
the second member ascends too. And each triple is built as
`(pin, left, right)` with `pin <= left <= right` by construction. So the
whole list is in ascending lexicographic order without a final sort.
Appending `results.sort()` at the end is not *wrong* — it costs `O(k log k)`
on `k` triples — but it tells an interviewer you did not reason about your
own loop order. Choosing a traversal so that a downstream requirement costs
nothing is a small, real piece of engineering.

**`sorted(amounts)` rather than `amounts.sort()`.** The second one rearranges
the treasurer's ledger behind their back. It happens to give the same
answer, and it happens to save `O(n)` space, and it is still a bug: the
caller handed you their chronological record and it is not yours to reorder.
The last assert in the self-check exists for no other reason. If you decide
the space matters more, that is a defensible call — but make it out loud and
document it, do not arrive at it by accident.

**Complexity, precisely.** Sorting is `O(n log n)`. The pin loop runs at most
`n - 2` times and each converging scan is `O(n)`, so the search is `O(n²)`
and dominates. Auxiliary space is `O(n)` for the sorted copy, plus the output
itself, which can hold `O(n²)` triples in the worst case and is a separate
line item from the working space. Then the sentence that earns the points:
**`O(n²)` is not obviously the floor here, but no better algorithm for this
problem is known, and a bound of 4,000 is calibrated to `O(n²)` — which tells
you the interviewer is not expecting better.**

## Download and run

Download
[challenge-01-settlement-trio-solution.py](./challenge-01-settlement-trio-solution.py)
and run it:

```bash
python challenge-01-settlement-trio-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-01-settlement-trio.py`.

## Common bugs to catch

- **A bare `AssertionError` on the unsorted ledger.** You forgot to sort:

  ```text
  Traceback (most recent call last):
      assert settlement_trios([-7, -3, -3, 10, 6], 0) == [(-7, -3, 10), (-3, -3, 6)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Converging pointers need a sorted tail — the whole steering rule is "the
  sum is too small, so reach for a bigger number, which is to the right."
  Without sortedness that sentence is false and the scan finds nothing. The
  function returned `[]`.

- **A bare `AssertionError` on the non-zero target.** You wrote
  `pair_target = -ledger[pin]`:

  ```text
  Traceback (most recent call last):
      assert settlement_trios([1, 3, 5, 7, 9], 15) == [(1, 5, 9), (3, 5, 7)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  That formula is right only when the balance is zero. It is
  `suspense - ledger[pin]`. Every example with a zero balance passes, which
  is exactly why the non-zero example is on this page.

- **A bare `AssertionError` on `[3, 3, 3]`.** You wrote the pin skip without
  the `pin > 0`:

  ```text
      [3, 3, 3] -> []
  ```

  ```text
  Traceback (most recent call last):
      assert settlement_trios([3, 3, 3], 9) == [(3, 3, 3)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  On the first iteration `ledger[pin - 1]` is `ledger[-1]`, the last and
  largest amount. When those happen to be equal — which is every ledger of
  identical amounts — the only pin is skipped and nothing is found.

- **Duplicate triples, with no exception at all.** You suppressed on the pin
  but not on the pointers:

  ```text
  [-2, -2, 0, 0, 2, 2] target 0 -> [(-2, 0, 2), (-2, 0, 2)]
  ```

  The correct answer is `[(-2, 0, 2)]`. Note that the examples on this page
  do **not** all catch this — `[-2, -2, 0, 2, 2, 4]` passes without the
  pointer suppressions, purely by luck of where the pointers land. Write the
  ledger above into your own tests.

- **A bare `AssertionError` because you sorted the caller's ledger.**

  ```text
      caller's ledger afterwards -> [-7, -3, -3, 6, 10]
  ```

  ```text
  Traceback (most recent call last):
      assert ledger == [-7, -3, -3, 10, 6]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `amounts.sort()` sorts in place and returns `None`. The answer you produced
  was right; the treasurer's chronological record is now gone.

- **Pinning all the way to the last position.** `range(len(ledger))` instead
  of `range(len(ledger) - 2)`. It does not raise — the inner `while left < right`
  simply never runs when the tail is too short — but it wastes two iterations
  and, worse, it means you did not notice that the `- 2` is also what makes
  the empty and two-entry ledgers work without a guard.

- **Sorting the output at the end because you did not trust the loop.** Not
  wrong, costs `O(k log k)`, and it is an admission. Trust the traversal
  after you have proved it, not before.

## Under the hood

<details>
<summary>Under the hood — why the pointer suppressions are subtle, and what four-of-something costs</summary>

**Why suppressing after a match is different from suppressing the pin.**

The pin suppression is a statement about *starting points*: two pins with the
same amount explore the same set of triples, so the second is redundant. It
is easy to see and easy to remember.

The pointer suppressions are a statement about what happens *inside* one
scan. After a match at `(left, right)`, both pointers must move — if only one
moved, the sum would change and the pair could never match again for the same
pin, so you would lose triples. But once both have moved, the new `left`
might carry the same amount as the old one, and the new `right` might carry
the same amount as the old one, and then the identical triple is found again.

The suppressions are written as `while` loops rather than single `if`s
because a ledger can hold many copies of the same amount. `[2] * 4000` with a
target of `6` would otherwise emit thousands of copies of `(2, 2, 2)`.

**Where the index-versus-amount distinction really bites.**

Count the *index* triples in `[-2, -2, 0, 2, 2, 4]` that sum to zero: one for
`(-2, -2, 4)` and four for `(-2, 0, 2)`, so five. Count the *amount* triples:
two. The gap between five and two is the entire problem, and it is why a
solution built by generating every index triple and then deduplicating with a
`set` — which does work, at `O(n³)` — is ruled out by the bound rather than
by being wrong.

**Four of something.**

The natural extension is two nested pins around the same converging scan:

```python
for first in range(len(ledger) - 3):
    if first > 0 and ledger[first] == ledger[first - 1]:
        continue
    for second in range(first + 1, len(ledger) - 2):
        if second > first + 1 and ledger[second] == ledger[second - 1]:
            continue
        # converging scan over ledger[second + 1:] for suspense - the two pins
```

`O(n³)`, and note the second pin's guard is `second > first + 1`, not
`second > 0` — the first entry of *this* pin's range is allowed to repeat the
outer pin's amount. That off-by-one is the classic mistake at this level, and
it is the same mistake as forgetting `pin > 0`, one layer deeper.

**Why sorting is free here and was forbidden in Exercise 3.**

Exercise 3 returns *positions*, and sorting destroys positions. This problem
returns *amounts*, so positions carry no information that survives into the
answer. Whenever you are about to sort, the question to ask out loud is not
"can I afford the time" but "does the answer depend on the order I am about
to destroy." Here it does not, and the `O(n log n)` disappears under the
`O(n²)` anyway.

**The hash-set alternative, and why it loses.**

Inside the pin loop you could scan the tail once with a set of complements
instead of converging pointers. Same `O(n²)` time. But it costs `O(n)` extra
space, and the deduplication becomes considerably fussier — a set finds
matches in arbitrary order, so you lose the free sorting *and* you have to
track which amount pairs you have already emitted. Name it in your write-up
and reject it for a stated reason, rather than not mentioning it at all.

</details>

## Acceptance checklist

- [ ] `python challenge-01-settlement-trio.py` prints `[(-2, -2, 4), (-2, 0, 2)]`, then `All checks passed.`
- [ ] The output is sorted ascending within each triple and across triples, with no final `sort()` call.
- [ ] All three duplicate suppressions are present, and you can name the ledger each one protects.
- [ ] The pin skip carries its `pin > 0` guard.
- [ ] `pair_target` is `suspense - ledger[pin]`, and there is no bare `0` anywhere in the function.
- [ ] `amounts` is unchanged after the call.
- [ ] `[-2, -2, 0, 0, 2, 2]` with a target of `0` returns exactly `[(-2, 0, 2)]`.
- [ ] You generated a ledger of a few thousand entries with heavy repetition and confirmed the runtime stayed flat.
- [ ] Your write-up explains why the natural traversal order already produces sorted output.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 1 challenge 1: settlement trio`.

**Practice elsewhere.** The same pattern appears as [LeetCode 15 · 3Sum](https://leetcode.com/problems/3sum/) if you want a judge to run against. Theirs fixes the target at zero and accepts the triples in any order, so it exercises neither the arbitrary target nor the output ordering — solve ours first.

## Stretch

- **Report how many ledger positions each explanation could be drawn from.**
  The board will want to know that `(-2, 0, 2)` has four possible sources and
  `(-2, -2, 4)` has one.

  ```python
  from collections import Counter
  from math import comb

  def trio_source_counts(amounts: list[int], suspense: int) -> list[tuple[tuple[int, int, int], int]]:
      """Pair each distinct trio with how many index triples produce it."""
      tally = Counter(amounts)
      out: list[tuple[tuple[int, int, int], int]] = []
      for trio in settlement_trios(amounts, suspense):
          a, b, c = trio
          if a == b == c:
              ways = comb(tally[a], 3)
          elif a == b:
              ways = comb(tally[a], 2) * tally[c]
          elif b == c:
              ways = tally[a] * comb(tally[b], 2)
          else:
              ways = tally[a] * tally[b] * tally[c]
          out.append((trio, ways))
      return out
  ```

  ```text
  [(-2, -2, 4), 1]
  [(-2, 0, 2), 4]
  ```

  Four branches, because "how many ways to choose three things" depends on
  how many of them are the same thing. Work out each branch before you read
  it; the combinatorics is the exercise, not the code.

- **Do it for four entries instead of three.** Two pins, one converging scan,
  `O(n³)`. Get the second pin's guard right — it is `second > first + 1`, and
  finding out why by breaking it first is worth more than being told.

- **Return index triples instead of amount triples.** Now sorting is
  forbidden and the whole approach has to change. Work out what it costs
  before you write a line, and say out loud which of the two contracts a real
  auditor would actually want.

Move on to [Challenge 2 — Ponding on the Levee Road](./challenge-02-levee-ponding.md).
