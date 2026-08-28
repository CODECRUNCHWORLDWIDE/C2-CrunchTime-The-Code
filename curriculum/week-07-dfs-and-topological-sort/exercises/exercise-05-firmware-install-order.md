# Exercise 5 — Firmware Install Order

> **Topic:** topological sort the other way round — walk depth-first, and add each package to the list when you *finish* it
> **Lecture:** [03 — Topological Sort and Cycle Detection](../lecture-notes/03-topological-sort.md)
> **Difficulty:** Medium/Hard
> **Target time:** 75 minutes
> **Why this one:** Exercise 4 answered "in what order?" by counting. This page answers the same question by walking, and the answer falls out of *when* you write a name down rather than out of any bookkeeping. That is the post-order idea, and it is the shape underneath both of this week's challenges and every tree problem in Phase 3. The last thing this page asks you to do is say which of the two you would reach for, and why — which is the question an interviewer actually asks.

## The Brief

An instrument rack runs on **firmware packages**. Each package may require
other packages to already be installed before it will work: the analyser's user
interface needs the chart widgets, the chart widgets need the graphics
renderer, and so on down.

The manifest is a dictionary. Each key is a package, and the list beside it is
what that package requires:

```python
requires = {
    "analyzer-ui": ["chart-widgets", "measure-core"],
    "chart-widgets": ["render-gl"],
    "measure-core": ["bus-driver", "calibration-tables"],
}
```

Your job: hand back an order in which every package appears **after**
everything it requires, so an engineer can install them one at a time from the
top of the list without anything failing.

That is the same question Exercise 4 asked about a dry-dock refit, and it has
the same name — a **topological order**. What is different is how you get it.

### The idea: write it down when you are done with it

Forget counting. Just walk.

Pick a package. Before you write its name down, go and install everything it
requires — which means visiting each of those, and before writing *their* names
down, installing everything *they* require, and so on. When a package has
nothing left below it, write it down. Then come back up one level and, once
that level's whole list is done, write *that* one down.

Names get written on the way back **up** out of the walk. That is what
**post-order** means: the work happens after the children, not before.

And that is the whole algorithm. A package's name can only be written once
everything underneath it is already on the list, so the list is correct by
construction. There is nothing to reverse at the end, no waiting counts to
maintain, and no ready pile.

Two more things it needs, both small:

- **A finished set.** `chart-widgets` and `measure-core` might both require
  the same thing. The second time you arrive at a package that is already on
  the list, stop — it is done. Without that, a wide manifest is walked
  exponentially many times.
- **A path.** If, while walking down, you arrive at a package you are *already
  standing on*, the requirements go round in a circle and no order exists. Say
  so, and say which packages:

  ```text
  requirement loop: bus-driver -> sensor-io -> bus-driver
  ```

  That is the grey set from [Exercise 3](./exercise-03-batch-loop-audit.md),
  doing exactly the same job here.

### The contract, precisely

`install_order(requires)` returns every package exactly once, each after
everything it requires.

- **Ties are pinned down** so the answer is one specific list: top-level
  packages are entered in sorted order, and each package's requirements are
  walked in sorted order.
- **A package named only as a requirement, never as a key, is still a
  package**, and still appears in the order. Manifests usually only list the
  things that *have* dependencies, so the leaves at the bottom of the rack are
  exactly the ones with no key of their own — and they are also the ones you
  install first. Missing them is not a small bug.
- `install_order({})` returns `[]`.
- A requirement loop raises `ValueError`, and the message spells the loop out.

## Starter

Create `exercise-05-firmware-install-order.py` in your practice repo and paste
this in. Fill in the one `TODO`.

```python
"""exercise-05-firmware-install-order.py — install a rack's firmware in order.

Depth-first, post-order: finish a package, then append it. Because a package is
only appended once everything below it is already on the list, the order comes
out right with nothing to reverse.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

# ---- Given data ----
RACK: dict[str, list[str]] = {
    "analyzer-ui": ["chart-widgets", "measure-core"],
    "chart-widgets": ["render-gl"],
    "measure-core": ["bus-driver", "calibration-tables"],
    "logger": ["alarm-led", "measure-core", "storage-fs"],
    "storage-fs": ["bus-driver"],
}

# bus-driver requires sensor-io and sensor-io requires bus-driver. Neither can
# be installed first, so neither can be installed at all.
TANGLED: dict[str, list[str]] = {
    "bus-driver": ["sensor-io"],
    "sensor-io": ["bus-driver"],
}


# ---- Your task ----
def install_order(requires: dict[str, list[str]]) -> list[str]:
    """Return an order in which every package follows everything it requires.

    Args:
        requires: Maps a package to the packages that must already be
            installed. A package named only as a requirement, never as a key,
            is still a package and still appears in the order.

    Returns:
        Every package exactly once, each one after everything it requires.
        Top-level packages are entered in sorted order and each package's
        requirements are walked in sorted order, so the order is one specific
        list rather than any legal one. An empty manifest gives an empty list.

    Raises:
        ValueError: If the requirements contain a loop. The message spells the
            loop out, e.g. "requirement loop: a -> b -> a".
    """
    # TODO: collect every package (keys AND everything named in the values),
    # then visit each in sorted order. Inside the visit: return early if it is
    # finished, raise if it is on the current path, otherwise walk its sorted
    # requirements and append the package on the way back out.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    rack_order = install_order(RACK)
    print(f"empty manifest : {install_order({})}")
    print(f"one package    : {install_order({'bus-driver': []})}")
    print(f"rack order     : {rack_order}")
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        print(f"tangled rack   : {refusal}")

    assert install_order({}) == []
    assert install_order({"bus-driver": []}) == ["bus-driver"]
    assert install_order({"logger": ["storage-fs"]}) == ["storage-fs", "logger"]
    assert rack_order == [
        "alarm-led",
        "render-gl",
        "chart-widgets",
        "bus-driver",
        "calibration-tables",
        "measure-core",
        "analyzer-ui",
        "storage-fs",
        "logger",
    ]
    assert sorted(rack_order) == sorted(
        set(RACK) | {name for needed in RACK.values() for name in needed}
    )
    for package, needed_by_it in RACK.items():
        for needed in needed_by_it:
            assert rack_order.index(needed) < rack_order.index(package)
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        assert str(refusal) == "requirement loop: bus-driver -> sensor-io -> bus-driver"
    else:
        raise AssertionError("a requirement loop should have been refused")
    print("All checks passed.")
```

Four words you need before you start.

**Post-order.** Doing the work *after* the things below you, on the way back up
out of a walk. Its opposite is **pre-order** — work on the way down, before you
descend. Both walk the same graph in the same shape; they differ only in when
the useful line runs. Almost every "combine results from below" problem is
post-order.

**Finished.** A package already on the order. Arriving at it again is not an
error and not a loop; it is just nothing left to do.

**On the path.** A package you have walked into and not yet walked out of. This
is the grey set from Exercise 3 under another name. Arriving at one of these is
a loop.

**Leaf.** A package that requires nothing. Leaves are the first names on the
order, and in a real manifest they are usually the ones with no key at all.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-07-dfs-and-topological-sort/exercises/exercise-05-firmware-install-order.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `install_order(requires)` returns every package exactly once.
2. Every package appears after everything it requires.
3. Packages named only inside a requirement list are included.
4. Top-level packages are entered in sorted order; each package's requirements
   are walked in sorted order. The answer is one specific list.
5. `install_order({})` returns `[]`.
6. A requirement loop raises `ValueError` whose message is
   `requirement loop: <a> -> <b> -> <a>`, naming the loop in walk order and
   closing it by repeating the first package.
7. A package is never walked twice, however many other packages require it.
8. The function keeps its type hints and its docstring.

## Constraints

- **At most 900 packages in one requirement chain.** This is the one place this
  week where recursion is the shipped answer, and the bound is what makes that
  honest. CPython's default limit is 1,000 frames, so a chain of 900 fits with
  room to spare — and a real firmware manifest is a dozen deep, not nine
  hundred. Say the bound out loud in an interview rather than hoping: *"this
  recurses to the depth of the requirement chain, so it is fine for a manifest
  and I would move it onto an explicit stack for anything that could be
  thousands deep."* The Stretch section writes that version.

- **Total manifest size up to 100,000 packages.** Depth and size are different
  numbers, and only depth threatens the recursion. A hundred thousand packages
  arranged twelve deep is completely safe; nine hundred arranged in a line is
  the edge. Being able to separate those two in one sentence is worth more than
  the code.

- **`O(V + E)`.** One look at every package and one look at every requirement,
  and then it is done — because the finished set means each package is walked
  exactly once and each requirement is read exactly once. Without it the walk
  is exponential: a chain of `n` diamonds re-walks the bottom `2^n` times.

- **Sort at the two points where a choice exists**, and only there. The
  top-level entry order and each requirement list. That is what makes the
  answer one specific list, and it is why a test can compare it item by item
  instead of merely checking that no rule was broken.

- **Collect the package list from the keys *and* the values.** In this manifest
  `alarm-led`, `render-gl`, `bus-driver` and `calibration-tables` have no keys.
  They are also the first four things you install. A version that only looks at
  `requires.keys()` produces an order that installs `chart-widgets` before
  `render-gl` exists, and nothing about that raises.

- **Report the loop, do not just refuse.** `ValueError("requirement loop")` is
  true and useless. The path list you are already keeping gives you the names
  for free, and an error message that names `bus-driver -> sensor-io ->
  bus-driver` is one somebody can act on without opening the manifest.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-firmware-install-order-solution.py
empty manifest : []
one package    : ['bus-driver']
rack order     : ['alarm-led', 'render-gl', 'chart-widgets', 'bus-driver', 'calibration-tables', 'measure-core', 'analyzer-ui', 'storage-fs', 'logger']
tangled rack   : requirement loop: bus-driver -> sensor-io -> bus-driver
All checks passed.
```

Read the rack order carefully, because it is not what a first guess predicts.
It does **not** start with the alphabetically smallest package overall. It
starts with `alarm-led` because the first *top-level* name in sorted order is
`analyzer-ui`, and the walk immediately dives underneath it — and `alarm-led`
is the first name that runs out of things below it.

Wait: `alarm-led` is not under `analyzer-ui` at all; it is required by
`logger`. So why is it first? Because the walk enters packages in sorted order
over **every** package, not just the keys — and `alarm-led` sorts before
`analyzer-ui`. It has no requirements, so it finishes immediately and goes
straight onto the list.

Then `analyzer-ui` is entered, which dives to `chart-widgets`, which dives to
`render-gl` — a leaf, so `render-gl` lands next, then `chart-widgets` finishes
behind it. That pair, adjacent and in that order, is post-order visible in the
output.

## Steps

1. Create the file, paste the starter, and run it. Three report lines print
   `None` and then `assert install_order({}) == []` fails with a bare
   `AssertionError`. Correct first run.
2. Build the package set first: `set(requires)`, then union every value list
   into it. Print it for `RACK` and count nine, not five.
3. Write the visit function with only the finished set — no loop detection at
   all yet. Get `RACK` right. This is about eight lines, and it is the whole
   algorithm.
4. Check the shape of the answer by hand on the small case
   `{"logger": ["storage-fs"]}`. It must be `["storage-fs", "logger"]`. If you
   get them the other way round you have written a pre-order walk: move the
   `append` from before the loop to after it.
5. Now add the path. Append the package before descending, pop it after; keep a
   set beside the list so the check is a hash lookup rather than a scan.
6. Point it at `TANGLED` and get the message exactly right, including the
   repeated package at the end that closes the loop.
7. Run the whole file. Then, with `All checks passed.` printing, do the thing
   this page is really for: write out, in one sentence each, why you would
   choose this over Exercise 4's counting version and why you would not. The
   second Under the hood block has both, but write yours before you read them.

## The Solution

```python
"""exercise-05-firmware-install-order-solution.py — install a rack's firmware in order.

Depth-first search, post-order. Finish a package, then append it. Because a
package is only appended once everything below it is already on the list, the
order is built bottom-up with no reversing and no waiting-count table.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
RACK: dict[str, list[str]] = {
    "analyzer-ui": ["chart-widgets", "measure-core"],
    "chart-widgets": ["render-gl"],
    "measure-core": ["bus-driver", "calibration-tables"],
    "logger": ["alarm-led", "measure-core", "storage-fs"],
    "storage-fs": ["bus-driver"],
}

# bus-driver requires sensor-io and sensor-io requires bus-driver. Neither can
# be installed first, so neither can be installed at all.
TANGLED: dict[str, list[str]] = {
    "bus-driver": ["sensor-io"],
    "sensor-io": ["bus-driver"],
}


# ---- Your task ----
def install_order(requires: dict[str, list[str]]) -> list[str]:
    """Return an order in which every package follows everything it requires.

    Args:
        requires: Maps a package to the packages that must already be
            installed. A package named only as a requirement, never as a key,
            is still a package and still appears in the order.

    Returns:
        Every package exactly once, each one after everything it requires.
        Top-level packages are entered in sorted order and each package's
        requirements are walked in sorted order, so the order is one specific
        list rather than any legal one. An empty manifest gives an empty list.

    Raises:
        ValueError: If the requirements contain a loop. The message spells the
            loop out, e.g. "requirement loop: a -> b -> a".
    """
    packages: set[str] = set(requires)
    for needed in requires.values():
        packages.update(needed)

    order: list[str] = []
    finished: set[str] = set()
    path: list[str] = []
    on_path: set[str] = set()

    def visit(package: str) -> None:
        """Install everything `package` needs, then record `package` itself."""
        if package in finished:
            return
        if package in on_path:
            trail = path[path.index(package) :] + [package]
            raise ValueError("requirement loop: " + " -> ".join(trail))
        path.append(package)
        on_path.add(package)
        for needed in sorted(requires.get(package, [])):
            visit(needed)
        on_path.discard(package)
        path.pop()
        finished.add(package)
        order.append(package)

    for package in sorted(packages):
        visit(package)
    return order


# ---- Self-check ----
if __name__ == "__main__":
    rack_order = install_order(RACK)
    print(f"empty manifest : {install_order({})}")
    print(f"one package    : {install_order({'bus-driver': []})}")
    print(f"rack order     : {rack_order}")
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        print(f"tangled rack   : {refusal}")

    assert install_order({}) == []
    assert install_order({"bus-driver": []}) == ["bus-driver"]
    assert install_order({"logger": ["storage-fs"]}) == ["storage-fs", "logger"]
    assert rack_order == [
        "alarm-led",
        "render-gl",
        "chart-widgets",
        "bus-driver",
        "calibration-tables",
        "measure-core",
        "analyzer-ui",
        "storage-fs",
        "logger",
    ]
    assert sorted(rack_order) == sorted(
        set(RACK) | {name for needed in RACK.values() for name in needed}
    )
    for package, needed_by_it in RACK.items():
        for needed in needed_by_it:
            assert rack_order.index(needed) < rack_order.index(package)
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        assert str(refusal) == "requirement loop: bus-driver -> sensor-io -> bus-driver"
    else:
        raise AssertionError("a requirement loop should have been refused")
    print("All checks passed.")
```

**The whole algorithm is where the `append` sits.**

```python
for needed in sorted(requires.get(package, [])):
    visit(needed)
...
order.append(package)
```

`append` after the loop. Move it above the loop and you have a pre-order walk,
which produces the exact reverse of what you want — every package before the
things it needs. Same code, same walk, same cost, opposite answer. This is the
smallest possible demonstration of why "pre-order or post-order?" is a real
question and not a piece of vocabulary.

**Nothing is reversed at the end, and that is not an accident.** Some
presentations of this algorithm build the list and then reverse it. That
happens when the graph is drawn with the arrows the other way — "package X is
required *by* Y" instead of "X *requires* Y". Our manifest points from a
package to what it needs, so finishing a package means everything it needs is
already down, and the list is already in install order. If you find yourself
reversing, check which way your arrows point before you add the `[::-1]`.

**`finished` and `on_path` are answering two different questions, and merging
them is the classic bug.** `finished` means "already on the list, nothing to
do". `on_path` means "I walked into this and have not walked out — I am
standing on it". Only the second is a loop. This is the same white / grey /
black distinction as [Exercise 3](./exercise-03-batch-loop-audit.md), spelled
with two sets instead of a colour table: not-in-either is white, `on_path` is
grey, `finished` is black. Same idea, different clothes; recognising that they
are the same idea is worth more than either spelling.

**`path` is a list and `on_path` is a set, deliberately.** The list keeps the
order, so the loop can be sliced out of it and named. The set makes the
membership test one hash lookup instead of a scan down the path, which matters
because that test runs once per requirement. Keeping two structures in step is
a real cost; it is paid here because the alternative is either a slow check or
an error message nobody can use.

**The loop message closes the ring on purpose.**

```python
trail = path[path.index(package) :] + [package]
```

`bus-driver -> sensor-io -> bus-driver` reads as a complete sentence. Without
the repeat it reads as a list of two packages and the reader has to infer the
last arrow. Note that this differs from Exercise 3's contract, which returns
the ring *without* the repeat because it hands back a list rather than a
sentence. Two reasonable contracts; the thing that matters is that each one is
stated.

**`requires.get(package, [])`, twice, for the same reason.** A leaf has no key.
Using `requires[package]` works on every package that has requirements and
raises `KeyError` on precisely the ones you install first.

**The recursion is bounded by the depth of the manifest, not its size.** Each
nested call is one link in a requirement chain. A hundred thousand packages
arranged a dozen deep costs a dozen frames. That is why this page can use
recursion honestly where the rest of the week does not — and why the constraint
above states the depth bound rather than a size bound.

## Download and run

Download
[exercise-05-firmware-install-order-solution.py](./exercise-05-firmware-install-order-solution.py)
and run it:

```bash
python exercise-05-firmware-install-order-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-05-firmware-install-order.py`.

## Common bugs to catch

- **The order is exactly backwards.** You appended before recursing instead of
  after:

  ```text
  rack order     : ['alarm-led', 'analyzer-ui', 'chart-widgets', 'render-gl', ...]
  Traceback (most recent call last):
      assert rack_order == [
             ^^^^^^^^^^^^^^^
  AssertionError
  ```

  `analyzer-ui` before `chart-widgets` before `render-gl` — every package ahead
  of the things it needs. That is a pre-order walk, and it is the single most
  common way this exercise goes wrong. Move the `append` below the `for` loop.

- **`KeyError` on a leaf package.**

  ```text
  Traceback (most recent call last):
      for needed in sorted(requires[package]):
                           ~~~~~~~~^^^^^^^^^
  KeyError: 'render-gl'
  ```

  `render-gl` requires nothing, so nobody wrote a line for it. `.get(package,
  [])`. The same oversight in the package-collection step is worse because it
  is silent: only the keys get an order, and four packages simply vanish.

- **A loop is reported where there is none.** You treated `finished` as if it
  meant "on the path":

  ```text
  Traceback (most recent call last):
      rack_order = install_order(RACK)
  ValueError: requirement loop: measure-core -> bus-driver
  ```

  `bus-driver` is required by both `measure-core` and `storage-fs`. The second
  arrival is at a *finished* package, which is ordinary. Check `finished`
  first, return early, and only then check the path.

- **The program hangs, or the recursion blows up on a manifest with a loop.**
  You left out the path check entirely:

  ```text
    File "firmware.py", line 44, in visit
      visit(needed)
      ~~~~~^^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  `bus-driver` needs `sensor-io` needs `bus-driver`, and neither is ever
  finished, so neither is ever cut off. Note what the exception is *not*: it is
  not a report of a loop. It is the recursion limit noticing something is wrong
  a thousand steps late.

- **`RecursionError` on a legitimate deep manifest.** Your chain really is more
  than a thousand packages long. That is outside this page's stated bound, and
  the fix is not `sys.setrecursionlimit` — see
  [Exercise 2](./exercise-02-conveyor-reachability.md), and the explicit-stack
  version in Stretch below.

- **`sorted()` on the top-level packages but not on the requirement lists**, or
  the other way round. Both are needed, and the failure is confusing because
  the order is still *legal* — every rule holds — it is simply not the one the
  test names:

  ```text
  Traceback (most recent call last):
      assert rack_order == [
             ^^^^^^^^^^^^^^^
  AssertionError
  ```

  Any time an assert on a topological order fails but you cannot find a rule
  you broke, the tie rule is where to look.

- **Three lines of `None`, then a bare `AssertionError`.** You ran the starter
  before filling in the `TODO`:

  ```text
  empty manifest : None
  one package    : None
  rack order     : None
  Traceback (most recent call last):
      assert install_order({}) == []
             ^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Correct first run. Note the `try` block printed nothing, because a stub that
  returns `None` never raises the `ValueError` the tangled rack should have
  produced.

## Under the hood

<details>
<summary>Under the hood — why post-order is correct, in three lines</summary>

The claim: **when `visit(p)` appends `p`, everything `p` requires is already in
`order`.**

Proof by looking at the code. `visit(p)` only reaches its `append` after the
`for` loop has finished, and that loop calls `visit(q)` for every `q` that `p`
requires. Each of those calls either appends `q` itself or returns early
because `q` is already in `finished` — and `finished` is only ever added to on
the line above the `append`, so being finished means being in `order`. Either
way, every `q` is in `order` before `p` goes in.

That is the whole correctness argument, and it is short enough to say out loud
in an interview. Notice it needs the loop check to be sound: the third
possibility for `visit(q)` is that it raises, and if it can neither append,
return, nor raise then the walk is not finite. The `on_path` check is what
rules that out.

**The same argument in one sentence:** *a package's name is written only after
every name below it is written, so reading the list from the top never installs
anything before its requirements.*

**Where else this shape turns up.** Any time you need results from the children
before you can answer for the parent — a directory's total size, an
expression tree's value, the height of a tree, the low-link in this week's
[Challenge 1](../challenges/challenge-01-chokepoint-mains.md). All of them are
this walk with a different line after the `for`.

</details>

<details>
<summary>Under the hood — post-order against Kahn, and how to answer "why this one?"</summary>

Exercise 4 and this page answer the same question. Both are `O(V + E)`. Here is
the comparison an interviewer is looking for.

**Reach for the post-order walk when:**

- You want short code and no auxiliary tables. This is about a dozen lines and
  keeps no counts.
- You want the loop *named*, not just detected. The path list gives it to you
  for nothing, and Kahn's leftovers only bound it.
- The graph is a tree, or nearly one. Trees have no loops, so the path check
  disappears and the walk collapses to "visit children, then do the work" —
  which is every tree problem in Phase 3.

**Reach for Kahn when:**

- The graph could be deep. Kahn is a loop over a heap; the post-order walk
  recurses to the depth of the graph unless you convert it.
- You want the **waves** — which packages can be installed at the same time.
  The post-order walk has no notion of "at the same time" anywhere in it.
- You want a smallest-ready-first tie rule. The post-order walk never computes
  "ready", so it cannot honour one; the best it can do is sort its entry points,
  which is a weaker guarantee.
- You want to know *which* work is blocked. Kahn's leftovers are that list.

**The sentence:** *"Post-order gives me the order and the loop's actual path in
a dozen lines with no counts, and it is the natural shape whenever a parent
needs answers from its children — I would switch to Kahn if the graph could be
deep, or if I needed the parallel waves or the blocked set, because neither
falls out of a depth-first walk."*

**A historical note you do not need but will meet.** The counting version is
usually credited to Arthur Kahn's 1962 paper; the depth-first version is
associated with Robert Tarjan's graph work in the early 1970s. Nobody in an
interview needs the names. They need what each one costs and what each one
hands you free.

</details>

## Acceptance checklist

- [ ] `python exercise-05-firmware-install-order.py` prints four report lines
      and then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] The rack order contains nine packages, not five.
- [ ] `install_order({"logger": ["storage-fs"]})` is `["storage-fs", "logger"]`.
- [ ] `install_order({})` is `[]`.
- [ ] `install_order(TANGLED)` raises `ValueError` with the message
      `requirement loop: bus-driver -> sensor-io -> bus-driver`.
- [ ] `RACK` produces no loop report, even though `bus-driver` is reached twice.
- [ ] You can say, without notes, why the `append` goes after the loop.
- [ ] You have written your own one-sentence answer to "why this and not
      Kahn?".
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 5: firmware install order`.

## Stretch

- **Measure each package's footprint** — how many distinct packages it drags in
  altogether. Same post-order walk, with a set union where the `append` was.

  ```python
  def install_footprint(requires: dict[str, list[str]]) -> dict[str, int]:
      """How many distinct packages each one pulls in, itself not counted."""
      beneath: dict[str, set[str]] = {}
      for package in install_order(requires):
          pool: set[str] = set()
          for needed in requires.get(package, []):
              pool.add(needed)
              pool |= beneath[needed]
          beneath[package] = pool
      return {package: len(pool) for package, pool in beneath.items()}
  ```

  ```text
  analyzer-ui        5
  logger             5
  measure-core       2
  chart-widgets      1
  storage-fs         1
  alarm-led          0
  bus-driver         0
  calibration-tables 0
  render-gl          0
  ```

  Two things worth noticing. First, the walk has disappeared: iterating
  `install_order` *is* the post-order traversal, because that list is already in
  the right order. When you have a topological order, you rarely need to walk
  again. Second, the sets are unioned rather than the counts added — `logger`
  sits on both `measure-core` and `storage-fs`, and both of those sit on
  `bus-driver`, so adding the counts would charge `bus-driver` twice and give
  `logger` a footprint of six instead of five.

- **Write the explicit-stack version**, the one that survives a manifest ten
  thousand deep.

  ```python
  def install_order_iterative(requires: dict[str, list[str]]) -> list[str]:
      """The same order, with the pending work in a list instead of frames."""
      packages: set[str] = set(requires)
      for needed in requires.values():
          packages.update(needed)
      order: list[str] = []
      finished: set[str] = set()
      for root in sorted(packages):
          if root in finished:
              continue
          stack: list[tuple[str, list[str], int]] = [
              (root, sorted(requires.get(root, [])), 0)
          ]
          while stack:
              package, needs, spot = stack[-1]
              if spot == len(needs):
                  finished.add(package)
                  order.append(package)
                  stack.pop()
                  continue
              stack[-1] = (package, needs, spot + 1)
              nxt = needs[spot]
              if nxt not in finished:
                  stack.append((nxt, sorted(requires.get(nxt, [])), 0))
      return order
  ```

  ```text
  same order as the recursive version: True
  10000-deep manifest: 10000 packages, first is pkg-00000
  ```

  Compare it honestly against the shipped answer. It is twice the length, the
  `spot` index does by hand what the `for` loop did for free, and it has no
  loop detection in it at all — adding that back means carrying `on_path`
  alongside. What it buys is a walk with no depth limit. That is the trade, and
  on a manifest that is a dozen deep it is not worth taking.

- **Show the pre-order walk is exactly the reverse.** Build the same walk with
  the `append` moved above the loop and compare.

  ```text
  post-order : ['alarm-led', 'render-gl', 'chart-widgets', 'bus-driver', ...]
  pre-order  : ['alarm-led', 'analyzer-ui', 'chart-widgets', 'render-gl', ...]
  is one the reverse of the other? False
  ```

  `False`, and that surprises people. Pre-order is not the reverse of
  post-order in general — reversing post-order gives you a valid *reverse*
  install order, but pre-order gives you something that is neither. One line
  moved, and the output stops being an answer to any question. That is worth
  sitting with for a minute.

**Practice elsewhere.** The same walk appears as
[LeetCode 210 · Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)
if you want a judge to run against — though there the arrows point the other
way, so the post-order list has to be reversed, and the contract returns an
empty list on a loop where ours raises with the loop named.

That is the last exercise. Next:
[Challenge 1 — Chokepoint Mains](../challenges/challenge-01-chokepoint-mains.md),
where the work done on the way back up is a number rather than a name.
