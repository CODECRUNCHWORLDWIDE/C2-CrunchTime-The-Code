# Getting Help

You will get stuck. In interview preparation that is not a detour — it *is* the training, because the interview itself is ninety minutes of being stuck in public. But you should never stay stuck for hours alone. Here's how to get unblocked.

## 1. Try this first (the 25-minute rule)

Set a timer for 25 minutes — the same length as a real screen — and work the problem out loud. In that time:

- **Re-read the contract.** Inputs, outputs, the empty case, what the return value actually means. Most "hard" problems are a misread problem.
- **Run FRAME from the top.** If you are stuck, you almost always skipped *Research constraints* or *Assess options* and started coding.
- **Say the invariant out loud.** "The window is always valid" or "everything left of `i` is sorted". If you cannot say it, you do not have an algorithm yet.
- **Shrink the input.** Trace your code by hand on three elements. Not ten. Three.
- **Print, print, print.** Add `print(state)` inside the loop and watch what your code actually does.

If the timer runs out, stop and ask. In a real interview you would have signalled by now — practise that here.

## 2. Ask a good question

A great question gets a great answer. A bad question gets ignored. Use this template:

```text
**The problem:**
Longest substring without repeating characters.

**My approach and why:**
Sliding window with a set, because membership needs to be O(1) and
order doesn't matter.

**What I wrote:**
def length_of_longest(s):
    seen, left, best = set(), 0, 0
    for right, ch in enumerate(s):
        if ch in seen:
            seen.remove(s[left]); left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best

**What I expected:**
length_of_longest("abba") -> 2

**What actually happened:**
3

**Where I'm confused:**
I think shrinking once isn't enough, but I can't state the condition
that says how far to shrink.
```

That last line is the whole question. Half the time, writing it makes you spot your own bug — the "[rubber duck](https://rubberduckdebugging.com/)" effect, which is also exactly what thinking aloud does for you in an interview.

## 3. Where to ask

| Channel | Best for |
| --- | --- |
| [GitHub Discussions](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code/discussions) | Curriculum questions, approach reviews, mock-interview partners |
| [GitHub Issues](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code/issues) | Bugs, typos, broken links, wrong complexity claims |
| [Python Discord](https://discord.gg/python) | Real-time Python help (active around the clock) |
| [Stack Overflow](https://stackoverflow.com/questions/tagged/python) | Specific technical questions |
| [r/cscareerquestions](https://www.reddit.com/r/cscareerquestions/) | Process questions — recruiters, timelines, offers |

Ask for a **review of your approach**, not for the answer. "Is a heap the right structure here, and why not a sorted list?" is a question that makes you better. "What's the solution?" is a question that makes you dependent.

## 4. Searching effectively

Before posting, **search** — but search for the *pattern*, not the problem.

- Searching the problem name gets you someone's solution, which you will remember for a week and lose.
- Searching "when does binary search on the answer apply" gets you the recognition rule, which you keep.
- Copy the **exact error message** (the last line of the traceback) into a search engine, with `python` in the query.
- Check the date on anything you find. Python 2 answers are still everywhere.

## 5. Reading the docs

The [official Python docs](https://docs.python.org/3/) are the single best source of truth. Bookmark them.

- The **Library Reference** answers "what does this function do?" — `heapq`, `collections.deque`, `bisect` and `functools.lru_cache` are the four you will live in.
- The **Tutorial** answers "how does this language feature work?".
- Module docs have runnable examples.

If a tutorial blog post contradicts the official docs, the docs are right.

## 6. Using AI assistants responsibly

Tools like Claude, ChatGPT and Copilot can help — but lean on them carefully, because the interview room does not have one:

- ✅ Use them to **explain** an error, a complexity bound, or a pattern you have already attempted.
- ✅ Use them to **critique your narration** — paste your FRAME write-up and ask where the reasoning is thin.
- ✅ Use them to **generate extra practice** in a pattern you keep failing.
- ❌ Don't paste a drill in and copy back the answer. The drill was the training; you skipped it.
- ❌ Don't let one write your solution. You will pass the drill and fail the screen.

A rule of thumb: if you can't re-derive it on a blank page tomorrow, you didn't learn it today.

## 7. When to stop for the day

Sometimes your brain just needs sleep. After about two hours of being stuck, a break beats persistence — and pattern recognition in particular consolidates overnight. Many problems that were impossible on Tuesday are obvious on Wednesday.

---

**Remember:** asking for help is a skill, and it is a *scored* skill. Interviewers do not penalise a candidate who says "I'm stuck on the shrink condition — can I talk through it?". They penalise silence.
