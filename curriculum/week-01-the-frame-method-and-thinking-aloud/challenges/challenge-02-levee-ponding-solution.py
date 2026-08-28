"""challenge-02-levee-ponding-solution.py — water held on a cambered levee road.

Two pointers walk inward from the ends of the survey, carrying one running
maximum each. At every step the lower of the two sections is processed,
because for that section the near rim is already known to be the binding
one. Two integers replace the two million-entry arrays the obvious solution
would build.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def ponded_volume(crown: list[int], shoulder: int) -> int:
    """Total the water held on the road after rain.

    Args:
        crown: Crown height of each one-metre section in centimetres above
            datum, west to east. A crown of 0 is a real section at datum.
        shoulder: The camber's per-section depth cap in centimetres.
            A shoulder of 0 sheds every drop and is a legal input.

    Returns:
        The total ponded volume in section-centimetres.
    """
    west, east = 0, len(crown) - 1
    west_max = east_max = 0
    total = 0

    while west < east:
        if crown[west] < crown[east]:
            west_max = max(west_max, crown[west])
            total += min(west_max - crown[west], shoulder)
            west += 1
        else:
            east_max = max(east_max, crown[east])
            total += min(east_max - crown[east], shoulder)
            east -= 1

    return total


# ---- Self-check ----
if __name__ == "__main__":
    surveys = [
        ([4, 1, 3, 0, 2, 5], 100),
        ([4, 1, 3, 0, 2, 5], 2),
        ([4, 1, 3, 0, 2, 5], 0),
        ([1, 5, 2, 6, 3], 100),
        ([8, 0, 5, 0, 8], 3),
        ([9, 6, 4, 1], 100),
        ([3, 3, 3], 100),
        ([2, 0, 2], 5),
        ([3, 0, 0, 3], 100),
        ([7, 2], 100),
        ([7], 100),
        ([], 100),
    ]
    for crown, shoulder in surveys:
        held = ponded_volume(crown, shoulder)
        print(f"shoulder {shoulder:>3} cm  holds {held:>2}  road {crown}")

    assert ponded_volume([4, 1, 3, 0, 2, 5], 100) == 10
    assert ponded_volume([4, 1, 3, 0, 2, 5], 2) == 7
    assert ponded_volume([4, 1, 3, 0, 2, 5], 0) == 0
    assert ponded_volume([1, 5, 2, 6, 3], 100) == 3
    assert ponded_volume([8, 0, 5, 0, 8], 3) == 9
    assert ponded_volume([9, 6, 4, 1], 100) == 0
    assert ponded_volume([3, 3, 3], 100) == 0
    assert ponded_volume([2, 0, 2], 5) == 2
    assert ponded_volume([3, 0, 0, 3], 100) == 6
    assert ponded_volume([7, 2], 100) == 0
    assert ponded_volume([7], 100) == 0
    assert ponded_volume([], 100) == 0
    print("All checks passed.")
