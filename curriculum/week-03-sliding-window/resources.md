# Week 3 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Sliding Window — Wikipedia overview**: <https://en.wikipedia.org/wiki/Sliding_window_protocol> — the term originates in networking; the concept is the same.
- **Python `collections.Counter`, `defaultdict`, `deque` — official docs**: <https://docs.python.org/3/library/collections.html>
- **Python `collections.deque` (specifically for O(1) appends and pops on both ends)**: <https://docs.python.org/3/library/collections.html#collections.deque>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>

## On the pattern itself

You will read several mutually inconsistent explanations of "sliding window" online. Trust the lectures here over any single blog post. The two concepts that *always* hold:

- **Window = a contiguous slice `s[left..right]`** (or `nums[left..right]`).
- **The two indices move only in one direction.** That's what makes it `O(n)` — each index advances at most `n` times.

If a write-up calls "two pointers from each end" a "sliding window," it's using the term loosely. In this course we keep the two patterns separate.

## Free practice platforms

- **LeetCode — Sliding Window tag** (free): <https://leetcode.com/tag/sliding-window/>
- **HackerRank — Interview Preparation Kit, Strings track**: <https://www.hackerrank.com/interview/interview-preparation-kit>
- **Exercism — Python Track**: <https://exercism.org/tracks/python>
- **Codeforces Educational** rounds: <https://codeforces.com/edu/courses>

## Mock-interview platforms (peer-based, free tiers)

- **Pramp**: <https://www.pramp.com/>
- **interviewing.io**: <https://interviewing.io/>
- **A peer who's also doing C2** — best option

## Videos on sliding window (free, no signup)

- **MIT 6.006 (recurring) — Lecture on Hashing** (free OCW; the dictionary-with-window discussion at the end): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/>
- **NeetCode's free sliding-window walkthroughs** (YouTube — free): search "neetcode sliding window"; pick one and watch one.

## Glossary cheat sheet

Keep this tab open this week. Builds on Weeks 1–2.

| Term | One-line definition |
|------|---------------------|
| **Window** | A contiguous slice `s[left..right]` of the input |
| **Fixed-size window** | A window of constant length `k`; both indices advance together |
| **Variable-size window** | A window whose length grows and shrinks based on an invariant |
| **Window invariant** | A property the loop maintains at every iteration ("at most k distinct chars," "sum ≥ target," etc.) |
| **Expand / shrink** | Move `right` to grow the window; move `left` to shrink it |
| **Amortized O(n)** | Total iteration count is O(n) even with a nested `while`, because each index advances at most n times |
| **Frequency table** | `Counter` or `defaultdict(int)` mapping value → count inside the window |
| **At most K** | "Window length ≤ K" or "at most K distinct values" — both produce valid sliding-window shapes |
| **Exactly K** | A reformulation, not a window: `exactly K = at_most(K) - at_most(K - 1)`. Write the helper once, call it twice. |
| **Monotonic deque** | A deque kept in monotonic order to query window max/min in O(1) — Week 9 |
| **Two-pointer (recap)** | Two indices that may converge, swap roles, or partition. *Different from sliding window.* |
| **Contiguous** | Adjacent in the original array / string; no skipping |
| **Subsequence (not us)** | Elements in original order but not necessarily contiguous — *not* sliding window territory |

## What you'll be glad you read

The `Counter` documentation is the one piece of "infrastructure" reading that pays back across this week and Week 9. `Counter`'s arithmetic (subtraction, intersection, equality) is the precise tool for "is the window's frequency table equal to / a superset of the target frequency table?" — which is the shape of half the sliding-window problems in real interviews.

If you read nothing else this week, read:

1. The `Counter` docs end-to-end.
2. One `deque` walkthrough — even if you don't use it this week.
3. The five exercise drill prompts before you start any of them, so you've primed the pattern.

---

*Broken link? Open an issue.*
