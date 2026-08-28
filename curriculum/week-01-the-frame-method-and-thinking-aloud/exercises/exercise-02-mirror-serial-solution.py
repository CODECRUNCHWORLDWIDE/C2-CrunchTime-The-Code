"""exercise-02-mirror-serial-solution.py — where a boarding serial stops mirroring.

Two pointers walk in from the ends of the printed serial, stepping over the
separators the printer sprinkles in. The first pair of significant characters
that disagrees hands back the printed index of its left member.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def first_mirror_break(serial: str) -> int | None:
    """Find where a printed serial first stops reading the same both ways.

    Args:
        serial: The serial exactly as printed, separators included.

    Returns:
        The index in `serial` of the left character of the first outside-in
        pair of significant characters that fails to mirror, or None when
        the serial mirrors — including when it holds no significant
        characters at all.
    """
    left, right = 0, len(serial) - 1
    while left < right:
        while left < right and not serial[left].isalnum():
            left += 1
        while left < right and not serial[right].isalnum():
            right -= 1
        if serial[left].lower() != serial[right].lower():
            return left
        left += 1
        right -= 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    tickets = [
        "RT7-e77-E7tr",
        "RT7-e77-E8tr",
        "8a-b-c8",
        "--G9",
        "Bb",
        "-K-",
        "--  --",
        "",
    ]
    for ticket in tickets:
        where = first_mirror_break(ticket)
        shown = "mirrors" if where is None else f"breaks at index {where}"
        print(f"{ticket!r:>16}  {shown}")

    assert first_mirror_break("RT7-e77-E7tr") is None
    assert first_mirror_break("RT7-e77-E8tr") == 2
    assert first_mirror_break("8a-b-c8") == 1
    assert first_mirror_break("--G9") == 2
    assert first_mirror_break("Bb") is None
    assert first_mirror_break("-K-") is None
    assert first_mirror_break("--  --") is None
    assert first_mirror_break("") is None
    print("All checks passed.")
