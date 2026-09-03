# Week 7 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each one, decide whether it is
depth-first search, topological sort, or something else — and if it is
depth-first, say which shape (recursive, explicit stack, three colours,
post-order) and which invariant it needs (a visited set, a parent pointer, the
grey set, waiting counts). One line of justification per answer. Lectures
closed. Time yourself: 45 seconds a question is the target.


---

**Q1.** "A radio org has a square link table where row `i`, column `j` holds `1`
when masts `i` and `j` hear each other directly. Report every cluster of masts
that can reach each other through any chain of links, as `(smallest mast in the
cluster, how many masts it holds)`."

<details>
<summary>Answer</summary>

**Depth-first search for connectivity, recursive.** One fresh walk per
   cluster, and because the outer loop climbs, the mast that starts a walk is
   automatically the cluster's smallest. Invariant: a `set[int]` of masts
   already reached. The table is symmetric, so the graph is undirected and no
   loop-detection machinery is needed — you are counting groups, not hunting
   circles. Cost `O(n²)`, because you cannot beat reading a table that has `n²`
   cells in it. This is
   [Exercise 1](./exercises/exercise-01-repeater-clusters.md).

</details>

**Q2.** "A cannery's batch plan says which stages feed which other stages.
Report one circle of stages that each wait on the next, or say there is none."

<details>
<summary>Answer</summary>

**Depth-first search with the three colours.** Directed loop detection.
   White is untouched, grey is on the path under your feet, black is finished.
   An arrow into a grey stage is a loop; an arrow into a black stage is
   ordinary and proves nothing. The undirected "is it my parent?" trick does
   not transfer to a directed graph. Cost `O(V + E)` — one look at every stage
   and one at every arrow.
   [Exercise 3](./exercises/exercise-03-batch-loop-audit.md), and
   [Lecture 3 §2](./lecture-notes/03-topological-sort.md).

</details>

**Q3.** "A dry dock has a list of refit jobs and a list of pairs saying which
job has to finish before which other job starts. Give one legal running order,
and separately the jobs that can never start."

<details>
<summary>Answer</summary>

**Topological sort, Kahn's algorithm.** Waiting counts, a set of ready jobs,
   and the leftovers when the ready set runs dry are exactly the jobs inside a
   circle plus everything downstream of one. You never look for the circle; you
   notice you ran out of work. Cost `O(V + E)`.
   [Exercise 4](./exercises/exercise-04-refit-order.md).

</details>

**Q4.** "A warehouse alarm spreads from one rack to every rack it touches, one
round per second. Report which racks are alerted after each round, as a list of
lists."

<details>
<summary>Answer</summary>

**Not depth-first — breadth-first, with the rounds tracked.** "One round per
   second, report each round" is the breadth-first signature: consume the whole
   queue as it stands, then let what it freed become the next round. A
   depth-first walk goes down one long arm to its end before touching the second
   rack, so it can tell you *which* racks are reached but never *when*. Week 6's
   idiom, and recognising it as **not** a Week 7 problem is the point of the
   question.

</details>

**Q5.** "A flood map is a grid of wet and dry squares. Report the area of the
largest single pool — a group of wet squares joined edge to edge."

<details>
<summary>Answer</summary>

**Depth-first search for connectivity, answering on the way back up.** Each
   walk returns the size of the pool it just flooded — `1 +` the sizes its
   neighbours returned — and you keep the largest. The visited marks are what
   stop the walk counting a square twice. Cost `O(rows × columns)`. Same shape
   as Q1, with a number carried out of the walk instead of a count kept outside
   it.

</details>

**Q6.** "Several rail yards each filed a sighting: the wagons they saw, listed
front to back. No yard saw the whole train. Reconstruct the front-to-back order
of every wagon, and say whether the sightings force it or merely allow it."

<details>
<summary>Answer</summary>

**Topological sort on an edge set you have to derive first.** The recognition
   is the hard half: each sighting's *neighbouring* pairs are the constraints,
   and everything else follows from them. Then it is Kahn — and "forces it or
   merely allows it" is answered by how many wagons are ready at each step, one
   at a time meaning forced.
   [Challenge 2](./challenges/challenge-02-consist-reconstruction.md).

</details>

**Q7.** "A pipe network joins pumping stations. Given two stations, report the
smallest number of pipes a technician has to walk along to get from one to the
other."

<details>
<summary>Answer</summary>

**Not depth-first — breadth-first.** "Smallest number of pipes" on a graph
   where every pipe costs the same is the canonical breadth-first signal
   (Week 6). A depth-first walk finds *a* route and has no idea whether it is
   short. This is a trap question: it reads exactly like Q8 until you notice
   the word "smallest".

</details>

**Q8.** "A pipe network joins pumping stations. Report every pipe whose failure
would cut some station off from a station it can currently reach."

<details>
<summary>Answer</summary>

**Depth-first search carrying discovery times and low-links.** Chokepoint —
   bridge — detection. Each station records when it was first reached, and the
   lowest such number anything below it can climb back to; a pipe is a
   chokepoint when nothing below it can get back above it. Cost `O(V + E)`. The
   obvious answer — remove each pipe in turn and re-walk the network — is
   `O(E × (V + E))` and does not finish at real sizes.
   [Challenge 1](./challenges/challenge-01-chokepoint-mains.md).

</details>

**Q9.** "A library's shelf index is a binary tree of integer shelf codes. The
rule is that every code below and to the left of a node is smaller than it, and
every code below and to the right is larger. Report the first code that breaks
the rule."

<details>
<summary>Answer</summary>

**Depth-first search on a tree, carrying bounds down.** Every node inherits a
   low and a high limit from its ancestors; go left and the high limit becomes
   this node's code, go right and the low limit does. Checking only against the
   parent passes trees that are wrong three levels down, which is the whole
   point of the problem. A left-to-right walk of the codes also works — they
   have to come out increasing — but needs care about what it carries between
   nodes. Cost `O(N)` time, `O(H)` space for the height of the tree.
   [Homework Problem 4](./homework/problem-04-shelf-index-audit.md).

</details>

**Q10.** "Given a list of volunteers, report every possible seating arrangement
of them around a table."

---

<details>
<summary>Answer</summary>

**Not plain depth-first — backtracking.** Generating every arrangement needs
    an undo step: mark a volunteer as seated, go deeper, then unmark on the way
    back out. That undo is exactly what a visited set is *not* — a visited set is
    permanent, and it is permanent because a graph walk wants each node once,
    where an arrangement search wants each volunteer once *per branch*.
    Backtracking is Week 12. The trap is that it looks identical to recursive
    depth-first search until you notice it is asked to produce every
    configuration rather than to visit every node.


---

</details>

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Your recognition is interview-ready, negative space included. Move on. |
| 7-8 | Good. Re-read [Lecture 1 §8](./lecture-notes/01-recursive-dfs.md) and [Lecture 3 §8](./lecture-notes/03-topological-sort.md) for the shapes you missed. Most people miss Q4 or Q7 the first time; that is normal. |
| 5-6 | Redo [Exercise 3](./exercises/exercise-03-batch-loop-audit.md) and [Exercise 4](./exercises/exercise-04-refit-order.md), saying the invariant out loud each time. Loop detection and topological sort are the two most heavily graded Phase 2 patterns. |
| <5 | The recognition is not automatic yet. Re-read all three lectures, redo all five exercises with the invariant stated aloud, then retake this. |

This quiz measures **fluency**, not difficulty. The questions that separate
people are Q4, Q7 and Q10 — the three that look like this week's material and
are not. Q7 is the sharpest: it is Q8's opening sentence with one word changed,
and one word is genuinely all it takes to move a problem from depth-first to
breadth-first.

When you are done, the [homework](./homework/README.md) is next.
