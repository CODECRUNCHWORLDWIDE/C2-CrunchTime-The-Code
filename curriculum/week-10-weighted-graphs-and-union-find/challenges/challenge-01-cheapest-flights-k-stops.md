# Challenge 1 — Cheapest Flights Within K Stops (Deep Dive, LeetCode 787)

> **Difficulty:** Medium-Hard (with the deep-dive treatment). **Target solve time:** 75 minutes including FRAME write-up and the algorithm-choice defense.

This is the deep-dive version of Exercise 2. The work this week is to **implement both** the Bellman-Ford form and the modified-Dijkstra-with-state form, and to defend the trade between them in the Examine section. Most Phase-2 onsite problems on weighted graphs ask exactly this kind of trade — "which algorithm did you pick and why" is the senior signal.

---

## Problem spec

There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` indicates that there is a flight from city `from_i` to city `to_i` with cost `price_i`.

You are also given three integers `src`, `dst`, and `k`. Return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return `-1`.

**Constraints (LeetCode):**

- `1 <= n <= 100`.
- `0 <= len(flights) <= (n * (n - 1) / 2)`.
- `0 <= from_i, to_i < n`.
- `from_i != to_i`.
- `1 <= price_i <= 10^4`.
- There will not be any multiple flights between two cities.
- `0 <= src, dst, k < n`.
- `src != dst`.

---

## Why this is the canonical hop-constrained shortest-path problem

Three reasons.

1. **It is the cleanest illustration of the snapshot idiom.** Bellman-Ford with a hop count needs to freeze the per-pass starting state so that within a single pass, multiple just-updated values do not chain into longer paths than the hop limit allows. Forgetting the snapshot is the single most common LC 787 bug; the senior implementation makes the snapshot explicit and defends it in a comment.

2. **It is the cleanest illustration of Dijkstra-with-state.** Modified Dijkstra with the state `(node, hops_used)` solves the same problem, often faster on graphs where the target is reachable in few hops. The state augmentation is the discriminating implementation detail.

3. **The two implementations have different practical characteristics.** Bellman-Ford is `O(K * E)` deterministically; Dijkstra-with-state is `O(?)` with the question mark being "depends on how early the target is reached." For LC 787's constraints, both are fast; for variants with larger `K` and sparser graphs, one wins decisively over the other.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (Bellman-Ford / Dijkstra-with-state):**
> Single-source shortest path with a hop-count constraint. Two correct
> algorithms: (a) Bellman-Ford bounded by K + 1 outer passes, with a
> per-pass snapshot of dist before relaxing -- O(K * E) time, O(V) space;
> (b) modified Dijkstra with state (node, hops_used) in the heap --
> O(?) time, depends on how quickly the target is reached. The snapshot
> in (a) is non-negotiable: without it, a single pass can chain multiple
> just-updated values and exceed the hop budget. Why not vanilla Dijkstra:
> the heap settles a node at its overall-cheapest distance, ignoring the
> hop budget. Why not unconstrained Bellman-Ford: V - 1 passes overshoot
> the K + 1 bound.
```

Read aloud; should hit 25-30 seconds.

---

## The intended algorithms

### Algorithm A — Bellman-Ford with snapshot

```python
from __future__ import annotations

from typing import List


def find_cheapest_price_bellman(
    n: int, flights: List[List[int]], src: int, dst: int, k: int
) -> int:
    """Bellman-Ford bounded by K + 1 passes; the snapshot is the key idiom."""
    dist: List[float] = [float("inf")] * n
    dist[src] = 0.0

    for _ in range(k + 1):
        # Snapshot dist BEFORE relaxing. Without this, a single pass can chain
        # multiple just-updated values within itself, producing paths of more
        # than K + 1 edges.
        prev = dist[:]
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w

    return int(dist[dst]) if dist[dst] != float("inf") else -1
```

### Algorithm B — Dijkstra-with-state

```python
import heapq
from collections import defaultdict
from typing import Dict, List, Tuple


def find_cheapest_price_dijkstra(
    n: int, flights: List[List[int]], src: int, dst: int, k: int
) -> int:
    """Modified Dijkstra with (node, hops_used) state."""
    graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    # State: (cost, node, hops_used). Heap orders by cost ascending.
    heap: List[Tuple[int, int, int]] = [(0, src, 0)]
    # best[(node, hops)] = the cheapest known cost to reach `node` using
    # exactly `hops` intermediate stops. Lets us prune dominated states.
    best: Dict[Tuple[int, int], int] = {}

    while heap:
        cost, node, hops = heapq.heappop(heap)
        if node == dst:
            return cost
        if hops > k:
            continue
        if (node, hops) in best and best[(node, hops)] <= cost:
            continue
        best[(node, hops)] = cost
        for neighbor, weight in graph.get(node, []):
            heapq.heappush(heap, (cost + weight, neighbor, hops + 1))

    return -1
```

The state augmentation — `(node, hops_used)` — is the discriminator from vanilla Dijkstra. Without `hops_used` in the heap, the algorithm would settle `node` at its overall-cheapest distance, ignoring the hop budget.

---

## The three subtle bugs

**Bug 1 — Forgetting the snapshot in Bellman-Ford.** Without `prev = dist[:]`, the per-pass relaxation uses the live `dist`, which means a single pass can chain `0 -> 1 -> 2 -> 3` in one outer iteration. On example 1 with `K = 1`, this would (incorrectly) accept the 3-edge path `0 -> 1 -> 2 -> 3` and return `400` instead of `700`. The snapshot is the cleanest fix; the alternative — adding an outer pass-counter and tracking "hops used to reach each node" — is more complex.

**Bug 2 — Marking a node visited in Dijkstra-with-state.** Vanilla Dijkstra marks `node` as visited on the *first* pop (the "settle once" invariant). In Dijkstra-with-state, this is wrong: a later pop of `node` with a *different* `hops_used` value may be the actual cheapest route to `dst`. The fix is to mark `(node, hops)` as visited, not `node`. The `best` dict in Algorithm B above is the right form.

**Bug 3 — Off-by-one on K vs K + 1.** The constraint says "at most `K` intermediate stops," which means at most `K + 1` *edges*. A 0-stop flight is a single direct edge. Confusing stops with edges is the single most common reading error on LC 787; the senior implementation states the bound in a comment.

---

## FRAME write-up template

### Frame

Restate the problem in your own words. Walk LC 787 example 1 by hand for *both* algorithms (Bellman-Ford trace from Solution 2; Dijkstra-with-state trace below). Address the off-by-one between stops and edges.

Dijkstra-with-state trace on example 1 (`src = 0`, `dst = 3`, `k = 1`):

```
heap: [(0, 0, 0)]
pop (0, 0, 0); push (100, 1, 1)  [edge 0 -> 1]
heap: [(100, 1, 1)]
pop (100, 1, 1); hops = 1 == k, so push neighbors with hops + 1 = 2
  push (200, 2, 2)  [edge 1 -> 2]
  push (700, 3, 2)  [edge 1 -> 3]
heap: [(200, 2, 2), (700, 3, 2)]
pop (200, 2, 2); hops = 2 > k = 1, skip.
heap: [(700, 3, 2)]
pop (700, 3, 2); node == dst = 3, return 700.
```

Note that `(200, 2, 2)` is discarded because `hops = 2` exceeds the `K = 1` budget. The state guard is `if hops > k: continue` *after* the target check — popping the target with `hops > k` is fine (we already passed through `dst` with a valid hop count).

### Research constraints

Open with the 30-second memo. State both algorithms. Defend the choice — for LC 787, both are fast and both fit in the constraints; the *defense* of why you picked one over the other is the work.

### Assess options

Two numbered plans, one per algorithm. State the data structure first; the loop structure second; the termination condition third.

### Make the solution

Implement *one* of the two as your primary submission. Mention the other in Examine · cost.

### Examine · verify

Trace both algorithms on example 1 (above) and example 3 (`k = 0`, so only direct flights count). The `k = 0` case is the most discriminating edge case — it forces the algorithm to reject all multi-edge paths.

### Examine · cost

- **Bellman-Ford:** `O(K * E)` time, `O(V)` space. Always runs `K + 1` passes; cannot early-terminate without losing the hop guarantee.
- **Dijkstra-with-state:** Hard to bound tightly. Worst case is `O(V * K * log(V * K))` for the heap with `V * K` distinct states. Best case is `O(K log K)` if the target is the first vertex reached. For LC 787's constraints, runs faster than Bellman-Ford on most inputs.
- **Trade:** Bellman-Ford is safer to write under pressure (fewer subtle bugs); Dijkstra-with-state is faster on real inputs but has the state-marking trap (Bug 2 above). For an onsite, write Bellman-Ford; mention Dijkstra-with-state in Examine · cost.

---

## Stretch — Algorithm C — Modified BFS with state

A third correct algorithm exists: **BFS with `(node, hops_used)` state**, where the BFS queue is ordered by `(hops, cost)` instead of by cost alone. This is correct because once we know we have used `h` hops, we cannot use more, and within each `h` level we relax greedily. It is not faster than Dijkstra-with-state; mention only as the *third* alternative.

---

## Rubric

The 30-second memo plus the five FRAME sections, with Examine split into verify and cost; total possible 100; passing 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; both algorithms named; snapshot mentioned |
| Frame | 10 | Both examples walked; off-by-one between stops and edges addressed |
| Research constraints | 20 | Both algorithms named; trade defended in 2-3 sentences |
| Assess options | 10 | Two numbered plans; one per algorithm; data structures stated |
| Make the solution | 25 | Primary implementation passes all LC 787 cases; type hints; PEP 8 |
| Examine · verify | 10 | One positive trace + the `k = 0` edge case; both walked |
| Examine · cost | 15 | Both complexity bounds derived; the snapshot vs state-marking bugs named |

---

## Acceptance

The challenge is complete when:

- The implementation passes all LC 787 sample cases (including the `k = 0` edge case).
- A FRAME write-up is committed under `frame-writeups/c2-week-10/challenge-01-cheapest-flights/`.
- The Research constraints section names *both* algorithms and defends the choice.
- A recording of at least 10 minutes is uploaded.

The senior signal is the **algorithm-choice defense** — most candidates implement one and stop. Mentioning both, walking the trade, and recommending one for an interview setting is the senior move.
