"""Exercise 3 — Maximum XOR of Two Numbers in an Array (LeetCode 421).

Pattern: binary trie (the bridge between bit manipulation and tries).

PROBLEM
-------
Given an integer array `nums`, return the maximum value of nums[i] ^ nums[j],
where 0 <= i <= j < len(nums).

CONSTRAINTS
-----------
- 1 <= len(nums) <= 2 * 10**5
- 0 <= nums[i] <= 2**31 - 1

EXAMPLES
--------
- find_maximum_xor([3, 10, 5, 25, 2, 8]) -> 28   (5 ^ 25 == 28)
- find_maximum_xor([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]) -> 127
- find_maximum_xor([0]) -> 0

FRAME CHECKLIST
----------------
- Frame: maximize the XOR over all pairs.
- Research constraints: brute force is O(n^2); for n up to 2*10**5 that is
  4*10**10 — too slow. That points at a binary trie. Insert every number
  MSB-first as a 32-bit path (alphabet {0, 1}). For each number, greedily
  walk the trie choosing the OPPOSITE bit when a child exists (bit ^ opp == 1
  contributes to the XOR), else the same bit. Accumulate the XOR.
  Why MSB-first: high bits dominate magnitude; commit them first.
- Assess options: 1) build the trie: for each num, descend bits 31..0 with
  setdefault. 2) for each num, walk the trie preferring 1 - bit; build the
  XOR. 3) track the running max.
- Make the solution: see below. HIGH_BIT = 31 covers 0..2**31 - 1.
- Examine (verify): trace [3, 10, 5, 25, 2, 8] -> 28; check single-element
  [0] -> 0.
- Examine (cost): O(n * 32) time, O(n * 32) trie space. Beats the O(n^2)
  brute force.
"""

from typing import Any, Dict, List

HIGH_BIT = 31  # non-negative 32-bit integers occupy bits 31..0


def find_maximum_xor(nums: List[int]) -> int:
    """Return the maximum nums[i] ^ nums[j] using a binary trie. O(n * 32)."""
    # TODO:
    #   root: Dict[int, Any] = {}
    #   1) Insert each number MSB-first:
    #        for bit_pos in range(HIGH_BIT, -1, -1):
    #            bit = (num >> bit_pos) & 1
    #            node = node.setdefault(bit, {})
    #   2) For each number, greedily walk choosing want = 1 - bit when present,
    #      OR-ing (1 << bit_pos) into the running value when the opposite bit
    #      is available; otherwise descend into the same bit.
    #   3) Track and return the maximum running value.
    raise NotImplementedError


if __name__ == "__main__":
    assert find_maximum_xor([3, 10, 5, 25, 2, 8]) == 28
    assert find_maximum_xor([0]) == 0
    assert find_maximum_xor([2, 4]) == 6
    assert find_maximum_xor([8, 10, 2]) == 10
    assert (
        find_maximum_xor(
            [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]
        )
        == 127
    )
    # Cross-check against the brute force on a small input.
    sample = [3, 10, 5, 25, 2, 8]
    brute = max(a ^ b for a in sample for b in sample)
    assert find_maximum_xor(sample) == brute
    print("exercise-03-maximum-xor: all tests passed")
