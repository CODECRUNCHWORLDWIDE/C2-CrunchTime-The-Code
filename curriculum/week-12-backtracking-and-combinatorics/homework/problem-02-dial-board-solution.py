"""problem-02-dial-board-solution.py - what a half-remembered extension could be.

An old works telephone has letters printed on its dial keys. Somebody remembers
which KEYS they pressed for an extension but not which letter each press was
meant to be, so every press could be any of the letters on that key.

List every extension the presses could have meant.

The walk has one level per press rather than one per item, and at each level it
tries every letter on that key. Nothing is ever skipped and nothing is ever
pruned - every branch runs to the bottom - which makes this the cleanest place
to see that the SHAPE of the tree comes from the problem and not from the
template. The template is the same three lines it has always been.

The count is the product of the letters on each key pressed, which is worth
computing before the walk: four presses on three-letter keys is 81 extensions
and eight presses is over six thousand.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# The dial. Keys 1 and 0 carry no letters at all - they are the operator and
# the exchange, and nobody dials a letter on them.
DIAL: dict[str, str] = {
    "1": "",
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
    "0": "",
}

PRESSES = "273"


# ---- Your task ----
def extensions(presses: str, dial: dict[str, str]) -> list[str]:
    """Return every extension the presses could have meant.

    Args:
        presses: The keys pressed, in order.
        dial: The dial, mapping each key to the letters printed on it.

    Returns:
        Every extension, in dial order. No presses means no extensions at all -
        an empty list, not a list holding the empty string, because nobody
        dialled anything.

    Raises:
        KeyError: If a press names a key the dial does not have.
        ValueError: If a press names a key carrying no letters, which cannot
            contribute a character and would silently shorten every answer.
    """
    if not presses:
        return []

    for key in presses:
        if key not in dial:
            raise KeyError(f"the dial has no key {key!r}")
        if not dial[key]:
            raise ValueError(f"key {key!r} carries no letters")

    found: list[str] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        if index == len(presses):
            found.append("".join(trail))
            return
        for letter in dial[presses[index]]:
            trail.append(letter)          # choose
            walk(index + 1)               # explore
            trail.pop()                   # undo

    walk(0)
    return found


def extension_count(presses: str, dial: dict[str, str]) -> int:
    """Return how many extensions exist, without enumerating them.

    Args:
        presses: The keys pressed.
        dial: The dial.

    Returns:
        The product of the letter counts, or 0 for no presses. Kept beside the
        enumeration so the two can check each other, and so the growth can be
        printed before anything is walked.
    """
    if not presses:
        return 0
    total = 1
    for key in presses:
        total *= len(dial.get(key, ""))
    return total


def extensions_matching(presses: str, dial: dict[str, str], opening: str) -> list[str]:
    """Return the possible extensions starting with a remembered opening.

    Args:
        presses: The keys pressed.
        dial: The dial.
        opening: Letters the caller is sure the extension starts with.

    Returns:
        The matching extensions, which is what makes this useful rather than
        merely long: remembering one letter cuts the list by the size of a key.
    """
    return [word for word in extensions(presses, dial) if word.startswith(opening)]


# ---- Self-check ----
if __name__ == "__main__":
    found = extensions(PRESSES, DIAL)

    print(f"PRESSES  {PRESSES}")
    print("    " + "   ".join(f"{key}={DIAL[key]}" for key in PRESSES))
    print()

    print(f"EVERY EXTENSION ({len(found)})")
    for start in range(0, len(found), 9):
        print("    " + "  ".join(found[start : start + 9]))
    print()

    print("HOW FAST THIS GROWS")
    for length in range(1, 7):
        keys = "7" * length
        print(f"    {length} presses on key 7: {extension_count(keys, DIAL):>6}")
    print()

    print("REMEMBERING ONE LETTER")
    print(f"    starts with A: {extensions_matching(PRESSES, DIAL, 'A')}")
    print()

    # 3 letters on 2, 4 on 7, 3 on 3: 3 * 4 * 3 = 36.
    assert len(found) == extension_count(PRESSES, DIAL) == 36

    # Every extension is one letter per press, and each letter is on its key.
    for word in found:
        assert len(word) == len(PRESSES)
        for letter, key in zip(word, PRESSES):
            assert letter in DIAL[key]

    # Every extension appears exactly once, and they come out in dial order.
    assert len(set(found)) == len(found)
    assert found == sorted(found)

    # Remembering the first letter divides the list by the letters on key 2.
    assert len(extensions_matching(PRESSES, DIAL, "A")) == 12
    assert len(extensions_matching(PRESSES, DIAL, "AP")) == 3
    assert extensions_matching(PRESSES, DIAL, "Z") == []

    # One press gives one extension per letter on that key.
    assert extensions("9", DIAL) == ["W", "X", "Y", "Z"]

    # No presses means nobody dialled, so there is nothing to report - not one
    # empty extension. That is a decision, and it is the one the docstring
    # makes; the opposite convention would make the count 1 rather than 0.
    assert extensions("", DIAL) == []
    assert extension_count("", DIAL) == 0

    # A key with no letters cannot contribute a character. Accepting it would
    # silently shorten every answer, so it is refused instead.
    for bad in ("21", "0", "230"):
        try:
            extensions(bad, DIAL)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    # A key that is not on the dial at all is a different mistake.
    try:
        extensions("2*", DIAL)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for a key not on the dial")

    print("All checks passed.")
