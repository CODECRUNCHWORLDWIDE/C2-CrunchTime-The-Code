# Exercise 2 — The Mirror Serial

> **Topic:** converging pointers that move unevenly, skipping characters that do not count, while keeping the original positions straight
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Easy/Medium
> **Target time:** 50 minutes, including a full FRAME narration out loud
> **Why this one:** same converging shape as Exercise 1, but the two pointers no longer move in lockstep — one side can skip several positions while the other stands still. That is where most people write their first off-by-one. It is also the first page where the *easy* solution gives a wrong answer rather than a slow one, because filtering the string first throws away the very positions the caller asked for.

## The Brief

A ferry terminal prints boarding serials on a small thermal printer. Every
serial is supposed to be a **mirror serial**: throw away the separators the
printer sprinkles in so people can read it aloud, ignore capital letters, and
what is left reads the same forwards and backwards.

Two words, defined before we use them.

**Significant characters** are the ones that carry meaning: ASCII letters and
digits. Everything else — hyphens, spaces, whatever punctuation the printer
emits — is a separator and means nothing. So in `RT7-e77-E7tr` the
significant characters are `R T 7 e 7 7 E 7 t r`, and the two hyphens are
scenery.

**Case never matters.** `E` and `e` are the same character. Digits have no
case at all, so `7` only ever matches `7`.

When the print head starts to drift, a serial stops mirroring. The terminal's
quality check does not want a yes-or-no answer, because a yes-or-no tells the
technician nothing useful. It wants **the position on the printed ticket
where the mirror first breaks.**

Here is exactly what that means. Run the check from both ends toward the
middle. The first time a pair of significant characters disagrees, report the
index of the **left** one, counted **in the original printed string** —
separators included in the count, because that is the physical spot on the
ticket the technician has to go and look at.

If the serial mirrors, return `None`. A serial with no significant characters
at all mirrors vacuously — there is nothing in it that could disagree.

```python
def first_mirror_break(serial: str) -> int | None:
    """Return the printed index where the serial first stops mirroring."""
```

Why `None` and not `-1`? Because `0` is a perfectly good answer — a serial
can break at its very first character. A caller writing `if result:` would
read `0` as "no break", and a caller writing `if result >= 0:` would have to
know about the sentinel. `None` is the one value that cannot be confused with
a real position.

## Starter

Save this as `exercise-02-mirror-serial.py` and fill in the `TODO`s.

```python
"""exercise-02-mirror-serial.py — where a boarding serial stops mirroring.

Two pointers walk in from the ends of the printed serial, stepping over the
separators the printer sprinkles in. The first pair of significant characters
that disagrees hands back the printed index of its left member.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def first_mirror_break(serial: str) -> int | None:
    """Find where a printed serial first stops reading the same both ways.

    Args:
        serial: The serial exactly as printed, separators included.

    Returns:
        The index in `serial` of the left character of the first outside-in
        pair of significant characters that fails to mirror, or None when
        the serial mirrors — including when it holds no significant
        characters at all.
    """
    # TODO: put one pointer at each end of the printed string
    # TODO: before each comparison, walk the left pointer forward past any
    #       separator and the right pointer backward past any separator —
    #       and guard both of those inner loops so they cannot run off
    # TODO: compare the two characters with case folded away; on a
    #       disagreement return the LEFT pointer, which is a printed index
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(first_mirror_break("RT7-e77-E8tr"), first_mirror_break("--G9"))

    assert first_mirror_break("RT7-e77-E7tr") is None
    assert first_mirror_break("8a-b-c8") == 1
    assert first_mirror_break("--  --") is None
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/exercise-02-mirror-serial.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `first_mirror_break` returns an `int` index into the **original printed
   string**, or `None`.
2. The index returned is the **left** member of the first disagreeing pair,
   scanning from the outside in.
3. Separators are skipped, never compared. Significant means
   `str.isalnum()` — ASCII letters and digits.
4. The comparison ignores case. `Bb` mirrors.
5. A mirroring serial returns `None`. So does a serial with no significant
   characters, and so does the empty string.
6. The function uses `O(1)` auxiliary space — two integers. No filtered copy
   of the serial, no reversed copy.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(serial) <= 1_000_000`.** A million characters is far longer
  than any ticket, and that is the point. The shortcut solution builds a
  filtered copy of the significant characters and then compares it against a
  reversed copy — two more strings of nearly a million characters each. At
  this bound that cost is something you can actually measure on a terminal
  that has other work to do, so `O(1)` auxiliary space is the graded
  requirement rather than a preference.

- **`serial` holds printable ASCII only.** Restricting to ASCII keeps
  "significant" unambiguous. With arbitrary Unicode, whether a character
  counts as a letter or a digit becomes a judgement call — `str.isalnum()`
  answers `True` for Roman numerals, circled digits and a great many scripts
  — and this exercise is about pointer bookkeeping, not about Unicode
  categories.

- **Significant characters are ASCII letters and digits; comparison folds
  case.** Digits have no case, so `'7'` compares only against `'7'`. Fixing
  the rule this precisely matters because "ignore case" and "ignore
  everything that is not a letter" are two different rules and a solution
  that conflates them passes the easy examples.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-02-mirror-serial.py
  'RT7-e77-E7tr'  mirrors
  'RT7-e77-E8tr'  breaks at index 2
       '8a-b-c8'  breaks at index 1
          '--G9'  breaks at index 2
            'Bb'  mirrors
           '-K-'  mirrors
        '--  --'  mirrors
              ''  mirrors
All checks passed.
```

Four of these lines are worth stopping on.

`'RT7-e77-E7tr'` mirrors even though its ten significant characters are
spread across twelve printed positions. Trace it and watch the two pointers
sit on *different* printed positions while staying perfectly in step on the
significant sequence.

`'RT7-e77-E8tr'` is the same serial with one digit drifted, and it breaks at
printed index `2`. That is the `7`, not the `8`. The contract says the left
member of the pair.

`'8a-b-c8'` breaks at index `1`. Not `0` — the two `8`s at the ends agree
first. Not `5` — that is the `c`, the right member of the pair. This example
separates "I return the left index" from "I return whichever index happened
to be in a variable."

`'--G9'` breaks at index `2`, and this is the example that punishes building
a filtered string. In the filtered string `g9` the break is at position `0`,
and `0` is the wrong answer. Once you have thrown the separators away you
have thrown away the mapping back to the ticket, and no amount of care later
recovers it.

## Steps

1. Save the starter and run it. `AssertionError`, as expected.
2. Put `left` at `0` and `right` at `len(serial) - 1`. Write the outer loop as
   `while left < right`.
3. Write the two skip loops *inside* the outer loop, before any comparison.
   The left one walks forward while the character is not significant; the
   right one walks backward. **Write the guard as you write the loop**, not
   afterwards: each skip loop needs `left < right and ...` in its condition,
   or on a ticket made entirely of separators it walks straight off the end
   of the string.
4. Compare `serial[left].lower()` against `serial[right].lower()`. On a
   disagreement, `return left`.
5. Otherwise step both pointers inward and go round again.
6. After the loop, `return None`.
7. Run it. Then trace `"--  --"` and `""` by hand and confirm you understand
   *which* guard saves each of them.

## The Solution

```python
"""exercise-02-mirror-serial-solution.py — where a boarding serial stops mirroring.

Two pointers walk in from the ends of the printed serial, stepping over the
separators the printer sprinkles in. The first pair of significant characters
that disagrees hands back the printed index of its left member.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def first_mirror_break(serial: str) -> int | None:
    """Find where a printed serial first stops reading the same both ways.

    Args:
        serial: The serial exactly as printed, separators included.

    Returns:
        The index in `serial` of the left character of the first outside-in
        pair of significant characters that fails to mirror, or None when
        the serial mirrors — including when it holds no significant
        characters at all.
    """
    left, right = 0, len(serial) - 1
    while left < right:
        while left < right and not serial[left].isalnum():
            left += 1
        while left < right and not serial[right].isalnum():
            right -= 1
        if serial[left].lower() != serial[right].lower():
            return left
        left += 1
        right -= 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    tickets = [
        "RT7-e77-E7tr",
        "RT7-e77-E8tr",
        "8a-b-c8",
        "--G9",
        "Bb",
        "-K-",
        "--  --",
        "",
    ]
    for ticket in tickets:
        where = first_mirror_break(ticket)
        shown = "mirrors" if where is None else f"breaks at index {where}"
        print(f"{ticket!r:>16}  {shown}")

    assert first_mirror_break("RT7-e77-E7tr") is None
    assert first_mirror_break("RT7-e77-E8tr") == 2
    assert first_mirror_break("8a-b-c8") == 1
    assert first_mirror_break("--G9") == 2
    assert first_mirror_break("Bb") is None
    assert first_mirror_break("-K-") is None
    assert first_mirror_break("--  --") is None
    assert first_mirror_break("") is None
    print("All checks passed.")
```

**The pointers never leave the printed string, and that is the whole design.**
`left` and `right` are indexes into `serial` itself, so when the comparison
fails, `left` already *is* the answer. Nothing has to be translated back.
Compare that with the filter-first approach, where you would have to build a
second list mapping each filtered position to its printed position — which is
another million-entry structure, for a problem that needed two integers.

**Skip first, compare second.** The two inner loops run before the
comparison, every time round. Reverse that order and a separator gets
compared against a letter, so every ticket with a hyphen in it "breaks"
immediately. The order is not a style choice; it is the algorithm.

**Both inner loops need `left < right` in their condition.** On `"--  --"`
there is nothing significant anywhere, so the left skip loop would keep
walking until it stepped past the last character and raised. The guard stops
it the moment it reaches the other pointer. Note what happens next: the two
pointers are now equal, so the comparison compares a character with itself,
which agrees, and then the outer loop ends. Vacuously a mirror, exactly as
the contract says, and it falls out of the guard rather than needing a
special case.

**`.lower()` on both sides, not on one.** Folding case means both characters
must be folded. Uppercasing both would work equally well; what does not work
is folding one side and hoping. Digits are unaffected — `'7'.lower()` is
`'7'` — so there is no need to branch on character type.

**The outer condition is `<`, not `<=`.** When the pointers land on the same
character the answer is already decided: a character always mirrors itself.
Running that iteration costs one comparison and tells you nothing. This is
the same reasoning as Exercise 1's swap count, one step gentler, because
here the extra iteration is merely wasted rather than wrong.

**Every printed position is visited at most twice.** The left pointer only
ever moves forward and the right pointer only ever moves backward, and they
stop when they meet. So the total number of character reads is bounded by the
length of the ticket, whatever the mix of separators — `O(n)` time, and the
skip loops do not turn it into anything worse even though they are nested
inside the outer loop. Being able to say *why* nested loops are still linear
here is worth more in an interview than the code is.

## Run it

Copy the worked answer on this page into `exercise-02-mirror-serial.py` and run it:

```bash
python exercise-02-mirror-serial.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-02-mirror-serial.py`.

## Common bugs to catch

- **`IndexError: string index out of range` on a ticket of separators.** You
  wrote the skip loop without its guard:

  ```text
  Traceback (most recent call last):
      first_mirror_break("--  --")
      while not serial[left].isalnum():
                ~~~~~~^^^^^^
  IndexError: string index out of range
  ```

  Nothing in `"--  --"` is significant, so the loop keeps stepping until
  `left` is `6` and there is no character there. The fix is
  `while left < right and not serial[left].isalnum():` — and the same guard
  on the right-hand loop, for the ticket where the *right* pointer is the one
  that runs out first.

- **A bare `AssertionError` on `"--G9"`.** You filtered the serial first and
  returned the position in the filtered string:

  ```text
  Traceback (most recent call last):
      assert first_mirror_break("--G9") == 2
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Your function returned `0`, because in `g9` the break really is at position
  `0`. The arithmetic is right and the answer is wrong, which is the worst
  combination there is. The moment you build a filtered copy you lose the
  mapping back to the ticket, and the technician cannot find the character
  you are talking about.

- **A bare `AssertionError` on `"Bb"`.** You compared the raw characters:

  ```text
  Traceback (most recent call last):
      assert first_mirror_break("Bb") is None
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `'B' != 'b'`, so your function reported a break at index `0`. Fold case on
  both sides. Pick `.lower()` or `.upper()` — it does not matter which, as
  long as you apply the same one to both characters.

- **Returning `-1` for "no break".** No exception, and the tests on this page
  would catch it — but in real code it is the bug that bites six months
  later, because index `0` is a legal answer and a caller writing
  `if result:` cannot tell `0` from "fine". This is precisely why the
  contract names `None`.

- **Returning the right index.** On `"8a-b-c8"` the answer is `1`, not `5`.
  Both are indexes of a character in the disagreeing pair, so both look
  plausible in a trace. Read the contract: the left one.

- **Comparing before skipping.** No exception, and almost every real ticket
  reports a break at index `0` or `1`. If your function says every serial is
  broken, check the order of your three operations before you check anything
  else.

- **`while left <= right` on the outer loop.** Harmless in the sense that a
  character mirrors itself, so the answer stays correct. It costs one extra
  iteration and it signals that you did not think about why `<` suffices. Say
  the reason out loud rather than shrugging at it.

## Under the hood

<details>
<summary>Under the hood — why two nested loops are still O(n), and what isalnum really tests</summary>

**The nested loops do not multiply.**

The instinct that a loop inside a loop is `O(n²)` is a good instinct, and here
it is wrong. The reason is that the inner loops do not restart from scratch —
they resume from wherever the pointer already stood.

Count it by charging the work to the pointers rather than to the loops. `left`
starts at `0`, only ever increases, and stops when it reaches `right`. So over
the entire run of the function, `left` advances at most `n` times in total,
across every inner and outer step put together. The same argument applies to
`right`, downward. Total pointer movement is at most `n`, so the total number
of character reads is at most about `2n`, so the function is `O(n)`.

This accounting trick — charge the work to a quantity that only moves one way
— is called an **amortised** argument, and it is how nearly every two-pointer
and sliding-window complexity claim is actually justified. You will use it
again in Week 3, where the window's two edges both crawl forward and the
naive reading suggests `O(n²)` there too.

**What `isalnum()` really answers.**

`str.isalnum()` is `True` when every character in the string is alphanumeric
by Unicode's definition, which is broader than "ASCII letter or digit". It
accepts `'²'`, `'Ⅷ'`, `'৩'` and a great deal else. Our constraint says the
ticket is printable ASCII, so inside this exercise the two definitions
coincide — but the constraint is what makes that true, not the method.

If you ever need the strict version, spell it out:

```python
def is_significant(character: str) -> bool:
    """True for ASCII letters and digits only."""
    return character.isascii() and character.isalnum()
```

**Case folding is harder than `.lower()` in general.**

For ASCII, `.lower()` is exactly right. For real Unicode it is not: the German
`ß` lowercases to itself but case-folds to `ss`, and comparing user-supplied
text properly wants `str.casefold()` rather than `str.lower()`. Knowing that
the distinction exists, and that our ASCII constraint is what lets us ignore
it, is the kind of thing that separates "I used the method I remembered" from
"I chose the method that fits the input."

**The `O(n)` floor.**

You cannot do better than reading the whole ticket in the worst case, because
a break can sit at the exact middle. The two pointers have to travel from both
ends to meet there, and that is `n` character reads however you arrange it. So
`O(n)` is not merely what this solution costs — it is the best any correct
solution can do.

</details>

## Acceptance checklist

- [ ] `python exercise-02-mirror-serial.py` prints `2 2` on the first line, then `All checks passed.`
- [ ] The value returned is an index into the **original** string, and you can point at the line that makes that true.
- [ ] Both skip loops carry a `left < right` guard, written at the same time as the loop.
- [ ] `"--  --"` and `""` return `None` without raising.
- [ ] `None`, not `-1`, is returned for "no break", and you can say in one sentence why that matters when `0` is a legal answer.
- [ ] No filtered or reversed copy of the serial exists anywhere in your solution.
- [ ] The function has type hints and a docstring.
- [ ] You narrated a full FRAME pass out loud with a recorder running, at least ten minutes.
- [ ] Committed to Git with a message like `Add Week 1 exercise 2: mirror serial`.
## Stretch

- **Report every break, not just the first.** The technician wants to know
  whether the head drifted once or is failing across the whole ticket.

  ```python
  def all_mirror_breaks(serial: str) -> list[int]:
      """Return the printed index of the left member of every disagreeing pair."""
      breaks: list[int] = []
      left, right = 0, len(serial) - 1
      while left < right:
          while left < right and not serial[left].isalnum():
              left += 1
          while left < right and not serial[right].isalnum():
              right -= 1
          if serial[left].lower() != serial[right].lower():
              breaks.append(left)
          left += 1
          right -= 1
      return breaks
  ```

  ```text
  '8a-b-c9' -> [0, 1]
  'RT7-e88-E9tr' -> [2]
  'RT7-e77-E7tr' -> []
  ```

  The middle line is worth a second look. `RT7-e88-E9tr` has two drifted
  characters in it and still reports only one break, because the second
  drifted pair turns out to agree once the pointers reach it. "Two characters
  wrong" and "two breaks" are not the same claim.

  Note the return type changed from `int | None` to `list[int]`, and that an
  empty list is now the honest "no breaks" value — because unlike `0`, an
  empty list is not a legal non-empty answer. Argue that choice in your
  write-up rather than copying it.

- **Report the pair, not just the left index.** Return
  `(left_index, right_index)` so the technician can look at both characters.
  Decide what a mirroring serial returns now, and notice that the reasoning
  about `None` versus a sentinel starts over from scratch with the new type.

- **Count significant characters without building anything.** Write a version
  that also returns how many significant characters the ticket held, still in
  `O(1)` space. The trap is that the two pointers stop in the middle, so
  neither of them has seen the whole ticket — work out what that means for
  your count before you write it.

When your ticket check is right, move on to
[Exercise 3 — The Widest Ballast Pair](./exercise-03-widest-ballast-pair.md).
