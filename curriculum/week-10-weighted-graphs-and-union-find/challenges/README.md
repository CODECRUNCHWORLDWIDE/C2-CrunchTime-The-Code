# Week 10 — Challenges

Two challenge problems. Challenge 1 is the **required** weekly challenge; Challenge 2 is **optional stretch** for learners ahead of schedule by Friday.

| # | Title | LC | Pattern | Required? |
|---|-------|---:|---------|-----------|
| 1 | [Cheapest Flights Within K Stops (deep dive)](./challenge-01-cheapest-flights-k-stops.md) | 787 | Bellman-Ford vs Dijkstra-with-state | Yes |
| 2 | [Smallest String With Swaps](./challenge-02-smallest-string-with-swaps.md) | 1202 | DSU + sort composition | Optional |

The deep dive on LC 787 is the required rep because it forces you to articulate the **algorithm choice** out loud — Bellman-Ford bounded by `K + 1` passes versus modified Dijkstra with state `(node, hops)`. Owning both forms and defending the trade is the senior signal.

The optional Smallest String With Swaps is the composition problem of the week — DSU to find the swap-equivalence classes, then sort within each class. Recognition is the work.

Each challenge is graded against the rubric in [`homework.md`](../homework.md#rubric).
