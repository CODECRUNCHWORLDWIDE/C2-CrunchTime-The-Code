"""problem-03-symmetric-dies-solution.py — where does the mirror break?

Same first two moves as this week's booklet challenge: find the earlier of
the two middle dies, cut there, and turn the back half around. Only the
third move differs. Instead of zipping the halves together, walk them side
by side and stop at the first pair whose codes disagree.

Then put the press back the way you found it. A safety check that leaves the
die chain scrambled has become a fault.

The chains are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per die sequence, then
"All checks passed."
"""

from __future__ import annotations


class Die:
    """One stamping die, in press order."""

    def __init__(self, code: str, next_die: "Die | None" = None) -> None:
        self.code = code
        self.next_die = next_die


def build_press(codes: list[str]) -> Die | None:
    """Wire a die chain from a list of codes.

    Args:
        codes: One code per die, in press order. Codes repeat freely.

    Returns:
        The first die, or None for an empty press.
    """
    if not codes:
        return None
    dies = [Die(code) for code in codes]
    for earlier, later in zip(dies, dies[1:]):
        earlier.next_die = later
    return dies[0]


def press_codes(first: Die | None) -> list[str]:
    """Walk a die chain into a list of codes, in press order."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.code)
        first = first.next_die
    return codes


def _lower_middle(first: Die) -> Die:
    """Return the last die of the front half — the earlier of two middles."""
    slow = first
    fast = first
    while fast.next_die is not None and fast.next_die.next_die is not None:
        slow = slow.next_die
        fast = fast.next_die.next_die
    return slow


def _reverse(first: Die | None) -> Die | None:
    """Turn a die chain around in place and return its new first die."""
    previous = None
    current = first
    while current is not None:
        following = current.next_die
        current.next_die = previous
        previous = current
        current = following
    return previous


def first_mirror_break(first: Die | None) -> int:
    """Return the position of the first die that differs from its mirror.

    Args:
        first: The first die of the press chain, or None for an empty press.

    Returns:
        The 0-based position, counted from the front, of the first die whose
        mirror partner carries a different code, or -1 when the whole
        sequence reads the same in either direction. The chain is left in
        its original order either way.
    """
    if first is None or first.next_die is None:
        return -1

    middle = _lower_middle(first)
    back = middle.next_die
    middle.next_die = None
    turned = _reverse(back)

    front_walk: Die | None = first
    back_walk = turned
    position = 0
    answer = -1
    while back_walk is not None:
        if front_walk.code != back_walk.code:
            answer = position
            break
        front_walk = front_walk.next_die
        back_walk = back_walk.next_die
        position += 1

    middle.next_die = _reverse(turned)
    return answer


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["A", "B", "B", "A"], -1),
        (["A", "B", "C", "B", "A"], -1),
        (["A"], -1),
        ([], -1),
        (["A", "B"], 0),
        (["A", "B", "C", "A"], 1),
        (["A", "B", "B", "C"], 0),
        (["X", "Y", "Z", "Y", "X", "Q"], 0),
    ]

    for codes, expected in CASES:
        press = build_press(codes)
        found = first_mirror_break(press)
        assert found == expected, f"{codes}: got {found}, wanted {expected}"
        assert press_codes(press) == codes, f"{codes}: the press was left scrambled"
        verdict = "symmetric" if found == -1 else f"breaks at position {found}"
        print(f"{str(codes):<36} {verdict}")

    long_press = build_press(["S"] * 9999 + ["T"])
    assert first_mirror_break(long_press) == 0
    assert len(press_codes(long_press)) == 10_000
    print(f"{'10000 dies, one odd one at the end':<36} breaks at position 0")

    print("All checks passed.")
