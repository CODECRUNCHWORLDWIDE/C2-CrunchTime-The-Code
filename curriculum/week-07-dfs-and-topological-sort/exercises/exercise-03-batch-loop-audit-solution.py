"""exercise-03-batch-loop-audit-solution.py — find a loop in a cannery's batch plan.

Three-colour depth-first search, carried on an explicit stack so a five
thousand stage plan cannot overflow CPython's thousand-frame recursion limit.
White is a stage nobody has started, grey is a stage on the path you are
standing on right now, black is a stage that is finished and proved clean. A
hop to a grey stage is a loop. A hop to a black stage is not.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

from collections.abc import Iterator

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
CLEAN_DIAMOND: dict[str, list[str]] = {
    "wash": ["blanch", "cook"],
    "blanch": ["fill"],
    "cook": ["fill"],
    "fill": ["seal"],
}

SELF_FEED: dict[str, list[str]] = {
    "retort": ["retort"],
}

SIMPLE_LOOP: dict[str, list[str]] = {
    "wash": ["fill"],
    "fill": ["seal"],
    "seal": ["retort"],
    "retort": ["fill"],
}

ROTATED_LOOP: dict[str, list[str]] = {
    "intake": ["press"],
    "press": ["soak"],
    "soak": ["mash"],
    "mash": ["press"],
}


def long_plan(stages: int, loop_back: bool) -> dict[str, list[str]]:
    """Build a plan that is one straight chain of `stages` stages.

    Args:
        stages: How many stages the chain holds.
        loop_back: When True the last stage feeds the first, closing the chain
            into one enormous loop.

    Returns:
        A feed table keyed by zero-padded stage names, so alphabetical order
        and chain order agree.
    """
    plan: dict[str, list[str]] = {}
    for index in range(stages - 1):
        plan[f"stage-{index:05d}"] = [f"stage-{index + 1:05d}"]
    if loop_back:
        plan[f"stage-{stages - 1:05d}"] = ["stage-00000"]
    return plan


# ---- Your task ----
def find_feed_loop(feeds: dict[str, list[str]]) -> list[str] | None:
    """Return the stages of one feed loop, or None when the plan has none.

    Args:
        feeds: Maps a stage name to the stages it feeds. A stage that appears
            only as a target and never as a key is still a stage.

    Returns:
        The stages of one loop in feed order, rotated so the list starts at the
        alphabetically smallest stage in that loop, with that stage not
        repeated at the end. None when no loop exists. Start stages are tried
        in sorted order and each stage's fed stages are walked in sorted order;
        the first loop found under that rule is the one returned.
    """
    stages: set[str] = set(feeds)
    for targets in feeds.values():
        stages.update(targets)
    colour: dict[str, int] = {stage: WHITE for stage in stages}

    for root in sorted(stages):
        if colour[root] != WHITE:
            continue
        colour[root] = GREY
        path: list[str] = [root]
        pending: list[tuple[str, Iterator[str]]] = [
            (root, iter(sorted(feeds.get(root, []))))
        ]
        while pending:
            stage, targets = pending[-1]
            descended = False
            for fed in targets:
                if colour[fed] == GREY:
                    loop = path[path.index(fed) :]
                    pivot = min(range(len(loop)), key=lambda spot: loop[spot])
                    return loop[pivot:] + loop[:pivot]
                if colour[fed] == WHITE:
                    colour[fed] = GREY
                    path.append(fed)
                    pending.append((fed, iter(sorted(feeds.get(fed, [])))))
                    descended = True
                    break
                # colour[fed] == BLACK: finished elsewhere, already proved clean.
            if not descended:
                colour[stage] = BLACK
                path.pop()
                pending.pop()
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty plan     : {find_feed_loop({})}")
    print(f"clean diamond  : {find_feed_loop(CLEAN_DIAMOND)}")
    print(f"self feed      : {find_feed_loop(SELF_FEED)}")
    print(f"simple loop    : {find_feed_loop(SIMPLE_LOOP)}")
    print(f"rotated loop   : {find_feed_loop(ROTATED_LOOP)}")

    clean_chain = find_feed_loop(long_plan(5_000, loop_back=False))
    closed_chain = find_feed_loop(long_plan(5_000, loop_back=True))
    print(f"5000 clean     : {clean_chain}")
    assert closed_chain is not None
    print(
        f"5000 looped    : {len(closed_chain)} stages, "
        f"{closed_chain[0]} .. {closed_chain[-1]}"
    )

    assert find_feed_loop({}) is None
    assert find_feed_loop({"wash": []}) is None
    assert find_feed_loop(CLEAN_DIAMOND) is None
    assert find_feed_loop(SELF_FEED) == ["retort"]
    assert find_feed_loop(SIMPLE_LOOP) == ["fill", "seal", "retort"]
    assert find_feed_loop(ROTATED_LOOP) == ["mash", "press", "soak"]
    assert clean_chain is None
    assert len(closed_chain) == 5_000
    assert closed_chain[0] == "stage-00000"
    assert closed_chain[-1] == "stage-04999"
    print("All checks passed.")
