"""exercise-03-rota-window-solution.py — counting compliant staffing blocks.

A ward publishes its roster as one role code per shift. Regulation says any
run of len(required) consecutive shifts must be covered by exactly the mix in
`required` — same roles, same counts, order irrelevant.

The window is a fixed size and the state inside it is a frequency table. One
Counter is built once from the requirement; the other is nudged by two keys
per slide. The graded line is the deletion: a key sitting at zero is not the
same as a key that is absent, and Counter equality knows the difference.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def count_compliant_blocks(roster: list[str], required: list[str]) -> int:
    """Return how many staffing blocks in the roster are compliant.

    Args:
        roster: Role codes, one per shift, in chronological order.
        required: The role mix a block must be covered by. Repeats are real
            requirements: two "RN" entries mean two registered nurses.

    Returns:
        The number of contiguous blocks of len(required) shifts whose role
        counts equal the requirement's. Overlapping blocks count separately.
        Zero when the requirement is empty or longer than the roster.
    """
    size = len(required)
    if size == 0 or size > len(roster):
        return 0

    wanted = Counter(required)
    window = Counter(roster[:size])
    compliant = 1 if window == wanted else 0

    for right in range(size, len(roster)):
        window[roster[right]] += 1
        leaving = roster[right - size]
        window[leaving] -= 1
        if window[leaving] == 0:
            del window[leaving]
        if window == wanted:
            compliant += 1

    return compliant


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]),
        (["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]),
        (["RN", "RN", "RN", "LPN"], ["RN", "RN"]),
        (["RN", "RN"], ["LPN"]),
        (["RN"], ["RN", "NA"]),
        (["RN"], []),
        ([], ["RN"]),
    ]
    for roster, required in cases:
        found = count_compliant_blocks(roster, required)
        print(f"required {str(required):<22} roster {str(roster):<44} -> {found}")
    print()

    assert count_compliant_blocks(["RN", "NA", "RN", "LPN", "RN", "NA"], ["RN", "NA"]) == 3
    assert count_compliant_blocks(["RN", "NA", "NA", "RN", "RN", "NA"], ["RN", "RN", "NA"]) == 2
    assert count_compliant_blocks(["RN", "RN", "RN", "LPN"], ["RN", "RN"]) == 2
    assert count_compliant_blocks(["RN", "RN"], ["LPN"]) == 0
    assert count_compliant_blocks(["RN"], ["RN", "NA"]) == 0
    assert count_compliant_blocks(["RN"], []) == 0
    assert count_compliant_blocks([], ["RN"]) == 0

    # The incremental table must agree with rebuilding one per block.
    for roster, required in cases:
        size = len(required)
        if size == 0 or size > len(roster):
            continue
        slow = sum(
            Counter(roster[i : i + size]) == Counter(required)
            for i in range(len(roster) - size + 1)
        )
        assert count_compliant_blocks(roster, required) == slow

    print("All checks passed.")
