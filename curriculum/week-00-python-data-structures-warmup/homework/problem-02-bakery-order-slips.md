# Problem 2 — The Bakery's Order Slips

> **Topic:** `split()` with no argument versus `split(" ")`, and normalising text somebody typed by hand
> **Lecture:** [01 — Strings and the Cost of Immutability](../lecture-notes/01-strings-and-immutability.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** the difference between `split()` and `split(" ")` has cost people correctness in real interviews, and the reason is that both look right. This page hands you a slip with three spaces in the middle of it and makes the difference show up in the answer rather than in a footnote.

## The Brief

A bakery takes orders on a paper pad. Each slip says how many, of what, for
whom:

```text
2 x sourdough / kelly
```

The pad is written with a pen by whoever is on the counter, so the spacing is
whatever the pen felt like. One slip has three spaces in the middle of the item
name. One has the customer's name in capitals. Two of them are not orders at
all — one is missing the quantity, one spells it as a word.

You are writing the little program that puts the pad on the kitchen board. For
every slip it prints either

```text
Kelly: 2 x sourdough
```

or, when the slip cannot be read,

```text
unreadable: x sourdough / kelly
```

and at the end it prints the basket: how much of each item was ordered in
total, in the order the items were first ordered.

Two rules about the text, and they are the reason the page exists.

**`split()` with no argument** breaks on *runs* of whitespace and throws away
whatever is at the ends. `"  1  x   rye    loaf  ".split()` gives you
`['1', 'x', 'rye', 'loaf']` — four clean fields, no matter how the pen
wandered.

**`split(" ")` with a space** breaks on every single space and keeps the gaps
as empty strings: `['', '', '1', '', 'x', '', '', 'rye', …]`. That is not a bug
in Python; it is what you need for `"a,,b".split(",")` to give three fields
with a blank in the middle, which is how every CSV file in the world works. It
is simply not what you want for a sentence.

Joining the fields back with `" ".join(parts[2:])` then gives you `rye loaf`,
single-spaced, whatever went in. Split-then-join is a normalising round trip
you get for free.

## Starter

Create `problem-02-bakery-order-slips.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""problem-02-bakery-order-slips.py — tidy the counter's order slips.

A quantity, an x, what was ordered, a slash, and who it is for. The spacing
is whatever the pen felt like.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

SLIPS: list[str] = [
    "2 x sourdough / kelly",
    "  1  x   rye    loaf / MO ",
    "3 x sourdough / Ade",
    "x sourdough / kelly",
    "two x baguette / Kelly",
    "5 x seeded roll / bo",
]


def fields(slip: str) -> tuple[int, str, str] | None:
    """Pull the three parts out of one slip.

    Args:
        slip: One raw line from the order pad.

    Returns:
        (quantity, item, customer), or None when the slip cannot be read.
        The item is lower-cased and single-spaced; the customer is
        title-cased.
    """
    # TODO: exactly one "/", then split() the left half, then check
    # parts[1] == "x" and parts[0].isdigit()
    ...


def tidy(slip: str) -> str:
    """Render one slip for the kitchen board, or say it is unreadable."""
    ...


def basket(slips: list[str]) -> dict[str, int]:
    """Add up how much of each item was ordered, first-ordered order."""
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for slip in SLIPS:
        print(tidy(slip))
    loaves = basket(SLIPS)
    print("basket: " + ", ".join(f"{item} {count}" for item, count in loaves.items()))

    assert fields("  1  x   rye    loaf / MO ") == (1, "rye loaf", "Mo")
    assert fields("x sourdough / kelly") is None
    assert fields("two x baguette / Kelly") is None
    assert fields("2 x sourdough") is None
    assert tidy("2 x sourdough / kelly") == "Kelly: 2 x sourdough"
    assert loaves == {"sourdough": 5, "rye loaf": 1, "seeded roll": 5}
    assert list(loaves) == ["sourdough", "rye loaf", "seeded roll"]
    assert basket([]) == {}
    assert SLIPS[1] == "  1  x   rye    loaf / MO "  # the pad is untouched
    print("All checks passed.")
```

Three things you need before you start.

**`text.isdigit()`** is true when every character is a digit and there is at
least one. `"2".isdigit()` is `True`; `"two"` and `""` are both `False`. It is
how you ask "can this be a number?" without a `try`.

**`text.title()`** upper-cases the first letter of each word and lower-cases
the rest, so `"MO"` becomes `"Mo"` and `"bo"` becomes `"Bo"`. Like every string
method it returns a new string.

**`slip.count("/")`** counts the separators before you split on them. Checking
for exactly one is how you reject a slip with none — and a slip with two, which
would otherwise unpack into three halves and raise.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-02-bakery-order-slips.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `fields` returns `None` unless the slip has exactly one `/`, at least three
   fields on the left, `x` as the second field, and a digit string as the
   first.
2. The item is everything after the `x`, lower-cased and single-spaced.
3. The customer is the right-hand half, trimmed, single-spaced and title-cased.
   An empty customer makes the slip unreadable.
4. `tidy` returns `"Customer: 2 x item"` or `"unreadable: <slip, trimmed>"`.
5. `basket` totals the quantities per item, items in first-ordered order, and
   ignores unreadable slips.
6. `basket([])` returns `{}`.
7. `SLIPS` is unchanged. Every function keeps its type hints and its docstring.

## Constraints

- **Use `split()` with no argument on the left half.** `split(" ")` would hand
  you empty strings between the pen's double spaces, `parts[1]` would be `""`
  instead of `"x"`, and the second slip would be rejected as unreadable for a
  reason that has nothing to do with the order.

- **Single-space the item with `" ".join(parts[2:])`, not by replacing
  doubles.** `item.replace("  ", " ")` fixes two spaces into one and leaves
  three spaces as two. Chaining more replaces is a hole you dig deeper. The
  split has already thrown the spacing away; joining puts exactly one back.

- **Check with `isdigit()`, not with a `try`/`int`.** Both work. `isdigit` says
  what it means, and reserving `try` for the cases where there is no cheap test
  keeps the shape of the function readable. Note the limit: `isdigit` is
  `False` for `"-2"` and for `"2.5"`, and a bakery has no use for either.

- **A slip with no customer is unreadable.** `"2 x sourdough /"` gives an empty
  right-hand half, which would print as `": 2 x sourdough"` — a line the
  kitchen cannot act on. Rejecting it is a decision, and it is the kind of
  decision a specification usually leaves out and an interviewer usually asks
  about.

- **At most 300 slips a day, each at most 120 characters.** A busy counter
  writes a few hundred slips; 120 characters is the width of the pad. Both
  bounds say the same thing: parsing is `O(total characters)` and nothing here
  needs to be clever. What they do *not* excuse is calling `fields` twice on
  the same slip — which `tidy` and `basket` between them already do, and which
  is worth noticing even when it costs nothing.

- **Names are ASCII.** `title()` on ASCII does what it looks like. On other
  alphabets it has opinions — it will happily capitalise after an apostrophe
  and turn `"o'brien"` into `"O'Brien"`, which is right, and `"mcdonald"` into
  `"Mcdonald"`, which is not. Real name handling is a much harder problem than
  it looks, and the bound is here so this page does not pretend otherwise.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-bakery-order-slips.py
Kelly: 2 x sourdough
Mo: 1 x rye loaf
Ade: 3 x sourdough
unreadable: x sourdough / kelly
unreadable: two x baguette / Kelly
Bo: 5 x seeded roll
basket: sourdough 5, rye loaf 1, seeded roll 5
All checks passed.
```

Line two is the one to check: `Mo: 1 x rye loaf`, single-spaced, from a slip
with three spaces inside the item and two spaces around it. If yours says
`rye    loaf`, you joined with the original text instead of the split fields.
And the basket is in first-ordered order — `sourdough` first because it was the
first thing anybody ordered, not because it is alphabetically first or the
biggest total.

## Steps

1. Create the file, paste the starter, and run it. Every line prints `None`.
2. Write `fields`, and write the rejections in order of cheapness: the `/`
   count, then the field count, then `parts[1] == "x"`, then `isdigit`.
3. Test it on the second slip alone in a REPL before running the whole file.
   `fields("  1  x   rye    loaf / MO ")` must be exactly
   `(1, "rye loaf", "Mo")`.
4. Now try it with `left.split(" ")` on purpose and look at what `parts[1]`
   becomes. That is the entire lesson of this page in one experiment.
5. Write `tidy`. It is an `if parsed is None` and an f-string.
6. Write `basket`. It is Exercise 4's counting loop with `+ quantity` instead
   of `+ 1`.
7. When it passes, add a slip of your own with a two-word item and a name in
   capitals, and check the board line before you check the assert.

## The Solution

```python
"""problem-02-bakery-order-slips-solution.py — tidy the counter's order slips.

Slips are written by hand on a pad: a quantity, an x, what was ordered, a
slash, and who it is for. The spacing is whatever the pen felt like.

`split()` with no argument is the whole trick: it collapses runs of spaces
and strips the ends. `split(" ")` does neither, and would leave you holding
a list full of empty strings.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

SLIPS: list[str] = [
    "2 x sourdough / kelly",
    "  1  x   rye    loaf / MO ",
    "3 x sourdough / Ade",
    "x sourdough / kelly",
    "two x baguette / Kelly",
    "5 x seeded roll / bo",
]


def fields(slip: str) -> tuple[int, str, str] | None:
    """Pull the three parts out of one slip.

    Args:
        slip: One raw line from the order pad.

    Returns:
        (quantity, item, customer), or None when the slip cannot be read.
        The item is lower-cased and single-spaced; the customer is
        title-cased.
    """
    if slip.count("/") != 1:
        return None
    left, right = slip.split("/")
    parts = left.split()
    if len(parts) < 3 or parts[1] != "x":
        return None
    if not parts[0].isdigit():
        return None
    customer = " ".join(right.split()).title()
    if not customer:
        return None
    return int(parts[0]), " ".join(parts[2:]).lower(), customer


def tidy(slip: str) -> str:
    """Render one slip the way the kitchen board wants it.

    Args:
        slip: One raw line from the order pad.

    Returns:
        "Customer: 2 x item", or "unreadable: <the slip, trimmed>".
    """
    parsed = fields(slip)
    if parsed is None:
        return f"unreadable: {slip.strip()}"
    quantity, item, customer = parsed
    return f"{customer}: {quantity} x {item}"


def basket(slips: list[str]) -> dict[str, int]:
    """Add up how much of each item was ordered.

    Args:
        slips: The whole pad, unreadable slips and all.

    Returns:
        A dict from item to total quantity, items in first-ordered order.
    """
    totals: dict[str, int] = {}
    for slip in slips:
        parsed = fields(slip)
        if parsed is None:
            continue
        quantity, item, _customer = parsed
        totals[item] = totals.get(item, 0) + quantity
    return totals


# ---- Self-check ----
if __name__ == "__main__":
    for slip in SLIPS:
        print(tidy(slip))
    loaves = basket(SLIPS)
    print("basket: " + ", ".join(f"{item} {count}" for item, count in loaves.items()))

    assert fields("  1  x   rye    loaf / MO ") == (1, "rye loaf", "Mo")
    assert fields("x sourdough / kelly") is None
    assert fields("two x baguette / Kelly") is None
    assert fields("2 x sourdough") is None
    assert tidy("2 x sourdough / kelly") == "Kelly: 2 x sourdough"
    assert loaves == {"sourdough": 5, "rye loaf": 1, "seeded roll": 5}
    assert list(loaves) == ["sourdough", "rye loaf", "seeded roll"]
    assert basket([]) == {}
    assert SLIPS[1] == "  1  x   rye    loaf / MO "  # the pad is untouched
    print("All checks passed.")
```

**The rejections are ordered by cost, cheapest first.**

```python
if slip.count("/") != 1:
    return None
left, right = slip.split("/")
parts = left.split()
if len(parts) < 3 or parts[1] != "x":
    return None
```

Counting a character is cheaper than splitting, and splitting the left half is
cheaper than splitting and joining the right one. None of that matters at 300
slips; the habit of putting the cheap guard first matters everywhere, and it
also reads in the order a person would check.

Note `!= 1` rather than `not in slip`. A slip with two slashes would unpack
into three values and raise `ValueError: too many values to unpack`, which is a
crash rather than a rejection. Counting first turns that into a `None`.

**`len(parts) < 3` and not `!= 3`,** because an item can be several words. The
item is then `" ".join(parts[2:])` — everything after the `x`, put back
together with exactly one space between each piece. Split threw the pen's
spacing away; join puts a canonical version back. That round trip is the whole
normalisation and it is two calls.

**`" ".join(right.split()).title()`** does the same thing to the customer, then
title-cases it. `"  MO "` becomes `"MO"` becomes `"Mo"`. Doing it in that order
matters: `.title()` on the untrimmed string would work too, but the trimming
has to happen either way and doing it with `split`/`join` also collapses a
double-barrelled name typed with two spaces.

**The empty-customer check comes after the join,** because `" ".join([])` is
`""` and that is exactly the case being rejected. Checking `right.strip()`
first would work as well; checking the value you are about to return is the one
that cannot drift away from what the function actually produces.

**`basket` ignores what it cannot read, and keeps the order it saw.**
`totals.get(item, 0) + quantity` is the counting idiom with a weight on it.
The dict remembers first-insertion order, so the basket reads in the order the
items were first ordered — no sorting, and no `OrderedDict`.

**One inefficiency worth naming.** `tidy` calls `fields`, and then `basket`
calls `fields` again on every slip, so each slip is parsed twice. At 300 slips
that is invisible, and it buys two functions that each do one thing and can
each be tested alone. If the pad were a year of slips you would parse once into
a list of records and pass that around. Being able to say *why* the cheap
version is fine here, and what you would change if it were not, is the Examine
step of FRAME.

## Run it

Copy the worked answer on this page into `problem-02-bakery-order-slips.py` and run it:

```bash
python problem-02-bakery-order-slips.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-02-bakery-order-slips.py`.

## Common bugs to catch

- **The second slip prints `unreadable`.** You split the left half with
  `split(" ")`. The pen's double space put an empty string at `parts[1]`, so
  the `x` check failed. The slip is fine; the split was not.

- **`Mo: 1 x rye    loaf`.** You kept the item as raw text —
  `left[left.index("x") + 1:]` or similar — instead of joining the split
  fields. The spacing came through because nothing ever removed it.

- **`ValueError: too many values to unpack (expected 2)`.** A slip had two
  slashes:

  ```text
  ValueError: too many values to unpack (expected 2)
  ```

  Count the separator before splitting on it. This is the same class of bug as
  reading `parts[1]` before checking how many parts there are.

- **`ValueError: invalid literal for int() with base 10: 'two'`.** You called
  `int` without checking first:

  ```text
  Traceback (most recent call last):
      return int(parts[0]), ...
             ^^^^^^^^^^^^^
  ValueError: invalid literal for int() with base 10: 'two'
  ```

  Either guard with `isdigit()` or wrap in `try`. Do not do both — a check
  followed by a `try` that can never fire reads as if the author was not sure.

- **`AttributeError: 'int' object has no attribute 'title'`.** You title-cased
  the wrong end of the tuple:

  ```text
  AttributeError: 'int' object has no attribute 'title'
  ```

  A reminder that unpacking in the wrong order fails loudly for strings and
  numbers, and silently when both fields are strings. Name your variables after
  what they hold.

- **`basket` counts slips instead of loaves.** You wrote `+ 1` instead of
  `+ quantity`. The totals are plausible, smaller, and wrong — `sourdough`
  comes out `2` because two slips mentioned it. Nothing raises.

- **The basket is alphabetical.** You sorted on the way out. The requirement
  asks for first-ordered order, which the dict was already keeping for you.

## Under the hood

<details>
<summary>Under the hood — what split really does, and the case for and against regex</summary>

**`split()` and `split(sep)` are two different algorithms sharing a name.**

The no-argument form skips leading whitespace, then reads a run of
non-whitespace as a field, then skips the whitespace after it, and repeats. So
the ends are trimmed and runs collapse. It treats spaces, tabs and newlines
alike.

The separator form scans for each occurrence of the separator and cuts there,
whatever is on either side. That is why the empties appear, and it is
non-negotiable: `"a,,b".split(",")` must give `['a', '', 'b']` or no CSV parser
could work.

```python
"  a  b  ".split()       # ['a', 'b']
"  a  b  ".split(" ")    # ['', '', 'a', '', 'b', '', '']
```

**Cost.** Both are `O(n)` time and `O(n)` space, and the pieces are new string
objects — copies, not views into the original, because a Python string owns its
characters. So a parser that splits the same line three times has done three
walks and three sets of allocations.

**`maxsplit` saves the rest of the work.** `slip.split("/", 1)` stops after the
first cut and gives you at most two pieces, with everything else left in the
second one. When you only want to cut once, saying so is both faster and more
precise — and it makes a stray second slash part of the customer's name instead
of an error, which may or may not be what you want. This page counts instead,
because rejecting a two-slash slip is the more honest behaviour for a kitchen.

**What about a regular expression?** `re.fullmatch(r"\s*(\d+)\s+x\s+(.+?)\s*/\s*(.+?)\s*", slip)`
does the whole job in one line, and for a format this fixed it is a reasonable
tool. It is not used here for two reasons. When it fails it tells you nothing
about *which* part failed, so "unreadable" loses the ability to say why — the
stretch on Challenge 1 is about exactly that. And in an interview, a hand-rolled
parser shows the reasoning a regex hides. Know that `re` exists, and reach for
it when the format is genuinely irregular rather than merely fiddly.

</details>

## Acceptance checklist

- [ ] `python problem-02-bakery-order-slips.py` prints six board lines, the
      basket line, then `All checks passed.`
- [ ] Slip two prints `Mo: 1 x rye loaf`, single-spaced.
- [ ] The left half is split with `split()` and no argument.
- [ ] Two of the six slips print `unreadable`, and you can say why each one
      failed.
- [ ] The basket totals loaves, not slips.
- [ ] The basket is in first-ordered order.
- [ ] You can say what `"a,,b".split(",")` returns and why it has to.

## Stretch

- **Say which rule each unreadable slip broke.**

  ```python
  def why_unreadable(slip: str) -> str | None:
      """Return the rule a slip broke, or None when it parses."""
      if slip.count("/") != 1:
          return "needs exactly one /"
      parts = slip.split("/")[0].split()
      if len(parts) < 3:
          return "too few fields"
      if parts[1] != "x":
          return "second field is not x"
      if not parts[0].isdigit():
          return "quantity is not a number"
      return "no customer"
  ```

  ```text
  ['too few fields', 'quantity is not a number']
  ```

  Useful, and it duplicates every rule in `fields`. The day somebody allows
  `X` as well as `x`, one of the two will be updated. The fix is to have
  `fields` return the reason alongside the result; deciding what shape that
  takes is a real design question and worth ten minutes of your own thought.

- **Group the basket by customer instead.**

  ```python
  def by_customer(slips: list[str]) -> dict[str, list[str]]:
      """Return each customer and the items they ordered, in slip order."""
      out: dict[str, list[str]] = {}
      for slip in slips:
          parsed = fields(slip)
          if parsed is None:
              continue
          quantity, item, customer = parsed
          out.setdefault(customer, []).append(f"{quantity} x {item}")
      return out
  ```

  ```text
  {'Kelly': ['2 x sourdough'], 'Mo': ['1 x rye loaf'], 'Ade': ['3 x sourdough'], 'Bo': ['5 x seeded roll']}
  ```

  Same parse, different key. Most "can you also show me…" requests are exactly
  this, which is why choosing what the key should be is most of the work in a
  dict problem.

- **Find out what `title()` does to a real name.**

  ```python
  for name in ["o'brien", "mcdonald", "van der berg", "MO"]:
      print(f"{name:<14} -> {name.title()}")
  ```

  ```text
  o'brien        -> O'Brien
  mcdonald       -> Mcdonald
  van der berg   -> Van Der Berg
  MO             -> Mo
  ```

  One of those four is wrong, one is arguable, and two are fine. Names are a
  much harder problem than string methods make them look — which is a good
  reason to store what somebody typed and display it back, rather than
  "correcting" it.

Next: [Problem 3 — The Sled Team's Rotation](./problem-03-sled-team-rotation.md).
