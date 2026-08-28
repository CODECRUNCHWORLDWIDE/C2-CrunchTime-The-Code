# Exercise 4 — Pre-Onsite 4-Week Plan

> **Type:** Capstone build step (planning). **Difficulty:** Straightforward once you have your weakness diagnosis. **Target time:** 1.5 hours. **Why:** When a real onsite gets scheduled — usually 1–4 weeks out — you do not want to improvise the prep. This drill produces `study-plan/pre-onsite-4-weeks.md`: a personalized, week-by-week last-mile sprint built from *your* weaknesses, ready to execute the moment a loop is booked.

This drill is the personalized version of the template in Lecture 3 §4. It depends on the **weakness self-diagnosis** — if you have not done it yet (it is Part 1 of the homework), do the diagnosis first, because the plan is only as good as the targets it is built on.

---

## The template (personalize every cell)

The four-week last-mile plan tapers from breadth to depth to mocks to rest:

| Week out | Theme | Daily volume | Your personalized focus |
|----------|-------|--------------|--------------------------|
| **4** | Breadth + re-diagnose | 2 problems/day, all patterns | _(fill: re-run the weakness diagnosis; touch all 14)_ |
| **3** | Depth on hot patterns + company research | 3 problems/day on your weak patterns | _(fill: your 2–3 hot patterns; the company's eng blog)_ |
| **2** | Full mocks + tailor the story bank | 1 full mock + 2 problems/day | _(fill: which stories to tailor for this company)_ |
| **1** | Taper + logistics + rest | 1–2 easy problems/day | _(fill: setup test, schedule, questions per interviewer)_ |

The taper in week 1 is non-negotiable: cramming the night before makes you tired and anxious — worse, not better. Week 1 is keeping warm, doing logistics, and sleeping.

---

## How to build yours

1. **Pull your weakness diagnosis** (homework Part 1): your ranked 2–3 hot patterns and 1 weak behavior.
2. **Fill Week 4** — list the 14 patterns; plan one touch each (a recognition rep or one problem). The goal is to confirm nothing has gone cold, and to re-rank the hot list.
3. **Fill Week 3** — assign your hot patterns to specific days, 3 problems each. Pick the problem sources now (e.g., the NeetCode roadmap section per pattern: <https://neetcode.io/>) so you are not deciding what to solve at 9pm.
4. **Fill Week 2** — schedule the full mocks (book the stranger sessions a week ahead). List the 3 behavioral stories you will tailor to *this* company's values.
5. **Fill Week 1** — the taper. Logistics checklist: test camera/mic, confirm the schedule, prepare 2–3 questions for each interviewer, plan meals and sleep for the day.

---

## Worked example (built from the Lecture 3 §1 sample diagnosis)

Hot: DP 2D, backtracking, binary-search-on-answer. Weak behavior: still goes silent under pressure. Onsite at a backend-heavy company.

```markdown
# Pre-Onsite 4-Week Plan — <Company>, SWE I, onsite <date>

## Week 4 out — breadth + re-diagnose
- Mon–Fri: 2 problems/day rotating all 14 patterns (recognition focus).
- Sat: re-run the weakness diagnosis. Re-rank hot list.
- Sun: 1 full coding mock (any unseen Medium).

## Week 3 out — depth on hot patterns
- Mon: DP 2D ×3 (NeetCode DP section — edit distance, LCS, grid paths).
- Tue: Backtracking ×3 (subsets, permutations, combination sum).
- Wed: Binary search on answer ×3 (Koko bananas, ship capacity, split array).
- Thu: DP 2D ×3 again (it's the weakest — double the reps).
- Fri: company research — read <Company>'s engineering blog; note their stack.
- Behavior drill all week: every problem solved OUT LOUD, no silent stretch >15s.

## Week 2 out — full mocks + tailor stories
- Mon: full mock (coding + design + behavioral) with a stranger (Pramp/io.io).
- Tue–Thu: 2 problems/day on hot patterns + tailor 3 stories to <Company>'s
  values (ownership, customer-obsession, etc.).
- Fri: full system-design mock (Exercise 2 / Challenge 2 framework).
- Behavior drill: watch the mock; confirm the silence weakness is shrinking.

## Week 1 out — taper + logistics + rest
- Mon–Wed: 1–2 EASY problems/day, just to stay warm. Re-read my 3 best write-ups.
- Thu: logistics — test camera + mic + shared editor; confirm schedule;
  prepare 2–3 questions for each interviewer; plan meals + sleep.
- Fri (day before): rest. No new problems. Sleep 8 hours.
- Onsite day: warm-up with ONE easy problem 90 min before, then go.
```

---

## Acceptance criteria

- [ ] `study-plan/pre-onsite-4-weeks.md` exists in the repo.
- [ ] All four weeks are filled with *your* hot patterns and weak behavior, not the generic template.
- [ ] Week 1 is a genuine taper (light volume), not more cramming.
- [ ] The plan names specific problem sources per hot pattern, so execution requires no further decisions.
- [ ] A logistics checklist is present for the final week.

---

## What to commit

- `study-plan/pre-onsite-4-weeks.md` — the personalized plan.

This file is one of the seven capstone deliverables, and it is the bridge between "I finished C2" and "I have an onsite next month." The homework's full go-forward plan wraps this four-week sprint inside the longer spaced-repetition + application cadence.

---

That is the last drill. Move to [the challenges](../challenges/README.md) — Mock #4 under full real conditions, and the system-design mock.
