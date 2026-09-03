# Exercise 1 — The Refund Pair

> **Topic:** the complement lookup — the canonical hash-map shape, where "search for a partner" becomes "ask whether the partner already went past"
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** this is the first problem of the week and the shape every other hash-map problem is a variation of. It also teaches the sentence you will say out loud in every interview from here on: *each step does O(1) average work on the map, and there are n steps, so the whole thing is O(n) time and O(n) space.* If that sentence is not automatic by the end of this page, the rest of the week will be harder than it needs to be.

## The Brief

Imagine a long shop receipt. Each line is one charge, in the order it happened.
Somebody says "you owe me a refund of 550" and you have to find **two** lines on
that receipt that add up to 550.

The slow way is the way a person does it: take line 1, check it against every
other line; take line 2, check it against every other line; and so on. On a
four-line receipt that is fine. On a receipt with two hundred thousand lines it
is twenty billion checks and you will never finish.

The fast way is a trick, and the trick is one change of question. Instead of
*"which other line pairs with this one?"* ask *"the number I need — have I
already walked past it?"* If you are standing on a charge of 400 and the refund
total is 550, the number you need is 150. You do not have to go looking for it.
You only have to remember every number you have already seen.

Remembering is what a **hash map** is for. A hash map — Python calls it a
`dict` — is a wall of pigeonholes where the label on a pigeonhole can be
anything you like, and finding the right pigeonhole takes the same tiny amount
of time whether there are ten of them or ten million. So you walk the receipt
once, and at each line you do two things: ask the map whether the number you
need is already in it, and then drop the number you are standing on into the
map.

Now the contract, and it has three details that are easy to skim.

A support agent is reconciling a customer's account. They have the customer's
charge history — a list of amounts in cents, **in the order the charges were
made** — and a refund total the customer disputes.

Find the **earliest-completing** pair of distinct charges that together equal
the refund total, and return their positions in the history.

"Earliest-completing" means: of all valid pairs, return the one whose **later**
position is smallest. Return the two positions in ascending order.

If no pair works, return `None`. Do not assume a solution exists.

## Starter

Create `exercise-01-refund-pair.py` in your practice repo and paste this in.
Fill in the `TODO`.

```python
"""exercise-01-refund-pair.py — the earliest-completing refund pair.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""


def find_refund_pair(charges: list[int], refund_total: int) -> tuple[int, int] | None:
    """Return the earliest-completing pair of positions summing to the total.

    Args:
        charges: Charge amounts in cents, in the order they were made.
        refund_total: The disputed refund total, in cents.

    Returns:
        (i, j) with i < j and charges[i] + charges[j] == refund_total,
        choosing the pair whose later position j is smallest. None if no
        pair sums to the total.
    """
    # TODO: one pass. Keep a dict from amount -> earliest position seen.
    # At each charge: work out the complement, ask the dict about it FIRST,
    # then record the current amount if it is new.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int, tuple[int, int] | None]] = [
        ([400, 150, 250, 300], 550, (0, 1)),
        ([100, 450, 450, 100], 550, (0, 1)),
        ([700, 700], 1400, (0, 1)),
        ([700], 1400, None),
        ([], 0, None),
        ([-200, 500, 200], 0, (0, 2)),
        ([100, 200, 300], 1000, None),
    ]

    for charges, total, expected in cases:
        found = find_refund_pair(charges, total)
        assert found == expected, (charges, total, found, expected)
        shown = "none" if found is None else f"{found[0]},{found[1]}"
        print(f"total {total:5d}  ->  {shown:>6}   from {charges}")

    print("All checks passed.")
```

Three words you need before you start.

**Complement.** The number that completes a pair. If the total is 550 and you
are standing on 400, the complement is 150. It is just
`target - what_i_have`, and it is the whole idea of this exercise.

**`dict`.** Python's hash map. `seen[400] = 0` files the fact "the amount 400
was first seen at position 0". `400 in seen` asks whether that pigeonhole is
occupied, and answers in the same time no matter how full the map is.

**`enumerate`.** `for i, x in enumerate(charges)` hands you the position and the
value together, so you never have to keep a counter by hand.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/exercises/exercise-01-refund-pair.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_refund_pair` returns a tuple `(i, j)` with `i < j`, where `i` and `j`
   are positions in the original list.
2. Of all valid pairs, it returns the one whose **later** position `j` is
   smallest. On `[400, 150, 250, 300]` with 550 that is `(0, 1)`, not `(2, 3)`.
3. It returns `None` — not `[]`, not `(-1, -1)`, not `False` — when no pair sums
   to the total.
4. A charge may not pair with itself. `[700]` with 1400 is `None`.
5. It runs in `O(n)` time and `O(n)` space. A nested loop fails this requirement
   even though it produces the right answers on all seven cases.
6. Negative charges work. A chargeback is a negative charge, and
   `[-200, 500, 200]` with total 0 is `(0, 2)`.
7. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(charges) <= 200_000`.** A busy account really can accumulate two
  hundred thousand lines over a few years. The bound is chosen to reject the
  nested loop rather than to describe a receipt: comparing every line against
  every other is about `2 x 10^10` additions, which is minutes of work for a
  question a single pass answers in a fraction of a second. When you say in an
  interview "the constraint rules out the quadratic solution", *this* is the
  arithmetic you are pointing at.

- **`-50_000 <= charges[i] <= 50_000`, in cents.** Charges may be negative,
  because a chargeback is a negative charge. This bound exists to break one
  specific shortcut: the "optimisation" that skips any charge larger than the
  refund total, on the grounds that nothing can pair with it. With negatives on
  the list that reasoning is false, and the sixth self-check is the case that
  catches it.

- **`refund_total` fits in the range any two charges could sum to.** So there is
  nothing clever to do with the target's magnitude and no arithmetic to guard:
  Python integers grow as large as they need to. Say that out loud anyway,
  because in a fixed-width language the sum of two charges is exactly where you
  would want to check.

- **Store the earliest position for each amount, and never overwrite it.** The
  contract asks for the pair that completes earliest. When an amount occurs
  twice, its earlier occurrence can only ever produce an equally good or better
  answer than its later one, so keeping the later one can only lose.
  `[100, 450, 450, 100]` with 550 is the case that shows it.

- **Ask the map before you add to it.** If you insert the current amount first,
  then a charge whose complement is itself finds *itself*, and you return one
  position paired with itself. `[700, 700]` with 1400 is the shortest input that
  catches it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-refund-pair-solution.py
total   550  ->     0,1   from [400, 150, 250, 300]
total   550  ->     0,1   from [100, 450, 450, 100]
total  1400  ->     0,1   from [700, 700]
total  1400  ->    none   from [700]
total     0  ->    none   from []
total     0  ->     0,2   from [-200, 500, 200]
total  1000  ->    none   from [100, 200, 300]
All checks passed.
```

Read the second row. Four pairs are valid on `[100, 450, 450, 100]` — `(0,1)`,
`(0,2)`, `(1,3)` and `(2,3)` — and the one that completes earliest is `(0,1)`,
because its later position is 1 while the others complete at 2, 3 and 3. If
your version prints `1,3` there, you overwrote the stored position when the
second `450` came past.

## Steps

1. Create the file, paste the starter, and run it before writing anything. The
   bare `...` makes `find_refund_pair` return `None`, so the first case fails
   its assert immediately. That is the correct starting point — it proves the
   self-check is real.
2. Write down, in one sentence, what the map's keys are and what its values are.
   Keys are amounts; values are positions. Getting that backwards is the most
   common way this exercise goes wrong, and it is far cheaper to catch now than
   in a debugger.
3. Write the loop with only the lookup in it — no insert yet. Run it. Every case
   now returns `None`, which is expected, because nothing was ever put in the
   map.
4. Add the insert *after* the lookup, guarded by `if amount not in
   earliest_at`. Run again.
5. When all seven cases pass, go back to `[400, 150, 250, 300]` and trace it by
   hand. Say out loud what the map holds at each step. You are rehearsing the
   thing you will have to do at a whiteboard.
6. Then say the cost sentence out loud, in one breath: *"one pass over n
   charges, each doing O(1) average work on the map, so O(n) time; the map holds
   at most one entry per distinct amount, so O(n) space."*

## The Solution

```python
"""exercise-01-refund-pair-solution.py — the earliest-completing refund pair.

One pass over the charge history, carrying a map from amount to the earliest
position that amount was seen at. At every charge we ask one question: have I
already seen the amount that would complete this one?

Time: O(n) — one pass, each dict operation O(1) average.
Space: O(n) — the map holds at most one entry per distinct amount.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def find_refund_pair(charges: list[int], refund_total: int) -> tuple[int, int] | None:
    """Return the earliest-completing pair of positions summing to the total.

    Args:
        charges: Charge amounts in cents, in the order they were made.
        refund_total: The disputed refund total, in cents.

    Returns:
        (i, j) with i < j and charges[i] + charges[j] == refund_total,
        choosing the pair whose later position j is smallest. None if no
        pair sums to the total.
    """
    earliest_at: dict[int, int] = {}
    for position, amount in enumerate(charges):
        complement = refund_total - amount
        if complement in earliest_at:
            return (earliest_at[complement], position)
        if amount not in earliest_at:
            earliest_at[amount] = position
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int, tuple[int, int] | None]] = [
        ([400, 150, 250, 300], 550, (0, 1)),
        ([100, 450, 450, 100], 550, (0, 1)),
        ([700, 700], 1400, (0, 1)),
        ([700], 1400, None),
        ([], 0, None),
        ([-200, 500, 200], 0, (0, 2)),
        ([100, 200, 300], 1000, None),
    ]

    for charges, total, expected in cases:
        found = find_refund_pair(charges, total)
        assert found == expected, (charges, total, found, expected)
        shown = "none" if found is None else f"{found[0]},{found[1]}"
        print(f"total {total:5d}  ->  {shown:>6}   from {charges}")

    print("All checks passed.")
```

**The change of question is the whole solution.**

```python
complement = refund_total - amount
if complement in earliest_at:
    return (earliest_at[complement], position)
```

"Which line pairs with this one" is a search, and a search over a list costs a
walk. "Have I already seen the number that pairs with this one" is a lookup, and
a lookup in a hash map costs almost nothing. The two questions have the same
answer and wildly different prices. Spotting that a search can be rewritten as a
lookup is what this entire week is teaching.

**The map remembers positions, not counts.** Its keys are amounts and its values
are the position each amount first appeared at. That is why the function can
return positions at all: the moment a complement is found, the map already knows
where its partner was standing.

**Lookup first, insert second, and the order is load-bearing.** On `[700, 700]`
with 1400 the first charge's complement is 700 — itself. If 700 were already in
the map at that moment, the function would return `(0, 0)`: one charge counted
twice, which is not a pair. Checking before inserting means position 0 can only
ever match something that came strictly earlier, and on the first iteration
nothing did.

**`if amount not in earliest_at` keeps the earliest position.** Without that
guard, the second `450` in `[100, 450, 450, 100]` overwrites position 1 with
position 2. The answer would still be a genuinely valid pair — `(2, 3)` does sum
to 550 — and it would still be the wrong one, because it completes at position 3
instead of position 1. This is the quietest class of bug on the page: correct
arithmetic, wrong selection.

**The loop returns the first match it finds, and that is exactly the tie-break
the contract asked for.** Walk it. The function scans positions left to right
and returns the moment a complement is found, so the `j` it returns is the
smallest `j` for which any partner exists. You never compare candidates or track
a best-so-far — the shape of the loop already answers the question. Notice how
often that happens once the data structure is right: the requirement disappears
into the algorithm instead of turning into an `if`.

**Returning `None` rather than a falsy stand-in is a real decision.** A caller
writing `if find_refund_pair(...)` would mishandle a legitimate `(0, 1)` if the
"nothing found" answer were `()` or `[]`, because an empty tuple is falsy and so
is `0`. `None` means *absence* and nothing else, and a caller has to write
`is None` to test for it — which is a sentence nobody writes by accident.

**The cost, said properly.** *Time `O(n)`*: one pass, each step doing one
subtraction, one membership test and at most one insert, all `O(1)` average on a
dict. *Space `O(n)` auxiliary*: the map holds at most one entry per distinct
amount, which is at most `n`; the returned tuple is `O(1)`. *Best case `O(1)`*:
if the first two charges pair, the function returns on the second iteration
having touched two elements. *Worst case* on a dict is `O(n)` per lookup under
adversarial collisions, which Python's randomised string hashing makes
unreachable in practice — say the sentence anyway, because being able to name
the worst case is what separates "I know dicts are fast" from "I know why".
*The alternative*: sort the charges and converge two pointers, which is
`O(n log n)` time — and worse than merely slower, sorting destroys the positions
the contract requires you to return, so it would need index tagging on top and
would still lose. *Improvement*: none. Any correct solution must read every
charge, so `O(n)` is the floor.

## Download and run

Download
[exercise-01-refund-pair-solution.py](./exercise-01-refund-pair-solution.py)
and run it:

```bash
python exercise-01-refund-pair-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-01-refund-pair.py`.

## Common bugs to catch

- **`TypeError: 'NoneType' object is not subscriptable`.** Your function fell
  off the end of a branch without returning a tuple, and then the self-check
  indexed the result:

  ```text
  Traceback (most recent call last):
      shown = "none" if found is None else f"{found[0]},{found[1]}"
                                             ~~~~~^^^
  TypeError: 'NoneType' object is not subscriptable
  ```

  A Python function that reaches its end returns `None` anyway, so this only
  fires when the caller expected a tuple. Usually it means one path through your
  `if` returns nothing at all.

- **`AssertionError` on `([700, 700], 1400)`.** You inserted before you looked
  up. The failing tuple in the assert tells you exactly what happened:

  ```text
  Traceback (most recent call last):
      assert found == expected, (charges, total, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([700, 700], 1400, (0, 0), (0, 1))
  ```

  `(0, 0)` is the charge at position 0 pairing with itself. Move the insert
  below the lookup.

- **`AssertionError` on `([100, 450, 450, 100], 550)`, got `(1, 3)`.** You wrote
  `earliest_at[amount] = position` with no guard, so the second `450` overwrote
  the first one's position. Both pairs are arithmetically valid; only one
  completes earliest. Add `if amount not in earliest_at`.

- **`AssertionError` on `([-200, 500, 200], 0)`, got `None`.** You added a
  shortcut like `if amount > refund_total: continue`. With negative charges on
  the list that reasoning does not hold — 500 is larger than the total of 0 and
  is still half of the answer. Delete the shortcut. An optimisation that changes
  the answer is not an optimisation.

- **`TypeError: unhashable type: 'list'`.** You used a list as a dict key, most
  likely by writing `earliest_at[charges]` instead of `earliest_at[amount]`:

  ```text
  Traceback (most recent call last):
      earliest_at[charges] = position
      ~~~~~~~~~~~^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  A dict key has to be hashable, and a list is not, because a list can change
  after you have filed it. Integers, strings and tuples can all be keys; lists,
  sets and dicts cannot.

- **The answer is right and the function is `O(n^2)`.** A nested loop passes all
  seven self-checks, because seven tiny inputs cannot tell the difference.
  Nothing on this page catches this for you — it is the one bug you have to
  catch by reading your own code. If your solution has two `for` loops, one
  inside the other, you solved a different exercise.

- **Returning the amounts instead of the positions.** `(400, 150)` instead of
  `(0, 1)`. Read the return annotation. The support agent needs to know *which
  lines* to look at; the amounts they already have.

## Under the hood

<details>
<summary>Under the hood — why a dict lookup is O(1), and what the word "average" is doing in that sentence</summary>

**A dict is an array you address by arithmetic instead of by counting.**

Take the key `400`. Python computes `hash(400)`, which for a small integer is
just `400`, and uses some bits of that number to pick a slot in an internal
array. Going to slot 400-ish takes the same time as going to slot 3: the machine
computes an address and jumps there. That is why the cost does not grow with how
much is in the map. Nothing was searched.

**Two keys can want the same slot, and that is called a collision.** If the
array has 8 slots, `400` and `408` might both land on slot 0. CPython handles
that by *open addressing*: it probes a sequence of other slots until it finds a
free one, or finds the key it was looking for. The probe sequence is derived
from the full hash rather than from "try the next one along", so unrelated keys
do not pile up behind each other.

**That is where the word "average" comes from.** If every key in your map
collided with every other, each lookup would degrade into walking a chain and
the cost would be `O(n)`. That is the honest worst case and you should be able
to say it. It does not happen by accident: the number of slots grows with the
number of entries — CPython resizes when the table is around two-thirds full —
so collisions stay rare. It could in principle be made to happen *on purpose*,
by an attacker choosing keys that all collide, which is why Python randomises
string hashing once per process so that nobody can precompute such a set.
Integer hashes are not randomised, since the hash of a small integer is the
integer, so a pathological integer key set is constructible in theory. It is a
curiosity, not something you will meet.

**Resizing is where "amortised" earns its keep.** When the table gets too full,
Python allocates a bigger one and refiles every entry into it. That single
insert is expensive — `O(n)` — while every other insert is cheap. Because the
table roughly doubles each time, the expensive inserts get rarer exactly as fast
as they get costlier, and the average over the whole run stays constant. The
word for "expensive rarely, cheap usually, constant on average" is
**amortised**, and it is the same argument that makes `list.append` cheap. Say
"amortised O(1)" for inserts and plain "O(1) average" for lookups and you are
saying something precise rather than something remembered.

**Hashing the key is not free when the key is big.** `hash(400)` is. `hash("a
two-hundred-character route code")` is not — it reads the whole string. So "dict
lookups are O(1)" quietly means "O(1) in the number of entries, O(k) in the size
of the key". With small integer keys, as here, there is nothing to say. With
long strings there is, and
[Challenge 2](../challenges/challenge-02-residency-board.md) comes back to it.

**Why this is `O(n)` space and not `O(100_001)`.** The map holds one entry per
*distinct amount that actually appeared*, not one per amount that could have. The
charge range is 100,001 values wide, and on a six-charge history the map holds at
most six entries. That distinction — space proportional to the data, not to the
range — is why a hash map is the right tool here and a flag array indexed by
amount is not. Exercise 2's ID range makes the same point ten million times
louder.

</details>

## Acceptance checklist

- [ ] `python exercise-01-refund-pair.py` prints seven rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] Your solution contains exactly one loop.
- [ ] The map lookup happens **before** the insert.
- [ ] The insert is guarded so an amount's earliest position is never overwritten.
- [ ] No pair is ever formed from one position with itself.
- [ ] The function returns `None`, not a falsy stand-in, when no pair exists.
- [ ] You can say the time and space sentence out loud without reading it.
- [ ] Committed to Git with a message like `Add Week 2 exercise 1: refund pair`.

## Stretch

- **Return every earliest-completing pair, not just one.** Change the contract:
  if several pairs complete at the same smallest `j`, return all of them.

  ```python
  def all_refund_pairs_at_earliest(
      charges: list[int], refund_total: int
  ) -> list[tuple[int, int]]:
      """Return every pair that completes at the smallest possible later position."""
      positions_of: dict[int, list[int]] = {}
      for position, amount in enumerate(charges):
          complement = refund_total - amount
          if complement in positions_of:
              return [(earlier, position) for earlier in positions_of[complement]]
          positions_of.setdefault(amount, []).append(position)
      return []

  print(all_refund_pairs_at_earliest([100, 100, 200], 300))
  print(all_refund_pairs_at_earliest([400, 150, 250, 300], 550))
  ```

  ```text
  [(0, 2), (1, 2)]
  [(0, 1)]
  ```

  The map's value went from one position to a list of positions, and the guard
  that kept the earliest one disappeared, because now you want them all. The
  cost did not change: still one pass, still `O(n)` time, still `O(n)` space —
  the lists together hold `n` positions in total, not `n` per key.

- **Count the pairs instead of finding one.** How many distinct `(i, j)` pairs
  sum to the total?

  ```python
  def count_refund_pairs(charges: list[int], refund_total: int) -> int:
      """Return how many distinct position pairs sum to the refund total."""
      times_seen: dict[int, int] = {}
      pairs = 0
      for amount in charges:
          pairs += times_seen.get(refund_total - amount, 0)
          times_seen[amount] = times_seen.get(amount, 0) + 1
      return pairs

  print(count_refund_pairs([100, 100, 200, 200], 300))
  print(count_refund_pairs([150, 150, 150], 300))
  ```

  ```text
  4
  3
  ```

  The map now stores a **frequency** rather than a position, and there is no
  early return, because a count needs every charge. Hold on to that shape: it is
  exactly the map that
  [Challenge 1](../challenges/challenge-01-balanced-shifts.md) needs, where one
  map has to carry a frequency *and* a position at the same time.

- **Prove the nested version is slow rather than assuming it.** That is
  [Homework Problem 2](../homework/problem-02-time-the-gap.md), and it is the
  most valuable forty-five minutes of the week. Write both versions, count the
  comparisons, and watch the two columns come apart.
Next: [Exercise 2 — The Repeated Badge](./exercise-02-badge-rescan.md).
