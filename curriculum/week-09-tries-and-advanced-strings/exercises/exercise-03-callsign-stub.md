# Exercise 3 — The Callsign Stub

> **Topic:** a count stored at every node, and the question it turns into one walk
> **Lecture:** [01 — Trie Basics and Autocomplete](../lecture-notes/01-trie-basics-and-autocomplete.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** it is the first page where the tree stores something other than letters. One integer per node turns "how many callsigns start this way" from a subtree walk into a lookup, and that move — precompute at build time, read at query time — is most of what makes a trie useful in practice.

## The Brief

Harbour control wants the **shortest opening letters that still name exactly one
vessel**. Say `KELPIE` and `KELVIN` are both registered: `KEL` names two ships and
is useless, `KELP` names one and is the answer.

A callsign that is a prefix of another has no stub at all — `KESTREL` is entirely
contained in `KESTRELTWO`, so no opening run of `KESTREL` names only `KESTREL`.
Report the whole callsign in that case.

## Starter

`exercise-03-callsign-stub-solution.py` sits beside this page with the callsigns
and the self-checks.

```text
KELPIE  KELVIN  KESTREL  KESTRELTWO  MARLIN  MARLOW  NARWHAL
```

Every node carries a count — the number of callsigns passing through it — under a
key that cannot be a letter, exactly as `END` cannot be. Two special keys now, and
both need the same care.

## Requirements

1. `build_stub_tree(callsigns)` returns a tree where every node counts the
   callsigns through it, and raises `ValueError` on a duplicate callsign.
2. `shortest_stub(root, callsign)` returns the shortest opening run naming only
   that callsign — or the whole callsign when no such run exists.
3. `all_stubs(callsigns)` returns the stub for every callsign.
4. `count_nodes(root)` returns the node count, for the same comparison as
   [Exercise 1](./exercise-01-gate-tag-tree.md).
5. A single registered callsign has a stub of one letter.

## Constraints

- **The count is incremented on the way down, at build time.** Counting the
  subtree at query time gives the same answer and is exactly the work this
  structure exists to avoid.
- **The root counts every callsign**, which is what makes `NARWHAL` — the only
  `N` — resolve at a single letter.
- **Duplicates are refused.** Two identical callsigns would make every count on
  their path wrong by one, and nothing downstream would report it.
- **A callsign that is a prefix of another has no stub.** Returning the whole
  callsign is the stated behaviour, not a fallback — the docstring says so and
  the checks assert it.
- **Two reserved keys now.** Say in the memo how you know neither can collide
  with a letter.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-03-callsign-stub-solution.py
KELPIE      -> KELP        (4 of 6)
KELVIN      -> KELV        (4 of 6)
KESTREL     -> KESTREL     (whole callsign)
KESTRELTWO  -> KESTRELT    (8 of 10)
MARLIN      -> MARLI       (5 of 6)
MARLOW      -> MARLO       (5 of 6)
NARWHAL     -> N           (1 of 7)

letters stamped   48
nodes in tree     33

All checks passed.
```

Three rows carry the whole exercise. `NARWHAL` resolves at **one letter**,
because nothing else starts with `N`. `KESTREL` gets the **whole callsign**,
because `KESTRELTWO` shadows every prefix of it. And `KESTRELTWO` needs eight
letters — one more than `KESTREL` is long — which is the shortest run that gets
past the shadow.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: a count per node, incremented on the way down, read on the way
   down again.
3. Build the tree. Increment the root's count too, and check the root's count
   equals the number of callsigns.
4. Write `shortest_stub` as a walk that stops at the first node whose count is 1.
5. Handle the shadowed case — a walk that never sees a count of 1 — before the
   pretty output. `KESTREL` is the test.
6. Add `all_stubs` and `count_nodes`, then write the FRAME pass.

## The Solution

```python
"""exercise-03-callsign-stub-solution.py — the shortest callsign stub.

Harbour control wants the shortest opening letters that still name exactly one
vessel. Build a prefix tree that remembers how many callsigns pass through
each node, then walk each callsign until the count drops to one.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"
PASSES = "#"

StubTree = dict

CALLSIGNS: list[str] = [
    "KELPIE",
    "KELVIN",
    "KESTREL",
    "KESTRELTWO",
    "MARLIN",
    "MARLOW",
    "NARWHAL",
]


def build_stub_tree(callsigns: list[str]) -> StubTree:
    """Return a prefix tree in which every node counts the callsigns through it.

    Args:
        callsigns: Distinct vessel callsigns.

    Returns:
        The root node. Each node carries PASSES, and END where a callsign stops.

    Raises:
        ValueError: If two callsigns are the same.
    """
    seen: set[str] = set()
    root: StubTree = {PASSES: 0}
    for callsign in callsigns:
        if callsign in seen:
            raise ValueError(f"callsign {callsign} was registered twice")
        seen.add(callsign)
        node = root
        node[PASSES] += 1
        for letter in callsign:
            node = node.setdefault(letter, {PASSES: 0})
            node[PASSES] += 1
        node[END] = True
    return root


def shortest_stub(root: StubTree, callsign: str) -> str:
    """Return the shortest opening letters that name only this callsign.

    Args:
        root: A tree built by `build_stub_tree`, holding this callsign.
        callsign: The callsign to shorten.

    Returns:
        The shortest prefix reaching a node with exactly one callsign through
        it. When no such prefix exists — because the callsign is the opening of
        a longer one — the whole callsign is returned.
    """
    node = root
    for cut, letter in enumerate(callsign, start=1):
        node = node[letter]
        if node[PASSES] == 1:
            return callsign[:cut]
    return callsign


def all_stubs(callsigns: list[str]) -> dict[str, str]:
    """Return every callsign paired with its shortest stub.

    Args:
        callsigns: Distinct vessel callsigns.

    Returns:
        A dict from callsign to stub, in the order the callsigns arrived.
    """
    root = build_stub_tree(callsigns)
    return {callsign: shortest_stub(root, callsign) for callsign in callsigns}


def count_nodes(root: StubTree) -> int:
    """Return how many nodes the tree holds, counting the root.

    Args:
        root: Any node. Called on the root, it counts the whole tree.

    Returns:
        The number of dicts in the tree. END and PASSES are not nodes.
    """
    total = 1
    for key, child in root.items():
        if key not in (END, PASSES):
            total += count_nodes(child)
    return total


# ---- Self-check ----
if __name__ == "__main__":
    stubs = all_stubs(CALLSIGNS)
    for callsign, stub in stubs.items():
        cut = "whole callsign" if stub == callsign else f"{len(stub)} of {len(callsign)}"
        print(f"{callsign:<11} -> {stub:<11} ({cut})")

    tree = build_stub_tree(CALLSIGNS)
    letters = sum(len(callsign) for callsign in CALLSIGNS)
    print()
    print(f"letters stamped  {letters:>3}")
    print(f"nodes in tree    {count_nodes(tree):>3}")

    assert stubs == {
        "KELPIE": "KELP",
        "KELVIN": "KELV",
        "KESTREL": "KESTREL",
        "KESTRELTWO": "KESTRELT",
        "MARLIN": "MARLI",
        "MARLOW": "MARLO",
        "NARWHAL": "N",
    }
    assert all_stubs(["SOLO"]) == {"SOLO": "S"}
    assert all_stubs(["TIDE", "TIDEWAY"]) == {"TIDE": "TIDE", "TIDEWAY": "TIDEW"}

    try:
        build_stub_tree(["MARLIN", "MARLIN"])
    except ValueError as problem:
        assert str(problem) == "callsign MARLIN was registered twice"
    else:
        raise AssertionError("a repeated callsign should have been rejected")

    print()
    print("All checks passed.")
```

The count is read *before* descending rather than after, which is what makes the
answer the shortest run rather than one letter longer. It is a one-character
difference in the loop and it is the thing to check first when the stubs come out
too long.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-03-callsign-stub-solution.py
```

No third-party packages, no arguments, no input. It prints each callsign with its
stub and the count it resolved at, the node totals, and then
`All checks passed.`

## Common bugs to catch

- **Counting the subtree at query time.** Symptom: correct stubs, and the
  structure doing no work for you.
- **Not counting at the root.** Symptom: `NARWHAL` gets a two-letter stub, because
  the walk cannot resolve at depth zero.
- **Reading the count after descending.** Symptom: every stub one letter too long.
- **Returning `None` for a shadowed callsign.** Symptom: `KESTREL` has no answer
  where "the whole callsign" is the answer.
- **Allowing duplicates.** Symptom: counts that never reach 1, and stubs equal to
  whole callsigns for no visible reason.
- **A letter used as the count key.** Symptom: a callsign containing that letter
  corrupts the tree silently.

## Acceptance checklist

- [ ] `NARWHAL` resolves at one letter; `KELPIE` at four; `MARLIN` at five.
- [ ] `KESTREL` returns the whole callsign; `KESTRELTWO` returns eight letters.
- [ ] The root's count equals the number of callsigns.
- [ ] A duplicate callsign raises `ValueError`.
- [ ] A register of one callsign gives a one-letter stub.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the *longest* stub in the register and which callsign it belongs to.
  That is the pair the harbour is most likely to confuse over the radio.
- Add a callsign and update the counts without rebuilding. It is one walk, and it
  is what makes this structure usable on a live register.
- Store the count and drop `END` entirely: a node is the end of a callsign when
  its count exceeds the sum of its children's counts. Work out whether that is
  true, then decide whether it is a good idea.
