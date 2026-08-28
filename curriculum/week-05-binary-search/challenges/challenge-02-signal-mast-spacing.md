# Challenge 2 — The Signal Mast Spacing

> **Topic:** binary search on the answer in the **maximise-the-minimum** direction, with a greedy placement as the predicate and the placement itself as part of the answer
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Hard
> **Target time:** 60 minutes the first time, 30 on a revisit
> **Why this one:** Exercise 5 searched downwards for the smallest reach that still worked. This one searches upwards for the largest spacing that still fits, and that flip changes three things at once — which branch keeps the midpoint, which way the midpoint rounds, and where the loop can spin forever. Getting all three right, and being able to say why each is what it is, is the week's second big skill.

## The Brief

A rail operator is bolting radio masts onto trackside posts. The posts are
already there — a survey has measured each one's distance from the yard in
metres — and a mast can only go on a post. Posts are listed in order, and no
two share a position.

Radios interfere when they are close together, so the operator wants the masts
**spread out**. Specifically: whatever pair of masts ends up closest together,
make *that* distance as large as possible.

```
posts:  0    4    9    13         25         31
        |    |    |    |          |          |

three masts on 0, 13, 31  ->  gaps 13 and 18  ->  the closest pair is 13m apart
three masts on 0, 13, 25  ->  gaps 13 and 12  ->  the closest pair is 12m apart
three masts on 0,  9, 25  ->  gaps  9 and 16  ->  the closest pair is  9m apart
```

The first arrangement is the best of those three, and in fact no arrangement
of three masts on those posts does better than 13. So the answer for three
masts is `13`.

Now think about what happens as you *demand* more spacing. Ask for at least 10
metres between masts and three masts fit easily. Ask for 13 and they still
fit — just. Ask for 14 and they do not fit at all.

```
required spacing:   1    ...   12    13    14    15   ...
three masts fit?   yes   ...  yes   yes    no    no   ...
```

One flip, in one place, and the last "yes" is the answer. That is a binary
search — but it runs the other way round from Exercise 5. There you wanted the
first "yes" in a run of "no"s; here you want the **last** "yes" before the
"no"s begin.

Testing a demanded spacing is a single walk down the line. Put a mast on the
first post — you may as well, since starting anywhere else only wastes room —
then walk right and plant a mast on the first post that is far enough from the
last one you planted. If you run out of posts before you run out of masts, the
demanded spacing was too greedy.

Return **both** the spacing and the placement: `(spacing, chosen_posts)`,
where `chosen_posts` is the list of positions that walk selects at the winning
spacing. Several placements can tie at the best spacing, so the contract names
one: the leftmost-greedy walk described above, which always starts at
`posts[0]`.

Three contract decisions:

- **Fewer than two masts returns `None`.** A spacing is a distance between two
  masts. With one mast, or none, there is no pair and therefore no question.
  Not `0` — zero is a real answer to a different question.
- **More masts than posts returns `None`.** They will not fit; a mast needs its
  own post.
- **An empty post line returns `None`**, by the same rule as the first two.

## Starter

Save this as `challenge-02-signal-mast-spacing.py` and fill in every `TODO`.

```python
"""challenge-02-signal-mast-spacing.py — the widest signal spacing.

Binary search on the ANSWER, maximise-the-minimum direction, with a greedy
placement sweep as the predicate.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

import random
from itertools import combinations

# ---- Given data ----
POSTS: list[int] = [0, 4, 9, 13, 25, 31]


# ---- Your task ----
def place_masts(posts: list[int], spacing: int, masts: int) -> list[int] | None:
    """Plant masts left to right, never closer together than `spacing`.

    Args:
        posts: Post positions in metres, ascending and distinct, not empty.
        spacing: The minimum distance to keep between two masts.
        masts: How many masts must be planted.

    Returns:
        The chosen post positions when all `masts` fit, otherwise None.
    """
    # TODO: always start on posts[0]
    # TODO: plant on the first post at least `spacing` from the last one planted
    # TODO: return None when you run out of posts before running out of masts
    ...


def mast_spacing(posts: list[int], masts: int) -> tuple[int, list[int]] | None:
    """Return the widest guaranteed spacing and the placement that achieves it.

    Args:
        posts: Post positions in metres, ascending and distinct.
        masts: How many masts the operator is bolting on.

    Returns:
        (spacing, chosen) where spacing is the largest achievable value of the
        smallest distance between two masts, and chosen is the leftmost-greedy
        placement at that spacing. None when masts < 2 or masts > len(posts).
    """
    # TODO: the contract branches first — fewer than two masts, more than posts
    # TODO: lo = 1, hi = (posts[-1] - posts[0]) // (masts - 1). Why is hi enough?
    # TODO: this is a LAST-yes search: lo = mid on success, hi = mid - 1 on failure
    # TODO: which means mid must round UP. Work out what happens if it does not.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"posts: {POSTS}")
    for count in (2, 3, 6, 7):
        print(f"{count} masts -> {mast_spacing(POSTS, count)}")

    assert mast_spacing(POSTS, 2) == (31, [0, 31])
    assert mast_spacing(POSTS, 3) == (13, [0, 13, 31])
    assert mast_spacing(POSTS, 6) == (4, [0, 4, 9, 13, 25, 31])
    assert mast_spacing(POSTS, 7) is None
    assert mast_spacing(POSTS, 1) is None
    assert mast_spacing(POSTS, 0) is None
    assert mast_spacing([], 2) is None
    assert mast_spacing([5, 6], 2) == (1, [5, 6])
    assert mast_spacing([0, 3, 4, 7, 10], 3) == (4, [0, 4, 10])
    assert mast_spacing([0, 5, 6, 11], 3) == (5, [0, 5, 11])
    assert POSTS[0] == 0  # the survey was never rearranged

    rng = random.Random(20250505)
    lines = 0
    for _ in range(300):
        line = sorted(rng.sample(range(0, 60), rng.randrange(2, 8)))
        for count in range(2, len(line) + 1):
            best = max(
                min(b - a for a, b in zip(pick, pick[1:]))
                for pick in combinations(line, count)
            )
            spacing, chosen = mast_spacing(line, count)
            assert spacing == best, (line, count, spacing, best)
            assert min(b - a for a, b in zip(chosen, chosen[1:])) >= best
        lines += 1
    print(f"cross-checked {lines} generated post lines against every choice of posts")
    print("All checks passed.")
```

Two ideas you need before you start.

**Last-yes searching.** Exercise 5 looked for the first `True` in
`False … False True … True`. Here the run is the other way round —
`True … True False … False` — and you want the last `True`. Same bisection,
mirrored: keep the midpoint when it succeeds (`lo = mid`), discard it when it
fails (`hi = mid - 1`).

**Rounding the midpoint up.** The moment one branch is `lo = mid`, the plain
midpoint becomes dangerous. With `lo = 4, hi = 5`, the ordinary
`lo + (hi - lo) // 2` gives `4`, and if the test succeeds you set `lo = 4` —
which changes nothing, and the loop runs forever. Rounding up,
`lo + (hi - lo + 1) // 2`, gives `5` and the interval always shrinks. The rule
is mechanical: **whichever branch keeps `mid`, round away from it.**

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/challenges/challenge-02-signal-mast-spacing.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `place_masts(posts, spacing, masts)` returns the chosen positions when the
   masts fit at that spacing, and `None` when they do not.
2. It always plants the first mast on `posts[0]`, and it is one pass over the
   posts — no nested loop, no re-scanning.
3. `mast_spacing(posts, masts)` returns `(spacing, chosen)`, where `spacing` is
   the largest achievable minimum gap.
4. `chosen` is the leftmost-greedy placement at that spacing, ascending, with
   exactly `masts` entries.
5. It returns `None` when `masts < 2` or `masts > len(posts)`, including for
   the empty post line.
6. The search interval is `lo = 1` to `hi = (posts[-1] - posts[0]) // (masts -
   1)`, and you can prove that upper bound.
7. The search keeps `mid` on success and rounds `mid` up. No `while True`, no
   iteration cap, no other escape hatch.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(posts) <= 200_000`.** A long branch line surveyed post by post.
  The predicate is one walk, so the whole search is `O(n log S)` where `S` is
  the span. Anything that re-walks per mast is `O(n²)` per test and will not
  finish.

- **`0 <= posts[i] <= 10**9`, ascending and distinct.** A billion-metre span
  means the answer interval is about a billion wide — thirty halvings, not
  five — and it is what rejects trying every spacing from 1 upwards.
  Distinctness matters for a specific reason: it guarantees that a demanded
  spacing of `1` always succeeds when there are enough posts, so the bottom of
  the interval is never itself infeasible. Allow two posts at the same
  position and that guarantee dies.

- **`0 <= masts <= 200_000`.** Mast counts of 0 and 1 are legal input, and so
  are counts above the post count. All three return `None`, and none of them
  may raise. Note that `masts - 1` appears in the upper bound, which is a
  division — so the `masts < 2` branch has to run before it.

- **Choosing the posts is not a search over combinations.** Picking `masts`
  posts out of 200,000 is a number with tens of thousands of digits. The whole
  point of bisecting the *answer* is that you never enumerate arrangements at
  all; you only ever ask one yes/no question about a candidate spacing.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-signal-mast-spacing.py
posts: [0, 4, 9, 13, 25, 31]
2 masts -> (31, [0, 31])
3 masts -> (13, [0, 13, 31])
6 masts -> (4, [0, 4, 9, 13, 25, 31])
7 masts -> None
cross-checked 300 generated post lines against every choice of posts
All checks passed.
```

The six-mast row is the floor of the problem: with a mast on every post, the
closest pair is whichever two posts are nearest each other, and no choice you
make can change that. The cross-check line is the important one — it re-solves
three hundred generated post lines by trying **every** combination of posts
and comparing. That is the proof that the greedy walk really does find the
optimum, and not merely a good arrangement.

## Steps

1. Save the starter and run it. `mast_spacing` returns `Ellipsis`, so the
   first `print` shows it and the first assert fails. Expected.
2. Write `place_masts` first and test it alone on the sample posts: at spacing
   `13` with three masts it should give `[0, 13, 31]`; at `14` it should give
   `None`.
3. Check the walk is one pass. The only loop is over `posts`, and the only
   state is the list of chosen positions. If you find yourself starting the
   walk again for a different first post, stop — the greedy start is provably
   safe, and the Under the hood block says why.
4. Now the contract branches: `masts < 2` and `masts > len(posts)` both return
   `None`. The first must come before anything divides by `masts - 1`.
5. Set the interval. `lo = 1`, because posts are distinct so a one-metre demand
   always succeeds. `hi = (posts[-1] - posts[0]) // (masts - 1)`, because
   `masts` masts have `masts - 1` gaps between them and those gaps have to fit
   inside the span, so no spacing wider than the average can work.
6. Write the loop: `while lo < hi`, round `mid` **up**, `lo = mid` when the
   masts fit, `hi = mid - 1` when they do not.
7. After the loop, run the walk once more at `lo` to produce the placement, and
   return both.
8. Trace `masts = 3` by hand and compare against the trace in The Solution.
   Then deliberately write the midpoint without the round-up, run it, and
   press `Ctrl-C` — meeting that hang once is worth more than reading about
   it.

## The Solution

```python
"""challenge-02-signal-mast-spacing-solution.py - the widest signal spacing.

Binary search on the ANSWER, in the maximise-the-minimum direction. The
predicate is a greedy placement sweep: at a trial spacing, plant a mast on
the first post and then on every post far enough from the last one planted.

The self-checks at the bottom are the starter's, unchanged. The last one
cross-checks the search against every possible choice of posts on small
lines. When they all pass the file prints "All checks passed."
"""

import random
from itertools import combinations

# ---- Given data ----
POSTS: list[int] = [0, 4, 9, 13, 25, 31]


# ---- Your task ----
def place_masts(posts: list[int], spacing: int, masts: int) -> list[int] | None:
    """Plant masts left to right, never closer together than `spacing`.

    Args:
        posts: Post positions in metres, ascending and distinct, not empty.
        spacing: The minimum distance to keep between two masts.
        masts: How many masts must be planted.

    Returns:
        The chosen post positions when all `masts` fit, otherwise None.
    """
    chosen = [posts[0]]
    for post in posts[1:]:
        if len(chosen) == masts:
            break
        if post - chosen[-1] >= spacing:
            chosen.append(post)
    return chosen if len(chosen) == masts else None


def mast_spacing(posts: list[int], masts: int) -> tuple[int, list[int]] | None:
    """Return the widest guaranteed spacing and the placement that achieves it.

    Args:
        posts: Post positions in metres, ascending and distinct.
        masts: How many masts the operator is bolting on.

    Returns:
        (spacing, chosen) where spacing is the largest achievable value of the
        smallest distance between two masts, and chosen is the leftmost-greedy
        placement at that spacing. None when masts < 2 or masts > len(posts).
    """
    if masts < 2 or masts > len(posts):
        return None

    lo, hi = 1, (posts[-1] - posts[0]) // (masts - 1)
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # round up, or lo == mid spins forever
        if place_masts(posts, mid, masts) is not None:
            lo = mid  # mid works, so the answer is mid or wider
        else:
            hi = mid - 1  # mid is too wide, so the answer is narrower
    chosen = place_masts(posts, lo, masts)
    assert chosen is not None  # lo == 1 always fits: the posts are distinct
    return lo, chosen


# ---- Self-check ----
if __name__ == "__main__":
    print(f"posts: {POSTS}")
    for count in (2, 3, 6, 7):
        print(f"{count} masts -> {mast_spacing(POSTS, count)}")

    assert mast_spacing(POSTS, 2) == (31, [0, 31])
    assert mast_spacing(POSTS, 3) == (13, [0, 13, 31])
    assert mast_spacing(POSTS, 6) == (4, [0, 4, 9, 13, 25, 31])
    assert mast_spacing(POSTS, 7) is None
    assert mast_spacing(POSTS, 1) is None
    assert mast_spacing(POSTS, 0) is None
    assert mast_spacing([], 2) is None
    assert mast_spacing([5, 6], 2) == (1, [5, 6])
    assert mast_spacing([0, 3, 4, 7, 10], 3) == (4, [0, 4, 10])
    assert mast_spacing([0, 5, 6, 11], 3) == (5, [0, 5, 11])
    assert POSTS[0] == 0  # the survey was never rearranged

    rng = random.Random(20250505)
    lines = 0
    for _ in range(300):
        line = sorted(rng.sample(range(0, 60), rng.randrange(2, 8)))
        for count in range(2, len(line) + 1):
            best = max(
                min(b - a for a, b in zip(pick, pick[1:]))
                for pick in combinations(line, count)
            )
            spacing, chosen = mast_spacing(line, count)
            assert spacing == best, (line, count, spacing, best)
            assert min(b - a for a, b in zip(chosen, chosen[1:])) >= best
        lines += 1
    print(f"cross-checked {lines} generated post lines against every choice of posts")
    print("All checks passed.")
```

**Say the reframe out loud, in four parts.** Same cadence as Exercise 5, with
the direction flipped:

> *Reframe:* find the **largest** spacing `s` such that `masts` masts can be
> planted on these posts with no two closer than `s`.
> *Interval:* `lo = 1`, because the posts are distinct so a demand of one
> metre always succeeds; `hi = span // (masts - 1)`, because `masts` masts have
> `masts - 1` gaps and all of them must fit inside the span, so nothing wider
> than the average gap can work.
> *Predicate:* the greedy walk plants all `masts` masts. Monotone downwards in
> `s`, because narrowing the demand never removes a placement that already
> satisfied a wider one.
> *Return:* the post-loop `lo`, the last spacing at which the walk succeeded.

**Why greedy is optimal, and not merely reasonable.** Two claims, and the
second is the one people skip. First, starting on `posts[0]` never hurts:
given any valid arrangement, sliding its leftmost mast down to `posts[0]` only
increases the gap to the next one. Second, having planted a mast, taking the
*earliest* legal next post never hurts either: any arrangement that skipped it
can have that mast slid left onto the earlier post, which widens the gap
behind and does not narrow the gap ahead by more than the arrangement already
allowed. So the greedy walk fits whenever anything fits — and the cross-check
at the bottom of the file tests exactly that claim against every combination
on three hundred generated lines.

**The upper bound is proved, not guessed.** `masts` masts sit in a line with
`masts - 1` gaps between them, and the whole arrangement fits inside
`posts[-1] - posts[0]` metres. If every gap were wider than
`span // (masts - 1)`, the gaps would add up to more than the span. So the
answer can never exceed that value — and the tighter the bound you can prove,
the fewer iterations you pay for.

**The round-up midpoint is not a style choice; it is the termination
argument.** With `lo = mid` in one branch, an ordinary midpoint can equal `lo`
whenever the interval is two wide, and then a successful test changes nothing.
Rounding up guarantees `mid > lo`, so every iteration moves at least one end.
The general rule, worth writing on a card: *the branch that keeps `mid` is the
branch that decides which way `mid` rounds — always round away from the
keeping side.*

**Trace `masts = 3` on the sample posts.** Span is `31 - 0 = 31`, so
`hi = 31 // 2 = 15`, and `lo = 1`.

| `lo` | `hi` | `mid` (rounded up) | greedy walk | fits? | move |
| ---: | ---: | ---: | :--- | :--- | :--- |
| 1 | 15 | 8 | `0, 9, 25` | yes | `lo = 8` |
| 8 | 15 | 12 | `0, 13, 25` | yes | `lo = 12` |
| 12 | 15 | 14 | `0, 25` only | no | `hi = 13` |
| 12 | 13 | 13 | `0, 13, 31` | yes | `lo = 13` |

`lo == hi == 13`. One more walk at 13 produces `[0, 13, 31]`, and the answer
is `(13, [0, 13, 31])`. Notice the third row: at a demand of 14 the walk
plants on 0, skips 4, 9 and 13 as too close, lands on 25 — and then 31 is only
6 metres further, so the third mast has nowhere to go.

**Returning the placement is what stops this being a remembered answer.** The
number alone would let you stop as soon as the loop exits. Returning the
positions forces one more run of the predicate at the winning spacing, and it
forces the contract to say *which* placement, because several can tie. `[0, 5,
11]` and `[0, 6, 11]` both achieve a minimum gap of 5 on `[0, 5, 6, 11]`; the
contract picks the first because the greedy walk is defined to take the
earliest legal post. Ambiguity in a return value is a bug in the specification,
not a detail to leave to the implementation.

**The `masts < 2` branch runs before the bound is computed.** `masts - 1` is a
divisor. With one mast that is a division by zero, and with zero masts it is
negative. Ordering the guards is the fix; there is nothing clever to do.

**`lo = 1` is safe because the posts are distinct.** Every pair of adjacent
posts is at least one metre apart, so a demand of one metre plants a mast on
every post in turn — which is why the walk at `lo` can never fail and the
`assert` at the end never fires. Say that out loud rather than assuming it:
the assertion is documentation of a proof, not a runtime check you are hoping
about.

## Download and run

Download
[challenge-02-signal-mast-spacing-solution.py](./challenge-02-signal-mast-spacing-solution.py)
and run it:

```bash
python challenge-02-signal-mast-spacing-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-02-signal-mast-spacing.py`.

## Common bugs to catch

- **The program hangs and prints nothing after the first row.** You used the
  ordinary midpoint with `lo = mid`. Press `Ctrl-C` and Python points straight
  at the guard:

  ```text
  Traceback (most recent call last):
    File "<string>", line 7, in <module>
      while lo <= hi:
            ^^^^^^^^
  KeyboardInterrupt
  ```

  With `lo = 12, hi = 13`, the plain midpoint is `12`; the walk succeeds; you
  set `lo = 12`, which it already was. Round the midpoint up.

- **`ZeroDivisionError: integer division or modulo by zero`.** You computed the
  upper bound before checking the mast count:

  ```text
  Traceback (most recent call last):
      lo, hi = 1, (posts[-1] - posts[0]) // (masts - 1)
                  ~~~~~~~~~~~~~~~~~~~~~~~^^~~~~~~~~~~~~
  ZeroDivisionError: integer division or modulo by zero
  ```

  One mast means zero gaps. The `masts < 2` guard is not politeness; it is what
  makes the divisor safe.

- **`IndexError: list index out of range` on the empty post line.** Same
  ordering problem, one step earlier — `posts[-1]` on an empty list. The
  `masts > len(posts)` guard catches it, because zero posts cannot hold two
  masts, so that guard has to run before any indexing.

- **`mast_spacing(POSTS, 3)` returns `12` instead of `13`.** You wrote
  `hi = mid` on failure instead of `hi = mid - 1`, or `lo = mid + 1` on
  success. In a last-yes search the successful midpoint is a candidate and must
  be kept; the failing one is not and must be excluded. Mixing the two shapes
  costs exactly one metre, every time, which is the hardest size of error to
  notice.

- **`[0, 3, 4, 7, 10]` with three masts returns `5`.** You computed the average
  spacing — span `10`, two gaps, so `5` — and returned it without testing it.
  At a demand of 5 the walk plants on 0, then 7, and then has nowhere to go.
  The average is an upper *bound*, not an answer; the whole search exists
  because the bound is usually not achievable.

- **The spacing is right and the placement is wrong.** You returned the `chosen`
  list from the last iteration of the loop rather than re-running the walk at
  the final `lo`. The last iteration is often a *failed* test, so that list is
  either `None` or a placement at the wrong spacing. Run the predicate once
  more, deliberately, after the loop.

- **The answers are right and a large line takes minutes.** Your walk restarts
  from a different first post to "try harder". It is one pass, always starting
  at `posts[0]`, and the optimality argument in The Solution is why you are
  allowed to.

## Under the hood

<details>
<summary>Under the hood — the cost, the mirror, and how to spot this shape in a prompt</summary>

**Cost.**

Time is `O(n log S)`, where `n` is the number of posts and `S` is the span
between the first and last. The search runs about `log2(S)` times — thirty at
the top of the constraints — and each iteration walks the posts once. The
extra walk after the loop is one more pass and changes nothing asymptotically.
Space is `O(masts)` for the placement it returns, and `O(1)` beyond that.

The alternatives are not close. Trying every spacing from 1 upwards is
`O(n · S)` — a billion walks. Enumerating placements is worse than
astronomical: choosing 100 posts out of 200,000 is a number with over 400
digits.

**The two directions, side by side.**

| | Minimise a threshold (Exercise 5) | Maximise a minimum (this page) |
| --- | --- | --- |
| Predicate run | `F F F T T T` | `T T T F F F` |
| Wanted | first `True` | last `True` |
| On success | `hi = mid` | `lo = mid` |
| On failure | `lo = mid + 1` | `hi = mid - 1` |
| Midpoint | round down | **round up** |
| Loop guard | `lo < hi` | `lo < hi` |

Read the table as one rule rather than two templates: *the branch that keeps
`mid` decides the rounding*. Keep `mid` on the `hi` side and round down; keep
it on the `lo` side and round up. Everything else is the same search.

**How the prompt gives it away.**

The phrasings that mean "bisect the answer, upward direction" are: *maximise
the minimum*, *the largest `x` such that*, *spread them out as much as
possible*, *make the worst-off as well-off as possible*. The downward twins
are *minimise the maximum*, *the smallest `x` such that*, *the cheapest
capacity that still copes*. In both cases the second half of the sentence
describes a property that cannot un-hold as `x` moves one way — and that is the
thing to check before committing, because a prompt can sound like this and have
a non-monotone property, in which case bisection quietly returns a plausible
wrong answer.

**Where it shows up outside practice problems.**

Placing cell towers or wireless access points so the nearest pair interferes
least. Choosing warehouse locations along a corridor. Scheduling maintenance
windows so the tightest turnaround is as generous as possible. Sampling a large
dataset so the closest pair of samples is as far apart as possible. In every
one, the same two-part structure: a cheap yes/no test for a candidate answer,
and a one-way relationship between the candidate and the test.

**Practice elsewhere.** The same maximise-the-minimum shape appears as
[LeetCode 1552 · Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/)
if you want a judge to run against. Its contract differs from ours — it returns
a bare number and never asks which positions were chosen, nor what happens with
fewer than two balls.

</details>

## Acceptance checklist

- [ ] `python challenge-02-signal-mast-spacing.py` prints the six report lines
      then `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You can deliver the four-part reframe in about thirty seconds.
- [ ] You can state the greedy optimality argument in two sentences — the
      leftmost start, and the earliest legal next post.
- [ ] The upper bound is `span // (masts - 1)` and you can prove it.
- [ ] The midpoint rounds up, and you can say what breaks if it does not.
- [ ] Both contract branches run before any division or indexing.
- [ ] The returned placement comes from a deliberate walk at the final `lo`.
- [ ] The cross-check against every combination passes on all three hundred
      generated lines.
- [ ] Committed to Git with a message like
      `Add Week 5 challenge 2: signal mast spacing`.

## Stretch

- **Report the gaps as well as the positions.** The operator wants to see the
  slack in the arrangement.

  ```python
  def spacing_report(posts: list[int], masts: int) -> list[int] | None:
      """Return the gaps between consecutive masts at the widest spacing."""
      answer = mast_spacing(posts, masts)
      if answer is None:
          return None
      _, chosen = answer
      return [b - a for a, b in zip(chosen, chosen[1:])]
  ```

  ```text
  3 masts -> gaps [13, 18]
  6 masts -> gaps [4, 5, 4, 12, 6]
  ```

  The smallest number in each list is the spacing the search returned. Two
  independent routes to the same number is the cheapest correctness test there
  is.

- **Ask the mirror question.** Given a required spacing, how many masts fit?

  ```python
  def masts_that_fit(posts: list[int], spacing: int) -> int:
      """Return the most masts that can be planted at this minimum spacing."""
      planted = [posts[0]]
      for post in posts[1:]:
          if post - planted[-1] >= spacing:
              planted.append(post)
      return len(planted)
  ```

  ```text
  spacing 13 -> 3 masts
  spacing 14 -> 2 masts
  ```

  This is the predicate with its arguments turned around, and it needs no
  search at all. Say out loud why one direction is a single walk and the other
  needs bisection — the answer is that one of them is asking a question the
  walk already answers.

- **Break the guarantee on purpose.** Allow two posts at the same position and
  re-run. Work out what happens to `lo = 1`: a demand of one metre no longer
  always succeeds, so the bottom of the interval is itself infeasible and the
  post-loop `assert` fires. Then decide what the contract *should* say — return
  `None`, or fall back to a spacing of zero — and defend the choice. Noticing
  that a constraint was load-bearing is worth more than any amount of extra
  code.

That is both challenges. Take the [quiz](../quiz.md), do the
[homework](../homework/README.md), then ship the
[mini-project](../mini-project/README.md).
