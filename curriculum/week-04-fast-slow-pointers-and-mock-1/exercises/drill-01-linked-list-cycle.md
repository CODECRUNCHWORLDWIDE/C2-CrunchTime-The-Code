# Drill 1 — Linked List Cycle

> **Pattern:** Fast/slow pointers — Floyd's cycle detection
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (with full UMPIRE narration)
> **Why first:** the cleanest possible application of Floyd's. If you can UMPIRE this in 15 minutes including the O(1)-space defense, you have the pattern.

## Problem statement

Given the head of a singly-linked list, return `True` if the list contains a cycle, and `False` otherwise. A **cycle** exists if some node's `.next` pointer points back to an earlier node in the list.

You must solve it in **O(1) extra space**. The naive `seen = set()` approach is O(n) space and will be rejected.

**Examples:**

- `head` represents `3 → 2 → 0 → -4 → (back to 2)` → `True` (cycle at index 1)
- `head` represents `1 → 2 → (back to 1)` → `True` (cycle at index 0)
- `head` represents `1` → `False` (single node, no self-loop)
- `head = None` → `False` (empty list)
- `head` represents `1 → 2 → 3 → 4 → 5` → `False` (terminates normally)

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm singly-linked (each node has one `next`). Confirm the cycle could be anywhere — possibly the head pointing to itself, possibly a long tail before a small cycle. Confirm the empty-list case. Confirm "O(1) extra space" is part of the spec.
- [ ] **M:** Fast/slow pointers, Floyd's cycle detection. The 30-second memo: *"This is a fast/slow-pointers problem because we're walking a linked list and looking for a cycle. The pattern is Floyd's tortoise and hare. The auxiliary state is just two pointers — slow and fast. The reason this isn't 'hash set of visited nodes' is that the spec requires O(1) space, and Floyd's is the canonical O(1)-space cycle algorithm."*
- [ ] **P:** Initialize `slow = head`, `fast = head`. Loop while `fast` and `fast.next` both non-None. Inside: advance slow by 1, fast by 2. If `slow is fast`, return True. If the loop exits via guard, return False. Edge case: `head is None` — the loop never enters; return False. Edge case: single node `head.next is None` — same.
- [ ] **I:** Write the code, narrating each line.
- [ ] **R:** Trace on `3 → 2 → 0 → -4 → (back to 2)`. Slow=3, Fast=3. Iter 1: Slow=2, Fast=0. Iter 2: Slow=0, Fast=2 (wrapped). Iter 3: Slow=-4, Fast=-4 (met). Return True. ✓ Trace on `1 → 2 → 3`. Slow=1, Fast=1. Iter 1: Slow=2, Fast=3. Iter 2: Slow=3, Fast=None.next=crash? No — guard catches `fast is None` after iter 1's advance puts fast on node 3, then guard sees `fast.next is None`. Loop exits. Return False. ✓
- [ ] **E:** **Time O(n)** — if no cycle, fast hits None in at most n/2 outer iterations. If cycle of length C with prefix T, slow takes at most T+C iterations to meet fast. **Space O(1)** — two pointers, no auxiliary set or dict. Tradeoff: the `seen = set()` algorithm is O(n) time, O(n) space; Floyd's matches the time and beats the space. Best/avg/worst all O(n).

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `has_cycle`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-04/drill-01-linked-list-cycle.md` in your portfolio repo.
- Your Match section includes the 30-second pattern-recognition memo (four sentences naming Floyd's, the speed ratio, the auxiliary state, and the O(1)-space rejection of the hash-set approach).
- Your Evaluate section explicitly states the **O(1)-space defense sentence**.
- Recording **≥ 10 minutes.** If you finished in 4 minutes, you skipped Match or Evaluate. Re-do it.

## Function signature (for the runner)

```python
class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def has_cycle(head: ListNode | None) -> bool:
    """Return True iff the linked list contains a cycle. O(1) extra space."""
    ...
```

The runner provides a helper `build_list_with_cycle(values, pos)` that builds a list and creates a cycle at index `pos` (or no cycle if `pos == -1`).

## Common bugs you should catch in Review

- **Forgetting the `fast.next` guard.** `while fast is not None and fast.next is not None`. Both must be non-None *before* dereferencing `fast.next.next`. Missing the `fast.next` check crashes on lists that terminate normally.
- **Comparing before advancing.** If you check `slow is fast` at the *top* of the loop, the first iteration returns True trivially (both start at head). Advance first, compare after.
- **Using `==` instead of `is`.** Identity comparison is the right thing for nodes. `==` happens to work in the standard interview prompt because `ListNode` doesn't override `__eq__`, but `is` is more clearly correct.
- **Handling `head is None` separately as a special case.** Not needed — the loop guard catches it; the first iteration's `fast is not None` is False, loop exits, return False.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you deliver the 30-second pattern-recognition memo cleanly? (Should hit four sentences in under 30 seconds.)
2. Did you say the standard **O(1)-space defense** sentence? (That's the interview tell for Floyd's specifically.)
3. How long did Match take? (Should be <30 seconds on this problem — Floyd's is a textbook signal once "linked list + cycle" is read.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    └── c2-week-04/
        ├── drill-01-linked-list-cycle.md       # write-up
        └── drill_01_solution.py                 # your solution
```

When done, push and move on to [Drill 2](drill-02-cycle-start.md).
