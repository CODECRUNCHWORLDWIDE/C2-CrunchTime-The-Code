# Week 12 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Subsets (LC 78)

### Understand

We have a list of distinct integers `nums` and we want to return every subset (the power set). There are exactly `2^n` subsets of an `n`-element input — including the empty subset and the full input. The output order is unconstrained; the order of elements within each subset is unconstrained.

Hand-walk on `nums = [1, 2]`:

```
Subsets of [1, 2]:
  []          (the empty subset)
  [1]         (just the first element)
  [2]         (just the second element)
  [1, 2]      (both)
Count: 4 = 2^2
```

### Match

Combinatorial enumeration. The 30-second memo:

> *Power-set enumeration. State = (start_index, path). At each level, choose which next element from the remaining tail to include. Every node — not just leaves — is a valid subset, so record at every node. Time O(2^n * n) for the deep-copy at each of 2^n nodes; space O(n) for the recursion stack and path. Trade vs. bit-enumeration (iterate mask from 0 to 2^n - 1 and read bits): same asymptotic, but the backtracking form generalizes to subsets II (deduplication) and combination sum (sum-based prune), which the bit-enumeration form does not.*

### Plan

1. Initialize `result = []` and `path = []`.
2. Define `backtrack(start)`:
   - Record `path[:]` to `result`.
   - For `i` from `start` to `len(nums) - 1`:
     - Append `nums[i]` to `path`.
     - Recurse with `backtrack(i + 1)`.
     - Pop `path`.
3. Call `backtrack(0)`.
4. Return `result`.

### Implement

```python
from __future__ import annotations

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """Return all 2^n subsets of nums in any order."""
    result: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result
```

### Review

Trace `nums = [1, 2]`:

```
backtrack(0): record []
  i=0: path=[1]; backtrack(1)
    record [1]
    i=1: path=[1,2]; backtrack(2)
      record [1,2]
      (loop empty: start=2 == len)
    pop -> [1]
  pop -> []
  i=1: path=[2]; backtrack(2)
    record [2]
  pop -> []

result = [[], [1], [1, 2], [2]]
```

Four subsets — `2^2` confirmed. Matches the hand-enumeration.

### Evaluate

- **Time:** `O(2^n * n)`. There are `2^n` subsets; each `result.append(path[:])` is `O(n)` for the deep-copy.
- **Space:** `O(n)` for the recursion stack and the `path` list (excluding the output, which is `O(2^n * n)`).
- **Trade-off:** vs. iterative bit-enumeration `for mask in range(2**n): subset = [nums[i] for i in range(n) if mask & (1 << i)]` — same asymptotic, but the backtracking form is the template for subsets II and combination sum. The bit-enumeration form does not generalize.

---

## Solution 2 — Permutations (LC 46)

### Understand

We have a list of distinct integers `nums` and we want to return every permutation (every ordering of every element). There are exactly `n!` permutations of an `n`-element input. The output order is unconstrained.

Hand-walk on `nums = [1, 2, 3]`:

```
Permutations of [1, 2, 3]:
  [1, 2, 3], [1, 3, 2]      (starting with 1)
  [2, 1, 3], [2, 3, 1]      (starting with 2)
  [3, 1, 2], [3, 2, 1]      (starting with 3)
Count: 6 = 3!
```

### Match

Combinatorial enumeration where order matters. The 30-second memo:

> *Permutation enumeration. State = (used_set, path). At each level, iterate every index; skip indices already in `used`; choose, recurse, unchoose both `used` and `path`. Record at leaves only (len(path) == n). Time O(n! * n) — n! permutations, each O(n) for the deep-copy. Space O(n) for the recursion stack plus the used set. Trade vs. itertools.permutations: same asymptotic, but the backtracking form generalizes to permutations II (deduplication) and N-Queens (constraint propagation), which the library form does not.*

### Plan

1. Initialize `result = []`, `path = []`, `used = set()`.
2. Define `backtrack()`:
   - If `len(path) == len(nums)`: record `path[:]`, return.
   - For `i` from `0` to `len(nums) - 1`:
     - If `i` in `used`: continue.
     - Add `i` to `used`, append `nums[i]` to `path`.
     - Recurse.
     - Pop `path`, remove `i` from `used`.
3. Call `backtrack()`.
4. Return `result`.

### Implement

```python
from __future__ import annotations

from typing import List, Set


def permute(nums: List[int]) -> List[List[int]]:
    """Return all n! permutations of nums."""
    result: List[List[int]] = []
    path: List[int] = []
    used: Set[int] = set()

    def backtrack() -> None:
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if i in used:
                continue
            used.add(i)
            path.append(nums[i])
            backtrack()
            path.pop()
            used.remove(i)

    backtrack()
    return result
```

### Review

Trace `nums = [1, 2]`:

```
backtrack(): path=[], used={}
  i=0: used={0}, path=[1]; backtrack()
    i=0: in used, skip
    i=1: used={0,1}, path=[1,2]; backtrack()
      len==2: record [1,2]
    pop, remove -> used={0}, path=[1]
  pop, remove -> path=[], used={}
  i=1: used={1}, path=[2]; backtrack()
    i=0: used={0,1}, path=[2,1]; backtrack()
      len==2: record [2,1]
    pop, remove
  pop, remove

result = [[1, 2], [2, 1]]
```

Two permutations — `2!` confirmed. Matches the hand-enumeration.

### Evaluate

- **Time:** `O(n! * n)`. `n!` permutations; each `result.append(path[:])` is `O(n)`.
- **Space:** `O(n)` for the recursion stack, the `path` list, and the `used` set.
- **Trade-off:** vs. `list(itertools.permutations(nums))` — equivalent in output (returns tuples; would need to convert to lists); the standard-library form is faster in practice. The backtracking form is the template that extends to LC 47 (permutations with duplicates) and N-Queens.

---

## Solution 3 — Combination Sum (LC 39)

### Understand

We have a list of distinct positive integers `candidates` and a positive integer `target`. We want every multiset (with repetition) of candidates summing to `target`. Two multisets are the same if they contain the same elements with the same frequencies; order does not matter.

Hand-walk on `candidates = [2, 3, 6, 7], target = 7`:

```
Combinations summing to 7:
  [2, 2, 3]   (2 + 2 + 3 = 7)
  [7]         (7 = 7)
Count: 2
```

### Match

Backtracking with reuse and sum-based pruning. The 30-second memo:

> *Multiset enumeration with sum constraint. State = (start_index, remaining_target, path). Reuse means recurse with start = i (not i + 1); the index-non-decreasing discipline prevents duplicate orderings. Sort candidates first; break the inner loop when candidates[i] > remaining. Record path[:] when remaining == 0. Time: loose worst case O(N^(target/min_candidate)); the sort + break cuts this drastically. Space O(target/min_candidate) for the recursion stack and path. Trade vs. unbounded knapsack DP (counting): DP counts the number of multisets but cannot enumerate them; backtracking is the only path when the prompt asks for the multisets themselves.*

### Plan

1. Sort `candidates` ascending. The prune depends on monotonicity.
2. Initialize `result = []` and `path = []`.
3. Define `backtrack(start, remaining)`:
   - If `remaining == 0`: record `path[:]`, return.
   - For `i` from `start` to `len(candidates) - 1`:
     - If `candidates[i] > remaining`: break.
     - Append `candidates[i]` to `path`.
     - Recurse with `backtrack(i, remaining - candidates[i])`.
     - Pop `path`.
4. Call `backtrack(0, target)`.
5. Return `result`.

### Implement

```python
from __future__ import annotations

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Return all combinations of candidates summing to target (reuse allowed)."""
    candidates.sort()
    result: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])    # reuse: i, not i + 1
            path.pop()

    backtrack(0, target)
    return result
```

### Review

Trace `candidates = [2, 3, 6, 7]` (already sorted), `target = 7`:

```
backtrack(0, 7):
  i=0 (2): path=[2]; backtrack(0, 5)
    i=0 (2): path=[2,2]; backtrack(0, 3)
      i=0 (2): path=[2,2,2]; backtrack(0, 1)
        i=0 (2): 2 > 1, break        # PRUNED
      pop -> [2,2]
      i=1 (3): path=[2,2,3]; backtrack(1, 0); record [2,2,3]
      pop -> [2,2]
      i=2 (6): 6 > 3, break          # PRUNED
    pop -> [2]
    i=1 (3): path=[2,3]; backtrack(1, 2)
      i=1 (3): 3 > 2, break          # PRUNED
    pop -> [2]
    i=2 (6): 6 > 5, break             # PRUNED
  pop -> []
  i=1 (3): path=[3]; backtrack(1, 4)
    i=1 (3): path=[3,3]; backtrack(1, 1)
      i=1 (3): 3 > 1, break           # PRUNED
    pop -> [3]
    i=2 (6): 6 > 4, break             # PRUNED
  pop -> []
  i=2 (6): path=[6]; backtrack(2, 1)
    i=2 (6): 6 > 1, break             # PRUNED
  pop -> []
  i=3 (7): path=[7]; backtrack(3, 0); record [7]
  pop -> []

result = [[2, 2, 3], [7]]
```

Two combinations confirmed. The prune (`break` on `candidates[i] > remaining`) eliminates the dead-end branches without recursing into them — without the prune, every dead end would consume a function call.

### Evaluate

- **Time:** `O(N^(target/min_candidate))` loose worst case — the recursion depth is bounded by `target / min_candidate`, and each level has up to `N` children. Tighter bounds depend on the specific inputs; the sort plus break is the constant-factor improvement that makes the algorithm pass LC time limits.
- **Space:** `O(target / min_candidate)` for the recursion stack and `path` (excluding the output).
- **Trade-off:** vs. unbounded knapsack DP — DP counts the number of multisets summing to target in `O(N * target)` time but cannot enumerate them. Backtracking is the only path when the prompt asks for the multisets themselves. vs. the naive recursion without sort and break — same correctness but explores `O(target / min)` more dead-end calls per branch.

---

## Closing — common bugs and how to avoid them

Across all three exercises:

1. **Forgetting the deep-copy at the leaf.** `result.append(path)` appends the *same* list every time; after the final unchoose, every entry in `result` is the empty list. Always use `result.append(path[:])` (or `list(path)`).
2. **Off-by-one on the `start` parameter.** Subsets uses `start = i + 1` (no reuse); combination sum uses `start = i` (reuse allowed); permutations uses no `start` (just `used`). Mixing these up produces duplicates or missing solutions.
3. **Forgetting to sort before applying the sum-based prune.** Combination sum without `candidates.sort()` cannot use `break` — the loop must continue past values larger than `remaining` (because later values might be smaller). The two-line change (sort plus break) is the senior signal.
4. **Two unchoose steps in the wrong order.** Permutations requires two state mutations on choose (`used.add(i)`, `path.append(nums[i])`); the unchoose must mirror them. Forgetting one of the two leaves the state corrupted.
5. **Recording at the wrong place.** Subsets records at *every node* (`result.append(path[:])` at the top of `backtrack`); permutations and combinations record at *leaves only* (`if len(path) == ...: result.append(path[:]); return`). The recording rule is the discriminator; getting it wrong silently produces the wrong output.

After this set of three, the pattern recognition for any standard backtracking should be reflexive. The week's mini-project (palindrome partitioning + sudoku solver) is the proof.

Move on to the [quiz](../quiz.md), then the [homework](../homework.md), then the [mini-project](../mini-project/README.md).
