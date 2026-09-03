# Week 10 — Challenges

Two challenge problems. Challenge 1 is the **required** weekly challenge; Challenge 2 is **optional stretch** for learners ahead of schedule by Friday.

| # | Title | LC | Pattern | Required? |
|---|-------|---:|---------|-----------|
| 1 | [The Reefer Transfer Budget](./challenge-01-reefer-transfer-budget.md) | Bounded hops, and what that does to the state | Yes |
| 2 | [The Gantry Swap Groups](./challenge-02-gantry-swap-groups.md) | Union-find composed with a sort | Optional |

Challenge 1 is the required rep because it forces you to articulate the **algorithm choice** out loud: repeated relaxing bounded by the hop budget, against the frontier picker with the state widened to `(place, hops used)`. Both work. Owning both forms and defending the trade between them is the senior signal, and it is a question a mock will ask directly.

The optional the gantry swap groups is the composition problem of the week — DSU to find the swap-equivalence classes, then sort within each class. Recognition is the work.

Each challenge is graded against the rubric in [`homework.md`](../homework/README.md#rubric).
