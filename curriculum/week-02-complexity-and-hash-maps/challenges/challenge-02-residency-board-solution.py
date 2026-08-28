"""challenge-02-residency-board-solution.py — a fixed-slot residency board.

Two structures, composed. A dict gives O(1) lookup by asset id but knows
nothing about order. A doubly-linked list gives O(1) removal and O(1) append
at the hot end but knows nothing about ids. Store the *node* in the dict, not
the payload, and both halves become O(1).

Time: O(1) average for pin, touch and peek. resident() is O(k) in the number
of resident assets, which is the size of its own return value.
Space: O(slots) — one node and one dict entry per resident asset.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


class _Slot:
    """One resident asset, linked between a colder and a hotter neighbour."""

    __slots__ = ("asset_id", "payload", "colder", "hotter")

    def __init__(self, asset_id: str = "", payload: str = "") -> None:
        self.asset_id = asset_id
        self.payload = payload
        self.colder: "_Slot | None" = None
        self.hotter: "_Slot | None" = None


class ResidencyBoard:
    """A fixed-slot LRU residency board.

    self._cold and self._hot are sentinels that are never resident. The
    coldest real asset is self._cold.hotter and the hottest is
    self._hot.colder, so no method ever has to null-check a neighbour.
    """

    def __init__(self, slots: int) -> None:
        """Create a board with `slots` slots.

        Args:
            slots: How many assets may be resident at once.

        Raises:
            ValueError: If slots is less than one.
        """
        if slots < 1:
            raise ValueError("a board needs at least one slot")
        self._capacity = slots
        self._index: dict[str, _Slot] = {}
        self._cold = _Slot()
        self._hot = _Slot()
        self._cold.hotter = self._hot
        self._hot.colder = self._cold

    def _unlink(self, slot: _Slot) -> None:
        """Take a slot out of the list. Both neighbours always exist."""
        slot.colder.hotter = slot.hotter
        slot.hotter.colder = slot.colder

    def _link_hot(self, slot: _Slot) -> None:
        """Put a slot back in at the hot end."""
        previous_hottest = self._hot.colder
        previous_hottest.hotter = slot
        slot.colder = previous_hottest
        slot.hotter = self._hot
        self._hot.colder = slot

    def pin(self, asset_id: str, payload: str) -> str | None:
        """Make an asset resident, counting it as a use.

        Args:
            asset_id: The asset to pin.
            payload: The asset's data.

        Returns:
            The id of the asset evicted to make room, or None when nothing
            was evicted — including every re-pin, which does not change how
            many slots are occupied.
        """
        slot = self._index.get(asset_id)
        if slot is not None:
            slot.payload = payload
            self._unlink(slot)
            self._link_hot(slot)
            return None

        evicted: str | None = None
        if len(self._index) == self._capacity:
            coldest = self._cold.hotter
            self._unlink(coldest)
            del self._index[coldest.asset_id]
            evicted = coldest.asset_id

        fresh = _Slot(asset_id, payload)
        self._index[asset_id] = fresh
        self._link_hot(fresh)
        return evicted

    def touch(self, asset_id: str) -> str | None:
        """Return an asset's payload and count it as a use.

        Args:
            asset_id: The asset to read.

        Returns:
            The payload, or None if the asset is not resident. A miss
            changes nothing.
        """
        slot = self._index.get(asset_id)
        if slot is None:
            return None
        self._unlink(slot)
        self._link_hot(slot)
        return slot.payload

    def peek(self, asset_id: str) -> str | None:
        """Return an asset's payload without counting it as a use.

        Args:
            asset_id: The asset to inspect.

        Returns:
            The payload, or None if the asset is not resident. The board is
            exactly as it was before the call.
        """
        slot = self._index.get(asset_id)
        return None if slot is None else slot.payload

    def resident(self) -> list[str]:
        """Return the resident asset ids in use order, coldest first."""
        order: list[str] = []
        slot = self._cold.hotter
        while slot is not self._hot:
            order.append(slot.asset_id)
            slot = slot.hotter
        return order


# ---- Self-check ----
if __name__ == "__main__":
    def peek_does_not_protect() -> None:
        board = ResidencyBoard(2)
        assert board.pin("brick", "brick_2k.ktx") is None
        assert board.pin("moss", "moss_2k.ktx") is None
        assert board.peek("brick") == "brick_2k.ktx"
        assert board.resident() == ["brick", "moss"]
        assert board.pin("rust", "rust_2k.ktx") == "brick"
        assert board.resident() == ["moss", "rust"]

    def touch_does_protect() -> None:
        board = ResidencyBoard(2)
        board.pin("brick", "brick_2k.ktx")
        board.pin("moss", "moss_2k.ktx")
        assert board.touch("brick") == "brick_2k.ktx"
        assert board.resident() == ["moss", "brick"]
        assert board.pin("rust", "rust_2k.ktx") == "moss"
        assert board.resident() == ["brick", "rust"]

    def repin_uses_but_never_evicts() -> None:
        board = ResidencyBoard(2)
        board.pin("bark", "bark_2k.ktx")
        board.pin("moss", "moss_2k.ktx")
        assert board.resident() == ["bark", "moss"]
        assert board.pin("bark", "bark_4k.ktx") is None
        assert board.resident() == ["moss", "bark"]
        assert board.peek("bark") == "bark_4k.ktx"
        assert board.pin("rust", "rust_2k.ktx") == "moss"
        assert board.resident() == ["bark", "rust"]

    def misses_are_inert() -> None:
        board = ResidencyBoard(2)
        board.pin("brick", "brick_2k.ktx")
        board.pin("moss", "moss_2k.ktx")
        assert board.touch("rust") is None
        assert board.peek("rust") is None
        assert board.resident() == ["brick", "moss"]

    def single_slot_board() -> None:
        board = ResidencyBoard(1)
        assert board.pin("brick", "brick_2k.ktx") is None
        assert board.pin("moss", "moss_2k.ktx") == "brick"
        assert board.touch("brick") is None
        assert board.peek("moss") == "moss_2k.ktx"
        assert board.resident() == ["moss"]

    def empty_board() -> None:
        board = ResidencyBoard(3)
        assert board.resident() == []
        assert board.touch("brick") is None
        assert board.peek("brick") is None

    def zero_slots_rejected() -> None:
        try:
            ResidencyBoard(0)
        except ValueError:
            return
        raise AssertionError("ResidencyBoard(0) should raise ValueError")

    for check in (
        peek_does_not_protect,
        touch_does_protect,
        repin_uses_but_never_evicts,
        misses_are_inert,
        single_slot_board,
        empty_board,
        zero_slots_rejected,
    ):
        check()
        print(f"ok  {check.__name__}")

    board = ResidencyBoard(2)
    session: list[tuple[str, str, str]] = [
        ("pin", "brick", "brick_2k.ktx"),
        ("pin", "moss", "moss_2k.ktx"),
        ("peek", "brick", ""),
        ("pin", "rust", "rust_2k.ktx"),
        ("touch", "moss", ""),
        ("pin", "bark", "bark_2k.ktx"),
        ("touch", "brick", ""),
        ("pin", "moss", "moss_4k.ktx"),
        ("peek", "moss", ""),
    ]
    print()
    print("call                         returned        resident (coldest first)")
    for method, asset_id, payload in session:
        if method == "pin":
            result = board.pin(asset_id, payload)
            call = f"pin({asset_id!r}, {payload!r})"
        elif method == "touch":
            result = board.touch(asset_id)
            call = f"touch({asset_id!r})"
        else:
            result = board.peek(asset_id)
            call = f"peek({asset_id!r})"
        print(f"{call:<28} {str(result):<15} {board.resident()}")

    assert board.resident() == ["bark", "moss"]
    print()
    print("All checks passed.")
