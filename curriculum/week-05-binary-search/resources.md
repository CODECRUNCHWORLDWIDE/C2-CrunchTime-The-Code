# Week 5 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Binary search — Wikipedia**: <https://en.wikipedia.org/wiki/Binary_search_algorithm> — the canonical reference; the "Variations" section covers lower/upper bound and the parametric idiom.
- **Python `bisect` module**: <https://docs.python.org/3/library/bisect.html> — the standard library's lower-bound / upper-bound implementation. Read once. You will not use it in drills (the point is writing the loop yourself), but interviewers expect you to know it exists and to *defend* writing the loop manually when asked.
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>

## On the pattern itself

Binary search is described under many names in the literature. The recognition skill is mapping the surface name to the underlying pattern:

- **Binary search** — the textbook name; usually means "find target in sorted array."
- **Bisection** — the numerical-methods name for the same idea applied to continuous functions (finding a root of `f(x) = 0`).
- **Lower bound / upper bound** — find the first / last position satisfying a predicate. The C++ STL names; Python's `bisect_left` and `bisect_right` are direct equivalents.
- **Parametric search** — searching for the answer to an optimization problem by binary-searching over the answer space. The interview-prep name is "binary search on the answer."
- **Galloping search** — a binary-search variant used in production sort algorithms (Timsort). Out of scope but worth knowing.

If a write-up uses "ternary search" or "exponential search" — those are different algorithms. Binary specifically halves the search space; nothing else this week does.

## Free practice platforms

- **HackerRank — Search domain**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=search>
- **Codeforces — Binary search tag**: <https://codeforces.com/problemset?tags=binary+search>
- **Exercism — Python Track, search exercises**: <https://exercism.org/tracks/python>

## On the off-by-one problem

Binary search is famous for being *almost* trivial and *actually* hard to write correctly. The off-by-one problem has multiple framings:

- **Jon Bentley, "Writing Correct Programs" (1983)** — a foundational paper noting that most binary-search implementations in textbooks had bugs. Search "Bentley writing correct programs binary search" for the abstract. Read once. The historical context is the point: this is a problem that *senior* engineers get wrong, not just juniors.
- **"Nearly all binary searches and mergesorts are broken"** — Joshua Bloch's 2006 blog post (then-engineer at Google) describing an integer-overflow bug in the JDK's binary search that survived for nine years: <https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/> — read this once. The fix is `mid = lo + (hi - lo) // 2`. In Python it does not matter for integer overflow (Python ints are arbitrary precision), but the *habit* matters because Java, C, and Rust all use it and your code might be ported.

## Videos on the pattern (free, no signup)

- **Any "binary search on the answer" walkthrough** (YouTube — free): search that exact phrase. If you have never seen the parametric idiom explained in video form, watch one before Exercise 5. Watch for the *shape* — reframe, interval, predicate, return — not for the specific problem the presenter picked; our drills use different contracts and you will get more from the video if you are listening for the cadence.
- **MIT 6.006 — Lecture on binary search trees** (free OCW): tangential but the discussion of "decision-tree depth" is the same idea as binary search depth.

## On parametric search specifically

Binary search on the answer is the highest-yield interview technique of the week. Two short reads, both free:

- **Codeforces — "EDU: Binary Search" course, Step 2 ("Searching for the answer")**: <https://codeforces.com/edu/course/2/lesson/6/2> — free; covers the parametric idiom with multiple worked examples. Read sections 1–3.
- **GeeksforGeeks — "Binary Search on Answer" articles**: search this exact phrase; multiple short articles. The vocabulary is consistent; pick one and skim.

The vocabulary item to install: **monotone predicate**. A function `feasible: int → bool` is monotone if `feasible(k) = True ⇒ feasible(k+1) = True` (or the mirror). Parametric search works *iff* the predicate is monotone. Recognizing monotonicity is the Research-constraints skill.

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1–4.

| Term | One-line definition |
|------|---------------------|
| **Binary search** | An `O(log n)` search algorithm that halves the search space at each step |
| **Search space** | The interval of indices (or values) currently under consideration; halves each iteration |
| **`lo`, `hi`, `mid`** | The three pointers of the canonical loop; `mid = lo + (hi - lo) // 2` |
| **Closed interval** | `[lo, hi]` — both endpoints included; pairs with `while lo <= hi` |
| **Half-open interval** | `[lo, hi)` — right endpoint excluded; pairs with `while lo < hi` |
| **Lower bound** | The leftmost index where `arr[i] >= target` (or the predicate flips True) |
| **Upper bound** | The leftmost index where `arr[i] > target` (the position *after* the last matching element) |
| **Rotated sorted array** | A sorted array whose elements have been cyclically shifted — what a ring-buffer dump looks like once the writer has wrapped, e.g. `[58, 61, 64, 70, 12, 19, 33, 47]` |
| **Pivot** | The index where the rotation begins; the smallest element in a rotated sorted array |
| **Monotone predicate** | A boolean function `f(k)` such that `f(k) = True ⇒ f(k+1) = True` (or the mirror) |
| **Parametric search** | Binary search applied to the *answer space* of an optimization problem, using a monotone predicate as comparator |
| **Search on the answer** | The interview-prep name for parametric search |
| **`feasible(k)`** | The convention name for the monotone predicate in a parametric search |
| **`count_at_most(v)`** | A predicate counting how many candidate values are `≤ v`; the comparator for every rank query solved by bisecting a value range |
| **Integer overflow safety** | Writing `mid = lo + (hi - lo) // 2` instead of `(lo + hi) // 2` — irrelevant in Python, mandatory in C/Java/Rust |

## What you will be glad you read

Two things, both short, both this week:

1. **Joshua Bloch's "Nearly all binary searches are broken"** — five-minute read. The takeaway is permanent: write `mid = lo + (hi - lo) // 2`, always, even though Python does not need it.
2. **Codeforces EDU "Searching for the answer"** sections 1–3 — twenty minutes. The cleanest treatment of parametric search in free material.

If you read nothing else this week, read those two and skim five binary-search problem titles from any practice set, predicting the sub-shape of each before you open it.

---

*Broken link? Open an issue.*
