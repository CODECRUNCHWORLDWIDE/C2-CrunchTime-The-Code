"""challenge-01-cold-store-aisle-sweep-solution.py — one walk, every code.

A cold store is a grid of bins, each stamped with one letter. A picker starts
at any bin and steps up, down, left or right, never entering the same bin
twice on one walk. The letters they pass spell a route code.

Given the pick list, report how many different starting bins each code can be
walked from. Codes that cannot be walked at all are left out of the report.

The trick is to hang the whole pick list on one prefix tree and walk the grid
once, instead of walking the grid once per code. The file prints both step
counts so the saving is visible rather than claimed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

BINS: list[str] = [
    "SALT",
    "TLAS",
    "AIME",
    "LTSP",
]

PICK_LIST: list[str] = [
    "SALT",
    "SALTS",
    "MAST",
    "TAIL",
    "LIT",
    "TIL",
    "PEST",
    "TALL",
    "SEA",
    "SLAT",
    "MEAL",
]


def build_pick_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree of the pick list, with each code at its own leaf.

    Args:
        codes: The route codes to look for. Each must be at least two letters.

    Returns:
        The root node. A node that ends a code carries END, and END holds the
        code itself, so a walk that reaches it already knows what it spelled.

    Raises:
        ValueError: If any code is shorter than two letters.
    """
    root: CodeTree = {}
    for code in codes:
        if len(code) < 2:
            raise ValueError(f"route code {code!r} is too short to be a walk")
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = code
    return root


def sweep(bins: list[str], codes: list[str]) -> tuple[dict[str, int], int]:
    """Return the starting-bin count for every walkable code, plus the work done.

    Args:
        bins: The store, one string per row. Every row is the same length.
        codes: The pick list.

    Returns:
        A pair. First, a dict from code to the number of distinct bins a walk
        spelling it can start from; codes that cannot be walked are absent.
        Second, how many bin-entry steps the sweep took.
    """
    root = build_pick_tree(codes)
    rows = len(bins)
    columns = len(bins[0]) if rows else 0
    starts: dict[str, set[tuple[int, int]]] = {}
    steps = 0

    def walk(row: int, column: int, node: CodeTree, origin: tuple[int, int]) -> None:
        nonlocal steps
        letter = bins[row][column]
        child = node.get(letter)
        if child is None:
            return
        steps += 1
        standing = bins[row]
        bins[row] = standing[:column] + " " + standing[column + 1 :]
        if END in child:
            starts.setdefault(child[END], set()).add(origin)
        for next_row, next_column in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= next_row < rows and 0 <= next_column < columns:
                walk(next_row, next_column, child, origin)
        bins[row] = standing

    for row in range(rows):
        for column in range(columns):
            walk(row, column, root, (row, column))

    return {code: len(cells) for code, cells in starts.items()}, steps


def naive_sweep(bins: list[str], codes: list[str]) -> tuple[dict[str, int], int]:
    """Return the same report, walking the grid once per code.

    Args:
        bins: The store, one string per row.
        codes: The pick list.

    Returns:
        A pair: the same dict `sweep` returns, and the bin-entry step count.
    """
    rows = len(bins)
    columns = len(bins[0]) if rows else 0
    report: dict[str, int] = {}
    steps = 0

    def walk(row: int, column: int, code: str, position: int) -> bool:
        nonlocal steps
        if bins[row][column] != code[position]:
            return False
        steps += 1
        if position == len(code) - 1:
            return True
        standing = bins[row]
        bins[row] = standing[:column] + " " + standing[column + 1 :]
        for next_row, next_column in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= next_row < rows and 0 <= next_column < columns:
                if walk(next_row, next_column, code, position + 1):
                    bins[row] = standing
                    return True
        bins[row] = standing
        return False

    for code in codes:
        if len(code) < 2:
            raise ValueError(f"route code {code!r} is too short to be a walk")
        found = 0
        for row in range(rows):
            for column in range(columns):
                if walk(row, column, code, 0):
                    found += 1
        if found:
            report[code] = found

    return report, steps


# ---- Self-check ----
if __name__ == "__main__":
    for row in BINS:
        print(" ".join(row))
    print()

    report, tree_steps = sweep(BINS, PICK_LIST)
    for code, count in sorted(report.items(), key=lambda pair: (-pair[1], pair[0])):
        bin_word = "bin" if count == 1 else "bins"
        print(f"{code:<6} {count} starting {bin_word}")

    missing = sorted(code for code in PICK_LIST if code not in report)
    print()
    print(f"not walkable  {', '.join(missing)}")

    plain_report, plain_steps = naive_sweep(BINS, PICK_LIST)
    print(f"one-tree steps {tree_steps:>6}")
    print(f"code-by-code   {plain_steps:>6}")

    assert report == {
        "SALT": 2,
        "SALTS": 2,
        "MAST": 1,
        "TAIL": 1,
        "LIT": 1,
        "TIL": 1,
        "PEST": 1,
    }
    assert plain_report == report
    assert tree_steps < plain_steps
    assert BINS == ["SALT", "TLAS", "AIME", "LTSP"]  # the store was put back

    try:
        sweep(BINS, ["S"])
    except ValueError as problem:
        assert str(problem) == "route code 'S' is too short to be a walk"
    else:
        raise AssertionError("a one-letter code should have been rejected")

    print()
    print("All checks passed.")
