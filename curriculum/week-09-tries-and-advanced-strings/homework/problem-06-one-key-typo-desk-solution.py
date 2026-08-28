"""problem-06-one-key-typo-desk-solution.py — one wrong key, nothing else.

The yard office types four-letter locker codes all day, and the commonest
mistake is hitting one neighbouring key. The desk should answer a single
question: which real codes are exactly one letter away from what was typed?

Exactly one. A code that matches perfectly is not an answer, because nothing
was mistyped. A code two letters away is not an answer either.

The walk carries a budget of one swap down the tree. While the budget is
unspent the walk may branch into every other letter; once it is spent the walk
must follow the typed letters exactly.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

LOCKERS: list[str] = ["HOLD", "HOLE", "HULL", "BOLT", "BOLD", "BOAT", "OARS"]

TYPED: list[str] = ["HOLD", "BOLD", "BOAT", "HULL", "OARS", "HOL", "HOLDS"]


def build_locker_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every locker code.

    Args:
        codes: The real locker codes. Duplicates are harmless.

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


def one_key_away(root: CodeTree, typed: str) -> list[str]:
    """Return every real code that differs from `typed` in exactly one letter.

    Args:
        root: A tree of real locker codes.
        typed: What the clerk typed. Must not be empty.

    Returns:
        The matching codes, sorted A to Z. Codes of a different length can
        never qualify, and neither can `typed` itself.

    Raises:
        ValueError: If `typed` is empty.
    """
    if not typed:
        raise ValueError("nothing was typed")
    found: list[str] = []

    def walk(node: CodeTree, position: int, spelled: str, swapped: bool) -> None:
        if position == len(typed):
            if swapped and END in node:
                found.append(spelled)
            return
        wanted = typed[position]
        for letter in sorted(key for key in node if key != END):
            if letter == wanted:
                walk(node[letter], position + 1, spelled + letter, swapped)
            elif not swapped:
                walk(node[letter], position + 1, spelled + letter, True)

    walk(root, 0, "", False)
    return found


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_locker_tree(LOCKERS)
    for typed in TYPED:
        near = one_key_away(tree, typed)
        shown = ", ".join(near) if near else "(nothing)"
        print(f"{typed:<6} {len(near)}  {shown}")

    assert one_key_away(tree, "HOLD") == ["BOLD", "HOLE"]
    assert one_key_away(tree, "BOLD") == ["BOLT", "HOLD"]
    assert one_key_away(tree, "BOAT") == ["BOLT"]
    assert one_key_away(tree, "HULL") == []
    assert one_key_away(tree, "OARS") == []
    assert one_key_away(tree, "HOL") == []
    assert one_key_away(tree, "HOLDS") == []
    assert one_key_away(tree, "ZOLD") == ["BOLD", "HOLD"]

    try:
        one_key_away(tree, "")
    except ValueError as problem:
        assert str(problem) == "nothing was typed"
    else:
        raise AssertionError("an empty entry should have been rejected")

    print()
    print("All checks passed.")
