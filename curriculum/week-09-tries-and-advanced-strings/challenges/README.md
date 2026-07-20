# Week 9 — Challenges

Two challenges. The first is required; the second is optional stretch.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [Word Search II](./challenge-01-word-search-ii.md) (LC 212) | Trie + DFS on grid (the canonical composition) | Hard | 60 min |
| 2 | [Replace Words](./challenge-02-replace-words.md) (LC 648) | Trie of roots; shortest-prefix replacement | Medium | 40 min |

The challenges scale the trie pattern beyond the canonical three operations. Challenge 1 composes the trie with backtracking DFS over a 2-D grid — the highest-yield trie problem in the Phase-2 portfolio. Challenge 2 is a recognition rep on the "given a dictionary of roots, replace each word by its shortest root" family.

By Sunday of Week 9, you must have a clean UMPIRE write-up of Challenge 1. Challenge 2 is stretch; do it if Friday goes well.

---

## What a complete challenge write-up looks like

For each challenge, the deliverable is:

1. **A UMPIRE write-up** — under `umpire-writeups/c2-week-09/challenges/`. Full six sections; the Match section opens with the 30-second pattern-recognition memo from the challenge file.
2. **A working implementation** — committed as `challenges/<challenge-name>.py` in your portfolio. Must pass the test cases listed in the challenge file.
3. **A recording** — minimum 10 minutes, walking through the Match → Plan → Implement narration. The Review and Evaluate sections can be brief if the implementation is clean.

The challenges grade *recognition speed* and *defense quality*. Implementation correctness is the entry bar; defending the algorithm choice over alternatives is what earns the senior signal.

---

## A note on the trie-on-grid composition

Challenge 1 is the highest-yield trie problem in Phase 2. Three reasons:

1. **It composes two patterns** — trie (W9) + DFS (W7). Composition is the Phase-2 discriminator; single-pattern problems are Phase-1 work.
2. **The naive solution is `O(W * m * n * 4^L)`** — for 50 words of length 10 on a 12x12 grid, that is over `10^9`. The trie solution drops the `W` factor by sharing dictionary prefixes across the DFS, getting to `O(m * n * 4^L)` — about `10^7`, three orders of magnitude cheaper.
3. **The implementation has three subtle bugs** that show up in interviews. Read the challenge file's "Common bugs" section before you start — knowing the bug list shortens your debug cycle by 20 minutes.

If you only ship one challenge this week, ship this one. The Replace Words stretch is recognition-rep practice; Word Search II is the portfolio piece.
