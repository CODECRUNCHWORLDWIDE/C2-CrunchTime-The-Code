# Exercise 3 — The Community Garden's Plot Map

> **Topic:** a list of lists — building one without accidentally sharing a row, and copying one without accidentally sharing all of them
> **Lecture:** [02 — Lists, Tuples and the Dynamic Array](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md)
> **Difficulty:** Beginner
> **Target time:** 25 minutes
> **Why this one:** every grid problem for the rest of this course — flood fill, islands, shortest path on a board — starts by building a grid and usually copies one. There is a one-character way to build that grid wrong, it raises no error, and the wrong version prints something plausible. This page makes the bug happen where you can see all twelve cells at once.

## The Brief

A community garden has three beds running north to south, and four plots in
each bed. The map on the shed door is a grid: a dot means nobody has claimed
that plot, and a letter means somebody has planted something.

```text
.C..
..B.
K...
```

In Python that map is a **list of lists**. The outer list holds the beds; each
bed is its own list of four cells.

Here is the trap, and it is the most-stepped-in trap in the language.

```python
beds = [["."] * 4] * 3
```

That looks like "three beds of four plots" and it is not. `["."] * 4` builds
one bed. Then `* 3` does **not** build three beds — it puts the *same bed* in
the list three times. Not three copies. One bed, pointed at from three places.
Plant a carrot in bed 0 and it appears in beds 1 and 2 as well, because there
was only ever one bed.

Think of it like a photocopy versus a mirror. `[["."] * 4 for _ in range(3)]`
runs the bed-building expression three separate times and gives you three
separate beds. `[["."] * 4] * 3` hangs two mirrors on one bed.

The same trap comes back the moment you copy a map. `beds[:]` gives you a new
outer list — and the *same* beds inside it.

Your job: build a map, plant in it, copy it safely, and count what is in it.

## Starter

Create `exercise-03-garden-plot-map.py` in your practice folder and paste this
in. Fill in every `TODO`.

```python
"""exercise-03-garden-plot-map.py — the community garden's plot map.

A map is a list of rows, and every row is a list of one-character cells.
Building one, copying one, and planting into one all look easy, and all
three have a way of quietly sharing a row that should have been separate.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

EMPTY = "."


def blank_map(rows: int, cols: int) -> list[list[str]]:
    """Return a fresh map with every plot empty.

    Args:
        rows: How many beds run north to south.
        cols: How many plots there are in each bed.

    Returns:
        A list of `rows` rows, each a separate list of `cols` cells.
    """
    # TODO: a comprehension, so the row expression runs once per row
    ...


def plant(plots: list[list[str]], row: int, col: int, crop: str) -> None:
    """Write one crop letter into one plot. Changes the map in place."""
    # TODO: one assignment
    ...


def copy_map(plots: list[list[str]]) -> list[list[str]]:
    """Return a map that shares nothing with the one handed in."""
    # TODO: a new outer list of NEW inner lists
    ...


def row_counts(plots: list[list[str]]) -> list[int]:
    """Return how many plots are planted in each bed."""
    # TODO: one count per row
    ...


def render(plots: list[list[str]]) -> str:
    """Return the map as text, one line per bed, no trailing newline."""
    # TODO: join the cells, then join the rows
    ...


# ---- Self-check ----
if __name__ == "__main__":
    beds = blank_map(3, 4)
    plant(beds, 0, 1, "C")
    plant(beds, 1, 2, "B")
    plant(beds, 2, 0, "K")

    print(render(beds))
    print(f"row counts: {row_counts(beds)}")

    spare = copy_map(beds)
    plant(spare, 0, 3, "T")
    print("after planting on the copy only:")
    print(render(spare))
    print(f"original row counts: {row_counts(beds)}")

    assert beds[0] is not beds[1]  # the beds are separate lists
    assert beds[0][3] == EMPTY  # the copy's tomato did not reach the original
    assert row_counts(beds) == [1, 1, 1]
    assert row_counts(spare) == [2, 1, 1]
    assert blank_map(0, 4) == []
    assert blank_map(2, 0) == [[], []]
    print("All checks passed.")
```

Three things you need before you start.

**`is` and `==` ask different questions.** `==` asks "do these hold the same
things?" `is` asks "are these the very same object?" Two separate empty beds
are `==` to each other and are not `is` each other. The first assert on the
page uses `is not` because equality could never catch this bug — the two
mirrored beds would compare equal right up until you planted something.

**A comprehension re-runs its expression.** `[expr for _ in range(3)]`
evaluates `expr` three times, so if `expr` builds a list you get three lists.
`[expr] * 3` evaluates `expr` once and repeats the result.

**`row[:]` is a copy of that row.** A slice of a list builds a new list holding
the same items. For a row of one-character strings that is exactly what you
want, because strings cannot be changed anyway.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/exercises/exercise-03-garden-plot-map.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `blank_map(rows, cols)` returns `rows` rows of `cols` cells, all `EMPTY`,
   and every row is a separate list.
2. `blank_map(0, 4)` returns `[]`. `blank_map(2, 0)` returns `[[], []]`.
3. `plant` changes the map in place and returns `None`.
4. `copy_map` returns a map that can be planted in without touching the
   original — no shared rows.
5. `row_counts` returns one number per bed, counting cells that are not
   `EMPTY`.
6. `render` returns the rows joined by newlines, with no trailing newline.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Build the map with a comprehension, never with `* rows` on a list of
  lists.** `[[EMPTY] * cols] * rows` puts one row in the map `rows` times, and
  planting in any of them plants in all of them. The first assert exists to
  catch exactly this and it uses `is not`, because two mirrored rows are still
  equal.

- **`[EMPTY] * cols` on its own is fine, and you should be able to say why.**
  That `*` also repeats one object — but the object is the string `"."`, and a
  string cannot be changed. Sharing a thing nobody can modify costs nothing and
  saves memory. The rule is: **`* n` is safe for things that cannot change, and
  a bug for things that can.**

- **`copy_map` must copy every row, not just the outer list.** `plots[:]` and
  `list(plots)` and `plots.copy()` all do the same thing — a **shallow copy**,
  a new outer list pointing at the same rows. Use `[row[:] for row in plots]`,
  which is one level deeper and is all this map needs.

- **Do not reach for `copy.deepcopy` here.** It is the general answer and it is
  the wrong reflex: it walks the whole structure, tracks objects it has already
  seen in case the structure points back at itself, and costs noticeably more
  than the row-by-row copy. Save it for structures you did not build yourself.
  The stretch measures the difference.

- **Maps are at most 50 by 50.** A community garden with more than a couple of
  thousand plots is a farm. The bound is here because the whole map is copied
  in `copy_map`, and copying is `O(rows × cols)` in both time and memory — at
  50 by 50 you may copy freely, and it is worth knowing the size at which that
  stops being true.

- **`crop` is one character.** The map is printed as a grid, and a two-letter
  crop would push its row out of line with the others. That is not a deep
  constraint; it is the difference between a map you can read at a glance and
  one you cannot.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-garden-plot-map.py
@@STDOUT:exercise-03-garden-plot-map-solution.py@@
```

The two blocks are the test. The first map has one crop per bed. Then a tomato
goes into the **copy** at row 0, and the copy shows four characters where the
original still shows three. If your two blocks are identical, your copy is
sharing rows with the original, and `original row counts` will read
`[2, 1, 1]`.

## Steps

1. Create the file, paste the starter, and run it. It fails at `render`,
   because everything before it returned `None`.
2. Write `blank_map` with a comprehension. Run it and print
   `blank_map(3, 4)` on its own to see the shape before anything is planted.
3. Now, on purpose, replace it with `return [[EMPTY] * cols] * rows` and run
   the file again. Read the printed map. Every bed has a carrot, a bean and a
   kale in it. **That is the bug this exercise is about** — look at it properly
   before you fix it.
4. Put the comprehension back and write `plant`, which is one line.
5. Write `copy_map`. Try the shallow version `return plots[:]` first and run
   the file: the maps print identically and `original row counts` comes back
   `[2, 1, 1]`. Then fix it with `[row[:] for row in plots]`.
6. Write `row_counts` and `render`.
7. When it passes, prove the fix rather than trusting it: in a REPL, build a
   map, copy it, and check `beds[0] is not spare[0]`.

## The Solution

```python
@@CODE:exercise-03-garden-plot-map-solution.py@@
```

**One comprehension is the whole fix.**

```python
return [[EMPTY] * cols for _ in range(rows)]
```

The part in front of `for` is an expression, and a comprehension evaluates it
once per pass. `rows` passes means `rows` separate row lists. The `_` is a
name that says "I am not going to use this" — the loop is here for its count,
not for its value.

Meanwhile `[EMPTY] * cols` *inside* it repeats one object `cols` times, and
that is fine, because that object is the string `"."`. Nobody can change a
string, so nobody can notice that all four cells point at the same one. The two
`*` operators in that line are the same operator doing the same thing, and one
is a bug and one is not, entirely because of what is being repeated.

**`copy_map` is a shallow copy applied one level down.**

```python
return [row[:] for row in plots]
```

`plots[:]` alone would build a new outer list holding the *same* row objects —
so planting in the copy would plant in the original, which is the same bug in
a different coat. `[row[:] for row in plots]` slices each row, and each slice
is a new list. The cells inside are strings, which cannot change, so two levels
is all this structure needs. Had the cells themselves been lists or dicts, two
levels would not have been enough, and that is the moment `copy.deepcopy`
earns its keep.

**`plant` changes the map and returns `None`, deliberately.** A map is a thing
the garden has one of. A function that returned a new map on every planting
would leave the caller juggling versions. Compare Exercise 1, where every
function returned something new and changed nothing — both are right, for
different jobs, and the name should tell you which you are looking at.

**`row_counts` counts with a generator expression inside `sum`.**
`sum(1 for cell in row if cell != EMPTY)` adds a 1 for every planted cell.
There are no square brackets, so no throwaway list of ones is built first. With
four cells that saves nothing; the habit is what you are building.

**`render` joins twice, and the inner join is the interesting one.**
`"".join(row)` turns four one-character strings into one four-character
string. `"\n".join(...)` then puts the rows together with a newline **between**
them and not after the last one — which is why the printed map does not end in
a blank line. Building the same text with `text += line + "\n"` would give you
a trailing newline you then have to remember to strip, and would copy the whole
map on every row.

**The empty cases fall out.** `blank_map(0, 4)` gives `[]` because `range(0)`
runs the expression zero times. `blank_map(2, 0)` gives `[[], []]` because
`[EMPTY] * 0` is an empty list — two beds with no plots in them, which is a
strange garden but a coherent answer. Neither needed a guard, and both are in
the asserts because a version built with a `while` loop and a counter usually
gets one of them wrong.

## Download and run

Download
[exercise-03-garden-plot-map-solution.py](./exercise-03-garden-plot-map-solution.py)
and run it:

```bash
python exercise-03-garden-plot-map-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-03-garden-plot-map.py`.

## Common bugs to catch

- **Every bed shows every crop, and there is no error at all.** You built the
  map with `[[EMPTY] * cols] * rows`:

  ```text
  KCB.
  KCB.
  KCB.
  ```

  Three plantings went into three different beds, and all three landed in the
  same bed, because there was only ever one. The kale, the carrot and the bean
  are sitting in columns 0, 1 and 2 of it, and the map shows that one row three
  times. **This bug raises nothing.** No traceback, no warning, just a map that
  is wrong in a way that looks tidy. The assert `beds[0] is not beds[1]` is the
  only thing on the page that can catch it.

- **`original row counts: [2, 1, 1]`.** Your `copy_map` is shallow — `plots[:]`
  or `list(plots)`. The outer list is new, so `spare is not beds`, and every
  row inside it is the original row, so planting in the copy planted in the
  original. This is the same bug as the one above, arriving from the other
  direction, and it is why the page asks for both checks.

- **`TypeError: 'str' object does not support item assignment`.** Your rows are
  strings, not lists of characters:

  ```text
  Traceback (most recent call last):
      plots[row][col] = crop
      ~~~~~~~~~~^^^^^
  TypeError: 'str' object does not support item assignment
  ```

  You probably built the map with `[EMPTY * cols for _ in range(rows)]` —
  multiplying the *string* rather than a one-item list, which gives `"...."`
  instead of `[".", ".", ".", "."]`. One pair of brackets. `render` would even
  have worked.

- **`IndexError: list index out of range`.** You planted outside the map:

  ```text
  Traceback (most recent call last):
      plots[row][col] = crop
      ~~~~~^^^^^
  IndexError: list index out of range
  ```

  Read which index the caret is under. If it is the first one you ran off the
  bottom of the map; if it is the second, off the side of a bed. This exercise
  has no bounds checking on purpose, and that is a decision worth noticing: a
  grid problem in Week 6 will need one, and it will need it at every one of
  four neighbours.

- **A negative row plants silently in the wrong bed.** `plant(beds, -1, 0,
  "K")` puts kale in the **last** bed and raises nothing, because a negative
  index counts from the end. When a grid coordinate comes from arithmetic —
  `row - 1` on the top row — that is how a bug walks off the top edge and wraps
  round to the bottom without telling you.

- **The rendered map has a blank line at the end.** You built it with
  `text += "".join(row) + "\n"`. `"\n".join(rows)` puts separators *between*
  rows only. The extra newline is harmless right up until you compare your
  output to the expected output character for character, which is what the
  course does.

## Under the hood

<details>
<summary>Under the hood — what a list actually holds, and what "shallow" really means</summary>

**A list does not contain its items. It contains pointers to them.**

A Python list is one block of memory holding addresses. `beds[0]` reads an
address and follows it to a row object that lives somewhere else entirely. So:

- `beds[:]` copies the **addresses**. Both lists then point at the same rows.
  That is what "shallow" means — one level of copying.
- `[row[:] for row in beds]` copies the addresses *and* makes each row copy its
  own addresses. Two levels.
- `copy.deepcopy(beds)` keeps copying until it reaches things that cannot be
  changed, and remembers what it has already copied so a structure that points
  back at itself does not loop forever.

`[x] * 3` copies one address three times. Every consequence in this exercise
follows from that single sentence.

**Why the language does not just fix it.** `*` on a list means "repeat this
sequence", and repeating a sequence of pointers by copying the pointers is
exactly what it says. Making it deep-copy instead would make
`[0] * 1_000_000` — a genuinely common and genuinely cheap line — allocate a
million objects. The behaviour is right; it is the reading of it that is
tempting and wrong.

**Two more places the same mirror appears.**

```python
def add(item, basket=[]):     # the list is built ONCE, when def runs
    basket.append(item)
    return basket
```

Every call with no basket shares the one list from the definition. Write
`basket=None` and build it inside.

```python
for plot in bed:
    if plot == EMPTY:
        bed.remove(plot)      # the index moves under the loop
```

Removing while iterating skips items. Build a new list instead:
`bed = [p for p in bed if p != EMPTY]`.

**The cost of a copy.** `copy_map` on an `r × c` map is `O(r × c)` time and
`O(r × c)` extra memory. That is fine at 3 by 4 and fine at 50 by 50. It is not
fine inside a loop that copies the map once per move — which is exactly how a
backtracking solution written in a hurry turns `O(moves)` into
`O(moves × r × c)`. Week 12 comes back to this with the alternative: change the
one cell, recurse, then change it back.

</details>

## Acceptance checklist

- [ ] `python exercise-03-garden-plot-map.py` prints two maps, two count lines,
      then `All checks passed.`
- [ ] The second map has four planted cells and the first still has three.
- [ ] `blank_map` uses a comprehension; `[[EMPTY] * cols] * rows` appears
      nowhere.
- [ ] `copy_map` copies every row.
- [ ] `blank_map(0, 4)` is `[]` and `blank_map(2, 0)` is `[[], []]`.
- [ ] `render` produces no trailing newline.
- [ ] You can explain, in one sentence, why `[EMPTY] * cols` is safe and
      `[[EMPTY] * cols] * rows` is not.

## Stretch

- **Count by column instead of by bed.**

  ```python
  def col_counts(plots: list[list[str]]) -> list[int]:
      """Return how many plots are planted in each column, west to east."""
      return [sum(1 for cell in column if cell != EMPTY) for column in zip(*plots)]
  ```

  ```text
  rows: [1, 1, 1]
  cols: [1, 1, 1, 0]
  ```

  `zip(*plots)` hands you the map turned on its side, one column at a time, as
  tuples. It is the standard way to walk a grid the other way and it copies
  nothing until you ask it to — `zip` is lazy, so the columns are built one at
  a time as the comprehension consumes them.

- **Watch a shallow copy fail, on purpose.**

  ```python
  beds = blank_map(2, 2)
  shallow = beds[:]
  deep = copy_map(beds)
  plant(beds, 0, 0, "C")
  print("shallow:", render(shallow).replace("\n", " | "))
  print("deep   :", render(deep).replace("\n", " | "))
  ```

  ```text
  shallow: C. | ..
  deep   : .. | ..
  ```

  The shallow copy saw the change because it was never a copy of the rows —
  only of the list holding them. Keep this snippet. It is four lines and it is
  the fastest way to re-convince yourself of the rule in six months.

- **Try `copy.deepcopy` and find out what it protects you from.**

  ```python
  import copy

  nested = [[{"crop": "carrot"}], [{"crop": "bean"}]]
  by_row = [row[:] for row in nested]
  by_deep = copy.deepcopy(nested)
  nested[0][0]["crop"] = "kale"
  print("row-slice copy:", by_row[0][0]["crop"])
  print("deepcopy      :", by_deep[0][0]["crop"])
  ```

  ```text
  row-slice copy: kale
  deepcopy      : carrot
  ```

  Two levels was enough for a map of strings and is not enough for a map of
  dicts. `deepcopy` keeps going until it reaches things that cannot change.
  That is why it is the right tool sometimes and the wrong reflex always —
  it costs more, and knowing how deep your own structure goes is cheaper than
  paying for arbitrary depth.

When your map is right, move on to
[Exercise 4 — The Depot's Lost-Property Shelf](./exercise-04-lost-property-shelf.md).
