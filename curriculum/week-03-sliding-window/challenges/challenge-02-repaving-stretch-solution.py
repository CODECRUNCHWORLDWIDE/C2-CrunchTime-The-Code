"""challenge-02-repaving-stretch-solution.py — the longest repavable stretch.

A highways authority logs the surface of every 20-metre segment along a route.
A resurfacing crew can repave at most `budget` segments in one pass, the pass
must cover a contiguous stretch, and the whole stretch must end up one
surface. Which stretch should they take, and what surface does it become?

The window's invariant is one subtraction: a stretch is affordable when its
length minus the count of its most common surface is at most the budget. That
difference is exactly the number of segments the crew would have to repave.
The catalogue is small, so re-reading the table's largest count each step is
six probes, which is a constant, which is what keeps the scan linear.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def longest_uniform_stretch(surfaces: list[str], budget: int) -> tuple[int, int, str] | None:
    """Return the longest stretch the crew can make uniform within budget.

    Args:
        surfaces: Surface code of each 20-metre segment, in route order.
        budget: How many segments the crew may repave in one pass. Zero is
            legal and asks for the longest already-uniform run.

    Returns:
        (start, end, surface) with surfaces[start:end] the stretch and
        `surface` what it becomes. Ties on length go to the larger start; ties
        on the surface inside the chosen stretch go to the alphabetically
        first code. An empty route returns None.
    """
    if not surfaces:
        return None

    counts: dict[str, int] = {}
    left = 0
    best: tuple[int, int] | None = None

    for right, surface in enumerate(surfaces):
        counts[surface] = counts.get(surface, 0) + 1

        # Segments to repave = window length - the most common surface in it.
        while (right - left + 1) - max(counts.values()) > budget:
            leaving = surfaces[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # Longer wins; then the later start. Both negated so one tuple
        # comparison says both rules.
        candidate = (-(right - left + 1), -left)
        if best is None or candidate < best:
            best = candidate

    negated_length, negated_start = best
    length, start = -negated_length, -negated_start
    tally = Counter(surfaces[start : start + length])
    most = max(tally.values())
    surface = min(code for code, seen in tally.items() if seen == most)
    return (start, start + length, surface)


def repaves_needed(stretch: list[str], surface: str) -> int:
    """Return how many segments of `stretch` are not already `surface`.

    Args:
        stretch: The segments inside a candidate window.
        surface: The surface the crew would lay.

    Returns:
        The count of segments that would have to be repaved.
    """
    return sum(1 for segment in stretch if segment != surface)


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], int]] = [
        (["asphalt", "chipseal", "asphalt", "gravel", "asphalt", "asphalt"], 1),
        (["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1),
        (["asphalt", "asphalt", "gravel", "asphalt", "asphalt"], 1),
        (["gravel", "gravel", "asphalt", "gravel", "gravel", "gravel"], 0),
        (["asphalt", "gravel", "concrete", "chipseal"], 0),
        (["concrete", "asphalt"], 1),
        (["asphalt", "concrete", "gravel"], 5),
        (["chipseal"], 0),
        ([], 3),
    ]
    for route, budget in cases:
        answer = longest_uniform_stretch(route, budget)
        if answer is None:
            print(f"budget {budget}  route {str(route):<66} -> None")
        else:
            start, end, surface = answer
            print(f"budget {budget}  route {str(route):<66} -> ({start}, {end}) as {surface}")
    print()

    assert longest_uniform_stretch(["asphalt", "chipseal", "asphalt", "gravel", "asphalt", "asphalt"], 1) == (2, 6, "asphalt")
    assert longest_uniform_stretch(["asphalt", "gravel", "asphalt", "gravel", "asphalt"], 1) == (2, 5, "asphalt")
    assert longest_uniform_stretch(["asphalt", "asphalt", "gravel", "asphalt", "asphalt"], 1) == (0, 5, "asphalt")
    assert longest_uniform_stretch(["gravel", "gravel", "asphalt", "gravel", "gravel", "gravel"], 0) == (3, 6, "gravel")
    assert longest_uniform_stretch(["asphalt", "gravel", "concrete", "chipseal"], 0) == (3, 4, "chipseal")
    assert longest_uniform_stretch(["concrete", "asphalt"], 1) == (0, 2, "asphalt")
    assert longest_uniform_stretch(["asphalt", "concrete", "gravel"], 5) == (0, 3, "asphalt")
    assert longest_uniform_stretch(["chipseal"], 0) == (0, 1, "chipseal")
    assert longest_uniform_stretch([], 3) is None

    # Brute force agrees: check every stretch against every surface it could
    # become, and pick by the contract's own ordering.
    for route, budget in cases:
        affordable = [
            (-(j - i), -i)
            for i in range(len(route))
            for j in range(i + 1, len(route) + 1)
            if min(repaves_needed(route[i:j], code) for code in set(route[i:j])) <= budget
        ]
        answer = longest_uniform_stretch(route, budget)
        if not affordable:
            assert answer is None
            continue
        negated_length, negated_start = min(affordable)
        start, length = -negated_start, -negated_length
        assert answer is not None
        assert (answer[0], answer[1] - answer[0]) == (start, length)
        assert repaves_needed(route[start : start + length], answer[2]) <= budget

    print("All checks passed.")
