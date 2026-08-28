# Week 7 — Exercises

Five exercises. Each one is a **page**: read the brief, copy the starter into
your own `.py` file in your practice repo, fill in the `TODO` blocks, and run
it. The page is the prompt; the file you create is the work.

```bash
python exercise-01-repeater-clusters.py
```

Do them **in order**. They are not five variations on one idea — each one hands
the next a tool it needs.

| # | Exercise | What it drills | Lecture | Difficulty | Target time |
|---|---|---|---|---|---:|
| 01 | [Repeater clusters](./exercise-01-repeater-clusters.md) | The recursive walk, a visited set, one fresh walk per group | 01 | Easy/Medium | 45 min |
| 02 | [Conveyor reachability](./exercise-02-conveyor-reachability.md) | The explicit stack, and the real `RecursionError` that forces it | 02 | Medium | 60 min |
| 03 | [Batch loop audit](./exercise-03-batch-loop-audit.md) | The three colours, and reporting the loop rather than its existence | 03 | Medium | 60 min |
| 04 | [Refit order](./exercise-04-refit-order.md) | Kahn's algorithm — waiting counts, a ready heap, and the leftovers | 03 | Medium | 60 min |
| 05 | [Firmware install order](./exercise-05-firmware-install-order.md) | The same order the other way round: finish a package, then append it | 03 | Medium/Hard | 75 min |

Exercise 1 is deliberately the last page this week where plain recursion is
safe. Exercise 2 is where it stops being safe, and it is the page that shows you
the exception and argues out why raising the limit is not the fix. Exercise 3
adds the two extra colours that turn "have I been here?" into "am I standing on
it?". Exercises 4 and 5 answer the same question — in what order can this be
done? — by two different routes, and the last thing Exercise 5 asks you to do is
say which one you would reach for and why.

---

## How each page is structured

Every page carries the brief, a starter you can paste and run, the answer with
an explanation, and a file you can download to compare against:

```python
"""
Exercise N — Title
"""

# ---- Given data ----
...

# ---- Your task ----
def do_the_thing(...):
    # TODO: implement
    ...

# ---- Self-check ----
if __name__ == "__main__":
    assert do_the_thing(...) == expected
    print("All checks passed.")
```

When the script prints `All checks passed.`, the exercise is done. Nothing here
needs a `pip install` — every exercise runs on the standard library, and most on
nothing but built-ins.

The answer is on the page, under **The Solution**, and it is not hidden behind
anything. Read it *after* you have written something and run it. The gap between
"this should work" and "why does it print that" is where the learning happens,
and reading first closes it for free.

Beside each page sits `<page stem>-solution.py` — the same program, runnable,
under a name that will not collide with the file you are writing.

---

## What is being graded

Phase 1 graded you mostly on getting the right answer. Phase 2 adds a second
axis: **the defence**. For every exercise this week, your write-up has to say
which shape you used — recursive, explicit stack, three colours, Kahn — why you
picked it, and what the other one would have cost. The recording catches whether
you can say it out loud; the write-up catches whether you can write it down.

That is the difference between "the code works" and "the code is the right
code", and it is the thing interviewers are actually listening for.

---

## Tips

- **Run before you write.** Every starter fails on its first run. That is the
  baseline that proves the self-check is real.
- **Read the exception text.** Each page's *Common bugs to catch* is keyed to
  the exact message you are likely to see, captured from a real run.
- **Say the invariant out loud** before you write the loop. "Visited means I
  have been here." "Grey means I am standing on it." If you cannot say it, the
  code will be a guess.
- **Type hints are part of the exercise.** Keep them; they are documentation
  that cannot go stale quietly.

After all five pass, move on to
[Challenge 1 — Chokepoint Mains](../challenges/challenge-01-chokepoint-mains.md),
the hardest depth-first application of the week.
