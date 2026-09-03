# Exercise 4 — The Stuck Gauge

> **Topic:** same-direction pointers — a read pointer that visits everything and a write pointer that only moves when something survives
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Easy/Medium
> **Target time:** 50 minutes, including a full FRAME narration out loud
> **Why this one:** your first same-direction problem, and it feels completely different from the three before it. Both pointers start at the front. Only one of them moves on every step. And the list you are reading is the same list you are writing into, which sounds reckless until you can state the one inequality that makes it safe.

## The Brief

A river gauge station reports the water level every fifteen minutes, in
millimetres above the station's **datum** — a fixed reference height the
district agreed on once and never moves. The measurement comes from a float
on an arm, and the arm sticks. When it sticks, the station keeps transmitting
the previous number, over and over, until the arm frees itself.

The hydrologist plotting the record wants the **run-collapsed** series. A run
of identical samples in a row says nothing about the river; it just thickens
the line on the chart. So collapse every run of equal *adjacent* samples down
to its first sample, keep everything else in the order it arrived, and do it
**in place** — the field logger has no room for a second copy of the record.

Two parts of the contract are graded, and both of them catch people.

**The series is not sorted, and it never will be.** The river goes up and it
goes down. A level of 300 mm on Tuesday and 300 mm again on Friday are two
different, real facts about the river, and both have to survive. Only
*adjacent* repeats collapse. If you find yourself removing every duplicate,
you have matched the wrong problem.

**Return the number of samples dropped**, not the number kept. That number is
what the hydrologist reads as "how long was the arm stuck this month." And
leave the tail alone: everything from the kept prefix onward is scratch. Do
not truncate the list, do not clear it, do not tidy it. The logger reuses
that memory and what is in it afterwards is nobody's business.

```python
def collapse_stuck_readings(levels: list[int]) -> int:
    """Collapse runs of equal adjacent samples in place; return how many were dropped."""
```

The picture to hold in your head is two people working down a shelf of boxes.
One walks along reading every label — that is the **read** pointer. The other
stands at the first free slot at the front and only steps forward when the
reader hands them a box worth keeping — that is the **write** pointer. The
writer never gets ahead of the reader, so every slot the writer puts a box
into has already been read.

## Starter

Save this as `exercise-04-stuck-gauge.py` and fill in the `TODO`s.

```python
"""exercise-04-stuck-gauge.py — collapsing a stuck river gauge.

A read pointer visits every sample; a write pointer marks where the next
kept sample goes and only advances when a sample survives. Only adjacent
repeats collapse.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def collapse_stuck_readings(levels: list[int]) -> int:
    """Collapse runs of equal adjacent samples in place, preserving order.

    Args:
        levels: The record, millimetres above datum. Rewritten in place so
            that levels[:kept] holds the collapsed series. Entries at or
            after `kept` are scratch and are deliberately left alone.

    Returns:
        The number of samples dropped, which is len(levels) - kept.
    """
    # TODO: an empty record drops nothing — say so before anything else
    # TODO: the first sample is always kept, so the next free slot is 1
    # TODO: walk `read` from 1 to the end. Keep a sample when it differs from
    #       the last sample you actually KEPT, not the last one you read.
    # TODO: return how many were dropped, not how many survived
    ...


# ---- Self-check ----
if __name__ == "__main__":
    wobble = [300, 300, 305, 300]
    print(collapse_stuck_readings(wobble), wobble[:3])

    stuck = [777, 777, 777, 777]
    assert collapse_stuck_readings(stuck) == 3
    assert stuck == [777, 777, 777, 777]
    assert collapse_stuck_readings([]) == 0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/exercise-04-stuck-gauge.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `collapse_stuck_readings` mutates `levels` in place so that
   `levels[:kept]` holds the collapsed series in its original order.
2. Only **adjacent** equal samples collapse. A value that recurs after an
   intervening different value is kept.
3. It returns the number of samples **dropped**, as an `int`.
4. It does not truncate, clear, or otherwise tidy the list. Entries at or
   after `kept` keep whatever they happen to hold.
5. An empty record returns `0` and does not raise.
6. `O(n)` time, one pass, and `O(1)` auxiliary space. No second list, no
   comprehension building a new record.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(levels) <= 2_000_000`.** Two million fifteen-minute samples is
  about fifty-seven years of continuous record, which is the real size of a
  long-running station's archive. At that size, building a fresh list doubles
  peak memory on a field logger that does not have it to spare. That is why
  this exercise grades in-place work with `O(1)` auxiliary space rather than
  accepting a comprehension.

- **`-5_000 <= levels[i] <= 20_000`, in millimetres relative to datum.**
  Readings below datum are negative and happen every drought. This bound is
  here to catch a specific mistake: treating `0` or a negative number as
  "missing data". A level of `0` means the river is sitting exactly at datum,
  which is a measurement, not an absence.

- **The series carries no ordering guarantee at all.** This is the bound that
  rejects the sorted-array habit of removing every duplicate. In a sorted
  list every duplicate is adjacent, so the two rules coincide and you can get
  away with the wrong one. Here they come apart, and the third example is
  built to make them come apart.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-04-stuck-gauge-solution.py
dropped 3  kept [412, 415, 409]  whole list [412, 415, 409, 415, 415, 409]  was [412, 412, 412, 415, 415, 409]
dropped 1  kept [300, 305, 300]  whole list [300, 305, 300, 300]  was [300, 300, 305, 300]
dropped 3  kept [777]  whole list [777, 777, 777, 777]  was [777, 777, 777, 777]
dropped 0  kept [500, 501, 502]  whole list [500, 501, 502]  was [500, 501, 502]
dropped 2  kept [-2, 0, -2]  whole list [-2, 0, -2, 0, -2]  was [-2, -2, 0, 0, -2]
dropped 0  kept [640]  whole list [640]  was [640]
dropped 0  kept []  whole list []  was []
All checks passed.
```

Look at the three columns on each line together — they are the whole lesson.

**Line 1.** Three samples dropped: two from the run of `412`s and one from
the run of `415`s. The kept prefix is `[412, 415, 409]`. The whole list still
ends `415, 415, 409`, which are the untouched originals sitting in the
scratch region. That is correct. If it makes you uncomfortable, good — the
discomfort is the thing to reason your way out of, not to code your way out
of.

**Line 2.** The level rises to 305 and comes back to 300. That second 300 is
a real reading and it stays, so only one sample is dropped. **A solution that
removes all duplicates returns `2` here and is wrong.** This is the single
most common failure on this page, and it comes from recall rather than from
reading.

**Line 3.** The whole record is one stuck run. Three samples dropped, only
`levels[0]` kept — and the list is **unchanged**, because every write was a
write of `777` onto a `777`. Non-zero return, identical list. If your own
test asserts on the whole list instead of on `levels[:kept]`, this is the
line where it lies to you.

**Line 5.** `-2` recurs legitimately after an intervening `0`, and `0` itself
is a real level at datum. Two real values that look like "empty" to a
careless eye, both surviving.

## Steps

1. Save the starter and run it. `AssertionError`.
2. Handle the empty record first, on its own line: `if not levels: return 0`.
   Do this before anything else, because the next step is invalid on an empty
   list.
3. Set `write = 1`. The first sample is always kept, so the next free slot is
   position `1`.
4. Loop `read` over `range(1, len(levels))`.
5. Inside: if `levels[read] != levels[write - 1]`, then
   `levels[write] = levels[read]` and `write += 1`. Otherwise do nothing at
   all — that is the sample being dropped.
6. Return `len(levels) - write`.
7. Now build a trace table for `[300, 300, 305, 300]` with four columns:
   `read`, the value, what you compared it against, and `write` afterwards.
   Do the same for `[-2, -2, 0, 0, -2]`. If the tables come out right, you
   understand the comparison; if they do not, the comparison is where to
   look.

## The Solution

```python
"""exercise-04-stuck-gauge-solution.py — collapsing a stuck river gauge.

A read pointer visits every sample; a write pointer marks where the next
kept sample goes and only advances when a sample survives. Only adjacent
repeats collapse, because the river really does come back to a level it
held before.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def collapse_stuck_readings(levels: list[int]) -> int:
    """Collapse runs of equal adjacent samples in place, preserving order.

    Args:
        levels: The record, millimetres above datum. Rewritten in place so
            that levels[:kept] holds the collapsed series. Entries at or
            after `kept` are scratch and are deliberately left alone.

    Returns:
        The number of samples dropped, which is len(levels) - kept.
    """
    if not levels:
        return 0

    write = 1
    for read in range(1, len(levels)):
        if levels[read] != levels[write - 1]:
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


# ---- Self-check ----
if __name__ == "__main__":
    records = [
        [412, 412, 412, 415, 415, 409],
        [300, 300, 305, 300],
        [777, 777, 777, 777],
        [500, 501, 502],
        [-2, -2, 0, 0, -2],
        [640],
        [],
    ]
    for levels in records:
        before = list(levels)
        dropped = collapse_stuck_readings(levels)
        kept = len(levels) - dropped
        print(f"dropped {dropped}  kept {levels[:kept]}  whole list {levels}  was {before}")

    record = [412, 412, 412, 415, 415, 409]
    assert collapse_stuck_readings(record) == 3
    assert record[:3] == [412, 415, 409]
    assert record == [412, 415, 409, 415, 415, 409]  # tail untouched on purpose

    wobble = [300, 300, 305, 300]
    assert collapse_stuck_readings(wobble) == 1
    assert wobble[:3] == [300, 305, 300]

    stuck = [777, 777, 777, 777]
    assert collapse_stuck_readings(stuck) == 3
    assert stuck == [777, 777, 777, 777]  # non-zero return, identical list

    assert collapse_stuck_readings([500, 501, 502]) == 0
    assert collapse_stuck_readings([-2, -2, 0, 0, -2]) == 2
    assert collapse_stuck_readings([640]) == 0
    assert collapse_stuck_readings([]) == 0
    print("All checks passed.")
```

**`write <= read` always holds, and that single inequality is the licence to
overwrite.** Both pointers start at their positions with `write` no further
along than `read`; `read` advances exactly once per iteration and `write`
advances at most once. So `write` can never overtake `read`, which means
every slot you write into has already been read. When an interviewer asks
whether you are clobbering your own input, that sentence is the answer — not
"I traced it and it seemed fine."

Note the `<=` rather than `<`. On the first iteration `read` is `1` and
`write` is `1`, so they are equal, and stating the invariant with a strict
`<` would be a subtle error an interviewer may well pick up on.

**The comparison is against `levels[write - 1]`, the last sample you
*kept*.** That is the definition of what the collapsed series currently ends
with, so no proof is required to use it. The alternative, `levels[read - 1]`,
also gives the right answer here — but only for a reason you would have to
construct on the spot: at the moment of the comparison in iteration `read`,
index `read - 1` still holds its original sample, because the earliest a
write could land on `read - 1` is during iteration `read` itself, after the
comparison. Prefer the one that needs no argument, and be able to explain the
difference when asked.

**`write = 1`, not `0`.** The first sample is always kept, so the next free
slot is `1`. Starting at `0` makes the first comparison read `levels[-1]`,
which in Python is the *last* sample in the record — and Python will not warn
you, because negative indexing is a feature. On `[500, 501, 502]` that
version returns `1` and leaves the list as `[501, 502, 502]`, a wrong answer
and a corrupted record from a single character.

**The empty guard is not defensive programming, it is arithmetic.** With no
guard, `write` is `1`, the loop body never runs, and the function returns
`0 - 1`, which is `-1`. Nobody drops minus-one samples. It is worth noticing
that this case fails in the *return value*, not in an index — which is why it
survives casual testing.

**Nothing is truncated, and that is a deliberate part of the contract.**
`del levels[write:]` and `levels[:] = levels[:write]` both "work". The first
violates the contract; the second violates it *and* allocates a new list,
which is the one thing the memory bound rules out. Returning a count and
leaving the tail is the standard shape for in-place compaction, and once you
have seen it here you will recognise it every time.

**One pass, no allocation.** `read` visits each sample exactly once and never
goes back, so the work is `O(n)` — and that is the floor, because you cannot
know whether the last sample is a repeat without looking at it. The state is
two integers regardless of whether the archive holds seven samples or two
million.

## Download and run

Download
[exercise-04-stuck-gauge-solution.py](./exercise-04-stuck-gauge-solution.py)
and run it:

```bash
python exercise-04-stuck-gauge-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-04-stuck-gauge.py`.

## Common bugs to catch

- **A bare `AssertionError` on `[300, 300, 305, 300]`.** You removed every
  duplicate instead of every adjacent duplicate:

  ```text
  Traceback (most recent call last):
      assert collapse_stuck_readings(wobble) == 1
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Your function returned `2`. It threw away the second `300`, which is a real
  reading taken two days later. This is the sorted-array solution wearing
  this problem's clothes, and it is the failure this exercise exists to
  produce.

- **A bare `AssertionError` on the empty record.** You left out the guard:

  ```text
  Traceback (most recent call last):
      assert collapse_stuck_readings([]) == 0
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `write` was `1`, the loop never ran, and `len(levels) - write` returned
  `-1`. No index was ever touched, which is exactly why nothing raised.

- **`write = 0`, silently corrupting the record.** No exception at all:

  ```text
  [412, 412, 412, 415, 415, 409]  ->  dropped 3, list [412, 415, 409, 415, 415, 409]
  [500, 501, 502]                 ->  dropped 1, list [501, 502, 502]
  ```

  The first record is right by accident. The second is wrong: the first
  comparison was `levels[1] != levels[-1]`, which asked whether Tuesday's
  reading matched the *last* reading in the archive. On a fifty-seven-year
  record that comparison is meaningless, and it never raises.

- **Returning the kept count.** `write` instead of `len(levels) - write`. On
  line 1 of the expected output that is `3` either way, which is why this bug
  can survive a single test. Try it on `[500, 501, 502]`: the contract wants
  `0` and the bug gives `3`.

- **Truncating.** `del levels[write:]` gives the right prefix and violates
  the contract. `levels[:] = levels[:write]` does the same and allocates a
  whole second record on the way. Neither raises, and both would fail a code
  review at the station, because the logger's caller reads the tail for its
  own reasons.

- **Asserting on the whole list in your own tests.**
  `[777, 777, 777, 777]` returns `3` with the list unchanged. If your test
  says `assert levels == [777]`, your test is wrong and your code may be
  fine. Assert on `levels[:kept]`.

## Under the hood

<details>
<summary>Under the hood — the invariant in full, and why a comprehension is not the same program</summary>

**Stating the invariant precisely.**

At the top of every iteration, two things are true:

1. `levels[:write]` is exactly the collapse of `levels_original[:read]`.
2. `write <= read`.

The first is what makes the answer right; the second is what makes the
mutation safe. Both survive an iteration. If the new sample differs from
`levels[write - 1]` — the last element of the collapsed prefix — then
appending it at `write` extends property 1 by one sample, and `write`
advancing by one alongside `read` advancing by one preserves property 2. If
it does not differ, the collapse of the longer prefix is the same as before,
so property 1 holds unchanged and `write` stays put, which only strengthens
property 2.

Being able to write down an invariant and show it survives one step is a
different skill from tracing an example, and it is the one that scales. A
trace convinces you about six samples. An invariant convinces you about two
million.

**The comprehension, and why it is a different program.**

```python
collapsed = [x for i, x in enumerate(levels) if i == 0 or x != levels[i - 1]]
```

That is one line, it is easy to read, and in ordinary code it is what you
should write. It is `O(n)` time, same as ours. What it is not is in place:
it builds a whole new list, so it is `O(n)` auxiliary space — the exact cost
the field logger cannot pay — and it hands back a new object rather than
rewriting the caller's. It also cannot report the dropped count without a
second `len()` comparison, which is a small thing but a real one.

Two programs, same output, different contracts. Knowing which contract you
are being asked for is most of the job.

**Where this pattern turns up next.**

The same read/write shape does partitioning (move everything satisfying a
test to the front), filtering (drop what fails a threshold), and the
three-way partition at the heart of quicksort. The variant with a low, a
middle and a high pointer sorts three categories in one pass. Week 4 replaces
the array with a linked list and the read/write pointers become fast/slow
pointers, but the accounting — one pointer that always moves, one that
sometimes does — is identical.

**A related question worth trying.** Keep at most *two* samples from any run,
because the hydrologist decides that a stuck arm for two consecutive samples
is normal float chatter while three or more means the arm needs greasing. The
sorted-array shortcut for that variant, "keep it if
`levels[read] != levels[write - 2]`", does **not** transfer to unsorted data.
Constructing a series where it drops a sample it should keep, before writing
any code, is the exercise.

</details>

## Acceptance checklist

- [ ] `python exercise-04-stuck-gauge.py` prints `1 [300, 305, 300]`, then `All checks passed.`
- [ ] `[300, 300, 305, 300]` returns `1`, and you can say in one sentence why it is not `2`.
- [ ] `[]` returns `0` and does not raise.
- [ ] `[777, 777, 777, 777]` returns `3` with the list unchanged.
- [ ] The list is never truncated, cleared, or reassigned.
- [ ] You can state the `write <= read` invariant, with the `<=` and not a `<`, and say what it licenses.
- [ ] You can say why comparing against `levels[write - 1]` needs no proof and `levels[read - 1]` does.
- [ ] Your trace table for `[-2, -2, 0, 0, -2]` shows `read`, `write`, and the value compared against, at every step.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 1 exercise 4: stuck gauge`.
## Stretch

- **Keep at most two samples from any run.** Chatter is normal; a long stick
  is not.

  ```python
  def collapse_keeping_two(levels: list[int]) -> int:
      """Keep at most two samples from any run of equal adjacent samples."""
      write = 0
      for read in range(len(levels)):
          if write < 2 or levels[read] != levels[write - 2] or levels[write - 1] != levels[write - 2]:
              levels[write] = levels[read]
              write += 1
      return len(levels) - write
  ```

  ```text
  [412, 412, 412, 415, 415, 409] -> dropped 1, kept [412, 412, 415, 415, 409]
  [300, 300, 305, 300]           -> dropped 0, kept [300, 300, 305, 300]
  [777, 777, 777, 777]           -> dropped 2, kept [777, 777]
  ```

  That condition is longer than the sorted-array version for a reason. Work
  out which of its three clauses is the one the sorted version does not need,
  and construct the unsorted series that proves it.

- **Report the runs instead of collapsing them.** Return a list of
  `(level, run_length)` pairs. Now the hydrologist can ask "how long was the
  longest stick this year" directly. Notice this version cannot be `O(1)`
  space, and say why in one sentence — it is a property of the *output*, not
  of the algorithm.

- **Collapse from the other end.** Keep the *last* sample of each run rather
  than the first, still in place, still one pass. Decide first whether the
  answer differs from the current version at all, and on which input.

When your gauge record collapses correctly, move on to
[Exercise 5 — The Market Awning](./exercise-05-market-awning.md).
