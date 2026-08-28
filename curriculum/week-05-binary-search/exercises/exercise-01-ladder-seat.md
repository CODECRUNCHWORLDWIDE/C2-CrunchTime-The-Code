# Exercise 1 — The Ladder Seat

> **Topic:** the canonical binary-search loop, written on a list that runs **downwards** instead of upwards
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Easy
> **Target time:** 12 minutes
> **Why this one:** binary search is four lines, and almost everybody can type those four lines. This page takes the muscle memory away by flipping the order of the list, so the two shrink rules swap sides. If you can still write the loop — and say out loud why each line is what it is — you own the template instead of the keystrokes.

## The Brief

Think of a very long staircase with one player standing on each step. The
strongest player is on the top step, and every step down holds a slightly
weaker player. Nobody shares a step, and nobody shares a rating.

That staircase is a **chess ladder**, and the org runs one. A player's step is
called their **seat**. Seat `0` is the top. The list of ratings you are handed
is in **strictly descending** order: biggest first, smallest last, no repeats.

The standings page needs one thing from you. Somebody types a rating, and you
say which seat holds it.

```
seat:      0     1     2     3     4     5
rating: 2410  2205  2199  1870  1602  1044
```

Ask for `1870` and the answer is `3`. Ask for `2200` and the answer is
"nobody" — `2200` sits in the gap between seats 1 and 2, and a gap is not a
seat.

Now the interesting part. You could read every rating from the top until you
find it. On a ladder of two million players that is two million reads for one
question. Instead you are going to **halve the problem**, over and over. Look
at the middle seat. Is that the rating? Done. Is the middle player *stronger*
than the rating you want? Then the player you want is further **down** the
staircase, and the whole top half disappears in one move. Weaker? The bottom
half disappears instead. Two million seats vanish in about twenty-one guesses.

That is **binary search**. And notice what just happened in that paragraph:
because the ladder runs downwards, "the middle is bigger than what I want"
means "go right" — the exact opposite of the ascending version in the lecture.
Do not translate it in your head. Re-derive it out loud.

Return the seat index. Return `None` when no seat holds that rating.

## Starter

Save this as `exercise-01-ladder-seat.py` and fill in the `TODO`s. It runs as
pasted — the self-check at the bottom will fail, and that failure is the
starting line, not a problem.

```python
"""exercise-01-ladder-seat.py — the chess ladder seat lookup.

One binary search over a strictly DESCENDING list of ratings.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
LADDER: list[int] = [2410, 2205, 2199, 1870, 1602, 1044]


# ---- Your task ----
def find_ladder_seat(ratings: list[int], rating: int) -> int | None:
    """Return the seat index holding `rating`, or None when no seat does.

    Args:
        ratings: Seat ratings, sorted strictly descending. Never modified.
        rating: The rating to look up.

    Returns:
        The index i with ratings[i] == rating, or None on a miss.
    """
    # TODO: closed interval [lo, hi] — hi starts at len(ratings) - 1
    # TODO: loop while lo <= hi, with mid = lo + (hi - lo) // 2
    # TODO: on a DESCENDING list, which comparison moves lo?
    # TODO: both shrink rules must step past mid, or the loop never ends
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (1870, 2200, 2410, 1044):
        print(f"rating {wanted:5d} -> seat {find_ladder_seat(LADDER, wanted)}")

    assert find_ladder_seat(LADDER, 1870) == 3
    assert find_ladder_seat(LADDER, 2200) is None
    assert find_ladder_seat(LADDER, 2410) == 0
    assert find_ladder_seat(LADDER, 1044) == 5
    assert find_ladder_seat([900, 12, -85], -85) == 2
    assert find_ladder_seat([1500], 1500) == 0
    assert find_ladder_seat([1500], 1499) is None
    assert find_ladder_seat([], 1500) is None
    assert LADDER[0] == 2410  # the ladder was never rearranged
    print("All checks passed.")
```

Three words you need before you start.

**Interval.** The stretch of seats you have not ruled out yet, held in two
numbers, `lo` and `hi`. At the start it is the whole ladder.

**Closed interval.** Writing `[lo, hi]` with a square bracket at both ends
means both `lo` and `hi` are still real candidates — the stretch includes its
own ends. That is the convention this page uses, and it comes as a package:
`hi` starts at `len(ratings) - 1`, the loop guard is `lo <= hi`, and both
shrink rules step **past** `mid`, with `mid + 1` and `mid - 1`. Take half of
this package and half of another one and you get the bugs at the bottom of
this page.

**Midpoint.** `mid = lo + (hi - lo) // 2`. In Python `(lo + hi) // 2` gives
the same number. Write the longer one anyway: in C, Java or Rust, `lo + hi`
on a huge list overflows a 32-bit integer and lands on a negative index, and
this spelling never can. Interviewers watch for it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/exercises/exercise-01-ladder-seat.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_ladder_seat(ratings, rating)` returns the index `i` where
   `ratings[i] == rating`.
2. It returns `None` — not `-1`, not `0` — when no seat holds that rating.
3. It reads at most about `log2(len(ratings))` ratings. No scan, no `in`, no
   `.index()`, no dict.
4. It uses the closed-interval package throughout: `hi = len(ratings) - 1`,
   guard `lo <= hi`, shrinks `mid + 1` and `mid - 1`.
5. It computes `mid` as `lo + (hi - lo) // 2`.
6. It never modifies `ratings`; `LADDER[0]` is still `2410` afterwards.
7. It handles the empty ladder without indexing anything.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(ratings) <= 2_000_000`.** Two million seats is the whole
  federation, and the standings page runs this lookup once per visitor. A scan
  reads up to two million ratings per visitor; this loop reads about
  twenty-one. That gap *is* the page's latency budget, which is why the bound
  is written this large rather than at a comfortable hundred.

- **The ladder is sorted strictly descending, so every rating is distinct.**
  Descending is the twist, and it is the whole point of the exercise. *Strict*
  means no ties, which is what makes "the seat" one answer rather than a run
  of them. Exercise 2 takes the strictness away and the shape of the answer
  changes with it.

- **`-400 <= ratings[i] <= 3_600`.** Ratings can be **negative** — a
  provisional player who forfeits three games in a row lands below zero. This
  bound exists to kill the tempting shortcut of returning `-1` for "not
  found": `-1` is a legal rating here, so a caller who got `-1` back could not
  tell an answer from a failure. `None` cannot be mistaken for a rating, and
  that is why the signature returns it.

- **The empty ladder is legal input.** The federation's first day has nobody on
  it. With `hi = len(ratings) - 1 = -1`, the guard `lo <= hi` is false straight
  away and the loop never touches the list — so the empty case needs no special
  branch, and you should be able to say why in one sentence.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-ladder-seat.py
rating  1870 -> seat 3
rating  2200 -> seat None
rating  2410 -> seat 0
rating  1044 -> seat 5
All checks passed.
```

Line two is the one to look at. `2200` sits inside the range of ratings on
the ladder and is still absent. "In range" and "present" are different facts,
and mistaking one for the other is the most common way this loop goes wrong.

## Steps

1. Save the starter and run it before writing anything:
   `python exercise-01-ladder-seat.py`. The first line prints
   `seat Ellipsis`, then the first assert fails. That is the correct starting
   point — it proves the self-check is real.
2. Write the closed-interval package down on paper before you type: `hi`
   starts at `len(ratings) - 1`, the guard is `lo <= hi`, the shrinks are
   `mid + 1` and `mid - 1`. Everything else is filling that in.
3. Set `lo, hi = 0, len(ratings) - 1` and open the `while lo <= hi:` loop.
4. Compute `mid`, then take the easy branch first: if `ratings[mid]` is the
   rating, return `mid`.
5. Now the branch that matters. On this ladder, if `ratings[mid]` is **bigger**
   than the rating you want, everything from `mid` upwards is too strong and
   the answer must be further down: `lo = mid + 1`. Otherwise `hi = mid - 1`.
   Say that sentence out loud before you type it.
6. After the loop, `return None`.
7. Run it. Then trace the `2200` miss by hand, on paper, and confirm the loop
   really does close to `lo = 2, hi = 1` and exit.
8. Once it passes, try `[1500]` and `[]` in a REPL and convince yourself the
   guard alone handles both.

## The Solution

```python
"""exercise-01-ladder-seat-solution.py - the chess ladder seat lookup.

One binary search over a strictly DESCENDING list of ratings. The descending
order is the whole twist: the two shrink rules swap sides compared with the
ascending template in the lecture.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
LADDER: list[int] = [2410, 2205, 2199, 1870, 1602, 1044]


# ---- Your task ----
def find_ladder_seat(ratings: list[int], rating: int) -> int | None:
    """Return the seat index holding `rating`, or None when no seat does.

    Args:
        ratings: Seat ratings, sorted strictly descending. Never modified.
        rating: The rating to look up.

    Returns:
        The index i with ratings[i] == rating, or None on a miss.
    """
    lo, hi = 0, len(ratings) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if ratings[mid] == rating:
            return mid
        if ratings[mid] > rating:
            lo = mid + 1  # midpoint is stronger, so the target sits lower down
        else:
            hi = mid - 1  # midpoint is weaker, so the target sits higher up
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (1870, 2200, 2410, 1044):
        print(f"rating {wanted:5d} -> seat {find_ladder_seat(LADDER, wanted)}")

    assert find_ladder_seat(LADDER, 1870) == 3
    assert find_ladder_seat(LADDER, 2200) is None
    assert find_ladder_seat(LADDER, 2410) == 0
    assert find_ladder_seat(LADDER, 1044) == 5
    assert find_ladder_seat([900, 12, -85], -85) == 2
    assert find_ladder_seat([1500], 1500) == 0
    assert find_ladder_seat([1500], 1499) is None
    assert find_ladder_seat([], 1500) is None
    assert LADDER[0] == 2410  # the ladder was never rearranged
    print("All checks passed.")
```

**The whole algorithm is one sentence: throw away the half that cannot hold
the answer.** Every trip round the loop reads exactly one rating and deletes
about half the seats still in play. Six become three, then one, then none. Two
million become about twenty-one reads, because that is how many times you can
halve two million before nothing is left.

**The descending order flips the two shrink rules, and nothing else.** On an
ascending list, a midpoint *smaller* than your target means "go right". Here
the list runs the other way, so a midpoint *larger* than your target means
"go right" — `lo = mid + 1`. The lesson generalises: the comparison is not a
fact about binary search, it is a fact about which way the data is sorted.
Read the data first, then write the comparison.

**The interval has to shrink, or the loop never ends.** Both branches move
past `mid`: `mid + 1` and `mid - 1`. Neither one can leave the interval the
same size. Write `lo = mid` instead and, once a single seat is left, `mid`
comes out equal to `lo` every time and the loop spins until you kill it. That
is not a hypothetical; it is the first entry under Common bugs to catch.

**The loop guard and the starting `hi` are one decision, not two.** `hi`
starts at the last valid index, so `hi` is a candidate, so the guard must be
`lo <= hi` in order to test it. Change either one on its own and the
single-seat case breaks: `[1500]` with `1500` returns `None`, because
`lo == hi == 0` and a `<` guard walks away without looking.

**`return None` is a real answer, not a fallback.** The loop exits when `lo`
has crawled past `hi`, and that is exactly the moment the interval is empty —
every seat ruled out. It is a proof that the rating is absent, not a guess.
`None` rather than `-1` or `0` is what keeps that proof distinguishable from
data, because `-1` is a legal rating and `0` is a legal seat.

**The empty ladder needs no code at all.** `hi` is `-1` before the loop
starts, the guard is false, and the function returns `None` without reading
anything. When a contract's degenerate case falls out of the invariant for
free, that is a sign the invariant is the right one.

## Download and run

Download
[exercise-01-ladder-seat-solution.py](./exercise-01-ladder-seat-solution.py)
and run it:

```bash
python exercise-01-ladder-seat-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-ladder-seat.py`.

## Common bugs to catch

- **The program hangs and never prints anything.** You wrote `lo = mid` or
  `hi = mid` inside the closed-interval loop. Once the interval narrows to one
  seat, `mid` lands on that seat every single time and neither end ever moves.
  Nothing prints, nothing crashes, the fan spins up. Press `Ctrl-C` and Python
  shows you exactly where it was stuck:

  ```text
  Traceback (most recent call last):
    File "<string>", line 7, in <module>
      while lo <= hi:
            ^^^^^^^^
  KeyboardInterrupt
  ```

  The fix is the invariant: in the closed convention **both** shrink rules
  exclude `mid`. If you catch yourself wanting `hi = mid`, you are reaching
  for the half-open convention — that is Exercise 2, and there `hi` starts at
  `len(...)` and the guard is `lo < hi`.

- **`IndexError: list index out of range`.** You set `hi = len(ratings)` and
  kept the `lo <= hi` guard — half of one convention, half of the other:

  ```text
  Traceback (most recent call last):
      if ratings[mid] == rating:
         ~~~~~~~^^^^^
  IndexError: list index out of range
  ```

  `len(ratings)` is one past the last seat. Under the closed guard the loop
  eventually computes `mid = len(ratings)` and reads a seat that does not
  exist. Closed pairs with `len - 1` and `<=`; half-open pairs with `len` and
  `<`.

- **A bare `AssertionError` on the first check, with
  `find_ladder_seat(LADDER, 1870)` returning `None`.** You wrote the ascending
  comparison `if ratings[mid] < rating: lo = mid + 1` out of habit. On a
  descending ladder that walks *away* from the answer every time, so the
  interval empties and you report "absent" for a rating that is sitting right
  there. This is the bug the exercise exists to provoke, and there is no
  traceback to help you — a wrong direction never crashes, it just lies.

- **`[1500]` with `1500` returns `None`.** You wrote `while lo < hi` with the
  closed convention. When the interval narrows to one seat, `lo == hi`, and
  `<` exits without ever testing it. The one-element list is the cheapest test
  there is for this, which is why it is in the self-check.

- **You return `-1` for "no seat".** Read the constraints again: `-1` is a
  legal rating on this ladder, so the caller cannot tell your failure code
  from a real answer. `0` is worse — it is the top seat. `None` is the only
  value in this contract that cannot be confused with data.

- **You return the rating instead of the seat.** `return ratings[mid]` looks
  plausible on a page full of numbers and is wrong on every input. Read the
  signature and the docstring: the caller already knows the rating. They typed
  it.

## Under the hood

<details>
<summary>Under the hood — why twenty-one reads, and why nothing beats it</summary>

**Where the number twenty-one comes from.**

Each iteration reads one rating and discards about half of what is left. Start
with `n` seats: after one read there are `n/2` left, then `n/4`, and so on.
The loop stops when nothing is left, so the question is how many halvings that
takes — which is exactly what `log2(n)` means. For two million,
`log2(2_000_000)` is a shade under 21.

The three approaches, side by side, at that size:

| Approach | Ratings read | Extra memory |
| --- | ---: | ---: |
| Scan from the top | 2,000,000 | none |
| Binary search | 21 | none |
| Dict from rating to seat | 1 | 2,000,000 entries |

The dict looks unbeatable until you count the build. Filling it reads all two
million ratings once — as expensive as a single scan — and this ladder is
rebuilt after every tournament round. You would pay a full scan to save twenty
reads. A dict wins when the same ladder is queried thousands of times between
rebuilds and loses when it is queried once, and knowing which situation you
are in is the actual skill.

**Why `O(log n)` is a floor, not just the best anyone has found.**

If the only move available is "compare the target against one rating", then
each comparison rules out at most half the seats. Narrowing `n` possibilities
down to `1` therefore needs at least `log2(n)` comparisons. So no
comparison-based method beats this one by more than a constant factor.
Beating it at all means not comparing — computing an address straight from the
value, which is what a dict does, and paying `O(n)` memory for the privilege.

**`bisect`, and why you are writing the loop by hand.**

Python ships this in the standard library:

```python
import bisect
i = bisect.bisect_left(ascending_values, target)
```

It is written in C, it is faster than your loop, and in production you should
use it. Two catches. It only works on **ascending** data, so this descending
ladder would need reversing or negating first. And an interviewer asking for
binary search is not asking whether you can find the library; they are asking
whether you can defend a boundary convention out loud. That skill does not
come from calling `bisect_left`.

**The overflow the mid formula is really about.**

`mid = (lo + hi) // 2` was the standard textbook spelling for decades, and it
is broken in any language with fixed-width integers. On a list of about 1.5
billion elements, `lo + hi` exceeds the largest 32-bit signed integer, wraps
round to a negative number, and the search crashes or reads the wrong memory.
The bug sat undetected in the JDK's own binary search for nine years. Python's
integers grow as large as they need to, so you are safe here — but you are
writing this to transfer it, and the habit costs nothing.

</details>

## Acceptance checklist

- [ ] `python exercise-01-ladder-seat.py` prints four rows then `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] The loop uses the closed-interval package: `len - 1`, `lo <= hi`,
      `mid + 1` / `mid - 1`.
- [ ] `mid` is computed as `lo + (hi - lo) // 2`.
- [ ] A miss returns `None`, and you can say in one sentence why `-1` is wrong
      here.
- [ ] You traced the `2200` miss by hand before running the file.
- [ ] `LADDER` is in its original order after every call.
- [ ] Committed to Git with a message like `Add Week 5 exercise 1: ladder seat`.

## Stretch

- **Return the seat the rating *would* take, instead of `None`.** The
  standings page wants to show a provisional player where they would land.

  ```python
  def would_be_seat(ratings: list[int], rating: int) -> int:
      """Return the seat a new player with this rating would occupy."""
      lo, hi = 0, len(ratings)
      while lo < hi:
          mid = lo + (hi - lo) // 2
          if ratings[mid] > rating:
              lo = mid + 1
          else:
              hi = mid
      return lo
  ```

  ```text
  2200 would take seat 2
  9999 would take seat 0
     1 would take seat 6
  ```

  Look at what changed: `hi` starts at `len`, the guard is `<`, one shrink
  rule is `hi = mid`, and there is no early return at all. That is the
  **half-open** package, whole. You have now written both conventions on the
  same data, which is the fastest way to stop mixing them.

- **Count the reads and check the twenty-one claim.** Add a counter next to
  `mid` and return it alongside the seat.

  ```text
  ladder of         6 seats:  3 reads
  ladder of     1_000 seats: 10 reads
  ladder of 2_000_000 seats: 21 reads
  ```

  Then double the last one and watch the count rise by exactly one. That is
  the shape of a logarithm, seen rather than recited.

- **Write it recursively, then argue against it.** A recursive binary search is
  four lines and reads nicely. Now work out its cost: one stack frame per
  halving, so `O(log n)` memory where the loop uses none, and in a language
  without tail calls — Python included — a deep enough recursion raises
  `RecursionError`. Say both facts out loud. Knowing why you prefer the loop
  is worth more than the loop.

When your seat lookup is right, move on to
[Exercise 2 — The Scan Window](./exercise-02-scan-window.md).
