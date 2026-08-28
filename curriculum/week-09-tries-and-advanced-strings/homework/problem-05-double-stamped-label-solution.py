"""problem-05-double-stamped-label-solution.py — labels made of other labels.

A boatyard stamps part labels from a set of metal dies, one die per registered
code. Some labels were stamped with two or more dies in a row, so the label
reads as one code but is really several registered codes joined up.

Find every registered code that is exactly two or more other registered codes
laid end to end, longest first.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

DIE_CODES: list[str] = [
    "FIN",
    "BOARD",
    "FINBOARD",
    "KEEL",
    "SON",
    "KEELSON",
    "BOARDKEELSON",
    "MAST",
    "MASTFIN",
    "FINBOARDMAST",
    "RUDDER",
]


def build_die_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every die code.

    Args:
        codes: The registered codes. Duplicates are harmless.

    Returns:
        The root node.

    Raises:
        ValueError: If any code is the empty string.
    """
    root: CodeTree = {}
    for code in codes:
        if not code:
            raise ValueError("a die code cannot be the empty string")
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def is_double_stamped(root: CodeTree, code: str) -> bool:
    """Return True when `code` is two or more registered codes end to end.

    Args:
        root: A tree of registered codes, including `code` itself.
        code: The label to test.

    Returns:
        True when `code` splits into at least two registered pieces. The whole
        label counts as one piece, so a label that only matches itself is False.
    """
    reachable: dict[int, bool] = {}

    def can_finish(start: int, pieces: int) -> bool:
        if start == len(code):
            return pieces >= 2
        if start in reachable and not reachable[start]:
            return False
        node = root
        for cut in range(start, len(code)):
            letter = code[cut]
            if letter not in node:
                break
            node = node[letter]
            if END not in node:
                continue
            if cut + 1 == len(code) and pieces == 0:
                continue  # that piece is the whole label, so it is not a build
            if can_finish(cut + 1, pieces + 1):
                return True
        reachable[start] = False
        return False

    return can_finish(0, 0)


def double_stamped(codes: list[str]) -> list[str]:
    """Return every code that is built from two or more other codes.

    Args:
        codes: The registered codes.

    Returns:
        The built codes, longest first, ties broken A to Z.
    """
    root = build_die_tree(codes)
    built = [code for code in codes if is_double_stamped(root, code)]
    return sorted(built, key=lambda code: (-len(code), code))


# ---- Self-check ----
if __name__ == "__main__":
    found = double_stamped(DIE_CODES)
    for code in found:
        print(f"{len(code):>3}  {code}")
    print()
    print(f"single-die codes  {sorted(set(DIE_CODES) - set(found))}")

    assert found == [
        "BOARDKEELSON",
        "FINBOARDMAST",
        "FINBOARD",
        "KEELSON",
        "MASTFIN",
    ]
    assert double_stamped(["RUDDER"]) == []
    assert double_stamped(["A", "B", "AB", "ABA"]) == ["ABA", "AB"]
    assert double_stamped([]) == []

    try:
        build_die_tree(["FIN", ""])
    except ValueError as problem:
        assert str(problem) == "a die code cannot be the empty string"
    else:
        raise AssertionError("an empty code should have been rejected")

    print()
    print("All checks passed.")
