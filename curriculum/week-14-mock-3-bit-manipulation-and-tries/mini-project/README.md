# Mini-Project — Mock #3, the Odd Tally and the Pairing Register

> Topic: the mock, plus one XOR-trick and one binary-trie write-up · Lecture: [1](../lecture-notes/01-bit-manipulation-fundamentals-and-xor.md), [2](../lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md) · Difficulty: Medium-Hard · Target time: 10 hours, Mock #3 on Friday · Why this one: the trie write-up is the bridge that ties this week's bit work back to the Week 9 trie family.

## The Brief

The week's deliverable is three pieces: the Mock #3 recording with its two-pass
self-feedback note, and two portfolio write-ups covering the two bit sub-shapes
that matter most.

**Half one, the odd tally.** A logger writes a fault code every time a relay
trips. Codes trip in pairs, so a healthy log holds every code an even number of
times. This log holds exactly **two** codes an odd number of times. Find them, in
constant space.

One odd code would be a single XOR fold and a two-line answer. Two is the version
worth writing up: folding everything gives you their XOR and neither of them. The
step that separates them is the trick — any set bit in that XOR is a position
where the two differ, so it splits the whole log into two halves with one odd
code in each.

**Half two, the pairing register.** Maintenance wants, for a given register, the
logged register that differs from it most in value — the largest XOR. Checking
every entry is the answer to say first. The **binary trie** is the answer to say
second: store the registers bit by bit from the top, then walk preferring the
opposite bit at each level.

The mock is the keystone. The two write-ups are the evidence that the bit
material is in your hands.

## Starter

The worked answer on this page has both halves solved and the self-checks.

```text
fault log:  00A3  1F04  00A3  2B77  1F04  0051  2B77  8C10

registers:  0000000000000011
            0111111100000000
            1000000000000000
            0000000011111111
```

Fold the fault log by hand first — eight XORs — and look at what you get. It is
not either answer, and seeing that is what makes the second half of the trick
necessary rather than clever.

## Requirements

1. `odd_pair(codes)` returns the two odd codes, **smaller first**, in constant
   space beyond the log itself.
2. It raises `ValueError` when the log does not hold exactly two odd codes —
   including the all-even case, which folds to zero.
3. `BitTrie` stores WIDTH-bit registers and offers `insert` and `best_partner`.
4. `best_partner` returns `None` on an empty trie, and refuses a register that
   does not fit in WIDTH bits.
5. Both halves narrated in FRAME, cross-referenced to each other and to the
   Week 9 trie write-up.

### What you ship

A Mock #3 artifact set plus two problem write-ups.

```
mocks/mock-03/
├── recording-link.md          ← link to the video (file too big to commit)
├── immediate-notes.md         ← 5-minute brain dump right after the clock stops
└── timestamps.md              ← pass-1 timestamps

frame-writeups/c2-week-14/
├── mock-03-self-feedback.md   ← the two-pass self-feedback + trajectory section
└── mini-project/
    ├── README.md                              ← short overview + index + reflection
    ├── problem-01-xor-trick-single-number.md  ← XOR fold (the relay fold
    └── problem-02-binary-trie-maximum-xor.md  ← binary trie (the pairing register,)
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (XOR trick):** the relay fold, narrated as a demonstration of XOR's *algebra* — pairs cancel via `a ^ a == 0`, the survivor remains via `a ^ 0 == a`, order is irrelevant by commutativity and associativity. The discriminator is the constant-space defense: "the hash-map answer is `O(n)` space; the XOR fold is `O(1)`."
- **Problem 2 (binary trie):** the pairing register, narrated as a demonstration of XOR's *structure* — high bits dominate magnitude, so insert MSB-first and greedily walk for the opposite bit. The discriminator is "the `O(n**2)` brute force is too slow; the binary trie is `O(n · 32)`," and the cross-reference to the Week 9 trie ("same dict-of-dict structure, alphabet `{0, 1}`").

Together they cover the bit family's two faces: algebraic cancellation and structural greedy search.

---

### FRAME structure for each write-up

The full five-section format. The Research constraints section opens with the 30-second memo above.

### Frame

Restate the problem in your own words. Walk one example by hand.

### Research constraints

Open with the 30-second memo. Then in 2–3 sentences name the sub-shape (XOR fold / binary trie), the discriminating cue, and the rejected alternative (hash map for Problem 1; brute force for Problem 2). Note the limits and what makes the problem hard:

- Problem 1 — state the binding constraints (linear time, constant space) and why they rule out the hash-map answer.
- Problem 2 — state why the `O(n**2)` brute force is too slow for the constraints, and the structural insight that high bits dominate the XOR.

### Assess options

Numbered steps; 4–6 lines. State the data structure (none / the binary trie) first, the loop shape second, the termination third.

- Problem 1: seed an accumulator at 0; XOR every element; return it.
- Problem 2: build the trie MSB-first; for each number, greedy opposite-bit walk; track the max.

### Make the solution

The code. Type hints on every function. Docstrings on every public function. Comments only where the line is non-obvious — the binary trie's `want = 1 - bit` and the same-bit fallback deserve a comment; the XOR accumulator does not.

### Examine (verify)

Trace each implementation by hand on at least two inputs: one positive case and one edge case (single element for both; for Problem 2 the edge is `[0]` → `0`).

### Examine (cost)

Time and space bounds **with derivation** — the derivation is mandatory, not the bound alone.

- Problem 1: `O(n)` time / `O(1)` space, derived from "one pass, one accumulator."
- Problem 2: `O(n · 32)` time / `O(n · 32)` space, derived from "n insertions of 32 bits, then n walks of 32 steps."

Mention at least one variant in each Examine (cost). Problem 1: the odd tally, which folds to `a ^ b` and partitions on a differing bit. Problem 2: the `O(n**2)` brute force, and a note that the trie generalizes to "max XOR with a constraint" variants.

---

### Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites Problem 2 in its Examine (cost): "Compare to the binary-trie write-up — the relay fold uses XOR's *algebra* (cancellation in a fold), while the pairing register uses XOR's *structure* (high bits dominate, so it needs a data structure). Same operator, two problem shapes."
- The Problem 2 write-up cites Problem 1 in its Research constraints, and cites the Week 9 trie: "Unlike the XOR-fold problem, this cannot be solved by a one-line fold — the structure (high bits dominate) requires the binary trie, which is the Week 9 dict-of-dict trie restricted to the alphabet `{0, 1}`."

The cross-references earn senior signal — they show you navigate the *taxonomy* of the bit family, not just the individual templates.

---

### Rubric

The Mock #3 artifact and each write-up are graded. Total possible: 100; passing: **70 on each component**.

### Mock #3 rubric (the keystone)

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Conditions held | 20 | Video on, hard 45-min clock, no peeking — verifiable from the recording |
| Two-pass review done | 20 | Pass-1 timestamps + pass-2 prescriptions both present |
| Self-feedback complete | 25 | All sections present; Research constraints / thinking-aloud / recovery / Examine (cost) each graded |
| Trajectory section | 20 | Honest comparison across Mock #1 → #2 → #3; prior behavior changes assessed |
| One behavior change for Mock #4 | 15 | Specific and testable; not "be more confident" |

### Problem 1 (XOR trick) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| 30-second memo at the top | 10 | All lines present; the constant-space discriminator vs hash map stated |
| Frame | 10 | One example walked; the contract restated in your own words |
| Research constraints | 20 | The constraints that rule out the hash map stated; XOR fold named; the four identities cited; hash map rejected with reason |
| Assess options | 10 | Accumulator-and-fold sketched |
| Make the solution | 25 | Test cases pass; type hints; PEP 8; idiomatic Python |
| Examine (verify) | 10 | Positive trace + single-element edge case |
| Examine (cost) | 15 | `O(n)`/`O(1)` derived; trade vs hash map; the odd tally variant named |

### Problem 2 (binary trie) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| 30-second memo at the top | 10 | All lines present; the MSB-first / opposite-bit rule stated |
| Frame | 10 | One example walked; the contract restated in your own words |
| Research constraints | 20 | Why brute force is too slow stated; binary trie named; greedy opposite-bit walk explained; brute force rejected |
| Assess options | 10 | Insert MSB-first + greedy walk outlined |
| Make the solution | 25 | Test cases pass; MSB-first insertion correct; same-bit fallback present; type hints |
| Examine (verify) | 10 | Positive trace + `[0]` edge case |
| Examine (cost) | 15 | `O(n · 32)` derived; brute-force trade; the Week 9 trie cross-reference present |

---

## Constraints

- **Constant space in half one.** A counter dictionary answers the question and
  misses the point; the whole reason this is a week-14 problem is that XOR
  answers it without one.
- **`both & -both` isolates the lowest set bit.** Say why in the memo — two's
  complement makes `-x` the complement plus one, so the two agree on exactly
  that bit. Any set bit would work; the lowest is simply the cheapest to name.
- **The split alone does not prove the answer.** A log with four odd codes also
  folds non-zero and splits cleanly. That is why the contract requires the count
  check, and why the error case is part of the deliverable rather than an
  afterthought.
- **Walk the trie from the TOP bit.** A difference high up outweighs every
  difference below it put together, which is why greedy is correct here and is
  the sentence the write-up needs.
- **A missing branch is not a compromise.** Taking the same bit when the opposite
  is absent is taking the only register left.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README.py
HALF ONE - the odd tally
    log: ['0x00A3', '0x1F04', '0x00A3', '0x2B77', '0x1F04', '0x0051', '0x2B77', '0x8C10']
    odd codes: 0x0051 and 0x8C10

HALF TWO - the pairing register
    stored  0000000000000011
    stored  0111111100000000
    stored  1000000000000000
    stored  0000000011111111

    query   0000000000000001
    partner 1000000000000000
    xor     1000000000000001  = 32769

    query   1111111111111111
    partner 0000000000000011
    xor     1111111111111100  = 65532

All checks passed.
```

The second query is the one to read. `1111111111111111` pairs with
`0000000000000011` — the register that is *most unlike* it — and the XOR is
65532, not 65535, because two bits happen to agree. The trie found that without
comparing against the other three registers at all.

## Steps

1. Read the self-checks. They are the spec.
2. Fold the fault log by hand and write down what you get. Then write the memo.
3. Implement the fold, then the split. Check `(5, 5, 5, 8)` — "odd" is not
   "once", and a solution that assumes it is fails there.
4. Add the count check and the `ValueError` cases.
5. Implement the trie insert, then `best_partner`. Test against brute force on
   every query rather than a handful; they must agree everywhere or the greedy
   argument is wrong.
6. Run Mock #3 on Friday under the conditions in
   [Challenge 1](../challenges/challenge-01-mock-3-timed-round.md).
7. Write all three pieces up and cross-reference them.

## The Solution

```python
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
```

The two halves are deliberately the same 16-bit registers seen twice: once as
values to fold, once as paths to walk. That is the week's whole argument — a
register is a number when you XOR it and a path when you index it, and choosing
which view to take is the skill.

## Run it

Download the solution beside this page and run it:

```bash
python README.py
```

No third-party packages, no arguments, no input. It prints both halves and then
`All checks passed.`

## Common bugs to catch

- **Reaching for a counter.** Symptom: correct, and linear space, which is the
  one thing the problem forbids.
- **Assuming "odd" means "once".** Symptom: `(5, 5, 5, 8)` returns the wrong
  pair. Three appearances is odd.
- **Returning the pair in fold order.** Symptom: the answer flips when the log
  is reordered. Sort them.
- **Skipping the count check.** Symptom: a log with four odd codes returns two
  numbers that are not any of them, confidently.
- **Walking the trie from the bottom bit.** Symptom: a partner that is worse than
  brute force finds, on most queries. High bits dominate.
- **Testing the trie on a few queries.** Symptom: agreement on the ones you
  picked. Compare against brute force across the range; it costs nothing.

## Acceptance checklist

The mini-project is complete when:

- The Mock #3 recording link, immediate notes, and pass-1 timestamps are committed under `mocks/mock-03/`.
- The Mock #3 self-feedback (with the trajectory section and one behavior change for Mock #4) is committed under `frame-writeups/c2-week-14/`.
- Both problem write-ups are committed under `frame-writeups/c2-week-14/mini-project/`, each with the 30-second memo at the top.
- The cross-references in both directions are present.
- Both implementations pass the test cases in the Week-14 exercise starters.

Push everything by Sunday end-of-day. Phase 4's second week is closed on the push.

---

## Stretch

- Extend half one to find **three** odd codes and say why the same trick does not
  simply repeat. It is the honest answer, and the reason is worth a paragraph.
- Report the best pairing for **every** stored register, not one query. The trie
  is already built; the loop is free, and the output is something maintenance
  could act on.
- Store a count at each trie node and support removing a register. That is what
  turns this structure into one you could run against a live log rather than a
  snapshot.

## The 30-second pattern-recognition memo templates

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (XOR trick)

```markdown
> **30-second pattern-recognition memo (XOR fold):**
> This is an XOR fold because [every element appears twice except one /
> I need to find the missing element with O(1) extra space].
> Why XOR: pairs cancel (a ^ a == 0), the survivor remains (a ^ 0 == a),
> order is irrelevant (commutative + associative).
> Time O(n), space O(1).
> Why not a hash map: [Counter is O(n) space; the constant-space constraint
> rules it out].
```

### For Problem 2 (binary trie)

```markdown
> **30-second pattern-recognition memo (binary trie):**
> This is a binary-trie problem because [I must maximize / query an XOR over
> a set of integers].
> Structure: a trie over the alphabet {0, 1}; insert each number MSB-first as
> a 32-bit path.
> Greedy walk: at each bit prefer the OPPOSITE bit's child (bit ^ opp == 1
> contributes to the XOR), falling back to the same bit if absent.
> Why MSB-first: high bits dominate the XOR magnitude; commit them first.
> Time O(n * 32), space O(n * 32). Why not brute force: O(n^2) is too slow.
> Bridge: this is the Week 9 dict-of-dict trie restricted to {0, 1}.
```

Read each aloud; both should hit 25–30 seconds.

---

## Self-reflection (in the mini-project README)

End `frame-writeups/c2-week-14/mini-project/README.md` with a short reflection — 4–6 sentences — addressing:

1. Which sub-shape felt more natural — the XOR fold's algebra or the binary trie's structure? Why?
2. What was the hardest part of the binary trie to articulate aloud — the MSB-first insertion, or the opposite-bit greedy walk?
3. Looking at the trajectory across Mock #1 → #2 → #3: what is the one habit that has genuinely improved, and the one that is still your weakest going into Mock #4?

The reflection is the portfolio-grade artifact. Future you — the one walking into the real onsite — will thank present you for writing it.

---

## After the mini-project

Move on to [Week 15 — Capstone + Mock #4](../../week-15-capstone-and-mock-4/). The fourteen-pattern catalog is complete; Week 15 is the dress rehearsal — the capstone project and the final recorded mock, run as the full loop you simulated here for the first time.
