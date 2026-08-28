# Exercise 4 — The Quote Rank

> **Topic:** bisecting a range of **prices** rather than a list of positions, using a counting question as the comparison
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Medium/Hard
> **Target time:** 35 minutes
> **Why this one:** every search so far has bisected a list you could point at. Here the list would have ten billion entries and you are not allowed to build it — but the *prices* still run from a smallest to a largest, and "how many quotes cost at most this much?" only ever goes up as the price rises. That is enough. Once you have made this swap, Exercise 5 is the same move on a problem with no list at all.

## The Brief

A freight broker prices a shipment by adding two numbers together: one
**handling** fee for the paperwork at the depot, and one **linehaul** fee for
the drive.

The rate card lists every handling fee the broker offers and every linehaul
fee, each list already in ascending order. Any handling fee can be paired with
any linehaul fee, so the quotes the broker can produce are every possible sum
of one from each list.

```
handling: 2  5  9        linehaul: 1  4  4

quotes:  2+1=3   2+4=6   2+4=6
         5+1=6   5+4=9   5+4=9
         9+1=10  9+4=13  9+4=13

sorted:  3  6  6  6  9  9  10  13  13
```

Nine quotes, and notice the repeats. Two different pairs that happen to cost
the same are **two quotes**, not one — the broker really could sell either.
That is called counting *with multiplicity*, and it is the reason the sorted
row above has three 6s in it.

A shipper asks for the **4th cheapest** quote, counting from 1. Reading off
the row: `3, 6, 6, 6` — the answer is `6`.

Now the second half, which is the part that stops you reusing a remembered
solution. Along with the price, return **how many quotes are strictly
cheaper** than it. For `k = 4` that number is `1`, not `3`: only the single
`3` is genuinely below `6`. The other two 6s are the same price, and "cheaper"
means cheaper.

Three lists at the top of that picture are fine. Real rate cards have a
hundred thousand entries in each list, which is **ten billion quotes** — too
many to write down, sort, or hold in memory. So you will never build the row.
Instead you will guess a price, count how many quotes come in at or below it,
and use that count to decide whether to guess higher or lower.

Return `(quote, strictly_cheaper)`. Return `None` when the rate card cannot
produce `k` quotes at all.

## Starter

Save this as `exercise-04-quote-rank.py` and fill in every `TODO`.

```python
"""exercise-04-quote-rank.py — the freight broker's k-th quote.

Binary search on VALUES, not on indices, with a counting predicate.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
HANDLING: list[int] = [2, 5, 9]
LINEHAUL: list[int] = [1, 4, 4]


# ---- Your task ----
def count_at_most(handling: list[int], linehaul: list[int], ceiling: int) -> int:
    """Return how many pairwise quotes cost at most `ceiling`.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        ceiling: The price to count up to, inclusive.

    Returns:
        The number of (handling, linehaul) pairs whose sum is <= ceiling,
        counted with multiplicity.
    """
    # TODO: start j at the LAST linehaul index, outside the loop
    # TODO: for each handling fee, walk j down while the pair is too dear
    # TODO: indices 0..j are j + 1 affordable linehauls. Do not write j.
    ...


def quote_rank(handling: list[int], linehaul: list[int], k: int) -> tuple[int, int] | None:
    """Return the k-th cheapest quote and how many quotes are cheaper still.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        k: The 1-based rank the shipper asked for.

    Returns:
        (quote, strictly_cheaper_count), or None when the rate card cannot
        produce k quotes at all.
    """
    # TODO: guard the empty rate card and an out-of-range k
    # TODO: half-open search over PRICES, from the cheapest to the dearest quote
    # TODO: the strictly-cheaper count is one more call to count_at_most
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for rank in (1, 2, 4, 5, 9, 10):
        print(f"k={rank:2d} -> {quote_rank(HANDLING, LINEHAUL, rank)}")

    assert quote_rank(HANDLING, LINEHAUL, 1) == (3, 0)
    assert quote_rank(HANDLING, LINEHAUL, 2) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 4) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 5) == (9, 4)
    assert quote_rank(HANDLING, LINEHAUL, 9) == (13, 7)
    assert quote_rank(HANDLING, LINEHAUL, 10) is None
    assert quote_rank([], [1, 4, 4], 1) is None
    assert quote_rank([7], [7], 1) == (14, 0)
    assert count_at_most(HANDLING, LINEHAUL, 6) == 4
    assert HANDLING == [2, 5, 9]  # the rate card was never rearranged
    print("All checks passed.")
```

Three ideas you need before you start.

**Searching values instead of positions.** Until now, `lo` and `hi` have been
indexes into a list. Here they are **prices**. The cheapest quote possible is
`handling[0] + linehaul[0]`; the dearest is `handling[-1] + linehaul[-1]`. The
answer is somewhere in between, and you can halve that price range exactly the
way you halved a list.

**A counting predicate.** In Exercise 1 the comparison was "is this the value?"
Here it is "are there at least `k` quotes at or below this price?" That
question can be answered without listing the quotes, and — crucially — its
answer only ever goes from no to yes as the price rises. It can never flip
back, because raising a ceiling cannot take away a quote that already fitted
under it. That one-way behaviour is called **monotone**, and it is the only
thing bisection ever actually needs.

**A two-pointer count.** To count pairs at or below a ceiling, walk the
handling fees upwards while walking a pointer down the linehaul list. As the
handling fee grows, the dearest linehaul you can still afford only gets
cheaper — so the pointer never has to go back up. That is what makes the whole
count one pass over both lists instead of one pass per handling fee.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/exercises/exercise-04-quote-rank.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `count_at_most(handling, linehaul, ceiling)` returns the number of pairs
   whose sum is at most `ceiling`, counted with multiplicity.
2. It is one pass: the linehaul pointer is created **before** the loop over
   handling fees and never reset inside it.
3. `quote_rank(handling, linehaul, k)` returns a tuple
   `(quote, strictly_cheaper)`.
4. `strictly_cheaper` counts quotes strictly below the answer. It is **not**
   `k - 1`.
5. It returns `None` when either list is empty, or when `k` exceeds
   `len(handling) * len(linehaul)`.
6. Nothing anywhere builds, sorts, or heaps the pairwise sums. No nested loop
   over both lists except inside `count_at_most`'s single sweep.
7. The price search uses the half-open package: guard `lo < hi`, `hi = mid` on
   true, `lo = mid + 1` on false.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(handling) <= 100_000` and `0 <= len(linehaul) <= 100_000`.** Ten
  billion quotes at the top end. You cannot list them, cannot sort them, and
  cannot put them in a heap — ten billion integers is eighty gigabytes before
  Python's per-object overhead. This bound is not there to make the problem
  hard; it is there to remove the obvious solution entirely, which is what
  forces the search into the value space. Both lists may be empty, and that is
  the degenerate case the contract names.

- **`0 <= handling[i] <= 10**9` and `0 <= linehaul[j] <= 10**9`.** A quote can
  reach two billion, which does not fit in a signed 32-bit integer. Python
  will not care; a C, Java or Go implementation would, and saying so out loud
  is a habit interviewers listen for. The bound also fixes the depth of the
  search: a price range two billion wide takes about 31 halvings, not five.

- **`k` is 1-based, and values of `k` beyond the pair count are legal input.**
  A shipper asks for "the third cheapest", not "the quote at index two". Asking
  for the tenth of nine quotes is a question with an answer — `None` — not an
  error to raise.

- **Both lists arrive sorted ascending.** They come off a published rate card
  that is already ordered. Sorting them yourself adds `O(n log n)` for
  something you were handed, and worse, it hides the fact that the two-pointer
  count depends on that order.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-quote-rank.py
k= 1 -> (3, 0)
k= 2 -> (6, 1)
k= 4 -> (6, 1)
k= 5 -> (9, 4)
k= 9 -> (13, 7)
k=10 -> None
All checks passed.
```

Rows two and three are the same answer for two different ranks, and that is
correct rather than a bug. Ranks 2, 3 and 4 are all the price `6`, and the
number of quotes strictly below `6` is `1` no matter which of those three
ranks you asked for. If your row for `k = 4` reads `(6, 3)`, your search is
right and you returned `k - 1` instead of counting.

## Steps

1. Save the starter and run it. Both functions return `Ellipsis`. Expected.
2. Enumerate the nine quotes for the sample rate card **by hand** before you
   write anything. Write the sorted row on paper and mark the ranks under it.
   Every learner who skips this step misreads the tie contract.
3. Write `count_at_most` first and test it alone. On the sample card it should
   give `0` at ceiling `2`, `1` at `3`, `4` at `6`, `6` at `9`, and `9` at
   `13`.
4. Check the pointer discipline: `j = len(linehaul) - 1` sits **above** the
   `for` loop, and there is no assignment to `j` inside the loop other than
   `j -= 1`. If you find yourself resetting it, the count has quietly become a
   nested loop.
5. Now the search. `lo` is the cheapest possible quote, `hi` the dearest.
   While `lo < hi`, count at the midpoint price: if there are at least `k`
   quotes at or below it, that price might be the answer, so `hi = mid`.
   Otherwise `lo = mid + 1`.
6. When the loop ends, `lo` is the answer price. Get the second half of the
   tuple with one more call: `count_at_most(..., lo - 1)`.
7. Add the guards at the top: empty lists, and `k` beyond
   `len(handling) * len(linehaul)`.
8. Trace `k = 4` on paper, all four iterations, and check your trace against
   the walk-through in The Solution.

## The Solution

```python
"""exercise-04-quote-rank-solution.py - the freight broker's k-th quote.

Binary search on VALUES, not on indices. There is no list of quotes to
bisect - there can be ten billion of them - but "how many quotes cost at
most v?" is non-decreasing in v, and that is all bisection needs.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
HANDLING: list[int] = [2, 5, 9]
LINEHAUL: list[int] = [1, 4, 4]


# ---- Your task ----
def count_at_most(handling: list[int], linehaul: list[int], ceiling: int) -> int:
    """Return how many pairwise quotes cost at most `ceiling`.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        ceiling: The price to count up to, inclusive.

    Returns:
        The number of (handling, linehaul) pairs whose sum is <= ceiling,
        counted with multiplicity.
    """
    j = len(linehaul) - 1
    total = 0
    for fee in handling:
        while j >= 0 and fee + linehaul[j] > ceiling:
            j -= 1  # j only ever falls, which is what keeps this O(n + m)
        total += j + 1
    return total


def quote_rank(handling: list[int], linehaul: list[int], k: int) -> tuple[int, int] | None:
    """Return the k-th cheapest quote and how many quotes are cheaper still.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        k: The 1-based rank the shipper asked for.

    Returns:
        (quote, strictly_cheaper_count), or None when the rate card cannot
        produce k quotes at all.
    """
    if not handling or not linehaul or k < 1:
        return None
    if k > len(handling) * len(linehaul):
        return None

    lo = handling[0] + linehaul[0]
    hi = handling[-1] + linehaul[-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_at_most(handling, linehaul, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo, count_at_most(handling, linehaul, lo - 1)


# ---- Self-check ----
if __name__ == "__main__":
    for rank in (1, 2, 4, 5, 9, 10):
        print(f"k={rank:2d} -> {quote_rank(HANDLING, LINEHAUL, rank)}")

    assert quote_rank(HANDLING, LINEHAUL, 1) == (3, 0)
    assert quote_rank(HANDLING, LINEHAUL, 2) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 4) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 5) == (9, 4)
    assert quote_rank(HANDLING, LINEHAUL, 9) == (13, 7)
    assert quote_rank(HANDLING, LINEHAUL, 10) is None
    assert quote_rank([], [1, 4, 4], 1) is None
    assert quote_rank([7], [7], 1) == (14, 0)
    assert count_at_most(HANDLING, LINEHAUL, 6) == 4
    assert HANDLING == [2, 5, 9]  # the rate card was never rearranged
    print("All checks passed.")
```

**The list being bisected is the price range, and it was never written down.**
`lo` and `hi` are prices. Every price between them is a candidate answer, and
the search halves that range about 31 times at the top of the constraints. The
quotes themselves are never enumerated — the only thing anyone ever asks about
them is "how many are under this line?"

**`count_at_most` is monotone, and monotone is the whole licence to bisect.**
Raise the ceiling and no pair that already fitted can stop fitting, so the
count goes up or stays flat, never down. That means the answer to "are there
at least `k`?" is a run of `False`s followed by a run of `True`s, with exactly
one flip. Bisection finds flips. It does not care whether the thing being
flipped came from a list.

**The two-pointer sweep is one pass, because `j` never climbs.** Handling fees
rise through the loop, so the dearest linehaul that still fits under the
ceiling can only get cheaper. `j` starts at the top once and drifts down at
most `len(linehaul)` steps in total, across the whole loop — not per
iteration. That is why the count is `O(n + m)` rather than `O(n × m)`, and it
is the single line most worth being able to defend out loud.

**`total += j + 1` because indices `0` through `j` are `j + 1` fees.** Writing
`total += j` undercounts by one for every handling fee — on the sample card
the count at `6` drops from `4` to `1` — and the search then converges on a
price that is too high. Off-by-one in a *counter* is quieter than off-by-one
in an index, because nothing crashes.

**The trace for `k = 4`, four iterations.** `lo = 3`, `hi = 13`.

| `lo` | `hi` | `mid` | `count_at_most(mid)` | `>= 4`? | move |
| ---: | ---: | ---: | ---: | :--- | :--- |
| 3 | 13 | 8 | 4 | yes | `hi = 8` |
| 3 | 8 | 5 | 1 | no | `lo = 6` |
| 6 | 8 | 7 | 4 | yes | `hi = 7` |
| 6 | 7 | 6 | 4 | yes | `hi = 6` |

`lo == hi == 6`, so the quote is `6`. Then one more call:
`count_at_most(5) = 1`, which is the strictly-cheaper count. Return `(6, 1)`.

**Why the answer is guaranteed to be a real quote, not just some integer.**
The count only changes at prices that some pair actually costs — between two
achievable prices, nothing new fits. So the smallest price where the count
reaches `k` must itself be achievable. That is worth saying explicitly,
because "the search returns a number in the range" and "the search returns a
price you can buy" are different claims and only one of them is what the
shipper wanted.

**The strictly-cheaper count costs one extra call and cannot be derived from
`k`.** `count_at_most(quote - 1)` counts everything strictly below the answer,
exactly, because quotes are integers. `k - 1` is only right when the answer is
not part of a tie — and on this data ties are the normal case, not the edge
case. The relationship to hold in your head is
`cheaper < k <= count_at_most(quote)`: the rank sits inside the block of equal
prices, and `cheaper` sits below the whole block.

## Download and run

Download
[exercise-04-quote-rank-solution.py](./exercise-04-quote-rank-solution.py)
and run it:

```bash
python exercise-04-quote-rank-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-04-quote-rank.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the empty rate card.** You read
  `handling[0]` to build the search range before checking that anything is
  there:

  ```text
  Traceback (most recent call last):
      return handling[0] + linehaul[0]
             ~~~~~~~~^^^
  IndexError: list index out of range
  ```

  An empty handling list means the broker cannot quote at all, so the guard is
  part of the contract, not defensive padding.

- **`k = 4` returns `(6, 3)`.** You returned `k - 1` as the cheaper count. It
  is right for `k = 1` and `k = 5`, and wrong for every rank that lands inside
  a run of equal prices — which on real rate cards is most of them. Count with
  the predicate you already have.

- **`count_at_most(HANDLING, LINEHAUL, 6)` returns `1` instead of `4`.** You
  wrote `total += j` instead of `total += j + 1`. Indices `0` through `j` are
  `j + 1` values. The assert in the self-check exists for exactly this.

- **The program is correct but takes minutes on a large rate card.** You reset
  `j = len(linehaul) - 1` at the top of the `for` loop. That turns one sweep
  into a hundred thousand sweeps, so a single predicate call goes from
  two-hundred-thousand steps to ten billion — and the search calls it
  thirty-one times. There is no exception to read here; the only symptom is
  time.

- **`k = 9` returns `(13, 8)` or `(12, 7)`.** You wrote `> k` instead of
  `>= k`, or a closed-interval shape with `hi = mid - 1`. Both step past the
  boundary price. This is a *smallest value such that* search: half-open,
  `hi = mid` on true, `lo = mid + 1` on false.

- **`k = 10` returns `(13, 7)` instead of `None`.** The out-of-range guard is
  missing. Without it every midpoint fails the predicate, `lo` walks all the
  way up to the dearest quote, and you return a plausible-looking answer to a
  question that has none. Silently wrong beats crashing only in the sense that
  it survives longer.

- **You return the count instead of the quote.** The post-loop `lo` is a
  price. The count is what you compared against `k` on the way there. Read the
  signature.

## Under the hood

<details>
<summary>Under the hood — the alternatives, and why the heap loses on this shape</summary>

**Three approaches, three cost profiles.**

| Approach | Time | Space | Fails when |
| --- | --- | --- | --- |
| Build and sort the sums | `O(nm log nm)` | `O(nm)` | immediately: 10¹⁰ entries |
| Min-heap, pop `k` times | `O(k log n)` | `O(n)` | `k` is large |
| Bisect the price range | `O((n + m) log V)` | `O(1)` | never, on these bounds |

The heap version is genuinely good and worth being able to describe. Seed it
with the cheapest pair, pop the smallest, push its two neighbours, repeat `k`
times. For small `k` — "show me the five cheapest quotes" — it beats bisection
outright. Its cost is tied to `k`, though, and `k` here can be ten billion,
which is why this contract chooses the method whose cost does not mention `k`
at all.

Being able to say "the heap is better when `k` is small, and here it is not"
is worth more in an interview than knowing only one of the two.

**Where `log V` comes from, and why it is not `log(nm)`.**

`V` is the *width of the price range*, `handling[-1] + linehaul[-1]` minus
`handling[0] + linehaul[0]`, up to about `2 × 10⁹`. The search halves that
range, so it runs about `log2(2 × 10⁹) ≈ 31` times. Notice this does not
depend on how many quotes there are. Ten billion quotes packed into a narrow
price band would be *fewer* iterations, not more. The size of the answer space
is what sets the depth of a value search — a genuinely different thing from
the size of the input.

**The sandwich, stated precisely.**

At the end of the search, two facts hold about the returned price `q`:

```
count_at_most(q - 1) < k <= count_at_most(q)
```

The right-hand side is the loop's exit condition. The left-hand side is why
`q` is the *smallest* such price: had `q - 1` also reached `k`, the loop would
have moved `hi` down to it. Together they say the `k`-th cheapest quote costs
exactly `q` — and the left-hand count is precisely the number the contract
asks you to return. The second element of the tuple is not extra work bolted
on; it is one half of the proof that the first element is right.

**Two-pointer counting is a pattern in its own right.**

The same sweep answers "how many pairs sum to at least `v`", "how many pairs
lie in a band", and "how many inversions are there between two sorted lists".
In every case the trick is the same: one pointer is monotone across the whole
outer loop, so the total work is the sum of two list lengths rather than their
product. You met the shape in Week 1 as the converging two-pointer; here it is
doing arithmetic instead of comparison, and in Week 8 it comes back inside a
merge.

</details>

## Acceptance checklist

- [ ] `python exercise-04-quote-rank.py` prints six rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You enumerated the nine sample quotes by hand before writing code.
- [ ] `j` is initialised once, outside the `for` loop, and only ever decreases.
- [ ] `count_at_most` adds `j + 1`, and you can say why in one sentence.
- [ ] The strictly-cheaper count comes from a predicate call, not from `k - 1`.
- [ ] The guards return `None` for empty lists and for out-of-range `k`.
- [ ] You can state the sandwich `cheaper < k <= count_at_most(quote)`.
- [ ] Committed to Git with a message like `Add Week 5 exercise 4: quote rank`.

## Stretch

- **Return a whole page of ranks in one pass over the search.** The shipper
  wants ranks 1 through 5 side by side.

  ```python
  def quote_page(handling: list[int], linehaul: list[int], first: int, last: int) -> list[tuple[int, int]]:
      """Return (quote, strictly_cheaper) for every rank from first to last."""
      page = [quote_rank(handling, linehaul, k) for k in range(first, last + 1)]
      return [row for row in page if row is not None]
  ```

  ```text
  ranks 1-5: [(3, 0), (6, 1), (6, 1), (6, 1), (9, 4)]
  ```

  Then work out what is wasteful about it — five full searches over the same
  price range — and sketch what you would cache. You do not have to build the
  cache; naming the waste is the exercise.

- **Count in a band instead of under a ceiling.** How many quotes cost between
  6 and 9 inclusive?

  ```python
  def count_between(handling: list[int], linehaul: list[int], low: int, high: int) -> int:
      """Return how many quotes cost at least `low` and at most `high`."""
      return count_at_most(handling, linehaul, high) - count_at_most(handling, linehaul, low - 1)
  ```

  ```text
  quotes between 6 and 9: 5
  ```

  Two calls and a subtraction, and the same trick as Exercise 2's
  `end - start`. Counting a range as the difference of two prefix counts is
  one of the most reusable ideas in this course.

- **Break the monotonicity on purpose.** Change `count_at_most` to count pairs
  whose sum is *exactly* the ceiling, then run the search again. It will
  return nonsense. Work out why: the exact-count is not monotone — it goes up
  and down as the ceiling moves — so there is no single flip for bisection to
  find. Knowing what makes a predicate unsuitable is how you avoid reaching
  for this pattern where it does not belong.

When your ranks are right, move on to
[Exercise 5 — The Paving Reach](./exercise-05-paving-reach.md).
