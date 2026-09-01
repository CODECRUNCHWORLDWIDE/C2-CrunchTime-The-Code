# Exercise 1 — Seed Packet Codes

> **Topic:** strings cannot be edited, so every "change" is really a new string — and the cheap way to build one is a list plus `"".join(...)`
> **Lecture:** [01 — Strings and the Cost of Immutability](../lecture-notes/01-strings-and-immutability.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** cleaning up text is the first thing almost every program does with its input, and it is where beginners write their first accidental `O(n²)`. If you build a string one character at a time with `+=`, you copy everything you have built so far, every single time. This page makes you feel that, on a job small enough to check by eye.

## The Brief

A community seed library keeps a shoebox of donated seed packets. Every packet
has a code written on it by hand, and no two volunteers write it the same way.
Some use spaces. Some use dashes. One of them drew three question marks.

You are writing the little program that turns those scribbles into shelf
labels. The rule the librarians agreed on is short:

- Keep only **letters and digits**. Everything else goes.
- Make the letters **capital**.
- Cut what is left into **blocks of four**, joined by a dash — `DON4-417K-ALE`.
- A packet whose code begins with `DON` was **donated**. Anything else was
  bought.

Here is the part that matters more than the rule. **A Python string cannot be
changed once it exists.** Think of a string as a word carved into a wooden
block. You cannot re-carve one letter. If you want a different word, you carve
a whole new block.

```python
code = "hello"
code[0] = "H"          # there is no mechanism for this
```

So every step above — dropping a character, capitalising it, adding a dash —
does not edit anything. It builds something new. Do that inside a loop, one
character at a time, and you carve a fresh block on every pass: first a block
of one letter, then of two, then of three. A hundred letters means five
thousand letters carved.

The way out is to keep the pieces in a **list** — a list *can* be added to
cheaply — and carve exactly once at the end with `"".join(pieces)`. That is
the habit this exercise is here to build.

## Starter

Create `exercise-01-seed-packet-codes.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""exercise-01-seed-packet-codes.py — tidy the seed library's codes.

Four small string functions. None of them edits a string, because none of
them can: each one builds a new string and hands it back.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

BLOCK = 4

RAW_PACKETS: list[str] = [
    "don 4417 kale",
    "buy-2210-tomato",
    "  DON 0001  ",
    "???",
    "bee balm #7",
    "sage 12",
]


def clean_code(raw: str) -> str:
    """Return the tidy form of one handwritten packet code.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The kept letters and digits, upper-cased, in blocks of four joined
        by "-". An empty string when nothing survives.
    """
    # TODO: keep letters and digits into a LIST, then join. Never `out += ch`.
    ...


def dropped_count(raw: str) -> int:
    """Return how many characters the cleaner threw away."""
    # TODO: count the characters that are not letters or digits
    ...


def is_donation(code: str) -> bool:
    """Return True when a cleaned code begins with the donation marker."""
    # TODO: str.startswith. Do not slice.
    ...


def shelf_line(raw: str) -> str:
    """Return one line of the shelf listing for a raw code."""
    # TODO: use the three functions above, then one f-string
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for raw in RAW_PACKETS:
        print(shelf_line(raw))

    assert clean_code("don 4417 kale") == "DON4-417K-ALE"
    assert clean_code("buy-2210-tomato") == "BUY2-210T-OMAT-O"
    assert clean_code("???") == ""
    assert clean_code("") == ""
    assert dropped_count("  DON 0001  ") == 5
    assert dropped_count("sage 12") == 1
    assert dropped_count("") == 0
    assert is_donation(clean_code("don 4417 kale"))
    assert not is_donation(clean_code("buy-2210-tomato"))
    assert RAW_PACKETS[0] == "don 4417 kale"  # the raw scans are untouched
    print("All checks passed.")
```

Four things you need before you start.

**`ch.isalnum()`** answers "is this one character a letter or a digit?" It
returns `True` or `False` and allocates nothing.

**`"".join(pieces)`** glues a list of strings together with nothing between
them. `"-".join(pieces)` puts a dash between them. `join` is a method **on the
separator**, not on the list — `pieces.join("-")` is the classic wrong way
round and Python will tell you so.

**A slice** like `kept[0:4]` means "a new list holding those four". Slices
never go out of range: ask for four when two are left and you get two.

**`code.startswith("DON")`** checks the front of a string without building a
copy of it. `code[:3] == "DON"` gets the same answer, but it carves a
three-letter block first and then throws it away.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/exercises/exercise-01-seed-packet-codes.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `clean_code` keeps only characters where `ch.isalnum()` is true, upper-cases
   them, and returns them in dash-separated blocks of `BLOCK` characters.
2. `clean_code("")` and `clean_code("???")` both return `""`, with no crash and
   no stray dash.
3. `dropped_count` returns how many characters of `raw` were **not** kept. It
   never looks at the cleaned code.
4. `is_donation` is true exactly when the cleaned code starts with `DON`.
5. `shelf_line` prints the cleaned code padded to 16 characters, then two
   spaces, then `donated` or `bought`, then two spaces, then the drop count and
   the word `dropped`. An empty code shows as `(empty)`.
6. The strings in `RAW_PACKETS` are the same afterwards as before. That is free
   here — but say out loud *why* it is free.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Build with a list and one `join`. Never `out += ch` in a loop.** Each `+=`
  builds a whole new string containing everything so far, so a code of `n`
  characters copies `1 + 2 + … + n` characters in total. That is `O(n²)`. The
  list-then-join version copies each character exactly once. On a six-character
  code the difference is invisible; the habit is what you are building, and
  Homework 1 makes you count the copies.

- **Use `ch.isalnum()`, not a hand-written list of allowed characters.** A
  hand-written check is longer, slower to read, and forgets a digit sooner or
  later. It also hides the real decision behind a wall of `or`.

- **`raw` is plain ASCII.** The seed library's scanner cannot produce anything
  else. This matters because `isalnum()` is true for letters in every alphabet
  — `"é"` and `"٣"` both pass — so on non-ASCII input this cleaner would keep
  characters the label printer cannot print. The bound is here so you never
  have to write that guard, not because the guard would be hard.

- **Codes are at most 40 characters.** They are written by hand on a paper
  packet, so there is a physical limit. The bound is small on purpose: it means
  you can check every answer on this page by eye, and it means a wrong `O(n²)`
  version still finishes instantly — you cannot feel this bug, you have to
  reason about it.

- **Use `startswith`, not a slice.** `code[:3]` allocates a new three-character
  string just to compare it and throw it away. `startswith` compares in place.
  Same answer, one less object, and it reads like the sentence you would say.

- **`dropped_count` counts the raw string, not the clean one.** Subtracting
  lengths (`len(raw) - len(code)`) would be wrong, because the cleaned code has
  dashes in it that were never in `raw`. This is the kind of shortcut that
  looks right and gives a number nobody notices is wrong.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-seed-packet-codes.py
DON4-417K-ALE     donated  2 dropped
BUY2-210T-OMAT-O  bought  2 dropped
DON0-001          donated  5 dropped
(empty)           bought  3 dropped
BEEB-ALM7         bought  3 dropped
SAGE-12           bought  1 dropped
All checks passed.
```

Look at row four. Three question marks leave nothing behind, so the code is
empty, so it prints `(empty)` — and it counts as `bought`, because an empty
string does not start with `DON`. Row three is the other one to check: five
characters were dropped there, two spaces at the front, one in the middle, two
at the end.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-seed-packet-codes.py`. It fails on the first line that
   uses a result. That is the correct starting point — it proves the
   self-checks are real.
2. Write `clean_code` in two stages. First get the keeping and the
   upper-casing right and return `"".join(kept)` — no blocks yet. Run it. Check
   that `"don 4417 kale"` gives you `DON4417KALE`.
3. Now add the blocks. Walk `start` from `0` to `len(kept)` in steps of `BLOCK`
   with `range(0, len(kept), BLOCK)`, take `kept[start:start + BLOCK]` each
   time, and join the blocks with `"-"`.
4. Check the empty case by hand before the assert does: `clean_code("???")`
   must be `""`, not `"-"`.
5. Write `dropped_count`. It is one `sum` over a generator expression, and it
   must count characters in `raw`.
6. Write `is_donation` and `shelf_line`. `shelf_line` should call the other
   three and contain no cleaning logic of its own.
7. When `All checks passed.` prints, try `clean_code("a")` and
   `clean_code("abcd")` and `clean_code("abcde")` in a REPL. The three
   boundaries around a block of four are where an off-by-one would hide.

## The Solution

```python
"""exercise-01-seed-packet-codes-solution.py — tidy the seed library's codes.

Four small string functions: clean a handwritten packet code into blocks of
four, count what had to be thrown away, say whether the packet was donated,
and lay one shelf line out.

Nothing here changes a string, because nothing can. Every function builds a
new string and hands it back.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

BLOCK = 4

RAW_PACKETS: list[str] = [
    "don 4417 kale",
    "buy-2210-tomato",
    "  DON 0001  ",
    "???",
    "bee balm #7",
    "sage 12",
]


def clean_code(raw: str) -> str:
    """Return the tidy form of one handwritten packet code.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The kept letters and digits, upper-cased, in blocks of four joined
        by "-". An empty string when nothing survives.
    """
    kept = [ch.upper() for ch in raw if ch.isalnum()]
    blocks = ["".join(kept[start:start + BLOCK]) for start in range(0, len(kept), BLOCK)]
    return "-".join(blocks)


def dropped_count(raw: str) -> int:
    """Return how many characters the cleaner threw away.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The number of characters in `raw` that were not letters or digits.
    """
    return sum(1 for ch in raw if not ch.isalnum())


def is_donation(code: str) -> bool:
    """Return True when a cleaned code begins with the donation marker.

    Args:
        code: A cleaned code, as returned by `clean_code`.

    Returns:
        True when the code starts with "DON", otherwise False.
    """
    return code.startswith("DON")


def shelf_line(raw: str) -> str:
    """Return one line of the shelf listing for a raw code.

    Args:
        raw: The code exactly as the volunteer wrote it.

    Returns:
        The cleaned code padded to 16 characters, then "donated" or
        "bought", then how many characters were dropped.
    """
    code = clean_code(raw)
    shown = code if code else "(empty)"
    source = "donated" if is_donation(code) else "bought"
    return f"{shown:<16}  {source}  {dropped_count(raw)} dropped"


# ---- Self-check ----
if __name__ == "__main__":
    for raw in RAW_PACKETS:
        print(shelf_line(raw))

    assert clean_code("don 4417 kale") == "DON4-417K-ALE"
    assert clean_code("buy-2210-tomato") == "BUY2-210T-OMAT-O"
    assert clean_code("???") == ""
    assert clean_code("") == ""
    assert dropped_count("  DON 0001  ") == 5
    assert dropped_count("sage 12") == 1
    assert dropped_count("") == 0
    assert is_donation(clean_code("don 4417 kale"))
    assert not is_donation(clean_code("buy-2210-tomato"))
    assert RAW_PACKETS[0] == "don 4417 kale"  # the raw scans are untouched
    print("All checks passed.")
```

**The whole cleaner is three lines, and the middle one is the interesting
one.**

```python
kept = [ch.upper() for ch in raw if ch.isalnum()]
```

Read it right to left: *for each character in `raw`, if it is a letter or a
digit, upper-case it, and collect the results into a list.* One pass over the
input, one list out. `ch.upper()` on a single character still builds a new
one-character string — you cannot change the one you have — but it is one tiny
string per character, not one growing string per character. That distinction
is the entire lesson.

**The blocks come from a range with a step.** `range(0, len(kept), BLOCK)`
gives `0, 4, 8, …`, and `kept[start:start + BLOCK]` takes the four that begin
there. The last block is short whenever the code does not divide by four, and
you do not have to write a single line to handle that: a slice that runs off
the end simply stops. Compare `kept[12]` on a list of eleven, which raises
`IndexError`. **Slices clamp, indexes raise.** That sentence is worth
memorising now; it saves a guard in almost every string problem in this course.

**`"-".join(blocks)` puts the dashes *between*, never at the ends.** Which is
why the empty case works for free. No blocks means nothing to put a separator
between, so `"-".join([])` is `""`. The version people write by hand —
appending `block + "-"` each time and then chopping the last character off —
has to special-case the empty code, and usually does not.

**`dropped_count` counts `raw`, not the difference in lengths.** `sum(1 for ch
in raw if not ch.isalnum())` asks exactly the question the librarians asked:
how many characters did we throw away? The tempting `len(raw) - len(code)`
gives 0 for `"don 4417 kale"` — eleven characters kept plus two dashes added
equals the thirteen we started with — and the number looks plausible enough
that nobody checks it.

**`startswith` reads the front without copying it.** `code.startswith("DON")`
compares at most three characters and allocates nothing. It also cannot fall
over on a short code: `"AB".startswith("DON")` is just `False`, where
`"AB"[:3]` quietly gives you `"AB"` and the comparison still works but for a
reason you would have to think about.

**Nothing here changed `RAW_PACKETS`, and nothing could have.** The strings
inside it are immutable, so there is no operation any of these four functions
could have performed that would edit one. That is the promise immutability
buys: you can hand a string to a function you have never read and know it will
come back the same. Lists give you no such promise — the next two exercises
are both about who is allowed to change whose list.

## Download and run

Download
[exercise-01-seed-packet-codes-solution.py](./exercise-01-seed-packet-codes-solution.py)
and run it:

```bash
python exercise-01-seed-packet-codes-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-seed-packet-codes.py`.

## Common bugs to catch

- **`TypeError: 'str' object does not support item assignment`.** You tried to
  fix a character in place:

  ```text
  Traceback (most recent call last):
      code[0] = code[0].upper()
      ~~~~^^^
  TypeError: 'str' object does not support item assignment
  ```

  There is no in-place edit of a string, anywhere, ever. Build a list of the
  characters you want and join it. If you genuinely need to poke at characters
  one at a time, `chars = list(code)` gives you a list you *can* assign into,
  and `"".join(chars)` turns it back — that round trip is `O(n)` and is the
  standard move.

- **`AttributeError: 'list' object has no attribute 'join'`.** The join went on
  the wrong object:

  ```text
  Traceback (most recent call last):
      return blocks.join("-")
             ^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'join'
  ```

  `join` belongs to the separator: `"-".join(blocks)`. It reads backwards the
  first fifty times and then never again. The reason it is built this way is
  that the separator is always a string, while the thing being joined can be
  any sequence at all.

- **`TypeError: sequence item 0: expected str instance, int found`.** You put
  something that is not a string into the list you joined:

  ```text
  TypeError: sequence item 0: expected str instance, int found
  ```

  `join` will not guess how you want a number written. The message even tells
  you which item is at fault — item 0 here. Convert first: `str(value)`.

- **A stray dash on the empty code.** `clean_code("???")` returns `"-"` instead
  of `""`. You built the code by appending `block + "-"` and then removed the
  final dash with `[:-1]`. On an empty code there is no final dash to remove,
  so `[:-1]` of `""` is `""` — but if you wrote `[:-1]` on a string that was
  only a dash, you get `""` too, and the bug hides until a one-block code. Use
  `"-".join(...)` and the problem cannot occur.

- **`dropped_count` returns 0 for `"don 4417 kale"`.** You wrote `len(raw) -
  len(code)`. Two spaces came out and two dashes went in, so the lengths match
  and the answer is silently wrong. There is no exception to catch here, which
  is exactly why the assert names the number.

- **Everything is upper-case except the digits, and you wondered why.**
  `"4".upper()` is `"4"`. Digits have no case. This is not a bug, but people
  spend real minutes on it, so: it is fine.

## Under the hood

<details>
<summary>Under the hood — why `+=` in a loop is quadratic, and why it sometimes is not</summary>

**The arithmetic.**

Building an `n`-character string with `out += ch` copies the whole accumulated
string on every pass. Pass 1 copies 1 character, pass 2 copies 2, and so on:

```text
1 + 2 + 3 + … + n  =  n(n + 1) / 2
```

which is `O(n²)`. The list-then-join version copies each character once into
the list and once into the final string: `2n`, which is `O(n)`. Homework 1
makes you count both numbers exactly rather than take this on trust.

**What `join` actually does.** It walks the sequence once to add up the total
length, allocates a string of exactly that size, and copies each piece in.
**One** allocation. That is why it is the fastest way to build a string in
Python and why it will still be the fastest way in ten years — the algorithm
has no slack left in it.

**The optimisation that muddies the water.** CPython contains a special case:
when the string on the left of a `+=` has a reference count of exactly 1 —
nobody else is holding it — the interpreter may resize it in place instead of
copying. When that fires, the naive loop behaves linearly and your measurement
disagrees with the theory.

It is real, and you should not lean on it. It vanishes the moment a second
name, a list, or a debugger holds a reference to that string. It is absent from
other Python implementations. And in an interview, "it's O(n²), though CPython
can sometimes resize in place" is the answer that shows you know both the
contract and the implementation. Leading with the optimisation sounds like
dodging.

**One more thing immutability buys.** Because a string can never change, its
hash can be computed once and remembered. That is what lets a string be a dict
key — Lecture 3's rule that a key must be "immutable all the way down" starts
right here.

</details>

## Acceptance checklist

- [ ] `python exercise-01-seed-packet-codes.py` prints six rows then `All checks passed.`
- [ ] The six rows match the expected output character for character.
- [ ] `clean_code` contains no `+=` on a string.
- [ ] `clean_code("")` and `clean_code("???")` both return `""`.
- [ ] `is_donation` uses `startswith` and no slice.
- [ ] `dropped_count` looks only at `raw`.
- [ ] Every function has type hints and a docstring.
- [ ] You can say, in one sentence, why the list-then-join version is linear.

## Stretch

- **Make the block size a parameter, and find out what happens at the edges.**

  ```python
  def clean_code_blocks(raw: str, block: int = 4) -> str:
      """Return the tidy code in blocks of `block` characters."""
      kept = [ch.upper() for ch in raw if ch.isalnum()]
      return "-".join("".join(kept[start:start + block]) for start in range(0, len(kept), block))
  ```

  ```text
  block 2 : DO-N4-41-7K-AL-E
  block 4 : DON4-417K-ALE
  block 99: DON4417KALE
  ```

  A block bigger than the code gives you one block, with no special case, for
  the same reason the empty code needed none. Try `block=0` as well and read
  the `ValueError` that `range` raises — a step of zero is the one input this
  shape genuinely cannot survive.

- **Count what was dropped, by kind.**

  ```python
  from collections import Counter

  def dropped_kinds(raw: str) -> dict[str, int]:
      """Return how many spaces, punctuation marks and others were dropped."""
      kinds = Counter("space" if ch.isspace() else "other" for ch in raw if not ch.isalnum())
      return dict(kinds)
  ```

  ```text
  '  DON 0001  ' -> {'space': 5}
  'buy-2210-tomato' -> {'other': 2}
  'bee balm #7' -> {'space': 2, 'other': 1}
  ```

  `Counter` is Lecture 3's tool and you have not met it properly yet. Use it
  here anyway and notice how little code it took; Exercise 4 explains what it
  is doing.

- **Prove the immutability claim to yourself.**

  ```python
  code = "DON4"
  before = id(code)
  code += "-417K"
  print(before == id(code))
  ```

  ```text
  False
  ```

  `id()` is the object's address. A different address means a different object:
  the `+=` did not change `"DON4"`, it built something new and pointed `code`
  at it. Run the same experiment on a list with `append` and watch the address
  stay put. That difference is the whole of the next two exercises.

When your labels are right, move on to
[Exercise 2 — The Cable Ferry's Waiting Lane](./exercise-02-cable-ferry-lane.md).
