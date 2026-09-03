# Problem 1 — Hose Clusters

> **Topic:** connected components, counted with a recursive depth-first walk and a visited set — from an edge list this time, not a grid
> **Lecture:** [01 — Recursive DFS](../lecture-notes/01-recursive-dfs.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** [Exercise 1 — Repeater Clusters](../exercises/exercise-01-repeater-clusters.md) hands you the graph as a matrix. This one hands you the same kind of graph as a list of pairs. The algorithm does not change one line. Being able to say that out loud — *same walk, different way of being handed the map* — is the thing an interviewer is listening for, because it means you recognised the pattern rather than the packaging. The messy log is the second half of the lesson: real inputs repeat themselves and contradict themselves, and a good answer shrugs.

## The Brief

A greenhouse waters its plants through a bench of **valves**. The valves are
numbered, starting at zero: valve 0, valve 1, valve 2, and so on up to one less
than however many there are.

Some valves are joined to each other by a **hose**. A hose is a two-way pipe. If
water reaches valve 3, and valve 3 has a hose to valve 4, then water reaches
valve 4 as well.

Follow that idea far enough and the bench falls apart into separate groups. Pick
any valve, follow every hose out of it, then every hose out of *those* valves,
and keep going until there is nothing new to reach. Everything you touched is one
**cluster** — one watering circuit. Nothing outside it can ever get wet from
inside it.

Two questions:

- **How many clusters are there?**
- **How big is the biggest one?**

A valve with no hose at all still counts. It is a cluster of one — a circuit that
waters exactly itself.

### The log is messy, and it is messy on purpose

You are not handed a tidy diagram. You are handed the maintenance log: a list of
pairs, one line per hose someone fitted. Real logs have two habits.

**The same hose gets written down twice.** Somebody fits hose 3-4, somebody else
checks it a week later and writes it down again. There is still one hose.

**A hose sometimes runs from a valve back to itself.** That is not a mistake —
a technician loops a short hose from a valve to its own drain to bleed air out
of the line. It joins valve 6 to valve 6, which tells you nothing new about who
is connected to whom.

Neither of those may change your answer. The tempting shortcut *does* change on
both of them, and that shortcut is the trap this page is built around: it is very
easy to reason "every hose glues two groups together, so the number of clusters
is the number of valves minus the number of hoses." On a clean log that is right.
On this log it is wrong by two.

### Why an edge list at all

You have already counted clusters in
[Exercise 1](../exercises/exercise-01-repeater-clusters.md), where the graph
arrived as a grid: a square table with a mark in row `i`, column `j` when `i` and
`j` are joined. That is an **adjacency matrix**.

Here the same graph arrives as a list of pairs. That is an **edge list**, and it
is what a database table or a CSV export actually looks like. The first thing you
do is turn the edge list into an **adjacency list** — for each valve, the valves
it is joined to — and from that point onward the code is identical to Exercise
1's. Same walk. Same visited set. Same counting loop. Only the first ten lines
differ.

## Starter

Create `problem-01-hose-clusters.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""problem-01-hose-clusters.py -- counting a greenhouse's irrigation clusters.

Turn the maintenance log into an adjacency list, walk it depth-first, and count
the clusters.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

# ---- Given data ----
VALVE_COUNT = 9

# (valve, valve) pairs, straight off the clipboard. Hose (3, 4) was written down
# twice, and valve 6 has a hose looped back to itself so the line can be bled.
MAINTENANCE_LOG: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (3, 4),
    (4, 5),
    (3, 4),
    (6, 6),
    (7, 8),
]


# ---- Your task ----
def survey_hoses(valve_count: int, hoses: list[tuple[int, int]]) -> tuple[int, int]:
    """Count the watering clusters and measure the biggest one.

    Args:
        valve_count: How many valves the bench has. They are numbered
            0 to valve_count - 1.
        hoses: The maintenance log. Each pair joins two valves. A repeated pair
            and a valve-to-itself pair are both allowed, and neither changes
            the answer.

    Returns:
        (cluster_count, largest_cluster_size). A valve joined to nothing is a
        cluster of one. A bench with no valves gives (0, 0).

    Raises:
        ValueError: A hose names a valve outside 0..valve_count - 1.
    """
    # TODO 1: build an adjacency list -- one list of neighbours per valve.
    # TODO 2: while building it, reject any valve number that is not on the
    #         bench. Name the offending number in the message.
    # TODO 3: walk from every valve you have not seen yet. Each fresh walk is
    #         one more cluster; the walk returns how many valves it touched.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    clusters, largest = survey_hoses(VALVE_COUNT, MAINTENANCE_LOG)
    print(f"bench: {VALVE_COUNT} valves, {len(MAINTENANCE_LOG)} hoses logged")
    print(f"  clusters        : {clusters}")
    print(f"  largest cluster : {largest}")

    assert (clusters, largest) == (4, 3)
    assert survey_hoses(0, []) == (0, 0)
    assert survey_hoses(1, []) == (1, 1)
    assert survey_hoses(4, []) == (4, 1)
    assert survey_hoses(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == (1, 5)
    assert survey_hoses(3, [(0, 1), (0, 1), (0, 1)]) == (2, 2)
    assert survey_hoses(3, [(1, 1)]) == (3, 1)

    try:
        survey_hoses(4, [(0, 9)])
    except ValueError as err:
        assert "9" in str(err)
    else:
        raise AssertionError("a valve outside the bench should raise ValueError")

    print("All checks passed.")
```

Three words you need before you start.

**Edge list.** A list of pairs, each pair naming two things that are joined.
`(3, 4)` means valve 3 and valve 4 are on the same hose. It says nothing about
valve 5.

**Adjacency list.** For each valve, the list of valves it is joined to. You build
it from the edge list by walking the pairs once and writing each pair down twice
— once under each end — because a hose is two-way.

**Visited set.** A `set` holding every valve you have already walked into. It is
the whole reason a cycle in the plumbing does not send you round forever, and —
on this page — it is also the reason a repeated hose and a self-loop cost you
nothing.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/homework/problem-01-hose-clusters.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `survey_hoses(valve_count, hoses)` returns a tuple
   `(cluster_count, largest_cluster_size)`.
2. A valve with no hose is its own cluster of size 1.
3. `survey_hoses(0, [])` returns `(0, 0)`.
4. A repeated pair in the log does not change either number.
   `survey_hoses(3, [(0, 1), (0, 1), (0, 1)])` is `(2, 2)`.
5. A pair joining a valve to itself does not change either number.
   `survey_hoses(3, [(1, 1)])` is `(3, 1)`.
6. A pair naming a valve outside `0..valve_count - 1` raises `ValueError`, and
   the message contains the offending number.
7. The function does not modify `hoses`.
8. Type hints and a docstring on every function you write, including the inner
   walk.

## Constraints

- **`0 <= valve_count <= 900`.** That number is chosen, not inherited. The
  longest possible chain on a 900-valve bench is 900 valves end to end, so the
  recursive walk goes at most 900 frames deep. CPython's default limit is 1,000
  frames — check it yourself with `sys.getrecursionlimit()` — so 900 leaves
  headroom for the handful of frames the module and the outer function already
  occupy. In other words: on this page the recursion is safe *because the bound
  was picked to make it safe*, and that is the honest reason. Raise the bound and
  the recursive version stops working;
  [Exercise 2 — Conveyor Reachability](../exercises/exercise-02-conveyor-reachability.md)
  is where that happens and where the iterative fix lives.

- **The log may hold up to 5,000 pairs**, which is more than enough to repeat
  every hose several times over. The bound exists so you cannot get away with
  "the log is small, I will just check each new pair against the ones I already
  read." That check is a scan inside a loop, and at 5,000 pairs it is 12.5
  million comparisons for a job the visited set does for free.

- **Do not deduplicate the log.** It is tempting to build a `set` of pairs first.
  It is not wrong, and it costs nothing here — but it is not the reason your
  answer is right, and reaching for it suggests you think duplicates are
  dangerous. They are not, once the visited set is in place. Say that out loud
  instead of coding around it.

- **The visited set is a `set`, never a `list`.** Asking `valve in seen` costs one
  step on a set and one step *per valve already seen* on a list. On a 900-valve
  bench that is the difference between 900 checks and roughly 400,000.

- **`hoses` is read, never written.** Building the adjacency list creates new
  lists; it does not sort, reverse or extend the caller's log.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-hose-clusters-solution.py
bench: 9 valves, 7 hoses logged
  clusters        : 4
  largest cluster : 3
the log is messy on purpose
  hose (3, 4) is written down twice
  hose (6, 6) loops valve 6 back to itself
  valves minus logged hoses would say 2 clusters, which is wrong
a 900-valve chain, the longest run the constraints allow
  clusters        : 1
  largest cluster : 900
All checks passed.
```

Read the fourth-from-last group again. Nine valves minus seven logged hoses is
two, and two is wrong — the answer is four. The shortcut fails by exactly the
number of lines the log wasted: one repeat and one self-loop. That is not bad
luck. It is what happens when you count *lines in a file* and call it *structure
in a graph*.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python problem-01-hose-clusters.py`. You get a `TypeError` on the line that
   unpacks the result, because the function still returns `...`. That is the
   correct starting point — it proves the self-check is real.
2. Build the adjacency list first, and print it. Nine valves means nine lists.
   Look at `joined[6]` and notice it holds `[6, 6]`; look at `joined[3]` and
   notice it holds `[4, 4]`. Both are harmless. Convince yourself of that before
   you write the walk.
3. Put the bounds check *inside* the same loop, before the two appends. Checking
   afterwards means you have already indexed with a bad number and got an
   `IndexError` instead of your own message.
4. Write the recursive walk. Three lines of body: mark this valve seen, start a
   size of one, and for each neighbour you have not seen, add on whatever that
   neighbour's walk returns.
5. Write the outer loop. For every valve from `0` upward, if you have not seen
   it, that is a new cluster — count it, walk it, and keep the biggest size you
   have seen.
6. Run the self-checks. When they pass, delete your bounds check on purpose and
   run again, so you have seen the `IndexError` it was protecting you from. Put
   it back.
7. Last, try `survey_hoses(4000, [(i, i + 1) for i in range(3999)])` in a REPL
   and read the `RecursionError`. That is the wall the `900` bound is standing in
   front of. Then go and read
   [Exercise 2](../exercises/exercise-02-conveyor-reachability.md), which climbs
   over it.

## The Solution

```python
"""problem-01-hose-clusters-solution.py -- counting a greenhouse's irrigation clusters.

Valves are numbered 0..valve_count-1 and hoses join pairs of them. Water that
reaches one valve in a group reaches every valve in that group, so "how many
separate watering circuits are there, and how big is the biggest one" is the
connected-components question -- asked from an edge list rather than a grid.

The maintenance log is a real log. The same hose can be written down twice, and
a hose can run from a valve back to itself. Neither changes the answer, because
the visited set absorbs both.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

# ---- Given data ----
VALVE_COUNT = 9

# (valve, valve) pairs, straight off the clipboard. Hose (3, 4) was written down
# twice, and valve 6 has a hose looped back to itself so the line can be bled.
MAINTENANCE_LOG: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (3, 4),
    (4, 5),
    (3, 4),
    (6, 6),
    (7, 8),
]


def survey_hoses(valve_count: int, hoses: list[tuple[int, int]]) -> tuple[int, int]:
    """Count the watering clusters and measure the biggest one.

    Args:
        valve_count: How many valves the bench has. They are numbered
            0 to valve_count - 1.
        hoses: The maintenance log. Each pair joins two valves. A repeated pair
            and a valve-to-itself pair are both allowed, and neither changes
            the answer.

    Returns:
        (cluster_count, largest_cluster_size). A valve joined to nothing is a
        cluster of one. A bench with no valves gives (0, 0).

    Raises:
        ValueError: A hose names a valve outside 0..valve_count - 1.
    """
    joined: list[list[int]] = [[] for _ in range(valve_count)]
    for left, right in hoses:
        for valve in (left, right):
            if not 0 <= valve < valve_count:
                raise ValueError(
                    f"hose names valve {valve}, which is outside 0..{valve_count - 1}"
                )
        joined[left].append(right)
        joined[right].append(left)

    seen: set[int] = set()

    def walk(valve: int) -> int:
        """Mark every valve reachable from this one, and count them."""
        seen.add(valve)
        size = 1
        for neighbour in joined[valve]:
            if neighbour not in seen:
                size += walk(neighbour)
        return size

    cluster_count = 0
    largest = 0
    for valve in range(valve_count):
        if valve not in seen:
            cluster_count += 1
            largest = max(largest, walk(valve))
    return (cluster_count, largest)


# ---- Self-check ----
if __name__ == "__main__":
    clusters, largest = survey_hoses(VALVE_COUNT, MAINTENANCE_LOG)
    print(f"bench: {VALVE_COUNT} valves, {len(MAINTENANCE_LOG)} hoses logged")
    print(f"  clusters        : {clusters}")
    print(f"  largest cluster : {largest}")

    print("the log is messy on purpose")
    print("  hose (3, 4) is written down twice")
    print("  hose (6, 6) loops valve 6 back to itself")
    print(
        f"  valves minus logged hoses would say "
        f"{VALVE_COUNT - len(MAINTENANCE_LOG)} clusters, which is wrong"
    )

    chain = [(step, step + 1) for step in range(899)]
    deep = survey_hoses(900, chain)
    print("a 900-valve chain, the longest run the constraints allow")
    print(f"  clusters        : {deep[0]}")
    print(f"  largest cluster : {deep[1]}")

    assert survey_hoses(VALVE_COUNT, MAINTENANCE_LOG) == (4, 3)
    assert survey_hoses(0, []) == (0, 0)
    assert survey_hoses(1, []) == (1, 1)
    assert survey_hoses(4, []) == (4, 1)
    assert survey_hoses(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == (1, 5)
    assert survey_hoses(3, [(0, 1), (0, 1), (0, 1)]) == (2, 2)
    assert survey_hoses(3, [(1, 1)]) == (3, 1)
    assert survey_hoses(2, [(1, 0)]) == (1, 2)
    assert deep == (1, 900)

    try:
        survey_hoses(4, [(0, 9)])
    except ValueError as err:
        assert "9" in str(err)
    else:
        raise AssertionError("a valve outside the bench should raise ValueError")

    print("All checks passed.")
```

**The edge list becomes an adjacency list, and then this is Exercise 1 again.**
Everything specific to this page happens in seven lines:

```python
joined: list[list[int]] = [[] for _ in range(valve_count)]
for left, right in hoses:
    ...
    joined[left].append(right)
    joined[right].append(left)
```

Both appends, every time. A hose is two-way, so it has to appear under both
ends. Forget one and half your hoses become one-way, which does not fail loudly —
it just quietly reports too many clusters when the walk happens to start at the
wrong end.

**The visited set is what makes the messy log a non-event.** Look at what the
repeat and the self-loop actually do. `(3, 4)` twice puts `4` into `joined[3]`
twice, so the walk considers valve 4 from valve 3 twice — and the second time,
`4 in seen` is already true, so nothing happens. `(6, 6)` puts `6` into
`joined[6]` twice, and by the time the walk looks at those neighbours, valve 6 is
the valve it is standing on, so it is already in `seen`. Both cases collapse into
the same one-line guard that was there anyway. **There is no special case for
either, and adding one would be the tell that you had not understood why.**

**The counting loop is where the answer comes from.** Every valve gets its turn.
If it is already in `seen`, some earlier walk reached it, so it belongs to a
cluster already counted. If it is not, nothing has reached it, so it starts a new
cluster — count one, walk it, and the walk's return value is that cluster's size.

**`max(largest, walk(valve))` rather than a list of sizes.** You only ever need
the biggest, so hold the biggest. Collecting all the sizes into a list and calling
`max` at the end gives the same answer and keeps `V` numbers alive to do it.

**Why `(0, 0)` needs no special case.** `range(0)` yields nothing, the loop body
never runs, and the two counters are still at their starting values of `0` and
`0`. The empty case falls out of the ordinary code. When a degenerate case can be
made to fall out rather than be tested for, take it — an untested branch is a
branch that eventually rots.

**`O(V + E)` — one look at every valve and one look at every hose, and then it is
done.** Building the adjacency list touches each of the `E` logged pairs once.
The walk enters each of the `V` valves once, because the visited set guarantees
it, and from each valve reads that valve's neighbour list. Every hose appears in
exactly two neighbour lists, so across the whole run each hose is read twice.
Space is `O(V + E)` too: `V` neighbour lists holding `2E` entries between them,
plus a visited set of at most `V`, plus a recursion stack at most as deep as the
longest chain.

## Download and run

Download
[problem-01-hose-clusters-solution.py](./problem-01-hose-clusters-solution.py)
and run it:

```bash
python problem-01-hose-clusters-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-01-hose-clusters.py`.

## Common bugs to catch

- **`IndexError: list index out of range`.** You built the adjacency list before
  checking the valve numbers:

  ```text
  Traceback (most recent call last):
      survey_hoses(4, [(0, 9)])
      ~~~~~~~~~~~~^^^^^^^^^^^^^
      joined[right].append(left)
      ~~~~~~^^^^^^^
  IndexError: list index out of range
  ```

  Python is telling you the truth, just not usefully: a caller who mistypes a
  valve number learns that some list somewhere was too short. Your own
  `ValueError` names the number, which is the difference between a two-minute fix
  and a twenty-minute one. Check *before* you index, in the same loop.

- **`RecursionError: maximum recursion depth exceeded`.** You ran the recursive
  walk on a bench far longer than the constraints allow — a 4,000-valve chain:

  ```text
  Traceback (most recent call last):
      largest = max(largest, walk(valve))
                             ~~~~^^^^^^^
      size += walk(neighbour)
              ~~~~^^^^^^^^^^^
      size += walk(neighbour)
              ~~~~^^^^^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Note `995`, not `4000`. Python gave up at the limit, roughly a thousand frames
  in. This is not a bug in your code — the code is right, and the input is
  outside the bound this page declared. The fix is not `sys.setrecursionlimit`;
  it is the explicit stack in
  [Exercise 2](../exercises/exercise-02-conveyor-reachability.md), and the
  Stretch below shows it.

- **The answer comes out as `2`.** You computed
  `valve_count - len(hoses)`. Seven lines were logged, so seven "merges" were
  assumed, but two of those lines merged nothing: `(3, 4)` the second time joined
  two valves that were already joined, and `(6, 6)` joined valve 6 to itself.
  There is no traceback — you get a plausible integer, which is exactly how this
  one survives a code review. The counting has to come from the walk.

- **Too many clusters, and the number changes if you reorder the log.** You wrote
  only `joined[left].append(right)`. Half of every hose is missing, so the walk
  can go from 3 to 4 but never from 4 to 3, and whether that matters depends
  entirely on which end the outer loop reaches first. A bug whose answer depends
  on input order is a bug that passes its tests on Tuesday.

- **It never finishes, or the sizes are enormous.** You dropped the
  `if neighbour not in seen` guard, or you add to `seen` in the wrong place — at
  the *neighbour* rather than at function entry. With a repeated hose in the log
  the walk bounces between two valves forever. Mark on entry, check before
  recursing; that is the shape from Lecture 1 §2 and it is the shape that keeps
  working when the colours arrive in Problem 2.

## Under the hood

<details>
<summary>Under the hood — three ways to hold a graph, and when the edge list is the right one</summary>

The same graph has three common shapes, and interviewers switch between them to
see whether you noticed.

| Shape | What it is | Space | "Are `u` and `v` joined?" | "List `u`'s neighbours" |
|---|---|---|---|---|
| Adjacency matrix | A `V x V` grid of marks | `O(V²)` | one step | `O(V)` |
| Adjacency list | Per node, a list of neighbours | `O(V + E)` | `O(degree)` | `O(degree)` |
| Edge list | A flat list of pairs | `O(E)` | `O(E)` | `O(E)` |

Exercise 1 gets a matrix; this page gets an edge list; both convert to, or
already are, something you can walk from. The conversion is the tell that you
know why: an edge list is a wonderful way to *store* a graph — it is exactly what
a database table looks like — and a terrible way to *walk* one, because the
question a walk asks over and over is "who are this node's neighbours," and the
edge list can only answer that by reading everything.

A bench with 900 valves and 5,000 hoses is *sparse*: nowhere near the 404,550
hoses that would join every pair. Sparse graphs are the normal case, and on a
sparse graph the adjacency list wins on space by a mile — 10,000 entries against
810,000 grid cells.

**The `[[] for _ in range(valve_count)]` spelling matters.** `[[]] * valve_count`
looks equivalent and is a classic disaster: it makes one list and points at it
`valve_count` times, so appending a neighbour to valve 3 appends it to every
valve at once. The comprehension makes a fresh list each time round.

**Why not union-find?** Connected components is the textbook use for union-find,
and it would work here in `O(E α(V))` — effectively linear, with a slightly
larger constant. It also handles the repeated hose and the self-loop without
comment: a union of two things already in the same set is a no-op. It is the
better answer when edges *arrive over time* and you have to answer questions in
between. When the whole graph is in front of you, DFS is shorter and needs no
extra data structure, and this is a DFS week.

</details>

## Acceptance checklist

- [ ] `python problem-01-hose-clusters.py` prints the bench summary then `All checks passed.`
- [ ] The two numbers match the Expected output exactly.
- [ ] A repeated pair and a self-loop are handled by the visited set, with no
      special case anywhere in your code.
- [ ] A valve number outside the bench raises `ValueError` naming that number,
      and the check runs before any indexing.
- [ ] The visited set is a `set`.
- [ ] `hoses` is unchanged after the function returns.
- [ ] You can say in one sentence how this differs from
      [Exercise 1](../exercises/exercise-01-repeater-clusters.md) — and the
      sentence is about the input format, not about the algorithm.
- [ ] Your FRAME write-up records the `O(V + E)` defense in your own words.
- [ ] Committed to Git with a message like
      `feat(week-07): homework problem 1, hose clusters`.

## Stretch

- **Return the clusters themselves, not just the count.** Same walk, iterative
  this time, collecting instead of tallying.

  ```python
  def list_clusters(valve_count: int, hoses: list[tuple[int, int]]) -> list[list[int]]:
      """Return each cluster as a sorted list of valve numbers."""
      joined: list[list[int]] = [[] for _ in range(valve_count)]
      for left, right in hoses:
          for valve in (left, right):
              if not 0 <= valve < valve_count:
                  raise ValueError(f"hose names valve {valve}, which is outside 0..{valve_count - 1}")
          joined[left].append(right)
          joined[right].append(left)
      seen: set[int] = set()
      clusters: list[list[int]] = []
      for start in range(valve_count):
          if start in seen:
              continue
          stack = [start]
          seen.add(start)
          group: list[int] = []
          while stack:
              valve = stack.pop()
              group.append(valve)
              for neighbour in joined[valve]:
                  if neighbour not in seen:
                      seen.add(neighbour)
                      stack.append(neighbour)
          clusters.append(sorted(group))
      return clusters
  ```

  ```text
  cluster of 3: [0, 1, 2]
  cluster of 3: [3, 4, 5]
  cluster of 1: [6]
  cluster of 2: [7, 8]
  ```

  Notice `seen.add(neighbour)` moved to the moment the valve goes *onto* the
  stack, not the moment it comes off. Mark on push, or a valve reachable by two
  routes gets pushed twice and counted twice.

- **Take the bound off.** Swap the recursion for an explicit stack and run a
  bench fifty-five times longer than this page allows.

  ```python
  def survey_hoses_iterative(valve_count: int, hoses: list[tuple[int, int]]) -> tuple[int, int]:
      """The same survey with an explicit stack, so depth costs heap not frames."""
      joined: list[list[int]] = [[] for _ in range(valve_count)]
      for left, right in hoses:
          for valve in (left, right):
              if not 0 <= valve < valve_count:
                  raise ValueError(f"hose names valve {valve}, which is outside 0..{valve_count - 1}")
          joined[left].append(right)
          joined[right].append(left)
      seen: set[int] = set()
      cluster_count = 0
      largest = 0
      for start in range(valve_count):
          if start in seen:
              continue
          cluster_count += 1
          seen.add(start)
          stack = [start]
          size = 0
          while stack:
              valve = stack.pop()
              size += 1
              for neighbour in joined[valve]:
                  if neighbour not in seen:
                      seen.add(neighbour)
                      stack.append(neighbour)
          largest = max(largest, size)
      return (cluster_count, largest)
  ```

  ```text
  50000-valve chain, iterative: (1, 50000)
  50000-valve chain, recursive: RecursionError
  ```

  Two lines of output, one whole lesson. The `900` bound was never about the
  problem; it was about the *implementation*. Change the implementation and the
  bound goes away.

- **Ask a question where the repeated hose genuinely matters.** "Which valve has
  the most hoses on it?" is not a connectivity question, and now the duplicate is
  real data.

  ```python
  from collections import Counter

  def busiest_valve(hoses: list[tuple[int, int]], ignore_repeats: bool) -> int | None:
      """Return the valve with the most hose ends on it, lowest number wins ties."""
      seen_pairs: set[tuple[int, int]] = set()
      tally: Counter[int] = Counter()
      for left, right in hoses:
          if left == right:
              continue
          pair = (min(left, right), max(left, right))
          if ignore_repeats:
              if pair in seen_pairs:
                  continue
              seen_pairs.add(pair)
          tally[left] += 1
          tally[right] += 1
      if not tally:
          return None
      return min(tally, key=lambda valve: (-tally[valve], valve))
  ```

  ```text
  counting the log as written : 4
  counting distinct hoses     : 1
  ```

  Two defensible answers to one English sentence, and the difference is entirely
  in what you decided "a hose" means. That decision belongs in your Frame step,
  out loud, before any code — which is the actual point of the exercise.
When your survey is right, move on to
[Problem 2 — Prep Step Audit](./problem-02-prep-step-audit.md).
