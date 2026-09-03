"""README-solution.py - the Week 14 mini-project, both write-ups worked.

Two problems on the same 16-bit fault codes, one for each sub-shape the week
teaches.

  Half one - the odd tally. A logger writes a fault code every time a relay
  trips. Codes are supposed to trip in pairs, so a healthy log holds every code
  an even number of times. This log holds exactly TWO codes an odd number of
  times. Find them, in constant space.

  One odd code would be a single XOR fold and a two-line answer. TWO odd codes
  is the version worth writing up, because folding everything gives you their
  XOR and not either of them - and the step that separates them is the trick:
  any set bit in that XOR is a bit position where the two differ, so it splits
  the whole log into two halves, one containing each.

  Half two - the pairing register. Maintenance wants, for a given register, the
  logged register that DIFFERS from it most in value - the largest XOR. Checking
  every entry is fine at this size and is the answer to say first. The binary
  trie is the answer to say second: store the registers bit by bit from the top,
  and to maximise the XOR walk the trie preferring the opposite bit at every
  level, taking what is there when the preferred branch is missing.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# Fault codes as logged. Every code appears twice except two of them.
FAULT_LOG: tuple[int, ...] = (
    0x00A3, 0x1F04, 0x00A3, 0x2B77, 0x1F04, 0x0051, 0x2B77, 0x8C10,
)

# Registers to pair off in half two.
REGISTERS: tuple[int, ...] = (0b0000_0000_0000_0011, 0b0111_1111_0000_0000,
                              0b1000_0000_0000_0000, 0b0000_0000_1111_1111)


# ---- Half one: the odd tally ----
def odd_pair(codes: tuple[int, ...]) -> tuple[int, int]:
    """The two codes appearing an odd number of times.

    Fold everything with XOR: every code appearing an even number of times
    cancels itself out, so what survives is the XOR of the two odd ones. It is
    non-zero, because the two are different - which means it has at least one
    set bit, and that bit is a position where they disagree.

    Split the log on that bit and fold each half separately. Each half now
    contains exactly one odd code, and every paired code stays in one half
    because both its copies share every bit.

    Args:
        codes: The log, in any order.

    Returns:
        The two odd codes, smaller first, so the answer is stable.

    Raises:
        ValueError: If the log does not hold exactly two odd codes.
    """
    both = 0
    for code in codes:
        both ^= code
    if both == 0:
        raise ValueError("no two codes appear an odd number of times")

    # The lowest set bit, isolated. `both & -both` works because two's
    # complement makes -x the bitwise complement plus one, which leaves exactly
    # the lowest set bit agreeing.
    splitter = both & -both

    first = 0
    for code in codes:
        if code & splitter:
            first ^= code
    second = both ^ first

    # A log with four odd codes also folds to non-zero and splits cleanly, so
    # the split alone does not prove the answer. Counting does.
    odd = [code for code in set(codes) if codes.count(code) % 2 == 1]
    if len(odd) != 2:
        raise ValueError(f"expected exactly two odd codes, found {len(odd)}")

    return (first, second) if first < second else (second, first)


# ---- Half two: the pairing register ----
class BitTrie:
    """The registers, stored bit by bit from the top."""

    def __init__(self) -> None:
        """Start empty. Each node is a two-slot list: bit 0, then bit 1."""
        self.root: list = [None, None]
        self.size = 0

    def insert(self, value: int) -> None:
        """Add one register.

        Args:
            value: A WIDTH-bit register.

        Raises:
            ValueError: If the value does not fit in WIDTH bits.
        """
        if not 0 <= value < (1 << WIDTH):
            raise ValueError(f"{value} is not a {WIDTH}-bit register")
        node = self.root
        for level in range(WIDTH - 1, -1, -1):
            bit = (value >> level) & 1
            if node[bit] is None:
                node[bit] = [None, None]
            node = node[bit]
        self.size += 1

    def best_partner(self, query: int) -> int | None:
        """The stored register whose XOR with `query` is largest.

        Walks from the top bit down, preferring the OPPOSITE bit at every level
        because a difference high up is worth more than every difference below
        it put together. Where the preferred branch is missing, take the other -
        that is not a compromise, it is the only register left.

        Args:
            query: The register being paired off.

        Returns:
            The best partner, or None when the trie is empty.
        """
        if self.size == 0:
            return None
        node = self.root
        found = 0
        for level in range(WIDTH - 1, -1, -1):
            bit = (query >> level) & 1
            want = 1 - bit
            if node[want] is not None:
                found = (found << 1) | want
                node = node[want]
            else:
                found = (found << 1) | bit
                node = node[bit]
        return found


def best_pairing(registers: tuple[int, ...], query: int) -> tuple[int, int]:
    """The best partner for `query` and the XOR it achieves, via the trie."""
    trie = BitTrie()
    for value in registers:
        trie.insert(value)
    partner = trie.best_partner(query)
    return partner, query ^ partner


# ---- Self-check ----
if __name__ == "__main__":
    print("HALF ONE - the odd tally")
    print(f"    log: {[f'0x{c:04X}' for c in FAULT_LOG]}")
    low, high = odd_pair(FAULT_LOG)
    print(f"    odd codes: 0x{low:04X} and 0x{high:04X}")
    print()

    print("HALF TWO - the pairing register")
    for value in REGISTERS:
        print(f"    stored  {value:0{WIDTH}b}")
    for query in (0b0000_0000_0000_0001, 0b1111_1111_1111_1111):
        partner, xor = best_pairing(REGISTERS, query)
        print()
        print(f"    query   {query:0{WIDTH}b}")
        print(f"    partner {partner:0{WIDTH}b}")
        print(f"    xor     {xor:0{WIDTH}b}  = {xor}")
    print()

    # ---- Half one.
    assert odd_pair(FAULT_LOG) == (0x0051, 0x8C10)

    # Order must not matter, and neither must which of the two is "first".
    assert odd_pair(tuple(reversed(FAULT_LOG))) == (0x0051, 0x8C10)
    assert odd_pair((7, 7, 3, 9)) == (3, 9)
    assert odd_pair((3, 9)) == (3, 9)

    # Codes appearing three times are odd too - "odd" is not "once".
    assert odd_pair((5, 5, 5, 8)) == (5, 8)

    # A log with no odd codes, or with the wrong number of them, is refused
    # rather than answered with two numbers that mean nothing.
    for bad in ((1, 1, 2, 2), (1, 2, 3, 4), (1,)):
        try:
            odd_pair(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    # ---- Half two.
    # The trie must agree with checking every register, on every query. That is
    # the whole claim, so it is tested exhaustively rather than on favourites.
    for query in range(0, 1 << WIDTH, 97):
        partner, xor = best_pairing(REGISTERS, query)
        brute = max(REGISTERS, key=lambda value: query ^ value)
        assert xor == (query ^ brute), (query, partner, brute)

    # An empty trie has no partner to offer.
    assert BitTrie().best_partner(0) is None

    # A trie holding one register always returns it, however bad the pairing.
    single = BitTrie()
    single.insert(0b1010_1010_1010_1010)
    assert single.best_partner(0b1010_1010_1010_1010) == 0b1010_1010_1010_1010

    # Registers are checked rather than silently truncated.
    for bad in (1 << WIDTH, -1):
        try:
            BitTrie().insert(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All checks passed.")
