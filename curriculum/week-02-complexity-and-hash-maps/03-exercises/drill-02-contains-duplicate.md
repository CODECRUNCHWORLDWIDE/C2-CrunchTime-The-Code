# Drill 2 — Contains Duplicate

> **Pattern:** Hash set, membership
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (full UMPIRE narration)
> **Why second:** the simplest hash-*set* use. Shorter than Drill 1's hash-map version because we don't need a value payload, just presence. The tradeoff discussion is the meat.

## Problem statement

Given an integer array `nums`, return `True` if any value appears **at least twice** in the array, and `False` if every element is distinct.

**Examples:**

- `nums = [1, 2, 3, 1]` → `True`
- `nums = [1, 2, 3, 4]` → `False`
- `nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]` → `True`
- `nums = []` → `False` (vacuously distinct)
- `nums = [42]` → `False`

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: unsorted, integers (positive or negative), empty array returns False. "At least twice" means ≥2 occurrences anywhere in the array.
- [ ] **M:** Hash set, membership. Single pass; for each element check "have I seen this before?" — if yes, return True; else add to the set. Alternative: sort + scan for adjacent equals (O(n log n)/O(1)); brute-force nested loop (O(n²)/O(1)). Hash set wins on time when n is large.
- [ ] **P:** Initialize `seen = set()`. Loop `for x in nums`. If `x in seen`, return True. Else `seen.add(x)`. After loop, return False.
- [ ] **I:** Implement. Watch the order: check first, add after.
- [ ] **R:** Trace on `[1,2,3,1]` (matches at i=3). Trace on `[1,2,3,4]` (loop completes, returns False). Trace empty (loop body never runs, returns False).
- [ ] **E (graded):** Time **O(n)** average — n iterations, each O(1) on the set. Space **O(n)** — set holds at most n entries (less if there are duplicates). Best case **O(1)** time if the second element equals the first (early termination). Tradeoffs: sort + scan is O(n log n)/O(1); brute-force is O(n²)/O(1). Hash set is the best time when O(n) memory is acceptable.

## Acceptance criteria

- Code passes `timed_runner.py` for `contains_duplicate`.
- Write-up at `umpire-writeups/c2-week-02/drill-02-contains-duplicate.md`.
- Evaluate section follows the five-piece structure and **explicitly states the best-case early-termination**.
- Recording ≥8 minutes.

## Function signature

```python
def contains_duplicate(nums: list[int]) -> bool:
    """Return True if any value appears at least twice in nums."""
    ...
```

## Common bugs to catch in Review

- **Returning the duplicate value instead of `True`.** Read the spec.
- **`return len(nums) != len(set(nums))` as a one-liner.** Correct! But you must say out loud that this is *exactly* a hash-set construction under the hood — same O(n)/O(n) — and that the explicit loop is preferred in interviews because it allows **early termination**. The one-liner always allocates the full set. The loop returns True as soon as it sees a duplicate.
- **Confusing "duplicate" with "adjacent duplicate."** The naive answer (`if nums[i] == nums[i+1]`) only works on sorted input.

## Stretch

**Contains Duplicate II** (LeetCode 219). Return True if there exist *i ≠ j* such that `nums[i] == nums[j]` AND `abs(i - j) <= k`. Same hash-set pattern, but you store `value → most-recent-index` and check whether `i - seen[x] <= k`. UMPIRE this one too.

**Contains Duplicate III** (LeetCode 220). Same as II but values are within `t` of each other. Requires a bucket-sort-style approach. Out of scope this week; bookmark for after Week 9.

Next: [Drill 3 — Group Anagrams](./drill-03-group-anagrams.md).
