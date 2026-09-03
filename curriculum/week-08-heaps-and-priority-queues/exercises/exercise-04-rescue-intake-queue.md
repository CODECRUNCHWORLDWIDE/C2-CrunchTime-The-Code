# Exercise 4 — The Rescue Intake Desk

> **Topic:** the heap-of-tuples idiom, and the tiebreaker that stops it crashing
> **Lecture:** [02 — Heaps of Tuples and the k-Closest Shape](../lecture-notes/02-heap-of-tuples-and-k-closest.md)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** the middle element of the tuple looks like bookkeeping and is load-bearing. Leave it out and the program crashes on real data with an error message that does not obviously point at the heap.

## The Brief

A wildlife rescue centre triages arrivals: **most urgent first**, and among
equally urgent patients, **whoever came through the door first**. Urgency is 1
(critical) to 5 (routine).

The queue is a heap of three-part tuples: `(urgency, admission number, patient)`.
The urgency does the sorting. The admission number breaks ties in arrival order.
And the third element — the patient record — is along for the ride and must
**never be compared with another patient record**, because a `Patient` is not an
orderable thing and Python will say so, loudly, the first time two of them meet.

That middle element is not decoration. It is what guarantees the comparison
never reaches the third.

## Starter

`exercise-04-rescue-intake-queue-solution.py` sits beside this page with the
day's arrivals and the self-checks.

`Patient` is a `dataclass` deliberately declared **without** ordering. That is
not an oversight to fix — it is the trap, armed. The file proves it by building
a queue without the tiebreaker and catching the `TypeError`.

```text
urgency  1 critical · 2 urgent · 3 prompt · 4 soon · 5 routine
arrivals 8 patients, admission numbers in arrival order
```

## Requirements

1. `IntakeQueue.admit(patient, urgency)` adds a patient and assigns the next
   admission number itself — the caller does not supply it.
2. `next_patient()` returns the patient who should be treated next, and removes
   them; `None` on an empty desk.
3. `front_urgency()` reads the urgency at the front without removing anyone;
   `None` on an empty desk.
4. `waiting()` reports how many are still queued.
5. `triage(arrivals)` returns the full treatment order as `(name, urgency word)`
   pairs.

## Constraints

- **The queue assigns admission numbers.** A caller passing its own can pass a
  duplicate, and a duplicate puts two patient records against each other.
- **Never compare two `Patient` records.** The tuple must resolve every
  comparison before it reaches the third element, and the file asserts this by
  demonstrating the failure rather than describing it.
- **Equal urgencies are treated in arrival order.** Strictly — this is a
  fairness rule, not a preference.
- **`front_urgency` does not pop.** Reading the front is `heap[0]`.
- An empty desk answers `None` twice over rather than raising.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-04-rescue-intake-queue-solution.py
waiting: 8
queue order: ['Bramble', 'Rook', 'Wisp', 'Marram', 'Pip', 'Fennel', 'Thistle', 'Clover']
front urgency: 1
treatment order:
  1. Bramble  critical
  2. Rook     critical
  3. Wisp     urgent
  4. Marram   urgent
  5. Pip      prompt
  6. Fennel   prompt
  7. Thistle  soon
  8. Clover   routine
empty desk, next patient: None
empty desk, front urgency: None
no tiebreaker: TypeError: '<' not supported between instances of 'Patient' and 'Patient'
All checks passed.
```

The last line before the checks is the exhibit: with the admission number
removed, the heap reaches the patient records and Python refuses. `'<' not
supported between instances of 'Patient' and 'Patient'` is what this bug looks
like in production, and it appears only when two patients happen to share an
urgency — which is to say, on a busy day and not on your test data.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: three-part tuple, what each part is for, and which one is
   never compared.
3. Build the queue with a counter inside it. Admit all eight arrivals.
4. Print the queue order and notice it is **not** the treatment order — a heap is
   not sorted, and this page's queue order proves it again.
5. Drain it and check the treatment order against the rules by hand.
6. Reproduce the `TypeError` without the tiebreaker, so you have seen it. Then
   write the FRAME pass.

## The Solution

```python
"""exercise-04-rescue-intake-queue-solution.py — the rescue centre's intake desk.

A wildlife rescue centre triages arrivals by how urgent they are, and treats
equal urgencies in the order they came through the door. The queue is a heap
of three-part tuples: (urgency, admission number, patient). The middle part is
what keeps the heap from ever comparing two patient records.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq
from dataclasses import dataclass

URGENCY_NAMES = {1: "critical", 2: "urgent", 3: "prompt", 4: "soon", 5: "routine"}


@dataclass
class Patient:
    """One animal on the intake desk. Deliberately not orderable."""

    name: str
    species: str
    note: str


# ---- Given data ----
# (patient, urgency 1 = seen first, 5 = seen last)
ARRIVALS: list[tuple[Patient, int]] = [
    (Patient("Pip", "swift", "fledgling, grounded"), 3),
    (Patient("Bramble", "hedgehog", "road injury"), 1),
    (Patient("Wisp", "barn owl", "wing droop"), 2),
    (Patient("Thistle", "hedgehog", "underweight"), 4),
    (Patient("Rook", "jackdaw", "tangled in fishing line"), 1),
    (Patient("Fennel", "fox cub", "orphaned"), 3),
    (Patient("Marram", "gull", "oiled"), 2),
    (Patient("Clover", "rabbit", "routine check"), 5),
]


# ---- Your task ----
class IntakeQueue:
    """A priority queue of patients, ties broken by who arrived first."""

    def __init__(self) -> None:
        """Start an empty desk with its admission counter at zero."""
        self._heap: list[tuple[int, int, Patient]] = []
        self._admitted = 0

    def __len__(self) -> int:
        """Return how many patients are still waiting."""
        return len(self._heap)

    def admit(self, patient: Patient, urgency: int) -> int:
        """Put a patient in the queue and return their admission number.

        Args:
            patient: The record to queue. It is never compared.
            urgency: 1 is seen first, 5 is seen last.

        Returns:
            The admission number, counting from 1, which is also the
            tiebreaker stored in the heap entry.
        """
        self._admitted += 1
        heapq.heappush(self._heap, (urgency, self._admitted, patient))
        return self._admitted

    def next_patient(self) -> Patient | None:
        """Remove and return the patient who should be seen next.

        Returns:
            The patient record, or None when nobody is waiting. An empty desk
            is a normal state, not an error, so this does not raise.
        """
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek_urgency(self) -> int | None:
        """Return the urgency of the patient at the front, without removing them.

        Returns:
            The urgency number, or None when nobody is waiting.
        """
        if not self._heap:
            return None
        return self._heap[0][0]

    def waiting(self) -> list[str]:
        """Return every waiting patient's name in the order they will be seen.

        The heap itself is not in that order, so this sorts a copy of the
        entries rather than reading the list as it stands.

        Returns:
            Names, most urgent first, ties by admission number.
        """
        return [patient.name for _, _, patient in sorted(self._heap, key=lambda e: e[:2])]


def triage(arrivals: list[tuple[Patient, int]]) -> list[tuple[str, str]]:
    """Return (name, urgency word) for every arrival, in treatment order.

    Args:
        arrivals: (patient, urgency) rows, in the order they came in.

    Returns:
        One row per patient, most urgent first, ties by arrival order.
    """
    desk = IntakeQueue()
    for patient, urgency in arrivals:
        desk.admit(patient, urgency)
    order = []
    while len(desk):
        urgency = desk.peek_urgency()
        patient = desk.next_patient()
        assert patient is not None
        order.append((patient.name, URGENCY_NAMES[urgency]))
    return order


# ---- Self-check ----
if __name__ == "__main__":
    desk = IntakeQueue()
    for patient, urgency in ARRIVALS:
        desk.admit(patient, urgency)

    print(f"waiting: {len(desk)}")
    print(f"queue order: {desk.waiting()}")
    print(f"front urgency: {desk.peek_urgency()}")

    print("treatment order:")
    for position, (name, word) in enumerate(triage(ARRIVALS), 1):
        print(f"  {position}. {name:<8} {word}")

    empty = IntakeQueue()
    print(f"empty desk, next patient: {empty.next_patient()}")
    print(f"empty desk, front urgency: {empty.peek_urgency()}")

    # What the tiebreaker is for: two entries that tie on urgency force the
    # heap to compare whatever sits in the next slot.
    without_counter: list[tuple[int, Patient]] = []
    try:
        heapq.heappush(without_counter, (1, ARRIVALS[1][0]))
        heapq.heappush(without_counter, (1, ARRIVALS[4][0]))
    except TypeError as error:
        print(f"no tiebreaker: {type(error).__name__}: {error}")

    assert desk.waiting()[0] == "Bramble"
    assert desk.waiting()[1] == "Rook"
    assert desk.peek_urgency() == 1
    assert len(desk) == 8
    assert [name for name, _ in triage(ARRIVALS)] == [
        "Bramble",
        "Rook",
        "Wisp",
        "Marram",
        "Pip",
        "Fennel",
        "Thistle",
        "Clover",
    ]
    assert triage(ARRIVALS)[0] == ("Bramble", "critical")
    assert empty.next_patient() is None
    assert empty.peek_urgency() is None
    assert len(triage([])) == 0
    print("All checks passed.")
```

The counter lives on the queue rather than in the caller because that is the
only way to guarantee it is unique — and uniqueness is the entire safety
property here, not a nicety.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-04-rescue-intake-queue-solution.py
```

No third-party packages, no arguments, no input. It prints the waiting count,
the raw queue order, the treatment order, the empty-desk answers, the
demonstrated `TypeError`, and then `All checks passed.`

## Common bugs to catch

- **A two-part tuple.** Symptom: works on your test data, crashes the first time
  two patients share an urgency. The most expensive bug on this page.
- **Letting callers supply the admission number.** Symptom: a duplicate, and the
  same crash by a different route.
- **Sorting the queue list to inspect it.** Symptom: an inspection that reorders
  the heap. Read `heap[0]`.
- **Reporting the queue order as the treatment order.** Symptom: a plausible list
  that is wrong from the second entry on.
- **Raising on an empty desk.** Symptom: an exception where "nobody is waiting"
  is a perfectly good answer.
- **Breaking ties by name.** Symptom: fairness by alphabet, which is not
  fairness. Arrival order is the rule.

## Acceptance checklist

- [ ] Eight patients admitted; `waiting()` reports 8.
- [ ] The treatment order is by urgency, then by arrival, verified by hand.
- [ ] `front_urgency()` is 1 and leaves the queue untouched.
- [ ] Both empty-desk answers are `None`.
- [ ] A queue built without the tiebreaker raises `TypeError`, demonstrated.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Let a patient's urgency be raised while they wait. Lazy deletion is the answer;
  say why re-heaping is not.
- Report the wait each patient had before treatment, and the worst wait per
  urgency band. That is the number the centre would put on a wall.
- Make `Patient` orderable and remove the admission number. It stops crashing and
  starts being unfair — say exactly how, because that is the more interesting
  failure.
