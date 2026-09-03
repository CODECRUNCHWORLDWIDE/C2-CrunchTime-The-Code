# C2 Content Policy — Original Problems Only

This course is published under **GPL-3.0**. Anyone may fork it, teach from it, print it, translate it, and redistribute it. That is only true if every problem in it is ours. This document is the rule that keeps it true.

It is binding on every contributor and every future edit.

---

## The rule

**Every problem posed in this course is written for this course.**

Not restated from somewhere else. Not reskinned from somewhere else. Written.

That covers the problem statement, the constraints, the examples, the test cases, the worked solutions, and the explanatory prose around them.

**And the course does not send the learner to a puzzle catalogue.** Not in a problem, not in a lecture, not in a resources list, not as a pointer to "the same pattern, if you want a judge to run against."

That second half is newer than the first, and it is a house rule rather than a legal requirement — the section below explains what we gave up and why. It is aimed at the ranked, numbered problem catalogues, not at every site on the internet: a mentored track, a contest archive or a peer mock-interview service is a different kind of thing and may still be listed.

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

**Teaching a published method.** FRAME is a *procedure*, excluded from copyright by § 102(b). We teach it in our own words. We do not copy anyone's write-up of it.

**Standard algorithms.** Dijkstra, KMP, Timsort, union-find — algorithms are not copyrightable. Textbook implementations are ours to write. What we may not do is copy a specific author's *implementation*, including their variable names when those are distinctive.

---

## What we gave up, and why

Naming an outside problem was legally fine and we stopped doing it anyway.

The legal position has not changed and is worth keeping on the record, because a future contributor will otherwise assume we were forced. Problem *titles* are not copyrightable — [37 CFR § 202.1(a)](https://www.law.cornell.edu/cfr/text/37/202.1) excludes "names, titles, and slogans." Problem *numbers* are facts (*Feist Publications v. Rural Telephone*, 499 U.S. 340). A hyperlink reproduces nothing at all. And nominative fair use (*New Kids on the Block v. News America Publishing*, 971 F.2d 302) permits naming a platform to say true things about it.

So a line reading "the same pattern appears as problem 51 on such-and-such a site, if you want a judge to run against" was defensible, and the course carried fifty-six of them.

They are gone, for two reasons that are ours rather than the law's.

1. **A pointer is an endorsement, whatever the disclaimer says.** Fifty-six lines sending a learner to one commercial catalogue is a recommendation of it, made by a free course that competes with it. We would rather the course stand on its own material.
2. **It quietly makes the outside catalogue the real syllabus.** Once every page ends by naming its outside twin, the pattern being taught becomes "problem 51" in the learner's head, and our version becomes the practice run. That is exactly backwards, and it undoes the pedagogical dividend the rest of this document is about.

The distinction being drawn is between a *catalogue* and a *resource*. A numbered list of interview puzzles competes with this course and re-anchors its material; a mentored language track, a contest archive, or a peer mock-interview service does not. The second kind stays in the resources lists.

What replaces them is nothing. A learner who wants more repetitions has the stretch section at the foot of every page, and those extend *our* problem rather than pointing away from it.

---

## What is forbidden

This document is the **one place** in the course where an outside platform may be named, because a rule that cannot name what it forbids cannot be enforced. Two entries below name one. Nothing outside this file may.

- Any problem statement taken or adapted from another platform.
- Any example input/output taken from another platform — including their explanation text.
- Any constraint block taken from another platform. **Choose our own bounds, and justify them pedagogically.**
- Any test case taken from another platform, especially judge cases that were never published as examples.
- Any implementation derived from another site's editorial, including its variable naming.
- Any section that announces borrowed provenance: a "Constraints (as published elsewhere)" heading, a "per their spec" aside, or similar. If that phrase is needed, the content underneath is already a violation.
- **Naming or linking a ranked problem catalogue** anywhere in the course — in a problem, a lecture, a resources list, a stretch goal or a further-reading section. That includes the sites whose whole shape is a numbered, tagged list of interview puzzles, and the roadmap sites built on top of one. Mentored tracks, contest archives and peer mock-interview services are not catalogues in this sense and may be listed.
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

> **All problems, examples, constraints and test cases in this course are original work**, written for this course and published under GPL-3.0.

The previous footer disclaimed affiliation with the platforms the course used to name. Nothing names them now, so there is no affiliation left to disclaim, and a disclaimer that mentions a company is itself a mention. If a future edit reintroduces a reference, the trademark disclaimer has to come back with it — which is one more reason not to.

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
