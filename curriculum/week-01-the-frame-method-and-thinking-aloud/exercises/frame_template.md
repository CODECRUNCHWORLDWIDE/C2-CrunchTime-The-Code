# Problem N: <title>

> <One-line restatement of the problem in your own words. Not a copy of the prompt — if you cannot compress it to one sentence, you have not finished Frame.>

**Pattern:** <pattern name, e.g. "Two-pointer, converging">
**Difficulty:** Easy / Medium / Hard
**My solve time:** <minutes>
**My FRAME narration recording:** <link to file or "see ./drill-NN-recording.m4a">

---

## F — Frame

- **Input:** <type, shape, what each part means>
- **Output:** <type, format, and what comes back when there is no answer>
- **Clarifying questions I'd ask in an interview:**
  - <q1>
  - <q2>
- **Worked examples by hand:**
  - `<input>` → `<output>` because <reason>
  - `<input>` → `<output>` because <reason>

## R — Research constraints

- **Size bounds:** `<bound>` — which rules out <complexity class>.
- **Properties I can exploit:** <sorted? unique? bounded range? nothing?>
- **Awkward inputs and what each should return:**
  - Empty input → <expected>
  - Single element → <expected>
  - All duplicates → <expected>
  - <negatives / ties / max size, whichever apply> → <expected>
- **Assumptions I'm making (be explicit):**
  - <assumption 1>
  - <assumption 2>
- **What makes this hard, in one sentence:** <the one thing>

## A — Assess options

I recognized this as a **<pattern>** problem because:

- <signal 1>
- <signal 2>

| Approach | Time | Space | Verdict |
|----------|------|-------|---------|
| <the simple one — always list it first> | <O(?)> | <O(?)> | Rejected: <reason> |
| <alternative> | <O(?)> | <O(?)> | Rejected: <reason>. Would win when <case>. |
| **<chosen>** | <O(?)> | <O(?)> | **Chosen:** <reason> |

**Plan, in English, before any code:**

1. <starting state — which variables, set to what>
2. <the loop or recursion>
3. <the decision inside it>
4. <termination condition and what is returned then>
5. <where the awkward inputs from R are handled>

## M — Make the solution

```python
def my_solution(<args>) -> <return type>:
    # <one-line comment that explains intent, not what the line does>
    <code>
```

Decisions I narrated while writing it:

- <why this variable name / this data structure / this guard placement>

## E — Examine

Trace on a small input — pick a **hostile** one, not one you expect to pass:

| Step | Variable A | Variable B | Action |
|-----:|:----------:|:----------:|--------|
| 0    | <val>      | <val>      | Initial |
| 1    | <val>      | <val>      | <what happened> |
| …    |            |            |        |

Edge cases from **R**, verified:

- Empty input → <actual behavior> ✓
- Single element → <actual behavior> ✓
- All duplicates → <actual behavior> ✓

Bug I caught while examining (if any): <describe and fix>

- **Time complexity:** **O(<n>)** because <reason>.
- **Space complexity:** **O(<1 or n>)** because <reason>.
- **Is this the floor?** <yes, because every element must be read / no, because …>
- **Tradeoffs:**
  - <alternative approach 1>: <time> / <space> — wins when <case>.
  - <alternative approach 2>: <time> / <space> — wins when <case>.
- **What I'd change in a real codebase:** <naming, abstractions, error handling>

---

## Self-feedback

- What I did well: <three things>
- What I'd do differently next time: <three things>
- Pattern recognition speed: <seconds it took to name the shape in step A>
- Did any step send me backwards? <e.g. "Examine found a case R never listed, so I went back to R"> — this is the method working, not failing.

---

## Provenance

Where this problem came from: <the C2 drill or challenge file, or — for a homework
"wild problem" — the practice site you pulled it from>
First attempted: <date>
Last reviewed: <date>

> Re-derive rather than re-read. If "last reviewed" is more than a month old,
> solve it again from the statement before you trust anything below it.
