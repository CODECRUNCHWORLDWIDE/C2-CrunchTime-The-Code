# Challenge 1 — The Tide Board Digest

> **Topic:** two topics at once — pulling fields out of hand-typed strings, and grouping what survives into a dict
> **Lecture:** [01 — Strings and the Cost of Immutability](../lecture-notes/01-strings-and-immutability.md) and [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** the exercises drilled one idea each. Real work never arrives that way. This one hands you text that is sometimes not data at all, asks you to reject it without stopping, and then asks for a summary where the rule changes depending on the group — the highest reading for one state, the lowest for the other. Two things to get right at once, and a shape you will meet every time a program reads a file.

## The Brief

A harbour keeps a tide board by the lock gate. Whoever is on duty types a line
into a tablet every time the water turns:

```text
0612 HW 3.42 north quay
```

Four fields, separated by spaces: the **time** on a 24-hour clock, the
**state** — `HW` for high water, `LW` for low water — the **height** in metres,
and where it was read. The place can be more than one word.

The board has been running for years and the log is not clean. Somebody typed
`bad line` while testing. Somebody typed `XX` for the state. Somebody wrote
`high` where the height should be. Your program must read what it can, quietly
put the rest aside, and **count how many it put aside** — because a log where
one line in three is unreadable is a broken tablet, and the harbour master
wants to know.

Then the summary. One row per state, and each row says three things:

- how many readings that state got,
- the **extreme** reading, which means the **highest** height for `HW` and the
  **lowest** for `LW`,
- **every** time that hit that extreme, in log order — not the first one, all
  of them.

That extreme rule is the part to slow down on. High water and low water are
opposite questions. A program that takes the maximum of both is right half the
time, gives a completely plausible number for the other half, and nobody
notices until a boat goes aground.

## Starter

Create `challenge-01-tide-board-digest.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""challenge-01-tide-board-digest.py — summarise the harbour log.

Read what can be read, put the rest aside and count it, then report one row
per water state with every time that hit the extreme.

Strings go in. A dict does the grouping. A string comes out.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from typing import NamedTuple

STATES = ("HW", "LW")

LOG: list[str] = [
    "0612 HW 3.42 north quay",
    "1104 LW 0.85 north quay",
    "1231 HW 3.60 boat pound",
    "bad line",
    "1755 LW 0.85 boat pound",
    "1840 HW 3.60 north quay",
    "2033 LW 1.20 slipway",
    "0700 XX 2.00 north quay",
    "0930 HW high boat pound",
]


class StateDigest(NamedTuple):
    """One state's summary: how many readings, the extreme, and its times."""

    count: int
    extreme: float
    times: list[str]


def is_clock(text: str) -> bool:
    """Return True when `text` is a four-digit 24-hour time."""
    # TODO: four digits, hours under 24, minutes under 60
    ...


def parse_line(line: str) -> tuple[str, str, float, str] | None:
    """Turn one log line into a reading, or reject it.

    Args:
        line: One raw line from the board.

    Returns:
        (clock, state, height, place), or None when the line is unreadable.
    """
    # TODO: split(), check the field count, check the clock and the state,
    # try float() for the height, and join the rest back into the place
    ...


def digest(lines: list[str]) -> dict[str, StateDigest]:
    """Summarise the readable lines, one entry per water state."""
    # TODO: group into a dict first, then reduce each group. max for HW,
    # min for LW, and keep EVERY time that matched.
    ...


def skipped(lines: list[str]) -> int:
    """Count the lines the parser refused."""
    ...


def report(lines: list[str]) -> str:
    """Render the whole digest as text, no trailing newline."""
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(report(LOG))

    summary = digest(LOG)
    assert list(summary) == ["HW", "LW"]
    assert summary["HW"].count == 3
    assert summary["HW"].extreme == 3.60
    assert summary["HW"].times == ["1231", "1840"]
    assert summary["LW"].extreme == 0.85
    assert summary["LW"].times == ["1104", "1755"]
    assert skipped(LOG) == 3
    assert parse_line("0612 HW 3.42 north quay") == ("0612", "HW", 3.42, "north quay")
    assert parse_line("2400 HW 3.42 north quay") is None
    assert parse_line("0612 HW 3.42") is None
    assert digest([]) == {}
    assert report([]) == "skipped 0 unreadable lines"
    assert LOG[3] == "bad line"  # the log is untouched
    print("All checks passed.")
```

Four things you need before you start.

**`line.split()` with no argument** splits on runs of whitespace and throws
away the ends. `line.split(" ")` splits on every single space and hands you
empty strings for the doubles. On hand-typed input the first one is almost
always what you want.

**`float("high")` raises.** There is no "did this work?" version of `float`, so
the shape is `try: … except ValueError: return None`. That is not defensive
programming for its own sake; converting text somebody typed is exactly the
case `try` exists for.

**A `NamedTuple`** is a tuple with names written on its boxes. `entry.extreme`
instead of `entry[1]`. You get it by writing a small class, and the result is
still a plain immutable tuple underneath.

**`max` and `min` both take a `key`,** and here you do not need one — you are
reducing a list of plain numbers. What you do need is to pick *which of the two
functions* to call, per group, and the neat way to do that is to put the
function itself in a variable: `pick = max if state == "HW" else min`.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/challenges/challenge-01-tide-board-digest.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `is_clock` accepts exactly four digits, hours `00`–`23`, minutes `00`–`59`.
2. `parse_line` returns `None` for: fewer than four fields, a bad clock, a
   state that is not `HW` or `LW`, or a height that is not a number. It never
   raises.
3. The place is everything after the height, joined back together with single
   spaces.
4. `digest` returns states in the order each was **first read**, not
   alphabetically.
5. For each state, `extreme` is the maximum height for `HW` and the minimum for
   `LW`, and `times` holds **every** clock that reached it, in log order.
6. `skipped` counts the rejected lines.
7. `report` prints one line per state and then the skipped count, with the
   height to two decimal places.
8. `digest([])` is `{}` and `report([])` still prints its skipped line.
9. `LOG` is unchanged. Every function keeps its type hints and its docstring.

## Constraints

- **A bad line must never stop the program.** This is the whole reason the log
  has three broken lines in it. A parser that raises on the fourth line reports
  nothing about the first three, and a night's readings are lost because
  somebody fat-fingered a tablet. Reject and continue.

- **Reject by returning `None`, not by raising and catching upstairs.**
  Exceptions are for the unexpected. A hand-typed log containing rubbish is
  expected. Returning `None` puts the decision where the knowledge is — inside
  the parser — and lets the caller write one `if parsed is None: continue`.

- **Group first, reduce second.** Walk the log once, dropping each reading into
  its state's list. *Then* take the extreme of each list. The tempting
  alternative — walking the whole log once per state — is `O(states × lines)`
  and gets slower every time somebody invents a new state code.

- **Keep every tying time, not the first.** `times` is a list because a tie is
  normal: the tide reaches the same height twice a day, near enough. A function
  that returns one time looks correct against every example where the tie does
  not happen, which is most of them. Both states in this log tie, on purpose.

- **Compare the heights as `float`, never as text.** `"3.60" > "3.6"` is
  `False` as text and `3.60 == 3.6` is `True` as numbers. Converting once, in
  the parser, means nothing downstream has to remember which it is holding.

- **At most 20,000 lines, and at most six states.** A tide board writes four
  lines a day, so twenty thousand is roughly fifteen years of harbour history —
  which is what somebody will hand you when they say "can you check the whole
  log". Six states is `HW`, `LW`, and room for the harbour to invent four more
  without your code caring. Neither bound rules anything out; both say the
  cheap single-pass version is comfortably enough, and that is worth stating
  rather than assuming.

- **Two decimal places in the report, always.** `f"{3.6:.2f}"` gives `3.60`.
  Printing the raw float gives `3.6` for one reading and `3.42` for another, so
  the column will not line up — and a tide height with an implied trailing zero
  is how somebody reads 3.6 metres as 3.06.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-tide-board-digest.py
HW  3 readings  extreme 3.60 m at 1231, 1840
LW  3 readings  extreme 0.85 m at 1104, 1755
skipped 3 unreadable lines
All checks passed.
```

Three lines, and every one of them is a decision. `HW` reports `3.60`, the
**highest** of `3.42, 3.60, 3.60`. `LW` reports `0.85`, the **lowest** of
`0.85, 0.85, 1.20` — if that row says `1.20`, you took the maximum of both
states. Both rows list two times, because both extremes were hit twice. And
three lines were skipped: the test line, the unknown state, and the height that
was a word.

## Steps

1. Create the file, paste the starter, and run it. `report` returns `None` and
   printing it prints `None` — no traceback, which is worth noticing on its
   own.
2. Write `is_clock` and test it by hand on `"0612"`, `"2400"`, `"12:30"`,
   `"612"` and `""` before going near the log.
3. Write `parse_line`. Do the cheap checks first — field count, then clock and
   state — and leave the `try`/`float` until last, because it is the only part
   that costs anything.
4. Run `[parse_line(line) for line in LOG]` in a REPL and read all nine
   results. Six tuples and three `None`s, and you should be able to say which
   is which without looking at the log.
5. Write `digest` in two halves, with a blank line between them. First half:
   one pass, `readings.setdefault(state, []).append((clock, metres))`. Second
   half: loop over that dict and reduce each list.
6. Get the extreme rule right before you get the times right. Print each
   state's extreme on its own first.
7. Now the times: `[clock for clock, metres in seen if metres == extreme]`.
   That is a second pass over one group, which is fine — it is `O(group)`, and
   the alternative is tracking a running list of ties inside a `max` you wrote
   by hand, which is four more lines and a bug.
8. Write `skipped` and `report`. Compare your three lines to the expected
   output character for character.

## The Solution

```python
"""challenge-01-tide-board-digest-solution.py — summarise the harbour log.

The tide board's log is a list of hand-typed lines. Some of them are not
lines at all. This program reads what it can, throws away what it cannot,
and reports one row per water state with every time that hit the extreme.

Strings go in. A dict does the grouping. A string comes out.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from typing import NamedTuple

STATES = ("HW", "LW")

LOG: list[str] = [
    "0612 HW 3.42 north quay",
    "1104 LW 0.85 north quay",
    "1231 HW 3.60 boat pound",
    "bad line",
    "1755 LW 0.85 boat pound",
    "1840 HW 3.60 north quay",
    "2033 LW 1.20 slipway",
    "0700 XX 2.00 north quay",
    "0930 HW high boat pound",
]


class StateDigest(NamedTuple):
    """One state's summary: how many readings, the extreme, and its times."""

    count: int
    extreme: float
    times: list[str]


def is_clock(text: str) -> bool:
    """Return True when `text` is a four-digit 24-hour time.

    Args:
        text: The first field of a log line.

    Returns:
        True for "0000" through "2359", False for anything else.
    """
    if len(text) != 4 or not text.isdigit():
        return False
    return int(text[:2]) < 24 and int(text[2:]) < 60


def parse_line(line: str) -> tuple[str, str, float, str] | None:
    """Turn one log line into a reading, or reject it.

    Args:
        line: One raw line from the board.

    Returns:
        (clock, state, height, place), or None when the line is unreadable.
    """
    parts = line.split()
    if len(parts) < 4:
        return None
    clock, state, height = parts[0], parts[1], parts[2]
    if not is_clock(clock) or state not in STATES:
        return None
    try:
        metres = float(height)
    except ValueError:
        return None
    return clock, state, metres, " ".join(parts[3:])


def digest(lines: list[str]) -> dict[str, StateDigest]:
    """Summarise the readable lines, one entry per water state.

    Args:
        lines: The raw log, unreadable lines and all.

    Returns:
        A dict from state to its StateDigest, states in the order each was
        first read. The extreme is the highest height for HW and the lowest
        for LW; times holds every clock that reached it, in log order.
    """
    readings: dict[str, list[tuple[str, float]]] = {}
    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            continue
        clock, state, metres, _place = parsed
        readings.setdefault(state, []).append((clock, metres))

    summary: dict[str, StateDigest] = {}
    for state, seen in readings.items():
        pick = max if state == "HW" else min
        extreme = pick(metres for _clock, metres in seen)
        summary[state] = StateDigest(
            count=len(seen),
            extreme=extreme,
            times=[clock for clock, metres in seen if metres == extreme],
        )
    return summary


def skipped(lines: list[str]) -> int:
    """Count the lines the parser refused.

    Args:
        lines: The raw log.

    Returns:
        How many lines could not be read as a reading.
    """
    return sum(1 for line in lines if parse_line(line) is None)


def report(lines: list[str]) -> str:
    """Render the whole digest as text.

    Args:
        lines: The raw log.

    Returns:
        One line per state, then one line counting the rejects. No trailing
        newline.
    """
    rows = []
    for state, entry in digest(lines).items():
        times = ", ".join(entry.times)
        rows.append(
            f"{state}  {entry.count} readings  "
            f"extreme {entry.extreme:.2f} m at {times}"
        )
    rows.append(f"skipped {skipped(lines)} unreadable lines")
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(report(LOG))

    summary = digest(LOG)
    assert list(summary) == ["HW", "LW"]
    assert summary["HW"].count == 3
    assert summary["HW"].extreme == 3.60
    assert summary["HW"].times == ["1231", "1840"]
    assert summary["LW"].extreme == 0.85
    assert summary["LW"].times == ["1104", "1755"]
    assert skipped(LOG) == 3
    assert parse_line("0612 HW 3.42 north quay") == ("0612", "HW", 3.42, "north quay")
    assert parse_line("2400 HW 3.42 north quay") is None
    assert parse_line("0612 HW 3.42") is None
    assert digest([]) == {}
    assert report([]) == "skipped 0 unreadable lines"
    assert LOG[3] == "bad line"  # the log is untouched
    print("All checks passed.")
```

**`parse_line` is a run of cheap rejections and one expensive one.**

```python
parts = line.split()
if len(parts) < 4:
    return None
```

Every check that can be made without allocating anything is made first. The
`try`/`float` is last because it is the only step that can raise, and doing it
last means it only ever runs on lines that already look right. That ordering is
free to write and it is the shape of every validator you will ever write.

Notice `len(parts) < 4` and not `!= 4`: the place is allowed to be several
words. `" ".join(parts[3:])` puts it back together, and it comes back
single-spaced no matter how it was typed, because `split()` threw the extra
spaces away and `join` put exactly one back. That is a normalising round trip
you get for nothing.

**`digest` groups, then reduces, and the two halves do not interleave.**

```python
readings.setdefault(state, []).append((clock, metres))
```

One pass. `setdefault` handles the first time each state appears — Exercise 4's
idiom, unchanged. The dict remembers insertion order, so `HW` comes before `LW`
in the report because `HW` was read first, and nothing sorted anything.

Then the reduce:

```python
pick = max if state == "HW" else min
extreme = pick(metres for _clock, metres in seen)
```

**A function is a value.** `pick` holds `max` or `min` and is then called.
That is one line where the obvious version is an `if` with two nearly-identical
branches inside it, and two nearly-identical branches are where a fix lands in
one of them.

**The times need a second look at the group, and that is the cheap way.**
Finding the extreme and collecting everything that ties it in a single pass
means keeping a running best *and* a running list, and clearing the list every
time the best improves. It is four lines and the clearing step is the one
people forget. Two passes over a group of three is not a cost worth optimising
— the first pass finds the number, the second collects the matches, and both
are `O(group)`.

**Comparing floats with `==` — is that not the thing you are told never to
do?** The warning is about floats you have *computed*: `0.1 + 0.2 == 0.3` is
`False`, because those decimals cannot be stored exactly. Here nothing is
computed. `float("3.60")` and `float("3.6")` both produce exactly the same bit
pattern, and `extreme` is one of the very values in the list, not an average of
them. Equality is safe when the value came out of the list it is being compared
against — and knowing *why* it is safe is what stops you either fearing `==`
everywhere or trusting it where it will bite.

**`report` builds a list of rows and joins once.** Not `text += row + "\n"` —
Exercise 1's rule, and the reason the returned string has no trailing newline
to strip.

**The cost.** `digest` is `O(n)` time in the number of lines: one pass to
parse and group, then a pass over each group to reduce, and the groups together
are the readings. Space is `O(n)` for the grouped readings. `report` calls both
`digest` and `skipped`, so it parses the log twice — `O(n)` either way, and a
deliberate choice: two clear functions that each do one thing, over one
function that returns two unrelated numbers. If the log were fifteen years long
and this were in a loop, you would parse once and pass the result around, and
you should be able to say that before anyone asks.

## Download and run

Download
[challenge-01-tide-board-digest-solution.py](./challenge-01-tide-board-digest-solution.py)
and run it:

```bash
python challenge-01-tide-board-digest-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-01-tide-board-digest.py`.

## Common bugs to catch

- **`ValueError: could not convert string to float: 'high'`.** The `try` is
  missing, or it is around the wrong line:

  ```text
  Traceback (most recent call last):
      metres = float(height)
               ^^^^^^^^^^^^^
  ValueError: could not convert string to float: 'high'
  ```

  The message names the offending text, which is genuinely useful when the log
  is fifteen years long. Wrap only the `float` call — a `try` around the whole
  function would also swallow a typo in your own code.

- **`IndexError: list index out of range`.** You read `parts[1]` before
  checking how many fields there were:

  ```text
  Traceback (most recent call last):
      clock, state, height = parts[0], parts[1], parts[2]
                                       ~~~~~^^^
  IndexError: list index out of range
  ```

  `"bad line"` has two fields. Count first, then read. This is why the length
  check is the very first thing in the function.

- **`ValueError: not enough values to unpack (expected 4, got 3)`.** You
  unpacked the parse result without checking it, on a line that gave you
  something shorter:

  ```text
  ValueError: not enough values to unpack (expected 4, got 3)
  ```

- **`TypeError: cannot unpack non-iterable NoneType object`.** The same
  mistake, on a line that was rejected:

  ```text
  Traceback (most recent call last):
      clock, state, metres, place = parse_line(line)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  A function that returns "a result or `None`" has to have its result checked
  before it is used. One line: `if parsed is None: continue`.

- **`LW` reports `1.20`.** You used `max` for both states. There is no error,
  the number is a real reading, and the row looks exactly as convincing as the
  correct one. Low water's extreme is the **lowest**. This is the bug the whole
  challenge is built around, and the only defence is reading the requirement
  twice.

- **`times` holds one clock instead of two.** You kept the first match and
  stopped, or you used `.index()`, which finds one position. The tide hits the
  same height twice a day; "every time that reached it" means every one.

- **`TypeError: '>' not supported between instances of 'float' and 'str'`.**
  Some heights are still text:

  ```text
  TypeError: '>' not supported between instances of 'float' and 'str'
  ```

  You converted in one branch and forgot the other, or you are comparing
  `parts[2]` rather than the parsed value. Convert once, in the parser, and
  nothing downstream can get this wrong.

- **`AttributeError: 'StateDigest' object has no attribute 'peak'`.** You named
  the field one thing and read it as another:

  ```text
  AttributeError: 'StateDigest' object has no attribute 'peak'
  ```

  This is the payoff of a `NamedTuple`. Had the digest been a plain tuple and
  you had written `entry[1]`, you would have got a number — the wrong one, with
  no complaint at all.

## Under the hood

<details>
<summary>Under the hood — what `split` costs, and why a NamedTuple is free</summary>

**`split()` is `O(n)` time and `O(n)` space.** It walks the line once and
builds a list of new string objects — the pieces are copies, not views into the
original, because a Python string owns its characters. So parsing a log of `n`
total characters allocates on the order of `n` characters again. That is fine,
and it is worth knowing it is not free: a parser that splits the same line
three times to get three fields has done three walks and three sets of
allocations for one line.

**`split()` and `split(" ")` are genuinely different functions.**

```python
"  a  b  ".split()       # ['a', 'b']
"  a  b  ".split(" ")    # ['', '', 'a', '', 'b', '', '']
```

The no-argument form treats any run of whitespace — spaces, tabs, newlines — as
one separator and strips the ends. The explicit form splits on each single
space and keeps the empties, because it has to: `"a,,b".split(",")` must give
you three fields, one of them blank, or CSV would be impossible. Know which one
you typed.

**A `NamedTuple` costs nothing at runtime.** It is a real tuple: same memory
layout, same immutability, same hashability, so it can be a dict key or a set
member. The names are looked up on the class, not stored per instance. So the
readability is free, and unlike a small dict there is no per-instance hash
table sitting behind it.

That is also why `StateDigest` here holds a **list** in its `times` field and
is therefore not hashable — a tuple is immutable at the top level, but
hashability needs immutable *all the way down*, and a list inside it breaks
that. If you needed these digests as dict keys you would store `tuple(times)`
instead. Challenge 2 leans on exactly this rule.

**Why the parser is not a regular expression.** A regex would do this in one
line, and for a fixed four-field format it is a reasonable tool. It is not used
here for two reasons: the failure modes get harder to explain — a
non-matching regex tells you nothing about *which* field was wrong — and in an
interview a hand-written parser shows the reasoning that a regex hides. Know
that `re` exists and reach for it when the format genuinely is irregular.

</details>

## Acceptance checklist

- [ ] `python challenge-01-tide-board-digest.py` prints three lines then
      `All checks passed.`
- [ ] No log line can make the program raise.
- [ ] `HW` uses the maximum and `LW` uses the minimum.
- [ ] Both rows list **two** times.
- [ ] `skipped` is 3, and you can name which three lines and why each failed.
- [ ] States come out in first-read order, with nothing sorted.
- [ ] Heights print with two decimal places.
- [ ] You can state the time and space cost of `digest` in one sentence.

## Stretch

- **Say why each rejected line was rejected.**

  ```python
  def reject_reason(line: str) -> str | None:
      """Return why a line was refused, or None when it parsed."""
      parts = line.split()
      if len(parts) < 4:
          return "too few fields"
      if not is_clock(parts[0]):
          return "bad clock"
      if parts[1] not in STATES:
          return "unknown state"
      try:
          float(parts[2])
      except ValueError:
          return "height is not a number"
      return None
  ```

  ```python
  print([reject_reason(line) for line in LOG if reject_reason(line)])
  ```

  ```text
  ['too few fields', 'unknown state', 'height is not a number']
  ```

  Notice the duplication: this function and `parse_line` now know the same four
  rules, and the day somebody adds a fifth state, one of them will be updated.
  The fix is to have `parse_line` return the reason too — a
  `tuple[Reading | None, str | None]`, or an exception carrying the reason.
  Deciding which is a design conversation, and having the conversation with
  yourself is the exercise.

- **Break the summary down by place as well as by state.**

  ```python
  def busiest_place(lines: list[str]) -> str | None:
      """Return the place with the most readings, ties by name A to Z."""
      counts: dict[str, int] = {}
      for line in lines:
          parsed = parse_line(line)
          if parsed is None:
              continue
          counts[parsed[3]] = counts.get(parsed[3], 0) + 1
      if not counts:
          return None
      return min(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0]
  ```

  ```text
  north quay
  ```

  Same dict shape as Exercise 4, over a field you were already parsing and
  throwing away. Most "can you also tell me…" requests are this: a key you
  already have, counted differently.

- **Find the range of the day.**

  ```python
  def tidal_range(lines: list[str]) -> float | None:
      """Return the highest HW minus the lowest LW, or None if either is missing."""
      summary = digest(lines)
      if "HW" not in summary or "LW" not in summary:
          return None
      return round(summary["HW"].extreme - summary["LW"].extreme, 2)
  ```

  ```text
  2.75
  ```

  Now take the `round` out and run it again. You still get `2.75` — these
  particular numbers happen to subtract exactly. Then try `0.1 + 0.2` in a
  REPL and you get `0.30000000000000004`. Both are the same arithmetic on the
  same kind of number, and one is tidy and one is not, which is precisely why
  you cannot tell by looking. The rule from the solution stands: comparing a
  value against one it came *from* is safe, and comparing a **computed** value
  against a decimal you typed is not. Round when you are about to show a
  number to a person; do not round to make a comparison work.

When your digest is right, move on to
[Challenge 2 — The Kiln Cone Audit](./challenge-02-kiln-cone-audit.md).
