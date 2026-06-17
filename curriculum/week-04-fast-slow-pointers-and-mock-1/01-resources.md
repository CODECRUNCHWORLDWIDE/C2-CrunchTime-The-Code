# Week 4 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Floyd's Cycle-Finding Algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Cycle_detection> — the canonical reference; covers Floyd's, Brent's, and the proofs.
- **Python data model — linked-list builders (chapter on classes)**: <https://docs.python.org/3/tutorial/classes.html> — refresher if it has been a while since you wrote a `class ListNode` by hand.
- **`unittest.mock` and recording tools — not standard library, but the system docs you'll need:** OBS Studio's quick-start (free): <https://obsproject.com/wiki/OBS-Studio-Quickstart>.
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>

## On the pattern itself

The fast/slow-pointer pattern has multiple names in the literature. They all refer to the same idea:

- **Floyd's cycle-finding algorithm** — the formal name.
- **Tortoise and hare** — Floyd's own metaphor.
- **Fast/slow pointers** — the interview-prep name.
- **Hare and tortoise** — same thing, different order.

If a write-up calls "two pointers from each end" a "fast/slow" approach, it's wrong; that's converging two-pointer. *Speed* is the discriminator.

## Free practice platforms

- **LeetCode — Linked List tag** (free): <https://leetcode.com/tag/linked-list/>
- **LeetCode — Two Pointers tag** (free): <https://leetcode.com/tag/two-pointers/> — the fast/slow problems live under this tag too.
- **HackerRank — Linked Lists track**: <https://www.hackerrank.com/domains/data-structures?filters%5Bsubdomains%5D%5B%5D=linked-lists>
- **Exercism — Python Track, linked-list exercises**: <https://exercism.org/tracks/python>

## Mock-interview platforms (peer-based, free tiers)

This is the week you'll actually use these.

- **Pramp** (free, peer-to-peer, you interview them then they interview you): <https://www.pramp.com/>
- **interviewing.io** (anonymous mocks; free tier limited but exists): <https://interviewing.io/>
- **A peer from C2 cohort** — best option. Schedule it on Discord/Slack, use Zoom or Meet.
- **Excalidraw** (free whiteboard for the visual part): <https://excalidraw.com/>
- **CoderPad sandbox** (free read-only template): <https://coderpad.io/sandbox> — same shell most real interviews use.
- **Solo mock with a recorder** — acceptable for Mock #1 if no peer available. Camera on, recorder running, talk to the camera as if it's an interviewer.

## Recording tools (free)

- **OBS Studio** — free, open-source, runs on macOS / Windows / Linux: <https://obsproject.com/>
- **QuickTime Player** (macOS only, built-in) — File → New Screen Recording. Click the dropdown arrow to enable internal mic.
- **Loom** (free tier: 25 videos, 5 min each — but for the mini-project's 45-minute mock you'll need OBS or QuickTime instead). <https://www.loom.com/>
- **Built into Zoom / Meet / Teams** — if you mock with a peer over video, every major platform has "record meeting" — use it.

## Videos on the pattern (free, no signup)

- **NeetCode — "Linked List Cycle" walkthrough** (YouTube — free): search "neetcode linked list cycle"; the 8-minute walkthrough is enough.
- **MIT 6.006 — Hashing lecture** (free OCW; the dictionary-with-window discussion at the end): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/> — tangential, but the *adjacency in a functional graph* idea connects to Happy Number.

## On *watching yourself* — the meta-skill

Mock #1 produces a video of yourself. Watching it is psychologically harder than doing it. Two short free reads on the meta-skill:

- *"How to watch a recording of yourself without flinching"* — search this phrase; multiple short blog posts. Pick one. The advice is consistent: first pass at 1.5×, second pass at 1.0× for the parts you flagged.
- The performing-arts literature on "self-tape critique" maps directly. Performers self-record audition tapes constantly; their feedback discipline is mature. Borrow it.

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1–3.

| Term | One-line definition |
|------|---------------------|
| **Linked list** | A sequence of nodes where each node points to the next |
| **Cycle** | A point in a linked list where a `.next` pointer goes back to an earlier node |
| **Fast pointer (hare)** | Advances two nodes per step |
| **Slow pointer (tortoise)** | Advances one node per step |
| **Floyd's algorithm** | Cycle detection using fast + slow pointers; O(n) time, O(1) space |
| **Cycle entrance** | The first node that is part of the cycle (where the non-cycle prefix meets the cycle) |
| **Functional graph** | A graph where every node has exactly one outgoing edge — e.g., `n -> sum_of_squares_of_digits(n)` |
| **Midpoint (lower)** | For a list of even length `2k`, node at index `k - 1` |
| **Midpoint (upper)** | For a list of even length `2k`, node at index `k` (this is what `slow` lands on with the speed-2 hare) |
| **Mock interview** | A timed, recorded interview simulation against a peer or solo against a camera |
| **Self-feedback rubric** | The structured grading checklist you apply to your own recording |
| **Behavior delta** | One specific thing you commit to changing for Mock #2 |
| **Reorder list** | The challenge problem: `L0 → L1 → … → Ln` becomes `L0 → Ln → L1 → Ln-1 → …` |
| **Brent's algorithm** | An alternative cycle-detection algorithm; faster in practice but Floyd's is the interview standard |

## What you'll be glad you read

Two things, both short, both this week:

1. **The Wikipedia "Cycle detection" article** — read sections on Floyd's specifically. The proof of the cycle-entrance lemma is one paragraph. Read it once; you'll re-derive it in Drill 2.
2. **One short blog post on how to set up an OBS recording for a coding interview** — most are 5-minute reads. Worth it Monday so Friday is friction-free.

If you read nothing else this week, read those two and skim the linked-list portion of LeetCode's "Linked List" tag titles.

---

*Broken link? Open an issue.*
