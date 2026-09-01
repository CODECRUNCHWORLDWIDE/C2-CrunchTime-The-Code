# Challenge 2 — The Texture Residency Board

> **Topic:** a hash map composed with a doubly-linked list — one structure for looking things up, a second for keeping them in order, joined by storing nodes instead of values
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Hard
> **Target time:** 2 hours 30 minutes
> **Why this one:** the week's only *design* problem. You are not writing a function, you are building a class whose invariants have to hold after every one of five methods, with a constant-time guarantee on three of them. And this contract deliberately splits "look at it" from "use it" — a join that remembered versions of this shape are welded shut at, because they only ever have one read method.

## The Brief

A shelf holds four books. You want a fifth. Something has to come off the shelf,
and the fair thing to take off is the one you have not opened in longest. That
rule has a name — **least recently used**, or LRU — and it is how caches
everywhere decide what to throw away.

Now the hard part, and it is not the rule. It is doing the bookkeeping *fast*.

You need to answer two completely different questions about the same collection:

- **"Where is the book called *Moss*?"** — a lookup by name. A hash map answers
  that instantly and has no idea what order anything is in.
- **"Which book has gone longest unopened?"** — a question about order. A list
  answers that instantly and has no idea where *Moss* is.

Neither structure can do both. So you use both, and you join them with one
trick: **the map's value is the list's node, not the book.** Look up *Moss* in
the map and you get the exact link in the chain, which you can then unhook and
re-hook at the hot end without walking anything. Two `O(1)` structures, composed
into one `O(1)` answer.

The linked list is a chain of nodes where each node knows its neighbour on both
sides. Because it knows both, removing a node from the middle is four pointer
writes and no searching — which is the entire reason it is a *doubly*-linked
list rather than a singly-linked one.

Here is the contract.

A game server keeps a fixed number of texture **slots** resident in GPU memory.
When a new texture is pinned and every slot is taken, the least recently used
texture is dropped to make room.

Build the `ResidencyBoard` class:

- **`ResidencyBoard(slots: int)`** — create a board with `slots` slots. A board
  with fewer than one slot is not a thing; raise `ValueError`.
- **`pin(asset_id: str, payload: str) -> str | None`** — make an asset resident,
  and **count it as a use**. If the asset was already resident, replace its
  payload and return `None`; nothing is evicted, because the number of occupied
  slots did not change. Otherwise, if the board is full, evict the least
  recently used asset first and **return the evicted asset's id**. Return `None`
  if nothing was evicted.
- **`touch(asset_id: str) -> str | None`** — return the asset's payload and
  **count it as a use**. Return `None` if the asset is not resident; a miss
  changes nothing about the board.
- **`peek(asset_id: str) -> str | None`** — return the asset's payload
  **without counting it as a use**. Return `None` if the asset is not resident.
  The board is exactly as it was before the call.
- **`resident() -> list[str]`** — return the resident asset ids in use order,
  **coldest first, hottest last**. This exists so the ordering is observable; it
  is a diagnostic, not a hot-path call.

**`pin`, `touch` and `peek` must each run in `O(1)` average time.** That is the
challenge. `resident()` is allowed to be linear in the number of resident
assets, for the obvious reason that it returns all of them.

**The `peek` split is the whole problem.** A debugger inspecting GPU memory must
not perturb what gets evicted next — observing a thing is not using it. Real
caches make that distinction, and an implementation that fused the two is simply
wrong here, whatever it does elsewhere.

## Starter

Create `challenge-02-residency-board.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""challenge-02-residency-board.py — a fixed-slot residency board.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the class is correct.
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
        # TODO: reject slots < 1, then set up the map and the two sentinels.
        ...

    def _unlink(self, slot: _Slot) -> None:
        """Take a slot out of the list. Both neighbours always exist."""
        # TODO: two pointer writes.
        ...

    def _link_hot(self, slot: _Slot) -> None:
        """Put a slot back in at the hot end."""
        # TODO: four pointer writes.
        ...

    def pin(self, asset_id: str, payload: str) -> str | None:
        # TODO: resident -> update payload, move hot, return None.
        # Not resident -> evict first IF full, then insert at the hot end.
        ...

    def touch(self, asset_id: str) -> str | None:
        # TODO: miss returns None and changes nothing. Hit moves hot.
        ...

    def peek(self, asset_id: str) -> str | None:
        # TODO: a bare map lookup. Nothing moves. Write this one first.
        ...

    def resident(self) -> list[str]:
        # TODO: walk from the cold sentinel to the hot one.
        ...


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
```

Three words before you start.

**Sentinel.** A fake node that is always there so the real ones always have
neighbours. Two of them, one at each end. They exist for exactly one reason: so
that no method ever has to ask "is the list empty?" or "is this the last one?"

**Invariant.** Something that is true before a method runs and true again after
it finishes. Write yours down before you write code — they are the actual
deliverable of a design problem, and this page lists five of them below.

**Composition.** Using two structures together so that each covers what the
other cannot. The joint is the important bit: here, the map's value is a
*node*, and that one decision is what makes everything `O(1)`.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/challenges/challenge-02-residency-board.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `pin`, `touch` and `peek` each run in `O(1)` average time. A design that
   scans the map or walks the list to find the coldest asset does not pass,
   however cleanly it reads.
2. `peek` provably does not reorder. A `peek` followed by an eviction must evict
   the peeked asset if it was coldest.
3. `touch` on a resident asset moves it to the hot end; on a non-resident asset
   it returns `None` and changes nothing.
4. `pin` on a resident asset updates the payload, counts as a use, and evicts
   nothing.
5. `pin` on a new asset evicts only when the board is full, and eviction happens
   **before** insertion.
6. `resident()` returns ids coldest first, hottest last, and never includes a
   sentinel.
7. `ResidencyBoard(0)` raises `ValueError`.
8. All three read paths signal absence with `None` — never `-1`, never an
   exception.
9. Every method keeps its type hints and its docstring.

## Constraints

- **`1 <= slots <= 100_000`.** The upper bound is the one that does the work: an
  implementation that finds the coldest asset by *scanning* its map on every
  eviction is `O(slots)` per pin, and at 100,000 slots across a million pins
  that is `10^11` operations. The bound exists to reject the scan-on-evict
  design, which is otherwise perfectly readable and completely correct.

- **Up to `2_000_000` calls across the five methods in one session.** Note
  honestly what this bound does *not* do: an `O(log slots)` design built on a
  heap of timestamps would survive it comfortably. `O(1)` is required
  explicitly, as a spec requirement, and you have to defend it rather than let a
  timer defend it for you.

- **`asset_id` is a non-empty ASCII string of at most 64 characters; `payload`
  is a string of at most 4,096 characters.** Because ids are strings, hashing
  one is `O(len(id))`, not free. With a 64-character cap that cost is a constant
  and folds into `O(1)` — but say the sentence out loud, because "it's a dict so
  it's O(1)" is the answer of somebody who has not thought about what gets
  hashed. The payload cap matters for a different reason: payloads are stored by
  reference, so a re-pin swaps a pointer and never copies 4,096 characters.

- **The read-versus-use split is a spec requirement, not an optimisation.** A
  debugger reading GPU memory must not change what gets evicted next. This is
  the constraint that makes a remembered LRU implementation wrong here, because
  the usual shape has one read method and no way to express the difference.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-residency-board-solution.py
ok  peek_does_not_protect
ok  touch_does_protect
ok  repin_uses_but_never_evicts
ok  misses_are_inert
ok  single_slot_board
ok  empty_board
ok  zero_slots_rejected

call                         returned        resident (coldest first)
pin('brick', 'brick_2k.ktx') None            ['brick']
pin('moss', 'moss_2k.ktx')   None            ['brick', 'moss']
peek('brick')                brick_2k.ktx    ['brick', 'moss']
pin('rust', 'rust_2k.ktx')   brick           ['moss', 'rust']
touch('moss')                moss_2k.ktx     ['rust', 'moss']
pin('bark', 'bark_2k.ktx')   rust            ['moss', 'bark']
touch('brick')               None            ['moss', 'bark']
pin('moss', 'moss_4k.ktx')   None            ['bark', 'moss']
peek('moss')                 moss_4k.ktx     ['bark', 'moss']

All checks passed.
```

**The third line of the session is the whole problem.** `peek('brick')` reads
brick's payload and does **not** protect it, so the very next `pin` evicts it.
If your implementation returns `moss` on that pin, you have written `peek` as an
alias for `touch`.

Two more lines are worth pausing on. `touch('brick')` on a non-resident asset
returns `None` and leaves the order alone — a miss is not a use. And
`pin('moss', 'moss_4k.ktx')` on an already-resident asset updates the payload,
counts as a use, and evicts **nothing**, because the number of occupied slots
did not change.

## Steps

1. Create the file, paste the starter, and run it. Every check fails.
2. **Write the invariants down on paper before you write any code.** All five of
   them are listed in the solution below, but write your own first and then
   compare — the comparison is more useful than the list.
3. Implement `__init__`, `_unlink` and `_link_hot`. Nothing else. Then, in a
   REPL, build a board, hand-make two `_Slot`s, link them, unlink one, and print
   the chain both ways. Convince yourself the pointer surgery is right in
   isolation, because every later bug will otherwise look like it lives
   somewhere else.
4. Implement `peek` and `resident()`. `peek` is one map lookup with no
   reordering call — write it *before* `touch` so the difference stays in your
   head.
5. Implement `touch`. Now compare it to `peek` line by line. They differ by two
   lines, and those two lines are the specification.
6. Implement `pin`, branching on resident-or-not. Only the not-resident branch
   can evict.
7. Run. All seven checks plus the session should pass.
8. Trace the single-slot board on paper. That is where sentinel bugs surface,
   because the coldest and hottest asset are the same node.
9. Break it on purpose: make `peek` call `_link_hot`. Watch
   `peek_does_not_protect` fail and read the assertion. Put it back.

## The Solution

```python
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
```

**Write the invariants first. They are the deliverable.**

1. `self._index` holds exactly the asset ids that appear in the linked list,
   excluding the two sentinels. Not a superset, not a subset. Every eviction
   updates **both**, or they drift apart and the next lookup hands you a node
   that is no longer linked to anything.
2. The list is ordered coldest to hottest. `self._cold.hotter` is the eviction
   candidate; `self._hot.colder` is the most recently used.
3. `pin` and `touch` on a **resident** asset move its slot to the hot end.
   `peek` moves nothing. `touch` and `peek` on a **non-resident** asset move
   nothing.
4. `len(self._index) <= self._capacity` after every call, and eviction happens
   **before** insertion, never after.
5. Sentinels are never in `self._index`, never returned by `resident()`, and
   never evicted.

Invariant 3 is the one this challenge exists to test. Invariant 1 is the one
that will actually bite you.

**The map stores nodes, not payloads, and that single decision is the design.**

```python
self._index: dict[str, _Slot] = {}
```

If the map stored payloads you would have `O(1)` reads and no way to reorder
anything, because you would not know where in the chain the asset sat. Storing
the node means a lookup hands you the exact link, and unhooking a link you
already hold is four pointer writes with nothing to search. Say that sentence in
an interview and you have said the whole answer.

**The sentinels remove every null check, and that is their only job.**

```python
self._cold.hotter = self._hot
self._hot.colder = self._cold
```

Because a real slot always has a neighbour on both sides, `_unlink` can
dereference `slot.colder` and `slot.hotter` unconditionally, and `_link_hot`
never has to ask whether the list is empty. Skip the sentinels and every method
grows two special cases — the empty list and the single-element list — and on a
one-slot board those two cases are most of the state space. "I use sentinels so
the pointer code has no special cases" is a sentence that buys credibility
cheaply and honestly.

**All the pointer surgery lives in two helpers, and nowhere else.** `_unlink`
and `_link_hot` are each provably correct in isolation, in about thirty seconds
of reading. Every public method is then a couple of helper calls plus its own
branch. That is not tidiness — it is the difference between one place where a
linking bug can live and five.

**Read `peek` against `touch`.** They differ by exactly two lines:

```python
        self._unlink(slot)
        self._link_hot(slot)
```

Those two lines *are* the contract. Every remembered version of this shape has
one read method and therefore cannot express the distinction at all, which is
why a memorised solution fails this page while a derived one does not. The
instant a contract distinguishes *observing* state from *using* it, any
implementation that fused the two is wrong — and no amount of recall tells you
that. Only reading the spec does.

**`pin` branches on residency before it looks at capacity, and the order
matters.** A re-pin does not change how many slots are occupied, so it cannot
evict. Check capacity first and you evict on every update, and eventually evict
the very asset you are updating. The resident branch returns early, which is
what keeps the eviction code on a path that only new assets reach.

**Eviction updates the list and the map together.**

```python
coldest = self._cold.hotter
self._unlink(coldest)
del self._index[coldest.asset_id]
```

Miss that `del` and the list shrinks while the map does not.
`len(self._index)` then drifts above capacity, and every later `pin` evicts
spuriously. This is invariant 1, and it is the bug that takes longest to find,
because it stays silent for a while before anything looks wrong.

**`resident()` is `O(k)` and cannot be better.** It builds a list of every
resident id, so its cost is the size of its own return value. Claiming `O(1)`
for it is a tell that you have stopped reading your own code. Say `O(k)` and say
why that is fine: it is a diagnostic, not a hot path.

**The cost, said properly.** *Time*: `O(1)` average for `pin`, `touch` and
`peek` — a constant number of map operations plus a constant number of pointer
writes, with map operations `O(1)` average and `O(n)` worst case under
adversarial collisions that Python's randomised string hashing makes unreachable
in practice. Hashing a 64-character id is `O(64)`, a constant, which folds in.
`resident()` is `O(k)` in the number of resident assets. *Space*: `O(slots)` —
one node and one map entry per resident asset, plus two sentinels. *Best,
average and worst are the same* for the three hot methods; there is no input
that makes them do more work. *Tradeoff*: a heap keyed by a use counter gets you
`O(log slots)` per operation with far less pointer work and a much smaller
chance of a linking bug — genuinely easier to get right, and rejected here only
because the spec demands `O(1)`. *Improvement*: none available; every operation
already touches a constant amount of state.

**`OrderedDict` is the same composition, pre-built.** Present this in an
interview *after* you have shown you can build the thing:

```python
from collections import OrderedDict


class ResidencyBoard:
    def __init__(self, slots: int) -> None:
        if slots < 1:
            raise ValueError("a board needs at least one slot")
        self._capacity = slots
        self._board: OrderedDict[str, str] = OrderedDict()

    def pin(self, asset_id: str, payload: str) -> str | None:
        if asset_id in self._board:
            self._board[asset_id] = payload
            self._board.move_to_end(asset_id)
            return None
        evicted: str | None = None
        if len(self._board) == self._capacity:
            evicted, _ = self._board.popitem(last=False)
        self._board[asset_id] = payload
        return evicted

    def touch(self, asset_id: str) -> str | None:
        if asset_id not in self._board:
            return None
        self._board.move_to_end(asset_id)
        return self._board[asset_id]

    def peek(self, asset_id: str) -> str | None:
        return self._board.get(asset_id)

    def resident(self) -> list[str]:
        return list(self._board)
```

`OrderedDict` *is* a hash map with a doubly-linked list threaded through it —
the exact composition this problem is about. `move_to_end` and
`popitem(last=False)` are both `O(1)`, so you may claim the complexity honestly.
Notice how naturally `peek` falls out: it is `.get`, with no reordering call,
because in this structure the reordering is *explicit* rather than implied by
access. Expect "now without `OrderedDict`" as the immediate follow-up, and
expect it to be fair — the point of the question is whether you can build the
composition, not whether you can name the module that ships one.

## Download and run

Download
[challenge-02-residency-board-solution.py](./challenge-02-residency-board-solution.py)
and run it:

```bash
python challenge-02-residency-board-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-02-residency-board.py`.

## Common bugs to catch

- **`peek` protects the asset it read.** The most likely failure on this
  challenge, because it is what the shape "usually" does:

  ```text
  Traceback (most recent call last):
      assert board.pin("rust", "rust_2k.ktx") == "brick"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  The pin returned `moss` instead of `brick`, because your `peek` moved brick to
  the hot end. Write `peek_does_not_protect` before you write `peek`.

- **`AttributeError: 'NoneType' object has no attribute 'hotter'`.** You skipped
  the sentinels, so a real slot's neighbour is sometimes `None`:

  ```text
  Traceback (most recent call last):
      slot.colder.hotter = slot.hotter
      ^^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'hotter'
  ```

  Either add the sentinels, or add a null check to every one of the four pointer
  writes and to both ends of every method. The sentinels are two objects; the
  null checks are a permanent tax.

- **Evicting on a re-pin.** Your `pin` checked capacity before checking
  residency. `repin_uses_but_never_evicts` catches it: the re-pin returns an
  evicted id where `None` was required, and on a one-slot board it evicts the
  asset it is updating.

- **`KeyError` on a later lookup after an eviction.** You unlinked the coldest
  node but forgot `del self._index[coldest.asset_id]`, so the map still names a
  node that is out of the chain. It stays silent until `len(self._index)` drifts
  past capacity:

  ```text
  Traceback (most recent call last):
      del self._index[coldest.asset_id]
        ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  KeyError: 'brick'
  ```

  That particular trace is the *second* eviction of an id you already removed —
  the first one is what left the structures inconsistent.

- **`touch` on a miss creates the asset.** A version that falls through into the
  insert path has quietly turned `touch` into `pin`. `misses_are_inert` catches
  it. A miss is not a use, and it is certainly not a write.

- **Mixing up the two ends.** Pick a convention — here, cold at the head, hot at
  the tail — write it in the class docstring, and never re-derive it mid-method.
  Half of all linked-list bugs are one moment of "wait, which end is which".

- **`resident()` includes a sentinel.** Your walk starts at `self._cold` instead
  of `self._cold.hotter`, or stops at `self._hot.colder` instead of at
  `self._hot`. The empty board is the case that shows it: `resident()` must be
  `[]`, not `['']`.

- **Returning `-1` or raising on a miss.** The contract says `None` for all
  three read paths. `-1` forces every caller to remember a magic number, and an
  exception makes a perfectly ordinary cache miss into an error.

- **Claiming `O(1)` for `resident()`.** It builds a list of every resident id.
  Say `O(k)`, and say why that is fine.

## Under the hood

<details>
<summary>Under the hood — what OrderedDict does internally, and why a heap is the honest alternative</summary>

**`OrderedDict` is this exact composition, in C.** CPython's implementation
keeps the ordinary dict for lookup and threads a separate doubly-linked list of
`_ODictNode` structures through it to remember insertion order. `move_to_end`
unlinks a node and relinks it at the tail; `popitem(last=False)` takes the head.
Both are the same four-pointer-writes operation you just wrote by hand. Building
it yourself is not busy-work — it is the thing the library is doing, and knowing
that is the difference between using a tool and understanding one.

Note that a plain `dict` also preserves insertion order, since 3.7, but it gives
you no way to *change* an existing key's position without deleting and
reinserting it. Delete-and-reinsert is also `O(1)` amortised, so
`d[k] = d.pop(k)` is a legitimate third implementation — and it is worth knowing
that it works, and worth knowing that it churns the hash table in a way
`move_to_end` does not.

**The heap alternative, stated fairly.** Give every asset a use counter that
increments on each `pin` or `touch`, and keep a min-heap of `(counter, id)`. The
coldest asset is the heap's root. `pin` and `touch` push a new entry, `peek`
touches nothing, and eviction pops until it finds an entry whose counter matches
the asset's current one — the *lazy deletion* trick, because you cannot cheaply
remove a stale entry from the middle of a heap.

That design is `O(log slots)` per operation, uses more memory because stale
entries accumulate, and is genuinely much easier to get right: there is no
pointer surgery, so there is no class of bug where the structures disagree. At
the constraint of two million calls it would run comfortably. It is rejected
here only because the spec says `O(1)`, and saying all of that out loud —
including that the rejected design is *easier* — is the judgment signal this
challenge grades.

**Why `__slots__` on `_Slot`.** By default every Python object carries a `__dict__`
for its attributes, which is a whole hash table per object. `__slots__` replaces
it with a fixed array of four references. On a board of 100,000 assets that is a
substantial saving, and attribute access gets slightly faster too. It costs you
the ability to add attributes at runtime, which a node has no business doing.
This is the kind of detail that is pointless on a six-item example and real at
the top of the constraint.

**What LRU is actually approximating, and where it fails.** LRU guesses that
recently used things will be used again soon, which is true of most access
patterns and spectacularly false for one: a sequential scan over more items than
there are slots. Read 101 textures on a 100-slot board and every single read
misses, because each one evicts the asset you are about to need. Real systems
handle this with segmented caches, or with LFU (least *frequently* used), or by
marking scans so they do not pollute the board. Being able to name the failure
mode of the policy you just implemented is a good answer to "what would you
change in production".

**The one thing to carry away.** One structure for lookup, a second for order,
joined by storing *nodes* in the map rather than values. Once you have seen it
you will see it everywhere: a frequency-tiered eviction board, a board with
per-entry expiry, a versioned map that answers "what did this key hold at time
t". Every one of them is this trick with a different second structure.

</details>

## Acceptance checklist

- [ ] `python challenge-02-residency-board.py` prints seven `ok` lines, the
      session table, then `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] `pin`, `touch` and `peek` are each `O(1)` average — nothing scans, nothing
      walks.
- [ ] `peek` contains no call to `_link_hot`.
- [ ] All the pointer surgery lives in `_unlink` and `_link_hot`, and nowhere
      else.
- [ ] Eviction updates the list **and** the map.
- [ ] `pin` checks residency before it checks capacity.
- [ ] You wrote the five invariants down before you wrote code, and can say
      which method could break each one.
- [ ] You can say what `resident()` costs and why that is acceptable.
- [ ] You can name the heap alternative and say why it is easier and still
      rejected.
- [ ] Committed to Git with a message like `Add Week 2 challenge 2: residency board`.

## Stretch

- **Cross-check against a deliberately naive board.** The naive one is obviously
  correct and obviously too slow, which makes it the perfect oracle.

  ```python
  import random


  class NaiveBoard:
      """Correct, and O(slots) per pin. A list of ids, coldest first."""

      def __init__(self, slots: int) -> None:
          self._capacity = slots
          self._order: list[str] = []
          self._payloads: dict[str, str] = {}

      def pin(self, asset_id: str, payload: str) -> str | None:
          self._payloads[asset_id] = payload
          if asset_id in self._order:
              self._order.remove(asset_id)
              self._order.append(asset_id)
              return None
          evicted = None
          if len(self._order) == self._capacity:
              evicted = self._order.pop(0)
              del self._payloads[evicted]
          self._order.append(asset_id)
          return evicted

      def touch(self, asset_id: str) -> str | None:
          if asset_id not in self._order:
              return None
          self._order.remove(asset_id)
          self._order.append(asset_id)
          return self._payloads[asset_id]

      def peek(self, asset_id: str) -> str | None:
          return self._payloads.get(asset_id)

      def resident(self) -> list[str]:
          return list(self._order)


  rng = random.Random(20260226)
  names = ["brick", "moss", "rust", "bark", "sand", "ice"]
  fast, slow = ResidencyBoard(3), NaiveBoard(3)
  disagreements = 0
  for _ in range(4000):
      asset = rng.choice(names)
      method = rng.choice(["pin", "touch", "peek"])
      if method == "pin":
          got, want = fast.pin(asset, asset + "_2k"), slow.pin(asset, asset + "_2k")
      elif method == "touch":
          got, want = fast.touch(asset), slow.touch(asset)
      else:
          got, want = fast.peek(asset), slow.peek(asset)
      if got != want or fast.resident() != slow.resident():
          disagreements += 1
  print(f"{disagreements} disagreements over 4000 random calls")
  ```

  ```text
  0 disagreements over 4000 random calls
  ```

  Note that the naive board's `peek` also does not reorder — you have to write
  the oracle to the same contract, or it tests nothing. Writing an oracle is a
  small design exercise in its own right.

- **Add per-entry expiry, and watch the composition absorb it.**

  ```python
  class ExpiringBoard(ResidencyBoard):
      """A residency board where an asset also goes stale after so many ticks."""

      def __init__(self, slots: int, lifetime: int) -> None:
          super().__init__(slots)
          self._lifetime = lifetime
          self._clock = 0
          self._pinned_at: dict[str, int] = {}

      def pin(self, asset_id: str, payload: str) -> str | None:
          self._clock += 1
          self._pinned_at[asset_id] = self._clock
          return super().pin(asset_id, payload)

      def peek(self, asset_id: str) -> str | None:
          born = self._pinned_at.get(asset_id)
          if born is None or self._clock - born >= self._lifetime:
              return None
          return super().peek(asset_id)


  board = ExpiringBoard(3, lifetime=2)
  board.pin("brick", "brick_2k")
  print(board.peek("brick"))
  board.pin("moss", "moss_2k")
  board.pin("rust", "rust_2k")
  print(board.peek("brick"))
  print(board.resident())
  ```

  ```text
  brick_2k
  None
  ['brick', 'moss', 'rust']
  ```

  A third map, keyed by the same ids, holding a third fact. The linked list did
  not change at all, which is the sign the composition was factored correctly.
  Note that `brick` is expired but still *resident* — expiry and eviction are
  different policies, and conflating them is a real design mistake worth having
  made once here rather than in production.

- **Make the eviction policy pluggable and implement LFU.** Replace "least
  recently used" with "least frequently used": count uses per asset and evict
  the smallest count, breaking ties toward the coldest. Doing it in `O(1)`
  requires a second composition — a map from count to a linked list of assets
  with that count — which is the same trick you just learned, applied twice.
  That is genuinely a hard problem and a fair thing to attempt only after this
  page is comfortable.

**Practice elsewhere.** The same pattern appears as [LeetCode 146 · LRU Cache](https://leetcode.com/problems/lru-cache/) if you want a judge to run against. The contract there has a single read method, signals absence with `-1` rather than `None`, and makes neither the eviction nor the internal ordering observable — so it never forces the read-versus-use split, which is the half of this page that a remembered solution cannot supply.

---

That concludes Week 2's challenges. Take the [quiz](../quiz.md), do the
[homework](../homework/README.md), then ship the
[mini-project](../mini-project/README.md).
