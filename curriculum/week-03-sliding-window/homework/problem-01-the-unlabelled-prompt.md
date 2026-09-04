# Problem 1 — The Unlabelled Prompt

> **Topic:** reading a contract that was never written down, then building a fixed-size window against the version you agreed
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Medium
> **Target time:** 90 minutes
> **Why this one:** every drill this week handed you the tie-break, named the sentinel and justified the bounds. Real prompts do none of that. This one is a single sentence from someone who is not a programmer, and the work is noticing the five things it does not say before you write a line of code. The window itself is Exercise 1's, which is the point — the algorithm is the easy half.

## The Brief

A ferry terminal counts how many cars drive up the ramp in each five-minute
slot and logs the counts in order. The operations manager sends you this:

> *"Which half hour was busiest on the ramp, and how full were we on average
> during it?"*

That is the whole prompt. It is one sentence, it is perfectly clear to the
person who wrote it, and it is not enough to write a function from.

Stop before you code and find what is missing. There are five things, and every
one of them changes the answer:

1. **What is a half hour?** Slots are five minutes, so six slots — but is that
   assumed, or should the window size be a parameter? If the terminal ever
   changes its slot length, a hard-coded `6` is a bug waiting to happen.
2. **What comes back?** "Which half hour" could mean the position of the
   window, the count of cars, or both. "How full were we on average" is a third
   number. A function returning one of the three is a function the manager has
   to phone you about.
3. **What if two half hours tie?** Real logs tie constantly, especially at
   quiet times. Somebody has to decide, and if you do not ask, the decision
   gets made by whichever comparison operator you happened to type.
4. **What if the log is shorter than a half hour?** A terminal that opened
   twenty minutes ago has four slots. There is no half hour in the data at all.
   Is that zero, or an error, or nothing?
5. **How is the average rounded?** `25 / 6` is `4.1666...`. Printing that to a
   manager is not an answer. One decimal place? Two? Rounded or truncated?

**The resolutions.** In a real conversation you would ask, and the manager
would answer. Here are the answers this page was written against. They are not
the only defensible set — that is the point — but they are the set you are
building to:

| Question | The answer we agreed |
| --- | --- |
| Window size | Six slots, but as a parameter with `6` as the default |
| Return value | `(start_slot, cars, average)` — position, total, and mean |
| Ties | The **earliest** start wins |
| Log shorter than the window | `None` |
| Rounding | `round(total / slots, 1)` — one decimal place |

Notice that the tie-break here is the **opposite** of Exercise 1's. That was
not an accident when the exercise was written and it is not an accident here.
The manager wants the earliest peak because the earlier one is the one the
morning shift can still be warned about. Same algorithm, different domain,
different rule, and the only way to know is to ask.

**Your job.** Build the window against that agreed contract. The algorithm is
Exercise 1's fixed-size running total, and it should take you fifteen minutes.
Spend the rest of the time on the part that matters: writing the five questions
down in your own words, and being able to say what each of them costs if you
guess wrong.

## Starter

Create `problem-01-the-unlabelled-prompt.py` and paste this in. Fill in every
`TODO`.

```python
"""problem-01-the-unlabelled-prompt.py — the busiest half hour.

The customer asked one sentence. The page lists the five questions it did not
answer, and the resolutions this file is built against.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def busiest_half_hour(boarded: list[int], slots: int = 6) -> tuple[int, int, float] | None:
    """Return the busiest window of consecutive five-minute slots.

    Args:
        boarded: Cars that boarded in each five-minute slot, in time order.
        slots: How many slots make a window. Six five-minute slots is the
            half hour the customer meant.

    Returns:
        (start_slot, cars, average) for the busiest window: its first slot,
        its total, and its cars-per-slot average rounded to one decimal
        place. Ties go to the earliest start. None when the log holds fewer
        than `slots` slots.
    """
    # TODO: resolution 4 — the log may be shorter than one window.
    # TODO: build the first window's total, and seed the best from it.
    # TODO: slide: add the slot coming in, subtract the one going out.
    # TODO: resolution 3 — the tie-break decides your comparison operator, and
    #       it is NOT the one Exercise 1 used.
    # TODO: resolution 2 and 5 — return three things, with the average rounded.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    ramp = [3, 0, 5, 2, 8, 1, 0, 9, 4, 2, 1, 6]
    windows = [sum(ramp[i : i + 6]) for i in range(len(ramp) - 5)]
    print(f"ramp log {ramp}")
    print(f"  half-hour totals by start slot : {windows}")
    print(f"  busiest half hour              : {busiest_half_hour(ramp)}")
    print()

    print(f"flat log, so the tie goes early : {busiest_half_hour([2, 2, 2, 2, 2, 2, 2])}")
    print(f"a quiet night is still an answer: {busiest_half_hour([0, 0, 0, 0, 0, 0])}")
    print(f"one-slot windows                : {busiest_half_hour([4, 9, 9, 1], slots=1)}")
    print(f"log shorter than one window     : {busiest_half_hour([1, 2, 3])}")
    print()

    assert busiest_half_hour(ramp) == (2, 25, 4.2)
    assert busiest_half_hour([2, 2, 2, 2, 2, 2, 2]) == (0, 12, 2.0)
    assert busiest_half_hour([0, 0, 0, 0, 0, 0]) == (0, 0, 0.0)
    assert busiest_half_hour([4, 9, 9, 1], slots=1) == (1, 9, 9.0)
    assert busiest_half_hour([1, 2, 3]) is None
    assert busiest_half_hour([]) is None

    # The window total really is the largest, and it really is the earliest.
    start, cars, average = busiest_half_hour(ramp)
    assert cars == max(windows)
    assert start == windows.index(max(windows))
    assert average == round(cars / 6, 1)

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/homework/problem-01-the-unlabelled-prompt.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `busiest_half_hour(boarded, slots=6)` returns
   `(start_slot, cars, average)` or `None`.
2. `slots` is a parameter with a default of `6`. No literal window size appears
   in the loop.
3. Ties go to the **earliest** start.
   `busiest_half_hour([2, 2, 2, 2, 2, 2, 2])` is `(0, 12, 2.0)`.
4. A log shorter than one window returns `None`.
5. A busiest total of zero is a real answer, not `None`.
6. The average is `round(total / slots, 1)` — a float, one decimal place.
7. The running total is maintained incrementally. Nothing inside the loop may
   call `sum`.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(boarded) <= 300_000`.** A ferry running eighteen hours a day logs
  about 78,000 slots a year, so this covers several years. The bound rejects
  the rescan — recomputing `sum(boarded[i:i + slots])` per position — which the
  drill already established is `O(n · slots)` and will not finish at this size.

- **`1 <= slots`.** A window of zero slots has no meaning, and dividing by it
  for the average would raise `ZeroDivisionError`. Excluding it in the contract
  is cheaper than guarding it in the body, and this is worth noticing: the
  return type *forced* a bound here. A function that returned only a position
  could have tolerated `slots = 0`; one that returns an average cannot.

- **`0 <= boarded[i] <= 400`.** A five-minute slot on a large double-deck ferry
  ramp. Counts are never negative and are frequently zero at night, which is
  what makes Requirement 5 a real requirement rather than a formality.

- **The rounding is part of the contract, not a display choice.** Two callers
  who round differently disagree about the answer, so the rule lives in the
  function. Note also that `round` in Python uses banker's rounding — `round(2.5)`
  is `2`, not `3` — which does not bite at one decimal place here but is the
  sort of thing to check rather than assume when money is involved.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-the-unlabelled-prompt.py
ramp log [3, 0, 5, 2, 8, 1, 0, 9, 4, 2, 1, 6]
  half-hour totals by start slot : [19, 16, 25, 24, 24, 17, 22]
  busiest half hour              : (2, 25, 4.2)

flat log, so the tie goes early : (0, 12, 2.0)
a quiet night is still an answer: (0, 0, 0.0)
one-slot windows                : (1, 9, 9.0)
log shorter than one window     : None

All checks passed.
```

Look at the totals row. Slots 3 and 4 both hold windows totalling 24, and the
winner is neither of them — 25 at slot 2 beats both. Now imagine the log had
one fewer car at slot 2. The two 24s would tie, and *which one you returned*
would come down to a character you typed without thinking about it. That is the
whole lesson of this problem, and it is why resolution 3 exists.

## Steps

1. Before touching the code, write the five questions out in your own words, in
   a file or a notebook. Beside each, write what you would guess if nobody
   answered, and what it would cost if the guess were wrong.
2. Create the file, paste the starter, and run it. Correct starting point.
3. Write the guard for resolution 4.
4. Build the first window and seed the best from it, not from zero.
5. Write the slide. It is Exercise 1's line, unchanged.
6. Choose the comparison operator from resolution 3, and pause on it. If you
   typed `>=` out of habit because that is what Exercise 1 needed, that habit is
   the thing this problem is trying to break.
7. Return all three values, with the average rounded.
8. Now go back to your list of five questions. For each one, change the
   resolution to the other plausible answer and say — out loud, in one sentence
   — which line of your code would have to change. If any of them would need
   more than a line or two, that tells you something about how you structured
   it.

## The Solution

```python
"""problem-01-the-unlabelled-prompt-solution.py — the busiest half hour.

The customer asked one sentence: "which half hour was busiest on the ramp, and
how full were we on average during it?" Everything else — what a half hour is,
what to return, what happens on a tie, what happens on a short log, how the
average is rounded — was never said. The page lists the five questions and the
answers this file was written against.

The algorithm is a fixed-size window with a running total. The teaching is in
the contract, not the loop: the tie-break here is the opposite of the one in
Exercise 1, on purpose.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def busiest_half_hour(boarded: list[int], slots: int = 6) -> tuple[int, int, float] | None:
    """Return the busiest window of consecutive five-minute slots.

    Args:
        boarded: Cars that boarded in each five-minute slot, in time order.
        slots: How many slots make a window. Six five-minute slots is the
            half hour the customer meant.

    Returns:
        (start_slot, cars, average) for the busiest window: its first slot,
        its total, and its cars-per-slot average rounded to one decimal
        place. Ties go to the earliest start. None when the log holds fewer
        than `slots` slots.
    """
    if slots > len(boarded):
        return None

    window_total = sum(boarded[:slots])
    best_total = window_total
    best_start = 0

    for right in range(slots, len(boarded)):
        window_total += boarded[right] - boarded[right - slots]
        # Strict >, because the customer wanted the earliest busiest window.
        if window_total > best_total:
            best_total = window_total
            best_start = right - slots + 1

    return (best_start, best_total, round(best_total / slots, 1))


# ---- Self-check ----
if __name__ == "__main__":
    ramp = [3, 0, 5, 2, 8, 1, 0, 9, 4, 2, 1, 6]
    windows = [sum(ramp[i : i + 6]) for i in range(len(ramp) - 5)]
    print(f"ramp log {ramp}")
    print(f"  half-hour totals by start slot : {windows}")
    print(f"  busiest half hour              : {busiest_half_hour(ramp)}")
    print()

    print(f"flat log, so the tie goes early : {busiest_half_hour([2, 2, 2, 2, 2, 2, 2])}")
    print(f"a quiet night is still an answer: {busiest_half_hour([0, 0, 0, 0, 0, 0])}")
    print(f"one-slot windows                : {busiest_half_hour([4, 9, 9, 1], slots=1)}")
    print(f"log shorter than one window     : {busiest_half_hour([1, 2, 3])}")
    print()

    assert busiest_half_hour(ramp) == (2, 25, 4.2)
    assert busiest_half_hour([2, 2, 2, 2, 2, 2, 2]) == (0, 12, 2.0)
    assert busiest_half_hour([0, 0, 0, 0, 0, 0]) == (0, 0, 0.0)
    assert busiest_half_hour([4, 9, 9, 1], slots=1) == (1, 9, 9.0)
    assert busiest_half_hour([1, 2, 3]) is None
    assert busiest_half_hour([]) is None

    # The window total really is the largest, and it really is the earliest.
    start, cars, average = busiest_half_hour(ramp)
    assert cars == max(windows)
    assert start == windows.index(max(windows))
    assert average == round(cars / 6, 1)

    print("All checks passed.")
```

**Strict `>`, and it is the only interesting character in the function.**

```python
if window_total > best_total:
```

The manager wanted the earliest busiest half hour, so a later window that
merely ties must not displace the incumbent. Exercise 1's manager wanted the
latest, so there it was `>=`. Same loop, same data shape, opposite character,
and no way to know which from the algorithm alone.

This is the general lesson and it is worth stating plainly: **the comparison
operator in a window is a property of the contract, not of the pattern.** Any
time you find yourself typing one by reflex, that is the moment to go back and
check what the prompt actually asked for — or, if the prompt did not say, the
moment to ask.

**The guard covers the empty log for free.** `slots` is at least 1 and
`len([])` is 0, so `1 > 0` is already true and an empty log returns `None`
through the same branch. One condition, two cases, and saying so is worth a
sentence in an interview.

**`slots` stays a parameter.** The manager said "half hour" and the terminal's
slots happen to be five minutes. Both of those are facts about today. A window
size baked into the loop is a function that silently means the wrong thing the
day the terminal moves to ten-minute slots, and nothing will fail — it will
just quietly answer a different question. The default keeps the common call
short; the parameter keeps the function honest.

**Returning three things is a decision, not generosity.** The manager asked two
questions in one sentence, so the answer has at least two parts. The position
is in there as well because "which half hour" without a position is not
actionable — you cannot go and look at the CCTV for a number of cars. Deciding
the return type from what the caller will *do* with it, rather than from what
is easiest to compute, is most of what "reading the contract" means.

**The average is computed once, at the end.** There is no reason to divide
inside the loop: only the winning window's average is ever wanted, and dividing
at every step would be `n` divisions for one answer. It is a small point and it
is the same instinct as Exercise 1's rule about `sum` — do the work once, on
the thing you actually chose.

**Why `round(..., 1)` and not string formatting.** The contract says the
function returns a float. Returning `f"{x:.1f}"` would hand the caller a string
they have to parse before they can compare two of them, and comparing two
rounded strings is a bug generator. Formatting is the caller's job; the
rounding rule is the contract's.

## Run it

Copy the worked answer on this page into `problem-01-the-unlabelled-prompt.py` and run it:

```bash
python problem-01-the-unlabelled-prompt.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-01-the-unlabelled-prompt.py`.

## Common bugs to catch

- **`busiest_half_hour([2, 2, 2, 2, 2, 2, 2])` returns `(1, 12, 2.0)`.** You
  used `>=` — Exercise 1's operator — on a contract that asked for the
  earliest. No traceback. This is the bug the whole problem is built around,
  and if you hit it, that is the exercise working.

- **`ZeroDivisionError: division by zero`.**

  ```text
  Traceback (most recent call last):
      return (best_start, best_total, round(best_total / slots, 1))
                                            ~~~~~~~~~~~^~~~~~~
  ZeroDivisionError: division by zero
  ```

  You called it with `slots=0`. The contract excludes that, and the traceback
  shows you why the exclusion had to exist: the average is what makes zero
  impossible to define.

- **`assert busiest_half_hour(ramp) == (2, 25, 4.2)` fails with `4.166666666666667`.**
  You returned the raw quotient. Resolution 5 is part of the contract; an
  unrounded float is a different answer, and it is the answer that makes two
  callers disagree.

- **`busiest_half_hour([0, 0, 0, 0, 0, 0])` returns `None`.** You seeded
  `best_total = 0` and then treated "never updated" as "nothing found". Six
  empty slots is a real half hour with a real total of zero. Seed from the
  first window.

- **`TypeError: cannot unpack non-sequence NoneType object`.**

  ```text
  Traceback (most recent call last):
      start, cars, average = busiest_half_hour(ramp)
      ^^^^^^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-sequence NoneType object
  ```

  Your function fell off the end without returning — usually a `return` sitting
  inside the `for` loop by one level of indentation.

- **A hard-coded `6`.** No exception, right answers on every test, and
  Requirement 2 unmet. The window size arrived as an argument for a reason.

- **Returning only the total.** You answered half the sentence. Re-read the
  prompt: there are two questions in it, and a third thing the manager needs in
  order to act on either.

## Under the hood

<details>
<summary>Under the hood — the questions worth asking about any prompt, and what "underspecified" costs</summary>

**A checklist that generalises.**

The five questions on this page are instances of a shorter list that works on
almost any coding prompt. Ask them in this order:

1. **What exactly comes back?** Type, shape, and — if it is a container — what
   is in it. "The longest run" is not a return type.
2. **What happens on empty input?** Every collection problem has this case and
   about half of all prompts forget it.
3. **What happens when there is no answer?** And critically: is the "no answer"
   value distinguishable from a valid answer? `0`, `-1` and `[]` are all
   ambiguous in some problems and fine in others.
4. **What happens on a tie?** If the answer is a single item chosen from
   several candidates, ties exist, and somebody decides.
5. **What are the bounds, and are the values signed?** A single negative number
   invalidates whole families of technique — as Exercise 4's non-negativity
   requirement showed.

Asking these takes under a minute and is scored positively in essentially every
interview. Not asking them and guessing right is scored as luck.

**The cost of each wrong guess, on this problem.**

| Guess | What breaks |
| --- | --- |
| Window size hard-coded | Silently wrong the day slot length changes; nothing fails |
| Return only the total | Caller cannot act on it; a second round trip |
| Wrong tie-break | Wrong answer on the quietest days, right on the busiest — so testing on real data hides it |
| Raise on a short log | Caller has to wrap every call in a `try` |
| No rounding rule | Two callers disagree; the bug appears in a report, not in code |

The third row is the interesting one. A wrong tie-break produces a bug that is
*more* likely to hide the more realistic your test data is, because busy
periods rarely tie. Bugs whose visibility is inversely correlated with data
realism are the ones that reach production.

**Why this page ships a resolution table rather than making you guess.**

A homework problem that genuinely withheld the contract could not have a
published answer, because there would be no single right one. The value here is
in doing the noticing *first* — writing your five questions before you scroll —
and then comparing them against the table. If you found four of the five, the
missing one is worth more attention than the code you wrote.

The habit transfers directly to the interview. You will be given a prompt with
holes in it, on purpose, and the holes are part of the assessment.

</details>

## Acceptance checklist

- [ ] `python problem-01-the-unlabelled-prompt.py` prints both sections then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] You wrote the five questions down **before** reading the resolution table.
- [ ] Your comparison operator is `>`, and you can say why it is not `>=`.
- [ ] `busiest_half_hour([0, 0, 0, 0, 0, 0])` returns `(0, 0, 0.0)`.
- [ ] `slots` is a parameter and no literal window size appears in the loop.
- [ ] No call to `sum` appears inside the loop.
- [ ] For each of the five resolutions you can name the line that would change if it were decided the other way.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 homework 1: the unlabelled prompt`.

## Stretch

- **Return every busiest half hour, not just one.** When you return all of
  them, the tie-break disappears — which is a good demonstration that a
  tie-break is a property of the contract rather than of the data.

  ```python
  def all_busiest_half_hours(boarded: list[int], slots: int = 6) -> list[int]:
      """Return the start slot of every window achieving the maximum total."""
      if slots > len(boarded):
          return []
      window_total = sum(boarded[:slots])
      best_total, starts = window_total, [0]
      for right in range(slots, len(boarded)):
          window_total += boarded[right] - boarded[right - slots]
          start = right - slots + 1
          if window_total > best_total:
              best_total, starts = window_total, [start]
          elif window_total == best_total:
              starts.append(start)
      return starts
  ```

  ```text
  [2, 2, 2, 2, 2, 2, 2] -> [0, 1]
  [3, 0, 5, 2, 8, 1, 0, 9, 4, 2, 1, 6] -> [2]
  ```

- **Take the prompt apart again with a harder sentence.** *"Tell me the worst
  stretch of the day for queueing."* Write down every question that raises —
  there are more than five, and at least two of them are about what "worst"
  means. Do not implement it. The exercise is the list.

- **Ask a peer for a one-line prompt from their own work.** Something a
  non-programmer said to them. Write the five questions against it and send
  them back. The fastest way to get good at this is to do it on sentences you
  did not write.

Next: [Problem 2 — The Courier's Zone Count](./problem-02-courier-zone-count.md).
