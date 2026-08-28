# Capstone Project Master Guide

> The capstone is your portfolio centerpiece — a single public repository proving that you can solve algorithmic problems *and explain yourself while you do it*, built week by week from Week 01 through Week 15.

This document is the **single source of truth** for what the capstone is, how it is graded, and how to submit it. The Week 15 curriculum folder ([curriculum/week-15-capstone-and-mock-4/](../../curriculum/week-15-capstone-and-mock-4/)) breaks the same content into a day-by-day plan, and its [mini-project spec](../../curriculum/week-15-capstone-and-mock-4/mini-project/) carries the full directory layout and README-cover template. Consult this file when you need the whole picture in one place.

---

## At a glance

| Aspect              | Detail                                                                            |
| ------------------- | --------------------------------------------------------------------------------- |
| Duration            | Built across all 15 weeks; ~7 hours of assembly and polish in Week 15             |
| Deliverable         | A public GitHub repository, `crunchtime-interview-prep-<yourhandle>`               |
| Format              | Write-ups, recordings and documents — not an application                          |
| Required submission | Repo URL + the Mock #1 → #4 trajectory note                                        |
| Audience            | Yourself, recruiters, hiring managers, the open-source community                   |

---

## Why a capstone?

Three reasons:

1. **Proof beats claims.** Anyone can say they are good at algorithms. Sixty-plus FRAME write-ups with stated complexity, four recorded mocks, and a commit history spanning fifteen weeks is evidence.
2. **You leave with something durable.** Certificates expire in a recruiter's attention within seconds. A public repository that shows how you think does not.
3. **The trajectory is the signal.** Mock #1 next to Mock #4 shows whether you can self-correct — and self-correction is what a senior engineer is actually reading for when they ask themselves whether you will grow on the job.

---

## This is not built in Week 15

Unlike a build-a-project capstone, nothing here is created from scratch at the end. Every week feeds the same repository:

- **Week 01** creates it, with five array write-ups.
- **Weeks 02–12** add a pattern each, plus the week's mini-project write-ups.
- **Weeks 04, 09, 14** add the first three recorded mocks.
- **Week 13** adds the behavioral story bank and coverage matrix.
- **Week 15** audits the lot, adds Mock #4, the system-design write-up, the recruiter-prep pack, the four-week plan, the badges, and the README cover.

If you have skipped mini-projects along the way, Week 15 is not enough time to backfill them. Do them in the week they belong to.

---

## What "done" looks like

Your capstone repo MUST include:

- **A README cover** that a recruiter can read in ninety seconds: who you are, what the repo is, and a progress dashboard with the headline numbers — write-up count, patterns covered, mocks recorded, system-design write-ups.
- **60+ FRAME write-ups** in `frame-writeups/`, each stating the problem contract, the approach considered *and rejected*, the chosen approach with a reason, and time and space complexity.
- **Four recorded mocks** in `mocks/`, each with honest two-pass self-feedback, ending with the Mock #1 → #4 trajectory note.
- **A system-design write-up** in `system-design/`.
- **A behavioral story bank** in `behavioral/` — twelve stories against the eight categories, with the coverage matrix.
- **A recruiter-prep pack** in `recruiter-prep/`.
- **A personalized study plan** in `study-plan/` covering the next four weeks and beyond.
- **Three honestly-earned badges** in `badges/`: `frame-apprentice`, `pattern-practitioner`, `crunchtime-graduate`.
- **Clean git history.** Sustained commits across fifteen weeks; no single "add everything" commit at the end.
- **A `LICENSE`** for your own work (CC-BY-4.0 or MIT are both fine — C2 itself stays GPL-3.0).
- **A `.gitignore`** excluding `__pycache__/`, `.venv/`, `.env`.

Full acceptance criteria and the README-cover template: [week-15 mini-project](../../curriculum/week-15-capstone-and-mock-4/mini-project/).

---

## The Week 15 plan

| Stage | Milestone                                                                                                      | Output                                     |
| ----- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 1     | [Portfolio audit](../../curriculum/week-15-capstone-and-mock-4/exercises/exercise-01-portfolio-audit.md)         | Every write-up graded against the quality bar |
| 2     | [System-design write-up](../../curriculum/week-15-capstone-and-mock-4/exercises/exercise-02-system-design-writeup.md) | One design documented end to end       |
| 3     | [Recruiter-prep pack](../../curriculum/week-15-capstone-and-mock-4/exercises/exercise-03-recruiter-prep-pack.md) | Resume, pitch, questions, target list      |
| 4     | [Mock #4, full loop](../../curriculum/week-15-capstone-and-mock-4/challenges/challenge-01-mock-4-full-loop.md)   | Recording + self-feedback                  |
| 5     | [System-design mock](../../curriculum/week-15-capstone-and-mock-4/challenges/challenge-02-system-design-mock.md) | Recording + self-feedback                  |
| 6     | [Four-week pre-onsite plan](../../curriculum/week-15-capstone-and-mock-4/exercises/exercise-04-pre-onsite-4-week-plan.md) | A written plan you will actually follow |
| 7     | README cover, badges, final push                                                                                | The repo goes public                       |

Push commits every day. Visible progress beats invisible perfection — and the commit graph is part of the artifact.

---

## Rubric

The scored rubric lives with the deliverable, in [week-15 mini-project § Rubric](../../curriculum/week-15-capstone-and-mock-4/mini-project/#rubric). In summary, it weights:

- the **write-up corpus** — count, coverage across patterns, and the quality bar
- the **mock record** — four recordings with honest self-feedback and the trajectory note
- the **supporting artifacts** — system design, behavioral bank, recruiter pack, study plan
- the **README cover** — whether the ninety seconds land
- **commit history and polish** — sustained work, honest badges

A capstone that clears the rubric is one you can send to a hiring manager unedited.

---

## Submission

When you're done:

1. **Repo must be public** on GitHub.
2. **Pin it** to your GitHub profile (Profile → Customize your pins).
3. **Host your mock recordings** somewhere streamable and link them from `mocks/`, or keep them private and say so — an unlisted link is fine, a broken one is not.
4. **Link the repo** from your resume and your LinkedIn.
5. **Open a Discussion** on this curriculum repo's [Discussions](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code/discussions) with: repo URL, your Mock #1 → #4 trajectory note, and what you would do differently.

The Code Crunch Worldwide community celebrates capstones in a monthly showcase — sharing is encouraged.

---

## After the capstone

You're done with the course. Now go interview.

- **Apply while the fluency is fresh.** The half-life of interview sharpness is short. Do not spend another month preparing.
- **Keep a maintenance rotation.** Two problems a week from patterns you have not touched recently.
- **Mock with strangers.** Friends are too kind to be useful.
- **Go deeper on system design** if you are targeting mid-level and above — it becomes the deciding round.
- **Mentor someone going through this curriculum.** Teaching is the strongest test of mastery, and explaining a pattern to a beginner is the same skill as explaining it to an interviewer.

---

## Questions?

- **"I have fewer than 60 write-ups."** → Ship what you have and say the real number. An honest 42 reads better than an inflated 60 you cannot defend.
- **"My Mock #1 is embarrassing."** → Keep it. The delta is the point. Deleting it deletes the evidence of growth.
- **"Can I make the repo private?"** → You can, but then it is not a portfolio. Private repos cannot be read by the person you are trying to convince.
- **"Can I use AI to help?"** → Yes, for explanations and for critiquing your narration. No, for writing the write-ups — see [community/support.md](../../community/support.md#6-using-ai-assistants-responsibly).

Good luck. Build the thing you would want to be judged on.
