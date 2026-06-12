# Lecture 2 — The Story Bank and the Coverage Matrix

> **Duration:** ~2 hours.
> **Outcome:** You can build a personal story bank of twelve STAR anecdotes from your real experience, give each a retrieval handle, tag each with every category it can answer, lay the whole bank out in a coverage matrix that proves every category is covered by at least two stories, quantify the Result of each story (or substitute a concrete observable), and find and fill the gaps in your coverage before the interview rather than during it.

Lecture 1 gave you the Match step (eight categories) and the Implement step (STAR). This lecture gives you the **preparation artifact** that makes both usable under pressure: the story bank. Without it, every behavioral answer is an improvisation — you hear the prompt, scramble through memory for something relevant, and try to structure it on the fly while talking. With it, the task collapses to *select and deliver*: name the category, retrieve the tagged story, run STAR. The bank is the single highest-leverage thing you build this week, and it is the mini-project deliverable.

The core insight is **reuse**. You do not need a separate story for every possible question, because most stories answer several categories. A good conflict story is often also an influence story and a teamwork story. A good failure story is often also a growth story and a pressure story. Twelve well-chosen, well-tagged stories cover roughly thirty distinct prompts. The coverage matrix is how you *prove* that — and how you find the holes.

This lecture covers the bank, the handle system, the coverage matrix, quantifying results, and gap-filling. Lecture 3 covers recovery, the opener, and the follow-up email.

---

## 1. The story bank — what it is and why it works

A story bank is a small, organized inventory of real anecdotes from your experience, each written once in STAR and tagged with the categories it covers. Twelve is the target — enough for full coverage with redundancy, few enough to actually rehearse cold.

Why a bank beats improvisation, in three points.

**It moves the hard work before the interview.** Recalling a relevant experience, structuring it, deciding what to include, finding the result — that is a lot of cognitive load to carry *while also* speaking fluently and reading the interviewer. The bank does all of that in advance, at your desk, with time to revise. In the room you are left with the easy part: pick and deliver.

**It guarantees coverage.** Improvisation has a failure mode: the prompt lands on a category for which you happen to have no good memory ready, and you stall or tell a weak story. The bank, validated by the coverage matrix, eliminates that failure mode by construction — every category has at least two stories before you walk in.

**It makes you sound *more* authentic, not less.** This is counterintuitive and important. A rehearsed story is not a robotic story. Rehearsal removes the scramble — the "um, let me think of a good example" — and frees your attention for delivery: pacing, the telling detail, eye contact, the landed result. The most natural-sounding answers in the room are the rehearsed ones. Improvisation sounds like improvisation.

---

## 2. The handle system — retrieval under pressure

Each story in your bank gets a short **handle** — a nickname two to four words long that you can think instantly when the category fires. "The migration rollback." "The teammate who went dark." "The 2 a.m. scope cut." "The schema I argued for." The handle is the index key; the full STAR story is the value.

The handle matters because retrieval, not storage, is the bottleneck under pressure. You will not have time to flip through your whole bank in your head. Instead, the flow is: hear the prompt → name the category (five seconds) → recall the one-or-two handles tagged to that category → pick → deliver. The handle is what makes that recall instant. Without handles, you are searching twelve full stories; with handles, you are scanning twelve short labels.

A practical drill: write your twelve handles on a single index card. Have a peer call out categories at random; you respond with the handle(s) you would use, no full story. The goal is sub-three-second recall. When you can do that for all eight categories, retrieval is no longer the bottleneck and you can focus your rehearsal time entirely on delivery.

---

## 3. Quantifying the Result — turning "it went well" into a defensible outcome

A story is not bank-ready until its Result lands. Lecture 1 §5 introduced this; here is the drill.

For each story, write the Result in one of two forms.

**Form A — the metric.** A number that shows impact. "Cut p99 latency from 600ms to 90ms." "Reduced the on-call pages from twelve a week to two." "Shipped on the original date with zero data loss." "Brought test coverage from 40% to 85%, and the next quarter's regression count dropped by half." Numbers are the strongest Result because they are concrete, comparative, and memorable.

**Form B — the concrete observable.** When no honest number exists — and for much real work, none does — substitute a specific, checkable outcome. "The design doc became the team's template for the next three projects." "The runbook meant the following on-call resolved the same incident without escalating." "The bug never recurred in the eight months I was there." "The teammate I unblocked shipped their feature on time and later told the manager the pairing was what made it possible." Each of these is specific and defensible.

The rule: **never fabricate a metric.** A made-up number ("we improved performance by 40%") collapses the instant the interviewer asks "how did you measure that?" — and they will ask, because precise numbers invite precise follow-ups. If you do not have the measurement, use a concrete observable instead. Honesty plus specificity beats a fake precision every time.

The failure to avoid: the Result that is an adjective, not an outcome. "It went really well." "It was a big success." "Everyone was happy." These score nothing because they are unfalsifiable and unspecific. Every story in your bank must end on a metric or a concrete observable. If you cannot produce either for a story, the story is not yet bank-ready — keep the experience, but find the real outcome before you rely on it.

---

## 4. The coverage matrix — proving the bank is complete

The coverage matrix is the artifact that turns twelve loose stories into a *system*. It is a grid: twelve story rows, eight category columns. A cell is checked if that story can answer that category. Building the matrix does three things: it proves every category is covered, it reveals stories that are one-trick (covering only one category — a sign the story is underused or the bank is unbalanced), and it shows you precisely where the holes are.

A worked example. Suppose a learner drafts these twelve handles and tags them:

| # | Handle | Conflict | Failure | Leadership | Teamwork | Ambiguity | Pressure | Influence | Growth |
|---|--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | The schema I argued for | ✓ | | | | | | ✓ | |
| 2 | The reconciliation bug | | ✓ | ✓ | | | ✓ | | |
| 3 | The on-call runbook | | | ✓ | ✓ | | | | |
| 4 | The teammate who went dark | ✓ | | | ✓ | | | ✓ | |
| 5 | The undefined research month | | | ✓ | | ✓ | | | |
| 6 | The 2 a.m. scope cut | | ✓ | | | | ✓ | | |
| 7 | The migration I drove | | | ✓ | ✓ | ✓ | | ✓ | |
| 8 | The code-review feedback | | ✓ | | ✓ | | | | ✓ |
| 9 | The hackathon win | | | ✓ | | | ✓ | | |
| 10 | The junior I mentored | | | ✓ | ✓ | | | | ✓ |
| 11 | The production outage | | ✓ | | | ✓ | ✓ | | ✓ |
| 12 | "Tell me about yourself" | | | | | | | | ✓ |
| | **Category totals** | **2** | **4** | **6** | **5** | **3** | **4** | **3** | **5** |

Read the bottom row. Every category has at least two stories — the acceptance bar. Conflict, at two, is the thinnest; if a loop is known to weight conflict heavily, this learner should add a third conflict story before that loop. No story is a pure one-trick except slot 12 (the opener, which is deliberately single-purpose). Every other story answers two to four categories, which is exactly the reuse that lets twelve stories cover the field.

**The two acceptance rules for the matrix:**

1. **Every category column sums to ≥ 2.** Two stories per category means that if you burn one on an early question, you still have a second for a later one — and you have a choice, so you can pick the *better* fit. A category with only one story is a single point of failure.
2. **Every story row (except the opener) sums to ≥ 2.** A story that answers only one category is underdeveloped or your bank is unbalanced. Re-frame the story to surface a second competency, or replace it with a richer experience. The exception is slot 12, "tell me about yourself," which is the opener and intentionally serves one purpose.

---

## 5. Framing one story for multiple categories

The reuse that makes the matrix dense comes from *framing* — telling the same underlying experience with the emphasis shifted to the asked competency. Consider the "teammate who went dark" story: a teammate stopped responding mid-project and you had to get the work done anyway.

- **Asked as Teamwork:** emphasize how you re-distributed the work, kept the rest of the team unblocked, and protected the teammate's standing rather than throwing them under the bus.
- **Asked as Conflict:** emphasize the hard conversation you had with the teammate when they resurfaced — how you raised the impact without accusation and reached an understanding.
- **Asked as Influence:** emphasize how you got the manager to re-scope the deadline by laying out the situation with data rather than complaint.

Same Situation, same facts, three different Actions emphasized and three different Results landed. The story is one entry in your bank; the framing is selected at delivery time based on the category. This is why the tagging in the matrix is per-category: each tag is a promise that you have rehearsed *that framing* of the story, not merely that the story is vaguely relevant.

A caution: do not over-stretch. If framing a story for a category feels like a reach — if you have to distort the facts to make it fit — do not tag it. A forced fit reads as a non-answer to the interviewer and wastes a question. Tag only the framings you can deliver cleanly and honestly.

---

## 6. Finding and filling gaps

The matrix's real value is showing you what you are missing *before* the interview. Two kinds of gap.

**Thin columns.** A category covered by only one story (or, worse, zero). The fix: mine a new story specifically for that category using the interrogation questions from Lecture 1 §6. If your Conflict column is thin, ask yourself the conflict-surfacing questions across all your experiences — "where did I push back? where did I disagree and engage?" — until you find a second real conflict and write it up.

**Thin rows.** A story that covers only one category. The fix: re-interrogate the experience for secondary competencies. A story you filed as pure Failure almost always also contains Growth (what you learned) and often Pressure (the stakes) or Ambiguity (why the mistake was easy to make). Add the framings and tag them.

A specific, common gap worth naming: many engineers have a thin **Influence** column, because they have plenty of stories where they *did* something but few where they *changed someone's mind*. If yours is thin, look specifically for moments you persuaded — a code-review you won, a design you sold, a manager you convinced to re-prioritize. Influence stories are high-value and frequently asked at senior levels; do not let the column sit at one.

Work the gaps until the matrix satisfies both acceptance rules. The hour you spend filling a thin column at your desk is worth ten times the panic of discovering the gap live, when the interviewer asks the one category you cannot answer.

---

## 7. The minimum viable bank, and the order to build it

If time is short, build the bank in this order, because it front-loads coverage.

1. **One story per category, eight total** — the floor. This alone guarantees you are never caught without *any* answer, which is the single most important property. Build these first.
2. **A second story for the four most-asked categories** — Conflict, Failure, Leadership, Teamwork. These four appear in nearly every loop; a single story each is a single point of failure. Twelve stories, reached.
3. **The opener** — "tell me about yourself," which is slot 12 and is asked in essentially every interview. Rehearse it last but do not skip it; it sets the tone for the whole round (Lecture 3 §2).

An eight-story bank that covers all eight categories beats an unbalanced twelve-story bank that has four conflict stories and no ambiguity story. **Coverage first, depth second.** The matrix is the tool that keeps you honest about which one you actually have.

---

## 8. What to take into Lecture 3

- The story bank is the week's central artifact: twelve real STAR anecdotes, each handled and tagged, that collapse the in-room task to *select and deliver*.
- Handles are the retrieval key. Drill category → handle recall to under three seconds.
- Every story's Result must be a metric or a concrete observable. Never fabricate a number; never end on an adjective.
- The coverage matrix proves completeness: every category ≥ 2 stories, every story (but the opener) ≥ 2 categories.
- One story covers multiple categories through *framing* — same facts, emphasis shifted to the asked competency. Tag only framings you can deliver honestly.
- Use the matrix to find thin columns and thin rows, and fill them at your desk, not in the room. Watch the Influence column especially.
- Coverage before depth. An eight-story bank covering all eight categories beats an unbalanced twelve.

Lecture 3 adds the senior polish: what to do when you realize mid-answer that you pulled the wrong story (recovery), how to deliver the opener that frames the whole loop, how to read the interviewer's follow-ups, what questions to ask them, and how to write the follow-up email that closes the loop. The bank is the material; Lecture 3 is the performance around it.
