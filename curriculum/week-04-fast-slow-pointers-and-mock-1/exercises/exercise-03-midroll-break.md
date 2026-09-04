# Exercise 3 — The Mid-Roll Break

> **Topic:** fast and slow pointers — the speed-2 midpoint, and the guard shift that picks which middle you land on
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §5
> **Difficulty:** Easy
> **Target time:** 30 minutes with full FRAME narration
> **Why this one:** this is the fast/slow move you will reuse most often, and it is the first sub-step of both of this week's challenges. It is also the one people think they already know — the version most books print returns the *other* middle, and this spec wants this one.

## The Brief

A live stream is delivered as a chain of segments. The player holds only the
first segment and follows `next_segment` from there. There is no length field
and no way to jump to segment number 400, because segments are still being
added to the far end while the stream plays.

The ad server needs to put one mid-roll break somewhere near the middle. The
rule the product team wrote down is: **the ad plays straight after the earlier
of the two middle segments**, so that the first half is never shorter than the
second.

Think of a paper strip you fold in half. If the strip has an even number of
squares, the fold lands cleanly between two squares, and the rule says the ad
goes after the square on the left. If the strip has an odd number of squares,
there is one square in the middle and no argument to have.

Return that segment together with how many segments come **before** it. Return
`None` for an empty stream.

Here is the trick this page is built around. The obvious way to find a middle
is to count the segments and then walk half that far — two passes. You cannot
do that here. The stream is still growing, so the second pass may see a longer
stream than the first one counted, and you would land in the wrong place. You
get **one** pass.

One pass is enough because of the tortoise and hare from
[Exercise 1](./exercise-01-conveyor-loop.md), used for something other than
finding a loop. Move one pointer one segment at a time and another two segments
at a time. When the fast one runs out of stream, the slow one has covered
exactly half. It has been in the middle the whole time; you just have to stop
at the right moment.

**Six segments, and which middle you get.** For `s1 s2 s3 s4 s5 s6` the two
middles are `s3` and `s4`. This spec wants `s3`, giving the split
`s1 s2 s3 | s4 s5 s6`. Most published versions of this move return `s4`. The
difference is one line, and the whole drill is knowing which line.

## Starter

Create `exercise-03-midroll-break.py` and paste this in. Fill in every `TODO`.

```python
"""exercise-03-midroll-break.py — where does the mid-roll ad go?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per stream and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Segment:
    """One block of a live stream. You can only follow it forward."""

    def __init__(self, segment_id: str, next_segment: "Segment | None" = None) -> None:
        self.segment_id = segment_id
        self.next_segment = next_segment


def build_stream(ids: list[str]) -> list[Segment]:
    """Wire a stream from a list of segment ids and hand back every segment.

    Args:
        ids: One id per segment, in play order. Ids may repeat.

    Returns:
        The segments, in order. Empty when `ids` is empty.
    """
    segments = [Segment(segment_id) for segment_id in ids]
    for earlier, later in zip(segments, segments[1:]):
        earlier.next_segment = later
    return segments


def mid_roll_point(first: Segment | None) -> tuple[Segment, int] | None:
    """Return the mid-roll segment and how many segments come before it.

    Args:
        first: The first segment of the stream, or None for an empty stream.

    Returns:
        A pair of (segment, count of segments strictly before it), or None
        for an empty stream. For an even number of segments this is the
        *earlier* of the two middles, so the first half is never shorter
        than the second.
    """
    # TODO 1: an empty stream has no middle. Return None before the loop —
    #         the guard below reaches inside `fast`, so `fast` must exist.
    # TODO 2: walk `slow` one segment per turn and `fast` two, counting the
    #         segments `slow` leaves behind it.
    # TODO 3: stop when there are fewer than two segments left in front of
    #         `fast`, then return the pair.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("s1 -> s2 -> s3 -> s4 -> s5", 5, 2),
        ("s1 -> ... -> s6", 6, 2),
        ("s1 -> s2 -> s3 -> s4", 4, 1),
        ("s1 -> s2 -> s3", 3, 1),
        ("s1 -> s2", 2, 0),
        ("s1", 1, 0),
        ("s1 -> ... -> s7", 7, 3),
    ]

    for shape, count, expected_index in CASES:
        segments = build_stream([f"s{number}" for number in range(1, count + 1)])
        result = mid_roll_point(segments[0])
        assert result is not None, f"{shape}: this stream is not empty"
        segment, before = result
        assert segment is segments[expected_index], f"{shape}: wrong segment"
        assert before == expected_index, f"{shape}: wrong offset"
        print(f"{shape:<28} break after {segment.segment_id}, {before} before it")

    markers = build_stream(["AD", "AD", "AD", "AD"])
    marker_segment, marker_before = mid_roll_point(markers[0])
    assert marker_segment is markers[1], "four identical ids: position is the answer"
    assert marker_before == 1
    print(f"{'AD -> AD -> AD -> AD':<28} break after AD, {marker_before} before it")

    assert mid_roll_point(None) is None, "an empty stream has no mid-roll point"
    print(f"{'(empty stream)':<28} no break")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-03-midroll-break.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `mid_roll_point(first)` returns a pair of `(segment, count before it)`, or
   `None` for an empty stream. It never returns `(None, 0)`.
2. For an even number of segments it returns the **earlier** of the two
   middles.
3. The count is of segments strictly before the returned one, so a one-segment
   stream gives `0`.
4. The first element of the pair is the `Segment` object, not its id.
5. One pass over the stream. No counting pass, no list, no `len`.
6. Segments are compared with `is`; ids are never used to decide position.
7. `mid_roll_point` keeps its type hints and its docstring.

## Constraints

- **Single pass, and this bound is not about speed.** Counting first and then
  walking half is also O(n), so complexity is not the argument. The argument is
  that the chain is still growing: between the counting pass and the walking
  pass, more segments arrive, and half of the new length is not the middle of
  the old one. Say that distinction out loud. Claiming the two-pass version is
  "slower" when it is not costs you credibility with anyone who checks.

- **Up to 100,000 segments, and the memory you use must not grow with that
  number.** The player runs on set-top hardware with a fixed frame budget.
  Copying the chain into a Python list makes this problem trivial by index and
  is exactly what the hardware cannot afford.

- **Segment ids are opaque and repeat.** An ad-insertion marker segment carries
  the same id every time it appears, so an id tells you nothing about where you
  are. One of the checks is a four-segment stream where every id is `AD`, and
  the assertion compares by identity.

- **The empty stream returns `None`, not `(None, 0)`.** A caller writing
  `segment, offset = mid_roll_point(head)` should fail loudly rather than
  quietly schedule an advert at position zero of a stream that does not exist.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-midroll-break.py
s1 -> s2 -> s3 -> s4 -> s5   break after s3, 2 before it
s1 -> ... -> s6              break after s3, 2 before it
s1 -> s2 -> s3 -> s4         break after s2, 1 before it
s1 -> s2 -> s3               break after s2, 1 before it
s1 -> s2                     break after s1, 0 before it
s1                           break after s1, 0 before it
s1 -> ... -> s7              break after s4, 3 before it
AD -> AD -> AD -> AD         break after AD, 1 before it
(empty stream)               no break
All checks passed.
```

Compare lines one and two. Five segments and six segments give the *same*
answer, `s3`. That is what the lower-middle convention means, and it is the
quickest way to check you implemented the right one: if six segments gives you
`s4`, you have the other convention. Line three is the shortest example where
the two disagree.

## Steps

1. **Frame.** Restate the ask, and say the convention out loud: the earlier of
   the two middles. Then ask the question a good candidate asks anyway — *which
   middle do you want?* — even though the spec answers it. Asking is graded
   even when the answer is written down.
2. **Research constraints.** Say why the two-pass version is rejected, in the
   right words: the chain grows, not "it is slower". Note the repeated ids.
   Note that the empty case must be handled before the loop, because the guard
   you are about to write reaches inside `fast`.
3. **Assess options.** Two-pass count-then-walk: simple, same big-O, wrong
   under a growing chain. Copy to a list: trivial, O(n) space, rejected by the
   set-top box. Fast and slow: one pass, fixed memory, and the only decision
   left is where the guard looks.
4. **Make the solution.** Write the empty check, then the loop. Get the guard
   right by asking what it must be true for you to take another double step:
   there have to be two more segments in front of `fast`.
5. **Examine, odd length.** Trace `s1 -> s2 -> s3 -> s4 -> s5`. slow=s1,
   fast=s1, before=0. `fast.next` is s2 and `fast.next.next` is s3, both there,
   so step: slow=s2, fast=s3, before=1. Still two ahead (s4, s5), so step:
   slow=s3, fast=s5, before=2. Now `fast.next` is `None` — stop. Answer
   `(s3, 2)`.
6. **Examine, even length.** Trace `s1 -> ... -> s6`. Same first two turns, so
   slow=s3, fast=s5, before=2. Guard: `fast.next` is s6, but `fast.next.next`
   is `None` — stop. Answer `(s3, 2)`. Lower middle, correct. **Trace both
   parities every time.** An odd-length trace can never catch this bug, because
   both conventions agree on odd lengths.
7. **Examine, cost.** O(n) time — the body runs about half as many times as
   there are segments and each turn is constant work. O(1) space — two pointers
   and an integer. And O(n) is the floor: you cannot know where the middle is
   without touching at least half the chain, and you cannot know the length
   without touching all of it.

## The Solution

```python
"""exercise-03-midroll-break-solution.py — where does the mid-roll ad go?

One walk. The slow pointer takes one segment per turn and the fast pointer
takes two, so when the fast one runs out of stream the slow one is standing
in the middle. The loop guard looks one segment *ahead* of the fast
pointer, which is what makes it stop on the earlier of the two middles.

The streams are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per stream, then
"All checks passed."
"""

from __future__ import annotations


class Segment:
    """One block of a live stream. You can only follow it forward."""

    def __init__(self, segment_id: str, next_segment: "Segment | None" = None) -> None:
        self.segment_id = segment_id
        self.next_segment = next_segment


def build_stream(ids: list[str]) -> list[Segment]:
    """Wire a stream from a list of segment ids and hand back every segment.

    Args:
        ids: One id per segment, in play order. Ids may repeat.

    Returns:
        The segments, in order. Empty when `ids` is empty. The caller reads
        `segments[0]` for the first segment and uses the rest to check
        answers by identity rather than by id.
    """
    segments = [Segment(segment_id) for segment_id in ids]
    for earlier, later in zip(segments, segments[1:]):
        earlier.next_segment = later
    return segments


def mid_roll_point(first: Segment | None) -> tuple[Segment, int] | None:
    """Return the mid-roll segment and how many segments come before it.

    Args:
        first: The first segment of the stream, or None for an empty stream.

    Returns:
        A pair of (segment, count of segments strictly before it), or None
        for an empty stream. For an even number of segments this is the
        *earlier* of the two middles, so the first half is never shorter
        than the second.
    """
    if first is None:
        return None

    slow = first
    fast = first
    before = 0
    while fast.next_segment is not None and fast.next_segment.next_segment is not None:
        slow = slow.next_segment
        fast = fast.next_segment.next_segment
        before += 1
    return slow, before


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("s1 -> s2 -> s3 -> s4 -> s5", 5, 2),
        ("s1 -> ... -> s6", 6, 2),
        ("s1 -> s2 -> s3 -> s4", 4, 1),
        ("s1 -> s2 -> s3", 3, 1),
        ("s1 -> s2", 2, 0),
        ("s1", 1, 0),
        ("s1 -> ... -> s7", 7, 3),
    ]

    for shape, count, expected_index in CASES:
        segments = build_stream([f"s{number}" for number in range(1, count + 1)])
        result = mid_roll_point(segments[0])
        assert result is not None, f"{shape}: this stream is not empty"
        segment, before = result
        assert segment is segments[expected_index], f"{shape}: wrong segment"
        assert before == expected_index, f"{shape}: wrong offset"
        print(f"{shape:<28} break after {segment.segment_id}, {before} before it")

    markers = build_stream(["AD", "AD", "AD", "AD"])
    marker_segment, marker_before = mid_roll_point(markers[0])
    assert marker_segment is markers[1], "four identical ids: position is the answer"
    assert marker_before == 1
    print(f"{'AD -> AD -> AD -> AD':<28} break after AD, {marker_before} before it")

    assert mid_roll_point(None) is None, "an empty stream has no mid-roll point"
    print(f"{'(empty stream)':<28} no break")

    print("All checks passed.")
```

**The guard is the whole exercise.**

```python
    while fast.next_segment is not None and fast.next_segment.next_segment is not None:
```

Read it as a question asked before each turn: *are there two more segments in
front of `fast`?* If yes, take another double step. If no, stop — and wherever
`slow` is standing when you stop is the answer.

The other convention asks a slightly different question — *is `fast` on a
segment, and is there one more after it?* — written `while fast is not None and
fast.next_segment is not None`. That version keeps going for one more turn on
even-length streams and lands `slow` on the later middle. One position of
difference in where the guard looks; one segment of difference in the answer.
Nothing else changes.

**Why the empty check has to come first.** This guard reaches inside `fast` on
its very first evaluation. If `fast` is `None`, that is an `AttributeError`
before the loop body has run once. The other convention's guard tests `fast`
itself first, so it survives an empty chain without help — which is precisely
why copying its shape while intending this convention breaks silently on one
input and works on all the others.

**The counter is free.** `before` starts at `0`, which is where `slow` starts,
and goes up once per slow step. It is not a separate pass and it costs nothing;
it just records how far the walk got. Starting it at `1` counts the segment
`slow` is standing on, which is not what "before it" means.

**Why one pass is enough at all.** Fast covers two segments for every one slow
covers. When fast has run out of stream it has covered the whole thing, so slow
has covered half of it. There is no cleverness hiding in the algorithm — the
speeds do the arithmetic, and the guard decides exactly which turn is the last
one.

**Returning `None` rather than `(None, 0)` is a contract decision, not a
detail.** A pair containing `None` unpacks happily and the caller carries on
believing there is a segment. A bare `None` fails at the unpacking line, in the
caller's own code, with a message naming what went wrong. Fail where the
mistake is, not three functions later.

## Run it

Copy the worked answer on this page into `exercise-03-midroll-break.py` and run it:

```bash
python exercise-03-midroll-break.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-midroll-break.py`.

To grade your own file against the week's larger cases, including
thousand-segment streams of both parities:

```bash
C2_WEEK04_SOLUTIONS=exercise-03-midroll-break pytest timed_runner.py -v -k mid_roll
```

See [`timed_runner.py`](./timed_runner.py) for the full case list.

## Common bugs to catch

- **Returning the later middle.** The four-segment stream gives `s3` instead of
  `s2`. No exception — just an ad in the wrong place, and a bug that passes
  every odd-length test you write. The fix is the guard, and only the guard:
  `fast.next_segment and fast.next_segment.next_segment`, not
  `fast and fast.next_segment`.

- **`AttributeError: 'NoneType' object has no attribute 'next_segment'`.** You
  put the empty check after the loop, or left it out:

  ```text
  Traceback (most recent call last):
      while fast.next_segment is not None and fast.next_segment.next_segment is not None:
            ^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'next_segment'
  ```

  `fast` is `None`, and this guard asks `None` for a `next_segment` before the
  loop has done anything at all. Handle the empty stream first.

- **`TypeError: cannot unpack non-iterable NoneType object`.** The caller
  unpacked the result of an empty stream:

  ```text
  Traceback (most recent call last):
      segment, before = mid_roll_point(None)
      ^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  That is the contract working as designed. It is the loud failure that
  `(None, 0)` would have hidden.

- **Off-by-one in the counter.** `before` counts segments *before* the answer.
  Initialising it to `1`, or bumping it after the loop, makes a one-segment
  stream report `1` when nothing precedes the only segment there is.

- **Returning the id instead of the segment.** Read the signature: the first
  element of the pair is a `Segment`. A caller needs the object so it can keep
  walking from there.

- **Deciding position from ids.** The `AD -> AD -> AD -> AD` check exists for
  this. Every id is the same string, so any comparison of ids gives you the
  first segment, and the assertion compares by identity and catches it.

## Under the hood

<details>
<summary>Under the hood — the four guard shapes, and why this one is the odd one out</summary>

There are four ways to write a midpoint guard and they are worth laying side by
side once, because after that you can derive the one you need instead of
remembering it.

| Guard | 4 segments | 5 segments | Safe on empty? |
|---|---|---|---|
| `fast and fast.next` | `s3` (upper) | `s3` | yes |
| `fast.next and fast.next.next` | `s2` (lower) | `s3` | **no** |
| `fast and fast.next` with `slow` started one back | `s2` | `s2` | needs a dummy |
| count then walk `n // 2` | `s3` | `s3` | yes, two passes |

Two things fall out of the table. First, the two one-pass conventions agree on
odd lengths and differ on even ones, which is why an odd-length test can never
tell you which one you wrote. Second, only the lower-middle guard is unsafe on
an empty chain, because it is the only one that dereferences before testing.
That asymmetry is not a wart in Python; it follows from the guard having to
look one place further ahead.

**Where the lower middle is the one you want.** Any time you are about to
*split* the chain. The lower middle is the last node of the front half, so
`front = first … middle` and `back = middle.next …`, and the front half is
never shorter. Both of this week's challenges and one homework problem start
exactly there:

- [Challenge 1 — Booklet Imposition](../challenges/challenge-01-booklet-imposition.md)
  cuts after it and zips the halves back together.
- [Homework Problem 3 — The Symmetric Die Sequence](../homework/problem-03-symmetric-dies.md)
  cuts after it and compares the halves.

If you had the upper middle, the front half would be the *shorter* one on odd
lengths, the leftover element would belong to the back half instead, and every
piece of tail-handling downstream would need rewriting. That is why this
convention is the one the drill teaches.

**A cheap way to remember which is which.** The guard that looks further ahead
stops earlier, and stopping earlier leaves you further back — on the lower
middle. Look ahead, land behind.

</details>

## Acceptance checklist

- [ ] `python exercise-03-midroll-break.py` prints nine lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] Six segments and five segments both return `s3`.
- [ ] The empty stream is handled **before** the loop, and returns `None`.
- [ ] One pass. No `len`, no list, no counting pass.
- [ ] Segments are compared with `is`; nothing compares `segment_id`.
- [ ] Your write-up traces one odd-length and one even-length stream.
- [ ] Your write-up says why the two-pass version is rejected *without*
      claiming it is asymptotically worse — because it is not.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/exercise-03-midroll-break.md`
      with a recording of at least 8 minutes.

## Stretch

- **Add the other convention beside it and prove they differ.** Write
  `upper_mid_roll_point` with the guard `fast is not None and
  fast.next_segment is not None`, then print both for streams of length 1 to 6:

  ```python
  def upper_mid_roll_point(first: Segment | None) -> tuple[Segment, int] | None:
      """The other convention: the later of the two middles."""
      if first is None:
          return None
      slow = fast = first
      before = 0
      while fast is not None and fast.next_segment is not None:
          slow = slow.next_segment
          fast = fast.next_segment.next_segment
          before += 1
      return slow, before
  ```

  ```text
  1 segments   lower s1   upper s1
  2 segments   lower s1   upper s2
  3 segments   lower s2   upper s2
  4 segments   lower s2   upper s3
  5 segments   lower s3   upper s3
  6 segments   lower s3   upper s4
  ```

  Every even row disagrees and every odd row agrees. That table is worth one
  line in your notes.

- **Split the stream into two halves and return both heads.** Cut after the
  lower middle and hand back the pair. This is the first sub-step of both
  challenges, and doing it now makes them shorter:

  ```python
  def split_stream(first: Segment | None) -> tuple[Segment | None, Segment | None]:
      """Cut after the lower middle. The front half is never the shorter one."""
      found = mid_roll_point(first)
      if found is None:
          return None, None
      middle, _ = found
      back = middle.next_segment
      middle.next_segment = None
      return first, back
  ```

  ```text
  6 segments   front s1 s2 s3   back s4 s5 s6
  5 segments   front s1 s2 s3   back s4 s5
  1 segment    front s1         back (empty)
  ```

- **Place two breaks instead of one, at a third and two thirds.** Same idea
  with a speed-3 hare, or with two slow pointers set off at different times.
  Work out the guard yourself rather than looking it up; the reasoning is the
  same question — *how many segments must be in front of `fast` for another
  step to be legal?*
When both parities trace clean, move on to
[Exercise 4 — The Wear-Level Rotation](./exercise-04-wear-level-rotation.md).
