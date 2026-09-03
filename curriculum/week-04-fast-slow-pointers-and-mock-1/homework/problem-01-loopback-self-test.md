# Problem 1 — The Loopback Self-Test

> **Topic:** fast and slow pointers on a functional graph — the same three phases, hidden inside what looks like an array question
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §6
> **Difficulty:** Medium
> **Target time:** 75 minutes, including the FRAME write-up
> **Why this one:** it is the most useful thing you will do with Floyd's outside of a chain of objects, and it is the hardest to *see*. The prompt hands you a list of integers and nothing else. If you can spot the chain in it, you can spot it anywhere.

## The Brief

A network switch checks its own wiring when it powers on. It releases one test
frame at port 0 and watches where the frame ends up.

The wiring is described by a **forwarding table**: a list called `hop`, where
`hop[i]` is the port that port `i` sends the frame to. Every port sends to
exactly one port. That is the entire rule.

A **healthy** fabric is one where a frame released at port 0 visits every port
exactly once and arrives back at port 0. Anything else is a misconfiguration: a
frame that settles into a smaller circuit, or one that passes through a few
ports and then gets stuck in a circuit it can never leave.

Return `True` if the fabric is healthy, `False` otherwise.

**Where the chain is hiding.** The word "list" makes this look like an array
problem. It is not. `hop[i]` gives every port exactly one successor, and a rule
that gives every state exactly one successor is a chain — a **functional
graph**, the same structure as
[Exercise 4](../exercises/exercise-04-wear-level-rotation.md). The "nodes" are
port numbers, the "next pointer" is a table lookup instead of arithmetic, and
the frame's path is a walk down that chain.

Because the number of ports is finite and nothing branches, the frame's path
always ends in a circuit. So the real question is about the *shape* of that
walk, and the answer is: the fabric is healthy exactly when the circuit covers
every port.

**One example to be careful with.** `[1, 0, 3, 2]` sends port 0 to 1, port 1 to
0, port 2 to 3 and port 3 to 2. Every port appears exactly once as a
destination — it is a perfect shuffle — and it is still broken, because it is
*two* separate two-port circuits and the frame never leaves the first one. A
solution that checks "does every port appear once as a destination" says
`True` here and is wrong. That example is why this problem is not "is this a
shuffle".

## Starter

Create `problem-01-loopback-self-test.py` and paste this in. Fill in every
`TODO`.

```python
"""problem-01-loopback-self-test.py — is the switch fabric healthy?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per table and then "All checks passed." when the module is right.
"""

from __future__ import annotations


def is_single_loopback(hop: list[int]) -> bool:
    """Return True when a frame from port 0 visits every port exactly once.

    Args:
        hop: The forwarding table. `hop[i]` is the port that port `i` sends
            the test frame to. Every entry is a valid port index.

    Returns:
        True when the frame's path from port 0 is one loop covering all the
        ports, False for any other shape, including an empty table.
    """
    # TODO 1: an empty table cannot pass. Say so first, and note that the
    #         walk below would raise on it.
    # TODO 2: phase one. Step `slow` once and `fast` twice until they hold
    #         the same port. No guard — the walk cannot end.
    # TODO 3: phase two. Put `finder` back at port 0, leave `slow` alone,
    #         step both until they agree. That is the loop's first port.
    # TODO 4: phase three. Walk once around, counting, first step first.
    # TODO 5: decide. Read the Solution's argument before you pick which
    #         condition to test — one of the obvious two is redundant.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ([1, 2, 3, 0], True),
        ([2, 3, 1, 0], True),
        ([0], True),
        ([1, 0, 3, 2], False),
        ([1, 2, 0, 4, 3], False),
        ([1, 1, 2, 3], False),
        ([0, 0], False),
        ([], False),
    ]

    for table, expected in CASES:
        found = is_single_loopback(table)
        assert found is expected, f"{table}: got {found}, wanted {expected}"
        verdict = "healthy" if found else "misconfigured"
        print(f"{str(table):<22} {verdict}")

    ring = list(range(1, 4096)) + [0]
    assert is_single_loopback(ring) is True
    print(f"{'4096 ports in a ring':<22} healthy")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/homework/problem-01-loopback-self-test.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `is_single_loopback(hop)` returns a `bool`, not a number and not `None`.
2. `[]` returns `False`.
3. `[0]` returns `True`. A one-port fabric loops back on itself, and that is
   the smallest healthy configuration there is.
4. `[1, 0, 3, 2]` returns `False`, even though it is a perfect shuffle.
5. Fixed memory: a handful of integers. No visited array **of any size**, no
   `set`, no `dict`.
6. There is no "no loop found" branch. The walk always ends in a loop.
7. Ports are integers, so the comparison is `==`.
8. The function keeps its type hints and its docstring.

## Constraints

- **Up to 65,536 ports, and you may not allocate a visited array of any
  size.** This check runs in the bootloader, before the memory allocator has
  been started, so there is nowhere to put `[False] * n` — not a list, not a
  `set`, not a `dict`. Note carefully that the size bound is **not** what
  rejects the O(n)-space solution here; 65,536 booleans would fit comfortably
  on any machine that has memory at all. The rejection is that there is no
  memory yet. This is the sharpest version of the distinction you have been
  practising all week, and stating it precisely is the whole interview tell.

- **The 16-bit ceiling is the port-index width in the fabric's descriptor
  format.** A table larger than 65,536 entries cannot be expressed in the
  format, so it cannot be handed to this function in the first place.

- **`0 <= hop[i] < len(hop)` for every entry.** Every port forwards to a real
  port. That is what guarantees the walk cannot run off the end, and it is what
  lets phase one skip its guard.

- **`hop == []` returns `False`, and this is an author's decision worth
  defending out loud.** A fabric with no ports cannot pass a loopback test, and
  returning `True` vacuously would let a descriptor table that failed to parse
  look healthy at boot. Choosing the *loud* answer for a degenerate input is a
  design habit, not a detail.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-loopback-self-test-solution.py
[1, 2, 3, 0]           healthy
[2, 3, 1, 0]           healthy
[0]                    healthy
[1, 0, 3, 2]           misconfigured
[1, 2, 0, 4, 3]        misconfigured
[1, 1, 2, 3]           misconfigured
[0, 0]                 misconfigured
[]                     misconfigured
4096 ports in a ring   healthy
All checks passed.
```

Line four is the perfect shuffle that is still broken. Line seven, `[0, 0]`, is
the other one to look at: port 0 forwards to itself, so the loop is one port
long in a fabric that has two.

## Examples worth walking

Each of these is chosen to break a different wrong solution, and your write-up
should walk all of them.

- `[1, 2, 3, 0]` → `True`. The walk is `0 -> 1 -> 2 -> 3 -> 0`.
- `[2, 3, 1, 0]` → `True`. The walk is `0 -> 2 -> 1 -> 3 -> 0`. A healthy
  fabric need not be wired in index order. If your solution only accepts
  `hop[i] == (i + 1) % n`, you matched the first example instead of solving the
  problem.
- `[1, 0, 3, 2]` → `False`. Two two-port circuits. Kills the "is it a shuffle"
  solution.
- `[1, 2, 0, 4, 3]` → `False`. A three-port circuit and a two-port circuit.
- `[1, 1, 2, 3]` → `False`. Not a shuffle at all: `0 -> 1 -> 1 -> 1 -> …`.
- `[0, 0]` → `False`. Loop of one, fabric of two.
- `[0]` → `True`. The smallest healthy fabric.
- `[]` → `False`. By the constraint above.

## Steps

1. **Frame.** Restate the ask. Say out loud that the table is a chain, not an
   array, and why. Confirm the empty-table decision and be ready to defend it.
   Walk `[1, 0, 3, 2]` by hand and say why it fails despite being a shuffle.
2. **Research constraints.** Name the bootloader. Say the precise sentence: the
   visited array is not *slower*, it is *unavailable*. Note that a rotation
   always exists, so there is no `None` case.
3. **Assess options.** The visited array is four lines and obviously correct:
   walk from 0, mark each port, stop on a repeat, then check you marked
   everything and came back to 0. Say what it is good at — it is clearer and it
   generalises to "which ports are unreachable" — and then say why the
   bootloader cannot run it.
4. **Assess options, part two.** Then settle a question rather than guessing at
   it: **are both the tail check and the length check necessary?** Work it out
   before you write code. See the Solution for the argument, but try it
   yourself first.
5. **Make the solution.** Empty guard, then Exercise 4's three phases with
   `hop[...]` in place of `next_slot(...)`, then the decision.
6. **Examine.** Trace `[1, 2, 0, 4, 3]`. Phase one: slow=0, fast=0. Turn 1:
   slow=1, fast=2. Turn 2: slow=2, fast=1 (two steps: 2→0→1). Turn 3: slow=0,
   fast=0. They meet at 0. Phase two: finder=0, slow=0, so the loop's first
   port is 0 with a tail of 0. Phase three: walker=1, loop=1; walker=2, loop=2;
   walker=0, loop=3, home. Loop is 3, there are 5 ports, so `False`. ✓
7. **Examine, cost.** O(n) time — each phase is bounded by the number of ports.
   O(1) space — four integers.

## The Solution

```python
"""problem-01-loopback-self-test-solution.py — is the switch fabric healthy?

The forwarding table looks like an array question and is not. `hop[i]` gives
port `i` exactly one successor, so following the table is walking a chain
whose links are port numbers. The frame's path therefore always ends in a
loop, and the fabric is healthy exactly when that loop covers every port.

Three phases, the same three as the wear-level drill: meet the pointers,
walk the meeting point back to the loop's first port, then measure the loop.

The self-checks at the bottom print one line per table, then
"All checks passed."
"""

from __future__ import annotations


def is_single_loopback(hop: list[int]) -> bool:
    """Return True when a frame from port 0 visits every port exactly once.

    Args:
        hop: The forwarding table. `hop[i]` is the port that port `i` sends
            the test frame to. Every entry is a valid port index.

    Returns:
        True when the frame's path from port 0 is one loop covering all the
        ports, False for any other shape, including an empty table.
    """
    if not hop:
        return False

    slow = 0
    fast = 0
    while True:  # No guard: one successor per port means the walk cannot end.
        slow = hop[slow]
        fast = hop[hop[fast]]
        if slow == fast:
            break

    finder = 0
    while finder != slow:
        finder = hop[finder]
        slow = hop[slow]

    walker = hop[finder]
    loop = 1
    while walker != finder:
        walker = hop[walker]
        loop += 1

    return loop == len(hop)


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ([1, 2, 3, 0], True),
        ([2, 3, 1, 0], True),
        ([0], True),
        ([1, 0, 3, 2], False),
        ([1, 2, 0, 4, 3], False),
        ([1, 1, 2, 3], False),
        ([0, 0], False),
        ([], False),
    ]

    for table, expected in CASES:
        found = is_single_loopback(table)
        assert found is expected, f"{table}: got {found}, wanted {expected}"
        verdict = "healthy" if found else "misconfigured"
        print(f"{str(table):<22} {verdict}")

    ring = list(range(1, 4096)) + [0]
    assert is_single_loopback(ring) is True
    print(f"{'4096 ports in a ring':<22} healthy")

    print("All checks passed.")
```

**The recognition first.** `i -> hop[i]` gives every port exactly one successor.
That is a functional graph, so the frame's path is a chain walk, so the walk has
a tail and then a loop — always, because the ports are finite and nothing
branches. Once you have said that, this is
[Exercise 4](../exercises/exercise-04-wear-level-rotation.md) with a table
lookup where the formula used to be, and a different question asked of the
answer.

**One of the two obvious conditions is redundant, and proving it is the point of
this problem.** The natural test is *tail is 0 and loop covers every port*.
Here is why the first half is free.

The tail and the loop are made of different ports — no port is in both, because
the moment the walk reaches a loop port it never leaves the loop. So the tail
and the loop together use `tail + loop` distinct ports out of `n`, which gives
you

```text
tail + loop <= n
```

Now suppose `loop == n`. Substituting, `tail + n <= n`, so `tail <= 0`, and a
count cannot be negative, so `tail == 0`. **The length check already forces the
tail check.** One condition does the work of two:

```python
    return loop == len(hop)
```

Finding a redundant condition in your own predicate, and being able to *prove*
it is redundant rather than deleting it and hoping, is a stronger signal than
adding a defensive one. Your write-up must say which check you kept and why.

**Phase one has no guard, and the absence is an argument.** Every port forwards
to a real port, so the walk cannot end. Writing a `return False` branch for "no
loop found" produces unreachable code, and unreachable code in a recorded mock
reads as *did not understand the structure*.

**The empty table is checked first because the walk would crash on it.**
`hop[slow]` on an empty list raises `IndexError` immediately. The guard is not
decoration; it is the only thing standing between the caller and a traceback.
And the answer it gives — `False` — is the one that makes a mis-parsed
descriptor table fail loudly at boot.

**Phase three takes its first step before it compares.** Same rule as everywhere
else this week. `[0, 0]` is the case that catches getting it wrong: port 0
forwards to itself, so the loop is one port long, and a walk that compares
before stepping reports zero and then says the fabric is healthy when the
fabric is as broken as it can be.

**Nothing here grows with the fabric.** `slow`, `fast`, `finder`, `walker`, and
one counter. That is the bootloader honoured — not because the numbers are
small, but because there are a fixed number of them.

## Download and run

Download
[problem-01-loopback-self-test-solution.py](./problem-01-loopback-self-test-solution.py)
and run it:

```bash
python problem-01-loopback-self-test-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-01-loopback-self-test.py`.

## Common bugs to catch

- **`IndexError: list index out of range`.** You walked an empty table, or a
  table with an entry pointing at a port that does not exist:

  ```text
  Traceback (most recent call last):
      s = hop[s]
          ~~~^^^
  IndexError: list index out of range
  ```

  For the empty table, add the guard. For an out-of-range entry, the constraint
  says it cannot happen — but if you are generating your own test tables,
  generating a bad one is exactly how you will see this.

- **Checking "is it a shuffle" and stopping there.** `len(set(hop)) == len(hop)`
  is `True` for `[1, 0, 3, 2]`, which is broken. It is a necessary condition,
  not a sufficient one, and it costs O(n) memory to check something that does
  not settle the question.

- **Accepting only the in-order ring.** If your solution really tests
  `hop[i] == (i + 1) % n`, then `[2, 3, 1, 0]` comes back `False`. You matched
  the first example rather than solving the problem, and the second example is
  there to catch it.

- **Returning `True` for `[]`.** Vacuous truth is the wrong answer here, and
  the constraint explains why. This is a decision, not an accident — make it on
  purpose and defend it out loud.

- **A phase-three loop that returns `0` on a fixed point.** `[0, 0]` reports a
  loop of zero, which is never equal to the port count, so the answer *happens*
  to come out right. That is worse than failing: the bug is invisible on this
  problem and will bite you on the next one. Initialise `walker = hop[finder]`
  with `loop = 1`.

- **Using `is` instead of `==`.** These are integers. Above 256 CPython stops
  keeping one shared copy, so identity comparison silently stops matching and
  the program never finishes. The 4,096-port check is what catches it, and the
  symptom is a hang rather than a traceback.

- **Writing a "no loop" branch.** There is none. Unreachable code, every time.

## Under the hood

<details>
<summary>Under the hood — the visited-array version, and what a permutation guarantees</summary>

**The version the bootloader cannot run, so you know exactly what you gave up.**

```python
def is_single_loopback_with_marks(hop: list[int]) -> bool:
    """The O(n)-space version: mark every port as the frame touches it."""
    if not hop:
        return False
    seen = [False] * len(hop)
    port, steps = 0, 0
    while not seen[port]:
        seen[port] = True
        port, steps = hop[port], steps + 1
    return port == 0 and steps == len(hop)
```

Seven lines, no lemma, same O(n) time, and it is clearer. On a server it is the
right answer. In a bootloader there is no allocator, so there is no `[False] *
n` to be had at any size. Say both halves of that out loud.

**A permutation is a fabric where every port is also *reached* by exactly one
port.** All three of `[1, 2, 3, 0]`, `[2, 3, 1, 0]` and `[1, 0, 3, 2]` are
permutations; only the first two are healthy. What a permutation guarantees is
that there is **no tail at all** — from any start, you are already inside a
circuit, because a port with no predecessor is the only way to get a tail and a
permutation has none. So on a permutation the question collapses to "is the
circuit the whole thing", which is why `tail + loop <= n` is so easy to satisfy
there and why the shuffle check feels like it should be enough.

**Every permutation splits into circuits, and that is a classic result.**
`[1, 0, 3, 2]` is two circuits of two. `[1, 2, 0, 4, 3]` is a circuit of three
and a circuit of two. A healthy fabric is exactly a permutation with **one**
circuit — what a mathematician calls an *n-cycle*. Roughly one in `n`
permutations of `n` things is an n-cycle, which is a nice fact to know when
someone asks how likely a random miswiring is to pass.

**Where the same shape turns up.** Any table where an entry names another entry.
A jump table in a firmware image. A parent array in a disjoint-set structure. A
list of "who does this person report to". All of them are chains, all of them
loop, and none of them will say so in the prompt.

</details>

## Acceptance checklist

- [ ] `python problem-01-loopback-self-test.py` prints nine lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] No visited array, `set` or `dict` of any size.
- [ ] Phase one has no guard, and you can say in one sentence why not.
- [ ] Phase three starts at `hop[finder]` with the count at `1`.
- [ ] Your predicate has **one** condition, and your write-up proves the other
      one is redundant using `tail + loop <= n`.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/hw-01-loopback-self-test.md`
      with a recording of at least 15 minutes.
- [ ] The write-up's Assess-options section says the visited array is
      *unavailable*, not *slower*.

## Stretch

- **Report the shape instead of a verdict.** Return `(tail, loop)` and let the
  caller decide. It is the same code with a different last line, and it is more
  useful to a firmware team than a boolean:

  ```python
  def loopback_shape(hop: list[int]) -> tuple[int, int]:
      """Return (ports touched once, ports in the circuit) from port 0."""
      slow = fast = 0
      while True:
          slow, fast = hop[slow], hop[hop[fast]]
          if slow == fast:
              break
      finder, tail = 0, 0
      while finder != slow:
          finder, slow, tail = hop[finder], hop[slow], tail + 1
      walker, loop = hop[finder], 1
      while walker != finder:
          walker, loop = hop[walker], loop + 1
      return tail, loop
  ```

  ```text
  [1, 2, 3, 0]           tail 0, loop 4
  [1, 2, 0, 4, 3]        tail 0, loop 3
  [1, 1, 2, 3]           tail 1, loop 1
  ```

- **Release the frame at every port, not just port 0.** Count how many distinct
  circuits the fabric has. Doing it without a visited array is genuinely hard —
  and working out *why* it is hard, rather than finding a trick, is the
  learning. The answer is that O(1) space buys you one walk's worth of
  information, and "how many circuits are there" is a question about the whole
  fabric.

- **Prove the redundancy the other way round.** Does `tail == 0` force
  `loop == n`? Find a table where the tail is zero and the loop is smaller than
  the fabric, and you have your counterexample in one line. Having both
  directions settled is what lets you say "one of these is redundant, and it is
  *that* one" instead of "one of these is probably redundant".
Next: [Problem 2 — Trim the Duplicate Scan](./problem-02-trim-scan.md).
