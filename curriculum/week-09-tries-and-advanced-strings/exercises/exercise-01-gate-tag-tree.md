# Exercise 1 — The Gate Tag Tree

> **Topic:** building a prefix tree out of nothing but nested dictionaries, and counting what it saves
> **Lecture:** [01 — Trie Basics and Autocomplete](../lecture-notes/01-trie-basics-and-autocomplete.md)
> **Difficulty:** Easy
> **Target time:** 35 minutes
> **Why this one:** every other page this week is this page with more on top. It also gets the two questions straight that people conflate for the rest of the course — "is this exact thing registered" and "is anything registered below here" are different questions with different answers, and a tree that cannot tell them apart is broken in a way nothing will report.

## The Brief

A canal authority registers a tag for every gate: `MARSH`, `MARSHEND`,
`MARSHGATE`, `MILL`, `MILLPOND`, `MILLRACE`, `MOOR`, `MOORHEN`.

Store them so that the letters shared between tags are stored **once**. `MARSH`,
`MARSHEND` and `MARSHGATE` share five letters; storing them three times is what a
plain list does, and the whole point of the structure is that it does not.

Then answer two questions with it, and keep them apart:

- **Is this exact tag registered?** `MOO` is not, even though every letter of it
  is in the tree.
- **Is anything at all registered below this prefix?** `MOOR` is, `MUD` is not.

## Starter

`exercise-01-gate-tag-tree-solution.py` sits beside this page with the tags and
the self-checks.

A node is a plain `dict`. Every key is one letter leading to a child node, except
one special key — `END` — which marks "a tag stops here". That is the entire data
structure; there is no class, no node type, nothing to import.

```text
tags        8
letters     53 stamped across all eight tags
```

Fifty-three letters, and the tree will not need fifty-three nodes. Work out
roughly how many before you build it.

## Requirements

1. `build_tag_tree(tags)` returns the root node, and raises `ValueError` on an
   empty tag.
2. `count_nodes(root)` returns how many nodes the tree holds.
3. `is_registered(root, tag)` is true only for a tag that was registered.
4. `any_registered_under(root, prefix)` is true when anything at all sits below
   the prefix.
5. An empty prefix is below everything, so it is true whenever the tree is
   non-empty.

## Constraints

- **A node is a dict and nothing else.** No class. The point of this page is to
  see that the structure is just nesting.
- **`END` must not be confusable with a letter.** Pick a key no tag can contain
  and say why in the memo — this is the one place where the "dict of dicts"
  representation can bite.
- **The two questions are different.** `is_registered` checks for `END` at the
  node it lands on; `any_registered_under` only checks that the node exists.
  Writing one and using it for both is the bug this exercise exists to prevent.
- **An empty tag is refused**, not stored. A tree with `END` at the root means
  every prefix query gets a surprising answer.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-01-gate-tag-tree.py
tags registered    8
letters stamped   53
nodes in tree     30
nodes saved       24

registered MARSH     yes
registered MARSHY    no
registered MILL      yes
registered MOO       no
registered MOORHEN   yes

anything under MAR       yes
anything under MOOR      yes
anything under MUD       no
anything under (empty)   yes

All checks passed.
```

Fifty-three letters, thirty nodes: **twenty-four nodes saved**. That is the whole
argument for the structure, and it is worth having it as a number rather than a
claim — on eight short tags it saves 45%, and the saving grows with how much the
tags have in common.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: a node is a dict, keys are letters, `END` marks a stop.
3. Build the tree with `setdefault`. It is three lines.
4. Count the nodes and compare against the letters stamped. Have the number
   before you have an opinion about it.
5. Write `is_registered`, then `any_registered_under`, and write them
   **separately** even though they share a walk. Check `MOO` against both — it
   answers no to the first and yes to the second, and that pair is the test.
6. Handle the empty prefix and the empty tag, then write the FRAME pass.

## The Solution

```python
"""exercise-01-gate-tag-tree-solution.py — the canal gate tag register.

Build a prefix tree out of nothing but nested dictionaries, count what it
costs in nodes, then answer two questions with it: is this exact tag
registered, and is anything at all registered below this prefix.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# A node is a plain dict. Every key is one letter leading to a child node,
# except END, which marks "a tag stops here".
END = "*"

# One node of the tree. The values are either child nodes or the END flag,
# so the annotation is deliberately loose.
TagTree = dict

GATE_TAGS: list[str] = [
    "MARSH",
    "MARSHEND",
    "MARSHGATE",
    "MILL",
    "MILLPOND",
    "MILLRACE",
    "MOOR",
    "MOORHEN",
]


def build_tag_tree(tags: list[str]) -> TagTree:
    """Return a prefix tree holding every tag.

    Args:
        tags: The gate tags to register. Order does not matter.

    Returns:
        The root node — a dict, empty when `tags` is empty.

    Raises:
        ValueError: If any tag is the empty string.
    """
    root: TagTree = {}
    for tag in tags:
        if not tag:
            raise ValueError("a gate tag cannot be the empty string")
        node = root
        for letter in tag:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def count_nodes(root: TagTree) -> int:
    """Return how many nodes the tree holds, counting the root.

    Args:
        root: Any node. Called on the root, it counts the whole tree.

    Returns:
        The number of dicts in the tree. END flags are not nodes.
    """
    total = 1
    for key, child in root.items():
        if key != END:
            total += count_nodes(child)
    return total


def is_registered(root: TagTree, tag: str) -> bool:
    """Return True when `tag` was registered exactly.

    Args:
        root: The root of the tree.
        tag: The tag to look up.

    Returns:
        True only when the walk finishes and an END flag sits there.
    """
    node = root
    for letter in tag:
        if letter not in node:
            return False
        node = node[letter]
    return END in node


def any_registered_under(root: TagTree, prefix: str) -> bool:
    """Return True when at least one registered tag starts with `prefix`.

    Args:
        root: The root of the tree.
        prefix: The prefix to test. The empty prefix matches everything.

    Returns:
        True when the walk survives to the end of `prefix`.
    """
    node = root
    for letter in prefix:
        if letter not in node:
            return False
        node = node[letter]
    return True


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_tag_tree(GATE_TAGS)
    letters = sum(len(tag) for tag in GATE_TAGS)
    nodes = count_nodes(tree)

    print(f"tags registered  {len(GATE_TAGS):>3}")
    print(f"letters stamped  {letters:>3}")
    print(f"nodes in tree    {nodes:>3}")
    print(f"nodes saved      {letters + 1 - nodes:>3}")
    print()

    for tag in ["MARSH", "MARSHY", "MILL", "MOO", "MOORHEN"]:
        print(f"registered {tag:<9} {'yes' if is_registered(tree, tag) else 'no'}")
    print()

    for prefix in ["MAR", "MOOR", "MUD", ""]:
        shown = prefix if prefix else "(empty)"
        answer = "yes" if any_registered_under(tree, prefix) else "no"
        print(f"anything under {shown:<9} {answer}")

    assert nodes == 30
    assert letters == 53
    assert is_registered(tree, "MARSH") is True
    assert is_registered(tree, "MARSHY") is False
    assert is_registered(tree, "MOO") is False
    assert any_registered_under(tree, "MOO") is True
    assert any_registered_under(tree, "MUD") is False
    assert any_registered_under(tree, "") is True
    assert count_nodes(build_tag_tree([])) == 1

    try:
        build_tag_tree(["MARSH", ""])
    except ValueError as problem:
        assert str(problem) == "a gate tag cannot be the empty string"
    else:
        raise AssertionError("an empty tag should have been rejected")

    print()
    print("All checks passed.")
```

The descent is the same three lines in both query functions, and they are still
written out twice rather than factored into one. That is deliberate at this
stage: the difference between the two functions is one line at the end, and
seeing that difference plainly is worth more here than the shared helper.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-01-gate-tag-tree.py
```

No third-party packages, no arguments, no input. It prints the node count against
the letter count, both sets of queries, and then `All checks passed.`

## Common bugs to catch

- **`is_registered` returning true for a prefix.** Symptom: `MOO` is registered.
  The node exists; the tag does not.
- **Using a letter as the end marker.** Symptom: a tag containing that letter
  breaks the tree silently.
- **Counting the root, or not counting it, without deciding.** Symptom: an
  off-by-one in the saving that makes the comparison meaningless. Decide, then say
  which in the docstring.
- **Storing an empty tag.** Symptom: `END` at the root and every prefix query
  returning something odd.
- **`any_registered_under("")` returning false.** Symptom: an empty prefix
  treated as a special case. It is not — everything is below it.

## Acceptance checklist

- [ ] Eight tags, 53 letters, 30 nodes — 24 saved.
- [ ] `MARSH` and `MOORHEN` are registered; `MARSHY` and `MOO` are not.
- [ ] `MAR` and `MOOR` have something under them; `MUD` does not.
- [ ] The empty prefix has something under it.
- [ ] An empty tag raises `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the saving as a percentage and re-run it on a register where the tags
  share nothing. The number collapses, and that is the honest boundary of the
  structure.
- Add `remove(root, tag)`. It is harder than it looks: unregistering `MARSH` must
  leave `MARSHEND` intact, so nodes only disappear when nothing passes through
  them any more.
- Count, per depth, how many nodes there are. The shape of that list tells you
  where the register's tags actually diverge.
