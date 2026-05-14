# Drill 1 — Binary Tree Level Order Traversal

> **Pattern:** Node-BFS on a tree — level-tracking idiom
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (with full UMPIRE narration)
> **Why first:** the cleanest possible exercise of the level-tracking idiom. A tree has no cycles, so the visited-set discipline is relaxed (no node is ever its own ancestor), but the outer `for _ in range(len(queue))` loop is the same shape you will use in every Phase 2 BFS problem.

## Problem statement

Given the root of a binary tree, return its **level-order traversal**: a list of lists, where the `i`-th inner list contains the values of the nodes at depth `i` (the root is at depth 0).

**Examples:**

- `root = [3, 9, 20, null, null, 15, 7]` → `[[3], [9, 20], [15, 7]]`
- `root = [1]` → `[[1]]`
- `root = []` → `[]`
- `root = [1, 2, 3, 4, 5, 6, 7]` → `[[1], [2, 3], [4, 5, 6, 7]]`

The tree node class:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm depth 0 = root. Confirm null root returns `[]`. Confirm output is list-of-lists, one inner list per depth.
- [ ] **M:** Node-BFS on a tree with the level-tracking idiom. The 30-second memo: *"BFS on a tree — every node is visited exactly once because a tree has no cycles, so the visited set is implicit (`None` children are filtered at enqueue time, no node is revisited). Level-tracking idiom: outer `for _ in range(len(queue))` consumes exactly one level per outer iteration. Auxiliary state: `deque` queue, output list. Why not DFS: DFS gives a pre/in/post-order traversal, not level order. Why not store `(node, depth)` tuples: level tracking is cleaner here because the output is grouped by level."*
- [ ] **P:** Initialize: `if root is None, return []`. Queue = `deque([root])`. Output = `[]`. Loop: while queue is non-empty, snapshot `len(queue)` and consume that many nodes into a new `level` list. For each node, append non-`None` left and right to the queue. Append `level` to output. Return output.
- [ ] **I:** Write the code. Speak the invariant: *"Every node enters the queue exactly once because trees have no cycles. The outer for-loop's `range(len(queue))` snapshot freezes the size of this level before the next level's nodes are enqueued."*
- [ ] **R:** Trace on `[3, 9, 20, null, null, 15, 7]`. queue=[3]. Iter 1: snapshot len=1. Dequeue 3, level=[3], enqueue 9, 20. Output=[[3]]. Iter 2: snapshot len=2. Dequeue 9, level=[9], (no children). Dequeue 20, level=[9, 20], enqueue 15, 7. Output=[[3], [9, 20]]. Iter 3: snapshot len=2. Dequeue 15, level=[15]. Dequeue 7, level=[15, 7]. Output=[[3], [9, 20], [15, 7]]. Iter 4: queue empty. Return. ✓ Edge: root=None → return [].
- [ ] **E:** **Time `O(N)`** where `N` = number of nodes — each node enqueued and dequeued once, constant work per node. **Space `O(W)`** where `W` is the max width of the tree — the queue holds at most one level. Worst-case `W = N/2` (a complete binary tree's last level). Tradeoff: DFS pre-order is `O(N)`/`O(H)` where `H` is height; for a balanced tree `H = log N`, smaller than `W = N/2`. BFS uses more space but produces the level-order output directly.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `level_order`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-06/drill-01-level-order.md` in your portfolio repo.
- Your Match section names the **level-tracking idiom** explicitly and justifies why the `range(len(queue))` snapshot works.
- Your Implement section uses `collections.deque` (not `list`) for the queue.
- Your Evaluate section states the **`O(N)` time / `O(W)` space defense sentence**.
- Recording **≥ 10 minutes.** If you finished in 4 minutes, you skipped Match or Evaluate. Re-do it.

## Function signature (for the runner)

```python
def level_order(root) -> list[list[int]]:
    """Return level-order traversal of binary tree rooted at `root`."""
    ...
```

## Common bugs you should catch in Review

- **Using `list.pop(0)` instead of `deque.popleft()`.** `pop(0)` is `O(N)` per call; total `O(N²)`. Use `deque`.
- **Forgetting to snapshot `len(queue)`.** Writing `while queue:` and dequeuing one at a time, then increment a counter — works but does not give level-grouped output. The `for _ in range(len(queue))` snapshot is what makes the inner loop a single level.
- **Enqueuing `None` children.** Always check `if node.left is not None` and `if node.right is not None` before enqueuing. Enqueuing `None` and then dequeuing it later causes an `AttributeError` on `.left` / `.right`.
- **Not handling root = None.** Return `[]` immediately. Otherwise the loop body runs once with `root` being `None` and crashes.
- **Using a visited set.** A tree has no cycles by definition; the visited set is unnecessary. Adding it is not wrong (it just costs an extra `O(N)` set), but stating "I'm using a visited set" on a tree problem is a tell that you do not recognize tree structure.

## Self-feedback template

After you finish, listen to your recording at 1.5×:

1. Did you state the **level-tracking idiom** before writing the code?
2. Did you justify why a tree does not need an explicit visited set?
3. Did you use `deque` (not `list`) for the queue?

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    └── c2-week-06/
        ├── drill-01-level-order.md           # write-up
        └── drill_01_solution.py               # your solution
```

When done, push and move on to [Drill 2](drill-02-shortest-path-grid.md).
