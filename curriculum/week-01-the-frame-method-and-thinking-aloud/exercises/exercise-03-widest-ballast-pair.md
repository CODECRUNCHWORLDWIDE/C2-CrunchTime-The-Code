# Exercise 3 — The Widest Ballast Pair

> **Topic:** converging pointers on a sorted row, steered by the running sum, returning *which* pair rather than *whether* one exists
> **Lecture:** [02 — The FRAME Method](../lecture-notes/02-the-frame-method.md)
> **Difficulty:** Easy/Medium
> **Target time:** 50 minutes, including a full FRAME narration out loud
> **Why this one:** Lecture 2 walks a simpler version of this problem — a yes-or-no. Here you must return **positions**, and choose a specific pair when several would do. That step, from "does one exist" to "which one," is where the pattern starts paying rent, because the choice rule turns out to be something the algorithm already gives you for free if you can see why.

Lecture 2 works the boolean version of this end to end. **Do not go back and
re-read it before you finish.** Re-derive it. The point is repetitions, not
novelty.

## The Brief

A river barge stows containers in a single row along the deck, position `0`
at the bow. The loading crane works from a manifest that is sorted by weight,
so the row is always in **non-decreasing** order — each container weighs the
same as or more than the one before it.

The barge is listing to one side. To correct it, the deckhands shift exactly
**two** containers across to the other side of the deck. The two weights have
to add up to exactly the correction figure the mate calculated. Not more, not
less — an over-correction just lists the barge the other way.

Often several pairs would work. The mate always picks the pair whose
positions are **furthest apart along the deck**. That is a real engineering
rule, not a tie-break invented to make the exercise harder: two containers
lifted from next to each other leave one wide hole in the middle of the
deck, which is the worst possible place to weaken a barge's back. Two lifted
from near the ends leave two small holes and the hull keeps its strength
along its length.

Return the two deck positions, **0-indexed**, in ascending order. If no pair
sums to the correction figure, return `None` — do not assume a solution
exists, because on a bad day there is not one and the mate re-ballasts with
water instead.

```python
def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Return (i, j) with i < j and weights[i] + weights[j] == correction, maximising j - i."""
```

**The tie-break is not really a tie-break, and you should be able to prove
that.** Suppose two different valid pairs `(i1, j1)` and `(i2, j2)` had
exactly the same span, with `i1 < i2`. Same span and a smaller left index
means `j1 < j2` as well. The row is sorted, so `weights[i1] <= weights[i2]`
and `weights[j1] <= weights[j2]`; and since both pairs sum to the same
figure, both of those have to be equalities. But then `(i1, j2)` also sums to
the figure, and its span is strictly larger than either. So a pair of equal
maximum span cannot exist: the widest pair is unique. Say that out loud.

## Starter

Save this as `exercise-03-widest-ballast-pair.py` and fill in the `TODO`s.

```python
"""exercise-03-widest-ballast-pair.py — the two containers to shift.

A sorted row of container weights, one correction figure, and a rule that
picks the pair standing furthest apart on the deck.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Find the furthest-apart pair of containers summing to the correction.

    Args:
        weights: Deck positions in non-decreasing weight order, kilograms.
        correction: The figure the two shifted containers must sum to.

    Returns:
        The pair of 0-indexed deck positions (i, j) with i < j, maximising
        j - i, or None when no pair sums to the correction figure.
    """
    # TODO: one pointer at the bow end, one at the stern end
    # TODO: add the two weights the pointers stand on. Too small? The only
    #       way to a bigger sum is a heavier left container, so move left up.
    #       Too big? Move right down. Exactly right? That is the answer.
    # TODO: when the pointers meet, no pair exists
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(widest_ballast_pair([120, 340, 500, 660, 880], 1000))

    assert widest_ballast_pair([-400, -100, 0, 100, 300], 0) == (1, 3)
    assert widest_ballast_pair([100, 100, 100, 100], 200) == (0, 3)
    assert widest_ballast_pair([10, 20, 30], 100) is None
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/exercise-03-widest-ballast-pair.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `widest_ballast_pair` returns a `tuple[int, int]` of **0-indexed** deck
   positions in ascending order, or `None`.
2. The two positions are distinct. A container cannot pair with itself.
3. Among all valid pairs, the one returned has the largest `j - i`.
4. `None` — not `[]`, not `(-1, -1)` — is returned when no pair sums to the
   correction figure.
5. The function does not modify `weights`.
6. The function runs in `O(n)` time and `O(1)` auxiliary space.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(weights) <= 1_000_000`.** A million containers is more than any
  barge on any river carries. The bound is chosen so that the obvious
  `O(n²)` answer — check every pair against every other pair — comes to
  roughly `5 × 10¹¹` operations and cannot finish. The constraint is
  therefore the hint: read it, and say out loud what it rules out, before you
  plan anything.

- **`weights` is guaranteed non-decreasing.** Sortedness is the entire reason
  converging pointers apply. If you had to sort it yourself you would pay
  `O(n log n)` *and* scramble the deck positions, which are the thing you
  have to return — so you would need to tag every weight with its original
  position first. Name that alternative and say why it loses here.

- **`-50_000 <= weights[i] <= 500_000`, in kilograms.** Negative readings are
  real: an empty cradle weighs less than the load cell's tare, so it reports
  a negative number. This bound exists to kill one specific "optimisation" —
  skipping any container heavier than the correction figure. A heavy
  container can still pair with a negative one, and the second example below
  is built to catch exactly that.

- **`correction` is any integer that two weights in that range could sum
  to.** It is the mate's arithmetic, not a promise that an answer exists.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-03-widest-ballast-pair-solution.py
correction  1000  pair (0, 4) span 4  [120, 340, 500, 660, 880]
correction     0  pair (1, 3) span 2  [-400, -100, 0, 100, 300]
correction   200  pair (0, 3) span 3  [100, 100, 100, 100]
correction  1000  pair (0, 3) span 3  [200, 200, 800, 800]
correction   300  pair (0, 1) span 1  [150, 150]
correction   300  no pair            [150]
correction     0  no pair            []
correction   100  no pair            [10, 20, 30]
All checks passed.
```

Line by line, the four that teach something.

**Line 1.** Two pairs work: `120 + 880` at `(0, 4)`, span 4, and `340 + 660`
at `(1, 3)`, span 2. The wider one wins. This line exists to make you
*check* the selection rule instead of returning the first pair you stumble
across.

**Line 2.** This is the example that punishes assuming the answer is the two
ends. `weights[0] + weights[4]` is `-100`, not `0`. The only valid pair is
`-100 + 100`, at span 2. It is also the negative-weight example: anything
that skips containers heavier than the correction figure never even looks at
position 1.

**Line 3.** Six pairs are valid, and every one of them sums to 200. This is
the example that punishes the hash-map habit — a one-pass "have I already
seen the complement" map hands back `(0, 1)`, which is correct arithmetic and
the wrong pair. Converging pointers get the widest for free, and the
explanation below says why.

**Line 8.** No pair reaches 100. The pointers cross, the loop ends, and
`None` comes back. The mate reaches for the water ballast.

## Steps

1. Save the starter and run it. `AssertionError`.
2. Put `left` at `0` and `right` at `len(weights) - 1`. Loop
   `while left < right`.
3. Compute `total = weights[left] + weights[right]`.
4. Three cases, in this order. Equal to the correction: return
   `(left, right)`. Less than it: the sum is too small, and because the row
   ascends the only way to grow it is a heavier left container, so
   `left += 1`. Greater: `right -= 1`.
5. After the loop, return `None`.
6. Run it. Then trace `[100, 100, 100, 100]` with `200` and write down the
   span at every step. You should see `3` on the very first iteration, which
   is the whole argument for why the first match is the widest.
7. Trace `[-400, -100, 0, 100, 300]` with `0` and watch the pointers walk
   past the outermost pair.

## The Solution

```python
"""exercise-03-widest-ballast-pair-solution.py — the two containers to shift.

A sorted row of container weights, one correction figure, and a rule that
picks the pair standing furthest apart on the deck. Converging pointers
examine pairs in strictly decreasing order of span, so the first match they
find is already the widest.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Find the furthest-apart pair of containers summing to the correction.

    Args:
        weights: Deck positions in non-decreasing weight order, kilograms.
        correction: The figure the two shifted containers must sum to.

    Returns:
        The pair of 0-indexed deck positions (i, j) with i < j, maximising
        j - i, or None when no pair sums to the correction figure.
    """
    left, right = 0, len(weights) - 1
    while left < right:
        total = weights[left] + weights[right]
        if total == correction:
            return (left, right)
        if total < correction:
            left += 1
        else:
            right -= 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    manifests = [
        ([120, 340, 500, 660, 880], 1000),
        ([-400, -100, 0, 100, 300], 0),
        ([100, 100, 100, 100], 200),
        ([200, 200, 800, 800], 1000),
        ([150, 150], 300),
        ([150], 300),
        ([], 0),
        ([10, 20, 30], 100),
    ]
    for weights, correction in manifests:
        pair = widest_ballast_pair(weights, correction)
        if pair is None:
            print(f"correction {correction:>5}  no pair            {weights}")
        else:
            i, j = pair
            print(f"correction {correction:>5}  pair {pair} span {j - i}  {weights}")

    assert widest_ballast_pair([120, 340, 500, 660, 880], 1000) == (0, 4)
    assert widest_ballast_pair([-400, -100, 0, 100, 300], 0) == (1, 3)
    assert widest_ballast_pair([100, 100, 100, 100], 200) == (0, 3)
    assert widest_ballast_pair([200, 200, 800, 800], 1000) == (0, 3)
    assert widest_ballast_pair([150, 150], 300) == (0, 1)
    assert widest_ballast_pair([150], 300) is None
    assert widest_ballast_pair([], 0) is None
    assert widest_ballast_pair([10, 20, 30], 100) is None
    print("All checks passed.")
```

**The span shrinks by exactly one every iteration, and that is the whole
answer to "why the widest?"** Look at the loop body: every path through it
either returns, or moves `left` up one, or moves `right` down one. Never
both, never more. So `right - left` goes `n-1`, `n-2`, `n-3`, … and the
algorithm therefore examines candidate pairs in **strictly decreasing order
of span**. The first pair it finds that sums correctly is, by construction,
the widest pair that does. There is no extra bookkeeping, no `best` variable,
no comparison — the traversal order *is* the selection rule. This is the
sentence most candidates cannot produce, and it is the one that turns "my
code passes" into "I know why my code is right."

**The steering rule leans entirely on sortedness.** When the total is too
small, you need a bigger number. The row ascends, so a bigger number is to
the *right* of `left` — moving `left` up is the only move that can raise the
sum without also throwing away a container you might still want. Symmetric on
the other side. Take sortedness away and the rule is meaningless, which is
why "is it sorted?" is the first question to ask about a problem like this.

**Nothing is discarded that could have mattered.** When you move `left` past
position `i`, you are claiming that no pair involving `i` can work. That is
true, and here is the argument: `weights[i] + weights[right]` was already too
small, and `weights[right]` is the *largest* weight still in play, so every
remaining partner for `i` is smaller still. Say that when an interviewer asks
whether you might be skipping the answer.

**`while left < right`, strictly.** With `<=` the pointers can land on the
same container and pair it with itself. On `[240]` with a correction of
`480`, that returns `(0, 0)` — one container doing the work of two, which is
not a thing a crane can lift.

**`None`, not a falsy tuple.** `return ()` or `return []` collides with a
caller writing `if result:` — and `(0, 4)` is a perfectly good truthy answer,
so the caller cannot tell the two apart. `None` is the value that means
"there is no answer" and cannot be mistaken for one.

**The empty and single-container rows need no special case.** With `[]`,
`right` starts at `-1` and `0 < -1` is false, so the loop never runs and
`None` comes back. With one container, `right` is `0` and `0 < 0` is false,
same story. That is correct **by construction**, not by luck — and saying
which of the two it is, out loud, is the difference between judgement and
getting away with it.

## Download and run

Download
[exercise-03-widest-ballast-pair-solution.py](./exercise-03-widest-ballast-pair-solution.py)
and run it:

```bash
python exercise-03-widest-ballast-pair-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-03-widest-ballast-pair.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the first line of the loop.**
  You initialised `right = len(weights)`:

  ```text
  Traceback (most recent call last):
      widest_ballast_pair([120, 340, 500, 660, 880], 1000)
      total = weights[left] + weights[right]
                              ~~~~~~~^^^^^^^
  IndexError: list index out of range
  ```

  Five containers occupy positions `0` through `4`. `len(weights)` is `5`,
  which is one past the last one. The last valid index is always
  `len(...) - 1`.

- **`TypeError: cannot unpack non-iterable NoneType object`.** You advanced
  the wrong pointer — `right -= 1` when the total was too small — and the
  function returned `None`, which the caller then tried to unpack:

  ```text
  Traceback (most recent call last):
      i, j = widest_ballast_pair([-400, -100, 0, 100, 300], 0)
      ^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  Nothing crashed inside the function. It ran to completion, crossed the
  pointers, and honestly reported that it had found nothing — because with
  the moves reversed it walks away from every candidate. The exception
  happens one level up, at the caller, which is why the message names
  unpacking rather than pointers.

- **A bare `AssertionError` with a pair that looks nearly right.** You added
  one to both indexes:

  ```text
  Traceback (most recent call last):
      assert widest_ballast_pair([120, 340, 500, 660, 880], 1000) == (0, 4)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  You returned `(1, 5)`. This contract is 0-indexed and says so. Adding `+1`
  because a problem you once saw somewhere else was 1-indexed is exactly the
  recall failure this course exists to prevent — you answered a question
  nobody asked.

- **Returning the weights instead of the positions.** `(120, 880)` instead of
  `(0, 4)`. Both are pairs of integers, so nothing raises, and on a row where
  the weights happen to be small the two can even look interchangeable. Read
  the signature.

- **Reaching for a hash map.** It is the right instinct on an *unsorted* row
  and the wrong one here. It costs `O(n)` space you do not need, and it finds
  *a* pair rather than the widest — on `[100, 100, 100, 100]` with `200` it
  returns `(0, 1)`. To honour the contract you would have to keep scanning
  and track the best span yourself, which is more code doing more work than
  the pointers do for free.

- **`while left <= right`.** Lets a container pair with itself when the
  pointers meet. On `[150]` with `300` it returns `(0, 0)`.

- **Tracking a `best` span "just to be safe".** No exception, correct answer,
  and it tells the interviewer you did not understand your own loop. If you
  find yourself adding a `best` variable here, stop and re-derive the
  span-decreases-by-one argument until you trust it.

## Under the hood

<details>
<summary>Under the hood — what the pointers prove, and what changes when the row is not sorted</summary>

**The correctness argument in full.**

Call a pair *valid* if it sums to the correction figure. Claim: if any valid
pair exists, the loop returns the one with the largest span.

The loop maintains an invariant: **every valid pair not yet examined lies
entirely inside the window `[left, right]`.** It holds at the start, because
the window is the whole row. It survives one iteration: if the total was too
small, then for every `j <= right`, `weights[left] + weights[j] <= weights[left] + weights[right] < correction`,
so no pair using `left` can be valid, and discarding `left` discards nothing
valid. The other branch is symmetric.

Combine that with the span observation — the span drops by exactly one per
iteration, so the loop enumerates candidate spans downward from `n-1` — and
you have both halves. Nothing valid is discarded, and spans are tried
largest first, so the first valid pair found is the widest one that exists.

**What the loop does *not* do.**

It does not examine every valid pair. On `[100, 100, 100, 100]` with `200`
there are six valid pairs and the loop looks at exactly one. That is the
efficiency, and it is also the limitation: if the mate had asked for the
*narrowest* pair instead, this loop could not answer, because it never sees
the narrow ones. That question needs a different algorithm, and working out
which is a genuinely good use of twenty minutes.

**The unsorted case, priced honestly.**

If the row arrived in loading order rather than weight order you have three
options.

*Sort it yourself.* `O(n log n)`, and it scrambles the deck positions — which
are the answer. You would have to sort `(weight, position)` pairs and read
the positions back out, which also costs `O(n)` space for the tagged list.

*Hash map on the complement.* One pass; for each weight, ask whether
`correction - weight` has been seen and where. `O(n)` time, `O(n)` space, and
it preserves positions. This is the right answer for an unsorted row, and it
is Week 2's material.

*Nested scan.* `O(n²)`, no extra space, and ruled out by the million-container
bound.

Sortedness is worth roughly a factor of `n` in space here. That is why "is
the input sorted?" belongs in Frame, before you have committed to anything.

**Why `O(n)` is the floor.**

The answer can involve the very last container in the row — line 1 of the
expected output is exactly that case — so any correct algorithm has to be
prepared to read the whole row. You cannot beat linear, and the two-pointer
version achieves it with three integers of state.

</details>

## Acceptance checklist

- [ ] `python exercise-03-widest-ballast-pair.py` prints `(0, 4)`, then `All checks passed.`
- [ ] The returned positions are 0-indexed and ascending.
- [ ] `None` is returned for the no-pair cases, including the empty row.
- [ ] There is no `best` variable anywhere in your loop, and you can say why one is not needed.
- [ ] You can state the span-decreases-by-one argument in your own words, without reading it off this page.
- [ ] You can state why moving `left` past a container discards nothing valid.
- [ ] `weights` is unchanged after the call.
- [ ] The function has type hints and a docstring.
- [ ] You narrated a full FRAME pass out loud with a recorder running, at least ten minutes.
- [ ] Committed to Git with a message like `Add Week 1 exercise 3: widest ballast pair`.
## Stretch

- **Return every valid pair, not just the widest.**

  ```python
  def all_ballast_pairs(weights: list[int], correction: int) -> list[tuple[int, int]]:
      """Return every (i, j) with i < j summing to correction, widest span first."""
      pairs: list[tuple[int, int]] = []
      left, right = 0, len(weights) - 1
      while left < right:
          total = weights[left] + weights[right]
          if total < correction:
              left += 1
          elif total > correction:
              right -= 1
          else:
              pairs.append((left, right))
              left += 1
              right -= 1
      return pairs
  ```

  ```text
  [120, 340, 500, 660, 880] target 1000 -> [(0, 4), (1, 3)]
  [100, 100, 100, 100] target 200 -> [(0, 3), (1, 2)]
  ```

  Look at the second line. Six pairs are valid and this returns two. The
  pointers step past four of them, because after a match both pointers move
  and the pairs that used only one of those two positions are gone. Work out
  which four are missing and why before you decide whether this function is
  correct — the answer depends on what "every valid pair" was supposed to
  mean, and that is a specification question, not a coding one.

- **Answer the narrowest-pair question.** Same input, but the mate now wants
  the two containers standing *closest* together. Try to adapt the loop, fail,
  and work out precisely why it cannot be adapted. Then design something that
  can. This is harder than it looks and it is the best twenty minutes on this
  page.

- **Handle an unsorted row without losing the positions.** Write the
  hash-map version, state its time and space, and say in one sentence which
  of the two you would ship if the manifest's sortedness were merely usually
  true rather than guaranteed.

When your ballast pair is right, move on to
[Exercise 4 — The Stuck Gauge](./exercise-04-stuck-gauge.md).
