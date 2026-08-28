"""exercise-03-callsign-stub-solution.py — the shortest callsign stub.

Harbour control wants the shortest opening letters that still name exactly one
vessel. Build a prefix tree that remembers how many callsigns pass through
each node, then walk each callsign until the count drops to one.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"
PASSES = "#"

StubTree = dict

CALLSIGNS: list[str] = [
    "KELPIE",
    "KELVIN",
    "KESTREL",
    "KESTRELTWO",
    "MARLIN",
    "MARLOW",
    "NARWHAL",
]


def build_stub_tree(callsigns: list[str]) -> StubTree:
    """Return a prefix tree in which every node counts the callsigns through it.

    Args:
        callsigns: Distinct vessel callsigns.

    Returns:
        The root node. Each node carries PASSES, and END where a callsign stops.

    Raises:
        ValueError: If two callsigns are the same.
    """
    seen: set[str] = set()
    root: StubTree = {PASSES: 0}
    for callsign in callsigns:
        if callsign in seen:
            raise ValueError(f"callsign {callsign} was registered twice")
        seen.add(callsign)
        node = root
        node[PASSES] += 1
        for letter in callsign:
            node = node.setdefault(letter, {PASSES: 0})
            node[PASSES] += 1
        node[END] = True
    return root


def shortest_stub(root: StubTree, callsign: str) -> str:
    """Return the shortest opening letters that name only this callsign.

    Args:
        root: A tree built by `build_stub_tree`, holding this callsign.
        callsign: The callsign to shorten.

    Returns:
        The shortest prefix reaching a node with exactly one callsign through
        it. When no such prefix exists — because the callsign is the opening of
        a longer one — the whole callsign is returned.
    """
    node = root
    for cut, letter in enumerate(callsign, start=1):
        node = node[letter]
        if node[PASSES] == 1:
            return callsign[:cut]
    return callsign


def all_stubs(callsigns: list[str]) -> dict[str, str]:
    """Return every callsign paired with its shortest stub.

    Args:
        callsigns: Distinct vessel callsigns.

    Returns:
        A dict from callsign to stub, in the order the callsigns arrived.
    """
    root = build_stub_tree(callsigns)
    return {callsign: shortest_stub(root, callsign) for callsign in callsigns}


def count_nodes(root: StubTree) -> int:
    """Return how many nodes the tree holds, counting the root.

    Args:
        root: Any node. Called on the root, it counts the whole tree.

    Returns:
        The number of dicts in the tree. END and PASSES are not nodes.
    """
    total = 1
    for key, child in root.items():
        if key not in (END, PASSES):
            total += count_nodes(child)
    return total


# ---- Self-check ----
if __name__ == "__main__":
    stubs = all_stubs(CALLSIGNS)
    for callsign, stub in stubs.items():
        cut = "whole callsign" if stub == callsign else f"{len(stub)} of {len(callsign)}"
        print(f"{callsign:<11} -> {stub:<11} ({cut})")

    tree = build_stub_tree(CALLSIGNS)
    letters = sum(len(callsign) for callsign in CALLSIGNS)
    print()
    print(f"letters stamped  {letters:>3}")
    print(f"nodes in tree    {count_nodes(tree):>3}")

    assert stubs == {
        "KELPIE": "KELP",
        "KELVIN": "KELV",
        "KESTREL": "KESTREL",
        "KESTRELTWO": "KESTRELT",
        "MARLIN": "MARLI",
        "MARLOW": "MARLO",
        "NARWHAL": "N",
    }
    assert all_stubs(["SOLO"]) == {"SOLO": "S"}
    assert all_stubs(["TIDE", "TIDEWAY"]) == {"TIDE": "TIDE", "TIDEWAY": "TIDEW"}

    try:
        build_stub_tree(["MARLIN", "MARLIN"])
    except ValueError as problem:
        assert str(problem) == "callsign MARLIN was registered twice"
    else:
        raise AssertionError("a repeated callsign should have been rejected")

    print()
    print("All checks passed.")
