# Drill 1 — Reverse a String In Place

> **Pattern:** Two-pointer, converging
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (with full UMPIRE narration)
> **Why first:** the simplest two-pointer problem in existence. If you can't UMPIRE this, you can't UMPIRE anything.

## Problem statement

Given a list of characters `s`, reverse it **in place**. You must use **O(1)** extra space (do not allocate a new list).

**Examples:**

- `["h", "e", "l", "l", "o"]` → `["o", "l", "l", "e", "h"]`
- `["A"]` → `["A"]`
- `[]` → `[]`

## UMPIRE checklist for this drill

Before you write a line of code, you must say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate the problem. Note that "in place" means modify `s` directly, return nothing (or return `s` itself, depending on the signature you write). Confirm the empty and single-element cases are no-ops.
- [ ] **M:** Two-pointer converging. Left at start, right at end. Swap. Advance both toward each other. Stop when they meet.
- [ ] **P:** Initialize `l = 0`, `r = len(s) - 1`. Loop while `l < r`. Swap `s[l]` and `s[r]`. Increment `l`, decrement `r`. No edge case needed; the loop naturally skips for length 0 or 1.
- [ ] **I:** Write the code, narrating each line.
- [ ] **R:** Trace on `["a", "b", "c", "d"]` and on `["a"]`.
- [ ] **E:** Time **O(n/2) = O(n)**. Space **O(1)** (just two integer pointers and a swap temporary, but Python does swap with tuple-unpacking which is also O(1)).

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `reverse_string_in_place`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-01/drill-01-reverse-string.md` in your portfolio repo.
- You have a recording of yourself narrating the solve (any audio quality).
- The recording is **at least 8 minutes long.** If you finished in 3 minutes, you skipped Review or Evaluate. Re-do it.

## Function signature (for the runner)

```python
def reverse_string_in_place(s: list[str]) -> None:
    """
    Reverse s in place. Do not allocate a new list.
    Returns None.
    """
    ...
```

## Common bugs you should catch in Review

- **Off-by-one:** Using `while l <= r` swaps the middle element with itself when length is odd. Harmless but wasteful; use `<`.
- **Forgetting to advance:** Forgetting `l += 1` or `r -= 1` produces an infinite loop. The test runner will time out.
- **Allocating a new list:** `return s[::-1]` would compile but uses O(n) extra space — violates the constraint.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. One thing I did well.
2. One thing I'd improve next time.
3. How long did Match take? (Should be <30 seconds on this problem.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
├── README.md
└── umpire-writeups/
    └── c2-week-01/
        ├── drill-01-reverse-string.md       # write-up
        ├── drill-01-reverse-string.py       # your solution
        └── drill-01-recording.md            # link to / notes on the recording
```

When done, push and move on to [Drill 2](drill-02-valid-palindrome.md).
