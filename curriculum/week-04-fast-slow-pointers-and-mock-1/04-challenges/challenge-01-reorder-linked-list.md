# Challenge 1 — Reorder Linked List (LeetCode 143)

> **Pattern:** Fast/slow midpoint **+** linked-list reversal **+** two-list merge — three sub-patterns in one problem
> **Difficulty:** Medium-Hard
> **Target solve time:** 60 minutes
> **Why hard:** correctness depends on three independent sub-procedures, each easy on its own. The interview tell is decomposing the problem into the three sub-steps *before* writing any code — and naming each sub-step's pattern out loud.

## Problem statement

You are given the head of a singly-linked list. Reorder the list **in place** from

```
L0 → L1 → L2 → … → L(n-2) → L(n-1)
```

to

```
L0 → L(n-1) → L1 → L(n-2) → L2 → L(n-3) → …
```

You **must not** modify the node values. Only the `.next` pointers may change.

**Examples:**

- Input: `1 → 2 → 3 → 4` → Output: `1 → 4 → 2 → 3`
- Input: `1 → 2 → 3 → 4 → 5` → Output: `1 → 5 → 2 → 4 → 3`
- Input: `1 → 2` → Output: `1 → 2` (unchanged; only two nodes)
- Input: `1` → Output: `1` (unchanged)
- Input: `None` → Output: `None`

The function should mutate the list in place and may return `None`.

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is **O(n) time** and **O(1) extra space**. The temptation to materialize the list into a Python list — making it trivial to merge by index — produces an O(n)-space solution, which interviewers reject.
- [ ] Your UMPIRE write-up **explicitly decomposes** the problem into the three sub-steps in the Match section. Naming them is the interview tell.
- [ ] Your write-up handles the **even-length and odd-length midpoint cases** without bugs.
- [ ] Recording **≥ 30 minutes** — yes, half an hour. First time on this problem is long; that's the right shape.

## The decomposition (the interview tell)

The clean approach decomposes into three sub-steps:

1. **Find the middle.** Use Drill 3's algorithm — fast/slow with the speed-2 hare. After this step, the list is conceptually split into a "left half" (head to middle) and a "right half" (middle.next onward). For even length, slow lands on the upper middle; we want to *split between* slow and slow.next, so the left half ends at the lower middle and the right half starts at the upper middle.

2. **Reverse the right half.** Standard iterative reversal — three pointers (`prev`, `curr`, `next`). After this step, the right half points backwards, ending at what was the original tail.

3. **Merge the two halves.** Interleave: take one node from the left half, one from the (reversed) right half, and so on. The left half is at most 1 node longer than the right (for odd-length inputs).

```
Before: 1 → 2 → 3 → 4 → 5

Step 1 (find middle): slow = node 3
Step 1.5 (split): left = 1 → 2 → 3 → None; right = 4 → 5 → None
                  (cut at slow.next; set slow.next = None)
Step 2 (reverse right): right = 5 → 4 → None
Step 3 (merge): 1 → 5 → 2 → 4 → 3 → None
```

The discriminator: most candidates can write each sub-step in isolation. The interview-tell move is *announcing the decomposition before starting any code*. Say it out loud in Plan:

> "Three sub-steps. First, fast/slow midpoint — that's Drill 3 from this week. Second, in-place reversal of the right half — standard iterative reversal. Third, merge the two halves by interleaving. After saying this aloud, I'll write each sub-step as a helper, then compose them in `reorder_list`."

## UMPIRE outline

- **U:** Restate. Confirm "in place" — only `.next` pointers may change, values are immutable. Confirm O(1) extra space. Confirm the alternating pattern: L0, L(n-1), L1, L(n-2), .... Walk `1 → 2 → 3 → 4 → 5` by hand to confirm output is `1 → 5 → 2 → 4 → 3`.

- **M:** Three composed sub-patterns. The 30-second memo:
  > *"This is a composition of three sub-patterns. First, fast/slow midpoint finding (Drill 3 this week). Second, linked-list reversal — three-pointer iterative reverse. Third, two-list merge by interleaving. Auxiliary state: a constant number of pointers; no array, no stack, no set. The single-array short-circuit would be O(n) space and is therefore rejectable. The composition runs in O(n) time — each sub-step is O(n), and they run in sequence."*

- **P:** Implement three helpers, then compose:
  1. `_middle(head)` — returns the **upper middle** (slow lands here when fast hits the end). For splitting, we actually want the lower middle as the end of the left half — so we'll use `prev_slow` or split *after* slow appropriately. *Decide your convention before coding.*
  2. `_reverse(head)` — standard iterative reversal, returns new head.
  3. `_merge(a, b)` — interleave a-then-b nodes; `a` is the left half (possibly 1 longer than `b`).
  Then `reorder_list(head)`: handle edge cases (empty, single, two nodes — already correct), find middle, split, reverse right half, merge.

- **I:** Implement. Watch the split: `right_head = slow.next; slow.next = None`. Watch the merge: alternate `a.next`, `b.next`, advancing `a` and `b` each by one. Three traps in section "Common bugs" below.

- **R:** Trace on `1 → 2 → 3 → 4 → 5`. Middle: slow lands on 3. Split: left = `1 → 2 → 3`, right = `4 → 5`. Reverse right: right = `5 → 4`. Merge: `1 → 5 → 2 → 4 → 3`. ✓ Trace on `1 → 2 → 3 → 4`. Middle: slow lands on 3 (upper middle). Split: left = `1 → 2 → 3`, right = `4`. Hmm — left has 3 nodes, right has 1. Reverse right: still `4`. Merge: `1 → 4 → 2 → 3`. ✓

  Wait — but the spec for `1 → 2 → 3 → 4` expects `1 → 4 → 2 → 3`. Let me check the *upper middle* convention against the split. If slow is the upper middle (node 3 for length 4), we split `slow.next = None` after slow — which leaves left = `1 → 2 → 3` (3 nodes) and right = `4` (1 node). That's actually right.

  Cross-check with `1 → 2 → 3 → 4 → 5 → 6` (length 6). Upper middle is node 4. Split: left = `1 → 2 → 3 → 4` (4 nodes), right = `5 → 6` (2 nodes). Reverse right: `6 → 5`. Merge: `1 → 6 → 2 → 5 → 3 → 4`. ✓ Correct alternation.

- **E (graded):** **Time O(n)** — each sub-step is O(n); three sub-steps in sequence is 3·O(n) = O(n). **Space O(1)** — a constant number of pointers across all three sub-steps; no auxiliary array, no recursion stack (the helpers are iterative). Tradeoff: the O(n)-space alternative is "materialize to a Python list, then assemble by index" — easy to write but rejected by the spec. Why O(1) is possible: each sub-step is well-known O(1)-space; the composition preserves the bound. Best/avg/worst all O(n) — no input makes this faster or slower asymptotically.

## Function signature

```python
class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def reorder_list(head: ListNode | None) -> None:
    """Reorder the linked list in place. Mutates .next pointers; does not return.

    Reorders L0 -> L1 -> ... -> Ln-1 -> Ln  into
              L0 -> Ln -> L1 -> Ln-1 -> ...
    """
    ...
```

## Test cases to verify

```python
import pytest

def list_to_values(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out

def build_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    tail = head
    for v in values[1:]:
        tail.next = ListNode(v)
        tail = tail.next
    return head

@pytest.mark.parametrize("values, expected", [
    ([1, 2, 3, 4], [1, 4, 2, 3]),
    ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
    ([1, 2], [1, 2]),
    ([1], [1]),
    ([], []),
    ([1, 2, 3, 4, 5, 6], [1, 6, 2, 5, 3, 4]),
    ([1, 2, 3, 4, 5, 6, 7], [1, 7, 2, 6, 3, 5, 4]),
    ([10, 20, 30], [10, 30, 20]),
])
def test_reorder_list(values, expected):
    head = build_list(values)
    reorder_list(head)
    assert list_to_values(head) == expected
```

## Common bugs you should catch in Review

- **Forgetting to split.** After finding the middle, you must `slow.next = None` (cutting the left half's tail) *before* reversing the right half. Without the cut, the reverse will turn the *whole* list into a half-cycle and corrupt everything.
- **Wrong middle convention.** If you use the lower-middle variant (`fast.next.next` guard), the left half has one fewer node than the right for even-length inputs, and the merge alternation produces the wrong shape. Pick a convention and stick with it; trace at least two cases to confirm.
- **Off-by-one in the merge.** The merge loop ends when one half (usually the right, since left is the longer or equal half) hits None. The left's last node should point to None *or* to the right's last node — depends on the lengths. Trace carefully.
- **Modifying values instead of pointers.** The spec says values are immutable. Reordering by overwriting `val` fields is wrong, even if it produces the right output sequence.
- **Recursive reversal.** Recursion costs O(n) stack space and busts the O(1) bound. Use iterative reversal with three pointers.
- **Materializing to a Python list.** O(n) space, also rejected by the spec. The interview tell is doing this *in place*.

## The "why O(n) time, O(1) space?" defense

Out loud, in your Evaluate section:

> "**Why O(n) time, O(1) space.** Three sub-steps in sequence. Find middle: O(n) time, O(1) space — two pointers, single pass. Reverse: O(n) time, O(1) space — three pointers, single pass over the right half. Merge: O(n) time, O(1) space — interleaves the two halves with constant additional pointers. Each is independently O(n)/O(1); composition keeps the bound. The Python-list materialization shortcut would be O(n)/O(n) — same time, worse space, and the spec rejects it."

Memorize the shape of that sentence. Saying it cleanly is the difference between "solved Reorder List" and "demonstrated mastery of the composition skill."

## Why this matters

Reorder List is *the* canonical "compose three sub-patterns" problem. Real onsite interviews ask compositions like this constantly — not because they're algorithmically deep individually, but because they test whether you can *decompose a multi-step problem into named sub-procedures* before you start coding. That decomposition is the senior-engineer skill.

When you revisit Week 4 in the mastery pathway, or before a real interview, **re-derive each sub-step from scratch** rather than re-reading your old solution. The composition will feel automatic the second time. The first time it should not.

## Stretch

**Palindrome Linked List** (LeetCode 234) — same decomposition: find middle, reverse second half, then *compare* (instead of merge) the two halves. The structure is identical; the third sub-step is the only thing that changes. Try it after Reorder List — should take 20 minutes once Reorder is in muscle memory.

**Reverse Nodes in k-Group** (LeetCode 25) — a generalization of reversal. Out of scope for Week 4 but a known follow-up if Reorder felt easy.

---

This concludes Week 4's exercises and challenge. Take the [quiz](../05-quiz.md), do the [homework](../06-homework.md), then ship the [mini-project](../07-mini-project/00-overview.md) — Mock Interview #1.
