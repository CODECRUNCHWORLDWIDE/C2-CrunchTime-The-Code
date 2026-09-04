# Problem 5 — System-Design Warm-Up

> **Topic:** sketching a URL shortener before anybody has told you the answer, and building the one piece of it that fits in forty minutes
> **Lecture:** [01 — What Interviewers Actually Score](../lecture-notes/01-what-interviewers-actually-score.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** real system design is Week 12. This is a warm-up, and its value comes entirely from doing it *before* you read anybody's canonical answer — because the gap between what you said and what the article says is a map of what you do not yet know, and you only get to draw that map once per problem.

## The Brief

Two halves. Do them in this order and do not swap them.

**Half one, and it is the important one.** Write a 300-word answer to:
*"How would you sketch a system that shortens long URLs into short ones, the
way bit.ly does?"* Write what you would actually say in an interview today,
with what you know today. **Do not look up the canonical answer first.**

Then, and only then, search for "URL shortener system design", read one free
article, and note three things you would add next time. Those three notes are
worth more than the essay.

**Half two.** Build the piece of that system you can actually finish in forty
minutes: turning a row number into a short code and back again.

Here is the idea, and it is simpler than people expect. When somebody submits
a long URL, you store it in a table and the database hands you a row number —
1, then 2, then 3, and so on forever. That number is already unique, because
the database made it that way. So the short code does not need to be random,
and it does not need to be hashed. It just needs to be that number, written
down in a way that is short.

Ordinary numbers are written in **base ten**: ten digits, `0` through `9`, and
each place is worth ten times the one to its right. Write the same number with
**sixty-two** digits — `0-9`, then `A-Z`, then `a-z` — and each place is worth
sixty-two times the one to its right, so it takes far fewer places. Row
916,132,831 is nine digits in base ten and five characters in base 62.

Two functions:

- `encode(row)` turns a row number into its short code.
- `decode(code)` turns a short code back into its row number.

They are exact inverses, which means no two rows can ever produce the same
code — and *that* is the property worth being able to state out loud, because
"how do you avoid collisions?" is the first question anybody asks about a URL
shortener.

## Starter

Save this as `problem-05-system-design-warmup.py` and fill in the `TODO`s.

```python
"""problem-05-system-design-warmup.py — the short code inside a URL shortener.

Base 62 is ordinary place-value arithmetic with sixty-two digits instead of
ten. Nothing here is random and nothing is hashed.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode(row: int) -> str:
    """Turn a row number into its base-62 short code."""
    # TODO: a negative row is not a row — raise ValueError
    # TODO: row 0 is the case the loop below cannot produce. Handle it first.
    # TODO: repeatedly divmod by BASE, collecting ALPHABET[remainder]
    # TODO: the digits come out least-significant first, so reverse them
    ...


def decode(code: str) -> int:
    """Turn a short code back into its row number."""
    # TODO: an empty code is not a code — raise ValueError
    # TODO: walk the characters left to right, row = row * BASE + position
    # TODO: a character that is not a base-62 digit must raise, not resolve
    #       to somebody else's link
    ...


def codes_available(length: int) -> int:
    """How many distinct codes exist at exactly this many characters."""
    # TODO: one line
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(encode(62), decode("10"), codes_available(5))

    assert encode(0) == "0"
    assert encode(61) == "z"
    assert all(decode(encode(row)) == row for row in range(5000))
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-05-system-design-warmup.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `system-design/notes-week-01.md` exists in your portfolio repo, holding a
   300-word answer written **before** you read anything, and three things you
   would add afterwards.
2. `encode(0)` returns `"0"`.
3. `decode(encode(row)) == row` for every row you try.
4. Two different rows never produce the same code.
5. `encode` raises `ValueError` on a negative row.
6. `decode` raises `ValueError` on an empty code and on a character that is
   not in the alphabet.
7. `codes_available(length)` returns `62 ** length`.
8. Every function keeps its type hints and its docstring.

## Constraints

- **The alphabet is `0-9A-Za-z`, in that order, and the order is part of the
  contract.** Change the order and every existing short code in your database
  points at a different row. This is the sort of constant that looks like a
  detail on the day you write it and is unchangeable six months later, which
  is worth noticing now: some constants are configuration and some are
  permanent, and the difference is whether anything has been published against
  them.

- **Row numbers start at `0` and there is nothing before them.** A negative
  row cannot be encoded, so `encode` raises rather than producing something.
  Returning `""` or `"-1"` for a bad input would push the problem into the
  caller, who will not check.

- **A bad code raises rather than resolving.** This is a security constraint,
  not a tidiness one. If `decode` quietly skipped characters it did not
  recognise, then `ab-c` and `abc` would resolve to the same row — so a typo,
  or a deliberately mangled link, would silently take a visitor to somebody
  else's URL. Reject what you do not understand.

- **No randomness and no hashing.** A random code needs a collision check
  against the database on every insert, and a hash of the URL needs one too
  because hashes collide. The reversible encoding needs neither, because the
  database already guaranteed the row number was unique. **Reuse a guarantee
  you already have rather than manufacturing a new one** — that is the design
  idea on this page, and it is worth more than the arithmetic.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python problem-05-system-design-warmup.py
row           0  ->  0        ->  row 0
row           1  ->  1        ->  row 1
row          61  ->  z        ->  row 61
row          62  ->  10       ->  row 62
row        3843  ->  zz       ->  row 3843
row        3844  ->  100      ->  row 3844
row   916132831  ->  zzzzz    ->  row 916132831
row   916132832  ->  100000   ->  row 916132832

1 characters covers             62 links
2 characters covers          3,844 links
3 characters covers        238,328 links
4 characters covers     14,776,336 links
5 characters covers    916,132,832 links
6 characters covers 56,800,235,584 links
7 characters covers 3,521,614,606,208 links

All checks passed.
```

The rows were chosen in pairs, and each pair is a place-value rollover. `61`
is the last one-character code and `62` is the first two-character one, the
same way `9` and `10` work in base ten. `3843` and `3844` do it again at two
characters, and `916132831` and `916132832` at five.

The table underneath is the number that matters in an interview. **Five
characters covers nine hundred million links.** That is a real answer to "how
long should the codes be?", arrived at by arithmetic rather than by guessing —
and being able to produce it in the room, out loud, is the difference between
a warm-up answer and a good one. Six characters covers fifty-six billion,
which is more links than anybody has ever shortened.

## Steps

1. **Write the essay first.** Set a timer for twenty minutes, close every
   other tab, and write 300 words on what you would say today. Save it to
   `system-design/notes-week-01.md`.
2. Save the starter and run it. `AssertionError`.
3. Write `encode`. Guard the negative case, then the zero case, then the
   loop. `divmod(row, BASE)` gives you the new row and the digit in one call.
4. Reverse the digits before joining them. They come out least-significant
   first, which is backwards.
5. Write `decode`. `row = row * BASE + position`, left to right. Use
   `ALPHABET.find(character)`, which returns `-1` for a character it cannot
   find, and raise on that.
6. Write `codes_available`. One line.
7. Run it. The round-trip assertion over five thousand rows is the one that
   proves the two functions are really inverses.
8. **Now** search "URL shortener system design", read one free article, and
   add three things to your notes that you did not think of. Be specific —
   "caching" is not a note; "cache the hot codes in memory, because reads
   outnumber writes by a hundred to one" is.

## The Solution

```python
"""problem-05-system-design-warmup-solution.py — the short code inside a URL shortener.

The design sketch is the written half of this problem. This is the one piece
of it you can actually build in forty minutes: turning a row number into a
short code, and turning it back again.

Base 62 is ordinary place-value arithmetic with sixty-two digits instead of
ten. Nothing here is random, nothing is hashed, and no two row numbers can
collide, because the conversion is reversible.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode(row: int) -> str:
    """Turn a row number into its base-62 short code.

    Args:
        row: The row's number in the links table. Zero or more.

    Returns:
        The short code, shortest first digit first. Row 0 encodes to "0".

    Raises:
        ValueError: If `row` is negative. There is no row before the first.
    """
    if row < 0:
        raise ValueError(f"row numbers start at 0, got {row}")
    if row == 0:
        return ALPHABET[0]

    digits: list[str] = []
    while row > 0:
        row, remainder = divmod(row, BASE)
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(code: str) -> int:
    """Turn a short code back into its row number.

    Args:
        code: A short code produced by `encode`.

    Returns:
        The row number it came from.

    Raises:
        ValueError: If the code is empty or holds a character that is not in
            the alphabet. A typo must fail loudly rather than resolve to
            somebody else's link.
    """
    if not code:
        raise ValueError("a short code cannot be empty")

    row = 0
    for character in code:
        position = ALPHABET.find(character)
        if position < 0:
            raise ValueError(f"{character!r} is not a base-62 digit")
        row = row * BASE + position
    return row


def codes_available(length: int) -> int:
    """How many distinct codes exist at exactly this many characters.

    Args:
        length: The code length in characters. Zero or more.

    Returns:
        62 to the power of `length`, which is the count of codes of that
        length or shorter, including the leading-zero forms.
    """
    return BASE**length


# ---- Self-check ----
if __name__ == "__main__":
    for row in [0, 1, 61, 62, 3843, 3844, 916_132_831, 916_132_832]:
        code = encode(row)
        print(f"row {row:>11}  ->  {code:<7}  ->  row {decode(code)}")

    print()
    for length in range(1, 8):
        print(f"{length} characters covers {codes_available(length):>14,} links")

    assert encode(0) == "0"
    assert encode(1) == "1"
    assert encode(61) == "z"
    assert encode(62) == "10"
    assert decode("0") == 0
    assert decode("z") == 61
    assert decode("10") == 62
    assert all(decode(encode(row)) == row for row in range(5000))
    assert len({encode(row) for row in range(5000)}) == 5000

    try:
        encode(-1)
    except ValueError as error:
        assert "start at 0" in str(error)
    else:
        raise AssertionError("encode(-1) should have raised")

    try:
        decode("hello world")
    except ValueError as error:
        assert "not a base-62 digit" in str(error)
    else:
        raise AssertionError("decode of a bad code should have raised")

    try:
        decode("")
    except ValueError:
        pass
    else:
        raise AssertionError("decode of an empty code should have raised")

    print()
    print("All checks passed.")
```

**Row 0 is the case the loop cannot produce, and every base conversion has
one.** `while row > 0` never runs when `row` is already `0`, so `digits` stays
empty and you get back `""`. An empty short code is not a short code. The
special case is one line and it is not a wart — it is the base case of the
conversion, the same way `0` needs the digit `0` in base ten.

**The digits come out backwards, so they get reversed.** `divmod` peels off
the *least* significant digit first, because that is the one the remainder
tells you about. Collect them in a list, reverse at the end. Forget the
reversal and `encode(62)` gives `"01"` and `encode(3844)` gives `"001"` — note
that both are still round-trippable if `decode` is reversed to match, so a
consistent pair of backwards functions would pass a naive round-trip test.
It would produce codes with leading zeros for no reason, and it would not
match anybody else's base-62. The round-trip test alone is not enough; you
need at least one assertion about a specific expected code.

**`decode` is Horner's method, whether or not you knew the name.**
`row = row * BASE + position`, once per character, left to right. It reads a
number the way you read one aloud: "sixty-two, then two more places." No
powers, no exponentiation, one multiply and one add per character. Compare the
version that computes `position * BASE ** exponent` and tracks an exponent —
same answer, more arithmetic, more to get wrong.

**`.find()` rather than `.index()`.** They do the same lookup; `find` returns
`-1` for a miss and `index` raises `ValueError: substring not found`. The
`index` version raises the *right kind* of error with a message that tells the
caller nothing about short codes. Catching it and re-raising works, and
checking `-1` is shorter and clearer. Either way, the thing that matters is
that a bad character never quietly becomes a valid row.

**Both errors carry the offending value.** `f"row numbers start at 0, got {row}"`
and `f"{character!r} is not a base-62 digit"` tell whoever reads the log which
input caused the problem. The `!r` on the character means a space shows up as
`' '` rather than as an invisible gap — worth remembering, because
whitespace-in-input bugs are otherwise very hard to see in a log.

**The two assertions at the end prove two different things.**
`decode(encode(row)) == row` for five thousand rows proves the functions are
inverses. `len({encode(row) for row in range(5000)}) == 5000` proves no two
rows share a code. The second follows from the first mathematically — an
invertible function cannot collide — and it is worth asserting anyway, because
"no collisions" is the claim you will be asked to defend and a test that
states it directly is a test somebody can read.

## Run it

Copy the worked answer on this page into `problem-05-system-design-warmup.py` and run it:

```bash
python problem-05-system-design-warmup.py
```

## Common bugs to catch

- **A bare `AssertionError` on `encode(0)`.** You wrote the loop without the
  zero case:

  ```text
      encode(0) -> ''
  ```

  ```text
  Traceback (most recent call last):
      assert encode(0) == "0"
             ^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `while row > 0` never ran, so the digit list is empty and `"".join([])` is
  the empty string. Every base conversion needs this case and it is always the
  first row in the table.

- **A bare `AssertionError` on `encode(62)`.** You forgot to reverse:

  ```text
      encode(62) -> '01'  encode(3844) -> '001'
  ```

  ```text
  Traceback (most recent call last):
      assert encode(62) == "10"
             ^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Leading zeros are the tell. If your codes start with `0` far more often than
  one time in sixty-two, the digits are the wrong way round.

- **`ValueError: substring not found` from a mistyped code.**

  ```text
  Traceback (most recent call last):
      decode("hello world")
      row = row * 62 + ALPHABET.index(c)
                       ~~~~~~~~~~~~~~^^^
  ValueError: substring not found
  ```

  Right exception, useless message — nothing in it says "short code" or names
  the character. Use `.find()` and raise your own, or catch this and re-raise
  with the detail.

- **Skipping unknown characters instead of raising.** No exception at all, and
  this is the dangerous one: `ab-c` and `abc` resolve to the same row, so a
  mangled link silently redirects a visitor to somebody else's URL. Rejecting
  input you do not understand is not pedantry.

- **`while row >= 0`.** Infinite loop. `divmod(0, 62)` is `(0, 0)`, so the row
  never changes and the digit list grows forever until the process is killed.
  The condition is `> 0`.

- **A round-trip test that passes on backwards code.** If `encode` reverses
  and `decode` reads right-to-left, every round trip works and every code is
  wrong. This is why the assertions name specific expected codes as well as
  testing the round trip. A test that only checks a function against its own
  inverse cannot detect an error they both share.

## Under the hood

<details>
<summary>Under the hood — the rest of the system, and why the row number is the right key</summary>

**What the other 95% of the design is.**

The encoder is one afternoon's work. The interview question is about the rest,
and the rest is roughly this:

*Write path.* A long URL arrives. Insert it into a table, get the row number
back, encode it, return the short code. One database write, no lookups, no
collision check.

*Read path.* A short code arrives. Decode it to a row number, look up the row,
redirect. One database read — and reads outnumber writes by something like a
hundred to one on a real shortener, which is what makes caching the obvious
first optimisation.

*The redirect itself.* `301` is permanent and browsers cache it, so you stop
seeing the traffic and your click analytics die. `302` is temporary and every
click comes back to you. Almost every real shortener uses `302` for exactly
that reason, and noticing the trade is a genuinely good thing to say out loud.

*Scaling the writes.* One database handing out row numbers is a single point
of contention. The standard fix is to give each server a *block* of numbers —
"you own 1,000,000 to 1,999,999" — so it can hand out codes without talking to
anybody. Codes stop being sequential, which is fine, and the uniqueness
guarantee survives because the blocks do not overlap.

*Custom codes and expiry.* Both are database columns, not encoder changes.
Worth saying, because it demonstrates you can tell which requirements disturb
the core design and which do not — the same judgement Challenge 2 tests with
its camber cap.

**Why not hash the URL?**

It is the first instinct and it has two problems. Hashes collide, so you need
a collision check on every insert, which is the database round-trip you were
trying to avoid. And the same URL always hashes to the same code, so two
different people shortening the same link cannot have separate analytics, and
nobody can ever shorten a URL twice on purpose.

The row number has neither problem, because uniqueness was somebody else's job
and they already did it.

**Why not random?**

Random codes are genuinely used, and for one good reason: sequential codes are
*enumerable*. If code `1a` exists, somebody can try `1b`, `1c` and walk your
entire database of links, some of which people expected to be unlisted.

The standard middle ground is to encode not the row number but a scrambled
version of it — multiply by a large number that has no common factor with
`62 ** 6` and take the remainder, which is reversible and shuffles the order.
You keep the collision-free guarantee and lose the enumerability. If you can
say that sentence in an interview you are well past warm-up territory.

**Base 62 versus base 64.**

Base 64 would be shorter still, but its extra two characters are `+` and `/`,
which have meanings inside a URL and would have to be percent-encoded —
making the "short" code longer. Some shorteners drop to base 58 as well,
removing `0`, `O`, `I` and `l` so that a code read aloud down a phone line is
unambiguous. Bitcoin addresses use base 58 for the same reason.

Which alphabet is right depends on whether codes get typed by humans. That is
a requirements question, and noticing that it is a requirements question
rather than a technical one is the point.

</details>

## Acceptance checklist

- [ ] `system-design/notes-week-01.md` exists, with a 300-word answer written before you read anything.
- [ ] The three things you would add next time are specific, not category names.
- [ ] `python problem-05-system-design-warmup.py` prints `10 62 916132832`, then `All checks passed.`
- [ ] `encode(0)` returns `"0"`.
- [ ] `encode(62)` returns `"10"`, not `"01"`.
- [ ] `decode(encode(row)) == row` for five thousand rows.
- [ ] Five thousand rows produce five thousand distinct codes.
- [ ] `encode(-1)` and `decode("")` and `decode("ab-c")` all raise `ValueError`.
- [ ] You can say out loud, in one sentence, why this scheme cannot produce a collision.
- [ ] You can say how many links five characters covers, without running the program.
- [ ] Every function has type hints and a docstring.

## Stretch

- **Make the codes non-enumerable while keeping them collision-free.**

  ```python
  SCRAMBLE = 387_420_489        # 3 ** 18, coprime with 62 ** 6
  SPACE = 62**6

  def scrambled_encode(row: int) -> str:
      """Encode a row number so that neighbouring rows get unrelated codes."""
      return encode(row * SCRAMBLE % SPACE)
  ```

  ```text
  row 1 -> 1yLxNU
  row 2 -> 3wxvbo
  row 3 -> 5vk9q8
  row 4 -> 7ubO4t
  ```

  Consecutive rows, unrelated codes. Now write `scrambled_decode` — you need
  the modular inverse of `SCRAMBLE`, which `pow(SCRAMBLE, -1, SPACE)` gives
  you in one call — and check that the round trip still holds for every row
  below a million. Then work out what happens when the row number reaches
  `SPACE`, and whether that is a bug or a capacity limit.

- **Pick the alphabet for humans.** Build a base-58 version with `0`, `O`,
  `I` and `l` removed. Compare the code lengths at a billion links, and decide
  whether the extra character is worth the reduction in phone-call ambiguity.

- **Write the read path.** A dict from code to URL, a `shorten(url)` and a
  `resolve(code)`. Then answer, in your notes: what happens when the same URL
  is shortened twice, and is that the behaviour you want?

Next: [Problem 6 — Week 1 Reflection](./README.md#problem-6--week-1-reflection-45-min).
