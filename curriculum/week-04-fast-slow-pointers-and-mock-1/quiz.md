# Week 4 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is fast/slow pointers or not — and if fast/slow, name the variant (Floyd's detection, Floyd's + entrance, midpoint, functional graph, fixed gap). One-line justification per answer. Lectures closed. Time yourself — 30 seconds per question is the target.

Four of the ten are **not** fast/slow. Being able to reject the pattern cleanly is the same skill as recognizing it, and it is the half most people never practice.

Answer key at the bottom.

---

**Q1.** "A warehouse's pick path is a chain of bays; each bay directs the picker to exactly one next bay, or to the loading dock. Determine whether a picker released at the first bay ever reaches the dock. You have a few hundred bytes of scratch memory on the handheld."

**Q2.** "A turnstile log lists employee badge IDs in the order they entered. Find the longest run of consecutive entries in which no badge appears twice."

**Q3.** "A podcast episode is stored as a chain of audio blocks with no length field and no random access. Find the block at which to insert the single mid-roll ad, in one pass."

**Q4.** "Given a stream of sensor readings and a required multiset of alarm codes, find the shortest contiguous burst of readings that contains every required code at least as many times as required."

**Q5.** "A firmware image contains a jump table: entry `i` holds the index of the entry the loader jumps to next. Starting at entry 0, report how many entries the loader touches once and never again, and how many it ends up cycling through forever. The loader runs before the heap exists."

**Q6.** "A pseudo-random dice engine computes each roll from the previous one with a fixed arithmetic formula and no other state. Determine after how many rolls the sequence begins repeating itself, without storing the rolls."

**Q7.** "A parcel's scan history is a forward-only chain of unknown length. Delete the scan that sits `k` positions back from the newest one, walking the chain only once."

**Q8.** "A build system's task list gives, for each task, the set of tasks that must finish before it. Determine whether the dependencies are satisfiable or contain a circular requirement."

**Q9.** "A phone tree escalates each unanswered call to exactly one other extension. When a call circulates forever, report the first extension it revisits, so the on-call team can be told where the misconfiguration begins."

**Q10.** "A conveyor holds a row of crates, each stamped with a weight. Working from both ends inward, determine whether the row of weights reads the same in either direction."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Fast/slow — Floyd's detection.** One outgoing edge per bay + "does it terminate" + a tight memory budget is the triple signal. Advance slow by one bay and fast by two; if they meet there is a loop and the picker never reaches the dock, and if fast runs out of bays the path terminates. `O(n)` time, `O(1)` space. This is [Exercise 1](exercises/exercise-01-conveyor-loop.md) minus the counting phase.

2. **NOT fast/slow — sliding window** (Week 3, the "longest" shape). Contiguous, "longest with a property," and a property that is cheap to maintain incrementally. The misdirection is that a window also uses two indices on a sequence — but both ends advance in lockstep, never at different speeds. Speed is the discriminator.

3. **Fast/slow — midpoint with the speed-2 hare.** "Forward-only, no length field, one pass, find the middle" is the canonical midpoint signal. Before writing anything, ask which middle: the guard `fast and fast.next` lands on the upper middle, and shifting it one position to `fast.next and fast.next.next` lands on the lower. This is [Exercise 3](exercises/exercise-03-midroll-break.md), which specifies the lower.

4. **NOT fast/slow — sliding window with a frequency invariant** (the Week 3 challenge shape). Different family entirely. The misdirection is "find a contiguous burst," which sounds like a traversal problem; the actual work is maintaining counts as the window grows and shrinks, and there is no second pointer moving at a different rate.

5. **Fast/slow on a functional graph.** `i → table[i]` gives every entry exactly one successor, so the jump table *is* a chain whose nodes are indices. Phase 1 finds a meeting point, phase 2 converts it to the entrance while counting the tail, and one more lap measures the rotation — the two numbers the question asks for. "Before the heap exists" is what rejects the visited-array approach, and note that the rejection is availability, not speed. This is [Exercise 4](exercises/exercise-04-wear-level-rotation.md) with a table lookup instead of a formula, and it is [Homework Problem 1](homework/README.md) with a different question asked of the answer.

6. **Fast/slow on a functional graph.** Each roll is a function of the previous roll and nothing else, which is the definition. "Without storing the rolls" is the `O(1)`-space requirement in disguise. Careful reading the question: "after how many rolls it begins repeating" is the *tail* length, which needs phase 2 — the meeting point from phase 1 alone does not give it.

7. **Fast/slow with a fixed gap.** Not Floyd's: the gap is constant and known in advance, so there is no meeting and no lemma. Advance fast by `k`, then walk both in lockstep until fast falls off the end; slow is then sitting where you need it. Single pass plus `O(1)` space is the tell. This is [Homework Problem 2](homework/README.md), where the contract also has to survive a `k` larger than the chain.

8. **NOT fast/slow — DFS with colors, or a topological sort** (Week 7). Floyd's requires *exactly one* outgoing edge per node. A task with three prerequisites has out-degree three, so there is no single chain to walk and no meaning to "step twice." Use white/grey/black DFS; a back-edge to a grey node is the cycle. This is the most important rejection in the quiz — a general directed graph looks like a cycle problem and is not this pattern.

9. **Fast/slow — Floyd's detection plus the `2k = k + nC` entrance lemma.** One outgoing edge per extension, and the question asks for the *entrance* rather than for existence. Phase 1 detects; phase 2 walks a fresh pointer from the start alongside slow at speed 1 until they collide, which lands on the entrance. Returning the phase-1 meeting point is the classic wrong answer — it is inside the loop but generally is not its first extension. This is [Exercise 2](exercises/exercise-02-escalation-loop.md).

10. **NOT fast/slow — converging two-pointer** (Week 1). "Working from both ends inward" is stated in the prompt. Both indices move one step per iteration, toward each other, and terminate when they cross. Different geometry of motion entirely. Note the near-miss: had the crates been a forward-only chain instead of a row you can index, the answer would be fast/slow — find the middle, reverse the back half, compare — which is exactly [Homework Problem 3](homework/README.md). The *structure*, not the question, decides the pattern.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Fast/slow pattern recognition is interview-ready. Move on. |
| 7–8 | Good — re-read [Lecture 1 §7 and §8](lecture-notes/01-floyds-tortoise-and-hare.md) for the ones you missed, especially Q5, Q7, and Q8. |
| 5–6 | Redo Drills 1, 2, and 4 with stricter Research constraints sections before Mock #1. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures and re-do all four drills with the recorder running before attempting the mock. |

This quiz is about **fluency**, not difficulty. Every question is something you should be able to answer in under 30 seconds once the patterns are in muscle memory.

Two questions deserve a second look regardless of your score. **Q8** is the one candidates get wrong under pressure, because "circular requirement" reads as a cycle problem and the reflex fires before the out-degree check does. **Q10** is the one that teaches the deepest lesson: the same question asked about a different structure has a different answer. Pattern matching is on structures, not on wordings.

When done, the [homework](homework/README.md) is next.
