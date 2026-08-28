"""problem-01-banner-copy-count-solution.py — count the copying, do not time it.

A sign painter builds a banner out of five-letter strips. Built with `+=`,
every strip forces the whole banner so far to be copied into a new string.
Built with `"".join`, every character is copied exactly once.

This program does not time anything. It counts characters copied, which is
the same number on every machine, so the table below is a fact rather than a
weather report.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

WORDS = ("BLOOM", "SEEDS", "GROWS", "HERBS", "ROOTS")
SIZES = (4, 8, 16, 32)


def strips(count: int) -> list[str]:
    """Return `count` banner strips, cycling through the five words.

    Args:
        count: How many strips the banner is made of.

    Returns:
        A list of five-character strings.
    """
    return [WORDS[index % len(WORDS)] for index in range(count)]


def copies_by_concat(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `+=`.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        The total number of characters copied. Each `+=` builds a brand new
        string, so it copies everything glued so far plus the new strip.
    """
    copied = 0
    banner = ""
    for piece in pieces:
        copied += len(banner) + len(piece)
        banner += piece
    return copied


def copies_by_join(pieces: list[str]) -> int:
    """Count the characters copied when the banner is built with `join`.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        The total number of characters copied. `join` measures first,
        allocates once, and copies each character exactly once.
    """
    return sum(len(piece) for piece in pieces)


def build_banner(pieces: list[str]) -> str:
    """Return the finished banner, built the cheap way.

    Args:
        pieces: The strips, in the order they are glued on.

    Returns:
        Every strip end to end.
    """
    return "".join(pieces)


def table(sizes: tuple[int, ...]) -> str:
    """Render the copy counts and how they grow.

    Args:
        sizes: Strip counts to report, each double the one before.

    Returns:
        A header line and one line per size. No trailing newline.
    """
    rows = [f"{'strips':>6}  {'+= copies':>10}  {'join copies':>11}  {'+= x':>5}  {'join x':>6}"]
    previous: tuple[int, int] | None = None
    for count in sizes:
        pieces = strips(count)
        concat = copies_by_concat(pieces)
        joined = copies_by_join(pieces)
        if previous is None:
            growth = f"{'-':>5}  {'-':>6}"
        else:
            growth = f"{concat / previous[0]:>5.2f}  {joined / previous[1]:>6.2f}"
        rows.append(f"{count:>6}  {concat:>10}  {joined:>11}  {growth}")
        previous = (concat, joined)
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(table(SIZES))

    pieces = strips(32)
    assert len(pieces) == 32
    assert build_banner(strips(3)) == "BLOOMSEEDSGROWS"
    assert copies_by_join(pieces) == 160  # 32 strips of 5, copied once each
    assert copies_by_concat(pieces) == 2640  # 5 * 32 * 33 // 2
    assert copies_by_concat(strips(64)) == 5 * 64 * 65 // 2
    assert copies_by_concat([]) == 0
    assert copies_by_join([]) == 0
    assert build_banner([]) == ""
    print("All checks passed.")
