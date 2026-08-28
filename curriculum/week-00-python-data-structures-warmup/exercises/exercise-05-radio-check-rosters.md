# Exercise 5 — Two Nights on the Coastal Net

> **Topic:** the swap that turns `O(n × m)` into `O(n + m)` — build a set once, then test membership against it
> **Lecture:** [03 — Dicts, Sets and the Hash Table](../lecture-notes/03-dicts-sets-and-the-hash-table.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** this is the single most reusable optimisation in interview coding, and it is one line. `x in some_list` walks the whole list. `x in some_set` does not. Swapping one for the other changes the shape of a solution more often than any clever algorithm will, and the part candidates forget is that the swap costs memory — saying that trade out loud is what the interviewer is listening for.

## The Brief

A coastal radio net meets after dark. The controller reads out a call and
writes down every station that answers, in the order they answer. Some
stations answer twice, because the first answer was stepped on by somebody
else transmitting at the same moment.

Two nights, two sheets:

```python
FIRST_NIGHT  = ["KC4ORT", "W2QRP", "N9TIDE", "W2QRP", "VE3GULL"]
SECOND_NIGHT = ["N9TIDE", "K5MOOR", "KC4ORT", "K5MOOR", "W7FOG"]
```

The controller wants three lists:

- who was **on both nights**,
- who is **new tonight**,
- who **went silent** — heard last night, not heard tonight.

Every one of those asks the same question over and over: *is this call sign on
the other sheet?* And that is where the cost is.

Asking a **list** that question means walking it from the front, comparing as
you go, until you find the sign or run out of sheet. Ask it once per station on
the other sheet and you have walked one list once per item of the other:
`n × m` comparisons.

A **set** answers it differently. A set is a dict with the values thrown away —
same labelled pigeonholes. It computes the sign's hash, goes straight to the
pigeonhole, and looks. That is one hop, however big the set is. Building the
set costs one walk, and then every question after that is free.

That is the trade, and you must be able to say the whole of it:

> Membership on a list is `O(n)`, so the nested version is `O(n × m)`. Building
> a set costs `O(m)` time and `O(m)` **space** up front, after which each test
> is `O(1)` average — so the whole thing becomes `O(n + m)` time at the cost of
> `O(m)` space.

The space half is the half people leave out.

One more thing this exercise insists on. Sets have no order and no duplicates —
that is the point of them — but the controller wants the answers **in the order
the stations answered**, each station once. So the set does the *asking* and a
list does the *remembering*. Reaching for `set(first) & set(second)` gives you
the right stations in an order you did not choose.

## Starter

Create `exercise-05-radio-check-rosters.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""exercise-05-radio-check-rosters.py — two nights on the coastal net.

Comparing last night's sheet with tonight's is three questions, and every
one of them is a membership test.

Sets answer the membership question. Lists keep the order. This drill uses
both, on purpose.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

FIRST_NIGHT: list[str] = ["KC4ORT", "W2QRP", "N9TIDE", "W2QRP", "VE3GULL"]
SECOND_NIGHT: list[str] = ["N9TIDE", "K5MOOR", "KC4ORT", "K5MOOR", "W7FOG"]


def both_nights(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard on both nights, in first-night order.

    Args:
        first: Last night's sheet, in the order stations answered.
        second: Tonight's sheet, in the order stations answered.

    Returns:
        Each repeat station once, ordered by when it answered last night.
    """
    # TODO: build ONE set from `second`, then walk `first` in order
    ...


def newcomers(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard tonight and not last night."""
    # TODO: same shape, other direction
    ...


def went_silent(first: list[str], second: list[str]) -> list[str]:
    """Return the stations heard last night and not tonight."""
    # TODO: same shape again
    ...


def net_size(sheet: list[str]) -> int:
    """Return how many different stations a sheet holds."""
    # TODO: one expression
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"both nights : {', '.join(both_nights(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"new tonight : {', '.join(newcomers(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"went silent : {', '.join(went_silent(FIRST_NIGHT, SECOND_NIGHT))}")
    print(f"distinct    : {net_size(FIRST_NIGHT)} last night, {net_size(SECOND_NIGHT)} tonight")

    assert both_nights(FIRST_NIGHT, SECOND_NIGHT) == ["KC4ORT", "N9TIDE"]
    assert newcomers(FIRST_NIGHT, SECOND_NIGHT) == ["K5MOOR", "W7FOG"]
    assert went_silent(FIRST_NIGHT, SECOND_NIGHT) == ["W2QRP", "VE3GULL"]
    assert net_size(FIRST_NIGHT) == 4
    assert net_size(SECOND_NIGHT) == 4
    assert both_nights([], SECOND_NIGHT) == []
    assert newcomers(FIRST_NIGHT, []) == []
    assert went_silent(FIRST_NIGHT, []) == ["KC4ORT", "W2QRP", "N9TIDE", "VE3GULL"]
    assert FIRST_NIGHT[1] == "W2QRP"  # both sheets are untouched
    print("All checks passed.")
```

Three things you need before you start.

**`set(sheet)`** walks the sheet once and hands you a set of its distinct
values. That walk is the `O(m)` you pay once.

**`sign in some_set`** is one hop. `sign in some_list` is a walk. They are
spelled identically, which is exactly why this mistake survives code review.

**A second set, for the answer.** Each output list must hold each station once.
Keeping a `seen` set alongside the output list is how you check "have I already
written this one down?" in one hop instead of scanning the answer so far.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/exercises/exercise-05-radio-check-rosters.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `both_nights` returns the stations on both sheets, each once, in
   **first-night** order.
2. `newcomers` returns the stations on the second sheet only, each once, in
   **second-night** order.
3. `went_silent` returns the stations on the first sheet only, each once, in
   **first-night** order.
4. `net_size` returns how many distinct stations a sheet holds.
5. Each function builds **one** set from the other sheet, before its loop, not
   inside it.
6. An empty sheet on either side gives a sensible answer and raises nothing.
7. Both input lists are unchanged afterwards.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Build the set once, outside the loop.** `if sign in set(second)` inside the
  loop rebuilds the whole set on every pass — that is `O(n × m)` again, with a
  worse constant than the list version it was meant to replace. This is the
  most common way the optimisation gets undone by the person applying it.

- **Do not answer with `set(first) & set(second)`.** It gives the right
  stations and the wrong order, because a set has no order to give. The
  controller reads these lists on the air in the order stations answered.
  Whenever a problem says "preserving the order they appeared", a set can be
  the *index* but never the *answer*.

- **De-duplicate with a `seen` set, not with `if sign not in kept`.** Checking
  the output list is a walk of the answer so far, which turns an `O(n)` pass
  into `O(n²)` — the very thing this page is about, hiding one line lower down.

- **Call signs are ASCII, upper-case, at most 8 characters.** That is the
  international format, and it matters here for one reason: comparisons are
  exact. `"kc4ort"` and `"KC4ORT"` are different stations to a set, because
  hashing works on the characters. If the sheets were typed by two different
  people you would normalise first — and that normalising pass is `O(n)`, which
  is free next to what it saves.

- **At most 400 stations on a sheet.** A busy net has a few dozen; 400 is a
  contest weekend. At that size the list version is genuinely fine — 160,000
  comparisons is nothing. The bound is honest, and the point of the exercise is
  that you are learning the shape here so that it is automatic in Week 3, where
  the same line runs inside a window over a million-element input and the
  difference is a solution that finishes and one that does not.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-radio-check-rosters.py
@@STDOUT:exercise-05-radio-check-rosters-solution.py@@
```

Both sheets have five entries and four distinct stations, because both have one
station that answered twice. `W2QRP` appears twice on the first sheet and once
in `went silent` — the duplicate does not double the answer. And `both nights`
reads `KC4ORT, N9TIDE`, which is first-night order; tonight `N9TIDE` answered
first, so an answer that reads `N9TIDE, KC4ORT` was built from the wrong sheet.

## Steps

1. Create the file, paste the starter, and run it. The first `", ".join(None)`
   fails.
2. Write `both_nights` the slow way first, on purpose: `if sign in second`,
   with `second` still a list. It passes. Every assert on this page passes with
   the slow version, which is the honest situation you are usually in.
3. Now make it fast: `tonight = set(second)` before the loop, and test against
   that. Nothing about the answer changes. Say out loud what did change.
4. Add the de-duplication with a `seen` set. Check `W2QRP` appears once in
   `went silent`, not twice.
5. Write `newcomers` and `went_silent` — the same shape, with the sheets and
   the `not` moved around. If all three end up looking almost identical, that
   is correct, and the stretch asks you what to do about it.
6. Write `net_size`.
7. When it passes, work out the complexity of each function in time **and**
   space, and write the sentence from The Brief in your own words for
   `both_nights`. That sentence is the deliverable of this page as much as the
   code is.

## The Solution

```python
@@CODE:exercise-05-radio-check-rosters-solution.py@@
```

**One set, built before the loop, is the whole optimisation.**

```python
tonight = set(second)
```

One line, one walk of the second sheet, and every question after it is a single
hop. Move that line inside the loop and you rebuild the set `n` times. Delete
it and test against the list instead and every question becomes a walk. The
answer is identical in all three versions, which is precisely why this has to
be reasoned about rather than tested for.

**The second set is doing a different job, and it is worth naming.** `seen`
answers "have I already written this station down?" The obvious alternative,
`if sign not in kept`, asks the same question of a **list** — and that list
grows as you go, so the check gets slower the further you get. Two sets, two
jobs: one is the other sheet, one is the answer so far.

**The list is what remembers the order.** `kept.append(sign)` inside a loop
over `first` builds the answer in first-night order, because that is the order
the loop visits. Sets cannot do this for you. The pattern — **walk the thing
whose order you want, ask the set about it** — is worth memorising as a
sentence, because it decides which of your two inputs goes in the loop.

**`went_silent(FIRST_NIGHT, [])` returns four names, not five.** `W2QRP`
answered twice last night and appears once in the answer, because `seen` caught
the second. The empty-second-sheet case is in the asserts for a reason: it is
the input most likely to be produced by a night nobody was on the air, and a
version built around `set(first) - set(second)` gets the *stations* right and
the *order* arbitrary.

**`net_size` is `len(set(sheet))`, and it is `O(n)` time and `O(n)` space.**
Not free. It builds a whole set to throw it away. That is the right call for
one number — but if you needed both the size and the membership tests, you
would build the set once and keep it, rather than calling this twice.

**The costs, said properly.** Each of the three functions is `O(n + m)` time —
one walk of one sheet to build the set, one walk of the other to answer — and
`O(n + m)` space: `O(m)` for the set of the other sheet, plus up to `O(n)` for
`seen` and the answer. The list version is `O(n × m)` time and `O(n)` space.
You bought time with memory. Say both halves.

## Download and run

Download
[exercise-05-radio-check-rosters-solution.py](./exercise-05-radio-check-rosters-solution.py)
and run it:

```bash
python exercise-05-radio-check-rosters-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-05-radio-check-rosters.py`.

## Common bugs to catch

- **`W2QRP` appears twice in `went silent`.** You dropped the `seen` set. The
  station answered twice last night, so the loop visits it twice, so it is
  written down twice. There is no exception — just a list with a repeat in it
  that a human would probably not notice on a busy sheet.

- **`both nights` reads `N9TIDE, KC4ORT`.** You looped over the wrong sheet.
  Both call signs are correct; the order is tonight's, not last night's. Walk
  the sheet whose order you want.

- **`TypeError: unhashable type: 'list'`.** You put something into a set that
  cannot be hashed:

  ```text
  Traceback (most recent call last):
      tonight = set([["KC4ORT"], ["W2QRP"]])
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  A set member must be **immutable all the way down**, because the set files it
  by its hash and a thing that can change would end up filed under a hash it no
  longer has. Strings and tuples are fine; lists and sets are not. Challenge 2
  is built on this rule.

- **`AttributeError: 'set' object has no attribute 'append'`.** You tried to
  build the answer in a set:

  ```text
  AttributeError: 'set' object has no attribute 'append'
  ```

  Sets have `add`, not `append` — and the deeper problem is that you wanted an
  ordered answer. A set will not give you one.

- **`TypeError: unsupported operand type(s) for -: 'set' and 'list'`.** You
  mixed the two halfway through:

  ```text
  TypeError: unsupported operand type(s) for -: 'set' and 'list'
  ```

  Set algebra works between sets. `set(first) - set(second)` is legal;
  `set(first) - second` is not. Python refusing here is a kindness — it is the
  one place the two types do not silently interchange.

- **The set is rebuilt inside the loop.** `if sign in set(second):` looks
  right, passes every assert, and is slower than the list version it replaced,
  because building a set is a walk *plus* hashing every element. Nothing tells
  you. The only defence is reading your own loop and asking what is constant.

## Under the hood

<details>
<summary>Under the hood — what a set is, and why intersection is cheaper than union</summary>

**A set is a dict with the values removed.** Same array of slots, same hashing,
same growth rule, same guarantees: `O(1)` average for `add`, `remove` and `in`,
`O(n)` worst case if every member collides.

Set algebra does **not** cost the same across the board, and the differences
are usable:

| Operation | Cost | Why |
|---|---|---|
| `s \| t` union | `O(len(s) + len(t))` | every member of both has to be looked at |
| `s & t` intersection | `O(min(len(s), len(t)))` | walk the **smaller**, probe the larger |
| `s - t` difference | `O(len(s))` | walk `s` only |
| `s <= t` subset | `O(len(s))` | walk `s`, probe `t` |

Intersection being `O(min(...))` is genuinely useful: intersecting a
ten-element set with a million-element set is ten probes, not a million. If you
only ever remember one asymmetry, remember that one.

**Why order is not available.** A set stores members wherever their hash sends
them. Two sets with the same members iterate in whatever order their slots
happen to be in, and for strings that order can differ between runs of the
program, because CPython salts string hashing at start-up to make
hash-collision attacks harder. So a set is not merely unordered as a matter of
policy — printing one twice from two different runs can genuinely give two
different orders. Never build an answer whose order matters out of a set.

**`frozenset` is the immutable one.** It can be a dict key or a member of
another set, because its hash cannot change under it. That is the whole of
Challenge 2's trick.

**When not to do the swap.** If you test membership once or twice, building the
set costs more than the walks it saves. And if the data is already sorted,
binary search gives `O(log n)` lookups with no extra memory at all — Week 5's
argument. "Use a set" is a very good default and it is not a law.

</details>

## Acceptance checklist

- [ ] `python exercise-05-radio-check-rosters.py` prints four lines then
      `All checks passed.`
- [ ] Each function builds its set **before** its loop, exactly once.
- [ ] Each answer is in the order of the sheet the function loops over.
- [ ] `W2QRP` appears once, not twice, in `went silent`.
- [ ] De-duplication uses a `seen` set, not a scan of the answer so far.
- [ ] Both input lists are unchanged.
- [ ] You can say the full trade — time saved, space paid — in one sentence.

## Stretch

- **Notice that your three functions are one function.**

  ```python
  def filtered_in_order(walk: list[str], other: list[str], *, present: bool) -> list[str]:
      """Return signs from `walk`, each once, kept when membership matches."""
      lookup = set(other)
      seen: set[str] = set()
      kept: list[str] = []
      for sign in walk:
          if (sign in lookup) == present and sign not in seen:
              seen.add(sign)
              kept.append(sign)
      return kept
  ```

  ```text
  both   : ['KC4ORT', 'N9TIDE']
  new    : ['K5MOOR', 'W7FOG']
  silent : ['W2QRP', 'VE3GULL']
  ```

  Three named functions calling one shared one is usually the better shape:
  the names are what the caller reads, and the body exists once so a fix lands
  once. The `*` in the signature forces `present=` to be written out at the
  call, because a bare `True` at a call site tells the reader nothing.

- **Measure the swap instead of believing it.**

  ```python
  signs = [f"K{number}ABC" for number in range(20_000)]
  misses = [f"Z{number}XYZ" for number in range(1_000)]

  as_list = sum(1 for sign in misses if sign in signs)
  as_set = set(signs)
  fast = sum(1 for sign in misses if sign in as_set)
  print(as_list, fast)
  ```

  ```text
  0 0
  ```

  Same answer, and the first line did twenty million comparisons to get it
  while the second did about twenty-one thousand. Time it if you like, but the
  arithmetic is the argument — Homework 1 and the mini-project both count the
  work instead of timing it, for exactly this reason.

- **See the asymmetry in `&` for yourself.**

  ```python
  small = {"KC4ORT", "W7FOG"}
  huge = {f"K{number}ABC" for number in range(200_000)}
  print(sorted(small & huge))
  print(sorted(huge & small))
  ```

  ```text
  []
  []
  ```

  Both spellings give the same answer and both cost the same, because Python
  looks at the two sizes and walks the smaller one whichever side you wrote it
  on. You do not have to remember to put the small set first — but you do have
  to know that `&` is `O(min)` and `|` is not, because that is the fact that
  decides which one belongs in your loop.

When your net report is right, the exercises are done. Move on to
[the challenges](../challenges/README.md).
