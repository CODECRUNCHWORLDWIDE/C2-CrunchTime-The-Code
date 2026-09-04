# Problem 1 — Counting the Copies in a Banner

> **Topic:** proving the cost of `+=` versus `"".join(...)` by counting the work instead of timing it
> **Lecture:** [01 — Strings and the Cost of Immutability](../lecture-notes/01-strings-and-immutability.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** Week 0 asks you to take a lot of complexity claims on trust. This is the first one you get to check, and checking it with a stopwatch would only tell you about your laptop. Counting the characters copied gives you the same number on every machine, and the ratio column turns "quadratic" from a word into something you can see.

## The Brief

A sign painter builds a banner out of five-letter strips of card:
`BLOOM`, `SEEDS`, `GROWS`, `HERBS`, `ROOTS`, and round again.

There are two ways to build it in Python, and Lecture 1 says one of them is
`O(n)` and the other is `O(n²)`. Your job is to prove it — not by timing, by
**counting**.

Here is what to count. A string cannot be changed, so `banner += strip` does
not add anything to `banner`. It builds a brand-new string holding everything
that was in the old one plus the new strip, and points the name at that. So
that one line copies `len(banner) + len(strip)` characters.

Do it for every strip and the copying adds up:

```text
strip 1:  0 + 5 characters copied
strip 2:  5 + 5
strip 3: 10 + 5
strip 4: 15 + 5   →  50 for four strips
```

`"".join(strips)` does something else entirely. It walks the list once to work
out how long the answer will be, allocates a string of exactly that size once,
and copies each character in. Every character is copied **once**: four strips
of five is twenty characters, and twenty is the whole bill.

You are writing four functions and a table. The table doubles the strip count
each row and prints how each number grew. A column that roughly doubles is
linear. A column that roughly quadruples is quadratic.

## Starter

Create `problem-01-banner-copy-count.py` in your practice folder and paste this
in. Fill in every `TODO`.

```python
"""problem-01-banner-copy-count.py — count the copying, do not time it.

Built with `+=`, every strip forces the whole banner so far to be copied.
Built with `"".join`, every character is copied exactly once.

Nothing here is timed, so the table is the same on every machine.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

WORDS = ("BLOOM", "SEEDS", "GROWS", "HERBS", "ROOTS")
SIZES = (4, 8, 16, 32)


def strips(count: int) -> list[str]:
    """Return `count` banner strips, cycling through the five words."""
    # TODO: one comprehension, using % to wrap round the five words
    ...


def copies_by_concat(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `+=`."""
    # TODO: build it for real, adding len(banner) + len(piece) each time
    ...


def copies_by_join(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `join`."""
    # TODO: every character is copied once
    ...


def build_banner(pieces: list[str]) -> str:
    """Return the finished banner, built the cheap way."""
    ...


def table(sizes: tuple[int, ...]) -> str:
    """Render the copy counts and how they grow, no trailing newline."""
    # TODO: a header row, then one row per size. The growth columns compare
    # each row with the row above; the first row has no row above it.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(table(SIZES))

    pieces = strips(32)
    assert len(pieces) == 32
    assert build_banner(strips(3)) == "BLOOMSEEDSGROWS"
    assert copies_by_join(pieces) == 160  # 32 strips of 5, copied once each
    assert copies_by_concat(pieces) == 2640  # 5 * 32 * 33 // 2
    assert copies_by_concat(strips(64)) == 5 * 64 * 65 // 2
    assert copies_by_concat([]) == 0
    assert copies_by_join([]) == 0
    assert build_banner([]) == ""
    print("All checks passed.")
```

Two things you need before you start.

**The exact row format.** The table's header and rows use these widths, so the
columns line up and the output matches character for character:

```python
f"{'strips':>6}  {'+= copies':>10}  {'join copies':>11}  {'+= x':>5}  {'join x':>6}"
f"{count:>6}  {concat:>10}  {joined:>11}  {growth}"
```

where `growth` is either `f"{'-':>5}  {'-':>6}"` for the first row or
`f"{concat / previous_concat:>5.2f}  {joined / previous_joined:>6.2f}"` after
that. `>` means right-aligned; the number after the dot is decimal places.

**The closed form, for checking your work.** With `n` strips of length `L`, the
`+=` version copies `L × n(n+1) / 2` characters and the `join` version copies
`L × n`. Your program should agree with that arithmetic exactly — the asserts
check two cases, and you should be able to derive the formula rather than
recognise it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-01-banner-copy-count.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `strips(n)` returns `n` strings, cycling `BLOOM, SEEDS, GROWS, HERBS, ROOTS`
   and repeating.
2. `copies_by_concat` counts `len(banner) + len(piece)` for every strip and
   returns the total.
3. `copies_by_join` returns the sum of the strip lengths.
4. `build_banner` returns the strips end to end.
5. `table` prints a header and one row per size, with the two growth columns
   comparing each row to the one above and `-` on the first row.
6. All four functions return `0` or `""` on an empty list, with no crash.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Count, do not time.** `timeit` would give you a different answer on every
  machine, a different answer on the same machine twice, and an answer that
  CPython's in-place resize optimisation can flip entirely. Counted work is a
  fact about the algorithm. This is the reason this problem exists in a course
  that could easily have shipped a stopwatch.

- **`copies_by_concat` must actually build the string.** You could compute the
  answer from the formula in one line, and then you would be checking your
  arithmetic rather than Python's behaviour. Build it, count as you go, and let
  the assert compare your count against the formula. That comparison is the
  proof.

- **Read the growth column, not the totals.** `2640` means nothing on its own.
  `3.88` next to `2.00` is the finding: doubling the strips roughly quadrupled
  one column and exactly doubled the other.

- **Sizes stop at 32.** They double so the growth column means something, and
  32 is where a quadratic column is already 16 times the linear one — big
  enough to be obvious and small enough that the whole table is checkable by
  hand. A bigger table would say the same thing more slowly.

- **Every strip is exactly five characters.** Equal lengths make the closed
  form clean, so you can check the program against arithmetic instead of
  against itself. Mixed lengths would still be `O(n²)`; they would just make
  the check harder for no teaching gain.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-banner-copy-count.py
strips   += copies  join copies   += x  join x
     4          50           20      -       -
     8         180           40   3.60    2.00
    16         680           80   3.78    2.00
    32        2640          160   3.88    2.00
All checks passed.
```

Look along the bottom row. Thirty-two strips is 160 characters of banner. The
`join` version copies 160 characters — the answer, once. The `+=` version
copies 2640, which is sixteen and a half times the finished thing, and almost
all of it is the same letters being carried from one temporary string to the
next. Then read the growth columns: `3.88` climbing towards 4, and `2.00`
exactly.

## Steps

1. Create the file, paste the starter, and run it. `print(None)` prints `None`
   and then the asserts fail.
2. Write `strips`. `WORDS[index % len(WORDS)]` is the wrap-round.
3. Write `copies_by_join` and `build_banner` — one line each.
4. Write `copies_by_concat`. Add to the counter **before** the `+=`, using the
   length the banner has at that moment.
5. Check one value by hand before trusting the program: four strips should be
   `5 + 10 + 15 + 20 = 50`.
6. Write `table`. Do the numbers first with a plain `print` per row, then add
   the alignment.
7. When it passes, add `64` and `128` to `SIZES` and watch the `+= x` column
   creep from `3.88` towards `3.97`. Work out why it approaches 4 from below
   and never reaches it. That question is the point of the whole page.

## The Solution

```python
"""problem-01-banner-copy-count-solution.py — count the copying, do not time it.

A sign painter builds a banner out of five-letter strips. Built with `+=`,
every strip forces the whole banner so far to be copied into a new string.
Built with `"".join`, every character is copied exactly once.

This program does not time anything. It counts characters copied, which is
the same number on every machine, so the table below is a fact rather than a
weather report.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

WORDS = ("BLOOM", "SEEDS", "GROWS", "HERBS", "ROOTS")
SIZES = (4, 8, 16, 32)


def strips(count: int) -> list[str]:
    """Return `count` banner strips, cycling through the five words.

    Args:
        count: How many strips the banner is made of.

    Returns:
        A list of five-character strings.
    """
    return [WORDS[index % len(WORDS)] for index in range(count)]


def copies_by_concat(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `+=`.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        The total number of characters copied. Each `+=` builds a brand new
        string, so it copies everything glued so far plus the new strip.
    """
    copied = 0
    banner = ""
    for piece in pieces:
        copied += len(banner) + len(piece)
        banner += piece
    return copied


def copies_by_join(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `join`.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        The total number of characters copied. `join` measures first,
        allocates once, and copies each character exactly once.
    """
    return sum(len(piece) for piece in pieces)


def build_banner(pieces: list[str]) -> str:
    """Return the finished banner, built the cheap way.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        Every strip end to end.
    """
    return "".join(pieces)


def table(sizes: tuple[int, ...]) -> str:
    """Render the copy counts and how they grow.

    Args:
        sizes: Strip counts to report, each double the one before.

    Returns:
        A header line and one line per size. No trailing newline.
    """
    rows = [f"{'strips':>6}  {'+= copies':>10}  {'join copies':>11}  {'+= x':>5}  {'join x':>6}"]
    previous: tuple[int, int] | None = None
    for count in sizes:
        pieces = strips(count)
        concat = copies_by_concat(pieces)
        joined = copies_by_join(pieces)
        if previous is None:
            growth = f"{'-':>5}  {'-':>6}"
        else:
            growth = f"{concat / previous[0]:>5.2f}  {joined / previous[1]:>6.2f}"
        rows.append(f"{count:>6}  {concat:>10}  {joined:>11}  {growth}")
        previous = (concat, joined)
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(table(SIZES))

    pieces = strips(32)
    assert len(pieces) == 32
    assert build_banner(strips(3)) == "BLOOMSEEDSGROWS"
    assert copies_by_join(pieces) == 160  # 32 strips of 5, copied once each
    assert copies_by_concat(pieces) == 2640  # 5 * 32 * 33 // 2
    assert copies_by_concat(strips(64)) == 5 * 64 * 65 // 2
    assert copies_by_concat([]) == 0
    assert copies_by_join([]) == 0
    assert build_banner([]) == ""
    print("All checks passed.")
```

**The counting line has to come before the concatenation.**

```python
copied += len(banner) + len(piece)
banner += piece
```

At that moment `banner` is still the old, shorter one, and the old length is
exactly what has to be carried into the new string. Swap the two lines and you
count the new length, which over-counts by five every time and quietly turns
your proof into a different formula.

**Why the growth is 4 and not exactly 4.** The `+=` total is `L × n(n+1)/2`.
Doubling `n` gives

```text
2n(2n + 1)     4n² + 2n
----------  =  --------  →  4 as n grows
 n(n + 1)       n² + n
```

At `n = 8` that is `3.60`; at `n = 32`, `3.88`. It climbs towards 4 and never
arrives, because the `+ n` term never quite vanishes. **That is what "quadratic"
means in practice** — not "exactly four times" but "four times, plus a smaller
term that matters less and less". A measurement that gives you 3.88 has
confirmed the claim, not contradicted it, and being able to say so is the
difference between reading a table and understanding one.

**The `join` column is exactly 2.00 at every size,** because its total is
`L × n` with no second term at all. Linear things are cleaner to measure than
quadratic ones, which is worth knowing when you are staring at a real
measurement wondering whether `2.3` means linear.

**`table` keeps the previous row in a variable.** `previous` starts as `None`,
which is how the first row knows it has nothing to compare against and prints
`-`. That is a small, common shape — the first pass through a loop is
different — and the `None` says "not yet" more clearly than a `0` would, since
a `0` would divide badly.

**What this proves and what it does not.** It proves that the `+=` loop
*requests* quadratically many character copies. It does not prove your program
will be quadratically slow, because CPython sometimes resizes a string in place
when nothing else refers to it, and then the copy never happens. The measured
version of this experiment can therefore come out linear on a good day. The
count cannot, because the count is about the algorithm, and the algorithm is
what you are asked about in an interview.

## Run it

Copy the worked answer on this page into `problem-01-banner-copy-count.py` and run it:

```bash
python problem-01-banner-copy-count.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-01-banner-copy-count.py`.

## Common bugs to catch

- **The `+= copies` column is 5 too high on every row.** You counted after the
  concatenation, so you used the new length. Count first.

- **`ZeroDivisionError: division by zero`.** Your growth column divided by the
  previous row on the first row:

  ```text
  Traceback (most recent call last):
      growth = f"{concat / previous[0]:>5.2f}"
                  ~~~~~~~^~~~~~~~~~~~~
  ZeroDivisionError: division by zero
  ```

  You initialised `previous` to `(0, 0)` instead of `None`. `None` cannot be
  divided by either, but it can be *tested*, and the test is the point.

- **`TypeError: unsupported operand type(s) for +: 'int' and 'str'`.** You
  added the strip itself instead of its length:

  ```text
  TypeError: unsupported operand type(s) for +: 'int' and 'str'
  ```

  `len(piece)`, not `piece`. Python stopping you here is a gift; the same slip
  inside an f-string would have silently produced a wrong table.

- **The columns do not line up.** You used `<` instead of `>` in the format
  specifiers, or left the widths out. Numbers go right-aligned so the digits
  stack; text goes left-aligned. A table whose columns wander is a table nobody
  reads.

- **`copies_by_join` returns the length of the joined string.** That is the
  same number here, and it is the same number for the wrong reason — you
  measured the output rather than counting the work. If the separator were
  `"-"` the two would differ, and the version that counts `len(piece)` is the
  one that stays honest.

- **`strips(0)` raises `ZeroDivisionError`.** You wrote
  `WORDS[index % count]` instead of `WORDS[index % len(WORDS)]`. The wrap-round
  is over the five words, not over the number of strips.

## Under the hood

<details>
<summary>Under the hood — why join allocates once, and what the resize optimisation really does</summary>

**`str.join` makes two passes and one allocation.** The first pass adds up the
lengths of every piece and of the separators. Then it allocates a string of
exactly that many characters. Then the second pass copies each piece into
place. Two walks, one allocation, every character copied once. There is no
slack left in that algorithm, which is why it is the answer and will stay the
answer.

**`+=` in a loop makes `n` allocations.** Each one is a fresh string, and the
one before it becomes garbage the moment the name moves. So the loop does not
just copy quadratically many characters — it also churns through `n` objects,
which costs allocator work the count on this page does not even include.

**The optimisation.** CPython's evaluation loop special-cases `str += str` when
the string on the left has a reference count of exactly 1, meaning nothing else
in the program is holding it. In that case the interpreter can ask the
allocator to grow the existing buffer in place and skip the copy entirely.

It disappears the moment anything else refers to that string:

```python
banner = ""
keep = []
for piece in pieces:
    banner += piece
    keep.append(banner)     # a second reference — no in-place resize possible
```

That is why a timing experiment on this problem is unreliable: the same loop is
linear or quadratic depending on a line somewhere else. It is also why other
Python implementations, which have no reference counting, never see the
speed-up at all.

**In an interview.** Say `O(n²)`. If you want to show depth, add: "CPython can
sometimes resize in place when the refcount is 1, so a naive benchmark may look
linear — I would not rely on it." Leading with the optimisation sounds like
dodging the question.

**The same argument applies to lists.** `result = result + [x]` in a loop is
`O(n²)`. `result.append(x)` is `O(n)` in total, for the reason the next
lecture derives: the list keeps spare room and only occasionally has to move.

</details>

## Acceptance checklist

- [ ] `python problem-01-banner-copy-count.py` prints a five-line table then
      `All checks passed.`
- [ ] The table matches the expected output character for character.
- [ ] `copies_by_concat` builds the string for real and counts as it goes.
- [ ] Four strips give 50, and you checked that by hand.
- [ ] The first row's growth columns show `-`, not a crash and not `0.00`.
- [ ] You can explain why the `+= x` column approaches 4 from below.
- [ ] You can say what this experiment proves and what it does not.

## Stretch

- **Count the wasted work, not the total.**

  ```python
  def wasted(pieces: list[str]) -> int:
      """Return the characters copied that the join version never copies."""
      return copies_by_concat(pieces) - copies_by_join(pieces)
  ```

  ```text
   4 strips: 30 wasted
   8 strips: 140 wasted
  16 strips: 600 wasted
  32 strips: 2480 wasted
  ```

  The waste is `L × n(n-1)/2` — everything except the one honest copy of each
  character. At 32 strips, 94% of the work is waste.

- **Do it with a separator and watch the two costs separate.**

  ```python
  def copies_by_join_sep(pieces: list[str], sep: str) -> int:
      """Characters copied by sep.join(pieces), separators included."""
      if not pieces:
          return 0
      return sum(len(piece) for piece in pieces) + len(sep) * (len(pieces) - 1)
  ```

  ```text
  join     : 160
  join "-" : 191
  join ", ": 222
  ```

  Separators go *between*, so there are `n - 1` of them, not `n`. That
  off-by-one is the same one that puts a trailing dash on a hand-built string,
  and here it is visible as a number.

- **Prove the refcount optimisation exists, then defeat it.**

  ```python
  banner = ""
  first = id(banner)
  for _ in range(1000):
      banner += "BLOOM"
  print("grew in place at least once:", id(banner) != first)

  pinned = ""
  keep = []
  addresses = set()
  for _ in range(100):
      pinned += "BLOOM"
      keep.append(pinned)
      addresses.add(id(pinned))
  print("distinct string objects while pinned:", len(addresses))
  ```

  ```text
  grew in place at least once: True
  distinct string objects while pinned: 100
  ```

  In the second loop every intermediate string is kept alive by `keep`, so the
  refcount is never 1, so every `+=` really does allocate — a hundred loops,
  a hundred different objects. That is the quadratic version you counted, made
  visible.

Next: [Problem 2 — The Bakery's Order Slips](./problem-02-bakery-order-slips.md).
