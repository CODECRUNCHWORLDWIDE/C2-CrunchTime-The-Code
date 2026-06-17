# Lecture 1 — Floyd's Tortoise and Hare

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a fast/slow-pointer problem within 30 seconds, write Floyd's cycle detection without notes, derive the cycle-entrance algorithm out loud, and pick the right midpoint convention from the prompt.

Three weeks of patterns now. Two-pointer (Week 1) walked two indices toward each other, or in the same direction at the same speed. Sliding window (Week 3) walked two indices in the same direction, never backwards, defining a contiguous region. This week introduces the third "two-index" family: **fast and slow pointers** — two indices moving in the same direction *at different speeds*. The speed difference is the entire algorithmic idea.

By the end of this lecture you should be able to read a problem and, within 30 seconds, say one of three things out loud: "fast/slow on a linked list," "fast/slow on a functional graph (integer sequence)," or "not fast/slow — here's why."

---

## 1. What "fast/slow pointers" means

A **fast pointer** advances *more than one step per iteration* — almost always **two**. A **slow pointer** advances *one step per iteration*. Both start at the same place (usually the head of a linked list). Both move in the same direction. They never go backwards.

Visualization on a 7-node linked list, no cycle:

```
nodes:  A → B → C → D → E → F → G → None

step 0:  s=A, f=A
step 1:  s=B, f=C
step 2:  s=C, f=E
step 3:  s=D, f=G
step 4:  s=E, f=None      ← fast hit the end. No cycle.
```

Visualization on a 7-node linked list with a cycle starting at C:

```
nodes:  A → B → C → D → E → F → G
                ↑                ↓
                └────────────────┘

step 0:  s=A, f=A
step 1:  s=B, f=C
step 2:  s=C, f=E
step 3:  s=D, f=G
step 4:  s=E, f=D    ← fast wrapped around the cycle
step 5:  s=F, f=F    ← they meet inside the cycle. Cycle confirmed.
```

The pattern's power comes from one observation:

> **If a cycle exists, fast and slow will collide inside it within `O(n)` steps. If no cycle, fast will reach the end of the list within `O(n/2)` steps.**

The fast pointer "laps" the slow one inside any cycle. That's the entire algorithm. The proof is in section 4.

---

## 2. Why this is *not* two-pointer (and not sliding window)

You now know three two-index patterns. They look similar at the line level. The discriminators:

| | Two-pointer converging | Sliding window | Fast/slow pointers |
|--|--|--|--|
| **Where do they start?** | One at each end | Both at the start | Both at the start |
| **Direction of motion** | Toward each other | Same direction, lockstep | Same direction, different speed |
| **What they represent** | Endpoints of a range that shrinks | Both ends of a contiguous window | Two checkpoints in the same traversal |
| **Why use it** | Sorted-array pair search, palindrome check | Compute over every contiguous slice | Detect a cycle, find a midpoint, find nth-from-end |
| **Termination** | When indices cross | When right hits the end | When fast meets slow (cycle) or fast hits None (no cycle) |
| **Underlying structure** | Array, string | Array, string | Linked list, functional graph (sometimes array) |

Quick test. Read these prompts. Two-pointer, sliding window, or fast/slow?

1. "Detect if a linked list has a cycle." → **Fast/slow.** Two checkpoints, different speeds, same traversal.
2. "Find the longest substring without repeating characters." → **Sliding window.** Already drilled in Week 3.
3. "Given a sorted array, find a pair summing to target." → **Two-pointer converging.** Indices move toward each other.
4. "Find the middle node of a linked list in one pass." → **Fast/slow.** Speed-2 hare lands on the middle when it reaches the end.
5. "Determine if `n` is a happy number." → **Fast/slow on a functional graph.** Not obviously a "linked list," but the same algorithm applies.

When in doubt, ask: *"are there two indices in the same direction moving at different speeds?"* If yes, fast/slow. If no, it's one of the other two patterns.

---

## 3. The minimal Floyd's algorithm — cycle detection

```python
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

def has_cycle(head: ListNode | None) -> bool:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

Six lines. Memorize the shape.

Four observations:

1. **The loop guard is `fast and fast.next`.** Both must be non-None *before* you advance fast two steps. Forgetting `fast.next` is the #1 bug — it crashes on null-tail lists.
2. **Advance, *then* compare.** If you compare before advancing, the loop body never gets to assert "cycle found" because slow and fast both start at `head`.
3. **Identity, not equality.** Use `slow is fast` (Python `is`), not `slow == fast`. Two distinct nodes might have the same `val` but they are not the same node. Identity comparison is correct.
4. **No auxiliary data structure.** No `set` of visited nodes. This is the algorithm's claim to fame — `O(1)` space. The naive cycle detection (hash-set of visited) is `O(n)` space; Floyd's is `O(1)`.

### Time and space

- **Time: O(n).** If no cycle, fast reaches None in at most `n/2` outer iterations. If a cycle exists of length `C` with a tail of length `T`, slow takes at most `T + C` steps to enter and traverse the cycle once; fast catches up within `C` of those. Total bounded by `n`.
- **Space: O(1).** Two pointers, no sets, no dicts. The interview tell.

Say the space defense out loud every time:

> "**O(1) space** because Floyd's uses only two pointers — no auxiliary set or dict. The alternative — `seen = set()`, walk once — works but is O(n) space. The whole point of Floyd's is to trade an obvious O(n)-space algorithm for an O(1)-space one with the same time complexity."

That is the sentence interviewers grade. Memorize the cadence.

---

## 4. The `2k = k + nC` cycle-entrance lemma

Detection is easy. Finding the **first node of the cycle** (the "entrance") is the part that looks like dark magic but is, in fact, a four-line proof.

### Setup

Let:

- `T` = length of the non-cycle prefix (number of nodes before the cycle begins).
- `C` = length of the cycle.
- `k` = number of steps slow took when it first meets fast inside the cycle.

When they meet:

- Slow has taken `k` steps total.
- Fast has taken `2k` steps total (twice the speed).
- Both are at the same node.

So the *difference* `2k - k = k` is some whole number of laps around the cycle:

```
k = nC   for some integer n ≥ 1
```

Now: slow has walked `k` steps. The first `T` of those got it to the cycle entrance. The remaining `k - T` steps walked it *into* the cycle. So slow is currently `k - T` steps past the cycle entrance — which is the same as `(k mod C) - T` if we think modulo `C`. And since `k = nC`, `k mod C = 0`, so slow is `-T mod C = C - T` steps past the entrance, equivalently `T` steps *before* the entrance (going around the cycle).

The clean way to state this:

> **If you start a third pointer at `head` and walk it at speed 1, while simultaneously walking slow at speed 1 from the meeting point, they will meet at the cycle entrance after exactly `T` steps.**

Because:
- The third pointer walks `T` steps from `head` and lands at the cycle entrance.
- Slow walks `T` steps from the meeting point. The meeting point is `k - T` past the entrance, so slow is now `(k - T) + T = k = nC` past the entrance — which is exactly the entrance (since `nC` is a whole number of laps).

### The code

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = head
    fast = head

    # Phase 1: detection
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # No cycle; loop ended via guard.
    # If we exited via break, slow and fast are at the meeting point.
    if fast is None or fast.next is None:
        return None  # Belt and suspenders.

    # Phase 2: find the entrance.
    finder = head
    while finder is not slow:
        finder = finder.next
        slow = slow.next
    return finder
```

Two notes on the Python:

- The `while/else` form: the `else` runs *only* if the loop ended via guard (no `break`). It's idiomatic Python; learn to read it.
- The "belt and suspenders" recheck after the break is defensive; in correct code with `break` it's redundant, but it costs nothing and protects against future edits.

The full algorithm is two `while` loops, both `O(n)`. Total time still `O(n)`, space still `O(1)`.

### Why this is in the lecture, not just the drill

In Mock #1 next week, if you get a "find cycle entrance" problem (LeetCode 142), the interview tell is not whether you can code it — most candidates can fake their way through with the algorithm half-memorized. The tell is whether you can **explain the lemma in three sentences**. Out loud. While drawing on a whiteboard. Practice the explanation now.

---

## 5. The midpoint micro-pattern

Find the middle node of a linked list in **one pass**. Naive: count nodes (`O(n)`), then walk to `n/2` (`O(n)`). Fast/slow: walk both pointers, slow lands on the middle exactly when fast reaches the end.

```python
def middle_node(head: ListNode | None) -> ListNode | None:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
```

The convention question: for an **even-length** list, which middle do we want? Two options:

- **Upper middle.** For `[1, 2, 3, 4]`, return node 3 (1-indexed). This is what the loop above returns — when fast reaches None, slow is one past the midpoint.
- **Lower middle.** For `[1, 2, 3, 4]`, return node 2. To get this, terminate the loop when `fast.next.next is None`:

```python
def middle_node_lower(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
```

In Mock #1, when you see a "find the middle" prompt, **ask the interviewer which convention they want** before writing code. That's a U-step move. Most prompts say "the middle" without specifying; clarifying is the right thing to do.

For odd-length lists both conventions return the same node, so the ambiguity only matters when length is even.

---

## 6. Fast/slow on a functional graph: Happy Number

Some fast/slow problems aren't on linked lists at all. They live on *functional graphs* — graphs where every node has exactly one outgoing edge defined by a function. Walk from any node, and you eventually either reach a fixed point or enter a cycle.

**Happy Number.** A number `n` is "happy" if repeatedly replacing it with the sum of squares of its digits eventually reaches 1. If you ever cycle through numbers without reaching 1, it's not happy.

Naive approach: keep a set of seen numbers, stop when you see a duplicate or hit 1. `O(?)` time (the chains are short in practice), `O(?)` space.

Fast/slow approach: slow does one digit-square step per iteration, fast does two. If they meet at 1, the number is happy. If they meet elsewhere, there's a cycle — not happy.

```python
def digit_square_sum(n: int) -> int:
    total = 0
    while n > 0:
        d = n % 10
        total += d * d
        n //= 10
    return total

def is_happy(n: int) -> bool:
    slow = n
    fast = n
    while True:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
        if fast == 1:
            return True
        if slow == fast:
            return False
```

The structure is identical to the linked-list version. The "node" is an integer; the "next pointer" is the `digit_square_sum` function; the "cycle" is a repeated value. The discriminator: every "node" has exactly one outgoing edge, so the iteration *is* a graph walk, and Floyd's applies.

This is the recognition skill we're drilling — *seeing* the linked-list-ness in a problem that doesn't mention linked lists. Drill 4 is this exact problem.

---

## 7. The canonical recognition signals (the 30-second match)

Stop. Read the prompt slowly. Ask these in order:

1. **Is there a linked list (or a similar iterated-pointer-walk structure)?** If yes, fast/slow is a strong candidate.
2. **Does the prompt mention "cycle," "loop," "infinite," or "repeating"?** Strong signal for cycle detection.
3. **Does the prompt mention "middle," "midpoint," "halfway"?** Strong signal for the speed-2 midpoint trick.
4. **Does the prompt mention "nth from the end" (no length given)?** Strong signal for a fixed-gap fast/slow variant (homework).
5. **Is the iteration a function applied repeatedly to produce the next value?** (Happy number, finding the duplicate in `[1..n]`.) That's a functional graph; fast/slow applies.
6. **Is the answer about a position, a node, or a yes/no on cycle existence?** Fast/slow's outputs are usually one of those three.

The 30-second decision tree:

```
linked list (or sequence with one outgoing edge per "node")?
├── No  ──→ not fast/slow. Pattern is two-pointer, sliding window, hash map, etc.
└── Yes
    ├── "cycle / loop / infinite / repeating"?         ──→ Floyd's cycle detection
    ├── "middle / midpoint / halfway"?                  ──→ Speed-2 midpoint trick
    ├── "nth from end" (no length given)?               ──→ Fixed-gap variant
    ├── "find the cycle entrance / start"?              ──→ Floyd's + 2k=k+nC lemma
    └── functional graph (n → f(n))?                   ──→ Treat as linked list; apply Floyd's
```

This decision tree is what we want in muscle memory by Sunday.

---

## 8. When fast/slow doesn't fit

Equally important: knowing when to *reject* the pattern.

- **Arrays where you need random access.** Fast/slow makes sense on a *linked* structure where you can only step from one node to the next. If you can index into an array, you don't need fast/slow — use direct indexing.
- **Multiple cycles to find / classify.** Floyd's detects *one* cycle reachable from `head`. If a problem asks you to enumerate all cycles in a graph with multiple components, that's DFS or union-find (Weeks 7 and beyond).
- **Cycle in a *general* directed graph.** Fast/slow needs each node to have *exactly one* outgoing edge (a functional graph). General directed cycle detection is DFS-with-colors (Week 7).
- **The output is the *length* of the cycle.** That's a fast/slow variant — once detected, walk slow around until it meets itself, counting. Doable, but the pattern recognition is to spot the cycle first, then count.

Recognizing the *negative space* of the pattern matters as much as the positive recognition.

---

## 9. Worked example end-to-end: linked list cycle II (find entrance)

We will work this in full UMPIRE, abbreviated. Drill 2 is this exact problem.

**[U — 2 minutes]**

> "I'm given the head of a linked list. If there's a cycle, return the node where the cycle begins. If not, return None. Confirm: I cannot modify the list. Walk an example: nodes `A → B → C → D → E`, with `E.next = C`. The cycle starts at C. Answer: node C."

**[M — 30 seconds]**

> "Fast/slow pointers. Linked list + 'cycle entrance' is the canonical Floyd's-with-entrance application. Use Floyd's to detect the cycle, then restart a finder pointer at head and walk both at speed 1 until they meet — that's the entrance, by the `2k = k + nC` lemma."

**[P — 2 minutes]**

> "Phase 1: slow = fast = head. Loop while `fast` and `fast.next`: advance slow by 1, fast by 2. If they meet, break; that's a cycle. If the loop ends via guard, return None.
> Phase 2: finder = head. While `finder is not slow`: advance both by 1. Return finder.
> Edge cases: empty list (head is None) → return None. Single node with no self-loop → fast.next is None on first iter → loop ends, return None."

**[I — 3 minutes]**

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None
    finder = head
    while finder is not slow:
        finder = finder.next
        slow = slow.next
    return finder
```

**[R — 2 minutes]**

> "Trace on `A → B → C → D → E → (C)`:
> Start: slow=A, fast=A.
> Iter 1: slow=B, fast=C. Not equal.
> Iter 2: slow=C, fast=E. Not equal.
> Iter 3: slow=D, fast=D. Equal! Break.
> Phase 2: finder=A, slow=D. Not equal: finder=B, slow=E. Not equal: finder=C, slow=C. Equal! Return C. ✓
> Cycle entrance is C. Correct."

**[E — 1 minute]**

> "**Time O(n)** — Phase 1 is at most `T + C` ≤ `n` iterations. Phase 2 is at most `T` iterations. **Space O(1)** — three pointers, no set or dict. Tradeoff: the naive 'walk with a `seen` set' is O(n) time, O(n) space; Floyd's matches the time and beats the space. No further improvement obvious. **Best/avg/worst** all O(n) — there's no input that makes Floyd's faster or slower asymptotically."

That's UMPIRE on a textbook fast/slow problem, end-to-end, in about 10 minutes. The drill is to do this every single time.

---

## 10. Two common bug patterns

After watching ~50 candidates solve this family in mock interviews, two bugs come up repeatedly. Build them into your Review checklist.

### Bug 1: forgetting the `fast.next` guard

```python
while fast is not None:        # WRONG — no fast.next guard
    slow = slow.next
    fast = fast.next.next      # crashes if fast.next is None
```

The fix:

```python
while fast is not None and fast.next is not None:
    ...
```

You need both `fast` *and* `fast.next` non-None before advancing fast two steps. The `and` short-circuits — if `fast` is None, we don't evaluate `fast.next`.

### Bug 2: using `==` instead of `is`

```python
if slow == fast:    # WRONG if nodes have a custom __eq__
    return True
```

`ListNode` in most interview prompts doesn't override `__eq__`, so `==` falls through to identity. But if it *did* override `__eq__` to compare by value, you'd get false positives — two distinct nodes with the same `val` would be reported as "the cycle." Identity comparison (`is`) is unambiguous.

Get in the habit. `is` for nodes, `==` for values.

---

## 11. Self-check

Without notes, answer:

1. **What's a fast pointer?** (One that advances more than one node per step — almost always exactly two.)
2. **What's the loop guard for Floyd's?** (`while fast is not None and fast.next is not None`.)
3. **State the `2k = k + nC` lemma.** (When slow and fast first meet, slow has walked `k` steps and fast `2k`. The difference `k` is some whole number of cycle laps. Starting a third pointer at head and walking both at speed 1 will land both at the cycle entrance after `T` more steps.)
4. **Why is Floyd's preferred over the hash-set approach?** (Same `O(n)` time, but `O(1)` space instead of `O(n)`. The space efficiency is the interview tell.)
5. **What does the midpoint loop return for a list of length 4?** (The third node — the "upper middle." For "lower middle," use `fast.next.next is None` as the guard.)
6. **Why does fast/slow apply to Happy Number?** (Because `n → digit_square_sum(n)` defines a functional graph — every node has exactly one outgoing edge. Floyd's works on any functional graph.)

If you can answer all six without hesitation, proceed to [Lecture 2 — The Mock Interview Protocol](./02-the-mock-interview-protocol.md).

---

## Further reading

- **Wikipedia — Cycle detection**: <https://en.wikipedia.org/wiki/Cycle_detection> — the formal treatment. Read Floyd's section; skim Brent's.
- **NeetCode's "Linked List Cycle" video** (free YouTube) — 8 minutes, the canonical walkthrough.
- **LeetCode 141, 142, 876, 202, 287** — the five problems that cover the family. Drills 1–4 use four of them; the fifth (287, Find the Duplicate Number) is in the homework.

Next: [Lecture 2 — The Mock Interview Protocol](./02-the-mock-interview-protocol.md).
