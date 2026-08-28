# Mini-Project — Six Sliding-Window Write-Ups with 30-Second Pattern-Recognition Memos

> The week's deliverable: a single, compact portfolio artifact that demonstrates **Research-constraints fluency** across all four sliding-window sub-shapes. The 30-second memo per problem is the discriminating element — interviewers grade Research constraints harder than candidates expect.

**Estimated time:** 7 hours, split across Thursday–Saturday.

This mini-project is *content-heavy* rather than *infrastructure-heavy*. You will produce six write-ups — one full FRAME pass each — anchored by a 30-second pattern-recognition memo at the very top. The Research constraints memos are the artifact's signature element; the rest of each write-up is standard FRAME.

The six problems below are stated in full. Every one of them is a **different contract** from the drill that shares its shape — a different return type, a different tie-break, a different sentinel for "impossible." That is deliberate. If you can paste a drill solution into a mini-project problem and pass, the mini-project has taught you nothing.

---

## Why this matters

Two reasons.

1. **Research constraints is the under-practiced step.** In Weeks 1–2 the *Make the solution* step got most of the attention because the patterns (two-pointer, hash map) were new. By Week 3 the implementation is increasingly mechanical; the *recognition* — naming the pattern in 30 seconds and stating the invariant — is where the interview points move. This mini-project is the first one in C2 that grades Research constraints as strictly as Make the solution.

2. **Sliding window has more confusable sub-shapes than any earlier pattern.** Fixed vs variable. Shape A vs shape B vs shape C. Frequency vs sum vs set as state. Six write-ups that each *explicitly disambiguate* the sub-shape force you to articulate the differences out loud. By the sixth, the disambiguation is reflexive.

---

## What you ship

Seven files: six problem write-ups plus a short overview.

```
frame-writeups/c2-week-03/mini-project/
├── README.md                              ← short overview + index
├── problem-01-maintenance-window.md       ← fixed-size, running sum, minimum
├── problem-02-reprint-run.md              ← variable shape A, multiplicity invariant
├── problem-03-pallet-seal.md              ← fixed-size + frequency invariant, returns positions
├── problem-04-recall-window.md            ← variable shape B, counting invariant
├── problem-05-tasting-flights.md          ← variable shape C, at-most-K distinct, counting
└── problem-06-rehearsal-block.md          ← variable shape B + frequency, matched count
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

These six filenames are what **you** create in your portfolio repo — they are not files in this course.

---

## The 30-second pattern-recognition memo (the signature element)

At the top of every write-up, immediately after the title, place a single bordered block in this exact shape:

```markdown
> **30-second pattern-recognition memo:**
> This is a sliding-window problem because [contiguity signal from the prompt].
> The window is [fixed-size with k = ... / variable-size].
> The shape is [fixed / A "longest" / B "shortest" / C "count"], because [signal].
> The invariant is: [property maintained at every iteration].
> The auxiliary state is: [running sum / frequency table / last-index map / frequency table plus a matched count].
> Why not [alternative]: [one sentence].
```

Five lines, optionally six (the negative-space sentence). Read aloud, it takes 25–30 seconds. That is the cadence at which a senior interviewer wants to hear Research constraints.

Worked example, for Exercise 2 (The Longest Clean Run):

> **30-second pattern-recognition memo:**
> This is a sliding-window problem because the prompt asks for the longest contiguous stretch of parts with a property.
> The window is variable-size; its length emerges from the data rather than arriving as input.
> The shape is A "longest," because I expand `right` and shrink `left` only while the invariant is broken, then record.
> The invariant is: every die ID inside `stamps[left..right]` is distinct.
> The auxiliary state is: a dict mapping each die ID to the most recent index at which it was seen.
> Why not a plain hash map: a hash map alone answers "have I ever seen this ID," not "have I seen it *inside the current contiguous slice*," which is the question the window structure exists to answer.

Six write-ups, six memos. By the sixth, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from five axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 30% | Five lines, all five elements named, hits cadence on read-aloud |
| Research constraints section (expanded body) | 25% | Explicit comparison against at least one other sub-shape; explicit rejection of one wrong pattern ("not two-pointer because...") |
| Make the solution + Examine (verify) | 20% | Clean code; trace on at least two of the stated examples; one common bug called out and avoided |
| Examine (cost) (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the amortized-`O(n)` defence sentence |
| Cross-references | 10% | Each write-up links to the relevant lecture section and at least one *other* mini-project write-up |

A grade of "great" on all six write-ups is the bar.

---

## The six problems

### Problem 1 — The Quietest Maintenance Window

**Sub-shape.** Fixed-size, running sum.

**Spec.** A data centre logs the number of API requests it served in each hour of operation, in chronological order. Operations must take the cluster offline for exactly `k` consecutive hours. Return the **total number of requests that would be lost** during the quietest such block — that is, the smallest total over any `k` consecutive hours.

Return `None` if `k` is larger than the log, or if the log is empty.

```python
def quietest_window_cost(requests: list[int], k: int) -> int | None:
    """Return the smallest total over any k consecutive hours of the log.
    Return None when k exceeds len(requests) or the log is empty."""
```

**Constraints.**

- `0 <= len(requests) <= 400_000`. A decade of hourly logs is about 88,000 entries, so this covers any real cluster with room to spare. The bound rejects the rescan: recomputing `sum(requests[i:i+k])` inside the loop is `O(n·k)`, which at `k` near `n` is roughly `1.6×10^11` additions and will not finish.
- `0 <= requests[i] <= 5_000_000`. A very busy hour on a large cluster. Counts are non-negative, so there is no sign trap here — the trap is that a block total can exceed `2^31`. That costs you nothing in Python, and it is worth one sentence in Examine (cost) about what a Java or C++ translation would need.
- `1 <= k`. A zero-hour outage is not an outage, so it is excluded from the contract rather than given an answer.

**Examples.**

- `requests = [80, 20, 30, 90, 10], k = 2` → `50`. Block totals by start: `100, 50, 120, 100`. The minimum is 50. This is the sanity example.
- `requests = [3, 4, 5], k = 2` → `7`. Totals are `7, 9`. This is the example that punishes the common wrong approach: seeding `best = 0` works for a maximum and is catastrophic for a minimum — the update never fires and the function returns 0.
- `requests = [0, 0, 0], k = 2` → `0`. A minimum of zero is a legitimate answer, not "no answer." If your code returns `None` here you have confused *no data* with *a total of zero*.
- `requests = [7], k = 1` → `7`. One hour, one block.
- `requests = [5, 5], k = 3` → `None`. The block does not fit.
- `requests = [], k = 1` → `None`. Empty log.

**Why included.** The simplest fixed-size window, and the cleanest contrast with Exercise 1. Same loop, opposite combine step, and — this is the point your memo should make — **no tie-break rule at all**, because the answer is a value rather than a position. Confirming the *absence* of a tie-break is itself a contract fact worth saying out loud in Frame.

**Stretch in your write-up:** state, in one sentence, what would have to be added to this contract if the caller wanted the *position* of the quietest block instead of its cost. Then say which of Exercise 1's rules you would reuse verbatim.

---

### Problem 2 — The Longest Reprint Run

**Sub-shape.** Variable-size, shape A, multiplicity invariant.

**Spec.** A bindery feeds a stack of book blocks through a trimmer. Each block carries the title code of the book it belongs to, and the stack is logged bottom to top. The trimmer blade dulls on repetition: a single pass tolerates the same title code at most `m` times before the blade must be reground.

Return the **length of the longest contiguous run of blocks** in which no title code appears more than `m` times.

If `m` is `0`, or the stack is empty, return `0`.

```python
def longest_reprint_run(titles: list[str], m: int) -> int:
    """Return the length of the longest contiguous run of blocks in which no
    title code appears more than m times. Return 0 when m is 0 or the stack
    is empty."""
```

**Constraints.**

- `0 <= len(titles) <= 300_000`. A month of bindery output. The bound rejects the restart-from-every-start brute force, which is about `4.5×10^10` counter operations here and will not finish.
- `0 <= m <= 50`. A blade tolerance. `m = 0` is legal input **and it is the guard case**: it drives the shrink loop until the window is empty, which is exactly where an unguarded `right - left + 1` reports a length for a window that does not exist.
- Title codes come from a catalogue of at most 2,000 codes, so the frequency table holds at most `min(n, 2000)` entries and the space claim is `O(min(n, 2000))` rather than a vague `O(n)`.

**Examples.**

- `titles = ["A", "B", "A", "A", "C", "A"], m = 2` → `4`. The run at indices 1–4 is `B, A, A, C`: `A` appears twice, `B` and `C` once each. Extending it either way puts a third `A` in the window. Indices 0–2 and 3–5 are also valid at length 3, so 4 is the answer.
- `titles = ["A", "A", "A", "B", "B", "B"], m = 2` → `4`. **This is the example that punishes the common wrong approach.** The valid run is indices 1–4, `A, A, B, B`. A solution that shrinks on `len(counts) > m` — the *at-most-K-distinct* condition from Exercise 5 — sees only two distinct titles in the whole stack and returns 6. The invariant here is on **multiplicity**, not on distinctness. Getting these two confused is the single graded error of this problem.
- `titles = ["A", "A", "A"], m = 1` → `1`. Every run of two already repeats.
- `titles = ["A", "B", "C"], m = 5` → `3`. The tolerance exceeds any possible count, so the invariant never breaks and the shrink loop never executes.
- `titles = ["A", "B"], m = 0` → `0`. Zero tolerance passes nothing.
- `titles = [], m = 2` → `0`. Empty stack.

**Why included.** Shape A with a *different invariant* from either Exercise 2 or Exercise 5. It is also the one place in the week where you can check only **one** count per iteration rather than the whole table: adding `titles[right]` can only raise that one title's count, so it is the only count that can have broken the invariant. Say that in Research constraints — it is a genuine efficiency observation, not a trick.

**Stretch in your write-up:** explain why the "delete the key when its count hits zero" discipline, which is load-bearing in Exercise 5, is *optional* here. (Hint: you never call `len(counts)`.)

---

### Problem 3 — The Pallet Seal Check

**Sub-shape.** Fixed-size, frequency invariant, returns positions.

**Spec.** A packing line seals pallets. A scanner reads the SKU of each carton as it passes, in order. A pallet is valid when its cartons match a **manifest** exactly: the same SKUs with the same multiplicities. Order within the pallet does not matter.

Return the **starting index of every valid pallet**, in ascending order, as a list. Pallets overlap: positions 0 and 1 are two different candidate pallets and both are checked.

If the manifest is empty, return `[]`. If the manifest is longer than the scan, return `[]`.

```python
def valid_pallet_starts(scan: list[str], manifest: list[str]) -> list[int]:
    """Return, ascending, every index i such that the multiset of
    scan[i : i + len(manifest)] equals the multiset of manifest.
    Return [] when manifest is empty or longer than scan."""
```

**Constraints.**

- `0 <= len(scan) <= 200_000`. A shift on a fast line. The bound rejects rebuilding a fresh `Counter` for every candidate pallet, which is `O(n·m)` and lands near `10^10` operations at the worst ratio.
- `0 <= len(manifest)`; a manifest longer than the scan is legal input and returns `[]`.
- SKUs are drawn from a catalogue of at most 40 codes. This bound is load-bearing in Examine (cost): it makes a whole-table comparison `O(40) = O(1)` per slide, which is what lets you claim `O(n)` overall. State the bound, then state what breaks without it — an unbounded catalogue makes each comparison `O(|catalogue|)` and the matched-count trick becomes necessary rather than optional.

**Examples.**

- `scan = ["X1", "X1", "Y2", "X1", "Y2", "X1"], manifest = ["X1", "Y2"]` → `[1, 2, 3, 4]`. Pallet size 2. By start index: `X1 X1` ✗, `X1 Y2` ✓, `Y2 X1` ✓, `X1 Y2` ✓, `Y2 X1` ✓. Overlapping pallets both count — settle that in Frame, not in Examine (verify).
- `scan = ["X1", "Y2", "Y2", "X1", "X1", "Y2"], manifest = ["X1", "X1", "Y2"]` → `[2, 3]`. **This is the example that punishes the common wrong approach.** Pallet size 3. The four candidates are `{X1:1, Y2:2}` ✗, `{Y2:2, X1:1}` ✗, `{Y2:1, X1:2}` ✓, `{X1:2, Y2:1}` ✓. A solution comparing *sets* of distinct SKUs sees `{X1, Y2}` in all four and returns `[0, 1, 2, 3]`. The manifest is two of one SKU and one of the other, not "some of each."
- `scan = ["X1", "X1", "X1"], manifest = ["X1"]` → `[0, 1, 2]`. The degenerate case: pallet size 1, every position valid.
- `scan = ["X1", "Y2"], manifest = ["Z3"]` → `[]`. The no-solution case. Return the empty list, not `None`.
- `scan = ["X1"], manifest = ["X1", "Y2"]` → `[]`. The manifest is longer than the scan. Note that building the first window from `scan[:2]` silently yields `["X1"]` — Python truncates rather than raising — and you would then compare a one-carton window against a two-carton manifest. Guard the length first.
- `scan = ["X1"], manifest = []` → `[]`. Defined by the contract, not derived. Say so in Frame.
- `scan = [], manifest = ["X1"]` → `[]`. Empty scan.

**Why included.** Same window and same invariant as Exercise 3, different **combine** step: you append `right - len(manifest) + 1` where the drill incremented a counter. Naming that as the only difference — and being right about it — is exactly the sort of structural observation that reads as senior.

**Stretch in your write-up:** compare explicitly with Exercise 3. Same window size, same frequency invariant, different return type, and one consequence you should name: a solution that returns early on the first match solves neither, but for two different reasons.

---

### Problem 4 — The Shortest Recall Window

**Sub-shape.** Variable-size, shape B, counting invariant.

**Spec.** A production line logs an inspection verdict for every unit it makes, in order: the string `"pass"` or the string `"fail"`. A recall must cover a **contiguous run of units** containing at least `q` failures.

Return the **length of the shortest such run**. If the line never accumulates `q` failures, return `0`.

```python
def shortest_recall_window(verdicts: list[str], q: int) -> int:
    """Return the length of the shortest contiguous run of units containing at
    least q failures. Return 0 when no run contains q failures."""
```

**Constraints.**

- `0 <= len(verdicts) <= 500_000`. A quarter of output on a high-volume line. The bound rejects checking every start/end pair, which is about `1.25×10^11` steps here.
- `1 <= q <= 1_000`. **The lower bound of 1 is what makes `0` a safe sentinel.** A run of length zero can never contain one or more failures, so `0` is unambiguous as "impossible." Exercise 4 could not use `0` because its quota could be met by a run of any length and a zero-length answer was a shape a buggy solution could produce. Same family, opposite decision, and your write-up must say why. If `q` could be `0`, the empty run would qualify and `0` would become ambiguous — that is the whole reason the bound starts at 1.
- Verdicts are exactly the two strings and nothing else. The window's entire state is therefore a single integer — a failure count — so the space claim is `O(1)`, not `O(n)`.

**Examples.**

- `verdicts = ["pass", "fail", "pass", "pass", "fail", "pass", "fail"], q = 2` → `3`. Failures sit at indices 1, 4, and 6. The run 4–6 holds two failures in three units; the run 1–4 holds two in four. Three is the answer.
- `verdicts = ["pass", "fail", "fail"], q = 2` → `2`. **This is the example that punishes the common wrong approach.** The correct shrink loop records the window length *before* dropping `verdicts[left]`. A solution that drops first and records second walks left past both failures and reports `1` — a one-unit run containing two failures, which is arithmetically impossible and should stop you cold in Examine (verify).
- `verdicts = ["fail", "pass", "pass", "pass", "fail"], q = 2` → `5`. The whole log is the only qualifying run. A solution that shrinks too eagerly loses it.
- `verdicts = ["fail", "fail", "pass"], q = 2` → `2`. The qualifying run sits at the very start, before any shrinking has happened.
- `verdicts = ["pass", "pass", "pass"], q = 1` → `0`. The no-solution case.
- `verdicts = [], q = 1` → `0`. Empty log.

**Why included.** Shape B with a **counting** invariant rather than a sum, which forces you to state the shrink condition as `failures >= q` rather than reaching for a running total by reflex. It is also the week's clearest lesson in sentinel choice: `None` and `0` are both defensible, and which one is correct depends on whether zero is reachable as a real answer.

**Stretch in your write-up:** explicitly name the positivity argument. A failure count can only decrease when you drop a unit from the left, never increase — the same monotonicity that non-negative inflow gives Exercise 4. Say what the analogue of a "negative reading" would be here, and why the domain rules it out.

---

### Problem 5 — The Tasting Flight Count

**Sub-shape.** Variable-size, shape C, at-most-K distinct, counting.

**Spec.** A brewery's bar is a row of taps, each pouring exactly one beer style, logged left to right along the counter. A **flight** is any contiguous run of one or more taps. A guest carrying a `k`-glass paddle can only manage `k` distinct styles.

Return **how many flights contain at most `k` distinct styles**. Flights are identified by position, so two runs with identical style sequences at different places along the bar count separately.

If `k` is `0`, or the bar is empty, return `0`.

```python
def flights_within_paddle(taps: list[str], k: int) -> int:
    """Return the number of contiguous runs of one or more taps containing at
    most k distinct styles. Return 0 when k is 0 or taps is empty."""
```

**Constraints.**

- `0 <= len(taps) <= 200_000`. A very large taproom, chosen so the answer itself is instructive: with `k` large enough, every run qualifies and the count is `n(n+1)/2`, about `2×10^10`. That fits a Python `int` without comment and would overflow a 32-bit counter — one sentence in Examine (cost). The bound also rules out *enumerating* the runs at all: there are `Θ(n²)` of them and you cannot list what you must count.
- `0 <= k <= 30`. A paddle holds at most 30 glasses. `k = 0` is legal and returns `0`.
- Styles come from a menu of at most 60 names, so the frequency table is `O(min(k + 1, 60))` and therefore `O(1)`.

**Examples.**

- `taps = ["ipa", "stout", "ipa", "lager"], k = 2` → `8`. Count it by length first: all four single taps qualify; all three adjacent pairs qualify; of the two triples, `ipa stout ipa` qualifies and `stout ipa lager` does not; the full row has three styles and does not. That is `4 + 3 + 1 = 8`.

  Now count the same input the shape-C way, because **this is where the common wrong approach shows up**. At each `right`, after restoring the invariant, the number of valid flights *ending at* `right` is `right - left + 1`. Running it: `right = 0` adds 1; `right = 1` adds 2; `right = 2` adds 3; `right = 3` breaks the invariant, shrinks `left` to 2, and adds 2. Total 8. A solution that adds `1` per `right` — counting only the single longest valid flight ending there — returns 4 and looks entirely plausible until you check it against the enumeration above.
- `taps = ["ipa", "ipa", "ipa"], k = 1` → `6`. Every run qualifies: `3 + 2 + 1`.
- `taps = ["ipa", "stout"], k = 1` → `2`. Only the two singles. The pair has two styles.
- `taps = ["ipa", "stout"], k = 5` → `3`. More glasses than styles; the invariant never breaks and every run qualifies.
- `taps = ["ipa"], k = 0` → `0`. Zero glasses carry nothing. Note that the shrink loop drives `left` past `right` here, so `right - left + 1` is `0` and the sum stays `0` — but say in your write-up whether your code reaches that by construction or by a guard, and which you prefer.
- `taps = [], k = 3` → `0`. Empty bar.

**Why included.** Shape C is the only sub-shape none of the five drills covers, and it is the one the homework's "exactly K" problem composes twice. The combine step — `answer += right - left + 1` — is one line, and the *justification* for that line is the whole problem: once the invariant holds at `right`, every run starting anywhere in `[left, right]` and ending at `right` also holds it, because dropping taps from the left can never increase the distinct count.

**Stretch in your write-up:** state the monotonicity argument above in one sentence, and then say what breaks if the invariant were *not* monotone under shrinking — for instance "at least `k` distinct styles." That failure is why shape C does not generalise to every predicate.

---

### Problem 6 — The Tightest Rehearsal Block

**Sub-shape.** Variable-size, shape B, frequency invariant, matched count.

**Spec.** An orchestra's rehearsal day is a schedule of ten-minute slots. Each slot is logged with the name of the one instrument section called to it, in order. A sectional coach has a **call sheet**: a list of section names, with repeats meaning "this section must be called this many times."

Return the **shortest contiguous block of slots that covers the whole call sheet**, counting duplicates, as `(start, length)`. Slots holding sections the call sheet does not want are simply ignored — they do not disqualify a block, but they do lengthen it.

- If several blocks tie on length, return the one with the **smallest** start. The coach takes the earliest slot that works, because the hall empties as the day goes on.
- If the call sheet is empty, return `(0, 0)`.
- If no block covers the call sheet, return `None`.

```python
def tightest_rehearsal_block(schedule: list[str], call: list[str]) -> tuple[int, int] | None:
    """Return (start, length) for the shortest contiguous block of schedule
    containing every section on call, counting duplicates. Ties break toward
    the smaller start. An empty call sheet returns (0, 0); an uncoverable call
    sheet returns None."""
```

**Constraints.**

- `0 <= len(schedule) <= 400_000`. A festival season of slots. The bound rejects walking forward from every start until the call sheet is covered, which is `O(n · len(call))`.
- `0 <= len(call) <= 50_000`. A call sheet longer than the schedule is legal input and returns `None` with no window work at all; guard it and say why in Research constraints.
- Section names come from a roster of at most 30 sections. That bound is small enough that comparing the window's whole frequency table against the call sheet's on every shrink step is *tempting* — `O(30)` looks free. Name the temptation, then reject it: the matched-count integer makes each step `O(1)` and, more importantly, makes the invariant something you **maintain** rather than something you **re-derive**. The second property is what an interviewer is listening for.
- A section on the call sheet that never appears in the schedule makes it uncoverable. So does one that appears, but fewer times than required. Both return `None`, and they are different failure modes worth separate tests.

**Examples.**

- `schedule = ["vln", "vla", "cel", "vln", "vla", "cel"], call = ["vln", "vla", "cel"]` → `(0, 3)`. **This is the example that punishes the common wrong approach, and it is the reason this problem exists.** Four blocks of length 3 cover the call sheet: starts 0, 1, 2 and 3. No shorter block can, since three distinct sections need three slots. The tie-break here goes to the **smallest** start — the *opposite* of Challenge 1's rule. Paste your kit-span solution in unchanged and it returns `(3, 3)`. The pattern transfers; the contract does not.
- `schedule = ["cel", "cel", "vln", "hrn", "vla", "cel", "vln"], call = ["vln", "vla", "cel"]` → `(4, 3)`. `vla` appears only at index 4, so every covering block contains it. The block at 4–6 is `vla, cel, vln`, length 3, and nothing shorter works. There is no tie here — this is the case that checks your length comparison independently of your tie-break.
- `schedule = ["vla", "vln", "vla", "vla", "vln"], call = ["vla", "vla"]` → `(2, 2)`. Duplicates on the call sheet are real requirements. A solution that treats the call sheet as a *set* declares victory at index 0 with a one-slot block and returns `(0, 1)`. Two viola slots means two.
- `schedule = ["vla", "vla", "vln"], call = ["vla", "vln"]` → `(1, 2)`. The surplus `vla` at index 0 must be trimmed; the `vla` at index 1 must not be. This catches the most common state bug — decrementing the matched count on *every* removal instead of only when a section's count drops *below* what the call sheet requires.
- `schedule = ["cel", "hrn", "vln"], call = ["vln", "cel"]` → `(0, 3)`. The `hrn` slot sits between the two sections wanted and cannot be removed. Irrelevant slots do not disqualify a block; they lengthen it. This is what separates "covers the call sheet" from "consists of the call sheet."
- `schedule = ["vln", "vln", "vln"], call = ["vln", "cel"]` → `None`. A required section never appears.
- `schedule = ["vla", "vln"], call = ["vla", "vla"]` → `None`. The section appears, but not often enough. Distinct failure mode from the one above; test both.
- `schedule = ["vln"], call = []` → `(0, 0)`. Defined by the contract. Note this is a *block*, not `None` — an empty requirement is satisfiable, unlike an impossible one.
- `schedule = [], call = ["vln"]` → `None`. Empty schedule.

**Why included.** This is the **discriminator**. It is Challenge 1's pattern — shape B, frequency invariant, matched count — with the tie-break inverted and the domain changed. That is on purpose, and you should say so openly in your write-up rather than pretending it is unrelated. What the mini-project is measuring is whether you can carry a *pattern* across a contract change. Most candidates can write the first five problems with care; this one proves the pattern is in muscle memory rather than memorized as a solution.

The two operators that carry the whole trick, restated:

- Increment the matched count only when a section's window count becomes **exactly equal** to its requirement. Going from two violas to three when the call sheet wants one must not increment again.
- Decrement it only when a section's window count becomes **strictly less** than its requirement. Going from three violas to two when the call sheet wants one must not decrement.

**Stretch in your write-up:** compare explicitly against Problem 3 (the pallet seal check). Both maintain a frequency invariant. Problem 3's window has a **fixed** size, so its invariant is table *equality* and the answer is a set of positions. This one's window is **variable**, so its invariant is table *containment* and the answer is a single shortest block. Show the lineage in three sentences.

---

## Acceptance criteria

- [ ] All six write-ups committed in `frame-writeups/c2-week-03/mini-project/`.
- [ ] Each write-up has the **30-second memo at the top** in the exact block format above.
- [ ] Each write-up has all five FRAME sections (Frame · Research constraints · Assess options · Make the solution · Examine).
- [ ] Each write-up's tests cover **every example stated in its spec**, plus at least one adversarial case you generated yourself.
- [ ] Each Examine (cost) section follows the **five-piece structure** from Week 2.
- [ ] Each Examine (cost) section includes the **amortized-`O(n)` defence sentence** for the variable-size shapes, or the equivalent `O(n)` defence for the fixed-size ones.
- [ ] The mini-project `README.md` is the index file linking to all six.
- [ ] At least six commits this week with meaningful messages — *"Add mini-project problem 4: shortest recall window"* is a good message.
- [ ] Repository is **still public** and the README still renders cleanly.

---

## Suggested order of operations

### Thursday — Problems 1, 2, 3 (2.5h)

1. Open your [Exercise 1](../exercises/exercise-01-staffing-block.md) write-up. Read your existing Research constraints section cold. Note what is thin.
2. Write the 30-second memo block for Problem 1. Read it aloud; time yourself.
3. Solve and write up Problem 1. It is short — the value is in the memo and in the "no tie-break" observation. Commit.
4. Problem 2. The graded moment is the multiplicity-versus-distinctness confusion; write the `["A", "A", "A", "B", "B", "B"]` test *before* you write the loop. Commit.
5. Problem 3. Reuse Exercise 3's window; change only the combine step. Commit.

### Friday — Problems 4, 5, 6 (3h)

6. Problem 4. Trace `["pass", "fail", "fail"]` with `q = 2` on paper before you code, so you feel the record-then-remove ordering. Commit.
7. Problem 5. New sub-shape. Read [Lecture 2 §3](../lecture-notes/02-the-shrinking-and-growing-mechanics.md) on shape C first, then write the monotonicity justification in your own words *before* implementing. Commit.
8. Problem 6. This is the hard one. Solve it from the pattern, not from your [Challenge 1](../challenges/challenge-01-shortest-kit-span.md) file — then diff the two solutions and confirm the only structural difference is the tie-break comparison. Commit.

### Saturday — Polish + memo audit (1.5h)

9. Read all six write-ups end to end. **Are the six 30-second memos consistent in shape?** They should be — same block, same cadence on read-aloud.
10. Read each memo aloud with a stopwatch. Each should land in 25–30 seconds. If any is over 40 seconds, tighten it.
11. Write the mini-project `README.md` index. Cross-link each problem to its corresponding drill or challenge, to the relevant lecture section, and to at least one other problem in this mini-project.
12. Send the repo link to one peer in the org. Ask: *"Read my six Research constraints memos out loud back to me. Do they all sound like the same person on the same week?"* If the answer is yes, you have shipped a coherent artifact. If no, you have inconsistency to clean.

---

## The mini-project README index

Suggested shape:

```markdown
# Week 3 — Sliding Window Mini-Project

Six sliding-window write-ups, each anchored by a 30-second pattern-recognition memo.

| # | Problem | Sub-shape | Auxiliary state |
|---|---------|-----------|-----------------|
| 1 | `problem-01-maintenance-window.md` | Fixed-size | Running sum |
| 2 | `problem-02-reprint-run.md` | Variable A (longest) | Frequency table |
| 3 | `problem-03-pallet-seal.md` | Fixed-size + frequency | Two frequency tables |
| 4 | `problem-04-recall-window.md` | Variable B (shortest) | One integer counter |
| 5 | `problem-05-tasting-flights.md` | Variable C (count) | Frequency table |
| 6 | `problem-06-rehearsal-block.md` | Variable B + frequency | Frequency tables + matched count |

## What this project demonstrates

- Research-constraints fluency: every problem's pattern is named in the first 30 seconds.
- Sub-shape discrimination: fixed vs variable; longest vs shortest vs count; sum vs frequency vs counter as state.
- Contract discipline: four different return types and three different "impossible" sentinels across six problems.
- Negative-space pattern rejection: at least one wrong pattern explicitly rejected per write-up.
```

That index, with your six links, is the second-most-important artifact of the week (after the six memos themselves).

---

## What "great" looks like (rubric)

| Criterion | Weight | "Great" looks like |
|-----------|------:|--------------------|
| Six 30-second memos consistent in shape | 35% | Same block at the top of every write-up; same cadence on read-aloud |
| Sub-shapes correctly named | 20% | Every memo correctly identifies fixed / variable A / B / C |
| Research constraints sections compare against alternatives | 15% | Each names at least one "why not X" rejection |
| Examine (cost) sections include the amortized-`O(n)` defence | 15% | Every variable-size write-up has the sentence from [Lecture 1 §6](../lecture-notes/01-the-sliding-window-pattern.md) |
| Cross-references present | 10% | Each problem links to a drill or challenge, a lecture section, and one other mini-project problem |
| Commits are meaningful | 5% | "Add mini-project problem 4" beats "update" |

---

## Why six, not five?

Five would cover the sub-shapes: fixed, A, B, C, and one frequency variant. The sixth is the **discriminator**, and it earns its place by being the only problem in the week whose contract *contradicts* one you have already solved. Carrying a pattern across a domain change is ordinary. Carrying it across a contract change, and noticing which line has to flip, is the thing being measured.

---

When you're done: push, send the link to one peer in the org for review, then move on to [Week 4 — Fast-and-Slow Pointers + Mock 1](../../week-04-fast-slow-pointers-and-mock-1/).
