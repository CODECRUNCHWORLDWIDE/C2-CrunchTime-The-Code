# Problem N: <title>

> <One-line restatement of the problem in your own words. Link to the original prompt at the end.>

**Pattern:** <pattern name, e.g. "Two-pointer, converging">
**Difficulty:** Easy / Medium / Hard
**My solve time:** <minutes>
**My UMPIRE narration recording:** <link to file or "see ./drill-NN-recording.m4a">

---

## U — Understand

- **Input:** <type, shape, bounds>
- **Output:** <type, format, empty case>
- **Clarifying questions I'd ask in an interview:**
  - <q1>
  - <q2>
- **Assumptions I'm making (be explicit):**
  - <assumption 1>
  - <assumption 2>
- **Worked examples by hand:**
  - `<input>` → `<output>` because <reason>
  - `<input>` → `<output>` because <reason>

## M — Match

I recognized this as a **<pattern>** problem because:

- <signal 1>
- <signal 2>

Alternative pattern I considered and rejected: <alt pattern>, because <reason>.

## P — Plan

In English, before any code:

1. <step 1>
2. <step 2>
3. <step 3>
4. <termination condition>
5. <edge case handling>

## I — Implement

```python
def my_solution(<args>) -> <return type>:
    # <one-line comment that explains intent, not what it does>
    <code>
```

## R — Review

Trace on small input:

| Step | Variable A | Variable B | Action |
|-----:|:----------:|:----------:|--------|
| 0    | <val>      | <val>      | Initial |
| 1    | <val>      | <val>      | <what happened> |
| …    |            |            |        |

Edge cases I verified:

- Empty input → <expected behavior>
- Single element → <expected behavior>
- All duplicates → <expected behavior>

Bug I caught while reviewing (if any): <describe and fix>

## E — Evaluate

- **Time complexity:** **O(<n>)** because <reason>.
- **Space complexity:** **O(<1 or n>)** because <reason>.
- **Tradeoffs:**
  - <alternative approach 1>: <time> / <space> — wins when <case>.
  - <alternative approach 2>: <time> / <space> — wins when <case>.
- **What I'd change in a real codebase:** <variable naming, abstractions, etc.>

---

## Self-feedback

- What I did well: <three things>
- What I'd do differently next time: <three things>
- Pattern recognition speed: <seconds it took to identify>

---

## Source

Original prompt: <link>
First attempted: <date>
Last reviewed: <date>
