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
