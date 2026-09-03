# Frequently Asked Questions

## About the program

### Is this really free?

Yes. The curriculum is licensed under [GPL-3.0](../LICENSE.md) — you can read, copy, modify, redistribute, and even teach from it commercially, as long as derivative works stay open source. There are no paid tiers, no upsells, no required services.

### Do I get a certificate?

Not by default — we're a public curriculum, not an accredited institution. However:

- Your **public interview-prep portfolio** — the FRAME write-ups, the mock debriefs, the solved problems with stated complexity — is the artifact that actually holds up in a conversation with a recruiter.
- Communities and instructors running this as a cohort may issue their own.
- The Code Crunch Worldwide community recognizes capstone completions in our showcase.

### How long does it take?

Two pathways, same material. The **intensive** is about 36 hours a week for 15 weeks (~540 hours). The **mastery** pathway is about 10 hours a week for a year (~520 hours). Pick by how much time you actually have, not by how soon you want to be done.

### Which pathway should I pick?

Take the intensive if you are between jobs or your interview cycle starts within about four months. Take the mastery pathway if you are working full-time, or if you want the pattern recognition to still be there next year. The mastery pathway is not the slow track — it is the one that produces durable intuition, because spacing is what makes recall stick.

### I already grind problems on a practice site. Why do I need this?

Because the failure mode this course fixes is not "couldn't solve it". It is "solved it and still got rejected" — no narration, no stated complexity, no recovery when the first approach was wrong. If you have solved two hundred problems and are still failing screens, the missing skill is [the FRAME Method](../README.md#the-frame-method), not more problems.

### I'm strong on some patterns already. Can I skip ahead?

You can. Take the **quiz** at the start of each week — if you score above 80% *and* can narrate a drill from that week out loud without stopping, the week is safe to skim. Do not skip the mock-interview weeks (4, 14, 15) regardless of your scores; they test something the drills don't.

### Can I use this to run a study group or teach a course?

Yes! That's why we built it. See [CONTRIBUTING.md](../CONTRIBUTING.md) and please share your experience back with the community.

---

## About the work

### What does a finished week look like?

- Every **drill** attempted under a timer, whether or not you finished it.
- The week's **challenges** solved, with time and space complexity written down.
- The **homework** committed to your portfolio repo.
- The **mini-project** done, with a README that explains the pattern it drills.
- The **quiz** taken, honestly.

### Do I have to do every drill?

The **homework** and **mini-project** are the must-dos. Drills are "as many as it takes until the pattern is automatic" — for some people that's three, for some it's all of them. Challenges are where the week's learning actually gets tested; don't skip those.

### I got the right answer but couldn't explain it. Does that count?

No, and this is the single most important thing the course teaches. An unexplained correct answer scores below an explained partial one in most real rubrics. Redo it out loud, recording yourself, until the narration is as fluent as the code.

### My solution works but it's ugly. Does that count?

Working code is the first goal. **Clean** code is the second, and in an interview it is scored — a senior engineer is asking "would I accept this in review?". Run `black` and `ruff` (see [coding standards](../resources/coding-standards.md)) and you'll catch most of it automatically.

### Should I memorise solutions?

No. Memorise **templates** — the binary-search boundary template, the sliding-window shrink loop, the BFS queue skeleton, the backtracking frame. Those transfer. Individual solutions don't.

### Can I use AI assistants (Copilot, ChatGPT, Claude)?

See [community/support.md § 6](support.md#6-using-ai-assistants-responsibly). Short answer: yes for explanations and for critiquing your narration, no for solving drills. The interview room does not have one.

---

## About the tools

### Why Python 3.11+?

Python 3.11 brought large performance gains and much better error locations ([PEP 657](https://peps.python.org/pep-0657/)), which matters when you are debugging under time pressure. 3.12 and 3.13 are better still. Use the newest stable release on your platform.

### Do I have to interview in Python?

No, and the patterns are language-independent. But the course's solutions, timed runners and templates are Python, and Python is the fastest language to write correct code in under pressure — fewer lines between you and the idea. If you interview in another language, port the templates in Week 00 and keep them beside you.

### Why VS Code and not PyCharm / Vim / etc.?

VS Code is free, cross-platform, has the lowest learning curve, and the largest Python-extension ecosystem. **Use whatever editor you like** — but do at least a few drills in a plain text box with no autocomplete, because that is what most interview platforms give you.

### Why GPL-3.0 and not MIT?

GPL-3.0 ensures the curriculum stays open. If someone forks it and improves it, those improvements must remain open for everyone. MIT would allow proprietary forks — fine for libraries, but at odds with our mission for an educational resource.

---

## About careers

### Will this get me a job?

This curriculum gives you the *skills* to pass a technical interview loop. Getting the job also requires networking, a resume that survives a six-second scan, applications at volume, and some luck on timing. Skill is necessary but not sufficient — keep that in mind, and start the outreach work in parallel, not after Week 15.

### What kind of roles does this prepare me for?

- Software engineer, entry to mid-level, at companies that run algorithmic screens
- Backend engineer
- Data engineer (with extra SQL depth)
- Any role whose loop includes a live coding round — which is most of them

### It's Week 8 and I have an onsite next week. What do I do?

Stop the sequence and go to the four-week pre-onsite plan in the study plans, compressed. Prioritise: the FRAME narration, the two or three patterns that company is known to ask, and one full mock under real conditions. Breadth will not help you in seven days; fluency will.

### What should I do after Week 15?

- **Keep the pattern rotation alive.** Two problems a week, from patterns you have not seen recently, is enough maintenance.
- **Do mocks with strangers.** Friends are too kind to be useful.
- **Go deeper on system design** if you are targeting mid-level and above — it becomes the deciding round.
- **Contribute back.** Write up a debrief of a real loop and open a PR.

---

## About contributing

### I found a bug / typo / a wrong complexity claim. What do I do?

[Open an Issue](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code/issues/new) or, even better, a Pull Request. Wrong complexity claims are the highest-value bug report in this repo. See [CONTRIBUTING.md](../CONTRIBUTING.md).

### Can I contribute a problem I was actually asked?

Contribute the *pattern*, not the question. Re-set it in a different domain, in your own words. See [CONTENT-POLICY.md](../CONTENT-POLICY.md) for why.

### I want to translate a week into Spanish. How?

Awesome! See [CONTRIBUTING.md § Translations](../CONTRIBUTING.md#translations).

### Can I sponsor / donate?

Code Crunch Worldwide is a learner-led volunteer effort. We don't currently accept donations — but **starring the repo** and sharing it with someone who is job-hunting helps more than you might think.

---

## Anything else?

Open a [Discussion](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code/discussions) and we'll add to this FAQ.
