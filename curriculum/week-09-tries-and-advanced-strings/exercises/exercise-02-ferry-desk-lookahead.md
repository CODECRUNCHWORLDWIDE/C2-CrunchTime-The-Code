# Exercise 2 — The Ferry Desk Lookahead

> **Topic:** collecting everything under a prefix, and stopping early once you have enough
> **Lecture:** [01 — Trie Basics and Autocomplete](../lecture-notes/01-trie-basics-and-autocomplete.md)
> **Difficulty:** Easy-Medium
> **Target time:** 35 minutes
> **Why this one:** it is the first page where the *limit* is part of the algorithm rather than a slice at the end. Collecting everything and taking the first two is correct and does the whole walk; stopping when you have two is the version a kiosk can run on every keystroke.

## The Brief

A clerk types the first few letters of a destination code and the kiosk shows the
codes that start that way — in order, A to Z, at most `limit` of them.

Two things have to be right. The order has to come out of the walk rather than
out of a sort afterwards, and the walk has to **stop** once it has `limit` codes
in hand.

## Starter

`exercise-02-ferry-desk-lookahead-solution.py` sits beside this page with the
register and the self-checks.

```text
BRIDGEND  BRIDGEPORT  BRIDGEWATER  BRINE  BROADSANDS  BROADWAY  BURNTISLAND
```

The file reports how many **nodes** each lookahead touched, so the early stop is
a number you can read rather than a claim you have to trust.

## Requirements

1. `build_code_tree(codes)` returns the tree; duplicate codes are harmless.
2. `descend(root, prefix)` returns the node the prefix lands on, or `None` when
   the prefix leads nowhere.
3. `codes_with_prefix(root, prefix, limit)` returns the codes in order, at most
   `limit` of them, **and** the number of nodes visited.
4. A prefix nothing starts with returns an empty list, having visited no nodes.
5. An empty prefix means the whole register, still subject to the limit.

## Constraints

- **Order comes from the walk.** Visit a node's children in sorted key order and
  the results arrive sorted. Collecting into a list and sorting it is a different
  algorithm with a different cost, and it is the one to name and reject.
- **Stop at the limit, in the walk.** Not after it. This is the constraint the
  node counts exist to prove.
- **`descend` is separated out** because it is the half that is shared with every
  other prefix question. Writing it inline is how the next three pages end up with
  four copies of it.
- **A dead prefix costs nothing.** `BX` should visit zero nodes below the
  descent, not walk the tree looking.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-02-ferry-desk-lookahead-solution.py
BR       limit 3   nodes  16  ['BRIDGEND', 'BRIDGEPORT', 'BRIDGEWATER']
BR       limit 99  nodes  29  ['BRIDGEND', 'BRIDGEPORT', 'BRIDGEWATER', 'BRINE', 'BROADSANDS', 'BROADWAY']
BRIDGE   limit 2   nodes   7  ['BRIDGEND', 'BRIDGEPORT']
BU       limit 5   nodes  10  ['BURNTISLAND']
BX       limit 5   nodes   0  []
(empty)  limit 2   nodes  13  ['BRIDGEND', 'BRIDGEPORT']

All checks passed.
```

Read the two `BR` rows against each other. Limited to three it visits 16 nodes;
unlimited it visits **29** and returns all six. The cap did not filter the
results afterwards — it stopped the walk. And the empty prefix with a limit of 2 visits 13 — it walks into `BRIDGEND`
and `BRIDGEPORT` and then stops, rather than touching all 29 nodes of the
register.

That last row is the exercise in one line.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: descend to the prefix, then collect in sorted order with a
   limit.
3. Write `descend` first, on its own, and check `BX` returns `None`.
4. Write the collection walk. Sort the child keys at each node.
5. Add the limit **inside** the walk, and add the node counter at the same time —
   the counter is how you find out whether the limit is really working.
6. Check the empty-prefix and dead-prefix cases, then write the FRAME pass.

## The Solution

```python
"""exercise-02-ferry-desk-lookahead-solution.py — the ferry desk lookahead.

A clerk types the first few letters of a destination code and the kiosk shows
the codes that start that way, A to Z, at most `limit` of them.

The walk stops the moment `limit` codes are in hand, which is why the file
reports how many nodes each lookahead touched.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

DESTINATIONS: list[str] = [
    "BRIDGEND",
    "BRIDGEPORT",
    "BRIDGEWATER",
    "BRINE",
    "BROADSANDS",
    "BROADWAY",
    "BURNTISLAND",
]


def build_code_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every destination code.

    Args:
        codes: The codes to register. Duplicates are harmless.

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


def descend(root: CodeTree, prefix: str) -> CodeTree | None:
    """Return the node the prefix ends at, or None when it runs off the tree.

    Args:
        root: The root of the tree.
        prefix: The letters typed so far.

    Returns:
        The node reached, or None when some letter has no child.
    """
    node = root
    for letter in prefix:
        if letter not in node:
            return None
        node = node[letter]
    return node


def codes_with_prefix(root: CodeTree, prefix: str, limit: int) -> tuple[list[str], int]:
    """Return up to `limit` registered codes starting with `prefix`, A to Z.

    Args:
        root: The root of the tree.
        prefix: The letters typed so far. The empty prefix matches everything.
        limit: The most codes to return. Zero returns nothing at all.

    Returns:
        A pair: the codes found, and how many nodes the walk entered.
    """
    found: list[str] = []
    visited = 0
    start = descend(root, prefix)
    if start is None or limit <= 0:
        return found, visited

    def walk(node: CodeTree, spelled: str) -> None:
        nonlocal visited
        if len(found) == limit:
            return
        visited += 1
        if END in node:
            found.append(prefix + spelled)
            if len(found) == limit:
                return
        for letter in sorted(key for key in node if key != END):
            walk(node[letter], spelled + letter)
            if len(found) == limit:
                return

    walk(start, "")
    return found, visited


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_code_tree(DESTINATIONS)

    for prefix, limit in [("BR", 3), ("BR", 99), ("BRIDGE", 2), ("BU", 5), ("BX", 5), ("", 2)]:
        codes, visited = codes_with_prefix(tree, prefix, limit)
        shown = prefix if prefix else "(empty)"
        print(f"{shown:<8} limit {limit:<3} nodes {visited:>3}  {codes}")

    three, _ = codes_with_prefix(tree, "BR", 3)
    assert three == ["BRIDGEND", "BRIDGEPORT", "BRIDGEWATER"]

    everything, _ = codes_with_prefix(tree, "BR", 99)
    assert everything == [
        "BRIDGEND",
        "BRIDGEPORT",
        "BRIDGEWATER",
        "BRINE",
        "BROADSANDS",
        "BROADWAY",
    ]

    capped, capped_nodes = codes_with_prefix(tree, "BR", 2)
    _, full_nodes = codes_with_prefix(tree, "BR", 99)
    assert capped == ["BRIDGEND", "BRIDGEPORT"]
    assert capped_nodes < full_nodes  # the cap really did stop the walk early

    assert codes_with_prefix(tree, "BX", 5) == ([], 0)
    assert codes_with_prefix(tree, "BR", 0) == ([], 0)
    assert codes_with_prefix(tree, "BURNTISLAND", 5) == (["BURNTISLAND"], 1)

    root_first, _ = codes_with_prefix(tree, "", 2)
    assert root_first == ["BRIDGEND", "BRIDGEPORT"]

    print()
    print("All checks passed.")
```

The node count is returned rather than printed inside the walk, so the function
stays pure and the self-checks can assert on it. A claim about early stopping
that nothing asserts is a claim that stops being true the first time somebody
edits the walk.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-02-ferry-desk-lookahead-solution.py
```

No third-party packages, no arguments, no input. It prints each lookahead with
its node count and results, and then `All checks passed.`

## Common bugs to catch

- **Collecting everything, then slicing.** Symptom: correct results, and a node
  count that does not change when the limit does.
- **Sorting the results at the end.** Symptom: correct order, and a walk that had
  to finish before it could produce any of it.
- **Not sorting the child keys.** Symptom: order that depends on insertion, which
  will look right until the register is loaded in a different order.
- **Checking the limit only between children rather than inside the recursion.**
  Symptom: overshooting by up to one subtree.
- **A dead prefix walking the tree.** Symptom: `BX` visiting nodes. `descend`
  returns `None` and there is nothing to walk.
- **The empty prefix special-cased.** Symptom: extra code for a case the general
  walk already handles.

## Acceptance checklist

- [ ] `BR` with no effective limit returns six codes in alphabetical order.
- [ ] `BRIDGE` with a limit of 2 returns two codes and visits 7 nodes.
- [ ] The empty prefix with a limit of 2 visits 13 nodes, not the whole tree.
- [ ] `BX` returns an empty list and visits no nodes below the descent.
- [ ] `BU` returns exactly `BURNTISLAND` under a limit of 5.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report, per keystroke of a full code, how many nodes the lookahead visits. The
  curve falls fast, and that shape is why kiosks feel instant after two letters.
- Add a ranking — most-booked destination first rather than alphabetical — and
  say what has to change. Sorted-by-walk stops being free, and naming why is the
  point.
- Cache the descent between keystrokes: typing `B`, `BR`, `BRI` should not
  re-descend from the root each time. That is what a real kiosk does.
