# Lecture 1 — Strings and the Cost of Immutability

**Reading time:** ~35 minutes. Have a REPL open. Every claim in here is one you should verify yourself.

---

## 1. One fact, and everything follows from it

**A Python string cannot be modified after it is created.**

```python
s = "hello"
s[0] = "H"
# TypeError: 'str' object does not support item assignment
```

There is no in-place string edit. Not a stylistic preference — there is no mechanism. Every operation that appears to change a string builds a new one and leaves the original alone.

That single fact generates most of the string-complexity mistakes people make in interviews. Work through the consequences deliberately now and you will not make them.

Why is it this way? Because immutability buys three things Python relies on: strings can be **hashable** (so they can be dict keys), they can be **shared safely** without defensive copying, and short strings can be **interned** so equality checks are often a pointer comparison. The cost is that every edit is a copy.

---

## 2. What is free

These are `O(1)` and you can use them without a second thought.

```python
s = "interview"

len(s)      # O(1) — the length is stored, never counted
s[0]        # O(1) — 'i'
s[-1]       # O(1) — 'w', negative indices are computed, not walked
ord('a')    # O(1) — 97
chr(97)     # O(1) — 'a'
```

`len` is `O(1)` for **every** built-in container in Python. It is never a loop. Say so if asked; a surprising number of candidates hedge.

`ord` and `chr` matter more than they look. They are how you build a fixed-size frequency array instead of a dict:

```python
counts = [0] * 26
for ch in s:
    counts[ord(ch) - ord('a')] += 1
```

That is `O(n)` time and **`O(1)` space** — 26 is a constant, not an `n`. A dict would be `O(k)` space where `k` is the alphabet size. When the problem guarantees lowercase ASCII, the array version is the stronger answer *and* the stronger complexity claim. Say "O(1) space because the alphabet is bounded at 26" out loud.

---

## 3. Slicing copies — the most-missed `O(n)` in Python

```python
s[a:b]      # O(b - a) time AND O(b - a) space
s[:]        # O(n) — a full copy
s[::-1]     # O(n) — reversed copy
```

Slicing looks like indexing. It costs like copying. This is the trap:

```python
def is_palindrome_bad(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_bad(s[1:-1])    # builds a new string every call
```

That is `O(n²)` time and `O(n²)` total allocation — `n/2` recursive calls, each slicing a string of length `n - 2i`. It also uses `O(n)` stack. The fix is to pass indices instead of slices:

```python
def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True
```

`O(n)` time, `O(1)` space. Same algorithm, correct implementation.

**The rule to internalize:** *if you are slicing inside a loop or a recursion, you have probably added a factor of `n`.* Pass `(lo, hi)` bounds instead. This comes back in Week 1 (two pointers), Week 3 (sliding window), and Week 5 (binary search) — every one of those patterns exists partly to avoid materializing subsequences.

**One exception worth knowing:** `s.startswith(prefix)` is `O(len(prefix))` and allocates nothing, whereas `s[:len(prefix)] == prefix` allocates a copy first. Prefer `startswith`.

---

## 4. Concatenation, and the `O(n²)` you will write by accident

`a + b` must allocate a new string of length `len(a) + len(b)` and copy both in. So it is `O(len(a) + len(b))`. That is fine once. In a loop it is a disaster:

```python
chars = "polder sluice gate"

out = ""
for ch in chars:          # n iterations
    out += ch             # copies the whole accumulated string each time

print(out)
```

Iteration `i` copies `i` characters. Total work is `1 + 2 + 3 + ... + n = n(n+1)/2`, which is **`O(n²)`**.

The fix is to collect into a list and join once:

```python
chars = "polder sluice gate"

parts = []
for ch in chars:
    parts.append(ch)      # amortized O(1) each
out = "".join(parts)      # O(total length), one allocation

print(out)
```

`O(n)` total. `str.join` walks the sequence once to compute the final length, allocates exactly that much, and copies each piece in — one allocation, no repeated copying.

**The caveat you should know but must not lead with.** CPython contains an optimization: when the target of `+=` has a reference count of exactly 1, it can resize in place, making the loop amortized `O(n)`. It is real. It is also an implementation detail that silently stops applying the moment anything else holds a reference to that string, it is absent from other Python implementations, and no interviewer will give you credit for relying on it. State `O(n²)` for the naive loop. Mention the optimization only as a footnote, if at all.

**Related:** the same argument applies to lists. `result = result + [x]` in a loop is `O(n²)`; `result.append(x)` is `O(n)` total.

---

## 5. Splitting and joining

```python
"a,b,c".split(",")      # O(n) -> ['a', 'b', 'c']
"a b  c".split()        # O(n) -> ['a', 'b', 'c'], splits on runs of whitespace
"".join(parts)          # O(total chars)
"-".join(parts)         # O(total chars + separators)
```

Both are `O(n)` time and `O(n)` space. `split()` with no argument is not the same as `split(" ")` — the no-argument form collapses runs of whitespace and strips the ends, which is almost always what you want when tokenizing a sentence.

```python
"  a  b  ".split()       # ['a', 'b']
"  a  b  ".split(" ")    # ['', '', 'a', '', 'b', '', '']
```

That difference has cost people correctness in real interviews. Know which one you typed.

---

## 6. Substring search — state the worst case

```python
sub in s          # O(n * m) worst case
s.find(sub)       # same; returns -1 if absent
s.index(sub)      # same; raises ValueError if absent
s.count(sub)      # O(n * m)
s.replace(a, b)   # O(n * m) time, O(n) space for the new string
```

where `n = len(s)` and `m = len(sub)`.

The naive algorithm tries each of `n - m + 1` starting positions and compares up to `m` characters — hence `O(n · m)`. That is the contract, and it is what you should say.

**The reality:** CPython 3.10 and later use a mix of a tuned naive scan for short needles and the **two-way (Crochemore–Perrin)** algorithm for longer ones, which is `O(n + m)` worst case. So the pathological input that used to make `in` quadratic no longer does.

**How to say this in an interview:** *"`in` is O(n·m) worst case by contract. CPython 3.10+ uses a two-way algorithm for long needles so in practice it is O(n+m), but I would not rely on that."* Leading with the implementation detail sounds like you are dodging; leading with the contract and then adding the detail sounds like you know the language. Week 9 makes you implement KMP so you can derive the `O(n + m)` bound yourself.

---

## 7. The transforming methods — all `O(n)`, all allocate

```python
s.upper()      s.lower()      s.strip()
s.lstrip()     s.rstrip()     s.title()
s.replace(a, b)
```

Every one is `O(n)` time and `O(n)` space, because every one returns a **new string**. This is the second-most-common silent cost. `s = s.strip().lower()` inside a loop over `n` strings is `O(total characters)`, which is usually fine — but if the same string is re-normalized on every iteration, hoist it out.

Cheap membership tests that do **not** allocate:

```python
ch.isalpha()    ch.isdigit()    ch.isalnum()    ch.isspace()    # O(1) on a single char
s.startswith(p)                                                  # O(len(p))
s.endswith(p)                                                    # O(len(p))
```

---

## 8. Comparison

```python
a == b     # O(min(len(a), len(b))) — early exit on first mismatch
a < b      # same; lexicographic
```

Equality is `O(1)` when the lengths differ, because Python checks length first. It can also be `O(1)` when both strings are interned to the same object — but do not claim that; it is not guaranteed.

Sorting characters:

```python
sorted(s)              # O(n log n) -> a LIST of chars, not a string
"".join(sorted(s))     # O(n log n) -> a string
```

That second line is the canonical **anagram key**: two words are anagrams exactly when their sorted characters match. It is `O(n log n)` per word. A `Counter` gives you the same grouping in `O(n)` — Lecture 3 covers why you would still sometimes choose the sort.

---

## 9. Worked example: the same problem, three ways

**Task.** Given a string, return it with every run of repeated characters collapsed to a single character. `"aaabbbcccd"` becomes `"abcd"`.

**Version 1 — the accidental quadratic.**

```python
def collapse_v1(s):
    out = ""
    for ch in s:
        if out == "" or ch != out[-1]:
            out += ch          # O(len(out)) each time
    return out
```

Time `O(n²)` worst case (input with no repeats — `out` grows to length `n`). Space `O(n)` for the output, but `O(n²)` total allocation churn.

**Version 2 — list plus join.**

```python
def collapse_v2(s):
    parts = []
    for ch in s:
        if not parts or ch != parts[-1]:
            parts.append(ch)   # amortized O(1)
    return "".join(parts)      # O(n)
```

Time `O(n)`. Auxiliary space `O(n)` for `parts`; output space `O(n)`. Note `parts[-1]` is `O(1)` — indexing the last element of a list is free.

**Version 3 — same cost, fewer lines.**

```python
def collapse_v3(s):
    return "".join(ch for i, ch in enumerate(s) if i == 0 or ch != s[i - 1])
```

Time `O(n)`. Space `O(n)` for the output. The generator expression itself is `O(1)` space — `join` consumes it lazily. This is the one place a generator beats a list comprehension on space, and it is worth knowing why: `[...]` materializes the whole list first, `(...)` does not.

**The Examine sentence for version 2:**

> **Time O(n)** because we make one pass and each append is amortized O(1). **Space O(n)** auxiliary for the parts list, O(n) output. The alternative was string concatenation in the loop at O(n²) time — I chose collect-then-join because it turns n allocations into one.

---

## 10. Check yourself

Answer before moving to Lecture 2. Cover the cheat sheet. Say each answer out
loud first — the interview is spoken — then open the fold and compare.

**1.** What are the time **and** space costs of `s[2:8]`?

<details>
<summary>Answer</summary>

`O(k)` time and `O(k)` space, where `k` is the length of the slice — six here.
A slice is a **new string**: Python copies the characters into a fresh
allocation. There is no view type for `str`, so there is no way to take a slice
without paying for it. Say both numbers; a candidate who gives only the time is
answering half the question.

</details>

**2.** Why does `for ch in s: out += ch` cost `O(n²)`, and what is the fix?

<details>
<summary>Answer</summary>

Because strings are immutable, `out += ch` cannot extend `out` in place — it
allocates a new string and copies everything accumulated so far. Iteration `i`
copies `i` characters, so the total is `1 + 2 + … + n = n(n+1)/2`, which is
`O(n²)`.

The fix is to collect into a list and join once:

```python
parts = []
for ch in s:
    parts.append(ch)
out = "".join(parts)
```

`str.join` walks the sequence once to compute the final length, allocates
exactly that much, and copies each piece in — one allocation, `O(n)` total.

</details>

**3.** What is the worst-case cost of `"abc" in text`, and what does CPython actually do?

<details>
<summary>Answer</summary>

The bound to state is `O(n·m)` — `n` the length of `text`, `m` the length of the
needle — because that is what naive scan-and-compare costs and it is the answer
you can defend from first principles.

Then add what actually happens: CPython does not scan naively. It uses a
Horspool-style bad-character skip for short needles and switches to the
Crochemore–Perrin *two-way* algorithm for longer ones, which is `O(n + m)` in
the worst case. Lead with the bound, follow with the implementation note. That
order is what reads as "knows the theory and has read the source", rather than
"memorised a trivium".

</details>

**4.** `"  a  b  ".split()` versus `"  a  b  ".split(" ")` — what does each return?

<details>
<summary>Answer</summary>

```python
"  a  b  ".split()      # ['a', 'b']
"  a  b  ".split(" ")   # ['', '', 'a', '', 'b', '', '']
```

With no argument, `split` treats any **run** of whitespace as one separator and
discards leading and trailing whitespace. Given an explicit separator it splits
on **every single occurrence**, so each adjacent pair of spaces yields an empty
string between them.

This is the bug behind half the "why is there an empty string in my list"
questions. Default to the no-argument form unless you genuinely need to preserve
empty fields — parsing a CSV line, where an empty field is data.

</details>

**5.** `s.startswith("http")` versus `s[:4] == "http"` — same result. Why prefer the first?

<details>
<summary>Answer</summary>

Both are correct, including on a string shorter than four characters. Prefer
`startswith` for three reasons:

- It allocates nothing. The slice builds a throwaway four-character string first.
- The `4` is a magic number that has to be kept in step with the literal. Change
  the prefix to `https` and forget the slice length, and the check silently
  starts lying.
- It takes a tuple: `s.startswith(("http://", "https://"))` is one call.

It also states intent. `startswith` reads as a question about a prefix; the
slice reads as arithmetic that happens to be about a prefix.

</details>

**6.** Building a 26-element `counts` list with `ord(ch) - ord('a')` — what is the space complexity, and how do you justify the answer out loud?

<details>
<summary>Answer</summary>

`O(1)` auxiliary space. The list has 26 entries whether the input is 10
characters or 10 million — its size is fixed by the alphabet, not by `n`.

The out-loud justification is the part being graded: *"The counts array is
bounded by the alphabet size, which is a constant 26 for lowercase ASCII and
does not grow with the input, so it is `O(1)` auxiliary space. If the alphabet
were a parameter — Unicode, say — I would call it `O(σ)` and say what `σ` is."*

Naming the assumption and then saying what happens when it is dropped is what
separates a memorised answer from an understood one.

</details>

**7.** `"".join(sorted(word))` — what is it for, and what does it cost?

<details>
<summary>Answer</summary>

It is the **canonical form** of a word: two words are anagrams exactly when
their sorted letters are equal, so this expression is the key you group
anagrams by.

For a word of length `m` it costs `O(m log m)` time — the sort dominates — and
`O(m)` space for the intermediate list of characters and the joined result. When
grouping `n` words, that is `O(n · m log m)` overall.

Worth knowing: for a fixed small alphabet you can key by a 26-slot count tuple
instead and drop the log factor to `O(m)`. Offer that only after the sorted-key
version is on the board and working.

</details>

**8.** Why can a string be a dict key when a list cannot?

<details>
<summary>Answer</summary>

Because a string is immutable, so its hash is fixed for its lifetime. A dict
places a key in a bucket chosen from its hash at insertion time and looks it up
the same way later; that only works if the hash cannot change underneath it.

A list is mutable. If a list could be a key, appending to it after insertion
would change its hash, and the entry would sit in a bucket the lookup no longer
visits — present in the dict and unreachable. Python forecloses that by giving
`list` no `__hash__` at all, so the attempt fails loudly at insertion rather
than quietly at lookup.

The general rule: hashable means immutable **all the way down**. A tuple is
hashable until it contains a list, at which point hashing it raises.

</details>

---

## Up Next

[Lecture 2 — Lists, Tuples and the Dynamic Array](02-lists-tuples-and-the-dynamic-array.md) — where `append` is amortized `O(1)`, the front of the list is expensive, and `[[0] * 3] * 2` is a bug.
