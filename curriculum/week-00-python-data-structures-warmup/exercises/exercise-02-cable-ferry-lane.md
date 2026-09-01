# Exercise 2 — The Cable Ferry's Waiting Lane

> **Topic:** why taking from the front of a list is expensive, and what `collections.deque` does instead
> **Lecture:** [02 — Lists, Tuples and the Dynamic Array](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** every queue you will write for the rest of this course — every breadth-first search, every scheduler, every "process these in order" loop — takes from the front. Written with a list, that one line quietly turns a linear algorithm into a quadratic one. Interviewers watch for this specific line. Get the habit now, while the queue is seven cars long and you can see it.

## The Brief

A cable ferry crosses a river on a chain. It takes three vehicles at a time,
and there is a single waiting lane on the bank leading down to the ramp.

Two things happen in that lane:

- A normal vehicle **joins the back**.
- An emergency vehicle — ambulance, fire engine — is waved **to the front**.

When the ferry docks, it takes whoever is nearest the ramp, up to three, and
casts off. If nobody is waiting it does not sail at all.

Now think about how you would hold that lane in memory. The obvious answer is
a list, and the obvious answer is the wrong one. **A list is a row of boxes,
side by side, in one block of memory.** Taking the item out of box zero does
not leave a hole — Python slides every remaining item down one box, so that
box zero is box zero again. With three cars that is two slides. With a hundred
thousand cars it is ninety-nine thousand nine hundred and ninety-nine slides,
for one car.

```python
lane = ["van-11", "car-02", "bus-07"]
lane.pop(0)          # "van-11" leaves, and the other two shuffle up
```

Waving a vehicle to the front is the same problem backwards: `lane.insert(0,
plate)` has to shove everything up one box to make room.

A **deque** — say "deck", short for double-ended queue — is built for exactly
this. Instead of one long row of boxes it keeps a chain of small blocks, and it
remembers where both ends are. Adding or removing at either end moves nothing.
What it gives up is the middle: `lane[4]` on a deque has to walk, where on a
list it is instant.

Your job is the lane and the boarding rule.

## Starter

Create `exercise-02-cable-ferry-lane.py` in your practice folder and paste this
in. Fill in every `TODO`.

```python
"""exercise-02-cable-ferry-lane.py — the cable ferry's waiting lane.

Vehicles join the lane at the back. Emergency vehicles join at the front.
The ferry takes whoever is nearest the ramp, up to a deck limit.

Both ends of the lane are busy, so the lane is a deque and never a list.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque

DECK = 3

ARRIVALS: list[tuple[str, bool]] = [
    ("van-11", False),
    ("car-02", False),
    ("bus-07", False),
    ("ambulance-1", True),
    ("car-19", False),
    ("car-33", False),
    ("fire-4", True),
]


def board(lane: deque[str], vehicle: str, urgent: bool) -> None:
    """Put one vehicle into the lane.

    Args:
        lane: The waiting lane, front of the lane at index 0.
        vehicle: The vehicle's plate.
        urgent: True for an emergency vehicle, which goes to the front.

    Returns:
        None. The lane is changed in place, on purpose.
    """
    # TODO: appendleft for urgent, append for everyone else. Return nothing.
    ...


def next_crossing(lane: deque[str], deck: int) -> list[str]:
    """Take the next boatload off the front of the lane."""
    # TODO: popleft until the boat is full or the lane is empty
    ...


def run_ferry(arrivals: list[tuple[str, bool]], deck: int) -> list[list[str]]:
    """Board every arrival, then sail until the lane is clear."""
    # TODO: build a deque, board everyone, then sail until nobody is left
    ...


# ---- Self-check ----
if __name__ == "__main__":
    sailings = run_ferry(ARRIVALS, DECK)
    for number, manifest in enumerate(sailings, 1):
        print(f"crossing {number}: {', '.join(manifest)}")
    print(f"lane empty after {len(sailings)} crossings")

    assert sailings[0] == ["fire-4", "ambulance-1", "van-11"]
    assert sailings[1] == ["car-02", "bus-07", "car-19"]
    assert sailings[2] == ["car-33"]
    assert len(sailings) == 3
    assert run_ferry([], DECK) == []
    assert next_crossing(deque(), DECK) == []
    assert len(ARRIVALS) == 7  # the arrivals log is untouched
    print("All checks passed.")
```

Three things you need before you start.

**A deque has four end methods.** `append` and `pop` work on the right-hand
end, exactly like a list. `appendleft` and `popleft` work on the left-hand end,
which a list has no cheap way to do at all. All four move nothing.

**`while lane:`** is true while the deque still holds something. An empty
deque, like an empty list, is false. This is how you avoid asking an empty lane
for a vehicle.

**Two urgent vehicles.** `fire-4` arrives last and goes in front of
`ambulance-1`, who was already at the front. That is what "wave it to the
front" means, and it is what the expected output shows. If your first crossing
starts with `ambulance-1`, you appended the second emergency vehicle to the
wrong end.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/exercises/exercise-02-cable-ferry-lane.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `board` puts an urgent vehicle at the **front** and everyone else at the
   **back**, and returns `None`.
2. `next_crossing` removes and returns up to `deck` plates from the front, in
   order. Those vehicles are gone from the lane afterwards.
3. `next_crossing` on an empty lane returns `[]` and does not raise.
4. `run_ferry` boards every arrival in order, then sails repeatedly until the
   lane is empty, and returns one manifest per crossing.
5. `run_ferry([], 3)` returns `[]` — an empty lane means no crossings at all,
   not one empty crossing.
6. The lane is a `collections.deque`. `pop(0)` and `insert(0, …)` appear
   nowhere in your solution.
7. Every function keeps its type hints and its docstring.

## Constraints

- **The lane is a `deque`, not a list.** Both ends are busy in this problem —
  emergency vehicles join at the front, the ferry takes from the front, normal
  vehicles join at the back. A list is cheap at one end only. This is the whole
  reason the exercise exists, so a list solution that passes the asserts still
  fails the exercise.

- **Never `lane.pop(0)`.** Removing the front of a list moves every remaining
  item down one slot, which is `O(n)`. Do it once per vehicle and the whole
  ferry day becomes `O(n²)`. `popleft()` on a deque moves nothing and is
  `O(1)`.

- **Never `lane.insert(0, plate)`.** Same cost, same reason, opposite
  direction: making room at the front shoves everything up one slot.
  `appendleft` does not.

- **`board` returns `None` and changes the lane in place.** That is unusual in
  this course — Exercise 1 was careful never to change what it was given — and
  it is deliberate here, because a waiting lane is a real thing with one
  identity. If `board` handed back a new lane, the caller would have to
  remember to keep it, and the day they forgot, vehicles would vanish. Say the
  rule out loud: **a function either returns a new thing or changes the thing
  it was given, and its name should tell you which.**

- **At most 200 vehicles in a day.** A cable ferry running a small river
  crossing does around sixty crossings in a day at three vehicles each. The
  bound is honest rather than convenient, and it is small enough that a list
  version would also finish instantly — which is the point. You are not
  choosing the deque because this input is big. You are choosing it because the
  same line, in Week 6's breadth-first search, will be handed a queue with a
  hundred thousand nodes in it.

- **The deck limit is at least 1.** A ferry that carries nothing would loop
  forever in `run_ferry`, taking no vehicles and never emptying the lane. Worth
  noticing: this is the only input that could hang the program, and it is
  excluded by the physical facts of the problem rather than by a guard.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-cable-ferry-lane.py
crossing 1: fire-4, ambulance-1, van-11
crossing 2: car-02, bus-07, car-19
crossing 3: car-33
lane empty after 3 crossings
All checks passed.
```

Read the first crossing carefully. `fire-4` was the **last** arrival of the day
and it sails first, because it went in front of `ambulance-1`, who had already
gone in front of everybody else. Then `van-11`, who had been waiting longest of
the ordinary vehicles. If your output starts `ambulance-1, fire-4`, your urgent
vehicles are queueing politely behind each other instead of jumping the whole
lane.

## Steps

1. Create the file, paste the starter, and run it. It fails immediately — the
   self-check tries to loop over `None`.
2. Write `board` first. It is four lines and an `if`. Run the file again: it
   still fails, but now on `next_crossing`.
3. Write `next_crossing`. Use `while lane and len(manifest) < deck:`. Both
   halves matter — the first stops you asking an empty lane for a vehicle, the
   second stops you emptying the whole lane onto one boat.
4. Write `run_ferry`. Board everyone in a loop, then sail in a second loop
   while the lane is not empty.
5. Run it and compare the three crossings against the expected output line for
   line before you read the asserts.
6. Now break it on purpose. Change the lane from `deque()` to `[]` and swap
   `popleft()` for `pop(0)` and `appendleft(x)` for `insert(0, x)`. The asserts
   still pass. Sit with that for a moment: **the wrong data structure gives the
   right answer.** The only thing that changed is the cost, which is why you
   have to be able to argue about cost rather than test for it.
7. Put the deque back.

## The Solution

```python
"""exercise-02-cable-ferry-lane-solution.py — the cable ferry's waiting lane.

Vehicles join the lane at the back. Emergency vehicles join at the front.
The ferry takes whoever is nearest the ramp, up to a deck limit, and comes
back for the rest.

Both ends of the lane are busy, so the lane is a deque and never a list.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

DECK = 3

ARRIVALS: list[tuple[str, bool]] = [
    ("van-11", False),
    ("car-02", False),
    ("bus-07", False),
    ("ambulance-1", True),
    ("car-19", False),
    ("car-33", False),
    ("fire-4", True),
]


def board(lane: deque[str], vehicle: str, urgent: bool) -> None:
    """Put one vehicle into the lane.

    Args:
        lane: The waiting lane, front of the lane at index 0.
        vehicle: The vehicle's plate.
        urgent: True for an emergency vehicle, which goes to the front.

    Returns:
        None. The lane is changed in place, on purpose.
    """
    if urgent:
        lane.appendleft(vehicle)
    else:
        lane.append(vehicle)


def next_crossing(lane: deque[str], deck: int) -> list[str]:
    """Take the next boatload off the front of the lane.

    Args:
        lane: The waiting lane. The vehicles taken are removed from it.
        deck: How many vehicles fit on the deck.

    Returns:
        Up to `deck` plates, nearest the ramp first. An empty list when the
        lane is already empty — the ferry does not sail empty.
    """
    manifest: list[str] = []
    while lane and len(manifest) < deck:
        manifest.append(lane.popleft())
    return manifest


def run_ferry(arrivals: list[tuple[str, bool]], deck: int) -> list[list[str]]:
    """Board every arrival, then sail until the lane is clear.

    Args:
        arrivals: (plate, urgent) pairs in the order they reached the slip.
        deck: How many vehicles fit on the deck.

    Returns:
        One manifest per crossing, in sailing order. Empty when nobody came.
    """
    lane: deque[str] = deque()
    for vehicle, urgent in arrivals:
        board(lane, vehicle, urgent)

    crossings: list[list[str]] = []
    while lane:
        crossings.append(next_crossing(lane, deck))
    return crossings


# ---- Self-check ----
if __name__ == "__main__":
    sailings = run_ferry(ARRIVALS, DECK)
    for number, manifest in enumerate(sailings, 1):
        print(f"crossing {number}: {', '.join(manifest)}")
    print(f"lane empty after {len(sailings)} crossings")

    assert sailings[0] == ["fire-4", "ambulance-1", "van-11"]
    assert sailings[1] == ["car-02", "bus-07", "car-19"]
    assert sailings[2] == ["car-33"]
    assert len(sailings) == 3
    assert run_ferry([], DECK) == []
    assert next_crossing(deque(), DECK) == []
    assert len(ARRIVALS) == 7  # the arrivals log is untouched
    print("All checks passed.")
```

**`board` is an `if` and two method calls, and the whole design is in which
two.**

```python
if urgent:
    lane.appendleft(vehicle)
else:
    lane.append(vehicle)
```

`appendleft` is the operation a list does not have. You can *simulate* it with
`insert(0, x)`, and people do, and that simulation is the bug. The deque has a
pointer to its left-hand end; putting something there is a couple of
assignments, no matter how long the lane is.

**`next_crossing` has two stopping conditions and needs both.**

```python
while lane and len(manifest) < deck:
```

Drop the first and an empty lane raises `IndexError: pop from an empty deque`.
Drop the second and the first crossing takes the entire queue. Loops that take
"up to n of whatever is left" almost always need this exact pair, and writing
them as one condition each time is how you stop thinking about it.

**`run_ferry` boards everybody and then sails.** That is a simplification of a
real ferry day, where arrivals and crossings interleave, and it is a
simplification the problem chose deliberately: it keeps the two behaviours you
are learning — boarding order and taking order — separate enough to test one at
a time. The stretch section interleaves them.

**The lane empties, so the second loop ends.** `while lane:` is true while the
deque holds something, and every pass removes at least one vehicle, as long as
`deck` is at least 1. That "at least one" is the termination argument, and
being able to say it out loud in one sentence is a habit that pays from Week 6
onwards, where the same shape of loop walks a graph and a missing "at least
one" runs forever.

**Why `list(ring)` never appears here.** Each manifest is built as a plain list
because that is what the caller wants — a small fixed group of names to print
or to load. The lane stays a deque for its whole life. Converting between the
two is `O(n)`, so a program that converts inside a loop has quietly paid for
the list it was trying to avoid.

## Download and run

Download
[exercise-02-cable-ferry-lane-solution.py](./exercise-02-cable-ferry-lane-solution.py)
and run it:

```bash
python exercise-02-cable-ferry-lane-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-cable-ferry-lane.py`.

## Common bugs to catch

- **`AttributeError: 'list' object has no attribute 'popleft'`.** Your lane is
  still a list:

  ```text
  Traceback (most recent call last):
      manifest.append(lane.popleft())
                      ^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  This is the friendly version of the bug, because it stops you. The unfriendly
  version is writing `lane.pop(0)` instead, which works perfectly and is
  quadratic. There is no exception for that one — only the argument.

- **`IndexError: pop from an empty deque`.** You took from the lane without
  checking there was anything in it:

  ```text
  Traceback (most recent call last):
      manifest.append(lane.popleft())
                      ^^^^^^^^^^^^^^
  IndexError: pop from an empty deque
  ```

  Add the `while lane and …` guard. Note the wording — a list raises
  `IndexError: pop from empty list`, a deque says `deque`. When a traceback
  names a type you did not expect, that is information.

- **`TypeError: 'NoneType' object is not iterable`.** You returned the result of
  an in-place method:

  ```text
  Traceback (most recent call last):
      for number, manifest in enumerate(sailings, 1):
                              ^^^^^^^^^^^^^^^^^^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  `lane.append(x)` and `lane.appendleft(x)` both return `None`, because they
  change the lane rather than build a new one. `return lane.appendleft(v)`
  therefore returns nothing at all. The same trap catches people with
  `list.sort()` and `list.reverse()`.

- **`TypeError: sequence index must be integer, not 'slice'`.** You tried to
  slice the lane:

  ```text
  Traceback (most recent call last):
      manifest = lane[:deck]
                 ^^^^^^^^^^^
  TypeError: sequence index must be integer, not 'slice'
  ```

  A deque does not support slicing, and that is not an oversight. Slicing needs
  the items to be in one contiguous row; a deque's whole trick is that they are
  not. If you genuinely need a slice, you have chosen the wrong container for
  the job — or you want `itertools.islice`, which walks instead of copying.

- **The first crossing is `ambulance-1, fire-4, van-11`.** Both emergency
  vehicles went to the front, but you kept a separate list of them and put it
  in front at the end, so they came out in arrival order. The rule is that each
  urgent vehicle jumps to the front **at the moment it arrives**, which puts the
  later one ahead. Two rules that sound identical in English and are not: this
  is why the expected output has two of them.

- **`run_ferry([], 3)` returns `[[]]`.** You used a `do…while` shape — sail
  once, then check. Python has no `do…while`, so this shows up as sailing
  before the loop or as a `while True` with a `break` in the middle. Check
  first: `while lane:`.

## Under the hood

<details>
<summary>Under the hood — what a deque is made of, and what it costs you</summary>

**A list is one row. A deque is a chain of rows.**

CPython's `list` is a single block of pointers with spare room at the end.
That is why `append` is cheap and the front is not: there is nowhere to grow at
the left, and removing at the left leaves a hole that has to be closed by
moving everything.

`collections.deque` is a **doubly linked list of blocks**, each block holding
64 pointers. The deque remembers the first block and the last block. Adding at
either end writes into the spare room of the end block, or links a fresh block
on. Nothing else moves. Removing is the same in reverse.

| Operation | `list` | `deque` |
|---|---|---|
| `append` / `pop()` | `O(1)` amortised | `O(1)` |
| `appendleft` / `popleft` | `O(n)` (as `insert(0,…)` / `pop(0)`) | `O(1)` |
| `x[i]` in the middle | `O(1)` | `O(n)` |
| `x[a:b]` | `O(b - a)` | not supported |

**The trade is random access, and it is a real trade.** To reach item 500 of a
deque, Python walks the block chain from whichever end is nearer. On a list
that is one multiplication and one memory read. So the rule is not "deques are
better". The rule is: **cheap at both ends, expensive in the middle — pick the
one that matches what your loop actually does.**

**`maxlen` is the other reason to reach for a deque.** `deque(maxlen=5)` keeps
the last five things and silently drops the oldest as new ones arrive, which is
a sliding window of fixed size in one argument. The stretch tries it.

**Why interviewers care about `pop(0)`.** Breadth-first search visits every
node once and takes each one off the front of a queue. With a deque that is
`O(V + E)` — the textbook cost. With a list it is `O(V²  + E)`, because every
one of the `V` removals shifts the rest of the queue. The algorithm is
identical; the line that reads `queue.pop(0)` is the entire difference, and it
is one of the most reliably-spotted mistakes in a technical interview. Week 6
is built on this.

</details>

## Acceptance checklist

- [ ] `python exercise-02-cable-ferry-lane.py` prints three crossings, the
      empty-lane line, then `All checks passed.`
- [ ] The first crossing starts with `fire-4`.
- [ ] The lane is a `deque`; `pop(0)` and `insert(0, …)` appear nowhere.
- [ ] `next_crossing` on an empty lane returns `[]` without raising.
- [ ] `run_ferry([], 3)` returns `[]`, not `[[]]`.
- [ ] `board` returns `None` and you can say why.
- [ ] You can state, in one sentence, what a deque gives up to be fast at both
      ends.

## Stretch

- **Let arrivals and crossings interleave.** A vehicle that turns up while the
  ferry is mid-river waits for the next one.

  ```python
  def run_ferry_live(arrivals: list[tuple[str, bool]], deck: int, gap: int) -> list[list[str]]:
      """Sail after every `gap` arrivals, then clear whatever is left."""
      lane: deque[str] = deque()
      crossings: list[list[str]] = []
      for index, (vehicle, urgent) in enumerate(arrivals, 1):
          board(lane, vehicle, urgent)
          if index % gap == 0:
              crossings.append(next_crossing(lane, deck))
      while lane:
          crossings.append(next_crossing(lane, deck))
      return crossings
  ```

  ```text
  crossing 1: van-11, car-02, bus-07
  crossing 2: ambulance-1, car-19, car-33
  crossing 3: fire-4
  ```

  `fire-4` now sails **last**, on a boat of its own — it arrived after the
  final scheduled crossing had already cast off, so there was nobody left for
  it to jump ahead of. Same rule, different timing, an answer that looks like
  the opposite of the original. No line of `board` or `next_crossing` had to
  change, which is the sign that the rule and the schedule really were separate
  things.

- **Give the lane a length limit.**

  ```python
  short_lane: deque[str] = deque(maxlen=4)
  for plate in ["a", "b", "c", "d", "e", "f"]:
      short_lane.append(plate)
  print(list(short_lane))
  ```

  ```text
  ['c', 'd', 'e', 'f']
  ```

  A full `deque` with a `maxlen` drops from the far end to make room, without a
  word of complaint. That is either exactly what you want — the last four
  readings, the last four moves — or a silent data loss bug. Know which one you
  asked for.

- **Find out what a deque is bad at.**

  ```python
  lane = deque(["van-11", "car-02", "bus-07", "car-19", "car-33"])
  print(lane[2])
  lane.remove("bus-07")
  print(list(lane))
  ```

  ```text
  bus-07
  ['van-11', 'car-02', 'car-19', 'car-33']
  ```

  Both of those work, and both are `O(n)` — the middle index has to be walked
  to, and the removal has to be searched for and then closed up. A driver who
  gives up and leaves the queue is a real thing that happens, and it is the one
  operation this container has no answer for. If your problem is mostly
  middles, you wanted a list, or a dict, or something else entirely.

When your ferry runs, move on to
[Exercise 3 — The Community Garden's Plot Map](./exercise-03-garden-plot-map.md).
