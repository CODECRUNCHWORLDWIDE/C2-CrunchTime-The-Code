# Exercise 2 — The Scan Window

> **Topic:** the half-open convention, and one lower-bound search run twice to bracket a run of duplicates
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Easy/Medium
> **Target time:** 20 minutes
> **Why this one:** real data repeats. The moment a value appears more than once, "find it" stops being a question with one answer and becomes "find where the run starts and where it ends". This page teaches the one search that answers both, and it is the search you will reuse in Weeks 8 and 9 without changing a line.

## The Brief

A parcel hub's handheld scanners write one row into a shift log every time
somebody scans a parcel. Each row records the **minute of the week** it
happened — a number from `0` to `10_079`, because a week has `7 × 1440` of
them.

The log is written as things happen, so the minutes only ever go up or stay
the same. They stay the same *a lot*: during a shift changeover, thousands of
parcels get scanned inside the same minute.

```
index:   0   1   2   3   4   5
minute: 61  61  61  64  64  70
```

An auditor asks for every scan from minute `64`. Looking at the picture, the
answer is "rows 3 and 4". You are going to return that as a **slice**, which
in Python is written `log[3:5]` — start at 3, stop *before* 5.

That "stop before" is the whole shape of this exercise. It is called a
**half-open** range: the first number is included, the second is not. It looks
odd for about a day and then you never want anything else, because two
beautiful things fall out of it. The number of rows is just `end - start`. And
an empty answer has somewhere to live: `(3, 3)` is a perfectly good slice that
happens to contain nothing.

That second point is the contract decision here. If nobody scanned anything in
minute `62`, you do **not** return some failure code. You return `(3, 3)` —
the place a minute-62 row *would* go if one arrived. The caller writes
`log[start:end]` and gets an empty list, with no special case anywhere.

Return `(start, end)` such that `minutes[start:end]` is exactly the run for
that minute.

## Starter

Save this as `exercise-02-scan-window.py` and fill in every `TODO`.

```python
"""exercise-02-scan-window.py — the parcel-hub scan window.

One lower-bound helper, called twice, returns the half-open slice bounds of
every scan in a single minute.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
SHIFT_LOG: list[int] = [61, 61, 61, 64, 64, 70]


# ---- Your task ----
def lower_bound(minutes: list[int], minute: int) -> int:
    """Return the first index whose scan minute is >= `minute`.

    Args:
        minutes: Scan minutes, non-decreasing, duplicates expected.
        minute: The minute to place.

    Returns:
        The index at which `minute` would be written to keep the log ordered.
        That is len(minutes) when every scan is earlier.
    """
    # TODO: half-open interval [lo, hi) — hi starts at len(minutes)
    # TODO: loop while lo < hi
    # TODO: one shrink rule excludes mid, the other keeps it. Which is which?
    ...


def scan_window(minutes: list[int], minute: int) -> tuple[int, int]:
    """Return (start, end) with minutes[start:end] the run for `minute`.

    Args:
        minutes: Scan minutes, non-decreasing.
        minute: The minute the auditor asked for.

    Returns:
        Half-open slice bounds. On a miss both bounds are the insertion
        point, which makes the slice empty and still valid.
    """
    # TODO: two calls to lower_bound. What is the second one looking for?
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (64, 61, 70, 62, 99):
        start, end = scan_window(SHIFT_LOG, wanted)
        print(f"minute {wanted:3d} -> ({start}, {end})  count {end - start}  {SHIFT_LOG[start:end]}")

    assert scan_window(SHIFT_LOG, 64) == (3, 5)
    assert scan_window(SHIFT_LOG, 61) == (0, 3)
    assert scan_window(SHIFT_LOG, 70) == (5, 6)
    assert scan_window(SHIFT_LOG, 62) == (3, 3)
    assert scan_window(SHIFT_LOG, 0) == (0, 0)
    assert scan_window(SHIFT_LOG, 99) == (6, 6)
    assert scan_window([300, 300, 300, 300], 300) == (0, 4)
    assert scan_window([], 5) == (0, 0)
    assert SHIFT_LOG[0] == 61  # the log was never rearranged
    print("All checks passed.")
```

Two ideas you need before you start.

**Lower bound.** The first position whose value is **greater than or equal to**
what you asked for. Not "where is it" — "where does it begin, or where would
it begin". On the log above, the lower bound of `64` is `3`, and the lower
bound of `62` is also `3`, because that is where a 62 would slot in. One
search, two jobs.

**Half-open interval `[lo, hi)`.** The other package, the mirror of Exercise
1's. `hi` starts at `len(minutes)` — one past the end, which is a legal
*bound* even though it is not a legal index. The guard is `lo < hi`. And the
two shrink rules are no longer symmetrical: `lo = mid + 1` when `mid` has been
ruled out, and `hi = mid` when `mid` is still in the running, because `hi` is
excluded anyway. When the loop ends, `lo` and `hi` are the same number, and
that number is the answer.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/exercises/exercise-02-scan-window.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `lower_bound(minutes, minute)` returns the first index whose value is
   `>= minute`, and `len(minutes)` when there is no such index.
2. `scan_window(minutes, minute)` returns a tuple `(start, end)` where
   `minutes[start:end]` is exactly the run of scans for that minute.
3. On a miss it returns `(p, p)` — an empty slice at the insertion point —
   never `(-1, -1)` and never `None`.
4. `end - start` is the number of scans in that minute, with no extra work.
5. `scan_window` calls `lower_bound` twice and contains no loop of its own.
6. Neither function indexes `minutes` outside the loop. In particular nothing
   reads `minutes[start]` to test for a match.
7. Both searches use the half-open package: `hi = len(minutes)`, guard
   `lo < hi`, shrinks `mid + 1` and `mid`.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(minutes) <= 5_000_000`.** Five million scans is one week at a
  busy hub. The auditor runs this query per minute of interest, all week, so
  the cost of the query is what the tool is judged on.

- **`0 <= minutes[i] <= 10_079`, and duplicates are guaranteed.** A week holds
  10,080 minutes, so a five-million-row log has about five hundred rows per
  minute on average, and changeover minutes hold far more. This is the bound
  that kills the tempting shortcut — "find any match, then walk left and right
  to the ends of the run". That walk costs one step per row in the run, and
  here the runs are enormous. Two binary searches cost the same on a run of
  two as on a run of fifty thousand.

- **The log is non-decreasing, not strictly increasing.** The ties *are* the
  problem. A search that assumes distinct values still returns an index; it
  just returns an arbitrary one from the middle of the run, which is the
  hardest kind of wrong to notice.

- **`minute + 1` may be `10_080`, which is outside the value range, and that
  is fine.** A lower bound for a value larger than everything in the log
  returns `len(minutes)`, which is exactly the exclusive end you want. Never
  guard against it — the guard is what would break the last-minute case.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-scan-window.py
minute  64 -> (3, 5)  count 2  [64, 64]
minute  61 -> (0, 3)  count 3  [61, 61, 61]
minute  70 -> (5, 6)  count 1  [70]
minute  62 -> (3, 3)  count 0  []
minute  99 -> (6, 6)  count 0  []
All checks passed.
```

Read the last two lines together. Minute `62` is absent from the middle of the
log and minute `99` is past the end of it, and neither one needed a branch:
both searches landed on the same insertion point and the slice came out empty
on its own. Notice also that `(6, 6)` mentions index 6 on a log of six rows.
That is legal as a *bound* and illegal as an *index* — which is why
requirement 6 forbids reading `minutes[start]`.

## Steps

1. Save the starter and run it. Both functions return `Ellipsis`, so the first
   line fails while unpacking the tuple. Expected.
2. Write `lower_bound` first, and write the half-open package down before you
   type it: `hi = len(minutes)`, guard `lo < hi`, shrinks `mid + 1` and `mid`.
3. Inside the loop there is exactly one comparison: `minutes[mid] < minute`.
   If that is true, `mid` is too early to be the answer, so exclude it —
   `lo = mid + 1`. Otherwise `mid` might be the answer, so keep it —
   `hi = mid`.
4. Test `lower_bound` on its own before writing anything else. On the sample
   log it should give `3` for `64`, `3` for `62`, `0` for `0`, and `6` for
   `99`.
5. Now write `scan_window`. `start` is the lower bound of the minute itself.
   `end` is the lower bound of **the next minute** — the first row that is too
   late to belong to this one.
6. Run it, then delete the `62` row from your mental model and re-trace it.
   Convince yourself that no absent check is needed anywhere.
7. Try `[300, 300, 300, 300]` with `300`. If you had written the walk-outwards
   version, that input would read every row; yours reads about two.

## The Solution

```python
"""exercise-02-scan-window-solution.py - the parcel-hub scan window.

One lower-bound helper, called twice, returns the half-open slice bounds of
every scan in a single minute. A miss comes back as an empty slice sitting at
the insertion point, so the caller never has to special-case it.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SHIFT_LOG: list[int] = [61, 61, 61, 64, 64, 70]


# ---- Your task ----
def lower_bound(minutes: list[int], minute: int) -> int:
    """Return the first index whose scan minute is >= `minute`.

    Args:
        minutes: Scan minutes, non-decreasing, duplicates expected.
        minute: The minute to place.

    Returns:
        The index at which `minute` would be written to keep the log ordered.
        That is len(minutes) when every scan is earlier.
    """
    lo, hi = 0, len(minutes)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if minutes[mid] < minute:
            lo = mid + 1  # mid tested False, so exclude it
        else:
            hi = mid  # hi is exclusive, so mid is still a candidate
    return lo


def scan_window(minutes: list[int], minute: int) -> tuple[int, int]:
    """Return (start, end) with minutes[start:end] the run for `minute`.

    Args:
        minutes: Scan minutes, non-decreasing.
        minute: The minute the auditor asked for.

    Returns:
        Half-open slice bounds. On a miss both bounds are the insertion
        point, which makes the slice empty and still valid.
    """
    return lower_bound(minutes, minute), lower_bound(minutes, minute + 1)


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (64, 61, 70, 62, 99):
        start, end = scan_window(SHIFT_LOG, wanted)
        print(f"minute {wanted:3d} -> ({start}, {end})  count {end - start}  {SHIFT_LOG[start:end]}")

    assert scan_window(SHIFT_LOG, 64) == (3, 5)
    assert scan_window(SHIFT_LOG, 61) == (0, 3)
    assert scan_window(SHIFT_LOG, 70) == (5, 6)
    assert scan_window(SHIFT_LOG, 62) == (3, 3)
    assert scan_window(SHIFT_LOG, 0) == (0, 0)
    assert scan_window(SHIFT_LOG, 99) == (6, 6)
    assert scan_window([300, 300, 300, 300], 300) == (0, 4)
    assert scan_window([], 5) == (0, 0)
    assert SHIFT_LOG[0] == 61  # the log was never rearranged
    print("All checks passed.")
```

**One search does both jobs, because "where is it" and "where would it go"
are the same question.** `lower_bound` never asks whether the minute is
present. It asks where the boundary is between rows that are too early and
rows that are not. That boundary exists whether or not anything sits on it,
which is why the miss case needs no code.

**`end` is the lower bound of the *next* minute.** The first row too late to
belong to minute 64 is the first row that is at least 65. That row's index is
one past the end of the run, which is exactly what a half-open end means. Say
it as a sentence — "start is where this minute begins, end is where the next
one begins" — and the second call writes itself.

**The two shrink rules are asymmetric on purpose.** `lo = mid + 1` excludes
`mid`, because the comparison just proved `mid` is too early. `hi = mid` keeps
`mid` in play, because `hi` is the *excluded* end, so setting `hi = mid` means
"everything from `mid` onwards is still possible". Write `hi = mid - 1` here
and you throw away the very row you were looking for; write `lo = mid` and the
loop never ends.

**When the loop stops, `lo == hi`, and that single number is the answer.**
That is the post-loop assertion, and it is worth memorising in this form:
*after a lower-bound search, `lo` is the first index whose value is at least
the target*. Everything else on this page is a consequence of that one
sentence.

**The count is free.** `end - start` counts the rows in the slice without
building it. On a run of fifty thousand scans, that is one subtraction instead
of fifty thousand list items. If the auditor only wanted the number, you never
have to materialise anything at all.

**`(-1, -1)` would be worse than wrong.** It is *silently* wrong. Python
accepts negative indices, so `minutes[-1:-1]` is a legal expression that
evaluates to `[]` — the caller sees an empty list, decides everything is fine,
and never learns that the insertion point was thrown away. And if they write
`minutes[start]` instead, `-1` hands them the last scan in the whole log as if
it were a match.

## Run it

Copy the worked answer on this page into `exercise-02-scan-window.py` and run it:

```bash
python exercise-02-scan-window.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-02-scan-window.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the `minute = 99` row.** You added
  an absent check that reads `minutes[start]`:

  ```text
  Traceback (most recent call last):
      return SHIFT_LOG[start] == 99
             ~~~~~~~~~^^^^^^^
  IndexError: list index out of range
  ```

  `start` is `6` on a log of six rows, because "past the end" is a real
  insertion point. The deeper fix is not to guard the read — it is to delete
  it. This contract never needs to know whether the minute is present.

- **The program hangs.** You wrote `lo = mid` in the half-open loop. When the
  interval is two rows wide, `mid` comes out equal to `lo`, and setting
  `lo = mid` changes nothing. In this convention exactly one rule keeps `mid`,
  and it is the `hi` one.

- **Minute `70` comes back as `(5, 5)`.** You wrote `hi = mid - 1`. That
  excludes a row the comparison had not ruled out, so the boundary lands one
  too early and the last run in the log loses its only member. In the
  half-open convention `hi` is already exclusive; subtracting one excludes it
  twice.

- **Minute `64` comes back as `(3, 4)`.** Your second call is
  `lower_bound(minutes, minute)` again, or you subtracted one from `end` to
  "fix" it. `end` is *meant* to be one past the last match. That is what makes
  `minutes[start:end]` correct and `end - start` the count. Do not fix it.

- **Minute `64` comes back as `(4, 5)` or `(3, 3)` on a big log.** You reached
  for a plain find-any search, got some index inside the run, and used it as
  the start. Any of the three 61s is a legal answer to "find a 61", and none of
  them is the answer to "where does the run of 61s begin".

- **Returning `(-1, -1)` on a miss.** Nothing crashes, which is the problem —
  `SHIFT_LOG[-1:-1]` is `[]` and the caller believes you. Meanwhile the
  insertion point, the one genuinely useful fact about a missing minute, has
  been thrown away.

- **Mixing the two conventions.** `hi = len(minutes)` with a `lo <= hi` guard
  reads one past the end; `hi = len(minutes) - 1` with `lo < hi` can never
  return `len(minutes)`, so the after-everything case is unreachable. Each
  convention is a package of three decisions. Take all three or none.

## Under the hood

<details>
<summary>Under the hood — why two searches beat find-then-walk, and what bisect is doing</summary>

**The cost of walking outwards.**

Find-any-then-expand looks cheaper: one `O(log n)` search, then a walk to each
end of the run. Its real cost is `O(log n + r)` for a run of length `r`. On
this data `r` averages five hundred and spikes far higher, so the walk
dominates the search by two orders of magnitude. Two lower bounds cost
`O(log n)` flat, whatever `r` is.

Worth being precise about *when* find-then-walk wins: when runs are short and
you already know it. `r = 1` makes it two reads instead of about forty-six on
a five-million-row log. That is a real win — and it is a bet on your data
staying the way it looks today. The constraints here are written to make you
lose that bet.

**`bisect_left` and `bisect_right` are these two searches.**

```python
import bisect
start = bisect.bisect_left(minutes, minute)    # your lower_bound
end   = bisect.bisect_right(minutes, minute)   # == bisect_left(minutes, minute + 1)
```

`bisect_right` differs from `bisect_left` by one character in the comparison:
`<=` instead of `<`. That is the whole difference between "first index at
least the target" and "first index strictly greater than the target". On
integers, `bisect_right(v)` and `bisect_left(v + 1)` land on the same index —
which is why this page can get away with one helper. On floats or strings
there is no "next value" to add one to, and you would need both spellings.

Both are written in C and both accept `lo` and `hi` arguments so you can
search a slice without copying it. In production, use them. In an interview,
write the loop.

**Why half-open is the convention the whole language uses.**

`range(3, 5)` gives 3 and 4. `log[3:5]` gives two items. `len(log)` is a legal
slice bound. All of these are the same decision, made once, everywhere: the
end is excluded. Three properties follow, and they are why the choice was made:

- The length of a range is `end - start`, with no `+ 1` anywhere.
- An empty range is expressible without a special value: `(3, 3)`.
- Adjacent ranges join without overlap or gaps: `[0, 3)` then `[3, 5)`.

The last one is what makes this exercise's answer composable. Take every
minute's window in turn and you have partitioned the log, exactly, with no
row counted twice and none missed.

</details>

## Acceptance checklist

- [ ] `python exercise-02-scan-window.py` prints five rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] `scan_window` contains no loop and no absent check — just two calls.
- [ ] Both searches use the half-open package: `len`, `lo < hi`, `mid + 1` /
      `mid`.
- [ ] You can state the post-loop assertion in one sentence.
- [ ] Nothing in your code reads `minutes[start]`.
- [ ] `[300, 300, 300, 300]` with `300` returns `(0, 4)` and reads about two
      rows, not four.
- [ ] Committed to Git with a message like `Add Week 5 exercise 2: scan window`.

## Stretch

- **Add the count without the slice.** The auditor's dashboard only wants
  numbers.

  ```python
  def scan_count(minutes: list[int], minute: int) -> int:
      """Return how many scans happened in this minute."""
      start, end = scan_window(minutes, minute)
      return end - start
  ```

  ```text
  minute 61 -> 3 scans
  minute 62 -> 0 scans
  ```

  Time it against `minutes.count(minute)` on a large log. The list method is
  `O(n)` and reads every row; this is `O(log n)` and reads about forty-six.

- **Bracket a whole hour instead of a minute.** The bounds compose.

  ```python
  def hour_window(minutes: list[int], hour: int) -> tuple[int, int]:
      """Return the slice bounds of every scan in a given hour of the week."""
      return lower_bound(minutes, hour * 60), lower_bound(minutes, (hour + 1) * 60)
  ```

  ```text
  hour 1 -> (0, 6)  6 scans
  hour 2 -> (6, 6)  0 scans
  ```

  Nothing about the helper changed. That is the sign you built a boundary
  finder rather than a minute finder.

- **Write `upper_bound` explicitly and prove it agrees.** Copy `lower_bound`
  and change the comparison to `minutes[mid] <= minute`.

  ```text
  upper_bound(64)      = 5
  lower_bound(64 + 1)  = 5
  agree on all 10_080 minutes: True
  ```

  Then say out loud why the agreement only holds for integers. The answer is
  in the Under the hood block, and finding it yourself first is worth more.

When your windows are right, move on to
[Exercise 3 — The Ring Buffer Probe](./exercise-03-ring-buffer-probe.md).
