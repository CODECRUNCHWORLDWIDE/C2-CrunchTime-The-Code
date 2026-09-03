"""problem-01-ledger-ribbon-solution.py - reading an adding machine's ribbon.

An old adding machine prints a ribbon of digits with no separators between
entries. Each entry is one or two digits and names a till code from 1 to 26.
No entry may start with a zero, because the machine never printed a leading
zero - so a 0 on the ribbon can only ever be the second digit of 10 or 20.

Given a ribbon, count the readings that account for every digit.

The count is built left to right. The number of readings of the first n digits
depends on two things and nothing else: the readings of the first n-1 digits,
when the last digit stands alone as a valid entry, and the readings of the
first n-2, when the last two digits together make a valid entry. That is the
whole recurrence, and it is why one pass and two carried numbers are enough.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Ribbons the shop found in the back of the machine.
RIBBONS: tuple[str, ...] = (
    "1226",
    "1010",
    "2101",
    "111111",
    "27",
    "06",
    "100",
    "2626262626",
)


# ---- Your task ----
def is_entry(digits: str) -> bool:
    """Say whether `digits` is one entry the machine could have printed.

    Args:
        digits: One or two characters from the ribbon.

    Returns:
        True when the digits name a till code from 1 to 26 without a leading
        zero. "0" and "06" are both False; "6" and "06" differ because the
        machine never printed a leading zero.
    """
    if not digits or digits[0] == "0":
        return False
    return 1 <= int(digits) <= 26


def reading_count(ribbon: str) -> int:
    """Count the ways `ribbon` can be read as a run of whole entries.

    Args:
        ribbon: The printed digits, with no separators.

    Returns:
        How many readings account for every digit. Zero when no reading does -
        which is a real answer, not an error. An empty ribbon has exactly one
        reading, the empty one, which is what makes the recurrence start
        cleanly.

    Raises:
        ValueError: If the ribbon holds anything but digits.
    """
    if not ribbon.isdigit() and ribbon != "":
        raise ValueError(f"ribbon {ribbon!r} is not all digits")

    # `two_back` is the count for the ribbon two digits shorter, `one_back` for
    # one digit shorter. Only those two ever matter, so the whole table is two
    # integers rather than a list.
    two_back, one_back = 1, 1
    for index in range(1, len(ribbon) + 1):
        count = 0
        if is_entry(ribbon[index - 1]):
            count += one_back
        if index >= 2 and is_entry(ribbon[index - 2 : index]):
            count += two_back
        two_back, one_back = one_back, count
    return one_back


def reading_table(ribbon: str) -> list[int]:
    """Return the count for every prefix of `ribbon`, shortest first.

    Args:
        ribbon: The printed digits.

    Returns:
        A list of length len(ribbon) + 1. Entry k is the number of readings of
        the first k digits, so entry 0 is 1 and the last entry is the answer.
        Useful for seeing where a ribbon dies: the first 0 in this list is the
        prefix that can no longer be read at all.
    """
    counts = [1] + [0] * len(ribbon)
    for index in range(1, len(ribbon) + 1):
        if is_entry(ribbon[index - 1]):
            counts[index] += counts[index - 1]
        if index >= 2 and is_entry(ribbon[index - 2 : index]):
            counts[index] += counts[index - 2]
    return counts


def first_dead_prefix(ribbon: str) -> int | None:
    """Return the length of the shortest unreadable prefix, or None.

    Args:
        ribbon: The printed digits.

    Returns:
        The length of the shortest prefix with no reading at all, or None when
        every prefix can be read. This is what tells an operator where the
        ribbon went wrong rather than merely that it did.
    """
    for length, count in enumerate(reading_table(ribbon)):
        if count == 0:
            return length
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print("RIBBON READINGS")
    for ribbon in RIBBONS:
        count = reading_count(ribbon)
        dead = first_dead_prefix(ribbon)
        note = "" if dead is None else f"   dead at prefix {dead}"
        print(f"    {ribbon:<12} {count:>4} readings{note}")
    print()

    print("PREFIX TABLE for 1226")
    for length, count in enumerate(reading_table("1226")):
        shown = "1226"[:length] or "(empty)"
        print(f"    {shown:<8} {count}")
    print()

    # 1226 reads as 1-2-2-6, 12-2-6, 1-22-6 and 12-26. Not 1-2-26, which is the
    # same as 1-2-26 already counted, and not 122-6, because 122 is over 26.
    assert reading_count("1226") == 5

    # A zero can only ever be the second digit of 10 or 20.
    assert reading_count("1010") == 1      # 10-10, and nothing else
    assert reading_count("100") == 0       # 10-0 fails; 1-00 fails
    assert reading_count("06") == 0        # no entry starts with a zero
    assert reading_count("2101") == 1      # 21-01 fails, so only 2-10-1

    # 27 cannot be one entry, so it is only 2-7.
    assert reading_count("27") == 1

    # All ones is the counting sequence this whole family is built on: the
    # count for n ones is the (n+1)th Fibonacci number.
    assert [reading_count("1" * n) for n in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]

    # Only every other pair is an entry: "26" is, "62" is not. So the count
    # doubles once per "26" and stands still in between - 2 to the power 5,
    # not a Fibonacci number. Alternating digits are worth checking by hand
    # exactly because they look like they should behave the same as "111111".
    assert reading_count("2626262626") == 32

    # The empty ribbon has one reading: the empty one. That is what makes the
    # recurrence start without a special case.
    assert reading_count("") == 1

    # The table's last entry is the answer, always.
    for ribbon in RIBBONS:
        assert reading_table(ribbon)[-1] == reading_count(ribbon)

    # A dead prefix is reported by length, so an operator knows where to look.
    assert first_dead_prefix("100") == 3
    assert first_dead_prefix("06") == 1
    assert first_dead_prefix("1226") is None

    # Anything that is not digits is refused rather than guessed at.
    for bad in ("12a6", "1 2"):
        try:
            reading_count(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print("All checks passed.")
