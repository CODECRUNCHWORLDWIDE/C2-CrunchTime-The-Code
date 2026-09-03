"""problem-03-sluice-pairing-solution.py - every legal run of a paired sluice.

A drainage board runs a bank of sluices. Every gate that is OPENED has to be
CLOSED again before the run ends, and a gate can never be closed that was not
opened - the linkage will not allow it.

Given a number of gates, list every legal sequence of opens and closes.

The interesting part is that the walk prunes on a COUNT rather than on a set.
There is no list of which gates are open, because the gates are
interchangeable - only how many are open matters. Two rules follow, and between
them they make every branch the walk takes legal, so nothing has to be checked
at the end:

    open a gate    while any remain unopened
    close a gate   while more have been opened than closed

That second rule is the one that does the work. A walk that generates every
sequence of opens and closes and filters the illegal ones afterwards gets the
same answer for far more effort - and the file counts the nodes of both so the
difference is a number.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
GATES = 3
OPEN, CLOSE = "<", ">"


# ---- Your task ----
def legal_runs(gates: int) -> tuple[list[str], int]:
    """Return every legal run of `gates` gates, and the nodes visited.

    Args:
        gates: How many gates the run opens and closes. Must not be negative.

    Returns:
        A pair: every legal sequence, in walk order, and how many nodes the
        walk entered. Zero gates has one run, the empty one, which is what
        makes the recurrence start without a special case.

    Raises:
        ValueError: If `gates` is negative.
    """
    if gates < 0:
        raise ValueError("a run cannot have a negative number of gates")

    found: list[str] = []
    trail: list[str] = []
    nodes = 0

    def walk(opened: int, closed: int) -> None:
        nonlocal nodes
        nodes += 1
        if closed == gates:
            found.append("".join(trail))
            return
        if opened < gates:
            trail.append(OPEN)
            walk(opened + 1, closed)
            trail.pop()
        if closed < opened:
            trail.append(CLOSE)
            walk(opened, closed + 1)
            trail.pop()

    walk(0, 0)
    return found, nodes


def legal_runs_by_filter(gates: int) -> tuple[list[str], int]:
    """Every sequence of the right length, filtered afterwards. For comparison.

    Args:
        gates: How many gates the run opens and closes.

    Returns:
        The same runs - this version is correct, only wasteful - and the nodes
        it visited. Generating all 2 ** (2 * gates) sequences and keeping the
        legal ones is the answer to name and reject in the write-up, and the
        node counts are what make the rejection concrete.

    Raises:
        ValueError: If `gates` is negative.
    """
    if gates < 0:
        raise ValueError("a run cannot have a negative number of gates")

    found: list[str] = []
    trail: list[str] = []
    nodes = 0

    def walk() -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == 2 * gates:
            run = "".join(trail)
            if is_legal(run):
                found.append(run)
            return
        for symbol in (OPEN, CLOSE):
            trail.append(symbol)
            walk()
            trail.pop()

    walk()
    return found, nodes


def is_legal(run: str) -> bool:
    """Say whether a run could actually be worked, without generating anything.

    Args:
        run: A sequence of opens and closes.

    Returns:
        True when every close has an open before it and nothing is left open at
        the end. Written independently of the walk on purpose: a verifier that
        shares the generator's assumptions verifies nothing.
    """
    standing = 0
    for symbol in run:
        if symbol == OPEN:
            standing += 1
        elif symbol == CLOSE:
            standing -= 1
            if standing < 0:
                return False
        else:
            return False
    return standing == 0


def deepest_standing(run: str) -> int:
    """Return the most gates standing open at once during a run.

    Args:
        run: A sequence of opens and closes.

    Returns:
        The high-water mark. This is the number the drainage board actually
        cares about, because it is how much water is in the system at once.
    """
    standing = deepest = 0
    for symbol in run:
        if symbol == OPEN:
            standing += 1
            deepest = max(deepest, standing)
        else:
            standing -= 1
    return deepest


# ---- Self-check ----
if __name__ == "__main__":
    runs, nodes = legal_runs(GATES)
    _, filtered_nodes = legal_runs_by_filter(GATES)

    print(f"GATES  {GATES}")
    print()

    print("EVERY LEGAL RUN")
    for run in runs:
        print(f"    {run}   deepest {deepest_standing(run)}")
    print()

    print("PRUNING AGAINST FILTERING")
    print(f"    nodes, pruned as we go : {nodes}")
    print(f"    nodes, filtered at the end: {filtered_nodes}")
    print()

    print("HOW MANY RUNS PER GATE COUNT")
    for count in range(7):
        print(f"    {count} gates: {len(legal_runs(count)[0]):>4}")
    print()

    # Three gates give five legal runs. The counts across gate numbers are the
    # Catalan numbers, which is worth naming in the write-up because it is what
    # tells you the answer grows fast but nothing like 2 ** 2n.
    assert len(runs) == 5
    assert [len(legal_runs(count)[0]) for count in range(7)] == [1, 1, 2, 5, 14, 42, 132]

    # Every run the walk produces is legal, checked independently.
    for run in runs:
        assert is_legal(run)
        assert len(run) == 2 * GATES

    # Every run appears exactly once.
    assert len(set(runs)) == len(runs)

    # The pruned and filtered walks agree on the answer and not on the work.
    filtered, _ = legal_runs_by_filter(GATES)
    assert sorted(filtered) == sorted(runs)
    assert nodes < filtered_nodes

    # Zero gates is one run, the empty one.
    assert legal_runs(0)[0] == [""]

    # One gate has exactly one legal run.
    assert legal_runs(1)[0] == ["<>"]

    # The verifier is not fooled by the obvious wrong sequences.
    assert is_legal("<<>>") is True
    assert is_legal("><") is False        # closes a gate that was never opened
    assert is_legal("<<>") is False       # leaves one standing at the end
    assert is_legal("<x>") is False       # not a run at all

    # The deepest standing level is 1 for the fully alternating run and `gates`
    # for the one that opens everything first.
    assert deepest_standing("<><><>") == 1
    assert deepest_standing("<<<>>>") == 3

    # A negative gate count is refused.
    for function in (legal_runs, legal_runs_by_filter):
        try:
            function(-1)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
