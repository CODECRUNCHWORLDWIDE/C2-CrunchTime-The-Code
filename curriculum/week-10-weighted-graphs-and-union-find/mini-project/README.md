# Mini-Project — Dijkstra + DSU, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-10 patterns — heap-based Dijkstra on a single-source shortest-path problem and Union-Find on a cycle-detection problem — with full FRAME narration end-to-end. The pair is the discriminating element — Mock #2 grades the *shortest-path family* and the *components-and-merge family* separately, and shipping one of each forces you to articulate the structural difference out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## The Brief

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; Make the solution was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the algorithm choice (Dijkstra / Bellman-Ford / DSU / MST), defend the asymptotic improvement over the naive baseline, and reject one wrong alternative." This mini-project is the fifth in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair, W9 string pair, W10 graph-and-DSU pair).

2. **Dijkstra and DSU are the two structural shapes of every interview weighted-graph question.** Half of all FAANG weighted-graph problems are shortest-path variants (Dijkstra, Bellman-Ford, Floyd-Warshall); the other half are components / merge / equivalence variants (DSU, with MST as a derived application). The pair forces you to articulate the differences: when do you want the algorithm first (Dijkstra) versus the data structure first (DSU); when does prefix sharing buy you anything (it does not — that was W9); when does amortized near-constant `find` buy you the algorithm (Kruskal MST).

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Frame, Assess options, Examine, *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a weighted-graph or DSU problem in 20-25 minutes, recorded, without rehearsal.

---

## Starter

Two starters sit beside this page. They are the spec, not the deliverable —
implement against them in your portfolio repo, not in this one.

- [`problem-01-dijkstra-starter.py`](./problem-01-dijkstra-starter.py) — the
  three signatures, the harbour's runs, and a harness that names which cases
  still fail. Fill in the adjacency build, the heap search and the worst-served
  lookup.
- [`problem-02-dsu-starter.py`](./problem-02-dsu-starter.py) — the `Harbour`
  skeleton and the cable planner. Fill in `network_of`, `join` and
  `cheapest_cable`.

The worked answer on this page solves both. Read it after your attempt.

Before any code, fill in the memo below from the prompt alone.

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (heap-Dijkstra)

```markdown
> **30-second pattern-recognition memo (Dijkstra):**
> This is a shortest-path problem because [the prompt asks for the minimum
> time / distance / cost from a source / to all reachable nodes].
> Weights are [non-negative -> Dijkstra; otherwise -> Bellman-Ford].
> Sub-shape: [heap-Dijkstra with `heapq`; lazy-delete guard].
> Why not BFS: [weights are non-uniform; BFS only works on unweighted].
> Why not Bellman-Ford: [weights non-negative; Dijkstra is faster by log V].
```

### For Problem 2 (DSU)

```markdown
> **30-second pattern-recognition memo (DSU):**
> This is a DSU problem because [the prompt asks about merging / components
> / equivalence / cycle detection / redundant edges].
> Sub-shape: [components-count / cycle-detection / account-merge /
> streaming-islands].
> Optimizations: [path compression in find + union by rank in union ->
> amortized O(alpha(n))].
> Why not BFS/DFS: [streaming queries / amortized near-constant per
> operation / simpler for the "iterate edges and union" formulation].
> The trigger word: [merge / connect / equivalent / redundant / group].
```

Read each aloud; both should hit 25-30 seconds.

---

## Requirements

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-10/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-dijkstra-network-delay-time.md              ← heap-Dijkstra on
└── problem-02-dsu-redundant-connection.md                 ← DSU on
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (heap-Dijkstra):** the algorithm is the canonical heap-based single-source shortest-paths from, narrated as if you were demoing the algorithm choice. The discriminator is the lazy-delete guard — articulating "the `heapq` has no decrease-key; the `if d > dist[node]: continue` guard skips stale entries on pop" is the defense.

- **Problem 2 (DSU + redundant connection):** the algorithm is Union-Find on (the radiator loop check). The Research constraints move is recognizing that the "find the redundant edge" prompt is exactly the cycle-detection sub-shape of DSU; the defense is "the first edge whose `union(u, v)` returns False is the redundant one — that union would have closed a cycle."

The two problems together cover every Week-10 idiom: heap-priority-queue mechanics, lazy-delete, the "settle once" invariant, DSU class form, path compression, union by rank, cycle detection. After this pair, the recognition for any weighted-graph or DSU problem should reduce to: *shortest path or components?*

---

### FRAME structure for each write-up

The full five-section format, with Examine split into its verify and cost halves. The Research constraints section opens with the 30-second memo above.

### Frame

Restate the problem in your own words. Walk one example by hand. Note the constraints. Specifically address:

- For Problem 1 — restate the input format (`times`, `n`, `k`), the output (max distance or `-1`), and the reachability check that produces the `-1` return.
- For Problem 2 — restate the input format (a list of edges on `n` vertices with one redundant), the output (the redundant edge), and the spec detail that the *last* such edge in the input is the answer.

### Research constraints

Open with the 30-second memo. Then in 2-3 sentences:

- Name the pattern: heap-Dijkstra (Problem 1) or DSU cycle-detection (Problem 2).
- Name the sub-shape: lazy-delete with `heapq` (Problem 1) or path-compression-plus-union-by-rank UnionFind class (Problem 2).
- Reject the alternative: BFS or Bellman-Ford for Problem 1; BFS-based cycle-detection for Problem 2.

### Assess options

Numbered steps; 4-6 lines each. State the data structure first. State the loop / recursion structure second. State the termination condition third.

For Problem 1: build adjacency list; init `dist` and heap; relax loop with lazy-delete guard; return `max(dist.values())` or `-1`.

For Problem 2: build UnionFind on `n + 1`; iterate edges in order; return the first edge whose `union` returns False.

### Make the solution

The code. Type hints on every function. Docstrings on every public method. Comments only where the line is non-obvious — the lazy-delete guard deserves a comment; the `setdefault` form does not.

### Examine · verify

Trace the implementation by hand on at least two inputs:

- One positive example (the canonical "it works" case).
- One edge case (single-vertex graph for Problem 1; small graph with the redundant edge as the first edge for Problem 2).

For Problem 2, the second trace must include the moment of `union` returning False — otherwise the cycle-detection work is invisible.

### Examine · cost

Time and space bounds with derivation. The derivation is mandatory, not the bound alone.

- Problem 1: `O((V + E) log V)` derived from "`V` heap pops + `E` heap pushes, each `O(log V)`."
- Problem 2: `O(N alpha(N))` derived from "`N` edges, each triggering a constant number of `find` + `union` calls; each call is amortized `O(alpha(N))`."

Mention at least one variant in each Examine · cost section. For Problem 1: Bellman-Ford (when negative weights), Floyd-Warshall (all-pairs). For Problem 2: BFS-based cycle-detection (correct but `O(V + E)` per query; DSU is better for streaming).

---

### Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites the Problem 2 write-up in the Examine · cost section: "Compare to the DSU write-up — both algorithms are near-linear in the input size, but Dijkstra *processes* a graph (relaxes edges until convergence), whereas DSU *maintains* a graph (answers `find` / `union` queries online). The algorithmic registers are complementary, not interchangeable."
- The Problem 2 write-up cites the Problem 1 write-up in the Research constraints section: "Unlike the Dijkstra problem, this is a structural / topological question about the graph — there are no edge weights and no source vertex. The right tool is a data structure (DSU), not an algorithm (Dijkstra)."

The cross-references are a small detail but they earn senior signal — they show you can navigate the *taxonomy* of graph algorithms, not just the individual templates.

---

### Rubric

Each write-up is graded on the 30-second memo plus the five FRAME sections, with Examine split into verify and cost. Total possible: 100 points; passing: 70.

### Problem 1 (heap-Dijkstra) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the non-negative-weights discriminator is stated |
| Frame | 10 | Two examples walked; the reachability check producing the `-1` return is stated |
| Research constraints | 20 | Dijkstra pattern named; heap-based form justified; BFS and Bellman-Ford rejected with reasons |
| Assess options | 10 | Steps numbered; data structure choice (`heapq` + `defaultdict`) stated; lazy-delete guard explained |
| Make the solution | 25 | All test cases pass; type hints on every function; PEP 8; idiomatic Python |
| Examine · verify | 10 | One positive trace + one edge case; both walked |
| Examine · cost | 15 | `O((V + E) log V)` derived; trade vs Bellman-Ford and Floyd-Warshall stated; one variant mentioned |

### Problem 2 (DSU) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the optimizations (path compression + union by rank) are named |
| Frame | 10 | Two examples walked; the spec detail (last redundant edge in input) is addressed |
| Research constraints | 20 | DSU pattern named; cycle-detection sub-shape identified; BFS-based alternative rejected |
| Assess options | 10 | UnionFind class outlined; iteration over edges; the `union` return value as the signal |
| Make the solution | 25 | All test cases pass; path compression and union by rank implemented correctly; type hints |
| Examine · verify | 15 | One positive trace + one trace where the redundant edge is detected on the first cycle-closing union |
| Examine · cost | 10 | `O(N alpha(N))` derived; the `alpha(N) <= 4` defense; BFS variant named |

### Cross-reference rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| Problem 1 cites Problem 2 in Examine · cost | 5 | Sentence comparing Dijkstra's processing register to DSU's maintenance register |
| Problem 2 cites Problem 1 in Research constraints | 5 | Sentence rejecting Dijkstra ("no edge weights, no source; the right tool is a data structure") |

Sum: 100 (Problem 1) + 100 (Problem 2) + 10 (cross-refs) = 210 / 2 = **105 average**.

A passing write-up scores at least 70 on each.

---

## Constraints

- **No run takes negative minutes.** That is what makes a settled quay
  final, and therefore what makes the heap legitimate. Say it out loud; with a
  negative run the whole approach is wrong rather than slow.
- **An unreachable quay is absent from the timings, not infinite.** A sentinel
  number invites arithmetic on it. Gull Rock is in the harbour and in no run.
- **`cheapest_cable` reports the networks left over**, not just the cost. A plan
  that quietly leaves a quay dark and returns a tidy number is the failure this
  contract exists to prevent.
- **Union-find answers membership, never the path.** If your write-up reaches
  for a traversal to decide "already joined?", say why the traversal is the
  wrong tool here.
- **Both optimisations**, compression and rank, and a sentence on what each buys.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README.py
HARBOUR UTILITIES PLAN - taxi from Ferry Slip

1. Water-taxi minutes
      0  Ferry Slip
      4  Bait Wharf
      7  Chandlery Steps
     12  Dry Dock
     18  Eel Stage
     21  Fish Quay

2. Worst wait and who is cut off
   longest wait: Fish Quay at 21 minutes
   no taxi run:  Gull Rock

3. Cheapest cable ring
      4k  Bait Wharf - Chandlery Steps
      5k  Eel Stage - Fish Quay
      6k  Chandlery Steps - Dry Dock
      7k  Ferry Slip - Bait Wharf
      8k  Dry Dock - Eel Stage
     15k  Fish Quay - Gull Rock
   total 45k over 6 trenches

4. Does the cable reach everybody?
   yes - one network

5. Data check
   refused: a run cannot take negative minutes: Gull Rock to Ferry Slip

FIRST DRAFT, island left off the cable plan
   no - 2 separate networks:
     Bait Wharf, Chandlery Steps, Dry Dock, Eel Stage, Ferry Slip, Fish Quay
     Gull Rock

5. Data check
   refused: a run cannot take negative minutes: Gull Rock to Ferry Slip
All checks passed.
```

Part 5 is the one to read twice. The planner refuses data rather than working
around it: a run of negative minutes is not a hard case to handle, it is a
harbour board that has mistyped a timetable, and the honest response is to say so.

## Steps

1. Read both harnesses. They are the spec, and anything they assert is a
   requirement whether or not the prose repeats it.
2. Fill in the memo for problem 1, then implement the adjacency build. Check
   Gull Rock — a quay with no runs must be safe to look up.
3. Implement the heap search. Watch Chandlery Steps come out at 7 and not 9:
   two legs beat the single direct run, which is the whole point of the search.
4. Fill in the memo for problem 2, then implement `Harbour`. Test the self-join
   early.
5. Implement `cheapest_cable`. Return the left-over network count from the
   start; adding it afterwards means threading it through everything twice.
6. Write both FRAME passes, then the report that puts the two answers side by
   side.

## The Solution

```python
"""harbour-planner-solution.py — the harbour utilities planner.

One report for a harbour board, built from two different questions about the
same set of quays.

  The taxi question is "how long from here to there?", and it is answered by
  growing outwards from the ferry slip, always finishing the nearest unfinished
  quay next. That is a shortest-path search with a heap and a settled set.

  The cable question is "what is the cheapest set of trenches that leaves
  nobody out?", and it is answered by walking the priced trenches from
  cheapest to dearest and keeping any trench that joins two quays not already
  joined. That is a minimum spanning tree, and the "already joined?" test is
  a union-find.

The report is printed to stdout in five parts. Nothing is read from the
keyboard, nothing is written to disk, and the whole thing runs on the
standard library.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
Run = tuple[str, str, int]      # (quay, quay, minutes for the water taxi)
Trench = tuple[str, str, int]   # (quay, quay, cost in thousands of pounds)

QUAYS: list[str] = [
    "Ferry Slip",
    "Bait Wharf",
    "Chandlery Steps",
    "Dry Dock",
    "Eel Stage",
    "Fish Quay",
    "Gull Rock",
]

TAXI_RUNS: list[Run] = [
    ("Ferry Slip", "Bait Wharf", 4),
    ("Ferry Slip", "Chandlery Steps", 9),
    ("Bait Wharf", "Chandlery Steps", 3),
    ("Bait Wharf", "Dry Dock", 11),
    ("Chandlery Steps", "Dry Dock", 5),
    ("Dry Dock", "Eel Stage", 6),
    ("Chandlery Steps", "Fish Quay", 14),
    ("Eel Stage", "Fish Quay", 4),
]

CABLE_TRENCHES: list[Trench] = [
    ("Ferry Slip", "Bait Wharf", 7),
    ("Ferry Slip", "Chandlery Steps", 12),
    ("Bait Wharf", "Chandlery Steps", 4),
    ("Bait Wharf", "Dry Dock", 9),
    ("Chandlery Steps", "Dry Dock", 6),
    ("Dry Dock", "Eel Stage", 8),
    ("Eel Stage", "Fish Quay", 5),
    ("Chandlery Steps", "Fish Quay", 11),
    ("Fish Quay", "Gull Rock", 15),
]

# The board's first draft left the island off the cable plan entirely.
FIRST_DRAFT: list[Trench] = [t for t in CABLE_TRENCHES if "Gull Rock" not in t[:2]]


# ---- Part one: the water taxi ----
def build_water(runs: list[Run]) -> dict[str, list[tuple[str, int]]]:
    """Return the taxi runs keyed by quay, both ways round.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).

    Returns:
        A dict where water[quay] is a list of (other quay, minutes).

    Raises:
        ValueError: If any run takes negative minutes. A negative run would
            break the settled-set rule this planner depends on, so it is
            refused at the door rather than producing a quiet wrong answer.
    """
    water: dict[str, list[tuple[str, int]]] = {}
    for here, there, minutes in runs:
        if minutes < 0:
            raise ValueError(f"a run cannot take negative minutes: {here} to {there}")
        water.setdefault(here, []).append((there, minutes))
        water.setdefault(there, []).append((here, minutes))
    return water


def run_minutes(runs: list[Run], start: str) -> dict[str, int]:
    """Return the shortest taxi time from start to every quay it can reach.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        start: The quay the taxi waits at.

    Returns:
        A dict of quay -> minutes. A quay no run reaches is left out.
    """
    water = build_water(runs)
    best: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]

    while queue:
        so_far, quay = heapq.heappop(queue)
        if quay in settled:
            continue
        settled.add(quay)
        for other, minutes in water.get(quay, []):
            total = so_far + minutes
            if total < best.get(other, float("inf")):
                best[other] = total
                heapq.heappush(queue, (total, other))

    return best


def longest_wait(runs: list[Run], quays: list[str], start: str) -> tuple[str, int]:
    """Return the reachable quay that waits longest for a taxi.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        quays: Every quay on the harbour board's list.
        start: The quay the taxi waits at.

    Returns:
        (quay, minutes), ties broken by quay name A to Z. Quays the taxi
        cannot reach are ignored here and reported separately.
    """
    minutes = run_minutes(runs, start)
    reachable = [quay for quay in quays if quay in minutes]
    latest, name = min((-minutes[quay], quay) for quay in reachable)
    return name, -latest


def stranded(runs: list[Run], quays: list[str], start: str) -> list[str]:
    """Return the quays no taxi run reaches, in name order.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        quays: Every quay on the harbour board's list.
        start: The quay the taxi waits at.

    Returns:
        A sorted list of quay names, empty when the taxi reaches everything.
    """
    minutes = run_minutes(runs, start)
    return sorted(quay for quay in quays if quay not in minutes)


# ---- Part two: the cable ring ----
class Harbour:
    """Quays grouped into cabled networks, with path compression and rank."""

    def __init__(self, quays: list[str]) -> None:
        """Start every quay in a network of its own.

        Args:
            quays: Every quay on the harbour board's list.
        """
        self.parent: dict[str, str] = {quay: quay for quay in quays}
        self.rank: dict[str, int] = {quay: 0 for quay in quays}
        self.networks: int = len(quays)

    def network_of(self, quay: str) -> str:
        """Return the quay that names this quay's network.

        Args:
            quay: The quay to look up.

        Returns:
            The root quay, flattening the path on the way back.
        """
        root = quay
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[quay] != root:
            self.parent[quay], quay = root, self.parent[quay]
        return root

    def join(self, left: str, right: str) -> bool:
        """Cable two networks together, shallower tree under deeper.

        Args:
            left: One quay.
            right: The other quay.

        Returns:
            True when the trench joined two networks that were apart. False
            when both quays were already cabled together.
        """
        left_root, right_root = self.network_of(left), self.network_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.networks -= 1
        return True


def cheapest_cable(
    quays: list[str], trenches: list[Trench]
) -> tuple[int, list[Trench], int]:
    """Return the cheapest set of trenches that cables every quay together.

    Args:
        quays: Every quay on the harbour board's list.
        trenches: Every trench the surveyor priced.

    Returns:
        (total cost, trenches in the order accepted, networks left over).
        The third number is 1 when the plan reaches every quay and more when
        it does not, so the caller can report the shortfall rather than being
        handed a plan that quietly leaves somebody dark.
    """
    harbour = Harbour(quays)
    chosen: list[Trench] = []
    total = 0
    for left, right, cost in sorted(trenches, key=lambda t: (t[2], t[0], t[1])):
        if harbour.join(left, right):
            chosen.append((left, right, cost))
            total += cost
            if len(chosen) == len(quays) - 1:
                break
    return total, chosen, harbour.networks


def dark_networks(quays: list[str], trenches: list[Trench]) -> list[list[str]]:
    """Return the separate networks a trench plan leaves behind.

    Args:
        quays: Every quay on the harbour board's list.
        trenches: Every trench the surveyor priced.

    Returns:
        A list of networks, each a sorted list of quay names, ordered by each
        network's first name.
    """
    harbour = Harbour(quays)
    for left, right, _ in trenches:
        harbour.join(left, right)
    grouped: dict[str, list[str]] = {}
    for quay in quays:
        grouped.setdefault(harbour.network_of(quay), []).append(quay)
    return sorted(sorted(group) for group in grouped.values())


# ---- Part three: the report ----
def report(quays: list[str], runs: list[Run], trenches: list[Trench], start: str) -> list[str]:
    """Return the harbour board's report, one line per list entry.

    Args:
        quays: Every quay on the harbour board's list.
        runs: Every water-taxi run, as (quay, quay, minutes).
        trenches: Every trench the surveyor priced.
        start: The quay the taxi waits at.

    Returns:
        The finished report as a list of lines, with no trailing blank line.
    """
    lines = [f"HARBOUR UTILITIES PLAN - taxi from {start}", ""]

    lines.append("1. Water-taxi minutes")
    minutes = run_minutes(runs, start)
    for wait, quay in sorted((m, q) for q, m in minutes.items()):
        lines.append(f"   {wait:4d}  {quay}")

    lines.append("")
    lines.append("2. Worst wait and who is cut off")
    quay, wait = longest_wait(runs, quays, start)
    lines.append(f"   longest wait: {quay} at {wait} minutes")
    cut_off = stranded(runs, quays, start)
    lines.append(f"   no taxi run:  {', '.join(cut_off) if cut_off else 'nobody'}")

    lines.append("")
    lines.append("3. Cheapest cable ring")
    total, chosen, networks = cheapest_cable(quays, trenches)
    for left, right, cost in chosen:
        lines.append(f"   {cost:4d}k  {left} - {right}")
    lines.append(f"   total {total}k over {len(chosen)} trenches")

    lines.append("")
    lines.append("4. Does the cable reach everybody?")
    if networks == 1:
        lines.append("   yes - one network")
    else:
        lines.append(f"   no - {networks} separate networks:")
        for group in dark_networks(quays, trenches):
            lines.append(f"     {', '.join(group)}")

    lines.append("")
    lines.append("5. Data check")
    try:
        run_minutes([*runs, ("Gull Rock", "Ferry Slip", -3)], start)
    except ValueError as problem:
        lines.append(f"   refused: {problem}")
    else:                                    # pragma: no cover - the guard must fire
        lines.append("   a negative run slipped through, which is a bug")
    return lines


# ---- Self-check ----
if __name__ == "__main__":
    for line in report(QUAYS, TAXI_RUNS, CABLE_TRENCHES, "Ferry Slip"):
        print(line)
    print()
    print("FIRST DRAFT, island left off the cable plan")
    for line in report(QUAYS, TAXI_RUNS, FIRST_DRAFT, "Ferry Slip")[-6:]:
        print(line)

    minutes = run_minutes(TAXI_RUNS, "Ferry Slip")
    assert minutes["Chandlery Steps"] == 7      # 4 + 3 beats the direct 9
    assert minutes["Dry Dock"] == 12            # 7 + 5 beats 4 + 11
    assert minutes["Fish Quay"] == 21           # 7 + 14 beats 12 + 6 + 4
    assert "Gull Rock" not in minutes
    assert longest_wait(TAXI_RUNS, QUAYS, "Ferry Slip") == ("Fish Quay", 21)
    assert stranded(TAXI_RUNS, QUAYS, "Ferry Slip") == ["Gull Rock"]

    total, chosen, networks = cheapest_cable(QUAYS, CABLE_TRENCHES)
    assert total == 45
    assert networks == 1
    assert len(chosen) == len(QUAYS) - 1
    assert chosen[0] == ("Bait Wharf", "Chandlery Steps", 4)
    assert chosen[-1] == ("Fish Quay", "Gull Rock", 15)

    draft_total, draft_chosen, draft_networks = cheapest_cable(QUAYS, FIRST_DRAFT)
    assert draft_networks == 2
    assert draft_total == 30
    assert dark_networks(QUAYS, FIRST_DRAFT)[-1] == ["Gull Rock"]

    try:
        run_minutes([("Ferry Slip", "Bait Wharf", -1)], "Ferry Slip")
    except ValueError as problem:
        assert "negative" in str(problem)
    else:                                    # pragma: no cover - the guard must fire
        raise AssertionError("a negative run should have been refused")
    print("All checks passed.")
```

One file, two questions, one report. `network_of` compresses on the way back up
rather than in a second pass — the shortest correct path compression, and the
most commonly mangled one.

## Run it

Download the solution beside this page and run it:

```bash
python README.py
```

No third-party packages, no arguments, no input. It prints the five-part harbour
report and then `All checks passed.`

Both starters run the same way and report which cases are still failing, so you
can work against them without reading the answer.

## Common bugs to catch

- **Settling a quay twice.** Symptom: correct answers, far too much work, and
  a heap that grows. Skip a popped quay that is already settled rather than
  trying to delete from the heap.
- **A sentinel for unreachable.** Symptom: Gull Rock reported at some enormous
  number of minutes, which then gets summed into a total. Leave it out.
- **Recursion in `network_of`.** Symptom: fine on five quays, `RecursionError`
  on a long chain.
- **Skipping the rank and keeping only compression.** Symptom: correct, slower,
  and a write-up that cannot say what the rank was for.
- **Kruskal without the "already joined?" test.** Symptom: a cycle in the plan
  and a bill higher than it needs to be. The redundant 6k trench is in the data
  precisely to catch this.
- **Reporting a total without the left-over count.** Symptom: a plan that looks
  complete and leaves Gull Rock dark.

## Acceptance checklist

The mini-project is complete when:

- Both write-ups are committed under `frame-writeups/c2-week-10/mini-project/`.
- Both have the 30-second memo at the top.
- The cross-references in both directions are present.
- Both have recordings of at least 10 minutes each.
- The implementations pass the test cases in the starters.

Push everything by Sunday end-of-day. Phase 2's sixth week is closed on the push.

---

## Stretch

- Add a trench to Gull Rock and watch the left-over count fall to 1. Predict
  the new total before you run it.
- Make one run take zero minutes and check the heap search still terminates.
  Zero-weight edges are legal and are a common source of heap bugs.
- Answer "which single trench, if it failed, would leave the most quays dark?"
  Your current structures nearly answer it; say what you would add and what it
  costs on every join.

## Self-reflection (in the mini-project README)

End the README.md for `frame-writeups/c2-week-10/mini-project/README.md` with a short reflection — 4-6 sentences — addressing:

1. Which template (Dijkstra or DSU) felt more natural? Why?
2. What was the hardest part of the lazy-delete guard or path compression to articulate aloud?
3. What is the one thing you want to drill before Mock #2?

The reflection is the portfolio-grade artifact. Future you will thank present you for writing it.

---

## After the mini-project

Move on to [Week 11 — Dynamic Programming I](../../week-11-dynamic-programming-i/). The Dijkstra and DSU intuition stay with you through the rest of Phase 2; you will use them again in the W12 retrospective and (for the systems-team interviews) in Mock #3.
