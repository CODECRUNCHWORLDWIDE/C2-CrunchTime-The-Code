# Week 12 — Homework

Six problems, all original, each with a runnable worked answer folded under it.
Allow about five hours. Do each with the lectures closed; open the reveal only
after your own version runs, or after fifteen minutes stuck on one step.

The six carry on from the exercises: a fixed-size choice, a fixed-depth product,
a count-based prune, a fixed split with three prunes, both dedup rules at once,
and the constraint-satisfaction shape.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Tasting Panel](#problem-1--the-tasting-panel) | Subsets of a fixed size, and the short-branch prune | 40 min |
| 2 | [The Dial Board](#problem-2--the-dial-board) | One level per position, every option at each | 35 min |
| 3 | [The Sluice Pairing](#problem-3--the-sluice-pairing) | Pruning on a count rather than a set | 50 min |
| 4 | [The Grid Reference Split](#problem-4--the-grid-reference-split) | Fixed depth, variable width, three prunes | 55 min |
| 5 | [The Tare Weight Picks](#problem-5--the-tare-weight-picks) | Both rules at once — each item once, and no duplicates | 55 min |
| 6 | [The Test Tray Fill](#problem-6--the-test-tray-fill) | Constraint satisfaction, and where the check goes | 55 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, copy the code out of its reveal
into a file of your own and run that:

```bash
python problem-01-tasting-panel.py
```

---

## Problem 1 — The Tasting Panel

**The brief.** A pottery co-operative picks a tasting panel from its members.
The panel holds exactly `size` people, and **who** is on it matters while the
order does not.

**The data.** Six members — Ada, Bram, Cato, Devi, Enid, Fen — and a panel of
three.

**Constraints.** A panel of zero is one panel, the empty one. A panel bigger than
the roster cannot be formed at all.

**Answer.** [Exercise 1](../exercises/exercise-01-glaze-sample-set.md) with the
size fixed, which changes two things. The recording moves from every node to the
nodes where the trail is full. And a new prune becomes possible: **once there are
not enough members left to fill the panel, the branch is dead however it
continues**, so it can be abandoned before it is walked.

Six choose three is 20 panels. The prune does not change that; it changes the
number of nodes, and the file prints both so the saving is a number.

**Signatures.** `panels(members, size)`, `panels_unpruned(members, size)`,
`panels_with(members, size, member)`, `panel_count(members, size)`.

**Watch for.** Recording at every node as in Exercise 1 — you get all 64 subsets
rather than the 20 panels. Pruning with `<` where `<=` belongs, which drops the
panels that use exactly the remaining members. Each member should sit on exactly
10 of the 20, which is a check worth doing because it does not depend on your
implementation.

The sizes across the whole roster come out as 1, 6, 15, 20, 15, 6, 1 and sum to
64 — Exercise 1's answer arrived at from the other direction.

<details>
<summary>Worked answer — <code>problem-01-tasting-panel-solution.py</code></summary>

```python
"""problem-01-tasting-panel-solution.py - every panel of a fixed size.

A pottery co-operative picks a tasting panel from its members. The panel must
hold exactly `size` people, and who is on it matters while the order does not -
a panel of Ada, Bram and Cato is the same panel however it is written down.

List every panel, and count the walk.

This is Exercise 1's subset walk with a size fixed, which changes two things.
The recording moves from every node to the nodes where the trail is full. And a
new prune becomes possible: once there are not enough members left to fill the
panel, the branch is dead however it continues, so it can be abandoned before
it is walked.

That prune is worth a printed number rather than a claim, so the file counts
nodes with and without it.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

from math import comb

# ---- Given data ----
MEMBERS: tuple[str, ...] = ("Ada", "Bram", "Cato", "Devi", "Enid", "Fen")
PANEL_SIZE = 3


# ---- Your task ----
def panels(members: tuple[str, ...], size: int) -> tuple[list[list[str]], int]:
    """Return every panel of exactly `size` members, and the nodes visited.

    Args:
        members: The co-operative's members, in roster order.
        size: How many people the panel holds.

    Returns:
        A pair: every panel, each in roster order, and how many nodes the walk
        entered. A size of zero has one panel, the empty one; a size larger
        than the roster has none.

    Raises:
        ValueError: If `size` is negative.
    """
    if size < 0:
        raise ValueError("a panel cannot have a negative size")

    found: list[list[str]] = []
    trail: list[str] = []
    nodes = 0

    def walk(index: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == size:
            found.append(list(trail))
            return
        # The prune: if every remaining member joined, would the panel still be
        # short? Then this branch cannot produce a panel and is not walked.
        for next_index in range(index, len(members)):
            if len(members) - next_index < size - len(trail):
                break
            trail.append(members[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found, nodes


def panels_unpruned(members: tuple[str, ...], size: int) -> tuple[list[list[str]], int]:
    """The same walk without the short-branch prune, shipped for the node count.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.

    Returns:
        The same panels - this version is correct, only wasteful - and the
        nodes it visited.

    Raises:
        ValueError: If `size` is negative.
    """
    if size < 0:
        raise ValueError("a panel cannot have a negative size")

    found: list[list[str]] = []
    trail: list[str] = []
    nodes = 0

    def walk(index: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == size:
            found.append(list(trail))
            return
        for next_index in range(index, len(members)):
            trail.append(members[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found, nodes


def panels_with(members: tuple[str, ...], size: int, member: str) -> list[list[str]]:
    """Return the panels that include a given member.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.
        member: The member who must be on the panel.

    Returns:
        The matching panels. Empty when the member is not on the roster.
    """
    found, _ = panels(members, size)
    return [panel for panel in found if member in panel]


def panel_count(members: tuple[str, ...], size: int) -> int:
    """Return how many panels exist, without enumerating them.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.

    Returns:
        The binomial coefficient. Kept beside the enumeration so the two can
        check each other.
    """
    if size < 0 or size > len(members):
        return 0
    return comb(len(members), size)


# ---- Self-check ----
if __name__ == "__main__":
    found, nodes = panels(MEMBERS, PANEL_SIZE)
    _, unpruned_nodes = panels_unpruned(MEMBERS, PANEL_SIZE)

    print(f"MEMBERS  {list(MEMBERS)}     PANEL SIZE  {PANEL_SIZE}")
    print()

    print("EVERY PANEL")
    for panel in found:
        print("    " + ", ".join(panel))
    print()

    print("WHAT THE SHORT-BRANCH PRUNE SAVES")
    print(f"    nodes with the prune : {nodes}")
    print(f"    nodes without it     : {unpruned_nodes}")
    print()

    print("PANELS BY SIZE")
    for size in range(len(MEMBERS) + 1):
        print(f"    {size}: {len(panels(MEMBERS, size)[0])}")
    print()

    # Six members choose three is twenty panels.
    assert len(found) == panel_count(MEMBERS, PANEL_SIZE) == 20

    # Every panel is the right size, in roster order, and appears once.
    order = {member: index for index, member in enumerate(MEMBERS)}
    for panel in found:
        assert len(panel) == PANEL_SIZE
        assert [order[member] for member in panel] == sorted(order[member] for member in panel)
    assert len({tuple(panel) for panel in found}) == len(found)

    # The prune changes the work and not the answer.
    unpruned, _ = panels_unpruned(MEMBERS, PANEL_SIZE)
    assert unpruned == found
    assert nodes < unpruned_nodes

    # Each member sits on the same number of panels: 20 * 3 / 6 = 10.
    for member in MEMBERS:
        assert len(panels_with(MEMBERS, PANEL_SIZE, member)) == 10

    # A member who is not on the roster is on no panel.
    assert panels_with(MEMBERS, PANEL_SIZE, "Gwil") == []

    # A panel of nobody is one panel, the empty one.
    assert panels(MEMBERS, 0)[0] == [[]]

    # A panel bigger than the roster cannot be formed at all.
    assert panels(MEMBERS, 7)[0] == []
    assert panel_count(MEMBERS, 7) == 0

    # The sizes across the whole roster are the binomial row, and they sum to
    # the number of subsets - which is Exercise 1's answer, arrived at from the
    # other direction.
    sizes = [len(panels(MEMBERS, size)[0]) for size in range(len(MEMBERS) + 1)]
    assert sizes == [1, 6, 15, 20, 15, 6, 1]
    assert sum(sizes) == 2 ** len(MEMBERS)

    # A negative size is refused rather than quietly returning nothing.
    try:
        panels(MEMBERS, -1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative panel size")

    print("All checks passed.")
```

</details>
---

## Problem 2 — The Dial Board

**The brief.** An old works telephone has letters printed on its dial keys.
Somebody remembers which **keys** they pressed for an extension but not which
letter each press was meant to be. List every extension the presses could have
meant.

**The data.** The dial, with keys 1 and 0 carrying no letters at all, and the
presses `273`.

**Constraints.** A key carrying no letters cannot contribute a character, so a
press on 1 or 0 is refused rather than skipped — skipping it would silently
shorten every answer. No presses means nobody dialled, so the answer is an empty
list rather than a list holding the empty string. That is a decision, and the
opposite convention would make the count 1 rather than 0.

**Answer.** One level per press rather than one per item, and at each level try
every letter on that key. Nothing is skipped and nothing is pruned — every branch
runs to the bottom.

That makes this the cleanest place to see that the **shape of the tree comes
from the problem**, not from the template. The three lines are the same three
lines they have been all week.

`273` gives 36 extensions: `3 × 4 × 3`, one factor per key.

**Signatures.** `extensions(presses, dial)`, `extension_count(presses, dial)`,
`extensions_matching(presses, dial, opening)`.

**Watch for.** Skipping a letterless key instead of refusing it. Treating the
empty press string as one empty extension. The answers should come out in dial
order without a sort — if you need to sort them, the loop is wrong.

<details>
<summary>Worked answer — <code>problem-02-dial-board-solution.py</code></summary>

```python
"""problem-02-dial-board-solution.py - what a half-remembered extension could be.

An old works telephone has letters printed on its dial keys. Somebody remembers
which KEYS they pressed for an extension but not which letter each press was
meant to be, so every press could be any of the letters on that key.

List every extension the presses could have meant.

The walk has one level per press rather than one per item, and at each level it
tries every letter on that key. Nothing is ever skipped and nothing is ever
pruned - every branch runs to the bottom - which makes this the cleanest place
to see that the SHAPE of the tree comes from the problem and not from the
template. The template is the same three lines it has always been.

The count is the product of the letters on each key pressed, which is worth
computing before the walk: four presses on three-letter keys is 81 extensions
and eight presses is over six thousand.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# The dial. Keys 1 and 0 carry no letters at all - they are the operator and
# the exchange, and nobody dials a letter on them.
DIAL: dict[str, str] = {
    "1": "",
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
    "0": "",
}

PRESSES = "273"


# ---- Your task ----
def extensions(presses: str, dial: dict[str, str]) -> list[str]:
    """Return every extension the presses could have meant.

    Args:
        presses: The keys pressed, in order.
        dial: The dial, mapping each key to the letters printed on it.

    Returns:
        Every extension, in dial order. No presses means no extensions at all -
        an empty list, not a list holding the empty string, because nobody
        dialled anything.

    Raises:
        KeyError: If a press names a key the dial does not have.
        ValueError: If a press names a key carrying no letters, which cannot
            contribute a character and would silently shorten every answer.
    """
    if not presses:
        return []

    for key in presses:
        if key not in dial:
            raise KeyError(f"the dial has no key {key!r}")
        if not dial[key]:
            raise ValueError(f"key {key!r} carries no letters")

    found: list[str] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        if index == len(presses):
            found.append("".join(trail))
            return
        for letter in dial[presses[index]]:
            trail.append(letter)          # choose
            walk(index + 1)               # explore
            trail.pop()                   # undo

    walk(0)
    return found


def extension_count(presses: str, dial: dict[str, str]) -> int:
    """Return how many extensions exist, without enumerating them.

    Args:
        presses: The keys pressed.
        dial: The dial.

    Returns:
        The product of the letter counts, or 0 for no presses. Kept beside the
        enumeration so the two can check each other, and so the growth can be
        printed before anything is walked.
    """
    if not presses:
        return 0
    total = 1
    for key in presses:
        total *= len(dial.get(key, ""))
    return total


def extensions_matching(presses: str, dial: dict[str, str], opening: str) -> list[str]:
    """Return the possible extensions starting with a remembered opening.

    Args:
        presses: The keys pressed.
        dial: The dial.
        opening: Letters the caller is sure the extension starts with.

    Returns:
        The matching extensions, which is what makes this useful rather than
        merely long: remembering one letter cuts the list by the size of a key.
    """
    return [word for word in extensions(presses, dial) if word.startswith(opening)]


# ---- Self-check ----
if __name__ == "__main__":
    found = extensions(PRESSES, DIAL)

    print(f"PRESSES  {PRESSES}")
    print("    " + "   ".join(f"{key}={DIAL[key]}" for key in PRESSES))
    print()

    print(f"EVERY EXTENSION ({len(found)})")
    for start in range(0, len(found), 9):
        print("    " + "  ".join(found[start : start + 9]))
    print()

    print("HOW FAST THIS GROWS")
    for length in range(1, 7):
        keys = "7" * length
        print(f"    {length} presses on key 7: {extension_count(keys, DIAL):>6}")
    print()

    print("REMEMBERING ONE LETTER")
    print(f"    starts with A: {extensions_matching(PRESSES, DIAL, 'A')}")
    print()

    # 3 letters on 2, 4 on 7, 3 on 3: 3 * 4 * 3 = 36.
    assert len(found) == extension_count(PRESSES, DIAL) == 36

    # Every extension is one letter per press, and each letter is on its key.
    for word in found:
        assert len(word) == len(PRESSES)
        for letter, key in zip(word, PRESSES):
            assert letter in DIAL[key]

    # Every extension appears exactly once, and they come out in dial order.
    assert len(set(found)) == len(found)
    assert found == sorted(found)

    # Remembering the first letter divides the list by the letters on key 2.
    assert len(extensions_matching(PRESSES, DIAL, "A")) == 12
    assert len(extensions_matching(PRESSES, DIAL, "AP")) == 3
    assert extensions_matching(PRESSES, DIAL, "Z") == []

    # One press gives one extension per letter on that key.
    assert extensions("9", DIAL) == ["W", "X", "Y", "Z"]

    # No presses means nobody dialled, so there is nothing to report - not one
    # empty extension. That is a decision, and it is the one the docstring
    # makes; the opposite convention would make the count 1 rather than 0.
    assert extensions("", DIAL) == []
    assert extension_count("", DIAL) == 0

    # A key with no letters cannot contribute a character. Accepting it would
    # silently shorten every answer, so it is refused instead.
    for bad in ("21", "0", "230"):
        try:
            extensions(bad, DIAL)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    # A key that is not on the dial at all is a different mistake.
    try:
        extensions("2*", DIAL)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for a key not on the dial")

    print("All checks passed.")
```

</details>
---

## Problem 3 — The Sluice Pairing

**The brief.** A drainage board runs a bank of sluices. Every gate **opened**
must be **closed** before the run ends, and a gate can never be closed that was
not opened — the linkage will not allow it. List every legal sequence of opens
and closes.

**The data.** Three gates.

**Constraints.** Zero gates is one run, the empty one.

**Answer.** The interesting part is that the walk prunes on a **count** rather
than a set. There is no list of which gates are open, because the gates are
interchangeable — only how many are open matters. Two rules:

```text
open a gate     while any remain unopened
close a gate    while more have been opened than closed
```

Between them, every branch the walk takes is legal, so nothing has to be checked
at the end.

The alternative — generate every sequence of opens and closes and filter — gets
the same five answers for **127 nodes against 22**. The file prints both.

Three gates give five runs, and the counts across gate numbers are 1, 1, 2, 5,
14, 42, 132 — the Catalan numbers, which is worth naming because it tells you the
answer grows fast but nothing like `2 ** 2n`.

**Signatures.** `legal_runs(gates)`, `legal_runs_by_filter(gates)`,
`is_legal(run)`, `deepest_standing(run)`.

**Watch for.** Allowing a close when none is open — that is the whole constraint.
Recording before the run is complete. `is_legal` is written independently of the
generator on purpose: a verifier that shares the generator's assumptions verifies
nothing.

<details>
<summary>Worked answer — <code>problem-03-sluice-pairing-solution.py</code></summary>

```python
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
```

</details>
---

## Problem 4 — The Grid Reference Split

**The brief.** A survey stamps grid references onto marker posts as four numbers
separated by dots. On old posts the dots have worn away. Given the digits, list
every reference the post could have been — **exactly four fields**, each from 0
to 255, none with a leading zero.

**The data.** Eight worn posts, including `25525511135`, `0000`, `010010` and a
fourteen-digit run.

**Constraints.** `0` is a field; `00` and `01` are not. `256` is not.

**Answer.** Fixed depth — four — with one, two or three digits at each level.
Three prunes, and **only one is an optimisation**:

```text
length prune   with `fields` left and `digits` left, dead unless
               fields <= digits <= 3 * fields          ← optional
value prune    a field over 255 is not a field         ← correctness
zero prune     a multi-digit field cannot start with 0 ← correctness
```

Telling those apart is the exercise. The length prune is what makes the
fourteen-digit post cost **1 node instead of 53**.

`010010` is the post to check by hand: it reads **two** ways, `0.10.0.10` and
`0.100.1.0`, and neither uses a leading zero. A solution that allows them finds
several more.

**Signatures.** `is_field(digits)`, `references(run)`, `references_unpruned(run)`,
`readable(run)`.

**Watch for.** Accepting `01` as 1. Forgetting that all four fields must be used
**and** all the digits consumed — checking one without the other passes on most
posts. Trying a fourth digit in a field.

<details>
<summary>Worked answer — <code>problem-04-grid-reference-split-solution.py</code></summary>

```python
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
```

</details>
---

## Problem 5 — The Tare Weight Picks

**The brief.** A works store keeps a bag of tare weights, some of them
identical — two 3lb weights are two separate lumps of iron, and either can go on
the pan, but a pan holding one is the same pan as one holding the other. Pick
weights summing to a target, using **each lump at most once**, and list the
distinct pans.

**The data.** A bag of nine weights with two 3s and two 1s, and a target of 8.

**Constraints.** Every weight positive; a target of zero is made by the empty
pan.

**Answer.** [Exercise 3](../exercises/exercise-03-clay-weigh-out.md) and
[Exercise 4](../exercises/exercise-04-repeat-bin-picks.md) in one problem, and
the two rules pull in opposite directions:

- from Exercise 3, the sum prune and a forwards-only walk — but recursing on
  `index + 1` rather than `index`, because a lump is used once;
- from Exercise 4, sort the bag and skip a repeat at the same level.

**Those are two different bugs and they look alike.** The file ships both wrong
walks: recursing on the same index invents `2+2+2+2` off a bag holding one 2,
and dropping the dedup reports the same pan once per set of lumps. Seven distinct
pans; the two wrong walks find 16 and 10.

**Signatures.** `tare_pans(bag, target)`, `tare_pans_reusing(bag, target)`,
`tare_pans_undeduped(bag, target)`, `fewest_lumps(bag, target)`.

**Watch for.** Getting one of the two rules and not the other — each alone
produces a plausible answer. The check that catches reuse is that no pan uses
more lumps of a weight than the bag holds; the check that catches missing dedup
is that every pan appears once. Two assertions, because they are two claims.

<details>
<summary>Worked answer — <code>problem-05-tare-weight-picks-solution.py</code></summary>

```python
"""problem-05-tare-weight-picks-solution.py - both rules at once.

A works store keeps a bag of tare weights. Some weights in the bag are
identical - two 3lb weights are two separate lumps of iron, and either can go
on the pan, but a pan holding one 3lb weight is the same pan as one holding the
other.

Pick weights from the bag summing to a target, using each LUMP at most once,
and list the distinct pans.

This is Exercise 3 and Exercise 4 in one problem, and the two rules pull in
opposite directions:

  from Exercise 3   the sum prune, and a walk that moves forwards only
  from Exercise 4   sort the bag, and skip a repeat at the same level

but with one thing changed from Exercise 3: the recursion moves to `index + 1`
rather than staying on `index`, because a lump can be used once. Getting that
one character wrong is a different bug from getting the dedup wrong, and both
produce plausible-looking answers.

The file ships three walks so the two failures can be told apart by running
them rather than by reasoning about them.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Two 3lb weights, two 1lb, and singles besides.
BAG: tuple[int, ...] = (10, 1, 2, 7, 6, 1, 5, 3, 3)
TARGET = 8


# ---- Your task ----
def tare_pans(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """Return every distinct pan of weights summing to `target`.

    Args:
        bag: The weights in the store, which may hold the same weight more than
            once. Every weight must be positive.
        target: The weight to make up. Must not be negative.

    Returns:
        Every distinct pan, each sorted, in walk order. Two pans are the same
        when they hold the same weights the same number of times.

    Raises:
        ValueError: If any weight is not positive, or the target is negative.
    """
    if any(weight <= 0 for weight in bag):
        raise ValueError("every tare weight must be positive")
    if target < 0:
        raise ValueError("a target weight cannot be negative")

    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                # The bag is sorted, so nothing further along fits either.
                break
            if next_index > index and weight == weights[next_index - 1]:
                # A repeat at this level would produce a pan already found.
                continue
            pan.append(weight)
            walk(next_index + 1, remaining - weight)   # + 1: one lump, once
            pan.pop()

    walk(0, target)
    return found


def tare_pans_reusing(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """The walk that recurses on the same index, shipped to be compared.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        Its answer, which uses a single lump more than once - so a bag holding
        one 2lb weight produces a pan of four 2lb weights. One character
        different from the right walk.
    """
    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                break
            if next_index > index and weight == weights[next_index - 1]:
                continue
            pan.append(weight)
            walk(next_index, remaining - weight)       # the bug
            pan.pop()

    walk(0, target)
    return found


def tare_pans_undeduped(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """The walk without the repeat skip, shipped to be compared.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        Its answer, which reports the same pan once per set of lumps rather
        than once per set of weights - so a pan using a 3lb weight appears
        twice when the bag holds two of them.
    """
    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                break
            pan.append(weight)
            walk(next_index + 1, remaining - weight)
            pan.pop()

    walk(0, target)
    return found


def fewest_lumps(bag: tuple[int, ...], target: int) -> list[int] | None:
    """Return a pan making `target` from the fewest lumps, or None.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        The shortest pan, ties going to the one found first, or None when the
        target cannot be made at all. Fewest lumps is what a storeman actually
        wants, because every lump is one thing to lift.

    Raises:
        ValueError: On the same inputs as `tare_pans`.
    """
    pans = tare_pans(bag, target)
    return min(pans, key=len) if pans else None


# ---- Self-check ----
if __name__ == "__main__":
    pans = tare_pans(BAG, TARGET)
    reusing = tare_pans_reusing(BAG, TARGET)
    undeduped = tare_pans_undeduped(BAG, TARGET)

    print(f"BAG  {sorted(BAG)}     TARGET  {TARGET}")
    print()

    print("EVERY DISTINCT PAN")
    for pan in pans:
        print(f"    {' + '.join(str(weight) for weight in pan)}")
    print()

    print("THE THREE WALKS")
    print(f"    distinct pans, each lump once : {len(pans)}   (the answer)")
    print(f"    recursing on the same index   : {len(reusing)}   (reuses a lump)")
    print(f"    without the repeat skip       : {len(undeduped)}   (same pan twice)")
    print()

    print(f"    fewest lumps for {TARGET}: {fewest_lumps(BAG, TARGET)}")
    print()

    # Every pan sums to the target and is sorted.
    for pan in pans:
        assert sum(pan) == TARGET
        assert pan == sorted(pan)

    # Every pan appears exactly once. That is the dedup rule working.
    assert len({tuple(pan) for pan in pans}) == len(pans)

    # No pan uses more lumps of a weight than the bag holds. That is the
    # "each lump once" rule working, and it is a different claim.
    for pan in pans:
        for weight in set(pan):
            assert pan.count(weight) <= BAG.count(weight)

    # The two failures are different and both are visible.
    # Reusing a lump invents pans the store cannot make: 2+2+2+2 off one 2.
    assert [2, 2, 2, 2] in reusing
    assert [2, 2, 2, 2] not in pans
    # Skipping the dedup repeats pans it has already found.
    assert len(undeduped) > len(pans)
    assert len({tuple(pan) for pan in undeduped}) == len(pans)

    # The fewest lumps for 8 is two.
    shortest = fewest_lumps(BAG, TARGET)
    assert shortest is not None and len(shortest) == 2 and sum(shortest) == TARGET

    # A target of zero is made by the empty pan, exactly once.
    assert tare_pans(BAG, 0) == [[]]

    # A target nothing can reach has no pans and no shortest.
    assert tare_pans((5, 10), 3) == []
    assert fewest_lumps((5, 10), 3) is None

    # A bag of identical weights gives one pan per reachable multiple.
    assert tare_pans((4, 4, 4), 8) == [[4, 4]]
    assert tare_pans((4, 4, 4), 12) == [[4, 4, 4]]
    assert tare_pans((4, 4, 4), 16) == []      # only three lumps in the bag

    # A zero or negative weight would make the sum prune unsound; a negative
    # target is meaningless. Both are refused.
    for bad_bag, bad_target in (((0, 2), 4), ((-1, 2), 4), ((2, 3), -1)):
        try:
            tare_pans(bad_bag, bad_target)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_bag}, {bad_target}")

    print("All checks passed.")
```

</details>
---

## Problem 6 — The Test Tray Fill

**The brief.** A glaze test tray is a square grid of wells. Every **row** must
hold each glaze exactly once, and so must every **column**. Some wells are
already filled. Finish the tray, or say it cannot be finished.

**The data.** A four-glaze tray part-filled from a previous session, and a
spoiled tray with two `A`s already sharing a column.

**Constraints.** The wells already filled are not moved. A tray that is already
spoiled is reported as spoiled, which is a better answer than "no solution
found".

**Answer.** This differs from every other walk of the week in one way: it does
not choose **which** well to fill. It fills them in a fixed order and chooses
only what goes in them. That keeps the state small — one set per row and one per
column — and makes the legality test a lookup rather than a scan.

The prune **is** the legality test, applied before descending rather than after.

That one decision is worth more here than anywhere else in the course:

```text
wells filled, pruning early :          25
wells filled, checking late :  15,836,737
```

Same tray, same answer, six orders of magnitude. If you write one sentence about
pruning all week, write it about this.

**Signatures.** `check_tray(tray, glazes)`, `already_spoiled(tray, glazes)`,
`fill_tray(tray, glazes)`, `fill_tray_late_check(tray, glazes)`.

**Watch for.** Undoing two of the three things you changed — the well, the row
set and the column set all have to go back. Scanning the row and column to test
legality instead of keeping sets, which is correct and turns a lookup into a
scan. Reporting "no solution" for a tray that was spoiled before the walk began.

<details>
<summary>Worked answer — <code>problem-06-test-tray-fill-solution.py</code></summary>

```python
"""problem-06-test-tray-fill-solution.py - filling a tray so nothing repeats.

A glaze test tray is a square grid of wells. Every ROW must hold each glaze
exactly once, and so must every COLUMN - that is the whole point of the tray,
because it lets the studio compare glazes across two firing gradients at the
same time.

Some wells are already filled from a previous session. Finish the tray, or say
that it cannot be finished.

This is the constraint-satisfaction shape, and it differs from every other
walk this week in one way: the walk does not choose WHICH well to fill in an
arbitrary order. It fills them in a fixed order and chooses only what goes in
them. That keeps the state small - one row and one column set per line - and it
is why the legality test is a lookup rather than a scan.

The prune is the legality test itself, applied BEFORE descending rather than
after. Placing a glaze and discovering at the bottom of the tray that it was
illegal is the same walk doing far more work for the same answer, and the file
counts nodes for both so the difference is a number.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
GLAZES: tuple[str, ...] = ("A", "B", "C", "D")
EMPTY = "."

# A tray part-filled from a previous session.
TRAY: tuple[str, ...] = (
    "A...",
    "..C.",
    ".B..",
    "...A",
)

# A tray that cannot be finished: two As already share a column.
SPOILED: tuple[str, ...] = (
    "A...",
    "A...",
    "....",
    "....",
)


# ---- Your task ----
def check_tray(tray: tuple[str, ...], glazes: tuple[str, ...]) -> None:
    """Raise unless `tray` is a square grid of glazes and empty wells.

    Args:
        tray: The tray, one string per row.
        glazes: The glazes in use.

    Raises:
        ValueError: If the tray is not square, is not the size of the glaze
            set, or holds a character that is neither a glaze nor EMPTY.
    """
    size = len(glazes)
    if len(tray) != size or any(len(row) != size for row in tray):
        raise ValueError(f"the tray must be {size} by {size}")
    allowed = set(glazes) | {EMPTY}
    for row in tray:
        for well in row:
            if well not in allowed:
                raise ValueError(f"{well!r} is not a glaze or an empty well")


def already_spoiled(tray: tuple[str, ...], glazes: tuple[str, ...]) -> bool:
    """Say whether the wells already filled break the rule between themselves.

    Args:
        tray: The tray.
        glazes: The glazes in use.

    Returns:
        True when some row or column already holds one glaze twice. Written
        independently of the fill on purpose - a tray can be unfinishable
        because of what is already in it, and saying so is a better answer
        than "no solution found".

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    for line in range(size):
        row = [tray[line][col] for col in range(size) if tray[line][col] != EMPTY]
        col = [tray[r][line] for r in range(size) if tray[r][line] != EMPTY]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return True
    return False


def fill_tray(
    tray: tuple[str, ...], glazes: tuple[str, ...]
) -> tuple[tuple[str, ...] | None, int]:
    """Finish the tray, or report that it cannot be finished.

    Args:
        tray: The tray, part filled.
        glazes: The glazes in use.

    Returns:
        A pair: the finished tray, or None when no filling exists, and how many
        wells the walk placed a glaze into.

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    wells = [list(row) for row in tray]
    rows: list[set[str]] = [set() for _ in range(size)]
    cols: list[set[str]] = [set() for _ in range(size)]

    for row in range(size):
        for col in range(size):
            glaze = wells[row][col]
            if glaze != EMPTY:
                if glaze in rows[row] or glaze in cols[col]:
                    return None, 0        # spoiled before the walk begins
                rows[row].add(glaze)
                cols[col].add(glaze)

    placed = 0

    def walk(position: int) -> bool:
        nonlocal placed
        if position == size * size:
            return True
        row, col = divmod(position, size)
        if wells[row][col] != EMPTY:
            return walk(position + 1)
        for glaze in glazes:
            # The legality test IS the prune, and it happens before descending.
            if glaze in rows[row] or glaze in cols[col]:
                continue
            wells[row][col] = glaze       # choose
            rows[row].add(glaze)
            cols[col].add(glaze)
            placed += 1
            if walk(position + 1):        # explore
                return True
            wells[row][col] = EMPTY       # undo - three things this time
            rows[row].discard(glaze)
            cols[col].discard(glaze)
        return False

    if walk(0):
        return tuple("".join(row) for row in wells), placed
    return None, placed


def fill_tray_late_check(
    tray: tuple[str, ...], glazes: tuple[str, ...]
) -> tuple[tuple[str, ...] | None, int]:
    """The same fill that checks legality only at the bottom, for comparison.

    Args:
        tray: The tray, part filled.
        glazes: The glazes in use.

    Returns:
        The same answer for far more work, and the wells it placed into. This
        is what "prune early" costs when it is not done, and on a four-glaze
        tray the difference is already large enough to print.

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    wells = [list(row) for row in tray]
    placed = 0

    def legal() -> bool:
        for line in range(size):
            row = [wells[line][c] for c in range(size) if wells[line][c] != EMPTY]
            col = [wells[r][line] for r in range(size) if wells[r][line] != EMPTY]
            if len(set(row)) != len(row) or len(set(col)) != len(col):
                return False
        return True

    def walk(position: int) -> bool:
        nonlocal placed
        if position == size * size:
            return legal()
        row, col = divmod(position, size)
        if wells[row][col] != EMPTY:
            return walk(position + 1)
        for glaze in glazes:
            wells[row][col] = glaze
            placed += 1
            if walk(position + 1):
                return True
            wells[row][col] = EMPTY
        return False

    if walk(0):
        return tuple("".join(row) for row in wells), placed
    return None, placed


# ---- Self-check ----
if __name__ == "__main__":
    filled, placed = fill_tray(TRAY, GLAZES)
    _, late_placed = fill_tray_late_check(TRAY, GLAZES)

    print("THE TRAY AS FOUND")
    for row in TRAY:
        print("    " + " ".join(row))
    print()

    print("THE TRAY FINISHED")
    for row in filled or ():
        print("    " + " ".join(row))
    print()

    print("CHECKING EARLY AGAINST CHECKING LATE")
    print(f"    wells filled, pruning early : {placed}")
    print(f"    wells filled, checking late : {late_placed}")
    print()

    print("A TRAY THAT CANNOT BE FINISHED")
    for row in SPOILED:
        print("    " + " ".join(row))
    print(f"    already spoiled: {already_spoiled(SPOILED, GLAZES)}")
    print(f"    fill_tray says : {fill_tray(SPOILED, GLAZES)[0]}")
    print()

    # The tray can be finished.
    assert filled is not None

    # Every row and every column holds each glaze exactly once.
    for line in range(len(GLAZES)):
        assert sorted(filled[line]) == sorted(GLAZES)
        assert sorted(filled[r][line] for r in range(len(GLAZES))) == sorted(GLAZES)

    # The wells that were already filled are untouched.
    for row in range(len(GLAZES)):
        for col in range(len(GLAZES)):
            if TRAY[row][col] != EMPTY:
                assert filled[row][col] == TRAY[row][col]

    # Checking early does strictly less work than checking late, for the same
    # answer. That is the whole argument for pruning where the choice is made.
    assert placed < late_placed
    assert fill_tray_late_check(TRAY, GLAZES)[0] is not None

    # A tray already spoiled is reported as spoiled, and cannot be filled.
    assert already_spoiled(SPOILED, GLAZES) is True
    assert fill_tray(SPOILED, GLAZES)[0] is None

    # A tray as found that is legal is not spoiled.
    assert already_spoiled(TRAY, GLAZES) is False

    # An empty tray fills straightforwardly; a full legal tray is returned as is.
    empty = tuple(EMPTY * len(GLAZES) for _ in GLAZES)
    assert fill_tray(empty, GLAZES)[0] is not None
    done = ("ABCD", "BCDA", "CDAB", "DABC")
    assert fill_tray(done, GLAZES)[0] == done

    # A tray of the wrong size, or holding something that is not a glaze, is
    # refused rather than guessed at.
    for bad in (("ABC", "BCA", "CAB"), ("ABCD", "BCDA", "CDAB", "DABX")):
        try:
            fill_tray(bad, GLAZES)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names what one node of the tree is, where the answer is recorded, and how many answers there could be — before any code. |
| Reason about options | Four to six bullets before coding, separating the prunes that are optimisations from the prunes that are correctness rules. |
| Assemble the solution | Choose, explore, undo, with the undo restoring *everything* the choose changed; type hints throughout. |
| Measure it | A trace on at least two inputs, one degenerate — and for the pages that count nodes, the number quoted rather than described. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement. Say what the walk costs *before* pruning and what the prune actually buys. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-12/homework/`, one file per
problem:

```
frame-writeups/c2-week-12/homework/
├── problem-1-tasting-panel.md
├── problem-2-dial-board.md
├── problem-3-sluice-pairing.md
├── problem-4-grid-reference-split.md
├── problem-5-tare-weight-picks.md
└── problem-6-test-tray-fill.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Tasting Panel | 25 min | 15 min | 40 min |
| 2 — Dial Board | 20 min | 15 min | 35 min |
| 3 — Sluice Pairing | 35 min | 15 min | 50 min |
| 4 — Grid Reference Split | 40 min | 15 min | 55 min |
| 5 — Tare Weight Picks | 40 min | 15 min | 55 min |
| 6 — Test Tray Fill | 40 min | 15 min | 55 min |

About five hours. Problems 5 and 6 are the two that pay off most: 5 because two
rules that look alike are two different bugs, and 6 because it is the clearest
demonstration in the whole course of what pruning at the right moment is worth.
