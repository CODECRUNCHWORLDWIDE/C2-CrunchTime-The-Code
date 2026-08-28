"""exercise-04-beacon-flash-period-solution.py — the beacon flash period.

A harbour beacon repeats a fixed block of long and short flashes. Given a
recorded strip, find the shortest block that, repeated a whole number of
times, reproduces the strip exactly.

The tool is the border table: for every cut of the strip, how long is the
longest opening run that is also the closing run. One pass builds it. The
obvious nested-loop version does the same job and gets slower and slower.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

STRIPS: list[str] = [
    "LSSLSSLSSLSS",
    "LSSLSSLSSL",
    "LLLL",
    "LSLS",
    "L",
    "LSSL",
    "SLLSSLLSLLSSLL",
]

# A long strip built to punish the nested-loop scan: a wall of long flashes,
# one short flash in the middle, then the same wall again.
LONG_STRIP: str = "L" * 600 + "S" + "L" * 600


def border_table(strip: str) -> tuple[list[int], int]:
    """Return the border length at every cut of `strip`, plus the work done.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair. First, a list as long as `strip`, where entry `i` is the length
        of the longest run that both opens and closes `strip[:i + 1]` without
        being the whole of it. Second, how many single-character comparisons
        the pass made.

    Raises:
        ValueError: If `strip` is empty.
    """
    if not strip:
        raise ValueError("a flash strip cannot be empty")
    size = len(strip)
    table = [0] * size
    comparisons = 0
    cursor = 1
    matched = 0
    while cursor < size:
        comparisons += 1
        if strip[cursor] == strip[matched]:
            matched += 1
            table[cursor] = matched
            cursor += 1
        elif matched:
            matched = table[matched - 1]
        else:
            table[cursor] = 0
            cursor += 1
    return table, comparisons


def naive_longest_border(strip: str) -> tuple[int, int]:
    """Return the longest border of `strip` the slow way, plus the work done.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair: the longest border length, and how many single-character
        comparisons the nested loops made.

    Raises:
        ValueError: If `strip` is empty.
    """
    if not strip:
        raise ValueError("a flash strip cannot be empty")
    size = len(strip)
    comparisons = 0
    for length in range(size - 1, 0, -1):
        fits = True
        for offset in range(length):
            comparisons += 1
            if strip[offset] != strip[size - length + offset]:
                fits = False
                break
        if fits:
            return length, comparisons
    return 0, comparisons


def shortest_block(strip: str) -> tuple[str, int]:
    """Return the shortest repeating block of `strip` and how often it repeats.

    Args:
        strip: The recorded flashes. Must not be empty.

    Returns:
        A pair: the block, and the number of whole repeats. When no shorter
        block tiles the strip, the strip itself is the block and the count is 1.

    Raises:
        ValueError: If `strip` is empty.
    """
    table, _ = border_table(strip)
    size = len(strip)
    step = size - table[-1]
    if size % step == 0:
        return strip[:step], size // step
    return strip, 1


# ---- Self-check ----
if __name__ == "__main__":
    for strip in STRIPS:
        block, repeats = shortest_block(strip)
        print(f"{strip:<15} block {block:<8} x{repeats}")

    slow_border, slow_cost = naive_longest_border(LONG_STRIP)
    fast_table, fast_cost = border_table(LONG_STRIP)
    print()
    print(f"long strip flashes    {len(LONG_STRIP):>7}")
    print(f"longest border        {slow_border:>7}")
    print(f"nested-loop compares  {slow_cost:>7}")
    print(f"one-pass compares     {fast_cost:>7}")
    print(f"times cheaper         {slow_cost // fast_cost:>7}")

    assert shortest_block("LSSLSSLSSLSS") == ("LSS", 4)
    assert shortest_block("LSSLSSLSSL") == ("LSSLSSLSSL", 1)
    assert shortest_block("LLLL") == ("L", 4)
    assert shortest_block("LSLS") == ("LS", 2)
    assert shortest_block("L") == ("L", 1)
    assert shortest_block("LSSL") == ("LSSL", 1)
    assert border_table("LSSLSSLSSLSS")[0] == [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert fast_table[-1] == slow_border
    assert fast_cost < slow_cost

    try:
        shortest_block("")
    except ValueError as problem:
        assert str(problem) == "a flash strip cannot be empty"
    else:
        raise AssertionError("an empty strip should have been rejected")

    print()
    print("All checks passed.")
