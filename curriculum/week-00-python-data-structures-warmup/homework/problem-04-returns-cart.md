# Problem 4 — The Library's Returns Cart

> **Topic:** ordering records with one tuple key, and the stable-sort trap that hides when nothing ties
> **Lecture:** [02 — Lists, Tuples and the Dynamic Array](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** almost every program you write ends with "put these in order". A two-part rule — most of this, then earliest of that — is the normal case, and there is exactly one clean way to say it: one `key` that returns a tuple. The version with one part in it gives the right answer on data where nothing ties, which is most data, which is why this bug ships.

## The Brief

A library's returns cart holds books that came back today. Each one carries
three things: its title, its shelf mark, and how many days late it was.

```python
Returned("Bread Science", "641", 11)
```

The desk wants two orderings out of the same cart.

**The lateness list**, for the overdue notices: latest first, and where two
books were the same number of days late, the earlier title. Alphabetically, not
by whichever happened to be nearer the top of the cart.

**The shelf walk**, for the trolley: shelf marks in order as text, and inside a
shelf, titles A to Z. Shelf marks are things like `598`, `641`, `REF` — digits
and letters mixed, so they sort as **text**, which puts every number before
every letter. That is not a mistake to fix; it is how a library's spine labels
actually sort, and it is why `REF` comes last.

The key idea is one line:

```python
sorted(cart, key=lambda book: (-book.days_late, book.title))
```

The `key` is a little function Python calls once on each book. Whatever it
returns is what gets compared. Return a **tuple** and Python compares box by
box, stopping at the first difference — so `(-11, "Bread Science")` against
`(-11, "Salt Marsh Birds")` matches on the first box and is settled by the
second. One tuple says the whole rule, in the order you would say it out loud.

The minus sign is the direction switch. Lateness wants to go **down** and
titles want to go **up**, in one pass. Negating the number flips just that one
comparison. `reverse=True` would flip both, which is why it is not used here.

And there is a trap. Python's sort is **stable**: two books that tie stay in
the order they arrived on the cart. That sounds helpful, and on this page it is
what hides the bug. Sort by lateness alone and the tied pair comes out in cart
order — an answer, just not the one that was asked for.

## Starter

Create `problem-04-returns-cart.py` in your practice folder and paste this in.
Fill in every `TODO`.

```python
"""problem-04-returns-cart.py — the library's returns cart.

Two orderings out of the same cart, and both of them have a tie in them.

One tuple key says a whole ordering rule, in the order you would say it out
loud. That is the entire lesson here.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from typing import NamedTuple


class Returned(NamedTuple):
    """One book on the cart."""

    title: str
    shelf: str
    days_late: int


CART: list[Returned] = [
    Returned("Tide Tables", "REF", 4),
    Returned("Bread Science", "641", 11),
    Returned("Knot Work", "623", 4),
    Returned("Salt Marsh Birds", "598", 11),
    Returned("Kiln Repair", "738", 0),
    Returned("Ferry Timetables", "REF", 2),
]


def by_lateness(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart ordered latest first, ties by title A to Z."""
    # TODO: sorted() with ONE key that handles both rules
    ...


def by_shelf(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart in trolley order: shelf as text, then title."""
    ...


def worst_offender(cart: list[Returned]) -> Returned | None:
    """Return the single latest book, ties by title. None on an empty cart."""
    # TODO: min() with the same key. Do not sort.
    ...


def total_days_late(cart: list[Returned]) -> int:
    """Add up the days late across the whole cart."""
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for book in by_lateness(CART):
        print(f"{book.days_late:>3}d  {book.shelf:<4} {book.title}")
    print("shelf walk: " + ", ".join(book.shelf for book in by_shelf(CART)))
    print(f"worst: {worst_offender(CART).title}")
    print(f"total days late: {total_days_late(CART)}")

    assert [b.title for b in by_lateness(CART)][:2] == ["Bread Science", "Salt Marsh Birds"]
    assert [b.title for b in by_lateness(CART)][2] == "Knot Work"  # not Tide Tables
    assert [b.shelf for b in by_shelf(CART)] == ["598", "623", "641", "738", "REF", "REF"]
    assert by_shelf(CART)[-2].title == "Ferry Timetables"
    assert worst_offender(CART).title == "Bread Science"
    assert worst_offender([]) is None
    assert total_days_late(CART) == 32
    assert CART[0].title == "Tide Tables"  # the cart is untouched
    print("All checks passed.")
```

Three things you need before you start.

**A `NamedTuple`** is a tuple with names written on its boxes. `book.title`
instead of `book[0]`. It is still a plain tuple underneath — immutable,
hashable, and cheap.

**`sorted()` versus `.sort()`.** `sorted(cart, …)` builds a new list and leaves
yours alone. `cart.sort(…)` rearranges the caller's own list and returns
`None`. You were handed `CART` itself, not a copy, so `.sort()` here would
reorder the library's record behind its back.

**`min` with the same key finds the winner in one walk.** Sorting six books to
read one is doing five sixths of the work for nothing. `min(cart,
key=lambda book: (-book.days_late, book.title))` walks once. Note it is `min`
and not `max`, because the key is already negated — and you cannot negate a
title, so flipping to `max` would break the tie-break.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-04-returns-cart.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `by_lateness` returns a **new** list, most days late first, ties broken by
   title A to Z.
2. `by_shelf` returns a **new** list, shelf marks A to Z as text, ties broken by
   title A to Z.
3. `worst_offender` returns the whole `Returned` record — not the title, not the
   number — and `None` on an empty cart.
4. `total_days_late` returns the sum across the cart.
5. `CART` is in its original order after every function has run.
6. The printed rows use `f"{book.days_late:>3}d  {book.shelf:<4} {book.title}"`
   exactly.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Use `sorted()`, never `cart.sort()`.** `.sort()` rearranges the list you
  were handed — and you were handed `CART` itself — then returns `None`. The
  last assert exists for exactly this, and it catches the version that looks
  right because the returned value was fine.

- **Say both rules in one key.** `(-book.days_late, book.title)` is the whole
  rule in one pass. Sorting twice — by title, then by lateness — gets the same
  answer here, and it is two full passes, it reads backwards (the *last* sort
  written is the *first* rule applied), and it stops working the day one of the
  two rules needs the opposite direction.

- **Negate the number; leave `reverse` alone.** `reverse=True` flips the whole
  key, so lateness would go down **and** titles would go Z to A, and the tied
  pair would come out backwards. A minus sign on one number mixes the two
  directions in a single pass. Only numbers negate, which is why the title
  stays as it is.

- **Find the worst with `min`, not `sorted(...)[0]`.** `min` walks once,
  holding the best it has seen. Sorting puts all six in order so you can read
  one and throw five away. With six books you cannot feel the difference; with
  a hundred thousand, sorting does roughly seventeen times the work for the
  same one answer.

- **Shelf marks sort as text, and that is the requirement.** `"598" < "623" <
  "641" < "738" < "REF"`, because digits come before letters in character
  order. Fixing this into numeric order would need a rule for `REF`, and the
  trolley walks the shelves in spine-label order, which is what text order
  gives you.

- **At most 500 books on a cart.** That is a full trolley plus the overnight
  drop box. It matters because it says `O(n log n)` sorting is free here, and
  because it is small enough that the `sorted(...)[0]` version would also be
  fine — so the reason to write `min` is the habit, and the habit is what is
  being graded.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-04-returns-cart.py
 11d  641  Bread Science
 11d  598  Salt Marsh Birds
  4d  623  Knot Work
  4d  REF  Tide Tables
  2d  REF  Ferry Timetables
  0d  738  Kiln Repair
shelf walk: 598, 623, 641, 738, REF, REF
worst: Bread Science
total days late: 32
All checks passed.
```

Rows three and four are the test. `Knot Work` and `Tide Tables` were both four
days late, and `K` comes before `T`. In the cart, `Tide Tables` is first — so
if your list shows it above `Knot Work`, your key has one part where it needs
two, and the stable sort left the tied pair exactly where it found it.

Rows one and two tie as well, at eleven days, and they happen to come out right
either way: `Bread Science` is already before `Salt Marsh Birds` in the cart.
That is what makes this bug survive — half the ties look correct by accident.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first
   `for book in None`.
2. Write `by_lateness` with `key=lambda book: -book.days_late` — one part only,
   on purpose. Run it. Four of the asserts pass and one fails. Look at rows
   three and four before you fix anything.
3. Add the title to the key and run again.
4. Write `by_shelf`. No minus sign anywhere: both parts go up.
5. Write `worst_offender` with `min` and the same key as `by_lateness`. Get the
   empty guard in before the `min`.
6. Write `total_days_late` — one `sum` over a generator expression.
7. When it passes, try `max(CART)` with no key at all in a REPL and work out
   why that particular book came back. The answer is in *Common bugs to catch*,
   but guess first.

## The Solution

```python
"""problem-04-returns-cart-solution.py — the library's returns cart.

Every book on the cart carries a title, a shelf mark and how many days late
it came back. The desk wants two orderings out of the same cart, and both
of them have a tie in them.

One tuple key says a whole ordering rule, in the order you would say it out
loud. That is the entire lesson here.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from typing import NamedTuple


class Returned(NamedTuple):
    """One book on the cart."""

    title: str
    shelf: str
    days_late: int


CART: list[Returned] = [
    Returned("Tide Tables", "REF", 4),
    Returned("Bread Science", "641", 11),
    Returned("Knot Work", "623", 4),
    Returned("Salt Marsh Birds", "598", 11),
    Returned("Kiln Repair", "738", 0),
    Returned("Ferry Timetables", "REF", 2),
]


def by_lateness(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart ordered latest first.

    Args:
        cart: The books to order. This list is not changed.

    Returns:
        A new list, most days late first, ties broken by title A to Z.
    """
    return sorted(cart, key=lambda book: (-book.days_late, book.title))


def by_shelf(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart in the order a trolley walks the shelves.

    Args:
        cart: The books to order. This list is not changed.

    Returns:
        A new list, shelf marks A to Z as text, ties broken by title.
    """
    return sorted(cart, key=lambda book: (book.shelf, book.title))


def worst_offender(cart: list[Returned]) -> Returned | None:
    """Return the single latest book.

    Args:
        cart: The books to search.

    Returns:
        The whole record, ties broken by title A to Z, or None on an empty
        cart.
    """
    if not cart:
        return None
    return min(cart, key=lambda book: (-book.days_late, book.title))


def total_days_late(cart: list[Returned]) -> int:
    """Add up the days late across the whole cart.

    Args:
        cart: The books to add up.

    Returns:
        The sum of every book's days late.
    """
    return sum(book.days_late for book in cart)


# ---- Self-check ----
if __name__ == "__main__":
    for book in by_lateness(CART):
        print(f"{book.days_late:>3}d  {book.shelf:<4} {book.title}")
    print("shelf walk: " + ", ".join(book.shelf for book in by_shelf(CART)))
    print(f"worst: {worst_offender(CART).title}")
    print(f"total days late: {total_days_late(CART)}")

    assert [b.title for b in by_lateness(CART)][:2] == ["Bread Science", "Salt Marsh Birds"]
    assert [b.title for b in by_lateness(CART)][2] == "Knot Work"  # not Tide Tables
    assert [b.shelf for b in by_shelf(CART)] == ["598", "623", "641", "738", "REF", "REF"]
    assert by_shelf(CART)[-2].title == "Ferry Timetables"
    assert worst_offender(CART).title == "Bread Science"
    assert worst_offender([]) is None
    assert total_days_late(CART) == 32
    assert CART[0].title == "Tide Tables"  # the cart is untouched
    print("All checks passed.")
```

**The key is a tuple, and the tuple is the whole rule.**

```python
key=lambda book: (-book.days_late, book.title)
```

Read it as one English sentence: *latest first, and when two tie, the earlier
title.* Python compares the two tuples box by box and stops the moment they
differ. `Knot Work` and `Tide Tables` were both four days late, so their first
boxes match, so Python moves to the second box, and `"Knot Work" < "Tide
Tables"` settles it.

**`by_shelf` is the same shape with no minus sign,** because both of its rules
go upwards. That symmetry is worth noticing: the tuple key does not have a
special mode for two-part rules. It is always "compare these things in this
order", and the minus signs are just which direction each one runs.

**`worst_offender` uses `min`, and the `min` is not a typo.** The key is
already negated, so the "best" book — the latest — produces the *smallest* key.
Switching to `max` would need the negation removed, and then the tie-break
would have to be reversed too, and you cannot reverse a string by negating it.
The shape to remember is
`min(items, key=lambda x: (-most_of_this, first_of_that))`, and it turns up
constantly.

**`total_days_late` puts a generator expression inside `sum`.**
`sum(book.days_late for book in cart)` with no square brackets adds the numbers
as they come. With brackets, Python would build a throwaway list of six
integers first. Six integers is nothing; the habit is what you are building.

**Nothing here changed `CART`.** Both orderings return new lists and both leave
the record alone, so the last assert holds and — more usefully — any two of
these functions can be called in any order and give the same answers. A
function that sorted in place would make the second call's answer depend on
whether the first one had run.

**The cost.** Both orderings are `O(n log n)` time and `O(n)` space for the new
list. `worst_offender` is `O(n)` time and `O(1)` space. `total_days_late` is
`O(n)` and `O(1)`. The alternative for the worst book — `by_lateness(cart)[0]`
— is `O(n log n)` and `O(n)`, for exactly the same answer. That is the sentence
to say out loud: *I used `min` rather than sorting, because I need one book and
not an ordering.*

## Run it

Copy the worked answer on this page into `problem-04-returns-cart.py` and run it:

```bash
python problem-04-returns-cart.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-04-returns-cart.py`.

## Common bugs to catch

- **`Tide Tables` prints above `Knot Work`.** Your key is
  `-book.days_late` alone. A stable sort keeps tied items in the order they
  arrived, and in the cart `Tide Tables` came first. You got *an* answer; you
  did not get the one the rule asks for. Note that the eleven-day tie above it
  still looks right, which is how this survives a glance.

- **`TypeError: 'NoneType' object is not iterable`.** You wrote
  `return cart.sort(...)`:

  ```text
  Traceback (most recent call last):
      for book in by_lateness(CART):
                  ^^^^^^^^^^^^^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  `.sort()` sorts in place and hands back `None`. The quieter half of this bug
  is that `CART` really did get reordered — so even if you patch the return
  value, the library's record is now wrong.

- **`TypeError: bad operand type for unary -: 'str'`.** You negated the title
  as well:

  ```text
  Traceback (most recent call last):
      sorted(cart, key=lambda book: (-book.days_late, -book.title))
                                                      ^^^^^^^^^^^
  TypeError: bad operand type for unary -: 'str'
  ```

  Only numbers negate, and you want titles going up anyway.

- **`AttributeError: 'Returned' object has no attribute 'late'`.** A field-name
  slip:

  ```text
  AttributeError: 'Returned' object has no attribute 'late'
  ```

  This is the payoff of a `NamedTuple`. Had the records been plain tuples and
  you had written `book[3]`, you would have got `IndexError: tuple index out of
  range`, which does not tell you what you meant — or worse, `book[1]`, which
  would have given you a shelf mark and no complaint at all.

- **`max(CART)` returns `Tide Tables`.** No traceback, because comparing two
  records is perfectly legal — a `NamedTuple` *is* a tuple, so it compares box
  by box, and box zero is the title. `Tide Tables` is the alphabetically last
  title on the cart, and it was four days late, not eleven. Any time a `max` or
  a `sorted` over records gives you an answer that looks alphabetical, you
  forgot the `key`.

- **`AttributeError: can't set attribute`.** You tried to change a record:

  ```text
  AttributeError: can't set attribute
  ```

  Tuples cannot be changed after they are made, and a `NamedTuple` inherits
  that. Use `book._replace(days_late=0)`, which hands you a changed copy and
  leaves the original alone.

- **`ValueError: min() iterable argument is empty`.** The empty guard is
  missing:

  ```text
  ValueError: min() iterable argument is empty
  ```

  An empty cart is a real morning. Guard, or pass `default=None`.

## Under the hood

<details>
<summary>Under the hood — what a key function really does, and why the sort is stable</summary>

**The key is called once per item, not once per comparison.**

When you write `sorted(cart, key=f)`, CPython does not call `f` every time it
compares two books. It walks the list once, calls `f` on each item, and builds
an internal array of `(key, item)` pairs. Then it sorts that array by key
alone. Then it throws the keys away and hands you the items.

The pattern has a name — **decorate, sort, undecorate** — and before `key=`
existed in Python 2.4 you wrote it by hand:

```python
decorated = [(-b.days_late, b.title, b) for b in cart]
decorated.sort()
result = [b for _, _, b in decorated]
```

Two consequences, and both matter in real code. An expensive key is fine: if
your key has to parse a date, it happens `n` times, not `n log n` times. And
the key must be comparable while the item never has to be — which is why
sorting records with no key at all falls back to comparing the records
themselves, and works, silently, on a `NamedTuple`.

**Timsort, and why stability is free.** Python's sort is **Timsort**, written
for CPython in 2002 by Tim Peters. It looks for stretches that are already in
order — real data is full of them — and merges those stretches together. On an
already-sorted list it does one pass and stops. Worst case is `O(n log n)`, and
it never degrades the way a naive quicksort can.

**Stable** means two items that compare equal keep their input order. Timsort
gets that by only merging adjacent runs and always preferring the left side on
a tie. It is not an extra step; it falls out of how the merge works.

Stability is genuinely useful — it is what lets you sort by one thing and then
by another and keep the first ordering inside groups of the second:

```python
cart.sort(key=lambda b: b.title)         # then
cart.sort(key=lambda b: -b.days_late)    # ties keep title order
```

That gives the same answer as the tuple key. So why does the page forbid it?
Two full sorts instead of one, it reads backwards, and it cannot express two
rules running in opposite directions. One key says the whole rule in one place,
in the order you would say it.

**`min` and `max` are the same function with the comparison flipped.** Both
take the same `key`, both make one pass, both hold one current best, and both
raise `ValueError` on an empty iterable unless you pass `default=`.

</details>

## Acceptance checklist

- [ ] `python problem-04-returns-cart.py` prints six rows, the shelf walk, the
      worst book, the total, then `All checks passed.`
- [ ] `Knot Work` prints above `Tide Tables`.
- [ ] The shelf walk reads `598, 623, 641, 738, REF, REF`.
- [ ] `worst_offender` uses `min` — no sort, no loop.
- [ ] `CART` is in its original order at the end.
- [ ] `reverse=True` appears nowhere.
- [ ] You can explain why `max(CART)` with no key returns `Tide Tables`.

## Stretch

- **Group the cart by shelf before you walk it.**

  ```python
  def shelves(cart: list[Returned]) -> dict[str, list[str]]:
      """Return each shelf and its titles, shelves and titles both A to Z."""
      out: dict[str, list[str]] = {}
      for book in by_shelf(cart):
          out.setdefault(book.shelf, []).append(book.title)
      return out
  ```

  ```text
  {'598': ['Salt Marsh Birds'], '623': ['Knot Work'], '641': ['Bread Science'], '738': ['Kiln Repair'], 'REF': ['Ferry Timetables', 'Tide Tables']}
  ```

  The sort happened first, so both the shelves and the titles inside each one
  come out in order without a single extra sort — the dict simply kept the
  order it was filled in. Sorting once and grouping after is usually cheaper
  than grouping and then sorting each group.

- **Ask for the top few instead of the top one.**

  ```python
  import heapq

  def latest_few(cart: list[Returned], wanted: int) -> list[str]:
      """Return the titles of the `wanted` latest books, in order."""
      picked = heapq.nsmallest(wanted, cart, key=lambda b: (-b.days_late, b.title))
      return [book.title for book in picked]
  ```

  ```text
  ['Bread Science', 'Salt Marsh Birds']
  ```

  `nsmallest(k, …)` keeps a heap of size `k` rather than sorting everything, so
  it is `O(n log k)` instead of `O(n log n)`. With six books that is slower than
  sorting, because of the setup. With a hundred thousand and `k = 5` it is not
  close. Week 8 builds the heap by hand; here, notice that the same `key`
  argument works unchanged.

- **Watch the stable sort do something useful for once.**

  ```python
  twice = sorted(sorted(CART, key=lambda b: b.title), key=lambda b: -b.days_late)
  once = by_lateness(CART)
  print([b.title for b in twice] == [b.title for b in once])
  ```

  ```text
  True
  ```

  Two sorts, same answer, because the second one left the first one's order
  inside each tie. It works — and it is two passes to say what one tuple says,
  and the day the tie-break needs to run the other way there is no minus sign
  you can add to fix it. Knowing why it works is worth more than using it.

Next: [Problem 5 — The Hive Inspection Log](./problem-05-hive-inspection-log.md).
