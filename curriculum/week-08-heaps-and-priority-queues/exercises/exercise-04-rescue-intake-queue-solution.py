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
