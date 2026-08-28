"""exercise-03-garden-plot-map-solution.py — the community garden's plot map.

A map is a list of rows, and every row is a list of one-character cells.
Building one, copying one, and planting into one all look easy, and all
three have a way of quietly sharing a row that should have been separate.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

EMPTY = "."


def blank_map(rows: int, cols: int) -> list[list[str]]:
    """Return a fresh map with every plot empty.

    Args:
        rows: How many beds run north to south.
        cols: How many plots there are in each bed.

    Returns:
        A list of `rows` rows, each a separate list of `cols` cells.
    """
    return [[EMPTY] * cols for _ in range(rows)]


def plant(plots: list[list[str]], row: int, col: int, crop: str) -> None:
    """Write one crop letter into one plot.

    Args:
        plots: The map to change.
        row: Which bed, counting from 0 at the north end.
        col: Which plot in that bed, counting from 0 at the west end.
        crop: The single letter that stands for the crop.

    Returns:
        None. The map is changed in place, on purpose.
    """
    plots[row][col] = crop


def copy_map(plots: list[list[str]]) -> list[list[str]]:
    """Return a map that shares nothing with the one handed in.

    Args:
        plots: The map to copy.

    Returns:
        A new outer list holding new inner lists with the same letters.
    """
    return [row[:] for row in plots]


def row_counts(plots: list[list[str]]) -> list[int]:
    """Return how many plots are planted in each bed.

    Args:
        plots: The map to count.

    Returns:
        One count per bed, north to south.
    """
    return [sum(1 for cell in row if cell != EMPTY) for row in plots]


def render(plots: list[list[str]]) -> str:
    """Return the map as text, one line per bed.

    Args:
        plots: The map to draw.

    Returns:
        The rows joined by newlines, with no trailing newline.
    """
    return "\n".join("".join(row) for row in plots)


# ---- Self-check ----
if __name__ == "__main__":
    beds = blank_map(3, 4)
    plant(beds, 0, 1, "C")
    plant(beds, 1, 2, "B")
    plant(beds, 2, 0, "K")

    print(render(beds))
    print(f"row counts: {row_counts(beds)}")

    spare = copy_map(beds)
    plant(spare, 0, 3, "T")
    print("after planting on the copy only:")
    print(render(spare))
    print(f"original row counts: {row_counts(beds)}")

    assert beds[0] is not beds[1]  # the beds are separate lists
    assert beds[0][3] == EMPTY  # the copy's tomato did not reach the original
    assert row_counts(beds) == [1, 1, 1]
    assert row_counts(spare) == [2, 1, 1]
    assert blank_map(0, 4) == []
    assert blank_map(2, 0) == [[], []]
    print("All checks passed.")
