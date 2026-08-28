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
