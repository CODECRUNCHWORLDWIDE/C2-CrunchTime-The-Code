# Homework Problem 3 — Re-narrate the Market Awning

> **Topic:** taking one Week 1 cost section and rewriting it to the five-piece structure, as a rehearsal for the mini-project
> **Lecture:** [03 — Stating Complexity Out Loud](../lecture-notes/03-stating-complexity-out-loud.md)
> **Difficulty:** Easy to do, hard to do honestly
> **Target time:** 30 minutes
> **Why this one:** the mini-project rewrites all five Week 1 cost sections. Doing one of them here, first, gets you into the rhythm and shows you how thin your Week 1 write-up actually was while the discovery is still cheap. The Market Awning is chosen because its tradeoff paragraph is the hardest of the five — there is no "the alternative is wrong" escape hatch, only an honest "the alternative is correct and quadratic".

<!-- no-runnable-file: the deliverable is an edited section of your own Week 1 write-up in your own portfolio repository. No script can rewrite your prose, and the algorithm this page discusses was already shipped in Week 1. The mini-project's complexity-audit-solution.py is the runnable companion to this work. -->

## The Brief

You wrote something in Week 1 that was correct and thin. Almost everybody does.
It probably read like this:

> **Evaluate.** O(n) time, O(1) space.

Six words. Everything in them is true. And it tells a reader nothing about
whether you thought about the problem or remembered a fact about it.

This problem is thirty minutes of turning those six words into half a page that
another engineer would learn something from. One drill, one section. The
mini-project does the other four.

The drill is
[Week 1 Exercise 5 — The Market Awning](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-05-market-awning.md).
A row of poles, a curtain hung between two of them, width `j - i - 1` and height
`min(height[i], height[j])`, and you return the largest area any single pair can
give you. You solved it with converging pointers that always move the shorter
side inward.

The five pieces, from Lecture 3, are: **time**, **space**,
**best / average / worst**, **tradeoffs**, **improvement**. Every cost section
in your portfolio from this week forward has those five, in that order, whether
or not each one has much to say. Sections with a fixed shape are faster to write
and much faster to read, and a piece with nothing in it is itself information —
"no meaningful spread here" is a real finding.

The Market Awning is the interesting one to start with because its tradeoff
paragraph cannot take the easy route. Three of the five Week 1 drills have a
rejected alternative that is *wrong* — it answers a different question, and you
can name the input that proves it. This one does not. Brute force over every
pair gives exactly the same answer on every input; it is simply `O(n^2)`. You
have to write the honest paragraph rather than the dramatic one, and that is a
harder sentence to make sound like something.

## Starter

Open your Week 1 write-up at
`frame-writeups/c2-week-01/exercise-05-market-awning.md` and replace its cost
section with this skeleton. Fill in every bracket.

```markdown
## E — Examine (cost)

*Cost section rewritten in Week 2 to the five-piece structure.*

**Time.** [What does one iteration do? How many iterations are there? Why?]
Therefore **O(_)**.

**Space.** [What did I allocate, and how big does it get?] Therefore
**O(_) auxiliary**.

**Best / average / worst.** [Do they differ here? If they do, name the input
that triggers the best case. If they do not, say so plainly — an invented
spread is worse than an honest "none".]

**Tradeoffs.**
- Alternative: brute force over every pair — O(_) time, O(_) space. [Does it
  give a different answer, or the same answer more slowly? Which constraint
  in the drill rejects it, and what is the arithmetic?]
- I chose the converging scan because [_].

**Improvement.** [Is there a faster algorithm? What is the lower bound, and
why?]
```

Two notes before you start.

**Read your old section cold, before you edit it.** Write down what is thin
about it in a scratch note — that note is raw material for the mini-project's
retrospective, and you will not be able to reconstruct the feeling once you have
fixed it.

**Do not edit the Week 1 problem page.** That file is course material. What you
rewrite is your own write-up in your own portfolio repository.

## Requirements

1. The cost section of `frame-writeups/c2-week-01/exercise-05-market-awning.md`
   follows the five-piece structure, in order.
2. It opens with the visible note *"Cost section rewritten in Week 2 to the
   five-piece structure."* Make the upgrade legible; do not hide it.
3. The **time** piece explains *why* the bound holds — the pointer-movement
   argument — rather than asserting `O(n)`.
4. The **space** piece names what is actually allocated.
5. The **best / average / worst** piece says plainly that there is no meaningful
   spread here, and says why.
6. The **tradeoffs** piece names brute force **with its complexity** and **with
   the arithmetic** that the drill's constraint rejects it by.
7. The tradeoffs piece is honest that the alternative is correct, not wrong.
8. The **improvement** piece names the lower bound and why it is one.
9. The whole section is between about a third and a half of a page, and reads
   aloud in roughly two minutes.

## Constraints

- **Rewrite only the cost section.** Not the whole write-up. The Frame,
  Research constraints, Assess options and Make the solution sections stay as
  they were — they were the work of a different week and they are honest records
  of it. Editing them now would be rewriting history rather than adding to it.

- **You may not claim the alternative is wrong.** It is not. Brute force
  produces the identical answer on every input, and the mini-project's audit
  proves that over 262 inputs. The temptation to reach for the stronger sentence
  is exactly what this problem is inoculating you against — a tradeoff paragraph
  that overstates its case is worse than one that understates it, because an
  interviewer who checks will find the overstatement.

- **Every complexity you state comes with a reason.** "O(n) because the two
  pointers only ever move inward and never move apart, so the total movement is
  bounded by the number of poles" is a cost section. "O(n)" is a fact you might
  have memorised.

- **Two minutes spoken, no notes.** That is the length target, and it is a
  target because it is the length of the answer in a real interview. A section
  that takes five minutes to say has stopped being an answer and become a
  lecture.

## Expected output

There is no program here, so the output is the section itself. This is what
"done" reads like:

```text
## E — Examine (cost)

*Cost section rewritten in Week 2 to the five-piece structure.*

**Time.** O(n). The two pointers start at the ends of the row and each
iteration moves exactly one of them inward. They never move apart, so the
total distance travelled across the whole run is bounded by the number of
poles, and each iteration does a constant amount of work: one min, one
multiply, one comparison against the running best.

**Space.** O(1) auxiliary. Three integers -- two indices and the best area
seen so far. Nothing is copied and nothing is allocated per pole.

**Best / average / worst.** No meaningful spread, and that is worth saying
rather than inventing one. There is no early exit, because a better pair
could always sit further in, so the scan always runs to the point where the
pointers meet. Every input is exactly O(n). Note the contrast with Exercise
3, which shares the converging shape and *can* return early the moment it
finds an exact sum -- same pattern, different termination story.

**Tradeoffs.**
- Alternative: brute force over every pair -- O(n^2) time, O(1) space. It
  gives the *same answer on every input*; it is not wrong, only quadratic.
  The drill bounds the row at 300,000 poles, which is about 4.5x10^10 pair
  evaluations, and that is the constraint that rejects it.
- I chose the converging scan because it buys a whole complexity class for
  the same O(1) space. This is the rare case with no tradeoff to make, only
  a better algorithm, and saying that plainly is better than manufacturing
  a downside.

**Improvement.** None. Any correct solution must inspect every pole height,
because the pole it skipped could have been half of the best pair, so O(n)
is the lower bound and the scan already meets it.
```

Notice three things about that. Every complexity is followed by "because".
"There is no spread" is stated as a finding rather than skipped. And the
tradeoff paragraph tells the truth about an alternative that is correct, which
is a harder and better paragraph than one that gets to say "wrong".

## Steps

1. Open your Week 1 write-up. Read the cost section cold, without editing. Write
   down in a scratch file what is missing — space? the reason for the time
   bound? any alternative at all?
2. Re-read [Lecture 3](../lecture-notes/03-stating-complexity-out-loud.md)'s
   five-piece structure, and the drill's own constraints section for the 300,000
   bound.
3. Paste the skeleton in and fill it top to bottom. Do not skip the
   best/average/worst piece just because the answer is "none" — writing "none,
   and here is why" is the exercise.
4. Do the arithmetic for the brute-force bound yourself:
   `300_000 * 299_999 / 2`. Round it and put the number in. A bound with a
   number attached is a different sentence from a bound without one.
5. Read the finished section out loud with a timer. If it runs over two and a
   half minutes, cut — most likely you explained the algorithm again, which
   belongs in *Make the solution* and not here.
6. Add the "rewritten in Week 2" note at the top, commit, and cross-link from
   the drill file to this homework write-up rather than duplicating the section
   in two places.

## The Solution

The finished section is the block under **Expected output** above — that is the
answer to this problem, in full, and it is deliberately not hidden.

**Why the shape is fixed.** Five pieces, always in the same order, whether or
not each has much to say. A reader who has seen one of your cost sections can
find any piece of the next one without reading it, and you stop deciding what to
include, which is where most of the time goes when a section has no shape. The
cost is that some pieces come out short. That is fine — "no meaningful spread
here" takes one line and is genuinely informative.

**Why the *why* matters more than the bound.** "O(n)" is a fact. Anybody can
memorise it for a problem they have seen. "O(n) because the pointers only move
inward and never apart, so their total travel is bounded by the number of poles"
is an argument, and an argument transfers to a problem you have not seen. It is
also the same argument shape as Exercise 5's disjointness defence this week and
as the amortisation story behind `list.append` — you are building one habit, not
five facts.

**Why the best/average/worst piece is the one people skip, and should not.**
Most write-ups omit it when there is no spread, which loses the information
that there is no spread. Worse, the habit of skipping means that on the drill
where there *is* a real spread — Week 1 Exercise 3, which returns the moment it
finds an exact sum, or this week's Exercise 2, which can finish after two taps —
the omission looks the same and the reader cannot tell the difference. Say
"none, and here is why" and the sections stay comparable.

**Why the honest tradeoff paragraph is the hard one.** Three of the five Week 1
drills let you write the strong sentence: *the alternative is wrong, and here is
the input.* That sentence closes the question. This one does not get it. Brute
force is correct on every input — the mini-project's audit checks 262 of them
and finds no disagreement — so the only true thing you can say is that it is
correct and quadratic, and that the drill's bound is what rejects it.

Resist upgrading that. A tradeoff paragraph that claims an alternative is wrong
when it is merely slow is a claim an interviewer can check in ten seconds, and
finding one overstatement makes them re-examine everything else you said. The
paragraph that says "this alternative is genuinely correct; I rejected it on the
constraint, and here is the arithmetic" is a stronger position precisely because
it gives ground where ground is owed.

**Why the arithmetic goes in.** `4.5 x 10^10` is a number a reader can weigh
against a laptop. "Quadratic is too slow" is a phrase they have to take on
trust. The drill's 300,000 bound was chosen so that this arithmetic works out to
"will not finish", and quoting it demonstrates that you read the constraint as a
*message* rather than as decoration. That reading habit is the thing Lecture 1
is really teaching.

**Why the lower-bound sentence closes it.** "None; every pole must be read,
because the pole you skipped could be half of the best pair" is a proof sketch,
not a shrug. It says you considered whether a better algorithm exists and
established that one cannot. That is a different and much better answer than
leaving the improvement piece blank.

## Download and run

There is no file to download. The deliverable is prose in your own repository,
and the algorithm it discusses was shipped in Week 1.

The check that matters is a reading, not a run. Clone your own portfolio repo
into a temporary folder, the way a stranger would, and read the section:

```bash
cd /tmp
git clone <your-portfolio-url> check
sed -n '/Examine (cost)/,/^## /p' check/frame-writeups/c2-week-01/exercise-05-market-awning.md
```

Then read it aloud with a timer. Two minutes, five pieces, every bound followed
by a reason. Delete `/tmp/check` when you are done.

The runnable companion to this work is the mini-project's
[complexity-audit-solution.py](../mini-project/complexity-audit-solution.py),
which runs the brute-force alternative against the converging scan and reports
that they agree on every input tried. Run that before you write the tradeoff
paragraph; it is the evidence the paragraph rests on.

## Common bugs to catch

- **"O(n) time, O(1) space." and nothing else.** The original problem, restated.
  If your rewrite is under a hundred words you have reformatted rather than
  rewritten. Every piece needs its "because".

- **Claiming brute force is wrong.** It is not. It returns the same integer on
  every input. Run the mini-project's audit if you doubt it — Drill 5's row
  reads `agrees; only slower`, and it is the one row in that table that does.

- **Skipping the best/average/worst piece because there is nothing to say.**
  There is something to say: that there is no spread, and why — no early exit,
  because a better pair could always sit further in. One line. Omitting it makes
  this section incomparable with the ones that do have a spread.

- **Explaining the algorithm again.** The cost section is not the place for "we
  start two pointers at the ends and move the shorter one". That belongs in
  *Make the solution*. If your section runs long, this is almost always why.

- **A bound with no number.** "The brute force is too slow at the drill's
  bound" leaves the reader to do arithmetic you should have done. `4.5 x 10^10`
  is the number.

- **Editing the Week 1 problem page.** `week-01-.../exercises/exercise-05-market-awning.md`
  is course material and not yours to change. Your write-up lives in
  `frame-writeups/c2-week-01/`.

- **Duplicating the section into two files.** Homework Problem 3 and the
  mini-project both cover this drill. Write it once and cross-link. Two copies
  drift, and the moment they do, one of them is teaching you something false.

- **Rewriting all five now.** That is the mini-project, and it is budgeted at
  five to seven hours for a reason. This problem is thirty minutes and one
  drill.

## Under the hood

<details>
<summary>Under the hood — why the greedy move is correct, which is the paragraph your write-up does not have to contain</summary>

Your cost section does not need this proof — the *Make the solution* section is
where a correctness argument belongs, if anywhere. But it is the one genuinely
non-obvious claim in Week 1, and it is worth having straight in your head,
because "why do you move the shorter one?" is a fair follow-up and a common one.

**The claim.** At every step, move the pointer standing at the shorter pole. You
never skip a better pair.

**The argument.** Suppose the pointers are at `i` and `j` and
`height[i] <= height[j]`. Consider every pair that uses `i`: that is `(i, j)`,
`(i, j-1)`, `(i, j-2)` and so on inward. Each of those has width no greater than
`j - i - 1`, because `j` is as far from `i` as anything left to consider. And
each has height at most `height[i]`, because the curtain hangs at the shorter of
the two and `height[i]` is already the shorter here — bringing the far pole
inward can only match or lower it.

So `(i, j)` is at least as good as every remaining pair involving `i`. You have
already measured it. There is nothing left at `i` worth finding, and you can
retire it.

Move the taller pointer instead and that argument does not run, because the
remaining pairs involving `j` can still be *taller* — the limiting height was
`i`, and `i` is still there. Week 1's second example, `[2, 7, 5, 5, 7, 2]`, is
built to punish exactly this: moving the taller side walks away from both 7-metre
poles and reports 8 instead of 14. The code compiles, the trace looks reasonable,
and the answer is wrong.

**Why the tie is not a special case.** When the two heights are equal, the
argument above applies to *both* pointers, so retiring either one is safe.
`<=` retires the left; `<` would retire the right; both are correct. Week 1's
constraint capped heights at 12 precisely so that ties are common and a careless
rule gets caught by a small input rather than by a large one.

**Why this belongs in your head and not in your cost section.** The five pieces
are about *cost*. Mixing a correctness proof into them is the most common way a
two-minute section becomes a five-minute one. Keep the proof in *Make the
solution*, keep the cost section to what it costs, and you will be able to
deliver both without either running long.

</details>

## Acceptance checklist

- [ ] `frame-writeups/c2-week-01/exercise-05-market-awning.md` has a cost
      section with all five pieces, in order.
- [ ] It opens with *"Cost section rewritten in Week 2 to the five-piece
      structure."*
- [ ] The time piece gives the pointer-movement reason, not just the bound.
- [ ] The space piece names the three integers.
- [ ] The best/average/worst piece says there is no spread, and why.
- [ ] The tradeoff piece names brute force with `O(n^2)` time, `O(1)` space, and
      the `4.5 x 10^10` arithmetic.
- [ ] The tradeoff piece says the alternative is correct, not wrong.
- [ ] The improvement piece names the lower bound and its reason.
- [ ] Read aloud, it lands between ninety seconds and two and a half minutes.
- [ ] The drill file cross-links to this write-up rather than duplicating it.
- [ ] The Week 1 course page was not edited.
- [ ] Committed with a message like `Upgrade Market Awning cost section to the five-piece structure`.

## Stretch

- **Do the same for Week 1 Exercise 3, the Widest Ballast Pair, and notice how
  different the tradeoff paragraph gets.** That drill's rejected alternative is
  this week's complement hash map, and it *is* wrong: on
  `[100, 100, 100, 100]` with correction 200 it returns `(0, 1)` where the
  answer is `(0, 3)`. Write both paragraphs back to back and read them aloud.
  The difference between "correct and quadratic" and "returns a different pair,
  and here is the input" is the difference this whole week is teaching.

- **Time yourself delivering all five sections cold**, once the mini-project is
  done. Open a recorder, look at the code and not at the write-up, and speak the
  cost section from memory. Five drills, two minutes each. The first one will be
  ragged and the fifth will be fluent, which is the point — and comparing
  recording one with recording five is the honest measure of whether this week
  landed.

- **Write the version you would say if the interviewer stopped you at thirty
  seconds.** Same content, ruthlessly cut: time with its reason, space, and the
  one sentence of tradeoff that matters. Being able to give the short version on
  demand and then expand it when asked is a separate skill from being able to
  give the long one, and it is the one that actually gets used.

Next: [Homework Problem 4 — The Tradeoff Story](./problem-04-tradeoff-story.md).
