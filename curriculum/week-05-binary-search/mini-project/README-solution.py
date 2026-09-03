"""binary_search_toolkit.py - the five Week 5 mini-project contracts, solved.

Five problems, five binary-search shapes, one file:

    1. nearest_channel       lower bound used as scaffolding for a nearest match
    2. shift_start           the wrap point of a rotated sequence
    3. seat_cursor           lower bound, returning the insertion point and a flag
    4. min_sprinkler_radius  parametric: minimise a threshold
    5. fairest_zone_split    parametric: maximise the minimum

Run it with no arguments. It prints one report line per problem, then runs
the acceptance tables from the mini-project brief and prints
"All checks passed."
"""

# ---------------------------------------------------------------- problem 1


def lower_bound(values: list[int], wanted: int) -> int:
    """Return the first index whose value is >= `wanted`.

    Args:
        values: An ascending list.
        wanted: The value to place.

    Returns:
        The index at which `wanted` would be inserted, which is len(values)
        when every value is smaller. Shared by problems 1 and 3.
    """
    lo, hi = 0, len(values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if values[mid] < wanted:
            lo = mid + 1
        else:
            hi = mid
    return lo


def nearest_channel(frequencies: list[int], wanted: int) -> int | None:
    """Return the index of the channel closest to `wanted`, lower wins a tie.

    Args:
        frequencies: Channel frequencies in kHz, strictly ascending.
        wanted: The frequency the user dialled.

    Returns:
        The index of the nearest channel, or None when the table is empty.
    """
    if not frequencies:
        return None

    cursor = lower_bound(frequencies, wanted)
    if cursor == 0:
        return 0
    if cursor == len(frequencies):
        return len(frequencies) - 1
    below = wanted - frequencies[cursor - 1]
    above = frequencies[cursor] - wanted
    return cursor - 1 if below <= above else cursor


# ---------------------------------------------------------------- problem 2


def shift_start(clock_ins: list[int]) -> tuple[int, int] | None:
    """Return the slot and minute of the earliest clock-in in a rotated roster.

    Args:
        clock_ins: A rotation of a strictly increasing list of minutes.

    Returns:
        (physical_index, minute) of the smallest entry, or None when empty.
    """
    if not clock_ins:
        return None

    lo, hi = 0, len(clock_ins) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if clock_ins[mid] > clock_ins[hi]:
            lo = mid + 1  # the wrap is strictly right of mid
        else:
            hi = mid  # mid is still a candidate for the earliest row
    return lo, clock_ins[lo]


# ---------------------------------------------------------------- problem 3


def seat_cursor(sold: list[int], wanted: int) -> tuple[int, bool]:
    """Return where a seat sits, or would sit, and whether it is already sold.

    Args:
        sold: Sold seat numbers, strictly ascending.
        wanted: The seat the patron asked for.

    Returns:
        (index, already_sold). The index is a legal insertion point even when
        the seat is absent, and may equal len(sold).
    """
    cursor = lower_bound(sold, wanted)
    return cursor, cursor < len(sold) and sold[cursor] == wanted


# ---------------------------------------------------------------- problem 4


def all_plants_reached(plants: list[int], hydrants: list[int], radius: int) -> bool:
    """Return True when every plant sits within `radius` of some hydrant.

    Args:
        plants: Plant positions in metres, ascending.
        hydrants: Hydrant positions in metres, ascending.
        radius: The sprinkler reach being tested.

    Returns:
        Whether the whole row is watered. One merge pass, O(n + m).
    """
    reach = 0
    for plant in plants:
        while reach < len(hydrants) and hydrants[reach] + radius < plant:
            reach += 1  # this hydrant cannot reach this plant or any later one
        if reach == len(hydrants) or hydrants[reach] - radius > plant:
            return False
    return True


def min_sprinkler_radius(plants: list[int], hydrants: list[int]) -> int | None:
    """Return the smallest whole-metre sprinkler reach that waters every plant.

    Args:
        plants: Plant positions in metres, ascending.
        hydrants: Hydrant positions in metres, ascending.

    Returns:
        The smallest radius that covers the row, 0 when there are no plants,
        or None when there are plants and no hydrants at all.
    """
    if not plants:
        return 0
    if not hydrants:
        return None

    lo = 0
    hi = max(abs(plants[0] - hydrants[0]), abs(plants[-1] - hydrants[0]))
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if all_plants_reached(plants, hydrants, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------------------------------------------------------------- problem 5


def zones_at_least(houses: list[int], target: int) -> int:
    """Return how many zones the greedy sweep closes at a per-zone floor.

    Args:
        houses: Parcel counts in street order.
        target: The per-zone total a courier must reach before the next zone
            can start.

    Returns:
        The number of zones closed. Houses left over at the end belong to the
        last zone, which only raises it, so they are not counted again.
    """
    zones = 0
    carried = 0
    for parcels in houses:
        carried += parcels
        if carried >= target:
            zones += 1
            carried = 0
    return zones


def fairest_zone_split(houses: list[int], couriers: int) -> int | None:
    """Return the largest achievable value of the smallest zone total.

    Args:
        houses: Parcel counts in street order.
        couriers: How many contiguous non-empty zones the street is cut into.

    Returns:
        The best-possible worst zone, 0 for an empty street with no couriers,
        or None when the split cannot be made.
    """
    if not houses:
        return 0 if couriers == 0 else None
    if couriers < 1 or couriers > len(houses):
        return None

    lo, hi = 0, sum(houses)
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # round up, or lo == mid spins forever
        if zones_at_least(houses, mid) >= couriers:
            lo = mid  # mid works, so the answer is mid or larger
        else:
            hi = mid - 1
    return lo


# ---------------------------------------------------------------- the report

if __name__ == "__main__":
    BAND = [881, 894, 902, 917, 940]
    ROSTER = [1305, 1340, 1412, 22, 405, 640, 1150]
    SOLD = [4, 9, 12, 20, 33]
    PLANTS, HYDRANTS = [2, 9, 14, 20], [5, 12]
    STREET = [4, 1, 7, 3, 6, 2]

    print(f"1 nearest_channel(band, 898)        -> {nearest_channel(BAND, 898)}")
    print(f"2 shift_start(roster)               -> {shift_start(ROSTER)}")
    print(f"3 seat_cursor(sold, 13)             -> {seat_cursor(SOLD, 13)}")
    print(f"4 min_sprinkler_radius(row)         -> {min_sprinkler_radius(PLANTS, HYDRANTS)}")
    print(f"5 fairest_zone_split(street, 3)     -> {fairest_zone_split(STREET, 3)}")

    # 1 - the frequency slot
    assert nearest_channel(BAND, 917) == 3
    assert nearest_channel(BAND, 910) == 3
    assert nearest_channel(BAND, 909) == 2
    assert nearest_channel(BAND, 898) == 1
    assert nearest_channel(BAND, 700) == 0
    assert nearest_channel(BAND, 1200) == 4
    assert nearest_channel([1000], 1) == 0
    assert nearest_channel([], 900) is None

    # 2 - the shift start
    assert shift_start(ROSTER) == (3, 22)
    assert shift_start([22, 405, 640]) == (0, 22)
    assert shift_start([640, 22]) == (1, 22)
    assert shift_start([22, 640]) == (0, 22)
    assert shift_start([500]) == (0, 500)
    assert shift_start([]) is None

    # 3 - the waitlist cursor
    assert seat_cursor(SOLD, 12) == (2, True)
    assert seat_cursor(SOLD, 13) == (3, False)
    assert seat_cursor(SOLD, 4) == (0, True)
    assert seat_cursor(SOLD, 33) == (4, True)
    assert seat_cursor(SOLD, 1) == (0, False)
    assert seat_cursor(SOLD, 40) == (5, False)
    assert seat_cursor([], 7) == (0, False)

    # 4 - the sprinkler reach
    assert min_sprinkler_radius(PLANTS, HYDRANTS) == 8
    assert min_sprinkler_radius(PLANTS, [5, 12, 19]) == 3
    assert min_sprinkler_radius([1, 2, 3], [100]) == 99
    assert min_sprinkler_radius([5], [5]) == 0
    assert min_sprinkler_radius([], [5, 12]) == 0
    assert min_sprinkler_radius([], []) == 0
    assert min_sprinkler_radius([3], []) is None

    # 5 - the delivery zones
    assert fairest_zone_split(STREET, 3) == 5
    assert fairest_zone_split(STREET, 2) == 11
    assert fairest_zone_split(STREET, 4) == 3
    assert fairest_zone_split(STREET, 6) == 1
    assert fairest_zone_split(STREET, 1) == 23
    assert fairest_zone_split(STREET, 7) is None
    assert fairest_zone_split(STREET, 0) is None
    assert fairest_zone_split([0, 0, 5], 3) == 0
    assert fairest_zone_split([], 0) == 0
    assert fairest_zone_split([], 1) is None

    print("All checks passed.")
