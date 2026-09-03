# Problem 2 — Trim the Duplicate Scan

> **Topic:** the fast/slow family's other member — a **fixed gap** between two walkers, with no meeting and no lemma
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §7
> **Difficulty:** Medium
> **Target time:** 45 minutes, including the FRAME write-up
> **Why this one:** it looks like Floyd's and it is not. Two pointers, same chain, same direction — but the gap between them is decided in advance rather than discovered. Being able to say which variant a problem needs, and why, is the recognition half of this week.

## The Brief

A parcel carries a chain of scans, oldest first. Every time a depot handheld
beeps at the label, one scan is added to the end.

The handhelds sometimes double-beep, which writes one scan too many. When the
depot notices, it sends a correction — and the correction always names the
offending scan by **how far back from the newest it sits**. `k = 1` means the
newest scan. `k = 2` means the one before it. And so on.

Remove the `k`-th-most-recent scan and return the first scan of the chain,
which may not be the scan that was first before.

Picture a train of carriages where you can only walk forwards from the engine.
Someone tells you to uncouple "the third carriage from the back". You do not
know how long the train is. Walking to the end to count and then walking back
is not allowed — you cannot walk backwards, and by the time you finish counting
the train may have grown another carriage.

Here is the move. Send one walker three carriages ahead of another, then walk
them **together**. When the front walker steps off the end of the train, the
back walker is standing exactly where you need it — because the gap between
them never changed.

That is the pattern: two pointers, one chain, same direction, and a gap that is
**fixed and known in advance**. There is no lapping, no meeting, and no lemma
to prove. Compare that to
[Exercise 2](../exercises/exercise-02-escalation-loop.md), where the gap closes
by one every turn until the pointers collide. Same family, different member.
Say which one you are in, out loud, every time.

**Three contract decisions, all deliberate.**

- If `k` is larger than the number of scans, **remove nothing** and return the
  chain unchanged. The handheld and the server can disagree about how many
  scans exist, and a correction that does not apply must not crash and must not
  quietly delete the wrong scan. Most published versions of this problem
  promise `k` is valid; this one does not.
- If `k` is zero or negative, raise `ValueError`. There is no zeroth-most-recent
  scan, and a caller passing `0` has an off-by-one that should be heard about
  now rather than three parcels later.
- If the chain is empty, return `None` for any positive `k`.

## Starter

Create `problem-02-trim-scan.py` and paste this in. Fill in every `TODO`.

```python
"""problem-02-trim-scan.py — drop the k-th scan from the end.

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per correction and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Scan:
    """One handheld scan on a parcel, oldest first."""

    def __init__(self, scan_code: str, next_scan: "Scan | None" = None) -> None:
        self.scan_code = scan_code
        self.next_scan = next_scan


def build_history(codes: list[str]) -> list[Scan]:
    """Wire a scan history from a list of codes and hand back every scan.

    Args:
        codes: One code per scan, oldest first. Codes repeat constantly.

    Returns:
        The scans, in order. Empty when `codes` is empty.
    """
    scans = [Scan(code) for code in codes]
    for earlier, later in zip(scans, scans[1:]):
        earlier.next_scan = later
    return scans


def history_codes(first: Scan | None) -> list[str]:
    """Walk a scan chain into a list of codes, oldest first."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.scan_code)
        first = first.next_scan
    return codes


def trim_scan(first: Scan | None, k: int) -> Scan | None:
    """Remove the k-th scan counted back from the newest one.

    Args:
        first: The oldest scan, or None for a parcel with no history.
        k: How far back from the newest scan the offending one sits. `k = 1`
            is the newest scan itself.

    Returns:
        The first scan of the resulting chain, which is None when the chain
        becomes empty. When `k` is larger than the number of scans the chain
        is returned unchanged, because a correction that does not apply must
        not delete something else instead.

    Raises:
        ValueError: If `k` is zero or negative.
    """
    # TODO 1: reject k <= 0, then answer None for an empty chain.
    # TODO 2: push `fast` k scans ahead. If it runs out of chain on the way,
    #         the correction does not apply — return the chain unchanged.
    # TODO 3: put a throwaway scan in FRONT of the chain and start `slow`
    #         there. Read the Solution for what that buys you.
    # TODO 4: walk both until `fast` is None, then unhook the scan just
    #         after `slow` and return the throwaway scan's successor.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["ARV", "SRT", "OFD", "DLV"], 1, ["ARV", "SRT", "OFD"]),
        (["ARV", "SRT", "OFD", "DLV"], 4, ["SRT", "OFD", "DLV"]),
        (["ARV", "SRT", "OFD", "DLV"], 5, ["ARV", "SRT", "OFD", "DLV"]),
        (["ARV"], 1, []),
        (["ARV"], 2, ["ARV"]),
        ([], 1, []),
        (["BEEP", "BEEP", "BEEP"], 2, ["BEEP", "BEEP"]),
    ]

    for codes, k, expected in CASES:
        scans = build_history(codes)
        first = scans[0] if scans else None
        result = history_codes(trim_scan(first, k))
        assert result == expected, f"{codes}, k={k}: got {result}"
        print(f"{str(codes):<34} k={k}  ->  {result}")

    # Three identical codes cannot tell you which scan went. Check by identity.
    beeps = build_history(["BEEP", "BEEP", "BEEP"])
    kept = trim_scan(beeps[0], 2)
    assert kept is beeps[0] and kept.next_scan is beeps[2]
    assert beeps[1] not in (kept, kept.next_scan)
    print(f"{'the middle BEEP went, by identity':<34} k=2  ->  ['BEEP', 'BEEP']")

    try:
        trim_scan(build_history(["ARV", "SRT"])[0], 0)
    except ValueError as caught:
        print(f"{'k of 0':<34} raises ValueError: {caught}")
    else:  # pragma: no cover - the raise below is the real check
        raise AssertionError("k of 0 must raise")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/homework/problem-02-trim-scan.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `trim_scan(first, k)` removes the `k`-th scan counted back from the newest
   and returns the first scan of the resulting chain.
2. `k` larger than the chain length leaves the chain **unchanged** and returns
   the original first scan.
3. `k <= 0` raises `ValueError`.
4. `trim_scan(None, k)` returns `None` for any positive `k`.
5. Removing the oldest scan — `k` equal to the chain length — must go through
   the same code path as every other `k`. No branch for it.
6. **One pass** over the chain, and fixed memory. No list of scans, no `len`.
7. Scans are identified by position only, never by `scan_code`.
8. `trim_scan` keeps its type hints and its docstring.

## Constraints

- **Single pass, and the rejection is not about speed.** The two-pass version —
  count the scans, then walk to position `length - k` — is the same O(n) time.
  It loses because the correction is applied on the handheld while the chain is
  still arriving in a streaming buffer: the handheld does not *keep* the chain,
  so it cannot walk it twice. This is the same shape of argument as
  [Exercise 3](../exercises/exercise-03-midroll-break.md), and it is worth
  saying carefully. "It cannot be done twice" is a different sentence from "it
  would be slower".

- **Up to 50,000 scans.** A parcel with a long international routing history.
  The bound is here so your solution is exercised on a chain far longer than
  `k`, where the fixed-gap invariant is the only thing keeping you correct — on
  a five-scan chain almost any muddle happens to work.

- **Scan codes repeat constantly.** Most parcels carry several `ARV` scans.
  You cannot identify the target scan by its code, only by its position. The
  `["BEEP", "BEEP", "BEEP"]` case is in the check list because its *output*
  cannot distinguish a correct answer from a wrong one — which is why the
  self-check follows it with a second check that compares by identity.

- **Fixed memory.** The handheld has a fixed frame budget per correction, so no
  list of scans and no dictionary of positions.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-trim-scan-solution.py
['ARV', 'SRT', 'OFD', 'DLV']       k=1  ->  ['ARV', 'SRT', 'OFD']
['ARV', 'SRT', 'OFD', 'DLV']       k=4  ->  ['SRT', 'OFD', 'DLV']
['ARV', 'SRT', 'OFD', 'DLV']       k=5  ->  ['ARV', 'SRT', 'OFD', 'DLV']
['ARV']                            k=1  ->  []
['ARV']                            k=2  ->  ['ARV']
[]                                 k=1  ->  []
['BEEP', 'BEEP', 'BEEP']           k=2  ->  ['BEEP', 'BEEP']
the middle BEEP went, by identity  k=2  ->  ['BEEP', 'BEEP']
k of 0                             raises ValueError: k counts back from the newest scan and starts at 1
All checks passed.
```

Line two is the one that needs the throwaway scan: `k = 4` on a four-scan chain
removes the *oldest* scan, so the first scan changes. Line three is the no-op:
`k = 5` on the same chain does nothing at all.

## Steps

1. **Frame.** Restate. Say the three contract decisions out loud and say why
   each one is what it is. Confirm that `k` equal to the chain length changes
   the head, and predict — before writing anything — that this will need no
   branch of its own.
2. **Research constraints.** Name the streaming buffer as the reason for one
   pass, in the right words. Note the repeated codes. Note that the bound is
   there to make `k` much smaller than the chain.
3. **Assess options.** Two-pass count-then-walk: simple, same big-O, impossible
   on a chain you do not keep. Copy to a list and index from the end: trivial,
   O(n) memory, rejected. Fixed gap: one pass, fixed memory, and the only real
   thinking is the head case.
4. **Assess options, and name the variant.** Say out loud that this is **not**
   Floyd's: the gap is constant and known in advance, so there is no meeting,
   no collision and no lemma. Getting that sentence right is what this problem
   is checking.
5. **Make the solution.** Guards first, then the `k`-step push, then the
   throwaway scan, then the lockstep walk, then the unhook.
6. **Examine, the ordinary case.** Trace `["ARV", "SRT", "OFD", "DLV"]` with
   `k = 1`. Push fast one scan: fast is at `SRT`. Throwaway in front, slow on
   the throwaway. Walk: fast=`OFD`, slow=`ARV`; fast=`DLV`, slow=`SRT`;
   fast=`None`, slow=`OFD`. Stop. Unhook the scan after `OFD`, which is `DLV`.
   Result `["ARV", "SRT", "OFD"]`. ✓
7. **Examine, the head case.** Same chain with `k = 4`. Push fast four scans and
   it lands on `None` — exactly at the end, not past it. Slow never moves, so
   it is still on the throwaway. Unhook the scan after the throwaway, which is
   `ARV`. Result `["SRT", "OFD", "DLV"]`. ✓ No branch fired, as predicted.
8. **Examine, the no-op case.** `k = 5`. The push runs out of chain on its
   fifth step, so we return the original chain untouched.
9. **Examine, cost.** O(n) time — the push is `k` steps and the lockstep walk
   is `length - k`, so together they are one pass over the chain. O(1) space —
   two pointers and one throwaway object.

## The Solution

```python
"""problem-02-trim-scan-solution.py — drop the k-th scan from the end.

This is the fast/slow family's other member: the gap between the two walkers
is fixed and known in advance, so nobody ever laps anybody and there is no
lemma to prove. Push one walker `k` scans ahead, then move both together.
When the front walker falls off the end, the back walker is standing exactly
one place in front of the scan to remove.

The dummy scan in front of the chain is what lets "remove the oldest scan"
use the same three lines as every other case.

The chains are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per correction, then
"All checks passed."
"""

from __future__ import annotations


class Scan:
    """One handheld scan on a parcel, oldest first."""

    def __init__(self, scan_code: str, next_scan: "Scan | None" = None) -> None:
        self.scan_code = scan_code
        self.next_scan = next_scan


def build_history(codes: list[str]) -> list[Scan]:
    """Wire a scan history from a list of codes and hand back every scan.

    Args:
        codes: One code per scan, oldest first. Codes repeat constantly.

    Returns:
        The scans, in order. Empty when `codes` is empty.
    """
    scans = [Scan(code) for code in codes]
    for earlier, later in zip(scans, scans[1:]):
        earlier.next_scan = later
    return scans


def history_codes(first: Scan | None) -> list[str]:
    """Walk a scan chain into a list of codes, oldest first."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.scan_code)
        first = first.next_scan
    return codes


def trim_scan(first: Scan | None, k: int) -> Scan | None:
    """Remove the k-th scan counted back from the newest one.

    Args:
        first: The oldest scan, or None for a parcel with no history.
        k: How far back from the newest scan the offending one sits. `k = 1`
            is the newest scan itself.

    Returns:
        The first scan of the resulting chain, which is None when the chain
        becomes empty. When `k` is larger than the number of scans the chain
        is returned unchanged, because a correction that does not apply must
        not delete something else instead.

    Raises:
        ValueError: If `k` is zero or negative.
    """
    if k <= 0:
        raise ValueError("k counts back from the newest scan and starts at 1")
    if first is None:
        return None

    fast = first
    for _ in range(k):
        if fast is None:
            return first  # k is past the oldest scan: leave the chain alone.
        fast = fast.next_scan

    dummy = Scan("", first)
    slow = dummy
    while fast is not None:
        fast = fast.next_scan
        slow = slow.next_scan
    slow.next_scan = slow.next_scan.next_scan
    return dummy.next_scan


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["ARV", "SRT", "OFD", "DLV"], 1, ["ARV", "SRT", "OFD"]),
        (["ARV", "SRT", "OFD", "DLV"], 4, ["SRT", "OFD", "DLV"]),
        (["ARV", "SRT", "OFD", "DLV"], 5, ["ARV", "SRT", "OFD", "DLV"]),
        (["ARV"], 1, []),
        (["ARV"], 2, ["ARV"]),
        ([], 1, []),
        (["BEEP", "BEEP", "BEEP"], 2, ["BEEP", "BEEP"]),
    ]

    for codes, k, expected in CASES:
        scans = build_history(codes)
        first = scans[0] if scans else None
        result = history_codes(trim_scan(first, k))
        assert result == expected, f"{codes}, k={k}: got {result}"
        print(f"{str(codes):<34} k={k}  ->  {result}")

    # Three identical codes cannot tell you which scan went. Check by identity.
    beeps = build_history(["BEEP", "BEEP", "BEEP"])
    kept = trim_scan(beeps[0], 2)
    assert kept is beeps[0] and kept.next_scan is beeps[2]
    assert beeps[1] not in (kept, kept.next_scan)
    print(f"{'the middle BEEP went, by identity':<34} k=2  ->  ['BEEP', 'BEEP']")

    try:
        trim_scan(build_history(["ARV", "SRT"])[0], 0)
    except ValueError as caught:
        print(f"{'k of 0':<34} raises ValueError: {caught}")
    else:  # pragma: no cover - the raise below is the real check
        raise AssertionError("k of 0 must raise")

    print("All checks passed.")
```

**The invariant is the whole algorithm, and it is one sentence.** After the
push, `fast` is exactly `k` scans in front of `slow`, and both then move one
scan per turn, so the gap stays `k` forever. When `fast` falls off the end,
`slow` is `k` scans back from the end — which is one scan in *front* of the
`k`-th-from-the-end, because `slow` started one place behind the chain proper.
That is the whole reason the throwaway scan exists.

**What the throwaway scan buys you.**

```python
    dummy = Scan("", first)
    slow = dummy
```

To unhook a scan you need the scan *before* it, so you can point that one past
the target. The oldest scan has nothing before it — unless you put something
there. The throwaway is a scan that exists for exactly three lines and is never
returned, and it turns "remove the head" from a special case into the same
three lines as every other removal. Returning `dummy.next_scan` at the end
gives you the new first scan whether or not the head changed.

Skipping it is the single largest source of bugs on this problem. The version
without it needs an `if slow is None: return first.next_scan` branch, that
branch is only exercised by one value of `k`, and that value is the one people
forget to test.

**The push checks before it steps, and that ordering is what makes the no-op
work.**

```python
    for _ in range(k):
        if fast is None:
            return first  # k is past the oldest scan: leave the chain alone.
        fast = fast.next_scan
```

On a four-scan chain with `k = 4`, the loop runs four times and `fast` ends up
`None` — legally, having taken exactly four steps. With `k = 5` the fifth
iteration finds `fast` already `None` before stepping, and that is the signal
that the correction does not apply. Check first, step second. Written the other
way you either crash on `k = 5` or reject `k = 4`, and `k = 4` is the case that
changes the head.

**`k <= 0` raises rather than returning something.** A correction naming the
zeroth-most-recent scan is not a correction that does not apply; it is a caller
that has miscounted. Returning the chain unchanged would let that bug travel.
Raising puts the traceback at the line that computed the bad `k`.

**The gap never closes, and that is the difference from Floyd's.** In
[Exercise 2](../exercises/exercise-02-escalation-loop.md) the fast pointer moves
twice per turn, so the gap shrinks and the two eventually collide — and it is
that collision the lemma is about. Here both pointers move once per turn. They
never meet, nothing is discovered, and the only thing being used is that a
constant gap stays constant. If you find yourself reaching for `fast.next.next`
on this page, you have brought the wrong variant.

**Nothing here grows with the parcel.** Two pointers and one throwaway scan.
The handheld's frame budget is honoured.

## Download and run

Download
[problem-02-trim-scan-solution.py](./problem-02-trim-scan-solution.py)
and run it:

```bash
python problem-02-trim-scan-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-02-trim-scan.py`.

## Common bugs to catch

- **`AttributeError: 'NoneType' object has no attribute 'next_scan'`.** The
  push stepped without checking:

  ```text
  Traceback (most recent call last):
      fast = fast.next_scan
             ^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'next_scan'
  ```

  A `k` larger than the chain walked off the end. Move the `if fast is None`
  test to the top of the loop body, before the step.

- **Rejecting `k` equal to the chain length.** If your push treats a `fast` of
  `None` after the final step as an error, `k = 4` on a four-scan chain returns
  the chain unchanged instead of dropping the oldest scan. `fast` ending on
  `None` is the *correct* state for that case — it means the gap reaches
  exactly to the front of the chain.

- **No throwaway scan, and a crash on the head case.** Without it, `slow`
  starts on the first scan, so when `k` equals the length `slow` never moves
  and `slow.next_scan.next_scan` unhooks the wrong scan — or `slow` is `None`
  and you get the `AttributeError` above. Put the throwaway in.

- **Searching by code.** `["BEEP", "BEEP", "BEEP"]` produces
  `["BEEP", "BEEP"]` for *any* removal, so a solution that finds the scan by
  matching its code looks completely correct. This is why the self-check
  follows that case with an identity assertion, and why your write-up has to
  say how you verified it.

- **Returning `first` instead of `dummy.next_scan`.** Works on every `k` except
  the one that changes the head — which is exactly the case the throwaway was
  added for. Return the throwaway's successor and the head case is free.

- **`ValueError` for the no-op case.** `k = 5` on a four-scan chain is not an
  error. The handheld and the server disagreeing about the scan count is
  normal, and the contract says a correction that does not apply is a no-op.
  Only `k <= 0` raises.

## Under the hood

<details>
<summary>Under the hood — the three fast/slow variants side by side, and where dummy nodes come from</summary>

**Three members of one family, and the differences that matter.**

| Variant | Fast moves | Gap over time | What it discovers | This week |
|---|---|---|---|---|
| Floyd's detection | 2 per turn | shrinks by 1 | that a loop exists | Exercise 1 |
| Floyd's + entrance | 2 per turn | shrinks, then both at 1 | where the loop starts | Exercise 2 |
| Fixed gap | 1 per turn | never changes | a position counted from the end | this page |

The midpoint trick in [Exercise 3](../exercises/exercise-03-midroll-break.md) is
a fourth relative: fast at two, but nobody is looking for a meeting — the
speeds are being used as a ratio rather than a chase. When you name the pattern
in an interview, name the *member*, not just the family. "Fast and slow
pointers, the fixed-gap variant" is a better first sentence than "two
pointers".

**Dummy nodes, and why they are not a hack.** A sentinel node in front of a
chain is a standard structure with a long history — the classic textbook
treatment of linked lists uses a permanent header node so that insertion and
deletion never need a special case at the front. Modern code usually skips the
permanent version because it costs an allocation per list, and creates a
temporary one inside the function instead, which is what this page does. The
principle is the same: *make the boundary look like the middle, and the code
stops branching.*

You will see the same idea under other names — a sentinel value at the end of an
array so a search loop needs no bounds check, a zero row prepended to a running
total so the first prefix has an answer. Recognising it as one idea rather than
three tricks is worth doing once.

**Why the two-pass version is genuinely fine most of the time.** On a chain you
own, in memory, counting and then walking is clear, easy to get right, and the
same O(n). The single-pass version exists for two situations: you are reading a
stream you cannot rewind, or the chain is long enough that touching it twice
costs real cache misses. Neither is "it is faster in big-O terms", and claiming
that is how you lose credibility. Name the real reason.

**The version that reads from a stream.** If the scans arrived one at a time
from a socket, you could not even hold the chain — but the fixed-gap idea still
works with a small ring buffer of the last `k` items. That is the shape this
problem is a simplification of, and it is why the constraint is written as
"cannot walk it twice" rather than "should not".

</details>

## Acceptance checklist

- [ ] `python problem-02-trim-scan.py` prints nine lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] There is a throwaway scan in front of the chain, and you can say in one
      sentence what it buys you.
- [ ] `k` equal to the chain length changes the head, with no branch of its own.
- [ ] `k` larger than the chain is a no-op, not an error.
- [ ] `k <= 0` raises `ValueError`.
- [ ] One pass. No `len`, no list, no counting walk.
- [ ] Your write-up says how you verified the `["BEEP", "BEEP", "BEEP"]` case,
      given that the output codes cannot tell a right answer from a wrong one.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/hw-02-trim-scan.md`,
      and its Assess-options section names this as the **fixed-gap** variant and
      says how it differs from Floyd's.

## Stretch

- **Return the removed scan as well as the new head.** The depot wants to log
  what was dropped. It is one extra name and a second return value:

  ```python
  def trim_scan_reporting(first: Scan | None, k: int) -> tuple[Scan | None, Scan | None]:
      """Return (new first scan, the scan that was removed or None)."""
      if k <= 0:
          raise ValueError("k counts back from the newest scan and starts at 1")
      if first is None:
          return None, None
      fast = first
      for _ in range(k):
          if fast is None:
              return first, None
          fast = fast.next_scan
      dummy = Scan("", first)
      slow = dummy
      while fast is not None:
          fast, slow = fast.next_scan, slow.next_scan
      dropped = slow.next_scan
      slow.next_scan = dropped.next_scan
      return dummy.next_scan, dropped
  ```

  ```text
  ['ARV', 'SRT', 'OFD', 'DLV']       k=1  ->  ['ARV', 'SRT', 'OFD'], dropped DLV
  ['ARV', 'SRT', 'OFD', 'DLV']       k=5  ->  ['ARV', 'SRT', 'OFD', 'DLV'], dropped None
  ```

- **Remove a run of `m` scans ending `k` back from the newest.** Same push, same
  lockstep walk, and the unhook now skips `m` scans instead of one. Work out
  what the push distance has to become — it is not `k` — before you write it.

- **Find the `k`-th scan from the end without removing it.** Same walk, return
  `slow.next_scan`. Then write the two-pass version beside it and time both on a
  50,000-scan chain. The times will be indistinguishable, which is the finding:
  the single pass is not here for speed.
Next: [Problem 3 — The Symmetric Die Sequence](./problem-03-symmetric-dies.md).
