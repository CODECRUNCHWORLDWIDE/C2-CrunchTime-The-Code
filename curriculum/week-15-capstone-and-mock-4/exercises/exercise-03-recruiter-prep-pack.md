# Exercise 3 — The Recruiter-Prep Pack

> Topic: the four artifacts that turn a finished portfolio into interviews · Lecture: [1](../lecture-notes/01-the-capstone-and-portfolio-polish.md) · Difficulty: straightforward and easy to leave undone · Target time: 2.5 hours · Why this one: sixty write-ups nobody has been shown is not a job search. This is the step that converts the work into conversations.

<!-- deliverable-page: the answer is a set of written artifacts, not a program -->

## The Brief

You are about to finish a fifteen-week programme with a portfolio that proves
you can do the work. None of that reaches anybody by itself.

This exercise produces the four artifacts that do the reaching: a résumé whose
bullets say what you built and what it changed, a tiered list of companies to
approach, a cold outreach template, and the follow-up and thank-you templates
you will otherwise write badly under time pressure.

None of it is difficult. All of it is the part people skip, and skipping it is
why good portfolios sit unread.

## Starter

Four parts, and they are below under Requirements. Do them in order — the
résumé bullets feed the outreach template, and the tier list decides how many
of each you need.

Write the résumé bullets first even if your résumé is
already written. The X-Y-Z shape is the thing being drilled, and most existing
bullets do not have it.

## Requirements

### Part A — the resume

Audit your resume against the **Tech Interview Handbook resume guide** (<https://www.techinterviewhandbook.org/resume/>) rather than a homemade rubric. The headline principles:

- **One page.** For early-career, always one page.
- **Bullets are accomplishments, not duties.** Each bullet: *action verb + what you did + the quantified impact.*
- **Prove every claim.** "Familiar with Python" is a duty. The portfolio repo *proves* it; link it.
- **Six-second scan.** A recruiter scans a resume in roughly six seconds. The top third must carry the signal.

### Resume bullet guidance — the X-Y-Z pattern

Google's recruiting team popularized the format: *"Accomplished [X] as measured by [Y] by doing [Z]."* Concretely:

| Weak (duty) | Strong (accomplishment) |
|-------------|--------------------------|
| "Responsible for the checkout page." | "Cut checkout page load time **40%** (3.1s → 1.9s) by lazy-loading below-the-fold components." |
| "Worked on the data pipeline." | "Built an ETL pipeline processing **2M records/day**, reducing report latency from 6h to 20min." |
| "Did interview prep." | "Solved **62 algorithm problems** in a documented framework; portfolio: github.com/me/..." |

Every bullet has a **number**. If you cannot quantify, estimate honestly ("~", "approximately") — a number a recruiter can picture beats an adjective. Link the portfolio repo in the header; it is the proof behind the "interview prep" line.

---

#### The X-Y-Z pattern



### Part B — the tiered target list

`target-companies.md` is a list of companies sorted into three tiers. Tiering keeps you from spending all your energy on five reach companies (and getting five "no"s) or only on safety companies (and underselling yourself).

| Tier | Definition | How many | Strategy |
|------|------------|----------|----------|
| **Reach** | Dream companies; high bar; low odds | 5–8 | Apply, but expect "no"; treat the loops as the best possible mock practice |
| **Target** | Strong fit; realistic odds; you'd happily accept | 15–25 | The core of the funnel; the bulk of your applications go here |
| **Safety** | Solid roles; high odds; good enough to accept | 8–12 | Apply early so you have momentum and a fallback while reach/target loops run |

For each company, record: name, role, why it fits you (one line), application channel (portal / referral / recruiter), and status. A tiny table per tier is enough:

```markdown
## Target

| Company | Role | Why fit | Channel | Status |
|---------|------|---------|---------|--------|
| Acme    | SWE I | Python backend, my strength | referral via J. | applied 6/18 |
| ...     | ...   | ...     | ...     | ...    |
```

Use **levels.fyi** (<https://www.levels.fyi/>) to sanity-check that a target role is worth the loop — not to negotiate (that is C13), just to aim the funnel at roles that match your level and would be worth accepting.

---

### Part C — the cold outreach template

The first message is the hardest and the one people endlessly over-polish. Keep it short, specific, and easy to say yes to. A real, usable template:

```
Subject: SWE candidate — quick question about <Team/Role> at <Company>

Hi <Name>,

I'm an early-career software engineer focused on <area — e.g., backend / Python>.
I came across <Company>'s <specific thing — a role posting, a blog post, a
product> and it's a strong fit for what I'm looking for.

I've spent the last few months on focused interview prep — here's my portfolio
of 60+ documented problem solves and a few recorded mock interviews:
<github link>.

Would you be open to a 15-minute chat about the <Role> opening, or could you
point me to the right person? Happy to work around your schedule.

Thanks for your time,
<Your name>
<phone / linkedin>
```

Why it works: it is **short** (a recruiter reads it in 20 seconds), it is **specific** (names a real thing about the company, so it does not read as mass-mail), it **proves the claim** (the portfolio link), and it makes the **ask small and easy** (15 minutes, or just a pointer). Send 8–12 of these a week (Lecture 3's cadence). Personalize the one specific line per company; reuse the rest.

A note on cold outreach tone: if you want one optional reference on warmth-without-flattery in outreach, "How to Win Friends and Influence People" by Dale Carnegie is the classic — but the template above is enough. Do not over-engineer the first message.

---

### Part D — follow-up and thank-you

Most positive responses come from the **follow-up**, not the first message — people are busy, and a polite nudge after 5–7 business days of silence often gets the reply. Also covered here: the thank-you after an interview.

### Follow-up after silence (5–7 business days)

```
Subject: Re: SWE candidate — <Team/Role> at <Company>

Hi <Name>,

Just floating this back to the top of your inbox in case it got buried — I'm
still very interested in the <Role> at <Company>. Portfolio again for
convenience: <github link>.

No worries at all if the timing isn't right; I'd appreciate a pointer to the
right person if you're not the one to ask.

Thanks,
<Your name>
```

### Thank-you after an interview (send within 24 hours)

```
Subject: Thank you — <Role> interview

Hi <Name>,

Thanks for taking the time to talk through <specific topic from the interview —
e.g., the rate-limiter design / the graph problem> today. I enjoyed
<one genuine specific — e.g., the discussion about how your team handles
on-call>.

I'm even more interested in the <Role> after our conversation. Please let me
know if there's anything else I can provide.

Best,
<Your name>
```

The thank-you is not a formality — it references *one specific thing* from the conversation, which proves you were present and engaged, and it keeps you top-of-mind during the debrief. Send it within 24 hours, while the interviewer still remembers you.

---

## Constraints

- **Every résumé bullet is X-Y-Z**: accomplished X, measured by Y, by doing Z.
  A bullet with no Y is a job description, not an accomplishment.
- **The number is in the bullet**, not implied by it. If you genuinely have no
  number, say what you measured instead and be honest that it is an estimate.
- **Three tiers, and be honest about which is which.** A target list that is
  all reach companies is a plan to be rejected forty times and learn nothing.
- **The outreach template is short.** A cold message that takes two minutes to
  read does not get read. Say who you are, what you built, what you want.
- **Personalise one sentence per message.** Exactly one is enough, and zero is
  visible from orbit.
- **The thank-you goes within 24 hours** and references something specific from
  the conversation. A generic thank-you is worse than none.

## Expected output

What the pack contains when it is done:

```text
resume              1 page, every bullet in X-Y-Z, every bullet with a number
target list         3 tiers, ~10-15 companies, each with a why
outreach template   1 short message + 1 personalised sentence per send
follow-up           1 template, sent 5-7 business days after silence
thank-you           1 template, sent within 24 hours of an interview

committed under     job-search/
```

The résumé is the artifact to spend the most time on and the tier list is the
one to be most honest in. Everything else is a template you will reuse fifty
times, which is why it is worth writing once, properly, now.

## Steps

1. Rewrite every résumé bullet in X-Y-Z. Do this first and expect it to take   the longest.
2. Find the number for each bullet. Where there is none, write the honest   estimate and label it.
3. Build the tier list. Ten to fifteen companies, three tiers, one line of why   each.
4. Write the cold outreach template, then write the personalised sentence for   the first three companies on the list.
5. Write the follow-up and thank-you templates.
6. Send the first three. The pack is not an artifact until it has been used   once.

## The Solution

The worked versions of all four artifacts are in the Requirements above — the
X-Y-Z bullets, the tier table, and both message templates are written out in
full there rather than described.

What is worth adding here is the **judgement** that the templates cannot carry.

**On the résumé.** The bullet that gets read is the first one under your most
recent role. Put the strongest number there, not the most recent work. If your
best number is from two roles ago, it is still your best number and it belongs
where it will be seen.

**On the tier list.** The right shape is roughly a third reach, a half
realistic, and a sixth safety — and the realistic tier is where the offers
come from. Candidates who apply only to their reach tier spend three months
learning nothing, because reach-tier rejections rarely come with feedback.

**On outreach.** The personalised sentence should be about something they
built, not something they wrote about culture. "I read your engineering post
on the migration off the monolith" lands; "I love your commitment to
innovation" does not, and it is the sentence that makes the message look
automated.

**On the follow-up.** One follow-up after five to seven business days, then
stop. A second follow-up converts almost nothing and costs the relationship
with the third.

**On the thank-you.** Reference a specific thing from the conversation — a
problem they described, a trade-off you discussed. It is the only part of the
message that proves you were listening, and it is the only part that matters.

## How to deliver it

- The four `recruiter-prep/` files. (Commit the resume as a PDF; keep the source — `.docx`/`.md` — in the repo too if you like, but the PDF is what recruiters open.)
- A note in `recruiter-prep/target-companies.md` of the three outreach messages sent (date + company), as the first entries in your funnel log.

---

Next: [Exercise 4 — Pre-Onsite 4-Week Plan](./exercise-04-pre-onsite-4-week-plan.md) — your personalized last-mile schedule.

## Common bugs to catch

- **Bullets that describe duties.** Symptom: "responsible for the payments
  service". Nobody was ever hired for a responsibility.
- **No numbers.** Symptom: a résumé that reads as competent and proves nothing.
- **A target list of only reach companies.** Symptom: three months of silent
  rejections and no feedback loop.
- **A long cold message.** Symptom: no replies. Three short paragraphs is the
  ceiling.
- **Zero personalisation.** Symptom: it reads as a mail merge, because it is
  one.
- **Following up three times.** Symptom: a recruiter who now associates your
  name with pressure.
- **A generic thank-you.** Symptom: a message that could have been sent before
  the interview happened.
- **Writing the pack and never sending anything.** Symptom: a complete
  `job-search/` folder and no interviews. Send three before you call this
  done.

## Acceptance checklist

- [ ] `recruiter-prep/resume-v3.pdf` exists, one page, every bullet quantified, portfolio linked, audited against the Tech Interview Handbook guide.
- [ ] `recruiter-prep/target-companies.md` exists with reach / target / safety tiers and 25+ companies total.
- [ ] `recruiter-prep/outreach-template.md` exists — the cold template, ready to personalize.
- [ ] `recruiter-prep/follow-up-template.md` exists — both the silence follow-up and the post-interview thank-you.
- [ ] You have sent at least **three real outreach messages** this week (stretch goal made requirement at the capstone — the funnel starts now).

---

## Stretch

- Have somebody who has hired engineers read your résumé for ninety seconds and
  then tell you, from memory, what you do. The gap between that and what you
  meant is the rewrite.
- Write the second version of the outreach message for a **referral** rather
  than a cold send. It is a different message and it converts several times
  better.
- Draft the answer to "what are you looking for?" in three sentences. It is
  asked on every recruiter screen and it is the answer people most often
  improvise.
