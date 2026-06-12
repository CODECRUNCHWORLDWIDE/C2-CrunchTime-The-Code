# Lecture 3 — The Recruiter-Prep Pack

> **Duration:** ~2 hours.
> **Outcome:** You can assemble the four-piece recruiter-prep pack that converts a finished portfolio into onsite invitations — a one-page resume in the canonical bullet shape with the portfolio linked; a LinkedIn profile optimized for recruiter search; a tiered target-company list of 25–40 companies; and the outreach template trio — and you understand the funnel math that sets how many applications you need in flight.

The portfolio (Lecture 1) is the proof. The mock (Lecture 2) is the rehearsal. This lecture builds the **conversion layer**: the materials that take a finished portfolio and a sharpened interview skill and turn them into actual interviews. A brilliant portfolio that no recruiter ever sees produces zero offers. The recruiter-prep pack is how the portfolio gets seen.

There are four pieces: the resume, the LinkedIn profile, the target-company list, and the outreach template. They are not independent — the resume and LinkedIn both link the portfolio; the target list drives the outreach; the outreach references the resume's strongest line. They are a system. This lecture builds each piece and connects them.

---

## 1. The resume — one page, strong bullets, portfolio linked

The resume is read in about six seconds on the first pass. Every design decision is a response to that six seconds.

### The one-page constraint

Until you have roughly eight years of experience, the resume is **one page**. A recruiter's six seconds is a fixed budget; two pages halves the attention each line gets. The one-page constraint forces the ruthless editing that makes the page strong. If it does not fit, cut the weakest bullets — not the font size.

### The bullet shape

Every bullet is **action verb + what you built + measurable scope or impact**. This is the single most important resume skill, and it is the subject of [Exercise 2](../exercises/exercise-02-resume-rewrite.md).

| Weak | Strong |
|------|--------|
| "Responsible for backend services" | "Designed and shipped three backend microservices handling 40k requests/min" |
| "Helped improve performance" | "Cut p99 API latency 45% by adding a Redis cache layer and query-batching" |
| "Worked on the data pipeline" | "Rebuilt the nightly ETL pipeline, reducing run time from 6 hours to 40 minutes" |
| "Did interview prep" | "Solved 60+ algorithm problems with documented complexity analysis — public portfolio: github.com/you/prep" |

The banned phrases: "responsible for," "helped with," "worked on," "assisted," "familiar with." They describe *presence*, not *achievement*. A bullet that cannot be rewritten into the strong shape is a bullet that does not belong on a one-page resume.

Quantify everything that can be quantified. If you cannot quantify the impact, name the **scope**: "a 14-week, 60-problem portfolio" is a scope even when there is no percentage to cite.

### The projects section links the portfolio

The CrunchTime portfolio is a project — treat it as one. A projects section with one strong bullet and the link:

```
PROJECTS
CrunchTime Interview-Prep Portfolio                    github.com/you/prep
  Solved 60+ data-structure and algorithm problems using the UMPIRE
  framework across 15 weeks; every solution documented with complexity
  analysis and four recorded mock interviews. Public, navigable, indexed
  by pattern.
```

That bullet does triple duty: it is a strong-shape achievement, it links the portfolio (so a curious recruiter clicks through to the proof), and it signals discipline (15 weeks, documented, recorded). For a career-changer or new grad, this is often the strongest item on the resume.

### The skills line matches the job descriptions

The skills line is not a list of everything you have ever touched. It is the set of keywords that match the jobs you are targeting. Pull the recurring phrases from your target job descriptions ("Python, data structures, distributed systems, SQL, REST APIs") and make the skills line mirror them. This matters for the human reader and, at larger companies, for the automated resume screen that filters on keywords.

---

## 2. LinkedIn — the four levers for recruiter search

Recruiters find candidates by *searching*: a keyword (a skill or title) plus a location. Your LinkedIn profile is therefore a search-optimization problem. There are four levers.

### Lever 1 — the headline

The headline is the most-indexed field and the first thing a searcher sees. Weak: "Aspiring software engineer | Open to work" (the word "aspiring" undersells; "open to work" is fine but not search signal). Strong: "Software Engineer | Python, Data Structures & Algorithms | Building [domain] tools". The strong version contains the exact keywords a recruiter searches and reads as a peer, not a hopeful.

### Lever 2 — the About section

Write it in the **first person**, 3–4 short paragraphs: what you do, the thread (same thread as your 90-second self-intro), what you are looking for, and the portfolio link. First person ("I build...") reads as a human; third person ("Jane is a passionate...") reads as a press release and is a tell of an unpolished profile. Repeat your target keywords naturally here — recruiter search reads the About section too.

### Lever 3 — the Featured section

Pin the **portfolio repo** to Featured with a one-line caption: "60+ algorithm problems solved with the UMPIRE framework — public portfolio." Featured is the one place on LinkedIn where you can surface a clickable artifact above the fold. Use it for the portfolio; it is your single best proof point.

### Lever 4 — the skills section

The skills list is filterable: recruiters narrow searches by skill. Order yours so the **top three** are the ones your target roles filter on (likely "Python," "Data Structures," "Algorithms" or your domain equivalents). The top three carry the most weight in search; do not bury them under "Microsoft Word."

The unifying discipline across all four levers: **recruiter search is literal**. Pull the exact phrasings from your target job descriptions and make sure those exact phrases appear in your headline, About, and skills. If the jobs say "distributed systems" and your profile says "scalable backends," the search may not connect you.

---

## 3. The target-company list — the spine of the search

The target list is the spine of the entire job search. Without it, you blast applications untargeted, your outreach is generic, and a strong candidate gets no replies. The list is the subject of [Challenge 1](../challenges/challenge-01-target-list-and-outreach.md).

### Tiering — reach / match / safety

Sort 25–40 companies into three tiers by how your profile compares to the typical bar:

- **Reach (~20%):** above your current bar. High upside, lower odds. The companies you would be thrilled by and slightly intimidated by.
- **Match (~60%):** your profile fits the typical bar. The bulk of the list and the bulk of your real interviews.
- **Safety (~20%):** below your bar; you are likely to get an offer. Not "settling" — these keep the funnel full and give you an offer in hand, which is leverage in negotiating the match-tier offers.

The 20/60/20 split is the default. A list that is all reach produces no interviews and crushing morale; a list that is all safety undersells you and leaves offers on the table. You need all three tiers running at once.

### Named teams and the "why this one" sentence

For each company, name a **team or product** where you can ("Stripe — the payments-reliability team," not just "Stripe"), and write one true, specific **"why this one"** sentence. The sentence is a filter (if you cannot write a true one, the company does not belong on the list) and it is raw material — the outreach message reuses it.

A target-list row:

| Company | Tier | Team/Product | Role link | Why this one |
|---------|------|--------------|-----------|--------------|
| Stripe | Reach | Payments reliability | [link] | I want to work on systems where correctness is non-negotiable, and Stripe's reliability bar is the industry reference. |
| [Mid-size SaaS] | Match | Platform team | [link] | They're scaling the exact ETL problems I rebuilt at my last job; I'd hit the ground running. |
| [Local startup] | Safety | Backend | [link] | Small team, broad ownership, and I already use their product daily. |

---

## 4. The outreach template trio

Cold outreach that gets a reply is short, specific, and makes no ask beyond a 15-minute chat. Three variants.

### Variant A — cold recruiter

```
Subject: SWE interested in [Team] at [Company]

Hi [Name],

I'm a software engineer with [X years / a strong DS&A foundation] in
[domain], and I've been following [Company]'s work on [specific product or
problem]. I'd be a strong fit for the [Role] on [Team] — I recently
[one strong, specific achievement], and I document my problem-solving
process in a public portfolio: [link].

Would you be open to a 15-minute chat about the team and what you're
looking for? Happy to work around your schedule.

Thanks,
[You]
```

Four sentences of substance. It references something real ("[Company]'s work on [specific product]"), names the role, makes one specific claim, links the portfolio as evidence, and asks only for 15 minutes.

### Variant B — warm referral

```
Hi [Name],

[Mutual connection] mentioned you work on [Team] at [Company] and suggested
I reach out. I'm exploring [Role]-type roles and [Company] is high on my
list because [specific, true reason]. My background is [one line]; here's a
portfolio of my recent work: [link].

Would you have 15 minutes to tell me what the team's like and whether it
might be a fit? No pressure either way — really appreciate it.

[You]
```

The warm referral converts an order of magnitude better than cold. Lead with the mutual connection, keep it just as short, and still make no ask beyond 15 minutes.

### Variant C — the follow-up

Sent **once**, 5–7 business days after no reply, then stop:

```
Hi [Name],

Quick nudge on my note from last week — still very interested in [Team] at
[Company] and would value 15 minutes whenever it's convenient. If now's not
a good time, no worries at all; happy to reconnect down the road.

[You]
```

One follow-up, then move on. Repeated follow-ups read as desperate and burn the contact. The rule: nudge once, then let it go.

---

## 5. The funnel math — why the numbers are what they are

The target list is 25–40 and the homework is a 50-application sprint because of the funnel. Rough, order-of-magnitude conversion for a prepared candidate with a portfolio:

| Stage | Rough conversion |
|-------|------------------|
| Application → recruiter reply | ~1 in 8–10 cold; much higher warm |
| Recruiter reply → phone screen | ~1 in 2 |
| Phone screen → onsite | ~1 in 3–4 |
| Onsite → offer | ~1 in 3 |

Multiply it through: from ~50 cold applications you get ~5–6 replies, ~3 phone screens, ~1 onsite, and you need a bit of luck for that to convert to an offer. That is *why* the advice is "weight heavily toward warm referrals" — a warm intro can convert at 1 in 2 at the top of the funnel instead of 1 in 8, collapsing the whole pipeline. The single highest-leverage move in the entire job search is turning cold applications into warm referrals, which is exactly what the outreach trio and the target list's named-team specificity are designed to do.

The takeaway is not "applications are hopeless" — it is "the funnel is real, so keep enough in flight (40–50) and tilt as much as you can toward warm." Track the funnel (the stretch-goal spreadsheet) so the numbers become legible and you can tell whether your bottleneck is at the top (no replies → outreach problem), the middle (replies but no onsites → phone-screen problem), or the bottom (onsites but no offers → interview-performance problem). Each bottleneck has a different fix.

---

## 6. The pieces are a system

A final framing. The four pieces are not a checklist of independent tasks; they are a system that moves a reader from "never heard of you" to "let's schedule the onsite":

- The **target list** decides who you contact and gives you the "why this one."
- The **outreach** uses that "why this one" to start a conversation and links the portfolio.
- The **portfolio** (Lecture 1) is the proof that converts the conversation to interest.
- The **resume and LinkedIn** are the formal artifacts the recruiter forwards internally, both linking back to the portfolio.

Build all four, and link them — resume to portfolio, LinkedIn to portfolio, outreach to portfolio, "why this one" to outreach. The portfolio is the hub; the other three are the spokes that drive traffic to it.

---

## 7. Closing — the conversion layer

Three takeaways:

1. **The resume bullet shape is the whole game.** Action verb + what you built + measurable scope or impact. Ban the weak phrases. Quantify or name the scope. Link the portfolio in projects.
2. **LinkedIn is a search-optimization problem.** Four levers — headline, About, Featured, skills — all tuned to the literal keywords in your target job descriptions. Recruiter search is literal; mirror the job descriptions.
3. **The target list and outreach run on the funnel math.** Tier 20/60/20, name the team, write the "why this one," and tilt hard toward warm referrals — the funnel rewards a warm intro an order of magnitude over a cold application.

This is the conversion layer. The portfolio proves you can do the work; the mock proves you can do it under pressure; the recruiter-prep pack puts both in front of someone who can hire you. Assemble all three this week and you finish the course not "studying for interviews" but running a real job search with a real portfolio behind you.

[Back to the README](../README.md). On to the [capstone spec](../mini-project/README.md).
