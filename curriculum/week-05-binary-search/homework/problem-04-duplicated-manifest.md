# Homework Problem 4 — The Duplicated Manifest

> **Topic:** rotated search when duplicates take the discriminator away, and the honest complexity that follows
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md) promised distinct ids, and that promise was doing far more work than it looked like. Take it away and the neat `O(log n)` claim becomes false — not slower, *false*. Being the candidate who says so, and names the input that proves it, is the whole point of this page.

## The Brief

A loading dock writes one row into a circular buffer for every truck that
arrives, and each row carries the **dock minute** the truck turned up. Trucks
arrive in time order, so in write order the minutes never go down — but
several trucks routinely arrive in the same minute, so **duplicates are
everywhere**. When the buffer fills, the next write wraps round to slot 0.

Dumping the buffer gives you the slots in physical order, slot 0 first, which
is a rotation of the write order.

```
slot:    0   1   2   3  4  5   6   7
minute: 47  47  51   8  8  8  19  33
                     ^ the oldest row: the writing wrapped here
```

The supervisor wants the **physical slot** of a row carrying a given minute,
because they are going to walk over and read that row. Several slots may carry
it; **any of them is a correct answer**. Return `None` when no row does.

Now the hard part, and it is not the code.

In [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md) the ids were
distinct, and that let you look at three positions and *know* which side of
the buffer held the wrap. With duplicates, that inference dies. Look at these
two dumps:

```
[2, 2, 2, 0, 2]        wraps at slot 3
[2, 0, 2, 2, 2]        wraps at slot 1
```

At the low, middle and high positions both dumps read `2, 2, 2`. Identical
evidence, different answers. No amount of cleverness extracts the wrap point
from those three reads, because the information is genuinely not there.

The repair is to give up one slot and try again: `lo += 1`, then loop. Each
fallback costs one row instead of half the buffer — so on a dump of one
repeated minute, the search degrades all the way to a scan.

Say that out loud in an interview, unprompted, and name the input. Most
candidates deliver a confident `O(log n)` defence on this problem that is
simply wrong, and the interviewer is waiting for it.

Two contract decisions, both different from Exercise 3:

- The answer is the **physical slot**, not an age. Exercise 3 asked you to
  convert; here the raw slot is what the supervisor wants.
- **Any** matching slot is correct, so your tests assert
  `slots[result] == stamp` rather than a fixed number.

## Starter

Save this as `problem-04-duplicated-manifest.py` and fill in every `TODO`.

```python
"""problem-04-duplicated-manifest.py — rotated search with duplicates.

The rotated buffer from the drill, with the distinctness guarantee removed.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
# Write order 8, 8, 8, 19, 33, 47, 47, 51, wrapped so the oldest row sits in
# slot 3.
MANIFEST: list[int] = [47, 47, 51, 8, 8, 8, 19, 33]


# ---- Your task ----
def find_stamp_slot(slots: list[int], stamp: int) -> int | None:
    """Return the physical slot of a row carrying `stamp`, or None.

    Args:
        slots: A rotation of a non-decreasing list of dock minutes.
            Duplicates are the normal shape of this data.
        stamp: The dock minute the supervisor is looking for.

    Returns:
        Any index i with slots[i] == stamp, or None when no row carries it.
    """
    # TODO: closed interval, and return the moment slots[mid] matches
    # TODO: when slots[lo], slots[mid] and slots[hi] are all equal, the probe
    #       learned nothing — pay one slot with lo += 1 and loop again
    # TODO: otherwise one half is genuinely sorted. Which one, and how do you
    #       tell? Watch the <= carefully.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (19, 51, 8, 20):
        print(f"stamp {wanted:3d} -> slot {find_stamp_slot(MANIFEST, wanted)}")

    for wanted in (19, 51, 33, 8, 47):
        slot = find_stamp_slot(MANIFEST, wanted)
        assert slot is not None and MANIFEST[slot] == wanted, (wanted, slot)
    assert find_stamp_slot(MANIFEST, 20) is None

    adversarial = [2, 2, 2, 0, 2]
    assert find_stamp_slot(adversarial, 0) == 3
    assert adversarial[find_stamp_slot(adversarial, 2)] == 2
    flat = [5, 5, 5, 5, 5]
    assert find_stamp_slot(flat, 9) is None
    assert flat[find_stamp_slot(flat, 5)] == 5
    assert find_stamp_slot([9], 9) == 0
    assert find_stamp_slot([9], 1) is None
    assert find_stamp_slot([], 7) is None
    assert MANIFEST[0] == 47  # the dump was never rebuilt
    print("All checks passed.")
```

One idea you need before you start.

**"Which half is sorted?" is the single-pass route.** At any midpoint of a
rotated dump, the wrap can only be in one of the two halves — so the other
half is a clean, non-decreasing run. Work out which one that is, check whether
the stamp falls inside its range, and keep that half if it does or the other
one if it does not. With distinct values, `slots[lo] <= slots[mid]` settles
which half is sorted. With duplicates, that test is only trustworthy when the
three probe points are not all equal, which is exactly what the fallback
branch is for.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/homework/problem-04-duplicated-manifest.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_stamp_slot(slots, stamp)` returns an index `i` with
   `slots[i] == stamp`, or `None` when no such index exists.
2. It returns `None` for the empty dump without indexing anything.
3. It handles an **un-rotated** dump with no special branch.
4. When `slots[lo]`, `slots[mid]` and `slots[hi]` are all equal, it shrinks by
   exactly one slot and loops again.
5. The sorted-half test uses `<=`, not `<`, and you can say why.
6. Your tests assert `slots[result] == stamp` wherever the stamp repeats, not a
   fixed index.
7. Nothing rebuilds or sorts the dump.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(slots) <= 100_000`.** One shift's arrivals. The worst case of
  this problem is genuinely `O(n)`, and this bound is chosen so that the
  degradation is *survivable* rather than fatal. That is precisely why you must
  be able to say where the worst case comes from instead of waving at
  `O(log n)`.

- **`0 <= slots[i] <= 1_439` and `0 <= stamp <= 1_439`.** A day has 1,440
  minutes, so a full buffer holds roughly seventy rows per distinct minute.
  **Duplicates are not an edge case here; they are the shape of the data.**
  This bound is what makes the fallback branch fire on ordinary input rather
  than on something contrived.

- **The dump may be un-rotated, and it may be empty.** The buffer has not
  wrapped yet, or the shift has not started. Neither deserves a special branch:
  the un-rotated case is handled by the sorted-half test, and the empty case by
  the loop guard plus one `None`.

- **Any matching slot is correct.** The supervisor is walking over to read one
  row, and every row carrying that minute says the same thing. This is what
  forces property-based assertions in your tests, the same discipline as
  [Problem 3](./problem-03-ridge-line.md).

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-04-duplicated-manifest.py
stamp  19 -> slot 6
stamp  51 -> slot 2
stamp   8 -> slot 3
stamp  20 -> slot None
All checks passed.
```

The `8` row is one of three correct answers — slots 3, 4 and 5 all carry an
`8`, and this search happens to land on 3. If yours prints 4 or 5, it is not
wrong. The `20` row is the trap: `20` sits comfortably between the smallest
and largest minute in the buffer and is still absent, because no truck arrived
that minute. "In range" never implied "present", and with duplicates it is
even easier to convince yourself otherwise.

## Steps

1. Save the starter and run it. `find_stamp_slot` returns `Ellipsis`, so the
   first assert fails. Expected.
2. Set up a closed-interval loop: `lo, hi = 0, len(slots) - 1`, guard
   `lo <= hi`. The empty dump falls out of that guard with no extra code.
3. Inside, compute `mid` and return immediately if `slots[mid]` is the stamp.
   Unlike the boundary searches this week, this one *is* hunting a value.
4. Write the fallback branch **before** the clever ones:
   `if slots[lo] == slots[mid] == slots[hi]: lo += 1`. Getting the order right
   matters — the sorted-half test is only sound once this case is excluded.
5. Now the two informative branches. If `slots[lo] <= slots[mid]`, the left half
   is a clean run: keep it when `slots[lo] <= stamp < slots[mid]`, otherwise
   keep the right. If not, the right half is the clean one: keep it when
   `slots[mid] < stamp <= slots[hi]`, otherwise keep the left.
6. Watch that `<=` in `slots[lo] <= slots[mid]`. When the interval narrows to
   two slots, `mid == lo`, so the left half has length one — and a strict `<`
   would declare it unsorted and send you the wrong way.
7. Run it. Then hand-trace `[2, 2, 2, 0, 2]` looking for `0` and confirm the
   fallback fires twice before the search finds it.
8. Trace `[5, 5, 5, 5, 5]` looking for `9`, count the iterations, and write the
   number down. That number is your complexity argument.

## The Solution

```python
"""problem-04-duplicated-manifest-solution.py - rotated search with duplicates.

The same rotated buffer as the drill, with the distinctness guarantee taken
away. When the three probe points all read the same stamp, no O(1) test can
say which half holds the wrap, so the loop gives up ONE slot and retries -
and that is why the worst case is a linear scan, not a logarithmic one.

The self-checks at the bottom are the starter's, unchanged. They assert the
property `slots[result] == stamp` rather than a fixed slot, because a stamp
may sit in several slots and any of them is a correct answer. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# Write order 8, 8, 8, 19, 33, 47, 47, 51, wrapped so the oldest row sits in
# slot 3.
MANIFEST: list[int] = [47, 47, 51, 8, 8, 8, 19, 33]


# ---- Your task ----
def find_stamp_slot(slots: list[int], stamp: int) -> int | None:
    """Return the physical slot of a row carrying `stamp`, or None.

    Args:
        slots: A rotation of a non-decreasing list of dock minutes.
            Duplicates are the normal shape of this data.
        stamp: The dock minute the supervisor is looking for.

    Returns:
        Any index i with slots[i] == stamp, or None when no row carries it.
    """
    lo, hi = 0, len(slots) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if slots[mid] == stamp:
            return mid
        if slots[lo] == slots[mid] == slots[hi]:
            lo += 1  # the probes learned nothing; pay one slot and retry
        elif slots[lo] <= slots[mid]:
            # the left half is genuinely sorted
            if slots[lo] <= stamp < slots[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # the right half is genuinely sorted
            if slots[mid] < stamp <= slots[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (19, 51, 8, 20):
        print(f"stamp {wanted:3d} -> slot {find_stamp_slot(MANIFEST, wanted)}")

    for wanted in (19, 51, 33, 8, 47):
        slot = find_stamp_slot(MANIFEST, wanted)
        assert slot is not None and MANIFEST[slot] == wanted, (wanted, slot)
    assert find_stamp_slot(MANIFEST, 20) is None

    adversarial = [2, 2, 2, 0, 2]
    assert find_stamp_slot(adversarial, 0) == 3
    assert adversarial[find_stamp_slot(adversarial, 2)] == 2
    flat = [5, 5, 5, 5, 5]
    assert find_stamp_slot(flat, 9) is None
    assert flat[find_stamp_slot(flat, 5)] == 5
    assert find_stamp_slot([9], 9) == 0
    assert find_stamp_slot([9], 1) is None
    assert find_stamp_slot([], 7) is None
    assert MANIFEST[0] == 47  # the dump was never rebuilt
    print("All checks passed.")
```

**One of the two halves is always a clean run, and that is what you bisect
on.** The wrap sits in exactly one place, so it is inside the left half or the
right half, never both. Whichever half does not contain it is non-decreasing
from end to end — so you can ask the ordinary question of it: does the stamp
fall between its two ends? If yes, keep it. If no, the stamp can only be in
the other half, so keep that one instead. Nothing here needs the wrap point
itself, which is why this is one pass rather than the drill's two.

**The equal-probes branch is an admission, not a trick.** When
`slots[lo]`, `slots[mid]` and `slots[hi]` all read the same, both halves look
equally plausible and the evidence genuinely does not distinguish them —
`[2, 2, 2, 0, 2]` and `[2, 0, 2, 2, 2]` are the witnesses. There is no repair
that recovers the missing information, so the loop buys information the only
way left: it discards one slot it has already ruled out and looks again.

**The honest complexity, in the words to use out loud.** *Typically
`O(log n)`; worst case `O(n)`, and the witness is a dump of one repeated
minute — `[5, 5, 5, 5, 5]` searching for anything absent. Every probe is
uninformative, the fallback fires every time, and the interval shrinks by one
slot per iteration instead of halving.* That is the sentence. Notice it names
an input rather than gesturing at "sometimes duplicates make it slow" — a
complexity claim without a witness is an opinion.

**Order the branches: fallback first.** The sorted-half test is only sound once
the all-equal case is excluded, so it has to come second. Put `slots[lo] <=
slots[mid]` first and `[2, 2, 2, 0, 2]` takes the left-half branch, concludes
`0` is not in `[2, 2)`, moves right, and misses the answer entirely.

**`<=`, not `<`, in the sorted-half test.** When the interval is two slots
wide, `mid == lo`, so `slots[lo] < slots[mid]` is false even though the
one-element left half is trivially sorted. That single character sends the
search the wrong way on the smallest intervals, which is exactly where a bug
is hardest to see. This is the same `<=`-versus-`<` decision as in
[Challenge 1](../challenges/challenge-01-order-book-boundary.md), for the same
underlying reason: equal values must not be treated as evidence of disorder.

**The three range tests use asymmetric comparisons on purpose.**
`slots[lo] <= stamp < slots[mid]` includes the left end and excludes `mid`,
because `mid` has already been tested for equality and rejected. The mirror
test `slots[mid] < stamp <= slots[hi]` does the same on the other side.
Including `mid` in either range would send the search back to a slot it has
already eliminated, which is one of the ways this loop can be made to spin.

**The un-rotated dump needs no branch.** With no wrap, `slots[lo] <=
slots[mid]` is always true, the left-half test always applies, and the whole
thing degenerates into an ordinary binary search. Every special case you do not
write is a special case that cannot be wrong.

## Run it

Copy the worked answer on this page into `problem-04-duplicated-manifest.py` and run it:

```bash
python problem-04-duplicated-manifest.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-04-duplicated-manifest.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the empty dump.** You read
  `slots[lo]` or `slots[hi]` before the loop, or you set up the interval and
  then indexed outside the guard:

  ```text
  Traceback (most recent call last):
      if slots[lo] == slots[mid] == slots[hi]:
         ~~~~~^^^^
  IndexError: list index out of range
  ```

  With an empty dump `hi` is `-1`, so `lo <= hi` is false and the loop body
  never runs. Every read has to live *inside* the loop.

- **`[2, 2, 2, 0, 2]` searching for `0` returns `None`.** The fallback branch
  is missing, or it comes after the sorted-half test. The first probe reads a
  `2` at both ends and in the middle, the left-half test fires wrongly, and the
  search walks away from slot 3.

- **The program hangs on `[5, 5, 5, 5, 5]`.** Your fallback does not actually
  shrink the interval — perhaps you wrote `mid += 1` or adjusted nothing at
  all. Press `Ctrl-C`:

  ```text
  Traceback (most recent call last):
    File "<string>", line 7, in <module>
      while lo <= hi:
            ^^^^^^^^
  KeyboardInterrupt
  ```

  Every branch of this loop must move `lo` up or `hi` down. The fallback moves
  it by one, which is slow and still progress.

- **`stamp = 51` returns `None`.** You used a strict `<` in the sorted-half
  test. `51` sits in slot 2, immediately before the wrap, and the strict
  comparison misclassifies the small interval that contains it.

- **`stamp = 20` returns a slot.** Your range tests include `mid`, so the
  search revisits eliminated slots and eventually reports one of them. The
  comparisons are deliberately asymmetric — re-read them.

- **You claimed `O(log n)` in your write-up.** This is the one graded here.
  With duplicates the bound is `O(n)`, the witness is a dump of one repeated
  minute, and the reason is that equal probes carry no information. Say it
  before the interviewer asks.

- **Your test hard-codes `find_stamp_slot(MANIFEST, 8) == 3`.** Slots 3, 4 and
  5 are all correct. Assert `MANIFEST[slot] == 8` instead, exactly as
  [Problem 3](./problem-03-ridge-line.md) required.

## Under the hood

<details>
<summary>Under the hood — what distinctness was buying, and the average case</summary>

**What the distinctness guarantee was worth.**

In [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md), strictly
increasing ids meant `slots[mid] > slots[hi]` was a *decision*: it told you
which side the wrap was on, every time, in constant time. That is what made
the two-pass solution cleanly `O(log n)` and what made the wrap point unique.

Take it away and three things break at once. The wrap point is no longer
unique — in `[5, 5, 5, 5, 5]` there is no distinguishable "oldest" row at all.
The comparison stops being a decision and becomes a hint. And the `O(log n)`
claim stops being true.

That is a general lesson worth carrying: a guarantee in the constraints is
rarely decoration. When a prompt says "all distinct", find out what the
distinctness is holding up before you decide it does not matter.

**Why you can shrink by one instead of giving up entirely.**

When the three probes are equal, `slots[lo]` is known not to be the stamp —
it equals `slots[mid]`, which the equality test has already rejected. So
discarding it loses nothing. Some implementations discard from both ends
(`lo += 1; hi -= 1`), which is equally sound and halves the constant on
adversarial input. Either is defensible; what is not defensible is a fallback
that discards a slot you have not ruled out.

**The average case is much better than the worst.**

The worst case needs *every* probe to be uninformative, which needs long runs
of one value spanning the whole interval. Real dock data has about seventy
rows per minute out of a hundred thousand — so the fallback fires occasionally
and the search is logarithmic in practice. That is precisely why the bound
matters in the interview and rarely bites in production, and being able to
separate "worst case" from "what actually happens" is a senior-level
distinction.
</details>

## Acceptance checklist

- [ ] `python problem-04-duplicated-manifest.py` prints four rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] The fallback branch comes **before** the sorted-half test.
- [ ] The sorted-half test uses `<=`, and you can say what breaks with `<`.
- [ ] You can state the worst case as `O(n)` and name `[5, 5, 5, 5, 5]` as the
      witness.
- [ ] You can say in one sentence why the duplicate case cannot be repaired in
      constant time.
- [ ] Your write-up contrasts this with Exercise 3: what distinctness bought,
      and what its removal costs.
- [ ] Your tests assert `slots[result] == stamp` wherever the stamp repeats.
- [ ] Committed to Git with a message like
      `Add Week 5 homework 4: duplicated manifest`.

## Stretch

- **Count the probes and watch the degradation.** Add a counter and run it on
  three shapes.

  ```python
  def probe_count(slots: list[int], stamp: int) -> int:
      """Return how many midpoints the search examines."""
      lo, hi, probes = 0, len(slots) - 1, 0
      while lo <= hi:
          mid = lo + (hi - lo) // 2
          probes += 1
          if slots[mid] == stamp:
              return probes
          if slots[lo] == slots[mid] == slots[hi]:
              lo += 1
          elif slots[lo] <= slots[mid]:
              hi, lo = (mid - 1, lo) if slots[lo] <= stamp < slots[mid] else (hi, mid + 1)
          else:
              lo, hi = (mid + 1, hi) if slots[mid] < stamp <= slots[hi] else (lo, mid - 1)
      return probes
  ```

  ```text
  distinct dump of 1000 rows, absent stamp : 10 probes
  70 rows per minute, absent stamp          : 12 probes
  one repeated minute, absent stamp         : 1000 probes
  ```

  Three numbers, one argument. Put them in your write-up instead of an
  adjective.

- **Return every matching slot instead of one.** The supervisor wants to know
  how many trucks arrived in that minute.

  ```text
  stamp 8 in the manifest -> slots [3, 4, 5]
  ```

  Work out what that costs. Finding one match is what this page does; finding
  *all* of them on a rotated dump means locating the wrap first — which is
  Exercise 3's machinery, and which duplicates have just broken. Say what you
  would do, and what you would have to give up.

- **Recover the drill's guarantee.** If the dock also recorded a strictly
  increasing arrival counter alongside the minute, the buffer would be
  searchable in `O(log n)` again. Sketch the change to the contract, and note
  what it costs in storage. Fixing a complexity problem by changing the data
  rather than the algorithm is a move worth having in your repertoire.

That is the coding homework. Next:
[Homework Problem 5 — Deciding Without the Full Picture](./problem-05-deciding-without-the-full-picture.md).
