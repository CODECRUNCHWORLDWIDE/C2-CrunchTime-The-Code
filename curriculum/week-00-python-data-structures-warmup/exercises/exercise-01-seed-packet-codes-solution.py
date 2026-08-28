"""exercise-01-seed-packet-codes-solution.py — tidy the seed library's codes.

Four small string functions: clean a handwritten packet code into blocks of
four, count what had to be thrown away, say whether the packet was donated,
and lay one shelf line out.

Nothing here changes a string, because nothing can. Every function builds a
new string and hands it back.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

BLOCK = 4

RAW_PACKETS: list[str] = [
    "don 4417 kale",
    "buy-2210-tomato",
    "  DON 0001  ",
    "???",
    "bee balm #7",
    "sage 12",
]


def clean_code(raw: str) -> str:
    """Return the tidy form of one handwritten packet code.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The kept letters and digits, upper-cased, in blocks of four joined
        by "-". An empty string when nothing survives.
    """
    kept = [ch.upper() for ch in raw if ch.isalnum()]
    blocks = ["".join(kept[start:start + BLOCK]) for start in range(0, len(kept), BLOCK)]
    return "-".join(blocks)


def dropped_count(raw: str) -> int:
    """Return how many characters the cleaner threw away.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The number of characters in `raw` that were not letters or digits.
    """
    return sum(1 for ch in raw if not ch.isalnum())


def is_donation(code: str) -> bool:
    """Return True when a cleaned code begins with the donation marker.

    Args:
        code: A cleaned code, as returned by `clean_code`.

    Returns:
        True when the code starts with "DON", otherwise False.
    """
    return code.startswith("DON")


def shelf_line(raw: str) -> str:
    """Return one line of the shelf listing for a raw code.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The cleaned code padded to 16 characters, then "donated" or
        "bought", then how many characters were dropped.
    """
    code = clean_code(raw)
    shown = code if code else "(empty)"
    source = "donated" if is_donation(code) else "bought"
    return f"{shown:<16}  {source}  {dropped_count(raw)} dropped"


# ---- Self-check ----
if __name__ == "__main__":
    for raw in RAW_PACKETS:
        print(shelf_line(raw))

    assert clean_code("don 4417 kale") == "DON4-417K-ALE"
    assert clean_code("buy-2210-tomato") == "BUY2-210T-OMAT-O"
    assert clean_code("???") == ""
    assert clean_code("") == ""
    assert dropped_count("  DON 0001  ") == 5
    assert dropped_count("sage 12") == 1
    assert dropped_count("") == 0
    assert is_donation(clean_code("don 4417 kale"))
    assert not is_donation(clean_code("buy-2210-tomato"))
    assert RAW_PACKETS[0] == "don 4417 kale"  # the raw scans are untouched
    print("All checks passed.")
