"""problem-01-claim-slip-merge-solution.py — merging lost-property slips by phone number.

A station lost-property office writes a claim slip every time someone rings
about a missing bag. Each slip has a name and one or more phone numbers. The
same person rings back from a different phone, and now there are two slips.

Two slips belong to the same person when they share at least one phone
number, and that spreads: slip A shares a number with slip B, slip B shares a
different number with slip C, so all three are one person. The name is not
the key — two different people can share a name, and this file's data has
exactly that.

  merged_claims — one record per person, phones sorted, records sorted

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# [name, phone, phone, ...] as written on each slip
Slip = list[str]

SLIPS: list[Slip] = [
    ["Rosa Lindqvist", "0117 496 0021", "0117 496 0088"],
    ["Rosa Lindqvist", "0117 496 0088", "07700 900142"],
    ["Rosa Lindqvist", "0117 496 5555"],
    ["Deniz Aksoy", "07700 900333"],
    ["Deniz Aksoy", "07700 900333", "0117 496 0777"],
    ["Marek Solc", "0117 496 9000"],
]


# ---- Your task ----
class Slips:
    """Slip numbers grouped into people, with path compression and rank."""

    def __init__(self, slip_count: int) -> None:
        """Start every slip as a person of its own.

        Args:
            slip_count: How many slips the office wrote.
        """
        self.parent: list[int] = list(range(slip_count))
        self.rank: list[int] = [0] * slip_count

    def person_of(self, slip: int) -> int:
        """Return the slip number that names this slip's person.

        Args:
            slip: The slip to look up.

        Returns:
            The root slip number, flattening the path on the way back.
        """
        root = slip
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[slip] != root:
            self.parent[slip], slip = root, self.parent[slip]
        return root

    def join(self, left: int, right: int) -> bool:
        """Merge two slips into one person, shallower tree under deeper.

        Args:
            left: One slip number.
            right: The other slip number.

        Returns:
            True when two separate people turned out to be one. False when
            they were already merged.
        """
        left_root, right_root = self.person_of(left), self.person_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        return True


def merged_claims(slips: list[Slip]) -> list[list[str]]:
    """Return one record per person, built from the slips that share a phone.

    Args:
        slips: Every slip, each [name, phone, phone, ...].

    Returns:
        A list of [name, phone, phone, ...] records. Phones inside a record
        are sorted and appear once. Records are sorted by name, then by the
        phone list, so two people with the same name still come out in a
        fixed order and a slip with no phone at all still sorts.
    """
    owners = Slips(len(slips))
    seen_on: dict[str, int] = {}
    for index, slip in enumerate(slips):
        for phone in slip[1:]:
            if phone in seen_on:
                owners.join(seen_on[phone], index)
            else:
                seen_on[phone] = index

    gathered: dict[int, set[str]] = {}
    for index, slip in enumerate(slips):
        gathered.setdefault(owners.person_of(index), set()).update(slip[1:])

    records = [[slips[root][0], *sorted(phones)] for root, phones in gathered.items()]
    return sorted(records, key=lambda record: (record[0], record[1:]))


def phone_owner(records: list[list[str]], phone: str) -> str | None:
    """Return the name on the record holding this phone number.

    Args:
        records: The output of merged_claims.
        phone: The number to look up.

    Returns:
        The name, or None when no record holds that number.
    """
    for record in records:
        if phone in record[1:]:
            return record[0]
    return None


# ---- Self-check ----
if __name__ == "__main__":
    records = merged_claims(SLIPS)
    print(f"{len(SLIPS)} slips merged into {len(records)} people")
    for record in records:
        print(f"  {record[0]}")
        for phone in record[1:]:
            print(f"      {phone}")

    print()
    print(f"who owns 07700 900142? {phone_owner(records, '07700 900142')}")
    print(f"who owns 0117 496 5555? {phone_owner(records, '0117 496 5555')}")
    print(f"who owns 0117 496 0001? {phone_owner(records, '0117 496 0001')}")

    assert records == [
        ["Deniz Aksoy", "0117 496 0777", "07700 900333"],
        ["Marek Solc", "0117 496 9000"],
        ["Rosa Lindqvist", "0117 496 0021", "0117 496 0088", "07700 900142"],
        ["Rosa Lindqvist", "0117 496 5555"],
    ]
    assert len(records) == 4                   # two of them are called Rosa Lindqvist
    assert phone_owner(records, "0117 496 0001") is None
    assert merged_claims([]) == []
    assert merged_claims([["Pat Ng"]]) == [["Pat Ng"]]
    print("All checks passed.")
