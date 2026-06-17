# Week 2 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Big-O Cheat Sheet** (community-maintained): <https://www.bigocheatsheet.com/> — pin the table to your wall
- **Python `dict` — official docs**: <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>
- **Python `set` — official docs**: <https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset>
- **`collections.Counter` and `defaultdict`**: <https://docs.python.org/3/library/collections.html>
- **CPython time complexity reference** (the source of truth for "is this O(1)?" questions about Python built-ins): <https://wiki.python.org/moin/TimeComplexity>
- **PEP 8 review (recurring)**: <https://peps.python.org/pep-0008/>

## On the Python `dict` and `set` internals

You do not need to memorize CPython internals, but knowing *why* dict lookups are O(1) average — and what makes them O(n) worst case — is the kind of judgment a senior interviewer probes for.

- **"Modern Dictionaries" by Raymond Hettinger** (PyCon talk, free on YouTube): <https://www.youtube.com/results?search_query=raymond+hettinger+modern+dictionaries>
- **CPython `dictobject.c` overview** (read the file header comment, not the code): <https://github.com/python/cpython/blob/main/Objects/dictobject.c>
- **"Why Python `dict` is faster than you think" (any decent blog post)** — search and pick one; the consensus story is consistent across sources.

## Free practice platforms (same as Week 1)

- **LeetCode** (free problems): <https://leetcode.com/> — search the **Hash Table** tag for Week 2 problems
- **HackerRank — Interview Preparation Kit**: <https://www.hackerrank.com/interview/interview-preparation-kit>
- **Exercism — Python Track**: <https://exercism.org/tracks/python>
- **Codeforces Educational** rounds: <https://codeforces.com/edu/courses>

## Mock-interview platforms (peer-based, free tiers)

- **Pramp**: <https://www.pramp.com/>
- **interviewing.io**: <https://interviewing.io/>
- **A peer who's also doing C2** — best option

## Videos on Big-O intuition (free)

- **MIT 6.006 Lecture 1 — Algorithmic Thinking** (free OCW): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/>
- **Princeton Algorithms Part I — Lecture 2 (Analysis)** (free Coursera audit): <https://www.coursera.org/learn/algorithms-part1>
- **CS50 — "Why Big-O matters"** (free): <https://cs50.harvard.edu/>

## Books / chapters (free)

- **Competitive Programmer's Handbook — Antti Laaksonen** — chapters on time complexity and hashing (fully free PDF): <https://cses.fi/book/book.pdf>
- **Algorithm Design Manual — Steven Skiena** — selected chapters preview free: <https://www.algorist.com/>

## Glossary cheat sheet

Keep this tab open this week.

| Term | One-line definition |
|------|---------------------|
| **Big-O** | Asymptotic upper bound; how runtime / space scales as `n → ∞` |
| **Big-Θ (theta)** | Tight bound; both upper and lower. In interviews, "O(n)" is often used where "Θ(n)" is meant. |
| **Big-Ω (omega)** | Asymptotic lower bound; the *best* you can do |
| **Amortized** | Average cost per operation across a long sequence — handles spiky operations like `list.append` |
| **Hash map** | Key → value mapping with O(1) average lookup / insert. Python's `dict`. |
| **Hash set** | Unordered collection of unique keys, O(1) average membership. Python's `set`. |
| **Collision** | Two distinct keys hashing to the same bucket; resolved by probing or chaining |
| **Load factor** | Filled-buckets ÷ total-buckets; high load factor → more collisions → slower lookups |
| **Frequency table** | Dict mapping each value → count of its occurrences |
| **Complement** | For target `t` and value `v`, the *complement* is `t − v`. Hash-map two-sum looks up complements. |
| **Counter** | `collections.Counter` — a dict subclass that counts occurrences automatically |
| **defaultdict** | `collections.defaultdict(list)` — a dict that auto-creates a default value on missing keys |
| **Set membership** | `x in S` — O(1) average for `set`, O(n) for `list`. Knowing the difference is the entire week. |
| **Single pass** | One traversal of the input; the goal of most hash-map solutions |

## What you'll be glad you read

The CPython `dict` overview is the one piece of "infrastructure" reading that pays back for years. If you read nothing else this week, read the header comment of `dictobject.c` and Raymond Hettinger's talk. You will be asked "is `x in dict` O(1)?" in real interviews — and answering "average yes, worst case O(n) due to collisions, Python uses open addressing with a randomized hash" beats "yes" every time.

---

*Broken link? Open an issue.*
