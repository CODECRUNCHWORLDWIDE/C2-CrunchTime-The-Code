# C2 Content Policy — Original Problems Only

This course is published under **GPL-3.0**. Anyone may fork it, teach from it, print it, translate it, and redistribute it. That is only true if every problem in it is ours. This document is the rule that keeps it true.

It is binding on every contributor and every future edit.

---

## The rule

**Every problem posed in this course is written for this course.**

Not restated from somewhere else. Not reskinned from somewhere else. Written.

That covers the problem statement, the constraints, the examples, the test cases, the worked solutions, and the explanatory prose around them.

---

## Why the stricter rule

A weaker rule — "restate other people's problems in your own words" — is legally defensible. [17 U.S.C. § 102(b)](https://www.law.cornell.edu/uscode/text/17/102) does not protect "any idea, procedure, process, system, method of operation," so the *algorithmic task* is free for anyone to teach. We could have gone that way.

We did not, for three reasons:

1. **Restating invites paste-then-paraphrase.** In practice the author opens the other site, then edits. That produces a derivative work, and it is detectable. The only reliable defense is to never open the page.
2. **Examples and test data have no idea/expression defense.** A curated test suite can be protectable as a compilation, and the industry's actual enforcement has been aimed here — [HackerRank's 2021 DMCA](https://github.com/github/dmca/blob/master/2021/11/2021-11-12-hackerrank.md) was over problem content, and Codeforces permits republishing statements while expressly restricting tests. Even a clean restatement paired with someone else's examples is exposed.
3. **Downstream freedom is the point.** A fork in another country, a printed workbook, a paid bootcamp built on this material — all of those are things GPL-3.0 promises. We cannot promise them on top of borrowed problems.

There is a pedagogical dividend, and it is not small. A learner who has memorized a problem *title* can retrieve a remembered solution without solving anything. Original problems defeat that. The course measures whether you can solve, not whether you can recall.

---

## What is allowed

**Reference by name and link.** Problem titles are not copyrightable — [37 CFR § 202.1(a)](https://www.law.cornell.edu/cfr/text/37/202.1) excludes "names, titles, and slogans." Problem numbers are facts (*Feist Publications v. Rural Telephone*, 499 U.S. 340). A hyperlink reproduces nothing. So this is fine, and is the standard form:

> **Practice elsewhere.** The same pattern appears as [LeetCode 51 · N-Queens](https://leetcode.com/problems/n-queens/) if you want a judge to run against.

Title, number, plain out-link. Nothing else crosses over.

**Naming the platforms.** Nominative fair use (*New Kids on the Block v. News America Publishing*, 971 F.2d 302) lets us name LeetCode, NeetCode, and CodePath to say true things about them. Plain word marks only.

**Teaching a published method.** FRAME is a *procedure*, excluded from copyright by § 102(b). We teach it in our own words. We do not copy anyone's write-up of it.

**Standard algorithms.** Dijkstra, KMP, Timsort, union-find — algorithms are not copyrightable. Textbook implementations are ours to write. What we may not do is copy a specific author's *implementation*, including their variable names when those are distinctive.

---

## What is forbidden

- Any problem statement taken or adapted from another platform.
- Any example input/output taken from another platform — including their explanation text.
- Any constraint block taken from another platform. **Choose our own bounds, and justify them pedagogically.**
- Any test case taken from another platform, especially judge cases that were never published as examples.
- Any implementation derived from another site's editorial, including its variable naming.
- Any section that announces borrowed provenance: `Constraints (LeetCode)`, `Per the LC spec`, or similar. If that phrase is needed, the content underneath is already a violation.
- Any logo, stylesheet, typography, or repo/domain name implying affiliation. No `leetcode-*`, no `neetcode-*`.
- Scraping any platform. That is contract, not copyright — the fair-use arguments above do not apply to it.
- **CodePath material in any form.** `github.com/codepath/compsci_guides` carries `license: null`, and their ToS requires prior written consent to republish. Their pedagogy may be described in our words; their prose, guides, and problem sets may not be reproduced at all.

---

## Tells that mean something was copied

Any of these in a diff is a rejection, no discussion:

| Tell | Why it is a tell |
|---|---|
| `.length` in a spec | This course is Python. `len(...)` is ours; `.length` is JavaScript, and came from somewhere |
| `{1=1, 2=2}` style output | Java's map rendering. Not Python |
| `nums`, `strs`, `k`, `n` with no domain meaning | Platform-generic naming. Ours are named for the story |
| A constraint like `1 <= n <= 9` with no stated reason | We justify every bound. An unjustified bound was inherited |
| An example whose explanation reads like a judge's | Ours explain the *teaching* point |
| `-10^4 <= nums[i] <= 10^4` | The canonical platform bound. Pick real ones |

---

## How to write an original problem

**Do not open the other site.** Start from the pattern, not from a page.

1. **Name the pattern** you need to drill — "variable-size sliding window with a frequency invariant."
2. **Invent a domain** where that pattern is the natural solution. Server logs, seating charts, inventory, sensor readings, scheduling. Pick something with real nouns.
3. **Write the contract yourself.** Inputs, output, and — deliberately — what happens on the empty case, the no-solution case, and ties. Vary these from the obvious defaults.
4. **Choose constraints that teach.** Every bound should have a reason you can state: this size forces the `O(n log n)` solution; this bound makes the `O(n²)` version time out; this one keeps the recursion depth safe.
5. **Write examples that teach.** Include the degenerate case, the no-solution case, and one that punishes the common wrong approach. Platform examples demonstrate; ours instruct.
6. **Generate test cases yourself**, including adversarial ones. Write the generator if that is easier.

**A costume is not enough.** Renaming Two Sum's array to "transaction amounts" is reskinning, and reskinning alone still tracks someone else's contract. Change the contract too: return indices instead of values, or require all pairs instead of one, or define the tie-break. The learner should not be able to map it one-to-one onto a remembered solution.

---

## Required footer

Every course README carries this, verbatim:

> **Not affiliated with, endorsed by, or sponsored by LeetCode, NeetCode, or CodePath.** Problem names and numbers are referenced for practice only; all problems, examples, constraints, and test cases in this course are original work, published under GPL-3.0. LeetCode is a trademark of LeetCode LLC; NeetCode and CodePath are trademarks of their respective owners.

---

## If you want problems you can legally reproduce

Should this course ever need to include an outside problem verbatim, only these are clean:

| Source | License | Note |
|---|---|---|
| [Exercism `problem-specifications`](https://github.com/exercism/problem-specifications) | MIT | Cleanest option |
| [Kattis](https://www.kattis.com/problem-package-format/spec/legacy.html) | Per-problem `license` field | Use only `public domain`, `cc0`, `cc by`, `cc by-sa` |
| [Codeforces](https://codeforces.com/blog/entry/967) | Explicit republish grant | Attribution + direct link required, in close proximity to the statement |

**Two traps.** Codeforces forbids republishing their problems on anything "supporting automatic testing" — so a graded auto-runner may only carry original problems. And Project Euler / CSES are **CC BY-NC-SA**: ShareAlike is viral and would force this whole curriculum under a non-commercial license, which is incompatible with GPL-3.0 and with letting others build on it. Do not use them.

---

*Questions about a specific case: open an issue before writing, not after.*
