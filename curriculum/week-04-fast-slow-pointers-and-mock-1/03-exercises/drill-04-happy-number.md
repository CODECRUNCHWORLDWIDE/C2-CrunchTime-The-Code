# Drill 4 — Happy Number (LeetCode 202)

> **Pattern:** Fast/slow pointers on a **functional graph** (no linked list in sight)
> **Difficulty:** Easy / Medium
> **Target solve time:** 20 minutes (with full UMPIRE narration including the functional-graph insight)
> **Why fourth:** the pattern recognition is non-obvious — there's no linked list. The drill is to *see* the linked-list-ness in a problem that doesn't mention it. This is the meta-skill of pattern matching.

## Problem statement

A number is **happy** if you can reach 1 by repeatedly replacing it with the sum of squares of its digits. If you ever enter a cycle of numbers that doesn't include 1, it's **not** happy.

Given an integer `n` (≥ 1), return `True` if `n` is happy and `False` otherwise.

**Examples:**

- `n = 19` → `True`. Chain: 19 → 1²+9² = 82 → 8²+2² = 68 → 6²+8² = 100 → 1²+0²+0² = 1. Happy.
- `n = 2` → `False`. Chain: 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle, no 1). Not happy.
- `n = 1` → `True`. Trivially.
- `n = 7` → `True`.

## The pattern-recognition insight

This problem doesn't *say* "linked list." But the iteration `n → digit_square_sum(n)` defines a **functional graph**: each integer has exactly one outgoing edge. Walking the chain *is* walking a linked list — the "nodes" are integers, the "next pointer" is the function, and the "cycle" is a repeated value.

Floyd's applies. The O(n)-space alternative (`seen = set()`) works but is rejectable in interviews that ask for constant space.

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm: happy = reaches 1; not happy = enters a non-1 cycle. Confirm `n ≥ 1`. Walk `n=19`: 19 → 82 → 68 → 100 → 1. Walk `n=2`: 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → 16 ... (cycle).
- [ ] **M:** Fast/slow pointers on a functional graph. The 30-second memo: *"This is a fast/slow-pointers problem because the iteration `n → digit_square_sum(n)` defines a functional graph — each integer has exactly one successor. Walking the chain is walking a linked list of integers. Floyd's detects whether we enter a cycle: if the cycle's repeated value is 1, the number is happy; otherwise not. Auxiliary state: two integers. O(1) space — the canonical reason to prefer Floyd's over `seen = set()` here."*
- [ ] **P:** Helper: `digit_square_sum(n)` — sum of squared digits. Main: `slow = fast = n`. Loop forever: `slow = step(slow)`, `fast = step(step(fast))`. If `fast == 1`, return True. If `slow == fast`, return False (entered a non-1 cycle). The loop terminates because the chain *must* either reach 1 or enter a cycle (the chain values are bounded — proof below).
- [ ] **I:** Write `digit_square_sum`, then the main fast/slow loop.
- [ ] **R:** Trace on `n=19`. Slow=19, Fast=19. Iter1: slow=82, fast=step(step(19))=step(82)=68. Iter2: slow=68, fast=step(step(68))=step(100)=1. Fast == 1 → return True. ✓ Trace on `n=2`. Slow=2, Fast=2. Iter1: slow=4, fast=step(step(2))=step(4)=16. Iter2: slow=16, fast=step(step(16))=step(37)=58. Iter3: slow=37, fast=step(step(58))=step(89)=145. Iter4: slow=58, fast=step(step(145))=step(42)=20. Iter5: slow=89, fast=step(step(20))=step(4)=16. Continue until slow == fast inside the cycle. Return False. ✓
- [ ] **E:** **Time O(log n)** per `digit_square_sum` step (number of digits), times O(?) iterations. The chains are short in practice — for `n ≤ 2³¹`, all chains either reach 1 quickly or enter the 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 cycle within ~10 steps. **Space O(1)** — two integers. Tradeoff: `seen = set()` of integers along the chain is the obvious alternative; O(1) extra space is what we trade for. Why O(1) is possible: same Floyd's reason — the iteration is a functional graph; cycle detection doesn't need history.

## Acceptance criteria

- Code passes the [`timed_runner.py`](./timed_runner.py) test cases for `is_happy`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-04/drill-04-happy-number.md`.
- Match section **names the functional-graph insight explicitly.** This is the recognition tell — most candidates code it with `set()` because they don't see the linked-list structure.
- Your write-up walks the cycle for `n=2` explicitly (at least the first 4–5 steps).
- Recording **≥ 12 minutes.**

## Function signatures (for the runner)

```python
def digit_square_sum(n: int) -> int:
    """Return the sum of squares of the digits of n. n must be >= 0."""
    ...

def is_happy(n: int) -> bool:
    """Return True iff n is a 'happy number' under digit-square-sum iteration. O(1) extra space."""
    ...
```

The runner tests both `digit_square_sum` and `is_happy`.

## Why this is the pattern-recognition drill

Drills 1–3 are obvious applications: "linked list" appears in the prompt. Drill 4 doesn't mention linked lists. The drill is to *see* one anyway. In Mock #1, you may get a problem where the linked-list-ness is similarly hidden (e.g., LeetCode 287 — Find the Duplicate Number, which is in homework). If you've internalized Drill 4, you'll spot the pattern.

Two more functional-graph problems you can apply Floyd's to once you have the pattern:

- **Find the Duplicate Number** (LeetCode 287) — array `nums[1..n]` with exactly one duplicate. Treat `i → nums[i]` as a functional graph. Floyd's finds the duplicate in O(n) time, O(1) space. (Homework Problem 1.)
- **Cycle in iterated `f(x) = x² + c mod p`** — Pollard's rho algorithm for integer factorization. Out of scope but you've now seen the pattern that underpins it.

## Common bugs you should catch in Review

- **Including `n` itself in the cycle-equality check before any step.** If `n=1`, the first thing `fast` does is step to `digit_square_sum(1) = 1` and stay there. The check `fast == 1` after the step correctly returns True. Don't compare `slow == fast` before stepping (they trivially equal `n` at start).
- **Forgetting that fast steps *twice* per iteration.** `fast = step(step(fast))` — two applications of the function per outer step.
- **Returning False before exiting the loop body.** The order in the loop body matters: step both, *then* check `fast == 1` (happy path), *then* check `slow == fast` (non-happy cycle). Reversing this misses the case where fast reaches 1 in the same iteration slow catches up.
- **Stack overflow from recursion.** Don't recurse `digit_square_sum`. Iterate.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you name the "functional graph" insight explicitly in Match? (This is the recognition tell.)
2. Did you justify the O(1) space over the `seen = set()` alternative?
3. Did you trace the cycle for `n=2` long enough to see the loop close? (At least 4 steps.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
└── umpire-writeups/
    └── c2-week-04/
        ├── drill-04-happy-number.md
        └── drill_04_solution.py
```

When done, push and move on to the [Reorder Linked List challenge](../04-challenges/challenge-01-reorder-linked-list.md).
