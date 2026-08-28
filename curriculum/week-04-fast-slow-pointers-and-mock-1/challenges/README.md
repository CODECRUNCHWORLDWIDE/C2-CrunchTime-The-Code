# Week 4 — Challenges

Two challenges. Both are compositions — the kind of multi-step problem a real
onsite interview is full of, where no single piece is deep but the pieces have
to be named and ordered before you start typing.

| # | Challenge | Sub-patterns | Difficulty | Target time |
|---|-----------|--------------|------------|------------:|
| 1 | [Booklet Imposition](./challenge-01-booklet-imposition.md) | Fast/slow lower middle + in-place reversal + two-chain zip | Medium-Hard | 90 min |
| 2 | [The Feed-Line Weld](./challenge-02-feedline-weld.md) | Tie a loop on purpose + Floyd's detection + the entrance lemma + untie | Medium-Hard | 90 min |

Do all five [drills](../exercises/README.md) first. Both challenges are built
out of pieces the drills already gave you, and neither is worth attempting cold.

**Challenge 1** reuses [Exercise 3](../exercises/exercise-03-midroll-break.md)
as its first sub-step: the lower middle is exactly the last page of the front
half, which is where the cut goes. The other two sub-steps — an iterative
reversal and a two-chain zip — are what it stitches on. Read its *wrong answer
that looks right* section before you start; the commonly published version of
this rewiring interleaves front-first, this spec interleaves back-first, and
every example distinguishes the two.

**Challenge 2** is the opposite shape. It hands you two chains with **no loop
anywhere** and asks you to find where they join. The move is to build a loop on
purpose — tie the end of one chain onto the head of the other — so that
[Exercise 1](../exercises/exercise-01-conveyor-loop.md)'s detection and
[Exercise 2](../exercises/exercise-02-escalation-loop.md)'s entrance lemma both
apply unchanged. Then untie it, on every path out of the function, because a
diagnostic that leaves the plant rewired is a second fault rather than a
finding.

That reduction — *turn this into something I have already solved* — is the most
transferable move in the course, and it is why the week has a second challenge
at all.

## Grading them

Both pages can be solved in the browser with nothing installed; each one links
its own [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/challenges/challenge-01-booklet-imposition.md)
starter. For the week's larger cases — the four-thousand-page booklet that
raises `RecursionError` on a recursive reversal, and the plants that assert the
wiring was restored — use the drill harness:

```bash
cd ../exercises
C2_WEEK04_SOLUTIONS=my_week04_solutions pytest timed_runner.py -v -k "impose or weld"
```

See [`timed_runner.py`](../exercises/timed_runner.py) for the full case list.

When both challenges pass, take the [quiz](../quiz.md), work the
[homework](../homework/README.md), and ship the
[mini-project](../mini-project/README.md) — Mock Interview #1.
