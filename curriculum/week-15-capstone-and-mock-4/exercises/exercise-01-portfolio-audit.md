# Exercise 1 — The Portfolio Audit

> Topic: bringing fifty write-ups to one bar before adding the last ten · Lecture: [1](../lecture-notes/01-the-capstone-and-portfolio-polish.md) · Difficulty: mechanical but exacting · Target time: 2.5 hours · Why this one: a recruiter opens a *random* write-up, not your best one. If the random one has a half-finished Evaluate section, they distrust all sixty.

<!-- deliverable-page: the answer is an audited repo and its audit log, not a program -->

## The Brief

This is the first step of the capstone week. Your portfolio repo has been
growing since Week 1 and holds roughly fifty write-ups. Before adding the
final ten or more to clear sixty, you audit what is already there.

Two reasons, and the second is the real one. It is faster to fix a weak
write-up than to write a new one. And the dashboard count on your README has
to be **true** — the number of write-ups that clear the bar, not the number of
files in the folder. A count that is really a file count is the first thing a
careful reader catches, and everything after it is discounted.

The deliverable is the fixed write-ups, an audit log, and a corrected count.

## Starter

The six-point bar is the starter. Every write-up in the repo — every one — has
to clear all six.

Every write-up — every one — must clear all six:

| # | Bar | Pass looks like |
|---|-----|-----------------|
| 1 | 30-second Research-constraints memo at the top | A bordered block: pattern named, discriminating cue, complexity, rejected alternative |
| 2 | All five FRAME sections present | Frame · Research constraints · Assess options · Make the solution · Examine — none skipped or stubbed |
| 3 | Code runs and is tested | Passes the stated examples; type hints; PEP 8 (<https://peps.python.org/pep-0008/>); idiomatic |
| 4 | Complexity stated with a derivation | Not just "O(n)" — *why*: "one pass, one accumulator" |
| 5 | A variant or trade-off named | In Examine: a follow-up, or the alternative and why it loses |
| 6 | A trace on two inputs | In Examine: a normal case and an edge case, walked by hand |

---

## Requirements

1. Every write-up under `frame-writeups/` scored against all six bars.
2. Every failure fixed, not merely recorded.
3. Every code snippet run, and passing its stated examples.
4. `frame-writeups/AUDIT.md` recording what you checked and what you fixed.
5. The README dashboard count corrected to the number that passes.

### The task, step by step

1. **List every write-up.**

   ```bash
   find frame-writeups -name "*.md" ! -name "README.md" | sort
   ```

   Paste the list into a scratch file as a checklist.

2. **Triage oldest-first.** The Week 1–3 write-ups are the most likely to fail bars 1, 4, and 6 (the 30-second-memo and complexity-derivation disciplines came later). Audit those first.

3. **Score each write-up against the six bars.** A 30-second scan per write-up is enough — you are checking for *presence*, not re-reading. Mark pass/fail per bar in your checklist.

4. **Fix the failures in frequency order:**
   - Backfill missing **Research-constraints memos** (bar 1) and **complexity derivations** (bar 4) first — quick, and they cluster in early write-ups.
   - **Run any untested code** (bar 3). Fix anything that does not run or does not pass the examples.
   - Add missing **edge-case traces** (bar 6).

5. **Re-count and update the dashboard.** The README dashboard count is the number of write-ups that *pass*. Run the count after fixing:

   ```bash
   find frame-writeups -name "*.md" ! -name "README.md" | wc -l
   ```

---

## Constraints

- **Thirty seconds per write-up on the first pass.** You are checking for
  *presence*, not re-reading. A careful re-read of fifty write-ups is a
  different exercise and you will not finish it.
- **Oldest first.** Weeks 1 to 3 fail bars 1, 4 and 6 most often, because the
  memo and complexity-derivation disciplines arrived later. That is where the
  fixes are, so that is where to start.
- **Fix in frequency order**, not file order. Backfill all the missing memos,
  then all the missing complexity derivations, then run the untested code.
  Batching by defect is several times faster than going file by file.
- **The count is the passing count.** If eight write-ups still fail after the
  audit, the dashboard says fifty-two, not sixty.
- **The audit log is portfolio evidence in its own right.** It is the artifact
  that shows you audit your own work, which is a thing employers buy.

## Expected output

What the audit produces, and roughly what to expect:

```text
write-ups found          ~50
fail at least one bar    typically 15-25, clustered in weeks 1-3
most common failures     bar 1 (no memo), bar 4 (no derivation), bar 6 (no trace)
time per fix             ~5 min for bars 1, 4 and 6; longer for bar 3

after the audit          every write-up clears all six
                         AUDIT.md committed
                         README count == passing count
```

If nothing fails, you audited too gently. Half of a fifty-write-up repo built
over fifteen weeks fails something, and the early weeks fail most.

## Steps

1. List every write-up into a scratch checklist.
2. Triage oldest first.
3. Score each one against the six bars — thirty seconds each, presence only.
4. Fix in frequency order: memos, then derivations, then untested code, then
   traces.
5. Re-run every code snippet. Fix anything that does not run.
6. Write `AUDIT.md`: what you checked, what failed, what you fixed.
7. Re-count and correct the dashboard.

## The Solution

Suppose `frame-writeups/04-ballast-pair.md`, written in Week 2, reads in its
entirety:

```markdown
# Ballast Pair

Use a hash map. Loop through, check if the complement is in the map.

def ballast_pair(weights, capacity):
    seen = {}
    for i, w in enumerate(weights):
        if capacity - w in seen:
            return [seen[capacity - w], i]
        seen[w] = i
```

Audit it against the six bars. **Bar 1 fails** — no recognition memo. **Bar 2
fails** — no Frame, no Reason, no Evaluate. **Bar 3 is partial** — the code is
correct, and it has no type hints, no docstring and no evidence it was ever run.
**Bar 4 fails** — no complexity anywhere. **Bar 5 fails** — no variant or
trade-off. **Bar 6 fails** — no trace. Five of six, and the one partial pass is
the code.

Here is the same write-up brought to the bar:

```markdown
# Ballast Pair

> **30-second recognition memo (hash map):**
> "Two items whose weights sum to a target" plus "one pass wanted" is a hash map
> of weight to index. Scanning, I check whether the complement — capacity minus
> this weight — has already been seen. Time O(n), space O(n). Why not the
> double loop: it is O(n squared) and buys back only O(1) space, which is not
> the scarce thing here.

## Frame
A ferry loading desk has a list of pallet weights and the tonnage still free on
the deck. Return the positions of the two pallets that exactly fill it. Exactly
one pair qualifies, and a pallet cannot pair with itself.
Example: `weights=[2,7,11,15], capacity=9` gives `[0,1]`, because 2 + 7 is 9.

## Reason about options
One pass is wanted, so the double loop is out. That points at a hash map — see
the memo. The rejected alternative is the brute force at O(n squared).

## Assemble the approach
1. An empty dict, weight to index.
2. For each `(i, w)`: if `capacity - w` is in `seen`, return `[seen[capacity - w], i]`.
3. Otherwise record `seen[w] = i`.

The check comes before the store, which is what makes two pallets of equal
weight work rather than matching a pallet against itself.

## Make the solution
```python
def ballast_pair(weights: list[int], capacity: int) -> list[int]:
    """Return the positions of the two pallets summing to capacity.

    One pass, O(n) time and O(n) space.
    """
    seen: dict[int, int] = {}
    for i, weight in enumerate(weights):
        complement = capacity - weight
        if complement in seen:
            return [seen[complement], i]
        seen[weight] = i
    return []   # the desk guarantees a pair; this is the defensive path
```

## Evaluate
- `weights=[2,7,11,15], capacity=9`: i=0, w=2, complement 7 unseen, store {2:0};
  i=1, w=7, complement 2 is seen, return [0,1]. Correct.
- Edge, `weights=[3,3], capacity=6`: i=0 stores {3:0}; i=1, complement 3 is seen,
  return [0,1]. Correct — and it is correct *because* the check precedes the
  store, which is the line the trace exists to prove.

Time O(n): one pass over the manifest. Space O(n): the dict holds up to one
entry per pallet. Trade-off: the double loop is O(1) space and O(n squared)
time, which is the wrong way round for a manifest of any size. Variant: if the
manifest were sorted by weight, two pointers give O(n) time and O(1) space —
worth naming as the space-optimal answer when the input is already sorted.
```

Now it clears all six. That fix took five minutes, and it converted a write-up
that would have cost a recruiter's trust into one that earns it.

## How to deliver it

Commit the fixed write-ups **individually**, with messages that say what was
fixed — `audit: backfill complexity derivation in 04-ballast-pair`. The commit
history becomes part of the evidence.

- The fixed write-ups (commit them individually with messages like `audit: backfill complexity derivation in 04-two-sum`).
- `frame-writeups/AUDIT.md` — the audit log.
- The updated README dashboard count.

---

Next: [Exercise 2 — System-Design Write-Up](./exercise-02-system-design-writeup.md) — the junior-level URL-shortener design artifact.

## Common bugs to catch

- **Re-reading instead of scanning.** Symptom: four write-ups audited in an
  hour and forty-six to go.
- **Recording failures without fixing them.** Symptom: a beautiful audit log
  and a repo that still fails. The log is the by-product; the fixes are the
  deliverable.
- **Counting files as the dashboard number.** Symptom: a count a reader can
  disprove by opening one file.
- **Fixing file by file rather than defect by defect.** Symptom: three times
  the work, because you reload the context for every file.
- **Skipping bar 3 because the code 'obviously works'.** Symptom: a snippet in
  the portfolio that raises on the example printed next to it. This is the
  most expensive failure of the six.
- **Auditing only the ones you remember being weak.** Symptom: the random
  write-up the recruiter opens is still weak, which was the whole premise.

## Acceptance checklist

- [ ] Every write-up under `frame-writeups/` has been scored against the six-point bar.
- [ ] Every failure has been fixed — no write-up in the repo fails any bar.
- [ ] All code snippets run and pass their stated examples.
- [ ] The README dashboard count reflects the true number of passing write-ups.
- [ ] An audit log (`frame-writeups/AUDIT.md`) records what you checked and what you fixed — the audit itself is portfolio evidence of rigor.

---

## Stretch

- Add a seventh bar of your own and re-audit against it. Whatever you find
  yourself repeatedly wishing were there is the bar.
- Write the audit as a script — grep for the memo block, for the five section
  headings, for a complexity claim — and run it on every write-up. It will not
  catch everything, and it will catch bars 1 and 2 perfectly.
- Re-audit in three months. A portfolio that is never re-audited becomes an
  archive, and the six bars drift the moment nothing checks them.
