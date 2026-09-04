# Exercise 4 — The Depot's Lost-Property Shelf

> **Topic:** the four ways to handle a key that is not in a dict yet, and which one to reach for
> **Lecture:** [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** more interview solutions turn on "use a dict" than on any other single idea, and almost all of them are one of the two shapes on this page: group things under a key, or count things under a key. Both of them have to answer the same awkward question — what do you do the *first* time you see a key? — and Python gives you four answers. Picking the right one is a readability signal interviewers read.

## The Brief

A bus depot keeps a lost-property shelf. Every time something is handed in, a
clerk writes down two things: the route it was found on, and what it is.

```python
("R12", "umbrella")
```

At the end of the month the depot manager asks four questions:

1. What is on the shelf, grouped by route, in the order it came in?
2. How many things did each route lose?
3. Which route lost the most?
4. Where did the first umbrella turn up?

Every one of those is a **dict**. A dict is a set of labelled pigeonholes. You
say the label, and the pigeonhole comes back straight away — Python does not
walk along the shelf looking for it, and it does not matter whether there are
ten pigeonholes or ten million.

The interesting part is not the lookup. It is what happens the **first** time a
route is mentioned, when the pigeonhole does not exist yet. `shelf["R12"]` on
a route nobody has lost anything on raises `KeyError`, so every grouping and
every count has to answer "and what if this is new?" — and that one question
has four different answers in Python. This exercise uses two of them and asks
you to be able to say why.

The last question has a wrinkle in it, and it is deliberate. Two routes tie for
worst, so the manager's rule is: **on a tie, the earlier route label wins**.
Labels are text, not numbers. `"R12"` comes before `"R7"`, because `1` comes
before `7`. That is not a bug and the expected output depends on it.

## Starter

Create `exercise-04-lost-property-shelf.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""exercise-04-lost-property-shelf.py — the depot's lost-property shelf.

Every item handed in is logged as (route, item). Four questions get asked
about that log, and every one of them is a dict away.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

FINDS: list[tuple[str, str]] = [
    ("R12", "umbrella"),
    ("R7", "water bottle"),
    ("R12", "hat"),
    ("R3", "umbrella"),
    ("R7", "glove"),
    ("R7", "umbrella"),
    ("R12", "scarf"),
    ("R3", "phone"),
]


def items_by_route(finds: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group the log by route, keeping the order things were handed in.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        A dict from route to its items. Routes appear in the order each was
        first seen, and each route's items in the order they arrived.
    """
    # TODO: setdefault, then append. One line in the loop.
    ...


def count_by_route(finds: list[tuple[str, str]]) -> dict[str, int]:
    """Count how many items each route lost."""
    # TODO: d.get(key, 0) + 1
    ...


def busiest_route(finds: list[tuple[str, str]]) -> str | None:
    """Return the route that lost the most, ties broken by route label."""
    # TODO: one pass with min() and a tuple key. None on an empty log.
    ...


def first_route_for(finds: list[tuple[str, str]], item: str) -> str | None:
    """Return the route where this kind of item first turned up."""
    # TODO: build a first-seen dict, then .get
    ...


# ---- Self-check ----
if __name__ == "__main__":
    shelf = items_by_route(FINDS)
    counts = count_by_route(FINDS)
    for route, items in shelf.items():
        print(f"{route:<4} {counts[route]}  {', '.join(items)}")

    print(f"busiest: {busiest_route(FINDS)}")
    print(f"first umbrella: {first_route_for(FINDS, 'umbrella')}")
    print(f"first kite: {first_route_for(FINDS, 'kite')}")

    assert list(shelf) == ["R12", "R7", "R3"]
    assert shelf["R7"] == ["water bottle", "glove", "umbrella"]
    assert counts == {"R12": 3, "R7": 3, "R3": 2}
    assert busiest_route(FINDS) == "R12"  # ties go to the earlier label as text
    assert busiest_route([]) is None
    assert first_route_for(FINDS, "umbrella") == "R12"
    assert first_route_for(FINDS, "kite") is None
    assert len(FINDS) == 8  # the log is untouched
    print("All checks passed.")
```

Four things you need before you start.

**`d.get(key, default)`** looks a key up and hands back `default` instead of
raising when it is missing. It does **not** store anything.

**`d.setdefault(key, default)`** looks a key up, and if it is missing it
*stores* the default first and then hands it back. So
`d.setdefault(route, []).append(item)` appends to the list that is now
definitely in the dict, whether or not it was there a moment ago.

**Dicts keep their order.** Since Python 3.7 a dict remembers the order keys
were first added, and that is a promise of the language, not an accident. It is
why the printed table comes out `R12, R7, R3` — the order the routes first
appeared — with no sorting anywhere.

**`min(items, key=...)`** walks once, holding the best it has seen. With a
tuple key it can answer a two-part rule in that one walk: `(-count, route)`
means *most items first, and on a tie the earlier label*.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/exercises/exercise-04-lost-property-shelf.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `items_by_route` returns routes in first-seen order and each route's items
   in arrival order.
2. `count_by_route` returns one count per route, also in first-seen order.
3. `busiest_route` returns the route with the most items; on a tie, the route
   whose label sorts earlier as text. It returns `None` on an empty log.
4. `first_route_for` returns the route of the **earliest** entry matching that
   item, or `None` when the item has never been handed in.
5. Nothing sorts the whole log. Every function makes one pass.
6. `FINDS` is unchanged afterwards.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Never index a dict you are not sure about.** `shelf[route].append(item)`
  raises `KeyError` the first time each route appears. Use `setdefault` for
  grouping and `get` for counting — and know the difference: `get` reads,
  `setdefault` reads **and stores**.

- **`d.get(route, []).append(item)` is a real bug, not a style choice.** It
  appends to a brand-new list that nobody kept, so the item vanishes with no
  error at all and the group comes out empty. If you take one thing from this
  page, take this: **`get` does not store.**

- **Rely on insertion order rather than sorting.** Sorting the routes would
  cost `O(r log r)` and — worse — would give the manager the wrong answer,
  because the report is meant to read in the order the depot saw them. The
  order is guaranteed, so use it.

- **Find the busiest route with `min` and a tuple key, not by sorting.**
  Sorting puts every route in order so you can read one and throw the rest
  away. `min` walks once. With three routes you cannot feel it; the habit is
  what you are building, and it is the same habit the whole course leans on.

- **Route labels sort as text.** `"R12" < "R7"` is true, because comparison
  goes character by character and `"1"` comes before `"7"`. The two routes that
  tie in this log are exactly those two, so the tie-break rule is visible in
  the output rather than hidden. If the depot wanted numeric order it would
  have to say so, and you would have to pull the digits out — which is a
  different problem and a much more annoying one.

- **At most 5000 items a month, across at most 200 routes.** A depot this size
  loses a few hundred things a month. The bound matters because it says a dict
  is more than enough and nothing here needs to be clever: even the
  worst-written version of this program finishes instantly. What the bound does
  *not* excuse is scanning the whole log once per route — that is `O(routes ×
  items)`, a million operations for an answer that costs five thousand.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-lost-property-shelf.py
R12  3  umbrella, hat, scarf
R7   3  water bottle, glove, umbrella
R3   2  umbrella, phone
busiest: R12
first umbrella: R12
first kite: None
All checks passed.
```

Two lines to check carefully. `busiest` is `R12` even though `R7` also lost
three things: the tie went to the earlier **label**, and `R12` is earlier than
`R7` as text. And `first kite` prints `None` rather than raising — that is
`.get` doing its job on an item nobody has ever lost.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first
   `.items()` call, because `items_by_route` returned `None`.
2. Write `items_by_route`. Try it with plain indexing first —
   `shelf[route].append(item)` — and read the `KeyError` it gives you. That
   error is the whole reason the other three ways exist.
3. Fix it with `setdefault`. Run again and check the printed table is in the
   order `R12, R7, R3` and not alphabetical.
4. Write `count_by_route` with `counts.get(route, 0) + 1`. Note that you could
   also have counted `len(items)` from the first function — decide for yourself
   whether that is cleverness or duplication, and be able to defend it.
5. Write `busiest_route`. Get the empty case first: `if not counts: return
   None`. Then one `min` with a tuple key.
6. Write `first_route_for`. It builds a small dict of first sightings with
   `setdefault` and then looks one item up with `get`.
7. When it passes, change the tie-break to `(-count, )` alone and run it again.
   The answer becomes `R7`, because `min` keeps the first key it met at that
   count and `R7` is not it — actually, work out for yourself which one it
   returns and why before you run it. Getting that prediction right is the
   exercise.

## The Solution

```python
"""exercise-04-lost-property-shelf-solution.py — the depot's lost-property shelf.

Every item handed in is logged as (route, item). Four questions get asked
about that log, and every one of them is a dict away.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

FINDS: list[tuple[str, str]] = [
    ("R12", "umbrella"),
    ("R7", "water bottle"),
    ("R12", "hat"),
    ("R3", "umbrella"),
    ("R7", "glove"),
    ("R7", "umbrella"),
    ("R12", "scarf"),
    ("R3", "phone"),
]


def items_by_route(finds: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group the log by route, keeping the order things were handed in.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        A dict from route to its items. Routes appear in the order each was
        first seen, and each route's items in the order they arrived.
    """
    shelf: dict[str, list[str]] = {}
    for route, item in finds:
        shelf.setdefault(route, []).append(item)
    return shelf


def count_by_route(finds: list[tuple[str, str]]) -> dict[str, int]:
    """Count how many items each route lost.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        A dict from route to its item count, in first-seen order.
    """
    counts: dict[str, int] = {}
    for route, _item in finds:
        counts[route] = counts.get(route, 0) + 1
    return counts


def busiest_route(finds: list[tuple[str, str]]) -> str | None:
    """Return the route that lost the most, ties broken by route label.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        The winning route label, or None when the log is empty.
    """
    counts = count_by_route(finds)
    if not counts:
        return None
    return min(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0]


def first_route_for(finds: list[tuple[str, str]], item: str) -> str | None:
    """Return the route where this kind of item first turned up.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.
        item: The item description to look for.

    Returns:
        The route label of the earliest matching entry, or None if this kind
        of item has never been handed in.
    """
    first: dict[str, str] = {}
    for route, found in finds:
        first.setdefault(found, route)
    return first.get(item)


# ---- Self-check ----
if __name__ == "__main__":
    shelf = items_by_route(FINDS)
    counts = count_by_route(FINDS)
    for route, items in shelf.items():
        print(f"{route:<4} {counts[route]}  {', '.join(items)}")

    print(f"busiest: {busiest_route(FINDS)}")
    print(f"first umbrella: {first_route_for(FINDS, 'umbrella')}")
    print(f"first kite: {first_route_for(FINDS, 'kite')}")

    assert list(shelf) == ["R12", "R7", "R3"]
    assert shelf["R7"] == ["water bottle", "glove", "umbrella"]
    assert counts == {"R12": 3, "R7": 3, "R3": 2}
    assert busiest_route(FINDS) == "R12"  # ties go to the earlier label as text
    assert busiest_route([]) is None
    assert first_route_for(FINDS, "umbrella") == "R12"
    assert first_route_for(FINDS, "kite") is None
    assert len(FINDS) == 8  # the log is untouched
    print("All checks passed.")
```

**`setdefault` is the grouping idiom, and it is one line.**

```python
shelf.setdefault(route, []).append(item)
```

Read it as: *get me the list for this route, making an empty one first if there
isn't one, and append to it.* Because `setdefault` **stores** the empty list
before handing it back, the thing you append to is the one in the dict. Swap in
`get` and the append lands on a list that is thrown away the instant the line
ends, and your groups come out empty with no error to explain why.

There is a fourth way, `collections.defaultdict(list)`, which builds the empty
list automatically on any miss. It is shorter still and Homework 5 uses it. It
has one sharp edge worth knowing now: merely *reading* a missing key inserts
it, so `if grouped[route]:` on a `defaultdict` quietly grows the dict.
`setdefault` never surprises anybody, which is why it is the one on this page.

**Counting uses `get`, because counting only reads.**

```python
counts[route] = counts.get(route, 0) + 1
```

The old count comes back — or `0` for a route nobody has seen — and the new one
is written. `get` is right here precisely because the line does its own
storing.

**Order is a guarantee, so nothing sorts.** Since Python 3.7 a dict remembers
the order its keys were first inserted, as a rule of the language rather than a
quirk of one implementation. The report prints `R12, R7, R3` because that is
the order the shelf filled up, and getting it needed no `OrderedDict`, no key
list, and no sort. Say the version number out loud in an interview — "insertion
order has been guaranteed since 3.7" — because plenty of people still hedge
about it.

**One `min`, one tuple key, one walk.**

```python
min(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0]
```

`counts.items()` gives `(route, count)` pairs. The key turns each pair into
`(-count, route)`, and Python compares those box by box, stopping at the first
difference. Negating the count makes "more is better" line up with "smaller
wins", so a single `min` answers a two-part rule. The trailing `[0]` pulls the
route back out of the winning pair.

Why `min` of a negated count rather than `max`? Because `max` would need the
tie-break negated too, and you cannot negate a string. Get used to the shape
`min(..., key=lambda x: (-thing_i_want_most_of, thing_i_want_first))` — it
turns up constantly, and it is the same shape Exercise 3 of Week 2 will hand
you again.

**`first_route_for` builds a small dict and then asks it once.**
`first.setdefault(found, route)` writes only on the first sighting of each item
description, because `setdefault` leaves an existing value alone. So the dict
ends up holding first sightings and nothing else, and `.get(item)` answers with
`None` for anything never handed in. Note what this avoids: a loop with a
`break`, which is four lines and has an "and what if we never found it" branch
that people forget.

## Run it

Copy the worked answer on this page into `exercise-04-lost-property-shelf.py` and run it:

```bash
python exercise-04-lost-property-shelf.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-04-lost-property-shelf.py`.

## Common bugs to catch

- **`KeyError: 'R12'`.** You indexed a pigeonhole that does not exist yet:

  ```text
  Traceback (most recent call last):
      shelf[route].append(item)
      ~~~~~^^^^^^^
  KeyError: 'R12'
  ```

  Note *which* route it names: the very first one, on the very first item. This
  is not a rare edge case, it is the normal case, and it is why `setdefault`,
  `get` and `defaultdict` all exist.

- **Every group comes out empty, with no error.** You wrote
  `shelf.get(route, []).append(item)`:

  ```text
  R12  3
  R7   3
  R3   2
  ```

  Wait — those counts are right and the items are gone. `get` handed you a
  fresh empty list, you appended to it, and the line ended, and the list went
  with it. Nothing was ever stored. **This is the single most expensive
  one-word mistake in this lecture**, because it fails silently and the counts
  keep looking correct.

- **`AttributeError: 'NoneType' object has no attribute 'append'`.** The
  sibling version of the same mistake:

  ```text
  Traceback (most recent call last):
      shelf.get(route).append(item)
      ^^^^^^^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'append'
  ```

  `get` with no default returns `None` on a miss. At least this one stops you.

- **`busiest` prints `R7`.** Your key is `-count` alone, with no tie-break, so
  the winner is whichever tied route `min` happened to meet first — and it
  meets them in dict order, which is first-seen order, which is `R12`… unless
  you used `max`, which keeps the **first** maximum too but is comparing
  un-negated counts, so it lands somewhere else. The lesson is not the
  mechanics. It is that **a rule with a tie in it needs the tie written down**,
  or the answer depends on things the rule never mentioned.

- **`TypeError: bad operand type for unary -: 'str'`.** You negated the label
  as well as the count:

  ```text
  Traceback (most recent call last):
      min(counts.items(), key=lambda pair: (-pair[1], -pair[0]))
                                                      ^^^^^^^^
  TypeError: bad operand type for unary -: 'str'
  ```

  Only numbers negate. You do not want the label reversed anyway — the rule
  asks for the earlier label, which is what an un-negated string already gives
  you.

- **`ValueError: min() iterable argument is empty`.** You called `min` on an
  empty log:

  ```text
  ValueError: min() iterable argument is empty
  ```

  `min` and `max` both raise on nothing at all, because there is no answer to
  give. Guard first, or pass `default=None`. Anything that reads a file or a
  form will hand you an empty list eventually.

- **The table prints in alphabetical order.** You sorted the routes on the way
  out. It is not wrong-looking, it is just not what was asked for — and it
  threw away information the dict was keeping for you for free.

## Under the hood

<details>
<summary>Under the hood — why a lookup is O(1), and what the worst case really is</summary>

**Where a key goes, and how it is found again.**

A dict is an array of slots. To store `"R12"`:

1. Compute `hash("R12")` — a number derived from the characters.
2. Take some low bits of it as a slot number.
3. If that slot is taken by a different key — a **collision** — jump to another
   slot by a fixed rule and try again.

Looking up repeats the same steps, so it finds the key in the same small number
of hops. CPython keeps the table under about two-thirds full, growing it when
it fills, so the expected number of hops is a small constant no matter how many
keys there are. That is what **`O(1)` average** means, and it is why depot size
does not appear in the cost.

**The worst case is `O(n)` and you should say so.** If every key landed in the
same slot, every lookup would walk a chain as long as the dict. That needs
either a terrible hash function or an attacker choosing your keys on purpose.
The interview-grade sentence is:

> Dict lookup is O(1) average. Worst case is O(n) if every key collides, which
> takes adversarial input — not a concern here.

One extra clause, and it is the difference between reciting a fact and
understanding the structure.

**What may be a key.** A key must be **hashable**, which means immutable all
the way down: numbers, strings, tuples of hashable things, `frozenset`. A list
may not be a key, because its hash would change the moment somebody appended
to it and the dict would lose the entry it had already filed. Exercise 5 and
Challenge 2 both lean on this.

**Views are lazy.** `shelf.items()` does not build a list of pairs. It returns
a small view object in constant time, and iterating it walks the dict. The view
also stays live — change the dict and the view sees it — which is why changing
a dict while looping over it raises `RuntimeError: dictionary changed size
during iteration` rather than quietly skipping entries.

**The memory cost is real.** A dict of `n` entries takes several times the
memory of a list of `n` items: the slot array has spare room in it by design,
and each entry carries its hash. Worth mentioning only if someone asks about
memory pressure, but it is the reason "just use a dict" is not free.

</details>

## Acceptance checklist

- [ ] `python exercise-04-lost-property-shelf.py` prints three route rows,
      three answer lines, then `All checks passed.`
- [ ] The table is in first-seen order, not alphabetical.
- [ ] `busiest` prints `R12` and you can say why it is not `R7`.
- [ ] `first kite` prints `None` and raises nothing.
- [ ] Grouping uses `setdefault`; counting uses `get`.
- [ ] No function sorts the whole log.
- [ ] You can state the average and worst case of a dict lookup in one
      sentence each.

## Stretch

- **Do the counting with `Counter` and see how much of your code disappears.**

  ```python
  from collections import Counter

  def count_by_route_counter(finds: list[tuple[str, str]]) -> Counter[str]:
      """Count how many items each route lost."""
      return Counter(route for route, _item in finds)
  ```

  ```text
  Counter({'R12': 3, 'R7': 3, 'R3': 2})
  counts['R99'] -> 0
  ```

  A `Counter` is a dict that answers `0` for anything it has never seen instead
  of raising, which removes the missing-key question entirely for counting
  problems. Note the printed order: most common first, because that is how a
  `Counter` chooses to display itself — but the dict underneath is still in
  insertion order, and `list(counts)` proves it.

- **Ask which items turn up on more than one route.**

  ```python
  def spread_across_routes(finds: list[tuple[str, str]]) -> dict[str, list[str]]:
      """Return each item description and the routes it was found on."""
      where: dict[str, list[str]] = {}
      for route, item in finds:
          seen = where.setdefault(item, [])
          if route not in seen:
              seen.append(route)
      return {item: routes for item, routes in where.items() if len(routes) > 1}
  ```

  ```text
  {'umbrella': ['R12', 'R3', 'R7']}
  ```

  Same idiom, the key and the value swapped over. Deciding *what the key should
  be* is most of the work in a dict problem, and swapping it is often the whole
  solution to the next question.

- **Watch a dict refuse to be changed underneath a loop.**

  ```python
  counts = {"R12": 3, "R7": 3}
  for route in counts:
      counts[route + "x"] = 0
  ```

  ```text
  RuntimeError: dictionary changed size during iteration
  ```

  Python could have let this quietly skip or repeat entries, and chose to stop
  you instead. When you need to add while walking, collect the additions in a
  list and apply them after the loop.

When your shelf report is right, move on to
[Exercise 5 — Two Nights on the Coastal Net](./exercise-05-radio-check-rosters.md).
