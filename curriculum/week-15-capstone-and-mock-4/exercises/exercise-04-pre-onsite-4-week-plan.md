# Exercise 4 — The Pre-Onsite Four-Week Plan

> Topic: the last-mile sprint, written before you need it · Lecture: [3](../lecture-notes/03-the-personalized-go-forward-study-plan.md) · Difficulty: straightforward once the weakness diagnosis exists · Target time: 1.5 hours · Why this one: a real onsite gets scheduled one to four weeks out, and that is the worst possible moment to be deciding what to study.

<!-- deliverable-page: the answer is a written plan, not a program -->

## The Brief

When a loop is booked it is usually one to four weeks away. That is exactly the
window in which nobody plans well: the adrenaline is up, every pattern feels
urgent, and the default is to grind whatever problem appears next.

This exercise produces `study-plan/pre-onsite-4-weeks.md` — a personalised,
week-by-week plan built from **your** weaknesses, written now, ready to execute
the moment a loop is scheduled.

It depends on the weakness self-diagnosis, which is Part 1 of this week's
homework. If you have not done it, do it first: the plan is only as good as the
targets it is built on.

## Starter

The four-week last-mile plan tapers from breadth to depth to mocks to rest:

| Week out | Theme | Daily volume | Your personalized focus |
|----------|-------|--------------|--------------------------|
| **4** | Breadth + re-diagnose | 2 problems/day, all patterns | _(fill: re-run the weakness diagnosis; touch all 14)_ |
| **3** | Depth on hot patterns + company research | 3 problems/day on your weak patterns | _(fill: your 2–3 hot patterns; the company's eng blog)_ |
| **2** | Full mocks + tailor the story bank | 1 full mock + 2 problems/day | _(fill: which stories to tailor for this company)_ |
| **1** | Taper + logistics + rest | 1–2 easy problems/day | _(fill: setup test, schedule, questions per interviewer)_ |

The taper in week 1 is non-negotiable: cramming the night before makes you tired and anxious — worse, not better. Week 1 is keeping warm, doing logistics, and sleeping.

---

## Requirements

1. All four weeks filled in, every cell personalised — no template text left.
2. Week 4 lists all fourteen patterns with one touch planned for each.
3. Week 3 names **your** two or three hot patterns and assigns them to days.
4. Week 2 schedules the mocks and names the stories you will tailor.
5. Week 1 is a genuine taper, with the logistics checklist filled in.
6. Problem sources chosen in advance, so no evening starts with a decision.

### How to build yours

1. **Pull your weakness diagnosis** (homework Part 1): your ranked 2–3 hot patterns and 1 weak behavior.
2. **Fill Week 4** — list the 14 patterns; plan one touch each (a recognition rep or one problem). The goal is to confirm nothing has gone cold, and to re-rank the hot list.
3. **Fill Week 3** — assign your hot patterns to specific days, 3 problems each. Pick the problem sources now — a specific book chapter, a specific tag, a specific set — one per pattern, so you are not deciding what to solve at nine in the evening.
4. **Fill Week 2** — schedule the full mocks (book the stranger sessions a week ahead). List the 3 behavioral stories you will tailor to *this* company's values.
5. **Fill Week 1** — the taper. Logistics checklist: test camera/mic, confirm the schedule, prepare 2–3 questions for each interviewer, plan meals and sleep for the day.

---

## Constraints

- **The taper in week 1 is not negotiable.** Cramming the night before makes
  you tired and anxious, which is worse than under-prepared. Week 1 is keeping
  warm, doing logistics, and sleeping.
- **Every cell is personalised.** A plan with template text in it is a template,
  and you will not follow it.
- **Pick the problem sources now.** Deciding what to solve at nine in the
  evening is how an evening gets spent deciding.
- **Book the mocks a week ahead.** Week 2's mocks only happen if week 3 books
  them.
- **Two or three hot patterns, not six.** A plan that targets everything targets
  nothing, and four weeks is not long.
- **The plan is built from the diagnosis**, not from what you enjoy practising.
  Those are rarely the same list.

## Expected output

What a finished plan looks like:

```text
week 4 out    breadth        2 problems/day, all 14 patterns touched, re-diagnose
week 3 out    depth          3 problems/day on 2-3 named hot patterns
week 2 out    mocks          1 full mock + 2 problems/day, 3 stories tailored
week 1 out    taper          1-2 easy problems/day, logistics, sleep

cells filled  all of them, with your patterns and your dates
sources       named per pattern, chosen in advance
mocks         booked, not intended
committed at  study-plan/pre-onsite-4-weeks.md
```

Notice the daily volume **falls** in the last week. That is the part people
rewrite when they get nervous, and rewriting it is the mistake the plan exists
to prevent — which is exactly why it is written now, calmly, rather than then.

## Steps

1. Pull your weakness diagnosis: the ranked two or three hot patterns and the   one weak behaviour.
2. Fill week 4. List all fourteen patterns; plan one touch each.
3. Fill week 3. Assign hot patterns to specific days and name the source for   each.
4. Fill week 2. Schedule the mocks with dates; list the three stories to tailor.
5. Fill week 1. The taper, plus the logistics checklist: camera and microphone   tested, schedule confirmed, two or three questions per interviewer, meals and   sleep planned.
6. Read it back and cut anything you would not actually do on a Tuesday.

## The Solution

Hot: DP 2D, backtracking, binary-search-on-answer. Weak behavior: still goes silent under pressure. Onsite at a backend-heavy company.

```markdown
# Pre-Onsite 4-Week Plan — <Company>, SWE I, onsite <date>

## Week 4 out — breadth + re-diagnose
- Mon–Fri: 2 problems/day rotating all 14 patterns (recognition focus).
- Sat: re-run the weakness diagnosis. Re-rank hot list.
- Sun: 1 full coding mock (any unseen Medium).

## Week 3 out — depth on hot patterns
- Mon: DP 2D ×3 (two-string tables and a grid: an edit-cost table, a longest-common-run table, a route count).
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

Two things in that plan are worth copying rather than the specifics.

**The volume curve.** Two problems a day, then three, then one mock plus two,
then one or two easy ones. It rises into week 2 and falls into week 1. Almost
every plan people write on their own rises all the way to the door, and almost
every one of those plans produces a tired candidate.

**The re-diagnosis in week 4.** The hot list you write today will be wrong by
the time the loop is booked, because you will have kept practising. Building
the re-diagnosis into week 4 is what keeps the plan from targeting a weakness
you already fixed.

## How to deliver it

- `study-plan/pre-onsite-4-weeks.md` — the personalized plan.

This file is one of the seven capstone deliverables, and it is the bridge between "I finished C2" and "I have an onsite next month." The homework's full go-forward plan wraps this four-week sprint inside the longer spaced-repetition + application cadence.

---

That is the last drill. Move to [the challenges](../challenges/README.md) — Mock #4 under full real conditions, and the system-design mock.

## Common bugs to catch

- **Leaving template text in a cell.** Symptom: a plan you will not follow,
  because it is not yours.
- **A flat or rising volume curve.** Symptom: a tired candidate on the day. The
  taper is the design.
- **Six hot patterns.** Symptom: four weeks of shallow passes over everything.
- **Mocks intended rather than booked.** Symptom: week 2 arrives with no
  partner and the mocks quietly become more problems.
- **No named sources.** Symptom: half of each evening spent choosing.
- **Building the plan from what you like practising.** Symptom: a plan that is
  pleasant and targets nothing the diagnosis found.
- **Skipping the logistics checklist.** Symptom: a camera problem in the first
  five minutes of the loop, which costs more than any pattern.

## Acceptance checklist

- [ ] `study-plan/pre-onsite-4-weeks.md` exists in the repo.
- [ ] All four weeks are filled with *your* hot patterns and weak behavior, not the generic template.
- [ ] Week 1 is a genuine taper (light volume), not more cramming.
- [ ] The plan names specific problem sources per hot pattern, so execution requires no further decisions.
- [ ] A logistics checklist is present for the final week.

---

## Stretch

- Write the **two-week** version. Some loops are booked ten days out, and
  compressing this plan under time pressure produces a worse one than deciding
  now what you would cut.
- Write the day-of schedule: wake time, what you review, what you eat, when you
  stop looking at anything. It is fifteen minutes now and it removes every
  decision from the worst morning to be making decisions.
- Add a per-week check: one sentence you will write at the end of each week
  saying whether the plan is working. A plan with no feedback step is a wish.
