# Challenge 2 — LRU Cache

> **Pattern:** Hash map + doubly-linked list (or Python's `OrderedDict`)
> **Difficulty:** Medium / Hard (depending on which version you implement)
> **Target solve time:** 120 minutes
> **Why hard:** the *design* dimension. You're not just writing a function; you're building a class with constant-time invariants on *every* operation. This problem appears in roughly half of senior interview loops at well-known companies.

## Problem statement

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**. Implement the `LRUCache` class:

- `LRUCache(capacity: int)` — initialize with a positive `capacity`.
- `get(key: int) -> int` — return the value of `key` if it exists in the cache; otherwise return `-1`. Accessing a key counts as a *use* (moves it to most-recently-used).
- `put(key: int, value: int) -> None` — update or insert. If the cache is at capacity, **evict the least-recently-used key** before inserting.

**Both `get` and `put` must run in O(1) average time.** That's the entire challenge.

**Example:**

```
cache = LRUCache(2)
cache.put(1, 1)      # cache = {1=1}
cache.put(2, 2)      # cache = {1=1, 2=2}
cache.get(1)         # returns 1, cache = {2=2, 1=1}    (1 is now most-recent)
cache.put(3, 3)      # evicts key 2; cache = {1=1, 3=3}
cache.get(2)         # returns -1 (not found)
cache.put(4, 4)      # evicts key 1; cache = {3=3, 4=4}
cache.get(1)         # returns -1
cache.get(3)         # returns 3
cache.get(4)         # returns 4
```

## Acceptance criteria

- [ ] Both `get` and `put` are O(1) average. A hash-map-only implementation that scans for the LRU key on eviction is O(n) per put and **does not pass**.
- [ ] Your UMPIRE write-up **describes the invariants of the doubly-linked list** explicitly — that's the design dimension.
- [ ] Tests pass on the cases at the bottom.
- [ ] Recording ≥30 minutes. This is the longest drill of the week.

## Two valid implementations

### Implementation A — `collections.OrderedDict` (the Pythonic answer)

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

`OrderedDict` maintains insertion order *and* supports O(1) `move_to_end` and `popitem(last=False)`. It is, internally, exactly a hash map + doubly-linked list — so you can use this and *claim* the complexity correctly.

**In an interview, mention this version first, but be prepared to write the explicit hash-map + doubly-linked-list version when the interviewer asks "now without `OrderedDict`."** That ask is universal.

### Implementation B — hash map + doubly-linked list (the from-scratch answer)

```python
class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: "_Node | None" = None
        self.next: "_Node | None" = None


class LRUCache:
    """Hash map + doubly-linked list. head = LRU sentinel; tail = MRU sentinel."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: dict[int, _Node] = {}
        self.head = _Node()          # LRU side
        self.tail = _Node()          # MRU side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node: _Node) -> None:
        # MRU side: insert just before self.tail
        before = self.tail.prev
        before.next = node
        node.prev = before
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_to_tail(node)
            return
        if len(self.map) == self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.map[lru.key]
        new_node = _Node(key, value)
        self.map[key] = new_node
        self._add_to_tail(new_node)
```

This version uses **sentinel head/tail nodes** to avoid null-checks on every `prev`/`next` operation. The hash map stores `key → node` for O(1) location; the linked list maintains order for O(1) move-to-end and pop-from-head.

**Invariants you must defend out loud:**

1. `self.map` always contains the same set of keys as the linked list (excluding sentinels).
2. `self.head.next` is the LRU entry; `self.tail.prev` is the MRU entry.
3. Every `get` and `put` of an existing key moves the node to the MRU side.
4. Eviction always pops `self.head.next`.

## UMPIRE outline

- **U:** Restate. Confirm capacity > 0; clarify whether `put` with capacity 0 is a thing (LeetCode says no); confirm both ops must be O(1) average.
- **M:** Hash map for O(1) key→node location; doubly-linked list for O(1) reorder.
- **P:**
  1. Sentinels avoid null-checks.
  2. `get`: lookup in map; if missing, return -1; else remove from list and re-add at tail; return value.
  3. `put`: if key in map, update value, move to tail; else if at capacity, evict head.next; insert new node at tail and into map.
- **I:** Implement the helper methods `_remove(node)` and `_add_to_tail(node)`. Then `get` and `put` reduce to a few helper calls.
- **R:** Trace the example above step by step. Show the linked list (left=LRU, right=MRU) at each step.
- **E:** **O(1) average per operation.** Each `get` / `put` does O(1) hash-map operations + O(1) linked-list pointer surgery. **O(capacity)** space for the cache plus map.

## Test cases

```python
import pytest

def test_lru_cache_basic():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)
    assert cache.get(2) == -1
    cache.put(4, 4)
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

def test_lru_cache_update_existing():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)        # update, also marks 1 as most-recent
    cache.put(3, 3)         # should evict 2, not 1
    assert cache.get(1) == 10
    assert cache.get(2) == -1
    assert cache.get(3) == 3

def test_lru_cache_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)         # evicts 1
    assert cache.get(1) == -1
    assert cache.get(2) == 2
```

## Common bugs

- **Forgetting to evict on `put` that updates an existing key.** Updating doesn't change cache size; only inserting a *new* key triggers eviction.
- **Wrong direction.** Most popular convention: head = LRU, tail = MRU. Pick a convention and stick with it; mixed conventions cause off-by-one bugs.
- **Forgetting to remove the key from the map on eviction.** Then the map and list disagree.
- **Allocating nodes inside the helper methods.** Don't; allocate once in `put`.
- **Not using sentinels.** Possible but error-prone — every operation needs to special-case empty / single-element lists.

## Why this matters

LRU Cache is the canonical *design* interview problem and the moment many candidates discover they don't actually understand how their language's standard library works. Implementing it from scratch with sentinels demonstrates:

1. **Comfort with linked-list pointer manipulation** — a basic skill that has nothing to do with cleverness.
2. **Comfort designing a class with invariants** — the design dimension of the rubric.
3. **The "two data structures composed" pattern** — hash map for lookup, linked list for order.

You will see variants of this pattern in subsequent weeks: LFU cache, time-keyed cache, snapshot map. The composition trick — hash map for one access pattern, *another structure* for the other access pattern — is the design move.

## Stretch

- **LFU Cache** (LeetCode 460) — least-*frequently*-used eviction. Harder; uses a hash map of frequency → linked list. After Week 9 (heaps).
- **First Unique Number** (LeetCode 1429) — same composition trick, different external interface.
- **Snapshot Array** (LeetCode 1146) — binary search on a list of (snap_id, value) pairs per index.

---

This concludes Week 2's challenges. Take the [quiz](../quiz.md), do the [homework](../homework.md), then ship the [mini-project](../mini-project/README.md) — re-doing Week 1's five Evaluate sections to the new standard.
