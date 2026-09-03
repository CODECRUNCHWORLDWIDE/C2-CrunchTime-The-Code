# Exercise 5 — The Market Awning

> **Topic:** converging pointers whose *move* is a greedy choice, plus the argument that the greedy choice never skips a better answer
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes, including a full FRAME narration out loud
> **Why this one:** the first medium of the week, and the first where the pointer movement is not obvious. In Exercise 3 the sum told you which pointer to move and the reason was arithmetic. Here you choose, and the proof that the choice is safe is the thing an interviewer is actually listening for. Anyone can write this loop. Far fewer can say why it works.

## The Brief

A weekly street market runs down one side of a road. Along it stands a row of
steel poles, one per stall slot, each surveyed to a height in whole metres.
Some poles are **stubs**: a snapped pole is still surveyed, still occupies
its slot in the row, and has height `0`.

The market wants to hang one rectangular **wind curtain** between **two** of
the poles — a vertical sheet along the road that blocks the low afternoon
sun and the wind coming off the water.

Three facts about how a curtain hangs, and each one is part of the arithmetic.

**It hangs level.** The curtain is lashed to both poles and its top edge is
one straight horizontal line, so that line sits at the height of the
**shorter** of the two poles. Tie it any higher and one corner has nothing to
hold it.

**It reaches the ground.** From the top edge it drops straight down. So its
height is exactly `min(height[i], height[j])` metres.

**It only spans the gap *between* the poles.** Each pole stands in a
one-metre planter that the fabric cannot cross. So a curtain between poles
`i` and `j` is `j - i - 1` metres wide — the ground strictly between them,
not the distance from pole to pole.

That last one is not a detail you can skim. It changes every answer on this
page, and it means two poles standing next to each other carry no curtain at
all: there is no gap between them to span.

Return the **largest curtain area** any single choice of two poles could
give, in square metres — width times height. If no choice yields any fabric
— too few poles, all poles adjacent, every pole snapped — return `0`.

```python
def max_curtain_area(pole_heights: list[int]) -> int:
    """Return max over i < j of min(pole_heights[i], pole_heights[j]) * (j - i - 1)."""
```

**Greedy** is the word for the shape of this algorithm. A greedy algorithm
makes the locally obvious move at each step and never goes back to
reconsider. Greedy algorithms are fast and are often wrong, so the price of
using one is being able to prove that the move you keep making cannot
discard the answer. That proof is on this page, and producing it in your own
words is the graded part.

## Starter

Save this as `exercise-05-market-awning.py` and fill in the `TODO`s.

```python
"""exercise-05-market-awning.py — the largest wind curtain on the row.

Two pointers start at the ends of the pole row, measure the curtain they
could hang, keep the best, then discard one of the two poles.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def max_curtain_area(pole_heights: list[int]) -> int:
    """Find the largest wind curtain that can hang between two poles.

    Args:
        pole_heights: Surveyed pole heights in whole metres, west to east.
            A height of 0 is a snapped stub that still occupies its slot.

    Returns:
        The largest achievable area in square metres, which is
        min(height[i], height[j]) * (j - i - 1) maximised over i < j, or 0
        when no choice of two poles yields any fabric.
    """
    # TODO: one pointer at each end of the row, and a running best of 0
    # TODO: each step, the height is the SHORTER pole and the width is the
    #       ground strictly between them — mind the - 1
    # TODO: keep the best area seen so far
    # TODO: then discard one pole and step that pointer inward. Which one?
    #       Work out the answer before you type it, and say it out loud.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(max_curtain_area([2, 6, 3, 8, 1, 7, 4]))

    assert max_curtain_area([2, 7, 5, 5, 7, 2]) == 14
    assert max_curtain_area([5, 5]) == 0
    assert max_curtain_area([]) == 0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/exercise-05-market-awning.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `max_curtain_area` returns an `int`: the largest achievable area in square
   metres.
2. The height of a curtain is `min` of the two pole heights. The width is
   `j - i - 1`.
3. Poles of height `0` are legal and are included in the row like any other.
4. Fewer than two poles returns `0`. So does a row where every choice gives
   zero fabric.
5. The function does not modify `pole_heights`.
6. `O(n)` time and `O(1)` auxiliary space. No nested loop.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(pole_heights) <= 300_000`.** Three hundred thousand poles is an
  absurd street market, deliberately. It is the bound that makes the
  all-pairs scan — around `4.5 × 10¹⁰` operations — impossible to finish, so
  the constraint itself forces the linear solution. Say that out loud when
  you pick the pattern, because "I chose `O(n)` because the constraint
  demanded it" is a much better answer than "I chose `O(n)` because faster is
  better."

- **`0 <= pole_heights[i] <= 12`, in metres.** Zero is legal and means a
  snapped stub; a solution that assumes every pole has positive height is
  caught by the all-stubs example below. The *upper* bound is deliberately
  tiny, and that is the interesting half: with only thirteen possible
  heights, **ties are common**. A careless rule for which pointer to move
  when the two heights are equal survives a small hand-trace and dies on a
  large input, so the tiny bound is what surfaces it.

- **The width is `j - i - 1`, not `j - i`.** It is never negative, because
  `i < j`. This is a constraint rather than a note because it is load-bearing
  in both directions: it changes every numeric answer, and it makes the
  adjacent-pole case come out as `0` instead of the shorter pole's height.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-05-market-awning-solution.py
best area  18 sq m   poles [2, 6, 3, 8, 1, 7, 4]
best area  14 sq m   poles [2, 7, 5, 5, 7, 2]
best area   0 sq m   poles [5, 5]
best area   0 sq m   poles [0, 9, 9, 0]
best area   0 sq m   poles [4]
best area   0 sq m   poles []
All checks passed.
```

**Line 1** is the reason this problem needs an algorithm rather than a rule of
thumb. The best pair is poles 1 and 5: the shorter is 6 m and there are
`5 - 1 - 1 = 3` metres of ground between them, giving 18. Now check the two
obvious heuristics. The *widest* pair, poles 0 and 6, gives
`min(2, 4) * 5 = 10`. The *tallest* pair, poles 3 and 5, gives
`min(8, 7) * 1 = 7`. Neither heuristic finds the answer, and the winner is
neither the widest nor the tallest choice.

**Line 2** is the example that punishes moving the taller pointer. The best
pair is 1 and 4: `min(7, 7) * 2 = 14`. Move the *taller* side inward at each
step and you walk away from both 7 m poles and report `8`, the area of the
outermost pair. The code compiles, the trace looks reasonable, and the answer
is wrong. Trace it both ways.

**Line 3** is the degenerate case and the one that punishes the `j - i` width
formula. Two perfectly good 5 m poles, standing next to each other, shading
exactly zero usable ground. If your answer is `5`, go back and re-read the
width definition.

**Line 4** is the no-solution case. Every pair either includes a snapped stub
— height `0`, so area `0` — or is the adjacent pair of 9 m poles, width `0`.
A solution that skips zero-height poles as "missing survey data" still lands
on `0` here by luck; one that assumes at least one pair yields fabric does
not.

## Steps

1. Save the starter and run it. `AssertionError`.
2. Put `left` at `0`, `right` at the last position, and `best` at `0`.
3. Loop `while left < right`. Compute the height as the `min` of the two
   poles and the width as `right - left - 1`. Multiply.
4. Keep the larger of that and `best`.
5. Now the decision. Before you write it, answer this out loud: *if the left
   pole is the shorter one, could any pair that still uses it beat the pair I
   just measured?* Work it out; do not guess. The answer is in the next
   section, but guessing first is the exercise.
6. Move the pointer standing on the shorter pole one step inward.
7. Return `best`. Run the file.
8. Build a trace table for `[2, 6, 3, 8, 1, 7, 4]` with columns `left`,
   `right`, the two heights, the width, the area and `best`. Confirm you
   reach `18`. Then trace `[2, 7, 5, 5, 7, 2]` correctly, and again with the
   taller-side rule, so you watch it produce `14` and `8`.

## The argument you must be able to make

Say something equivalent to this, in your own words, without reading it off
the page:

> Suppose the left pole is strictly shorter than the right one. The pair I
> just measured has area `h[left] * (right - left - 1)`. Now consider any
> *other* pair that still uses `left` — that is, `left` together with some
> pole `right'` somewhere between them. Its width, `right' - left - 1`, is
> strictly smaller, because `right'` is closer. Its height,
> `min(h[left], h[right'])`, is at most `h[left]`, because a minimum
> involving `h[left]` cannot exceed it. So both factors are no larger and one
> of them is strictly smaller: every remaining pair that uses `left` has a
> strictly smaller area than the one I just measured. Nothing is lost by
> discarding `left`, so I discard it. The argument is symmetric when the
> right pole is the shorter one, and when the two are equal it applies to
> whichever one I choose to move.

Being able to say that in an interview is the difference between "solved it"
and "demonstrated mastery." Write it in your own sentences — if your write-up
reads like the paragraph above word for word, you copied instead of
understanding, and it will not survive a follow-up question.

## The Solution

```python
"""exercise-05-market-awning-solution.py — the largest wind curtain on the row.

Two pointers start at the ends of the pole row, measure the curtain they
could hang, keep the best, then discard the shorter pole. Discarding the
shorter pole is safe because every remaining pair that still uses it is
narrower and no taller.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def max_curtain_area(pole_heights: list[int]) -> int:
    """Find the largest wind curtain that can hang between two poles.

    Args:
        pole_heights: Surveyed pole heights in whole metres, west to east.
            A height of 0 is a snapped stub that still occupies its slot.

    Returns:
        The largest achievable area in square metres, which is
        min(height[i], height[j]) * (j - i - 1) maximised over i < j, or 0
        when no choice of two poles yields any fabric.
    """
    left, right = 0, len(pole_heights) - 1
    best = 0
    while left < right:
        height = min(pole_heights[left], pole_heights[right])
        area = height * (right - left - 1)
        if area > best:
            best = area
        if pole_heights[left] < pole_heights[right]:
            left += 1
        else:
            right -= 1
    return best


# ---- Self-check ----
if __name__ == "__main__":
    rows = [
        [2, 6, 3, 8, 1, 7, 4],
        [2, 7, 5, 5, 7, 2],
        [5, 5],
        [0, 9, 9, 0],
        [4],
        [],
    ]
    for poles in rows:
        print(f"best area {max_curtain_area(poles):>3} sq m   poles {poles}")

    assert max_curtain_area([2, 6, 3, 8, 1, 7, 4]) == 18
    assert max_curtain_area([2, 7, 5, 5, 7, 2]) == 14
    assert max_curtain_area([5, 5]) == 0
    assert max_curtain_area([0, 9, 9, 0]) == 0
    assert max_curtain_area([4]) == 0
    assert max_curtain_area([]) == 0
    print("All checks passed.")
```

**The `best` variable is genuinely needed here, and in Exercise 3 it was
not.** That contrast is worth holding on to. In Exercise 3 the traversal
order *was* the selection rule, so the first match was the answer. Here the
loop visits `n - 1` pairs in no particular order of area, so it has to
remember the largest it has seen. Knowing which situation you are in — "the
order gives me the answer" versus "I have to keep score" — is a real
distinction and it is easy to get backwards.

**Exactly one pointer moves per iteration, so the loop runs at most `n - 1`
times.** They start `n - 1` apart and the gap closes by one each step. That
is where the `O(n)` comes from, and it is the same accounting as every other
converging-pointer problem this week.

**The tie rule does not matter, and you should say so rather than hoping.**
When the two poles are exactly equal the argument above applies to either
one, so `else: right -= 1` and `else: left += 1` are equally correct. What
matters is that you *make* a choice and can defend it. With heights capped at
12 metres, ties are common, so a candidate who has not thought about the
equal case is about to find out the hard way.

**The width is `right - left - 1` and it is written once.** There is no
temptation to write it twice here, which is the point: compute the area in
one place, from one formula, so that the `- 1` cannot be right in one branch
and wrong in another.

**`while left < right` keeps a pole from pairing with itself.** With `<=`,
the pointers eventually stand on the same pole and the width becomes
`-1`, turning a positive height into a **negative** area. On this page that
happens to be harmless, because `best` starts at `0` and a negative never
beats it — but "harmless because of an unrelated detail" is not the same as
"correct", and the moment someone changes `best` to start at the first area
computed, it stops being harmless.

**Every degenerate row falls out without a special case.** One pole: `right`
is `0`, `0 < 0` is false, the loop never runs, `best` is `0`. Empty row:
`right` is `-1`, same. All stubs: every height is `0`, so every area is `0`.
Adjacent poles only: every width is `0`. Four different reasons, one return
value, no guards — and being able to enumerate the four is a better answer
than "it handles edge cases."

## Download and run

Download
[exercise-05-market-awning-solution.py](./exercise-05-market-awning-solution.py)
and run it:

```bash
python exercise-05-market-awning-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-05-market-awning.py`.

## Common bugs to catch

- **A bare `AssertionError` on `[5, 5]`.** You used `right - left` as the
  width:

  ```text
  Traceback (most recent call last):
      assert max_curtain_area([5, 5]) == 0
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Your function returned `5` — a curtain hung between two poles with no
  ground between them. Every other answer on the page is wrong too, by
  varying amounts, which is why this bug is worth catching on the smallest
  input rather than the largest.

- **A bare `AssertionError` on `[2, 7, 5, 5, 7, 2]`.** You moved the taller
  pole inward:

  ```text
  Traceback (most recent call last):
      assert max_curtain_area([2, 7, 5, 5, 7, 2]) == 14
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Your function returned `8`. Nothing crashed, the loop terminated, the
  complexity is the same — and it walked away from both 7 m poles on the
  first step, because it kept the short outer poles and threw away the tall
  inner ones. This is what an unproved greedy move looks like when it fails:
  quietly, with a plausible number.

- **Forgetting to keep the best.** Returning the last area computed, or the
  area at the moment the loop exits. On line 1 of the expected output that
  gives a small number from a narrow pair near the middle. If your answers
  are consistently too small and always come from a late iteration, this is
  it.

- **Skipping zero-height poles.** A stub still occupies a slot and still
  counts toward the distance between two other poles. Removing it from the
  row would shorten every width that spans it, so on
  `[9, 0, 0, 0, 9]` a filtered row reports the two 9 m poles as adjacent and
  returns `0` instead of `27`.

- **A nested loop.** No exception on the six small examples — it gives the
  right answer on every one of them, quickly. On a row of three hundred
  thousand poles it does not finish. If you wrote a nested loop, you missed
  the pattern *and* the constraint that rules it out. Stop and redo the plan
  rather than optimising the loop you have.

- **`while left <= right`.** The self-paired pole gives a negative area:

  ```text
  min(5, 5) * (0 - 0 - 1) = -5
  ```

  On this page `best` starts at `0` so the negative is swallowed. Rely on
  that and you have written code that is correct for a reason you did not
  choose.

- **Returning the pair instead of the area.** Read the signature. The market
  wants a number of square metres, not two pole numbers.

## Under the hood

<details>
<summary>Under the hood — what the greedy move really discards, and why the -1 is not a detail</summary>

**Restating the proof as an invariant.**

Call a pair *live* if both its poles are still inside the window
`[left, right]`. The loop maintains: **the best area over all pairs is either
already recorded in `best`, or is the area of some live pair.**

It holds at the start, because every pair is live. It survives an iteration:
suppose `h[left] < h[right]`. We record the area of `(left, right)` into
`best`. Every other pair using `left` is `(left, right')` with
`left < right' < right`, and its area is
`min(h[left], h[right']) * (right' - left - 1)`, which is at most
`h[left] * (right' - left - 1)`, which is strictly less than
`h[left] * (right - left - 1)` — the area we just recorded. So every pair
using `left` is already beaten by something in `best`, and dropping `left`
from the window loses nothing. Symmetric on the other side.

When the loop ends, no live pairs remain, so the best area over all pairs is
in `best`. That is the whole correctness proof, and it fits in a paragraph.

**How many pairs does it actually skip?**

There are `n(n-1)/2` pairs and the loop examines `n - 1` of them. On three
hundred thousand poles that is about forty-five billion pairs skipped in
favour of three hundred thousand examined. The proof is what buys that, and
it is why "prove the greedy move" is not an academic exercise — it is the
only thing standing between this solution and a wrong answer nobody notices.

**Why the `- 1` is not cosmetic.**

Change the width to `j - i` and the problem becomes a different one with
different answers everywhere — but the *algorithm* still works, because the
proof only ever used two facts: that width shrinks as the pointers close in,
and that height is bounded by the shorter pole. Both survive the change. So
the `- 1` is load-bearing for the arithmetic and irrelevant to the reasoning,
and separating those two things is a useful habit. When an interviewer adds a
twist to a problem, the first question is always which part of your argument
the twist actually disturbs.

**What makes greedy safe in general.**

Greedy algorithms need an *exchange argument*: a proof that any optimal
solution can be transformed into one that agrees with your greedy choice,
without getting worse. Here the transformation is trivial — you are not
choosing which pair to keep, you are choosing which pole to discard, and you
have shown the discarded pole cannot appear in the winner. Week 10 does
intervals and greedy properly, and the same shape of argument comes back:
show that the thing you are throwing away could not have been in the answer.

**The other two solutions, for completeness.**

The `O(n²)` all-pairs scan is easy to write and easy to defend as correct.
It is ruled out by the bound, not by taste. There is no useful `O(n log n)`
middle ground for this problem — unlike Exercise 3, where sorting would be
the fallback, sorting the poles here destroys the positions that the width
depends on. So the choice is genuinely between the quadratic scan and the
linear one, which is why the greedy proof is not optional.

</details>

## Acceptance checklist

- [ ] `python exercise-05-market-awning.py` prints `18`, then `All checks passed.`
- [ ] The width in your code is `right - left - 1`, and it appears exactly once.
- [ ] You move the pointer on the **shorter** pole, and you can prove that is safe without reading this page.
- [ ] You decided what happens when the two heights are equal, and you can say why either choice is correct.
- [ ] `[5, 5]`, `[0, 9, 9, 0]`, `[4]` and `[]` all return `0`, and you can give the *different* reason for each.
- [ ] Your trace table for `[2, 6, 3, 8, 1, 7, 4]` shows `left`, `right`, both heights, the width, the area and `best`.
- [ ] Your write-up records what the taller-side rule returns on `[2, 7, 5, 5, 7, 2]`, and why that is a wrong answer rather than a slower one.
- [ ] There is no nested loop anywhere in your solution.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 1 exercise 5: market awning`.
## Stretch

- **Return which two poles win, not just the area.**

  ```python
  def best_curtain_pair(pole_heights: list[int]) -> tuple[int, int, int]:
      """Return (left_pole, right_pole, area) for the largest curtain, or (-1, -1, 0)."""
      left, right = 0, len(pole_heights) - 1
      best = (-1, -1, 0)
      while left < right:
          area = min(pole_heights[left], pole_heights[right]) * (right - left - 1)
          if area > best[2]:
              best = (left, right, area)
          if pole_heights[left] < pole_heights[right]:
              left += 1
          else:
              right -= 1
      return best
  ```

  ```text
  [2, 6, 3, 8, 1, 7, 4] -> (1, 5, 18)
  [2, 7, 5, 5, 7, 2]    -> (1, 4, 14)
  [0, 9, 9, 0]          -> (-1, -1, 0)
  ```

  Note the sentinel on the last line, and note that this function now has the
  problem Exercise 3 warned you about: `(-1, -1, 0)` is a tuple you can
  confuse with a real answer if you are careless. Decide whether you would
  ship it or return `None`, and defend the choice.

- **Two curtains instead of one.** The market wants to hang two curtains that
  do not overlap, maximising the total area. Do not write it yet — first work
  out whether the greedy move still holds, and convince yourself one way or
  the other. This is a much harder problem than it looks, and recognising
  *that* is the skill being trained.

- **Cap the curtain height.** The fabric only comes in a certain drop, say
  four metres, so the height is `min(min(h[i], h[j]), max_drop)`. Work out
  which parts of the greedy proof still hold. Challenge 2 this week does the
  same trick to a harder problem, so the reasoning transfers directly.

After the five exercises, take the [quiz](../quiz.md), then start the
[homework](../homework/README.md) and the
[mini-project](../mini-project/README.md). If you want more, the
[challenges](../challenges/README.md) are where the week gets hard.
