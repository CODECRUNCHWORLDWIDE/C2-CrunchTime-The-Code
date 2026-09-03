# Exercise 1 — The Relay Fold

> **Topic:** the XOR fold, and the three properties that make it work
> **Lecture:** [01 — Bit Manipulation Fundamentals and XOR](../lecture-notes/01-bit-manipulation-fundamentals-and-xor.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** it is the smallest problem where XOR is the whole answer, so there is nothing else to hide behind. It also gets the honest part out of the way early — the fold alone cannot tell "one unpaired code" from "three unpaired codes", so the contract needs a count as well, and noticing that is more useful than the trick itself.

## The Brief

A signal box logs a relay code every time a relay trips. Relays trip in pairs —
one going in, one going out — so a healthy log holds every code **twice**. This
log holds one code **once**.

Find it, in one pass and in constant space.

## Starter

`exercise-01-relay-fold-solution.py` sits beside this page with the log and the
self-checks.

```text
0x2B  0x14  0x2B  0x77  0x14  0x09  0x77
```

Fold it by hand before writing anything. Seven XORs, and watching the running
value come back to where it was when a pair completes is the clearest possible
demonstration of why this works.

## Requirements

1. `lone_relay(codes)` returns the unpaired code.
2. It raises `ValueError` when the log does not hold **exactly one** unpaired
   code — including the all-paired case, which folds to zero.
3. `fold_trail(codes)` returns the running fold after each code.
4. `lone_relay_by_counting(codes)` is the counter version, kept to be compared
   rather than used.
5. Order does not affect the answer.

## Constraints

- **Constant space.** A counter dictionary answers the same question in linear
  space, and the whole reason this problem gets asked is that constant space is
  possible. Name it, reject it, and say why.
- **Name the three properties.** `a ^ a == 0`, `a ^ 0 == a`, and that XOR is
  associative and commutative. All three are load-bearing: the first cancels the
  pairs, the second leaves the survivor alone, and the third is why the order the
  pairs arrived in does not matter.
- **The fold alone is not a proof.** A log with three unpaired codes also folds
  to something non-zero. The count check is part of the contract, not a nicety.
- **Zero can be the answer.** A solution that treats a non-zero fold as the
  success condition gets `(7, 7, 0)` wrong.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-01-relay-fold-solution.py
TRIP LOG AND THE RUNNING FOLD
    0x2B   running fold 0x2B
    0x14   running fold 0x3F
    0x2B   running fold 0x14
    0x77   running fold 0x63
    0x14   running fold 0x77
    0x09   running fold 0x7E
    0x77   running fold 0x09

    the lone relay: 0x09

All checks passed.
```

Read the running fold down the page. After `0x2B, 0x14, 0x2B` it is back to
`0x14` — the pair has cancelled and the value is exactly what it would have been
had those two codes never been logged. That is the cancellation happening in
front of you, and it is worth having seen once.

## Steps

1. Read the self-checks. They are the spec.
2. Fold the log by hand. Seven XORs.
3. Write the memo: the three properties, and the one sentence about what
   survives the fold.
4. Write the fold. It is three lines.
5. Add the count check, and check it fires on `(1, 2, 3)` — a log that folds
   non-zero and has no answer.
6. Write the counter version too, so the rejection in your write-up is informed.
7. Check `(7, 7, 0)`, then write the FRAME pass.

## The Solution

```python
"""exercise-01-relay-fold-solution.py - the one relay that tripped alone.

A signal box logs a relay code every time a relay trips. Relays trip in pairs -
one going in, one going out - so a healthy log holds every code twice. This log
holds one code once.

Find it, in one pass and in constant space.

XOR is the whole answer, and it works because of three properties worth naming
out loud rather than taking on trust:

    a ^ a == 0        a code cancels itself
    a ^ 0 == a        zero leaves a code alone
    order does not matter, because XOR is associative and commutative

Fold the whole log with XOR and every paired code cancels itself out, whatever
order the pairs arrived in. What survives is the code that had no partner.

A counter dictionary answers the same question and is the answer to name and
reject: it is linear space where this is constant, and the whole reason this
problem is asked is that constant space is possible.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Relay codes as logged, in the order they tripped.
TRIP_LOG: tuple[int, ...] = (0x2B, 0x14, 0x2B, 0x77, 0x14, 0x09, 0x77)


# ---- Your task ----
def lone_relay(codes: tuple[int, ...]) -> int:
    """Return the code that appears once when every other appears twice.

    Args:
        codes: The trip log, in any order.

    Returns:
        The unpaired code.

    Raises:
        ValueError: If the log does not hold exactly one unpaired code. The
            fold alone cannot tell that apart - a log with three unpaired codes
            also folds to something non-zero - so the count is checked as well,
            and that check is part of the contract rather than an extra.
    """
    folded = 0
    for code in codes:
        folded ^= code

    lone = [code for code in set(codes) if codes.count(code) % 2 == 1]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one unpaired code, found {len(lone)}")
    return folded


def fold_trail(codes: tuple[int, ...]) -> list[int]:
    """Return the running fold after each code, for reading.

    Args:
        codes: The trip log.

    Returns:
        One value per code: the XOR of everything up to and including it.
        Printing this is what makes the cancellation visible - the running
        value returns to a previous number the moment a pair completes.
    """
    trail: list[int] = []
    folded = 0
    for code in codes:
        folded ^= code
        trail.append(folded)
    return trail


def lone_relay_by_counting(codes: tuple[int, ...]) -> int:
    """The counter version, kept to be compared rather than used.

    Args:
        codes: The trip log.

    Returns:
        The same answer for linear space. This is the alternative to name and
        reject in the write-up, and it is worth writing once so the rejection
        is informed.

    Raises:
        ValueError: On the same logs as `lone_relay`.
    """
    counts: dict[int, int] = {}
    for code in codes:
        counts[code] = counts.get(code, 0) + 1
    lone = [code for code, count in counts.items() if count % 2 == 1]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one unpaired code, found {len(lone)}")
    return lone[0]


# ---- Self-check ----
if __name__ == "__main__":
    print("TRIP LOG AND THE RUNNING FOLD")
    for code, folded in zip(TRIP_LOG, fold_trail(TRIP_LOG)):
        print(f"    0x{code:02X}   running fold 0x{folded:02X}")
    print()

    print(f"    the lone relay: 0x{lone_relay(TRIP_LOG):02X}")
    print()

    # 0x09 is the code with no partner.
    assert lone_relay(TRIP_LOG) == 0x09

    # The two versions agree, and the write-up should say why one is preferred.
    assert lone_relay(TRIP_LOG) == lone_relay_by_counting(TRIP_LOG)

    # Order genuinely does not matter, which is what "commutative" buys.
    assert lone_relay(tuple(reversed(TRIP_LOG))) == 0x09
    assert lone_relay((0x09, 0x2B, 0x2B, 0x14, 0x14, 0x77, 0x77)) == 0x09

    # A log of one code is that code.
    assert lone_relay((5,)) == 5

    # Zero can be the lone code, which is the case a "fold to non-zero" test
    # would get wrong.
    assert lone_relay((7, 7, 0)) == 0

    # The running fold returns to a previous value when a pair completes: after
    # 0x2B, 0x14, 0x2B the fold is back to 0x14 alone.
    assert fold_trail((0x2B, 0x14, 0x2B))[-1] == 0x14

    # A log where every code is paired folds to zero and has no answer. So does
    # one with three unpaired codes, which folds to something non-zero and
    # would fool a solution that only checked the fold.
    for bad in ((1, 1, 2, 2), (1, 2, 3), ()):
        for function in (lone_relay, lone_relay_by_counting):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__} for {bad}")

    print("All checks passed.")
```

The count check makes the function `O(n²)` as written, because `count` scans the
log per distinct code. On a real log you would count once into a dict — which is
the linear space the fold was avoiding. That tension is real and worth a
paragraph: the fold is constant-space, and *verifying its precondition* is not.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-01-relay-fold-solution.py
```

No third-party packages, no arguments, no input. It prints the log with the
running fold, the lone relay, and then `All checks passed.`

## Common bugs to catch

- **Treating a non-zero fold as success.** Symptom: `(7, 7, 0)` returns nothing
  useful, and `(1, 2, 3)` returns a confident wrong answer.
- **Reaching for a counter.** Symptom: correct, linear space, and the one thing
  the problem forbids.
- **Assuming "unpaired" means "appears once".** On this page it does — but the
  check is on parity, and saying which you implemented matters.
- **Initialising the fold to the first code and looping from the second.**
  Symptom: correct, and one more special case than the `a ^ 0 == a` property
  needs. Start at zero.
- **Sorting the log first.** Symptom: correct, `O(n log n)`, and a sign the
  commutativity did not land.

## Acceptance checklist

- [ ] The lone relay is `0x09`.
- [ ] The answer is unchanged when the log is reversed or reordered.
- [ ] A one-code log returns that code.
- [ ] `(7, 7, 0)` returns `0`.
- [ ] All-paired, three-unpaired and empty logs all raise `ValueError`.
- [ ] The fold and the counter version agree.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Find the unpaired code when every other appears **three** times. The fold no
  longer works — three copies do not cancel — and saying why in one sentence is
  worth more than the code that replaces it. That is
  [Homework 1](../homework/README.md).
- Find **two** unpaired codes. It is the mini-project's first half, and the step
  that separates them is a genuinely good trick.
- Report which position in the log the lone relay was at, not just its code. The
  fold does not know, and working out what would have to change is the point.
