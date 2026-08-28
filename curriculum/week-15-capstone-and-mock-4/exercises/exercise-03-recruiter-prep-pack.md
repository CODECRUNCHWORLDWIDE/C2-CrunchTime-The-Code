# Exercise 3 — Recruiter-Prep Pack

> **Type:** Capstone build step (writing, not coding). **Difficulty:** Straightforward if you have the inputs. **Target time:** 2 hours. **Why:** A polished portfolio with no applications going out is a hobby. This drill builds the three artifacts that turn the portfolio into a job search: a resume that passes the six-second scan, a tiered target list, and the outreach + follow-up templates that fill the funnel.

This drill produces the `recruiter-prep/` folder: `resume-v3.pdf`, `target-companies.md`, `outreach-template.md`, `follow-up-template.md`. The templates below are real, usable text — adapt them, do not invent fancier ones.

> A scope note, per the C2 syllabus: this drill stops at *getting the conversation*. **Compensation, negotiation, leveling, and offer mechanics are out of scope here** — they live in [C13 · Hack the Interview](../../../C13-HACK-THE-INTERVIEW/). Build the outreach; take the negotiation to C13 when an offer lands.

---

## Part A — the resume

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

## Part B — the tiered target-company list

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

## Part C — the outreach template (cold)

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

## Part D — the follow-up + thank-you template

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

## Acceptance criteria

- [ ] `recruiter-prep/resume-v3.pdf` exists, one page, every bullet quantified, portfolio linked, audited against the Tech Interview Handbook guide.
- [ ] `recruiter-prep/target-companies.md` exists with reach / target / safety tiers and 25+ companies total.
- [ ] `recruiter-prep/outreach-template.md` exists — the cold template, ready to personalize.
- [ ] `recruiter-prep/follow-up-template.md` exists — both the silence follow-up and the post-interview thank-you.
- [ ] You have sent at least **three real outreach messages** this week (stretch goal made requirement at the capstone — the funnel starts now).

---

## What to commit

- The four `recruiter-prep/` files. (Commit the resume as a PDF; keep the source — `.docx`/`.md` — in the repo too if you like, but the PDF is what recruiters open.)
- A note in `recruiter-prep/target-companies.md` of the three outreach messages sent (date + company), as the first entries in your funnel log.

---

Next: [Exercise 4 — Pre-Onsite 4-Week Plan](./exercise-04-pre-onsite-4-week-plan.md) — your personalized last-mile schedule.
