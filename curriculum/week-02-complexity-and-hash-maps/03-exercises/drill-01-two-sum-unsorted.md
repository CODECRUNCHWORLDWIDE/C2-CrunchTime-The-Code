# Drill 1 — Two Sum (Unsorted)

> **Pattern:** Hash map, complement lookup
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (full UMPIRE narration)
> **Why first:** the canonical hash-map problem. If you can't UMPIRE this with confidence, no other hash-map drill will land.

## Problem statement

Given an array of integers `nums` and an integer `target`, return the indices `[i, j]` of the **two numbers** such that `nums[i] + nums[j] == target`. You may assume each input has **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

**Examples:**

- `nums = [2, 7, 11, 15]`, `target = 9` → `[0, 1]`
- `nums = [3, 2, 4]`, `target = 6` → `[1, 2]`
- `nums = [3, 3]`, `target = 6` → `[0, 1]`

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm: input is **unsorted**, indices into the *original* array, exactly one solution exists, you can't use the same element twice. Walk one example: `[2,7,11,15]` target 9 → `[0,1]`.
- [ ] **M:** Hash map, complement lookup. Single pass; for each `x` ask "have I seen `target - x` before?" The hash map stores `value → index`. Alternative considered: sort then two-pointer — but sorting would scramble indices, so the hash map wins here.
- [ ] **P:** Initialize `seen = {}`. Loop `for i, x in enumerate(nums)`. Compute `complement = target - x`. If `complement in seen`, return `[seen[complement], i]`. Else `seen[x] = i`. After the loop, return `[]` (defensive; spec says one solution exists).
- [ ] **I:** Implement. Order matters: **check first, insert after** — otherwise `[3, 3]` with target 6 will see `3` and match itself.
- [ ] **R:** Trace on `[2,7,11,15]` target 9, and on the duplicate case `[3,3]` target 6.
- [ ] **E (the graded section this week):** Use the five-piece structure. Time **O(n)** (each iteration is O(1) average on the hash map). Space **O(n)** (the hash map). Worst-case is O(n) per op on collision but with Python's randomized hash we treat as O(1) average. Tradeoff: sort-then-two-pointer would be O(n log n)/O(1) — strictly worse on time, better on space, but scrambles indices. No improvement obvious; O(n) is the lower bound.

## Acceptance criteria

- Code passes `timed_runner.py` for `two_sum_unsorted`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-02/drill-01-two-sum-unsorted.md` in your portfolio repo.
- Your write-up's **Evaluate** section is at least three paragraphs and follows the five-piece structure.
- Recording is ≥10 minutes — short recordings mean you skipped Evaluate.

## Function signature

```python
def two_sum_unsorted(nums: list[int], target: int) -> list[int]:
    """
    Return indices [i, j] with i < j (or any order, as long as both are valid)
    such that nums[i] + nums[j] == target. Exactly one solution exists.
    """
    ...
```

## Common bugs to catch in Review

- **Insert before check.** Walking `[3, 3]` with target 6 — if you insert `3 → 0` before checking, then on the same iteration the complement check sees `3` in `seen` and returns `[0, 0]`. Wrong. The correct order: check first, *then* insert.
- **Using the same element twice.** `nums = [5]`, target 10 — naive check `if target - x == x` would falsely match. The "check before insert" discipline prevents this naturally; the only `x` in `seen` is a *previous* element.
- **Returning values instead of indices.** Read the spec.
- **O(n²) instead of O(n).** If you wrote a nested loop, you missed the pattern. Stop, redo Plan, write the hash-map version.

## Self-feedback

After you finish, listen back at 1.5×. Note three things:

1. Did you say the **standard Evaluate sentence** out loud? ("Each iteration is O(1) average on the hash map; n iterations → O(n) time.")
2. Did you mention the **tradeoff** with sort-then-two-pointer? You should, every time, on this problem.
3. How long did Match take? Should be <30 seconds — "this is the canonical hash-map complement lookup."

Add those notes to the end of your write-up.

## What to commit

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    └── c2-week-02/
        ├── drill-01-two-sum-unsorted.md
        └── drill_01_solution.py
```

Next: [Drill 2 — Contains Duplicate](./drill-02-contains-duplicate.md).
