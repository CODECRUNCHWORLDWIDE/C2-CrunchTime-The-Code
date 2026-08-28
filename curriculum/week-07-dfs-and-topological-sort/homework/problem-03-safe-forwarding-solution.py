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
