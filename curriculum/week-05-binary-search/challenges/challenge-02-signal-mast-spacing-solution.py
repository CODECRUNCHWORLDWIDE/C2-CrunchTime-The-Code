"""challenge-02-signal-mast-spacing-solution.py - the widest signal spacing.

Binary search on the ANSWER, in the maximise-the-minimum direction. The
predicate is a greedy placement sweep: at a trial spacing, plant a mast on
the first post and then on every post far enough from the last one planted.

The self-checks at the bottom are the starter's, unchanged. The last one
cross-checks the search against every possible choice of posts on small
lines. When they all pass the file prints "All checks passed."
"""

import random
from itertools import combinations

# ---- Given data ----
POSTS: list[int] = [0, 4, 9, 13, 25, 31]


# ---- Your task ----
def place_masts(posts: list[int], spacing: int, masts: int) -> list[int] | None:
    """Plant masts left to right, never closer together than `spacing`.

    Args:
        posts: Post positions in metres, ascending and distinct, not empty.
        spacing: The minimum distance to keep between two masts.
        masts: How many masts must be planted.

    Returns:
        The chosen post positions when all `masts` fit, otherwise None.
    """
    chosen = [posts[0]]
    for post in posts[1:]:
        if len(chosen) == masts:
            break
        if post - chosen[-1] >= spacing:
            chosen.append(post)
    return chosen if len(chosen) == masts else None


def mast_spacing(posts: list[int], masts: int) -> tuple[int, list[int]] | None:
    """Return the widest guaranteed spacing and the placement that achieves it.

    Args:
        posts: Post positions in metres, ascending and distinct.
        masts: How many masts the operator is bolting on.

    Returns:
        (spacing, chosen) where spacing is the largest achievable value of the
        smallest distance between two masts, and chosen is the leftmost-greedy
        placement at that spacing. None when masts < 2 or masts > len(posts).
    """
    if masts < 2 or masts > len(posts):
        return None

    lo, hi = 1, (posts[-1] - posts[0]) // (masts - 1)
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # round up, or lo == mid spins forever
        if place_masts(posts, mid, masts) is not None:
            lo = mid  # mid works, so the answer is mid or wider
        else:
            hi = mid - 1  # mid is too wide, so the answer is narrower
    chosen = place_masts(posts, lo, masts)
    assert chosen is not None  # lo == 1 always fits: the posts are distinct
    return lo, chosen


# ---- Self-check ----
if __name__ == "__main__":
    print(f"posts: {POSTS}")
    for count in (2, 3, 6, 7):
        print(f"{count} masts -> {mast_spacing(POSTS, count)}")

    assert mast_spacing(POSTS, 2) == (31, [0, 31])
    assert mast_spacing(POSTS, 3) == (13, [0, 13, 31])
    assert mast_spacing(POSTS, 6) == (4, [0, 4, 9, 13, 25, 31])
    assert mast_spacing(POSTS, 7) is None
    assert mast_spacing(POSTS, 1) is None
    assert mast_spacing(POSTS, 0) is None
    assert mast_spacing([], 2) is None
    assert mast_spacing([5, 6], 2) == (1, [5, 6])
    assert mast_spacing([0, 3, 4, 7, 10], 3) == (4, [0, 4, 10])
    assert mast_spacing([0, 5, 6, 11], 3) == (5, [0, 5, 11])
    assert POSTS[0] == 0  # the survey was never rearranged

    rng = random.Random(20250505)
    lines = 0
    for _ in range(300):
        line = sorted(rng.sample(range(0, 60), rng.randrange(2, 8)))
        for count in range(2, len(line) + 1):
            best = max(
                min(b - a for a, b in zip(pick, pick[1:]))
                for pick in combinations(line, count)
            )
            spacing, chosen = mast_spacing(line, count)
            assert spacing == best, (line, count, spacing, best)
            assert min(b - a for a, b in zip(chosen, chosen[1:])) >= best
        lines += 1
    print(f"cross-checked {lines} generated post lines against every choice of posts")
    print("All checks passed.")
