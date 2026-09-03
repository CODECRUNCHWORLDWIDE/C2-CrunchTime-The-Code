# Challenge 1 — Booklet Imposition

> **Topic:** three chain sub-patterns composed — the fast/slow lower middle, an in-place reversal, and a two-chain zip
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §5
> **Difficulty:** Medium to Hard
> **Target time:** 90 minutes, and a recording of at least 30 minutes
> **Why this one:** every sub-step is easy. Getting them in the right order, with the right cut, is not. Real onsite interviews are full of problems shaped exactly like this — not deep, but three-deep — and the thing being graded is whether you name the three pieces *before* you start typing.

## The Brief

A zine is printed as a saddle-stitched booklet: a stack of sheets folded down
the middle and stapled through the fold. To assemble one, the finishing machine
does not feed pages in reading order. It works **outside-in**.

Take a stack of pages and think about which sheet is on the outside of the
folded booklet. It is the last page and the first page, printed back to back.
The next sheet in holds the second-to-last page and the second page. And so on,
working inwards, until you reach the middle.

So the machine feeds: the last page, then the first page, then the
second-to-last, then the second, then the third-to-last, then the third… If the
page count is odd, the single middle page has no partner and is fed last, on
its own.

The pages arrive as a chain. The finisher can only follow `next_page` forward
and it holds nothing except the first page.

Given

```text
P0 -> P1 -> P2 -> ... -> P(n-2) -> P(n-1)
```

rewire it into

```text
P(n-1) -> P0 -> P(n-2) -> P1 -> P(n-3) -> P2 -> ...
```

and return the **new first page**.

You may change `next_page`. You may **not** change `number`. The page numbers
are printed on paper; swapping them in memory would give you a chain that lies
about what the machine will actually feed.

**Why the function returns something.** The first page of the collated chain is
the booklet's original *last* page. A caller who kept the old head would be
holding a pointer into the middle of the answer.

**The wrong answer that looks right.** The most commonly published version of
this rewiring goes front-first: `P0 -> P(n-1) -> P1 -> P(n-2) -> …`, which
turns `1 2 3 4 5 6` into `1 6 2 5 3 4`. That is a different machine's feed
order. Every example below distinguishes the two, and the difference in the
code is one line.

## Starter

Create `challenge-01-booklet-imposition.py` and paste this in. Fill in every
`TODO`.

```python
"""challenge-01-booklet-imposition.py — collate a booklet outside-in.

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per booklet and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Page:
    """One page of a booklet, in chain order. Only `next_page` may change."""

    def __init__(self, number: int, next_page: "Page | None" = None) -> None:
        self.number = number
        self.next_page = next_page


def build_chain(numbers: list[int]) -> Page | None:
    """Wire a booklet from a list of printed page numbers.

    Args:
        numbers: The number printed on each page, in chain order. Numbers
            may repeat and need not be sequential.

    Returns:
        The first page, or None for an empty booklet.
    """
    if not numbers:
        return None
    pages = [Page(number) for number in numbers]
    for earlier, later in zip(pages, pages[1:]):
        earlier.next_page = later
    return pages[0]


def chain_numbers(first: Page | None) -> list[int]:
    """Walk a booklet into a list of page numbers, refusing to hang.

    Args:
        first: The first page of the chain, or None.

    Returns:
        The printed numbers in feed order.

    Raises:
        AssertionError: If the chain loops, which means the rewiring is
            wrong and a plain walk would never stop.
    """
    numbers: list[int] = []
    while first is not None:
        numbers.append(first.number)
        first = first.next_page
        assert len(numbers) < 100_000, "the imposition created a loop"
    return numbers


def _lower_middle(first: Page) -> Page:
    """Return the last page of the front half — the earlier of two middles."""
    # TODO 1: Exercise 3, with `next_page` instead of `next_segment`.
    ...


def _reverse(first: Page | None) -> Page | None:
    """Turn a chain around in place and return its new first page."""
    # TODO 2: three names — previous, current, following — and one loop.
    #         No recursion; see the Constraints for why.
    ...


def _interleave(front: Page, back: Page | None) -> Page:
    """Zip two chains together, one page each, starting with `back`.

    Args:
        front: The front half. Never empty, and never shorter than `back`.
        back: The reversed back half, or None when the booklet has one page.

    Returns:
        The head of the zipped chain.
    """
    # TODO 3: take from `back` first. Save both successors BEFORE you rewire
    #         anything. Stop the moment `back` runs out, and leave whatever
    #         is left of `front` attached where it already is.
    ...


def impose(first_page: Page | None) -> Page | None:
    """Rewire a booklet into outside-in feed order and return the new head.

    Args:
        first_page: The first page of the chain, or None for no booklet.

    Returns:
        The new first page, which is the booklet's original last page.
    """
    # TODO 4: empty booklet, then middle, then cut, then reverse, then zip.
    #         The cut must happen before the reverse. See Common bugs.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ([], []),
        ([7], [7]),
        ([1, 2], [2, 1]),
        ([1, 2, 3], [3, 1, 2]),
        ([1, 2, 3, 4], [4, 1, 3, 2]),
        ([1, 2, 3, 4, 5], [5, 1, 4, 2, 3]),
        ([1, 2, 3, 4, 5, 6], [6, 1, 5, 2, 4, 3]),
        ([1, 2, 3, 4, 5, 6, 7], [7, 1, 6, 2, 5, 3, 4]),
        ([11, 4, 4, 90], [90, 11, 4, 4]),
        ([-3, 12, -3], [-3, -3, 12]),
    ]

    for numbers, expected in CASES:
        fed = chain_numbers(impose(build_chain(numbers)))
        assert fed == expected, f"{numbers}: got {fed}, wanted {expected}"
        print(f"{str(numbers):<24} feeds as {fed}")

    kept = [5, 5, 9, 2, 2, 2, 8]
    assert sorted(chain_numbers(impose(build_chain(kept)))) == sorted(kept)

    long_run = chain_numbers(impose(build_chain(list(range(4000)))))
    assert len(long_run) == 4000
    assert long_run[0] == 3999
    assert long_run[1] == 0
    assert long_run[-1] == 1999
    print(f"{'4000 pages':<24} feeds as [3999, 0, 3998, 1, ..., 2000, 1999]")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/challenges/challenge-01-booklet-imposition.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `impose(first_page)` returns the **new first page**, which is the booklet's
   original last page, and rewires the chain in place.
2. `1 2 3 4 5 6` comes out as `6 1 5 2 4 3`. Back half first, every time.
3. For an odd page count the lone middle page is fed **last**, on its own.
4. `impose(None)` returns `None`. A one-page booklet returns that page and the
   loops must not run.
5. Only `next_page` is written. `number` is never assigned.
6. The reversal is **iterative**. See the Constraints for the arithmetic.
7. Fixed memory: a constant number of page variables across all three
   sub-steps. No list, no stack, no set.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Up to 4,000 pages, and that number is chosen to break one specific
  solution.** A recursive reversal of the back half pushes about `n / 2` stack
  frames. At 4,000 pages that is 2,000 frames against CPython's default limit
  of 1,000, so the recursive version does not run slowly — it raises
  `RecursionError`. Say the arithmetic out loud: *4000 divided by 2 is 2000,
  and the limit is 1000.* A bound that turns a style preference into a hard
  failure is worth naming precisely.

- **Fixed memory, because the imposition runs on the finisher's embedded
  controller.** Walking the chain into a Python list makes the rewiring trivial
  by index, and it is the single most common way people solve this. It is also
  O(n) space and is rejected. As everywhere this week: it is not a worse
  algorithm, it just does not fit. Say that sentence rather than pretending the
  list version is slow.

- **Page numbers repeat and need not be sequential.** Inserts, plates and blank
  versos all reuse numbers. There is no sorting, no arithmetic on numbers, and
  no way to tell one page from another except by where it sits in the chain.
  `[11, 4, 4, 90]` is in the check list because any solution that identifies
  pages by number fails it.

- **The chain has no loop when you get it.** This is a rewiring problem, not a
  detection problem. But if your intermediate state accidentally makes one, a
  plain walk would never stop — which is why `chain_numbers` carries an assert
  rather than trusting you.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-booklet-imposition-solution.py
[]                       feeds as []
[7]                      feeds as [7]
[1, 2]                   feeds as [2, 1]
[1, 2, 3]                feeds as [3, 1, 2]
[1, 2, 3, 4]             feeds as [4, 1, 3, 2]
[1, 2, 3, 4, 5]          feeds as [5, 1, 4, 2, 3]
[1, 2, 3, 4, 5, 6]       feeds as [6, 1, 5, 2, 4, 3]
[1, 2, 3, 4, 5, 6, 7]    feeds as [7, 1, 6, 2, 5, 3, 4]
[11, 4, 4, 90]           feeds as [90, 11, 4, 4]
[-3, 12, -3]             feeds as [-3, -3, 12]
4000 pages               feeds as [3999, 0, 3998, 1, ..., 2000, 1999]
All checks passed.
```

The five-page line is the one that decides your split convention. Page 3 is the
lone middle and it is fed **last**. If it comes out in the middle of the
result, you split at the wrong place.

## Steps

1. **Frame.** Restate. Confirm "rewire only" — `next_page` may change, `number`
   may not. Confirm the alternation starts at the **back**. Confirm the
   function returns the new head. Walk `1 2 3 4 5` by hand and confirm the
   answer is `5 1 4 2 3` and not `1 5 2 4 3`.
2. **Research constraints.** Name the 4,000-page bound and do the recursion
   arithmetic out loud. Name the memory bound and what it rejects. Note that
   numbers repeat, so only position exists.
3. **Assess options, and this is the graded step.** Say the decomposition
   before you write anything:

   > "Three sub-steps. First, the fast/slow lower middle — that is Exercise 3
   > this week — and I cut after it, so the front half is the longer one.
   > Second, an iterative in-place reversal of the back half; iterative rather
   > than recursive because the page bound is 4,000 and the recursion limit is
   > 1,000. Third, zip the two halves together taking from the reversed back
   > half first, and let the front half's leftover page stay attached at the
   > end when the count is odd. I will write each as a helper, then compose
   > them, and the composed function returns the reversed back half's head."

   Naming the three pieces before touching the keyboard is the whole
   discriminator. It is visible on a recording in a way correctness is not.
4. **Make the solution, one helper at a time, testing each.** `_lower_middle`
   is a copy of Exercise 3 with a renamed attribute; check it against a
   four-page and a five-page chain before moving on. `_reverse` is three names
   and a loop; check it in isolation. `_interleave` is the only new thinking.
5. **Make the solution, the composition.** Empty check, middle, **cut**,
   reverse, zip, return. The cut is one line and leaving it out is the bug that
   costs people twenty minutes.
6. **Examine, odd length.** Trace `1 2 3 4 5`. Lower middle: page 3. Cut: front
   is `1 2 3`, back is `4 5`. Reverse the back: `5 4`. Zip: take 5, take 1,
   take 4, take 2; back is empty, and 2's `next_page` is still 3 from before
   the cut. Result `5 1 4 2 3`, head is page 5. ✓
7. **Examine, even length.** Trace `1 2 3 4`. Lower middle: page 2. Cut: front
   `1 2`, back `3 4`. Reverse: `4 3`. Zip: take 4, take 1, take 3, take 2; both
   empty. Result `4 1 3 2`, head is page 4. ✓
8. **Examine, the one-page booklet.** Lower middle: page 7, and the loop never
   runs. Cut: front is `7`, back is `None`. Reversing `None` gives `None`.
   Zipping with an empty back half returns `front`. Result `7`. ✓ That trace is
   what proves the empty-back-half branch, and skipping it is how people ship a
   version that crashes on a one-page zine.
9. **Examine, cost.** O(n) time — three linear passes one after another, so
   three times O(n) is O(n). O(1) space — a fixed number of page variables in
   each sub-step, and running them in sequence rather than nesting them keeps
   the bound. Best, average and worst are the same; no booklet shape changes
   the work.

## The Solution

```python
"""challenge-01-booklet-imposition-solution.py — collate a booklet outside-in.

Three small jobs, done in a row, none of which needs a spare copy of the
chain:

1. Find the earlier of the two middle pages and cut the chain there, so the
   front half is never shorter than the back half.
2. Turn the back half around, one page at a time.
3. Zip the two halves together, taking from the turned-around back half
   first, and let whatever is left of the front half stay attached.

The booklets are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per booklet, then
"All checks passed."
"""

from __future__ import annotations


class Page:
    """One page of a booklet, in chain order. Only `next_page` may change."""

    def __init__(self, number: int, next_page: "Page | None" = None) -> None:
        self.number = number
        self.next_page = next_page


def build_chain(numbers: list[int]) -> Page | None:
    """Wire a booklet from a list of printed page numbers.

    Args:
        numbers: The number printed on each page, in chain order. Numbers
            may repeat and need not be sequential.

    Returns:
        The first page, or None for an empty booklet.
    """
    if not numbers:
        return None
    pages = [Page(number) for number in numbers]
    for earlier, later in zip(pages, pages[1:]):
        earlier.next_page = later
    return pages[0]


def chain_numbers(first: Page | None) -> list[int]:
    """Walk a booklet into a list of page numbers, refusing to hang.

    Args:
        first: The first page of the chain, or None.

    Returns:
        The printed numbers in feed order.

    Raises:
        AssertionError: If the chain loops, which means the rewiring is
            wrong and a plain walk would never stop.
    """
    numbers: list[int] = []
    while first is not None:
        numbers.append(first.number)
        first = first.next_page
        assert len(numbers) < 100_000, "the imposition created a loop"
    return numbers


def _lower_middle(first: Page) -> Page:
    """Return the last page of the front half — the earlier of two middles."""
    slow = first
    fast = first
    while fast.next_page is not None and fast.next_page.next_page is not None:
        slow = slow.next_page
        fast = fast.next_page.next_page
    return slow


def _reverse(first: Page | None) -> Page | None:
    """Turn a chain around in place and return its new first page."""
    previous = None
    current = first
    while current is not None:
        following = current.next_page
        current.next_page = previous
        previous = current
        current = following
    return previous


def _interleave(front: Page, back: Page | None) -> Page:
    """Zip two chains together, one page each, starting with `back`.

    Args:
        front: The front half. Never empty, and never shorter than `back`.
        back: The reversed back half, or None when the booklet has one page.

    Returns:
        The head of the zipped chain.
    """
    if back is None:
        return front

    head = back
    while back is not None:
        back_next = back.next_page
        front_next = front.next_page
        back.next_page = front
        if back_next is None:
            break  # The front half's leftover page is already attached.
        front.next_page = back_next
        back = back_next
        front = front_next
    return head


def impose(first_page: Page | None) -> Page | None:
    """Rewire a booklet into outside-in feed order and return the new head.

    Args:
        first_page: The first page of the chain, or None for no booklet.

    Returns:
        The new first page, which is the booklet's original last page.
    """
    if first_page is None:
        return None
    middle = _lower_middle(first_page)
    back = middle.next_page
    middle.next_page = None
    return _interleave(first_page, _reverse(back))


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ([], []),
        ([7], [7]),
        ([1, 2], [2, 1]),
        ([1, 2, 3], [3, 1, 2]),
        ([1, 2, 3, 4], [4, 1, 3, 2]),
        ([1, 2, 3, 4, 5], [5, 1, 4, 2, 3]),
        ([1, 2, 3, 4, 5, 6], [6, 1, 5, 2, 4, 3]),
        ([1, 2, 3, 4, 5, 6, 7], [7, 1, 6, 2, 5, 3, 4]),
        ([11, 4, 4, 90], [90, 11, 4, 4]),
        ([-3, 12, -3], [-3, -3, 12]),
    ]

    for numbers, expected in CASES:
        fed = chain_numbers(impose(build_chain(numbers)))
        assert fed == expected, f"{numbers}: got {fed}, wanted {expected}"
        print(f"{str(numbers):<24} feeds as {fed}")

    kept = [5, 5, 9, 2, 2, 2, 8]
    assert sorted(chain_numbers(impose(build_chain(kept)))) == sorted(kept)

    long_run = chain_numbers(impose(build_chain(list(range(4000)))))
    assert len(long_run) == 4000
    assert long_run[0] == 3999
    assert long_run[1] == 0
    assert long_run[-1] == 1999
    print(f"{'4000 pages':<24} feeds as [3999, 0, 3998, 1, ..., 2000, 1999]")

    print("All checks passed.")
```

**The decomposition is the answer; the code is bookkeeping.** Three passes,
each of which you have already written this week or could write in two minutes.
What makes the problem hard is that the three have to happen in an order, and
the boundary between them — the cut — is easy to forget because nothing in the
prompt mentions it.

**Why the *lower* middle, specifically.** The lower middle is the last page of
the front half, so cutting after it leaves the front half with `ceil(n / 2)`
pages and the back half with `floor(n / 2)`. The front half is therefore never
shorter. That is exactly the invariant the zip needs: the back half runs out
first or at the same time, and when the count is odd the leftover page belongs
to the front half and ends up fed last — which is what the machine does.

Take the *upper* middle instead and the halves swap sizes for odd counts. The
leftover page now belongs to the back half, the zip's ending is wrong, and page
3 lands in the middle of the five-page result instead of at the end. One
guard, two conventions, a whole different answer. See
[Exercise 3](../exercises/exercise-03-midroll-break.md) for the guard shift.

**The cut has to happen before the reversal.**

```python
    back = middle.next_page
    middle.next_page = None
```

Without that second line, the back half is still attached to the front half.
Reversing it walks straight on through the front half too, and you end up with
a chain that points at itself. `chain_numbers` catches it with an assert
instead of hanging, which is the only reason the failure is readable:

```text
AssertionError: the imposition created a loop
```

**The reversal is three names and no cleverness.**

```python
    previous = None
    current = first
    while current is not None:
        following = current.next_page
        current.next_page = previous
        previous = current
        current = following
```

Read it as: *remember where I was going, point backwards instead, then shuffle
both names along.* `following` exists solely because the second line destroys
the only route to the rest of the chain — you have to save it first. When the
loop ends, `current` is `None` and `previous` is the last page you touched,
which is the new head.

**The zip's ending is the subtle part.**

```python
        if back_next is None:
            break  # The front half's leftover page is already attached.
```

At that moment `back` has just been pointed at `front`, and `front` still
carries whatever the cut left after it. For an even count that is nothing, so
the chain ends there. For an odd count that is exactly one page — the lone
middle — so it stays attached and gets fed last. One `break` handles both
parities, because the cut already put the leftover in the right half.

Break the wrong way — set `front.next_page = back_next` before checking — and
you overwrite the leftover page's link with `None` and lose it. The five-page
booklet drops page 3 and the check reports four pages where there were five.

**Save both successors before rewiring either page.** Inside the zip, the two
lines that read `back.next_page` and `front.next_page` come first, then the
line that writes. Reverse that order and you follow a pointer you have already
changed, which is how people lose half a booklet. Save, rewire, advance, in
that order, every time.

**The memory claim holds because the sub-steps are in sequence, not nested.**
Each of the three uses a fixed number of names, and they run one after another
rather than one inside another, so the total is still fixed. That is worth
saying out loud, because "each part is O(1) so the whole is O(1)" is not
automatically true — it is true here because nothing accumulates between them.

## Download and run

Download
[challenge-01-booklet-imposition-solution.py](./challenge-01-booklet-imposition-solution.py)
and run it:

```bash
python challenge-01-booklet-imposition-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-01-booklet-imposition.py`.

To grade your own file against the week's larger cases, including the
4,000-page run that breaks a recursive reversal:

```bash
C2_WEEK04_SOLUTIONS=challenge-01-booklet-imposition pytest ../exercises/timed_runner.py -v -k impose
```

See [`timed_runner.py`](../exercises/timed_runner.py) for the full case list.

## Common bugs to catch

- **Zipping front-first.** You get `1 6 2 5 3 4` instead of `6 1 5 2 4 3`. No
  exception, just the other machine's feed order. This is the single most
  likely failure for anyone who has met this composition before, and the fix is
  one line: the zip's `head` and its first take both come from `back`.

- **`AssertionError: the imposition created a loop`.** You forgot the cut:

  ```text
  Traceback (most recent call last):
      assert len(numbers) < 100_000, "the imposition created a loop"
             ^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: the imposition created a loop
  ```

  The reversal ran on a back half that was still joined to the front half, so
  it turned the whole chain around and left a page pointing at something it
  should not. Set `middle.next_page = None` before reversing.

- **`RecursionError: maximum recursion depth exceeded`.** Your reversal is
  recursive:

  ```text
  Traceback (most recent call last):
      return rev(nxt, node)
    [Previous line repeated 994 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  This is the 4,000-page bound doing its job. The recursive version is elegant
  and it will not run on this input. Note the useful detail in the message:
  Python stops at the limit rather than at the end of the chain, so the traceback
  tells you nothing about your booklet — only that you went too deep.

- **Losing the lone middle page.** The five-page booklet comes out as four
  pages. You wrote `front.next_page = back_next` before checking whether
  `back_next` was `None`, so on the last turn you overwrote the leftover page's
  link. Check first, then write.

- **`AttributeError: 'NoneType' object has no attribute 'next_page'`.** Almost
  always the empty booklet reaching `_lower_middle`, whose guard reads inside
  `fast` on its first evaluation:

  ```text
  Traceback (most recent call last):
      while fast.next_page is not None and fast.next_page.next_page is not None:
            ^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'next_page'
  ```

  `impose` must return `None` before calling any helper. The same guard shape
  bit you in Exercise 3; it is the price of the lower-middle convention.

- **The one-page booklet crashing in the zip.** Its back half is `None`, so the
  zip has nothing to start from. `_interleave` returns `front` in that case, as
  its first two lines. Without them you get `AttributeError` on
  `back.next_page`.

- **Assigning to `number`.** Producing the right sequence of numbers by
  shuffling the labels rather than the links passes the multiset check and is
  still forbidden — the finisher feeds physical paper, and the paper does not
  renumber itself. Obey the spec rather than the test.

## Under the hood

<details>
<summary>Under the hood — why three passes and not one, and what this composition is really called</summary>

**Could you do it in one pass?** Not without extra memory. To interleave from
both ends of a forward-only chain you must be able to walk *backwards* from the
end, and the only ways to get that are to reverse a half in place (three
passes, no memory) or to remember the pages (one pass, O(n) memory). The
constraint chooses for you. Saying this out loud is worth doing, because "why
not one pass?" is the natural follow-up question and the honest answer is a
tradeoff, not a limitation of your solution.

**The composition has a name in the printing trade.** *Imposition* is the whole
craft of arranging pages on a sheet so that folding and trimming produces a
readable book, and saddle-stitch imposition is the simplest scheme in it. Real
imposition software also handles creep — the inner sheets stick out further,
so page positions shift by fractions of a millimetre — which is a fine example
of a problem whose interesting part is nothing to do with the data structure.

**Three passes is not three times slower than one.** All three are linear, and
constant factors matter far less than the number of times you traverse memory
that is not in cache — which, for a chain of objects scattered across the heap,
is dominated by the chase itself. If this were an array, three passes over four
thousand contiguous integers would be faster than one pass with unpredictable
jumps. Worth knowing; not worth mentioning unless asked.

**Where else the reverse-a-half move shows up.** Any time you need to compare or
combine a chain with itself back-to-front and cannot afford a copy.
[Homework Problem 3](../homework/problem-03-symmetric-dies.md) this week is the
same first two sub-steps with a different third, and it adds the requirement
that you put the chain back afterwards — which this challenge does not ask for,
and which is the standard interview follow-up.

**Splitting a chain in half is also the primitive merge sort needs.** Change the
third sub-step to "return `(front, back)`" and you have the split half of a
merge sort that runs on a chain in O(1) extra space — which is the reason merge
sort, not quicksort, is the sort you use on a linked structure.

</details>

## Acceptance checklist

- [ ] `python challenge-01-booklet-imposition.py` prints eleven lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] `1 2 3 4 5 6` feeds as `6 1 5 2 4 3` — back half first.
- [ ] The five-page booklet feeds page 3 **last**.
- [ ] `middle.next_page = None` happens before the reversal.
- [ ] The reversal is iterative, and you can state the frame arithmetic.
- [ ] No list, no stack, no set anywhere; `number` is never assigned.
- [ ] The empty and one-page booklets are traced by hand in your write-up.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/challenge-01-booklet-imposition.md`
      with a recording of at least 30 minutes, and its Assess-options section
      names all three sub-steps **before** any code appears.

## Stretch

- **Split and return both halves instead of zipping them.** Change only the
  third sub-step and you have the primitive a chain merge sort needs:

  ```python
  def split_halves(first_page: Page | None) -> tuple[Page | None, Page | None]:
      """Cut after the lower middle and return both halves, front first."""
      if first_page is None:
          return None, None
      middle = _lower_middle(first_page)
      back = middle.next_page
      middle.next_page = None
      return first_page, back
  ```

  ```text
  [1, 2, 3, 4, 5, 6]       front [1, 2, 3]   back [4, 5, 6]
  [1, 2, 3, 4, 5]          front [1, 2, 3]   back [4, 5]
  [7]                      front [7]         back []
  ```

- **Undo the imposition.** Write `deimpose` that takes a collated chain and puts
  it back into reading order. It is the same three sub-steps with the zip
  replaced by an unzip, and it is a genuinely good ten minutes because the
  unzip's ending has the mirror-image trap.

  ```text
  [6, 1, 5, 2, 4, 3]       reads back as [1, 2, 3, 4, 5, 6]
  [5, 1, 4, 2, 3]          reads back as [1, 2, 3, 4, 5]
  ```

- **Feed the front-first order instead, and keep both.** One line differs — the
  zip's `head` and its first take come from `front` rather than `back`. Having
  both functions side by side, and being able to say which line differs, is the
  clearest possible proof that you understood the composition rather than
  memorising one output.

  ```text
  outside-in   [1, 2, 3, 4, 5, 6]  ->  [6, 1, 5, 2, 4, 3]
  front-first  [1, 2, 3, 4, 5, 6]  ->  [1, 6, 2, 5, 3, 4]
  ```
When the booklet collates, move on to
[Challenge 2 — The Feed-Line Weld](./challenge-02-feedline-weld.md).
