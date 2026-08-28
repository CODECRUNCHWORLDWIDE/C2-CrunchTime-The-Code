"""exercise-05-radio-check-rosters-solution.py — two nights on the coastal net.

The net controller reads out call signs and writes down who answers. Some
stations answer twice, because the first answer was stepped on. Comparing
last night's sheet with tonight's is three questions, and every one of them
is a membership test.

Sets answer the membership question. Lists keep the order. This drill uses
both, on purpose.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

FIRST_NIGHT: list[str] = ["KC4ORT", "W2QRP", "N9TIDE", "W2QRP", "VE3GULL"]
SECOND_NIGHT: list[str] = ["N9TIDE", "K5MOOR", "KC4ORT", "K5MOOR", "W7FOG"]


def both_nights(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard on both nights, in first-night order.

    Args:
        first: Last night's sheet, in the order stations answered.
        second: Tonight's sheet, in the order stations answered.

    Returns:
        Each repeat station once, ordered by when it answered last night.
    """
    tonight = set(second)
    seen: set[str] = set()
    kept: list[str] = []
    for sign in first:
        if sign in tonight and sign not in seen:
            seen.add(sign)
            kept.append(sign)
    return kept


def newcomers(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard tonight and not last night.

    Args:
        first: Last night's sheet.
        second: Tonight's sheet, in the order stations answered.

    Returns:
        Each new station once, ordered by when it answered tonight.
    """
    last_night = set(first)
    seen: set[str] = set()
    kept: list[str] = []
    for sign in second:
        if sign not in last_night and sign not in seen:
            seen.add(sign)
            kept.append(sign)
    return kept


def went_silent(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard last night and not tonight.

    Args:
        first: Last night's sheet, in the order stations answered.
        second: Tonight's sheet.

    Returns:
        Each missing station once, ordered by when it answered last night.
    """
    tonight = set(second)
    seen: set[str] = set()
    kept: list[str] = []
    for sign in first:
        if sign not in tonight and sign not in seen:
            seen.add(sign)
            kept.append(sign)
    return kept


def net_size(sheet: list[str]) -> int:
    """Return how many different stations a sheet holds.

    Args:
        sheet: One night's sheet, duplicates and all.

    Returns:
        The count of distinct call signs on it.
    """
    return len(set(sheet))


# ---- Self-check ----
if __name__ == "__main__":
    print(f"both nights : {', '.join(both_nights(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"new tonight : {', '.join(newcomers(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"went silent : {', '.join(went_silent(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"distinct    : {net_size(FIRST_NIGHT)} last night, {net_size(SECOND_NIGHT)} tonight")

    assert both_nights(FIRST_NIGHT, SECOND_NIGHT) == ["KC4ORT", "N9TIDE"]
    assert newcomers(FIRST_NIGHT, SECOND_NIGHT) == ["K5MOOR", "W7FOG"]
    assert went_silent(FIRST_NIGHT, SECOND_NIGHT) == ["W2QRP", "VE3GULL"]
    assert net_size(FIRST_NIGHT) == 4
    assert net_size(SECOND_NIGHT) == 4
    assert both_nights([], SECOND_NIGHT) == []
    assert newcomers(FIRST_NIGHT, []) == []
    assert went_silent(FIRST_NIGHT, []) == ["KC4ORT", "W2QRP", "N9TIDE", "VE3GULL"]
    assert FIRST_NIGHT[1] == "W2QRP"  # both sheets are untouched
    print("All checks passed.")
