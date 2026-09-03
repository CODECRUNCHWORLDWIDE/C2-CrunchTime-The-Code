# Exercise 4 — The Beacon Flash Period

> **Topic:** the border table, and the arithmetic that reads a repeat out of it
> **Lecture:** [03 — KMP and the Z-Algorithm](../lecture-notes/03-kmp-and-z-algorithm.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** the border table is the one piece of string machinery in this course that is genuinely hard to derive on the spot, and this is the smallest problem that needs the whole of it. It is also the page where the cost difference stops being asymptotic and becomes a printed number.

## The Brief

A harbour beacon repeats a fixed block of long and short flashes. Given a
recorded strip, find the **shortest block** that, repeated a whole number of
times, reproduces the strip exactly.

`LSSLSSLSSLSS` is `LSS` four times. `LSSLSSLSSL` is not a whole number of
repeats of anything shorter than itself, so the answer is the whole strip, once.

## Starter

`exercise-04-beacon-flash-period-solution.py` sits beside this page with seven
strips and the self-checks.

```text
LSSLSSLSSLSS    LSSLSSLSSL    LLLL    LSLS    L    LSSL    SLLSSLLSLLSSLL
```

There is also a long strip built to punish the obvious approach: six hundred long
flashes, one short, then six hundred long again. It is 1201 flashes and its
longest border is 600, which is the worst case for a nested loop and the best
demonstration of why the one-pass table exists.

## Requirements

1. `border_table(strip)` returns the border length at every cut, **and** the
   number of single-character comparisons the pass made.
2. `naive_longest_border(strip)` does the same job the obvious way, also
   returning its comparison count, so the two can be compared rather than
   asserted.
3. `shortest_block(strip)` returns the block and how many times it repeats.
4. An empty strip raises `ValueError`.
5. A strip that is not a whole number of repeats returns itself, once.

## Constraints

- **A border is a *proper* prefix.** The whole strip is not a border of itself,
  and getting that wrong makes every answer come out as one repeat of everything.
- **The repeat test is arithmetic, not search.** With `n` the strip length and
  `b` its longest border, the strip repeats exactly when `n % (n - b) == 0`, and
  the block length is `n - b`. Deriving that line is the exercise; the code
  around it is short.
- **One pass, and the position never goes backwards.** That is the whole claim of
  the table, and the comparison counts are in the file to make it checkable.
- **Both counts are returned, not printed.** A cost claim that nothing asserts
  stops being true silently.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-04-beacon-flash-period-solution.py
LSSLSSLSSLSS    block LSS      x4
LSSLSSLSSL      block LSSLSSLSSL x1
LLLL            block L        x4
LSLS            block LS       x2
L               block L        x1
LSSL            block LSSL     x1
SLLSSLLSLLSSLL  block SLLSSLL  x2

long strip flashes       1201
longest border            600
nested-loop compares   180900
one-pass compares        1799
times cheaper             100

All checks passed.
```

The last four lines are the exercise. On the 1201-flash strip the nested loop
makes **180,900** comparisons and the one-pass table makes **1,799** — a hundred
times fewer, on an input small enough to fit on a screen. Asymptotics stop being
abstract at that point.

Note also `SLLSSLLSLLSSLL`, which repeats as `SLLSSLL` twice. It is in the data
because it is the case where the answer is neither the whole strip nor an obvious
short block, and a solution that guesses rather than computes gets it wrong.

## Steps

1. Read the self-checks. They are the spec.
2. Do `LSSLSSLSSLSS` by hand: write the border length at every cut. Twelve
   numbers. Do not skip this — the table is much easier to write once you have
   built one.
3. Write the memo: the table, then the `n % (n - b)` line and why it holds.
4. Write `border_table`, counting comparisons as you go.
5. Write `naive_longest_border` too. It is six lines and it is what makes the
   cost claim checkable.
6. Add `shortest_block` on top of the table.
7. Check the degenerate strips — one flash, no repeat, all the same flash — then
   write the FRAME pass.

## The Solution

```python
"""exercise-04-beacon-flash-period-solution.py — the beacon flash period.

A harbour beacon repeats a fixed block of long and short flashes. Given a
recorded strip, find the shortest block that, repeated a whole number of
times, reproduces the strip exactly.

The tool is the border table: for every cut of the strip, how long is the
longest opening run that is also the closing run. One pass builds it. The
obvious nested-loop version does the same job and gets slower and slower.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

STRIPS: list[str] = [
    "LSSLSSLSSLSS",
    "LSSLSSLSSL",
    "LLLL",
    "LSLS",
    "L",
    "LSSL",
    "SLLSSLLSLLSSLL",
]

# A long strip built to punish the nested-loop scan: a wall of long flashes,
# one short flash in the middle, then the same wall again.
LONG_STRIP: str = "L" * 600 + "S" + "L" * 600


def border_table(strip: str) -> tuple[list[int], int]:
    """Return the border length at every cut of `strip`, plus the work done.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair. First, a list as long as `strip`, where entry `i` is the length
        of the longest run that both opens and closes `strip[:i + 1]` without
        being the whole of it. Second, how many single-character comparisons
        the pass made.

    Raises:
        ValueError: If `strip` is empty.
    """
    if not strip:
        raise ValueError("a flash strip cannot be empty")
    size = len(strip)
    table = [0] * size
    comparisons = 0
    cursor = 1
    matched = 0
    while cursor < size:
        comparisons += 1
        if strip[cursor] == strip[matched]:
            matched += 1
            table[cursor] = matched
            cursor += 1
        elif matched:
            matched = table[matched - 1]
        else:
            table[cursor] = 0
            cursor += 1
    return table, comparisons


def naive_longest_border(strip: str) -> tuple[int, int]:
    """Return the longest border of `strip` the slow way, plus the work done.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair: the longest border length, and how many single-character
        comparisons the nested loops made.

    Raises:
        ValueError: If `strip` is empty.
    """
    if not strip:
        raise ValueError("a flash strip cannot be empty")
    size = len(strip)
    comparisons = 0
    for length in range(size - 1, 0, -1):
        fits = True
        for offset in range(length):
            comparisons += 1
            if strip[offset] != strip[size - length + offset]:
                fits = False
                break
        if fits:
            return length, comparisons
    return 0, comparisons


def shortest_block(strip: str) -> tuple[str, int]:
    """Return the shortest repeating block of `strip` and how often it repeats.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair: the block, and the number of whole repeats. When no shorter
        block tiles the strip, the strip itself is the block and the count is 1.

    Raises:
        ValueError: If `strip` is empty.
    """
    table, _ = border_table(strip)
    size = len(strip)
    step = size - table[-1]
    if size % step == 0:
        return strip[:step], size // step
    return strip, 1


# ---- Self-check ----
if __name__ == "__main__":
    for strip in STRIPS:
        block, repeats = shortest_block(strip)
        print(f"{strip:<15} block {block:<8} x{repeats}")

    slow_border, slow_cost = naive_longest_border(LONG_STRIP)
    fast_table, fast_cost = border_table(LONG_STRIP)
    print()
    print(f"long strip flashes    {len(LONG_STRIP):>7}")
    print(f"longest border        {slow_border:>7}")
    print(f"nested-loop compares  {slow_cost:>7}")
    print(f"one-pass compares     {fast_cost:>7}")
    print(f"times cheaper         {slow_cost // fast_cost:>7}")

    assert shortest_block("LSSLSSLSSLSS") == ("LSS", 4)
    assert shortest_block("LSSLSSLSSL") == ("LSSLSSLSSL", 1)
    assert shortest_block("LLLL") == ("L", 4)
    assert shortest_block("LSLS") == ("LS", 2)
    assert shortest_block("L") == ("L", 1)
    assert shortest_block("LSSL") == ("LSSL", 1)
    assert border_table("LSSLSSLSSLSS")[0] == [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert fast_table[-1] == slow_border
    assert fast_cost < slow_cost

    try:
        shortest_block("")
    except ValueError as problem:
        assert str(problem) == "a flash strip cannot be empty"
    else:
        raise AssertionError("an empty strip should have been rejected")

    print()
    print("All checks passed.")
```

`n % (n - b) == 0` is the whole algorithm and it deserves the paragraph the
docstring gives it. The intuition: if the strip has a border of length `b`, then
sliding the strip along by `n - b` lines it up with itself. When `n - b` divides
`n` evenly, that slide tiles the strip exactly — which is what "repeats" means.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-04-beacon-flash-period-solution.py
```

No third-party packages, no arguments, no input. It prints each strip with its
block and repeat count, the two comparison counts on the long strip, and then
`All checks passed.`

## Common bugs to catch

- **Treating the whole strip as its own border.** Symptom: every strip returns
  itself once.
- **`n % b` instead of `n % (n - b)`.** Symptom: right on `LLLL`, wrong on almost
  everything else. The block is the *non*-border part.
- **A nested loop that looks like one pass.** Symptom: correct output and a
  comparison count that grows quadratically. The count is the check.
- **Backing the position up on a mismatch.** Symptom: the table is right and the
  cost claim is not.
- **An empty strip returning an empty block.** Symptom: a division by zero one
  line later. Refuse it.
- **Assuming the block divides evenly without checking.** Symptom: `LSSLSSLSSL`
  reported as `LSS` three and a bit times.

## Acceptance checklist

- [ ] `LSSLSSLSSLSS` is `LSS` four times; `LSSLSSLSSL` is itself, once.
- [ ] `SLLSSLLSLLSSLL` is `SLLSSLL` twice.
- [ ] `LLLL` is `L` four times; `L` is `L` once.
- [ ] The 1201-flash strip has a longest border of 600.
- [ ] The one-pass count is about a hundred times below the nested-loop count.
- [ ] An empty strip raises `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the block for every *prefix* of a strip, not just the whole one. The
  table already holds it, and the list is what a live beacon watcher would show.
- Build a strip that makes the nested loop worse still, and say what shape does
  it. It is not the longest strip, it is the most self-similar one.
- Use the same table to find every occurrence of a short code inside a long
  strip — that is [Homework 3](../homework/README.md#problem-3--the-splice-point),
  and it is the same table read differently.
