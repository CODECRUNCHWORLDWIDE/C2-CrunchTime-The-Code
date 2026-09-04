# Problem 3 — The Symmetric Die Sequence

> **Topic:** the fast/slow lower middle and an in-place reversal, composed — then put back exactly as found
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §5
> **Difficulty:** Medium
> **Target time:** 45 minutes, including the FRAME write-up
> **Why this one:** two of its three sub-steps are identical to this week's [booklet challenge](../challenges/challenge-01-booklet-imposition.md). Recognising that, and saying so out loud before you write anything, is the transfer this problem is testing. The third sub-step is different, and so is the requirement to leave the machine as you found it.

## The Brief

A stamping press runs a chain of dies in order. Each die presses one shape into
the metal as the strip passes under it.

When the strip jams, the operator clears it by running the press **backwards**.
That is only safe if the die sequence reads the same backwards as forwards —
otherwise the reverse pass stamps the wrong shapes into metal that already has
shapes in it, and the whole strip is scrap.

A sequence that reads the same in either direction is **symmetric**. `A B B A`
is symmetric. `A B C B A` is symmetric, with `C` alone in the middle and no
partner. `A B C A` is not.

The controller's safety check has to answer more than yes or no. A bare "not
safe" sends a technician to inspect the entire press. What they need is
**which die to pull** — so return the **position of the first die, counted from
the front, that does not match its mirror partner**. Return `-1` if the whole
sequence is symmetric.

Here is what a mirror partner is. Pair the first die with the last, the second
with the second-to-last, and so on, working inwards. Those are the pairs that
have to agree.

**One example that decides the contract.** `A B C A` has two pairs: position 0
against position 3, which both read `A` and agree; and position 1 against
position 2, which read `B` and `C` and do not. So the answer is `1` — the
smaller of the two positions in the failing pair, because the spec says
*counted from the front*. Answering `2` is the obvious wrong reading and it is
in the check list for that reason.

**And one requirement that is normally an afterthought.** The chain must be in
its original order when the function returns. Reversing half of it is the
expected technique, so reversing it back is part of the job. A press controller
that leaves the die chain scrambled after a safety check has turned a safety
check into a fault. This is usually asked as an interview follow-up; here it is
in the spec and it is graded.

## Starter

Create `problem-03-symmetric-dies.py` and paste this in. Fill in every `TODO`.

```python
"""problem-03-symmetric-dies.py — where does the mirror break?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per die sequence and then "All checks passed." when the module is
right.
"""

from __future__ import annotations


class Die:
    """One stamping die, in press order."""

    def __init__(self, code: str, next_die: "Die | None" = None) -> None:
        self.code = code
        self.next_die = next_die


def build_press(codes: list[str]) -> Die | None:
    """Wire a die chain from a list of codes.

    Args:
        codes: One code per die, in press order. Codes repeat freely.

    Returns:
        The first die, or None for an empty press.
    """
    if not codes:
        return None
    dies = [Die(code) for code in codes]
    for earlier, later in zip(dies, dies[1:]):
        earlier.next_die = later
    return dies[0]


def press_codes(first: Die | None) -> list[str]:
    """Walk a die chain into a list of codes, in press order."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.code)
        first = first.next_die
    return codes


def _lower_middle(first: Die) -> Die:
    """Return the last die of the front half — the earlier of two middles."""
    # TODO 1: Exercise 3, with `next_die` instead of `next_segment`.
    ...


def _reverse(first: Die | None) -> Die | None:
    """Turn a die chain around in place and return its new first die."""
    # TODO 2: three names — previous, current, following — and one loop.
    ...


def first_mirror_break(first: Die | None) -> int:
    """Return the position of the first die that differs from its mirror.

    Args:
        first: The first die of the press chain, or None for an empty press.

    Returns:
        The 0-based position, counted from the front, of the first die whose
        mirror partner carries a different code, or -1 when the whole
        sequence reads the same in either direction. The chain is left in
        its original order either way.
    """
    # TODO 3: an empty press and a one-die press are both symmetric.
    # TODO 4: find the lower middle and cut after it.
    # TODO 5: reverse the back half, then walk the two halves side by side,
    #         counting from 0, and stop at the first pair that disagrees.
    # TODO 6: put the press back together BEFORE returning — on every path,
    #         including the one that found a break.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["A", "B", "B", "A"], -1),
        (["A", "B", "C", "B", "A"], -1),
        (["A"], -1),
        ([], -1),
        (["A", "B"], 0),
        (["A", "B", "C", "A"], 1),
        (["A", "B", "B", "C"], 0),
        (["X", "Y", "Z", "Y", "X", "Q"], 0),
    ]

    for codes, expected in CASES:
        press = build_press(codes)
        found = first_mirror_break(press)
        assert found == expected, f"{codes}: got {found}, wanted {expected}"
        assert press_codes(press) == codes, f"{codes}: the press was left scrambled"
        verdict = "symmetric" if found == -1 else f"breaks at position {found}"
        print(f"{str(codes):<36} {verdict}")

    long_press = build_press(["S"] * 9999 + ["T"])
    assert first_mirror_break(long_press) == 0
    assert len(press_codes(long_press)) == 10_000
    print(f"{'10000 dies, one odd one at the end':<36} breaks at position 0")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/homework/problem-03-symmetric-dies.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `first_mirror_break(first)` returns the 0-based position, counted from the
   front, of the first die whose mirror partner differs — or `-1`.
2. `A B C A` returns `1`, not `2`. The position counted from the front is the
   smaller index of the failing pair.
3. An empty press and a one-die press both return `-1`.
4. **The chain is in its original order when the function returns**, on every
   path out of it, including the path that found a break.
5. Fixed memory. No list of codes, no stack of the first half, no copy.
6. The reversal is iterative. See the Constraints for why.
7. `first_mirror_break` keeps its type hints and its docstring.

## Constraints

- **The chain must be restored, and this is graded.** The technique reverses
  half the chain, so putting it back is part of the job rather than a courtesy.
  Your own test must assert the restoration, not just the return value — the
  self-check above does exactly that after every single case, which is why a
  solution that restores only on the symmetric path fails on the fifth case
  rather than the one that broke it.

- **Fixed memory, because the controller has a fixed frame budget per safety
  check.** Walking the codes into a list and comparing `codes ==
  codes[::-1]` is three lines and obviously correct. It is O(n) space and it is
  rejected. Same sentence as everywhere this week: not slower, does not fit.

- **Up to 20,000 dies, and that bound is chosen to break one solution.** A
  recursive comparison of the halves, or a recursive reversal, pushes about
  `n / 2` frames. At 20,000 dies that is 10,000 frames against CPython's
  default limit of 1,000, so the recursive version does not run slowly — it
  raises `RecursionError`. As in
  [Challenge 1](../challenges/challenge-01-booklet-imposition.md), the size is
  picked to make the recursion a hard failure rather than an inelegance.

- **Die codes repeat freely.** A code appearing twice tells you nothing about
  position. The 10,000-die check is nine thousand nine hundred and ninety-nine
  dies coded `S` and one coded `T`, and the answer is still position `0` —
  because position 0's mirror partner is the last die.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-symmetric-dies.py
['A', 'B', 'B', 'A']                 symmetric
['A', 'B', 'C', 'B', 'A']            symmetric
['A']                                symmetric
[]                                   symmetric
['A', 'B']                           breaks at position 0
['A', 'B', 'C', 'A']                 breaks at position 1
['A', 'B', 'B', 'C']                 breaks at position 0
['X', 'Y', 'Z', 'Y', 'X', 'Q']       breaks at position 0
10000 dies, one odd one at the end   breaks at position 0
All checks passed.
```

The last two lines before the long run are the ones to study.
`["A", "B", "B", "C"]` breaks at `0` even though the inner pair matches — the
break is at the *outermost* failing pair, not the first one you would notice
reading left to right. And `["X", "Y", "Z", "Y", "X", "Q"]` breaks at `0` too:
a sequence that is symmetric except for one extra die on the end still fails at
position 0, because position 0's partner is now `Q`. If you want to answer `5`
there, re-read the contract.

## Steps

1. **Frame.** Restate. Say what a mirror partner is, out loud, and walk
   `A B C A` to show why the answer is `1` and not `2`. Confirm the empty and
   one-die cases. Confirm the restoration requirement and say it back as *the
   press must be exactly as I found it*.
2. **Research constraints.** Name the frame budget and what it rejects. Name
   the 20,000-die bound and do the recursion arithmetic. Note that codes repeat.
3. **Assess options, and this is the graded step.** Say the decomposition, and
   say explicitly that two of its three sub-steps are the booklet challenge's:

   > "Three sub-steps, and the first two are Challenge 1's. Find the lower
   > middle with fast and slow, and cut after it, so the front half is the
   > longer one. Reverse the back half in place, iteratively — 20,000 dies
   > against a 1,000-frame limit. The third sub-step is where this differs:
   > instead of zipping the halves together, walk them side by side comparing
   > codes and counting from zero, and stop at the first pair that disagrees.
   > Then reverse the back half again and reattach it, on every path out."

4. **Make the solution, helpers first.** `_lower_middle` and `_reverse` are
   copies. Say out loud that you are copying them rather than deriving them
   again — reuse you can name is a strength, reuse you hide is not.
5. **Make the solution, the comparison walk.** Count from 0. Stop when the back
   half runs out, not when the front half does. Work out why before you write
   it, and see the Solution if you get stuck.
6. **Make the solution, the restoration.** One line, placed after the loop and
   before the return, so both paths go through it.
7. **Examine, odd length.** Trace `A B C B A`. Lower middle: position 2, the
   `C`. Front half `A B C`, back half `B A`, reversed to `A B`. Compare: `A`
   against `A`, position 0, agree; `B` against `B`, position 1, agree; the back
   half runs out. Answer `-1`. Notice the `C` was never compared — it has no
   partner, and the back half running out is what skips it.
8. **Examine, even length.** Trace `A B C A`. Lower middle: position 1, the
   `B`. Front half `A B`, back half `C A`, reversed to `A C`. Compare: `A`
   against `A`, position 0, agree; `B` against `C`, position 1, disagree.
   Answer `1`. ✓
9. **Examine, restoration.** After returning `1`, walk the chain from the head
   and confirm you get `A B C A` back. The self-check does this for you after
   every case; do it once by hand so you know what it is checking.
10. **Examine, cost.** O(n) time — three linear passes plus one more to restore.
    O(1) space — a fixed number of die variables.

## The Solution

```python
"""problem-03-symmetric-dies-solution.py — where does the mirror break?

Same first two moves as this week's booklet challenge: find the earlier of
the two middle dies, cut there, and turn the back half around. Only the
third move differs. Instead of zipping the halves together, walk them side
by side and stop at the first pair whose codes disagree.

Then put the press back the way you found it. A safety check that leaves the
die chain scrambled has become a fault.

The chains are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per die sequence, then
"All checks passed."
"""

from __future__ import annotations


class Die:
    """One stamping die, in press order."""

    def __init__(self, code: str, next_die: "Die | None" = None) -> None:
        self.code = code
        self.next_die = next_die


def build_press(codes: list[str]) -> Die | None:
    """Wire a die chain from a list of codes.

    Args:
        codes: One code per die, in press order. Codes repeat freely.

    Returns:
        The first die, or None for an empty press.
    """
    if not codes:
        return None
    dies = [Die(code) for code in codes]
    for earlier, later in zip(dies, dies[1:]):
        earlier.next_die = later
    return dies[0]


def press_codes(first: Die | None) -> list[str]:
    """Walk a die chain into a list of codes, in press order."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.code)
        first = first.next_die
    return codes


def _lower_middle(first: Die) -> Die:
    """Return the last die of the front half — the earlier of two middles."""
    slow = first
    fast = first
    while fast.next_die is not None and fast.next_die.next_die is not None:
        slow = slow.next_die
        fast = fast.next_die.next_die
    return slow


def _reverse(first: Die | None) -> Die | None:
    """Turn a die chain around in place and return its new first die."""
    previous = None
    current = first
    while current is not None:
        following = current.next_die
        current.next_die = previous
        previous = current
        current = following
    return previous


def first_mirror_break(first: Die | None) -> int:
    """Return the position of the first die that differs from its mirror.

    Args:
        first: The first die of the press chain, or None for an empty press.

    Returns:
        The 0-based position, counted from the front, of the first die whose
        mirror partner carries a different code, or -1 when the whole
        sequence reads the same in either direction. The chain is left in
        its original order either way.
    """
    if first is None or first.next_die is None:
        return -1

    middle = _lower_middle(first)
    back = middle.next_die
    middle.next_die = None
    turned = _reverse(back)

    front_walk: Die | None = first
    back_walk = turned
    position = 0
    answer = -1
    while back_walk is not None:
        if front_walk.code != back_walk.code:
            answer = position
            break
        front_walk = front_walk.next_die
        back_walk = back_walk.next_die
        position += 1

    middle.next_die = _reverse(turned)
    return answer


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["A", "B", "B", "A"], -1),
        (["A", "B", "C", "B", "A"], -1),
        (["A"], -1),
        ([], -1),
        (["A", "B"], 0),
        (["A", "B", "C", "A"], 1),
        (["A", "B", "B", "C"], 0),
        (["X", "Y", "Z", "Y", "X", "Q"], 0),
    ]

    for codes, expected in CASES:
        press = build_press(codes)
        found = first_mirror_break(press)
        assert found == expected, f"{codes}: got {found}, wanted {expected}"
        assert press_codes(press) == codes, f"{codes}: the press was left scrambled"
        verdict = "symmetric" if found == -1 else f"breaks at position {found}"
        print(f"{str(codes):<36} {verdict}")

    long_press = build_press(["S"] * 9999 + ["T"])
    assert first_mirror_break(long_press) == 0
    assert len(press_codes(long_press)) == 10_000
    print(f"{'10000 dies, one odd one at the end':<36} breaks at position 0")

    print("All checks passed.")
```

**The decomposition, and the two-thirds you already own.** Finding the lower
middle is [Exercise 3](../exercises/exercise-03-midroll-break.md). Reversing a
chain in place is
[Challenge 1](../challenges/challenge-01-booklet-imposition.md)'s second
sub-step. Neither needed rethinking; both needed renaming an attribute. What is
new here is comparing rather than zipping, and putting the chain back.

Saying that out loud is the point of the problem. In a real interview,
recognising that a new problem is two-thirds of one you solved yesterday is
worth more than solving it from scratch — and it is audible on a recording in a
way that correctness is not.

**Why the loop stops on the back half.**

```python
    while back_walk is not None:
```

The lower middle makes the front half `ceil(n / 2)` dies and the back half
`floor(n / 2)`, so the front half is never shorter. On an even count they are
the same length and either would do. On an odd count the front half has one
extra die — the lone middle — and that die has no mirror partner, so it must
not be compared. Stopping when the back half runs out skips it for free.

Stop on the front half instead and, on an odd count, you would compare the lone
middle against `None` and crash. The asymmetry in the halves is not an accident
of the algorithm; it is what the termination condition is built on.

**Positions count from the front, which is why `position` sits on the front
walker.** Both walkers step together, so a single counter describes both — but
the number it names is the front walker's index, and the contract asks for that
one. `A B C A` breaks at `1`, the `B`, not at `2`, the `C`. The pair is the same
pair either way; the spec picks which end to name it from.

**The cut and the restoration are one thought split in two.**

```python
    middle.next_die = None
    ...
    middle.next_die = _reverse(turned)
```

Cutting is what lets the reversal touch only the back half. Reversing the
already-reversed back half turns it the right way round again, and assigning it
back to `middle.next_die` closes the gap the cut opened. Both lines refer to
`middle`, which is why `middle` has to survive the whole function rather than
being a temporary inside a helper.

**The restoration is placed after the loop, not inside the branches.** There is
exactly one `return` in this function, and the line before it puts the chain
back. That is deliberate. Write the restoration inside the symmetric path and
the press stays scrambled on precisely the input where a technician is about to
touch it — and the tests that check the return value would all still pass. This
is the shape of bug that ships.

**Two guards, not one.** `first is None` and `first.next_die is None` are both
handled up front. The first is because `_lower_middle` reads inside `fast` on
its very first evaluation, the same trap as
[Exercise 3](../exercises/exercise-03-midroll-break.md). The second is not
strictly necessary — a one-die chain has an empty back half and the loop never
runs — but it says the intent plainly and costs nothing.

**Nothing here grows with the press.** `middle`, `back`, `turned`,
`front_walk`, `back_walk`, and two integers. The controller's frame budget is
honoured.

## Run it

Copy the worked answer on this page into `problem-03-symmetric-dies.py` and run it:

```bash
python problem-03-symmetric-dies.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-03-symmetric-dies.py`.

## Common bugs to catch

- **Leaving the press scrambled on the break path.** The classic version of this
  bug restores only when the sequence turns out symmetric. Every return-value
  test still passes; the chain is wrong. The self-check catches it on the fifth
  case:

  ```text
  Traceback (most recent call last):
      assert press_codes(press) == codes, f"{codes}: the press was left scrambled"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: ['A', 'B']: the press was left scrambled
  ```

- **`AttributeError: 'NoneType' object has no attribute 'next_die'`.** Two
  likely causes. Either the empty press reached `_lower_middle`, whose guard
  reads inside `fast` immediately, or your comparison loop stops on the front
  half and walked past the end on an odd count:

  ```text
  Traceback (most recent call last):
      while fast.next_die is not None and fast.next_die.next_die is not None:
            ^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'next_die'
  ```

- **`RecursionError: maximum recursion depth exceeded`.** Your reversal or your
  comparison is recursive:

  ```text
  Traceback (most recent call last):
      return rev(nxt, node)
    [Previous line repeated 994 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  20,000 dies against a 1,000-frame limit. The bound exists to make this a
  failure rather than a style note.

- **Returning the wrong end of the failing pair.** `A B C A` gives `2` instead
  of `1`. You reported the back walker's position, or counted the pair from the
  back. The contract says counted from the front, and `A B C A` is in the list
  for exactly this.

- **Answering `5` for `X Y Z Y X Q`.** You looked for the die that "spoils" a
  sequence that is otherwise symmetric. That is a different question. Position
  0's mirror partner is the last die, which is `Q`, so the very first pair
  fails.

- **Comparing dies with `is` instead of comparing codes with `==`.** These are
  two different die objects that must carry the same *code*. `front_walk is
  back_walk` is only ever true in the middle of an odd chain, so a solution
  using `is` reports a break at position 0 on every input including `A B B A`.
  Identity for the chain's structure, equality for the values it carries — the
  same split you drew in [Exercise 4](../exercises/exercise-04-wear-level-rotation.md).

- **Forgetting the lone middle has no partner.** On `A B C B A`, comparing all
  three front dies against a back half of two either crashes or, if you
  guarded it, reports a false break at position 2.

## Under the hood

<details>
<summary>Under the hood — the O(n)-space versions, and what "restore it" costs</summary>

**The two versions the controller cannot run, for comparison.**

```python
def is_symmetric_with_a_list(first: Die | None) -> int:
    """The O(n)-space version: walk the codes out and compare both ways."""
    codes = press_codes(first)
    for position, (front, back) in enumerate(zip(codes, reversed(codes))):
        if front != back:
            return position
    return -1
```

Five lines, obviously correct, never touches the chain, and needs a list as long
as the press. There is also a half-as-hungry version that pushes only the front
half onto a stack and then compares the back half against it — O(n / 2), which
is still O(n). On a server, take the five-line one. Say that out loud, then say
why the controller cannot.

**Restoring costs one extra pass, and it is worth naming that.** The comparison
itself is three passes: find the middle, reverse, compare. Restoring adds a
fourth. All four are linear, so the total is still O(n), but the constant went
from three to four — a 33% increase in traversals for a requirement that is
often waved away as an afterthought. When an interviewer asks "could you also
restore the list?", the honest answer is "yes, one more pass, and here is where
it goes" rather than "yes, trivially".

**Why the front half being the longer one matters here and not everywhere.**
It matters because the loop terminates on the back half. If you had built the
halves the other way round — upper middle, back half longer — you would have to
terminate on the front half and then explicitly skip the back half's extra die.
Same answer, more code, more places to be wrong. Choosing the split so that the
awkward leftover ends up on the side you are *not* testing is a small design
decision that removes a branch, and noticing you made it is worth a line in
your write-up.

**Where the composition goes next.** Change the third sub-step again and you get
other problems for free: zip the halves and you have
[Challenge 1](../challenges/challenge-01-booklet-imposition.md); return the two
halves and you have the split a merge sort on a chain needs; compare while
summing and you have "is this sequence its own reverse under some
transformation". The first two sub-steps are a reusable primitive — *give me
the second half, backwards, in place* — and it is worth naming it as one.

</details>

## Acceptance checklist

- [ ] `python problem-03-symmetric-dies.py` prints nine lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] The chain is restored on **every** path, and your own test asserts it.
- [ ] `A B C A` returns `1`.
- [ ] `X Y Z Y X Q` returns `0`.
- [ ] The comparison loop terminates on the back half, and you can say why in
      one sentence involving odd lengths.
- [ ] Everything is iterative; no recursion anywhere.
- [ ] No list of codes, no stack, no copy of the chain.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/hw-03-symmetric-dies.md`,
      and its Assess-options section compares this with the booklet challenge —
      same first two sub-steps, different third.

## Stretch

- **Return every break, not just the first.** The technician would rather pull
  three dies in one visit than come back twice. Collect the positions instead of
  stopping — and notice that this version needs O(number of breaks) memory to
  return the answer, which is a genuinely different space claim from the one on
  this page.

  ```text
  ['A', 'B', 'C', 'A']                 breaks at [1]
  ['A', 'B', 'B', 'C']                 breaks at [0]
  ['A', 'X', 'Y', 'C']                 breaks at [0, 1]
  ```

- **Report the pair, not just the position.** Return
  `(position, front code, back code)` so the log says what was expected and what
  was found. It is two extra names and it makes the output far more useful to
  someone who cannot see the press.

  ```text
  ['A', 'B', 'C', 'A']                 position 1: front 'B', mirror 'C'
  ['X', 'Y', 'Z', 'Y', 'X', 'Q']       position 0: front 'X', mirror 'Q'
  ```

- **Pull out the shared primitive.** Write `second_half_reversed(first)` that
  returns `(middle, reversed_back)`, and rebuild both this problem and
  [Challenge 1](../challenges/challenge-01-booklet-imposition.md) on top of it.
  Two problems, one primitive, and the diff between them is the third sub-step —
  which is the clearest possible demonstration that you saw the shared structure.
Next: [Problem 4 — Behavioral Story #4](./problem-04-behavioral-story.md).
