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
