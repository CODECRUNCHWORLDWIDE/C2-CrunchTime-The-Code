# Drill 3 — Middle of the Linked List (LeetCode 876)

> **Pattern:** Fast/slow pointers — speed-2 midpoint
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (with full UMPIRE narration)
> **Why third:** the most common fast/slow micro-pattern; reused as a sub-step in the challenge. Once you have this in muscle memory you can use it as a primitive in larger problems.

## Problem statement

Given the head of a singly-linked list, return the **middle node**. For lists of even length, return the **upper middle** (the second of the two middle nodes).

You must solve it in a **single pass** with **O(1) extra space**. Counting nodes first then walking to `n/2` is O(n) time but two passes; we want one pass.

**Examples:**

- `1 → 2 → 3 → 4 → 5` → node 3 (the single middle of an odd-length list)
- `1 → 2 → 3 → 4 → 5 → 6` → node 4 (the *upper* middle of an even-length list)
- `1` → node 1
- `1 → 2` → node 2 (upper middle)
- `head = None` → `None`

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm: upper middle for even length (the spec says it; some variants want lower middle — clarify with the interviewer in a real interview). Confirm "one pass" is part of the spec.
- [ ] **M:** Fast/slow pointers, speed-2 midpoint. The 30-second memo: *"This is a fast/slow-pointers problem because we want the middle of a singly-linked list in one pass. The pattern: walk slow by 1, fast by 2; when fast reaches None (or its next is None), slow is at the upper middle. Why this works: in `n` outer iterations, fast walks `2n` positions; the moment fast hits the end (position `n` for even length, `n` for odd), slow is at position `n/2` — the midpoint. Auxiliary state: two pointers. O(1) space."*
- [ ] **P:** `slow = head`, `fast = head`. Loop while `fast` and `fast.next`: advance slow by 1, fast by 2. Return slow. Edge case: `head is None` — return None (loop never enters, slow is None).
- [ ] **I:** Write the code, narrating each line. Note: this is the *upper-middle* convention; for lower middle, the guard is `fast.next.next`.
- [ ] **R:** Trace on `1 → 2 → 3 → 4 → 5` (odd). Slow=1, Fast=1. Iter1: Slow=2, Fast=3. Iter2: Slow=3, Fast=5. Guard fails (fast.next is None). Return Slow=3. ✓ Trace on `1 → 2 → 3 → 4 → 5 → 6` (even). Slow=1, Fast=1. Iter1: Slow=2, Fast=3. Iter2: Slow=3, Fast=5. Iter3: Slow=4, Fast=None (after fast.next.next). Guard fails. Return Slow=4. ✓ Upper middle, correct.
- [ ] **E:** **Time O(n)** — single pass; outer loop runs n/2 times. **Space O(1)** — two pointers. Tradeoff: two-pass naive (count then walk) is also O(n) time but visibly walks the list twice. Single-pass is the "show off" version interviewers grade for. No further improvement; O(n) is optimal — you must visit at least n/2 nodes to find the middle.

## Acceptance criteria

- Code passes the [`timed_runner.py`](./timed_runner.py) test cases for `middle_node`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-04/drill-03-middle-of-list.md`.
- Match memo names the speed-2 trick and the "single pass" advantage over two-pass naive.
- Your Review traces both an odd-length and an even-length example.
- Recording **≥ 8 minutes.**

## Function signature (for the runner)

```python
def middle_node(head: ListNode | None) -> ListNode | None:
    """Return the (upper) middle node of the linked list. O(1) space, single pass."""
    ...
```

## Common bugs you should catch in Review

- **Returning the lower middle when upper was requested.** Watch the guard. `while fast and fast.next` → upper middle. `while fast.next and fast.next.next` → lower middle (and you need a `None`-safe special case for empty / single-node).
- **Empty list crash.** `head is None` → fast is None, guard fails first iteration, slow is None, return None. The guard handles it; don't special-case unless the spec says otherwise.
- **Off-by-one in even-length traces.** Walking through `1 → 2 → 3 → 4` by hand: many candidates land on node 2 (lower middle) when the spec says node 3. Trace carefully.
- **Comparing values instead of nodes.** The return is the *node*, not the value. Return slow, not slow.val.

## Why this is reused

Drill 3 is the building block for the **Reorder Linked List challenge** later this week. The first of three sub-steps of that challenge is "find the middle" — exactly Drill 3's algorithm. If Drill 3 is automatic, the challenge becomes "two more sub-steps you already know."

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you ask out loud which middle convention the spec wants? (In a real interview, this is a U-step move.)
2. Did you trace *both* an odd-length and even-length example?
3. Did you say the "single pass" advantage over the naive two-pass solution?

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
└── umpire-writeups/
    └── c2-week-04/
        ├── drill-03-middle-of-list.md
        └── drill_03_solution.py
```

When done, push and move on to [Drill 4](./drill-04-happy-number.md).
