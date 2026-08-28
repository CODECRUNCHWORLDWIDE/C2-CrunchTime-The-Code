# Challenge 2 — Sum of Two Integers (LeetCode 371)

> **Difficulty:** Medium. **Target solve time:** 50 minutes including the FRAME write-up.

Add two integers without using `+` or `-`. This is the bit problem that most cleanly separates strong candidates, because the *correct* answer in Python requires confronting a subtlety almost no other bit problem surfaces: **Python integers are unbounded, so they never overflow** — which means you have to *simulate* a fixed-width register with a mask. Surfacing and handling that detail is a genuine senior signal.

---

## Problem spec

Given two integers `a` and `b`, return the sum `a + b` without using the operators `+` and `-`.

```
Input:  a = 1, b = 2
Output: 3

Input:  a = 2, b = 3
Output: 5

Input:  a = -2, b = 3
Output: 1
```

**Constraints (LeetCode):**

- `-1000 <= a, b <= 1000`

The constraint range is small, but the problem is about *technique*, not scale: you may not use `+` or `-`, so you build addition out of bit operations.

---

## The idea — addition as XOR + carry

Binary addition of two bits decomposes into two pieces:

- **Sum without carry:** `a ^ b`. XOR is addition mod 2 per bit (`0+0=0, 0+1=1, 1+0=1, 1+1=0`), which is exactly "add the bits and drop the carry."
- **Carry:** `(a & b) << 1`. A carry is generated wherever *both* bits are `1` (that is the `a & b`), and a carry propagates to the *next* position up (that is the `<< 1`).

So `a + b == (a ^ b) + ((a & b) << 1)` — but the right side still has a `+`. The trick is to *iterate*: set `a` to the sum-without-carry and `b` to the carry, and repeat until the carry is zero. Each iteration pushes the carry one position higher; the process terminates because the carry eventually shifts off the top.

```
add 5 (0101) and 3 (0011):
  iter 1: sum = 0101 ^ 0011 = 0110 (6);  carry = (0101 & 0011) << 1 = 0001 << 1 = 0010 (2)
  iter 2: sum = 0110 ^ 0010 = 0100 (4);  carry = (0110 & 0010) << 1 = 0010 << 1 = 0100 (4)
  iter 3: sum = 0100 ^ 0100 = 0000 (0);  carry = (0100 & 0100) << 1 = 0100 << 1 = 1000 (8)
  iter 4: sum = 0000 ^ 1000 = 1000 (8);  carry = (0000 & 1000) << 1 = 0000 (0)  -> stop
  result: 8   ✓
```

---

## The Python subtlety — why you need a mask

In C or Java, the carry eventually shifts past bit 31 and falls off the end of the 32-bit register; the loop terminates naturally. **In Python it never does** — `int` is unbounded, so `(a & b) << 1` keeps producing larger and larger carries for negative inputs (whose conceptual two's-complement form has infinitely many leading `1`s), and the loop runs forever.

The fix is to *simulate* a 32-bit register with the mask `0xFFFFFFFF` (32 ones):

- After each step, AND both `a` and `b` with `0xFFFFFFFF` to keep only the low 32 bits — this throws away the carry that "should" have fallen off the top.
- The loop condition becomes `while b & 0xFFFFFFFF` (equivalently `while b`), which now terminates because the carry can no longer grow without bound.
- When the loop ends, `a` holds the 32-bit *unsigned* result. If the answer should be negative (the sign bit, bit 31, is set — i.e. `a > 0x7FFFFFFF`), convert the unsigned 32-bit pattern back to a signed Python int. Two equivalent conversions: `a - 0x100000000`, or `~(a ^ 0xFFFFFFFF)`.

Why `~(a ^ 0xFFFFFFFF)` works: `a ^ 0xFFFFFFFF` flips the low 32 bits (the magnitude of the two's-complement negative), and `~` then produces the correct negative Python int. It is the same value as `a - 0x100000000`; pick whichever you can explain cleanly. **Narrating this masking step out loud is the senior signal of the whole problem** — most candidates write the XOR/carry loop and then loop forever on `-2 + 3` because they forgot Python does not overflow.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (bit-arithmetic / add-without-plus):**
> Add without `+`/`-`, so I build addition from bits. Sum-without-carry is
> `a ^ b` (XOR is per-bit add mod 2); carry is `(a & b) << 1` (carry where
> both bits are 1, propagated one position up). Iterate: a := sum, b := carry,
> until carry is 0. Python subtlety: ints are unbounded and never overflow, so
> I mask with `& 0xFFFFFFFF` each step to simulate a 32-bit register and stop
> the loop; at the end I convert the unsigned 32-bit value back to signed if
> bit 31 is set. Time O(1) (bounded by 32 bit positions), space O(1).
```

Read aloud; should hit 25–30 seconds.

---

## FRAME outline

- **Frame:** add two ints without `+`/`-`. Hand-walk `5 + 3 = 8` and `-2 + 3 = 1`.
- **Research constraints:** range `[-1000, 1000]`, so negatives are in scope — that is what forces the masking. The shape is bit-arithmetic. The memo above. Reject "just use `sum()`" (it uses `+` under the hood) and "convert to string and add digit-wise" (uses `+` for the digit math and is far messier).
- **Assess options:**
  1. Define `MASK = 0xFFFFFFFF` and `INT_MAX = 0x7FFFFFFF`.
  2. While `b & MASK` is nonzero: compute `carry = (a & b) << 1`; set `a = (a ^ b) & MASK`; set `b = carry & MASK`.
  3. After the loop, mask `a`; if `a <= INT_MAX` it is non-negative, return it; else convert to signed with `~(a ^ MASK)` (or `a - 0x100000000`).
- **Make the solution:** see below.
- **Examine (verify):** trace `-2 + 3 = 1` (the case that loops forever without the mask) and `2 + 3 = 5`.
- **Examine (cost):** `O(1)` time (at most ~32 carry-propagation steps), `O(1)` space.

---

## Function signature and reference implementation

```python
def get_sum(a: int, b: int) -> int:
    """Return a + b using only bit operations (no + or -).

    Sum-without-carry is a ^ b; carry is (a & b) << 1; iterate until the carry
    is zero. Python ints are unbounded, so mask to 32 bits each step to simulate
    a fixed-width register; convert back to a signed int at the end.
    Time O(1) (bounded by the 32 bit positions), space O(1).
    """
    MASK = 0xFFFFFFFF       # 32 ones — simulate a 32-bit register
    INT_MAX = 0x7FFFFFFF    # largest positive 32-bit signed value

    while b & MASK:                 # while there is still a carry to add
        carry = (a & b) << 1        # carry: both bits 1, propagated up one
        a = (a ^ b) & MASK          # sum without carry, kept to 32 bits
        b = carry & MASK            # the carry becomes the next addend
    a &= MASK
    # If bit 31 is set, the result is negative — convert the unsigned pattern
    # back to a signed Python int. ~(a ^ MASK) == a - 0x100000000.
    return a if a <= INT_MAX else ~(a ^ MASK)
```

---

## Test cases

```python
assert get_sum(1, 2) == 3
assert get_sum(2, 3) == 5
assert get_sum(-2, 3) == 1
assert get_sum(-2, -3) == -5
assert get_sum(0, 0) == 0
assert get_sum(-1, 1) == 0
assert get_sum(1000, -1000) == 0
assert get_sum(123, -456) == -333
```

---

## Common bugs

1. **Forgetting the mask → infinite loop.** Without `& 0xFFFFFFFF`, `-2 + 3` never terminates: the negative carry grows without bound because Python ints do not overflow. This is *the* bug of the problem.
2. **Masking only `a` and not `b` (or vice versa).** Both must be masked each iteration, or the loop condition `while b & MASK` never settles.
3. **Skipping the signed conversion.** Without the final `a if a <= INT_MAX else …`, a negative result comes back as a large positive (the raw unsigned 32-bit pattern). Trace `-5`: the loop ends with `a == 0xFFFFFFFB`, and you must convert it back to `-5`.
4. **Using a 32-bit shift that loses the sign in the loop body.** Compute `carry` *before* masking `a`, then mask both — the order in the reference above is deliberate.

---

## Why this matters

Sum of Two Integers looks like a toy ("just add two numbers"), but it is the cleanest interview probe for a specific senior trait: **knowing that the abstraction you are standing on has edges.** Python hides integer width from you everywhere else; this problem is where that abstraction leaks, and the candidate who *anticipates* the leak — "Python ints are unbounded, so I have to simulate the register" — before the loop hangs is signaling that they understand the machine beneath the language. That is the difference between a candidate who has memorized the XOR/carry trick and one who understands two's complement. The masking is not a trick to memorize; it is a consequence to derive. Derive it out loud, and this Medium becomes a strong-hire signal.

When the write-up is committed and recorded, Week 14's challenges are done. Move to the [mini-project](../mini-project/README.md).
