# Drill 2 — Valid Palindrome

> **Pattern:** Two-pointer, converging
> **Difficulty:** Easy/Medium
> **Target solve time:** 20 minutes (full UMPIRE narration)

## Problem statement

Given a string `s`, determine whether it is a **palindrome** considering only **alphanumeric characters** and ignoring **case**.

**Examples:**

- `"A man, a plan, a canal: Panama"` → `True`
- `"race a car"` → `False`
- `""` (empty) → `True`
- `".,"` (no alphanumerics) → `True`
- `"0P"` → `False` (`'0' != 'p'`)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm "alphanumeric" = letters (a-z, A-Z) and digits (0-9). Confirm "ignore case" = compare lowercase. Confirm: empty string and "all punctuation" are palindromes (vacuously true).
- [ ] **M:** Two-pointer converging. Skip non-alphanumeric on each side; compare lowercase characters.
- [ ] **P:** `l=0, r=n-1`. Loop while `l<r`. Inner while: advance `l` past non-alphanumeric. Inner while: retreat `r` past non-alphanumeric. Compare `s[l].lower()` vs `s[r].lower()`. If mismatch, return False. Else advance both.
- [ ] **I:** Code with care for nested `while` guards (`l<r` inside the skip loops).
- [ ] **R:** Trace on `"A man, a plan, a canal: Panama"` (True), `"race a car"` (False), `""` (True), `".,"` (True).
- [ ] **E:** **O(n)** time (each char visited ≤2 times). **O(1)** space.

## Acceptance criteria

- Code passes `timed_runner.py` for `is_palindrome`.
- UMPIRE write-up at `umpire-writeups/c2-week-01/drill-02-valid-palindrome.md`.
- Recording ≥10 minutes.

## Function signature

```python
def is_palindrome(s: str) -> bool:
    ...
```

## Common bugs to catch in Review

- **Missing inner-loop guard:** `while not s[l].isalnum(): l += 1` can walk off the end if the string is all punctuation. Use `while l < r and not s[l].isalnum(): l += 1`.
- **Case-sensitive compare:** Comparing `s[l]` to `s[r]` directly (not lowered) fails on `"Aa"`.
- **Using `s.replace()` / regex first:** Works but uses O(n) space; this drill is about staying in O(1).

## Stretch

Add a version that allows **at most one deletion** and still returns `True` if a one-deletion palindrome is possible. (LeetCode 680 — "Valid Palindrome II.") Two-pointer with a single skip retry. UMPIRE this one too.

Next: [Drill 3 — Two Sum II (Sorted)](drill-03-two-sum-sorted.md).
