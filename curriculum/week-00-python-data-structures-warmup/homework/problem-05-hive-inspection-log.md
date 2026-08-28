# Problem 5 — The Hive Inspection Log

> **Topic:** `defaultdict` for grouping, `Counter` for counting, and why `most_common` is not the ranking you were asked for
> **Lecture:** [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Beginner
> **Target time:** 25 minutes
> **Why this one:** `Counter` removes a whole class of work, and `most_common` is the method everybody reaches for next. It has a tie-break, nobody tells you what it is, and it is almost never the one the specification wanted. This log is built so that the difference shows up in the first two rows.

## The Brief

A beekeeper walks the apiary once a month and writes a line for every hive she
looks at:

```python
("hive-02", "varroa")
```

Four questions come out of that log.

**What did each hive show?** Every finding for a hive, in the order she noticed
it.

**How often did each finding come up?** Across the whole apiary.

**What are the top few findings for the report?** Most common first — and where
two findings came up the same number of times, **alphabetically**. That is the
apiary's rule, written down.

**Which hives had a particular problem?** Each hive once, in name order.

Two tools do most of this.

A **`defaultdict(list)`** is a dict that builds an empty list the moment you
touch a key that is not there yet. `grouped[hive].append(finding)` just works,
first time and every time — no `setdefault`, no check.

A **`Counter`** is a dict that answers `0` instead of raising for anything it
has never seen. `Counter(findings)` counts a whole sequence in one pass.

And here is the trap the page is built on. `Counter.most_common(2)` looks
exactly like the ranking you were asked for. It is not. When two findings tie,
`most_common` puts the one that was **written down first** ahead — insertion
order — because that is the order the underlying dict is in and nothing sorts
it further. This log has `varroa` and `queen seen` tied on three each, and
`varroa` was written first. The apiary's rule says `queen seen` goes first,
because `q` comes before `v`.

So the ranking function has to sort, and it has to say both rules in one key:
`(-count, finding)`.

## Starter

Create `problem-05-hive-inspection-log.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""problem-05-hive-inspection-log.py — what the beekeepers found.

Every hive visit is logged as (hive, finding). Four questions come out of
that log at the end of the month, and each one is a different shape of dict.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import Counter, defaultdict

INSPECTIONS: list[tuple[str, str]] = [
    ("hive-02", "varroa"),
    ("hive-01", "queen seen"),
    ("hive-01", "brood healthy"),
    ("hive-03", "varroa"),
    ("hive-02", "queen seen"),
    ("hive-03", "low stores"),
    ("hive-01", "varroa"),
    ("hive-04", "queen seen"),
    ("hive-02", "low stores"),
]


def findings_by_hive(log: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group the log by hive, keeping the order things were noticed.

    Returns:
        A plain dict from hive to its findings, hives in first-seen order.
    """
    # TODO: defaultdict(list) in the loop, plain dict on the way out
    ...


def finding_tally(log: list[tuple[str, str]]) -> Counter[str]:
    """Count how often each finding was written down."""
    # TODO: one Counter over a generator expression
    ...


def top_findings(log: list[tuple[str, str]], wanted: int) -> list[tuple[str, int]]:
    """Rank findings, most common first, ties broken alphabetically.

    Returns:
        Up to `wanted` (finding, count) pairs. NOT most_common(wanted) —
        that breaks ties by insertion order, which is not the rule here.
    """
    # TODO: sorted() with a tuple key, then slice
    ...


def hives_with(log: list[tuple[str, str]], finding: str) -> list[str]:
    """Return every hive where one particular thing was found, sorted."""
    # TODO: a set comprehension, then sorted()
    ...


# ---- Self-check ----
if __name__ == "__main__":
    grouped = findings_by_hive(INSPECTIONS)
    for hive in sorted(grouped):
        print(f"{hive}: {', '.join(grouped[hive])}")
    for finding, count in top_findings(INSPECTIONS, 3):
        print(f"  {count} x {finding}")
    print(f"varroa in: {', '.join(hives_with(INSPECTIONS, 'varroa'))}")

    tally = finding_tally(INSPECTIONS)
    assert tally["varroa"] == 3
    assert tally["queen seen"] == 3
    assert tally["kite"] == 0  # a Counter answers 0, it does not raise
    assert tally.most_common(2)[0][0] == "varroa"  # insertion order wins here
    assert top_findings(INSPECTIONS, 2)[0][0] == "queen seen"  # A to Z wins here
    assert top_findings(INSPECTIONS, 3) == [
        ("queen seen", 3),
        ("varroa", 3),
        ("low stores", 2),
    ]
    assert grouped["hive-01"] == ["queen seen", "brood healthy", "varroa"]
    assert list(grouped) == ["hive-02", "hive-01", "hive-03", "hive-04"]
    assert hives_with(INSPECTIONS, "varroa") == ["hive-01", "hive-02", "hive-03"]
    assert hives_with(INSPECTIONS, "wax moth") == []
    assert top_findings([], 3) == []
    assert len(INSPECTIONS) == 9  # the log is untouched
    print("All checks passed.")
```

Three things you need before you start.

**`defaultdict(list)`** takes a function — `list`, not `list()` — and calls it
to build a value whenever a missing key is touched. It has one sharp edge:
*reading* a missing key inserts it. `if grouped["hive-09"]:` on a defaultdict
quietly adds `hive-09` with an empty list. Use `.get` when you only want to
look.

**`dict(grouped)`** turns a defaultdict back into a plain dict, keeping the
order and the values. Returning the plain one means a caller who reads a key
you never saw gets a `KeyError` rather than a silent empty list — which is the
honest answer for a hive nobody inspected.

**`Counter[str]` in a type hint** means "a Counter whose keys are strings". A
`Counter` is a dict subclass, so everything you know about dicts still applies.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-05-hive-inspection-log.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `findings_by_hive` returns a **plain** dict, hives in first-seen order, each
   hive's findings in the order they were noticed.
2. `finding_tally` returns a `Counter` over the findings.
3. `top_findings` ranks by count descending, ties alphabetically, and returns at
   most `wanted` pairs.
4. `top_findings([], 3)` returns `[]`.
5. `hives_with` returns each matching hive once, sorted A to Z, and `[]` when
   nothing matches.
6. `INSPECTIONS` is unchanged. Every function keeps its type hints and its
   docstring.

## Constraints

- **Do not use `most_common(wanted)` for the ranking.** It ties by insertion
  order, and this apiary's rule is alphabetical. The two disagree in this log
  on purpose. `most_common` is the right tool when *you* get to choose the tie
  rule, or when there are no ties — and knowing which situation you are in is
  the whole skill.

- **Return a plain dict, not the `defaultdict`.** Handing a defaultdict to a
  caller hands them a dict that grows when they read it. Somebody checks
  `report["hive-09"]`, gets an empty list, sees no error, and the apiary's
  report now lists a hive that was never visited.

- **Dedupe the hives with a set, not with `if hive not in found`.** Checking a
  growing list is a walk of the answer so far, which turns an `O(n)` pass into
  `O(n²)`. The set does it in one hop. Then sort once at the end, because the
  requirement asks for name order and a set has no order to give.

- **Sort only where a rule asks for order.** The grouped findings keep arrival
  order because that is what the beekeeper noticed. The hive list is sorted
  because the report says so. Sorting things nobody asked to be sorted destroys
  information the dict was keeping for free.

- **At most 2000 visits a month across at most 300 hives, with at most 40
  distinct findings.** Those are the numbers for a large commercial apiary
  inspected monthly, and 40 findings is a full inspection sheet. The finding
  bound is the interesting one: it means the `Counter` is tiny however long the
  log is, so ranking is `O(distinct log distinct)` — a sort of forty things,
  not of two thousand.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-05-hive-inspection-log.py
@@STDOUT:problem-05-hive-inspection-log-solution.py@@
```

The two ranking lines are the point of the page. `queen seen` and `varroa` both
appear three times, and `queen seen` prints first — alphabetically. In the log,
`varroa` was written down first, so `most_common(2)` would have put it on top.
Both are three; only one of them is the answer that was asked for.

Note also that the hive rows are printed in **sorted** order by the self-check,
while `list(grouped)` is in first-seen order. Two different orderings of the
same dict, and the code says which is which.

## Steps

1. Create the file, paste the starter, and run it. It fails at
   `sorted(grouped)` because `findings_by_hive` returned `None`.
2. Write `findings_by_hive` with a `defaultdict(list)`, returning
   `dict(grouped)`.
3. Write `finding_tally`. One line.
4. Write `top_findings` as `tally.most_common(wanted)` first, on purpose. Run
   the file. One assert fails, and it is the one that names `queen seen`. Read
   the two asserts above it — they are documenting the disagreement.
5. Now write it properly: sort `tally.items()` with `(-count, finding)` and
   slice.
6. Write `hives_with` with a set comprehension inside `sorted`.
7. When it passes, try `tally["wax moth"]` in a REPL and then check `len(tally)`
   before and after. Then do the same with `grouped["hive-09"]` on a
   `defaultdict` and compare. One of the two grows.

## The Solution

```python
@@CODE:problem-05-hive-inspection-log-solution.py@@
```

**`defaultdict(list)` makes the grouping loop one line.**

```python
grouped[hive].append(finding)
```

No `setdefault`, no `if hive not in grouped`. The defaultdict calls `list` to
build an empty list the first time each hive is touched. Compare Exercise 4's
`shelf.setdefault(route, []).append(item)` — both are right, and the difference
is where the default lives: in the container, or at the call site. The
defaultdict is shorter and it applies everywhere, including places you did not
mean it to.

Which is why the return is `dict(grouped)`. Inside the function, a container
that fills in the blanks is exactly what you want. Outside it, a caller reading
a hive that does not exist should get `KeyError` and know they asked for
something that is not there.

**`Counter` is the counting loop, gone.**

```python
return Counter(finding for _hive, finding in log)
```

One pass, `O(n)` time and `O(k)` space for `k` distinct findings. And
`tally["kite"]` is `0` rather than a `KeyError`, which removes the missing-key
question from every line that reads a count.

**`top_findings` sorts, and the sort is the requirement.**

```python
ordered = sorted(tally.items(), key=lambda pair: (-pair[1], pair[0]))
return ordered[:wanted]
```

`most_common(wanted)` would be shorter, faster and wrong. Its ties fall to
insertion order — the order findings were first written down — and this apiary
ranks ties alphabetically. Once you have decided to sort, the tuple key says
both rules in one pass, exactly as Problem 4 does: negate the count so that
"more" sorts first, leave the text alone so it goes A to Z.

The slice at the end needs no guard. `ordered[:3]` on a list of two gives two,
and `top_findings([], 3)` gives `[]`, because slices clamp where indexes raise.

**`hives_with` builds a set and then sorts it once.**

```python
return sorted({hive for hive, noted in log if noted == finding})
```

The set comprehension does the deduplication in one hop per entry; `sorted`
turns it into the ordered list the report asks for. Doing it the other way —
appending to a list and checking `if hive not in found` — is a scan of the
answer for every entry, and it is the same `O(n²)` that Exercise 5 spends a page
on, hiding inside an innocent-looking `if`.

**The costs, together.** Grouping and tallying are one pass each, `O(n)` time,
`O(n)` and `O(k)` space. Ranking is `O(k log k)`, a sort of the *distinct*
findings, which the constraints bound at forty — so the ranking cost does not
grow with the log at all. `hives_with` is `O(n)` to build the set and
`O(h log h)` to sort the hives that matched. Being able to say "the sort is
over the distinct findings, not the log" is the difference between quoting a
complexity and understanding one.

## Download and run

Download
[problem-05-hive-inspection-log-solution.py](./problem-05-hive-inspection-log-solution.py)
and run it:

```bash
python problem-05-hive-inspection-log-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-05-hive-inspection-log.py`.

## Common bugs to catch

- **`varroa` ranks above `queen seen`.** You used `most_common`. Both are three;
  `most_common` broke the tie by which was written down first, and the apiary
  breaks it alphabetically. No error, and on a log with no ties the two
  functions agree perfectly — which is why this reaches production.

- **`KeyError: 'hive-01'`.** You used a plain dict and indexed it in the loop:

  ```text
  Traceback (most recent call last):
      grouped[hive].append(finding)
      ~~~~~~~^^^^^^
  KeyError: 'hive-01'
  ```

  The first time each hive appears there is no list to append to. That is what
  `defaultdict` and `setdefault` are both for.

- **`len(tally)` grew after you only read from it.** You made the tally a
  `defaultdict(int)` instead of a `Counter`:

  ```python
  tally = defaultdict(int)
  if tally["wax moth"] > 0:   # this INSERTS "wax moth" with the value 0
      ...
  ```

  A `Counter` returns `0` for a missing key **without** storing it. A
  `defaultdict(int)` stores. Use `Counter` for counting, and `.get(key, 0)` on
  a defaultdict when you only want to look.

- **The report lists a hive nobody visited.** You returned the `defaultdict`
  itself and a caller read a missing key. The dict grew on read. Return
  `dict(grouped)`.

- **`hives_with` returns a hive twice.** You appended to a list without
  checking, or checked with `if hive not in found` and the check was on the
  wrong variable. A set comprehension cannot produce a duplicate.

- **`TypeError: unhashable type: 'list'`.** You tried to count something that
  cannot be a dict key:

  ```text
  TypeError: unhashable type: 'list'
  ```

  `Counter` is a dict, so everything it counts must be hashable. Counting
  `[hive, finding]` pairs fails; counting `(hive, finding)` tuples works.

- **The hive rows print in first-seen order.** You looped over `grouped`
  directly instead of `sorted(grouped)`. Both orderings are legitimate; the
  self-check asks for one of them in the printout and the other in the assert,
  so that the difference is visible rather than assumed.

## Under the hood

<details>
<summary>Under the hood — what most_common costs, and why Counter is not always the answer</summary>

**`most_common` has two costs, depending on how you call it.**

| Call | Cost | What it does |
|---|---|---|
| `counts.most_common()` | `O(k log k)` | sorts every distinct item |
| `counts.most_common(w)` | `O(k log w)` | keeps a heap of size `w` |

The second one is worth memorising. Asking for the top 10 of a million distinct
items does not sort a million things — it walks them once, keeping a heap of
ten. That is `heapq.nlargest` underneath, and Week 8 makes you build it.

Its tie-break is insertion order, and that is not documented as a promise so
much as it is what falls out of a stable sort over a dict that remembers
insertion order. Which is precisely why a specification with its own tie rule
means you sort yourself.

**Counter arithmetic is occasionally the entire solution.**

```python
Counter("mississippi") - Counter("misp")     # keeps only positive counts
```

`a - b` answers "what is left over", `a & b` answers "what do both have", and
`a + b` merges. `not (Counter(target) - Counter(pool))` answers "can I build
`target` out of `pool`" in one line, in `O(n + m)`.

**Two frequency maps are equal exactly when the two sequences are
rearrangements of each other**, and that comparison is `O(k)`:

```python
Counter(a) == Counter(b)     # O(n + m) total, beats sorting's O(n log n)
```

So why does anyone sort to compare instead? Because a `Counter` is **not
hashable** — it is a mutable dict — so it cannot be a dict key or a set member.
When you need to *group* by "same contents", you need a key, and
`tuple(sorted(items))` or a `frozenset` is what you reach for. Challenge 2 is
built on exactly that. When you only need to *compare two*, `Counter` wins on
cost. Knowing which the problem asks for is the Frame step.

**`defaultdict`'s factory is a function, not a value.** `defaultdict(list)`
calls `list` each time, so every key gets its own new list. `defaultdict([])`
raises `TypeError: first argument must be callable or None` — and it is a good
thing it does, because a single shared list handed to every key is the aliasing
bug from Exercise 3 wearing a different hat.

</details>

## Acceptance checklist

- [ ] `python problem-05-hive-inspection-log.py` prints four hive rows, three
      ranking rows, the varroa line, then `All checks passed.`
- [ ] `queen seen` ranks above `varroa`.
- [ ] `findings_by_hive` returns a plain dict.
- [ ] `hives_with` dedupes with a set, not a list scan.
- [ ] `top_findings([], 3)` returns `[]` with no guard needed.
- [ ] You can say what `most_common`'s tie-break is and when it is acceptable.
- [ ] You can say why a `Counter` cannot be a dict key.

## Stretch

- **Ask the log the other way round: which findings did each hive have that
  nobody else did?**

  ```python
  def unique_findings(log: list[tuple[str, str]]) -> dict[str, list[str]]:
      """Return the findings that turned up at exactly one hive."""
      hives_per_finding: dict[str, set[str]] = {}
      for hive, finding in log:
          hives_per_finding.setdefault(finding, set()).add(hive)
      out: dict[str, list[str]] = {}
      for finding, hives in hives_per_finding.items():
          if len(hives) == 1:
              out.setdefault(next(iter(hives)), []).append(finding)
      return out
  ```

  ```text
  {'hive-01': ['brood healthy']}
  ```

  Two dicts, one built from the other, and no comparison of any hive against
  any other. `next(iter(hives))` is how you take the single member out of a set
  of one — there is no `hives[0]`, because a set has no positions.

- **Count pairs instead of single findings.**

  ```python
  pairs = Counter(INSPECTIONS)
  print(pairs.most_common(3))
  print(len(pairs), "distinct hive-finding pairs")
  ```

  ```text
  [(('hive-02', 'varroa'), 1), (('hive-01', 'queen seen'), 1), (('hive-01', 'brood healthy'), 1)]
  9 distinct hive-finding pairs
  ```

  Every pair is unique in this log, which is itself a finding: no hive was
  written down with the same problem twice. It works because a **tuple is
  hashable**, so it can be a `Counter` key. Try it with `list(pair)` instead
  and read the `TypeError`.

- **See a `defaultdict` grow while you are only looking at it.**

  ```python
  from collections import defaultdict

  grouped = defaultdict(list)
  grouped["hive-01"].append("varroa")
  print(len(grouped))
  if grouped["hive-09"]:
      pass
  print(len(grouped), dict(grouped))
  ```

  ```text
  1
  2 {'hive-01': ['varroa'], 'hive-09': []}
  ```

  One `if` that did nothing, and the apiary now has a hive-09. This is the
  single reason the solution returns a plain dict.

Next: [Problem 6 — The Tool Crib's Sign-Offs](./problem-06-tool-crib-signoffs.md).
