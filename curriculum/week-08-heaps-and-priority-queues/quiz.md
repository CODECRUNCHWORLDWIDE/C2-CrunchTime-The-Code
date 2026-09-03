# Week 8 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is a heap problem — and if heap, name the sub-shape (top-k / k-closest / two-heap / k-way merge / scheduler / lazy deletion) and any invariant required (size bound / balance / tiebreaker / negation). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target.


---

**Q1.** "Given an unsorted array of integers and an integer `k`, return the k-th largest element in the array."

<details>
<summary>Answer</summary>

**Top-k via size-k MIN-heap.** The minimum of the heap is the k-th largest — the eviction bar. `O(n log k)` time, `O(k)` space. Exercise 1 exactly. The discriminator with Q5: we want the *k-th* largest, not the largest; we need state across iterations.

</details>

**Q2.** "Given an array of 2-D points and an integer `k`, return the `k` points closest to the origin by Euclidean distance."

<details>
<summary>Answer</summary>

**k-closest via size-k MAX-heap (negated).** Priority is `-d²`; the heap holds the k closest seen so far; the root is the farthest of the k. `O(n log k)`. Exercise 2 exactly. The heap-of-tuples idiom — entries are `(-d², x, y)`; the coordinates serve as a tiebreaker. Why distance-squared: skip `sqrt`; monotone with distance.

</details>

**Q3.** "Given a stream of integers, support two operations: `add_num(x)` and `find_median()`, both efficient."

<details>
<summary>Answer</summary>

**Two-heap pattern.** Max-heap of the lower half (negated for `heapq`); min-heap of the upper half; balanced so sizes differ by at most 1. `O(log n)` per add; `O(1)` per median. Exercise 3 exactly. Lecture 3 §1.

</details>

**Q4.** "Given an array of `k` sorted linked lists, merge them into one sorted linked list."

<details>
<summary>Answer</summary>

**k-way merge.** Heap of size k of `(value, list_index, node)` tuples. Pop the min, emit, refill from `node.next`. `O(N log k)` where `N` is the total element count. Challenge 1 exactly. The list-index tiebreaker is mandatory because `ListNode` has no `__lt__`.

</details>

**Q5.** "Given an unsorted array of integers, return the *largest* element."

<details>
<summary>Answer</summary>

**NOT a heap problem — `max(arr)`.** The largest element is `O(n)` with one pass and no auxiliary structure. A heap is overkill at `k = 1`. This is a *negative-space* discriminator with Q1: "k-th largest" vs "largest." Recognizing the difference is the senior signal.

</details>

**Q6.** "Given a list of words and an integer `k`, return the `k` most frequent words. Ties are broken alphabetically (smaller word ranks first)."

<details>
<summary>Answer</summary>

**Heap-of-tuples with conflicting tiebreaker direction.** Max-heap by count (most-frequent first); tiebreak by alphabetical order *forward* (smaller word ranks first). The cleanest path: sort the `Counter.items()` by `(-count, word)` and take the first `k`. A pure-heap version requires a custom `__lt__` because the count and word tiebreaker directions oppose. Lecture 2 §10.

</details>

**Q7.** "Given a weighted directed graph with non-negative edge weights, return the shortest path from a source to all other nodes."

<details>
<summary>Answer</summary>

**NOT a Week-8 problem (yet) — Dijkstra's algorithm.** Uses a min-heap as its frontier (so the heap *does* show up); but the *algorithm* is Dijkstra, covered in C5. Recognizing "this is a graph shortest-path problem, the heap is incidental" is the discriminator. The Week-8 patterns are top-k / k-closest / two-heap / k-way merge / scheduler — not shortest path.

</details>

**Q8.** "Given a stream of integers and a window size `w`, return the median of the current `w`-element window after each insertion."

<details>
<summary>Answer</summary>

**Two-heap PLUS lazy deletion.** Sliding window median. The two heaps from Q3, but the window expires older elements as new ones arrive. Lazy-delete the expired element from the appropriate heap; clean stale entries on the median query. Lecture 3 §4. The canonical Phase-3 problem in this family.

</details>

**Q9.** "Given an array of integers and an integer `k`, return the `k` smallest elements in *sorted order*."

<details>
<summary>Answer</summary>

**Either heapq.nsmallest OR sort.** For `k` smallest in sorted order: `sorted(arr)[:k]` is `O(n log n)`; `heapq.nsmallest(k, arr)` is `O(n log k)` *and returns sorted*. For `k << n`, the heap is cheaper. The senior framing: if you need *sorted* output, `nsmallest` is the one-liner; if you do not need sorted output, a manual size-k max-heap is the template rep.

</details>

**Q10.** "Given a 2-D matrix where each row is sorted, find the smallest element that does not appear in the matrix."

---

<details>
<summary>Answer</summary>

**Trick question — not a heap problem.** "Smallest element that does not appear" is a *missing-number* problem; a sorted-row matrix is irrelevant to the heap pattern. The intended solution is binary search or a hash set. Recognizing "this is not Week 8" is the negative-space discriminator. (If the problem were "smallest element in a sorted matrix," that *would* be a k-way merge — but that is a different problem.)


---

</details>

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Heap recognition is interview-ready, including the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 1 §7](./lecture-notes/01-heapq-and-top-k.md) and [Lecture 3 §7](./lecture-notes/03-two-heap-and-k-way-merge.md) for the sub-shape questions you missed. Most learners miss Q5 or Q7 first time; that is normal. |
| 5-6 | Redo Exercises 2 and 3 with stricter Research constraints sections. The k-closest and two-heap recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the size-bound and tiebreaker invariants stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q5, Q7, and Q10 — all "looks like a heap but is not" questions. Recognizing the negative space is the senior-level skill being measured.

Q5 (`max(arr)`) and Q10 (missing element in a sorted matrix) are the cleanest negative-space traps. Q7 (Dijkstra) is the trickier one — the heap *is* present, but the algorithm has a different name; treating it as "just a heap problem" loses the point.

When done, the [homework](./homework/README.md) is next.
