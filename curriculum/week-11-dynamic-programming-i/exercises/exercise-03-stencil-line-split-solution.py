"""exercise-03-stencil-line-split-solution.py — the widest readable cover.

A depot stencils part codes onto crates as one unbroken run of characters, with
no separators. Sometimes the die slips and leaves marks that are not part of
any code. Given a stencil line and the depot's code book, report the largest
number of characters that can be accounted for by a left-to-right sequence of
whole codes that do not overlap.

Everything not covered is a smudge, and a smudge may sit anywhere.

The file carries the rule twice — a memoized recursion and a bottom-up table —
and checks that they agree.
"""

from __future__ import annotations

import functools

# The Kelbray depot code book.
CODE_BOOK = frozenset(
    {"ZINC", "HEX", "BOLT", "NUT", "WASHER", "PIN", "CLIP", "M8", "M10"}
)

# One crate as the die left it. ZINC HEX BOLT M8, two slipped marks, then
# WASHER PIN.
CRATE_LINE = "ZINCHEXBOLTM8XXWASHERPIN"


def best_cover_cached(line: str, codes: frozenset[str]) -> int:
    """Top-down: the recurrence said out loud, with every answer remembered."""
    lengths = sorted({len(code) for code in codes})

    @functools.cache
    def cover_from(start: int) -> int:
        """The most characters coverable in line[start:]."""
        if start >= len(line):
            return 0
        best = cover_from(start + 1)  # treat line[start] as a smudge
        for width in lengths:
            if start + width <= len(line) and line[start : start + width] in codes:
                best = max(best, width + cover_from(start + width))
        return best

    return cover_from(0)


def best_cover(line: str, codes: frozenset[str]) -> int:
    """Return the most characters of `line` coverable by whole codes.

    Args:
        line: The stencil line, read left to right.
        codes: The depot's code book. May be empty.

    Returns:
        The largest number of characters that a non-overlapping, left-to-right
        sequence of whole codes can account for. Zero if nothing matches.

    Raises:
        ValueError: If the code book contains an empty string, which would
            cover nothing and could be used any number of times.
    """
    if "" in codes:
        raise ValueError("the code book must not contain an empty code")

    lengths = sorted({len(code) for code in codes})
    covered = [0] * (len(line) + 1)
    for end in range(1, len(line) + 1):
        best = covered[end - 1]  # line[end - 1] is a smudge
        for width in lengths:
            if width <= end and line[end - width : end] in codes:
                candidate = covered[end - width] + width
                if candidate > best:
                    best = candidate
        covered[end] = best
    return covered[len(line)]


def cover_table(line: str, codes: frozenset[str]) -> list[int]:
    """The full bottom-up table, kept for the walkthrough on the page."""
    lengths = sorted({len(code) for code in codes})
    covered = [0] * (len(line) + 1)
    for end in range(1, len(line) + 1):
        best = covered[end - 1]
        for width in lengths:
            if width <= end and line[end - width : end] in codes:
                best = max(best, covered[end - width] + width)
        covered[end] = best
    return covered


def _report() -> None:
    """Print the table walk, the checks, and the agreement between the two."""
    short = "NUTXHEX"
    print(f"walking {short!r}")
    print("prefix        covered")
    for end, value in enumerate(cover_table(short, CODE_BOOK)):
        print(f"{short[:end]:<12}  {value}")

    cases: list[tuple[str, int]] = [
        ("", 0),                       # nothing to read
        ("XYZ", 0),                    # no code fits anywhere
        ("NUT", 3),                    # exactly one code, exact fit
        ("XNUT", 3),                   # a smudge in front
        ("NUTX", 3),                   # a smudge behind
        ("M10", 3),                    # M10 beats M8 followed by nothing
        ("M8M10", 5),                  # both, back to back
        ("PINPINPIN", 9),              # a code may repeat
        ("NUTXHEX", 6),                # a smudge in the middle
        ("CLIPINNUT", 7),              # CLIP and PIN overlap: only one may win
        (CRATE_LINE, 22),
    ]
    print()
    for line, expected in cases:
        tabled = best_cover(line, CODE_BOOK)
        recursed = best_cover_cached(line, CODE_BOOK)
        assert tabled == expected, f"{line!r} -> {tabled}, expected {expected}"
        assert recursed == expected, f"cached disagrees on {line!r}"
        gap = len(line) - expected
        print(f"best_cover({line!r:<26}) == {expected:>2}   ({gap} smudged)")

    assert best_cover(CRATE_LINE, frozenset()) == 0
    print("\nan empty code book covers nothing:", best_cover(CRATE_LINE, frozenset()))

    try:
        best_cover("NUT", frozenset({"NUT", ""}))
    except ValueError as problem:
        print(f'an empty code raises ValueError: {problem}')

    print("All checks passed.")


if __name__ == "__main__":
    _report()
