"""exercise-01-gate-tag-tree-solution.py — the canal gate tag register.

Build a prefix tree out of nothing but nested dictionaries, count what it
costs in nodes, then answer two questions with it: is this exact tag
registered, and is anything at all registered below this prefix.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# A node is a plain dict. Every key is one letter leading to a child node,
# except END, which marks "a tag stops here".
END = "*"

# One node of the tree. The values are either child nodes or the END flag,
# so the annotation is deliberately loose.
TagTree = dict

GATE_TAGS: list[str] = [
    "MARSH",
    "MARSHEND",
    "MARSHGATE",
    "MILL",
    "MILLPOND",
    "MILLRACE",
    "MOOR",
    "MOORHEN",
]


def build_tag_tree(tags: list[str]) -> TagTree:
    """Return a prefix tree holding every tag.

    Args:
        tags: The gate tags to register. Order does not matter.

    Returns:
        The root node — a dict, empty when `tags` is empty.

    Raises:
        ValueError: If any tag is the empty string.
    """
    root: TagTree = {}
    for tag in tags:
        if not tag:
            raise ValueError("a gate tag cannot be the empty string")
        node = root
        for letter in tag:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def count_nodes(root: TagTree) -> int:
    """Return how many nodes the tree holds, counting the root.

    Args:
        root: Any node. Called on the root, it counts the whole tree.

    Returns:
        The number of dicts in the tree. END flags are not nodes.
    """
    total = 1
    for key, child in root.items():
        if key != END:
            total += count_nodes(child)
    return total


def is_registered(root: TagTree, tag: str) -> bool:
    """Return True when `tag` was registered exactly.

    Args:
        root: The root of the tree.
        tag: The tag to look up.

    Returns:
        True only when the walk finishes and an END flag sits there.
    """
    node = root
    for letter in tag:
        if letter not in node:
            return False
        node = node[letter]
    return END in node


def any_registered_under(root: TagTree, prefix: str) -> bool:
    """Return True when at least one registered tag starts with `prefix`.

    Args:
        root: The root of the tree.
        prefix: The prefix to test. The empty prefix matches everything.

    Returns:
        True when the walk survives to the end of `prefix`.
    """
    node = root
    for letter in prefix:
        if letter not in node:
            return False
        node = node[letter]
    return True


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_tag_tree(GATE_TAGS)
    letters = sum(len(tag) for tag in GATE_TAGS)
    nodes = count_nodes(tree)

    print(f"tags registered  {len(GATE_TAGS):>3}")
    print(f"letters stamped  {letters:>3}")
    print(f"nodes in tree    {nodes:>3}")
    print(f"nodes saved      {letters + 1 - nodes:>3}")
    print()

    for tag in ["MARSH", "MARSHY", "MILL", "MOO", "MOORHEN"]:
        print(f"registered {tag:<9} {'yes' if is_registered(tree, tag) else 'no'}")
    print()

    for prefix in ["MAR", "MOOR", "MUD", ""]:
        shown = prefix if prefix else "(empty)"
        answer = "yes" if any_registered_under(tree, prefix) else "no"
        print(f"anything under {shown:<9} {answer}")

    assert nodes == 30
    assert letters == 53
    assert is_registered(tree, "MARSH") is True
    assert is_registered(tree, "MARSHY") is False
    assert is_registered(tree, "MOO") is False
    assert any_registered_under(tree, "MOO") is True
    assert any_registered_under(tree, "MUD") is False
    assert any_registered_under(tree, "") is True
    assert count_nodes(build_tag_tree([])) == 1

    try:
        build_tag_tree(["MARSH", ""])
    except ValueError as problem:
        assert str(problem) == "a gate tag cannot be the empty string"
    else:
        raise AssertionError("an empty tag should have been rejected")

    print()
    print("All checks passed.")
