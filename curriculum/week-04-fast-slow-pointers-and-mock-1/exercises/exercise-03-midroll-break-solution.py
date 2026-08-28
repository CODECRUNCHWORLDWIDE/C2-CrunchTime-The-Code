"""exercise-03-midroll-break-solution.py — where does the mid-roll ad go?

One walk. The slow pointer takes one segment per turn and the fast pointer
takes two, so when the fast one runs out of stream the slow one is standing
in the middle. The loop guard looks one segment *ahead* of the fast
pointer, which is what makes it stop on the earlier of the two middles.

The streams are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per stream, then
"All checks passed."
"""

from __future__ import annotations


class Segment:
    """One block of a live stream. You can only follow it forward."""

    def __init__(self, segment_id: str, next_segment: "Segment | None" = None) -> None:
        self.segment_id = segment_id
        self.next_segment = next_segment


def build_stream(ids: list[str]) -> list[Segment]:
    """Wire a stream from a list of segment ids and hand back every segment.

    Args:
        ids: One id per segment, in play order. Ids may repeat.

    Returns:
        The segments, in order. Empty when `ids` is empty. The caller reads
        `segments[0]` for the first segment and uses the rest to check
        answers by identity rather than by id.
    """
    segments = [Segment(segment_id) for segment_id in ids]
    for earlier, later in zip(segments, segments[1:]):
        earlier.next_segment = later
    return segments


def mid_roll_point(first: Segment | None) -> tuple[Segment, int] | None:
    """Return the mid-roll segment and how many segments come before it.

    Args:
        first: The first segment of the stream, or None for an empty stream.

    Returns:
        A pair of (segment, count of segments strictly before it), or None
        for an empty stream. For an even number of segments this is the
        *earlier* of the two middles, so the first half is never shorter
        than the second.
    """
    if first is None:
        return None

    slow = first
    fast = first
    before = 0
    while fast.next_segment is not None and fast.next_segment.next_segment is not None:
        slow = slow.next_segment
        fast = fast.next_segment.next_segment
        before += 1
    return slow, before


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("s1 -> s2 -> s3 -> s4 -> s5", 5, 2),
        ("s1 -> ... -> s6", 6, 2),
        ("s1 -> s2 -> s3 -> s4", 4, 1),
        ("s1 -> s2 -> s3", 3, 1),
        ("s1 -> s2", 2, 0),
        ("s1", 1, 0),
        ("s1 -> ... -> s7", 7, 3),
    ]

    for shape, count, expected_index in CASES:
        segments = build_stream([f"s{number}" for number in range(1, count + 1)])
        result = mid_roll_point(segments[0])
        assert result is not None, f"{shape}: this stream is not empty"
        segment, before = result
        assert segment is segments[expected_index], f"{shape}: wrong segment"
        assert before == expected_index, f"{shape}: wrong offset"
        print(f"{shape:<28} break after {segment.segment_id}, {before} before it")

    markers = build_stream(["AD", "AD", "AD", "AD"])
    marker_segment, marker_before = mid_roll_point(markers[0])
    assert marker_segment is markers[1], "four identical ids: position is the answer"
    assert marker_before == 1
    print(f"{'AD -> AD -> AD -> AD':<28} break after AD, {marker_before} before it")

    assert mid_roll_point(None) is None, "an empty stream has no mid-roll point"
    print(f"{'(empty stream)':<28} no break")

    print("All checks passed.")
