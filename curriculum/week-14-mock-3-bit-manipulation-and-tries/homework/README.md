# Week 14 — Homework

Six problems, all original, each with a runnable worked answer folded under it.
Allow about four and a half hours. Do each with the lectures closed; open the
reveal only after your own version runs, or after fifteen minutes stuck on one
step.

Mock #3 is on Friday, so this set is deliberately shorter and more mechanical
than most weeks. The point is recognition speed, not depth.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Triple-Logged Fault](#problem-1--the-triple-logged-fault) | When the XOR fold stops working, and what replaces it | 45 min |
| 2 | [The Lamp Distance](#problem-2--the-lamp-distance) | Popcount, and the one line that turns it into a distance | 35 min |
| 3 | [The Reversed Loom](#problem-3--the-reversed-loom) | Bit layout — the walk and the fold | 45 min |
| 4 | [The Common Prefix Range](#problem-4--the-common-prefix-range) | A structural observation that replaces a loop | 45 min |
| 5 | [The Missing Ticket](#problem-5--the-missing-ticket) | Two right answers, and the constraint that separates them | 30 min |
| 6 | [The Paired Ribbon Swap](#problem-6--the-paired-ribbon-swap) | Two masks, two shifts, every pair at once | 40 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, copy the code out of its reveal
into a file of your own and run that:

```bash
python problem-01-triple-logged-fault.py
```

---

## Problem 1 — The Triple-Logged Fault

**The brief.** A relay tester writes every fault code **three** times. One code
in this log appears only once, because an engineer wrote it in by hand. Find it,
in linear time and constant space.

**The data.** Ten entries: three codes logged three times each, plus `0x0051`.

**Constraints.** Constant space, which rules out a counter. Zero can be the lone
code.

**Answer.** The XOR fold from
[Exercise 1](../exercises/exercise-01-relay-fold.md) **does not work**, and being
clear about why is half the problem: XOR cancels in *pairs*, so three copies
leave one behind, and folding the whole log gives you the XOR of every distinct
code.

What works is counting per **bit position** rather than per code. Every bit of a
tripled code contributes three to that position's total, and three divides by
three. So the positions whose totals are **not** divisible by three are exactly
where the lone code has a bit. Reassemble those bits.

That generalises: for codes appearing `k` times, count per position and take the
total mod `k`. The XOR fold is the `k = 2` case of the same idea, done faster.

The file ships the fold so you can watch it fail — on this log it returns
`0x3481`, which is the XOR of the distinct codes and not anybody's answer.

**Signatures.** `lone_fault(codes, repeats=3)`, `position_totals(codes)`,
`lone_fault_by_folding(codes)`.

**Watch for.** Reaching for the fold because it worked last time. Assuming a
non-zero result means success. The per-position count is `O(n × width)`, which is
still linear in the log — say so rather than calling it `O(n)` and hoping.

<details>
<summary>Worked answer — <code>problem-01-triple-logged-fault-solution.py</code></summary>

```python
"""problem-01-triple-logged-fault-solution.py - when the fold stops working.

A relay tester writes every fault code THREE times - once when the fault is
raised, once when it is confirmed, once when it is cleared. One code in this log
appears only once, because an engineer wrote it in by hand and the tester never
saw it.

Find it, in linear time and constant space.

The XOR fold from Exercise 1 does not work here and it is worth being clear
why: XOR cancels a code in PAIRS, so three copies leave one behind, and folding
the whole log leaves the XOR of every distinct code rather than the odd one out.

What does work is counting per BIT POSITION rather than per code. Every bit of a
tripled code contributes three to that position's total, and three is divisible
by three. So the positions whose totals are NOT divisible by three are exactly
the positions where the lone code has a bit, and reassembling those bits gives
the answer.

That generalises: for codes appearing k times, count per position and take the
total mod k. The XOR fold is the k = 2 case of the same idea, done faster.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# Every code three times except 0x0051, which was written once by hand.
FAULT_LOG: tuple[int, ...] = (
    0x00A3, 0x1F04, 0x00A3, 0x2B77, 0x1F04, 0x0051, 0x2B77,
    0x00A3, 0x1F04, 0x2B77,
)


# ---- Your task ----
def lone_fault(codes: tuple[int, ...], repeats: int = 3) -> int:
    """Return the code logged once when every other is logged `repeats` times.

    Args:
        codes: The fault log, in any order. Every code must fit in WIDTH bits.
        repeats: How many times a normal code appears. Must be at least 2.

    Returns:
        The code that appears once.

    Raises:
        ValueError: If `repeats` is below 2, if any code does not fit in WIDTH
            bits, or if the log does not hold exactly one code appearing a
            number of times not divisible by `repeats`.
    """
    if repeats < 2:
        raise ValueError("a normal code must be logged at least twice")
    for code in codes:
        if not 0 <= code < (1 << WIDTH):
            raise ValueError(f"{code} is not a {WIDTH}-bit fault code")

    lone = [code for code in set(codes) if codes.count(code) % repeats]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one odd code, found {len(lone)}")

    answer = 0
    for position in range(WIDTH):
        total = sum(code >> position & 1 for code in codes)
        if total % repeats:
            answer |= 1 << position
    return answer


def position_totals(codes: tuple[int, ...]) -> list[int]:
    """Return how many codes have a bit at each position, lowest first.

    Args:
        codes: The fault log.

    Returns:
        A list of length WIDTH. Printing it beside the totals mod 3 is what
        makes the method visible: the positions that do not divide evenly are
        exactly the lone code's bits, and you can read the answer off the page.
    """
    return [sum(code >> position & 1 for code in codes) for position in range(WIDTH)]


def lone_fault_by_folding(codes: tuple[int, ...]) -> int:
    """The XOR fold, kept to be run and seen failing.

    Args:
        codes: The fault log.

    Returns:
        Whatever the fold produces, which on a tripled log is NOT the lone
        code. It is the XOR of every distinct code, because three copies of a
        code cancel down to one. Shipped so the failure is something you have
        watched rather than been told about.
    """
    folded = 0
    for code in codes:
        folded ^= code
    return folded


# ---- Self-check ----
if __name__ == "__main__":
    print("FAULT LOG")
    print("    " + "  ".join(f"0x{code:04X}" for code in FAULT_LOG))
    print()

    print("BITS PER POSITION, AND THE REMAINDER MOD 3")
    totals = position_totals(FAULT_LOG)
    for position in range(WIDTH - 1, -1, -1):
        mark = "  <- the lone code has a bit here" if totals[position] % 3 else ""
        print(f"    bit {position:>2}: {totals[position]:>2}   mod 3 = {totals[position] % 3}{mark}")
    print()

    answer = lone_fault(FAULT_LOG)
    folded = lone_fault_by_folding(FAULT_LOG)
    print(f"    counting per position: 0x{answer:04X}")
    print(f"    the XOR fold instead : 0x{folded:04X}   (not the answer)")
    print()

    # The hand-written code is 0x0051.
    assert lone_fault(FAULT_LOG) == 0x0051

    # The fold does NOT find it, and that is the point of shipping it.
    assert lone_fault_by_folding(FAULT_LOG) != 0x0051
    # ...specifically, it is the XOR of the distinct codes.
    distinct = 0
    for code in set(FAULT_LOG):
        distinct ^= code
    assert lone_fault_by_folding(FAULT_LOG) == distinct

    # Order does not matter.
    assert lone_fault(tuple(reversed(FAULT_LOG))) == 0x0051

    # The method is not special to three. Two is the XOR fold's case, and the
    # per-position count gets the same answer more slowly.
    assert lone_fault((7, 7, 3), repeats=2) == 3
    assert lone_fault((5, 5, 5, 5, 9), repeats=4) == 9

    # Zero can be the lone code, which a "non-zero means found" test misses.
    assert lone_fault((7, 7, 7, 0)) == 0

    # A log of one code is that code.
    assert lone_fault((0x2B,)) == 0x2B

    # A log where everything divides evenly has no answer, and so does one with
    # two odd codes - which would otherwise return a number that is neither.
    for bad in ((1, 1, 1, 2, 2, 2), (1, 2), ()):
        try:
            lone_fault(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    # A code too wide for the register is refused rather than silently truncated.
    try:
        lone_fault((1 << WIDTH, 1, 1, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for an over-wide code")

    # A repeat count below 2 is meaningless.
    try:
        lone_fault(FAULT_LOG, repeats=1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for repeats below 2")

    print("All checks passed.")
```

</details>
---

## Problem 2 — The Lamp Distance

**The brief.** Two indicator panels are supposed to show the same register. When
they disagree, report **in how many lamp positions** — not whether, but how far
apart.

**The data.** Five pairs of readings, from identical to completely opposite.

**Constraints.** Negative registers are refused, because a negative Python
integer has no finite binary width and the counting loop would not terminate.

**Answer.** XOR joins the two halves of this problem in one line. `a ^ b` lights
a bit exactly where the two registers disagree, so **the distance is the lamp
count of the XOR**. Once that sentence is written down there is no second
algorithm to write.

The counting itself is `n &= n - 1`, which clears the lowest lit lamp and
nothing else — so the loop turns once per **lit** lamp rather than once per
position. The file counts turns both ways: a register with two lamps lit costs 2
turns against 16 tested.

**Signatures.** `lamps_lit(value)`, `lamps_lit_by_position(value)`,
`lamp_distance(first, second)`, `worst_pair(readings)`.

**Watch for.** Comparing the registers position by position, which is correct and
misses the whole point. `n &= n - 1` on a negative value never terminates. The
distance obeys the triangle inequality, which is worth asserting because it is
what makes "distance" the right word.

<details>
<summary>Worked answer — <code>problem-02-lamp-distance-solution.py</code></summary>

```python
"""problem-02-lamp-distance-solution.py - how far apart two panels are.

A works has two indicator panels that are supposed to show the same register.
When they disagree, the electrician wants to know HOW MUCH - not whether, but in
how many lamp positions.

Two questions, and the second falls out of the first in one line:

    lamps_lit(value)      how many lamps one panel has lit
    lamp_distance(a, b)   in how many positions the two panels differ

XOR is what joins them. `a ^ b` lights a bit exactly where the two registers
disagree, so the distance is the lamp count of the XOR - and once that sentence
is written down there is no second algorithm to write.

The counting itself is the Kernighan loop from Exercise 2: `n &= n - 1` clears
the lowest lit lamp, so the loop turns once per LIT lamp rather than once per
lamp position. On a 16-bit register differing in two places, that is two turns
and not sixteen.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# Readings taken from the two panels at the same moment.
PANEL_A: tuple[int, ...] = (0b0000_0000_0000_0000, 0b1111_0000_1111_0000,
                            0b1010_1010_1010_1010, 0b0000_0000_1111_1111,
                            0b1111_1111_1111_1111)
PANEL_B: tuple[int, ...] = (0b0000_0000_0000_0001, 0b1111_0000_1111_0000,
                            0b0101_0101_0101_0101, 0b1111_1111_0000_0000,
                            0b0000_0000_0000_0000)


# ---- Your task ----
def check_register(name: str, value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        name: What the value is, for the message.
        value: The register reading.

    Raises:
        ValueError: If the value is negative or too wide. Negative matters:
            a negative Python integer has no finite binary width, so the
            clearing loop below would never terminate.
    """
    if not 0 <= value < (1 << WIDTH):
        raise ValueError(f"{name} {value} is not a {WIDTH}-bit register")


def lamps_lit(value: int) -> tuple[int, int]:
    """Return how many lamps are lit, and how many turns it took.

    Args:
        value: The register reading.

    Returns:
        A pair: the number of lit lamps, and the number of loop turns - which
        are the same number, and that is the point. The loop runs once per lit
        lamp, never once per position.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register("value", value)
    count = turns = 0
    while value:
        value &= value - 1      # clears the lowest lit lamp and nothing else
        count += 1
        turns += 1
    return count, turns


def lamps_lit_by_position(value: int) -> tuple[int, int]:
    """The same count, testing every position. For comparison.

    Args:
        value: The register reading.

    Returns:
        A pair: the count, and the turns - which is always WIDTH, whatever the
        value. Shipped so "once per lit lamp" is a number rather than a claim.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register("value", value)
    count = 0
    for position in range(WIDTH):
        count += value >> position & 1
    return count, WIDTH


def lamp_distance(first: int, second: int) -> int:
    """Return in how many positions two registers differ.

    Args:
        first: One panel's reading.
        second: The other panel's reading.

    Returns:
        The number of differing lamp positions. Zero when the panels agree,
        WIDTH when they disagree everywhere.

    Raises:
        ValueError: If either value does not fit in WIDTH bits.
    """
    check_register("first", first)
    check_register("second", second)
    return lamps_lit(first ^ second)[0]


def worst_pair(readings: tuple[int, ...]) -> tuple[int, int, int] | None:
    """Return the two readings that differ most, and by how much.

    Args:
        readings: Register readings.

    Returns:
        A triple: the two positions in the list and the distance between them,
        or None when there are fewer than two readings. Ties go to the earliest
        pair, so the answer is one pair.

    Raises:
        ValueError: If any reading does not fit in WIDTH bits.
    """
    if len(readings) < 2:
        return None
    best = (0, 1, -1)
    for first in range(len(readings)):
        for second in range(first + 1, len(readings)):
            gap = lamp_distance(readings[first], readings[second])
            if gap > best[2]:
                best = (first, second, gap)
    return best


# ---- Self-check ----
if __name__ == "__main__":
    print("PANEL READINGS AND THEIR DISTANCE")
    print("    A                  B                  differ")
    for a, b in zip(PANEL_A, PANEL_B):
        print(f"    {a:0{WIDTH}b}   {b:0{WIDTH}b}   {lamp_distance(a, b):>2}")
    print()

    print("CLEARING THE LOWEST LAMP AGAINST TESTING EVERY POSITION")
    for value in (0b0000_0000_0000_0000, 0b0000_0000_0000_0011,
                  0b1010_1010_1010_1010, 0b1111_1111_1111_1111):
        lit, turns = lamps_lit(value)
        _, position_turns = lamps_lit_by_position(value)
        print(f"    {value:0{WIDTH}b}  {lit:>2} lit   {turns:>2} turns / {position_turns} tested")
    print()

    pair = worst_pair(PANEL_A)
    print(f"    the two panel-A readings that differ most: {pair}")
    print()

    # A register agrees with itself everywhere.
    for value in PANEL_A:
        assert lamp_distance(value, value) == 0

    # All zeroes against all ones differ in every position.
    assert lamp_distance(0, (1 << WIDTH) - 1) == WIDTH

    # Alternating patterns are the maximal disagreement short of that.
    assert lamp_distance(0b1010_1010_1010_1010, 0b0101_0101_0101_0101) == WIDTH

    # The distance is symmetric, which follows from XOR being symmetric.
    for a, b in zip(PANEL_A, PANEL_B):
        assert lamp_distance(a, b) == lamp_distance(b, a)

    # The two counting methods agree on every value in the data.
    for value in PANEL_A + PANEL_B:
        assert lamps_lit(value)[0] == lamps_lit_by_position(value)[0]

    # The clearing loop turns once per lit lamp; the positional test always
    # turns WIDTH times. That is the whole claim, and it is asserted.
    for value in PANEL_A + PANEL_B:
        lit, turns = lamps_lit(value)
        assert turns == lit
        assert lamps_lit_by_position(value)[1] == WIDTH

    # A register of zero costs no turns at all.
    assert lamps_lit(0) == (0, 0)

    # The distance obeys the triangle inequality, which is worth checking
    # because it is what makes "distance" the right word.
    for a in PANEL_A:
        for b in PANEL_B:
            for c in PANEL_A:
                assert lamp_distance(a, c) <= lamp_distance(a, b) + lamp_distance(b, c)

    # Fewer than two readings has no worst pair.
    assert worst_pair(()) is None
    assert worst_pair((5,)) is None

    # Out-of-range registers are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        try:
            lamps_lit(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All checks passed.")
```

</details>
---

## Problem 3 — The Reversed Loom

**The brief.** A ribbon loom was made up back to front — the sensor's lowest line
reaches the display's highest lamp, and so on. Every reading arrives with its
bits reversed. Reverse them back.

**The data.** Seven readings, including two that are unchanged by the fault.

**Constraints.** Sixteen bits, and the register is unsigned.

**Answer.** Two ways, and both are worth writing.

The **walk**: take bits off the bottom of the reading and push them onto the
bottom of the answer, sixteen times. The answer grows upwards while the reading
shrinks downwards, and that is what performs the reversal. This is the answer to
give at a panel.

The **fold**: swap halves, then quarters, then eighths, down to single bits. Four
masked steps instead of sixteen, and the same four lines would be five for a
32-bit register. This is the answer to *mention*.

**Signatures.** `unloom(value)`, `unloom_by_folding(value)`,
`unloom_steps(value)`, `symmetric(value)`.

**Watch for.** Building the answer by shifting *right* — the direction is the
whole trick. Testing on symmetric readings only: `1100000000000011` is unchanged
by the fault, so it proves nothing. The strongest check needs no known-good
answer at all: **reversing twice gives back the original**, on every value.

<details>
<summary>Worked answer — <code>problem-03-reversed-loom-solution.py</code></summary>

```python
"""problem-03-reversed-loom-solution.py - a cable loom wired back to front.

A sensor board is wired to a display through a ribbon loom, and the loom was
made up back to front: the sensor's lowest line reaches the display's highest
lamp, and so on all the way down. Every reading arrives with its bits reversed.

Reverse them back.

Two ways, and both are worth writing:

    the walk         take the bits off the bottom of the reading and push them
                     onto the bottom of the answer, WIDTH times. The answer
                     grows upwards while the reading shrinks downwards, which
                     is what performs the reversal.

    the fold         swap halves, then quarters, then eighths, down to single
                     bits. Four masked steps for a 16-bit register instead of
                     sixteen, and it is the one worth being able to explain
                     rather than the one worth writing first.

The walk is the answer to give at a panel. The fold is the answer to mention.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1

# ---- Given data ----
READINGS: tuple[int, ...] = (
    0b0000_0000_0000_0001,
    0b1000_0000_0000_0000,
    0b0000_0000_1111_1111,
    0b1010_1010_1010_1010,
    0b1100_0000_0000_0011,
    0b0000_0000_0000_0000,
    0b1111_1111_1111_1111,
)


# ---- Your task ----
def check_reading(value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        value: The reading as it arrived.

    Raises:
        ValueError: If the value is negative or too wide.
    """
    if not 0 <= value <= MASK:
        raise ValueError(f"{value} is not a {WIDTH}-bit reading")


def unloom(value: int) -> int:
    """Return `value` with its bits reversed, by walking them.

    Args:
        value: The reading as it arrived through the loom.

    Returns:
        The reading as the sensor sent it.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    answer = 0
    for _ in range(WIDTH):
        # Push the answer up to make room, then take the reading's lowest bit.
        answer = (answer << 1) | (value & 1)
        value >>= 1
    return answer


def unloom_by_folding(value: int) -> int:
    """Return `value` with its bits reversed, by swapping halves repeatedly.

    Swaps the two halves of the register, then the halves of each half, and so
    on down to single bits. Four steps for 16 bits, and the same four lines
    would be five for 32.

    Args:
        value: The reading as it arrived.

    Returns:
        The reading as the sensor sent it.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    # Swap 8-bit halves, then 4-bit, then 2-bit, then single bits.
    value = ((value & 0x00FF) << 8) | ((value & 0xFF00) >> 8)
    value = ((value & 0x0F0F) << 4) | ((value & 0xF0F0) >> 4)
    value = ((value & 0x3333) << 2) | ((value & 0xCCCC) >> 2)
    value = ((value & 0x5555) << 1) | ((value & 0xAAAA) >> 1)
    return value & MASK


def unloom_steps(value: int) -> list[str]:
    """Return the folding version's register after each swap, for reading.

    Args:
        value: The reading as it arrived.

    Returns:
        Five binary strings: the reading, then the register after each of the
        four swaps. Printing them is what makes the method make sense - the
        halves visibly change places, then the quarters, and so on.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    steps = [f"{value:0{WIDTH}b}"]
    for keep, shift in ((0x00FF, 8), (0x0F0F, 4), (0x3333, 2), (0x5555, 1)):
        drop = (~keep) & MASK
        value = ((value & keep) << shift) | ((value & drop) >> shift)
        steps.append(f"{value:0{WIDTH}b}")
    return steps


def symmetric(value: int) -> bool:
    """Say whether a reading is unchanged by the loom.

    Args:
        value: The reading.

    Returns:
        True when the reading reads the same both ways, so the miswired loom
        makes no difference to it. Those readings are exactly the ones that
        would hide the fault, which is why the electrician wants them named.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    return unloom(value) == value


# ---- Self-check ----
if __name__ == "__main__":
    print("READINGS THROUGH THE LOOM")
    print("    as received        as sent            same?")
    for value in READINGS:
        print(f"    {value:0{WIDTH}b}   {unloom(value):0{WIDTH}b}   {symmetric(value)}")
    print()

    print("THE FOLDING VERSION, STEP BY STEP")
    print("    starting from 1100000000000011")
    for step in unloom_steps(0b1100_0000_0000_0011):
        print(f"    {step}")
    print()

    # The lowest bit becomes the highest and back again.
    assert unloom(0b0000_0000_0000_0001) == 0b1000_0000_0000_0000
    assert unloom(0b1000_0000_0000_0000) == 0b0000_0000_0000_0001

    # A byte of ones moves from the bottom to the top.
    assert unloom(0b0000_0000_1111_1111) == 0b1111_1111_0000_0000

    # An alternating pattern shifts by one, which is a good hand check.
    assert unloom(0b1010_1010_1010_1010) == 0b0101_0101_0101_0101

    # The two methods agree on every reading in the data...
    for value in READINGS:
        assert unloom(value) == unloom_by_folding(value)

    # ...and on a wide sweep of the whole register range, which is the check
    # that matters: bit tricks are exactly the code that passes six hand-picked
    # examples and fails a seventh.
    for value in range(0, 1 << WIDTH, 97):
        assert unloom(value) == unloom_by_folding(value)

    # Reversing twice gives back the original, always. That is the strongest
    # property this function has and it needs no known-good answer to check.
    for value in range(0, 1 << WIDTH, 89):
        assert unloom(unloom(value)) == value

    # All zeroes and all ones are unchanged, and so is any palindrome.
    assert unloom(0) == 0
    assert unloom(MASK) == MASK
    assert symmetric(0) and symmetric(MASK)
    assert symmetric(0b1100_0000_0000_0011)
    assert not symmetric(0b0000_0000_0000_0001)

    # The folding version really does swap halves first: after one step the
    # two bytes have changed places and nothing else has moved.
    steps = unloom_steps(0b1111_1111_0000_0000)
    assert steps[1] == "0000000011111111"

    # Out-of-range readings are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        for function in (unloom, unloom_by_folding, unloom_steps):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
```

</details>
---

## Problem 4 — The Common Prefix Range

**The brief.** A meter runs through every count from `low` to `high`. A latching
board ANDs them all together. Report what is left — **without** looping through
the range, which can be the whole 16-bit space.

**The data.** Eight ranges, from a single count to the entire register space.

**Constraints.** `low` above `high` is refused rather than silently swapped.

**Answer.** One structural observation replaces the loop: **the AND of a range is
the common high-bit prefix of its two ends, with every lower bit zeroed.**

Why: take any bit position below the point where `low` and `high` first differ.
Somewhere inside the range that bit flips to 0 — it must, because the range
crosses a boundary at that position — and once a column holds a zero, the AND of
that column is zero. Above the first difference, both ends agree and so does
everything between them.

So: shift both ends right until they are equal, then shift back left by the same
count. On the whole 16-bit space that is 16 operations against 65,536.

`5 to 7` latches **4**: 101, 110, 111 agree on the 4 and disagree below it.

**Signatures.** `check_range(low, high)`, `latched(low, high)`,
`latched_by_looping(low, high)`, `common_prefix(low, high)`.

**Watch for.** Looping "just for small ranges", which is the habit the problem
exists to break. An off-by-one in the shift count — the check that catches it is
the sweep over every small range, not the eight in the data. The answer's low
bits must be exactly the ones the shifting cleared, which is a property worth
asserting.

<details>
<summary>Worked answer — <code>problem-04-common-prefix-range-solution.py</code></summary>

```python
"""problem-04-common-prefix-range-solution.py - what a whole range has in common.

A meter runs through every count from `low` to `high` inclusive during a test.
A latching relay board is wired to AND every count together, so what is left at
the end is the bits that were set in EVERY count of the range.

Report that value, without looping through the range - because the range can be
the whole 16-bit space and the board would have to be modelled a million times.

The structural observation is the whole problem, and it is one sentence: the AND
of a range is the common HIGH-BIT PREFIX of its two ends, with every lower bit
zeroed.

Why: take any bit position below the point where `low` and `high` first differ.
Somewhere inside the range that bit flips to 0 - it must, because the range
crosses a boundary at that position - and once a column holds a 0, the AND of
that column is 0. Above the first difference, both ends agree and so does
everything between them.

So the answer is: shift both ends right until they are equal, then shift that
value back left by the same amount.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1

# ---- Given data ----
RANGES: tuple[tuple[int, int], ...] = (
    (5, 7),
    (0, 0),
    (12, 12),
    (0, 1),
    (26, 30),
    (600, 700),
    (0, MASK),
    (0b1111_0000_0000_0000, 0b1111_0000_1111_1111),
)


# ---- Your task ----
def check_range(low: int, high: int) -> None:
    """Raise unless `low` and `high` are a valid range of WIDTH-bit counts.

    Args:
        low: The first count.
        high: The last count.

    Raises:
        ValueError: If either end is out of range, or `low` is above `high`.
    """
    for name, value in (("low", low), ("high", high)):
        if not 0 <= value <= MASK:
            raise ValueError(f"{name} {value} is not a {WIDTH}-bit count")
    if low > high:
        raise ValueError(f"low {low} is above high {high}")


def latched(low: int, high: int) -> tuple[int, int]:
    """Return the AND of every count in the range, and the shifts it took.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        A pair: the latched value, and how many positions the two ends had to
        be shifted before they agreed - which is how many low bits are zero in
        the answer.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    shifts = 0
    while low < high:
        low >>= 1
        high >>= 1
        shifts += 1
    return low << shifts, shifts


def latched_by_looping(low: int, high: int) -> int:
    """The same value, ANDing every count. For checking, not for using.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        The same answer, in time proportional to the size of the range rather
        than to the width of the register. On a range of the whole 16-bit space
        that is 65,536 operations against 16.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    latch = MASK
    for count in range(low, high + 1):
        latch &= count
    return latch


def common_prefix(low: int, high: int) -> str:
    """Return the shared opening bits of the two ends, as a string.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        The bits the two ends agree on, from the top down, as "0"s and "1"s -
        empty when they differ at the very first bit. Printing this beside the
        answer is what turns the rule from a recipe into something visible.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    low_bits = f"{low:0{WIDTH}b}"
    high_bits = f"{high:0{WIDTH}b}"
    shared: list[str] = []
    for left, right in zip(low_bits, high_bits):
        if left != right:
            break
        shared.append(left)
    return "".join(shared)


# ---- Self-check ----
if __name__ == "__main__":
    print("RANGES, THEIR SHARED PREFIX, AND WHAT LATCHES")
    for low, high in RANGES:
        value, shifts = latched(low, high)
        prefix = common_prefix(low, high) or "(none)"
        print(f"    {low:>5} to {high:<5}  prefix {prefix:<16}  latched {value:>5}  ({shifts} shifts)")
    print()

    print("THE STRUCTURAL OBSERVATION, ON 5 TO 7")
    for count in range(5, 8):
        print(f"    {count}  {count:0{WIDTH}b}")
    print(f"    =  {latched(5, 7)[0]:0{WIDTH}b}")
    print()

    # 5, 6 and 7 are 101, 110, 111. They agree on the 4 and disagree below it.
    assert latched(5, 7)[0] == 4

    # A range of one count is that count.
    for count in (0, 12, MASK):
        assert latched(count, count)[0] == count
        assert latched(count, count)[1] == 0

    # A range that crosses zero-to-one latches nothing, because the lowest bit
    # flips inside it.
    assert latched(0, 1)[0] == 0

    # The whole register space latches nothing at all.
    assert latched(0, MASK)[0] == 0

    # The high nibble survives when only the low bits move.
    assert latched(0b1111_0000_0000_0000, 0b1111_0000_1111_1111)[0] == 0b1111_0000_0000_0000

    # The closed form and the loop agree on every range in the data.
    for low, high in RANGES:
        assert latched(low, high)[0] == latched_by_looping(low, high), (low, high)

    # ...and on a sweep of small ranges, which is where an off-by-one in the
    # shifting would show up.
    for low in range(0, 64):
        for high in range(low, min(low + 20, 64)):
            assert latched(low, high)[0] == latched_by_looping(low, high), (low, high)

    # The answer's low bits are exactly the ones the shifting cleared.
    for low, high in RANGES:
        value, shifts = latched(low, high)
        assert value & ((1 << shifts) - 1) == 0

    # The answer is never above the lower end, and never below zero.
    for low, high in RANGES:
        assert 0 <= latched(low, high)[0] <= low

    # The shared prefix and the number of shifts describe the same split.
    for low, high in RANGES:
        assert len(common_prefix(low, high)) == WIDTH - latched(low, high)[1]

    # A backwards or out-of-range pair is refused rather than looping forever.
    for bad_low, bad_high in ((7, 5), (-1, 5), (0, 1 << WIDTH)):
        try:
            latched(bad_low, bad_high)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_low}, {bad_high}")

    print("All checks passed.")
```

</details>
---

## Problem 5 — The Missing Ticket

**The brief.** A cloakroom issues tickets 0 to n. Every ticket but one comes
back. Find the missing number.

**The data.** Nine returns from ten tickets.

**Constraints.** A ticket returned twice, or one never issued, is refused — the
arithmetic would otherwise produce a confident number that means nothing.

**Answer.** Two right answers, and the interesting part is what separates them.

The **sum**: add 0 to n with the closed form, subtract what came back. One line —
and it builds a number as large as the whole range, which on a fixed-width
register can overflow.

The **fold**: XOR every returned ticket *and* every number from 0 to n together.
Each returned ticket cancels against its own position in the range, and what
survives had nothing to cancel against. Nothing ever grows.

**Python's integers do not overflow, so here both are safe and the sum is
simpler.** The fold is the answer that stays safe when the register is 32 bits
wide. Being able to say *which constraint* makes the difference is the thing
being drilled — "use XOR because it is clever" is not the answer.

**Signatures.** `check_returns(returned)`, `missing_by_folding(returned)`,
`missing_by_summing(returned)`, `fold_trail(returned)`.

**Watch for.** Bounding the range loop at `len(returned)` rather than
`len(returned) + 1` — it works whenever the missing ticket is not the last one.
The missing ticket can be either end. No returns at all means ticket 0 is
missing, which is a real case.

<details>
<summary>Worked answer — <code>problem-05-missing-ticket-solution.py</code></summary>

```python
"""problem-05-missing-ticket-solution.py - the one ticket that never came back.

A cloakroom issues tickets numbered 0 to n. At the end of the night every
ticket but one has been handed back. Find the missing number.

Two answers, and the second is better than the first for a reason worth saying
out loud rather than guessing at.

    the sum          add 0 to n with the closed form, subtract what came back.
                     One line, and it builds a number as large as the whole
                     range - which on a fixed-width register can overflow, in a
                     language that has fixed-width registers.

    the fold         XOR every returned ticket AND every number from 0 to n
                     together. Each number that came back cancels itself
                     against its own position in the range, and what survives
                     is the one that had nothing to cancel against.

Python's integers do not overflow, so here both are safe and the sum is simpler.
The fold is the answer that stays safe when the register is 32 bits wide, and
being able to say WHICH constraint makes the difference is the thing being
drilled. "Use XOR because it is clever" is not the answer.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Tickets 0 to 9 were issued. These came back.
RETURNED: tuple[int, ...] = (3, 0, 1, 9, 2, 5, 8, 7, 6)


# ---- Your task ----
def check_returns(returned: tuple[int, ...]) -> int:
    """Raise unless `returned` is a valid set of returns, and give the range.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The highest ticket issued - which is len(returned), because exactly one
        of 0 to n is missing and n of them came back.

    Raises:
        ValueError: If a ticket is outside 0 to n, or if the same ticket came
            back twice. Both would make the answer meaningless, and neither is
            detected by the arithmetic itself.
    """
    highest = len(returned)
    for ticket in returned:
        if not 0 <= ticket <= highest:
            raise ValueError(f"ticket {ticket} was never issued")
    if len(set(returned)) != len(returned):
        raise ValueError("the same ticket came back twice")
    return highest


def missing_by_folding(returned: tuple[int, ...]) -> int:
    """Return the missing ticket, by XOR.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The one number from 0 to n that did not come back.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    folded = 0
    for number in range(highest + 1):
        folded ^= number
    for ticket in returned:
        folded ^= ticket
    return folded


def missing_by_summing(returned: tuple[int, ...]) -> int:
    """Return the missing ticket, by arithmetic. Kept to be compared.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The same answer. The sum of 0 to n is n * (n + 1) // 2, and what is
        left after subtracting the returns is the missing ticket.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    return highest * (highest + 1) // 2 - sum(returned)


def fold_trail(returned: tuple[int, ...]) -> list[int]:
    """Return the running fold, range first then returns, for reading.

    Args:
        returned: The tickets handed back.

    Returns:
        The value after each XOR. The first half folds the whole range down to
        something, and the second half cancels it away ticket by ticket until
        only the missing one is left.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    trail: list[int] = []
    folded = 0
    for number in range(highest + 1):
        folded ^= number
        trail.append(folded)
    for ticket in returned:
        folded ^= ticket
        trail.append(folded)
    return trail


# ---- Self-check ----
if __name__ == "__main__":
    highest = check_returns(RETURNED)
    print(f"TICKETS 0 TO {highest} WERE ISSUED")
    print(f"    came back : {sorted(RETURNED)}")
    print(f"    missing   : {missing_by_folding(RETURNED)}")
    print()

    print("THE RUNNING FOLD")
    trail = fold_trail(RETURNED)
    print("    folding the range 0 to " + str(highest) + ":")
    print("      " + "  ".join(str(value) for value in trail[: highest + 1]))
    print("    then cancelling the returns:")
    print("      " + "  ".join(str(value) for value in trail[highest + 1 :]))
    print()

    # Ticket 4 never came back.
    assert missing_by_folding(RETURNED) == 4

    # The two methods agree here...
    assert missing_by_folding(RETURNED) == missing_by_summing(RETURNED)

    # ...and on every possible single omission from a range of 0 to 30, which
    # is the check that matters: an off-by-one in the range bound shows up on
    # exactly one of these and on none of a handful of hand-picked cases.
    for size in range(1, 31):
        for missing in range(size + 1):
            returns = tuple(number for number in range(size + 1) if number != missing)
            assert missing_by_folding(returns) == missing, (size, missing)
            assert missing_by_summing(returns) == missing, (size, missing)

    # Order does not matter to either method.
    assert missing_by_folding(tuple(reversed(RETURNED))) == 4

    # The smallest case: one ticket issued, none returned. The missing one is 0.
    assert missing_by_folding(()) == 0
    assert missing_by_summing(()) == 0

    # The missing ticket can be either end of the range, which is where a loop
    # bounded at `len(returned)` rather than `len(returned) + 1` goes wrong.
    assert missing_by_folding((1, 2, 3)) == 0
    assert missing_by_folding((0, 1, 2)) == 3

    # A ticket that was never issued, or one returned twice, is refused. The
    # arithmetic would otherwise produce a confident number that means nothing.
    for bad in ((0, 1, 99), (0, 1, 1), (0, -1, 2)):
        for function in (missing_by_folding, missing_by_summing):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__} for {bad}")

    print("All checks passed.")
```

</details>
---

## Problem 6 — The Paired Ribbon Swap

**The brief.** A ribbon cable was crimped with each **pair** of lines swapped —
0 with 1, 2 with 3, and so on. Put them back.

**The data.** Seven registers, including three the fault does not change at all.

**Constraints.** Sixteen bits, unsigned.

**Answer.** Two masks and two shifts, done at once:

```text
0x5555  0101...0101  keeps the even lines, shifted up one
0xAAAA  1010...1010  keeps the odd lines, shifted down one
                     OR the two together
```

A loop over pairs is correct and is the answer to write first. The masked version
does every pair at once in constant time regardless of register width — and it is
the same shape as Problem 3's folding reversal, which is not a coincidence and is
worth a sentence in the write-up.

**Signatures.** `uncrimp(value)`, `uncrimp_by_looping(value)`,
`crossed_pairs(value)`, `unharmed(value)`.

**Watch for.** The two masks the wrong way round, which produces a plausible
answer on symmetric data. Testing with all-zeroes or all-ones — the fault leaves
them **unchanged**, so they are the worst possible readings to test a ribbon
with, and `unharmed` exists to name them.

Two properties need no known-good answer and are worth more than any example:
swapping twice returns the original, and the swap never changes how many lines
are live.

<details>
<summary>Worked answer — <code>problem-06-paired-ribbon-swap-solution.py</code></summary>

```python
"""problem-06-paired-ribbon-swap-solution.py - a ribbon crimped in the wrong pairs.

A ribbon cable carries a 16-bit register. It was crimped with each PAIR of
lines swapped: line 0 and line 1 have changed places, and so have 2 and 3, and
so on all the way up. The register arrives with every adjacent pair the wrong
way round.

Put them back.

The whole answer is two masks and two shifts, done at once:

    take the even lines, shift them up one
    take the odd lines, shift them down one
    OR the two together

    0x5555 is 0101...0101, which keeps the even lines
    0xAAAA is 1010...1010, which keeps the odd lines

Doing it as a loop over pairs is correct and is the answer to write first. The
masked version is the answer to be able to explain: it does every pair at once,
in constant time regardless of the register width, and it is the same shape as
the folding reversal in Problem 3 - which is not a coincidence and is worth a
sentence.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1
EVEN_LINES = 0x5555      # 0101 0101 0101 0101
ODD_LINES = 0xAAAA       # 1010 1010 1010 1010

# ---- Given data ----
REGISTERS: tuple[int, ...] = (
    0b0000_0000_0000_0001,
    0b0000_0000_0000_0010,
    0b1010_1010_1010_1010,
    0b0101_0101_0101_0101,
    0b1100_1100_1100_1100,
    0b0000_0000_0000_0000,
    0b1111_1111_1111_1111,
)


# ---- Your task ----
def check_register(value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        value: The register as it arrived.

    Raises:
        ValueError: If the value is negative or too wide.
    """
    if not 0 <= value <= MASK:
        raise ValueError(f"{value} is not a {WIDTH}-bit register")


def uncrimp(value: int) -> int:
    """Return `value` with every adjacent pair of lines swapped back.

    Args:
        value: The register as it arrived through the ribbon.

    Returns:
        The register as it was sent.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    return (((value & EVEN_LINES) << 1) | ((value & ODD_LINES) >> 1)) & MASK


def uncrimp_by_looping(value: int) -> int:
    """The same swap, one pair at a time. For comparison.

    Args:
        value: The register as it arrived.

    Returns:
        The same answer, in WIDTH / 2 turns rather than in one expression. This
        is the version to write first and the one to check the masked version
        against.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    answer = 0
    for position in range(0, WIDTH, 2):
        low = value >> position & 1
        high = value >> (position + 1) & 1
        answer |= high << position
        answer |= low << (position + 1)
    return answer


def crossed_pairs(value: int) -> list[int]:
    """Return the pair positions where the two lines differ.

    Args:
        value: The register as it arrived.

    Returns:
        The lowest line number of each pair whose two lines carry different
        values - which are exactly the pairs the miscrimp actually changes.
        A pair carrying 00 or 11 comes through the wrong crimp unharmed, and
        those are the readings that hide the fault.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    differing = value ^ uncrimp(value)
    return [position for position in range(0, WIDTH, 2) if differing >> position & 3]


def unharmed(value: int) -> bool:
    """Say whether the miscrimp leaves a register unchanged.

    Args:
        value: The register.

    Returns:
        True when every pair carries the same value on both lines, so the swap
        makes no difference. These are the readings an electrician must not
        test with.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    return uncrimp(value) == value


# ---- Self-check ----
if __name__ == "__main__":
    print("REGISTERS THROUGH THE MISCRIMPED RIBBON")
    print("    as received        as sent            crossed pairs")
    for value in REGISTERS:
        pairs = crossed_pairs(value)
        shown = ", ".join(str(pair) for pair in pairs) if pairs else "(none)"
        print(f"    {value:0{WIDTH}b}   {uncrimp(value):0{WIDTH}b}   {shown}")
    print()

    print("THE TWO MASKS")
    print(f"    even lines  0x{EVEN_LINES:04X}  {EVEN_LINES:0{WIDTH}b}")
    print(f"    odd lines   0x{ODD_LINES:04X}  {ODD_LINES:0{WIDTH}b}")
    print(f"    together    0x{EVEN_LINES | ODD_LINES:04X}  {EVEN_LINES | ODD_LINES:0{WIDTH}b}")
    print()

    # The lowest line moves up one and back.
    assert uncrimp(0b01) == 0b10
    assert uncrimp(0b10) == 0b01

    # Alternating patterns invert completely, because every pair is crossed.
    assert uncrimp(0b1010_1010_1010_1010) == 0b0101_0101_0101_0101
    assert uncrimp(0b0101_0101_0101_0101) == 0b1010_1010_1010_1010

    # A pattern in pairs is unharmed, because both lines of each pair agree.
    assert uncrimp(0b1100_1100_1100_1100) == 0b1100_1100_1100_1100
    assert unharmed(0b1100_1100_1100_1100)

    # All zeroes and all ones are unharmed too, which is exactly why they are
    # the worst readings to test a ribbon with.
    assert unharmed(0) and unharmed(MASK)
    assert crossed_pairs(0) == [] and crossed_pairs(MASK) == []

    # The two masks are complements and together cover the whole register.
    assert EVEN_LINES & ODD_LINES == 0
    assert EVEN_LINES | ODD_LINES == MASK

    # The masked and looping versions agree on every register in the data...
    for value in REGISTERS:
        assert uncrimp(value) == uncrimp_by_looping(value)

    # ...and across a sweep of the whole range, which is where a mask written
    # the wrong way round would show up.
    for value in range(0, 1 << WIDTH, 97):
        assert uncrimp(value) == uncrimp_by_looping(value)

    # Swapping twice gives back the original, always. This property needs no
    # known-good answer, which makes it the strongest check available.
    for value in range(0, 1 << WIDTH, 89):
        assert uncrimp(uncrimp(value)) == value

    # The swap never changes how many lines are live - it moves them.
    for value in range(0, 1 << WIDTH, 89):
        assert bin(uncrimp(value)).count("1") == bin(value).count("1")

    # Every crossed pair really does differ across its two lines.
    for value in REGISTERS:
        for pair in crossed_pairs(value):
            assert (value >> pair & 1) != (value >> (pair + 1) & 1)

    # Out-of-range registers are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        for function in (uncrimp, uncrimp_by_looping, crossed_pairs):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the operation and what it does to a single bit column, before any code. |
| Reason about options | The obvious answer named first, then the bit answer, with the constraint that makes the second worth having — width, space, or the size of the range. |
| Assemble the solution | Masks named as constants rather than written inline; every width assumption stated; type hints throughout. |
| Measure it | A property that needs no known-good answer — reversing twice, swapping twice, agreeing with a slow version across a sweep — not six hand-picked examples. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement, in the register's own width rather than abstract n. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-14/homework/`, one file per
problem:

```
frame-writeups/c2-week-14/homework/
├── problem-1-triple-logged-fault.md
├── problem-2-lamp-distance.md
├── problem-3-reversed-loom.md
├── problem-4-common-prefix-range.md
├── problem-5-missing-ticket.md
└── problem-6-paired-ribbon-swap.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md) — and to Mock #3 on Friday.

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Triple-Logged Fault | 30 min | 15 min | 45 min |
| 2 — Lamp Distance | 20 min | 15 min | 35 min |
| 3 — Reversed Loom | 30 min | 15 min | 45 min |
| 4 — Common Prefix Range | 30 min | 15 min | 45 min |
| 5 — Missing Ticket | 15 min | 15 min | 30 min |
| 6 — Paired Ribbon Swap | 25 min | 15 min | 40 min |

About four hours. Problems 1 and 5 are the two that matter most for Mock #3, and
for the same reason: each has an answer that *nearly* works, and the mark is for
knowing which constraint rules it out.
