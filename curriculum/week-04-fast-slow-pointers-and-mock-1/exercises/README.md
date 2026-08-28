# Week 4 — Exercises

Five drills. Each one is a full page: the brief, a starter you can paste and
run, the answer with an explanation, and a `-solution.py` beside it you can
download and compare against. Narrate FRAME out loud with the recorder running,
then grade yourself with [`timed_runner.py`](./timed_runner.py).

| # | Drill | Pattern | Difficulty | Target time |
|---|-------|---------|------------|------------:|
| 1 | [The Conveyor Loop](./exercise-01-conveyor-loop.md) | Floyd's detection, then a counting walk to measure the loop | Easy | 30 min |
| 2 | [The Escalation Loop](./exercise-02-escalation-loop.md) | Floyd's plus the cycle-entrance lemma, with the distance counted | Medium | 45 min |
| 3 | [The Mid-Roll Break](./exercise-03-midroll-break.md) | Speed-2 midpoint, lower-middle convention | Easy | 30 min |
| 4 | [The Wear-Level Rotation](./exercise-04-wear-level-rotation.md) | The same three phases on a functional graph — integers, no objects | Easy/Medium | 40 min |
| 5 | [The Relay Hop Budget](./exercise-05-relay-hop-budget.md) | Measure the loop, then answer a huge question with one remainder | Medium | 45 min |

Do them in order; each one leans on the one before it.

Exercise 1 is the simplest use of Floyd's and adds a counting walk. Exercise 2
builds on it with the entrance lemma. Exercise 3 is the variant you will reuse
most — it is the first sub-step of both challenges and of homework Problem 3.
Exercise 4 takes the whole toolkit to a structure with no objects in it at all.
Exercise 5 stops *describing* loops and starts *using* one, which is what cycle
detection is actually for.

## Two opposed conventions, on purpose

Exercises 1, 2, 3 and 5 walk objects, so identity (`is`) is the comparison —
labels, ids and call signs repeat, and several cases exist only to punish `==`.
Exercise 4 walks integers, so equality (`==`) is the comparison, and its large
cases exist only to punish `is`.

Say which world you are in, out loud, every time you start a drill. That habit
is the reason the week is split this way.

## Running the harness

Every drill's page has an [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-01-conveyor-loop.md)
link, so you can solve any of them in the browser with nothing installed. When
you want the week's larger and nastier cases — two-hundred-thousand-chute
sorters, thousand-slot walks above CPython's cached-integer range, the
four-thousand-page booklet that breaks a recursive reversal — point the harness
at your own module:

```bash
pytest timed_runner.py -v
```

By default it imports `solutions.py` from beside itself. To point it somewhere
else:

```bash
C2_WEEK04_SOLUTIONS=my_package.week04 pytest timed_runner.py -v
```

Anything you have not written yet is reported as skipped, so you can run it
after Exercise 1 and watch the skips turn into passes across the week. The node
classes and the builders live in the harness, not in your module — do not
redefine them, and do not convert the chains into lists, because most of these
drills are graded on fixed memory and no test can check that for you.

The harness also covers both [challenges](../challenges/README.md), so a full
run at the end of the week grades all seven problems at once.

When all five drills pass, move on to
[Challenge 1 — Booklet Imposition](../challenges/challenge-01-booklet-imposition.md),
which reuses Exercise 3's lower-middle split as its first sub-step.
