"""challenge-02-berth-ledger-shorthand-solution.py — longest stem wins.

The harbourmaster's ledger is full of long berth names. The office keeps a
list of registered stems, and the house rule is that a berth name is written
down as the LONGEST registered stem that opens it.

So with QUAY and QUAYSIDE both registered, QUAYSIDEWEST is filed as QUAYSIDE,
not as QUAY. Stopping at the first stem you meet is the whole trap.

The line comes back rewritten, along with how many names were shortened and
which names matched no stem at all.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

StemTree = dict

STEMS: list[str] = [
    "NORTH",
    "QUAY",
    "QUAYSIDE",
    "DRY",
    "DRYDOCK",
    "LAY",
]

LEDGER: list[str] = [
    "NORTHGATE QUAYSIDEWEST DRYDOCKTWO LAYBY GRAINSILO QUAY",
    "DRY DRYDOCK DRYDOCKING",
    "PONTOON RAMP",
]


def build_stem_tree(stems: list[str]) -> StemTree:
    """Return a prefix tree holding every registered stem.

    Args:
        stems: The stems the office has registered. Duplicates are harmless.

    Returns:
        The root node.

    Raises:
        ValueError: If any stem is the empty string.
    """
    root: StemTree = {}
    for stem in stems:
        if not stem:
            raise ValueError("a stem cannot be the empty string")
        node = root
        for letter in stem:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def longest_stem(root: StemTree, name: str) -> str:
    """Return the longest registered stem that opens `name`, or "".

    Args:
        root: A tree of registered stems.
        name: The berth name to shorten.

    Returns:
        The longest prefix of `name` that is a registered stem. The empty
        string when no stem opens it.
    """
    node = root
    best = ""
    for cut, letter in enumerate(name, start=1):
        if letter not in node:
            break
        node = node[letter]
        if END in node:
            best = name[:cut]
    return best


def shorten(root: StemTree, line: str) -> tuple[str, int, list[str]]:
    """Rewrite one ledger line with every berth name cut back to its stem.

    Args:
        root: A tree of registered stems.
        line: One ledger line: berth names separated by single spaces.

    Returns:
        A triple. The rewritten line; how many names were actually made
        shorter; and the names no stem opened, first appearance first, with
        no repeats. A name that already equals its stem is neither shortened
        nor unmatched.

    Raises:
        ValueError: If `line` is empty.
    """
    if not line:
        raise ValueError("a ledger line cannot be empty")
    rewritten: list[str] = []
    shortened = 0
    unmatched: list[str] = []
    for name in line.split(" "):
        stem = longest_stem(root, name)
        if not stem:
            rewritten.append(name)
            if name not in unmatched:
                unmatched.append(name)
            continue
        rewritten.append(stem)
        if stem != name:
            shortened += 1
    return " ".join(rewritten), shortened, unmatched


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_stem_tree(STEMS)
    for line in LEDGER:
        rewritten, shortened, unmatched = shorten(tree, line)
        print(f"in   {line}")
        print(f"out  {rewritten}")
        print(f"     shortened {shortened}, unmatched {unmatched}")
        print()

    assert shorten(tree, LEDGER[0]) == (
        "NORTH QUAYSIDE DRYDOCK LAY GRAINSILO QUAY",
        4,
        ["GRAINSILO"],
    )
    assert shorten(tree, LEDGER[1]) == ("DRY DRYDOCK DRYDOCK", 1, [])
    assert shorten(tree, LEDGER[2]) == ("PONTOON RAMP", 0, ["PONTOON", "RAMP"])
    assert shorten(tree, "PONTOON PONTOON") == ("PONTOON PONTOON", 0, ["PONTOON"])
    assert longest_stem(tree, "QUAYSIDEWEST") == "QUAYSIDE"
    assert longest_stem(tree, "QUA") == ""
    assert longest_stem(tree, "SILO") == ""

    try:
        shorten(tree, "")
    except ValueError as problem:
        assert str(problem) == "a ledger line cannot be empty"
    else:
        raise AssertionError("an empty line should have been rejected")

    try:
        build_stem_tree(["NORTH", ""])
    except ValueError as problem:
        assert str(problem) == "a stem cannot be the empty string"
    else:
        raise AssertionError("an empty stem should have been rejected")

    print("All checks passed.")
