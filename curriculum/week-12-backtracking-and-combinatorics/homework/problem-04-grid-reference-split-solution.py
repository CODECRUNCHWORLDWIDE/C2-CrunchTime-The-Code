"""problem-04-grid-reference-split-solution.py - putting the dots back in a reference.

A survey stamps grid references onto marker posts as four numbers separated by
dots. On old posts the dots have worn away and only the digits are left.

Given a run of digits, list every reference it could have been. A reference has
exactly FOUR fields, each field is a number from 0 to 255, and no field may
have a leading zero - "0" is a field and "00" and "01" are not, because the
stamp never struck a leading zero.

The walk has a fixed depth - four - and at each level it tries one, two or
three digits. It prunes three ways, and only one of the three is an
optimisation:

    length prune    with `fields` fields left and `digits` digits left, a
                    branch is dead unless fields <= digits <= 3 * fields
    value prune     a field over 255 is not a field
    zero prune      a field of more than one digit cannot start with 0

The last two are correctness rules dressed as prunes. The first is the only one
you could leave out and still be right, and it is the one that does the work.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
FIELDS = 4
MAX_FIELD = 255

STAMPS: tuple[str, ...] = (
    "25525511135",
    "0000",
    "101023",
    "255255255255",
    "1111",
    "010010",
    "1",
    "12345678901234",
)


# ---- Your task ----
def is_field(digits: str) -> bool:
    """Say whether `digits` is one field the stamp could have struck.

    Args:
        digits: One to three characters from the run.

    Returns:
        True when the digits are a number from 0 to 255 with no leading zero.
        "0" is a field; "00" and "01" are not, and "256" is not.
    """
    if not digits or len(digits) > 3:
        return False
    if len(digits) > 1 and digits[0] == "0":
        return False
    return int(digits) <= MAX_FIELD


def references(run: str) -> tuple[list[str], int]:
    """Return every reference `run` could be, and the nodes visited.

    Args:
        run: The digits left on the post, with no separators.

    Returns:
        A pair: every reference as a dotted string, in walk order, and how many
        nodes the walk entered. A run that cannot be split at all gives an
        empty list, which is a real answer.

    Raises:
        ValueError: If the run holds anything but digits.
    """
    if run and not run.isdigit():
        raise ValueError(f"run {run!r} is not all digits")

    found: list[str] = []
    trail: list[str] = []
    nodes = 0

    def walk(start: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == FIELDS:
            if start == len(run):
                found.append(".".join(trail))
            return

        # The length prune, and it is the only optional one of the three.
        left = FIELDS - len(trail)
        digits_left = len(run) - start
        if not left <= digits_left <= 3 * left:
            return

        for length in (1, 2, 3):
            field = run[start : start + length]
            if len(field) < length:
                break
            if not is_field(field):
                continue
            trail.append(field)
            walk(start + length)
            trail.pop()

    walk(0)
    return found, nodes


def references_unpruned(run: str) -> tuple[list[str], int]:
    """The same walk without the length prune, shipped for the node count.

    Args:
        run: The digits left on the post.

    Returns:
        The same references - this version is correct, only wasteful - and the
        nodes it visited.

    Raises:
        ValueError: If the run holds anything but digits.
    """
    if run and not run.isdigit():
        raise ValueError(f"run {run!r} is not all digits")

    found: list[str] = []
    trail: list[str] = []
    nodes = 0

    def walk(start: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == FIELDS:
            if start == len(run):
                found.append(".".join(trail))
            return
        for length in (1, 2, 3):
            field = run[start : start + length]
            if len(field) < length:
                break
            if not is_field(field):
                continue
            trail.append(field)
            walk(start + length)
            trail.pop()

    walk(0)
    return found, nodes


def readable(run: str) -> bool:
    """Say whether a run could be a reference at all.

    Args:
        run: The digits left on the post.

    Returns:
        True when at least one reading exists. Cheaper to say than to list,
        and it is what a surveyor in the field actually asks first.
    """
    return bool(references(run)[0])


# ---- Self-check ----
if __name__ == "__main__":
    print("WORN POSTS")
    for run in STAMPS:
        found, nodes = references(run)
        _, plain_nodes = references_unpruned(run)
        shown = ", ".join(found) if found else "(no reading)"
        print(f"    {run:<15} {len(found):>2}  nodes {nodes:>3}/{plain_nodes:<3}  {shown}")
    print()

    # The headline post reads two ways.
    found, _ = references("25525511135")
    assert found == ["255.255.11.135", "255.255.111.35"]

    # Every field of every reading is a field, and the fields rejoin to the run.
    for run in STAMPS:
        for reference in references(run)[0]:
            fields = reference.split(".")
            assert len(fields) == FIELDS
            assert all(is_field(field) for field in fields)
            assert "".join(fields) == run

    # A run of four zeroes has exactly one reading, and it is not 00.0.0.0.
    assert references("0000")[0] == ["0.0.0.0"]

    # Leading zeroes are refused, and 010010 is the post that shows what that
    # actually costs. It reads two ways - and neither reading is the obvious
    # 01.00.10 or 0.10.01.0, because no field may open with a zero unless it
    # IS zero. A solution that allows leading zeroes finds several more.
    assert references("010010")[0] == ["0.10.0.10", "0.100.1.0"]
    assert readable("010010") is True
    for reference in references("010010")[0]:
        for field in reference.split("."):
            assert field == "0" or not field.startswith("0")

    # The largest possible reference reads exactly one way.
    assert references("255255255255")[0] == ["255.255.255.255"]

    # Too few digits and too many are both unreadable, and the length prune
    # means the walk barely starts on either.
    assert references("1")[0] == []
    assert references("12345678901234")[0] == []
    short_nodes = references("1")[1]
    assert short_nodes <= 2

    # The prune changes the work and not the answer, on every post.
    for run in STAMPS:
        pruned, pruned_nodes = references(run)
        plain, plain_nodes = references_unpruned(run)
        assert pruned == plain, run
        assert pruned_nodes <= plain_nodes, run
    # ...and on the long unreadable post it is a large difference, which is the
    # whole argument for the prune.
    assert references("12345678901234")[1] < references_unpruned("12345678901234")[1]

    # A field is a field only up to 255 and only without a leading zero.
    assert is_field("0") and is_field("255") and is_field("25")
    assert not is_field("00") and not is_field("01") and not is_field("256")
    assert not is_field("") and not is_field("1234")

    # Anything that is not digits is refused.
    for bad in ("1.2.3.4", "25a5"):
        try:
            references(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print("All checks passed.")
