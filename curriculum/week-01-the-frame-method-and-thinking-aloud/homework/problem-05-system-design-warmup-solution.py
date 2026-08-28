"""problem-05-system-design-warmup-solution.py — the short code inside a URL shortener.

The design sketch is the written half of this problem. This is the one piece
of it you can actually build in forty minutes: turning a row number into a
short code, and turning it back again.

Base 62 is ordinary place-value arithmetic with sixty-two digits instead of
ten. Nothing here is random, nothing is hashed, and no two row numbers can
collide, because the conversion is reversible.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode(row: int) -> str:
    """Turn a row number into its base-62 short code.

    Args:
        row: The row's number in the links table. Zero or more.

    Returns:
        The short code, shortest first digit first. Row 0 encodes to "0".

    Raises:
        ValueError: If `row` is negative. There is no row before the first.
    """
    if row < 0:
        raise ValueError(f"row numbers start at 0, got {row}")
    if row == 0:
        return ALPHABET[0]

    digits: list[str] = []
    while row > 0:
        row, remainder = divmod(row, BASE)
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(code: str) -> int:
    """Turn a short code back into its row number.

    Args:
        code: A short code produced by `encode`.

    Returns:
        The row number it came from.

    Raises:
        ValueError: If the code is empty or holds a character that is not in
            the alphabet. A typo must fail loudly rather than resolve to
            somebody else's link.
    """
    if not code:
        raise ValueError("a short code cannot be empty")

    row = 0
    for character in code:
        position = ALPHABET.find(character)
        if position < 0:
            raise ValueError(f"{character!r} is not a base-62 digit")
        row = row * BASE + position
    return row


def codes_available(length: int) -> int:
    """How many distinct codes exist at exactly this many characters.

    Args:
        length: The code length in characters. Zero or more.

    Returns:
        62 to the power of `length`, which is the count of codes of that
        length or shorter, including the leading-zero forms.
    """
    return BASE**length


# ---- Self-check ----
if __name__ == "__main__":
    for row in [0, 1, 61, 62, 3843, 3844, 916_132_831, 916_132_832]:
        code = encode(row)
        print(f"row {row:>11}  ->  {code:<7}  ->  row {decode(code)}")

    print()
    for length in range(1, 8):
        print(f"{length} characters covers {codes_available(length):>14,} links")

    assert encode(0) == "0"
    assert encode(1) == "1"
    assert encode(61) == "z"
    assert encode(62) == "10"
    assert decode("0") == 0
    assert decode("z") == 61
    assert decode("10") == 62
    assert all(decode(encode(row)) == row for row in range(5000))
    assert len({encode(row) for row in range(5000)}) == 5000

    try:
        encode(-1)
    except ValueError as error:
        assert "start at 0" in str(error)
    else:
        raise AssertionError("encode(-1) should have raised")

    try:
        decode("hello world")
    except ValueError as error:
        assert "not a base-62 digit" in str(error)
    else:
        raise AssertionError("decode of a bad code should have raised")

    try:
        decode("")
    except ValueError:
        pass
    else:
        raise AssertionError("decode of an empty code should have raised")

    print()
    print("All checks passed.")
