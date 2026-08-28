"""problem-03-splice-point-solution.py — finding every splice in a spool label.

A cable spool is labelled with the colour bands printed along it, one letter
per band. A splice code is a short band sequence the workshop wants to find.
Report every position where the code appears — including positions that
overlap an earlier hit, because a splice can share bands with its neighbour.

The one-pass scan reuses the code's own border table, so the position in the
label never moves backwards. The nested-loop version re-reads bands it has
already seen, and on a label built from a repeating pattern it re-reads almost
all of them.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

LABEL = "RGRGRGBRGRGRGR"
CODE = "RGRGR"

# A label built to punish the nested-loop scan: one long repeat, one odd band.
LONG_LABEL = "RG" * 2000
LONG_CODE = "RG" * 20 + "B"


def border_table(code: str) -> list[int]:
    """Return the border length at every cut of `code`.

    Args:
        code: The splice code. Must not be empty.

    Returns:
        A list as long as `code`, where entry `i` is the length of the longest
        run that both opens and closes `code[:i + 1]` without being all of it.

    Raises:
        ValueError: If `code` is empty.
    """
    if not code:
        raise ValueError("a splice code cannot be empty")
    table = [0] * len(code)
    cursor = 1
    matched = 0
    while cursor < len(code):
        if code[cursor] == code[matched]:
            matched += 1
            table[cursor] = matched
            cursor += 1
        elif matched:
            matched = table[matched - 1]
        else:
            table[cursor] = 0
            cursor += 1
    return table


def splice_points(label: str, code: str) -> list[int]:
    """Return every start position where `code` appears in `label`.

    Args:
        label: The bands printed along the spool. May be empty.
        code: The splice code to find. Must not be empty.

    Returns:
        The start positions, smallest first. Overlapping hits are all listed.
        Empty when the code does not appear.

    Raises:
        ValueError: If `code` is empty.
    """
    table = border_table(code)
    hits: list[int] = []
    matched = 0
    for position, band in enumerate(label):
        while matched and band != code[matched]:
            matched = table[matched - 1]
        if band == code[matched]:
            matched += 1
        if matched == len(code):
            hits.append(position - matched + 1)
            matched = table[matched - 1]
    return hits


def splice_points_by_scan(label: str, code: str) -> list[int]:
    """Return the same positions the slow way, for checking only.

    Args:
        label: The bands printed along the spool.
        code: The splice code to find. Must not be empty.

    Returns:
        The start positions, smallest first.

    Raises:
        ValueError: If `code` is empty.
    """
    if not code:
        raise ValueError("a splice code cannot be empty")
    return [
        start
        for start in range(len(label) - len(code) + 1)
        if label[start : start + len(code)] == code
    ]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"label  {LABEL}")
    print(f"code   {CODE}")
    print(f"hits   {splice_points(LABEL, CODE)}")
    print()

    for label, code in [("RGRGR", "RGRGR"), ("RGB", "RGRGR"), ("", "RG"), ("BBBB", "BB")]:
        print(f"{label or '(empty)':<8} in-code {code:<6} {splice_points(label, code)}")

    print()
    print(f"long label bands   {len(LONG_LABEL)}")
    print(f"long code bands    {len(LONG_CODE)}")
    print(f"long label hits    {len(splice_points(LONG_LABEL, LONG_CODE))}")

    assert splice_points(LABEL, CODE) == [0, 7, 9]
    assert splice_points("RGRGR", "RGRGR") == [0]
    assert splice_points("RGB", "RGRGR") == []
    assert splice_points("", "RG") == []
    assert splice_points("BBBB", "BB") == [0, 1, 2]
    assert splice_points(LONG_LABEL, LONG_CODE) == splice_points_by_scan(LONG_LABEL, LONG_CODE)
    assert border_table("RGRGR") == [0, 0, 1, 2, 3]

    try:
        splice_points(LABEL, "")
    except ValueError as problem:
        assert str(problem) == "a splice code cannot be empty"
    else:
        raise AssertionError("an empty code should have been rejected")

    print()
    print("All checks passed.")
