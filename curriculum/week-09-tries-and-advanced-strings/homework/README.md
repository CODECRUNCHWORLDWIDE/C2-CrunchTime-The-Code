# Week 9 — Homework

Six problems, all original, each with a runnable worked answer folded under it.
Allow about five hours. Do each with the lectures closed; open the reveal only
after your own version runs, or after fifteen minutes stuck on one step.

The six cover every shape the week teaches: a wildcard walk, a chain of prefixes,
the border table, a tree built backwards, a tree that queries itself, and a walk
carrying a budget.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Smudged Stencil](#problem-1--the-smudged-stencil) | Prefix tree with a single-character wildcard | 45 min |
| 2 | [The Growable Dock Sign](#problem-2--the-growable-dock-sign) | Every prefix must itself be a word | 40 min |
| 3 | [The Splice Point](#problem-3--the-splice-point) | The border table, and a scan that never backs up | 55 min |
| 4 | [The Radio Tail Watch](#problem-4--the-radio-tail-watch) | A tree built backwards, walked from the newest letter | 50 min |
| 5 | [The Double-Stamped Label](#problem-5--the-double-stamped-label) | A tree queried against its own contents | 55 min |
| 6 | [The One-Key Typo Desk](#problem-6--the-one-key-typo-desk) | A walk carrying a budget of one mismatch | 50 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, copy the code out of the reveal
into a file of your own and run that file:

```bash
python problem-01-smudged-stencil.py
```

---

## Problem 1 — The Smudged Stencil

**The brief.** Depot crates carry a stencilled code. Rain smudges letters, and
the clerk types a question mark where a letter is unreadable. **One question mark
stands for exactly one letter** — never for none, and never for two. Given the
register of real codes and a smudged pattern, list every code the pattern could
be, A to Z.

**The data.** Eight stencils: `CRATE GRATE GRAPE CRANE PLATE SLATE SLATS PLAN`.

**Constraints.** The wildcard is exactly one letter, so a four-character pattern
can only match a four-character code. `??` matches nothing here, because no code
is two letters long — and that is a real answer, not an empty one.

**Answer.** Build a prefix tree over the codes, then walk it one character at a
time. On a letter, descend that one branch. On a `?`, **descend every branch**.
At the end of the pattern, collect the codes at nodes marked as ends.

The reason the tree beats scanning the register is what happens on `?????`: a
scan tries every code against every position, while the tree's five-wildcard walk
visits each node once and stops dead on any branch that runs out of depth. Sorted
output falls out of walking the branches in order rather than needing a sort.

On this data `?????` gives **seven** codes — every five-letter stencil — and
`PL??` gives one, `PLAN`.

**Signatures.** `build_stencil_tree(codes)`, `matches(root, pattern)`.

**Watch for.** Letting `?` match zero characters or two — the length has to be
exact. Returning codes from nodes that are merely *on the way* rather than marked
as ends: `PL??` must not return `PLATE`. And a pattern longer than every code
returns an empty list, not an error.

<details>
<summary>Worked answer — <code>problem-01-smudged-stencil-solution.py</code></summary>

```python
"""problem-01-smudged-stencil-solution.py — reading a smudged crate stencil.

Depot crates carry a stencilled code. Rain smudges letters, and the clerk
types a question mark where a letter is unreadable. One question mark stands
for exactly one letter, never for none and never for two.

Given the register of real codes and a smudged pattern, list every code the
pattern could be, A to Z.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"
SMUDGE = "?"

CodeTree = dict

STENCILS: list[str] = [
    "CRATE",
    "GRATE",
    "GRAPE",
    "CRANE",
    "PLATE",
    "SLATE",
    "SLATS",
    "PLAN",
]

PATTERNS: list[str] = ["?RATE", "GRA?E", "?????", "SLAT?", "PL??", "CRATE", "??"]


def build_stencil_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every stencil code.

    Args:
        codes: The codes in the register. Duplicates are harmless.

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


def matches(root: CodeTree, pattern: str) -> list[str]:
    """Return every registered code the smudged pattern could be, A to Z.

    Args:
        root: A tree of registered codes.
        pattern: Letters, with SMUDGE standing for exactly one unknown letter.

    Returns:
        The matching codes, sorted A to Z. Empty when nothing matches.

    Raises:
        ValueError: If `pattern` is empty.
    """
    if not pattern:
        raise ValueError("a stencil pattern cannot be empty")
    found: list[str] = []

    def walk(node: CodeTree, position: int, spelled: str) -> None:
        if position == len(pattern):
            if END in node:
                found.append(spelled)
            return
        mark = pattern[position]
        if mark == SMUDGE:
            for letter in sorted(key for key in node if key != END):
                walk(node[letter], position + 1, spelled + letter)
        elif mark in node:
            walk(node[mark], position + 1, spelled + mark)

    walk(root, 0, "")
    return sorted(found)


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_stencil_tree(STENCILS)
    for pattern in PATTERNS:
        hits = matches(tree, pattern)
        shown = ", ".join(hits) if hits else "(nothing)"
        print(f"{pattern:<7} {len(hits)}  {shown}")

    assert matches(tree, "?RATE") == ["CRATE", "GRATE"]
    assert matches(tree, "GRA?E") == ["GRAPE", "GRATE"]
    assert matches(tree, "?????") == [
        "CRANE",
        "CRATE",
        "GRAPE",
        "GRATE",
        "PLATE",
        "SLATE",
        "SLATS",
    ]
    assert matches(tree, "SLAT?") == ["SLATE", "SLATS"]
    assert matches(tree, "PL??") == ["PLAN"]
    assert matches(tree, "CRATE") == ["CRATE"]
    assert matches(tree, "??") == []
    assert matches(tree, "?") == []

    try:
        matches(tree, "")
    except ValueError as problem:
        assert str(problem) == "a stencil pattern cannot be empty"
    else:
        raise AssertionError("an empty pattern should have been rejected")

    print()
    print("All checks passed.")
```

</details>
---

## Problem 2 — The Growable Dock Sign

**The brief.** A dock sign is built by sliding letter tiles on, one at a time,
left to right. **Every stage has to be a code the harbour already recognises** —
you cannot show a half-finished word to the public. Find the longest sign that
can be built this way, and report the whole build, stage by stage.

**The data.** Fourteen codes, including the chains `B BE BER BERT BERTH`,
`D DO DOC DOCK DOCKS`, and `Q QU QUAY`, plus the orphan `TIDE`.

**Constraints.** `DOCKS` is five letters and so is `BERTH`, so the tie has to
resolve by a stated rule. `TIDE` is longer than `QUAY` and buildable at no stage
past its first letter — length alone is not the answer.

**Answer.** Build the prefix tree, then walk **only through nodes marked as
ends**. The moment a node on the path is not itself a code, that branch is dead —
there is no point looking further down it, because every deeper sign would have
to pass through the stage you just rejected.

That early stop is the whole idea. Checking each code's prefixes separately does
the same work repeatedly; the tree does the chain once and shares it between
every code that starts the same way.

Longest here is **BERTH**, in five stages.

**Signatures.** `build_register_tree(codes)`, `longest_build(root)`.

**Watch for.** Walking past a non-end node "just in case" — that is the pruning,
and without it the answer is `TIDE`. Ties between two equally long chains need a
rule, and the file states one rather than trusting dictionary order. An empty
register gives an empty build.

<details>
<summary>Worked answer — <code>problem-02-growable-dock-sign-solution.py</code></summary>

```python
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
```

</details>
---

## Problem 3 — The Splice Point

**The brief.** A cable spool is labelled with the colour bands printed along it,
one letter per band. A splice code is a short band sequence the workshop wants to
find. Report **every** position where the code appears — **including positions
that overlap an earlier hit**, because a splice can share bands with its
neighbour.

**The data.** Label `RGRGRGBRGRGRGR`, code `RGRGR`. Plus a 4000-band label built
from a repeating pattern, to make the cost visible.

**Constraints.** Overlaps count. On `BBBB` looking for `BB` the answer is
`[0, 1, 2]`, not `[0, 2]`, and getting that right is what stops you advancing by
the code's whole length after a hit.

**Answer.** The **border table**: for each position in the code, the length of
the longest proper prefix that is also a suffix ending there. On a mismatch it
says how far back to slide the code without moving the position in the label at
all — so the label is read once, forwards, and never backed up.

The nested-loop version re-reads bands it has already seen. On a label built from
a repeating pattern that is nearly all of them, which is exactly the case here
and exactly why the long label is in the data.

On the shipped label the hits are `[0, 7, 9]` — 7 and 9 overlap.

**Signatures.** `border_table(code)`, `splice_points(label, code)`.

**Watch for.** Advancing by the code length after a hit, which drops every
overlap. Building the table with `>=` where `>` belongs, which makes a border
claim a prefix is its own proper prefix. An empty code, or a code longer than the
label, returns an empty list.

<details>
<summary>Worked answer — <code>problem-03-splice-point-solution.py</code></summary>

```python
"""problem-03-splice-point-solution.py — finding every splice in a spool label.

A cable spool is labelled with the colour bands printed along it, one letter
per band. A splice code is a short band sequence the workshop wants to find.
Report every position where the code appears — including positions that
overlap an earlier hit, because a splice can share bands with its neighbour.

The one-pass scan reuses the code's own border table, so the position in the
label never moves backwards. The nested-loop version re-reads bands it has
already seen, and on a label built from a repeating pattern it re-reads almost
all of them.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

LABEL = "RGRGRGBRGRGRGR"
CODE = "RGRGR"

# A label built to punish the nested-loop scan: one long repeat, one odd band.
LONG_LABEL = "RG" * 2000
LONG_CODE = "RG" * 20 + "B"


def border_table(code: str) -> list[int]:
    """Return the border length at every cut of `code`.

    Args:
        code: The splice code. Must not be empty.

    Returns:
        A list as long as `code`, where entry `i` is the length of the longest
        run that both opens and closes `code[:i + 1]` without being all of it.

    Raises:
        ValueError: If `code` is empty.
    """
    if not code:
        raise ValueError("a splice code cannot be empty")
    table = [0] * len(code)
    cursor = 1
    matched = 0
    while cursor < len(code):
        if code[cursor] == code[matched]:
            matched += 1
            table[cursor] = matched
            cursor += 1
        elif matched:
            matched = table[matched - 1]
        else:
            table[cursor] = 0
            cursor += 1
    return table


def splice_points(label: str, code: str) -> list[int]:
    """Return every start position where `code` appears in `label`.

    Args:
        label: The bands printed along the spool. May be empty.
        code: The splice code to find. Must not be empty.

    Returns:
        The start positions, smallest first. Overlapping hits are all listed.
        Empty when the code does not appear.

    Raises:
        ValueError: If `code` is empty.
    """
    table = border_table(code)
    hits: list[int] = []
    matched = 0
    for position, band in enumerate(label):
        while matched and band != code[matched]:
            matched = table[matched - 1]
        if band == code[matched]:
            matched += 1
        if matched == len(code):
            hits.append(position - matched + 1)
            matched = table[matched - 1]
    return hits


def splice_points_by_scan(label: str, code: str) -> list[int]:
    """Return the same positions the slow way, for checking only.

    Args:
        label: The bands printed along the spool.
        code: The splice code to find. Must not be empty.

    Returns:
        The start positions, smallest first.

    Raises:
        ValueError: If `code` is empty.
    """
    if not code:
        raise ValueError("a splice code cannot be empty")
    return [
        start
        for start in range(len(label) - len(code) + 1)
        if label[start : start + len(code)] == code
    ]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"label  {LABEL}")
    print(f"code   {CODE}")
    print(f"hits   {splice_points(LABEL, CODE)}")
    print()

    for label, code in [("RGRGR", "RGRGR"), ("RGB", "RGRGR"), ("", "RG"), ("BBBB", "BB")]:
        print(f"{label or '(empty)':<8} in-code {code:<6} {splice_points(label, code)}")

    print()
    print(f"long label bands   {len(LONG_LABEL)}")
    print(f"long code bands    {len(LONG_CODE)}")
    print(f"long label hits    {len(splice_points(LONG_LABEL, LONG_CODE))}")

    assert splice_points(LABEL, CODE) == [0, 7, 9]
    assert splice_points("RGRGR", "RGRGR") == [0]
    assert splice_points("RGB", "RGRGR") == []
    assert splice_points("", "RG") == []
    assert splice_points("BBBB", "BB") == [0, 1, 2]
    assert splice_points(LONG_LABEL, LONG_CODE) == splice_points_by_scan(LONG_LABEL, LONG_CODE)
    assert border_table("RGRGR") == [0, 0, 1, 2, 3]

    try:
        splice_points(LABEL, "")
    except ValueError as problem:
        assert str(problem) == "a splice code cannot be empty"
    else:
        raise AssertionError("an empty code should have been rejected")

    print()
    print("All checks passed.")
```

</details>
---

## Problem 4 — The Radio Tail Watch

**The brief.** A harbour radio desk receives letters one at a time, forever.
Certain words are **call words** the duty officer must be told about, and a call
word counts **only when it lands at the very end** of what has arrived so far.

**The data.** Call words `PAN PANPAN MAY MAYDAY`; the stream `QPANPANZMAYDAY`.

**Constraints.** The stream never ends, so nothing may be re-scanned from the
start. `PANPAN` contains `PAN`, so one letter can complete two different call
words at different times — and the answer at each letter is which call word ended
*there*.

**Answer.** Build the tree out of the call words **spelled backwards**. Then a
walk from the newest letter backwards through the stream is an ordinary walk down
a prefix tree, and it stops as soon as no branch matches.

That inversion is the whole trick and it is worth a paragraph in the write-up:
the interesting end of a stream is the newest letter, and a prefix tree only walks
forwards, so you reverse the words rather than the stream.

**Signatures.** `TailWatch` with the letter-at-a-time interface.

**Watch for.** Storing the whole stream and re-searching it — correct, and
unbounded in memory on a stream that does not end. Reporting a call word that
ends anywhere but at the newest letter. And the walk must stop at the deepest
matching branch rather than walking the whole history back.

<details>
<summary>Worked answer — <code>problem-04-radio-tail-watch-solution.py</code></summary>

```python
"""problem-04-radio-tail-watch-solution.py — watching the tail of a stream.

A harbour radio desk receives letters one at a time, forever. Certain words
are call words the duty officer must be told about, and a call word counts
only when it lands at the very end of what has arrived so far.

Because the interesting end of the stream is the newest letter, the tree is
built out of the call words spelled backwards. Then a walk from the newest
letter backwards is an ordinary walk down a prefix tree.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CallTree = dict

CALL_WORDS: list[str] = ["PAN", "PANPAN", "MAY", "MAYDAY"]

STREAM = "QPANPANZMAYDAY"


class TailWatch:
    """A radio tail watch over a fixed list of call words."""

    def __init__(self, call_words: list[str]) -> None:
        """Build the reversed tree and the buffer.

        Args:
            call_words: The words to watch for. Must not be empty, and no word
                may be the empty string.

        Raises:
            ValueError: If the list is empty or holds an empty word.
        """
        if not call_words:
            raise ValueError("a tail watch needs at least one call word")
        self._root: CallTree = {}
        for word in call_words:
            if not word:
                raise ValueError("a call word cannot be the empty string")
            node = self._root
            for letter in reversed(word):
                node = node.setdefault(letter, {})
            node[END] = True
        self._longest = max(len(word) for word in call_words)
        self._tail: list[str] = []

    def feed(self, letter: str) -> str:
        """Take one more letter and report the longest call word ending here.

        Args:
            letter: Exactly one character from the stream.

        Returns:
            The longest call word that ends at this letter, or "" when none
            does.

        Raises:
            ValueError: If `letter` is not exactly one character.
        """
        if len(letter) != 1:
            raise ValueError("feed takes exactly one letter at a time")
        self._tail.append(letter)
        if len(self._tail) > self._longest:
            self._tail.pop(0)

        node = self._root
        best = ""
        spelled = 0
        for back in reversed(self._tail):
            if back not in node:
                break
            node = node[back]
            spelled += 1
            if END in node:
                best = "".join(self._tail[-spelled:])
        return best


# ---- Self-check ----
if __name__ == "__main__":
    watch = TailWatch(CALL_WORDS)
    heard: list[str] = []
    for letter in STREAM:
        call = watch.feed(letter)
        heard.append(call)
        print(f"{letter}  {call or '-'}")

    print()
    print(f"call words heard  {[call for call in heard if call]}")

    assert [call for call in heard if call] == ["PAN", "PANPAN", "MAY", "MAYDAY"]
    assert heard[3] == "PAN"
    assert heard[6] == "PANPAN"
    assert heard[13] == "MAYDAY"

    quiet = TailWatch(["TIDE"])
    assert [quiet.feed(letter) for letter in "TIDAL"] == ["", "", "", "", ""]

    try:
        TailWatch([])
    except ValueError as problem:
        assert str(problem) == "a tail watch needs at least one call word"
    else:
        raise AssertionError("an empty watch list should have been rejected")

    try:
        TailWatch(CALL_WORDS).feed("AB")
    except ValueError as problem:
        assert str(problem) == "feed takes exactly one letter at a time"
    else:
        raise AssertionError("a two-letter feed should have been rejected")

    print()
    print("All checks passed.")
```

</details>
---

## Problem 5 — The Double-Stamped Label

**The brief.** A boatyard stamps part labels from a set of metal dies, one die per
registered code. Some labels were stamped with two or more dies in a row, so the
label reads as one code but is really several registered codes joined end to end.
Find every registered code that is **exactly two or more other registered codes**
laid end to end, longest first.

**The data.** Eleven die codes including `FIN`, `BOARD`, `FINBOARD`, `KEEL`,
`SON`, `KEELSON`, `BOARDKEELSON`, `MAST`, `MASTFIN`, `FINBOARDMAST`, `RUDDER`.

**Constraints.** "Two or more" is the rule, so a code is not double-stamped by
being itself. `FINBOARDMAST` is three dies, which is why the rule is not "exactly
two". And `BOARDKEELSON` is made from `BOARD` plus `KEELSON`, which is itself
made from two dies — the decomposition does not have to be into single dies only.

**Answer.** Build the tree over all the codes, then for each code walk it against
**the tree it is a member of**, splitting wherever a registered code ends and
recursing on the remainder. Count the pieces; two or more means double-stamped.

The subtlety is that a code must not match itself as its own only piece, which is
what the "two or more" count is really enforcing.

Five codes qualify here, longest first: `BOARDKEELSON`, `FINBOARDMAST`,
`FINBOARD`, `KEELSON`, `MASTFIN`.

**Signatures.** `build_die_tree(codes)`, `is_double_stamped(root, code)`,
`double_stamped(codes)`.

**Watch for.** Counting a code as made of one piece — itself. Missing the
three-piece cases by only ever trying one split. Re-walking the same suffix
repeatedly on a large register, which is where memoising the suffix pays.

<details>
<summary>Worked answer — <code>problem-05-double-stamped-label-solution.py</code></summary>

```python
"""problem-05-double-stamped-label-solution.py — labels made of other labels.

A boatyard stamps part labels from a set of metal dies, one die per registered
code. Some labels were stamped with two or more dies in a row, so the label
reads as one code but is really several registered codes joined up.

Find every registered code that is exactly two or more other registered codes
laid end to end, longest first.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

DIE_CODES: list[str] = [
    "FIN",
    "BOARD",
    "FINBOARD",
    "KEEL",
    "SON",
    "KEELSON",
    "BOARDKEELSON",
    "MAST",
    "MASTFIN",
    "FINBOARDMAST",
    "RUDDER",
]


def build_die_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every die code.

    Args:
        codes: The registered codes. Duplicates are harmless.

    Returns:
        The root node.

    Raises:
        ValueError: If any code is the empty string.
    """
    root: CodeTree = {}
    for code in codes:
        if not code:
            raise ValueError("a die code cannot be the empty string")
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = True
    return root


def is_double_stamped(root: CodeTree, code: str) -> bool:
    """Return True when `code` is two or more registered codes end to end.

    Args:
        root: A tree of registered codes, including `code` itself.
        code: The label to test.

    Returns:
        True when `code` splits into at least two registered pieces. The whole
        label counts as one piece, so a label that only matches itself is False.
    """
    reachable: dict[int, bool] = {}

    def can_finish(start: int, pieces: int) -> bool:
        if start == len(code):
            return pieces >= 2
        if start in reachable and not reachable[start]:
            return False
        node = root
        for cut in range(start, len(code)):
            letter = code[cut]
            if letter not in node:
                break
            node = node[letter]
            if END not in node:
                continue
            if cut + 1 == len(code) and pieces == 0:
                continue  # that piece is the whole label, so it is not a build
            if can_finish(cut + 1, pieces + 1):
                return True
        reachable[start] = False
        return False

    return can_finish(0, 0)


def double_stamped(codes: list[str]) -> list[str]:
    """Return every code that is built from two or more other codes.

    Args:
        codes: The registered codes.

    Returns:
        The built codes, longest first, ties broken A to Z.
    """
    root = build_die_tree(codes)
    built = [code for code in codes if is_double_stamped(root, code)]
    return sorted(built, key=lambda code: (-len(code), code))


# ---- Self-check ----
if __name__ == "__main__":
    found = double_stamped(DIE_CODES)
    for code in found:
        print(f"{len(code):>3}  {code}")
    print()
    print(f"single-die codes  {sorted(set(DIE_CODES) - set(found))}")

    assert found == [
        "BOARDKEELSON",
        "FINBOARDMAST",
        "FINBOARD",
        "KEELSON",
        "MASTFIN",
    ]
    assert double_stamped(["RUDDER"]) == []
    assert double_stamped(["A", "B", "AB", "ABA"]) == ["ABA", "AB"]
    assert double_stamped([]) == []

    try:
        build_die_tree(["FIN", ""])
    except ValueError as problem:
        assert str(problem) == "a die code cannot be the empty string"
    else:
        raise AssertionError("an empty code should have been rejected")

    print()
    print("All checks passed.")
```

</details>
---

## Problem 6 — The One-Key Typo Desk

**The brief.** The yard office types four-letter locker codes all day, and the
commonest mistake is hitting one neighbouring key. The desk answers one question:
which real codes are **exactly one letter** away from what was typed?

Exactly one. A code that matches perfectly is not an answer, because nothing was
mistyped. A code two letters away is not an answer either.

**The data.** Lockers `HOLD HOLE HULL BOLT BOLD BOAT OARS`; typed strings
including `HOLD`, `BOLD`, `BOAT`, `HULL`, and the wrong-length `HOL` and `HOLDS`.

**Constraints.** Only substitutions count — no insertions, no deletions — so a
code of a different length is never an answer. `HOL` and `HOLDS` both return
nothing, and that is the constraint doing its job rather than a gap in the data.

**Answer.** Walk the tree carrying a **budget of one swap**. While the budget is
unspent the walk may branch into every letter other than the typed one, spending
the budget as it does. Once it is spent the walk must follow the typed letters
exactly. At the end, accept only nodes that are marked as ends **and** whose
budget was actually spent.

That last clause is the one people miss: a walk that never spends the budget has
found the typed code itself, which is not a typo.

`HOLD` gives `BOLD` and `HOLE`; `BOAT` gives only `BOLT`; `HULL` gives nothing.

**Signatures.** `build_locker_tree(codes)`, `one_key_away(root, typed)`.

**Watch for.** Returning the exact match — the budget must be spent. Allowing the
budget to go negative, which quietly turns this into two-letter matching. Walking
a branch after the budget is spent and the letters diverge.

<details>
<summary>Worked answer — <code>problem-06-one-key-typo-desk-solution.py</code></summary>

```python
"""problem-06-one-key-typo-desk-solution.py — one wrong key, nothing else.

The yard office types four-letter locker codes all day, and the commonest
mistake is hitting one neighbouring key. The desk should answer a single
question: which real codes are exactly one letter away from what was typed?

Exactly one. A code that matches perfectly is not an answer, because nothing
was mistyped. A code two letters away is not an answer either.

The walk carries a budget of one swap down the tree. While the budget is
unspent the walk may branch into every other letter; once it is spent the walk
must follow the typed letters exactly.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

LOCKERS: list[str] = ["HOLD", "HOLE", "HULL", "BOLT", "BOLD", "BOAT", "OARS"]

TYPED: list[str] = ["HOLD", "BOLD", "BOAT", "HULL", "OARS", "HOL", "HOLDS"]


def build_locker_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree holding every locker code.

    Args:
        codes: The real locker codes. Duplicates are harmless.

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


def one_key_away(root: CodeTree, typed: str) -> list[str]:
    """Return every real code that differs from `typed` in exactly one letter.

    Args:
        root: A tree of real locker codes.
        typed: What the clerk typed. Must not be empty.

    Returns:
        The matching codes, sorted A to Z. Codes of a different length can
        never qualify, and neither can `typed` itself.

    Raises:
        ValueError: If `typed` is empty.
    """
    if not typed:
        raise ValueError("nothing was typed")
    found: list[str] = []

    def walk(node: CodeTree, position: int, spelled: str, swapped: bool) -> None:
        if position == len(typed):
            if swapped and END in node:
                found.append(spelled)
            return
        wanted = typed[position]
        for letter in sorted(key for key in node if key != END):
            if letter == wanted:
                walk(node[letter], position + 1, spelled + letter, swapped)
            elif not swapped:
                walk(node[letter], position + 1, spelled + letter, True)

    walk(root, 0, "", False)
    return found


# ---- Self-check ----
if __name__ == "__main__":
    tree = build_locker_tree(LOCKERS)
    for typed in TYPED:
        near = one_key_away(tree, typed)
        shown = ", ".join(near) if near else "(nothing)"
        print(f"{typed:<6} {len(near)}  {shown}")

    assert one_key_away(tree, "HOLD") == ["BOLD", "HOLE"]
    assert one_key_away(tree, "BOLD") == ["BOLT", "HOLD"]
    assert one_key_away(tree, "BOAT") == ["BOLT"]
    assert one_key_away(tree, "HULL") == []
    assert one_key_away(tree, "OARS") == []
    assert one_key_away(tree, "HOL") == []
    assert one_key_away(tree, "HOLDS") == []
    assert one_key_away(tree, "ZOLD") == ["BOLD", "HOLD"]

    try:
        one_key_away(tree, "")
    except ValueError as problem:
        assert str(problem) == "nothing was typed"
    else:
        raise AssertionError("an empty entry should have been rejected")

    print()
    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the structure — prefix tree, border table, reversed tree, budgeted walk — and what a node means in this problem. |
| Reason about options | Four to six bullets before any code, with the scan-everything alternative named and costed rather than dismissed. |
| Assemble the solution | Idiomatic Python; one clear representation for a node; type hints on every function. |
| Measure it | A trace on at least two inputs, one of them a degenerate case. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off, and the improvement — in terms of the register's own size, not abstract n. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-09/homework/`, one file per
problem:

```
frame-writeups/c2-week-09/homework/
├── problem-1-smudged-stencil.md
├── problem-2-growable-dock-sign.md
├── problem-3-splice-point.md
├── problem-4-radio-tail-watch.md
├── problem-5-double-stamped-label.md
└── problem-6-one-key-typo-desk.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Smudged Stencil | 35 min | 10 min | 45 min |
| 2 — Growable Dock Sign | 30 min | 10 min | 40 min |
| 3 — Splice Point | 40 min | 15 min | 55 min |
| 4 — Radio Tail Watch | 35 min | 15 min | 50 min |
| 5 — Double-Stamped Label | 40 min | 15 min | 55 min |
| 6 — One-Key Typo Desk | 35 min | 15 min | 50 min |

About five hours, and Mock #2 grades the recognition step rather than the code.
