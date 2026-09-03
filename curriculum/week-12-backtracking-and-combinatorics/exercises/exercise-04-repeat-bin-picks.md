# Exercise 4 — The Repeat Bin Picks

> **Topic:** deduplication, and the difference between skipping a repeat *here* and skipping it everywhere
> **Lecture:** [02 — Pruning, Deduplication and String Partitioning](../lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** the fix is two lines and the plausible wrong version of it returns *exactly as many answers as the right one* on this data. That is the nastiest failure in the week, and it is much better met here than in a mock.

## The Brief

A clay store keeps a bin of body samples. Some samples in the bin are
**identical** — two bags of the same stoneware are the same stoneware, and a
test using one is the same test as a test using the other.

List every **distinct** set of samples that could be taken from the bin.

[Exercise 1](./exercise-01-glaze-sample-set.md) walked a shelf of distinct
glazes and every subset came out once. A bin with repeats breaks that: the walk
finds one set per **position**, and two positions holding the same sample
produce the same set twice.

## Starter

`exercise-04-repeat-bin-picks-solution.py` sits beside this page with the bin
and the self-checks.

```text
stoneware   porcelain   stoneware   raku   porcelain
```

Two stoneware, two porcelain, one raku. Work out how many **distinct** picks
exist before writing anything — it is not `2 ** 5`, and the formula is short
enough to derive in a minute.

## Requirements

1. `distinct_picks(samples)` returns every distinct subset, each sorted, empty
   set first.
2. `picks_with_duplicates(samples)` is the walk with no skip at all — shipped to
   be compared.
3. `picks_over_skipped(samples)` is the walk that skips a repeat **everywhere** —
   the plausible wrong fix, also shipped.
4. `pick_count(samples)` returns the count without enumerating.
5. The order the bin arrives in makes no difference to the answer.

## Constraints

- **Sort the bin first.** Identical samples have to sit next to each other before
  any skip rule can see them.
- **Skip a repeat only when it is a sibling at this level.** The test is
  `next_index > index and bin[next_index] == bin[next_index - 1]`. The
  `next_index > index` half is what confines it to this level, and dropping it is
  the wrong fix this page exists to show.
- **A pick that genuinely uses a sample twice must survive.** Two stoneware bags
  means the pick holding both is real, and the over-skipping version loses it.
- **`pick_count` is derived, not enumerated.** For each distinct sample the bin
  holds `k` of, a pick may take 0 to `k` of them, so the answer is the product of
  `k + 1`. That formula is the check.
- **Order-independence is a requirement**, not an accident. The same bin
  shuffled gives the same answer.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-04-repeat-bin-picks-solution.py
BIN  ['stoneware', 'porcelain', 'stoneware', 'raku', 'porcelain']

EVERY DISTINCT PICK
    0  (none)
    1  porcelain
    2  porcelain, porcelain
    3  porcelain, porcelain, raku
    4  porcelain, porcelain, raku, stoneware
    5  porcelain, porcelain, raku, stoneware, stoneware
    3  porcelain, porcelain, stoneware
    4  porcelain, porcelain, stoneware, stoneware
    2  porcelain, raku
    3  porcelain, raku, stoneware
    4  porcelain, raku, stoneware, stoneware
    2  porcelain, stoneware
    3  porcelain, stoneware, stoneware
    1  raku
    2  raku, stoneware
    3  raku, stoneware, stoneware
    1  stoneware
    2  stoneware, stoneware

THE THREE WALKS
    distinct picks        : 18   (the answer)
    no skip at all        : 32   (one per set of positions)
    skipping repeats always: 18   (same count, wrong picks)
      ...of which distinct  : 8

All checks passed.
```

Read the three-walk block carefully, because it is the whole page.

The correct walk finds **18** picks — `3 × 3 × 2`, one factor per distinct
sample.

The walk with **no skip** finds **32**, which is `2 ** 5`. It has found one pick
per set of positions, and the duplicates are visible.

The walk that **skips a repeat everywhere** finds **18 as well** — the same
number as the right answer — and only **8** of them are distinct. It never picks
both stoneware bags, and it pads the count back out with picks it has already
found.

A test that counted the answers would pass it. That is why the file asserts on
the *distinct* count and on the presence of `["stoneware", "stoneware"]`, and not
on the length.

## Steps

1. Read the self-checks. They are the spec.
2. Derive the count: `3 × 3 × 2 = 18`. Have it before you have an implementation.
3. Write the walk with no skip and confirm 32 picks with duplicates among them.
4. Add the sort and the skip. Get 18 distinct.
5. Now write the over-skipping version deliberately and run all three. Compare
   the counts — and then compare the *distinct* counts, which is where it falls
   over.
6. Confirm `["stoneware", "stoneware"]` is in the right answer and absent from
   the over-skipped one.
7. Shuffle the bin and confirm the answer does not move. Then write FRAME.

## The Solution

```python
"""exercise-04-repeat-bin-picks-solution.py - picking from a bin with repeats in it.

A clay store keeps a bin of body samples. Some samples in the bin are
identical - two bags of the same stoneware are the same stoneware, and a test
using one is the same test as a test using the other.

List every DISTINCT set of samples that could be taken from the bin.

Exercise 1 walked a shelf of distinct glazes and every subset came out once. A
bin with repeats in it breaks that: the walk finds one set per POSITION, and
two positions holding the same sample produce the same set twice.

The fix is two lines and both are needed:

    sort the bin        so identical samples sit next to each other
    skip a repeat       at the same level of the walk only

The second half of that second line is the part people get wrong. Skipping a
repeat everywhere removes sets that genuinely use the sample twice; skipping it
only when it is a SIBLING of a choice already made at this level removes
exactly the duplicates and nothing else.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Two bags of stoneware, two of porcelain, one of raku.
BIN: tuple[str, ...] = ("stoneware", "porcelain", "stoneware", "raku", "porcelain")


# ---- Your task ----
def distinct_picks(samples: tuple[str, ...]) -> list[list[str]]:
    """Return every distinct set of samples that could be taken from the bin.

    Args:
        samples: The bin, which may hold the same sample more than once.

    Returns:
        Every distinct subset, each sorted, with the empty set first. Two picks
        are the same when they hold the same samples the same number of times,
        however the bin was ordered.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            # Skip a repeat only when it is a sibling of a choice already made
            # at THIS level. `next_index > index` is what makes it "at this
            # level"; without it, a pick using the sample twice disappears too.
            if next_index > index and bin_order[next_index] == bin_order[next_index - 1]:
                continue
            trail.append(bin_order[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found


def picks_with_duplicates(samples: tuple[str, ...]) -> list[list[str]]:
    """The same walk without the skip, shipped to be compared.

    Args:
        samples: The bin.

    Returns:
        One pick per set of positions rather than per set of samples, so
        identical picks appear more than once. Its length is 2 to the power of
        the bin size, whatever the bin holds.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            trail.append(bin_order[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found


def picks_over_skipped(samples: tuple[str, ...]) -> list[list[str]]:
    """The walk that skips a repeat everywhere, shipped to be compared.

    Args:
        samples: The bin.

    Returns:
        Its answer, which is missing every pick that uses a repeated sample
        more than once - so a bin of two stoneware bags never produces the pick
        holding both - and which pads the count back out with duplicates. On
        the shipped bin it returns exactly as many picks as the correct walk
        does, and they are not the same picks. This is the plausible wrong fix
        and it fails silently, which is why it is worth running once.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []
    seen_at_all: set[str] = set()

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            sample = bin_order[next_index]
            if sample in seen_at_all:
                continue
            seen_at_all.add(sample)
            trail.append(sample)
            walk(next_index + 1)
            trail.pop()
            seen_at_all.discard(sample)

    walk(0)
    return found


def pick_count(samples: tuple[str, ...]) -> int:
    """Return how many distinct picks exist, without enumerating them.

    For each distinct sample the bin holds `k` of, a pick may take 0 to `k` of
    them, so the answer is the product of `k + 1` over the distinct samples.

    Args:
        samples: The bin.

    Returns:
        The number of distinct picks. Kept beside the enumeration so the two
        can check each other - which is the only cheap test of a walk whose
        whole job is not to repeat itself.
    """
    counts: dict[str, int] = {}
    for sample in samples:
        counts[sample] = counts.get(sample, 0) + 1
    total = 1
    for count in counts.values():
        total *= count + 1
    return total


# ---- Self-check ----
if __name__ == "__main__":
    print(f"BIN  {list(BIN)}")
    print()

    picks = distinct_picks(BIN)
    print("EVERY DISTINCT PICK")
    for pick in picks:
        shown = ", ".join(pick) if pick else "(none)"
        print(f"    {len(pick)}  {shown}")
    print()

    loose = picks_with_duplicates(BIN)
    over = picks_over_skipped(BIN)
    print("THE THREE WALKS")
    print(f"    distinct picks        : {len(picks)}   (the answer)")
    print(f"    no skip at all        : {len(loose)}   (one per set of positions)")
    print(f"    skipping repeats always: {len(over)}   (same count, wrong picks)")
    print(f"      ...of which distinct  : {len({tuple(pick) for pick in over})}")
    print()

    # Two stoneware, two porcelain, one raku: 3 * 3 * 2 = 18 distinct picks.
    assert len(picks) == pick_count(BIN) == 18

    # Every pick appears exactly once. That is the whole claim.
    assert len({tuple(pick) for pick in picks}) == len(picks)

    # The empty pick comes first.
    assert picks[0] == []

    # Picks that use a repeated sample twice must be present. This is what the
    # over-skipping version loses.
    assert ["stoneware", "stoneware"] in picks
    assert ["porcelain", "porcelain"] in picks

    # The unskipped walk finds 2 ** 5 = 32 picks, with repeats among them.
    assert len(loose) == 32
    assert len({tuple(pick) for pick in loose}) == len(picks)

    # The over-skipping walk is the nastiest of the three, because on this bin
    # it finds exactly as many picks as the right answer does - 18 - and they
    # are not the same 18. It never picks both stoneware bags, and it makes up
    # the numbers with duplicates of picks it has already found. A test that
    # only counted would pass it.
    assert len(over) == len(picks)
    assert ["stoneware", "stoneware"] not in over
    assert len({tuple(pick) for pick in over}) < len(picks)

    # A bin with no repeats behaves exactly like Exercise 1.
    assert len(distinct_picks(("a", "b", "c"))) == pick_count(("a", "b", "c")) == 8

    # A bin that is all one sample gives one pick per possible count, 0 to k.
    assert distinct_picks(("x", "x", "x")) == [[], ["x"], ["x", "x"], ["x", "x", "x"]]

    # An empty bin still has one pick: the empty one.
    assert distinct_picks(()) == [[]]

    # The order the bin arrives in makes no difference to the answer.
    shuffled = ("raku", "porcelain", "stoneware", "porcelain", "stoneware")
    assert distinct_picks(shuffled) == picks

    print("All checks passed.")
```

Both wrong walks are shipped and both are asserted against — the unskipped one
on its length, the over-skipped one on its *distinct* length and on a specific
missing pick. Two different assertions, because the two failures are different
and a single "is it 18" check catches neither.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-04-repeat-bin-picks-solution.py
```

No third-party packages, no arguments, no input. It prints every distinct pick,
the three walks side by side, and then `All checks passed.`

## Common bugs to catch

- **Skipping a repeat everywhere.** Symptom: the right *count* and the wrong
  picks. The headline failure of this page.
- **No sort.** Symptom: the skip rule never fires, because identical samples are
  not adjacent, and you get 32.
- **De-duplicating at the end with a set.** Symptom: the right answer, all the
  work, and an answer whose order depends on hashing. It also does not scale —
  the walk still visits every position.
- **Skipping on `next_index > 0` rather than `next_index > index`.** Symptom: the
  first branch at each level is wrong in a way that is very hard to see.
- **Comparing against the previous *choice* rather than the previous
  *position*.** Symptom: works on some bins, not others.
- **Asserting only on the length.** Symptom: a test that passes the over-skipped
  walk, which is the entire reason this page exists.

## Acceptance checklist

- [ ] 18 distinct picks, and `pick_count` agrees.
- [ ] Every pick appears exactly once; the empty pick is first.
- [ ] `["stoneware", "stoneware"]` and `["porcelain", "porcelain"]` are both present.
- [ ] The unskipped walk finds 32, whose distinct count is 18.
- [ ] The over-skipped walk finds 18 of which only 8 are distinct.
- [ ] A bin of three identical samples gives four picks.
- [ ] The same bin shuffled gives the same answer.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Apply the same rule to [Exercise 2](./exercise-02-firing-order.md): every
  distinct *order* of a bin with repeats. The skip rule is the same shape and it
  sits in a different place, and working out where is the exercise.
- Report the count without enumerating, for a bin of a hundred samples. The
  formula runs instantly; the walk does not.
- Take the counterweights from [Exercise 3](./exercise-03-clay-weigh-out.md), make
  them a bin with repeats and each usable **once**, and combine both rules. That
  is the composition a mock actually asks for.
