# Exercise 5 — The Stripped Manifest Line

> **Topic:** a tree and a memo working together — all the codes starting here, in one walk
> **Lecture:** [02 — the stripped manifest line and Aho-Corasick](../lecture-notes/02-word-break-and-aho-corasick.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** it is the composition the week is building towards. The tree answers "which codes start at this position" in one descent; the memo makes sure no position is ever solved twice. Either alone is not enough, and seeing why is the exercise.

## The Brief

A grain terminal's manifest lines arrive with the separators stripped out, so
`FISH MEAL CAKE` turns up as `FISHMEALCAKE`. Every piece is a registered cargo
code. Put the gaps back, **using as few pieces as possible**.

## Starter

`exercise-05-stripped-manifest-line-solution.py` sits beside this page with the
codes, the lines and the self-checks.

```text
codes   FISH  MEAL  FISHMEAL  MEALCAKE  CAKE  OIL  SEED  OILSEED

lines   FISHMEALCAKE  OILSEEDCAKE  FISHOIL  MEAL
        CAKEFISHMEALSEED  FISHMEALCAKEX  SEEDLING
```

The register is built to be ambiguous on purpose. `FISHMEALCAKE` splits as
`FISH MEAL CAKE`, as `FISHMEAL CAKE`, and as `FISH MEALCAKE` — three valid
answers, and the rule picks the shortest. Two pieces beats three.

## Requirements

1. `build_code_tree(codes)` returns the tree.
2. `split_line(root, line)` returns the fewest pieces that reconstruct the line,
   in order.
3. A line that cannot be split returns an empty list, not a partial split.
4. An empty line returns an empty list.
5. The same position is never solved twice.

## Constraints

- **Fewest pieces**, and the tie-break has to be stated. Two answers with the
  same number of pieces need a rule; the file has one and says what it is.
- **One descent per position.** Walking the tree from a position hands you every
  code starting there as you go. Testing each code separately against the line
  does the same job once per code.
- **The memo is not optional.** Without it, `CAKEFISHMEALSEED` re-solves the same
  suffixes repeatedly, and the cost stops being linear in the line length.
- **A failed split returns nothing**, not the pieces it managed. A partial answer
  reads as success and is worse than an empty list.
- **`SEEDLING` is unsplittable** even though it starts with `SEED`. Getting that
  right means the search must be able to fail after a good start.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-05-stripped-manifest-line-solution.py
FISHMEALCAKE      2  FISH MEALCAKE
OILSEEDCAKE       2  OILSEED CAKE
FISHOIL           2  FISH OIL
MEAL              1  MEAL
CAKEFISHMEALSEED  3  CAKE FISHMEAL SEED
FISHMEALCAKEX     0  (no split)
SEEDLING          0  (no split)

All checks passed.
```

`FISHMEALCAKE` comes back as **two** pieces, not three — `FISHMEAL CAKE`. That is
the "fewest" rule doing visible work, and it is the row to check first, because a
solution that takes the first valid split it finds gets three.

`FISHMEALCAKEX` and `SEEDLING` both return nothing. Both start promisingly and
both dead-end, which is exactly what they are in the data for.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: descend from a position, note every code end you pass, recurse
   on the remainder, keep the best.
3. Build the tree, then write the descent that yields every code starting at a
   given position. Check it by hand at position 0 of `FISHMEALCAKE` — it should
   yield `FISH` and `FISHMEAL`.
4. Write the recursion without the memo first, and get `FISHMEALCAKE` to come back
   as two pieces.
5. Add the memo. Then add a counter and confirm each position is solved once.
6. Handle the failing lines and the empty line, then write the FRAME pass.

## The Solution

```python
"""exercise-05-stripped-manifest-line-solution.py — putting the gaps back.

A grain terminal's manifest lines arrive with the separators stripped out, so
FISH MEAL CAKE turns up as FISHMEALCAKE. Every piece is a registered cargo
code. Put the gaps back, using as few pieces as possible.

A prefix tree reads all the codes that could start at one position in a single
walk, and a memo makes sure no position is ever solved twice.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

CARGO_CODES: list[str] = [
    "FISH",
    "MEAL",
    "FISHMEAL",
    "MEALCAKE",
    "CAKE",
    "OIL",
    "SEED",
    "OILSEED",
]

LINES: list[str] = [
    "FISHMEALCAKE",
    "OILSEEDCAKE",
    "FISHOIL",
    "MEAL",
    "CAKEFISHMEALSEED",
    "FISHMEALCAKEX",
    "SEEDLING",
]


def build_code_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every cargo code.

    Args:
        codes: The registered codes. Duplicates are harmless.

    Returns:
        The root node.
    """
    root: CodeTree = {}
    for code in codes:
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def split_line(root: CodeTree, line: str) -> list[str]:
    """Return the fewest-piece split of `line` into registered codes.

    Args:
        root: A tree of the registered codes.
        line: The run of letters to split. Must not be empty.

    Returns:
        The pieces, in order. Where two splits use the same number of pieces,
        the one that compares smaller piece by piece wins. An empty list means
        no split into registered codes exists.

    Raises:
        ValueError: If `line` is empty.
    """
    if not line:
        raise ValueError("a manifest line cannot be empty")

    best_from: dict[int, list[str] | None] = {}

    def best(start: int) -> list[str] | None:
        if start == len(line):
            return []
        if start in best_from:
            return best_from[start]
        winner: list[str] | None = None
        node = root
        for cut in range(start, len(line)):
            letter = line[cut]
            if letter not in node:
                break
            node = node[letter]
            if END not in node:
                continue
            rest = best(cut + 1)
            if rest is None:
                continue
            candidate = [line[start : cut + 1]] + rest
            if winner is None or (len(candidate), candidate) < (len(winner), winner):
                winner = candidate
        best_from[start] = winner
        return winner

    found = best(0)
    return found if found is not None else []


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_code_tree(CARGO_CODES)
    for line in LINES:
        pieces = split_line(tree, line)
        shown = " ".join(pieces) if pieces else "(no split)"
        print(f"{line:<17} {len(pieces)}  {shown}")

    assert split_line(tree, "FISHMEALCAKE") == ["FISH", "MEALCAKE"]
    assert split_line(tree, "OILSEEDCAKE") == ["OILSEED", "CAKE"]
    assert split_line(tree, "FISHOIL") == ["FISH", "OIL"]
    assert split_line(tree, "MEAL") == ["MEAL"]
    assert split_line(tree, "CAKEFISHMEALSEED") == ["CAKE", "FISHMEAL", "SEED"]
    assert split_line(tree, "FISHMEALCAKEX") == []
    assert split_line(tree, "SEEDLING") == []

    try:
        split_line(tree, "")
    except ValueError as problem:
        assert str(problem) == "a manifest line cannot be empty"
    else:
        raise AssertionError("an empty line should have been rejected")

    print()
    print("All checks passed.")
```

The memo is keyed on the position, not on the remaining string. Both work; the
position is a small integer and the string is a copy, and on a long manifest line
that difference is the whole memory profile.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-05-stripped-manifest-line-solution.py
```

No third-party packages, no arguments, no input. It prints each line with its
piece count and split, and then `All checks passed.`

## Common bugs to catch

- **Taking the first valid split.** Symptom: `FISHMEALCAKE` in three pieces. Valid
  is not the same as fewest.
- **No memo.** Symptom: correct answers and exponential time on a line with many
  ambiguous prefixes. It will not show up on these seven lines, which is why the
  constraint says it rather than the data.
- **Memoising on the remaining substring.** Symptom: correct, and a copy of the
  tail at every position.
- **Returning a partial split on failure.** Symptom: `SEEDLING` comes back as
  `['SEED']`, which reads as an answer.
- **Testing each code against the line separately.** Symptom: correct, and the
  tree doing nothing. The descent is the point.
- **Not handling the empty line.** Symptom: a recursion that never terminates, or
  one that returns `None` where `[]` is meant.

## Acceptance checklist

- [ ] `FISHMEALCAKE` splits into two pieces: `FISHMEAL CAKE`.
- [ ] `CAKEFISHMEALSEED` splits into three.
- [ ] `MEAL` splits into one.
- [ ] `FISHMEALCAKEX` and `SEEDLING` both return an empty list.
- [ ] The empty line returns an empty list.
- [ ] Every position is solved at most once.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return **every** minimal split rather than one, for a line that has more than
  one. The register above has such a line; find it.
- Report how many positions the memo saved on `CAKEFISHMEALSEED`. It is a small
  number here and the growth curve is the interesting part.
- Allow one unregistered piece anywhere in the line and report where it was. That
  is what a terminal would actually want, because the failing manifest is the one
  a human has to look at.
