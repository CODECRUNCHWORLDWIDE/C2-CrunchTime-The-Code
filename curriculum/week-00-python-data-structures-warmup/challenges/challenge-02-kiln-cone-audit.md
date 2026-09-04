# Challenge 2 — The Kiln Cone Audit

> **Topic:** two topics at once — ranking records with a tuple key, and using a `frozenset` as a dict key to find things that match
> **Lecture:** [02 — Lists, Tuples and the Dynamic Array](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md) and [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** "group the things that are the same" is one of the most common shapes in interview coding, and the whole trick is choosing a key that two matching things both produce. Here the key is a **set** — and a set cannot be a dict key, because it can change. `frozenset` is the answer, and knowing *why* it is the answer is the difference between remembering an idiom and understanding hashability.

## The Brief

A pottery runs five kilns. Every firing goes in the book as three things: which
kiln, which **cone**, and how many hours it ran.

```python
("bisque-1", "04", 9)
```

A cone is the code for a firing temperature. Potters write them as `04`, `06`,
`6`, `10` — and those are **labels, not numbers**. Cone `04` is cooler than
cone `6`, and cone `06` is cooler than `04`. The numbering is genuinely like
that. Your program never has to understand it; it only has to stop treating the
labels as arithmetic.

The studio wants two things out of the book.

**A league table.** Every kiln, most hours first. Where two kilns ran the same
hours, the earlier name goes first — as text, A to Z.

**The kilns that are doing the same job.** Two kilns match when the **set** of
cones they have fired is exactly the same, ignoring how often and in what
order. Report only the groups with two or more kilns in them, biggest group
first, and inside each group put the names in order.

That second question is the interesting one. To find things that match, you
build the thing they have in common and use it as a **key** — the same move as
grouping by route in Exercise 4, except the key here is not a string. It is a
set of cones. And this happens:

```python
groups[{"04", "06"}] = ["bisque-1"]
# TypeError: unhashable type: 'set'
```

A dict files a key by its hash. A set can have things added to it, which would
change its hash, and then the dict could never find the entry again — so Python
refuses up front rather than losing your data later. A **`frozenset`** is a set
that cannot be changed, so its hash is safe, so it may be a key.

That is the rule stated properly: **a key must be immutable all the way down.**

## Starter

Create `challenge-02-kiln-cone-audit.py` in your practice folder and paste this
in. Fill in every `TODO`.

```python
"""challenge-02-kiln-cone-audit.py — audit the pottery's kilns.

Every firing is logged as (kiln, cone, hours). Produce a league table of
kiln hours, and find the kilns whose cone sets match exactly.

A dict adds the hours up. A frozenset is what lets one kiln's set of cones
become the key that finds its twins.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

FIRINGS: list[tuple[str, str, int]] = [
    ("bisque-1", "04", 9),
    ("glaze-a", "6", 11),
    ("bisque-2", "04", 8),
    ("glaze-b", "6", 12),
    ("bisque-1", "06", 7),
    ("glaze-a", "10", 6),
    ("test-kiln", "6", 4),
    ("bisque-2", "06", 9),
    ("glaze-b", "10", 5),
    ("test-kiln", "10", 3),
    ("bisque-1", "04", 5),
]


def hours_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, int]:
    """Add up the hours each kiln ran, kilns in first-seen order."""
    # TODO: one pass, get(kiln, 0) + hours
    ...


def cones_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, frozenset[str]]:
    """Collect the distinct cone codes each kiln has fired."""
    # TODO: gather into sets, then freeze each one on the way out
    ...


def ranked(firings: list[tuple[str, str, int]]) -> list[tuple[str, int]]:
    """Rank kilns by hours, most first, ties by kiln name A to Z."""
    # TODO: sorted() with ONE tuple key that says both rules
    ...


def twin_kilns(firings: list[tuple[str, str, int]]) -> list[list[str]]:
    """Find the kilns whose cone sets match exactly.

    Returns:
        One list per group of two or more kilns sharing an identical cone
        set. Names inside a group sorted A to Z; groups ordered by size,
        largest first, ties broken by the group's first name.
    """
    # TODO: group by the frozenset, drop the singletons, then order
    ...


def audit(firings: list[tuple[str, str, int]]) -> str:
    """Render the league table and the matching cone sets, no trailing newline."""
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(audit(FIRINGS))

    totals = hours_by_kiln(FIRINGS)
    assert totals == {
        "bisque-1": 21,
        "glaze-a": 17,
        "bisque-2": 17,
        "glaze-b": 17,
        "test-kiln": 7,
    }
    assert list(totals) == ["bisque-1", "glaze-a", "bisque-2", "glaze-b", "test-kiln"]
    assert ranked(FIRINGS)[:2] == [("bisque-1", 21), ("bisque-2", 17)]
    assert [kiln for kiln, _hours in ranked(FIRINGS)][-1] == "test-kiln"
    assert cones_by_kiln(FIRINGS)["bisque-1"] == frozenset({"04", "06"})
    assert twin_kilns(FIRINGS) == [
        ["glaze-a", "glaze-b", "test-kiln"],
        ["bisque-1", "bisque-2"],
    ]
    assert twin_kilns([]) == []
    assert ranked([]) == []
    assert FIRINGS[0] == ("bisque-1", "04", 9)  # the log is untouched
    print("All checks passed.")
```

Four things you need before you start.

**A tuple key says a whole ordering rule.** `key=lambda pair: (-pair[1],
pair[0])` means *most hours first, and on a tie the earlier name.* Python
compares tuples box by box and stops at the first difference. Negate the number
you want descending; leave `reverse` alone, because `reverse=True` would flip
the names as well.

**`frozenset(cones)`** turns a set into a frozen one. Same members, same
equality, same speed to test — and hashable, so it may be a dict key or a
member of another set. It has no `add` or `remove`, which is the whole point.

**Two frozensets with the same members are equal and hash the same,** whatever
order they were built in. That is what makes the grouping work: `bisque-1`
built its set as `04` then `06`, `bisque-2` built it as `04` then `06` too —
but even if one had gone the other way round, the keys would match.

**`sorted` is stable,** which means tied items stay in the order they arrived.
That sounds helpful and here it is the trap: three kilns tie on 17 hours, so a
key with only the hours in it leaves them in log order, not in name order. The
expected output shows which.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/challenges/challenge-02-kiln-cone-audit.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `hours_by_kiln` totals the hours per kiln, kilns in first-seen order.
2. `cones_by_kiln` returns each kiln's **distinct** cones as a `frozenset`.
3. `ranked` returns `(kiln, hours)` pairs, most hours first, ties by kiln name
   A to Z as text.
4. `twin_kilns` returns only groups of **two or more**; names inside a group
   sorted A to Z; groups ordered by size descending, ties by the group's first
   name.
5. `twin_kilns([])` and `ranked([])` both return `[]`.
6. `audit` prints one row per kiln in league order — name padded to 10, hours
   right-aligned in 3 with an `h`, then the sorted cones — then
   `matching cone sets:` and one indented line per group.
7. `FIRINGS` is unchanged. Every function keeps its type hints and its
   docstring.

## Constraints

- **The grouping key is a `frozenset`, not a sorted tuple or a joined string.**
  All three would work here. `frozenset` is the one that says what it means: a
  collection where order and repeats do not count. `tuple(sorted(cones))` says
  "an ordered sequence I have canonicalised", which is a different claim about
  the data, and `",".join(sorted(cones))` says "a string" and breaks the day a
  cone code contains a comma. Choose the type that matches the idea.

- **Say both ordering rules in one key.** `sorted(totals.items(), key=lambda
  pair: (-pair[1], pair[0]))`. Sorting twice — once by name, then again by
  hours — happens to give the same answer here, but it is two full passes, it
  reads backwards (the *last* sort is the *first* rule), and it stops working
  the moment one rule needs the opposite direction.

- **Do not use `reverse=True`.** It flips the whole key, so hours would go
  down **and** names would go Z to A, and the three tied kilns would come out
  backwards. A minus sign on the number mixes the two directions in one pass.
  Only numbers negate, which is why the name is left alone.

- **Cone codes are text and sort as text.** `"10"` sorts before `"6"`, because
  `"1"` comes before `"6"`. That is why the expected output reads
  `cones 10, 6`. It is not a bug and it is not to be "fixed" — a cone code is
  a label, and inventing a numeric ordering for it would need pottery knowledge
  this program does not have and does not need.

- **Build each kiln's cones as a `set` first, then freeze once at the end.**
  A `frozenset` cannot be added to, so building one up would mean creating a
  new frozenset per cone — `O(cones²)` work for a set you are about to finish
  anyway. Gather in a mutable set, freeze on the way out. This is the general
  shape for every immutable container: build loose, freeze once.

- **At most 200 kilns and 100,000 firings.** A studio with 200 kilns is an
  industrial pottery, and 100,000 firings is decades of book. The bound matters
  because it rules out the obvious wrong approach to the twins: comparing every
  kiln against every other is `O(kilns² × cones)`, which is 40,000 comparisons
  here and fine — and is the same shape that becomes unusable the moment
  "kilns" is "customers" and there are a million of them. Grouping by key is
  `O(firings)`, and the reason to write it that way now is that it is not
  harder.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-kiln-cone-audit.py
bisque-1    21h  cones 04, 06
bisque-2    17h  cones 04, 06
glaze-a     17h  cones 10, 6
glaze-b     17h  cones 10, 6
test-kiln    7h  cones 10, 6
matching cone sets:
  glaze-a, glaze-b, test-kiln
  bisque-1, bisque-2
All checks passed.
```

Read rows two, three and four. All three kilns ran 17 hours, and they come out
`bisque-2, glaze-a, glaze-b` — name order. In the log they appear as `glaze-a`,
`bisque-2`, `glaze-b`, so if your table shows that instead, your key has one
part where it needs two and the stable sort left the tie where it found it.

Then the groups. `glaze-a`, `glaze-b` and `test-kiln` have all fired cones `6`
and `10` and nothing else, so they are one group of three. `bisque-1` and
`bisque-2` have both fired `04` and `06`. The three-kiln group comes first
because it is bigger.

## Steps

1. Create the file, paste the starter, and run it. `audit` returns `None`, so
   the first thing printed is `None` and then the asserts fail.
2. Write `hours_by_kiln`. It is Exercise 4's counting loop with `+ hours`
   instead of `+ 1`.
3. Write `cones_by_kiln`. Gather into `dict[str, set[str]]` in the loop, then
   return a dict comprehension that freezes each one.
4. Write `ranked` with the hours only in the key, and run it. Look at the three
   tied kilns. **Then** add the name to the key and look again. Seeing the
   before and the after is worth more than being told.
5. Write `twin_kilns`. Try `groups[cones]` with a plain `set` as the key first,
   on purpose, and read the `TypeError`.
6. Fix it with the frozensets you are already returning, then drop the
   singletons with `if len(names) > 1` and sort the groups.
7. Write `audit` last. Build a list of rows and join once.
8. When it passes, add a firing of your own to `FIRINGS` — say
   `("test-kiln", "04", 2)` — and predict what happens to both halves of the
   report before you run it. `test-kiln` leaves its group, the group shrinks to
   two, and the group ordering changes. Predicting that correctly is the sign
   you have understood the key.

## The Solution

```python
"""challenge-02-kiln-cone-audit-solution.py — audit the pottery's kilns.

Every firing is logged as (kiln, cone, hours). The studio wants two things
out of that log: a league table of kiln hours, and the kilns that are doing
the same job as each other.

A dict adds the hours up. A frozenset is what lets one kiln's set of cones
become the key that finds its twins.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

FIRINGS: list[tuple[str, str, int]] = [
    ("bisque-1", "04", 9),
    ("glaze-a", "6", 11),
    ("bisque-2", "04", 8),
    ("glaze-b", "6", 12),
    ("bisque-1", "06", 7),
    ("glaze-a", "10", 6),
    ("test-kiln", "6", 4),
    ("bisque-2", "06", 9),
    ("glaze-b", "10", 5),
    ("test-kiln", "10", 3),
    ("bisque-1", "04", 5),
]


def hours_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, int]:
    """Add up the hours each kiln ran.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        A dict from kiln to total hours, kilns in first-seen order.
    """
    totals: dict[str, int] = {}
    for kiln, _cone, hours in firings:
        totals[kiln] = totals.get(kiln, 0) + hours
    return totals


def cones_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, frozenset[str]]:
    """Collect the distinct cone codes each kiln has fired.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        A dict from kiln to a frozenset of its cone codes. Frozen because
        these sets are used as dict keys in `twin_kilns`.
    """
    gathered: dict[str, set[str]] = {}
    for kiln, cone, _hours in firings:
        gathered.setdefault(kiln, set()).add(cone)
    return {kiln: frozenset(cones) for kiln, cones in gathered.items()}


def ranked(firings: list[tuple[str, str, int]]) -> list[tuple[str, int]]:
    """Rank the kilns by hours run, most first.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        (kiln, hours) pairs, most hours first, ties broken by kiln name
        A to Z as text.
    """
    totals = hours_by_kiln(firings)
    return sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))


def twin_kilns(firings: list[tuple[str, str, int]]) -> list[list[str]]:
    """Find the kilns whose cone sets match exactly.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        One list per group of two or more kilns sharing an identical cone
        set. Names inside a group are sorted A to Z; groups are ordered by
        size, largest first, ties broken by the group's first name.
    """
    groups: dict[frozenset[str], list[str]] = {}
    for kiln, cones in cones_by_kiln(firings).items():
        groups.setdefault(cones, []).append(kiln)

    found = [sorted(names) for names in groups.values() if len(names) > 1]
    return sorted(found, key=lambda names: (-len(names), names[0]))


def audit(firings: list[tuple[str, str, int]]) -> str:
    """Render the whole audit as text.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        The league table, then the matching cone sets. No trailing newline.
    """
    cones = cones_by_kiln(firings)
    rows = [
        f"{kiln:<10} {hours:3d}h  cones {', '.join(sorted(cones[kiln]))}"
        for kiln, hours in ranked(firings)
    ]
    rows.append("matching cone sets:")
    for group in twin_kilns(firings):
        rows.append(f"  {', '.join(group)}")
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(audit(FIRINGS))

    totals = hours_by_kiln(FIRINGS)
    assert totals == {
        "bisque-1": 21,
        "glaze-a": 17,
        "bisque-2": 17,
        "glaze-b": 17,
        "test-kiln": 7,
    }
    assert list(totals) == ["bisque-1", "glaze-a", "bisque-2", "glaze-b", "test-kiln"]
    assert ranked(FIRINGS)[:2] == [("bisque-1", 21), ("bisque-2", 17)]
    assert [kiln for kiln, _hours in ranked(FIRINGS)][-1] == "test-kiln"
    assert cones_by_kiln(FIRINGS)["bisque-1"] == frozenset({"04", "06"})
    assert twin_kilns(FIRINGS) == [
        ["glaze-a", "glaze-b", "test-kiln"],
        ["bisque-1", "bisque-2"],
    ]
    assert twin_kilns([]) == []
    assert ranked([]) == []
    assert FIRINGS[0] == ("bisque-1", "04", 9)  # the log is untouched
    print("All checks passed.")
```

**`cones_by_kiln` builds loose and freezes once.**

```python
gathered.setdefault(kiln, set()).add(cone)
...
return {kiln: frozenset(cones) for kiln, cones in gathered.items()}
```

The loop needs a container it can add to, so it uses a plain `set`. The result
needs a container that can be a key, so the comprehension freezes each one
exactly once at the end. `frozenset(cones)` is `O(len(cones))`, and it happens
once per kiln rather than once per firing.

**The frozenset is the key, and that is the whole of the twin-finding.**

```python
groups.setdefault(cones, []).append(kiln)
```

Two kilns that fired the same cones produce two frozensets that are equal and
hash the same, so they land in the same pigeonhole, so they end up in the same
list. Nothing compares one kiln to another anywhere in this function. That is
what a key buys you: **matching without comparing.** The alternative — every
kiln against every other — is `O(kilns²)` and gets slower quadratically, while
this is one pass.

Try it with an ordinary `set` and Python stops you with `TypeError: unhashable
type: 'set'`. It is not being fussy. A set that could be a key could be changed
after filing, and the dict would then be holding an entry under a hash the key
no longer produces — an entry that is in the dict and cannot be found. Refusing
at the door is the only safe answer, and the same rule is why a list cannot be
a key and a tuple usually can.

**Both orderings are one tuple key each.**

```python
sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
sorted(found, key=lambda names: (-len(names), names[0]))
```

Read each as an English sentence. *Most hours first, then the earlier name.*
*Biggest group first, then the group whose first name is earlier.* The minus
sign is the direction switch on the number; the second box is left alone
because names go up. This shape — `(-what_i_want_most_of, what_breaks_the_tie)`
— appears in almost every ranking you will write, and it is worth being able to
type without thinking.

**`sorted(names)` inside a group, and `names[0]` after it.** The names are
sorted before the groups are ordered, so `names[0]` is genuinely the earliest
name in the group and the group-ordering tie-break is well defined. Do it the
other way round and the tie-break depends on which kiln happened to be logged
first, which is not a rule anybody wrote down.

**`audit` sorts the cones only for printing.** The frozensets have no order —
they never did — so the report has to choose one, and A-to-Z as text is the
choice. Notice that this sort happens in the rendering function and nowhere
else: the data keeps its true shape, and the presentation layer does the
presenting. Mixing those two up is how a set ends up stored as a sorted list
"so it prints nicely" and then two equal things stop being equal.

**The cost.** `hours_by_kiln` and `cones_by_kiln` are each `O(f)` for `f`
firings, one pass with `O(1)`-average dict work. `ranked` is `O(k log k)` for
`k` kilns, because it sorts. `twin_kilns` is one pass over the kilns to group —
each frozenset hash is `O(cones)` — then `O(g log g)` to order `g` groups.
Space is `O(k × cones)` for the gathered sets. The whole audit is dominated by
one pass over the log plus one sort of the kilns, and the thing it avoids is
the `O(k²)` all-pairs comparison. Say that as one sentence and you have the
Examine step of FRAME for this problem.

## Run it

Copy the worked answer on this page into `challenge-02-kiln-cone-audit.py` and run it:

```bash
python challenge-02-kiln-cone-audit.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-02-kiln-cone-audit.py`.

## Common bugs to catch

- **`TypeError: unhashable type: 'set'`.** You used a plain set as the key:

  ```text
  Traceback (most recent call last):
      groups.setdefault(cones, []).append(kiln)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: unhashable type: 'set'
  ```

  This is the error the challenge is built around. Freeze the set. And be able
  to say the reason: a key is filed by its hash, a set's contents can change,
  so its hash could change, so the entry could become unfindable.

- **`AttributeError: 'frozenset' object has no attribute 'add'`.** You tried to
  build the frozen version up one cone at a time:

  ```text
  AttributeError: 'frozenset' object has no attribute 'add'
  ```

  A frozenset has no way to change it — that is the entire feature. Gather in a
  `set`, freeze at the end.

- **The three 17-hour kilns come out `glaze-a, bisque-2, glaze-b`.** Your key
  is `-pair[1]` alone. Python's sort is **stable**, so tied items keep the
  order they arrived in, and that order is the log's. You got *an* answer; the
  rule asked for a specific one.

- **`TypeError: bad operand type for unary -: 'str'`.** You negated the name as
  well as the hours:

  ```text
  Traceback (most recent call last):
      sorted(totals.items(), key=lambda pair: (-pair[1], -pair[0]))
                                                         ^^^^^^^^
  TypeError: bad operand type for unary -: 'str'
  ```

  Only numbers negate, and you do not want the names reversed anyway.

- **Every kiln appears in `matching cone sets`, each on its own line.** You
  forgot `if len(names) > 1`. A group of one is not a match — it is a kiln
  doing its own job — and reporting it turns a short useful list into a
  restatement of the kiln register.

- **`cones 6, 10` instead of `cones 10, 6`.** You sorted the cones as numbers
  with `key=int`. It looks tidier and it is a different program: `04` and `06`
  would then both become `4` and `6`, two cone codes that mean something else
  entirely. The codes are labels. Sort them as text.

- **A kiln's cones come out with repeats in them.** You collected into a list
  instead of a set. `bisque-1` fired cone `04` twice, so its list is
  `["04", "06", "04"]`, which is not equal to `bisque-2`'s `["04", "06"]` — and
  the two kilns stop being twins for a reason that has nothing to do with what
  they fire. "Distinct" is doing real work in the requirement.

## Under the hood

<details>
<summary>Under the hood — hashability, and why a frozenset's hash is order-free</summary>

**The rule, stated exactly.** An object may be a dict key or a set member when
it is **hashable**: it has a `__hash__`, and two objects that compare equal
hash the same. In practice that means immutable all the way down.

```python
hash((1, 2, 3))     # fine
hash((1, [2]))      # TypeError: unhashable type: 'list'
```

`(1, [2])` **is** a tuple, and a tuple is immutable at the top level — you
cannot replace its second box. But hashing it means hashing everything inside
it, and the list inside can change. So the tuple is not hashable. "Immutable at
the top" is not the rule; "immutable all the way down" is.

| Hashable | Not hashable |
|---|---|
| `int`, `float`, `bool`, `str`, `bytes`, `None` | `list` |
| `tuple` — only if every element is | `dict` |
| `frozenset` | `set` |
| a `NamedTuple` of hashable fields | a `NamedTuple` holding a list |

**Why a frozenset's hash does not depend on order.** CPython hashes each
member, mixes each one through the same scrambling function, and combines them
with an operation that does not care about order. So
`frozenset({"04", "06"})` and `frozenset({"06", "04"})` produce the same hash
and compare equal — which is exactly the property this challenge needs, and it
is not an accident. A tuple, by contrast, folds its elements in order, so
`(1, 2)` and `(2, 1)` hash differently.

**Cost.** Hashing a frozenset is `O(members)` the first time. Small sets are
cheap; a frozenset of a million elements used as a key is not.

**The alternative keys, and when each is right.**

| Key | When it is the right one |
|---|---|
| `frozenset(cones)` | order and repeats do not matter — this problem |
| `tuple(sorted(cones))` | order does not matter but repeats do, or you need a printable key |
| `",".join(sorted(cones))` | you need a key that is genuinely a string — a filename, a database column |

The middle one is the standard canonical-key move and you will meet it again:
sort the parts, freeze them into a tuple, use it as the key. It costs
`O(m log m)` per key, where the frozenset costs `O(m)` — a real difference when
the sets are large.

**Where this goes next.** Week 2 makes the "group by a canonical key" shape
explicit and names it. Week 6 puts `(row, col)` tuples into a `visited` set
several million times. Both are this rule, and neither will explain it again.

</details>

## Acceptance checklist

- [ ] `python challenge-02-kiln-cone-audit.py` prints five kiln rows, the
      `matching cone sets:` line, two group lines, then `All checks passed.`
- [ ] The three 17-hour kilns are in name order.
- [ ] The grouping key is a `frozenset`.
- [ ] Groups of one are not reported.
- [ ] Cones print as text order — `10, 6` — and you can say why.
- [ ] Nothing compares one kiln against another.
- [ ] You can explain, in one sentence, why a `set` cannot be a dict key.

## Stretch

- **Ask the opposite question: which kiln is doing something no other kiln
  does?**

  ```python
  def unique_cones(firings: list[tuple[str, str, int]]) -> dict[str, list[str]]:
      """Return each kiln's cones that no other kiln has fired."""
      cones = cones_by_kiln(firings)
      out: dict[str, list[str]] = {}
      for kiln, mine in cones.items():
          others: set[str] = set()
          for other, theirs in cones.items():
              if other != kiln:
                  others |= theirs
          only_mine = sorted(mine - others)
          if only_mine:
              out[kiln] = only_mine
      return out
  ```

  ```text
  {}
  ```

  An empty answer, and it is the right one: every cone in this book is fired by
  at least two kilns. An empty result that you can *explain* is a finding.
  Notice also that this is `O(kilns²)` — the all-pairs shape the main solution
  avoided. Sometimes that is genuinely the cheapest thing available; the point
  is to notice when you have written it.

- **Rank the cones themselves by how much kiln time they account for.**

  ```python
  def hours_by_cone(firings: list[tuple[str, str, int]]) -> list[tuple[str, int]]:
      """Rank cones by total hours, most first, ties by cone code A to Z."""
      totals: dict[str, int] = {}
      for _kiln, cone, hours in firings:
          totals[cone] = totals.get(cone, 0) + hours
      return sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
  ```

  ```text
  [('6', 27), ('04', 22), ('06', 16), ('10', 14)]
  ```

  The same function with the first and second fields of the record swapped. Ask
  yourself what else in the log could be a key, and you have the list of
  questions this book can answer without any new code.

- **Prove the order-free hash to yourself.**

  ```python
  first = frozenset(["04", "06"])
  second = frozenset(["06", "04"])
  print(first == second, hash(first) == hash(second))
  print({first: "bisque"}[second])
  ```

  ```text
  True True
  bisque
  ```

  Built in opposite orders, filed under the same hash, found by either. That is
  the property the whole challenge rests on, and it is two lines to check.

When your audit is right, the challenges are done. Move on to
[the homework](../homework/README.md).
