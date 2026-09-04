# Exercise 1 — Repeater Clusters

> **Topic:** recursive depth-first search with a visited set, used to find connected components and count each one
> **Lecture:** [01 — Recursive DFS](../lecture-notes/01-recursive-dfs.md)
> **Difficulty:** Easy/Medium
> **Target time:** 45 minutes
> **Why this one:** this is the smallest problem where the recursive DFS template earns its keep, and the smallest where "count the links" and "walk the links" give different answers. Get the outer loop right here — one fresh walk per cluster, and the mast that starts the walk is the cluster's name — and connected components stop being a thing you look up. It is also, deliberately, the last page this week where plain recursion is safe.

## The Brief

A volunteer emergency-radio org keeps a set of **repeater masts** on hilltops.
A repeater mast is a box on a pole that hears a weak radio message and shouts
it again, louder, so it travels further. The masts are numbered `0`, `1`, `2`,
and so on up to one less than however many there are.

Some masts can hear each other directly. The org keeps that in a **link
table**: a square grid of `0`s and `1`s. `links[i][j]` is `1` when mast `i` and
mast `j` hear each other directly, and `0` when they do not. The grid is
symmetric — if `i` hears `j`, then `j` hears `i`, so `links[i][j]` and
`links[j][i]` always agree.

**The diagonal is always `0`.** `links[3][3]` is `0`, always. A mast is not
listed as hearing itself. Most link tables you meet elsewhere put a `1` there;
this one does not, on purpose, and later on the page you will see exactly which
wrong answer that choice catches.

Now the idea worth having. Think of it like people at a noisy party. Two people
are in the same conversation if they can hear each other — **or** if a friend
in between can hear them both and pass the message along. You do not need to
hear someone directly to be in their conversation.

Masts work the same way. Two masts are in the same **cluster** when a message
can get from one to the other through any chain of direct links, however long.
A mast that hears nobody at all is still a cluster — a cluster of one.

Your job: write `survey_clusters(links)`. It hands back one entry per cluster:
a pair `(leader, size)`, where `leader` is the smallest mast number in that
cluster and `size` is how many masts it holds. The entries come back sorted
ascending by leader. No masts at all gives an empty list.

The important thing to notice is that `size` is not "how many `1`s are in that
mast's row". A mast with one direct link can sit in a cluster of three hundred.
You have to walk the chain.

## Starter

Create `exercise-01-repeater-clusters.py` in your practice repo and paste this
in. Fill in the `TODO`.

```python
"""exercise-01-repeater-clusters.py — the repeater-mast cluster survey.

Walk a symmetric 0/1 link table and report one (leader, size) pair per
cluster of masts that can reach each other.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

# ---- Given data ----
PAIR_AND_A_LONER: list[list[int]] = [
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 0],
]

CHAIN_OF_THREE: list[list[int]] = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
]

FULLY_LINKED_TRIPLE: list[list[int]] = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

INTERLEAVED: list[list[int]] = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def chain_of_masts(masts: int) -> list[list[int]]:
    """Build an n x n link table whose masts form one straight relay chain.

    Args:
        masts: How many masts the chain holds.

    Returns:
        A symmetric table with a zero diagonal where mast i hears mast i + 1.
    """
    table = [[0] * masts for _ in range(masts)]
    for mast in range(masts - 1):
        table[mast][mast + 1] = 1
        table[mast + 1][mast] = 1
    return table


# ---- Your task ----
def survey_clusters(links: list[list[int]]) -> list[tuple[int, int]]:
    """Return one (leader, size) pair per cluster, ascending by leader.

    Args:
        links: A symmetric n x n table of 0s and 1s with a zero diagonal.
            `links[i][j] == 1` means masts i and j hear each other directly.

    Returns:
        One (leader, size) pair per cluster, where leader is the smallest mast
        number in that cluster, sorted ascending by leader. An empty table
        gives an empty list.
    """
    # TODO: one fresh DFS per unvisited mast, counting what it marks
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"no masts at all   : {survey_clusters([])}")
    print(f"one lonely mast   : {survey_clusters([[0]])}")
    print(f"pair and a loner  : {survey_clusters(PAIR_AND_A_LONER)}")
    print(f"chain of three    : {survey_clusters(CHAIN_OF_THREE)}")
    print(f"fully-linked trio : {survey_clusters(FULLY_LINKED_TRIPLE)}")
    print(f"interleaved       : {survey_clusters(INTERLEAVED)}")
    print(f"900-mast chain    : {survey_clusters(chain_of_masts(900))}")

    assert survey_clusters([]) == []
    assert survey_clusters([[0]]) == [(0, 1)]
    assert survey_clusters([[0, 0], [0, 0]]) == [(0, 1), (1, 1)]
    assert survey_clusters(PAIR_AND_A_LONER) == [(0, 2), (2, 1)]
    assert survey_clusters(CHAIN_OF_THREE) == [(0, 3), (3, 1)]
    assert survey_clusters(FULLY_LINKED_TRIPLE) == [(0, 3)]
    assert survey_clusters(INTERLEAVED) == [(0, 2), (1, 2), (4, 1)]
    assert survey_clusters(chain_of_masts(900)) == [(0, 900)]
    print("All checks passed.")
```

Three words you need before you start.

**Depth-first search**, or DFS. A way of walking a set of connected things.
Stand on one, walk to a neighbour, then from there to *its* neighbour, and keep
going as deep as you can before turning round. The opposite habit — check every
neighbour first, then their neighbours — is breadth-first search, which you met
last week. Both reach the same masts. DFS is shorter to write when you only
care *whether* you get there.

**Visited set.** A `set` of the masts you have already stood on. Without it,
mast 0 walks to mast 1, mast 1 looks back at mast 0, and the two of them bounce
forever. With it, every mast is entered exactly once, and that single fact is
what makes the whole thing fast.

**Connected component.** The proper name for what this page calls a cluster: a
group where everything can reach everything else, and nothing outside can be
reached at all.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/exercises/exercise-01-repeater-clusters.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `survey_clusters(links)` returns a list of `(leader, size)` tuples — plain
   tuples, not lists and not dicts.
2. `leader` is the **smallest mast number** in its cluster.
3. `size` is how many masts the cluster holds, counted by walking the links,
   not by adding up a row.
4. The result is sorted ascending by `leader`.
5. `survey_clusters([])` returns `[]`, not `[(0, 0)]` and not `None`.
6. A mast that hears nobody is its own cluster of size one:
   `survey_clusters([[0]]) == [(0, 1)]`.
7. `survey_clusters(chain_of_masts(900))` returns `[(0, 900)]` — one cluster,
   nine hundred masts, no crash.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= n <= 900`, and `links` is `n` rows of `n` numbers.** Nine hundred is
  chosen for two reasons, and both are worth saying out loud in Examine. First,
  `900 x 900` is 810,000 table cells, so *reading the table* is already the
  floor — you cannot beat "one look at every cell", so `O(n^2)` is not a defeat
  here, it is the answer. Second, the longest possible chain of masts is 900
  links deep, and the recursive walk therefore stacks at most 900 calls, which
  sits just under CPython's default limit of 1000. The recursive template is
  safe on this page **on purpose**, so that
  [Exercise 2](./exercise-02-conveyor-reachability.md) can be the page where it
  stops being safe.

- **`links[i][j] == links[j][i]` for every `i` and `j`.** The link table is
  symmetric because radio is symmetric: if mast 3 can hear mast 7, mast 7 can
  hear mast 3. This is an *undirected* graph, which is why nothing on this page
  needs the directed-graph machinery from Lecture 3. If you find yourself
  reaching for cycle colours, re-read the prompt.

- **`links[i][i] == 0` for every `i`.** A mast is never listed as hearing
  itself. This is the reverse of the usual convention, and the reason is
  pedagogical: a solution that decides "mast `i` exists because `links[i][i]`
  is `1`" reports **zero clusters on every input here**, loudly and
  immediately, instead of quietly working until the day the convention changes.
  Count masts with `len(links)`.

- **Use a `set` for visited, never a `list`.** Asking `mast in visited` costs
  the same tiny amount every time on a set. On a list it costs a scan of the
  whole list, so the survey quietly turns from 810,000 steps into hundreds of
  millions on a full table. Nothing crashes; it just gets slow, which is the
  worst kind of bug.

- **Every mast is read exactly once, so read every cell exactly once.** The
  outer loop climbs from mast `0` upwards and starts a walk only at a mast
  nobody has visited. Because it climbs, the mast that starts a walk is
  automatically the smallest in its cluster — that is your leader, free, with
  no second pass to find a minimum.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-repeater-clusters.py
no masts at all   : []
one lonely mast   : [(0, 1)]
pair and a loner  : [(0, 2), (2, 1)]
chain of three    : [(0, 3), (3, 1)]
fully-linked trio : [(0, 3)]
interleaved       : [(0, 2), (1, 2), (4, 1)]
900-mast chain    : [(0, 900)]
All checks passed.
```

Look hard at the fourth line. `CHAIN_OF_THREE` gives `[(0, 3), (3, 1)]`, and
mast `0` has exactly **one** `1` in its row. Its cluster still holds three
masts, because `0` reaches `2` *through* `1`. If your answer is
`[(0, 2), (1, 3), (2, 2), (3, 1)]` you counted direct links instead of walking
the chain — that is the single most common wrong answer, and it is why this
example is on the page.

Look at the sixth line too. `INTERLEAVED` gives leaders `0`, `1` and `4`. The
leaders are not consecutive, and the clusters are not blocks of neighbouring
numbers — mast `0` is grouped with mast `2`, and mast `1` with mast `3`.
Clusters have nothing to do with how the masts are numbered.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-repeater-clusters.py`. You get a `TypeError` on the
   first `print`. That is the correct starting point — it proves the
   self-checks are real.
2. Write the outer loop first, with no walking at all. For each mast from `0`
   upwards, if it is not in `visited`, add it and append `(mast, 1)`. Run it.
   You now get one cluster per mast, every size `1`. That is wrong, but it is
   wrong in a shape you can fix.
3. Now write the inner walk. Give it one job: mark this mast, then for every
   other mast in the row that holds a `1` and has not been visited, walk there
   too. Have it return how many masts it marked — `1` for itself, plus whatever
   the deeper calls report.
4. Wire the walk's return value into the outer loop's `append`. Run again.
   `PAIR_AND_A_LONER` should now be `[(0, 2), (2, 1)]`.
5. Trace `CHAIN_OF_THREE` on paper before you trust it. Start at `0`, mark it,
   go to `1`, mark it, go to `2`, mark it, come back, come back. Three marks,
   one cluster. Then the outer loop reaches `3`, which nobody marked, and that
   is the second cluster.
6. Run the 900-mast check last. If it passes, you have just proved the recursion
   depth argument on real input rather than on a promise.
7. When `All checks passed.` prints, open a REPL with
   `python -i exercise-01-repeater-clusters.py` and try tables you invent. A
   ring of four masts is a good one — everyone has two links, and there is only
   one cluster.

## The Solution

```python
"""exercise-01-repeater-clusters-solution.py — the repeater-mast cluster survey.

Recursive depth-first search over a symmetric 0/1 link table. Each fresh DFS
start is one cluster, and because the outer loop climbs from mast 0 upwards,
the mast that starts a cluster is automatically that cluster's leader.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
PAIR_AND_A_LONER: list[list[int]] = [
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 0],
]

CHAIN_OF_THREE: list[list[int]] = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
]

FULLY_LINKED_TRIPLE: list[list[int]] = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

INTERLEAVED: list[list[int]] = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def chain_of_masts(masts: int) -> list[list[int]]:
    """Build an n x n link table whose masts form one straight relay chain.

    Args:
        masts: How many masts the chain holds.

    Returns:
        A symmetric table with a zero diagonal where mast i hears mast i + 1.
    """
    table = [[0] * masts for _ in range(masts)]
    for mast in range(masts - 1):
        table[mast][mast + 1] = 1
        table[mast + 1][mast] = 1
    return table


# ---- Your task ----
def survey_clusters(links: list[list[int]]) -> list[tuple[int, int]]:
    """Return one (leader, size) pair per cluster, ascending by leader.

    Args:
        links: A symmetric n x n table of 0s and 1s with a zero diagonal.
            `links[i][j] == 1` means masts i and j hear each other directly.

    Returns:
        One (leader, size) pair per cluster, where leader is the smallest mast
        number in that cluster, sorted ascending by leader. An empty table
        gives an empty list.
    """
    total = len(links)
    visited: set[int] = set()
    clusters: list[tuple[int, int]] = []

    def walk(mast: int) -> int:
        """Mark every mast reachable from `mast` and return how many that was."""
        visited.add(mast)
        reached = 1
        row = links[mast]
        for other in range(total):
            if row[other] == 1 and other not in visited:
                reached += walk(other)
        return reached

    for mast in range(total):
        if mast not in visited:
            clusters.append((mast, walk(mast)))
    return clusters


# ---- Self-check ----
if __name__ == "__main__":
    print(f"no masts at all   : {survey_clusters([])}")
    print(f"one lonely mast   : {survey_clusters([[0]])}")
    print(f"pair and a loner  : {survey_clusters(PAIR_AND_A_LONER)}")
    print(f"chain of three    : {survey_clusters(CHAIN_OF_THREE)}")
    print(f"fully-linked trio : {survey_clusters(FULLY_LINKED_TRIPLE)}")
    print(f"interleaved       : {survey_clusters(INTERLEAVED)}")
    print(f"900-mast chain    : {survey_clusters(chain_of_masts(900))}")

    assert survey_clusters([]) == []
    assert survey_clusters([[0]]) == [(0, 1)]
    assert survey_clusters([[0, 0], [0, 0]]) == [(0, 1), (1, 1)]
    assert survey_clusters(PAIR_AND_A_LONER) == [(0, 2), (2, 1)]
    assert survey_clusters(CHAIN_OF_THREE) == [(0, 3), (3, 1)]
    assert survey_clusters(FULLY_LINKED_TRIPLE) == [(0, 3)]
    assert survey_clusters(INTERLEAVED) == [(0, 2), (1, 2), (4, 1)]
    assert survey_clusters(chain_of_masts(900)) == [(0, 900)]
    print("All checks passed.")
```

**The outer loop is the cluster counter, and the walk is the cluster.** Every
time the outer loop finds a mast nobody has visited, that is a brand new
cluster, because if it belonged to an earlier one, an earlier walk would have
marked it. So the number of times the outer loop starts a walk *is* the number
of clusters. You never count clusters; you notice how many times you had to
start again.

**The leader is free because the loop ascends.** `for mast in range(total)`
goes `0, 1, 2, …`. The first mast of a cluster the loop meets is therefore the
smallest-numbered mast in it. There is no second pass looking for a minimum,
and no sorting at the end — the result is already in leader order because it
was built in leader order. Say that out loud in an interview; it is the kind of
observation that separates "I made it work" from "I know why it works".

**`visited.add(mast)` is the very first line of `walk`, not the last.** Mark on
entry. If you marked on the way out instead, mast `0` would walk to mast `1`,
which would look back at an unmarked mast `0`, and the two would ping-pong
until the interpreter gave up. Marking on entry is the invariant that makes
"every mast is entered at most once" true, and every cost argument on this page
leans on it.

**The walk returns a count, so the recursion does the adding for you.**
`reached` starts at `1` — this mast — and each deeper call hands back the size
of the piece it explored. No shared counter, no `nonlocal`, nothing to reset
between clusters. A nonlocal counter also works, and is a perfectly good answer;
returning the size just keeps each call's meaning self-contained, which is
easier to defend when someone asks what `walk` promises.

**`row = links[mast]` is pulled out of the loop on purpose.** Inside the loop
you would otherwise index the outer list and then the inner list on every one
of `n` iterations. On an 810,000-cell table that is 810,000 avoidable index
operations. It changes nothing about the complexity and quite a lot about the
clock.

**The cost, said in plain words: one look at every cell of the table, and then
it is done.** That is `O(n^2)` time — and on a table input `O(n^2)` is the
floor, not a failure, because the input *is* `n^2` numbers. Space is `O(n)`:
the visited set holds at most `n` masts, and the recursion is at most as deep
as the longest chain of masts, which is `n` in the worst case. That worst case
is exactly what the 900-mast check exercises, and 900 frames is why the bound
is 900 and not 9,000.

## Run it

Copy the worked answer on this page into `exercise-01-repeater-clusters.py` and run it:

```bash
python exercise-01-repeater-clusters.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-01-repeater-clusters.py`.

## Common bugs to catch

- **`RecursionError: maximum recursion depth exceeded` on a six-mast table.**
  You dropped the `and other not in visited` from the walk's `if`:

  ```text
  Traceback (most recent call last):
      clusters.append((mast, walk(mast)))
                             ~~~~^^^^^^
      reached += walk(other)
                 ~~~~^^^^^^^
      reached += walk(other)
                 ~~~~^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Six masts, a thousand frames. Mast `0` walks to mast `1`; mast `1` looks back
  at mast `0`, which is in the table as a `1`, and walks there; and round they
  go. Adding to `visited` is not enough on its own — you also have to *check*
  it before you recurse. This is the fastest way to prove to yourself why the
  visited set is an invariant and not an optimisation.

- **Every size is one more than the number of `1`s in the row.** You returned
  `1 + sum(row)` per mast instead of walking:

  ```text
  [(0, 2), (1, 3), (2, 2), (3, 1)]
  Traceback (most recent call last):
      assert survey_clusters(CHAIN_OF_THREE) == [(0, 3), (3, 1)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Four entries where the answer has two. Direct links are not the cluster.
  Mast `0` has one link and a cluster of three; mast `1` has two links and the
  same cluster of three. The only way to get the size is to walk it.

- **`survey_clusters([])` raises `IndexError`.** You measured the table's width
  with `len(links[0])`:

  ```text
  Traceback (most recent call last):
      print(survey_clusters([]))
            ~~~~~~~~~~~~~~~^^^^
      width = len(links[0])
                  ~~~~~^^^
  IndexError: list index out of range
  ```

  An empty table has no first row to measure. The table is square, so
  `len(links)` is both the height and the width, and it is `0` on the empty
  case without any guard at all.

- **Every table returns `[]`.** You used the diagonal to decide whether a mast
  exists — `if links[mast][mast] == 1` — which is the convention most link
  tables use and is not this one's:

  ```text
  []
  Traceback (most recent call last):
      assert survey_clusters(CHAIN_OF_THREE) == [(0, 3), (3, 1)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  This is exactly what the zero diagonal is there to catch, and it is the
  reason the constraint is stated as loudly as it is. The masts are
  `range(len(links))`; the table only says who hears whom.

- **The result is in a strange order, or a leader is not the smallest number.**
  You collected clusters into a dict or a set first, or you started the outer
  loop somewhere other than `0`. The leader property is not something you
  compute — it falls out of climbing from `0` upwards and starting a walk only
  at unvisited masts. If you had to sort the result at the end, something
  earlier went wrong.

## Under the hood

<details>
<summary>Under the hood — why a matrix input caps how clever you are allowed to be</summary>

**You cannot beat `O(n^2)` here, and it is worth knowing why that is a fact
about the input rather than about your code.**

The link table has `n^2` numbers in it. Any correct answer has to be allowed to
depend on all of them, because flipping a single `0` to a `1` anywhere can
merge two clusters and change the output. So a correct algorithm must at least
be able to look at every cell, and that alone is `n^2` work. No traversal, no
clever data structure, and no amount of union-find gets under that floor while
the input is shaped this way.

Written as an adjacency **list** instead — each mast paired with just the masts
it actually hears — the same survey is `O(V + E)`: one look at every mast and
one look at every link, and then it is done. On a sparse network, where each
mast hears two or three others, that is dramatically less work than 810,000
cells. The algorithm did not get better. The input got smaller.

That is the real lesson, and it comes up in interviews as a follow-up: *"what
if the graph were given as an adjacency list?"* The answer is that the code
barely changes — swap `for other in range(total)` for `for other in
adjacent[mast]` — and the complexity claim changes completely.

**Why not union-find?**

Union-find (also called disjoint-set) is the other classic tool for connected
components, and it would work. It is `O(n^2 * a(n))` here, where `a` is the
inverse Ackermann function and is effectively a small constant — so, the same
`O(n^2)`, with a slightly bigger constant factor and considerably more code.

It also gives you the wrong leader. Union-find's representative for a group is
whichever element ended up as the tree root, which depends on the order the
unions happened and on the union-by-rank tie-breaks. It is not the smallest
index. You would have to take a second pass over every mast to find the true
minimum per group — which is exactly the pass this page's outer loop lets you
skip.

Union-find earns its place when links *arrive over time* and you have to answer
"are these two connected?" between arrivals. DFS needs the whole table up
front. That difference, not the complexity, is the one to say out loud.

**Why not BFS?**

Breadth-first search from last week answers this identically, in the same
`O(n^2)`, with the same visited-set invariant. The only differences are that it
needs an explicit `deque` and a couple more lines, and that it never risks a
recursion limit. On this page's bound of 900 that last point does not bite,
which is why the recursive version is fine here — and precisely why
[Exercise 2](./exercise-02-conveyor-reachability.md) raises the bound until it
does.

</details>

## Acceptance checklist

- [ ] `python exercise-01-repeater-clusters.py` prints seven lines then `All checks passed.`
- [ ] The printed lines match the expected output character for character.
- [ ] `survey_clusters([])` returns `[]` with no guard clause needed for `links[0]`.
- [ ] `visited` is a `set`, and `visited.add` is the first line of the walk.
- [ ] The recursive call is guarded by `not in visited` on the calling side.
- [ ] Nothing in your solution reads `links[i][i]`.
- [ ] The result is never sorted at the end — it comes out in leader order.
- [ ] You can say the cost sentence out loud: one look at every cell of the table, and then it is done.
- [ ] The function keeps its type hints and its docstring.

## Stretch

- **Return the masts themselves, not just how many.**

  ```python
  def cluster_members(links: list[list[int]]) -> list[list[int]]:
      """Return the masts of each cluster, ascending, clusters ordered by leader."""
      total = len(links)
      visited: set[int] = set()
      clusters: list[list[int]] = []

      def walk(mast: int, members: list[int]) -> None:
          visited.add(mast)
          members.append(mast)
          for other in range(total):
              if links[mast][other] == 1 and other not in visited:
                  walk(other, members)

      for mast in range(total):
          if mast not in visited:
              members: list[int] = []
              walk(mast, members)
              clusters.append(sorted(members))
      return clusters
  ```

  ```text
  [[0, 2], [1, 3], [4]]
  [[0, 1, 2], [3]]
  ```

  The first line is `INTERLEAVED`, the second is `CHAIN_OF_THREE`. Note the
  `sorted(members)` — DFS visits in walk order, not numeric order, so the list
  arrives shuffled. The size never noticed, which is why the main exercise
  could get away without it.

- **Find the biggest cluster, ties going to the lower leader.**

  ```python
  def widest_cluster(links: list[list[int]]) -> tuple[int, int]:
      """Return the (leader, size) of the biggest cluster; ties go to the lower leader."""
      return max(e1.survey_clusters(links), key=lambda cluster: (cluster[1], -cluster[0]))
  ```

  ```text
  interleaved      : (0, 2)
  chain of three   : (0, 3)
  ```

  `INTERLEAVED` has two clusters of size two, and the tuple key settles it:
  biggest size first, then the *smaller* leader, which is why the leader is
  negated and the size is not. Same trick as Week 5's sorting key, on `max`
  instead of `sorted`.

- **Rewrite the walk with an explicit stack, and push the bound past 900.**

  ```python
  def survey_clusters_iteratively(links: list[list[int]]) -> list[tuple[int, int]]:
      """The same survey with the pending masts on an explicit stack."""
      total = len(links)
      visited: set[int] = set()
      clusters: list[tuple[int, int]] = []
      for leader in range(total):
          if leader in visited:
              continue
          size = 0
          stack = [leader]
          while stack:
              mast = stack.pop()
              if mast in visited:
                  continue
              visited.add(mast)
              size += 1
              row = links[mast]
              stack.extend(other for other in range(total) if row[other] == 1)
          clusters.append((leader, size))
      return clusters
  ```

  ```text
  interleaved      : [(0, 2), (1, 2), (4, 1)]
  2000-mast chain  : [(0, 2000)]
  ```

  Two thousand masts, which the recursive version on this page cannot survive.
  Notice where the visited check moved: the recursive version checks *before*
  recursing, this one checks *after* popping, because the same mast can be
  pushed twice before either copy comes off. That difference is the whole
  subject of the next page.
When your survey is right, move on to
[Exercise 2 — Conveyor Reachability](./exercise-02-conveyor-reachability.md),
where the chains get long enough to break the recursion you just wrote.
