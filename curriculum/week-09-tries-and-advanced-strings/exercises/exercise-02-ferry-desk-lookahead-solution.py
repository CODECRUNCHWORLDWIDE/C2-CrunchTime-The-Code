"""exercise-02-ferry-desk-lookahead-solution.py — the ferry desk lookahead.

A clerk types the first few letters of a destination code and the kiosk shows
the codes that start that way, A to Z, at most `limit` of them.

The walk stops the moment `limit` codes are in hand, which is why the file
reports how many nodes each lookahead touched.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

DESTINATIONS: list[str] = [
    "BRIDGEND",
    "BRIDGEPORT",
    "BRIDGEWATER",
    "BRINE",
    "BROADSANDS",
    "BROADWAY",
    "BURNTISLAND",
]


def build_code_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every destination code.

    Args:
        codes: The codes to register. Duplicates are harmless.

    Returns:
        The root node.
    """
    root: CodeTree = {}
    for code in codes:
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def descend(root: CodeTree, prefix: str) -> CodeTree | None:
    """Return the node the prefix ends at, or None when it runs off the tree.

    Args:
        root: The root of the tree.
        prefix: The letters typed so far.

    Returns:
        The node reached, or None when some letter has no child.
    """
    node = root
    for letter in prefix:
        if letter not in node:
            return None
        node = node[letter]
    return node


def codes_with_prefix(root: CodeTree, prefix: str, limit: int) -> tuple[list[str], int]:
    """Return up to `limit` registered codes starting with `prefix`, A to Z.

    Args:
        root: The root of the tree.
        prefix: The letters typed so far. The empty prefix matches everything.
        limit: The most codes to return. Zero returns nothing at all.

    Returns:
        A pair: the codes found, and how many nodes the walk entered.
    """
    found: list[str] = []
    visited = 0
    start = descend(root, prefix)
    if start is None or limit <= 0:
        return found, visited

    def walk(node: CodeTree, spelled: str) -> None:
        nonlocal visited
        if len(found) == limit:
            return
        visited += 1
        if END in node:
            found.append(prefix + spelled)
            if len(found) == limit:
                return
        for letter in sorted(key for key in node if key != END):
            walk(node[letter], spelled + letter)
            if len(found) == limit:
                return

    walk(start, "")
    return found, visited


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_code_tree(DESTINATIONS)

    for prefix, limit in [("BR", 3), ("BR", 99), ("BRIDGE", 2), ("BU", 5), ("BX", 5), ("", 2)]:
        codes, visited = codes_with_prefix(tree, prefix, limit)
        shown = prefix if prefix else "(empty)"
        print(f"{shown:<8} limit {limit:<3} nodes {visited:>3}  {codes}")

    three, _ = codes_with_prefix(tree, "BR", 3)
    assert three == ["BRIDGEND", "BRIDGEPORT", "BRIDGEWATER"]

    everything, _ = codes_with_prefix(tree, "BR", 99)
    assert everything == [
        "BRIDGEND",
        "BRIDGEPORT",
        "BRIDGEWATER",
        "BRINE",
        "BROADSANDS",
        "BROADWAY",
    ]

    capped, capped_nodes = codes_with_prefix(tree, "BR", 2)
    _, full_nodes = codes_with_prefix(tree, "BR", 99)
    assert capped == ["BRIDGEND", "BRIDGEPORT"]
    assert capped_nodes < full_nodes  # the cap really did stop the walk early

    assert codes_with_prefix(tree, "BX", 5) == ([], 0)
    assert codes_with_prefix(tree, "BR", 0) == ([], 0)
    assert codes_with_prefix(tree, "BURNTISLAND", 5) == (["BURNTISLAND"], 1)

    root_first, _ = codes_with_prefix(tree, "", 2)
    assert root_first == ["BRIDGEND", "BRIDGEPORT"]

    print()
    print("All checks passed.")
