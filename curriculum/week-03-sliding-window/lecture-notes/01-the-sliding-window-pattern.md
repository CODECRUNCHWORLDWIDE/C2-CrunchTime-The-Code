# Lecture 1 — The Sliding Window Pattern

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a sliding-window problem within 30 seconds, name the two sub-shapes (fixed vs variable), state the window invariant out loud, and pick the right loop shape on first read.

Last week we learned to reach for a `dict` or `set` when the input is unsorted. This week we learn to recognize when a problem that *looks* like "compute something over every contiguous subarray" is actually a single linear scan with two indices that never go backwards. That recognition saves you a complexity class — usually `O(n·k)` or `O(n²)` collapses to `O(n)` — and it shows up in roughly one in five interview problems at the medium tier.

By the end of this lecture you should be able to read a problem and, within 30 seconds, say one of three things out loud: "fixed-size sliding window," "variable-size sliding window," or "not sliding window — here's why."

---

## 1. What "sliding window" means

A **window** is a contiguous slice of the input — `nums[left..right]` for an array, `s[left..right]` for a string. The **sliding** is the discipline: both `left` and `right` move in only one direction (forward), and they never cross. The window's *contents* change as the indices move, but its **shape** is always a contiguous slice.

Visualization, fixed window of size 3:

```
nums:  [ a  b  c  d  e  f ]
        [ a  b  c ]              ← window at left=0, right=2
           [ b  c  d ]           ← slide: left=1, right=3
              [ c  d  e ]        ← slide: left=2, right=4
                 [ d  e  f ]     ← slide: left=3, right=5
```

Variable window, growing and shrinking:

```
s:  [ a  b  c  a  b  c  b  b ]
    [ a ]                        ← right=0
    [ a  b ]                     ← right=1
    [ a  b  c ]                  ← right=2
       [ b  c  a ]               ← right=3 caused a repeat; left moved to 1
          [ c  a  b ]            ← right=4 caused a repeat; left moved to 2
             [ a  b  c ]         ← right=5 caused a repeat; left moved to 3
                [ b  c  b ]      ← right=6 caused a repeat; left moved to 5
                   [ c  b ]      ← left moves past the repeat
```

The pattern's power comes from one observation:

> **Each index advances at most `n` times. The total work is `O(n)` no matter how the inner shrink loop looks.**

That amortized argument is what makes sliding window an `O(n)` pattern even when the inner loop *appears* to do extra work. We'll formalize it in section 6.

---

## 2. Why this is *not* two-pointer (and why the distinction matters)

Last week and the week before, you saw "two-pointer converging" — `left = 0, right = n-1`, move toward each other. You also saw "two-pointer same-direction" — `read` and `write`, both starting at 0, partitioning the array in place.

Sliding window uses two indices. They start at the same end. They move in the same direction. So far this *looks* like the same-direction two-pointer. The difference:

| | Same-direction two-pointer | Sliding window |
|--|--|--|
| **What the two indices represent** | One reads, one writes — they don't define a region | Both define a *contiguous region* (the window) |
| **Why you'd use it** | In-place mutation / partitioning | Compute something about every contiguous slice |
| **Auxiliary state** | Usually none | Almost always: a running sum, a `Counter`, a `set` |
| **What changes between iterations** | One element is overwritten | The window contents shift; the auxiliary state is updated incrementally |
| **The answer is** | A modified array / a count of uniques | A length, a count of windows, a max/min over windows |

Quick test. Read these prompts. Two-pointer or sliding window?

1. "Remove duplicates from a sorted array in place." → **Same-direction two-pointer.** The `read` and `write` don't define a region; one just reads, one writes.
2. "Find the longest substring without repeating characters." → **Sliding window.** The window contents are the substring; the auxiliary state is "have I seen this character in the window?"
3. "Move all zeros to the end." → **Same-direction two-pointer.** Same shape as remove-duplicates.
4. "Find the longest subarray with sum at most K." → **Sliding window.** The window is the subarray; the auxiliary state is the running sum.

When in doubt, ask: *"is there a contiguous slice that the algorithm is reasoning about?"* If yes, sliding window. If no, two-pointer.

---

## 3. The two sub-shapes

Sliding window has two sub-shapes that look superficially similar but produce very different loop bodies. Picking the right one in Match saves you the panic of writing code that doesn't fit the problem.

| Sub-shape | Window size | Triggered by |
|-----------|-------------|--------------|
| **Fixed-size window** | Constant `k` from the prompt | "for every contiguous subarray of length `k`," "moving average of size `k`" |
| **Variable-size window** | Grows and shrinks based on an invariant | "longest substring with property P," "shortest subarray with property P," "count of windows satisfying P" |

The recognition signal that disambiguates: **does the prompt give you a number `k` upfront, or does the window length emerge from the algorithm?**

### Fixed-size — the trigger words

- "every contiguous subarray of length `k`"
- "moving average of size `k`"
- "maximum sum of any `k`-length subarray"
- "permutation of `pattern` as a substring" (the window size equals `len(pattern)`)
- "find all anagrams of `p` in `s`" (same — the window size is `len(p)`)

When you see a length supplied as input, the window's size is determined before you write a line of code. The loop body is the same on every iteration.

### Variable-size — the trigger words

- "longest substring [with some property]"
- "shortest subarray [with some property]"
- "longest run of [characters / values] with at most K distinct"
- "number of subarrays with [property]"
- "smallest window containing all characters of `t`"

When the *answer itself* is a length or count of windows, the loop has to *find* the right window size. The loop body has an inner shrink condition that's specific to the problem.

---

## 4. Fixed-size windows: the canonical shape

```python
def fixed_window_template(nums, k):
    # Initialize the first window: nums[0..k-1]
    state = initialize_state(nums[:k])
    answer = current_value(state)

    # Slide: at each step, remove nums[left], add nums[right]
    for right in range(k, len(nums)):
        left = right - k
        update_remove(state, nums[left])
        update_add(state, nums[right])
        answer = combine(answer, current_value(state))

    return answer
```

Three observations:

1. **The first window is built explicitly.** The loop doesn't start at index 0; it starts at index `k` (the first index *not* in the initial window). The work to build the first window is `O(k)`, then each slide is `O(1)`.
2. **State updates are incremental.** Adding `nums[right]` and removing `nums[right - k]` together cost `O(1)` per slide, *not* `O(k)`. If you recompute the state from scratch each iteration, you've written an `O(n·k)` algorithm — which means you didn't actually do sliding window, you did brute force in a sliding-window-shaped wrapper.
3. **`left` is derived from `right`.** Many writers introduce `left` as a separate variable. Either works; the derivation makes the invariant `right - left + 1 == k` explicit.

### Canonical problem: maximum sum of any subarray of size `k`

```python
def max_sum_k(nums, k):
    if k > len(nums):
        return 0
    window_sum = sum(nums[:k])
    best = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)
    return best
```

**O(n) time, O(1) space.** The naive "for each starting index, compute sum of k elements" is `O(n·k)`. Sliding window collapses it by reusing the previous window's sum.

The discriminator: **what does `window_sum` mean at any point in the loop?** It is the sum of `nums[right-k+1..right]`. That's the invariant. State it out loud during your Plan step.

---

## 5. Variable-size windows: the expand-then-shrink shape

```python
def variable_window_template(nums):
    state = empty_state()
    left = 0
    answer = initial_answer()

    for right in range(len(nums)):
        update_add(state, nums[right])

        # Shrink while the invariant is broken (or while we want a smaller window)
        while invariant_broken(state):
            update_remove(state, nums[left])
            left += 1

        # At this point the invariant holds.
        answer = combine(answer, window_value(left, right, state))

    return answer
```

Four observations:

1. **The outer `for` advances `right` once per iteration.** It never backs up. So `right` makes at most `n` steps.
2. **The inner `while` advances `left` until the invariant holds.** It also never backs up. Across the entire algorithm, `left` also makes at most `n` steps.
3. **Total inner-loop iterations across all `right` values sum to at most `n`.** Not `n` per outer iteration — `n` *total*. That's the amortized argument.
4. **State updates on both sides.** `update_add` runs once per outer step; `update_remove` runs each time `left` advances. Both must be `O(1)` for the algorithm to be `O(n)`.

### The first canonical problem: longest substring without repeating characters

```python
def longest_unique_substring(s: str) -> int:
    last_seen = {}     # char -> most recent index in the current window
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            # ch is already in the window; shrink past its old position
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

**O(n) time, O(min(n, alphabet)) space.** Each character is processed once when `right` reaches it; `left` jumps forward to skip past duplicates. The window invariant: **every character inside `s[left..right]` is unique.**

Notice the shape: the `while` shrink loop is *implicit* here — we jump `left` directly to the position just past the old occurrence, rather than removing one character at a time. Both shapes are valid sliding window. The explicit-shrink version is sometimes clearer:

```python
def longest_unique_substring_explicit(s: str) -> int:
    in_window = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in in_window:
            in_window.remove(s[left])
            left += 1
        in_window.add(ch)
        best = max(best, right - left + 1)
    return best
```

Same complexity, same correctness. Use whichever shape your interviewer's prompt nudges you toward. In your Plan step, state which shape you're choosing and why.

### The second canonical shape: "longest with at most K distinct"

A whole family of problems uses this template. The invariant: **the window contains at most `K` distinct values.** When adding a value pushes the distinct count over `K`, shrink from the left until it's back to `K`.

```python
def longest_at_most_k_distinct(s: str, k: int) -> int:
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

This template is the heart of Drill 5 (Fruit Into Baskets — at most 2 distinct) and one of the family of follow-ups (longest with exactly K, longest with at most K). Internalize it.

### The third canonical shape: "shortest with property P"

For "find the *shortest* subarray such that the property holds," the loop shape flips: you expand `right` until the property holds, then *shrink* `left` while the property *still* holds. The answer is updated *inside the shrink loop*, not after it.

```python
def shortest_at_least_target(nums, target):
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

This is the shape of Drill 4 (Minimum Size Subarray Sum). The invariant maintained by the shrink loop is the *opposite* of the longest-with-at-most-K case — we shrink *while the property holds*, not *while it's broken*. That sign flip is the difference between "longest" and "shortest" sliding window.

We will work this shape in detail in Lecture 2.

---

## 6. The amortized `O(n)` argument — say it out loud

Every sliding-window write-up should include this sentence in Evaluate:

> "**Why this is O(n).** The outer loop advances `right` exactly `n` times. The inner `while` advances `left` — but `left` can only move forward, and only up to `n` times across the entire algorithm. So the total inner-loop work, summed over all outer iterations, is at most `n`. Total work: `n + n = 2n = O(n)`."

That's the *amortized* argument. It is the single most important sentence in any sliding-window interview answer. Memorize the shape. Say it on every problem.

A common mistake: looking at the nested `for ... while ...` and calling it `O(n²)`. That's wrong, and it's the failure mode this lecture exists to fix. The inner `while` does *not* run up to `n` times *per outer iteration* — it runs up to `n` times *in total*. Two loops, two indices, each advancing at most `n` times.

Compare:

```python
# This is O(n^2): inner loop bound depends on the outer index
for i in range(n):
    for j in range(i, n):    # j resets at each i
        ...

# This is O(n): inner loop variable doesn't reset
left = 0
for right in range(n):
    while condition:         # left does not reset
        left += 1
    ...
```

The difference: in the second pattern, `left` *carries forward* from outer iteration to outer iteration. Once advanced, it never goes back. That's what makes the total inner work `O(n)`, not `O(n²)`.

---

## 7. Picking the right auxiliary state

The state inside the window is almost always one of four shapes. Pick correctly during Plan.

| Property of the window | Auxiliary state | Update cost |
|------------------------|-----------------|-------------|
| Sum / product / count | A single integer / float | O(1) per add/remove |
| Distinctness / membership | `set` or `Counter` | O(1) average per add/remove |
| Character/value frequency | `Counter` or `defaultdict(int)` | O(1) average per add/remove |
| Max / min in window | Monotonic `deque` (Week 9) | O(1) amortized per add/remove |

A common mistake: using a `list` and calling `min()` or `max()` on it each iteration. That's `O(k)` per iteration, which makes the whole algorithm `O(n·k)` — back to brute force. Pick the right data structure.

For frequency tables, `Counter` and `defaultdict(int)` are interchangeable for the basic add/remove pattern. `Counter` gives you arithmetic and equality for free (`Counter("aab") == Counter("aba")` is `True`); `defaultdict` is a touch faster on raw inserts. Most interviewers don't care which you pick — but say which and why.

---

## 8. The canonical recognition signals (the 30-second match)

Stop. Read the prompt slowly. Ask these in order:

1. **Is the problem about a contiguous slice?** Look for *substring*, *subarray*, *contiguous*, *consecutive*. If yes, sliding window is a strong candidate.
2. **Is there a fixed length `k` given as input?** If yes, fixed-size window. If no, go to 3.
3. **Is the answer a length, a count of windows, or a max/min/sum over windows?** If yes, variable-size window is likely. If no, reconsider — might be DP or hash map.
4. **Are the inputs all non-negative (for sum-based problems)?** If "sum at least target" or "sum at most target" with possible negatives, sliding window may not apply — the monotone-shrink invariant breaks. Use prefix-sum + hash map instead (Week 2's Challenge 1 territory).
5. **Is the property *contiguity*, or is it *subsequence*?** Subsequence problems (elements in order but not adjacent) are *not* sliding window. They're DP.

The 30-second decision tree:

```
"contiguous slice" mentioned or implied?
├── No  ──→ not sliding window. Pattern is hash map, DP, or something else.
└── Yes
    ├── Fixed length k given?  ──→ fixed-size window
    └── Length is the answer?
        ├── "longest / largest" satisfying P?  ──→ variable window, shrink while P broken
        ├── "shortest / smallest" satisfying P? ──→ variable window, shrink while P holds
        └── "count of subarrays" satisfying P?  ──→ variable window, may need atMostK-trick
```

```mermaid
flowchart TD
  A["Contiguous slice mentioned"] -->|No| B["Not sliding window"]
  A -->|Yes| C["Fixed length k given"]
  C -->|Yes| D["Fixed-size window"]
  C -->|No| E["Length is the answer"]
  E -->|Longest satisfying P| F["Variable window - shrink while P broken"]
  E -->|Shortest satisfying P| G["Variable window - shrink while P holds"]
  E -->|Count of subarrays| H["Variable window - atMostK trick"]
```

*The 30-second recognition path from a contiguous-slice cue to the right window shape.*

This decision tree is what we want in muscle memory by Sunday.

---

## 9. When sliding window doesn't fit

Equally important: knowing when to *reject* the pattern.

- **Negative numbers + "sum at most K"** — the running sum is not monotonic, so shrinking from the left doesn't restore the invariant cleanly. Use prefix-sum + hash map.
- **Non-contiguous subsequence problems** — sliding window is contiguous by definition. "Longest increasing subsequence" is not contiguous; it's DP.
- **"Exactly K distinct" framing** — direct sliding window doesn't naturally count "exactly K." A common reformulation: **exactly K = atMostK − atMost(K−1)**. Run the at-most-K sliding window twice; subtract. This is in the homework.
- **Window over a tree or graph** — sliding window is a 1-D pattern. Tree/graph "windows" are BFS or DFS, covered Weeks 6–7.

Recognizing the *negative space* of the pattern matters as much as the positive recognition.

---

## 10. Worked example end-to-end: longest substring without repeating characters

We will work this in full UMPIRE, abbreviated. Drill 2 is this exact problem.

**[U — 2 minutes]**

> "I'm given a string `s`. I need the length of the longest substring (contiguous) where every character is unique. Confirm: substring not subsequence; characters can repeat outside the substring but not inside it. Walk an example: `'abcabcbb'` — longest unique substring is `'abc'`, length 3."

**[M — 30 seconds]**

> "Sliding window. Contiguous + 'longest with property' is the canonical variable-size shape. Auxiliary state: a `set` of characters in the current window, or a `dict` mapping char → last-seen index."

**[P — 2 minutes]**

> "Outer loop `right` from 0 to n-1. Maintain `left` starting at 0. Use `last_seen` dict. When `right` lands on a char already in the window (its `last_seen` is `>= left`), jump `left` to `last_seen[ch] + 1`. Update `last_seen[ch] = right`. Update `best = max(best, right - left + 1)`. Return `best`."

**[I — 3 minutes]**

```python
def longest_unique_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

**[R — 2 minutes]**

> "Trace on `'abcabcbb'`. r=0 ('a'): not in window, last_seen={a:0}, best=1, left=0. r=1 ('b'): best=2. r=2 ('c'): best=3. r=3 ('a'): 'a' is at last_seen=0 ≥ left=0, so left jumps to 1. last_seen={a:3,b:1,c:2}, best stays 3. r=4 ('b'): 'b' at last_seen=1 ≥ left=1, left jumps to 2. r=5 ('c'): 'c' at last_seen=2 ≥ left=2, left jumps to 3. r=6 ('b'): 'b' at last_seen=4 ≥ left=3, left jumps to 5. r=7 ('b'): 'b' at last_seen=6 ≥ left=5, left jumps to 7. best stays 3. ✓"

**[E — 1 minute]**

> "**Time O(n).** Outer loop is n iterations; the `last_seen` lookup and assignment are O(1) average. **Space O(min(n, alphabet))** — the dict holds at most one entry per distinct character ever seen. Tradeoff: brute force 'for each pair (l, r), check uniqueness' is O(n³) (or O(n²) with a set). Sliding window collapses it. No improvement obvious; O(n) is the lower bound."

That's UMPIRE on a textbook sliding-window problem, end-to-end, in about 10 minutes. The drill is to do this every single time.

---

## 11. Self-check

Without notes, answer:

1. **What's a window?** (A contiguous slice `s[left..right]` of the input.)
2. **What's the difference between sliding window and two-pointer converging?** (Sliding window's indices move only forward and define a contiguous region; two-pointer converging may move either direction and doesn't necessarily define a region.)
3. **For each sub-shape (fixed / variable), name a canonical problem and its time complexity.** (Fixed: max sum of k-subarray, O(n). Variable: longest substring without repeat, O(n).)
4. **State the amortized O(n) argument.** (Each index moves at most n times total; the nested `for/while` does at most 2n iterations summed across the algorithm.)
5. **When does sliding window not fit?** (Negative numbers + "sum at most K"; non-contiguous subsequences; "window over a graph" — those are BFS/DFS.)
6. **What's the auxiliary state for "longest substring with at most K distinct characters"?** (A frequency table, `Counter` or `defaultdict(int)`.)

If you can answer all six without hesitation, proceed to [Lecture 2 — The Shrinking and Growing Mechanics](./02-the-shrinking-and-growing-mechanics.md).

---

## Further reading

- **NeetCode's free sliding-window playlist** (YouTube): a clean, free run-through of 10+ canonical problems. Skim two or three videos at 1.5×.
- **CP-Algorithms — Sliding Window Maximum**: <https://cp-algorithms.com/data_structures/deque.html#sliding-window-minimum> — preview of the deque-based window-max idiom for Week 9.
- **LeetCode Sliding Window tag** (free practice ground): <https://leetcode.com/tag/sliding-window/> — pick titles and predict fixed vs variable before reading constraints.

Next: [Lecture 2 — The Shrinking and Growing Mechanics](./02-the-shrinking-and-growing-mechanics.md).
