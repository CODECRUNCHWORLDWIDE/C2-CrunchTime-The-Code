# Exercise 3 — The Ring Buffer Probe

> **Topic:** searching a sorted sequence whose starting point has moved, by finding the wrap point first and then searching through it
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Medium
> **Target time:** 25 minutes
> **Why this one:** the order in this data is perfectly intact — it just does not start at index 0. Seeing that a rotation moves *where the order begins* and breaks nothing else is the insight, and it is worth more than the code. Two searches compose here, and composing searches is what Week 8 and the challenge are built on.

## The Brief

Picture a circle of eight lockers, numbered 0 to 7. A turnstile at a stadium
gate writes one row into the next locker every time somebody passes through.
When it fills locker 7 it goes back to locker 0 and writes over the oldest row.
That is a **ring buffer**: a fixed circle of slots that never runs out of room
because it eats its own tail.

Each row carries a **reading id** from a counter that only ever goes up. So in
the order the rows were *written*, the ids ascend strictly. But when you dump
the buffer you get the lockers in **physical order** — slot 0 first — and the
writer was somewhere in the middle of the circle when you looked.

```
slot:  0   1   2   3    4   5   6   7
id:   58  61  64  70   12  19  33  47
                        ^ the oldest row: this is where the writing wrapped
```

Read that dump starting at slot 4 and going round: `12, 19, 33, 47, 58, 61,
64, 70`. Perfectly ascending. The dump is a **rotation** of the write order:
the same sequence, cut in one place and the two pieces swapped.

The auditor does not care which locker a row sits in. Lockers are an accident
of when the writer happened to wrap. What they want is the row's **age**: how
many rows currently in the buffer are older than it. That is the same as its
position in write order, counting from 0.

So `12` — the oldest row, sitting in slot 4 — has age `0`. And `58`, sitting
in slot 0, has age `4`, because four rows were written before it.

Return the age. Return `None` when the id is not in the buffer at all.

Two searches get you there. The first finds the **wrap point** — the slot
holding the oldest row. The second searches the buffer *as if* it started
there, and the position it lands on is the answer, already in the units the
auditor asked for.

## Starter

Save this as `exercise-03-ring-buffer-probe.py` and fill in every `TODO`.

```python
"""exercise-03-ring-buffer-probe.py — the turnstile ring buffer.

Two composed binary searches: one for the wrap point, one through it.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
# Write order 12, 19, 33, 47, 58, 61, 64, 70, wrapped so the oldest row
# sits in slot 4.
DUMP: list[int] = [58, 61, 64, 70, 12, 19, 33, 47]


# ---- Your task ----
def wrap_point(slots: list[int]) -> int:
    """Return the slot index holding the oldest reading id.

    Args:
        slots: A rotation of a strictly increasing list of ids. Not empty.

    Returns:
        The index of the smallest id, which is 0 when the dump never wrapped.
    """
    # TODO: half-open shape, but hi starts at len(slots) - 1 here. Why?
    # TODO: compare slots[mid] against slots[hi], never against slots[lo]
    ...


def rows_older_than(slots: list[int], reading_id: int) -> int | None:
    """Return the 0-based position of `reading_id` in write order.

    Args:
        slots: The physical dump, slot 0 first.
        reading_id: The id to locate.

    Returns:
        How many rows in the buffer are older than that row, or None when
        the id is not in the buffer at all.
    """
    # TODO: guard the empty dump before anything else
    # TODO: find the wrap point, then closed-interval search over
    #       slots[(start + mid) % n] for mid in 0 .. n - 1
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"wrap point: slot {wrap_point(DUMP)} holds id {DUMP[wrap_point(DUMP)]}")
    for wanted in (12, 70, 58, 50):
        print(f"id {wanted:3d} -> age {rows_older_than(DUMP, wanted)}")

    assert rows_older_than(DUMP, 12) == 0
    assert rows_older_than(DUMP, 70) == 7
    assert rows_older_than(DUMP, 58) == 4
    assert rows_older_than(DUMP, 50) is None
    assert rows_older_than([12, 19, 33, 47], 33) == 2
    assert rows_older_than([91, 7], 91) == 1
    assert rows_older_than([91, 7], 7) == 0
    assert rows_older_than([5], 5) == 0
    assert rows_older_than([5], 9) is None
    assert rows_older_than([], 5) is None
    assert DUMP[0] == 58  # the dump was never rebuilt
    print("All checks passed.")
```

Two ideas you need before you start.

**Rotation.** Cut a sorted list at one point and swap the two pieces. The
order inside each piece is untouched; only the join is out of order, and there
is exactly one join. That single fact is what keeps binary search legal here.

**The logical view.** You are not going to rebuild the list. Instead, when you
want the row at write-position `t`, you read
`slots[(start + t) % len(slots)]` — walk `t` steps forward from the wrap
point, and wrap round with `%` if you run off the end. The `%` operator gives
the remainder after division, and it is what turns a straight line into a
circle. Reading through that expression, positions `0, 1, 2, …` come out
strictly ascending, which is precisely what an ordinary binary search needs.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/exercises/exercise-03-ring-buffer-probe.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `wrap_point(slots)` returns the index of the smallest id, and `0` when the
   dump has not wrapped.
2. `rows_older_than(slots, reading_id)` returns the row's 0-based position in
   write order.
3. It returns `None` when the id is absent, including when the id falls inside
   the range of ids held in the buffer.
4. It returns `None` for the empty dump, without indexing anything.
5. Both searches are binary. Together they read about `2 · log2(n)` slots, and
   nothing in your code touches every slot.
6. Nothing rebuilds the un-rotated list. No `slots[p:] + slots[:p]`, no `sorted`,
   no copy of any kind.
7. There is no `if the dump is rotated` branch anywhere.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(slots) <= 262_144`.** The buffer is `2^18` rows, roughly three
  days at this gate's peak rate. One scan of that would be cheap — but the
  dashboard is not doing one. It re-probes the buffer for every id on its watch
  list, about forty thousand ids, on every refresh. At `O(n)` per probe that is
  ten billion reads per refresh; at `O(log n)` it is about seven hundred
  thousand. The bound and the probe volume are one argument, and you need both
  halves of it.

- **The ids are strictly increasing in write order, so they are all distinct.**
  Distinctness is load-bearing twice over. It makes the wrap point unique — one
  smallest id, one join — and it makes `slots[mid] > slots[hi]` a trustworthy
  test. Take distinctness away and both claims fail; that is
  [Homework Problem 4](../homework/problem-04-duplicated-manifest.md), where
  the worst case degrades to a scan.

- **`1 <= reading_id <= 2**31 - 1`.** The counter is never reset, so after a
  few years an id is a ten-digit number while the buffer holds a quarter
  million rows. **Ids are not indices.** Any attempt to compute a slot from
  the id — `reading_id % len(slots)`, or an offset from `slots[0]` — dies on
  this bound, because the ids in the buffer need not be consecutive: the
  writer skips an id whenever a pass fails validation.

- **The empty dump is legal input.** The gate has not opened yet. This is the
  one case that genuinely needs a guard, because `len(slots) - 1` is `-1` and
  `% 0` raises, and both of those are in the code you are about to write.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-ring-buffer-probe.py
wrap point: slot 4 holds id 12
id  12 -> age 0
id  70 -> age 7
id  58 -> age 4
id  50 -> age None
All checks passed.
```

The third row is the one that catches wrong answers. Id `58` is sitting in
slot `0` and its age is `4`. If your program prints `0` there, it returned the
locker number and never converted. The last row is the other trap: `50` sits
between `47` and `58`, comfortably inside the range of ids in the buffer, and
it is still absent — the writer skipped it.

## Steps

1. Save the starter and run it. `wrap_point` returns `Ellipsis`, so the first
   `print` fails while indexing with it. Expected.
2. Write `wrap_point` first, and test it on its own. The rule: compare
   `slots[mid]` against `slots[hi]`. If the midpoint is **bigger** than the
   last slot, the join must be somewhere to the right of `mid`, so
   `lo = mid + 1`. Otherwise the join is at `mid` or to its left, and `mid` is
   still a candidate, so `hi = mid`.
3. Check it on three shapes: the sample dump (expect `4`), an un-rotated dump
   like `[12, 19, 33, 47]` (expect `0`), and `[91, 7]` (expect `1`).
4. Now write `rows_older_than`. Guard the empty dump on the first line.
5. Find the wrap point, then run an ordinary closed-interval search over
   positions `0` to `n - 1`, reading each position as
   `slots[(start + mid) % n]`.
6. When you find a match, return the **position**, not the slot. That is the
   entire point of the exercise, and it is one line of restraint.
7. Trace `id = 50` on paper and confirm the loop closes to `lo > hi` and falls
   through to `return None`.
8. Trace `[91, 7]` with `91` and confirm you get `1`. It is the smallest input
   that punishes returning the slot.

## The Solution

```python
"""exercise-03-ring-buffer-probe-solution.py - the turnstile ring buffer.

Two composed binary searches. The first finds the wrap point - the slot
holding the oldest row. The second searches the logical view that the wrap
point defines, and the logical index it lands on IS the row's age.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# Write order 12, 19, 33, 47, 58, 61, 64, 70, wrapped so the oldest row
# sits in slot 4.
DUMP: list[int] = [58, 61, 64, 70, 12, 19, 33, 47]


# ---- Your task ----
def wrap_point(slots: list[int]) -> int:
    """Return the slot index holding the oldest reading id.

    Args:
        slots: A rotation of a strictly increasing list of ids. Not empty.

    Returns:
        The index of the smallest id, which is 0 when the dump never wrapped.
    """
    lo, hi = 0, len(slots) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if slots[mid] > slots[hi]:
            lo = mid + 1  # the wrap is strictly right of mid
        else:
            hi = mid  # mid is still a candidate for the oldest slot
    return lo


def rows_older_than(slots: list[int], reading_id: int) -> int | None:
    """Return the 0-based position of `reading_id` in write order.

    Args:
        slots: The physical dump, slot 0 first.
        reading_id: The id to locate.

    Returns:
        How many rows in the buffer are older than that row, or None when
        the id is not in the buffer at all.
    """
    n = len(slots)
    if n == 0:
        return None

    start = wrap_point(slots)
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        probe = slots[(start + mid) % n]
        if probe == reading_id:
            return mid
        if probe < reading_id:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"wrap point: slot {wrap_point(DUMP)} holds id {DUMP[wrap_point(DUMP)]}")
    for wanted in (12, 70, 58, 50):
        print(f"id {wanted:3d} -> age {rows_older_than(DUMP, wanted)}")

    assert rows_older_than(DUMP, 12) == 0
    assert rows_older_than(DUMP, 70) == 7
    assert rows_older_than(DUMP, 58) == 4
    assert rows_older_than(DUMP, 50) is None
    assert rows_older_than([12, 19, 33, 47], 33) == 2
    assert rows_older_than([91, 7], 91) == 1
    assert rows_older_than([91, 7], 7) == 0
    assert rows_older_than([5], 5) == 0
    assert rows_older_than([5], 9) is None
    assert rows_older_than([], 5) is None
    assert DUMP[0] == 58  # the dump was never rebuilt
    print("All checks passed.")
```

**A rotation does not break bisection; it moves where bisection starts.** The
sequence is still ascending everywhere except at one join. Once you know where
that join is, the whole circle reads in order again — and finding the join is
itself a bisection, because the join is exactly the boundary between "bigger
than the last slot" and "not bigger".

**`slots[hi]`, never `slots[lo]`, is the thing to compare against.** Compare
against `slots[lo]` and an un-rotated dump lies to you: on `[12, 19, 33, 47]`,
`slots[mid]` is greater than `slots[lo]`, so you conclude the join is on the
right and walk to the last slot instead of the first. Comparing against
`slots[hi]` gets the un-rotated case right for free, because in an un-rotated
dump every midpoint is smaller than the last slot and `hi` marches all the way
down to 0.

**The wrap search keeps `mid`, so it uses `hi = mid`.** Until something to its
left proves otherwise, `mid` could be the oldest slot. `hi = mid - 1` would
throw the answer away. Notice this search has no equality test and no early
return at all: it is not looking for a *value*, it is converging on a
*boundary*, and it always runs to `lo == hi`.

**The second search is completely ordinary.** Closed interval, `lo <= hi`,
`mid ± 1`, early return on a match. The only unusual line is `probe`, which
reads through the rotation instead of directly. That line is the entire trick,
and it costs one modulo per read.

**The answer needs no conversion, because the search was already in the right
units.** `mid` here is a position in write order — that is what the logical
view means. A learner who searches the physical slots instead has to convert
afterwards with `(slot - start) % n`, which works, and which is one more place
to be off by one. Choosing coordinates so the answer falls out is a habit
worth stealing.

**The un-rotated dump needs no special case.** `wrap_point` returns `0`, the
probe expression becomes `slots[mid % n]`, which is `slots[mid]`, and the
second search is a plain binary search. Every branch you do not write is a
branch that cannot be wrong.

**Rebuilding the list would be correct and would throw away the point.**
`slots[start:] + slots[:start]` gives you a clean ascending list in one line —
and reads all quarter of a million rows to do it, which is the cost you came
here to avoid, multiplied by forty thousand probes per refresh.

## Run it

Copy the worked answer on this page into `exercise-03-ring-buffer-probe.py` and run it:

```bash
python exercise-03-ring-buffer-probe.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-03-ring-buffer-probe.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the empty dump.** You read
  `slots[len(slots) - 1]` before checking whether there is anything to read:

  ```text
  Traceback (most recent call last):
      return slots[len(slots) - 1]
             ~~~~~^^^^^^^^^^^^^^^^
  IndexError: list index out of range
  ```

  On an empty list that index is `-1`, which Python happily interprets as "the
  last element" — of a list with no elements. Hence the crash. Guard `n == 0`
  on the first line of `rows_older_than`.

- **`ZeroDivisionError: integer modulo by zero`.** Same missing guard, one line
  later:

  ```text
  Traceback (most recent call last):
      return slots[(start + t) % len(slots)]
                   ~~~~~~~~~~~~^~~~~~~~~~~~
  ZeroDivisionError: integer modulo by zero
  ```

  `%` is division's remainder, and dividing by zero is undefined however you
  spell it. Two different crashes, one missing guard.

- **`[91, 7]` with `91` returns `0`.** You returned the physical slot. `91`
  really is in slot 0 — and it was written *second*, so its age is `1`. This is
  the bug the contract was built to catch, and it never crashes.

- **An un-rotated dump lands on the last slot.** You compared `slots[mid]`
  against `slots[lo]` in the wrap search. On `[12, 19, 33, 47]` every midpoint
  is bigger than `slots[lo]`, so you walk right every time and finish at slot
  3 instead of slot 0. Compare against `slots[hi]`.

- **`[64, 12, 19]` gives a wrap point of `0` instead of `1`.** You wrote
  `hi = mid - 1` in the wrap search. With `lo = 0, hi = 2`, `mid = 1`:
  `slots[1] = 12` is not bigger than `slots[2] = 19`, so the join is at `mid`
  or left of it — and `hi = mid - 1` steps straight over the answer. In this
  search `mid` stays.

- **`[5]` with `5` returns `None`.** You used `lo < hi` for the *second*
  search. That one is a closed-interval find-any, and when it narrows to a
  single candidate `lo == hi`, so a `<` guard exits without testing it. Two
  searches on one page, two different conventions — say which is which out
  loud before you write either.

- **An id inside the range comes back as a match when it is absent.** You
  assumed "between the smallest and largest id" implies "present". The writer
  skips ids for failed passes, so `50` is missing from a buffer that runs from
  `12` to `70`. The final `return None` is not decoration.

- **`slots[p:] + slots[:p]` appears anywhere in your solution.** Correct
  answer, wrong complexity: `O(n)` time and `O(n)` memory per probe, forty
  thousand times a refresh.

## Under the hood

<details>
<summary>Under the hood — the one-pass alternative, and which contract each one suits</summary>

**The single-pass "which half is sorted?" search.**

There is a well-known one-pass version that finds the *physical slot* without
ever locating the wrap point:

```python
lo, hi = 0, len(slots) - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2
    if slots[mid] == reading_id:
        return mid
    if slots[lo] <= slots[mid]:           # the left half is sorted
        if slots[lo] <= reading_id < slots[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    else:                                  # the right half is sorted
        if slots[mid] < reading_id <= slots[hi]:
            lo = mid + 1
        else:
            hi = mid - 1
return None
```

At any midpoint, at least one of the two halves is guaranteed to be a clean
ascending run — the join can only be in one of them. Check whether the target
falls inside the sorted half's range: if it does, keep that half; if it does
not, keep the other one.

It is one pass instead of two, and for the contract "give me the physical
slot" it is the better answer. For *this* contract it is not, because the age
conversion needs the wrap point anyway — so the second search would come back
regardless, and you would have written two different search shapes instead of
one shape twice.

Note the `<=` in `slots[lo] <= slots[mid]`. When the interval narrows to two
slots, `mid == lo`, so the left half has length one; a strict `<` would call
it unsorted and send you the wrong way. That single character is the most
common bug in this version, and it is a good reason to prefer the two-pass
form when either would do.

**Why the wrap search is a lower bound in disguise.**

Look at the predicate the wrap search is really testing: *is `slots[mid]`
bigger than the last slot?* On `[58, 61, 64, 70, 12, 19, 33, 47]` that is
`True, True, True, True, False, False, False, False`. One flip, in one place —
which is the shape every binary search needs. `wrap_point` is the lower bound
of `False`, which is why it converges instead of returning early, and why it
keeps `mid`.

Seeing a rotated search as a monotone predicate rather than as a special
algorithm is the transferable move. It is the same move Exercise 5 makes on a
problem with no list in it at all.

**Ring buffers in the wild.**

The structure is everywhere: kernel log buffers (`dmesg`), audio and video
capture, network interface descriptor rings, `collections.deque` with a
`maxlen`. They all share the property this exercise turns on — the physical
index is meaningless on its own and only becomes meaningful relative to a
head pointer. Real implementations store that pointer, so no search is needed.
You are searching for it here because a *dump* has lost it: the file on disk
has the slots and not the header.

</details>

## Acceptance checklist

- [ ] `python exercise-03-ring-buffer-probe.py` prints five rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] `wrap_point` compares against `slots[hi]` and keeps `mid` with
      `hi = mid`.
- [ ] The second search is closed-interval with `lo <= hi` and `mid ± 1`.
- [ ] The empty dump is guarded before any indexing or any `%`.
- [ ] There is no "is it rotated?" branch and no rebuilt list anywhere.
- [ ] You can say in one sentence why a rotation does not break bisection.
- [ ] Committed to Git with a message like
      `Add Week 5 exercise 3: ring buffer probe`.

## Stretch

- **Return the age and the slot together.** Auditors want the age; engineers
  want to know which locker to go and read.

  ```python
  def probe(slots: list[int], reading_id: int) -> tuple[int, int] | None:
      """Return (age, physical_slot) for a reading id, or None if absent."""
      age = rows_older_than(slots, reading_id)
      if age is None:
          return None
      return age, (wrap_point(slots) + age) % len(slots)
  ```

  ```text
  id 12 -> age 0, slot 4
  id 58 -> age 4, slot 0
  ```

  The conversion runs both ways with the same `%`. Write both directions once
  and the "which one am I holding?" confusion stops for good.

- **Find the newest row without searching for it.** The newest id is the one
  written just before the wrap.

  ```python
  def newest_id(slots: list[int]) -> int | None:
      """Return the most recently written id, or None for an empty dump."""
      if not slots:
          return None
      return slots[wrap_point(slots) - 1]
  ```

  ```text
  newest id in the dump: 70
  ```

  That `- 1` with no `%` is not a slip: Python's negative indexing wraps for
  you, so at a wrap point of 0 it reads the last slot, which is exactly right.
  Say out loud why that is the correct row.

- **Break it on purpose.** Feed your solution a dump with a repeated id —
  `[47, 47, 51, 8, 8, 8, 19, 33]` — and watch `wrap_point` return something
  indefensible. Then work out *why* `slots[mid] > slots[hi]` stops
  discriminating when the values can tie. That failure is the subject of
  [Homework Problem 4](../homework/problem-04-duplicated-manifest.md); meeting
  it here first makes that page much shorter.

When your probe is right, move on to
[Exercise 4 — The Quote Rank](./exercise-04-quote-rank.md).
