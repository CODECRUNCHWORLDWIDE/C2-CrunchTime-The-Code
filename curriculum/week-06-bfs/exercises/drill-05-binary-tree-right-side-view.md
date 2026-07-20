# Drill 5 — Binary Tree Right Side View

> **Pattern:** Node-BFS on a tree — level-tracking with "last node per level" emit
> **Difficulty:** Medium
> **Target solve time:** 20 minutes (with full UMPIRE narration)
> **Why fifth and last:** the cleanest exercise of *level-tracking with a per-level operation*. After Drill 1 (level order: emit all nodes per level) and Drill 4 (word ladder: emit when level matches), this drill emits the *last node* at each level. The pattern transfers directly to "leftmost at each level," "average per level," "max per level" — a family of LC variants you will see in homework.

## Problem statement

Given the root of a binary tree, imagine yourself standing on the **right side** of the tree. Return the values of the nodes you can see, **ordered from top to bottom**.

You see one node per depth: the rightmost node at that depth.

**Examples:**

- `root = [1, 2, 3, null, 5, null, 4]` → `[1, 3, 4]`
- `root = [1, null, 3]` → `[1, 3]`
- `root = []` → `[]`
- `root = [1, 2, 3, 4]` → `[1, 3, 4]` (depth 0: 1, depth 1: 3, depth 2: 4; depth 2 has only one node, which is the rightmost)

The tree node class:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm "right side view" = the rightmost node at each depth. Confirm a node with no right sibling but the rightmost-at-its-depth is still visible (it is). Confirm empty tree → `[]`. Walk an example: `[1, 2, 3, null, 5, null, 4]`. Depth 0: just node 1. Depth 1: nodes 2 and 3, rightmost is 3. Depth 2: nodes 5 and 4; rightmost is 4. Answer: `[1, 3, 4]`.
- [ ] **M:** Node-BFS on a tree with level tracking. The 30-second memo: *"BFS with the level-tracking idiom — outer `for _ in range(len(queue))` consumes exactly one level; emit the last value dequeued at each level. This is variant 'one per level' of the level-tracking idiom, distinct from Drill 1's 'all per level.' Why BFS over DFS: BFS naturally exposes level boundaries; DFS would need to maintain a 'max depth seen so far' to detect 'first time at this depth from the right' — works but more bookkeeping."*
- [ ] **P:** Initialize: if root is None, return []. Queue = `deque([root])`. Result = `[]`. Loop: while queue, snapshot `len(queue)`. Iterate `len` times: dequeue node, enqueue its non-`None` left and right children, on the **last** iteration of this level (the `i == len - 1` check) append node.val to result. Return result.
- [ ] **I:** Write the code, narrating each line. Two equivalent shapes: (a) check `i == len - 1` inside the inner loop, append at that iteration; (b) after the inner loop, append the value of the last node visited. Both work. Speak the level-tracking invariant: *"The `range(len(queue))` snapshot is taken before any children are enqueued; the inner loop processes exactly this level's nodes."*
- [ ] **R:** Trace on `[1, 2, 3, null, 5, null, 4]`. Queue=[1], result=[]. Iter 1: snapshot len=1. Dequeue 1 (last at level), enqueue 2, 3. Append 1 to result. Result=[1]. Iter 2: snapshot len=2. Dequeue 2, enqueue 5. Dequeue 3 (last), enqueue 4. Append 3. Result=[1, 3]. Iter 3: snapshot len=2. Dequeue 5. Dequeue 4 (last). Append 4. Result=[1, 3, 4]. Iter 4: queue empty. Return [1, 3, 4]. ✓
- [ ] **E:** **Time `O(N)`** — every node enqueued and dequeued once. **Space `O(W)`** where `W` is max tree width; worst case `W = N/2` for a complete binary tree. Tradeoff: DFS preorder-right-first (visit root, recurse right, recurse left, append first-seen at each depth) is `O(N)`/`O(H)` — for a balanced tree, smaller space. BFS is more natural for level-aware operations because the level boundary is explicit in the loop structure.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `right_side_view`.
- UMPIRE write-up at `umpire-writeups/c2-week-06/drill-05-binary-tree-right-side-view.md`.
- Your Match section names the **level-tracking idiom** and the **"one per level" variant** explicitly.
- Your Match section explicitly compares against the DFS alternative (preorder-right-first with "first seen at this depth").
- Your Implement section uses the `range(len(queue))` snapshot.
- Your Evaluate section states the **`O(N) / O(W)` defense sentence**.
- Recording **≥ 12 minutes**.

## Function signature (for the runner)

```python
def right_side_view(root) -> list[int]:
    """Return list of rightmost-at-each-depth values, top to bottom."""
    ...
```

## Common bugs you should catch in Review

- **Forgetting the `range(len(queue))` snapshot.** Iterating `for node in queue` while enqueuing into the same queue is a Python anti-pattern (deque does not error on it but the semantics are unclear). The snapshot freezes "this level" before children are added.
- **Appending the wrong "last."** The rightmost-at-level is the **last dequeued**, not the rightmost-child-of-the-rightmost-parent. They are the same in a complete tree but differ for skewed trees: `[1, 2, null, 4]` has the right side view `[1, 2, 4]` even though node 2 has no right child — node 4 is the rightmost at depth 2.
- **Enqueuing right before left.** Either order works for *right* side view as long as you emit the **last** dequeued. Most clean implementations enqueue left then right (consistent with reading order), and emit the `i == len - 1` node.
- **Returning `None` for empty tree.** Return `[]`. None is wrong by spec.
- **Computing max depth first, then doing a second pass.** Works but two passes is `O(N) + O(N) = O(N)` — same asymptotic but uglier. One pass with the level-tracking idiom is cleaner.

## Self-feedback template

1. Did you state **"node-BFS on a tree with level tracking"** in Match?
2. Did you describe the **"one per level" variant** explicitly?
3. Did you compare against DFS in the Match section?
4. Did you use the `range(len(queue))` snapshot?

## What to commit

```
umpire-writeups/c2-week-06/
├── drill-05-binary-tree-right-side-view.md
└── drill_05_solution.py
```

When done, push and move on to [the challenge](../challenges/challenge-01-minimum-knight-moves.md).

This concludes the five drills. The level-tracking idiom you just practiced — *outer loop is the level, inner loop is the level's nodes* — generalizes to the entire family of "one X per level" problems: leftmost, rightmost, max, min, average, sum, count. Eight LeetCode variants, one template.
