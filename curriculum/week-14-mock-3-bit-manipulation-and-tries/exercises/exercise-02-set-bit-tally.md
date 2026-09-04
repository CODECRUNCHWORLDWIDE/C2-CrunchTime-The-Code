# Exercise 2 — The Set-Bit Tally

> **Topic:** a table where every answer is one operation away from a smaller one already in it
> **Lecture:** [02 — Bitmasks, Subset Enumeration and Bit DP](../lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md)
> **Difficulty:** Easy-Medium
> **Target time:** 35 minutes
> **Why this one:** it is the smallest bit problem where the answer is a *table* rather than a value, and the recurrence is one line you can derive at the panel. It also introduces `n &= n - 1`, which is the single most useful bit idiom in the week.

## The Brief

A panel of indicator lamps shows a register in binary. The maintenance log
wants, for **every** register value from 0 up to a limit, how many lamps are
lit.

Counting each value on its own is fine and is the answer to say first. The
answer worth writing up notices the work has already been done.

## Starter

The worked answer on this page carries the limits and the self-checks.

Write out the counts for 0 to 7 by hand first:

```text
0  000  0     4  100  1
1  001  1     5  101  2
2  010  1     6  110  2
3  011  2     7  111  3
```

Now look at 6 and 3. And at 4 and 2. And at 5 and 2. The pattern is there before
any code is.

## Requirements

1. `lamp_tally(limit)` returns the count for every value from 0 to `limit`,
   **and** the number of additions the pass made.
2. `lamp_tally_one_at_a_time(limit)` builds the same table by counting each
   value's bits from scratch, also returning its work count.
3. `lamps_lit(value)` counts one value's lamps using `value &= value - 1`.
4. `fullest_value(limit)` returns the smallest value with the most lamps lit.
5. Negative limits and values are refused.

## Constraints

- **The recurrence is `lit[n] == lit[n >> 1] + (n & 1)`.** Shifting right by one
  drops the last lamp; whatever is left is a number below `n`, so it is already
  in the table. Add back the lamp that was dropped.
- **`n >> 1` is strictly smaller than `n` for `n > 0`.** That is the whole
  correctness argument for filling the table upwards, and it belongs in the memo.
- **`value &= value - 1` clears the lowest lit lamp and nothing else.** So the
  loop runs once per **lit** lamp, not once per lamp position — a 64-bit register
  with two lamps lit costs two turns.
- **Negative values are refused.** A negative Python integer has no finite binary
  width, so the clearing loop would not terminate. Refuse it rather than masking
  around it.
- **Report the work counts**, so the comparison is a number.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-02-set-bit-tally.py
LAMPS LIT, 0 TO 16
      0      0   0
      1      1   1
      2     10   1
      3     11   2
      4    100   1
      5    101   2
      6    110   2
      7    111   3
      8   1000   1
      9   1001   2
     10   1010   2
     11   1011   3
     12   1100   2
     13   1101   3
     14   1110   3
     15   1111   4
     16  10000   1

REUSING THE TABLE AGAINST COUNTING EACH VALUE
    to    16:      16 additions       54 bit tests
    to  1024:    1024 additions     9228 bit tests

    fullest value below 16: 15 (1111) with 4 lamps

All checks passed.
```

The comparison block is the point, and it is the ratio rather than the totals
that matters. Up to 16, the table makes 16 additions against 54 bit tests. Up to
1024, it is 1,024 against 9,228 — the table's work grows in step with the limit
while the bit-by-bit count grows faster, because every value costs a turn per bit
of its width.

That is `O(n)` against `O(n log n)`, visible in two rows.

## Steps

1. Read the self-checks. They are the spec.
2. Write out 0 to 7 by hand and find the pattern.
3. Write the memo: the recurrence in one line, plus the sentence about why
   `n >> 1` is already computed.
4. Build the table upwards, counting additions.
5. Write the one-at-a-time version too, and compare.
6. Write `lamps_lit` with `value &= value - 1` and check it agrees with the
   table for every value.
7. Handle the negative cases, then write the FRAME pass.

## The Solution

```python
"""exercise-02-set-bit-tally-solution.py - counting lamps, and reusing the count.

A panel of indicator lamps shows a register in binary. The maintenance log
wants, for every register value from 0 up to a limit, how many lamps are lit.

Counting each value on its own is fine and is the answer to say first. The
answer worth writing up notices that the work has already been done: a value's
lamp count is its own last bit plus the count of the value with that last bit
shifted off - and that value is smaller, so it is already in the table.

    lit[n] == lit[n >> 1] + (n & 1)

Shifting right by one drops the last lamp. Whatever is left is a number below
`n`, already counted. Add back the lamp that was dropped.

That is one table pass and one addition per value, against a bit-by-bit count
per value. The file counts the operations both ways so the difference is a
printed number rather than a claim about constants.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
LIMIT = 16
BIG_LIMIT = 1024


# ---- Your task ----
def lamp_tally(limit: int) -> tuple[list[int], int]:
    """Return the lamp count for every value from 0 to `limit`, and the work.

    Args:
        limit: The highest register value to count. Must not be negative.

    Returns:
        A pair: a list of length limit + 1 where entry n is the number of lamps
        lit for register value n, and how many additions the pass made.

    Raises:
        ValueError: If `limit` is negative.
    """
    if limit < 0:
        raise ValueError("a register limit cannot be negative")
    lit = [0] * (limit + 1)
    additions = 0
    for value in range(1, limit + 1):
        # value >> 1 is strictly smaller, so lit[value >> 1] is already written.
        lit[value] = lit[value >> 1] + (value & 1)
        additions += 1
    return lit, additions


def lamp_tally_one_at_a_time(limit: int) -> tuple[list[int], int]:
    """The same table, counting each value's bits from scratch. For comparison.

    Args:
        limit: The highest register value to count.

    Returns:
        The same list - this version is correct, only wasteful - and how many
        single-bit tests it made.

    Raises:
        ValueError: If `limit` is negative.
    """
    if limit < 0:
        raise ValueError("a register limit cannot be negative")
    lit: list[int] = []
    tests = 0
    for value in range(limit + 1):
        count = 0
        remaining = value
        while remaining:
            count += remaining & 1
            remaining >>= 1
            tests += 1
        lit.append(count)
    return lit, tests


def lamps_lit(value: int) -> int:
    """Return how many lamps one register value lights, by clearing them.

    Uses `value &= value - 1`, which clears the lowest lit lamp and nothing
    else. That makes the loop run once per LIT lamp rather than once per lamp
    position, so a register with two lamps lit costs two turns however wide the
    register is.

    Args:
        value: The register value. Must not be negative.

    Returns:
        The number of lit lamps.

    Raises:
        ValueError: If `value` is negative. A negative integer in Python has no
            finite binary width, so the loop would not terminate.
    """
    if value < 0:
        raise ValueError("a register value cannot be negative")
    count = 0
    while value:
        value &= value - 1
        count += 1
    return count


def fullest_value(limit: int) -> tuple[int, int]:
    """Return the value below `limit` lighting the most lamps, and how many.

    Args:
        limit: The highest register value to consider.

    Returns:
        A pair: the smallest value with the most lamps lit, and that count.

    Raises:
        ValueError: If `limit` is negative.
    """
    lit, _ = lamp_tally(limit)
    best = max(lit)
    return lit.index(best), best


# ---- Self-check ----
if __name__ == "__main__":
    lit, additions = lamp_tally(LIMIT)
    _, tests = lamp_tally_one_at_a_time(LIMIT)

    print(f"LAMPS LIT, 0 TO {LIMIT}")
    for value in range(LIMIT + 1):
        print(f"    {value:>3}  {value:>5b}   {lit[value]}")
    print()

    _, big_additions = lamp_tally(BIG_LIMIT)
    _, big_tests = lamp_tally_one_at_a_time(BIG_LIMIT)
    print("REUSING THE TABLE AGAINST COUNTING EACH VALUE")
    print(f"    to {LIMIT:>5}:  {additions:>6} additions   {tests:>6} bit tests")
    print(f"    to {BIG_LIMIT:>5}:  {big_additions:>6} additions   {big_tests:>6} bit tests")
    print()

    fullest, count = fullest_value(LIMIT)
    print(f"    fullest value below {LIMIT}: {fullest} ({fullest:b}) with {count} lamps")
    print()

    # The table opens 0, 1, 1, 2, 1, 2, 2, 3 - which is the pattern to check by
    # hand before trusting anything else.
    assert lit[:8] == [0, 1, 1, 2, 1, 2, 2, 3]

    # A power of two lights exactly one lamp, whatever its size.
    for power in range(5):
        assert lit[2 ** power] == 1

    # One less than a power of two lights every lamp below it.
    assert lit[15] == 4
    assert lit[7] == 3

    # The table version and the one-at-a-time version agree everywhere.
    slow, _ = lamp_tally_one_at_a_time(LIMIT)
    assert lit == slow

    # ...and `lamps_lit` agrees with both, value by value.
    for value in range(LIMIT + 1):
        assert lamps_lit(value) == lit[value]

    # The table does strictly less work, and the gap widens with the limit.
    assert additions < tests
    assert big_additions < big_tests
    assert big_tests / big_additions > tests / additions

    # A limit of zero is a table of one entry: zero lamps.
    assert lamp_tally(0)[0] == [0]

    # The fullest value below 16 is 15, with four lamps. Ties go to the
    # smallest value, which is why 15 rather than anything above it.
    assert fullest_value(LIMIT) == (15, 4)

    # Negative limits and values are refused rather than looping forever.
    try:
        lamp_tally(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative limit")
    try:
        lamps_lit(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative value")

    print("All checks passed.")
```

Three ways of counting bits appear in this one file — the table recurrence, the
bit-by-bit shift, and the clear-lowest loop — and they agree on every value from
0 to the limit. That agreement is asserted rather than assumed, because three
implementations of the same thing is exactly where a quiet disagreement hides.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-02-set-bit-tally.py
```

No third-party packages, no arguments, no input. It prints the table, the two
work counts at both limits, the fullest value, and then `All checks passed.`

## Common bugs to catch

- **`lit[n >> 1] + 1` unconditionally.** Symptom: every count one too high for
  even numbers. The `+ (n & 1)` is the lamp that was dropped, and it is often
  zero.
- **Filling the table downwards.** Symptom: reading entries that are not written
  yet, and a table of zeroes.
- **Starting the loop at 0 rather than 1.** Symptom: `0 >> 1` is 0, so entry 0
  reads itself. It happens to give the right answer here, which is worse than
  crashing.
- **`value &= value - 1` on a negative value.** Symptom: the loop never ends.
- **Comparing the two versions' work counts without checking they agree on the
  table.** Symptom: a fast wrong version declared an improvement.
- **`fullest_value` returning the largest such value rather than the smallest.**
  Symptom: right on this data by luck. State the tie-break.

## Acceptance checklist

- [ ] The table opens 0, 1, 1, 2, 1, 2, 2, 3.
- [ ] Every power of two lights exactly one lamp; 15 lights four.
- [ ] All three counting methods agree on every value.
- [ ] The table does less work than the one-at-a-time version, and the gap
      widens at the larger limit.
- [ ] `fullest_value(16)` is `(15, 4)`.
- [ ] A limit of zero gives `[0]`.
- [ ] Negative limits and values raise `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Derive a second recurrence: `lit[n] == lit[n & (n - 1)] + 1`. It is equally
  short and it says something different about the number. Say which you find
  easier to justify at a panel.
- Report the first value below the limit with exactly `k` lamps lit, for each
  `k`. The table already holds it.
- Time `int.bit_count()` against your loop on a million values. Python has had it
  since 3.10, and knowing that — and still being able to write the loop — is the
  answer that scores.
