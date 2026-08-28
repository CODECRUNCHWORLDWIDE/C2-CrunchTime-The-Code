"""README-solution.py — the Week 3 sliding-window toolkit.

Six problems, six functions, one file. Each one is a different corner of the
same pattern, and the point of putting them side by side is that you can see
how little changes between them:

    1. quietest_window_cost   fixed window, running sum, smallest total
    2. longest_reprint_run    growing window, one count watched
    3. valid_pallet_starts    fixed window, two frequency tables, positions out
    4. shortest_recall_window shrinking window, a single counter
    5. flights_within_paddle  growing window, counting whole families at once
    6. tightest_rehearsal_block shrinking window, tables plus a matched count

Every one is a single pass with two indices that only move forward. What
differs is the state inside the window, the moment the answer is recorded, and
the contract — four return types and three different ways of saying "no".

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def quietest_window_cost(requests: list[int], k: int) -> int | None:
    """Return the smallest request total over any k consecutive hours.

    Args:
        requests: Requests served in each hour of operation, in time order.
        k: How many consecutive hours the outage covers.

    Returns:
        The requests lost during the quietest block. None when the block does
        not fit inside the log. There is no tie-break, because the answer is a
        number rather than a position.
    """
    if k > len(requests):
        return None

    window_total = sum(requests[:k])
    quietest = window_total
    for right in range(k, len(requests)):
        window_total += requests[right] - requests[right - k]
        if window_total < quietest:
            quietest = window_total
    return quietest


def longest_reprint_run(titles: list[str], m: int) -> int:
    """Return the longest run of blocks in which no title repeats past m times.

    Args:
        titles: Title code of each book block, logged bottom to top.
        m: How many times one title may appear before the blade is reground.

    Returns:
        The length of the longest qualifying run. Zero when m is zero or the
        stack is empty.
    """
    if m == 0 or not titles:
        return 0

    counts: dict[str, int] = {}
    left = 0
    longest = 0

    for right, title in enumerate(titles):
        counts[title] = counts.get(title, 0) + 1
        # Only the title just added can have broken the invariant, so only its
        # count needs checking. That is why no other count is looked at here.
        while counts[title] > m:
            counts[titles[left]] -= 1
            left += 1
        if right - left + 1 > longest:
            longest = right - left + 1

    return longest


def valid_pallet_starts(scan: list[str], manifest: list[str]) -> list[int]:
    """Return the start index of every pallet matching the manifest exactly.

    Args:
        scan: SKU of each carton, in the order the scanner read them.
        manifest: The SKUs a pallet must hold. Repeats are real requirements.

    Returns:
        Ascending start indices of every window whose SKU counts equal the
        manifest's. Empty list when the manifest is empty or longer than the
        scan. Overlapping pallets are separate candidates and both count.
    """
    size = len(manifest)
    if size == 0 or size > len(scan):
        return []

    wanted = Counter(manifest)
    window = Counter(scan[:size])
    starts = [0] if window == wanted else []

    for right in range(size, len(scan)):
        window[scan[right]] += 1
        leaving = scan[right - size]
        window[leaving] -= 1
        if window[leaving] == 0:
            del window[leaving]
        if window == wanted:
            starts.append(right - size + 1)

    return starts


def shortest_recall_window(verdicts: list[str], q: int) -> int:
    """Return the length of the shortest run holding at least q failures.

    Args:
        verdicts: "pass" or "fail" for each unit, in production order.
        q: How many failures a recall must cover. At least one, which is what
            makes zero a safe way of saying "impossible".

    Returns:
        The length of the shortest qualifying run, or 0 when the line never
        accumulates q failures.
    """
    left = 0
    failures = 0
    shortest = 0

    for right, verdict in enumerate(verdicts):
        if verdict == "fail":
            failures += 1
        while failures >= q:
            # Record first. Removing first measures a window you just broke.
            length = right - left + 1
            if shortest == 0 or length < shortest:
                shortest = length
            if verdicts[left] == "fail":
                failures -= 1
            left += 1

    return shortest


def flights_within_paddle(taps: list[str], k: int) -> int:
    """Return how many flights hold at most k distinct beer styles.

    Args:
        taps: The style poured by each tap, logged left to right along the bar.
        k: How many glasses the guest's paddle holds, so how many distinct
            styles one flight may contain.

    Returns:
        The number of contiguous runs of one or more taps within the limit.
        Zero when k is zero or the bar is empty.
    """
    if k == 0 or not taps:
        return 0

    counts: dict[str, int] = {}
    left = 0
    flights = 0

    for right, style in enumerate(taps):
        counts[style] = counts.get(style, 0) + 1

        while len(counts) > k:
            leaving = taps[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # Dropping taps from the left can never raise the distinct count, so
        # every flight ending here and starting at or after `left` qualifies.
        flights += right - left + 1

    return flights


def tightest_rehearsal_block(schedule: list[str], call: list[str]) -> tuple[int, int] | None:
    """Return the shortest block of slots covering the whole call sheet.

    Args:
        schedule: The section called to each ten-minute slot, in order.
        call: Sections the coach needs. Repeats are real requirements.

    Returns:
        (start, length) for the shortest covering block. Ties go to the
        smaller start — the opposite of Challenge 1, and the reason this
        problem exists. An empty call sheet returns (0, 0); a call sheet no
        block can cover returns None.
    """
    if not call:
        return (0, 0)
    if len(call) > len(schedule):
        return None

    wanted = Counter(call)
    distinct_wanted = len(wanted)

    in_block: dict[str, int] = {}
    left = 0
    matched = 0
    best: tuple[int, int] | None = None

    for right, section in enumerate(schedule):
        in_block[section] = in_block.get(section, 0) + 1
        if section in wanted and in_block[section] == wanted[section]:
            matched += 1

        while matched == distinct_wanted:
            candidate = (right - left + 1, left)
            if best is None or candidate < best:
                best = candidate
            leaving = schedule[left]
            in_block[leaving] -= 1
            if leaving in wanted and in_block[leaving] < wanted[leaving]:
                matched -= 1
            left += 1

    if best is None:
        return None
    length, start = best
    return (start, length)


# ---- Self-check ----
if __name__ == "__main__":
    print("1 - the quietest maintenance window")
    for requests, k in [([80, 20, 30, 90, 10], 2), ([3, 4, 5], 2), ([0, 0, 0], 2), ([7], 1), ([5, 5], 3), ([], 1)]:
        print(f"    k={k}  {str(requests):<20} -> {quietest_window_cost(requests, k)}")

    print("2 - the longest reprint run")
    for titles, m in [(["A", "B", "A", "A", "C", "A"], 2), (["A", "A", "A", "B", "B", "B"], 2), (["A", "A", "A"], 1), (["A", "B", "C"], 5), (["A", "B"], 0), ([], 2)]:
        print(f"    m={m}  {str(titles):<32} -> {longest_reprint_run(titles, m)}")

    print("3 - the pallet seal check")
    for scan, manifest in [(["X1", "X1", "Y2", "X1", "Y2", "X1"], ["X1", "Y2"]), (["X1", "Y2", "Y2", "X1", "X1", "Y2"], ["X1", "X1", "Y2"]), (["X1", "X1", "X1"], ["X1"]), (["X1", "Y2"], ["Z3"]), (["X1"], ["X1", "Y2"]), (["X1"], []), ([], ["X1"])]:
        print(f"    {str(manifest):<20} {str(scan):<44} -> {valid_pallet_starts(scan, manifest)}")

    print("4 - the shortest recall window")
    for verdicts, q in [(["pass", "fail", "pass", "pass", "fail", "pass", "fail"], 2), (["pass", "fail", "fail"], 2), (["fail", "pass", "pass", "pass", "fail"], 2), (["fail", "fail", "pass"], 2), (["pass", "pass", "pass"], 1), ([], 1)]:
        print(f"    q={q}  {str(verdicts):<64} -> {shortest_recall_window(verdicts, q)}")

    print("5 - the tasting flight count")
    for taps, k in [(["ipa", "stout", "ipa", "lager"], 2), (["ipa", "ipa", "ipa"], 1), (["ipa", "stout"], 1), (["ipa", "stout"], 5), (["ipa"], 0), ([], 3)]:
        print(f"    k={k}  {str(taps):<40} -> {flights_within_paddle(taps, k)}")

    print("6 - the tightest rehearsal block")
    for schedule, call in [(["vln", "vla", "cel", "vln", "vla", "cel"], ["vln", "vla", "cel"]), (["cel", "cel", "vln", "hrn", "vla", "cel", "vln"], ["vln", "vla", "cel"]), (["vla", "vln", "vla", "vla", "vln"], ["vla", "vla"]), (["vla", "vla", "vln"], ["vla", "vln"]), (["cel", "hrn", "vln"], ["vln", "cel"]), (["vln", "vln", "vln"], ["vln", "cel"]), (["vla", "vln"], ["vla", "vla"]), (["vln"], []), ([], ["vln"])]:
        print(f"    {str(call):<22} {str(schedule):<56} -> {tightest_rehearsal_block(schedule, call)}")
    print()

    assert quietest_window_cost([80, 20, 30, 90, 10], 2) == 50
    assert quietest_window_cost([3, 4, 5], 2) == 7
    assert quietest_window_cost([0, 0, 0], 2) == 0
    assert quietest_window_cost([7], 1) == 7
    assert quietest_window_cost([5, 5], 3) is None
    assert quietest_window_cost([], 1) is None

    assert longest_reprint_run(["A", "B", "A", "A", "C", "A"], 2) == 4
    assert longest_reprint_run(["A", "A", "A", "B", "B", "B"], 2) == 4
    assert longest_reprint_run(["A", "A", "A"], 1) == 1
    assert longest_reprint_run(["A", "B", "C"], 5) == 3
    assert longest_reprint_run(["A", "B"], 0) == 0
    assert longest_reprint_run([], 2) == 0

    assert valid_pallet_starts(["X1", "X1", "Y2", "X1", "Y2", "X1"], ["X1", "Y2"]) == [1, 2, 3, 4]
    assert valid_pallet_starts(["X1", "Y2", "Y2", "X1", "X1", "Y2"], ["X1", "X1", "Y2"]) == [2, 3]
    assert valid_pallet_starts(["X1", "X1", "X1"], ["X1"]) == [0, 1, 2]
    assert valid_pallet_starts(["X1", "Y2"], ["Z3"]) == []
    assert valid_pallet_starts(["X1"], ["X1", "Y2"]) == []
    assert valid_pallet_starts(["X1"], []) == []
    assert valid_pallet_starts([], ["X1"]) == []

    assert shortest_recall_window(["pass", "fail", "pass", "pass", "fail", "pass", "fail"], 2) == 3
    assert shortest_recall_window(["pass", "fail", "fail"], 2) == 2
    assert shortest_recall_window(["fail", "pass", "pass", "pass", "fail"], 2) == 5
    assert shortest_recall_window(["fail", "fail", "pass"], 2) == 2
    assert shortest_recall_window(["pass", "pass", "pass"], 1) == 0
    assert shortest_recall_window([], 1) == 0

    assert flights_within_paddle(["ipa", "stout", "ipa", "lager"], 2) == 8
    assert flights_within_paddle(["ipa", "ipa", "ipa"], 1) == 6
    assert flights_within_paddle(["ipa", "stout"], 1) == 2
    assert flights_within_paddle(["ipa", "stout"], 5) == 3
    assert flights_within_paddle(["ipa"], 0) == 0
    assert flights_within_paddle([], 3) == 0

    assert tightest_rehearsal_block(["vln", "vla", "cel", "vln", "vla", "cel"], ["vln", "vla", "cel"]) == (0, 3)
    assert tightest_rehearsal_block(["cel", "cel", "vln", "hrn", "vla", "cel", "vln"], ["vln", "vla", "cel"]) == (4, 3)
    assert tightest_rehearsal_block(["vla", "vln", "vla", "vla", "vln"], ["vla", "vla"]) == (2, 2)
    assert tightest_rehearsal_block(["vla", "vla", "vln"], ["vla", "vln"]) == (1, 2)
    assert tightest_rehearsal_block(["cel", "hrn", "vln"], ["vln", "cel"]) == (0, 3)
    assert tightest_rehearsal_block(["vln", "vln", "vln"], ["vln", "cel"]) is None
    assert tightest_rehearsal_block(["vla", "vln"], ["vla", "vla"]) is None
    assert tightest_rehearsal_block(["vln"], []) == (0, 0)
    assert tightest_rehearsal_block([], ["vln"]) is None

    # Problem 5 counts what Problem 5 says it counts: check the shape-C sum
    # against a flat enumeration of every flight on a small bar.
    bar = ["ipa", "stout", "ipa", "lager", "ipa", "ipa", "stout"]
    for limit in range(0, 5):
        slow = sum(
            1
            for i in range(len(bar))
            for j in range(i + 1, len(bar) + 1)
            if len(set(bar[i:j])) <= limit
        )
        assert flights_within_paddle(bar, limit) == slow

    print("All checks passed.")
