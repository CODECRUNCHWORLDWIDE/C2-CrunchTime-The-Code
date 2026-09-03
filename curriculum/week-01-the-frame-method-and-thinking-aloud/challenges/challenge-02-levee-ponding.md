# Challenge 2 — Ponding on the Levee Road

> **Topic:** converging pointers carrying one running maximum on each side, so that two integers replace two whole precomputed arrays
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Hard
> **Target time:** 120 minutes
> **Why this one:** the loop invariant here is genuinely non-obvious. Most engineers solve this shape once with two precomputed arrays and only meet the constant-space version years later. We are doing the constant-space version now, and we are going to justify it rather than remember it. It is also the canonical "looks like dynamic programming, is actually two pointers" problem, which is why senior interviewers reach for it.

## The Brief

A flood district surveys the service road that runs along the top of a levee.
The road is measured in one-metre sections, and the survey gives the **crown
height** of each section — how high the middle of the road sits, in
centimetres above the district's **datum**, a fixed reference height agreed
once and never moved. The list runs west to east, so section 0 is the western
end.

After rain, water ponds in the dips. Think of a bathtub. The water line in a
bathtub is set by its **lowest rim** — fill it past that and the rest runs
over the side. A section of road works the same way: it holds water up to the
level of the lower of the two highest crowns on either side of it. And water
sitting at the very ends of the road, with nothing beyond it to hold it in,
simply runs off.

There is one more thing, and it is the part that is not standard. The road is
**cambered**: it is deliberately built with a crossfall so that water sheets
off the shoulder instead of sitting on the asphalt. So each section can hold
at most `shoulder` centimetres of depth. Anything deeper spills over the side
and down the levee face, where it is the levee's problem and not the road's.

Each section is one metre long and one metre wide, so a section holding `d`
centimetres of depth holds `d` units of volume. Return the **total ponded
volume** across the whole road, in section-centimetres.

```python
def ponded_volume(crown: list[int], shoulder: int) -> int:
    """Return the total water held on the road after rain."""
```

Written out, the water at section `i` is:

```text
min( min(highest crown at or west of i, highest crown at or east of i) - crown[i],
     shoulder )
```

never less than zero. The answer is that quantity summed over every section.

Note where the camber sits in that formula. It is a **per-section** cap
applied to that section's own depth. It has nothing to do with the rims and
it is not a cap on the total. Keeping those two straight is most of this
problem.

## Starter

Save this as `challenge-02-levee-ponding.py` and fill in the `TODO`s.

```python
"""challenge-02-levee-ponding.py — water held on a cambered levee road.

Two pointers walk inward from the ends of the survey, carrying one running
maximum each.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def ponded_volume(crown: list[int], shoulder: int) -> int:
    """Total the water held on the road after rain.

    Args:
        crown: Crown height of each one-metre section in centimetres above
            datum, west to east. A crown of 0 is a real section at datum.
        shoulder: The camber's per-section depth cap in centimetres.
            A shoulder of 0 sheds every drop and is a legal input.

    Returns:
        The total ponded volume in section-centimetres.
    """
    # TODO: a pointer at each end, a running maximum for each side starting
    #       at 0, and a running total
    # TODO: each step, process whichever side stands on the LOWER crown —
    #       because for that section you already know which rim binds
    # TODO: update that side's running maximum BEFORE you add, so the
    #       quantity you add can never be negative
    # TODO: cap each section's depth at `shoulder`, unconditionally
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(ponded_volume([4, 1, 3, 0, 2, 5], 100), ponded_volume([4, 1, 3, 0, 2, 5], 2))

    assert ponded_volume([8, 0, 5, 0, 8], 3) == 9
    assert ponded_volume([1, 5, 2, 6, 3], 100) == 3
    assert ponded_volume([2, 0, 2], 5) == 2
    assert ponded_volume([], 100) == 0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/challenges/challenge-02-levee-ponding.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `ponded_volume` returns an `int`: the total ponded volume in
   section-centimetres.
2. Each section's depth is capped at `shoulder`, **individually**. The cap is
   never applied to the total.
3. The cap is applied unconditionally, including when it does not bind.
4. Water at either end of the road runs off, so the two end sections never
   contribute.
5. A crown of `0` is a real section at datum, not missing data.
6. `shoulder = 0` returns `0` for any road.
7. Empty, one-section and two-section roads all return `0` without a guard,
   and you can say why.
8. `O(n)` time and `O(1)` auxiliary space. No precomputed arrays.
9. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(crown) <= 1_000_000`.** A million one-metre sections is a
  thousand kilometres of levee-top road, which is the scale of a real
  river-system levee network. This bound does two jobs at once, and you
  should name both. It makes the `O(n²)` solution — for each section, scan
  west for the highest crown and east for the highest crown — about `10¹²`
  operations, which is hopeless. And it makes the `O(n)`-space solution,
  which precomputes two million-entry running-maximum lists, cost tens of
  megabytes in CPython on a field machine that does not have them. **This
  challenge grades `O(n)` time and `O(1)` auxiliary space**, and the second
  half of the bound is what rules out the middle answer.

- **`0 <= crown[i] <= 5_000`, in centimetres above datum.** Heights are never
  negative, because the datum is defined as the lowest surveyed point on the
  network. That is why the running maxima can safely start at `0` — no real
  crown is below it. It also means **a crown of `0` is a genuine section at
  datum**, and a solution that treats zeros as gaps and skips them gets
  `[2, 0, 2]` wrong.

- **`0 <= shoulder <= 5_000`, in centimetres.** `shoulder = 0` is legal and
  meaningful: a fully cambered road sheds every drop, and the answer is `0`
  however deep the dips are. It is the degenerate case that catches a
  solution which only applies the cap when it decides the cap is "small
  enough to matter."

## The three solutions, in order of increasing merit

Say all three out loud before you write any code. An interviewer wants to
hear that you know what you are choosing between, and this is the problem
where that is worth the most.

**`O(n²)` time, `O(1)` space.** For each section `i`, scan west for the
highest crown at or before `i`, scan east for the highest crown at or after
`i`, take the smaller of the two, subtract `crown[i]`, clamp at zero, clamp at
`shoulder`, and add it up. Easy to write, easy to defend as correct, ruled out
by the bound.

**`O(n)` time, `O(n)` space.** Precompute `west_max[i]`, the running maximum
from the west end, and `east_max[i]` from the east end. Then one pass adds
`min(min(west_max[i], east_max[i]) - crown[i], shoulder)` at each section.
This is what most candidates produce first, and on a road of ordinary length
it is a perfectly good answer that you should be willing to defend. It is not
the answer for a million sections on a field machine.

**`O(n)` time, `O(1)` space.** The two-pointer version. **This is what we
want.**

## The two-pointer insight

Keep two pointers, `west` and `east`, moving inward, and two **single
integers** — not lists — `west_max` and `east_max`, holding the highest crown
seen so far from each side.

At each step, look at the two sections the pointers stand on and process
**the lower one**.

Suppose `crown[west] < crown[east]`. Then somewhere to the east there is a
crown at least as high as `crown[east]`, which is strictly higher than
`crown[west]`. So for the *western* section, the eastern rim is not what
limits the water — the western rim is, because it is the smaller of the two.
Which means `west_max` alone decides the water line at `west`, and we do not
need to know anything more about the east. Update `west_max` to include
`crown[west]`, add `min(west_max - crown[west], shoulder)`, and step `west`
inward.

Otherwise it is symmetric: update `east_max`, add
`min(east_max - crown[east], shoulder)`, and step `east` inward.

The invariant is: **at every step, for whichever side we choose to process,
we already know its bottleneck.** That is why two integers suffice where the
array version needed two lists.

Note where the camber fits. The cap is a per-section limit applied to that
section's depth alone. It does not interact with the rims at all, so it slots
into the formula and leaves the invariant completely untouched. Say that
sentence out loud — an interviewer adding a twist to a known problem is
checking whether you can tell which parts of your reasoning the twist
actually disturbs.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python challenge-02-levee-ponding-solution.py
shoulder 100 cm  holds 10  road [4, 1, 3, 0, 2, 5]
shoulder   2 cm  holds  7  road [4, 1, 3, 0, 2, 5]
shoulder   0 cm  holds  0  road [4, 1, 3, 0, 2, 5]
shoulder 100 cm  holds  3  road [1, 5, 2, 6, 3]
shoulder   3 cm  holds  9  road [8, 0, 5, 0, 8]
shoulder 100 cm  holds  0  road [9, 6, 4, 1]
shoulder 100 cm  holds  0  road [3, 3, 3]
shoulder   5 cm  holds  2  road [2, 0, 2]
shoulder 100 cm  holds  6  road [3, 0, 0, 3]
shoulder 100 cm  holds  0  road [7, 2]
shoulder 100 cm  holds  0  road [7]
shoulder 100 cm  holds  0  road []
All checks passed.
```

The first three lines are the same road three times, and they isolate the
camber. With a 100 cm shoulder nothing is capped: the water line across
sections 1 to 4 is set by the crown of `4` on the west, because the `5` on
the east is higher, so the depths are `3, 1, 4, 2` and the total is `10`.
Drop the shoulder to `2` and those same four depths clip to `2, 1, 2, 2`,
total `7` — two of the four sections lose water over the side. Drop it to `0`
and the road sheds everything. Trace all three before you write anything.

**Line 4**, `[1, 5, 2, 6, 3]`, is the one to trace second. Only section 2
holds water, three centimetres of it, held between the `5` to its west and
the `6` to its east. This example exercises **both branches** of the pointer
move — the first step processes the west side, the second processes the east
— where the earlier examples only ever process one. If your `if`/`else`
ordering is wrong, the first three lines can still pass and this one will
not.

**Line 5**, `[8, 0, 5, 0, 8]` with a 3 cm shoulder, is the example that
punishes applying the cap to the total. Uncapped this road holds
`8 + 3 + 8 = 19`. With a 3 cm camber every one of the three dips clips to
`3`, giving `9`. Cap the total instead and you get `3`.

**Line 6**, `[9, 6, 4, 1]`, is a road that only ever descends. There is no
eastern rim anywhere, so nothing is held. This catches a solution that adds
`west_max - crown[i]` without ever consulting the other side.

**Line 8**, `[2, 0, 2]`, is the smallest road that holds anything at all. If
it returns `0`, your `<` versus `<=` on the pointer comparison is sending
equal-height rims down a branch that never adds.

## Steps

1. Save the starter and run it. `AssertionError`.
2. Set `west = 0`, `east = len(crown) - 1`, `west_max = east_max = 0`,
   `total = 0`.
3. Loop `while west < east`.
4. Compare `crown[west]` against `crown[east]`. If the western crown is
   strictly lower, take the western branch; otherwise the eastern one.
5. In the western branch, **update `west_max` first**, then add
   `min(west_max - crown[west], shoulder)`, then `west += 1`. Doing the
   update first is what makes the added quantity non-negative by
   construction, so you never need a `max(0, ...)` clamp.
6. Mirror it in the eastern branch.
7. Return `total`.
8. Now trace `[4, 1, 3, 0, 2, 5]` with `shoulder = 100` and again with
   `shoulder = 2`, writing down `west`, `east`, `west_max`, `east_max` and
   `total` at every iteration. Then trace `[1, 5, 2, 6, 3]`, the one that
   uses both branches. Then the three degenerate roads.

## The Solution

```python
"""challenge-02-levee-ponding-solution.py — water held on a cambered levee road.

Two pointers walk inward from the ends of the survey, carrying one running
maximum each. At every step the lower of the two sections is processed,
because for that section the near rim is already known to be the binding
one. Two integers replace the two million-entry arrays the obvious solution
would build.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def ponded_volume(crown: list[int], shoulder: int) -> int:
    """Total the water held on the road after rain.

    Args:
        crown: Crown height of each one-metre section in centimetres above
            datum, west to east. A crown of 0 is a real section at datum.
        shoulder: The camber's per-section depth cap in centimetres.
            A shoulder of 0 sheds every drop and is a legal input.

    Returns:
        The total ponded volume in section-centimetres.
    """
    west, east = 0, len(crown) - 1
    west_max = east_max = 0
    total = 0

    while west < east:
        if crown[west] < crown[east]:
            west_max = max(west_max, crown[west])
            total += min(west_max - crown[west], shoulder)
            west += 1
        else:
            east_max = max(east_max, crown[east])
            total += min(east_max - crown[east], shoulder)
            east -= 1

    return total


# ---- Self-check ----
if __name__ == "__main__":
    surveys = [
        ([4, 1, 3, 0, 2, 5], 100),
        ([4, 1, 3, 0, 2, 5], 2),
        ([4, 1, 3, 0, 2, 5], 0),
        ([1, 5, 2, 6, 3], 100),
        ([8, 0, 5, 0, 8], 3),
        ([9, 6, 4, 1], 100),
        ([3, 3, 3], 100),
        ([2, 0, 2], 5),
        ([3, 0, 0, 3], 100),
        ([7, 2], 100),
        ([7], 100),
        ([], 100),
    ]
    for crown, shoulder in surveys:
        held = ponded_volume(crown, shoulder)
        print(f"shoulder {shoulder:>3} cm  holds {held:>2}  road {crown}")

    assert ponded_volume([4, 1, 3, 0, 2, 5], 100) == 10
    assert ponded_volume([4, 1, 3, 0, 2, 5], 2) == 7
    assert ponded_volume([4, 1, 3, 0, 2, 5], 0) == 0
    assert ponded_volume([1, 5, 2, 6, 3], 100) == 3
    assert ponded_volume([8, 0, 5, 0, 8], 3) == 9
    assert ponded_volume([9, 6, 4, 1], 100) == 0
    assert ponded_volume([3, 3, 3], 100) == 0
    assert ponded_volume([2, 0, 2], 5) == 2
    assert ponded_volume([3, 0, 0, 3], 100) == 6
    assert ponded_volume([7, 2], 100) == 0
    assert ponded_volume([7], 100) == 0
    assert ponded_volume([], 100) == 0
    print("All checks passed.")
```

**Processing the lower side is safe, and here is the argument in one
paragraph.** Say `crown[west] < crown[east]`. The true water line at section
`west` is `min(true_west_max, true_east_max)`, where those are the highest
crowns over the whole road on each side. We do not know `true_east_max`, but
we know it is at least `crown[east]`, which is strictly greater than
`crown[west]`. We also know `west_max` is exactly `true_west_max` for this
section, because the western pointer has already walked past every section
west of it. So either `west_max <= crown[east] <= true_east_max`, in which
case `west_max` is the minimum and is the right answer — or `west_max` is
larger, in which case `west_max > crown[east] > crown[west]` and the water at
`west` is limited by the east instead. That second case cannot happen while
we are taking this branch, because the branch condition compares crowns, not
maxima. Work through why, out loud, until you believe it: it is the one step
of this proof that people skip.

**Updating the running maximum before adding is what removes the clamp.**
After `west_max = max(west_max, crown[west])`, the value `west_max` is at
least `crown[west]`, so `west_max - crown[west]` is zero or positive by
construction. Reverse the two lines and the quantity goes negative every time
the pointer stands on a new high point, and you need a `max(0, ...)` to patch
it. Getting the order right means the code has one fewer thing in it and one
fewer thing to be wrong.

**The cap is applied unconditionally and to each section separately.**
`min(..., shoulder)` costs one comparison when the cap does not bind, and
writing `if shoulder < something: apply cap` buys nothing while creating a
branch that behaves differently on inputs nobody tested. Applying it to the
total instead is a different problem entirely — line 5 of the expected output
is `9` and the total-cap version says `3`.

**Two integers replace two lists, and that is the entire win.** The array
version stores a running maximum for every section because it does not know,
at the time it builds them, which sections will need which. The pointer
version discovers that it only ever needs the running maximum *on the side it
is currently processing*, and that side's maximum is a single number it has
been carrying all along. A million sections of `int` in a CPython list is
tens of megabytes; two integers is thirty-odd bytes.

**`while west < east`, and the meeting section holds nothing.** With `<`, the
section where the pointers would meet is never processed at all. That is
correct, and the reason is worth knowing: the pointers always advance away
from the lower crown, so the section they converge on is a highest section on
the road — and a highest section has no rim above it on either side, so it
holds no water. Writing `<=` therefore gives the same answer here, because
the extra iteration adds `min(east_max - crown[m], shoulder)` where
`east_max` has just been updated to `crown[m]` itself, which is zero. Knowing
that it is harmless *and why* is a much better answer than assuming it is.

**Every degenerate road falls out by construction.** Empty road: `east`
starts at `-1`, `0 < -1` is false, the loop never runs, `0` comes back.
One section: `east` is `0`, same. Two sections: one iteration runs, the
processed section is an end section, its running maximum equals its own crown,
so it adds zero. Flat road: every crown equals every running maximum, so
every addition is zero. Descending road: the eastern branch runs every time
and `east_max` is always the current crown. Five different reasons, one
return value, and no guards — say which reason applies to which road rather
than saying "it handles edge cases."

**Complexity.** Exactly one pointer moves per iteration and they start `n - 1`
apart, so the loop runs at most `n - 1` times: **`O(n)` time**. The state is
four integers regardless of road length: **`O(1)` auxiliary space**. And
`O(n)` time is the floor, because a single section anywhere on the road can
change the answer, so every section must be read.

## Download and run

Download
[challenge-02-levee-ponding-solution.py](./challenge-02-levee-ponding-solution.py)
and run it:

```bash
python challenge-02-levee-ponding-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-02-levee-ponding.py`.

## Common bugs to catch

- **A bare `AssertionError`, with a total that is too small.** You added
  before updating the running maximum:

  ```text
      [4, 1, 3, 0, 2, 5] shoulder 100 -> 6
  ```

  ```text
  Traceback (most recent call last):
      assert ponded_volume([4, 1, 3, 0, 2, 5], 100) == 10
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  On the first western step, `west_max` is still `0` while `crown[west]` is
  `4`, so `west_max - crown[west]` is `-4`, and `min(-4, 100)` is `-4`. The
  negative silently eats four centimetres of real water later in the sum.
  Update first; then the quantity is non-negative by construction and no
  clamp is needed.

- **A bare `AssertionError` on `[8, 0, 5, 0, 8]`.** You capped the total
  instead of each section:

  ```text
      [8, 0, 5, 0, 8] shoulder 3 -> 3
  ```

  ```text
  Traceback (most recent call last):
      assert ponded_volume([8, 0, 5, 0, 8], 3) == 9
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `min(total, shoulder)` at the end is a different problem. The camber is a
  property of one metre of road, not of the road.

- **A bare `AssertionError` on `[2, 0, 2]`.** You filtered zero-crown
  sections out as missing survey data:

  ```text
      [2, 0, 2] shoulder 5 -> 0
  ```

  ```text
  Traceback (most recent call last):
      assert ponded_volume([2, 0, 2], 5) == 2
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  A crown of `0` is a real section sitting exactly at datum, and it is the
  only section on that road that holds anything. Removing it leaves
  `[2, 2]`, two adjacent rims with no dip between them.

- **`IndexError: list index out of range` on the empty road.** You seeded the
  running maxima from the ends of the list:

  ```text
  Traceback (most recent call last):
      ponded_volume([], 100)
      west_max, east_max = crown[0], crown[-1]
                           ~~~~~^^^
  IndexError: list index out of range
  ```

  Seed them at `0` instead. The constraint says no crown is below datum, so
  `0` is a safe floor and it costs you nothing — and it removes the only
  place in the function that could have raised.

- **Skipping the cap when `shoulder` looks large.** A branch like
  `if shoulder < 100: apply cap` passes every example where the cap does not
  bind and quietly changes behaviour elsewhere. There is nothing to save
  here: `min(a, b)` on two integers is one comparison.

- **Wrong comparison direction.** `crown[west] < crown[east]` sends the
  equal-crown case into the eastern branch. That is correct, but only because
  the two branches are symmetric — verify it on `[2, 0, 2]` and `[3, 0, 0, 3]`
  rather than assuming it.

- **Assuming a minimum road length.** The empty road and the one-section road
  both return `0` with no special case, and that is correct by construction
  rather than by luck. Say which it is; a guard you add "to be safe" on a
  branch that can never execute is a small lie in your code.

## Under the hood

<details>
<summary>Under the hood — the invariant written out, and how to check a clever solution against a dumb one</summary>

**The invariant, precisely.**

At the top of every iteration:

1. `west_max` is the highest crown over `crown[0 .. west - 1]`, or `0` if
   that range is empty.
2. `east_max` is the highest crown over `crown[east + 1 .. n - 1]`, or `0`.
3. `total` is the exact ponded volume of every section already processed.

Properties 1 and 2 are maintained by the `max` call at the top of each
branch. Property 3 is the one that needs the argument in *The Solution*
above: for the side being processed, the running maximum on that side is
already the binding rim, so the depth computed there is final and will never
need revisiting.

That last clause is what makes constant space possible. In the array version
you keep every running maximum because you do not know in advance which
sections need which. Here, the *order* in which you process sections is
chosen precisely so that each section's answer is already determined when you
reach it.

**Why "process the lower side" is the right choice and not merely a working
one.**

The rule is not arbitrary and it is not a heuristic. Take the section with
the lower crown of the two. Its far-side rim is guaranteed to be at least as
high as the other pointer's crown, which is higher than its own. So the far
rim can never be the binding constraint *unless* the near rim is higher
still — and in that case the near rim is what you would be comparing against
anyway. Either way the near side's running maximum, capped by nothing else,
gives the correct water line. Take the *higher* side instead and that
guarantee evaporates: you would be computing a depth against a rim you have
not finished discovering.

**Cross-checking a clever solution against an obviously-correct one.**

This is the single most useful testing technique on this page, and it
generalises to every problem with a non-obvious invariant. Write the
straightforward `O(n)`-space two-array version, generate a few thousand
random roads and shoulders, and assert that the two agree on every one:

```python
import random

def ponded_volume_arrays(crown: list[int], shoulder: int) -> int:
    """The obviously-correct O(n)-space version, for cross-checking only."""
    n = len(crown)
    if n == 0:
        return 0
    west_max = [0] * n
    east_max = [0] * n
    running = 0
    for i in range(n):
        running = max(running, crown[i])
        west_max[i] = running
    running = 0
    for i in range(n - 1, -1, -1):
        running = max(running, crown[i])
        east_max[i] = running
    return sum(min(min(west_max[i], east_max[i]) - crown[i], shoulder) for i in range(n))

for _ in range(5000):
    road = [random.randint(0, 12) for _ in range(random.randint(0, 15))]
    cap = random.choice([0, 1, 3, 100])
    assert ponded_volume(road, cap) == ponded_volume_arrays(road, cap), (road, cap)
```

Silence means five thousand agreements. The slow version is easy to believe
because it is a direct transcription of the formula in the brief; the fast
one is not. Testing the one you doubt against the one you do not is worth
more than any number of hand-picked examples.

Note that the array version also earns its keep as an *answer*. If a
follow-up asked for the per-section depths rather than the total, the arrays
are already there and the pointer version cannot produce them without
rethinking. Say that when you compare the two: constant space is not free,
it costs you the intermediate results.

**Why this problem is asked.**

It separates candidates who recall a solution from candidates who can hold an
invariant in their head and reason about it. Adding the camber is our way of
making sure it is the second thing being tested — a remembered solution
returns the uncapped total, which is wrong on five of the twelve examples on
this page.

</details>

## Acceptance checklist

- [ ] `python challenge-02-levee-ponding.py` prints `10 7`, then `All checks passed.`
- [ ] The solution is `O(n)` time and `O(1)` auxiliary space, excluding the input.
- [ ] The running maximum is updated **before** the addition, and there is no `max(0, ...)` clamp anywhere.
- [ ] `min(..., shoulder)` is applied to every section unconditionally.
- [ ] `[8, 0, 5, 0, 8]` with a shoulder of `3` returns `9`, not `3`.
- [ ] `[2, 0, 2]` returns `2`, and no section is filtered out for having a crown of `0`.
- [ ] You can justify the invariant in your own words — why processing the lower side is correct, and why two integers replace two lists.
- [ ] You can state exactly which part of your reasoning the camber cap does and does not disturb.
- [ ] You cross-checked against the two-array version on a few thousand random roads.
- [ ] You narrated a full FRAME pass out loud, at least twenty minutes. The first time you solve this you will pause — pausing out loud with "let me think about why that's true" is worth more than pausing silently.
- [ ] Committed to Git with a message like `Add Week 1 challenge 2: levee ponding`.
## Stretch

- **Return the depth at every section, not just the total.**

  ```python
  def ponded_depths(crown: list[int], shoulder: int) -> list[int]:
      """Return the water depth held at each section, west to east."""
      n = len(crown)
      depths = [0] * n
      west, east = 0, n - 1
      west_max = east_max = 0
      while west < east:
          if crown[west] < crown[east]:
              west_max = max(west_max, crown[west])
              depths[west] = min(west_max - crown[west], shoulder)
              west += 1
          else:
              east_max = max(east_max, crown[east])
              depths[east] = min(east_max - crown[east], shoulder)
              east -= 1
      return depths
  ```

  ```text
  [4, 1, 3, 0, 2, 5] shoulder 100 -> [0, 3, 1, 4, 2, 0]
  [4, 1, 3, 0, 2, 5] shoulder 2   -> [0, 2, 1, 2, 2, 0]
  [8, 0, 5, 0, 8] shoulder 3      -> [0, 3, 3, 3, 0]
  ```

  The output list is now `O(n)`, so the auxiliary-space claim changes. Say
  precisely what it changes to, and notice that the *working* space is still
  four integers — the size of the answer is not the same thing as the cost of
  computing it.

- **Find the deepest single section rather than the total.** One line
  changes. Then ask yourself whether you could also report *where* it is, and
  what happens on a tie.

- **Make the shoulder vary along the road.** The camber is rebuilt in
  stretches, so `shoulder` becomes a list the same length as `crown`. Work
  out which parts of the invariant survive before you touch the code. The
  answer is instructive: the cap was never entangled with the rims, so
  almost nothing changes — and being able to say *that*, quickly and with
  confidence, is exactly what the camber was added to test.

---

This concludes Week 1's exercises and challenges. Take the
[quiz](../quiz.md), do the [homework](../homework/README.md), then ship the
[mini-project](../mini-project/README.md) — your portfolio repo's first
commit.
