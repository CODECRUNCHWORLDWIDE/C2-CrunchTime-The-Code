# Challenge 2 — The Repaving Stretch

> **Topic:** a growing window whose invariant is a *subtraction* over a frequency table, and a second answer the window alone cannot give you
> **Lecture:** [02 — The Shrinking and Growing Mechanics](../lecture-notes/02-the-shrinking-and-growing-mechanics.md)
> **Difficulty:** Hard
> **Target time:** 90 minutes
> **Why this one:** Challenge 1 asked what the window *contains*. This one asks what the window could be *turned into* if you were allowed to change a few things inside it, which is a genuinely different kind of invariant and one people find much harder to state. It also has a sting in the tail: the classic speed-up for this shape gives you the right length and makes the second half of the answer impossible, and noticing that is the real test.

## The Brief

A highways authority keeps a record of every road it looks after. Each road is
divided into 20-metre **segments**, and for each segment the record says what
the surface is: `"asphalt"`, `"concrete"`, `"chipseal"` or `"gravel"`. The
segments are listed in order, from one end of the route to the other, so the
record is just a list of strings.

A resurfacing crew goes out for one shift at a time. In a shift they can do two
things and no more:

- They work on a **contiguous stretch** of the route. They set up at one point
  and work forward; they do not skip about.
- They can lay new surface on at most **`budget`** segments. That is how much
  material fits on the truck.

When they finish, the whole stretch they worked on has to be **one single
surface** end to end. That is the point of the shift — a road that changes
surface every fifty metres is what they were sent to fix.

So think about what that costs. Suppose the crew takes a stretch of nine
segments: six are already asphalt, two are gravel, one is concrete. If they
decide the stretch will be asphalt, the six asphalt segments need no work and
the other three do. Three repaves. If they decide it will be gravel instead,
they would have to repave seven. Obviously they pick asphalt.

That reasoning generalises into one line, and the line is the whole problem:

```text
segments to repave = how long the stretch is - how many segments already share its most common surface
```

Because whatever the most common surface in the stretch is, keeping it and
changing everything else is the cheapest option available. So a stretch is
**affordable** exactly when that difference is at most the budget.

**Your job.** Return the longest affordable stretch as `(start, end, surface)`.
The first two are a half-open span, so `surfaces[start:end]` is the stretch
itself. The third is the surface it ends up as.

That third element is what makes this harder than it looks. A window can tell
you *how long* the best stretch is. Telling you *which surface* it becomes
means knowing something about the winning window's contents after the fact, and
the fastest known version of this algorithm deliberately throws that
information away. Read *Under the hood* once you have it working; the trap is
worth meeting on purpose.

**The contract.** Ties on length go to the **largest** start — the depot sits
at the far end of the route, so among equally long stretches the crew takes the
one that starts nearest to it and saves the driving. Inside the winning
stretch, if two surfaces are equally common, take the **alphabetically first**
code, so the answer is deterministic. `budget` may be `0`, which is a real
question and not an edge case: it asks for the longest stretch that is *already*
uniform. An empty route returns `None`.

## Starter

Create `challenge-02-repaving-stretch.py` and paste this in. Fill in every
`TODO`.

```python
"""challenge-02-repaving-stretch.py — the longest repavable stretch.

Find the longest contiguous stretch of road the crew can make uniform within
its material budget, and say what surface it becomes.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import Counter


def longest_uniform_stretch(surfaces: list[str], budget: int) -> tuple[int, int, str] | None:
    """Return the longest stretch the crew can make uniform within budget.

    Args:
        surfaces: Surface code of each 20-metre segment, in route order.
        budget: How many segments the crew may repave in one pass. Zero is
            legal and asks for the longest already-uniform run.

    Returns:
        (start, end, surface) with surfaces[start:end] the stretch and
        `surface` what it becomes. Ties on length go to the larger start; ties
        on the surface inside the chosen stretch go to the alphabetically
        first code. An empty route returns None.
    """
    # TODO: the empty route is the only input with no answer at all.
    # TODO: a frequency table, `left` at 0, `best` unset.
    # TODO: walk `right` over the route, adding to the table.
    # TODO: while the stretch costs more than the budget, drop surfaces[left]:
    #         decrement, delete the key on zero, advance left.
    #       The cost is the line from the brief. Write it as one expression.
    # TODO: record. Both rules — longer wins, then later start — belong in one
    #       comparison, which means negating both numbers.
    # TODO: after the loop, work out the surface from the winning stretch:
    #       the most common code in it, ties going alphabetically first.
    ...


def repaves_needed(stretch: list[str], surface: str) -> int:
    """Return how many segments of `stretch` are not already `surface`.

    Args:
        stretch: The segments inside a candidate window.
        surface: The surface the crew would lay.

    Returns:
        The count of segments that would have to be repaved.
    """
    # TODO: count the segments that do not already match.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], int]] = [
        (["asphalt", "chipseal", "asphalt", "gravel", "asphalt", "asphalt"], 1),
        (["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1),
        (["asphalt", "asphalt", "gravel", "asphalt", "asphalt"], 1),
        (["gravel", "gravel", "asphalt", "gravel", "gravel", "gravel"], 0),
        (["asphalt", "gravel", "concrete", "chipseal"], 0),
        (["concrete", "asphalt"], 1),
        (["asphalt", "concrete", "gravel"], 5),
        (["chipseal"], 0),
        ([], 3),
    ]
    for route, budget in cases:
        answer = longest_uniform_stretch(route, budget)
        if answer is None:
            print(f"budget {budget}  route {str(route):<66} -> None")
        else:
            start, end, surface = answer
            print(f"budget {budget}  route {str(route):<66} -> ({start}, {end}) as {surface}")
    print()

    assert longest_uniform_stretch(["asphalt", "chipseal", "asphalt", "gravel", "asphalt", "asphalt"], 1) == (2, 6, "asphalt")
    assert longest_uniform_stretch(["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1) == (2, 5, "asphalt")
    assert longest_uniform_stretch(["asphalt", "asphalt", "gravel", "asphalt", "asphalt"], 1) == (0, 5, "asphalt")
    assert longest_uniform_stretch(["gravel", "gravel", "asphalt", "gravel", "gravel", "gravel"], 0) == (3, 6, "gravel")
    assert longest_uniform_stretch(["asphalt", "gravel", "concrete", "chipseal"], 0) == (3, 4, "chipseal")
    assert longest_uniform_stretch(["concrete", "asphalt"], 1) == (0, 2, "asphalt")
    assert longest_uniform_stretch(["asphalt", "concrete", "gravel"], 5) == (0, 3, "asphalt")
    assert longest_uniform_stretch(["chipseal"], 0) == (0, 1, "chipseal")
    assert longest_uniform_stretch([], 3) is None

    # Brute force agrees: check every stretch against every surface it could
    # become, and pick by the contract's own ordering.
    for route, budget in cases:
        affordable = [
            (-(j - i), -i)
            for i in range(len(route))
            for j in range(i + 1, len(route) + 1)
            if min(repaves_needed(route[i:j], code) for code in set(route[i:j])) <= budget
        ]
        answer = longest_uniform_stretch(route, budget)
        if not affordable:
            assert answer is None
            continue
        negated_length, negated_start = min(affordable)
        start, length = -negated_start, -negated_length
        assert answer is not None
        assert (answer[0], answer[1] - answer[0]) == (start, length)
        assert repaves_needed(route[start : start + length], answer[2]) <= budget

    print("All checks passed.")
```

Two things you need before you start.

**The cost expression.** `(right - left + 1) - max(counts.values())`. The first
half is how many segments are in the window. The second is how many of them
already share the most common surface. The difference is the work. Write it
out and stare at it until it reads as English rather than as arithmetic,
because every mistake on this page is really a mistake about what that line
means.

**Monotone under shrinking.** Trimming a segment off the left can only make the
cost the same or lower — it removes one segment from the length, and it removes
at most one from the top count. So once the cost drops to within budget, more
trimming cannot push it back out. That is why a single `while` is enough, and
it is the same property that made Exercise 4's shrink safe.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/challenges/challenge-02-repaving-stretch.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `longest_uniform_stretch(surfaces, budget)` returns `(start, end, surface)`
   or `None`.
2. `start` and `end` are a **half-open span**, so `surfaces[start:end]` is the
   stretch. On `["chipseal"]` with budget `0` the answer is `(0, 1, "chipseal")`.
3. Ties on length go to the **largest** start.
   `longest_uniform_stretch(["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1)`
   is `(2, 5, "asphalt")`, not `(0, 3, "asphalt")`.
4. The reported surface is the most common one **inside the winning stretch**,
   ties going to the alphabetically first code.
5. `budget == 0` is a real question and returns the longest already-uniform run.
6. An empty route returns `None`.
7. The frequency table is maintained incrementally. Nothing inside the loop may
   build a `Counter` from a slice.
8. Every count that reaches zero has its key deleted.
9. `repaves_needed` is used only by the self-check, never by the solution.
10. Both functions keep their type hints and their docstrings.

## Constraints

- **`0 <= len(surfaces) <= 300_000`.** A 6,000-kilometre route at 20 metres a
  segment is 300,000 segments, so this covers an entire national route list.
  The bound rejects the try-every-stretch brute force, which examines about
  `4.5 x 10^10` windows and rebuilds a count for each — the version the
  self-check uses, and the reason the self-check only runs it on nine-element
  routes.

- **`0 <= budget <= 5_000`, and zero is legal on purpose.** One crew's material
  load for a shift. A budget of zero is not a degenerate input to be guarded
  away: it is the question "where is the road already consistent?", which a
  highways authority asks constantly. It is also the case where the shrink loop
  works hardest, so it is the best test of whether your cost expression is
  right.

- **Surface codes come from a fixed catalogue of at most 6 codes.** A highways
  authority maintains a handful of surface types, not an open-ended set. This
  bound is load-bearing and it is the sentence to say out loud: it makes
  `max(counts.values())` at most six comparisons, which is a constant, which is
  what keeps the whole scan linear. Without it, re-reading the largest count at
  every step would cost `O(catalogue)` per step and the claim would fail.

- **Cost is computed from the maintained table, never from a slice.**
  `Counter(surfaces[left:right + 1])` inside the loop is correct and quadratic,
  and the size bound rejects it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-repaving-stretch.py
placeholder
```

The second row is the tie-break test. Three stretches of length 3 are
affordable at a budget of 1 — segments 0–2, 1–3 and 2–4 — and nothing longer
is, because any four consecutive segments here split two and two and would cost
two repaves. The contract wants the last of the three.

The fifth row is the one people find surprising. With a budget of zero and four
different surfaces in a row, every stretch of two already costs one repave, so
the longest affordable stretch is a single segment — and *all four* segments
tie. The largest start wins, giving `(3, 4, "chipseal")`. If your code returns
`(0, 1, "asphalt")` your cost expression is fine and your tie-break is not.

The sixth row tests the surface tie-break on its own: `["concrete", "asphalt"]`
with a budget of 1 takes the whole route, both surfaces appear once, and the
alphabetically first wins.

## Steps

1. Create the file, paste the starter, and run it. Every row errors on
   unpacking `None`. Correct starting point.
2. Write the empty-route guard. It is the only input with no answer, and it
   also protects `max(counts.values())` from ever seeing an empty table.
3. Set up `counts`, `left = 0` and `best = None`.
4. Write the outer loop and the increment.
5. Write the cost expression as its own thought before you put it in a `while`.
   Print it at each step on the first test case if that helps; seeing the
   numbers 0, 1, 1, 2, 1, 1 come out is worth more than reasoning about them.
6. Write the shrink. Decrement, delete on zero, advance — the same three lines
   as Exercise 5, and the deletion matters here for a different reason: a key
   at zero would not change `max` on most inputs, but it *would* on a stretch
   that has just been emptied of its most common surface.
7. Record after the shrink. Both rules go in one tuple, and both numbers are
   negated, because a smaller tuple must mean a *longer* stretch with a *later*
   start.
8. After the loop, take the winning span and work out its surface. Counting the
   winning stretch once, at the end, is `O(n)` once — not per step — so it is
   cheap and it is obviously correct.
9. Write `repaves_needed` last. Like Challenge 1's `covers`, it exists so a
   brute force built from a different idea can disagree with you.
10. Before you trust anything, trace the fourth case — budget zero — by hand.
    Six steps, and the shrink fires three times.

## The Solution

```python
placeholder
```

**The cost line is the invariant, and everything else is bookkeeping.**

```python
while (right - left + 1) - max(counts.values()) > budget:
```

Read it as the sentence from the brief: *the number of segments in this stretch,
minus the number that already share its most common surface, is how many the
crew would have to repave.* The `while` says: keep trimming until that is
within budget.

Two things are worth checking that you believe. First, that keeping the most
common surface really is optimal — it is, because any other choice leaves fewer
segments untouched by definition. Second, that the table can never be empty
when `max` runs — it cannot, because the segment at `right` was added
immediately above, so there is always at least one key.

**Why `while` and not `if`.** A single new segment can push the cost up by one
at most, so it is tempting to think one trim always suffices. It does not, and
the fourth test case shows why: at a budget of zero, arriving at `"asphalt"` in
a run of gravel forces the window down to a single segment, which takes two
trims. More generally, a trim removes one from the length *and* may remove one
from the top count, in which case the cost does not fall at all. The `while` is
what makes the loop correct rather than merely usually correct.

**The deletion is still load-bearing, for a subtler reason than usual.** In
Exercise 5 a stale zero key broke `len(counts)`. Here it would break
`max(counts.values())` — a surface that has entirely left the window, sitting
at zero, is harmless, but a surface that leaves while it was the *most common*
one must not keep a count that misrepresents the window. Deleting on zero keeps
the table an honest description of what is inside the span, which is the
property every line here depends on.

**Both rules, one comparison, both negated.**

```python
candidate = (-(right - left + 1), -left)
if best is None or candidate < best:
    best = candidate
```

Longer wins and later start wins, and tuple comparison ranks *upward*, so both
numbers are negated to flip the direction. It looks fussy and it removes an
entire class of bug: there is exactly one place where the ranking lives, and it
reads in the same order as the contract states the rules.

**The surface is computed once, at the end, and that is a deliberate choice.**

```python
tally = Counter(surfaces[start : start + length])
most = max(tally.values())
surface = min(code for code, seen in tally.items() if seen == most)
```

You could carry the winning table along in `best` and save this pass. It would
be marginally faster and materially harder to get right, because the table you
carry has to be a *copy* — the live one keeps changing underneath you. One
`O(n)` pass at the end, on a window you have already finished choosing, costs
nothing next to the `O(n)` scan you just did and is obviously correct by
inspection. Preferring the version you can verify by reading, when the costs
are the same order, is a real engineering judgement and worth saying out loud.

The `min(...)` is the alphabetical tie-break: among the codes that hit the top
count, take the smallest string. `min` over a generator with a filter is the
idiomatic way to say "the smallest thing satisfying a condition" without
building a list first.

**Why the whole thing is linear.** `right` advances exactly `n` times. `left`
only moves forward and never passes `right`, so it advances at most `n` times
across the entire function. Every dictionary operation is `O(1)` on average,
and `max(counts.values())` touches at most six entries by the catalogue bound —
a constant. The final tally is one more `O(n)` pass. Total `O(n)` time, `O(1)`
space, with the catalogue bound doing the work in both claims. State the bound
before you make the claim.

## Download and run

Download
[challenge-02-repaving-stretch-solution.py](./challenge-02-repaving-stretch-solution.py)
and run it:

```bash
python challenge-02-repaving-stretch-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-02-repaving-stretch.py`.

## Common bugs to catch

- **`ValueError: max() iterable argument is empty`.**

  ```text
  Traceback (most recent call last):
      while (right - left + 1) - max(counts.values()) > budget:
                                 ~~~^^^^^^^^^^^^^^^^^
  ValueError: max() iterable argument is empty
  ```

  Your shrink loop emptied the window and then asked for the largest count in
  an empty table. It happens when the cost expression is wrong in a way that
  keeps the condition true forever — usually `- max(...)` written as
  `- len(counts)`, which is Exercise 5's invariant, not this one.

- **`longest_uniform_stretch(["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1)`
  returns `(0, 3, "asphalt")`.** You used `>` where the tie-break needs the
  later of two equal-length stretches, or you compared un-negated numbers. No
  traceback; a genuinely affordable stretch of the right length, and the wrong
  one.

- **`longest_uniform_stretch(["asphalt", "gravel", "concrete", "chipseal"], 0)`
  returns `(0, 1, "asphalt")`.** The same tie-break bug, showing up on a route
  where *every* candidate ties. This case is the more reliable detector of the
  two, because it does not depend on your cost expression being right first.

- **Shrinking on distinctness instead of cost.** Writing
  `while len(counts) > 1` asks "is this stretch already uniform?", which is the
  `budget == 0` question hard-coded. It passes the fourth and eighth cases and
  fails everything with a budget above zero. If your answers are all short, this
  is why.

- **The wrong surface on a correct span.** You took the most common surface in
  the *whole route*, or in the table as it stood at the end of the loop, rather
  than in the winning stretch. The live table describes the last window the loop
  looked at, which is almost never the best one.

- **`KeyError` on the delete.**

  ```text
  Traceback (most recent call last):
      del counts[leaving]
      ^^^^^^^^^^^^^^^^^^^
  KeyError: 'gravel'
  ```

  You deleted unconditionally rather than only on zero.

- **Half-open confusion.** Returning `(start, start + length - 1)` gives you an
  inclusive pair, and `surfaces[start:end]` then drops the last segment. Check
  against `["chipseal"]` with budget `0`, which must be `(0, 1, "chipseal")`.

- **Rebuilding the table inside the loop.** `Counter(surfaces[left:right + 1])`
  per step is correct and quadratic. No exception, right answers, and the
  challenge not met.

## Under the hood

<details>
<summary>Under the hood — the famous optimisation, and why this contract deliberately breaks it</summary>

**The optimisation you will find if you go looking.**

There is a well-known trick for this shape. Instead of re-reading
`max(counts.values())` at every step, keep a variable `best_count` and **never
let it decrease**, even when segments leave the window:

```python
best_count = max(best_count, counts[surface])
if (right - left + 1) - best_count > budget:
    counts[surfaces[left]] -= 1
    left += 1
```

Note two changes. `best_count` only ever goes up, and the `while` has become an
`if` — the window never actually shrinks, it just stops growing and slides.

It is correct *for the length*, and the argument is elegant. A window is only
ever worth recording when it is longer than the best so far, and it can only get
longer if some surface's count has risen above the previous `best_count`. So a
stale, too-large `best_count` can make the window slide when it might have
grown — but only into positions that could never have produced a longer answer
anyway. The window's length becomes a high-water mark rather than a true
measurement, and the high-water mark is what you wanted.

**And it makes this page's contract impossible to satisfy.**

Because the window is no longer guaranteed to be affordable, its contents at
the end are not guaranteed to describe a valid stretch. The `best_count`
variable does not remember *which* surface it belonged to, and even if you made
it remember, that surface may have left the window several steps earlier. You
end up with a correct length attached to a span you cannot trust and a surface
you cannot name.

That is why this problem asks for `(start, end, surface)` rather than a bare
length, and it is the whole reason it exists as a challenge. The lesson
generalises well beyond road surfaces: **an optimisation that discards
information is only safe while nobody asks for the information.** A contract
change you did not anticipate can invalidate a technique you were sure of, and
the way to notice is to ask what each shortcut is throwing away before you take
it.

Try it. Implement the fast version, return only the length, and check it
against the page's solution on all nine cases — the lengths will agree. Then
try to add the surface, and watch where it fails.

**Cost, stated precisely.**

Time is `O(n)`, amortised, plus one `O(n)` pass at the end for the tally.
`right` advances `n` times; `left` advances at most `n` times across the whole
run; `max(counts.values())` is at most six comparisons by the catalogue bound.
Best, average and worst are all `O(n)` — no early exit, since a longer stretch
can appear anywhere.

Space is `O(min(n, 6))`, so `O(1)`. Say the tighter of the two bounds and say
which one binds.

Without the catalogue bound the honest claim is `O(n · c)` time for the `max`
re-reads, where `c` is the number of distinct surfaces. That is when the
never-decreasing `best_count` trick stops being a micro-optimisation and starts
being the difference between linear and not — which is a much better reason to
reach for it than "it is faster", and a much better thing to say in an
interview.

**A third approach, for completeness.** Since the catalogue is tiny, you could
run six separate windows — one per surface — each asking "the longest stretch
in which at most `budget` segments are *not* this surface". Each is a simple
at-most-K window over a binary condition, and you take the best of the six. It
is `O(n · c)`, it is embarrassingly easy to get right, and it hands you the
surface for free because each pass already knows which one it is about. On a
catalogue of six that is a perfectly defensible engineering choice. Being able
to propose it, cost it, and say why you did or did not pick it is worth more
than knowing the clever version.

</details>

## Acceptance checklist

- [ ] `python challenge-02-repaving-stretch.py` prints nine rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] You can write the cost expression from memory and say what each half means.
- [ ] `longest_uniform_stretch(["asphalt", "gravel", "concrete", "chipseal"], 0)` returns `(3, 4, "chipseal")`.
- [ ] `longest_uniform_stretch(["concrete", "asphalt"], 1)` returns `(0, 2, "asphalt")`.
- [ ] The shrink is a `while`, and every count reaching zero has its key deleted.
- [ ] The surface is computed from the winning stretch, not from the live table.
- [ ] No `Counter(...)` of a slice appears inside the loop.
- [ ] The brute-force check passes on all nine routes.
- [ ] You have read *Under the hood* and can say, in one sentence, why the fast version cannot report the surface.
- [ ] Committed to Git with a message like `Add Week 3 challenge 2: the repaving stretch`.

## Stretch

- **Implement the never-decreasing version and compare.**

  ```python
  def longest_uniform_length(surfaces: list[str], budget: int) -> int:
      """Return only the LENGTH of the longest affordable stretch."""
      counts: dict[str, int] = {}
      left, best_count, longest = 0, 0, 0
      for right, surface in enumerate(surfaces):
          counts[surface] = counts.get(surface, 0) + 1
          best_count = max(best_count, counts[surface])
          if (right - left + 1) - best_count > budget:
              counts[surfaces[left]] -= 1
              left += 1
          longest = max(longest, right - left + 1)
      return longest
  ```

  ```text
  (["asphalt", "chipseal", "asphalt", "gravel", "asphalt", "asphalt"], 1) -> 4
  (["asphalt", "gravel", "concrete", "chipseal"], 0)                      -> 1
  ```

  Check it against `longest_uniform_stretch` on all nine cases — the lengths
  match every time. Then spend ten minutes trying to make it report the surface
  as well, and write down in your notes exactly where it defeats you. That note
  is the point of the exercise.

- **Run one window per surface instead.** Six passes, each a plain at-most-K
  window over "is this segment already the surface I care about?". Compare the
  code you get with the page's solution and decide, honestly, which you would
  rather maintain.

- **Add a per-surface price.** Suppose gravel costs one unit a segment and
  concrete costs four, and the budget is money rather than segments. The window
  invariant stops being a simple subtraction, because the cheapest target
  surface is no longer just the most common one. Work out what the new
  invariant is and whether it is still monotone under shrinking — the answer
  is not obvious, and finding out is a better use of an hour than another
  problem you already know how to do.

**Practice elsewhere.** The same pattern appears as [LeetCode 424 · Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) if you want a judge to run against. The contract there is over single characters, returns a bare length, and defines no tie-break — which is exactly why the never-decreasing trick is the standard answer to it and not to this one.

That is both challenges. Next: the [homework](../homework/README.md), then the
[mini-project](../mini-project/README.md).
