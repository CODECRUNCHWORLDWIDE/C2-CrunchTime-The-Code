# Lecture 3 — Arrays and Two Pointers

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a two-pointer problem within 30 seconds, name the three sub-shapes of the pattern, and apply each to canonical problems.

The two-pointer pattern is the cleanest, geometrically obvious pattern to learn first — and it's the one many interviewers reach for to warm up a candidate. By Sunday you should be able to spot it instantly.

---

## 1. What "two pointers" means

Two pointers is exactly what it sounds like: you have **two indices** moving through a sequence (usually an array or string), and the algorithm is defined by **how the pointers move relative to each other.**

There are three common sub-shapes:

| Sub-shape | Pointer setup | Use case |
|-----------|---------------|----------|
| **Converging** | Left at `0`, right at `n-1`; move toward each other | Sorted array, find a pair |
| **Same-direction** | Both start at `0`; one races ahead, one lags | In-place mutation, partitioning |
| **Two-input** | One pointer per array | Merge-like operations |

Most interview problems use one of these three. We'll see all three this week.

The key insight: the **two-pointer pattern replaces a nested loop with a linear scan.** That's where the time saving comes from. A naïve O(n²) double-loop becomes O(n).

---

## 2. Sub-shape 1: Converging pointers

This is the most common. Setup:

```
left → ────────────────────────── ← right
   ↓                                  ↓
arr[0]  arr[1]  arr[2]  ...  arr[n-2]  arr[n-1]
```

You move `left` forward or `right` backward based on some condition. The loop ends when they meet or cross.

### Canonical problem: Two Sum II (sorted)

(We worked this in detail in Lecture 2. Recap:)

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
```

**Recognition signals for converging pointers:**

- Input is **sorted** (or can cheaply be sorted).
- You're looking for a **pair** (or sometimes a triple).
- The problem involves a **target sum / target product / target difference** between two elements.
- Naïve solution is `O(n²)` with two nested loops.

When you see all four signals, jump straight to converging two-pointer.

### Variants to recognize

- **Reverse a string in place.** `left=0, right=n-1`, swap, advance both, stop when they meet. O(n)/O(1).
- **Valid palindrome.** Same setup; compare instead of swap; return False if any mismatch.
- **Container with most water.** Same setup; track the maximum area as pointers converge.
- **3-Sum.** Pin one element, then run converging two-pointer on the remainder. O(n²)/O(1) — better than the O(n³) naïve.

---

## 3. Sub-shape 2: Same-direction (fast & slow, or read/write)

Setup:

```
write ↓                          read ↓
[arr[0]  arr[1]  arr[2]  ...  arr[k]  arr[k+1]  arr[k+2] ...]
```

Both start at the beginning. One races ahead (the "read pointer"); the other lags (the "write pointer"). You use this to **partition** or **filter** an array in place.

### Canonical problem: Remove duplicates from sorted array (in place)

```python
def remove_duplicates(nums: list[int]) -> int:
    """Modify nums in place; return the new length."""
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

The `read` pointer scans through every element. The `write` pointer only advances when we find a new unique element. Result: O(n) time, O(1) space, in-place.

**Recognition signals for same-direction pointers:**

- You're asked to **modify the array in place** ("do not allocate a new array").
- You need to **filter, partition, or compact** the array.
- O(n) time with O(1) extra space is the implied target.

### Variants to recognize

- **Move zeros to end.** `read` scans; `write` keeps the next non-zero position.
- **Sort colors (Dutch national flag).** Three pointers: low/mid/high. Variant with three pointers because you partition into three classes.
- **Linked list cycle detection (Floyd's tortoise and hare).** A fast-slow variant where one pointer moves 2× the other. We cover this in Week 4.

---

## 4. Sub-shape 3: Two-input pointers

Setup: two arrays, two pointers, one per array.

```
arr_a:  [a₀  a₁  a₂  ...  a_m]
          ↑i

arr_b:  [b₀  b₁  b₂  ...  b_n]
          ↑j
```

You advance `i` or `j` based on which array contributes the next element.

### Canonical problem: Merge two sorted arrays

```python
def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    # Append remaining
    result.extend(a[i:])
    result.extend(b[j:])
    return result
```

O(m + n) time, O(m + n) space (the result). The "in place" variant (LeetCode 88) is a classic interview question that uses two-input pointers with a third write-pointer on the result.

**Recognition signals for two-input pointers:**

- **Two inputs**, both sequences.
- Both are usually **sorted** (or the algorithm produces a sorted output).
- The naïve "concatenate and sort" is `O((m+n) log(m+n))`; two-pointer merge is `O(m+n)`.

---

## 5. Recognizing the pattern in <30 seconds

A useful exercise: read each of these one-line prompts and decide which sub-shape applies. Try before reading the answer.

1. "Given a sorted array and a target, return indices summing to target."
2. "Modify the array in place so all zeros are at the end."
3. "Determine whether a string is a palindrome."
4. "Find the longest substring without repeating characters."
5. "Merge two sorted arrays into one."
6. "Given an array, find three numbers summing to zero."

Answers:

1. **Converging.** Sorted + pair + target — textbook.
2. **Same-direction.** In place + filter — write/read pointers.
3. **Converging.** Compare from both ends, move inward.
4. **NOT two-pointer.** This is sliding window — we cover it Week 3. Don't force the pattern; the wrong fit is a worse trap than no fit.
5. **Two-input.** Two arrays, both sorted.
6. **Converging (with a pin).** Sort, then for each element pin it and run converging pointers on the remainder.

Note #4 — sometimes a problem *looks* like two-pointer but is sliding window. Sliding window also uses two indices, but they move *only* in one direction and define a *window* between them. Two-pointer can move either pointer in either direction (converging) or use the pointers to *partition* (same-direction).

Don't panic about the distinction yet — by Week 4 it'll be obvious.

---

## 6. Common bugs in two-pointer code

- **Off-by-one in the loop condition.** `while left <= right` vs `while left < right`. Which is right depends on whether you want to *include* the case when they overlap. Most converging pointer problems want `<`.
- **Forgetting to advance a pointer.** You handled the equal case and returned, but on the not-equal case you didn't advance — infinite loop.
- **Advancing the wrong pointer.** When the sum is too small, you advance `right` instead of `left`. Compiles fine; wrong answer. Trace on paper to catch this.
- **Mutating the array while reading it** in the same-direction variant. Use the `write < read` invariant — the `write` pointer can only point at positions already passed by `read`, so we can safely overwrite.
- **Edge case: empty array.** Most two-pointer code blows up on `len(arr) == 0` because `right = -1`, then `left < right` is False immediately and you skip the loop — that's *correct behavior* but only by luck. Add an explicit early return when the answer depends on having ≥2 elements.

---

## 7. The "I'll just use a hash map" temptation

For many two-pointer problems, a hash map gives the same time complexity (`O(n)`) but uses `O(n)` extra space. **You will be tempted to reach for the hash map by default** because it's familiar from C1.

When to prefer two-pointer:

- The input is already sorted (no extra cost to "do it the proper way").
- The problem says "do it in O(1) extra space."
- The interviewer asks "can you improve the space complexity?" after your hash-map answer.

When to prefer hash map:

- The input is unsorted *and* sorting first would change the complexity to `O(n log n)`.
- Indices matter and sorting would scramble them.
- You need to recover not just whether a pair exists but multiple pairs / unique pairs.

In Week 2 we'll go deep on hash maps. For Week 1, prefer two-pointer when the sorted property is available — that's the pattern recognition we're training.

---

## 8. Worked example: Valid Palindrome (with case + non-alphanumeric stripping)

A common Week-1 problem because it exercises both converging pointers *and* string preprocessing decisions.

**Problem.** Given a string `s`, return `True` if it is a palindrome considering only alphanumeric characters, ignoring case.

**UMPIRE compressed:**

- **U:** Input is a string with arbitrary characters. We compare only letters and digits, lowercase. Empty string and single character are palindromes.
- **M:** Two-pointer converging. Skip non-alphanumeric on each side.
- **P:** Two pointers left=0, right=n-1. Loop while left<right. Skip non-alphanumeric on left. Skip on right. Compare lowercase. If mismatch, False. If match, advance both. After loop, True.
- **I:**

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

- **R:** Trace `"A man, a plan, a canal: Panama"`:
  - left=0 (A), right=29 (a). Match. l=1, r=28.
  - left=1 ( ), skip to letter. left=2 (m). right=28 (m). Match. l=3, r=27.
  - … keep going. All match. Return True. ✓
  - Trace `"race a car"`: r-a-c-e-a-c-a-r. r/r, a/a, c/c, e/c — mismatch. Return False. ✓
- **E:** **O(n)** time (each character visited at most twice). **O(1)** space (just two integer pointers).

Notice the **nested inner whiles** for skipping non-alphanumeric. They are a common stumble — make sure each has its own `left < right` guard or you'll walk off the end of the string.

---

## 9. Self-check

- Name the three sub-shapes of two-pointer.
- For each, name a canonical problem and the time / space complexity.
- What's the difference between same-direction two-pointer and sliding window?
- Why is two-pointer often preferred over hash maps when the input is sorted?
- Trace `[1, 3, 4, 5, 7]` with target 11 through your two-sum-sorted function. (Answer: returns `[2, 3]`.)

---

## 10. Up next

The [exercises](../exercises/README.md) for this week are five UMPIRE drills, each a two-pointer problem of increasing difficulty. Work them in order. Don't skim solutions online — the point isn't to know the answer, it's to drill the method.

After exercises: the [quiz](../quiz.md), the [homework](../homework.md), and the [mini-project](../mini-project/README.md) (set up your portfolio repo).
