# Exercise 2 — The Longest Clean Run

> **Topic:** a variable-size window that grows on the right and jumps on the left, with a "no repeats" invariant
> **Lecture:** [02 — The Shrinking and Growing Mechanics](../lecture-notes/02-the-shrinking-and-growing-mechanics.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the first window whose width is not handed to you — it stretches and snaps back depending on what it finds. This is the shape you will reuse more than any other. It also asks for a **span** rather than a length, which is where most people discover their loop was never actually keeping track of *where* the best window was.

## The Brief

A stamping press punches parts out of metal. Every part gets marked with the ID
number of the **die** — the shaped tool — that made it, and the line writes
those IDs down in the order the parts came off. So the log is a list of
numbers, one per part, and the number is which tool stamped it.

Dies wear out. Between recalibrations, the same die must not be used twice, so
a stretch of consecutive parts is called a **clean run** when no die ID appears
in it more than once. `[9, 3, 4, 1]` is clean. `[9, 3, 9]` is not, because die
9 turns up twice.

**Your job.** Find the longest clean run and return **where it is**, not how
long it is.

The way to say "where" in Python is a **half-open span**: a pair `(start, end)`
where `start` is the first position and `end` is one past the last. It is
exactly what goes inside the square brackets of a slice, so `stamps[start:end]`
hands the caller the run itself with nothing to adjust. Half-open looks odd
until you notice two things it gives you for free: the length is just
`end - start`, and the empty run is `(0, 0)` rather than something with a minus
sign in it.

Now the technique. The window here is not a fixed-width piece of card any more.
It is elastic. You push its right edge forward one part at a time. Most of the
time nothing is wrong and the window just gets longer. But the moment the part
you added repeats a die that is **already inside the window**, the window is no
longer clean, and the only way to fix that is to pull the left edge forward
past the earlier copy.

The thing that makes this fast is that the left edge **never goes backwards**.
It only ever jumps forward. So across the whole log the right edge moves `n`
times and the left edge moves at most `n` times, and the total work is
proportional to `n` even though there is a jump inside the loop.

One trap is worth naming before you start, because nearly everyone hits it.
You will keep a dictionary remembering where each die was last seen. When a die
repeats, you move the left edge past its previous position. But a die may have
been seen *before the window started* — it is in your dictionary and it is not
in your window. Moving the left edge for that one drags it **backwards**, and a
backwards left edge means the window silently contains a duplicate and reports
a length it does not have.

**The contract.** Return the longest clean run as `(start, end)`. If several
clean runs tie on length, return the one with the **smallest** start. If the
log is empty, return `(0, 0)` — an empty run has no repeats in it, so it is
trivially clean, and this is a span rather than a `None`.

## Starter

Create `exercise-02-longest-clean-run.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-02-longest-clean-run.py — the longest clean run.

Find the longest stretch of consecutive parts in which no die ID repeats, and
return where it is as a half-open span.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def longest_clean_run(stamps: list[int]) -> tuple[int, int]:
    """Return the longest stretch of parts with no repeated die ID.

    Args:
        stamps: Die IDs, one per part, in production order.

    Returns:
        A half-open span (start, end) with stamps[start:end] the longest clean
        run. Ties go to the smaller start. An empty log returns (0, 0).
    """
    # TODO: a dict mapping each die ID to the last index it was seen at,
    #       a `left` edge starting at 0, and a best span starting at (0, 0).
    # TODO: walk `right` over the log with enumerate.
    #       - if this die was seen before AND that sighting is at or after
    #         `left`, the copy is inside the window: move `left` past it.
    #       - record this sighting, whether or not you moved.
    #       - if the window is now strictly longer than the best so far,
    #         remember it as a half-open span.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    logs: list[list[int]] = [
        [7, 3, 9, 3, 4, 1, 9],
        [1, 2, 2, 1],
        [2, 1, 2, 3],
        [5, 5, 5, 5],
        [4],
        [],
    ]
    for log in logs:
        start, end = longest_clean_run(log)
        print(f"{str(log):<22} -> span ({start}, {end}) = {log[start:end]}")
    print()

    assert longest_clean_run([7, 3, 9, 3, 4, 1, 9]) == (2, 6)
    assert longest_clean_run([1, 2, 2, 1]) == (0, 2)
    assert longest_clean_run([2, 1, 2, 3]) == (1, 4)
    assert longest_clean_run([5, 5, 5, 5]) == (0, 1)
    assert longest_clean_run([4]) == (0, 1)
    assert longest_clean_run([]) == (0, 0)

    # Whatever span comes back really is clean, and really is maximal.
    for log in logs:
        start, end = longest_clean_run(log)
        run = log[start:end]
        assert len(set(run)) == len(run), f"{run} repeats a die"
        for begin in range(len(log)):
            for stop in range(begin + 1, len(log) + 1):
                candidate = log[begin:stop]
                if len(set(candidate)) == len(candidate):
                    assert len(candidate) <= end - start

    print("All checks passed.")
```

Two words you need before you start.

**Invariant.** The promise the loop keeps. Here it is: *every die ID in
`stamps[left .. right]` is different from every other.* Your job each step is
to add one part and then, if you have broken the promise, do the smallest thing
that restores it.

**Amortised.** A cost that is small *on average across the whole run*, even
though one individual step can be big. The left edge can jump five places in
one iteration — but it can only ever do that by using up five places it will
never visit again. Add all the jumps together and they come to at most `n`.
"One step can be slow, all the steps together cannot" is the argument, and you
will use it every week from here.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/exercises/exercise-02-longest-clean-run.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `longest_clean_run(stamps)` returns a **half-open span**, so
   `stamps[start:end]` is the run. On `[4]` the answer is `(0, 1)`, never
   `(0, 0)`.
2. Ties on length go to the **smaller** start. `longest_clean_run([7, 3, 9, 3, 4, 1, 9])`
   is `(2, 6)`, not `(3, 7)`.
3. An empty log returns `(0, 0)`, not `None`.
4. `left` never decreases. A die last seen before the window began must not
   move it.
5. Distinctness is maintained incrementally. Nothing inside the loop may build
   a `set` of a slice.
6. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(stamps) <= 300_000`.** A month of press output. The size is
  chosen to reject the obvious brute force — "for every start, walk right until
  a repeat, using a fresh set" — which is about `4.5 x 10^10` set operations
  here and will not finish this afternoon. It is also small enough that the
  linear solution is instant, so if your program hangs, you picked the wrong
  shape rather than writing slow Python.

- **`1 <= stamps[i] <= 10_000`.** Die IDs are catalogue numbers from a tool crib
  that holds ten thousand tools. This bound earns its place in the cost
  argument: it lets you say the dictionary holds at most `min(n, 10_000)`
  entries, so the space claim is that rather than a vague `O(n)`. Being able to
  state the tighter bound, and say which of the two numbers is the binding one
  for a given input, is the kind of precision an interviewer notices.

- **IDs are positive, so `0` is never a valid die ID.** That leaves `0` free as
  a marker if you want one. You will not need one — `dict.get` returning `None`
  says "never seen" perfectly well — but knowing the value is available is part
  of reading a spec.

- **The left edge moves forward only.** This is a rule about your loop, and it
  is what makes the whole thing linear. If you find yourself computing
  `left = something` without checking that the something is ahead of where you
  already are, stop.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-longest-clean-run.py
placeholder
```

Look at the second row. `[1, 2, 2, 1]` has two clean runs of length 2 —
`[1, 2]` at the front and `[2, 1]` at the back — and the answer is the earlier
one. Look at the fourth row too: every run of two parts in `[5, 5, 5, 5]`
already repeats, so the longest clean run is a single part, and the tie-break
picks the first.

## Steps

1. Create the file, paste the starter, and run it. Every line prints `(0, 0)`
   and the first assert fails. That is the correct starting point.
2. Set up your three pieces of state before the loop: the dictionary, `left`,
   and `best`.
3. Write the loop with `for right, die in enumerate(stamps)`. Getting the index
   and the value together is worth the extra word.
4. Look the die up. `last_index.get(die)` gives you `None` if it has never been
   seen — which is different from `0`, and the difference matters, because `0`
   is a real index.
5. Write the guard. You move `left` only when the previous sighting is **at or
   after** `left`. Say the condition out loud in English before you type it:
   *"if I have seen this die, and I saw it inside the window I am currently
   holding."*
6. Record the sighting. This happens on every iteration, jump or no jump.
7. Compare and record the best. The tie-break decides the operator. Read
   Requirement 2 again first.
8. Trace `[1, 2, 2, 1]` by hand, on paper, one row per step, with columns for
   `right`, `die`, `left`, the window, and `best`. It is four rows and it is
   the single most useful five minutes on this page.

## The Solution

```python
placeholder
```

**Three pieces of state, and each has exactly one job.**

`last_index` remembers where every die was last seen. `left` is the window's
left edge. `best` is the longest clean span found so far, stored as the answer
type rather than as a length, so there is nothing to reconstruct at the end.
Storing the best as a length and trying to work out the span afterwards is the
most common way this problem goes wrong.

**The guard is the whole exercise.**

```python
if seen_at is not None and seen_at >= left:
    left = seen_at + 1
```

Two conditions, and both are load-bearing. `is not None` asks *have I ever seen
this die*. `>= left` asks *and was that sighting inside the window I am holding
right now*. A die seen at index 0 while the window starts at index 2 is a die
that has already been left behind: it is not in the window, it cannot have
broken anything, and moving `left` for it would drag the edge backwards.

Watch what happens on `[1, 2, 2, 1]` without the second condition. At the last
part, die 1 was last seen at index 0, so `left` becomes 1 — but the window had
already moved on to index 2. Now the window is `[2, 2, 1]`, which contains a
repeat, and the code cheerfully reports a clean run of length 3. No exception,
no warning, just a wrong answer that looks right.

**`is not None`, not a plain truth test.** `if seen_at and ...` is wrong here,
because a die last seen at index `0` gives `seen_at = 0`, and `0` is falsy.
That single character turns a real sighting at the very start of the log into
"never seen". Any time a dictionary's values are indices, `is not None` is the
test you want.

**Recording the sighting happens every time.**

```python
last_index[die] = right
```

Outside the `if`, unconditionally, whether or not the edge moved. The
dictionary is a record of *the most recent* sighting of every die you have ever
passed, not just the ones that caused trouble. Putting this line inside the
`if` is a subtle bug: dies that never repeat never get recorded, so the second
time they appear, nothing happens.

**Strict `>`, and that is the graded character.** The contract sends ties to the
*smaller* start, so a window that merely equals the incumbent must **not**
replace it. This is the exact opposite of Exercise 1, and the two drills
disagree on purpose. On `[7, 3, 9, 3, 4, 1, 9]` the final window is also
length 4; with `>=` you would return `(3, 7)` and be wrong for a reason that
has nothing to do with your understanding of windows.

**The span is `(left, right + 1)`, and the `+ 1` is the half-open convention.**
`right` is the index of the last part *inside* the run, and `end` is one past
it. Check it against `[4]`: at `right = 0` the span is `(0, 1)`, and
`[4][0:1]` is `[4]`. If you write `(left, right)` you get `(0, 0)`, an empty
run, on a log that plainly has one part in it.

**Why the loop is linear even though it contains a jump.** `right` advances
exactly `n` times. `left` only ever moves forward and never passes `right`, so
across the entire run it advances at most `n` times in total — not `n` times
per iteration. Two indices, at most `2n` moves between them, every dictionary
operation constant on average. That is the amortised argument, and it is the
sentence to have ready when someone asks why a loop with a jump inside it is
not quadratic.

## Download and run

Download
[exercise-02-longest-clean-run-solution.py](./exercise-02-longest-clean-run-solution.py)
and run it:

```bash
python exercise-02-longest-clean-run-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-longest-clean-run.py`.

## Common bugs to catch

- **`longest_clean_run([1, 2, 2, 1])` returns `(1, 4)` instead of `(0, 2)`.**
  The missing `>= left` guard. No traceback — the window quietly holds a
  duplicate and reports a length it does not have. The self-check catches it
  with its own distinctness assertion:

  ```text
  Traceback (most recent call last):
      assert len(set(run)) == len(run), f"{run} repeats a die"
  AssertionError: [2, 2, 1] repeats a die
  ```

  That message is the one to recognise. Any time a window reports a length its
  own contents contradict, the shrink rule is wrong rather than the bookkeeping.

- **`longest_clean_run([7, 3, 9, 3, 4, 1, 9])` returns `(3, 7)`.** You used
  `>=` on the length comparison. Both spans are length 4; the contract asks for
  the earlier one. This is the mirror image of Exercise 1's graded bug, and the
  two pages disagree so that you read the rule instead of remembering a symbol.

- **`longest_clean_run([4])` returns `(0, 0)`.** You stored `(left, right)`
  instead of `(left, right + 1)`. The span is half-open: `end` is one past the
  last part.

- **A die at index 0 is treated as never seen.** You wrote `if seen_at and ...`.
  `0` is falsy, so the sighting is ignored and the window keeps a duplicate.
  Reproduce it deliberately on `[1, 2, 1]`: the correct answer is `(1, 3)`, and
  the truthiness version gives `(0, 3)`.

- **`KeyError`.**

  ```text
  Traceback (most recent call last):
      seen_at = last_index[die]
                ~~~~~~~~~~^^^^^
  KeyError: 7
  ```

  You indexed the dictionary directly instead of using `.get`. The first time
  any die appears there is no key to read. `.get(die)` returns `None` instead
  of raising, which is precisely the "have I seen this before" question you
  wanted to ask.

- **Stale entries in a set-based version.** If you write the explicit shrink —
  `while die in in_window: in_window.discard(stamps[left]); left += 1` — you
  must discard `stamps[left]` *before* incrementing `left`. Swap those two
  lines and the set keeps an element that is no longer in the window, the loop
  never terminates on some inputs, and you get:

  ```text
  Traceback (most recent call last):
      in_window.discard(stamps[left])
                        ~~~~~~^^^^^^
  IndexError: list index out of range
  ```

- **Rebuilding distinctness from scratch.**
  `len(set(stamps[left:right + 1])) == right - left + 1` is a correct test and
  a wrong solution: it is `O(n)` per call, so the whole function becomes
  quadratic and the 300,000 bound rejects it. Requirement 5 exists to rule this
  out by reading rather than by timing.

- **Returning the length instead of the span.** Read the signature. `4` is not
  `(2, 6)`, and the caller cannot get from one to the other.

## Under the hood

<details>
<summary>Under the hood — the amortised argument written out, and the two other ways to write this loop</summary>

**The amortised argument, spelled out.**

A loop with a `while` inside it *looks* quadratic, and beginners are right to
be suspicious. The reason this one is not comes down to a single observation:
`left` is monotone. It starts at 0, it only ever increases, and it never passes
`right`, which itself stops at `n - 1`.

So instead of asking "how much work does one iteration do", ask "how much work
do all the iterations do together". `right` advances `n` times. `left` advances
some number of times in total, and that number is at most `n`, because each
advance uses up a position it can never revisit. Total index movement across
the entire function: at most `2n`. Every dictionary read and write is `O(1)`
on average. So the whole thing is `O(n)`.

This is the standard shape of the argument, and it is worth learning as a
sentence you can say rather than a fact you know: *"the inner loop is bounded
across the whole run, not per iteration, because the index it advances never
resets."*

**Space, stated precisely.**

The dictionary holds one entry per **distinct** die seen so far, which is at
most `min(n, 10_000)`. Both halves of that matter and which one binds depends
on the input: a 300,000-part log from a crib of 10,000 dies is bounded by the
crib; a 50-part log is bounded by its own length. Saying `O(n)` is not wrong,
but it is less than you know.

**Two other ways to write the same loop.**

*The set version.* Instead of remembering where each die was seen, keep a set
of what is currently in the window, and shrink one step at a time:

```python
in_window: set[int] = set()
left = 0
best = (0, 0)
for right, die in enumerate(stamps):
    while die in in_window:
        in_window.discard(stamps[left])
        left += 1
    in_window.add(die)
    if right - left + 1 > best[1] - best[0]:
        best = (left, right + 1)
```

Same answer, same complexity, and no `>= left` guard needed — because the set
holds only what is genuinely inside the window, so the question cannot arise.
It does more index moves in the worst case (it walks the left edge forward one
place at a time instead of jumping), and the trade is that it is easier to get
right. If you find the guard fiddly, write this one and understand why it needs
no guard.

*The count version.* Keep a frequency table and shrink while the count of the
die you just added is above 1. That generalises: change the `1` to an `m` and
you have "no die used more than `m` times", which is the
[mini-project's Problem 2](../mini-project/README.md). The last-index version
does **not** generalise that way, which is worth knowing before you pick a
favourite.

**Why the last-index version is the one on the page.** It does the fewest index
moves, and — more usefully — it is the one that makes the "is this sighting
inside the window?" question explicit. That question comes back repeatedly:
any time you cache a position and later ask whether it is still relevant, you
are asking the same thing. The bug is worth meeting once, deliberately, on a
four-element list.

</details>

## Acceptance checklist

- [ ] `python exercise-02-longest-clean-run.py` prints six rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `longest_clean_run([1, 2, 2, 1])` returns `(0, 2)`, and you can say why.
- [ ] `longest_clean_run([4])` returns `(0, 1)`, not `(0, 0)`.
- [ ] `longest_clean_run([])` returns `(0, 0)`, not `None`.
- [ ] `left` never decreases anywhere in your loop.
- [ ] No `set(...)` of a slice appears inside the loop.
- [ ] You have a hand-written trace of `[1, 2, 2, 1]`, four rows.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 exercise 2: the longest clean run`.

## Stretch

- **Loosen the invariant: no die used more than twice.**

  ```python
  def longest_run_within_tolerance(stamps: list[int], tolerance: int) -> tuple[int, int]:
      """Return the longest span in which no die ID appears more than `tolerance` times."""
      counts: dict[int, int] = {}
      left = 0
      best = (0, 0)
      for right, die in enumerate(stamps):
          counts[die] = counts.get(die, 0) + 1
          while counts[die] > tolerance:
              counts[stamps[left]] -= 1
              left += 1
          if right - left + 1 > best[1] - best[0]:
              best = (left, right + 1)
      return best
  ```

  ```text
  [7, 3, 9, 3, 4, 1, 9] tolerance 2 -> (0, 7)
  [5, 5, 5, 5]          tolerance 2 -> (0, 2)
  ```

  Note which count the `while` looks at: only the die you just added, because
  it is the only one whose count can have gone up. That observation is worth
  saying out loud — it is the difference between checking one number and
  scanning a table.

- **Return every longest clean run, not just one.** The mechanics barely
  change: keep a list, clear it when you find something strictly longer, append
  when you tie.

  ```python
  def all_longest_clean_runs(stamps: list[int]) -> list[tuple[int, int]]:
      """Return every clean run of maximal length, in order of start."""
      last_index: dict[int, int] = {}
      left, best_length, spans = 0, 0, []
      for right, die in enumerate(stamps):
          seen_at = last_index.get(die)
          if seen_at is not None and seen_at >= left:
              left = seen_at + 1
          last_index[die] = right
          length = right - left + 1
          if length > best_length:
              best_length, spans = length, [(left, right + 1)]
          elif length == best_length:
              spans.append((left, right + 1))
      return spans
  ```

  ```text
  [7, 3, 9, 3, 4, 1, 9] -> [(2, 6), (3, 7)]
  ```

  Notice that the tie-break disappeared. When you return all of them there is
  nothing to break, which is a good reminder that a tie-break is a property of
  the contract and not of the algorithm.

- **Find the longest run with *at least* two distinct dies.** Try it, then work
  out why the window shape fails, and what you would use instead. The answer is
  in Lecture 1's section on when the pattern does not fit, but guess first: it
  has to do with whether shrinking the window can ever *fix* a broken promise.

**Practice elsewhere.** The same pattern appears as [LeetCode 3 · Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) if you want a judge to run against. The contract there returns a length rather than a span, so it never forces you to track where the best window was, and it defines no tie-break.

Next: [Exercise 3 — The Rota Window](./exercise-03-rota-window.md).
