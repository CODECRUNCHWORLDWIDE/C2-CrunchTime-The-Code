# Exercise 1 — Portfolio Audit

> **Type:** Capstone build step (not a coding problem). **Difficulty:** Mechanical but exacting. **Target time:** 2.5 hours. **Why:** A recruiter opens a *random* write-up, not your best one. If the random one has a half-finished Examine, the recruiter distrusts all sixty. The audit makes every write-up clear the same bar, so any write-up a recruiter opens proves you can communicate.

This is the first drill of the capstone week. Your portfolio repo has been growing since Week 1 and holds roughly fifty write-ups. Before you add the final ten-plus to clear sixty, you audit what you have — because it is faster to fix a weak write-up than to write a new one, and because the dashboard count must be *true* (the count of write-ups that pass the bar, not the count of files).

---

## The six-point quality bar

Every write-up — every one — must clear all six:

| # | Bar | Pass looks like |
|---|-----|-----------------|
| 1 | 30-second Research-constraints memo at the top | A bordered block: pattern named, discriminating cue, complexity, rejected alternative |
| 2 | All five FRAME sections present | Frame · Research constraints · Assess options · Make the solution · Examine — none skipped or stubbed |
| 3 | Code runs and is tested | Passes the stated examples; type hints; PEP 8 (<https://peps.python.org/pep-0008/>); idiomatic |
| 4 | Complexity stated with a derivation | Not just "O(n)" — *why*: "one pass, one accumulator" |
| 5 | A variant or trade-off named | In Examine: a follow-up, or the alternative and why it loses |
| 6 | A trace on two inputs | In Examine: a normal case and an edge case, walked by hand |

---

## The task

1. **List every write-up.**

   ```bash
   find frame-writeups -name "*.md" ! -name "README.md" | sort
   ```

   Paste the list into a scratch file as a checklist.

2. **Triage oldest-first.** The Week 1–3 write-ups are the most likely to fail bars 1, 4, and 6 (the 30-second-memo and complexity-derivation disciplines came later). Audit those first.

3. **Score each write-up against the six bars.** A 30-second scan per write-up is enough — you are checking for *presence*, not re-reading. Mark pass/fail per bar in your checklist.

4. **Fix the failures in frequency order:**
   - Backfill missing **Research-constraints memos** (bar 1) and **complexity derivations** (bar 4) first — quick, and they cluster in early write-ups.
   - **Run any untested code** (bar 3). Fix anything that does not run or does not pass the examples.
   - Add missing **edge-case traces** (bar 6).

5. **Re-count and update the dashboard.** The README dashboard count is the number of write-ups that *pass*. Run the count after fixing:

   ```bash
   find frame-writeups -name "*.md" ! -name "README.md" | wc -l
   ```

---

## Worked example — auditing a weak Week-2 write-up

Suppose `frame-writeups/04-two-sum.md` (an early one) reads, in its entirety:

```markdown
# Two Sum

Use a hash map. Loop through, check if complement is in the map.

def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

Audit: **bar 1 fails** (no Research-constraints memo). **Bar 2 fails** (no Frame / Research constraints / Examine). **Bar 3 partial** (code is correct but has no type hints, no docstring, untested). **Bar 4 fails** (no complexity). **Bar 5 fails** (no variant). **Bar 6 fails** (no trace). This write-up fails five of six.

The fix — bringing it to the bar:

```markdown
# Two Sum (LC 1)

> **30-second pattern-recognition memo (hash map):**
> "Find two indices summing to a target" + "one pass desired" → hash map of
> value → index. As I scan, I check whether the complement (target - n) is
> already seen. Time O(n), space O(n). Why not the O(n^2) double loop: a hash
> map trades O(n) space for dropping the time from O(n^2) to O(n).

## Frame
Given an array `nums` and an integer `target`, return the indices of the two
numbers that add to `target`. Exactly one solution; cannot reuse an element.
Example: `nums=[2,7,11,15], target=9 → [0,1]` because `2 + 7 == 9`.

## Research constraints
One pass is wanted, so the O(n^2) double loop is out. That points at a hash
map (see memo). The brute force is the rejected alternative: O(n^2).

## Assess options
1. Empty dict `seen: value → index`.
2. For each `(i, n)`: if `target - n` in `seen`, return `[seen[target-n], i]`.
3. Otherwise record `seen[n] = i`.

## Make the solution
```python
from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    """Return indices of the two numbers adding to target. O(n) time, O(n) space."""
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []  # problem guarantees a solution; defensive return
```

## Examine
- `nums=[2,7,11,15], target=9`: i=0 n=2, complement 7 not seen, store {2:0};
  i=1 n=7, complement 2 in seen → return [0,1]. Correct.
- Edge `nums=[3,3], target=6`: i=0 store {3:0}; i=1 complement 3 in seen → [0,1].
  Correct (duplicates handled because we check before storing).

Time O(n): one pass. Space O(n): the dict holds up to n entries. Trade-off:
the O(n^2) double loop uses O(1) space but is too slow at scale. Variant: if
the array were sorted, the two-pointer approach gives O(n) time / O(1) space —
worth naming as the space-optimal alternative when sorted input is allowed.
```

Now it passes all six bars. That fix took five minutes and converted a write-up that would have lost a recruiter's trust into one that earns it.

---

## Acceptance criteria

- [ ] Every write-up under `frame-writeups/` has been scored against the six-point bar.
- [ ] Every failure has been fixed — no write-up in the repo fails any bar.
- [ ] All code snippets run and pass their stated examples.
- [ ] The README dashboard count reflects the true number of passing write-ups.
- [ ] An audit log (`frame-writeups/AUDIT.md`) records what you checked and what you fixed — the audit itself is portfolio evidence of rigor.

---

## What to commit

- The fixed write-ups (commit them individually with messages like `audit: backfill complexity derivation in 04-two-sum`).
- `frame-writeups/AUDIT.md` — the audit log.
- The updated README dashboard count.

---

Next: [Exercise 2 — System-Design Write-Up](./exercise-02-system-design-writeup.md) — the junior-level URL-shortener design artifact.
