# Challenge 1 — Mock #3, the Timed Round

> Format: a recorded full-loop mock under near-real conditions · Time: a hard 45-minute clock, plus ~90 minutes of review and write-up · Difficulty: this is a mock, not a problem — the difficulty is the conditions · Why this one: it is the closest you have come to the real screen.

## The Brief

This is the keystone of Week 14. Mock #1 in Week 4 was your first time on camera;
Mock #2 in Week 9 raised the bar to a real unseen problem. Mock #3 raises it to
**near-real conditions**: video on, a hard 45-minute clock, and no peeking at
anything.

The full protocol lives in
[Lecture 3](../lecture-notes/03-the-mock-interview-protocol-mock-3-and-tries-review.md).
This page is the deliverable framing — how to run it, what to record, how to
review it, and how to write the trajectory comparison across all three mocks.

## Starter

The conditions are the starter, and they are not negotiable. They are listed in
full below.

If you are running solo and have nobody to set you an unseen problem, the
fallback is **the fault register pair**, and the worked answer on this page
solves it. Do not read it until your clock has stopped — reading it first does
not make the mock easier, it makes it pointless.

### The fallback problem — the fault register pair

A machine writes a 16-bit fault register every cycle. Maintenance wants the two
cycles whose registers disagree in the **most bit positions**, because that pair
brackets the widest change in machine state.

```text
cycle 0   1000000000000000
cycle 1   0000000000000001
cycle 2   0000111111111111
cycle 3   0001000000000000
```

Return the number of differing bits and the pair of cycles. Fewer than two
cycles returns `None`; a register that does not fit in 16 bits raises
`ValueError`; ties go to the earliest pair.

Note carefully what is being maximised: the **number of differing bits**, not
the value of the difference. In the data above, cycles 0 and 3 produce the
largest XOR *value* and disagree in only two bits, while cycles 0 and 2 disagree
in thirteen. Under a clock, a candidate who maximises the wrong one gets a
plausible pair and the wrong answer — and does not notice.

## Requirements

Immediately (5 minutes, while fresh): free-write raw observations into `mocks/mock-03/immediate-notes.md`. Do not grade.

Saturday (two passes):

1. **Pass 1 — 1.5×, whole recording, timestamp doc.** 10–15 timestamps of *patterns*, not every filler word. Save as `mocks/mock-03/timestamps.md`.
2. **Pass 2 — 1.0×, flagged segments only.** For each, write *what happened* + *what to do differently*.

Then the self-feedback write-up at `frame-writeups/c2-week-14/mock-03-self-feedback.md`.

---

### The self-feedback structure

```markdown
# Mock #3 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name, and where it came from]
**Flavor:** A (peer) / B (platform) / C (solo)
**Duration:** 45 minutes
**Outcome:** [solved / solved with bug / didn't finish]

## What I felt during the mock
[3–5 honest sentences.]

## What the recording shows
[5–8 observations, each with a wall-clock timestamp from pass 2.]

## The Research-constraints memo — graded
[Under 30 seconds? Named the sub-shape, the bound, one rejected alternative?]

## The thinking-aloud — graded
[Did I go silent? When? Did I narrate pauses?]

## The recovery moves — graded
[When the first approach hit a wall, did I narrate the recovery audibly?]

## The Examine (cost) section — graded
[Did I state time + space + a trade-off + one variant, unprompted?]

## Trajectory across Mock #1 → #2 → #3
[The new section. Pull the one behavior change you named after Mock #1 and
after Mock #2. Did you actually make them? Is the Mock #1 weakness gone,
improving, or still present? 3–4 sentences. This is the self-correction
record a senior engineer reads.]

## ONE behavior change for Mock #4
[One sentence. Specific. Testable.]

## What I'm not going to change
[One or two things you noticed but are deliberately not over-correcting.]
```

---

### Rubric

Total possible: 100; passing: 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Conditions held | 15 | Video on, hard 45-min clock honored, no peeking — verifiable from the recording |
| Research-constraints memo delivered | 20 | Under 30 seconds; sub-shape named; complexity stated; one alternative rejected |
| Thinking-aloud | 15 | No silent stretch over 20 seconds; pauses narrated |
| Recovery audible | 10 | At least one course-correction narrated out loud (if one occurred) |
| Examine (cost) unprompted | 15 | Time + space + trade-off + one variant, stated without being asked |
| Two-pass review done | 10 | Pass 1 timestamps + pass 2 prescriptions both present |
| Trajectory section | 15 | Honest comparison across all three mocks; prior behavior changes assessed |

A passing mock is one you ran under the real conditions and *watched honestly* — not one where you solved the problem. A solved problem with a skipped Examine (cost) and no trajectory section fails; an unfinished problem with a clean Research-constraints memo, an audible recovery, and an honest trajectory passes.

---

## Constraints

The conditions of the round itself, which are the real constraints here:

- **Video on.** Screen + face + audio, all three tracks. The face track is required by Mock #3, not optional.
- **Hard 45-minute clock.** When the timer hits zero, you stop mid-line. No extensions, no "let me just finish this function."
- **No peeking.** No practice site open. No notes. No re-reading the lectures. No glancing at the trie template. If you cannot recall the binary-trie shape from memory, narrate the gap and code what you remember — the gap is *data*.
- **An unseen problem.** Pick a Medium you have not solved. The pattern should be in the bit / trie family or a mix, but it does not have to be — Mock #3 tests recognition across the whole catalog under pressure.

---

And for the fallback problem:

- **Registers are 16 bits, unsigned.** Anything outside that is refused.
- **Ties go to the earliest pair**, so the answer is one pair rather than a
  family of them.
- Say the brute-force answer out loud first — every pair — and then say what it
  would cost at a million cycles. Naming the bound you are accepting is worth
  more under a clock than reaching for something clever and not finishing.

## Expected output

Real stdout from the fallback problem's worked answer, captured on CPython 3.13.2:

```text
$ python challenge-01-mock-3-timed-round.py
fault registers
    cycle 0  1000000000000000
    cycle 1  0000000000000001
    cycle 2  0000111111111111
    cycle 3  0001000000000000

    widest: cycles 0 and 2, disagreeing in 13 of 16 bits
            1000000000000000
            0000111111111111
        xor 1000111111111111

All checks passed.
```

The XOR line is the exhibit. Thirteen of sixteen positions differ, and you can
count them on the page — which is the kind of check worth doing out loud in the
last five minutes of a round, when you no longer trust your own arithmetic.

## Steps

### How to pick the problem

**If running for real (recommended):** pick a *different* unseen medium problem than the fallback below. Use a peer (Flavour A) who selects a problem you have not seen, or a peer mock-interview service (Flavour B) that selects for you, or — last resort — a random bit-flavoured or trie-flavoured medium problem, from anywhere, that you have not opened. The point of a mock is the *unseen* problem; reading the fallback below disqualifies it for your real attempt.

**If you have no other option (solo, no platform, need a problem now):** use the fallback below — but only if you have not already studied it this week. Note that the pairing register is Exercise 3, so if you have done the exercise, this fallback is *not* unseen for you and you must pick something else.

---

### During the round — the 45-minute allocation

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| 0:00 – 0:03 | 3 min | **F.** Read aloud. Restate. One or two clarifying questions. Walk an example. |
| 0:03 – 0:05 | 2 min | **R.** Name the limits and the pattern. The 30-second memo. |
| 0:05 – 0:10 | 5 min | **A.** Sketch the approach, data structures, complexity target. |
| 0:10 – 0:25 | 15 min | **M.** Write the code. Narrate each line. Narrate the pauses. |
| 0:25 – 0:35 | 10 min | **E · verify.** Trace at least two examples. Find at least one bug. |
| 0:35 – 0:43 | 8 min | **E · cost.** Time and space. Trade-offs. One variant. |
| 0:43 – 0:45 | 2 min | Wrap-up. Summarize. Thank the interviewer. |

Guidelines, not rules — but the structure is the discipline. Bank saved Research constraints time in Examine (verify).

---

## The Solution

```python
"""challenge-01-mock-3-timed-round-solution.py - the fallback problem, worked.

Mock #3 is a timed round, not a problem. This file is the FALLBACK the page
offers for solo mode: something genuinely unseen to work under the clock, and
the reference answer to read only afterwards.

The fault register pair. A machine writes a 16-bit fault register every cycle.
Maintenance wants the two cycles whose registers disagree in the MOST bit
positions, because that pair brackets the widest change in machine state and is
where the fault is worth looking for.

Note what is being maximised: the NUMBER of differing bits, not the value of
the difference. Those are different questions and they have different answers -
0b1000 and 0b0000 differ by 8 in value and by one bit; 0b0111 and 0b0000 differ
by 7 in value and by three bits. A candidate who maximises the XOR value has
answered a different question, and under a clock they will not notice.

  bit_spread     - the widest disagreement, and the pair that produces it
  spread_report  - the pair, with the registers drawn in binary

The obvious answer is every pair, which is fine at this size and is the one to
say out loud first. The write-up is expected to name what it would cost at a
million cycles and what it would reach for then.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# One fault register per cycle, in cycle order.
# Chosen so that the two questions have DIFFERENT answers: cycles 0 and 3
# produce the largest XOR value and disagree in only two bits, while cycles 0
# and 2 disagree in thirteen. A candidate maximising the wrong one gets a
# plausible pair and the wrong answer.
REGISTERS: tuple[int, ...] = (
    0b1000_0000_0000_0000,
    0b0000_0000_0000_0001,
    0b0000_1111_1111_1111,
    0b0001_0000_0000_0000,
)


def differing_bits(left: int, right: int) -> int:
    """How many bit positions the two registers disagree in.

    XOR marks every disagreeing position with a 1, so the answer is how many
    1 bits the XOR has. int.bit_count does that in one call; the loop it
    replaces is the thing worth being able to write from memory.

    Args:
        left: One register.
        right: The other.

    Returns:
        A count between 0 and WIDTH.
    """
    return (left ^ right).bit_count()


def bit_spread(registers: tuple[int, ...]) -> tuple[int, tuple[int, int]] | None:
    """The pair of cycles disagreeing in the most bit positions.

    Args:
        registers: One register per cycle, in cycle order.

    Returns:
        (bits, (earlier cycle, later cycle)), or None when there are fewer than
        two cycles to compare. Ties are settled by the earlier first cycle, then
        the earlier second - so the answer is one pair rather than a family.

    Raises:
        ValueError: If a register does not fit in WIDTH bits.
    """
    for index, value in enumerate(registers):
        if not 0 <= value < (1 << WIDTH):
            raise ValueError(f"cycle {index} holds {value}, which is not a {WIDTH}-bit register")

    if len(registers) < 2:
        return None

    best_bits = -1
    best_pair = (0, 0)
    for i in range(len(registers)):
        for j in range(i + 1, len(registers)):
            bits = differing_bits(registers[i], registers[j])
            # Strictly greater, so the first pair found at a given width wins.
            # Cycles are visited in order, so that is the earliest pair.
            if bits > best_bits:
                best_bits, best_pair = bits, (i, j)
    return best_bits, best_pair


def spread_report(registers: tuple[int, ...]) -> None:
    """Print every register, then the widest-disagreeing pair."""
    for index, value in enumerate(registers):
        print(f"    cycle {index}  {value:0{WIDTH}b}")
    found = bit_spread(registers)
    if found is None:
        print("    not enough cycles to compare")
        return
    bits, (i, j) = found
    print()
    print(f"    widest: cycles {i} and {j}, disagreeing in {bits} of {WIDTH} bits")
    print(f"            {registers[i]:0{WIDTH}b}")
    print(f"            {registers[j]:0{WIDTH}b}")
    print(f"        xor {registers[i] ^ registers[j]:0{WIDTH}b}")


# ---- Self-check ----
if __name__ == "__main__":
    print("fault registers")
    spread_report(REGISTERS)

    bits, pair = bit_spread(REGISTERS)

    # The reported count must be the count for the reported pair, and no pair
    # may beat it. Those two assertions together are the definition.
    assert differing_bits(REGISTERS[pair[0]], REGISTERS[pair[1]]) == bits
    for i in range(len(REGISTERS)):
        for j in range(i + 1, len(REGISTERS)):
            assert differing_bits(REGISTERS[i], REGISTERS[j]) <= bits

    # The trap this problem is built around: maximising the XOR VALUE picks a
    # different pair from maximising the number of differing BITS.
    spread = [(differing_bits(REGISTERS[i], REGISTERS[j]), REGISTERS[i] ^ REGISTERS[j], (i, j))
              for i in range(len(REGISTERS)) for j in range(i + 1, len(REGISTERS))]
    by_bits = max(spread, key=lambda row: (row[0], -row[2][0], -row[2][1]))
    by_value = max(spread, key=lambda row: row[1])
    assert by_bits[2] != by_value[2], "the data must distinguish the two questions"

    # Small and degenerate cases.
    assert bit_spread(()) is None
    assert bit_spread((5,)) is None
    assert bit_spread((0, 0)) == (0, (0, 1))
    assert bit_spread((0, 0xFFFF)) == (16, (0, 1))

    # The tie-break: two pairs at the same width, earliest wins.
    assert bit_spread((0b0001, 0b0010, 0b0100))[1] == (0, 1)

    # Registers are checked rather than silently truncated.
    for bad in ((1 << WIDTH,), (-1,)):
        try:
            bit_spread(bad + (0,))
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print()
    print("All checks passed.")
```

Every pair, compared. That is `O(n²)` and it is the right first answer for four
cycles; the write-up is expected to say what it would reach for at a million.

The two assertions that matter are together near the top: the reported count is
the count for the reported pair, **and** no pair beats it. Either alone passes
for a solution that is wrong in a way that looks right.

## Run it

Download the worked answer beside this page and run it:

```bash
python challenge-01-mock-3-timed-round.py
```

No third-party packages, no arguments, no input. It prints the registers, the
widest-disagreeing pair, and then `All checks passed.`

Again: after the clock stops.

## Common bugs to catch

- **Maximising the XOR value.** Symptom: a plausible pair, and the wrong one.
  The question asks how many positions differ, not how large the difference is.
- **Counting bits with a string.** Symptom: it works, and it says you did not
  know `int.bit_count()` or the loop it replaces. Either is fine; not knowing
  either is what the exercise is for.
- **Comparing a cycle with itself.** Symptom: a reported width of 0 on a pair
  that is not a pair. The inner loop starts at `i + 1`.
- **Returning the registers instead of the cycle numbers.** Symptom: two
  identical-looking registers and no way to find them in the log.
- **No answer for fewer than two cycles.** Symptom: an exception where `None`
  is the honest answer.
- **Stopping the clock to fix a bug.** Symptom: a mock that measures something
  other than what the real screen measures.

## Acceptance checklist

Challenge 1 is complete when, under `mocks/mock-03/` and `frame-writeups/c2-week-14/`:

- The recording link is committed (the video file is too big to commit; commit the link).
- The immediate notes, pass-1 timestamps, and self-feedback write-up are all present.
- The self-feedback includes the trajectory section and names one behavior change for Mock #4.

Then move to [Challenge 2 — the ledger adder](./challenge-02-ledger-adder.md).

## Stretch

- Do the fallback problem again in `O(n · WIDTH)` using a trie over the bit
  patterns, and say honestly whether you would have reached it under the clock.
- Report the widest pair **per bit position** — which position disagrees most
  often across all pairs. It is a different question and a one-line change.
- Re-run Mock #1's problem under Mock #3's conditions and compare the two
  recordings. The trajectory is the artifact, not either round.

## The one-behavior-change rule (still binding)

Pick exactly **one** change for Mock #4. Specific. Testable. "I will state the complexity bound out loud before the interviewer asks" is good. "I will be more confident" is not. Over three mocks, three deliberate changes compound; ten attempted at once compound to zero.

---
