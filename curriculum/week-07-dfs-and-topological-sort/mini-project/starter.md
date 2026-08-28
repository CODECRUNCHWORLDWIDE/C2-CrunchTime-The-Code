# Mini-Project scaffolding — the two write-ups

This is not a problem page. It is the skeleton you copy into your portfolio repo
for the written half of [the mini-project](./README.md), so you spend your
Saturday writing rather than deciding what to write.

Make this folder in your portfolio repo:

```text
frame-writeups/c2-week-07/mini-project/
├── README.md
├── problem-01-the-loop-audit.md
└── problem-02-the-restart-order.md
```

---

## `README.md` — the overview

```markdown
# Week 7 mini-project — the restart planner

One program, two write-ups. The program plans the restart of a dairy line after
its annual clean: it audits the plan for circular waits, produces a start order,
groups that order into crew waves, and measures what is holding each stage up.

| Write-up | Half | Pattern | Recording |
|---|---|---|---|
| [The loop audit](./problem-01-the-loop-audit.md) | depth-first | three colours, explicit stack | `<link>` (`<mm:ss>`) |
| [The restart order](./problem-02-the-restart-order.md) | topological | Kahn, waves, critical path | `<link>` (`<mm:ss>`) |

**Code:** `<link to your restart-planner.py>`

## What I would do differently next time

<Three or four sentences. Be specific. "I would test the broken plan first"
beats "I would plan better".>
```

---

## Each write-up

Copy this twice, once per half. Keep the headings exactly — they are the five
FRAME steps, and a reader who has read one of your write-ups can then skim any
of them.

```markdown
# <Half> — <one-line description>

> **Recognition, in two lines.**
> This is a <pattern> problem because <the signal in the prompt>.
> The invariant that makes it correct: <one clause>.

## Frame

Restate the problem in your own words. Say what goes in and what comes out, and
name the thing you had to ask about before you could start.

## Research constraints

The bounds, and what each one rules out. The edge cases: empty input, a stage
with no key of its own, a duplicated dependency, a self-loop. What makes this
problem harder than it first looks.

## Assess options

The simple approach first, and what it costs. Then the one you shipped, and
what it costs. Then — and this is the part that is graded — **the other
template, rejected out loud**: what it would have given you, what it would have
cost, and why you did not use it here.

## Make the solution

The code, in the order you wrote it, with the two or three decisions that were
not obvious called out as you reach them.

## Examine

Trace two examples by hand, one of them a failure case. Name one bug you
avoided and how you know. Then the cost: time, space, and one sentence on what
you would improve if this had to run on a graph a thousand times bigger.
```

---

## Two rules that make the pair worth more than two singles

1. **Each write-up rejects the other out loud**, in Assess options. Write-up one
   argues why the colour walk is the right tool for *naming* a loop and what
   Kahn's leftover count would have given instead. Write-up two argues why Kahn
   is the right tool for the order and the waves and what a depth-first
   post-order would have cost.
2. **Each write-up links the other.** Somebody landing on either one should
   reach the whole picture in a click.

The recognition block at the top is what you rehearse. Two lines, under thirty
seconds, said without looking.
