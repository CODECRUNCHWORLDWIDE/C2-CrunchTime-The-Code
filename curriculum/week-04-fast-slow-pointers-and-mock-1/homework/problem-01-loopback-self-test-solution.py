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
