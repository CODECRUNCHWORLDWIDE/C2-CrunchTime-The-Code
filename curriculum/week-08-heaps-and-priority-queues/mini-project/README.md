# Mini-Project — The Repair Café Desk

> Topic: every Week 8 idiom in one working system · Lecture: [1](../lecture-notes/01-heapq-and-top-k.md), [2](../lecture-notes/02-heap-of-tuples-and-k-closest.md), [3](../lecture-notes/03-two-heap-and-k-way-merge.md) · Difficulty: Medium-Hard · Target time: 10 hours across Thursday to Saturday · Why this one: the exercises drilled the idioms one at a time; this is the page where they have to work together, and where the seams between them are the thing being graded.

## The Brief

A repair café opens for one afternoon. One bench, three ways for a job to arrive,
and a queue that is emphatically **not** first-come-first-served.

Every idiom the week taught appears here doing real work rather than being
demonstrated:

- the three intake channels are stitched into one arrival ledger by a **k-way
  merge**, so the ledger is built without sorting anything;
- the desk is a **heap of tuples** — `(urgency, ticket)` — so equal urgencies are
  served in arrival order and two job records are never compared with each other;
- a job whose owner takes it home again is marked withdrawn rather than hunted
  for in the heap: **lazy deletion**;
- the end-of-day "who waited longest" table is a **max-heap by negation**,
  because `heapq` only ever hands back the smallest thing.

The deliverable is the running system **and** two FRAME write-ups on the two
idioms that carry it: the k-way merge that builds the ledger, and the two-part
queue — heap-of-tuples plus lazy deletion — that runs the bench. Those two are
what Mock #2 grades separately, and writing one of each forces you to say out
loud where they differ.

## Starter

`README-solution.py` sits beside this page: the whole day, from doors open to
doors shut, with its self-checks.

```text
opening minute    0
closing minute  180

walk-in    min   0  toaster         normal        25 min
           min  35  table lamp      when you can  15 min
           min  60  kettle          normal        20 min
           min  95  radio           when you can  30 min
phone      min  10  sewing machine  urgent        45 min
           min  35  hairdryer       normal        20 min
           min 110  fan heater      urgent        35 min
web form   min   5  bicycle wheel   when you can  40 min
           min  48  food mixer      normal        30 min
           min  72  laptop fan      urgent        25 min
           min 150  turntable       when you can  20 min

withdrawn  min  70  ticket 4        min 130  ticket 9
```

Two rules are the café's own and are not conventions. When two channels report
the same minute, **the person standing in the room is written down first**, then
the phone, then the web form. And the bench **finishes what it starts** — a job
that runs past closing time is not interrupted, but a job that could not be
started before closing is left for next week.

## Requirements

1. `stitch_arrivals(logs)` merges the three channels into one ledger in minute
   order, assigning ticket numbers as it goes.
2. `RepairDesk` offers `queue`, `withdraw`, `take_next`, `still_waiting`, and a
   `len()` that counts only jobs really still waiting.
3. `run_day(logs, withdrawals, opening, closing)` returns what was served, what
   was withdrawn, and what was left queued at closing.
4. `longest_waits(served, count)` returns the longest waits, longest first.
5. `bench_minutes(served, opening, closing)` returns minutes worked and idle.
6. Every job is accounted for: served plus withdrawn plus left queued equals the
   ledger.

### What you ship

Three files under `frame-writeups/c2-week-08/mini-project/`:

```
frame-writeups/c2-week-08/mini-project/
├── README.md                        ← overview, index, and the reflection
├── problem-01-arrival-ledger.md     ← the k-way merge write-up
└── problem-02-repair-desk.md        ← heap-of-tuples plus lazy deletion
```

Each write-up is 100–200 lines: the five FRAME sections plus a five-line
recognition memo at the top. The code belongs inside the Assemble section, not
in a separate file.

### The recognition memo

Five lines at the top of each write-up, written to be read in thirty seconds:

1. **The shape.** k-way merge / bounded top-k / heap of tuples / lazy deletion /
   two-heap statistic.
2. **What is in the heap**, exactly, and how big it gets.
3. **The invariant** — the size bound, the balance, or the tiebreaker.
4. **The alternative you rejected**, and the one-sentence reason.
5. **The cost**, both time and space, with the discriminator that decides it.

### Cross-references

The two write-ups have to be navigable as a pair, and the rubric grades that:

- The merge write-up says why the heap holds **one row per channel** and not the
  whole log, and points at the desk write-up for the case where the heap's
  contents are the queue itself.
- The desk write-up says why the tuple's middle element exists, and points back
  at the merge for a heap where every entry is unique by construction and no
  tiebreaker is needed.
- Both name the same rejected alternative — sort everything — and say why it is
  a different answer in each case.

### Rubric

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the shape and the invariant in five lines, without hedging. |
| Reason about options | Four to six bullets of algorithm before any code, with the rejected alternative named. |
| Assemble the solution | Idiomatic Python; `heapq` operations only; type hints throughout; the negation confined to the heap. |
| Measure it | A hand trace of at least one minute of the day, and one bug named and prevented. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off, and the improvement — for both write-ups, and they must not be the same paragraph twice. |

Twenty points per write-up, forty for the pair.

## Constraints

- **The heap never holds a `Job`.** `Job` is deliberately not orderable. The heap
  holds `(urgency, ticket)`; the records live in a dict beside it. This is the
  constraint the whole design turns on.
- **Withdrawal must not touch the heap.** Finding one entry inside a heap means
  looking at all of them, and removing it means rebuilding what is left. Write
  the ticket down instead; pay one skipped pop later.
- **`len()` must exclude withdrawn tickets**, even though they are still sitting
  in the heap. A count that includes them is the classic lazy-deletion bug and it
  is invisible until somebody reports it.
- **The merge holds one row per channel**, never a whole log.
- **Ties in the ledger break by channel precedence**, encoded, not assumed.
- **The bench finishes what it starts.** A job begun at minute 150 that needs 40
  minutes runs to 190, and the day's report says so.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README-solution.py
arrival ledger
  ticket  1  min   0  walk-in    toaster         normal       25 min
  ticket  2  min   5  web form   bicycle wheel   when you can 40 min
  ticket  3  min  10  phone      sewing machine  urgent       45 min
  ticket  4  min  35  walk-in    table lamp      when you can 15 min
  ticket  5  min  35  phone      hairdryer       normal       20 min
  ticket  6  min  48  web form   food mixer      normal       30 min
  ticket  7  min  60  walk-in    kettle          normal       20 min
  ticket  8  min  72  web form   laptop fan      urgent       25 min
  ticket  9  min  95  walk-in    radio           when you can 30 min
  ticket 10  min 110  phone      fan heater      urgent       35 min
  ticket 11  min 150  web form   turntable       when you can 20 min

bench log
  min   0- 25  ticket  1  toaster         waited   0 min
  min  25- 70  ticket  3  sewing machine  waited  15 min
  min  70- 90  ticket  5  hairdryer       waited  35 min
  min  90-115  ticket  8  laptop fan      waited  18 min
  min 115-150  ticket 10  fan heater      waited   5 min
  min 150-180  ticket  6  food mixer      waited 102 min

longest waits
  102 min  food mixer
   35 min  hairdryer
   18 min  laptop fan

jobs in    : 11
jobs fixed : 6
withdrawn  : ['table lamp', 'radio']
still queued at closing: ['kettle', 'bicycle wheel', 'turntable']
bench worked 180 of 180 minutes, idle 0
All checks passed.
```

The line to read is the food mixer: it waited **102 minutes** with an urgency of
"normal", while the fan heater arrived at minute 110 and waited five. That is not
a bug — it is the priority rule doing exactly what it was asked to do, and it is
the number the café would argue about. A report that does not surface it is not
telling the volunteers anything they can act on.

## Steps

1. Read the self-checks in the shipped file. They are the spec.
2. Write the two recognition memos **before** any code. If you cannot write them,
   you do not yet know which structure you are building.
3. Build `stitch_arrivals` and check the ledger by hand — eleven rows, tickets 1
   to 11, and the minute-35 tie resolving walk-in before phone.
4. Build `RepairDesk` with the tuple queue, then add withdrawal as lazy deletion.
   Get `len()` right at this point, not later.
5. Run the day. Check the accounting identity: served plus withdrawn plus
   leftover equals eleven.
6. Add `longest_waits` and `bench_minutes`.
7. Write both FRAME passes and the cross-references between them.

## The Solution

```python
"""repair_desk.py — a repair cafe's priority desk, from doors open to doors shut.

One bench, one afternoon, three ways for a job to arrive, and a queue that is
not first-come-first-served. Every Week 8 idiom appears here doing real work:

  * the three intake channels are stitched into one arrival ledger by a k-way
    merge, so the ledger is built without sorting anything;
  * the desk itself is a heap of (urgency, ticket) tuples, so equal urgencies
    are served in the order they arrived and two job records are never
    compared with each other;
  * a job whose owner takes it home again is marked withdrawn rather than
    hunted for in the heap — lazy deletion;
  * the end-of-day "who waited longest" table is a max-heap, built by storing
    minus the wait, because `heapq` only ever hands back the smallest thing.

Run it with no arguments. It prints the day's report.
"""

import heapq
from dataclasses import dataclass

# ---- The day ----
OPENING_MINUTE = 0
CLOSING_MINUTE = 180

# When two channels report the same minute, the person standing in the room is
# written down first, then the phone, then the web form. It is the desk's own
# rule and it is not alphabetical.
CHANNEL_ORDER: tuple[str, ...] = ("walk-in", "phone", "web form")

# (minute the job arrived, item, urgency 1 = most urgent, repair minutes)
CHANNEL_LOGS: dict[str, list[tuple[int, str, int, int]]] = {
    "walk-in": [
        (0, "toaster", 2, 25),
        (35, "table lamp", 3, 15),
        (60, "kettle", 2, 20),
        (95, "radio", 3, 30),
    ],
    "phone": [
        (10, "sewing machine", 1, 45),
        (35, "hairdryer", 2, 20),
        (110, "fan heater", 1, 35),
    ],
    "web form": [
        (5, "bicycle wheel", 3, 40),
        (48, "food mixer", 2, 30),
        (72, "laptop fan", 1, 25),
        (150, "turntable", 3, 20),
    ],
}

# (minute, ticket) — the owner came back for it before the bench got to it.
WITHDRAWALS: list[tuple[int, int]] = [(70, 4), (130, 9)]

URGENCY_WORD = {1: "urgent", 2: "normal", 3: "when you can"}


@dataclass
class Job:
    """One thing to fix. Deliberately not orderable: the heap never sees it."""

    ticket: int
    minute: int
    channel: str
    item: str
    urgency: int
    repair_minutes: int


@dataclass
class Served:
    """One finished job, with the numbers the end-of-day report needs."""

    job: Job
    started: int
    finished: int

    @property
    def waited(self) -> int:
        """Return how long the job sat in the queue before the bench took it."""
        return self.started - self.job.minute


def stitch_arrivals(logs: dict[str, list[tuple[int, str, int, int]]]) -> list[Job]:
    """Merge the channel logs into one arrival ledger and hand out tickets.

    Each channel's log is already in minute order, so the merge holds one
    pending arrival per channel — three entries — instead of sorting all
    eleven. Tickets are handed out in ledger order, which is what makes them
    a usable tiebreaker later.

    Args:
        logs: Channel name to (minute, item, urgency, repair minutes) rows,
            each list ascending by minute.

    Returns:
        Jobs in arrival order, ticket 1 first. Arrivals sharing a minute are
        ordered by CHANNEL_ORDER.
    """
    pending: list[tuple[int, int, str, int]] = []
    for rank, channel in enumerate(CHANNEL_ORDER):
        rows = logs.get(channel, [])
        if rows:
            pending.append((rows[0][0], rank, channel, 0))
    heapq.heapify(pending)

    ledger: list[Job] = []
    while pending:
        minute, rank, channel, position = heapq.heappop(pending)
        _, item, urgency, repair_minutes = logs[channel][position]
        ledger.append(
            Job(len(ledger) + 1, minute, channel, item, urgency, repair_minutes)
        )
        if position + 1 < len(logs[channel]):
            following = logs[channel][position + 1][0]
            heapq.heappush(pending, (following, rank, channel, position + 1))
    return ledger


class RepairDesk:
    """The waiting queue: most urgent first, ties to whoever arrived first."""

    def __init__(self) -> None:
        """Start with an empty queue and nothing withdrawn."""
        self._waiting: list[tuple[int, int]] = []
        self._jobs: dict[int, Job] = {}
        self._withdrawn: set[int] = set()

    def __len__(self) -> int:
        """Return how many jobs are really still waiting, stale ones excluded."""
        return len(self._waiting) - sum(
            1 for _, ticket in self._waiting if ticket in self._withdrawn
        )

    def queue(self, job: Job) -> None:
        """Add a job to the queue.

        Args:
            job: The job to wait its turn. Only its urgency and ticket go into
                the heap; the record itself is kept in a dict beside it.
        """
        self._jobs[job.ticket] = job
        heapq.heappush(self._waiting, (job.urgency, job.ticket))

    def withdraw(self, ticket: int) -> bool:
        """Mark a waiting job as taken home, without touching the heap.

        Finding one entry inside a heap means looking at all of them, and
        removing it means rebuilding what is left. Writing the ticket down
        instead costs nothing now and one skipped entry later.

        Args:
            ticket: The ticket to withdraw.

        Returns:
            True when the ticket was waiting, False when it was already served,
            already withdrawn, or never existed.
        """
        if ticket not in self._jobs or ticket in self._withdrawn:
            return False
        self._withdrawn.add(ticket)
        return True

    def take_next(self) -> Job | None:
        """Remove and return the job the bench should start next.

        Withdrawn tickets are skipped here, which is where lazy deletion is
        finally paid for: one pop each, once, and never more than once.

        Returns:
            The job, or None when nothing real is waiting.
        """
        while self._waiting:
            _, ticket = heapq.heappop(self._waiting)
            if ticket not in self._withdrawn:
                return self._jobs[ticket]
        return None

    def still_waiting(self) -> list[Job]:
        """Return the jobs that are still queued, in the order they would be taken.

        Returns:
            Jobs, most urgent first, ties by ticket. Withdrawn tickets are left
            out.
        """
        live = [entry for entry in self._waiting if entry[1] not in self._withdrawn]
        return [self._jobs[ticket] for _, ticket in sorted(live)]


def run_day(
    logs: dict[str, list[tuple[int, str, int, int]]],
    withdrawals: list[tuple[int, int]],
    opening: int,
    closing: int,
) -> tuple[list[Served], list[Job], list[Job]]:
    """Run the bench from opening to closing and report what happened.

    Args:
        logs: The channel logs.
        withdrawals: (minute, ticket) pairs. A withdrawal for a ticket that is
            already on the bench is ignored.
        opening: The first minute the bench can start work.
        closing: The last minute the bench can start work is `closing - 1`. A
            job already under way runs past closing; it is not abandoned.

    Returns:
        (served jobs in the order they were finished, jobs withdrawn before
        the bench reached them, jobs still queued when the doors shut).
    """
    ledger = stitch_arrivals(logs)
    arriving: dict[int, list[Job]] = {}
    for job in ledger:
        arriving.setdefault(job.minute, []).append(job)
    withdrawing: dict[int, list[int]] = {}
    for minute, ticket in withdrawals:
        withdrawing.setdefault(minute, []).append(ticket)

    desk = RepairDesk()
    served: list[Served] = []
    withdrawn: list[Job] = []
    by_ticket = {job.ticket: job for job in ledger}
    free_at = opening

    for minute in range(opening, closing):
        for job in arriving.get(minute, []):
            desk.queue(job)
        for ticket in withdrawing.get(minute, []):
            if desk.withdraw(ticket):
                withdrawn.append(by_ticket[ticket])
        if minute < free_at:
            continue
        job = desk.take_next()
        if job is None:
            continue
        free_at = minute + job.repair_minutes
        served.append(Served(job, minute, free_at))

    return served, withdrawn, desk.still_waiting()


def longest_waits(served: list[Served], count: int) -> list[tuple[int, str]]:
    """Return the jobs whose owners waited longest, longest first.

    `heapq` is a min-heap and there is no max-heap to reach for, so the wait is
    stored negated and negated again on the way out.

    Args:
        served: The finished jobs.
        count: How many rows the table should hold.

    Returns:
        (minutes waited, item) rows, longest wait first. Ties go to the lower
        ticket, which is the earlier arrival.
    """
    if count <= 0:
        return []
    board = [(-record.waited, record.job.ticket, record.job.item) for record in served]
    heapq.heapify(board)
    table = []
    while board and len(table) < count:
        stored, _, item = heapq.heappop(board)
        table.append((-stored, item))
    return table


def bench_minutes(served: list[Served], opening: int, closing: int) -> tuple[int, int]:
    """Return how many minutes the bench worked and how many it stood idle.

    Args:
        served: The finished jobs.
        opening: The minute the doors opened.
        closing: The minute the doors shut.

    Returns:
        (minutes worked inside opening hours, minutes idle inside them).
    """
    worked = sum(
        min(record.finished, closing) - record.started
        for record in served
        if record.started < closing
    )
    return worked, (closing - opening) - worked


def main() -> None:
    """Print the day's report."""
    ledger = stitch_arrivals(CHANNEL_LOGS)
    print("arrival ledger")
    for job in ledger:
        print(
            f"  ticket {job.ticket:2d}  min {job.minute:3d}  {job.channel:<9}"
            f"  {job.item:<15} {URGENCY_WORD[job.urgency]:<12} {job.repair_minutes} min"
        )

    served, withdrawn, leftover = run_day(
        CHANNEL_LOGS, WITHDRAWALS, OPENING_MINUTE, CLOSING_MINUTE
    )

    print()
    print("bench log")
    for record in served:
        print(
            f"  min {record.started:3d}-{record.finished:3d}  ticket"
            f" {record.job.ticket:2d}  {record.job.item:<15} waited {record.waited:3d} min"
        )

    print()
    print("longest waits")
    for waited, item in longest_waits(served, 3):
        print(f"  {waited:3d} min  {item}")

    print()
    worked, idle = bench_minutes(served, OPENING_MINUTE, CLOSING_MINUTE)
    print(f"jobs in    : {len(ledger)}")
    print(f"jobs fixed : {len(served)}")
    print(f"withdrawn  : {[job.item for job in withdrawn]}")
    print(f"still queued at closing: {[job.item for job in leftover]}")
    print(f"bench worked {worked} of {CLOSING_MINUTE - OPENING_MINUTE} minutes, idle {idle}")

    assert len(ledger) == 11
    assert [job.ticket for job in ledger] == list(range(1, 12))
    assert ledger[3].item == "table lamp" and ledger[4].item == "hairdryer"
    assert len(served) == 6
    assert served[0].job.item == "toaster" and served[0].waited == 0
    assert longest_waits(served, 3)[0] == (102, "food mixer")
    assert longest_waits(served, 0) == []
    assert [job.item for job in withdrawn] == ["table lamp", "radio"]
    assert [job.item for job in leftover] == ["kettle", "bicycle wheel", "turntable"]
    assert len(served) + len(withdrawn) + len(leftover) == len(ledger)
    print("All checks passed.")


if __name__ == "__main__":
    main()
```

The `Job` dataclass being unorderable is not an oversight to work around — it is
the safety property. If the heap can never reach a `Job`, then no amount of
ticket collision can produce the `TypeError` that
[Exercise 4](../exercises/exercise-04-rescue-intake-queue.md) demonstrates, and
the queue is correct by construction rather than by testing.

## Download and run

Download the solution beside this page and run it:

```bash
python README-solution.py
```

No third-party packages, no arguments, no input. It prints the arrival ledger,
the bench log, the longest waits, the day's accounting, and then
`All checks passed.`

## Common bugs to catch

- **Putting the `Job` in the heap.** Symptom: a `TypeError` between two `Job`
  records, on the first minute where two jobs share an urgency.
- **`len()` counting withdrawn tickets.** Symptom: a queue that reports three
  waiting when one is waiting. Nothing crashes; the report is simply wrong.
- **Removing withdrawn entries from the heap eagerly.** Symptom: correct output,
  and an `O(n)` scan plus a rebuild for something that costs nothing to defer.
- **Pushing all three channel logs into the merge heap.** Symptom: correct
  ledger, `O(n)` space, and no k-way merge.
- **Breaking a minute tie alphabetically.** Symptom: phone before walk-in at
  minute 35, which is not the café's rule.
- **Interrupting a job at closing.** Symptom: a bench log that ends exactly at
  180 every time, which real benches do not.
- **Losing a job in the accounting.** Symptom: served plus withdrawn plus
  leftover is ten, not eleven. Assert the identity rather than eyeballing it.

## Acceptance checklist

- [ ] Eleven jobs in the ledger, tickets 1 to 11, minute order.
- [ ] Minute 35 resolves to the table lamp (walk-in) before the hairdryer (phone).
- [ ] Six jobs served, two withdrawn, three still queued — and they sum to eleven.
- [ ] The food mixer's 102-minute wait appears in the longest-waits table.
- [ ] `withdraw` on an already-served or unknown ticket returns `False`.
- [ ] `len()` on the desk excludes withdrawn tickets.
- [ ] The file runs start to finish and prints `All checks passed.`
- [ ] Both write-ups exist, both have memos, and they cross-reference each other.

## Stretch

- Add a second bench. The queue does not change; the day loop does — and saying
  precisely which part changes is worth more than the code.
- Let a waiting job's urgency be raised at a given minute. Lazy deletion is the
  answer again; say why re-heaping is not.
- Report the café's idle minutes against the wait times and say whether the bench
  or the priority rule is the constraint. On this data one of them plainly is.
- Replay the same day first-come-first-served and compare the longest wait under
  each rule. That comparison is the argument for the priority queue, in numbers.

## Self-reflection

Close the mini-project README with four short paragraphs:

1. **Which idiom was hardest**, and what specifically made it hard — not "heaps
   are tricky" but the sentence you could not write until you understood it.
2. **The bug you actually hit**, and how you found it. If you hit none, say what
   you would have hit had the self-checks not been there.
3. **The pair comparison.** In one paragraph: how the merge heap and the queue
   heap differ in what they hold, how big they get, and what keeps them correct.
4. **What you would do differently.** One concrete thing, not a resolution.

## After the mini-project

Mock #2 is next week and grades both of these shapes separately. The write-ups
are your revision notes for it: if you cannot reconstruct either memo from
memory on Sunday evening, re-read the one you cannot, then write it again
without looking.
