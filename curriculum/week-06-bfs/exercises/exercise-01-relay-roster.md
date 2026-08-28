# Exercise 1 — Relay Roster

> **Topic:** walking a network one hop at a time, and freezing the size of a hop before the queue grows
> **Lecture:** [01 — The BFS Template](../lecture-notes/01-the-bfs-template.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** this is the smallest problem where the level snapshot matters, so it is the cleanest place to learn it. Every "by level", "by tier", "by round" answer for the rest of the course is this one loop. It also drills the thing beginners forget on their first graph: a network is not the same as a list of keys, so "who exists" and "who did we reach" are two different questions and you need both.

## The Brief

A river has broken its banks. The response team keeps a mesh of small radio
relays across the valley, and each one repeats anything it hears.

Think of shouting in a canyon. You shout once. The people who can hear you
shout it on. The people who can hear *them* shout it on again. The message
travels outward in rings.

A **hop** is one of those rings. Hop 0 is you. Hop 1 is everyone who hears
you directly. Hop 2 is everyone who first hears it from someone in hop 1.
Nobody appears twice: once you have heard the message, hearing it again
changes nothing.

The mesh is written down as a dictionary. Each key is a relay's call-sign,
and its value is the list of relays that **can hear it**:

```python
"BASE": ["KILO", "MIKE"]
```

That says KILO and MIKE can both hear BASE. It does **not** say BASE can
hear them. Hills do that: a relay in a dip can shout up the valley and hear
nothing back. So this is a **one-way** network, and you must read it in the
direction it is written.

Your job is to write the roster the radio operator reads out: hop 0, hop 1,
hop 2, and so on, with each hop's call-signs in alphabetical order. Then the
part the operator actually worries about — the **stranded** list. Those are
the relays the mesh mentions somewhere but the broadcast never reaches. On a
flood night, that list is the one that gets somebody in a boat.

Two details that are decisions, not accidents:

- The mesh mentions a call-sign if it is a key **or** if it appears in
  anybody's list. A relay that only ever listens is still a relay.
- A call-sign that is not mentioned anywhere is not a relay at all, so
  broadcasting from it raises `ValueError`. An empty mesh mentions nobody, so
  every base raises.

## Starter

Create `exercise-01-relay-roster.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""exercise-01-relay-roster.py — who hears the flood warning, and when.

A mesh of radio relays. The base station transmits once; every relay that
hears it repeats the message; every relay that hears a repeat repeats it
again. Report the roster of call-signs at each hop, plus the relays nobody
ever reaches.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque

# ---- Given data ----
# Who each relay can be heard BY. Terrain makes this one-way in places:
# NOVA can hear BASE, but BASE sits in a dip and cannot hear NOVA.
LINKS: dict[str, list[str]] = {
    "BASE": ["KILO", "MIKE"],
    "KILO": ["NOVA", "OSCAR"],
    "MIKE": ["OSCAR", "PAPA"],
    "NOVA": ["BASE"],
    "OSCAR": ["QUEBEC"],
    "PAPA": [],
    "QUEBEC": [],
    "ROMEO": ["SIERRA"],
    "SIERRA": ["ROMEO"],
}


# ---- Your task ----
def every_sign(links: dict[str, list[str]]) -> set[str]:
    """Return every call-sign the mesh mentions, as a transmitter or a listener.

    Args:
        links: The mesh. Each key is a relay; its value is the relays that
            can hear it.

    Returns:
        A set holding every call-sign that appears anywhere in the mesh.
    """
    # TODO: start from the keys, then fold in every listener list
    ...


def broadcast_roster(
    links: dict[str, list[str]], base: str
) -> tuple[list[list[str]], list[str]]:
    """Return the hop-by-hop roster of a broadcast, and the relays it misses.

    Args:
        links: The mesh. Each key is a relay; its value is the relays that
            can hear it.
        base: The call-sign that transmits first.

    Returns:
        A pair. The first item is a list of hops: hop 0 holds only `base`,
        hop 1 holds every relay that hears `base` directly, and so on. Each
        hop's call-signs are sorted A to Z. The second item is every
        call-sign the broadcast never reaches, also sorted A to Z.

    Raises:
        ValueError: If `base` is not a call-sign the mesh mentions. An empty
            mesh mentions nothing, so every base raises.
    """
    # TODO: raise ValueError when base is not mentioned anywhere
    # TODO: deque seeded with base, a `reached` set holding base
    # TODO: while the queue has anything in it:
    #         snapshot len(queue) FIRST, then pop exactly that many
    #         collect them into this hop, sorted, and append to the roster
    # TODO: stranded is every mentioned sign that is not in `reached`
    ...


# ---- Self-check ----
if __name__ == "__main__":
    hops, stranded = broadcast_roster(LINKS, "BASE")
    for number, roster in enumerate(hops):
        print(f"hop {number}: {', '.join(roster)}")
    print(f"stranded: {', '.join(stranded)}")

    assert hops == [
        ["BASE"],
        ["KILO", "MIKE"],
        ["NOVA", "OSCAR", "PAPA"],
        ["QUEBEC"],
    ]
    assert stranded == ["ROMEO", "SIERRA"]

    # A relay that hears nobody is still a hop of its own, alone.
    lonely, lonely_stranded = broadcast_roster(LINKS, "PAPA")
    assert lonely == [["PAPA"]]
    assert len(lonely_stranded) == 8

    # Starting inside the stranded island reaches only the island.
    island, island_stranded = broadcast_roster(LINKS, "ROMEO")
    assert island == [["ROMEO"], ["SIERRA"]]
    assert island_stranded == ["BASE", "KILO", "MIKE", "NOVA", "OSCAR", "PAPA", "QUEBEC"]

    # An empty mesh mentions nobody, so every base is off-mesh.
    for mesh, sign in (({}, "BASE"), (LINKS, "TANGO")):
        try:
            broadcast_roster(mesh, sign)
        except ValueError as error:
            assert "is not on this mesh" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
```

Four words you need before you start.

**Queue.** A queue is a line at a counter. Things join at the back and leave
from the front — first in, first served. That order is the whole reason this
works: relays leave the queue in the order they were reached, so hop 1 is
fully dealt with before hop 2 starts.

**`deque`.** `collections.deque` is Python's queue. `append` puts something
on the back and `popleft` takes one off the front, and both are fast no
matter how long the queue is. A plain list can do the same job with
`pop(0)`, and Exercise 4 shows you exactly what that costs.

**Reached set.** A `set` of the call-signs already spoken for. Checking "is
this one in the set?" is instant however big the set gets. Mark a relay the
moment you put it in the queue, not when you take it out — the difference is
the single most common BFS bug and the *Common bugs* section shows what it
looks like.

**Snapshot.** `for _ in range(len(queue))` measures the queue **once**,
before the body runs. Inside the body the queue grows. Because the count was
taken first, the loop still stops after exactly one hop's worth. That one
line is the whole trick on this page.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/exercises/exercise-01-relay-roster.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `every_sign` returns a `set` holding every call-sign in the mesh, whether
   it appears as a key, in a listener list, or in both.
2. `broadcast_roster` returns a **tuple** of two things: the hops, and the
   stranded list.
3. Hop 0 is `[base]` and nothing else, every time.
4. Each hop is sorted A to Z. The order relays came off the queue in is not
   the order they are printed in.
5. No call-sign appears in two hops, and none appears twice in one hop.
6. The stranded list holds every mentioned call-sign the broadcast never
   reached, sorted A to Z. It is `[]` when the broadcast reaches everybody.
7. A `base` the mesh does not mention raises `ValueError` whose message
   contains `is not on this mesh`.
8. Both functions keep their type hints and their docstrings.

## Constraints

- **Use `collections.deque`, not a list.** `deque.popleft()` takes the front
  item and leaves everything else where it is. `list.pop(0)` slides every
  remaining item one place left, so a queue of ten thousand costs ten
  thousand slides per removal. This mesh has nine relays and you would never
  feel it — but the habit is what you are building here, and Exercise 4 puts
  a number on it.

- **Mark a relay as reached when you *add* it to the queue.** Not when you
  take it off. OSCAR can hear both KILO and MIKE, and both are in hop 1. If
  you only mark on the way out, KILO puts OSCAR in the queue, MIKE puts it in
  again before either copy is dealt with, and OSCAR turns up twice in hop 2.

- **Take the snapshot before you pop anything.**
  `for _ in range(len(queue))` reads the length once and then counts down.
  Writing `while queue:` inside instead would drain hop 2 and hop 3 into the
  same hop, because they get added while you are still going.

- **Read `links` with `.get(sign, ())`, not `links[sign]`.** SIERRA appears
  in ROMEO's list. Whether SIERRA is also a key of `links` is up to whoever
  typed the mesh in, and on a real network somebody will eventually forget.
  `links[sign]` raises `KeyError` on that relay; `.get(sign, ())` treats it
  as a relay that nobody can hear, which is exactly what the missing entry
  means.

- **Sort each hop when the hop is finished, not as you go.** Collect the
  call-signs first, then `sorted(...)` once. Inserting into a sorted list one
  item at a time does the same work several times over, and it hides the
  structure: a hop is a batch, and it is sorted because it is a batch.

- **`every_sign` returns a set, not a list.** You subtract with it —
  `signs - reached` — and set subtraction is one operation. Doing the same
  thing with a list means scanning `reached` once per call-sign.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
@@OUTPUT@@
```

Look at hop 2. NOVA, OSCAR and PAPA are printed alphabetically, but they did
not arrive that way — KILO contributed NOVA and OSCAR, then MIKE contributed
PAPA and tried to contribute OSCAR a second time. The single copy of OSCAR
is the reached set doing its job.

And notice who is *not* in hop 3 or later: BASE. NOVA can hear BASE, so there
is a link pointing back at it, but BASE was reached at hop 0 and never gets a
second turn.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-relay-roster.py`. It fails on the first line that uses
   a result. That is the correct starting point — it proves the self-check is
   real.
2. Fill in `every_sign` first and check it by hand in a REPL. `LINKS` has
   nine keys and no listener that is not also a key, so the answer is nine
   call-signs. If you get eight or ten, fix that before going near the queue.
3. Write the loop with the snapshot but **no sorting** yet, and print each
   hop as it is built. Read the raw order. That order is what a queue gives
   you and it is worth seeing once.
4. Add the sort. The printed table should now match the expected output line
   for line.
5. Work out the stranded list. It is one line: subtract `reached` from the
   set `every_sign` gave you, and sort the result.
6. Add the `ValueError`. Run once with `base="TANGO"` on purpose and read the
   message you wrote — a message that does not say which call-sign was wrong
   is a message you will curse at midnight.
7. When `All checks passed.` prints, open `python -i exercise-01-relay-roster.py`
   and broadcast from every call-sign in turn. Two of the nine reach almost
   nobody. Work out why before you look.

## The Solution

```python
@@CODE@@
```

**The snapshot is the whole algorithm.**

```python
for _ in range(len(queue)):
```

`range(len(queue))` is worked out **once**, before the first pop. Say the
queue holds KILO and MIKE, so the range is `range(2)`. Inside the body those
two get popped and four more get appended — but the range was already fixed
at two, so the loop stops. Everything appended during the hop waits for the
next turn round the outer `while`. That is what makes a hop a hop.

Try writing it the other way and you can feel the bug: if the inner loop were
`while queue:` the whole mesh would collapse into one enormous hop, because
you would keep going as long as anything was in the queue, which is forever
until the network runs out.

**The reached set is marked at the door, not at the counter.**

```python
if listener not in reached:
    reached.add(listener)
    queue.append(listener)
```

Those three lines always travel together. OSCAR can hear KILO and OSCAR can
hear MIKE, and both are in hop 1. KILO reaches OSCAR, so OSCAR is marked and
queued. MIKE then checks, finds OSCAR already marked, and moves on. Move the
`reached.add` down to where the sign comes *off* the queue and OSCAR is in
the queue twice before either copy is looked at — so it appears twice in hop
2, and so does everything downstream of it.

**Hop 0 is not a special case, and that is deliberate.** The queue starts
holding exactly one thing, so the first turn of the outer loop pops one
thing, sorts a one-item list, and appends `[base]`. There is no
`if is_first_hop` anywhere, and there does not need to be. Seeding the queue
correctly is how you avoid special cases in the body — a habit that pays off
properly in Exercise 3, where the queue starts with several things in it and
nothing else changes at all.

**`links.get(sign, ())` is the difference between a program and a demo.**
The mesh is data somebody typed. A relay mentioned in a list but missing as a
key is not an error in the mesh — it is a relay that nobody can hear, which
is an ordinary thing for a relay to be. `.get` says that. `links[sign]` says
"the mesh is malformed", which is a different and wrong claim.

**Stranded is a set subtraction, and it has to be.** `signs - reached` asks
"who is mentioned and was not reached", in one step, without a loop. This is
also why `every_sign` hands back a set rather than a list: the subtraction
is the reason the set exists.

**The empty mesh needs no special code either.** `every_sign({})` is the
empty set, `base` is not in it, and the `ValueError` fires. One check covers
both "the mesh is empty" and "you typed the call-sign wrong", because from
the mesh's point of view those are the same thing.

## Download and run

Download
[exercise-01-relay-roster-solution.py](./exercise-01-relay-roster-solution.py)
and run it:

```bash
python exercise-01-relay-roster-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-relay-roster.py`.

## Common bugs to catch

- **`AttributeError: 'list' object has no attribute 'popleft'`.** You wrote
  `queue = [base]` and then reached for `popleft`:

  ```text
  Traceback (most recent call last):
      queue.popleft()
      ^^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  A list is not a queue; it is a list that can be used as one, badly. Import
  `deque` and seed it with `deque([base])`. The mirror-image mistake gets you
  `TypeError: deque.pop() takes no arguments (1 given)` — that is a `deque`
  being asked for `pop(0)`, which it refuses on purpose.

- **`KeyError: 'KILO'`.** You read the mesh with `links[sign]`:

  ```text
  Traceback (most recent call last):
      for x in links["KILO"]:
               ~~~~~^^^^^^^^
  KeyError: 'KILO'
  ```

  In `LINKS` every listener happens to be a key too, so this one hides until
  you edit the data. Add `"BASE": ["TANGO"]` to the mesh and it fires on the
  first run. Use `.get(sign, ())`.

- **OSCAR appears twice in hop 2.** No exception, just a wrong roster:

  ```text
  hop 2: NOVA, OSCAR, OSCAR, PAPA
  ```

  You moved `reached.add(...)` to the moment a call-sign comes *off* the
  queue. Both KILO and MIKE reach OSCAR, and with the marking done late both
  copies get queued. Put the `add` immediately after the `not in` check,
  where the solution has it.

- **Every relay lands in hop 1.** Also no exception:

  ```text
  hop 0: BASE
  hop 1: KILO, MIKE, NOVA, OSCAR, PAPA, QUEBEC
  ```

  Your inner loop is `while queue:` instead of `for _ in range(len(queue))`.
  It keeps consuming everything appended during the hop, so all the hops run
  together into one. The snapshot is what separates them.

- **`stranded` comes back holding QUEBEC.** You built the "mentioned"
  collection from `links.keys()` only, or you subtracted the wrong way round.
  Print `every_sign(LINKS)` and `reached` side by side; one of them is not
  what you think it is.

- **`TypeError: unhashable type: 'list'`.** You tried to put a hop into the
  reached set instead of a call-sign:

  ```text
  Traceback (most recent call last):
      seen.add([0, 1])
      ~~~~~~~~^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  A set can only hold things that cannot change underneath it. Strings and
  tuples can go in; lists cannot. You want `reached.add(listener)`, one
  call-sign at a time.

## Under the hood

<details>
<summary>Under the hood — why the hops really are shortest distances, and what it costs</summary>

**The claim.** The hop a relay lands in is the smallest number of repeats it
could possibly take to reach it. Not "a" number of repeats — the smallest.

**Why.** The queue only ever holds relays from two neighbouring hops: some of
hop `k` still waiting, then some of hop `k + 1` just added. It can never hold
hop `k + 2` while hop `k` is still in there, because hop `k + 2` only gets
added while hop `k + 1` is being dealt with, which only starts once hop `k`
is gone. So relays come off the queue in non-decreasing hop order, and the
first time you reach a relay is the earliest anybody could.

That is the entire proof, and it is worth being able to say it in one
sentence out loud: *the queue never holds two hops that are more than one
apart, so the first time you see a relay is the soonest it could be seen.*

Notice what the argument uses: every step counts the same. One repeat is one
repeat. The moment repeats have different costs — one relay is slow, another
is fast — the argument collapses, and you need a different algorithm. That is
Dijkstra's, and it belongs to a later course. The one-line test is: *are all
my steps the same size?* If yes, this works. If no, it does not.

**What it costs.** Call the number of relays `R` and the number of "can hear"
entries `L`. Every relay joins the queue at most once, because the reached
set says so, so there are at most `R` pops. Every entry in every list is
looked at at most once, when its transmitter is popped, so that is `L` looks.
Total work is `O(R + L)` — linear in the size of the mesh. There is no way to
do better, because you have to at least read the mesh.

The sorting is on top of that. Each hop is sorted once, and the hops together
hold at most `R` call-signs, so the sorting adds `O(R log R)` in the worst
case — one enormous hop. It is not the algorithm; it is the presentation.

**Memory.** The reached set holds up to `R` call-signs. The queue holds at
most one hop plus part of the next, which for a wide flat mesh is also close
to `R`. So `O(R)`.

**The other way to do it.** Instead of a snapshot you can put the hop number
on the queue alongside the call-sign — `queue.append((listener, hop + 1))` —
and group afterwards. Both are correct. The snapshot is better when the
answer is *per hop*, because the hop is already a batch you can sum, sort or
count. The pair is better when the answer is *per relay*, because then you
want the number attached to the relay and never need the batch. Exercise 2
uses the pair for exactly that reason. Say out loud which one you picked and
why; interviewers ask.

</details>

## Acceptance checklist

- [ ] `python exercise-01-relay-roster.py` prints four hop lines, the
      stranded line, then `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] `collections.deque` is imported and used; no `pop(0)` anywhere.
- [ ] The reached set is added to at the same moment the queue is appended
      to — same `if`, adjacent lines.
- [ ] The inner loop is `for _ in range(len(queue))`, with the length read
      before any popping.
- [ ] The mesh is read with `.get`, never with `[...]`.
- [ ] `broadcast_roster(LINKS, "TANGO")` raises `ValueError` and the message
      names TANGO.
- [ ] Both functions have type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 exercise 1: relay roster`.

## Stretch

- **Report the hop each relay landed in, instead of the roster.** Same walk,
  the other output shape.

  ```python
  def hop_of(links: dict[str, list[str]], base: str) -> dict[str, int]:
      """Return the hop each reachable relay lands in."""
      hops, _ = broadcast_roster(links, base)
      return {sign: number for number, roster in enumerate(hops) for sign in roster}
  ```

  ```text
  {'BASE': 0, 'KILO': 1, 'MIKE': 1, 'NOVA': 2, 'OSCAR': 2, 'PAPA': 2, 'QUEBEC': 3}
  ```

  Note that this builds the dict *from* the roster rather than re-walking the
  mesh. One walk, two shapes of answer.

- **Find the mesh's weakest relay.** Which single relay, taken off the air,
  strands the most others?

  ```python
  def worst_to_lose(links: dict[str, list[str]], base: str) -> tuple[str, int]:
      """Return the relay whose loss strands the most others, and how many."""
      losses = {}
      for gone in every_sign(links) - {base}:
          thinned = {
              sign: [s for s in heard if s != gone]
              for sign, heard in links.items()
              if sign != gone
          }
          _, stranded = broadcast_roster(thinned, base)
          losses[gone] = len(stranded)
      return max(losses.items(), key=lambda pair: (pair[1], pair[0]))
  ```

  ```text
  ('OSCAR', 3)
  ```

  Three, not more: ROMEO and SIERRA were stranded already, and losing OSCAR
  takes QUEBEC with it. KILO ties on three — it takes NOVA — and the tie-break
  in the `key` picks the later name so the answer is stable. Notice that
  losing KILO does *not* cost you OSCAR, because MIKE reaches OSCAR too. That
  is what redundancy looks like, and it is a real question network engineers
  ask. The answer is just "run the same walk once per relay".

- **Broadcast from two bases at once.** Change one line — the seed — and
  nothing else.

  ```python
  queue = deque(bases)
  reached = set(bases)
  ```

  ```text
  hop 0: BASE, ROMEO
  hop 1: KILO, MIKE, SIERRA
  hop 2: NOVA, OSCAR, PAPA
  hop 3: QUEBEC
  stranded:
  ```

  Hop 0 now holds two call-signs, nobody is stranded any more, and the rest
  of the loop does not care.
  Hold on to that: it is the entire content of Exercise 3.

When your roster is right, move on to
[Exercise 2 — Hoist Route](./exercise-02-hoist-route.md).
