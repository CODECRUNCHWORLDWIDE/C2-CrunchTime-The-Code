"""problem-02-dsu-starter.py - the cheapest cable run, to fill in.

The same harbour, a different question. The board wants power to every quay for
the least money. Trenches have prices; a trench is worth digging only if it
joins two quays that are not already connected by trenches already chosen.

Walk the trenches cheapest first and keep the ones that join two separate
networks. The "already joined?" test is the whole reason union-find is here: it
answers membership, and it never needs to know the path.

Fill in the three bodies. Do not change the signatures or the harness: the
harness is the spec.

Run it and it will tell you which cases still fail. When they all pass it prints
"All checks passed."
"""

Trench = tuple[str, str, int]   # (quay, quay, cost in thousands of pounds)

QUAYS: list[str] = [
    "Ferry Slip",
    "Bait Wharf",
    "Chandlery Steps",
    "Dry Dock",
    "Gull Rock",
]

TRENCHES: list[Trench] = [
    ("Ferry Slip", "Bait Wharf", 3),
    ("Bait Wharf", "Chandlery Steps", 2),
    ("Ferry Slip", "Chandlery Steps", 6),   # redundant once the two above are in
    ("Chandlery Steps", "Dry Dock", 4),
]
# Gull Rock has no trench at all: it stays dark, and that is a real answer.


class Harbour:
    """Quays grouped by which of them are already joined by chosen trenches."""

    def __init__(self, quays: list[str]) -> None:
        """Start every quay in a network of its own.

        Args:
            quays: Every quay the harbour has.
        """
        # TODO: a parent map, a rank map, and a live count of networks.
        raise NotImplementedError

    def network_of(self, quay: str) -> str:
        """The quay that names this quay's network, flattening on the way.

        Args:
            quay: The quay to look up.

        Returns:
            The root quay. Two quays are joined exactly when this returns the
            same name for both.
        """
        # TODO: walk to the root, then point everything on the path AT the root.
        # Iterate rather than recurse: a long chain will blow the stack.
        raise NotImplementedError

    def join(self, left: str, right: str) -> bool:
        """Merge two networks, shallower under deeper.

        Args:
            left: One quay.
            right: The other quay.

        Returns:
            True when they were apart and are now one. False when they were
            already joined - which is exactly the trench Kruskal skips.
        """
        # TODO: find both roots; if equal return False; otherwise attach by rank
        # and decrement the network count.
        raise NotImplementedError


def cheapest_cable(
    quays: list[str], trenches: list[Trench]
) -> tuple[int, list[Trench], int]:
    """The cheapest set of trenches that leaves nobody out who can be reached.

    Args:
        quays: Every quay the harbour has.
        trenches: Every trench that could be dug, with its price.

    Returns:
        (total cost, trenches in the order accepted, networks left over). That
        third number is 1 when the plan reaches every quay and more when it does
        not - so the caller can report the shortfall rather than being handed a
        plan that quietly leaves somebody dark. Returning only the first two is
        the mistake this contract exists to prevent.
    """
    # TODO: sort by price, keep a trench when join() returns True, and report
    # how many networks are left at the end.
    raise NotImplementedError


# ---- Harness. This is the spec - do not edit. ----
if __name__ == "__main__":
    failed = 0

    def check(label: str, got, want) -> None:
        global failed
        ok = got == want
        failed += not ok
        print(f"    {'ok ' if ok else 'FAIL'} {label:<32} got {got!r}")
        if not ok:
            print(f"         want {want!r}")

    h = Harbour(QUAYS)
    check("starts apart", h.networks, 5)
    check("join joins", h.join("Ferry Slip", "Bait Wharf"), True)
    check("re-join is a no-op", h.join("Bait Wharf", "Ferry Slip"), False)
    check("self join is a no-op", h.join("Dry Dock", "Dry Dock"), False)
    check("same network", h.network_of("Ferry Slip") == h.network_of("Bait Wharf"), True)
    check("different network", h.network_of("Ferry Slip") == h.network_of("Gull Rock"), False)

    total, chosen, left_over = cheapest_cable(QUAYS, TRENCHES)
    check("total cost", total, 9)
    check("trench count", len(chosen), 3)
    check("redundant trench skipped",
          ("Ferry Slip", "Chandlery Steps", 6) in chosen, False)
    check("cheapest first", [t[2] for t in chosen], [2, 3, 4])
    # Gull Rock has no trench, so the plan cannot reach it and the count says so.
    check("networks left over", left_over, 2)

    print()
    print("All checks passed." if failed == 0 else f"{failed} check(s) still failing.")
