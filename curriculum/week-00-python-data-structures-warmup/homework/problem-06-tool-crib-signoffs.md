# Problem 6 — The Tool Crib's Sign-Offs

> **Topic:** set algebra — union, intersection, difference and subset — and what each one costs
> **Lecture:** [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** when the data is "who may do what", every question anybody asks is set algebra, and writing it as loops is how a four-word answer becomes fifteen lines. This page is also where the cost table stops being uniform: `&` is cheaper than `|`, on purpose, and the reason is usable.

## The Brief

A makerspace keeps a tool crib. Every member has a set of machines they have
been signed off on:

```python
{"lathe", "bandsaw", "drill press"}
```

Four questions get asked at the crib, over and over.

**What have we got?** Every tool somebody is signed off on. That is a
**union** — `a | b` — everything in either.

**What can everybody run?** The tools every single member holds. That is an
**intersection** — `a & b` — the things in both.

**What rests on one person?** The tools exactly one member can run. Those are
the jobs that stop when that member is on holiday. Neither union nor
intersection answers this; it is a counting question, and a `Counter` does it.

**Can this member take this job?** The job calls for a set of tools. If the
member's set contains all of them, they can take it. That is a **subset** —
`job <= tools` — and when they cannot, the shortfall is a **difference**:
`job - tools`, the tools the job needs that the member does not have.

The one asymmetry worth carrying around: `s & t` costs `O(min(len(s),
len(t)))`, because Python walks the smaller set and looks each member up in the
larger one. `s | t` has to touch everything in both, so it is
`O(len(s) + len(t))`. Intersecting a two-element set with a million-element set
is two lookups, not a million.

## Starter

Create `problem-06-tool-crib-signoffs.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""problem-06-tool-crib-signoffs.py — who may run which machine.

Every question the crib gets asked is set algebra: what have we got, what
can everybody run, what rests on one person, and can this member take this
job.

Sorting happens once, at the very end, only because a printed line has to
be in some order.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import Counter

SIGNOFFS: dict[str, set[str]] = {
    "ama": {"lathe", "bandsaw", "drill press"},
    "bo": {"bandsaw", "drill press", "laser"},
    "cai": {"bandsaw", "lathe", "welder", "drill press"},
}

JOB: set[str] = {"bandsaw", "welder"}


def all_tools(signoffs: dict[str, set[str]]) -> set[str]:
    """Return every tool somebody is signed off on."""
    # TODO: union them together. Start from an empty set.
    ...


def everyone_can_run(signoffs: dict[str, set[str]]) -> set[str]:
    """Return the tools every member is signed off on.

    Returns:
        The intersection of every member's set, or an empty set when the
        crib has no members at all.
    """
    # TODO: set.intersection(*sets) — and guard the empty crib first
    ...


def single_point_of_failure(signoffs: dict[str, set[str]]) -> list[str]:
    """Return the tools exactly one member can run, sorted A to Z."""
    # TODO: a Counter over every member's tools, then keep the ones at 1
    ...


def missing_for(job: set[str], tools: set[str]) -> list[str]:
    """Return what a member still needs before taking a job, sorted."""
    # TODO: one difference, then sorted()
    ...


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
```

Three things you need before you start.

**`|=` on a set is `add` for many at once.** `covered |= tools` puts everything
from `tools` into `covered`. It changes `covered` in place — which is fine when
`covered` is a set you built a line earlier, and a bug when it is a set
somebody handed you.

**`set.intersection(*sets)`** intersects a whole list of sets at once. The `*`
spreads the list out into separate arguments. On an empty list it raises,
because "the intersection of no sets at all" has no sensible answer — hence the
guard.

**`sorted(a_set)`** returns a list. A set has no order, so any printed line has
to choose one, and the choosing belongs at the printing end and nowhere else.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-06-tool-crib-signoffs.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `all_tools` returns the union of every member's set, and `set()` for an
   empty crib.
2. `everyone_can_run` returns the intersection of every member's set, and
   `set()` for an empty crib.
3. `single_point_of_failure` returns the tools held by exactly one member,
   sorted A to Z.
4. `missing_for(job, tools)` returns the job's tools that the member lacks,
   sorted A to Z, and `[]` when they lack none.
5. No member's set is changed by any function.
6. Sorting happens only where a printed line or a stated order requires it.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Never `|=` a set you were given.** `covered |= tools` inside the loop is
  correct only because `covered` is the local set built one line above. Written
  the other way round — `tools |= covered` — it would grow a member's sign-off
  list, and the crib's records would gain tools nobody was ever signed off on.
  The last assert is there for exactly that.

- **Guard the empty crib before `set.intersection(*sets)`.** With no arguments
  it raises `TypeError: unbound method set.intersection() needs an argument`.
  "Everything that all zero members can run" is a genuine question with no
  answer — mathematically it is every tool that exists, which is not a set this
  program has — so returning `set()` is a decision, and one worth being able to
  defend.

- **Count with a `Counter`, not with pairwise comparisons.** "Exactly one
  member" is a counting question. Comparing every member against every other is
  `O(members²)` and answers a different question badly. One pass over the
  members, updating a tally, is `O(total sign-offs)`.

- **Use `<=` for "can they take it", not a loop.** `job <= tools` is the subset
  test, it reads like the sentence, and it stops at the first missing tool. A
  hand-written `all(tool in tools for tool in job)` does the same thing and is
  longer; a `for` loop with a flag is longer still and has a way of forgetting
  the `break`.

- **Sort at the printing end only.** The sets are the data and they have no
  order. Storing them sorted "so they print nicely" would turn them into lists,
  and then two members with the same tools in a different order would stop
  being equal — which is the property Challenge 2 depends on.

- **At most 300 members and 80 tools.** A large makerspace has a couple of
  hundred members and the crib has a wall of machines. The tool bound is the
  useful one: every set is small, so every union and intersection is cheap
  whatever the membership does, and `single_point_of_failure` is a tally of at
  most 80 things.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-06-tool-crib-signoffs.py
all tools : bandsaw, drill press, laser, lathe, welder
everyone  : bandsaw, drill press
only one  : laser, welder
job needs : bandsaw, welder
  ama  missing welder
  bo   missing welder
  cai  can take it
All checks passed.
```

Read the last three lines. `ama` and `bo` are both missing the welder — `bo`
has the laser, `ama` has the lathe, and neither of those is what the job needs.
Only `cai` holds both the bandsaw and the welder. And `only one` lists `laser`
and `welder`: if `bo` and `cai` are away on the same week, two capabilities
leave with them.

## Steps

1. Create the file, paste the starter, and run it. `", ".join(None)` fails on
   the first line.
2. Write `all_tools`. Start with `covered: set[str] = set()` and `|=` each
   member's tools in.
3. Write `everyone_can_run`. Guard the empty crib, then
   `set.intersection(*sets)`.
4. Try it without the guard on `{}` and read the `TypeError`. That message is
   worth seeing once.
5. Write `single_point_of_failure` with a `Counter` and `tally.update(tools)`.
6. Write `missing_for` — one difference and a `sorted`.
7. When it passes, add yourself to `SIGNOFFS` with one tool nobody else has,
   and predict what changes in all four answers before you run it.

## The Solution

```python
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
```

**`all_tools` builds a new set and grows only that.**

```python
covered: set[str] = set()
for tools in signoffs.values():
    covered |= tools
```

`covered` was created one line earlier, so changing it in place is safe and
cheap — it avoids building an intermediate set on every pass, which
`covered = covered | tools` would do. The rule is not "never mutate"; it is
**only mutate what you made**.

**`set.intersection(*sets)` does the whole intersection in one call.** Calling
it on the class rather than on an instance — `set.intersection(a, b, c)` rather
than `a.intersection(b, c)` — makes it read as an operation over a list rather
than as something the first set does to the others. Underneath, CPython starts
from the smallest set, which is why intersecting many sets is bounded by the
smallest of them and not by the biggest.

The guard is not defensive noise. `set.intersection()` with nothing to
intersect raises, and it should — the honest mathematical answer is "every tool
that could ever exist", which no program has. Returning `set()` is a choice,
and writing the guard is where you make it on purpose.

**"Exactly one" is a tally, not a comparison.**

```python
tally: Counter[str] = Counter()
for tools in signoffs.values():
    tally.update(tools)
return sorted(tool for tool, holders in tally.items() if holders == 1)
```

`tally.update(tools)` adds one for every tool in the set. One pass over the
members, `O(total sign-offs)`. The shape people reach for instead — for each
member, check every *other* member — is `O(members²)` and asks a harder
question than the one that was posed.

**`missing_for` is a difference, and the subset test is the same question
answered `True`/`False`.**

```python
return sorted(job - tools)
```

`job - tools` is "what the job needs and the member does not have". When it is
empty, the member can take the job — which is exactly what `job <= tools` says
in one operator. Both are in the self-check on purpose: the difference tells
you *what is missing*, the subset test tells you *whether anything is*, and a
program usually wants one of them and prints the other.

**The costs are not all the same, and the differences are usable.**

| Operation | Cost | Why |
|---|---|---|
| `s \| t` | `O(len(s) + len(t))` | every member of both has to be touched |
| `s & t` | `O(min(len(s), len(t)))` | walk the smaller, look up in the larger |
| `s - t` | `O(len(s))` | walk `s` only |
| `s <= t` | `O(len(s))` | walk `s`, look up in `t`, stop at the first miss |

The `&` asymmetry is the one to remember. If you only carry one fact about sets
past this week, carry that intersecting a small set with a huge one is cheap.

## Run it

Copy the worked answer on this page into `problem-06-tool-crib-signoffs.py` and run it:

```bash
python problem-06-tool-crib-signoffs.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-06-tool-crib-signoffs.py`.

## Common bugs to catch

- **`TypeError: unbound method set.intersection() needs an argument`.** The
  empty-crib guard is missing:

  ```text
  TypeError: unbound method set.intersection() needs an argument
  ```

  An empty crib is a real state — it is what the file looks like on day one.

- **`SIGNOFFS["ama"]` grew a `laser`.** You wrote the union the wrong way
  round, `tools |= covered`, and modified a member's own set. There is no
  error, the union comes out right, and every member's record is now the union
  of everyone before them. The last assert exists for this and nothing else.

- **`TypeError: unsupported operand type(s) for -: 'set' and 'list'`.** You
  passed a list where a set was expected:

  ```text
  TypeError: unsupported operand type(s) for -: 'set' and 'list'
  ```

  Set algebra works between sets. The operator form is strict about this on
  purpose; the method form, `job.difference(["bandsaw"])`, accepts any iterable
  — which is convenient and is why the two spellings are not interchangeable.

- **`TypeError: unhashable type: 'set'`.** You tried to put sets into a set —
  to group members by what they can run, say:

  ```text
  TypeError: unhashable type: 'set'
  ```

  A set member must be immutable all the way down. `frozenset(tools)` is what
  goes in. Challenge 2 is built on this.

- **`AttributeError: 'set' object has no attribute 'append'`.** Sets have
  `add`:

  ```text
  AttributeError: 'set' object has no attribute 'append'
  ```

  And if you wanted `append`, ask yourself whether you actually wanted a list —
  because if the order matters, a set was the wrong container from the start.

- **`only one` lists every tool.** You counted tools per member instead of
  members per tool — `tally.update(signoffs.keys())` or a Counter over the
  wrong loop variable. Say the question out loud: *how many members hold this
  tool?* The tool is the key.

- **The printed lines come out in a different order each run.** You printed a
  set directly instead of `sorted(...)`. Set iteration order depends on hashes,
  and CPython salts string hashing at start-up, so two runs of the same program
  can genuinely disagree. Anything a person reads gets sorted.

## Under the hood

<details>
<summary>Under the hood — why intersection is O(min), and what frozenset is for</summary>

**A set is a dict with the values thrown away.** Same array of slots, same
hashing, same growth rule, same guarantees: `O(1)` average for `add`, `remove`
and `in`, `O(n)` worst case if every member collides.

**Why `&` is `O(min)`.** To intersect, CPython iterates one set and tests each
member against the other. Iterating costs one step per member; testing costs
`O(1)` average. So it iterates the **smaller** one and tests against the
larger — and it checks the sizes first, which is why `small & huge` and
`huge & small` cost the same. You do not have to remember to put the small set
on the left.

Union cannot do that. Every member of both sets ends up in the answer, so both
have to be walked. Difference walks only the left-hand side, and subset walks
the left-hand side and stops early on the first miss — which makes
`job <= tools` cheaper than building `job - tools` when all you want is the
yes-or-no.

**`frozenset` is the immutable one.** No `add`, no `remove`, so its hash cannot
change under it, so it may be a dict key or a member of another set:

```python
crews = set()
crews.add(frozenset({"lathe", "bandsaw"}))     # fine
crews.add({"lathe", "bandsaw"})                # TypeError: unhashable type: 'set'
```

Two frozensets with the same members are equal and hash the same however they
were built, because the hash mixes the members with an operation that does not
care about order. That property is what makes "group everyone with identical
sign-offs" a one-pass job instead of an all-pairs comparison.

**Set operations have method forms, and they are not identical to the
operators.**

| Operator | Method | Difference |
|---|---|---|
| `a \| b` | `a.union(b)` | the method takes any iterable, and any number of them |
| `a & b` | `a.intersection(b)` | same |
| `a - b` | `a.difference(b)` | same |
| `a <= b` | `a.issubset(b)` | same |

The operators demand sets on both sides. The methods will take a list, a tuple,
a generator. That is convenient and it is a real difference in strictness —
`{1, 2} - [1]` raises, `{1, 2}.difference([1])` does not.

</details>

## Acceptance checklist

- [ ] `python problem-06-tool-crib-signoffs.py` prints four summary lines,
      three member lines, then `All checks passed.`
- [ ] `everyone_can_run({})` returns `set()` rather than raising.
- [ ] No member's set is changed by any function.
- [ ] "Exactly one" is answered with a tally, not by comparing members.
- [ ] Sorting happens only at the printing end.
- [ ] You can say why `&` is `O(min)` and `|` is not.
- [ ] You can say why a `set` cannot go inside another set.

## Stretch

- **Find the members whose sign-offs are identical.**

  ```python
  def matching_members(signoffs: dict[str, set[str]]) -> list[list[str]]:
      """Return groups of two or more members with the exact same sign-offs."""
      groups: dict[frozenset[str], list[str]] = {}
      for member, tools in signoffs.items():
          groups.setdefault(frozenset(tools), []).append(member)
      return [sorted(names) for names in groups.values() if len(names) > 1]
  ```

  ```text
  []
  ```

  Nobody matches in this crib, and an empty answer you can explain is a
  finding. The mechanism is Challenge 2's: freeze the set, use it as the key,
  and never compare one member against another.

- **Ask who could take the job with one more sign-off.**

  ```python
  def nearly_qualified(job: set[str], signoffs: dict[str, set[str]]) -> list[str]:
      """Return members who are exactly one tool short of the job."""
      return sorted(name for name, tools in signoffs.items() if len(job - tools) == 1)
  ```

  ```text
  ['ama', 'bo']
  ```

  The same difference, asked about its size rather than its contents. This is
  the shape of most "who should we train next" questions, and it is one line
  because the data was kept as sets.

- **Watch `|=` change the wrong thing.**

  ```python
  before = set(SIGNOFFS["ama"])
  covered = SIGNOFFS["ama"]        # NOT a copy — the same set
  covered |= {"laser"}
  print(before == SIGNOFFS["ama"], sorted(SIGNOFFS["ama"]))
  ```

  ```text
  False ['bandsaw', 'drill press', 'lathe', 'laser']
  ```

  `covered = SIGNOFFS["ama"]` does not copy anything; it gives the same set a
  second name. `|=` then grows the crib's record. This is Exercise 3's aliasing
  bug in set clothing, and the fix is the same: `set(SIGNOFFS["ama"])` when you
  need your own.

That is the homework. Next: [the mini-project](../mini-project/README.md).
