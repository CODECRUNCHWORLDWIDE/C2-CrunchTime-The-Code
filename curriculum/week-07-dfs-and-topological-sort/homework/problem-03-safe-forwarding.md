# Problem 3 — Safe Forwarding

> **Topic:** an answer that depends on *every* branch succeeding, and the recursion limit that decides how you compute it
> **Lecture:** [02 — Iterative DFS](../lecture-notes/02-iterative-dfs.md), [03 — Topological Sort](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Medium-Hard
> **Target time:** 60 minutes
> **Why this one:** it is the page where the recursive version stops being a style preference. Both answers are correct on the switchboard; only one of them survives a 5,000-extension relay chain, and the file shows the other one failing.

## The Brief

Every office extension may carry **forwarding rules** — a list of other
extensions a call can be sent to. An extension with **no** forwarding rules is a
desk, and a call that reaches a desk is answered by a person.

An extension is **settled** when *every* possible chain of forwards starting
from it ends at a desk. An extension that can get caught in a forwarding circle,
or that can reach one, is not settled: one unlucky routing choice and the call
rings forever.

Report the settled extensions.

## Starter

`problem-03-safe-forwarding-solution.py` sits beside this page with the
switchboard and the self-checks.

Ten extensions. Three of them ring forever, and the interesting part is that
they do not all ring for the same reason — one is *in* a forwarding circle, and
another merely forwards into one. Work out which is which on paper before you
start; it is the distinction the whole problem turns on.

## Requirements

1. `settled_extensions(forwards)` returns the settled extensions, sorted.
2. `settled_extensions_by_colour(forwards)` gets the same answer by the
   three-colour walk — shipped so the two can be compared.
3. `relay_chain(length)` builds a chain of a given length, for the depth test.
4. An extension with no forwarding rules is a desk and is always settled.
5. Both routes agree on every switchboard that either can handle.

## Constraints

- **Every branch must succeed, not just one.** This is the constraint that
  separates this problem from ordinary reachability. An extension forwarding to
  a desk *and* to a circle is not settled — one bad choice is enough.
- **A circle is not settled, and neither is anything that can reach one.** Those
  are two different failures with one answer, and the switchboard has both.
- **Recursion is bounded and the bound is in the data.** The constraints allow a
  relay chain of 5,000 extensions, and Python's default recursion limit is 1,000.
  The colour walk hits `RecursionError` on that chain; the counting run does not.
  Say which you would write and why.
- **The counting run goes backwards.** Start from the desks and peel off any
  extension whose forwarding targets have *all* already settled. That "all"
  mirrors the rule exactly, which is what makes the two approaches agree.
- **Sorted output**, so two runs agree and a test can assert it.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python problem-03-safe-forwarding.py
switchboard: 10 extensions in all
  settled : ['201', '301', '302', '401', '701', '801', '901']
  ringing : ['501', '502', '601']
a 5000-extension relay chain, the widest the constraints allow
  backwards Kahn : 5000 settled
  colour walk    : RecursionError
All checks passed.
```

The last block is the exhibit. On a 5,000-extension relay chain — the widest the
constraints allow — the backwards counting run settles all 5,000 and the colour
walk raises `RecursionError`.

Both are correct algorithms. Only one of them is an answer to *this* problem, and
the difference is a bound stated in the constraints rather than anything about
the algorithms themselves. That is the sentence the write-up wants.

## Steps

1. Read the self-checks. They are the spec.
2. Work out by hand which three extensions ring, and which of them is in a circle
   rather than merely reaching one.
3. Write the memo: settled means *every* chain ends at a desk; the recursion
   bound is 5,000 against a limit of 1,000.
4. Write the backwards counting run first. Desks settle immediately; an extension
   settles when all its targets have.
5. Write the colour walk too, so the comparison is real.
6. Run both on `relay_chain(5000)` and watch the second one fail.
7. Write the FRAME pass, with the depth bound in the Reason section rather than
   the Evaluate one — it decides the algorithm, so it belongs before the choice.

## The Solution

```python
"""problem-03-safe-forwarding-solution.py -- which office extensions always get answered.

Every extension may carry forwarding rules: a list of other extensions a call
can be sent to. An extension with no forwarding rules is a desk, and a call that
reaches a desk is answered by a person.

An extension is settled when every possible chain of forwards starting from it
ends at a desk. An extension that can get caught in a forwarding circle, or that
can reach one, is not settled -- one unlucky routing choice and the call rings
forever.

Two routes give the same answer:

  * the three-colour walk, remembering per extension whether its whole fan-out
    reached desks, and
  * Kahn's counting run backwards -- start from the desks and peel off any
    extension whose every forwarding target has already settled.

This file ships the backwards Kahn, because it is a loop rather than a
recursion and the bound here is 5,000 extensions -- five times CPython's
1,000-frame default. The recursive route is kept beside it so the difference can
be seen rather than taken on trust.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

from collections import deque

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
# "901" is named as a target and never as a key, so it is a desk and it counts.
SWITCHBOARD: dict[str, list[str]] = {
    "201": ["301", "302"],
    "301": ["401"],
    "302": [],
    "401": [],
    "501": ["502"],
    "502": ["501"],
    "601": ["501"],
    "701": ["302"],
    "801": ["901"],
}


def settled_extensions(forwards: dict[str, list[str]]) -> list[str]:
    """List every extension whose every forwarding chain ends at a desk.

    Args:
        forwards: Each extension mapped to the extensions it can forward to. An
            extension named only as a target, never as a key, is a desk.

    Returns:
        Every settled extension, sorted. An empty switchboard gives [].
    """
    callers: dict[str, list[str]] = {}
    pending: dict[str, int] = {}
    for extension, targets in forwards.items():
        pending.setdefault(extension, 0)
        callers.setdefault(extension, [])
        for target in targets:
            pending[extension] += 1
            pending.setdefault(target, 0)
            callers.setdefault(target, []).append(extension)

    ready: deque[str] = deque(
        extension for extension, count in pending.items() if count == 0
    )
    settled: list[str] = []
    while ready:
        extension = ready.popleft()
        settled.append(extension)
        for caller in callers[extension]:
            pending[caller] -= 1
            if pending[caller] == 0:
                ready.append(caller)
    return sorted(settled)


def settled_extensions_by_colour(forwards: dict[str, list[str]]) -> list[str]:
    """The same answer via the three-colour walk. Kept for comparison.

    Grey means "on the chain of forwards we are following right now", so a hop
    onto a grey extension is the circle. Each extension's verdict is remembered
    the moment it turns black, which is what keeps the whole thing linear.

    Args:
        forwards: Each extension mapped to the extensions it can forward to.

    Returns:
        Every settled extension, sorted.

    Raises:
        RecursionError: The longest forwarding chain is deeper than CPython's
            frame limit. That is the whole reason this is not the shipped route.
    """
    colour: dict[str, int] = {}
    verdict: dict[str, bool] = {}

    def walk(extension: str) -> bool:
        state = colour.get(extension, WHITE)
        if state == GREY:
            return False
        if state == BLACK:
            return verdict[extension]
        colour[extension] = GREY
        answer = all(walk(target) for target in forwards.get(extension, []))
        colour[extension] = BLACK
        verdict[extension] = answer
        return answer

    everyone: set[str] = set(forwards)
    for targets in forwards.values():
        everyone.update(targets)
    return [extension for extension in sorted(everyone) if walk(extension)]


def relay_chain(length: int) -> dict[str, list[str]]:
    """Build a switchboard of `length` extensions, each forwarding to the next.

    Args:
        length: How many extensions the chain holds. The last one is a desk.

    Returns:
        A forwarding table with exactly `length` distinct extensions in it.
    """
    return {f"x{seat:04d}": [f"x{seat + 1:04d}"] for seat in range(length - 1)}


# ---- Self-check ----
if __name__ == "__main__":
    answer = settled_extensions(SWITCHBOARD)
    everyone: set[str] = set(SWITCHBOARD)
    for targets in SWITCHBOARD.values():
        everyone.update(targets)
    print(f"switchboard: {len(everyone)} extensions in all")
    print(f"  settled : {answer}")
    print(f"  ringing : {sorted(everyone - set(answer))}")

    big = relay_chain(5000)
    settled_big = settled_extensions(big)
    print("a 5000-extension relay chain, the widest the constraints allow")
    print(f"  backwards Kahn : {len(settled_big)} settled")
    try:
        settled_extensions_by_colour(big)
        colour_result = "finished"
    except RecursionError:
        colour_result = "RecursionError"
    print(f"  colour walk    : {colour_result}")

    assert answer == ["201", "301", "302", "401", "701", "801", "901"]
    assert settled_extensions({}) == []
    assert settled_extensions({"210": []}) == ["210"]
    assert settled_extensions({"210": ["210"]}) == []
    assert settled_extensions({"210": ["211"]}) == ["210", "211"]
    assert settled_extensions({"210": ["211", "212"], "211": ["212"], "212": []}) == [
        "210",
        "211",
        "212",
    ]
    assert len(settled_big) == 5000
    assert settled_extensions_by_colour(SWITCHBOARD) == answer
    assert settled_extensions_by_colour({}) == []
    assert colour_result == "RecursionError"

    print("All checks passed.")
```

The colour walk is shipped knowing it cannot handle the largest legal input, and
the file asserts that it raises rather than merely noting it. An exhibit nothing
asserts stops being an exhibit the first time somebody tidies the file.

## Run it

Download the solution beside this page and run it:

```bash
python problem-03-safe-forwarding.py
```

No third-party packages, no arguments, no input. It prints the switchboard's
settled and ringing extensions, the 5,000-chain comparison, and then
`All checks passed.`

## Common bugs to catch

- **Settling an extension when *any* branch reaches a desk.** Symptom: the
  extension that forwards both to a desk and into a circle is reported settled.
  It is the most plausible wrong answer here.
- **Treating "in a circle" and "reaches a circle" differently.** Symptom: one of
  the three ringing extensions is misreported. They have the same answer.
- **Recursion on the largest legal input.** Symptom: `RecursionError`, on data
  the constraints explicitly allow.
- **Raising the recursion limit instead.** Symptom: it works, until it segfaults
  — the limit exists because the C stack is finite. Say so rather than raising it.
- **A desk treated as a special case.** Symptom: extra code for something the
  "all targets settled" rule already handles, vacuously.
- **Unsorted output.** Symptom: a test that passes intermittently.

## Acceptance checklist

- [ ] Seven extensions settle; three ring.
- [ ] The two routes agree on the switchboard.
- [ ] `relay_chain(5000)` settles all 5,000 by the counting run.
- [ ] The colour walk raises `RecursionError` on that chain, asserted.
- [ ] A desk is settled; an extension forwarding only to desks is settled.
- [ ] Output is sorted.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report *why* each ringing extension rings — in a circle, or reaching one. The
  counting run does not distinguish them; working out what would have to change
  is the interesting half.
- Return the shortest forwarding chain to a desk, for each settled extension.
  That is the routing a switchboard would actually prefer.
- Make the colour walk iterative with an explicit stack, and re-run the 5,000
  chain. It now works — and comparing its memory against the counting run's is a
  fair fight rather than a rout.
