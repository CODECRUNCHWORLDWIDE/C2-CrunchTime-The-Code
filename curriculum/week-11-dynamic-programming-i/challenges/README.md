# Week 11 — Challenges

Two challenges. Challenge 1 is required; Challenge 2 is a recommended stretch.

| # | Challenge | Sub-shape | Difficulty | Target time |
|---|-----------|-----------|------------|------------:|
| 1 | [The Timetable Amendment Slip](./challenge-01-timetable-amendment.md) | 2D over two sequences, with a three-way choice and unequal costs | Hard | 75 min |
| 2 | [The Reversible Rake](./challenge-02-reversible-rake.md) | 2D over one sequence read from both ends, filled on the diagonal | Hard | 60 min |

Challenge 1 is the required deliverable. It is the three-way-choice table, and
what makes it a challenge rather than an exercise is that the three edits do not
all cost the same — so the recurrence cannot be copied from anywhere and has to
be derived from the costs on the page.

Challenge 2 is the shape people find hardest to *start*, because the table is not
filled row by row. Entries depend on shorter stretches of the same sequence, so
the fill runs along diagonals, and working out that order before writing anything
is most of the work.

Both have a runnable worked solution beside the page:

```bash
python challenge-01-timetable-amendment-solution.py
```

**How these differ from the exercises.** The reasoning step is harder: there is
more than one valid table shape, and the write-up has to defend the one chosen
and name the one rejected. Both pages also expect an Evaluate section that
compares two implementations rather than describing one. Allocate the full target
time, and spend it before the code rather than during it.
