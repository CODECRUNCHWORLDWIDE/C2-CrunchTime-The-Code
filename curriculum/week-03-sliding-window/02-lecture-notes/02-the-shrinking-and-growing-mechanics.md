# Lecture 2 — The Shrinking and Growing Mechanics

> **Duration:** ~2 hours.
> **Outcome:** You can write the variable-size sliding-window loop without notes, decide *when to expand* and *when to shrink* from the prompt alone, and explain the difference between the "longest" shape and the "shortest" shape out loud.

Lecture 1 introduced the pattern and its two sub-shapes. This lecture goes deep on the variable-size case — because that's where 80% of the bugs live. The mechanics of *when to expand* and *when to shrink* are not interchangeable across problems; the shape flips depending on whether you want "longest" or "shortest." Picking the wrong shape produces code that runs but is silently incorrect — the worst kind of interview bug.

By the end of this lecture you should be able to look at a variable-size sliding-window problem and, before writing any code, say one of two things out loud: "expand `right` until invariant breaks, then shrink `left` to restore," or "expand `right` until property holds, then shrink `left` while property still holds, recording the answer inside the shrink."

---

## 1. Two indices that don't converge — the geometry

Visualize the indices on a number line:

```
0 ──────────────────────────────── n-1
^                                  ^
left                              right (eventually)

left ───→  ───→  ───→
              right ───→  ───→  ───→
```

Both start at `0`. `right` moves first; `left` follows. They never cross. They both move strictly forward. The window is the half-open or inclusive interval between them, depending on convention. In this course we use **inclusive on both ends**: `s[left..right]` is the window when `left <= right`, and an empty window when `left > right` (which we avoid in steady state).

Compare with two-pointer converging:

```
0 ──────────────────────────────── n-1
^                                  ^
left ───→                  ←─── right
```

Two-pointer converging has them moving *toward* each other; the algorithm ends when they meet. Sliding window has them moving *together*, in the same direction; the algorithm ends when `right` reaches `n-1`. Same number of pointers, opposite geometry.

This is the source of the most common conceptual mistake. *Both* patterns use "two pointers" — but the *direction of motion* is the distinguishing feature.

---

## 2. When to expand `right`

In every variable-size sliding window, `right` advances **exactly once per outer iteration**. The body of the outer `for right in range(n)` loop:

1. Read `nums[right]` or `s[right]`.
2. Update the auxiliary state to include the new element (`update_add`).
3. Decide whether to shrink, then potentially update the answer.

`right` is not conditional. It doesn't pause. It doesn't back up. It is a steady drumbeat from `0` to `n - 1`. That regularity is what gives sliding window its `O(n)` guarantee — the outer loop's iteration count is fixed.

The only thing that varies is what happens inside.

---

## 3. When to shrink `left`

`left` is where the mechanics differ. Three loop shapes cover the vast majority of variable-size sliding-window problems.

### Shape A: shrink while the invariant is *broken* (the "longest" shape)

```python
for right in range(n):
    update_add(state, nums[right])
    while invariant_broken(state):
        update_remove(state, nums[left])
        left += 1
    # Invariant holds. The window is the largest valid one ending at right.
    best = max(best, right - left + 1)
```

The invariant is something like:

- "At most K distinct values."
- "All characters are unique."
- "Sum ≤ target."

You expand `right`, possibly breaking the invariant. You shrink `left` until the invariant holds again. *Then* you record the answer — the answer is the *current window length*, which by construction is the longest valid window ending at this `right`.

Canonical problems:

- **Longest substring without repeating characters** (Drill 2)
- **Longest substring with at most K distinct characters** (the homework's stretch)
- **Fruit into baskets** (Drill 5 — at most 2 distinct)

### Shape B: shrink while the property *still holds* (the "shortest" shape)

```python
for right in range(n):
    update_add(state, nums[right])
    while property_holds(state):
        # Record the answer *inside* the shrink loop.
        best = min(best, right - left + 1)
        update_remove(state, nums[left])
        left += 1
```

The property is something like:

- "Sum ≥ target."
- "Window contains all characters of `t`."

You expand `right` until the property holds. Then you shrink `left` *while the property still holds*, recording the answer at each step (because shrinking might produce a smaller valid window). When the property breaks, you stop shrinking and let `right` resume.

Canonical problems:

- **Minimum size subarray sum** (Drill 4)
- **Minimum window substring** (Challenge)
- **Shortest subarray with at least K occurrences of X**

The sign flip — shrink *while broken* vs. *while holding* — is the discriminator between longest and shortest. Get this wrong and the algorithm silently produces the right code for the wrong problem.

### Shape C: count of windows satisfying a property

For "**how many subarrays have property P**," neither shape A nor shape B directly applies. The trick: count, for each `right`, **how many valid windows end at that `right`**, then sum.

```python
for right in range(n):
    update_add(state, nums[right])
    while invariant_broken(state):
        update_remove(state, nums[left])
        left += 1
    # Number of valid windows ending at right is right - left + 1
    answer += right - left + 1
```

This works because, once the invariant holds at `right`, every window `[i..right]` for `i in [left..right]` is also valid (by monotonicity of the invariant). So we count `right - left + 1` valid windows at this step.

Canonical problems:

- **Count subarrays with at most K distinct integers**
- **Count subarrays with product less than K** (positive numbers only)

For *exactly K*, use the trick from Lecture 1: **exactly K = atMostK − atMost(K − 1)**.

---

## 4. The four-piece anatomy of a sliding-window loop body

Every variable-size sliding window has the same four pieces inside its outer loop. The order matters; mixing it up produces bugs.

```python
for right in range(n):
    # 1. ADD: incorporate nums[right] into the window state.
    update_add(state, nums[right])

    # 2. SHRINK: while the loop condition holds, remove nums[left] and advance.
    while shrink_condition(state):
        update_remove(state, nums[left])
        left += 1

    # 3. RECORD: update the answer based on the current window.
    answer = combine(answer, current_window_value(left, right, state))
```

The interview-quality version states each step out loud during Plan. "Add `nums[right]` to the window. Then shrink while the invariant is broken. Then record the window length."

When the answer is recorded **inside** the shrink loop (shape B, "shortest"), the four pieces re-order:

```python
for right in range(n):
    update_add(state, nums[right])
    while property_holds(state):
        # Record FIRST — the window is currently valid.
        answer = min(answer, right - left + 1)
        update_remove(state, nums[left])
        left += 1
```

The reorder is subtle. In shape A, the answer is recorded *once per outer iteration* (after the shrink). In shape B, the answer is recorded *every time `left` advances* (inside the shrink). Both are `O(n)` amortized — but the structure is different.

---

## 5. Worked example A: longest substring with at most K distinct characters

A classic. Pre-Drill 5 warm-up.

**Problem.** Given a string `s` and an integer `k`, return the length of the longest substring that contains at most `k` distinct characters.

**UMPIRE compressed:**

- **U:** Restate. Confirm `k ≥ 0`, return 0 if `s` empty or `k == 0`. Walk an example: `s = "eceba"`, `k = 2` → `3` (`"ece"`).
- **M:** Variable-size sliding window, shape A (longest). Auxiliary state: a frequency table; the invariant is `len(table) ≤ k`.
- **P:** Outer `for right`. Add `s[right]` to the table. While `len(table) > k`, decrement count of `s[left]`, delete the key if its count hits 0, advance `left`. Record `best = max(best, right - left + 1)`.
- **I:**

```python
def longest_at_most_k_distinct(s: str, k: int) -> int:
    if k == 0 or not s:
        return 0
    counts = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

- **R:** Trace `s = "eceba"`, `k = 2`:
  - r=0 ('e'): counts={e:1}, |counts|=1 ≤ 2, best=1.
  - r=1 ('c'): counts={e:1, c:1}, |counts|=2 ≤ 2, best=2.
  - r=2 ('e'): counts={e:2, c:1}, best=3.
  - r=3 ('b'): counts={e:2, c:1, b:1}, |counts|=3 > 2; shrink. left=0, e:2→1. left=1, c:1→0, del 'c'. counts={e:1, b:1}. left=2. best=3.
  - r=4 ('a'): counts={e:1, b:1, a:1}, |counts|=3 > 2; shrink. left=2, e:1→0, del 'e'. counts={b:1, a:1}. left=3. best=3.
  - Return 3. ✓
- **E:** **O(n) time** — amortized, each index moves at most n times. **O(k) space** — the counts dict holds at most k+1 entries (transiently, before shrink restores the invariant). Tradeoff: brute force "for each pair (l, r), build a set of chars in s[l..r] and check size" is O(n³). Sliding window collapses it. No improvement obvious.

This is the template for an entire family of problems. Internalize the shape; you'll re-use it on Drill 5 (Fruit Into Baskets is exactly this template with `k=2`) and on the homework's "exactly K distinct" stretch.

---

## 6. Worked example B: minimum size subarray sum (shape B)

**Problem.** Given an array of positive integers `nums` and a target integer `target`, return the **minimal length** of a contiguous subarray whose sum is `>= target`. If no such subarray exists, return 0.

**Why "positive integers" matters:** with negatives, the running sum is not monotonic in `right` (it can dip and recover). The sliding-window invariant — "shrinking from the left always *decreases* the sum" — relies on every element being non-negative. With negatives, you need prefix-sum + hash map (Week 2's Challenge 1 shape), not sliding window.

**UMPIRE compressed:**

- **U:** Positive integers only. Return *minimum length*. If no subarray reaches the target, return 0. Walk: `nums = [2,3,1,2,4,3]`, `target = 7` → `2` (`[4,3]`).
- **M:** Variable-size sliding window, shape B (shortest). Auxiliary state: a running sum; the property is `running >= target`.
- **P:** Outer `for right`. Add `nums[right]` to running. While `running >= target`, record `best = min(best, right - left + 1)`, subtract `nums[left]` from running, advance `left`. After the outer loop, return `0` if `best` is still infinity, else `best`.
- **I:**

```python
def min_size_subarray_sum(target: int, nums: list[int]) -> int:
    left = 0
    running = 0
    best = float("inf")
    for right, x in enumerate(nums):
        running += x
        while running >= target:
            best = min(best, right - left + 1)
            running -= nums[left]
            left += 1
    return 0 if best == float("inf") else best
```

- **R:** Trace `nums = [2,3,1,2,4,3]`, `target = 7`:
  - r=0 (2): running=2, no shrink.
  - r=1 (3): running=5, no shrink.
  - r=2 (1): running=6, no shrink.
  - r=3 (2): running=8 ≥ 7. Shrink: best=4 (window length 4: [2,3,1,2]); running-=2, running=6, left=1. running=6 < 7, exit shrink.
  - r=4 (4): running=10 ≥ 7. Shrink: best=4→min(4,4)=4; running-=3, running=7, left=2. Still 7 ≥ 7; best=min(4,3)=3; running-=1, running=6, left=3. Exit shrink.
  - r=5 (3): running=9 ≥ 7. Shrink: best=min(3,3)=3; running-=2, running=7, left=4. Still 7 ≥ 7; best=min(3,2)=2; running-=4, running=3, left=5. Exit shrink.
  - Return 2. ✓
- **E:** **O(n) time** (amortized; both indices move at most n times). **O(1) space** (one running sum, two pointers). Tradeoffs: brute force is O(n²); prefix-sum + binary search is O(n log n)/O(n); sliding window with the positivity guarantee is O(n)/O(1) — strictly best.

This is the template you'll use on Drill 4 directly, and again on the Minimum Window Substring challenge with a richer invariant.

---

## 7. The frequency-invariant variant: matching a target Counter

The hardest sliding-window family uses an invariant like "**the window contains all characters of `t` with at least the required counts**." This is the shape of Drill 3 (permutation in string) and Challenge 1 (minimum window substring).

The trick: don't compare full Counters on every iteration — that's `O(alphabet)` per step. Instead, maintain a single integer `need` (or `formed`) that tracks **how many required characters are currently satisfied**.

```python
from collections import Counter

def min_window_substring(s: str, t: str) -> str:
    if not s or not t:
        return ""
    need = Counter(t)
    required = len(need)         # number of distinct chars needed
    formed = 0                   # number of distinct chars currently satisfied
    window_counts = {}
    left = 0
    best = (float("inf"), 0, 0)  # (length, left, right)
    for right, ch in enumerate(s):
        window_counts[ch] = window_counts.get(ch, 0) + 1
        if ch in need and window_counts[ch] == need[ch]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lch = s[left]
            window_counts[lch] -= 1
            if lch in need and window_counts[lch] < need[lch]:
                formed -= 1
            left += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]
```

The invariant: `formed` equals `required` exactly when every required character is in the window with at least the required count. Each character's contribution to `formed` flips *at most twice* across the whole algorithm (once when count hits target, once when it dips below). So the total work is `O(n)` amortized, with `O(|alphabet| + |t|)` space.

This is the shape worked end-to-end in the Week 3 Challenge.

---

## 8. The bug census — what goes wrong in shrink loops

Across hundreds of student solutions, these are the bugs that appear most often. Memorize them; they're the ones to scan for in Review.

- **Forgetting to update the answer in shape B.** Shape A records the answer *after* the shrink loop. Shape B records *inside* the shrink loop. Mixing them up means you either miss valid windows or count invalid ones.
- **Missing the inner-loop guard.** `while invariant_broken(state):` without an upper bound on `left` will run past the end of the array if the invariant can never be restored. Pair the condition with `and left <= right` for safety on weird inputs.
- **Not removing on `left` advance.** The shrink loop's body must call `update_remove(state, nums[left])` *before* `left += 1`. Otherwise the state still reflects the now-discarded element.
- **Order of operations in shape B.** Record-then-remove, not remove-then-record. If you remove first, the window you measured is no longer the one you're recording.
- **Recomputing the window value from scratch.** `len(set(s[left:right+1]))` looks innocent but is `O(n)` per call, which makes the whole algorithm `O(n²)`. Maintain the state incrementally.
- **Counter-as-state with negative counts.** `Counter` subtraction can leave keys with value 0 in the dict. `del` them when their count hits 0; otherwise `len(counts)` lies about distinct count.
- **Mixing up "at most" and "exactly."** "Exactly K distinct" is a different problem from "at most K distinct." The naive sliding-window approach to "exactly K" is wrong. Use the atMostK − atMost(K − 1) trick.
- **Forgetting the empty-input / k=0 case.** Most templates default to "return 0" on empty input or `k=0`. State it explicitly at the top of the function or in the loop precondition.

---

## 9. The shape decision flow, on a single page

Read the problem. Then, before writing code, run through this flow out loud:

```
1. Is this sliding window?
   - Contiguous slice mentioned? ─→ probably yes.
   - Negative numbers + "sum at most/least k"? ─→ NO; use prefix-sum + hash map.
   - Non-contiguous subsequence? ─→ NO; use DP.

2. Fixed or variable?
   - "Window of size k" or "every k-subarray"? ─→ fixed-size; Lecture 1 §4.
   - Length is the answer? ─→ variable-size; continue.

3. Variable — which shape?
   - "Longest with property P"? ─→ shape A: shrink while P broken.
   - "Shortest with property P"? ─→ shape B: shrink while P holds; record inside.
   - "Count windows with property P"? ─→ shape C: at each right, add (right - left + 1).

4. What's the auxiliary state?
   - Sum/count? ─→ single integer.
   - Distinctness? ─→ set or Counter.
   - Frequency match against a target? ─→ Counter + a need/formed integer.
   - Max/min over the window? ─→ monotonic deque (Week 9 territory).

5. What's the invariant, in one sentence?
   - State it out loud. If you can't, you don't yet understand the problem.
```

By Sunday, this flow should be reflexive. Drill 1 is fixed-size — easy warm-up. Drills 2 and 5 are shape A. Drill 4 is shape B. Drill 3 is fixed-size with frequency invariant. Challenge 1 is the hardest combination (shape B + frequency invariant + need counter).

---

## 10. The full state-update playbook

For each auxiliary-state shape, here are the standard add/remove operations. Memorize them; you will use them every single time.

### Running sum

```python
def update_add(state, x):
    state["sum"] += x

def update_remove(state, x):
    state["sum"] -= x
```

### Frequency table (`Counter` or `defaultdict(int)`)

```python
def update_add(counts, x):
    counts[x] = counts.get(x, 0) + 1

def update_remove(counts, x):
    counts[x] -= 1
    if counts[x] == 0:
        del counts[x]              # critical for "distinct count" invariants
```

The `del` step is what most students forget. Without it, `len(counts)` includes keys with count 0, and the at-most-K invariant becomes wrong.

### Set (distinctness)

```python
def update_add(seen, x):
    seen.add(x)

def update_remove(seen, x):
    seen.discard(x)                # or seen.remove(x) if you know it's there
```

For sets, you usually pair this with a "while x in seen: shrink" inner loop. The set has no duplicates by definition, so removal is unconditional once `left` reaches the duplicate.

### Frequency match against a target (the `need`/`formed` trick)

```python
# Setup
need = Counter(t)
required = len(need)
formed = 0
window_counts = {}

# On add:
window_counts[ch] = window_counts.get(ch, 0) + 1
if ch in need and window_counts[ch] == need[ch]:
    formed += 1

# On remove:
window_counts[lch] -= 1
if lch in need and window_counts[lch] < need[lch]:
    formed -= 1
```

The invariant: `formed == required` iff every required character is satisfied. This is the precise tool for Challenge 1.

---

## 11. Self-check

Without notes, answer:

1. **What's the four-piece anatomy of a variable-size sliding-window loop?** (Add, shrink-condition, record — in either shape A's or shape B's order.)
2. **What's the difference between shape A and shape B?** (Shape A shrinks while invariant broken, records after; shape B shrinks while property holds, records inside.)
3. **Why is sliding window O(n) and not O(n²) despite the nested for/while?** (Amortized argument: each index advances at most n times in total across the whole algorithm.)
4. **What's the canonical bug in shape A's shrink loop?** (Forgetting to remove the element at `left` before advancing, leaving stale state.)
5. **Why does the sliding-window approach to "subarray sum at least K" require positive numbers?** (Shrinking from the left must monotonically decrease the sum; negatives break that monotonicity.)
6. **Trace the longest-at-most-2-distinct sliding window on `'aabbccc'`.** (Best window: `'bbccc'` length 5 or `'aabb'` length 4 or `'ccc'`... walk through it; the answer is 5.)
7. **What's the auxiliary state for Challenge 1 (minimum window substring)?** (A `Counter` of target frequencies, a `dict` of window frequencies, and the `need/formed` pair of integers.)

If you can answer all seven, proceed to the [exercises](../03-exercises/00-overview.md). If you can't, re-read sections 3–7 before starting Drill 1.

---

## Further reading

- **CP-Algorithms — Two Pointers Technique** (the article conflates two-pointer and sliding window in places — read critically): <https://cp-algorithms.com/two_pointers/two_pointers.html>
- **NeetCode's sliding-window playlist** — walks the canonical 10 problems in this lecture's vocabulary.
- **LeetCode editorial for Problem 76 (Minimum Window Substring)** — the official write-up is excellent and pairs well with Challenge 1.

Next: the [exercises](../03-exercises/00-overview.md). Five drills, in order. Recorder running.
