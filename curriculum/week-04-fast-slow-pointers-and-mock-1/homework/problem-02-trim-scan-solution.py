"""problem-02-trim-scan-solution.py — drop the k-th scan from the end.

This is the fast/slow family's other member: the gap between the two walkers
is fixed and known in advance, so nobody ever laps anybody and there is no
lemma to prove. Push one walker `k` scans ahead, then move both together.
When the front walker falls off the end, the back walker is standing exactly
one place in front of the scan to remove.

The dummy scan in front of the chain is what lets "remove the oldest scan"
use the same three lines as every other case.

The chains are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per correction, then
"All checks passed."
"""

from __future__ import annotations


class Scan:
    """One handheld scan on a parcel, oldest first."""

    def __init__(self, scan_code: str, next_scan: "Scan | None" = None) -> None:
        self.scan_code = scan_code
        self.next_scan = next_scan


def build_history(codes: list[str]) -> list[Scan]:
    """Wire a scan history from a list of codes and hand back every scan.

    Args:
        codes: One code per scan, oldest first. Codes repeat constantly.

    Returns:
        The scans, in order. Empty when `codes` is empty.
    """
    scans = [Scan(code) for code in codes]
    for earlier, later in zip(scans, scans[1:]):
        earlier.next_scan = later
    return scans


def history_codes(first: Scan | None) -> list[str]:
    """Walk a scan chain into a list of codes, oldest first."""
    codes: list[str] = []
    while first is not None:
        codes.append(first.scan_code)
        first = first.next_scan
    return codes


def trim_scan(first: Scan | None, k: int) -> Scan | None:
    """Remove the k-th scan counted back from the newest one.

    Args:
        first: The oldest scan, or None for a parcel with no history.
        k: How far back from the newest scan the offending one sits. `k = 1`
            is the newest scan itself.

    Returns:
        The first scan of the resulting chain, which is None when the chain
        becomes empty. When `k` is larger than the number of scans the chain
        is returned unchanged, because a correction that does not apply must
        not delete something else instead.

    Raises:
        ValueError: If `k` is zero or negative.
    """
    if k <= 0:
        raise ValueError("k counts back from the newest scan and starts at 1")
    if first is None:
        return None

    fast = first
    for _ in range(k):
        if fast is None:
            return first  # k is past the oldest scan: leave the chain alone.
        fast = fast.next_scan

    dummy = Scan("", first)
    slow = dummy
    while fast is not None:
        fast = fast.next_scan
        slow = slow.next_scan
    slow.next_scan = slow.next_scan.next_scan
    return dummy.next_scan


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        (["ARV", "SRT", "OFD", "DLV"], 1, ["ARV", "SRT", "OFD"]),
        (["ARV", "SRT", "OFD", "DLV"], 4, ["SRT", "OFD", "DLV"]),
        (["ARV", "SRT", "OFD", "DLV"], 5, ["ARV", "SRT", "OFD", "DLV"]),
        (["ARV"], 1, []),
        (["ARV"], 2, ["ARV"]),
        ([], 1, []),
        (["BEEP", "BEEP", "BEEP"], 2, ["BEEP", "BEEP"]),
    ]

    for codes, k, expected in CASES:
        scans = build_history(codes)
        first = scans[0] if scans else None
        result = history_codes(trim_scan(first, k))
        assert result == expected, f"{codes}, k={k}: got {result}"
        print(f"{str(codes):<34} k={k}  ->  {result}")

    # Three identical codes cannot tell you which scan went. Check by identity.
    beeps = build_history(["BEEP", "BEEP", "BEEP"])
    kept = trim_scan(beeps[0], 2)
    assert kept is beeps[0] and kept.next_scan is beeps[2]
    assert beeps[1] not in (kept, kept.next_scan)
    print(f"{'the middle BEEP went, by identity':<34} k=2  ->  ['BEEP', 'BEEP']")

    try:
        trim_scan(build_history(["ARV", "SRT"])[0], 0)
    except ValueError as caught:
        print(f"{'k of 0':<34} raises ValueError: {caught}")
    else:  # pragma: no cover - the raise below is the real check
        raise AssertionError("k of 0 must raise")

    print("All checks passed.")
