# Exercise 3 — The Stencil Line

> **Topic:** 1-D DP over the prefixes of a string, where the step back is not a fixed size
> **Lecture:** [01 — The DP Pipeline and 1D States](../lecture-notes/01-the-dp-pipeline-and-1d-states.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** in Exercises 1 and 2 the recurrence stepped back a fixed number of places — one, two, three. Here the step back depends on which code matched, so the inner loop is over *possible steps* rather than over a constant. That is the shape of most string DPs, and it is where the cost of a DP stops being obviously linear.

## The Brief

The Kelbray depot stencils part codes straight onto its crates. There are no
spaces and no dashes — the die presses one long run of characters, so a crate
carrying a zinc-plated hex bolt comes out reading `ZINCHEXBOLT`.

Two things make reading them back harder than it sounds.

First, the die slips. Every so often it leaves a mark that is not part of any
code. Nobody knows in advance where those marks are.

Second, codes can look like pieces of each other. `CLIP` and `PIN` are both in
the code book, and in the run `CLIPIN` they **overlap** — the `PIN` starts
before the `CLIP` has finished. You cannot have both. A character belongs to at
most one code.

The depot's question is not "is this line valid" — most lines are not. It is
**"how much of this line can we actually account for?"** Given the line and the
code book, find the largest number of characters that a left-to-right sequence
of whole, non-overlapping codes can cover. Everything left over is a smudge,
and smudges may sit anywhere: at the front, at the back, in the middle, or all
three.

The recurrence in English, before any Python:

> **Look at the prefix of the line that ends at position `i`. Either the last
> character is a smudge, in which case the best cover is whatever was best for
> the prefix ending at `i-1`; or the prefix ends with a whole code of some width
> `w`, in which case the best cover is `w` plus whatever was best for the prefix
> ending at `i-w`. Take the largest of all those options.**

Notice the "of some width `w`". That is what is new. In Exercise 1 the steps
back were 1, 2 and 3 — always the same three. Here they are the widths of
whatever codes actually match right there, which changes from position to
position.

## Starter

Create `exercise-03-stencil-line-split.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-03-stencil-line-split.py — the widest readable cover.

How many characters of a stencil line can be accounted for by a left-to-right
sequence of whole, non-overlapping codes?

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import functools

CODE_BOOK = frozenset(
    {"ZINC", "HEX", "BOLT", "NUT", "WASHER", "PIN", "CLIP", "M8", "M10"}
)

CRATE_LINE = "ZINCHEXBOLTM8XXWASHERPIN"


def best_cover_cached(line: str, codes: frozenset[str]) -> int:
    """Top-down: the recurrence said out loud, with every answer remembered."""
    lengths = sorted({len(code) for code in codes})

    @functools.cache
    def cover_from(start: int) -> int:
        """The most characters coverable in line[start:]."""
        # TODO: base case — nothing left to read
        # TODO: option one, treat line[start] as a smudge and move on by 1
        # TODO: option two, for each width in `lengths`, if the slice starting
        #       here is in `codes`, take width + cover_from(start + width)
        # TODO: return the largest option
        ...

    return cover_from(0)


def best_cover(line: str, codes: frozenset[str]) -> int:
    """Return the most characters of `line` coverable by whole codes.

    Args:
        line: The stencil line, read left to right.
        codes: The depot's code book. May be empty.

    Returns:
        The largest number of characters a non-overlapping, left-to-right
        sequence of whole codes can account for.

    Raises:
        ValueError: If the code book contains an empty string.
    """
    # TODO: reject an empty code
    # TODO: collect the distinct code widths once, before the loop
    # TODO: covered = [0] * (len(line) + 1)
    # TODO: for each end position, start from covered[end - 1] and try every
    #       width that fits and matches
    ...


def cover_table(line: str, codes: frozenset[str]) -> list[int]:
    """The full bottom-up table. Entry i covers the first i characters."""
    # TODO: the same fill as best_cover, returning the whole list
    ...


if __name__ == "__main__":
    for end, value in enumerate(cover_table("NUTXHEX", CODE_BOOK)):
        print(end, value)

    assert best_cover("", CODE_BOOK) == 0
    assert best_cover("XYZ", CODE_BOOK) == 0
    assert best_cover("NUTXHEX", CODE_BOOK) == 6
    assert best_cover("CLIPINNUT", CODE_BOOK) == 7
    assert best_cover(CRATE_LINE, CODE_BOOK) == 22
    assert best_cover_cached(CRATE_LINE, CODE_BOOK) == 22
    print("All checks passed.")
```

Three words you need before you start.

**Prefix.** The first `i` characters of the line, for some `i`. Python spells it
`line[:i]`. A DP "over prefixes" means the state is *how far along the line you
are*, and nothing else.

**Slice.** `line[a:b]` is the characters from `a` up to but not including `b`.
`len(line[a:b])` is `b - a` whenever both ends are inside the string, which is
the arithmetic this whole exercise rests on.

**Set membership.** `"NUT" in codes` where `codes` is a `set` or `frozenset` is
a hash lookup: constant time, no matter how many codes there are. The same test
against a `list` walks the whole list. That single choice is the difference
between this exercise being fast and being slow, and it is worth saying out loud
in an interview.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-11-dynamic-programming-i/exercises/exercise-03-stencil-line-split.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `best_cover(line, codes)` returns an `int`: the most characters coverable.
2. `best_cover("", codes)` returns `0` for any code book.
3. `best_cover(line, frozenset())` returns `0`. An empty code book is legal —
   a new depot has not filled one in yet — and covers nothing.
4. `best_cover("XYZ", CODE_BOOK)` returns `0`, not `-1` and not `None`.
5. `best_cover("CLIPINNUT", CODE_BOOK)` returns `7`. Overlapping codes cannot
   both be used.
6. `best_cover("PINPINPIN", CODE_BOOK)` returns `9`. A code may be used as many
   times as it fits.
7. `best_cover(CRATE_LINE, CODE_BOOK)` returns `22`, leaving 2 characters
   smudged.
8. A code book containing `""` raises `ValueError`.
9. `cover_table(line, codes)` returns `len(line) + 1` entries and its last entry
   equals `best_cover(line, codes)`.
10. `best_cover_cached` agrees with `best_cover` on every case.

## Constraints

- **A stencil line is at most 20,000 characters.** One crate carries a few
  dozen; 20,000 is a whole pallet's worth of lines pasted together, which is how
  the depot actually files them at the end of a shift. The bound matters because
  the running time is the line length times the number of distinct code widths,
  and at 20,000 by 12 that is a quarter of a million slice comparisons — fast.
  A solution that tries every possible split point instead would be
  exponential and would not finish on a line of 40.

- **The code book holds at most 400 codes, each 1 to 12 characters.** Twelve is
  the widest die the depot owns, so no code can be longer. That bound is what
  keeps the inner loop short: there are at most 12 distinct widths to try at
  each position, no matter how many codes there are.

- **Never an empty code.** An empty string would "cover" nothing and could be
  used any number of times at any position, so every prefix would have infinitely
  many valid readings and the table would stop meaning anything. It is a broken
  code book, not an edge case, so raise.

- **Codes are compared exactly, case included.** The die presses upper case, and
  a lower-case letter in a code book means somebody typed it by hand into the
  wrong field. Silently case-folding would hide that.

- **Collect the distinct widths once, before the loop.** Rebuilding
  `{len(code) for code in codes}` inside the loop turns a 400-code book into 400
  extra operations at every one of 20,000 positions — eight million pieces of
  pointless work, for a set that never changes. Hoisting invariant work out of a
  loop is not micro-optimisation here; it is a factor of the code-book size.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-03-stencil-line-split-solution.py
placeholder
```

Read the little table first. `NUTXHEX` stays at 0 for two characters — `N` and
`NU` are not codes — then jumps to 3 when `NUT` completes. It then stays at 3
for three more characters while `X`, `H` and `HE` fail to complete anything, and
jumps to 6 the moment `HEX` lands. **A DP table that goes flat is not stuck; it
is recording that nothing improved.**

## Steps

1. Create the file, paste the starter, run it. It fails on the first assert.
2. Write `cover_from` inside `best_cover_cached` first. Two options, the largest
   wins. Check it on `"NUT"` (3) and `"XNUT"` (3) before going further.
3. Try `best_cover_cached("CLIPINNUT", CODE_BOOK)` and satisfy yourself that 7
   is right by writing the nine characters on paper and drawing brackets. The
   overlap is the trap in this exercise and it is worth meeting by hand.
4. Write `cover_table`. Walk `end` from 1 to `len(line)`. Start from
   `covered[end - 1]`, which is the "last character is a smudge" option, then
   try each width.
5. Watch the indices. The code that *ends* at `end` and is `width` wide is
   `line[end - width : end]`, and the prefix before it ends at `end - width`.
   Those two must be consistent or every answer will be off.
6. Write `best_cover` by returning the last entry of the same fill. Run, and
   compare the table you print against the expected output line for line.

## The Solution

```python
placeholder
```

**The state is one number — how far along the line you are — so this is still
a 1-D DP.** What changed from Exercise 1 is only the set of places the
recurrence can look back to. There it was always three fixed steps. Here it is
"one step, plus one step for every code width that matches right here", and the
matching part is decided by a set lookup.

**Every character has exactly two fates, and that is the whole proof.** In the
best cover of a prefix, the last character is either inside some code or it is
not. If it is not, the rest of the cover is a best cover of the prefix one
shorter. If it is, that code is some width `w` wide, it ends exactly at `i`,
and the rest of the cover is a best cover of the prefix `w` shorter. The
recurrence tries both, so it cannot miss an option; and each option describes a
different last character fate, so it cannot count one twice.

**`covered[end - 1]` is not a fallback, it is a real option.** A lot of learners
write the loop over widths first and add "if nothing matched, carry the previous
value" as an afterthought. That is the same code, but thinking of it as an
afterthought leads to the bug where a match that is *worse* than smudging the
character overwrites the better answer. Start from the smudge option and let the
widths compete with it.

**Overlap is handled by arithmetic, not by a check.** There is no code anywhere
in the solution that asks "does this code overlap the previous one?" It cannot
happen: taking a code of width `w` ending at `end` jumps the state straight to
`end - w`, so the next thing considered ends at or before `end - w`. The
non-overlap rule is baked into where the recurrence looks. **When a constraint
disappears from your code entirely, it usually means you chose the state well.**

**The set matters as much as the recurrence.** `line[end - width : end] in
codes` is a slice — which costs time proportional to the slice, up to 12
characters — followed by a hash lookup, which is effectively constant. Had
`codes` been a list, that lookup would walk up to 400 strings, and the whole
thing would be 400 times slower for no reason at all. Choosing `frozenset` over
`list` here is a bigger win than any change you could make to the loop.

**The two versions face opposite directions, again.** `cover_from(start)` asks
"how much can I cover from here to the end?" and recursion carries answers
backwards to the caller. The table asks "how much can I cover in the first `end`
characters?" and the loop carries answers forwards. Both are the same
recurrence. The table is the one you would ship: no stack, and on a 20,000
character line the recursion would be 20,000 frames deep.

**Complexity.** There are `n + 1` states and each does at most `W` slice-and-
lookup steps, where `W` is the number of distinct code widths — at most 12 here.
Each slice costs up to 12 character copies. So the whole thing is `O(n · W · L)`
with `L` the longest code, and with `W` and `L` both bounded by 12 that is
linear in the length of the line. Space is `O(n)` for the table. The rolling
trick from Exercise 2 does **not** apply cleanly: the recurrence can reach 12
entries back, so you would have to keep 12 — which is a real reduction, just
not a dramatic one.

## Download and run

Download
[exercise-03-stencil-line-split-solution.py](./exercise-03-stencil-line-split-solution.py)
and run it:

```bash
python exercise-03-stencil-line-split-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-stencil-line-split.py`.

## Common bugs to catch

- **`best_cover("CLIPINNUT", CODE_BOOK)` returns 10.** You allowed codes to
  overlap — usually by looping over *start* positions and adding a code's width
  without moving the state past it. Ten is more characters than the line has,
  which is the tell. Any cover total larger than `len(line)` means overlap.

- **Off by the code width.**

  ```text
  AssertionError: 'NUTXHEX' -> 3, expected 6
  ```

  You wrote `covered[end - width] + width` but sliced `line[end : end + width]`,
  which looks *forwards* from `end` while the table entry looks backwards. The
  slice that ends at `end` is `line[end - width : end]`. Write those two
  expressions next to each other and check they describe the same characters.

- **`IndexError: list index out of range`.**

  ```text
  Traceback (most recent call last):
    File "exercise-03-stencil-line-split.py", line 61, in best_cover
      candidate = covered[end - width] + width
                  ~~~~~~~^^^^^^^^^^^^^
  IndexError: list index out of range
  ```

  Only if you indexed past the end. The far more likely failure is the silent
  one: `end - width` going negative reads from the *end* of the table, no error,
  wrong answer. The `width <= end` guard is what prevents it, and it is the same
  guard as in Exercise 1.

- **Every answer is 0.** Your membership test is against a string rather than a
  set of strings. `"NUT" in "NUTXHEX"` is `True`, but `"N" in CODE_BOOK` is
  `False` — mixing the two up gives answers that are wrong in both directions.
  Print `type(codes)` if you are unsure.

- **`TypeError: unhashable type: 'set'`.**

  ```text
  TypeError: unhashable type: 'set'
  ```

  You passed a plain `set` into a function whose inner helper is decorated with
  `functools.cache`, and the cache tried to use it as a key. `frozenset` is the
  version that can be hashed, which is why the signature asks for one. In this
  file the cache is on `cover_from`, which takes only an integer — but move the
  cache one level out and you will meet this immediately.

- **The empty code book raises instead of returning 0.** You wrote
  `max(...)` over an empty sequence:

  ```text
  ValueError: max() iterable argument is empty
  ```

  Starting from the smudge option and improving on it avoids this entirely —
  there is always at least one candidate, so there is never an empty `max`.

- **It is correct but slow on a long line.** You built the width set inside the
  loop, or you tested `line[end - width : end] in codes` for every code rather
  than every distinct width. Both are the same mistake: doing work per code
  when the work only depends on the widths.

## Under the hood

<details>
<summary>Under the hood — the cost of slicing, and how a trie removes it</summary>

**Slicing is not free, and the page's complexity bound admits it.** `line[a:b]`
builds a brand-new string of `b - a` characters. Inside the loop that happens up
to `W` times per position, so the true count of character copies is
`n · W · L`. With the depot's numbers — `W ≤ 12`, `L ≤ 12` — that is at most 144
copies per position, a constant, so the whole thing is linear. But the constant
is real, and on a much larger alphabet of codes it would be the thing you
optimised first.

**The fix is a trie, which Week 9 built.** Instead of slicing out a candidate
and hashing it, walk the code book's trie character by character from position
`end` backwards (or build the trie of reversed codes). Each step is one
character comparison, and you stop the moment no code can continue. That turns
`n · W · L` character copies into `n · L` character *comparisons* with no
allocation at all. It is the standard upgrade for this shape, and knowing it
exists is worth more in an interview than implementing it under time pressure.

**Why a rolling window of 12 is the honest space bound.** The recurrence at
`end` reads `covered[end - width]` for widths up to `L`. Everything older than
`end - L` can be thrown away. So a `collections.deque` of `L + 1` entries
suffices, giving `O(L)` space instead of `O(n)`:

```python
from collections import deque

def best_cover_rolling(line: str, codes: frozenset[str]) -> int:
    lengths = sorted({len(code) for code in codes})
    span = max(lengths, default=0) + 1
    window = deque([0], maxlen=span)     # window[-1] is covered[end - 1]
    for end in range(1, len(line) + 1):
        best = window[-1]
        for width in lengths:
            if width <= end and width < len(window) + 1 and line[end - width : end] in codes:
                best = max(best, window[-width] + width)
        window.append(best)
    return window[-1]
```

Read that carefully before trusting it: `window[-width]` is only `covered[end -
width]` while the window is full, so the early iterations need thought. This is
the general shape of every space reduction and also the general reason to leave
one out until somebody asks — the index arithmetic is where the bugs live, and
`O(n)` on a 20,000 character line is 160 kilobytes.

**Full coverage is a special case, not a different problem.** "Can this line be
read with no smudges at all?" is exactly `best_cover(line, codes) ==
len(line)`. Solving the harder question first and reading the easier one off it
is often cheaper than writing both. It also gives a better answer to the user:
"22 of 24, smudge near the middle" beats "no".

**What a boolean version would change.** If you only needed the yes-or-no, the
table would hold `True`/`False` and the recurrence would be `any(...)` instead
of `max(...)`. Same states, same transitions, same complexity — a different
*aggregation*. Recognising that the table shape and the aggregation are separate
choices is the single most transferable idea in this week: counting, maximising,
minimising and deciding are four aggregations over the same tables.

</details>

## Acceptance checklist

- [ ] `python exercise-03-stencil-line-split.py` prints the eight table rows then `All checks passed.`
- [ ] `best_cover("", CODE_BOOK)` and `best_cover(CRATE_LINE, frozenset())` both return `0`.
- [ ] `best_cover("CLIPINNUT", CODE_BOOK)` returns `7`, not `10`.
- [ ] `best_cover("PINPINPIN", CODE_BOOK)` returns `9`.
- [ ] A code book containing `""` raises `ValueError`.
- [ ] The distinct widths are computed once, outside the loop.
- [ ] The code book is a `frozenset`, and you can say why it is not a list.
- [ ] `cover_table(line, codes)[-1] == best_cover(line, codes)` on every case you try.
- [ ] Committed to Git with a message like `Add Week 11 exercise 3: stencil line split`.

## Stretch

- **Report the reading, not just the number.** Walk the finished table backwards
  and recover which codes were used and where.

  ```python
  def cover_plan(line: str, codes: frozenset[str]) -> list[tuple[int, str]]:
      """The (start, code) pairs of one best cover, left to right."""
      covered = cover_table(line, codes)
      lengths = sorted({len(code) for code in codes}, reverse=True)
      plan: list[tuple[int, str]] = []
      end = len(line)
      while end > 0:
          if covered[end] == covered[end - 1]:
              end -= 1                       # that character was a smudge
              continue
          for width in lengths:
              piece = line[end - width : end]
              if width <= end and piece in codes and covered[end] == covered[end - width] + width:
                  plan.append((end - width, piece))
                  end -= width
                  break
      return plan[::-1]

  for start, code in cover_plan(CRATE_LINE, CODE_BOOK):
      print(f"{start:>3}  {code}")
  ```

  ```text
    0  ZINC
    4  HEX
    7  BOLT
   11  M8
   15  WASHER
   21  PIN
  ```

  The two smudged characters, at 13 and 14, simply never appear. Note what the
  reconstruction needed: the whole table. The rolling version in *Under the
  hood* throws away exactly the entries this walk reads.

- **Ask the yes-or-no question instead.** Full coverage falls out of the number
  you already have.

  ```python
  def reads_cleanly(line: str, codes: frozenset[str]) -> bool:
      """True when the whole line is codes, with no smudge anywhere."""
      return best_cover(line, codes) == len(line)

  print(reads_cleanly("ZINCHEXBOLT", CODE_BOOK))
  print(reads_cleanly(CRATE_LINE, CODE_BOOK))
  ```

  ```text
  True
  False
  ```

- **Charge for smudges instead of counting them.** Suppose a smudge in the
  middle of a line costs more than one at the end, because it is likelier to be
  misread. Change the aggregation, keep the table.

  ```python
  def fewest_smudge_runs(line: str, codes: frozenset[str]) -> int:
      """The fewest separate runs of uncovered characters in a best cover."""
      lengths = sorted({len(code) for code in codes})
      # state: (characters covered, smudge runs so far, ended on a smudge)
      best: list[tuple[int, int, int]] = [(0, 0, 0)] * (len(line) + 1)
      for end in range(1, len(line) + 1):
          covered, runs, on_smudge = best[end - 1]
          option = (covered, runs + (0 if on_smudge else 1), 1)
          for width in lengths:
              if width <= end and line[end - width : end] in codes:
                  prev_covered, prev_runs, _ = best[end - width]
                  if prev_covered + width > option[0]:
                      option = (prev_covered + width, prev_runs, 0)
          best[end] = option
      return best[-1][1]

  print(fewest_smudge_runs(CRATE_LINE, CODE_BOOK))
  print(fewest_smudge_runs("XNUTXHEXX", CODE_BOOK))
  ```

  ```text
  1
  3
  ```

  The table did not change shape at all — the state grew by two numbers, and the
  comparison changed. That is what "the same DP with a richer state" looks like,
  and it is the move that turns Exercise 2's tie-break into a general technique.

**Practice elsewhere.** The same prefix-DP shape appears as
[LeetCode 139 · Word Break](https://leetcode.com/problems/word-break/) if you
want a judge to run against.

When your cover is right, move on to
[Exercise 4 — The Terrace Route Table](./exercise-04-terrace-route-table.md).
