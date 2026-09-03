# Challenge 2 — The Berth Ledger Shorthand

> Topic: the longest matching stem, not the first one · Lecture: [1](../lecture-notes/01-trie-basics-and-autocomplete.md) · Difficulty: Medium-Hard · Target time: 55 minutes including the FRAME write-up · Why this one: the walk is four lines and the trap is one of them. Stopping at the first stem you meet is the natural way to write it and the wrong answer, and it passes any test data where no stem is a prefix of another.

## The Brief

The harbourmaster's ledger is full of long berth names. The office keeps a list of
registered **stems**, and the house rule is that a berth name is written down as
the **longest** registered stem that opens it.

So with `QUAY` and `QUAYSIDE` both registered, `QUAYSIDEWEST` is filed as
`QUAYSIDE`, not as `QUAY`.

Rewrite a whole ledger line, and report how many names were shortened and which
names matched no stem at all.

## Starter

`challenge-02-berth-ledger-shorthand-solution.py` sits beside this page with the
stems, the ledger and the self-checks.

```text
stems    NORTH  QUAY  QUAYSIDE  DRY  DRYDOCK  LAY

ledger   NORTHGATE QUAYSIDEWEST DRYDOCKTWO LAYBY GRAINSILO QUAY
         DRY DRYDOCK DRYDOCKING
         PONTOON RAMP
```

Two pairs of stems nest — `QUAY` inside `QUAYSIDE`, `DRY` inside `DRYDOCK` — and
they are there for exactly one reason. A walk that returns the first stem it
meets gets `QUAY` and `DRY`, and it will look right on any register where no stem
opens another.

The second ledger line is the one to check by hand. `DRY` is itself a stem and
stays as it is; `DRYDOCK` is a stem and stays; `DRYDOCKING` shortens to
`DRYDOCK`. One shortening out of three names.

## Requirements

1. `build_stem_tree(stems)` returns a prefix tree over the stems.
2. `longest_stem(root, name)` returns the longest registered stem opening the
   name, or the name unchanged when none does.
3. `shorten(root, line)` returns the rewritten line, the number of names actually
   shortened, and the names that matched no stem.
4. A name **equal** to a stem is not counted as shortened — nothing changed.
5. Word order and spacing are preserved.

## Constraints

- **Longest, not first.** Walk to the end of the name, remembering the deepest
  stem end you passed, and return that. Returning early is the bug.
- **A name that matches no stem passes through unchanged** and is reported. It is
  not an error and it is not dropped.
- **An exact match is not a shortening.** `QUAY` in the ledger is already a stem;
  the count must not include it. This is the off-by-one the shipped data is built
  to catch — line one has five names that touch a stem and only **four**
  shortenings.
- **The walk stops when the tree runs out**, not when the name does. Once there is
  no child for the next letter, no longer stem can exist.
- **Unmatched names are reported in order**, so two runs agree.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-berth-ledger-shorthand-solution.py
in   NORTHGATE QUAYSIDEWEST DRYDOCKTWO LAYBY GRAINSILO QUAY
out  NORTH QUAYSIDE DRYDOCK LAY GRAINSILO QUAY
     shortened 4, unmatched ['GRAINSILO']

in   DRY DRYDOCK DRYDOCKING
out  DRY DRYDOCK DRYDOCK
     shortened 1, unmatched []

in   PONTOON RAMP
out  PONTOON RAMP
     shortened 0, unmatched ['PONTOON', 'RAMP']

All checks passed.
```

Line one is the whole challenge in one row. `QUAYSIDEWEST` becomes `QUAYSIDE`
rather than `QUAY`, `DRYDOCKTWO` becomes `DRYDOCK` rather than `DRY`, and the
count is **4** — not 5 — because the trailing `QUAY` was already a stem and
nothing about it changed.

Line three shortens nothing and reports both names as unmatched, which is a
perfectly good outcome and not a failure.

## Steps

1. Read the self-checks. They are the spec.
2. Do line two by hand. Three names, one shortening. If your answer is three
   shortenings you have the exact-match bug before you have written any code.
3. Write the memo: walk the name against the tree, remember the deepest stem end
   passed, stop when the tree runs out.
4. Write `longest_stem` and check it on `QUAYSIDEWEST` and `DRYDOCKING`.
5. Write `shorten` on top of it. Count a shortening only when the result differs
   from the input.
6. Collect the unmatched names in order.
7. Handle the empty line and a name shorter than every stem, then write the FRAME
   pass.

## The Solution

```python
"""challenge-02-berth-ledger-shorthand-solution.py — longest stem wins.

The harbourmaster's ledger is full of long berth names. The office keeps a
list of registered stems, and the house rule is that a berth name is written
down as the LONGEST registered stem that opens it.

So with QUAY and QUAYSIDE both registered, QUAYSIDEWEST is filed as QUAYSIDE,
not as QUAY. Stopping at the first stem you meet is the whole trap.

The line comes back rewritten, along with how many names were shortened and
which names matched no stem at all.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

StemTree = dict

STEMS: list[str] = [
    "NORTH",
    "QUAY",
    "QUAYSIDE",
    "DRY",
    "DRYDOCK",
    "LAY",
]

LEDGER: list[str] = [
    "NORTHGATE QUAYSIDEWEST DRYDOCKTWO LAYBY GRAINSILO QUAY",
    "DRY DRYDOCK DRYDOCKING",
    "PONTOON RAMP",
]


def build_stem_tree(stems: list[str]) -> StemTree:
    """Return a prefix tree holding every registered stem.

    Args:
        stems: The stems the office has registered. Duplicates are harmless.

    Returns:
        The root node.

    Raises:
        ValueError: If any stem is the empty string.
    """
    root: StemTree = {}
    for stem in stems:
        if not stem:
            raise ValueError("a stem cannot be the empty string")
        node = root
        for letter in stem:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def longest_stem(root: StemTree, name: str) -> str:
    """Return the longest registered stem that opens `name`, or "".

    Args:
        root: A tree of registered stems.
        name: The berth name to shorten.

    Returns:
        The longest prefix of `name` that is a registered stem. The empty
        string when no stem opens it.
    """
    node = root
    best = ""
    for cut, letter in enumerate(name, start=1):
        if letter not in node:
            break
        node = node[letter]
        if END in node:
            best = name[:cut]
    return best


def shorten(root: StemTree, line: str) -> tuple[str, int, list[str]]:
    """Rewrite one ledger line with every berth name cut back to its stem.

    Args:
        root: A tree of registered stems.
        line: One ledger line: berth names separated by single spaces.

    Returns:
        A triple. The rewritten line; how many names were actually made
        shorter; and the names no stem opened, first appearance first, with
        no repeats. A name that already equals its stem is neither shortened
        nor unmatched.

    Raises:
        ValueError: If `line` is empty.
    """
    if not line:
        raise ValueError("a ledger line cannot be empty")
    rewritten: list[str] = []
    shortened = 0
    unmatched: list[str] = []
    for name in line.split(" "):
        stem = longest_stem(root, name)
        if not stem:
            rewritten.append(name)
            if name not in unmatched:
                unmatched.append(name)
            continue
        rewritten.append(stem)
        if stem != name:
            shortened += 1
    return " ".join(rewritten), shortened, unmatched


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_stem_tree(STEMS)
    for line in LEDGER:
        rewritten, shortened, unmatched = shorten(tree, line)
        print(f"in   {line}")
        print(f"out  {rewritten}")
        print(f"     shortened {shortened}, unmatched {unmatched}")
        print()

    assert shorten(tree, LEDGER[0]) == (
        "NORTH QUAYSIDE DRYDOCK LAY GRAINSILO QUAY",
        4,
        ["GRAINSILO"],
    )
    assert shorten(tree, LEDGER[1]) == ("DRY DRYDOCK DRYDOCK", 1, [])
    assert shorten(tree, LEDGER[2]) == ("PONTOON RAMP", 0, ["PONTOON", "RAMP"])
    assert shorten(tree, "PONTOON PONTOON") == ("PONTOON PONTOON", 0, ["PONTOON"])
    assert longest_stem(tree, "QUAYSIDEWEST") == "QUAYSIDE"
    assert longest_stem(tree, "QUA") == ""
    assert longest_stem(tree, "SILO") == ""

    try:
        shorten(tree, "")
    except ValueError as problem:
        assert str(problem) == "a ledger line cannot be empty"
    else:
        raise AssertionError("an empty line should have been rejected")

    try:
        build_stem_tree(["NORTH", ""])
    except ValueError as problem:
        assert str(problem) == "a stem cannot be the empty string"
    else:
        raise AssertionError("an empty stem should have been rejected")

    print("All checks passed.")
```

The walk carries the best stem seen so far rather than returning at the first
one — one extra variable, and it is the difference between the right answer and a
plausible wrong one. That variable is what the whole write-up should be about.

## Download and run

Download the solution beside this page and run it:

```bash
python challenge-02-berth-ledger-shorthand-solution.py
```

No third-party packages, no arguments, no input. It prints each ledger line in
and out with its counts, and then `All checks passed.`

## Common bugs to catch

- **Returning the first stem found.** Symptom: `QUAYSIDEWEST` files as `QUAY`.
  The register above is built to expose it; a register without nested stems is
  not.
- **Counting an exact match as a shortening.** Symptom: line one reports 5 where
  4 is right.
- **Dropping unmatched names.** Symptom: a shorter line out than in. They pass
  through unchanged.
- **Walking past the end of the tree.** Symptom: an exception on
  `GRAINSILO`, which diverges at the first letter.
- **Rebuilding the line by joining on a single space unconditionally.** Symptom:
  spacing that differs from the input on a line with two spaces in it.
- **Reporting unmatched names from a set.** Symptom: an order that changes
  between runs, and a test that passes intermittently.

## Acceptance checklist

- [ ] `QUAYSIDEWEST` files as `QUAYSIDE`; `DRYDOCKTWO` files as `DRYDOCK`.
- [ ] Line one reports 4 shortenings and `['GRAINSILO']` unmatched.
- [ ] Line two reports 1 shortening and nothing unmatched.
- [ ] Line three reports 0 shortenings and both names unmatched.
- [ ] A name equal to a stem is unchanged and uncounted.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the **saving** — letters before against letters after — for the whole
  ledger. It is the number that justifies the shorthand existing.
- Add a stem and re-file only the names that could have changed, rather than the
  whole ledger. Working out which those are is a prefix question and the tree
  already answers it.
- Reverse the rule: file each name under the **shortest** stem that opens it, and
  say in one sentence what changes in the walk. It is one line, and knowing which
  line is the proof you understood this page.
