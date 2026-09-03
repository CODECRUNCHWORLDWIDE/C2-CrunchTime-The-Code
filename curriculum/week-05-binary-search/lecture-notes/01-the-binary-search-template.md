# Lecture 1 — The Binary-Search Template

> **Duration:** ~2 hours.
> **Outcome:** You can write the canonical `lo <= hi` loop from memory, pick the correct shrink rule for each of the four variants (find any / find first / find last / find boundary), defend your boundary convention out loud, and handle the rotated-sorted-array case without re-deriving the algorithm.

Four weeks of Phase 1 trained you on linear-time patterns — two-pointer, sliding window, fast/slow. This lecture introduces the first *logarithmic*-time pattern of the course. The geometry is different: instead of walking across the array linearly, you bisect it. The trade is also different: you give up the simplicity of "one pointer, one direction" for the asymptotic win of `O(log n)`, and you pay for the speed with *boundary discipline*. Every binary-search bug in interview history is a boundary bug.

By the end of this lecture you should be able to read a sorted-array problem and, within 30 seconds, say one of four things out loud: "classic binary search — find any," "binary search lower bound — find first," "binary search upper bound — find last," or "boundary search — find smallest `k` such that ...". The fifth thing — "this is not binary search, here is why" — is just as important and is graded in the quiz.

---

## 1. What binary search means

A **binary search** is an algorithm that, given a *sorted* sequence and a target property, halves the search space at each iteration until the target is located. The classical setting is "find a target value in a sorted array," but the *idea* generalizes: anywhere you can answer "is the answer to the left or to the right?" in `O(1)` based on a midpoint test, binary search applies.

Visualization on a 7-element sorted array, target = 13:

```
indices:  0    1    2    3    4    5    6
values: [ 1,   3,   7,  10,  13,  17,  21]

step 0:  lo=0, hi=6, mid=3  ─→ arr[3] = 10, 10 < 13, search right half
step 1:  lo=4, hi=6, mid=5  ─→ arr[5] = 17, 17 > 13, search left half
step 2:  lo=4, hi=4, mid=4  ─→ arr[4] = 13, found, return 4
```

Three iterations on a 7-element array. With `n = 1_000_000`, twenty iterations. With `n = 1_000_000_000`, thirty. The asymptotic complexity is `O(log₂ n)`. The base of the logarithm is fixed because the search space halves at each step.

The pattern's power comes from one observation:

> **At every iteration, you eliminate half of the remaining search space. If the search space has size `n`, the number of iterations is bounded by `⌈log₂ n⌉`.**

That is the entire algorithm. The hard part is writing the loop without an off-by-one error.

---

## 2. The canonical template — closed interval

```python
def binary_search(arr: list[int], target: int) -> int:
    """Return the index of target in arr, or -1 if not present. O(log n) time, O(1) space."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Nine lines. Memorize the shape.

Five observations:

1. **Initialization: `lo = 0`, `hi = len(arr) - 1`.** Both endpoints are *valid indices*. The interval `[lo, hi]` is *closed* on both sides — every integer in it is a real index into `arr`. This is the **closed-interval convention**.
2. **Loop guard: `while lo <= hi`.** The `<=` pairs with the closed interval. When `lo == hi`, the interval contains exactly one element; we must test it. When `lo > hi`, the interval is empty and we exit.
3. **Mid formula: `mid = lo + (hi - lo) // 2`.** Equivalent to `(lo + hi) // 2` in Python (arbitrary-precision integers), but the form above is *overflow-safe* in C / Java / Rust. **Always write it this way.** The habit transfers.
4. **Shrink rules:**
   - `arr[mid] < target` → the answer (if it exists) is strictly right of mid → `lo = mid + 1`. We exclude mid because we just tested it.
   - `arr[mid] > target` → the answer is strictly left of mid → `hi = mid - 1`. Same reasoning.
   - `arr[mid] == target` → return mid.
   The `+ 1` and `- 1` are not optional. They are the reason the loop terminates — every iteration shrinks the interval by at least one element.
5. **Post-loop: `return -1`.** If the loop exits via the `lo <= hi` guard, the target is not in the array.

One house rule before you copy that last line into a drill. The template above returns `-1` because that is the shape every textbook prints, and you should be able to read it. **This course's contracts return `None`.** An in-band sentinel like `-1` or `0` only works when the sentinel cannot also be a legitimate answer, and in half of this week's problems it can be — index `0` is a real position, and a negative value is a real reading. Learn the template with `-1`; write your solutions with `None`; be ready to say which you would use and why.

### Time and space

- **Time: O(log n).** Each iteration halves the search space; the loop body is `O(1)`.
- **Space: O(1).** Three integers (`lo`, `hi`, `mid`). No recursion stack.

Say the time defense out loud every time:

> "**O(log n) time** because each iteration halves the search interval — starting from `n` and dividing by two on each step gives `log₂(n)` iterations. **O(1) space** — three pointers, no recursion. The trade against linear search is the requirement that the array be *sorted*; if the input is unsorted, sorting first costs `O(n log n)`, which dominates and makes the optimization useless for a single query. Binary search is the right tool when the array is already sorted or when many queries amortize the sort cost."

That is the sentence interviewers grade. Memorize the cadence.

---

## 3. The closed vs half-open templates

Two boundary conventions exist for binary search. Both are correct; they shrink the space differently. Pick one and *defend it*.

### Convention A — closed interval `[lo, hi]`

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2
    if arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
```

- Initial `hi = len(arr) - 1`.
- Loop guard `lo <= hi`.
- Shrink with `mid + 1` and `mid - 1`.
- Terminates when `lo > hi`.
- Post-loop, `lo` is the lower-bound index (the leftmost position satisfying the predicate).

### Convention B — half-open interval `[lo, hi)`

```python
lo, hi = 0, len(arr)
while lo < hi:
    mid = lo + (hi - lo) // 2
    if arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid
```

- Initial `hi = len(arr)` (one *past* the last valid index).
- Loop guard `lo < hi`.
- Shrink with `mid + 1` on the left and `mid` (not `mid - 1`) on the right.
- Terminates when `lo == hi`.
- Post-loop, `lo` (= `hi`) is the lower-bound index.

The half-open convention is what Python's `bisect_left` and C++'s `std::lower_bound` use internally. The closed convention is what most introductory textbooks use.

**This course uses the closed convention** for the "find any target" variant and the half-open convention for the "find boundary / first true" variant. The reason: the closed convention's post-loop assertion ("if found, returned inside the loop") is the cleanest fit for the classic search, and the half-open convention's post-loop assertion (`lo == hi == first true position`) is the cleanest fit for boundary search.

Pick a convention per *variant*, not per problem. Stick to those two conventions and you will write fewer bugs.

---

## 4. Off-by-one diagnostics — the four bug patterns

Off-by-one in binary search has four canonical shapes. Recognize them when you debug.

### Bug 1 — infinite loop

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] < target:
        lo = mid       # WRONG — should be mid + 1
    else:
        hi = mid - 1
```

When `lo == hi == mid`, if `arr[mid] < target`, we set `lo = mid`, which is unchanged. The loop spins forever. The fix is `lo = mid + 1` — we already tested `mid`, so it is correct to exclude it.

**Rule of thumb:** in the closed convention, both shrink rules must *exclude* `mid`. Use `mid + 1` and `mid - 1`. Anything else loops forever.

### Bug 2 — overshoot

```python
lo, hi = 0, len(arr)         # WRONG — should be len(arr) - 1 with closed convention
while lo <= hi:
    mid = lo + (hi - lo) // 2
    if arr[mid] < target:    # crashes when mid == len(arr)
        lo = mid + 1
    else:
        hi = mid - 1
```

Initializing `hi = len(arr)` with the closed convention puts an invalid index into the interval. On the first iteration, `mid` could be `len(arr) - 1` (safe) — but if the input is the empty array, the loop runs once with `mid = 0` and crashes on `arr[mid]`. The mismatch between the initialization and the guard is the bug.

**Rule of thumb:** the initialization must match the guard. Closed `[lo, hi]` ↔ `hi = len(arr) - 1` ↔ `lo <= hi`. Half-open `[lo, hi)` ↔ `hi = len(arr)` ↔ `lo < hi`.

### Bug 3 — missed last element

```python
lo, hi = 0, len(arr) - 1
while lo < hi:               # WRONG — closed convention needs <=
    mid = lo + (hi - lo) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
return -1
```

When `lo == hi`, the interval still contains one element — but the `<` guard exits without testing it. If the target *is* that element, we incorrectly return `-1`.

**Rule of thumb:** use `<=` with the closed convention, `<` with the half-open convention. Match them.

### Bug 4 — wrong mid for "find last"

When searching for the *last* occurrence (upper-bound family), the mid formula must round *up*, not down:

```python
mid = lo + (hi - lo + 1) // 2   # round-up version, for the upper-bound family
```

Otherwise the loop hangs at `lo == hi - 1`. This is the most subtle bug in binary search. We will work it out in section 7 (find first / last with duplicates).

---

## 5. The four variants — a decision table

Most binary-search problems fit one of four shapes. Recognize the shape; pick the template.

| # | Variant | Problem shape | Convention | Mid formula | Shrink (less) | Shrink (greater-equal) | Return |
|---|---------|---------------|-----------|-------------|---------------|------------------------|--------|
| 1 | **Find any** | Is target in arr? | Closed `[lo, hi]` | `(hi - lo) // 2` | `lo = mid + 1` | `hi = mid - 1` | mid (in loop) or -1 |
| 2 | **Find first** (lower bound) | Leftmost i where arr[i] >= target | Half-open `[lo, hi)` | `(hi - lo) // 2` | `lo = mid + 1` | `hi = mid` | `lo` |
| 3 | **Find last** (upper bound) | Rightmost i where arr[i] <= target | Closed `[lo, hi]` | `(hi - lo + 1) // 2` | `lo = mid` | `hi = mid - 1` | `lo` |
| 4 | **Find boundary** (predicate) | Smallest k where feasible(k) is True | Half-open `[lo, hi)` | `(hi - lo) // 2` | `lo = mid + 1` | `hi = mid` | `lo` |

Variants 2 and 4 use the same template. Variant 4 is the parametric-search version — covered in Lecture 2.

Memorize the table. In a mock interview, when you read "find first / leftmost / smallest k," your hand should write variant 2 without thinking.

---

## 6. The "find first" template — lower bound

Find the leftmost index `i` such that `arr[i] >= target`. If no such index exists, return `len(arr)`.

```python
def lower_bound(arr: list[int], target: int) -> int:
    """Return the leftmost index i such that arr[i] >= target, or len(arr) if none."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

Six lines. The half-open convention.

The invariant: at every step, **the answer is in `[lo, hi)`**. That is, every index `< lo` has `arr[i] < target`, and every index `>= hi` either does not exist or has `arr[i] >= target`.

When `lo == hi`, the interval is empty, and `lo` is the first position where the predicate (`arr[i] >= target`) flips from False to True. That is the lower bound, by definition.

### Worked trace on `arr = [1, 3, 3, 5, 8]`, target = 3

```
step 0:  lo=0, hi=5, mid=2, arr[2]=3, not < 3, hi=2
step 1:  lo=0, hi=2, mid=1, arr[1]=3, not < 3, hi=1
step 2:  lo=0, hi=1, mid=0, arr[0]=1, < 3, lo=1
step 3:  lo=1, hi=1, loop exits
return 1
```

The leftmost index with value `>= 3` is index 1. Correct.

### Trade with `bisect_left`

Python's `bisect.bisect_left(arr, target)` does exactly this. In an interview you may use it *if asked* — but the interview standard is to **write the loop yourself**. The library call gets a half-point; the hand-written loop gets full marks.

---

## 7. The "find last" template — upper bound

Find the rightmost index `i` such that `arr[i] <= target`. If no such index exists, return `-1`.

```python
def upper_bound_inclusive(arr: list[int], target: int) -> int:
    """Return the rightmost index i such that arr[i] <= target, or -1 if none."""
    lo, hi = -1, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2     # round up
        if arr[mid] <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo
```

Seven lines. Note four differences from lower bound:

1. **`lo = -1`.** The "no valid answer" sentinel — interpreted as "before the array begins."
2. **`hi = len(arr) - 1`.** Closed-on-the-right convention.
3. **`mid` rounds *up*.** `lo + (hi - lo + 1) // 2`. Without the `+ 1`, the loop hangs at `lo == hi - 1`.
4. **Shrink `lo = mid` (not `mid + 1`).** We want to *keep* mid as a candidate; we just established `arr[mid] <= target`.

The round-up `mid` formula is non-obvious. Here is why it is necessary.

Suppose `lo = 3, hi = 4`. The standard mid `lo + (hi - lo) // 2 = 3 + 0 = 3`. If `arr[3] <= target`, we set `lo = 3` — unchanged. Infinite loop.

With the round-up mid: `lo + (hi - lo + 1) // 2 = 3 + 1 = 4`. If `arr[4] <= target`, we set `lo = 4`, and the loop exits. If `arr[4] > target`, we set `hi = 3`, and the loop exits.

The round-up `mid` is the price you pay for `lo = mid` (keeping mid as a candidate). The lower-bound variant has the dual problem with `hi = mid` and uses round-down.

**Mnemonic:** if you write `lo = mid` (keeping mid on the left), round up. If you write `hi = mid` (keeping mid on the right), round down. Anything else loops.

---

## 8. The whole run of a repeated value — two searches, one contract

Given a non-decreasing sequence with duplicates, return the **half-open slice bounds** of the run of entries equal to a value. That is, return `(start, end)` such that `data[start:end]` is exactly that run.

The trick is to call **lower bound twice**: once for the value itself, which gives `start`, and once for the value *plus one*, which gives `end`. Nothing else is needed.

```python
def value_run(data: list[int], value: int) -> tuple[int, int]:
    """Return (start, end) with data[start:end] exactly the entries equal to value.
    data is non-decreasing. On a miss, both searches land on the same insertion
    point and the slice comes out empty. O(log n) time, O(1) space."""

    def lower_bound(cutoff: int) -> int:
        lo, hi = 0, len(data)          # half-open [lo, hi)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if data[mid] < cutoff:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return lower_bound(value), lower_bound(value + 1)
```

Look at what is *absent*. There is no "is it present?" check, no sentinel, and no branch for the empty sequence. If the value is missing, both searches converge on the same insertion point, the slice is empty, and the caller can still write `data[start:end]` without special-casing anything. If the sequence itself is empty, both searches return `0` and the answer is `(0, 0)`. The contract does the work the branches would have done.

Two properties fall out, and both are worth saying out loud:

- `end - start` is the count of matching entries, for free.
- The return value is always a **valid slice** into `data` — never a value the caller must interpret.

Compare that with the shape you will see on most judges, which returns inclusive endpoints and a sentinel pair like `[-1, -1]` on a miss. That version is correct too, but it pushes work onto every caller: `-1` silently means "the last element" to a slice, and the count becomes `last - first + 1` with an off-by-one waiting in it. Choosing the half-open contract is a design decision, and being able to defend a design decision is what separates a candidate from a code generator.

This is [Exercise 2](../exercises/exercise-02-scan-window.md), where the sequence is a scan log and the value is a minute of the week.

---

## 9. Rotated sorted array — the "which half is sorted?" trick

A rotated sorted array is a sorted array that has been cyclically shifted. The physical dump of a ring buffer is the everyday example: ids ascend as they are written, the writer wraps to slot 0 when the buffer fills, and what you read back is `[58, 61, 64, 70, 12, 19, 33, 47]` — the ascending sequence `12, 19, 33, 47, 58, 61, 64, 70` starting from the middle. A rotated array contains exactly one "pivot" where the order breaks.

At any step of binary search on a rotated array, **at least one of the two halves `[lo, mid]` and `[mid, hi]` is fully sorted** (un-rotated). Identify which half is sorted, then check whether the target lies in that half. If yes, recurse into the sorted half; if no, recurse into the other half.

```mermaid
flowchart TD
  A["Compute mid"] --> B{"arr at mid equals target"}
  B -->|Yes| C["Return mid"]
  B -->|No| D{"Is left half sorted"}
  D -->|Yes| E{"Is target in left range"}
  D -->|No| F{"Is target in right range"}
  E -->|Yes| G["Search left half"]
  E -->|No| H["Search right half"]
  F -->|Yes| I["Search right half"]
  F -->|No| J["Search left half"]
```
*Each step picks the sorted half, then decides whether the target lies inside it.*

```python
def search_rotated(arr: list[int], target: int) -> int:
    """Search for target in a rotated sorted array. Returns index, or -1 if absent."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if arr[lo] <= arr[mid]:
            # left half [lo, mid] is sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # right half [mid, hi] is sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

Twelve lines. The decision is `arr[lo] <= arr[mid]` — if the left endpoint is `<=` the middle, the left half is sorted; otherwise the right half is.

The `<=` (not `<`) handles the edge case where `lo == mid` (single-element interval on the left). The standard mistake is using strict `<` and breaking when the left half has length 1.

This single-pass search returns the **physical** index. That is one of the two routes through [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md), which asks for something else — the row's *age* — and therefore needs the wrap point as well. Exercise 3 grades whether you can name both routes and say which contract makes each one the better choice. The wrap-point search on its own is Mini-Project Problem 2; the duplicate-tolerant version, where this discriminator stops working, is [Homework Problem 4](../homework/README.md).

### Worked trace on the buffer dump `arr = [58, 61, 64, 70, 12, 19, 33, 47]`, target = 19

```
step 0:  lo=0, hi=7, mid=3, arr[3]=70, != 19
         arr[0]=58 <= arr[3]=70, so [0, 3] is sorted
         is 19 in [58, 70)? No → lo = 4
step 1:  lo=4, hi=7, mid=5, arr[5]=19, == 19 → return 5
```

Two iterations. Now the miss, `target = 50` — an id inside the buffer's range that the writer happened to skip:

```
step 0:  lo=0, hi=7, mid=3, arr[3]=70, != 50
         arr[0]=58 <= arr[3]=70, so [0, 3] is sorted
         is 50 in [58, 70)? No → lo = 4
step 1:  lo=4, hi=7, mid=5, arr[5]=19, != 50
         arr[4]=12 <= arr[5]=19, so [4, 5] is sorted
         is 50 in [12, 19)? No → lo = 6
step 2:  lo=6, hi=7, mid=6, arr[6]=33, != 50
         arr[6]=33 <= arr[6]=33, so [6, 6] is sorted
         is 50 in [33, 33)? No → lo = 7
step 3:  lo=7, hi=7, mid=7, arr[7]=47, != 50
         arr[7]=47 <= arr[7]=47, so [7, 7] is sorted
         is 50 in [47, 47)? No → lo = 8
         lo > hi, loop exits → not found
```

Note step 2 and step 3: the "sorted half" is a single element, and the range test `arr[lo] <= target < arr[mid]` is empty and therefore false. That is exactly the case the `<=` in the discriminator protects. With a strict `<` the branch flips and the search walks off in the wrong direction.

The shape is identical to classic binary search; the only added complexity is the "which half is sorted?" branch.

---

## 10. When binary search does not apply

Equally important: knowing when to *reject* the pattern.

- **Unsorted array, single query, no monotonicity.** If the array is unsorted and you have one lookup to make, sort + binary search is `O(n log n)`. Linear scan is `O(n)`. Linear wins for a single query. The trade flips for `>= log n` queries.
- **No monotone predicate.** Binary search needs a way to decide "left or right" at each midpoint. Without monotonicity (in values *or* in a predicate), the algorithm has no comparator and does not work.
- **Continuous parameter, discrete answer.** Bisection on a real interval works, but with care about epsilon and termination. Out of scope for Phase 2; revisit in Phase 3.
- **Hash-map territory.** "Is this key present?" with no order requirement is `O(1)` with a hash. Binary search is `O(log n)`. Hash wins unless you also need order-related queries (range, predecessor, successor).
- **Linked structures.** Binary search needs random access. A linked list has no `O(1)` `mid` access; you would walk the list linearly to find the middle, which destroys the asymptotic win.

Recognizing the *negative space* of the pattern matters as much as the positive recognition. [Quiz](../quiz.md) questions Q3, Q5, and Q8 are the negative-space questions.

---

## 11. Worked example end-to-end: the ladder seat

We will work this in full FRAME, abbreviated. This is [Exercise 1](../exercises/exercise-01-ladder-seat.md), and it is the classic template with one deliberate twist: the sequence runs **descending**.

**[F — 1 minute]**

> "I am given the org's chess ladder as a list of ratings and one rating to look up. Return the seat index holding that rating, or `None` if nobody has it. Confirm three things. The list is sorted **strictly descending** — strongest first — so no two players share a rating. Seat indices are positions in the list as given; I must not reorder it. A match may not exist, and the absent value is `None`, because seat `0` is a real seat and a negative rating is a real rating, so no in-band sentinel is safe. Walk an example: `ratings = [2410, 2205, 2199, 1870, 1602, 1044]`, looking for `1870`. Answer: seat 3."

**[R — 20 seconds]**

> "Classic binary search — variant 1, 'find any.' The 30-second memo: *Sorted sequence plus a single exact-match query is the canonical signal. Closed interval `[lo, hi]` with `lo <= hi`. Auxiliary state: three integers. Because the order is descending, the branch that moves `lo` is `ratings[mid] > rating`, not `<` — I am re-deriving that, not recalling it. Why not a linear scan: two million ratings per page view against twenty-one comparisons. Why not a dict from rating to seat: `O(1)` per lookup but `O(n)` to build and `O(n)` to hold, and the ladder is rebuilt after every match, so the build cost dominates a single query.*"

**[A — 1 minute]**

> "Closed-interval convention. Initialize `lo = 0`, `hi = len(ratings) - 1`. Loop while `lo <= hi`. Compute `mid = lo + (hi - lo) // 2` — overflow-safe habit. If `ratings[mid] == rating`, return `mid`. If `ratings[mid] > rating`, the target is weaker and therefore *further down* the ladder: `lo = mid + 1`. Otherwise `hi = mid - 1`. If the loop exits, return `None`."

**[M — 2 minutes]**

```python
def find_ladder_seat(ratings: list[int], rating: int) -> int | None:
    """Return the seat index i with ratings[i] == rating, or None.
    ratings is sorted strictly DESCENDING. O(log n) time, O(1) space."""
    lo, hi = 0, len(ratings) - 1      # closed [lo, hi]
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if ratings[mid] == rating:
            return mid
        elif ratings[mid] > rating:   # descending: bigger midpoint means go right
            lo = mid + 1
        else:
            hi = mid - 1
    return None
```

Speak the boundary defense while your hands are moving: *"Closed interval `[lo, hi]` with `lo <= hi`. Both shrink rules exclude `mid` — `mid + 1` and `mid - 1` — so the interval strictly shrinks every iteration and the loop terminates."*

**[E · verify — 1 minute]**

> "Trace on `[2410, 2205, 2199, 1870, 1602, 1044]`, rating = 1870.
> Step 0: `lo=0, hi=5, mid=2`, `ratings[2]=2199 > 1870`, so go right: `lo=3`.
> Step 1: `lo=3, hi=5, mid=4`, `ratings[4]=1602 < 1870`, so go left: `hi=3`.
> Step 2: `lo=3, hi=3, mid=3`, `ratings[3]=1870`, match, return 3. ✓
> Now the miss, rating = 2200 — a value sitting between two real ratings.
> `lo=0, hi=5, mid=2`, `2199 < 2200`, go left: `hi=1`.
> `lo=0, hi=1, mid=0`, `2410 > 2200`, go right: `lo=1`.
> `lo=1, hi=1, mid=1`, `2205 > 2200`, go right: `lo=2`.
> `lo=2 > hi=1`, loop exits, return `None`. ✓
> And the empty ladder: `hi = -1`, the guard `0 <= -1` is false immediately, the loop never touches the list, return `None`. ✓"

**[E · cost — 1 minute]**

> "**Time `O(log n)`** — each iteration halves a closed interval of size `n`, so at most `⌈log₂ n⌉` iterations, and the body is `O(1)`. **Space `O(1)`** — three integers, no recursion. Best case `O(1)` when the rating sits at the first midpoint; worst and average `O(log n)`. Tradeoff: a linear scan is `O(n)` time and `O(1)` space — same space, worse time, and the ladder is already ordered so we pay nothing to use the order. A hash map is `O(1)` per query but `O(n)` to build and `O(n)` to hold; it wins only when the same ladder is queried many times between rebuilds. Improvement: none asymptotically — `Ω(log n)` is the comparison-model floor for this query."

That is FRAME on classic binary search, end-to-end, in about six minutes. The drill is to do this every time, even when the algorithm feels trivial — and *especially* when a small twist like the descending order tempts you to type the template from muscle memory instead of deriving it.

---

## 12. Two common bug patterns

After watching candidates write binary search in mocks, two bugs come up repeatedly. Build them into your Examine (verify) checklist.

### Bug 1 — `mid = mid` infinite loop (variant 3)

```python
lo, hi = 0, len(arr) - 1
while lo < hi:
    mid = lo + (hi - lo) // 2     # WRONG for variant 3 — round-down on round-up variant
    if predicate(mid):
        lo = mid
    else:
        hi = mid - 1
```

When `lo == hi - 1`, mid = `lo + 0 = lo`. If the predicate is True, `lo = mid = lo` — unchanged. Infinite loop. Fix: round up. `mid = lo + (hi - lo + 1) // 2`.

**Rule:** if your shrink rule is `lo = mid`, round up. If `hi = mid`, round down. Match them.

### Bug 2 — wrong convention for the variant

```python
# Wanted: find first occurrence of target
lo, hi = 0, len(arr) - 1     # WRONG — should be 0, len(arr) with half-open
while lo <= hi:
    mid = lo + (hi - lo) // 2
    if arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1           # WRONG — should be hi = mid
return lo                       # ambiguous — could be one past last
```

Mixing the closed convention's guard (`<=`) with the half-open shrink (`hi = mid`) produces a loop that either misses the answer or overruns. The fix is to use one *complete* convention per variant. Lower bound: half-open. Upper bound: closed with round-up. No mixing.

Get in the habit: write the convention name at the top of your variable initializer comment. `# half-open [lo, hi)` or `# closed [lo, hi]`. Three seconds; saves five minutes of debug.

---

## 13. Self-check

Without notes, answer:

**1.** What is the canonical loop guard for the closed-interval template?

<details>
<summary>Answer</summary>

`while lo <= hi`.

</details>

**2.** What is the mid formula and why is it written that way?

<details>
<summary>Answer</summary>

`mid = lo + (hi - lo) // 2`. Equivalent to `(lo + hi) // 2` in Python but overflow-safe in C / Java / Rust; habit transfers.

</details>

**3.** Why do you write `hi = mid - 1` in the closed convention but `hi = mid` in the half-open?

<details>
<summary>Answer</summary>

Closed: every index in `[lo, hi]` is a candidate; we have just tested `mid` and ruled it out, so it must be excluded — `hi = mid - 1`. Half-open: every index in `[lo, hi)` is a candidate and `hi` is already exclusive, so `hi = mid` drops `mid` from the range while keeping the contract. Mixing the two is the classic infinite loop: `hi = mid` in the closed convention never shrinks the range when `hi == lo + 1`.

</details>

**4.** For the upper-bound variant (find last), why does `mid` round up?

<details>
<summary>Answer</summary>

To avoid `mid = lo` when `lo == hi - 1`, which combined with `lo = mid` produces an infinite loop. Rounding up forces progress.

</details>

**5.** In a rotated sorted array, what is the discriminator at each midpoint?

<details>
<summary>Answer</summary>

`arr[lo] <= arr[mid]` — if True, the left half is sorted; if False, the right half is.

</details>

**6.** What is the time and space complexity, with defense sentence?

<details>
<summary>Answer</summary>

`O(log n)` time because each iteration halves the search space; `O(1)` space — three pointers, no recursion. Defense: linear scan is `O(n)`/`O(1)`; binary search trades the same space for `O(log n)` time *if* the array is sorted.

</details>

If you can answer all six without hesitation, proceed to [Lecture 2 — Binary Search on the Answer](./02-binary-search-on-the-answer.md).

---

## 14. The 30-second recognition signals

Stop. Read the prompt slowly. Ask these in order:

1. **Is the input a sorted array, or can it be sorted cheaply?** If yes, binary search is a strong candidate for any "find" query.
2. **Does the prompt mention "find the index of," "is target present," "first / last occurrence of"?** Strong signal for variants 1, 2, 3 respectively.
3. **Is the prompt a rotated-sorted-array problem?** Almost always: variant 1 with the "which half sorted?" branch.
4. **Does the prompt say "logarithmic time" or "O(log n) required"?** That is the interview-tell signal — binary search is one of two `O(log n)` patterns at this level (the other is balanced-tree-backed `bisect`).
5. **Does the prompt ask "find the smallest `k` such that …" or "minimize the maximum X" or "maximize the minimum Y"?** That is the *parametric* signal — covered in Lecture 2.
6. **Is there a monotone predicate hiding in the problem?** Even when no array is given, if you can write a `feasible(k)` boolean that is monotone, parametric search applies.

The 30-second decision tree:

```
sorted array (or cheaply sortable)?
├── No  ──→ is there a monotone predicate on an answer space?
│              ├── Yes ──→ binary search on the answer (Lecture 2)
│              └── No  ──→ not binary search; pick another pattern
└── Yes
    ├── "is target present / find index of"?       ──→ variant 1 (classic)
    ├── "first / leftmost / lower bound"?           ──→ variant 2 (half-open)
    ├── "last / rightmost / upper bound"?           ──→ variant 3 (round-up)
    ├── "rotated sorted array"?                     ──→ variant 1 + "which half sorted?"
    └── "smallest k such that predicate is True"?   ──→ variant 4 (parametric on indices)
```

```mermaid
flowchart TD
  A["Sorted array or cheaply sortable"] -->|No| B["Monotone predicate on an answer space"]
  B -->|Yes| C["Binary search on the answer Lecture 2"]
  B -->|No| D["Not binary search"]
  A -->|Yes| E["What does the prompt ask"]
  E -->|"Find index of target"| F["Variant 1 classic"]
  E -->|"First or leftmost"| G["Variant 2 half-open"]
  E -->|"Last or rightmost"| H["Variant 3 round-up"]
  E -->|"Rotated sorted array"| I["Variant 1 plus which half sorted"]
  E -->|"Smallest k with predicate true"| J["Variant 4 parametric"]
```
*Reading the prompt routes you to one of the four variants, or off the binary-search path entirely.*

This decision tree is what we want in muscle memory by Sunday.

---

## 15. The boundary-defense sentence

In Mock #2 (Week 9), you will get a binary-search problem. The interview tell is not whether you can write the loop — most candidates can fake it. The tell is whether you can **defend your boundary convention in one sentence, on demand**.

> "I picked the **closed-interval** convention `[lo, hi]` with `lo <= hi` because the search space is closed on both sides — every integer in the interval is a real candidate. The shrink rules `lo = mid + 1` and `hi = mid - 1` both exclude `mid` (which we just tested), so the loop strictly progresses and terminates when `lo > hi`. I could have used the half-open `[lo, hi)` with `lo < hi` — it works too — but I find the closed convention's invariant easier to state out loud."

That is the cadence interviewers want. Memorize the shape, plug in the names. The cadence carries across all four variants.

---

## Further reading

- **Wikipedia — Binary search algorithm**: <https://en.wikipedia.org/wiki/Binary_search_algorithm> — the formal treatment. Read the Variations section.
- **Joshua Bloch — "Nearly all binary searches are broken"**: <https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/> — five minutes; permanent takeaway.
- **A judge to run against.** If you want a scoreboard once the drills are done, any practice archive holds hundreds of instances of the classic family. Expect their contracts to differ from ours — most return `-1`, guarantee a solution exists, or skip the empty case entirely — so do the drills first, and read each outside contract from scratch rather than assuming it matches one you have already solved here.

Next: [Lecture 2 — Binary Search on the Answer](./02-binary-search-on-the-answer.md).
