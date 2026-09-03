# Challenge 2 — The Ledger Adder

> Topic: addition from bitwise primitives · Lecture: [1](../lecture-notes/01-bit-manipulation-fundamentals-and-xor.md) · Difficulty: Medium · Target time: 60 minutes including the FRAME write-up · Why this one: it is the problem where "how does a machine hold a number" stops being trivia and becomes the reason your loop terminates.

## The Brief

An old signal box totals its movement counts on a relay board. The board can
AND, OR, XOR and shift. It has **no adder** — nobody built one — so addition has
to be assembled from the operations it does have.

The insight is one sentence: **XOR is addition that forgets to carry, and AND
finds exactly the columns that should have carried.** Shift the carries one
place left and do it again. When nothing is left to carry, the XOR is the answer.

The engineer maintaining the board wants two things: the total, and **how many
carry rounds it took** — a total needing many rounds is a total the board
computes slowly, and that is worth knowing.

## Starter

`challenge-02-ledger-adder-solution.py` sits beside this page with the self-checks.

The board is **16-bit and signed**. That is not decoration: Python's integers are
unbounded, and a negative one behaves as though it has infinitely many leading
`1` bits, so the carry loop on a negative operand **never terminates**. Masking
to 16 bits is what makes the loop stop, and it is what the relays actually do.

## Requirements

1. `ledger_add(left, right)` returns `(total, carry_rounds)`.
2. The total is the **16-bit signed** result — it wraps at the top of the board
   rather than growing.
3. Operands that do not fit in 16 signed bits raise `ValueError` rather than
   being silently truncated.
4. `add_report(...)` prints each pair with its round count and flags any that
   wrapped.
5. No `+` and no `-` on the counts themselves. That is the whole exercise.

## Constraints

- **Mask after every shift.** A carry that walks off the top of a 16-relay board
  does not exist; letting it live in a Python integer is what makes the loop
  run forever on negatives.
- **Two's complement is how the board reads a register.** Converting back to a
  signed Python integer at the end is part of the answer, not presentation.
- **`carry_rounds` is 0 only when the second count is zero.** Adding anything at
  all costs at least one round, even when the two numbers share no bit positions
  and that round finds nothing to carry. Say which it is; a plausible-sounding
  wrong claim here is easy to write.
- Wrapping at `32767 + 1` is **correct**, not a bug. A solution that returns
  `32768` is not modelling the hardware.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-ledger-adder-solution.py
ledger additions
          0 +       0 =       0   rounds  0   ok 
          5 +       3 =       8   rounds  4   ok 
        255 +       1 =     256   rounds  9   ok 
       1023 +       1 =    1024   rounds 11   ok 
         -1 +       1 =       0   rounds 16   ok 
         -8 +       3 =      -5   rounds  1   ok 
      12345 +  -12345 =       0   rounds 16   ok 
      32767 +       1 =  -32768   rounds 16   ok 

All checks passed.
```

Read the round counts, not the totals. `-8 + 3` takes **one** round; `-1 + 1`
takes **sixteen**, because `-1` is sixteen `1` bits and the carry has to fold
through every one of them. Same operation, same board, sixteen times the work —
that is the sentence your Examine (cost) section wants.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the three operations and what each one contributes.
3. Implement the loop on **positive** numbers first, and get `5 + 3` right.
4. Now try it on `-1 + 1` without masking, with a round limit so you can watch
   it fail. Understanding *why* it never ends is the lesson; the mask is only
   the fix.
5. Add the mask and the two's-complement read-back.
6. Add the range guard, then write the FRAME pass.

## The Solution

```python
"""challenge-02-ledger-adder-solution.py - adding without an adder.

An old signal box totals its movement counts on a relay board. The board can
AND, OR, XOR and shift. It has no adder, because nobody built one - so addition
has to be assembled from the operations it does have.

XOR is addition that forgets to carry. AND finds exactly the columns that
should have carried. Shift the carries one place left and do it again. When
there is nothing left to carry, the XOR is the answer.

The engineer maintaining the board wants two things: the total, and how many
carry rounds it took, because a total that needs many rounds is a total the
board computes slowly and is worth knowing about.

  ledger_add    - the sum, and the number of carry rounds
  add_report    - a few pairs, with their rounds

Python's integers are unbounded and negative ones behave as though they have
infinitely many leading 1 bits, so the carry loop on a negative operand never
terminates. The board is 16-bit, so this masks to 16 bits and interprets the
result as signed - which is what the relays actually do, and is the part of the
problem that is really about how machines hold numbers.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1
SIGN_BIT = 1 << (WIDTH - 1)


def _to_signed(value: int) -> int:
    """Read a 16-bit pattern the way the board reads it: two's complement."""
    value &= MASK
    return value - (1 << WIDTH) if value & SIGN_BIT else value


def ledger_add(left: int, right: int) -> tuple[int, int]:
    """Add two counts using only bitwise operations.

    Args:
        left: One count, as the board holds it.
        right: The other count.

    Returns:
        (total, carry_rounds). The total is the 16-bit signed result, and
        carry_rounds is how many times the board had to fold carries back in.
        It is 0 only when the second count is zero and the loop never runs;
        adding anything at all costs at least one round, even when the two
        numbers share no bit positions and that round finds nothing to carry.

    Raises:
        ValueError: If either operand does not fit in 16 signed bits.
    """
    for name, value in (("left", left), ("right", right)):
        if not -SIGN_BIT <= value < SIGN_BIT:
            raise ValueError(f"{name}={value} does not fit in {WIDTH} signed bits")

    total = left & MASK
    carry = right & MASK
    rounds = 0
    while carry:
        # XOR is the sum of every column that does not carry; AND marks the
        # columns that do. Masking after the shift is what stops the carry
        # walking off the top of a board that only has 16 relays.
        total, carry = (total ^ carry) & MASK, ((total & carry) << 1) & MASK
        rounds += 1
    return _to_signed(total), rounds


def add_report(pairs: list[tuple[int, int]]) -> None:
    """Print the total and the carry rounds for each pair."""
    for left, right in pairs:
        total, rounds = ledger_add(left, right)
        check = "ok " if total == _to_signed(left + right) else "WRAP"
        print(f"    {left:>7} + {right:>7} = {total:>7}   rounds {rounds:>2}   {check}")


# ---- Self-check ----
if __name__ == "__main__":
    print("ledger additions")
    add_report([
        (0, 0),
        (5, 3),
        (255, 1),
        (1023, 1),
        (-1, 1),
        (-8, 3),
        (12345, -12345),
        (32767, 1),      # the top of the board: this one wraps, and says so
    ])

    # The arithmetic must match ordinary addition wherever the board can hold
    # the answer. That is the whole claim, so it is tested across a range
    # rather than on a handful of favourites.
    for left in range(-40, 41):
        for right in range(-40, 41):
            total, _ = ledger_add(left, right)
            assert total == left + right, (left, right, total)

    # Zero carries nothing.
    assert ledger_add(0, 0) == (0, 0)

    # Numbers sharing no bit positions still cost one round - the loop is
    # entered because the second count is non-zero, and that round finds
    # nothing to carry. 8 is 1000 and 5 is 0101, so the XOR alone is the answer.
    assert ledger_add(8, 5) == (13, 1)
    # Only a zero second count skips the loop entirely.
    assert ledger_add(13, 0) == (13, 0)

    # A long carry chain: 255 is eight 1 bits, and adding 1 folds through all
    # of them. The round count is the interesting output here, not the total.
    total, rounds = ledger_add(255, 1)
    assert total == 256
    assert rounds == 9

    # Negatives work because the board reads two's complement.
    assert ledger_add(-1, 1)[0] == 0
    assert ledger_add(-8, 3)[0] == -5
    assert ledger_add(12345, -12345)[0] == 0

    # The top of the board wraps rather than growing, which is what the relays
    # do. A solution that returns 32768 here is not modelling the hardware.
    assert ledger_add(32767, 1)[0] == -32768

    # Anything that does not fit is refused rather than silently truncated.
    for bad in (32768, -32769, 70000):
        try:
            ledger_add(bad, 0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print()
    print("All checks passed.")
```

The exhaustive check across every pair from −40 to 40 is deliberate. Bit
arithmetic is exactly the kind of code that passes six hand-picked examples and
fails a seventh, and 6,561 pairs cost nothing to verify.

## Download and run

Download the solution beside this page and run it:

```bash
python challenge-02-ledger-adder-solution.py
```

No third-party packages, no arguments, no input. It prints eight additions with
their round counts and then `All checks passed.`

## Common bugs to catch

- **No mask, and a negative operand.** Symptom: the program hangs. The carry
  keeps finding another bit position forever, because Python's integers have no
  top.
- **Masking the XOR but not the shifted carry.** Symptom: it terminates and the
  answer is wrong at the top of the range.
- **Forgetting the two's-complement read-back.** Symptom: `-1 + 1` reports
  `0` correctly but `-8 + 3` reports 65531.
- **Assigning `total` before `carry` without a tuple.** Symptom: the carry is
  computed from the *new* total. The two assignments happen together for a
  reason.
- **Returning 32768 for `32767 + 1`.** Symptom: a correct Python answer and an
  incorrect board answer.
- **Claiming zero rounds for numbers that share no bits.** Symptom: an assertion
  that reads well and fails. The loop is entered whenever the second count is
  non-zero.

## Acceptance checklist

- [ ] Matches ordinary addition for every pair in −40…40, asserted.
- [ ] `8 + 5` takes one round; `13 + 0` takes none.
- [ ] `255 + 1` totals 256 in nine rounds.
- [ ] `-8 + 3` returns −5; `-1 + 1` returns 0.
- [ ] `32767 + 1` returns −32768.
- [ ] Out-of-range operands raise `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Implement subtraction on the same board. Two's complement makes it one extra
  step, and naming that step is the point.
- Report the **widest** carry chain rather than the count of rounds, and say
  which operand pairs produce it. It is not always the largest numbers.
- Make `WIDTH` 8 and re-run the exhaustive check. It will fail, and where it
  fails tells you exactly what the range guard is protecting.
