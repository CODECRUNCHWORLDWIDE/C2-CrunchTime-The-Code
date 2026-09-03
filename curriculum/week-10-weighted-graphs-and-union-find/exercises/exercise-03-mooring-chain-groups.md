# Exercise 3 — The Mooring Chain Groups

> **Topic:** union-find, and watching path compression flatten the parent array
> **Lecture:** [03 — Union-Find and the DSU Triggers](../lecture-notes/03-union-find-and-the-dsu-triggers.md)
> **Difficulty:** Easy-Medium
> **Target time:** 35 minutes
> **Why this one:** union-find is four lines of code and one idea, and the idea is invisible unless you look at the parent array. This page prints it before and after a single lookup, so path compression stops being a phrase and becomes a thing you have seen happen.

## The Brief

A boatyard has twelve numbered berths. Over a morning the crew shackle pairs of
berths together with chain. Shackle 3 to 7, and anything already chained to 3 is
now chained to 7 as well — the chain does not care how it got there.

Report three things: how many separate chains exist after each shackle, the
finished chains as sorted lists, and the parent array **before and after** one
lookup, so path compression is visible.

## Starter

`exercise-03-mooring-chain-groups-solution.py` sits beside this page with the
shackles and the self-checks.

```text
12 berths, numbered 0 to 11

shackles, in order
  0-1   1-2   2-3   3-0   5-6   7-8   6-7   9-10   10-9   4-5
```

Two of those ten shackles join nothing. `3-0` closes a loop — 0 and 3 are already
in one chain by then — and `10-9` is the same shackle done twice. Both must leave
the chain count unchanged, and spotting them on the count line is the first check
of your implementation.

## Requirements

1. `Moorings` implements union-find with a `chain_of` lookup and a `shackle`
   join.
2. `chain_counts(berth_count, shackles)` returns the number of chains after each
   shackle.
3. `chain_roster(berth_count, shackles)` returns the finished chains as sorted
   lists, in a stable order.
4. `parent_trail(berth_count, shackles, berth)` returns the parent array before
   and after one `chain_of` call.
5. A berth nobody shackled is a chain of one.

## Constraints

- **Path compression on lookup.** After `chain_of(0)` every berth on that lookup
  path points straight at the root, and the printed arrays have to show it.
- **Union by size or rank on join**, and the write-up says which and why. Without
  it the parent array can grow into a chain and lookups stop being near-constant.
- **A redundant shackle changes nothing.** Both `3-0` and `10-9` must leave the
  count where it was. If either drops it, the join is not checking roots first.
- **Berth 11 is a chain on its own.** A berth nobody touched is not missing from
  the roster.
- **The roster order is stable**, so two runs agree and a test can assert it.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-03-mooring-chain-groups-solution.py
chains left after each shackle
  shackle  0-1  -> 11 chains
  shackle  1-2  -> 10 chains
  shackle  2-3  -> 9 chains
  shackle  3-0  -> 9 chains
  shackle  5-6  -> 8 chains
  shackle  7-8  -> 7 chains
  shackle  6-7  -> 6 chains
  shackle  9-10 -> 5 chains
  shackle 10-9  -> 5 chains
  shackle  4-5  -> 4 chains

finished chains
  [0, 1, 2, 3]
  [4, 5, 6, 7, 8]
  [9, 10]
  [11]

parents before chain_of(0): [1, 2, 3, 3, 8, 6, 8, 8, 8, 10, 10, 11]
parents after  chain_of(0): [3, 3, 3, 3, 8, 6, 8, 8, 8, 10, 10, 11]
All checks passed.
```

Two things to read.

**The count line** starts at 12 implied and falls to 4, and it does **not** fall
at `3-0` or at `10-9`. Those two rows are the redundancy check, sitting in the
output where you cannot miss them.

**The parent arrays** are the exercise. Before `chain_of(0)` the array starts
`[1, 2, 3, 3, ...]` — berth 0 points at 1, which points at 2, which points at 3.
Afterwards it starts `[3, 3, 3, 3, ...]` — every berth on that path now points
straight at the root. That is path compression, in two printed lines, and nothing
about the chains themselves changed.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: an array of parents, a lookup that walks to the root, a join
   that points one root at the other.
3. Write `chain_of` **without** compression first and print the parent array.
   Then add compression and print it again. The difference is the point of the
   page.
4. Add union by size. Say in the memo what would go wrong without it.
5. Write `chain_counts` and check `3-0` and `10-9` leave it unchanged.
6. Write `chain_roster` with a stable order, and confirm berth 11 is in it.
7. Write the FRAME pass, with the two parent arrays in the Measure section.

## The Solution

```python
"""exercise-03-mooring-chain-groups-solution.py — union-find on a boatyard's moorings.

A boatyard has twelve numbered berths. Over a morning the crew shackle pairs
of berths together with chain. Shackle 3 to 7, and anything already chained
to 3 is now chained to 7 as well — the chain does not care how it got there.

Three things to report:

  chain_counts  — how many separate chains exist after each shackle
  chain_roster  — the finished chains, as sorted lists of berth numbers
  parent_trail  — the parent array before and after one find, so you can see
                  path compression flatten it

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
BERTH_COUNT = 12

# (berth, berth) pairs, in the order the crew shackled them
SHACKLES: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),   # closes a loop; nothing new is joined
    (5, 6),
    (7, 8),
    (6, 7),
    (9, 10),
    (10, 9),  # the same shackle, done twice
    (4, 5),
]


# ---- Your task ----
class Moorings:
    """Berths grouped into chains, with path compression and union by rank.

    Every berth starts alone. `join` shackles two berths together. `chain_of`
    reports which chain a berth belongs to, named after its root berth.
    """

    def __init__(self, berth_count: int) -> None:
        """Start every berth in a chain of its own.

        Args:
            berth_count: How many berths the yard has, numbered from 0.
        """
        self.parent: list[int] = list(range(berth_count))
        self.rank: list[int] = [0] * berth_count
        self.chains: int = berth_count

    def chain_of(self, berth: int) -> int:
        """Return the root berth of this berth's chain, flattening on the way.

        Args:
            berth: The berth to look up.

        Returns:
            The root berth. Two berths are on the same chain exactly when
            this returns the same number for both.
        """
        root = berth
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[berth] != root:      # path compression, second pass
            self.parent[berth], berth = root, self.parent[berth]
        return root

    def join(self, left: int, right: int) -> bool:
        """Shackle two berths together, smaller tree under larger.

        Args:
            left: One berth.
            right: The other berth.

        Returns:
            True when this shackle joined two chains that were apart.
            False when the two berths were already on one chain, which means
            the shackle closed a loop and changed nothing.
        """
        left_root, right_root = self.chain_of(left), self.chain_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.chains -= 1
        return True


def chain_counts(berth_count: int, shackles: list[tuple[int, int]]) -> list[int]:
    """Return how many separate chains remain after each shackle.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.

    Returns:
        One number per shackle. A shackle that closed a loop repeats the
        previous number, which is how a loop shows up in the report.
    """
    moorings = Moorings(berth_count)
    counts = []
    for left, right in shackles:
        moorings.join(left, right)
        counts.append(moorings.chains)
    return counts


def chain_roster(berth_count: int, shackles: list[tuple[int, int]]) -> list[list[int]]:
    """Return the finished chains, each as a sorted list of berth numbers.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.

    Returns:
        A list of chains, sorted by each chain's smallest berth. A berth that
        was never shackled to anything is a chain of one and is included.
    """
    moorings = Moorings(berth_count)
    for left, right in shackles:
        moorings.join(left, right)
    grouped: dict[int, list[int]] = {}
    for berth in range(berth_count):
        grouped.setdefault(moorings.chain_of(berth), []).append(berth)
    return sorted(grouped.values())


def parent_trail(berth_count: int, shackles: list[tuple[int, int]], berth: int) -> tuple[list[int], list[int]]:
    """Return the parent array either side of one `chain_of` call.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.
        berth: The berth to look up once, after all the shackling.

    Returns:
        (before, after) copies of the parent array. Any position that changed
        was shortened by path compression.
    """
    moorings = Moorings(berth_count)

    def plain_root(start: int) -> int:
        """Walk to the root without flattening anything on the way."""
        while moorings.parent[start] != start:
            start = moorings.parent[start]
        return start

    for left, right in shackles:
        left_root, right_root = plain_root(left), plain_root(right)
        if left_root != right_root:            # no rank either, so the tree stays deep
            moorings.parent[left_root] = right_root
            moorings.chains -= 1
    before = list(moorings.parent)
    moorings.chain_of(berth)
    return before, list(moorings.parent)


# ---- Self-check ----
if __name__ == "__main__":
    print("chains left after each shackle")
    for (left, right), left_over in zip(SHACKLES, chain_counts(BERTH_COUNT, SHACKLES)):
        print(f"  shackle {left:2d}-{right:<2d} -> {left_over} chains")

    print()
    print("finished chains")
    for chain in chain_roster(BERTH_COUNT, SHACKLES):
        print(f"  {chain}")

    before, after = parent_trail(BERTH_COUNT, SHACKLES, 0)
    print()
    print(f"parents before chain_of(0): {before}")
    print(f"parents after  chain_of(0): {after}")

    assert chain_counts(BERTH_COUNT, SHACKLES) == [11, 10, 9, 9, 8, 7, 6, 5, 5, 4]
    assert chain_roster(BERTH_COUNT, SHACKLES) == [
        [0, 1, 2, 3],
        [4, 5, 6, 7, 8],
        [9, 10],
        [11],
    ]

    moorings = Moorings(4)
    assert moorings.join(0, 1) is True
    assert moorings.join(1, 0) is False        # already one chain
    assert moorings.chains == 3
    assert moorings.chain_of(0) == moorings.chain_of(1)
    assert moorings.chain_of(2) != moorings.chain_of(3)
    assert before != after                     # the find really did flatten something
    print("All checks passed.")
```

`parent_trail` exists only to make the mechanism printable. It is not something a
production union-find would expose, and it is exactly the sort of thing worth
writing while you are learning one — an invariant you can print is an invariant
you can check.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-03-mooring-chain-groups-solution.py
```

No third-party packages, no arguments, no input. It prints the count after each
shackle, the finished chains, both parent arrays, and then `All checks passed.`

## Common bugs to catch

- **Joining without checking the roots first.** Symptom: the count falls at `3-0`
  and at `10-9`, which is two berths joined that were already joined.
- **Comparing berths instead of roots.** Symptom: chains that split back apart
  depending on the order the shackles arrive in.
- **No compression.** Symptom: correct answers, a parent array that stays deep,
  and lookups that get slower as the morning goes on.
- **No union by size.** Symptom: correct answers on twelve berths, and a
  degenerate chain on ten thousand.
- **Dropping untouched berths.** Symptom: a roster of three chains where four is
  right. Berth 11 counts.
- **An unstable roster order.** Symptom: a test that passes on Tuesday.

## Acceptance checklist

- [ ] The chain count falls to 4 and does not move at `3-0` or `10-9`.
- [ ] The roster is `[0,1,2,3]`, `[4,5,6,7,8]`, `[9,10]`, `[11]`.
- [ ] Berth 11 appears as a chain of one.
- [ ] `chain_of(0)` flattens every berth on its path to point at the root.
- [ ] The parent arrays before and after differ, and the chains do not.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Count the total steps taken by all twelve lookups, with and without
  compression. On twelve berths the difference is small; print it anyway, then
  scale the yard to a thousand and print it again.
- Report the **size** of each chain without building the roster. The union-by-size
  bookkeeping already knows it.
- Add an `unshackle`. It is much harder than it looks, and working out why is
  worth more than the code — union-find is a one-way structure by design.
