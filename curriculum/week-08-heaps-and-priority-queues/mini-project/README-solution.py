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
