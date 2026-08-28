"""problem-02-growable-dock-sign-solution.py — the sign that grows a letter at a time.

A dock sign is built by sliding letter tiles on, one at a time, left to right.
Every stage has to be a code the harbour already recognises — you cannot show
a half-finished word to the public.

Given the register of codes, find the longest sign that can be built this way,
and report the whole build, stage by stage.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

REGISTER: list[str] = [
    "B",
    "BE",
    "BER",
    "BERT",
    "BERTH",
    "D",
    "DO",
    "DOC",
    "DOCK",
    "DOCKS",
    "Q",
    "QU",
    "QUAY",
    "TIDE",
]


def build_register_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every recognised code.

    Args:
        codes: The register. Duplicates are harmless.

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


def longest_build(root: CodeTree) -> list[str]:
    """Return the stages of the longest sign that can be built a letter at a time.

    Args:
        root: A tree of recognised codes.

    Returns:
        The stages, shortest first, ending with the finished sign. Where two
        builds are equally long, the one that compares smaller stage by stage
        wins. Empty when no single letter is a recognised code.
    """
    best: list[str] = []

    def walk(node: CodeTree, stages: list[str]) -> None:
        nonlocal best
        if len(stages) > len(best) or (len(stages) == len(best) and stages < best):
            best = list(stages)
        for letter in sorted(key for key in node if key != END):
            child = node[letter]
            if END not in child:
                continue  # this stage would not be a recognised code
            stages.append((stages[-1] if stages else "") + letter)
            walk(child, stages)
            stages.pop()

    walk(root, [])
    return best


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_register_tree(REGISTER)
    stages = longest_build(tree)
    for step, stage in enumerate(stages, start=1):
        print(f"stage {step}  {stage}")
    print()
    print(f"longest sign  {stages[-1] if stages else '(none)'}")
    print(f"stages        {len(stages)}")

    assert stages == ["B", "BE", "BER", "BERT", "BERTH"]

    gapped = build_register_tree(["Q", "QU", "QUAY"])
    assert longest_build(gapped) == ["Q", "QU"]

    assert longest_build(build_register_tree(["TIDE"])) == []
    assert longest_build(build_register_tree([])) == []

    tied = build_register_tree(["A", "AB", "Z", "ZY"])
    assert longest_build(tied) == ["A", "AB"]

    print()
    print("All checks passed.")
