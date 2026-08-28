"""problem-06-tool-crib-signoffs-solution.py — who may run which machine.

The makerspace keeps one set of signed-off tools per member. Every question
the crib gets asked is set algebra: what have we got, what can everybody
run, what rests on one person, and can this member take this job.

Sets answer all four. Sorting happens once, at the very end, only because a
printed line has to be in some order.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import Counter

SIGNOFFS: dict[str, set[str]] = {
    "ama": {"lathe", "bandsaw", "drill press"},
    "bo": {"bandsaw", "drill press", "laser"},
    "cai": {"bandsaw", "lathe", "welder", "drill press"},
}

JOB: set[str] = {"bandsaw", "welder"}


def all_tools(signoffs: dict[str, set[str]]) -> set[str]:
    """Return every tool somebody is signed off on.

    Args:
        signoffs: A member's name to the set of tools they may run.

    Returns:
        The union of every member's set.
    """
    covered: set[str] = set()
    for tools in signoffs.values():
        covered |= tools
    return covered


def everyone_can_run(signoffs: dict[str, set[str]]) -> set[str]:
    """Return the tools every member is signed off on.

    Args:
        signoffs: A member's name to the set of tools they may run.

    Returns:
        The intersection of every member's set. An empty set when the crib
        has no members at all.
    """
    sets = list(signoffs.values())
    if not sets:
        return set()
    return set.intersection(*sets)


def single_point_of_failure(signoffs: dict[str, set[str]]) -> list[str]:
    """Return the tools exactly one member can run.

    Args:
        signoffs: A member's name to the set of tools they may run.

    Returns:
        Those tool names, sorted A to Z. These are the ones that stop the
        shop when that member is away.
    """
    tally: Counter[str] = Counter()
    for tools in signoffs.values():
        tally.update(tools)
    return sorted(tool for tool, holders in tally.items() if holders == 1)


def missing_for(job: set[str], tools: set[str]) -> list[str]:
    """Return what a member still needs before taking a job.

    Args:
        job: The tools the job calls for.
        tools: The tools this member is signed off on.

    Returns:
        The shortfall, sorted A to Z. Empty when the member can take it.
    """
    return sorted(job - tools)


# ---- Self-check ----
if __name__ == "__main__":
    print(f"all tools : {', '.join(sorted(all_tools(SIGNOFFS)))}")
    print(f"everyone  : {', '.join(sorted(everyone_can_run(SIGNOFFS)))}")
    print(f"only one  : {', '.join(single_point_of_failure(SIGNOFFS))}")
    print(f"job needs : {', '.join(sorted(JOB))}")
    for member in sorted(SIGNOFFS):
        gap = missing_for(JOB, SIGNOFFS[member])
        verdict = "can take it" if not gap else f"missing {', '.join(gap)}"
        print(f"  {member:<4} {verdict}")

    assert all_tools(SIGNOFFS) == {"bandsaw", "drill press", "laser", "lathe", "welder"}
    assert everyone_can_run(SIGNOFFS) == {"bandsaw", "drill press"}
    assert single_point_of_failure(SIGNOFFS) == ["laser", "welder"]
    assert missing_for(JOB, SIGNOFFS["cai"]) == []
    assert missing_for(JOB, SIGNOFFS["ama"]) == ["welder"]
    assert JOB <= SIGNOFFS["cai"]  # the subset test says the same thing
    assert not (JOB <= SIGNOFFS["bo"])
    assert all_tools({}) == set()
    assert everyone_can_run({}) == set()
    assert SIGNOFFS["ama"] == {"lathe", "bandsaw", "drill press"}  # nobody was changed
    print("All checks passed.")
