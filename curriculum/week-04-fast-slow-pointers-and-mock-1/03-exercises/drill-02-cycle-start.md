# Drill 2 — Cycle Start (LeetCode 142, "Linked List Cycle II")

> **Pattern:** Fast/slow pointers — Floyd's + the `2k = k + nC` cycle-entrance lemma
> **Difficulty:** Medium
> **Target solve time:** 25 minutes (with full UMPIRE narration including the lemma)
> **Why second:** detection is mechanical; *finding the entrance* is the algorithmic insight. The interview tell is explaining the lemma cleanly out loud.

## Problem statement

Given the head of a singly-linked list, return the **node where the cycle begins** if a cycle exists, otherwise `None`. The "cycle begins" at the first node that is part of the cycle (i.e., the node `T` non-cycle nodes after the head, where `T = 0` if the head itself is part of the cycle).

You must solve it in **O(1) extra space**.

**Examples:**

- `head` represents `3 → 2 → 0 → -4 → (back to 2)` → node with value 2 (the entrance, at index 1)
- `head` represents `1 → 2 → (back to 1)` → node with value 1 (entrance at index 0; head is part of the cycle)
- `head` represents `1` → `None`
- `head = None` → `None`
- `head` represents `1 → 2 → 3 → 4 → 5` → `None` (no cycle)

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm "cycle entrance" is the first node *in* the cycle, not the last non-cycle node. Confirm the head-is-entrance case (`pos = 0`). Confirm "O(1) space."
- [ ] **M:** Fast/slow pointers, Floyd's detection + the `2k = k + nC` lemma. The 30-second memo: *"This is Floyd's cycle detection with the cycle-entrance lemma. Phase 1: walk slow by 1 and fast by 2 until they meet inside the cycle. Phase 2: by the `2k = k + nC` lemma, restarting a third pointer at head and walking it at speed 1 alongside slow will land both at the cycle entrance. Auxiliary state: three pointers. Why this works: when slow and fast first meet, slow has walked `k` steps, fast `2k`; their difference `k` is some whole number of cycle laps, which forces the entrance to be `T` steps from head and `T` steps from the meeting point."*
- [ ] **P:** Phase 1: `slow = fast = head`. Loop while `fast` and `fast.next`: advance slow by 1, fast by 2. If `slow is fast`, break. If loop ends via guard, return None. Phase 2: `finder = head`. While `finder is not slow`: advance both by 1. Return finder. Edge cases: empty list → None. Single non-self-pointing node → None.
- [ ] **I:** Write the code, narrating each line. Use `while/else` for Phase 1 — the `else` runs only if the loop exits via guard (no cycle).
- [ ] **R:** Trace on `3 → 2 → 0 → -4 → (back to 2)`. Phase 1: Slow=3, Fast=3. Iter1: Slow=2, Fast=0. Iter2: Slow=0, Fast=2. Iter3: Slow=-4, Fast=-4. Meet! Phase 2: Finder=3, Slow=-4. Not equal: Finder=2, Slow=2. Equal! Return node-2. ✓
- [ ] **E:** **Time O(n)** — Phase 1 is at most `T + C` ≤ n; Phase 2 is at most `T` ≤ n. **Space O(1)** — three pointers, no auxiliary set. Tradeoff: the `seen = set()` approach is O(n) time + O(n) space; this matches the time, beats the space. The lemma is the *insight*; the code is mechanical once the lemma is named.

## Acceptance criteria

- Code passes the [`timed_runner.py`](./timed_runner.py) test cases for `detect_cycle`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-04/drill-02-cycle-start.md`.
- Your Match section **explains the `2k = k + nC` lemma in three sentences.** This is non-negotiable; the lemma is the interview tell.
- Your Evaluate section states the O(1)-space defense.
- Recording **≥ 15 minutes.** The lemma explanation alone should take ~2 minutes.

## Function signature (for the runner)

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    """Return the cycle-entrance node, or None if no cycle. O(1) space."""
    ...
```

## Common bugs you should catch in Review

- **Returning the meeting node instead of the entrance.** The meeting point is *inside* the cycle but not (in general) at the entrance. You need Phase 2 to find the entrance. Don't shortcut.
- **Re-initializing `slow` in Phase 2.** Slow stays at the meeting point. Only `finder` starts at `head`. Both then walk at speed 1.
- **Forgetting the no-cycle case.** If Phase 1's loop ends via guard, return None *before* entering Phase 2. (The `while/else` form makes this clean.)
- **Off-by-one on `pos = 0`.** If the head itself is in the cycle, Phase 2's first comparison is `finder is slow` — both *should* be the head when slow has walked `nC` steps. The math works; don't special-case.

## The lemma — say it out loud

> "Let `T` = nodes before the cycle, `C` = cycle length. When slow and fast first meet, slow has walked `k` steps; fast has walked `2k`. Both are at the same node, so `k` is a whole number of cycle laps: `k = nC`. Slow has walked `T` steps to reach the entrance, then `k - T` steps into the cycle, so slow is `k - T` steps past the entrance — which equals `nC - T = -T (mod C)`, equivalently `T` steps *short* of the entrance going forward. So if I start a third pointer at `head` and walk both at speed 1, both will land at the entrance after exactly `T` more steps."

That paragraph, read aloud, is ~30 seconds. Memorize the cadence.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you explain the lemma cleanly out loud in under 60 seconds? (Aim: 30–45 seconds.)
2. Did you handle the no-cycle case before Phase 2? (Common bug: running Phase 2 on bad data.)
3. Did you trace at least one example end-to-end? (Without a trace, the lemma can sound right but the code can still be wrong.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
└── umpire-writeups/
    └── c2-week-04/
        ├── drill-02-cycle-start.md
        └── drill_02_solution.py
```

When done, push and move on to [Drill 3](./drill-03-middle-of-list.md).
