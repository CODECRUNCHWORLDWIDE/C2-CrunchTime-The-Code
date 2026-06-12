# Lecture 1 — The Public Portfolio

> **Duration:** ~2 hours.
> **Outcome:** You can turn a pile of 60+ UMPIRE write-ups into a curated, public, navigable portfolio that a hiring manager reads in four minutes — a README that answers who/what/start-here above the fold, an index grouped by the 14 patterns, three or four flagship pieces, and every entry audited to public-ready standard.

Fourteen weeks of patterns are behind you. You have a folder — `umpire-writeups/c2-week-01/` through `c2-week-14/` — with 60-plus markdown files in it. This lecture is about the gap between *that folder* and *a portfolio*. They are not the same artifact, and the difference is the whole subject of the week.

A folder of files is **raw material**. It is private, unindexed, inconsistent in places, full of the asides you wrote to yourself ("stuck for 10 minutes here," "TODO: re-check this trace"), and organized by *when you did the work* rather than *what a reader cares about*. A **portfolio** is the opposite: public, curated, consistent, indexed by pattern, with the asides stripped and a clear "start here." A hiring manager who lands on your portfolio should understand in twenty seconds what they are looking at and, in four minutes, form a confident impression that you run a disciplined problem-solving process.

This lecture has four parts: why the portfolio is a product (not a folder), the README structure, the index-by-pattern, and the public-readiness audit that turns each drill note into a portfolio entry.

---

## 1. The portfolio is a product; the reader is a hiring manager with four minutes

The single mental shift this week requires: **stop thinking of the write-ups as your study notes and start thinking of them as a product with a user**. The user is a hiring manager or recruiter. They are busy, skeptical, and skimming. They have thirty other candidates. They will give your portfolio about four minutes before deciding whether to forward you to the team or close the tab.

Everything about the portfolio's design follows from that user and that four minutes:

- **They land on the README first.** So the README must do the heavy lifting. If the README is a wall of text or, worse, the default GitHub "No README" placeholder, you have lost them before they clicked anything.
- **They skim, they do not read.** So the structure must be scannable: headers, tables, short "start here" links. A reader who has to read three paragraphs to learn what the repo is has already left.
- **They are pattern-matching for signal.** A hiring manager is not going to read all 60 write-ups. They are looking for evidence: "does this person know graphs? DP? Can they communicate?" So you surface that evidence — the index by pattern is the evidence map, and the flagship pieces are the proof points.
- **Consistency is itself a signal.** Sixty write-ups that all have the same six UMPIRE sections in the same order says, without a word, "this person runs a repeatable process." Sixty write-ups in sixty different shapes says the opposite.

The portfolio is not a diary of your learning. It is a *demonstration of your competence*, designed for a specific reader with a specific, short attention budget. Design it for them.

---

## 2. The README — the front door

The README is the entire user experience for the first thirty seconds. It must answer three questions **above the fold** (before any scrolling), in this order:

1. **Who are you?** One line. "Software Engineer focused on backend systems and distributed data." Not your life story — the one line a recruiter would put in their notes.
2. **What is this repo?** One line. "60+ algorithm problems solved with the UMPIRE framework across 15 weeks of structured interview preparation." The reader now knows exactly what they are looking at.
3. **Where do I start?** Three or four links. The flagship pieces. This is the highest-leverage element in the whole portfolio — it tells a skimmer where your best work is so they do not have to hunt.

Below the fold comes the index by pattern, a short "about this portfolio" section, and contact info. The skeleton is in [resources.md](../resources.md#cheatsheet--the-portfolio-readme-skeleton); paste it and fill it.

A few rules for the README specifically:

- **Above the fold is sacred.** The first screenful — roughly the first 15 lines as GitHub renders them — must contain the who, the what, and the start-here. Everything a reader needs to decide "this is worth four minutes" lives there.
- **Use a blockquote for the one-line pitch.** GitHub renders `>` blockquotes with a visual indent that draws the eye. Put your "what is this repo" line there.
- **Links are relative and tested.** `[edit distance](./umpire-writeups/c2-week-11/challenge-01-edit-distance.md)` not an absolute URL. Then click every one after you push — a portfolio with a broken "start here" link is worse than no start-here at all.
- **No emoji-soup, no buzzword-soup.** A clean, plain README reads as senior. A README stuffed with badges, emojis, and "passionate ninja rockstar" reads as junior. Restraint is the signal.

---

## 3. The index by pattern — the evidence map

The reader wants to know what you can do. They think in *capabilities* — graphs, DP, backtracking — not in *weeks*. So the index is grouped by the 14 patterns, not by the 14 weeks. The week is at most a secondary tag.

The index is a table. One row per pattern; the cell lists the write-ups for that pattern as links.

```markdown
## Index by pattern

| Pattern | Write-ups |
|---------|-----------|
| Hash maps & complexity (W2) | [two-sum](...), [group-anagrams](...), [subarray-sum-equals-k](...) |
| Sliding window (W3) | [longest-substring-no-repeat](...), [min-window-substring](...) |
| Fast/slow pointers (W4) | [linked-list-cycle](...), [cycle-start](...), [middle-of-list](...) |
| Binary search (W5) | [search-rotated](...), [koko-bananas](...) |
| BFS (W6) | [level-order](...), [rotting-oranges](...), [word-ladder](...) |
| DFS & topological sort (W7) | [course-schedule](...), [number-of-islands](...) |
| Heaps & priority queues (W8) | [kth-largest](...), [merge-k-lists](...), [top-k-frequent](...) |
| Tries & advanced strings (W9) | [implement-trie](...), [word-search-ii](...) |
| Weighted graphs & union-find (W10) | [network-delay](...), [redundant-connection](...) |
| Dynamic programming (W11–12) | [climbing-stairs](...), [lcs](...), [edit-distance](...), [coin-change](...) |
| Backtracking (W12) | [subsets](...), [permutations](...), [n-queens](...) |
| System design (W13) | [design-url-shortener](...), [design-rate-limiter](...) |
| Mocks (W4, 9, 14, 15) | [mock-1](...), [mock-2](...), [mock-3](...), [mock-4](...) |
```

Three observations:

1. **Every pattern row should have at least two links.** A pattern row with one entry reads as "barely touched this." If a pattern is thin in your portfolio, that is a signal to back-fill (the Monday homework task) — do one or two more write-ups in that pattern before you publish.
2. **The mock row is part of the evidence.** Four mocks with self-feedback notes is itself a strong signal: it says you practice under pressure and you self-correct. Surface it.
3. **The count is the headline.** Somewhere near the top, state the number: "60+ problems." A specific, verifiable number is more persuasive than "many problems." Count yours; if it is 58, do two more and make it 60.

---

## 4. The public-readiness audit — drill note → portfolio entry

This is the part most learners skip, and it is the part that separates an amateur portfolio from a professional one. A drill note and a public portfolio entry are *different artifacts*. The drill note was written for an audience of one — you, two days ago, trying to learn. The portfolio entry is written for a skeptical stranger evaluating you for a job.

Run every write-up through this audit before it goes in the index:

**Audit checklist (per write-up):**

- [ ] **One-line summary at the top.** Immediately under the title, a single line: "2D DP, three-way-min recurrence; O(mn) time, O(min(m,n)) space." A skimmer reads only this line for most entries; it must stand alone.
- [ ] **No private asides.** Delete "I was stuck for 10 minutes," "I always forget this," "TODO," "re-check this." Those were notes to yourself. A stranger reads them as "this person is uncertain."
- [ ] **The code block runs.** Copy the code into a file and run it against the sample cases. A portfolio with code that throws a `SyntaxError` when a hiring manager pastes it is a disqualifier. This is non-negotiable.
- [ ] **All six UMPIRE sections present, in order.** Understand, Match, Plan, Implement, Review, Evaluate. If a section is thin (the Evaluate is often the weakest), strengthen it now. Consistency across all entries is the signal.
- [ ] **Links work.** Internal links to lecture notes or other write-ups must resolve. Click every one after pushing.
- [ ] **Complexity stated and correct.** Every entry ends with the time and space bound, derived, not asserted. A wrong complexity claim in a public portfolio is worse than none.
- [ ] **No typos in the first paragraph.** A skimmer reading the first three lines and hitting a typo downgrades the whole repo. Spell-check at least the top of each file.

The audit is roughly 5–10 minutes per write-up. With 60 write-ups that is 5–10 hours — which is why it is spread across the week and is the bulk of the capstone time budget. Do not try to audit all 60 in one sitting; do the flagship pieces first (they get the most reads), then the rest in pattern order.

### The one-line summary — the highest-leverage edit

Of all the audit items, the **one-line summary** is the highest-leverage. Here is why: a hiring manager skimming your index clicks maybe three entries and reads the first line of ten more. For those ten, the one-line summary *is* the write-up. It must convey the pattern, the key insight, and the complexity in one scannable line.

Weak (no summary, reader has to read three paragraphs to get the gist):

```markdown
# Edit Distance

## Understand
The problem asks us to find the minimum number of operations...
```

Strong (summary stands alone):

```markdown
# Edit Distance (LC 72)

> 2D string-pair DP. State dp[i][j] = min edits to convert s1[:i] to s2[:j].
> Three-way-min recurrence (delete/insert/replace). O(mn) time, O(min(m,n))
> space with rolling row.

## Understand
...
```

A reader who reads only the blockquote knows you understand the problem. That is the goal.

---

## 5. The flagship pieces — choose for range

The "start here" set is three or four write-ups. Choose them to demonstrate **range**, not to show your three easiest wins. A good flagship set covers different families:

- **One dynamic-programming piece** (e.g., Edit Distance) — DP is the highest-signal pattern; a clean DP write-up with the four-step pipeline narrated is the strongest single proof point.
- **One graph piece** (e.g., Course Schedule / topological sort) — graphs are the second-highest signal and show you can model a problem, not just apply a template.
- **One that shows communication** (e.g., your Mock #4 self-feedback, or a write-up with an especially strong Evaluate section) — this proves you can *talk* about your work, which is half of what an interview grades.
- **Optionally, the deep-dive piece** (stretch goal) — if you wrote the 800-word deep dive on your single best problem, that is the strongest flagship of all.

The flagship set is the curation. It says: "If you only read three things, read these — they show I can do the hard patterns and I can communicate." That is exactly the impression a four-minute skim should leave.

---

## 6. Public vs. private — the one judgment call

One decision you must make deliberately: **is the portfolio repo public?** It must be, for a hiring manager to see it without you granting access. But "public" means the whole world can read it, including:

- Your contact info — fine, that is the point. Use a professional email, not a joke handle.
- Your code and reasoning — fine, this is your demonstration.
- Any private asides you forgot to strip — **not fine**. This is the second reason the audit matters: the world sees the "I always mess this up" note you forgot to delete. Audit before you flip the repo to public.

Do not put anything in the portfolio you would not want a hiring manager to read. That includes commit messages — `git log` is public on a public repo, so a commit message like "fixing my dumb mistake again" is visible. Keep the commit history clean enough to survive a skim, or squash it before going public.

---

## 7. Closing — the portfolio is the proof

Three takeaways:

1. **The portfolio is a product with a user.** The user is a hiring manager with four minutes. Every design decision — README structure, index by pattern, flagship set, the audit — follows from that user and that budget. Design for them, not for yourself.
2. **The README does the heavy lifting.** Who, what, start-here, above the fold. If the README is right, the reader gives you the four minutes. If it is wrong, they close the tab in twenty seconds.
3. **The audit is the difference between amateur and professional.** Stripping asides, fixing links, verifying the code runs, adding the one-line summary — this is unglamorous work, and it is exactly the work that makes a portfolio look like it was built by someone who ships. Do not skip it.

The portfolio is the single artifact that proves, publicly and at a glance, that you run a disciplined problem-solving process on any prompt. It is the most valuable thing you build this week. Lecture 2 runs the mock that proves the process holds under pressure; Lecture 3 builds the pack that converts the portfolio into interviews.

[Back to the README](../README.md). On to [Lecture 2 — Mock #4, the Exit Interview](./02-mock-4-the-exit-interview.md).
