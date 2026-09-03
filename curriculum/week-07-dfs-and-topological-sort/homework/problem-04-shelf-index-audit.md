# Problem 4 — The Shelf Index Audit

> **Topic:** a rule about a node and *everything beneath it*, not a node and its children
> **Lecture:** [01 — Recursive DFS](../lecture-notes/01-recursive-dfs.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** the obvious check is wrong, it passes the sound index, and it passes a broken one too. The file ships it so you can watch it pass something it should have caught — which is a much better lesson than being told the rule.

## The Brief

A library's shelf index is a binary tree written as plain tuples:
`(code, left, right)`, where `code` is an integer and `left` and `right` are
either another node or `None`. No classes, so the whole index can be printed and
read.

The rule the index has to keep is **not** about a node and its two children. It
is about a node and **every code beneath it**: everything down the left branch is
strictly smaller, everything down the right branch is strictly larger.

Report the first code that breaks the rule, in pre-order, or `None` when the
index is sound.

## Starter

`problem-04-shelf-index-audit-solution.py` sits beside this page with four
indexes and the self-checks.

```text
SOUND_INDEX      keeps the rule
STRAYED_INDEX    one code in the wrong subtree
TWO_FAULTS       two breaks - the answer is the first in pre-order
REPEATED_CODE    (50, (50, None, None), None) - strictly smaller, so 50 is a break
```

`STRAYED_INDEX` is the one to trace by hand. Its broken code is larger than its
own parent and smaller than an ancestor further up — so a check comparing each
node against its parent passes it, and the index is still wrong.

## Requirements

1. `first_bad_code(root)` returns the first offending code in pre-order, or
   `None`.
2. `first_bad_code_parent_only(root)` is the wrong check that compares each node
   against its parent — shipped to be run and seen passing a broken index.
3. `ladder(depth)` builds a one-sided spine, for the depth test.
4. An empty index is sound.
5. Equal codes break the rule, because the rule says *strictly*.

## Constraints

- **The rule is about ancestors, not parents.** Every node carries a range it
  must fall inside — open at the top on the far left, open at the bottom on the
  far right — and descending narrows it. That range is the whole algorithm.
- **Strictly smaller and strictly larger.** A repeated code is a break, and
  `REPEATED_CODE` is in the data to make sure the comparison is `<` and not `<=`.
- **Pre-order decides which break is reported** when there is more than one.
  State the order rather than letting the traversal choose it silently.
- **The spine is 900 deep**, which is inside Python's default recursion limit but
  not by much. Say what you would do at 5,000 — the honest answer is the same
  answer as [Problem 3](./problem-03-safe-forwarding.md).
- **An empty index is sound**, not an error. There is nothing in it to break the
  rule.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python problem-04-shelf-index-audit-solution.py
sound index          : None
strayed index        : 60
  parent-only check  : None
two faults, pre-order: 35
repeated code        : 50
empty index          : None
900-deep sound spine : None
All checks passed.
```

Two lines together are the exhibit:

```text
strayed index        : 60
  parent-only check  : None
```

The correct audit finds code 60 in the wrong subtree. The parent-only check finds
nothing at all — it is not confused, it is answering a different and easier
question, and it will keep answering it confidently on every broken index of this
shape.

That is what a plausible wrong rule looks like from the outside: not an error,
just a clean bill of health for something that is broken.

## Steps

1. Read the self-checks. They are the spec.
2. Trace `STRAYED_INDEX` by hand and find the offending code. Then check it
   against its own parent and confirm it looks fine there.
3. Write the memo: every node carries a `(low, high)` range; descending left
   lowers the ceiling, descending right raises the floor.
4. Write the audit. Start the root with no bounds at all.
5. Write the parent-only version too, and run both. Watch it pass the strayed
   index.
6. Check `TWO_FAULTS` reports the *first* in pre-order, and `REPEATED_CODE`
   reports the repeat.
7. Write the FRAME pass, with the parent-only failure as the worked example.

## The Solution

```python
"""problem-04-shelf-index-audit-solution.py -- auditing a library's binary shelf index.

The index is a binary tree written as plain tuples: (code, left, right), where
code is an integer shelf code and left and right are either another node or
None. No classes, so the whole index can be printed and read.

The rule the index has to keep is not about a node and its two children. It is
about a node and every code beneath it: everything down the left branch is
strictly smaller, everything down the right branch is strictly larger. A check
that only compares a node against its parent passes indexes that are broken,
and this file ships that wrong check beside the right one so the gap can be
seen.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

Node = tuple[int, "Node | None", "Node | None"]

# ---- Given data ----
# Every code on the left of 50 is under 50; every code on its right is over 50.
SOUND_INDEX: Node = (
    50,
    (30, (20, None, None), (40, None, None)),
    (70, (60, None, None), (80, None, None)),
)

# 60 sits to the right of 30, so a parent-only check is happy with it. But it is
# in the left branch of 50, where nothing may reach 50. This is the case the
# whole problem is about.
STRAYED_INDEX: Node = (
    50,
    (30, (20, None, None), (60, None, None)),
    (70, None, None),
)

# Two faults. Pre-order meets 35 first: node, then left branch, then right.
TWO_FAULTS: Node = (
    50,
    (30, (35, None, None), (40, None, None)),
    (70, (10, None, None), None),
)

# A code equal to an ancestor's. Strictly smaller means 50 is not allowed here.
REPEATED_CODE: Node = (50, (50, None, None), None)


def first_bad_code(root: Node | None) -> int | None:
    """Find the first shelf code, in pre-order, that breaks its ancestors' range.

    Args:
        root: The index, as nested (code, left, right) tuples, or None.

    Returns:
        The offending code, or None when the index is sound. An empty index --
        None -- is sound, so None in gives None out.
    """

    def audit(node: Node | None, low: int | None, high: int | None) -> int | None:
        if node is None:
            return None
        code, left, right = node
        if low is not None and code <= low:
            return code
        if high is not None and code >= high:
            return code
        from_left = audit(left, low, code)
        if from_left is not None:
            return from_left
        return audit(right, code, high)

    return audit(root, None, None)


def first_bad_code_parent_only(root: Node | None) -> int | None:
    """The tempting wrong check: compare each node only against its own children.

    Kept so the page can show what it misses. Do not use it.

    Args:
        root: The index, as nested (code, left, right) tuples, or None.

    Returns:
        The first code it objects to, or None. It says None for indexes that are
        badly broken, which is the point.
    """

    def audit(node: Node | None) -> int | None:
        if node is None:
            return None
        code, left, right = node
        if left is not None and left[0] >= code:
            return left[0]
        if right is not None and right[0] <= code:
            return right[0]
        from_left = audit(left)
        if from_left is not None:
            return from_left
        return audit(right)

    return audit(root)


def ladder(depth: int) -> Node | None:
    """Build a right-leaning index of ascending codes 1..depth.

    Args:
        depth: How many nodes the spine holds.

    Returns:
        The root of the spine, or None when depth is 0.
    """
    node: Node | None = None
    for code in range(depth, 0, -1):
        node = (code, None, node)
    return node


# ---- Self-check ----
if __name__ == "__main__":
    print(f"sound index          : {first_bad_code(SOUND_INDEX)}")
    print(f"strayed index        : {first_bad_code(STRAYED_INDEX)}")
    print(f"  parent-only check  : {first_bad_code_parent_only(STRAYED_INDEX)}")
    print(f"two faults, pre-order: {first_bad_code(TWO_FAULTS)}")
    print(f"repeated code        : {first_bad_code(REPEATED_CODE)}")
    print(f"empty index          : {first_bad_code(None)}")
    print(f"900-deep sound spine : {first_bad_code(ladder(900))}")

    assert first_bad_code(SOUND_INDEX) is None
    assert first_bad_code(STRAYED_INDEX) == 60
    assert first_bad_code_parent_only(STRAYED_INDEX) is None
    assert first_bad_code(TWO_FAULTS) == 35
    assert first_bad_code(REPEATED_CODE) == 50
    assert first_bad_code(None) is None
    assert first_bad_code((7, None, None)) is None
    assert first_bad_code((0, (-1, None, None), (1, None, None))) is None
    assert first_bad_code((50, None, (50, None, None))) == 50
    assert first_bad_code(ladder(900)) is None
    assert first_bad_code(ladder(0)) is None

    print("All checks passed.")
```

The bounds are passed down rather than values passed up, and both work. Passing
down is shorter here and states the invariant directly — "this node must fall in
this range" — which is exactly the sentence the write-up needs anyway.

## Download and run

Download the solution beside this page and run it:

```bash
python problem-04-shelf-index-audit-solution.py
```

No third-party packages, no arguments, no input. It prints the audit of all four
indexes, the parent-only check's answer on the strayed one, the deep spine, and
then `All checks passed.`

## Common bugs to catch

- **Comparing each node against its parent only.** Symptom: a clean bill of
  health for `STRAYED_INDEX`. The whole point of the page.
- **`<=` where `<` belongs.** Symptom: `REPEATED_CODE` passes. The rule says
  strictly.
- **Not narrowing the range on the way down.** Symptom: correct on shallow
  indexes and wrong on anything three deep.
- **Reporting the deepest break rather than the first in pre-order.** Symptom:
  `TWO_FAULTS` returns the wrong one of the two. State the order.
- **Treating an empty index as an error.** Symptom: an exception where `None` is
  the answer.
- **Initialising the root's bounds to some large number.** Symptom: it works
  until a shelf code exceeds it. Use `None` for "no bound" and mean it.

## Acceptance checklist

- [ ] `SOUND_INDEX` returns `None`; `STRAYED_INDEX` returns 60.
- [ ] The parent-only check returns `None` on `STRAYED_INDEX`, asserted.
- [ ] `TWO_FAULTS` returns the first break in pre-order.
- [ ] `REPEATED_CODE` returns 50.
- [ ] An empty index returns `None`.
- [ ] A 900-deep sound spine returns `None`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report *every* break rather than the first. It is the version a librarian could
  act on, and it needs the walk to keep going after a failure.
- Return the range each broken code was allowed to be in. That turns "60 is
  wrong" into "60 had to be under 55", which is the difference between a finding
  and a fix.
- Rewrite the audit iteratively with an explicit stack carrying the bounds, and
  run it on a 5,000-deep spine. It is the same change
  [Problem 3](./problem-03-safe-forwarding.md) argues for, on a different shape.
