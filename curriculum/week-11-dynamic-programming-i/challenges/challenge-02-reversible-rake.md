# Challenge 2 — The Reversible Rake

> Topic: interval DP, filled by span · Lecture: [3](../lecture-notes/03-state-space-reduction-and-recognition.md) · Difficulty: Medium-Hard · Target time: 70 minutes including the FRAME write-up · Why this one: it is the first table in the course that cannot be filled row by row, and finding that out by getting it wrong is the lesson.

## The Brief

A shunting yard makes up a **rake** of wagons from a standing line. Each wagon
carries a one-letter type code. A rake is **reversible** when its codes read the
same from either end, because the locomotive can then run round and push it back
without the load being redistributed.

Wagons may be detached from anywhere, but the ones that remain **keep their
order** — nothing is shunted past anything else.

The yard does not want a length. It wants the **wagons**, and it wants the list
of positions to detach, because that is the work a shunter actually does.

## Starter

The worked answer on this page carries the line and the self-checks.

```text
O X B V A N B X O
0 1 2 3 4 5 6 7 8
```

Find the longest reversible rake by hand before you start. Three pairs nest, and
one wagon sits in the middle. Knowing the answer is 7 before you code makes the
table easy to check and hard to fool yourself about.

## Requirements

1. `longest_rake(line)` returns the rake's type codes, in order.
2. `detach_list(line)` returns the positions to detach, **left to right** — the
   order a shunter walks the line — as zero-based indices into the original.
3. Ties are settled by keeping the **leftmost** wagon available, so the answer is
   one rake rather than a family of them.
4. `rake_report(...)` prints both for several lines.
5. The empty line returns an empty rake and an empty detach list, without a
   special case in the recurrence.

## Constraints

- **The table is filled by increasing span**, not row by row. An entry depends on
  strictly shorter spans; filling by row reads entries that have not been written
  yet, and the result looks *almost* right, which is worse than looking wrong.
- **A span of two is not a span of four with the middle removed.** When the ends
  match and there is nothing between them, the inner span is empty and worth 0 —
  guard it rather than indexing.
- **State the tie-break and then implement it.** A tie-break you promise in a
  docstring and do not implement is worse than none; the reader now trusts a
  claim that is false.
- **The rake must be a subsequence**, not a substring. Wagons keep their order;
  they do not have to be adjacent.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-reversible-rake.py
standing lines
    OXBVANBXO    rake OXBVBXO    detach [4, 5]
    BOX          rake B          detach [1, 2]
    AA           rake AA         detach []
    AB           rake A          detach [1]
    ABCBA        rake ABCBA      detach []
    (empty)      rake (none)     detach []
    XYZ          rake X          detach [1, 2]

    line OXBVANBXO -> rake OXBVBXO (7 wagons)

All checks passed.
```

`XYZ` reporting `X` rather than `Z` is the tie-break doing its job. All three
wagons are equally good as a rake of one; the contract says leftmost, so `X` it
is, and the detach list is `[1, 2]`.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the table's axes, and say why the fill order is by span.
3. Fill the diagonal — one wagon is trivially reversible — then the spans of two.
4. Fill the rest and check `OXBVANBXO` gives 7 before reconstructing anything.
5. Write the backward walk, keeping a front list and a back list. Reverse the
   back list at the end and say why that is needed.
6. Implement the tie-break, then verify it with `XYZ`.
7. Assert the rake reads the same both ways and is a subsequence — those two
   properties are the definition, so they are the tests worth having.
8. Write the FRAME pass.

## The Solution

```python
"""challenge-02-reversible-rake-solution.py - the longest rake that reads both ways.

A shunting yard makes up a rake of wagons from a standing line. Each wagon has a
one-letter type code. A rake is REVERSIBLE when its type codes read the same from
either end, because the locomotive can then run round and push it back without
the load being redistributed.

Wagons may be detached from anywhere in the line, but the ones that remain keep
their order - nothing is shunted past anything else. So the longest reversible
rake is the longest subsequence of the line that reads the same both ways.

The yard does not want a length. It wants the WAGONS, and it wants to know which
ones to detach, because that is the work.

  longest_rake     - the wagon codes of the longest reversible rake
  detach_list      - the positions to detach, in the order a shunter walks them
  rake_report      - both, for a few lines

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# One type code per wagon, from the buffer stop outwards.
STANDING_LINE = "OXBVANBXO"


# ---- Your task ----
def _table(line: str) -> list[list[int]]:
    """Longest reversible rake within line[lo..hi], for every lo and hi.

    Filled by increasing span length, because the answer for a span depends on
    strictly shorter spans and on nothing else. Filling row by row instead
    reads entries that have not been written yet - which is the bug that makes
    this table look almost right.

    Args:
        line: The standing line of type codes.

    Returns:
        A square table; entry [lo][hi] is the best length within that span.
    """
    size = len(line)
    best = [[0] * size for _ in range(size)]
    for lo in range(size):
        best[lo][lo] = 1  # one wagon reads the same either way

    for span in range(2, size + 1):
        for lo in range(size - span + 1):
            hi = lo + span - 1
            if line[lo] == line[hi]:
                # The two ends pair off. For a span of two that inner span is
                # empty, which is 0 - hence the guard rather than best[lo+1][hi-1].
                inner = best[lo + 1][hi - 1] if span > 2 else 0
                best[lo][hi] = inner + 2
            else:
                best[lo][hi] = max(best[lo + 1][hi], best[lo][hi - 1])
    return best


def longest_rake(line: str) -> str:
    """The type codes of the longest reversible rake.

    Args:
        line: The standing line of type codes.

    Returns:
        The rake's codes in order. Ties are settled by taking the leftmost
        wagon available at each step, so the answer is one rake rather than a
        family of them.
    """
    if not line:
        return ""

    best = _table(line)
    lo, hi = 0, len(line) - 1
    front: list[str] = []
    back: list[str] = []

    while lo <= hi:
        if lo == hi:
            front.append(line[lo])
            break
        if line[lo] == line[hi]:
            front.append(line[lo])
            back.append(line[hi])
            lo, hi = lo + 1, hi - 1
        elif best[lo + 1][hi] > best[lo][hi - 1]:
            # Strictly greater, so an equal pair falls through to the branch
            # below and the BACK wagon is dropped. That keeps the leftmost
            # wagon available, which is the tie-break the docstring promises -
            # and a tie-break you state but do not implement is worse than none.
            lo += 1
        else:
            hi -= 1

    back.reverse()
    return "".join(front + back)


def detach_list(line: str) -> list[int]:
    """Positions to detach, left to right, to leave the longest rake.

    Args:
        line: The standing line of type codes.

    Returns:
        Zero-based positions in the ORIGINAL line. Left to right is how a
        shunter walks the line, so it is the order the list is given in.
    """
    keep = longest_rake(line)
    detach: list[int] = []
    at = 0
    for position, code in enumerate(line):
        if at < len(keep) and code == keep[at]:
            at += 1
        else:
            detach.append(position)
    return detach


def rake_report(lines: list[str]) -> None:
    """Print the rake and the detach list for each standing line."""
    for line in lines:
        rake = longest_rake(line)
        detach = detach_list(line)
        shown = line or "(empty)"
        print(f"    {shown:<12} rake {rake or '(none)':<10} detach {detach}")


# ---- Self-check ----
if __name__ == "__main__":
    print("standing lines")
    rake_report([STANDING_LINE, "BOX", "AA", "AB", "ABCBA", "", "XYZ"])

    rake = longest_rake(STANDING_LINE)
    print()
    print(f"    line {STANDING_LINE} -> rake {rake} ({len(rake)} wagons)")

    # The rake must read the same both ways. That is the definition, so it is
    # the first thing asserted, for every case.
    for line in (STANDING_LINE, "BOX", "AA", "AB", "ABCBA", "", "XYZ", "AABAA"):
        got = longest_rake(line)
        assert got == got[::-1], (line, got)

    # It must be a subsequence of the line: same order, nothing shunted past.
    for line in (STANDING_LINE, "ABCBA", "XYZ", "AABAA"):
        got = longest_rake(line)
        at = 0
        for code in line:
            if at < len(got) and code == got[at]:
                at += 1
        assert at == len(got), (line, got)

    # And the detach list must be exactly the wagons not in the rake.
    for line in (STANDING_LINE, "ABCBA", "XYZ", "AABAA", "AA", ""):
        assert len(detach_list(line)) == len(line) - len(longest_rake(line))

    # Known answers.
    assert longest_rake("ABCBA") == "ABCBA"      # already reversible
    assert detach_list("ABCBA") == []
    assert longest_rake("AA") == "AA"
    assert longest_rake("") == ""
    assert detach_list("") == []

    # A line with no repeats leaves a single wagon, and the tie-break says which.
    assert longest_rake("XYZ") == "X"   # leftmost, per the tie-break
    assert detach_list("XYZ") == [1, 2]

    # The shipped line: OXBVANBXO. Three pairs nest - O..O, X..X, B..B - around
    # one wagon from the middle, so the best rake is 7 of the 9 wagons.
    assert len(longest_rake(STANDING_LINE)) == 7
    assert len(detach_list(STANDING_LINE)) == 2

    print()
    print("All checks passed.")
```

The reconstruction builds a front and a back and joins them, rather than
inserting into the middle of one list. Inserting at the middle is `O(n)` per
wagon and reads worse; two lists and a reverse is `O(n)` once.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-02-reversible-rake.py
```

No third-party packages, no arguments, no input. It prints the report for seven
lines and then `All checks passed.`

## Common bugs to catch

- **Filling row by row.** Symptom: correct on short lines, subtly low on longer
  ones. The entry you need has not been computed yet.
- **Indexing the inner span at length two.** Symptom: `IndexError`, or a rake two
  wagons too long. `best[lo+1][hi-1]` does not exist when `hi = lo + 1`.
- **Returning the length.** Symptom: a correct number and a yard that still does
  not know which wagons to detach.
- **A tie-break that contradicts the docstring.** Symptom: `XYZ` returns `Z`
  while the docs promise leftmost. Either change the comparison or change the
  promise — but they must agree.
- **Building the answer with `insert(0, …)`.** Symptom: correct, quadratic, and
  harder to read than the two-list version.
- **Testing only that the length is right.** Symptom: a "rake" that is not
  reversible and is not a subsequence. Assert both properties directly.

## Acceptance checklist

- [ ] `OXBVANBXO` returns a rake of 7 with a detach list of 2.
- [ ] `ABCBA` is already reversible: nothing detached.
- [ ] `XYZ` returns `X`, not `Z`.
- [ ] The empty line returns an empty rake and an empty detach list.
- [ ] Every rake reads the same both ways *and* is a subsequence of its line —
      asserted, not eyeballed.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report **how many** distinct longest rakes the line has. The count needs a
  second table and it is a good test of whether you understood the first.
- Allow one wagon to be turned rather than detached — a code that reads the same
  reversed — and say where that changes the recurrence.
- Solve it with memoised recursion instead of a table and compare the two on a
  60-wagon line. State which you would ship, and why the answer is not always the
  faster one.
