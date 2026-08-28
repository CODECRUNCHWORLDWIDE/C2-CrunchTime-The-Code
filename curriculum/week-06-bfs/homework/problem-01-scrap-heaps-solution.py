"""problem-01-scrap-heaps-solution.py — measuring the heaps in a salvage yard.

A drone photograph of a salvage yard, drawn as rows of text. A hash is scrap
metal, a dot is bare ground. Scrap that touches edge to edge is one heap; a
corner touch is not enough, because a grab cannot lift across a corner.

The yard manager does not want the number of heaps. He wants the sizes,
biggest first, so he can plan which ones the grab clears today.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# A yard with one long heap, several middling ones, and a single sheet at
# (3, 8) that touches the pair above it only at a corner — so it is a heap
# of its own, not part of theirs.
YARD: tuple[str, ...] = (
    "##....###.",
    "##.....#..",
    "#........#",
    "....##..#.",
    "#...##....",
    "#...##..#.",
    "#.......#.",
    "......###.",
    ".#....#...",
    ".#....#...",
)

TOUCHING: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def heap_sizes(yard: tuple[str, ...]) -> list[int]:
    """Return the size of every scrap heap, biggest first.

    Args:
        yard: The rows of the photograph. `#` is scrap, `.` is bare ground.

    Returns:
        One number per heap — how many squares of scrap it holds — sorted
        largest to smallest. Equal sizes keep no particular order because
        nothing distinguishes them. An empty yard, or one with no scrap in
        it, gives an empty list.
    """
    if not yard or not yard[0]:
        return []

    rows, columns = len(yard), len(yard[0])
    counted: set[tuple[int, int]] = set()
    sizes: list[int] = []

    for row in range(rows):
        for column in range(columns):
            if yard[row][column] != "#" or (row, column) in counted:
                continue
            counted.add((row, column))
            queue = deque([(row, column)])
            size = 0
            while queue:
                at_row, at_column = queue.popleft()
                size += 1
                for down, across in TOUCHING:
                    next_cell = (at_row + down, at_column + across)
                    if (
                        0 <= next_cell[0] < rows
                        and 0 <= next_cell[1] < columns
                        and yard[next_cell[0]][next_cell[1]] == "#"
                        and next_cell not in counted
                    ):
                        counted.add(next_cell)
                        queue.append(next_cell)
            sizes.append(size)

    return sorted(sizes, reverse=True)


# ---- Self-check ----
if __name__ == "__main__":
    sizes = heap_sizes(YARD)
    print(f"heaps    : {len(sizes)}")
    print(f"sizes    : {sizes}")
    print(f"scrap    : {sum(sizes)} squares")

    assert sum(sizes) == sum(row.count("#") for row in YARD)
    assert sizes == sorted(sizes, reverse=True)
    assert sizes == [7, 6, 5, 4, 3, 2, 1, 1]
    # The sheet at (3, 8) and the sheet at (2, 9) meet at a corner only, so
    # they are the two heaps of size 1 rather than one heap of size 2.
    assert sizes.count(1) == 2

    # A corner touch is not a join. These two heaps stay separate.
    assert heap_sizes(("#.", ".#")) == [1, 1]
    # An edge touch is.
    assert heap_sizes(("##", "..")) == [2]
    # Nothing to count.
    assert heap_sizes(()) == []
    assert heap_sizes(("",)) == []
    assert heap_sizes(("...", "...")) == []
    # One heap filling the whole yard.
    assert heap_sizes(("###", "###")) == [6]

    print("All checks passed.")
