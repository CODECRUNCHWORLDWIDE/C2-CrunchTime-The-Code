# Week 15 — Final Readiness Self-Assessment

This is the last quiz of C2, and it is different from the pattern-recognition quizzes of the prior weeks. It does not test one pattern — it tests whether you are *ready to apply.* Ten questions across four axes: pattern recognition, behavioral, complexity, and meta-readiness. Some have a clean right answer; the meta-readiness ones are honest self-assessments where the "answer" is a standard you hold yourself to.

Answer all ten before opening the key. Lectures closed. Be honest on the self-assessment questions — inflating them only fools you, and the funnel will correct you anyway.

---

## Pattern recognition

**Q1.** A prompt says: *"Given a sorted array, find the smallest index where `nums[i] >= target`."* Name the pattern and the complexity target.

**Q2.** A prompt says: *"Given a list of course prerequisites as pairs, return an order in which all courses can be taken, or report that it is impossible."* Name the pattern, the data structure, and what "impossible" corresponds to.

**Q3.** A prompt says: *"Find the maximum sum of any contiguous subarray of length exactly `k`."* Name the pattern and why it is `O(n)` and not `O(n·k)`.

## Behavioral

**Q4.** An interviewer asks: *"Tell me about a time you disagreed with a teammate."* In one sentence each, what are the four parts of a strong answer, and which part should consume the most time?

**Q5.** Your behavioral answer so far has been: *"My team built a feature that improved things and everyone was happy."* Name the two biggest problems with this answer against the behavioral rubric.

## Complexity

**Q6.** You solve a problem with a hash map: one pass, storing each element once. State the time and space complexity and the one-line derivation for each.

**Q7.** An interviewer says your `O(n²)` solution is too slow for `n = 10⁵`. Roughly how many operations is `n²` at that size, and why does that matter for a typical 1-second limit?

## Meta-readiness

**Q8.** Can you, right now, deliver a clean 30-second Research-constraints memo on a random Medium from a pattern you have not touched in three weeks — naming the pattern, the cue, the complexity, and one rejected alternative? (Honest yes/no, and which patterns you are *not* yet confident on.)

**Q9.** Across your four mocks, what is the one behavior change that is now reflexive, and the one weakness that is still present in Mock #4? (If you cannot name both, that is itself the answer.)

**Q10.** Do you have, published and public, a portfolio that clears the capstone bar — 60+ audited write-ups, four mock self-feedbacks, a system-design write-up, a story bank, a recruiter pack, and a personalized study plan — that you would send a recruiter *today*? (Honest yes/no.)

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

**Q1 — Binary search (specifically the lower-bound / `bisect_left` variant).** Sorted input + "smallest index where a condition flips from false to true" is the binary-search-on-a-predicate signal. Complexity target `O(log n)`. (The naive linear scan is `O(n)`; the sorted-input cue rules it out.)

**Q2 — Topological sort (DFS or Kahn's BFS).** Build a directed graph (adjacency list) from the prerequisite pairs; "impossible" corresponds to a **cycle** in the graph (a circular dependency means no valid order exists). Kahn's algorithm detects it when fewer than all nodes are emitted; DFS detects it via a node revisited while still on the recursion stack. Time `O(V + E)`.

**Q3 — Fixed-size sliding window.** Compute the first window's sum, then slide: add the entering element, subtract the leaving one — each step is `O(1)`, so the whole scan is `O(n)`. The naive `O(n·k)` recomputes each window's sum from scratch; the window's incremental update is what drops it to `O(n)`.

**Q4 — STAR: Situation, Task, Action, Result.** Situation (the context, ~10s), Task (your specific responsibility, ~10s), **Action (what *you* did — the most time, ~60s)**, Result (the quantified outcome, ~20s). Action consumes the most time because that is where the signal lives — what you specifically did and decided.

**Q5 — (1) No "I", all "we"** — it surfaces no individual ownership signal; the interviewer cannot tell what *you* did. **(2) No quantified result** — "improved things" and "everyone was happy" give the interviewer no number to score; a result without a number is a result they cannot write down in the debrief. (Bonus problem: it is all Situation/Result with no Action — the part that carries the signal is missing entirely.)

**Q6 — Time `O(n)`:** one pass over `n` elements, `O(1)` work per element. **Space `O(n)`:** the hash map holds up to `n` entries. The derivation, not just the bound, is what the Examine (cost) section requires and what a senior states unprompted.

**Q7 — `n² = (10⁵)² = 10¹⁰` operations.** Commodity hardware does roughly `10⁸`–`10⁹` simple operations per second, so `10¹⁰` is ~10–100 seconds — well over a 1-second limit. That is *why* the interviewer flags `O(n²)` at `n = 10⁵`: it does not finish in time, and it signals you need a better-than-quadratic approach (often `O(n log n)` or `O(n)`).

**Q8 — Self-assessment.** A confident "yes" with a short list of *not-yet-confident* patterns is the ready answer. A "no" or a vague "I think so" means the Research constraints step is not yet reflexive across the catalog — those patterns go straight into the **hot tier** of your spaced-repetition schedule (homework Part 2). The value is the honesty: naming the weak patterns is the diagnosis.

**Q9 — Self-assessment from your four mock self-feedbacks.** If you can name both — the reflexive habit *and* the still-present weakness — your self-correction record is intact and the weakness is a known last-mile drill target. If you *cannot* name both, your mocks were not watched honestly enough; re-watch Mock #4 with the trajectory section open. The still-present weakness seeds the homework's weakness diagnosis.

**Q10 — The capstone gate.** A truthful "yes" means C2 is complete and you are ready to apply *now*. A "no" means you know exactly what remains — finish the missing deliverable before you call the course done. This is the one question with real stakes: do not inflate it. A recruiter will open the repo, and a "yes" you cannot back up costs you the conversation.

</details>

---

## How to score

Score the seven objective questions (Q1–Q7) out of 7, then read the meta-readiness questions (Q8–Q10) as gates, not points.

| Q1–Q7 score | Q8–Q10 | Meaning |
|------------:|--------|---------|
| 6–7 | All three honest "yes" | **You are interview-ready. Start applying this week.** Pattern recognition, behavioral structure, and complexity are reflexive; the portfolio is public and clears the bar; your self-correction record is intact. Open your personalized study plan, set the application cadence, and put real applications into the funnel. |
| 6–7 | Q10 is "no" | **Ready on skills; finish the capstone.** Your fundamentals are there, but the portfolio is not yet shippable. Finish the missing deliverable (most often: the audit, the system-design write-up, or the study plan), then apply. Do not apply with a "60+" claim you cannot back up. |
| 4–5 | any | **Close — drill the gaps before applying broadly.** Re-read the lectures for the patterns you missed in Q1–Q3 and re-run any behavioral answer that tripped Q4–Q5. Put the missed patterns in the hot tier of your spaced-repetition schedule. You can start *targeted* applications (safety tier) while you close the gaps. |
| ≤3 | any | **Not yet — more reps needed.** The fundamentals are not yet reflexive. Re-run the weakness diagnosis (homework Part 1), drill the weak patterns hard for two weeks on the spaced-repetition schedule, run one more mock, and retake this assessment. Applying now would waste real loops — and loops are a limited resource. |

This assessment measures **readiness to apply**, not difficulty. The decisive questions are the meta-readiness ones: **Q8** (is Research constraints reflexive across the catalog), **Q9** (is your self-correction record intact), and **Q10** (is the portfolio actually shippable). You can answer Q1–Q7 perfectly and still not be ready if Q10 is a "no" — a recruiter cannot grade skills you have not made public. Be honest; the honesty is the readiness.

---

When done, the final deliverable is next: the [homework](./homework/README.md) — your personalized go-forward study plan.
