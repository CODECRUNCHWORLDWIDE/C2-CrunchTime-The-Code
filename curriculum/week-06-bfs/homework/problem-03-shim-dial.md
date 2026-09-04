# Problem 3 — The Shim Dial

> **Topic:** BFS on a graph nobody wrote down — the states are the nodes and the moves are the edges
> **Lecture:** [01 — The BFS Template](../lecture-notes/01-the-bfs-template.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** every graph so far arrived as a grid or a dictionary. This one arrives as a *machine*, and the whole exercise is seeing that a dial setting is a node and a move is an edge. Once that sentence is written down the code is Exercise 1 again.

## The Brief

A stamping press sets its die height with **four thumbwheels**, each showing a
digit. The setter has exactly two moves:

- **nudge** one wheel up by one, where 9 rounds to 0 — the ratchet only turns one
  way, so there is no nudging down;
- **swap** two neighbouring wheels, lifting them off their splines and putting
  them back the other way round.

Some settings are **interlocked**: the press refuses to sit on them even for a
moment, so a route that passes through one is not a route at all.

Find the fewest moves from one setting to another.

## Starter

`problem-03-shim-dial-solution.py` sits beside this page with the interlocks and
the self-checks.

```text
wheels       4
interlocked  0100  1000  0010  0001
```

The ratchet being one-way is the detail that makes this interesting. `0000` to
`9000` is **nine** nudges, not one — you cannot turn a wheel back, so the cheap
route in the other direction does not exist. If your answer to that case is 1,
you have quietly given the machine a move it does not have.

## Requirements

1. `check_code(name, code)` rejects anything that is not exactly `WHEELS` digits,
   with a message naming which argument was wrong.
2. `next_settings(code)` returns every setting one move away — four nudges and
   three swaps, seven in all.
3. `dial_moves(start, target, interlocked)` returns the fewest moves, or `None`
   when the target cannot be reached.
4. A start that is itself interlocked has no route, even to itself.
5. `start == target` is zero moves, provided the setting is legal.

## Constraints

- **The graph is implicit.** There is no adjacency list to walk; `next_settings`
  *is* the adjacency list, computed on demand. Say so in the memo — it is the
  whole recognition step.
- **Nudges only go up.** `9 → 0` wraps; `0 → 9` does not exist.
- **Swaps are neighbouring wheels only** — positions 0-1, 1-2, 2-3. Not any two
  wheels, and not wrapping from 3 to 0.
- **Interlocked settings are never entered**, including as the start. Filtering
  them at dequeue rather than enqueue works and enqueues them first, which is the
  bug this constraint exists to prevent.
- **Mark seen on enqueue.** The state space here is ten thousand settings and a
  dequeue-time mark will still terminate — it just does far more work than the
  cost you will claim in the write-up.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python problem-03-shim-dial.py
0000 -> 0000: 0
0000 -> 0009: 9
0000 -> 9000: 9
0000 -> 1234: 10
0000 -> 4321: 10
0000 -> 0100: None (interlocks on)
0100 -> 0000: None (interlocks on)
All checks passed.
```

The two `None` results are the point of the interlock data. `0000 → 0100` is one
nudge away and unreachable, because `0100` is itself interlocked. `0100 → 0000`
is unreachable for the other reason — the *start* is interlocked, so the press
was never sitting there to begin with. Two different impossibilities, the same
answer, and a solution that only handles one of them passes half the checks.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: the state is a four-digit string, the edges are the two moves,
   and the graph is generated rather than stored.
3. Write `next_settings` first and check its length by hand: four nudges plus
   three swaps is seven, always. On `0000` three of those seven are `0000`
   itself, because swapping two identical digits changes nothing — the visited
   set discards them, so the generator does not have to.
4. Write the search. Filter interlocked settings at enqueue.
5. Handle the interlocked start and `start == target` before the pretty output.
6. Write the FRAME pass, naming the state space size: 10,000 settings.

## The Solution

```python
"""problem-03-shim-dial-solution.py — resetting a four-wheel shim dial.

A stamping press sets its die height with four thumbwheels, each showing a
digit. The setter has exactly two moves:

  * nudge one wheel up by one, where 9 nudges round to 0 — the ratchet only
    turns one way;
  * lift two neighbouring wheels off their splines and swap them.

Some codes are interlocked: the press refuses to sit on them even for a
moment. Find the fewest moves from one setting to another.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
WHEELS = 4
INTERLOCKED: tuple[str, ...] = ("0100", "1000", "0010", "0001")


# ---- Your task ----
def check_code(name: str, code: str) -> None:
    """Raise unless `code` is four digits.

    Args:
        name: What the code is, for the message.
        code: The code to check.

    Raises:
        ValueError: If the code is not exactly four characters, or holds
            anything but the digits 0 to 9.
    """
    if len(code) != WHEELS or not code.isdigit():
        raise ValueError(f"{name} {code!r} is not a four-digit setting")


def next_settings(code: str) -> list[str]:
    """Return every setting one move away from `code`.

    Args:
        code: The current four-digit setting.

    Returns:
        Seven settings: four nudges, one per wheel, and three swaps, one per
        neighbouring pair. Duplicates are kept — swapping two wheels showing
        the same digit gives `code` back, and the search discards it anyway.
    """
    moves = []
    for wheel in range(WHEELS):
        nudged = str((int(code[wheel]) + 1) % 10)
        moves.append(code[:wheel] + nudged + code[wheel + 1 :])
    for wheel in range(WHEELS - 1):
        moves.append(
            code[:wheel] + code[wheel + 1] + code[wheel] + code[wheel + 2 :]
        )
    return moves


def dial_moves(start: str, target: str, interlocked: tuple[str, ...] = ()) -> int | None:
    """Return the fewest moves from `start` to `target`.

    Args:
        start: The setting the wheels show now.
        target: The setting the job card asks for.
        interlocked: Settings the press refuses to sit on.

    Returns:
        The number of moves, counting one nudge or one swap as one move.
        Zero when the wheels already show the target. None when the target
        cannot be reached — including when `start` itself is interlocked,
        because then the press is already in a state it will not accept and
        the setter has to call an engineer, not turn a wheel.

    Raises:
        ValueError: If any of the settings is not four digits.
    """
    check_code("start", start)
    check_code("target", target)
    for code in interlocked:
        check_code("interlock", code)

    blocked = set(interlocked)
    if start in blocked or target in blocked:
        return None
    if start == target:
        return 0

    queue = deque([start])
    seen = blocked | {start}
    moves = 0
    while queue:
        moves += 1
        for _ in range(len(queue)):  # this move's worth of settings, no more
            code = queue.popleft()
            for candidate in next_settings(code):
                if candidate == target:
                    return moves
                if candidate not in seen:
                    seen.add(candidate)
                    queue.append(candidate)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for start, target, locks in (
        ("0000", "0000", ()),
        ("0000", "0009", ()),
        ("0000", "9000", ()),
        ("0000", "1234", ()),
        ("0000", "4321", ()),
        ("0000", "0100", INTERLOCKED),
        ("0100", "0000", INTERLOCKED),
    ):
        answer = dial_moves(start, target, locks)
        note = " (interlocks on)" if locks else ""
        print(f"{start} -> {target}: {answer}{note}")

    assert dial_moves("0000", "0000") == 0
    assert dial_moves("0000", "0001") == 1  # one nudge
    assert dial_moves("0000", "0009") == 9  # the ratchet only turns one way
    assert dial_moves("0000", "9000") == 9
    assert dial_moves("0100", "1000") == 1  # one swap, not nine nudges twice
    assert dial_moves("0000", "1234") == 10  # 1 + 2 + 3 + 4 nudges
    assert dial_moves("0000", "4321") == 10  # same digits, so the same cost
    assert dial_moves("0009", "9000") == 3  # three swaps walk the 9 along

    # An interlocked target can never be the answer.
    assert dial_moves("0000", "0100", INTERLOCKED) is None
    # An interlocked start is a call to the engineer, not a search.
    assert dial_moves("0100", "0000", INTERLOCKED) is None
    # Interlocks that are neither end still push the route around.
    assert dial_moves("0000", "0011", ("0001", "0010")) == 3

    for name, start, target in (
        ("start", "000", "0000"),
        ("target", "0000", "00x0"),
    ):
        try:
            dial_moves(start, target)
        except ValueError as error:
            assert name in str(error) and "four-digit setting" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
```

`next_settings` returns seven settings unconditionally, duplicates included. It
could filter them, and deliberately does not: the visited set already rejects a
setting the search has seen, and giving the generator a second reason to drop
things is how the two disagree later. One place decides what has been visited.

## Run it

Download the solution beside this page and run it:

```bash
python problem-03-shim-dial.py
```

No third-party packages, no arguments, no input. It prints the five cases and
then `All checks passed.`

## Common bugs to catch

- **Nudging in both directions.** Symptom: `0000 → 9000` returns 1. The ratchet
  does not turn back.
- **Swapping any two wheels.** Symptom: routes shorter than the machine allows.
  Neighbours means adjacent.
- **Filtering interlocks at dequeue.** Symptom: correct answers, and interlocked
  settings sitting in the queue — which is to say, a search that entered a state
  the press refuses.
- **Not checking the start.** Symptom: `0100 → 0000` returns a number when the
  press was never on `0100`.
- **Filtering duplicates in `next_settings` instead of trusting the visited
  set.** Symptom: nothing, until the day the two rules disagree. One place
  decides what has been seen.
- **Marking seen on dequeue.** Symptom: right answers, far more work, and no way
  to tell from the output.

## Acceptance checklist

- [ ] `0000 → 9000` is 9 moves.
- [ ] `0000 → 1234` and `0000 → 4321` are both 10 moves.
- [ ] Both interlocked cases return `None` — one for the target, one for the start.
- [ ] `next_settings` returns seven settings for any code, `0000` included.
- [ ] `check_code` rejects a three-digit or non-digit code, naming the argument.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return the route itself, not just its length. It needs a parent map, and it is
  the version a setter could actually follow.
- Add a "nudge down" move and re-run. Some answers halve; say which and why, and
  what that says about the shape of the state graph.
- Count how many of the 10,000 settings are reachable from `0000` with the
  interlocks on. The answer is a property of the machine, not of the search.
