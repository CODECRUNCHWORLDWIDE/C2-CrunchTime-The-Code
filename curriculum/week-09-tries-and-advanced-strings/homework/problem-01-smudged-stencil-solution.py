"""problem-01-smudged-stencil-solution.py — reading a smudged crate stencil.

Depot crates carry a stencilled code. Rain smudges letters, and the clerk
types a question mark where a letter is unreadable. One question mark stands
for exactly one letter, never for none and never for two.

Given the register of real codes and a smudged pattern, list every code the
pattern could be, A to Z.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"
SMUDGE = "?"

CodeTree = dict

STENCILS: list[str] = [
    "CRATE",
    "GRATE",
    "GRAPE",
    "CRANE",
    "PLATE",
    "SLATE",
    "SLATS",
    "PLAN",
]

PATTERNS: list[str] = ["?RATE", "GRA?E", "?????", "SLAT?", "PL??", "CRATE", "??"]


def build_stencil_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every stencil code.

    Args:
        codes: The codes in the register. Duplicates are harmless.

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


def matches(root: CodeTree, pattern: str) -> list[str]:
    """Return every registered code the smudged pattern could be, A to Z.

    Args:
        root: A tree of registered codes.
        pattern: Letters, with SMUDGE standing for exactly one unknown letter.

    Returns:
        The matching codes, sorted A to Z. Empty when nothing matches.

    Raises:
        ValueError: If `pattern` is empty.
    """
    if not pattern:
        raise ValueError("a stencil pattern cannot be empty")
    found: list[str] = []

    def walk(node: CodeTree, position: int, spelled: str) -> None:
        if position == len(pattern):
            if END in node:
                found.append(spelled)
            return
        mark = pattern[position]
        if mark == SMUDGE:
            for letter in sorted(key for key in node if key != END):
                walk(node[letter], position + 1, spelled + letter)
        elif mark in node:
            walk(node[mark], position + 1, spelled + mark)

    walk(root, 0, "")
    return sorted(found)


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_stencil_tree(STENCILS)
    for pattern in PATTERNS:
        hits = matches(tree, pattern)
        shown = ", ".join(hits) if hits else "(nothing)"
        print(f"{pattern:<7} {len(hits)}  {shown}")

    assert matches(tree, "?RATE") == ["CRATE", "GRATE"]
    assert matches(tree, "GRA?E") == ["GRAPE", "GRATE"]
    assert matches(tree, "?????") == [
        "CRANE",
        "CRATE",
        "GRAPE",
        "GRATE",
        "PLATE",
        "SLATE",
        "SLATS",
    ]
    assert matches(tree, "SLAT?") == ["SLATE", "SLATS"]
    assert matches(tree, "PL??") == ["PLAN"]
    assert matches(tree, "CRATE") == ["CRATE"]
    assert matches(tree, "??") == []
    assert matches(tree, "?") == []

    try:
        matches(tree, "")
    except ValueError as problem:
        assert str(problem) == "a stencil pattern cannot be empty"
    else:
        raise AssertionError("an empty pattern should have been rejected")

    print()
    print("All checks passed.")
