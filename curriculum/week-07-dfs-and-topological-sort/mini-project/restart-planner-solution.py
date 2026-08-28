"""restart-planner-solution.py - the plant restart planner.

A dairy line has been shut down for its annual clean. Every stage in the plant
needs some other stages running before it can be started, and the shift
supervisor needs four things before anyone touches a switch:

  1. Is the plan even startable, or do two stages each wait on the other?
  2. One legal order to start everything in, single file.
  3. The crew waves - which stages can be started at the same moment.
  4. How much of the plant is holding up each stage, and which chain is
     longest, because that chain is how long the restart takes.

Every walk in this file keeps its pending work in a list on the heap rather
than on Python's call stack, so the same planner runs on a fifteen-stage dairy
line and on a twenty-thousand-stage chain without changing a line. The scale
check at the bottom proves it.

Run it:  python restart-planner-solution.py
"""

from __future__ import annotations

import heapq

# Three colours, and they mean exactly what Lecture 3 says they mean.
# WHITE: not started. GREY: on the path I am standing on right now.
# BLACK: finished, and everything under it is proved clean.
WHITE, GREY, BLACK = 0, 1, 2

# ---- The plant ----
# stage -> the stages that must already be running before it can start.
NEEDS: dict[str, list[str]] = {
    "air-compressor": [],
    "boiler": ["softener"],
    "capper": ["filler", "air-compressor"],
    "case-packer": ["capper", "labeller"],
    "chiller": ["well-pump"],
    "cip-loop": ["steam-header", "softener"],
    "filler": ["pasteuriser", "cip-loop", "air-compressor"],
    "glycol-loop": ["chiller"],
    "homogeniser": ["pasteuriser"],
    "labeller": ["filler"],
    "pasteuriser": ["steam-header", "glycol-loop", "cip-loop"],
    "silo-agitator": ["well-pump"],
    "softener": ["well-pump"],
    "steam-header": ["boiler"],
    "well-pump": [],
}

# Last year somebody typed the glycol loop into the well pump's needs. The
# plant would not start, and nobody could say why. This is that plan.
BROKEN_NEEDS: dict[str, list[str]] = {**NEEDS, "well-pump": ["glycol-loop"]}


def every_stage(needs: dict[str, list[str]]) -> list[str]:
    """Every stage named anywhere in the plan, sorted.

    A stage that only ever appears in somebody else's needs list is still a
    stage. Missing them is the quietest bug in this whole family of problems:
    the plan looks fine and the order comes out short.
    """
    seen = set(needs)
    for wants in needs.values():
        seen.update(wants)
    return sorted(seen)


def tidy_plan(needs: dict[str, list[str]]) -> dict[str, list[str]]:
    """The plan with every stage present as a key and no repeated needs.

    The maintenance system emits the same dependency from two different forms,
    so `["softener", "softener"]` is normal input. Counting it twice would tell
    the planner that the boiler is waiting on two things when it is waiting on
    one, and the boiler would never be released.
    """
    tidy = {stage: [] for stage in every_stage(needs)}
    for stage, wants in needs.items():
        tidy[stage] = sorted(dict.fromkeys(wants))
    return tidy


def find_need_loop(needs: dict[str, list[str]]) -> list[str] | None:
    """One circular wait, or None when the plan is sound.

    The loop is returned in "needs" order and rotated so it begins at the
    alphabetically smallest stage in it, so the same plan always reports the
    same loop the same way round.
    """
    plan = tidy_plan(needs)
    colour = {stage: WHITE for stage in plan}

    for start in sorted(plan):
        if colour[start] != WHITE:
            continue
        colour[start] = GREY
        path = [start]
        stack = [(start, iter(plan[start]))]

        while stack:
            stage, pending = stack[-1]
            stepped_down = False
            for nxt in pending:
                if colour[nxt] == GREY:
                    loop = path[path.index(nxt) :]
                    spin = loop.index(min(loop))
                    return loop[spin:] + loop[:spin]
                if colour[nxt] == WHITE:
                    colour[nxt] = GREY
                    path.append(nxt)
                    stack.append((nxt, iter(plan[nxt])))
                    stepped_down = True
                    break
            if not stepped_down:
                colour[stage] = BLACK
                path.pop()
                stack.pop()
    return None


def restart_order(needs: dict[str, list[str]]) -> list[str]:
    """One legal single-file start order: smallest ready stage first."""
    plan = tidy_plan(needs)
    waiting_on = {stage: len(plan[stage]) for stage in plan}
    unlocks: dict[str, list[str]] = {stage: [] for stage in plan}
    for stage, wants in plan.items():
        for want in wants:
            unlocks[want].append(stage)

    ready = [stage for stage in plan if waiting_on[stage] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        stage = heapq.heappop(ready)
        order.append(stage)
        for later in unlocks[stage]:
            waiting_on[later] -= 1
            if waiting_on[later] == 0:
                heapq.heappush(ready, later)

    if len(order) != len(plan):
        loop = find_need_loop(needs) or []
        raise ValueError("restart plan has a loop: " + " -> ".join(loop + loop[:1]))
    return order


def restart_waves(needs: dict[str, list[str]]) -> list[list[str]]:
    """The same start order, grouped into waves the crew can run at once."""
    plan = tidy_plan(needs)
    waiting_on = {stage: len(plan[stage]) for stage in plan}
    unlocks: dict[str, list[str]] = {stage: [] for stage in plan}
    for stage, wants in plan.items():
        for want in wants:
            unlocks[want].append(stage)

    wave = sorted(stage for stage in plan if waiting_on[stage] == 0)
    waves: list[list[str]] = []
    started = 0
    while wave:
        waves.append(wave)
        started += len(wave)
        freed: list[str] = []
        for stage in wave:
            for later in unlocks[stage]:
                waiting_on[later] -= 1
                if waiting_on[later] == 0:
                    freed.append(later)
        wave = sorted(freed)

    if started != len(plan):
        loop = find_need_loop(needs) or []
        raise ValueError("restart plan has a loop: " + " -> ".join(loop + loop[:1]))
    return waves


def stages_underneath(needs: dict[str, list[str]]) -> dict[str, int]:
    """How many distinct stages must already be running under each stage."""
    plan = tidy_plan(needs)
    beneath: dict[str, set[str]] = {}
    for stage in restart_order(needs):
        pool: set[str] = set()
        for want in plan[stage]:
            pool.add(want)
            pool |= beneath[want]
        beneath[stage] = pool
    return {stage: len(pool) for stage, pool in beneath.items()}


def longest_chain(needs: dict[str, list[str]]) -> list[str]:
    """The longest run of stages that must be started one after another."""
    plan = tidy_plan(needs)
    order = restart_order(needs)
    depth: dict[str, int] = {}
    beneath: dict[str, str | None] = {}
    for stage in order:
        best, best_from = 0, None
        for want in plan[stage]:
            if depth[want] > best:
                best, best_from = depth[want], want
        depth[stage] = best + 1
        beneath[stage] = best_from

    last = min(order, key=lambda stage: (-depth[stage], stage))
    chain: list[str] = []
    walker: str | None = last
    while walker is not None:
        chain.append(walker)
        walker = beneath[walker]
    chain.reverse()
    return chain


def print_report(needs: dict[str, list[str]]) -> None:
    """The whole restart report, in the order the supervisor reads it."""
    plan = tidy_plan(needs)
    links = sum(len(wants) for wants in plan.values())
    loop = find_need_loop(needs)

    if loop is not None:
        print(f"audit          : loop found - {' -> '.join(loop + loop[:1])}")
        print("                 nothing can start; fix the loop, then re-plan")
        return

    print(f"audit          : {len(plan)} stages, {links} dependencies, no loops")
    print()

    print("start order    : smallest ready stage first")
    for position, stage in enumerate(restart_order(needs), 1):
        print(f"  {position:2d}  {stage}")
    print()

    waves = restart_waves(needs)
    print(f"crew waves     : {len(waves)} waves, every stage in a wave starts at once")
    for number, wave in enumerate(waves, 1):
        print(f"  wave {number}  {', '.join(wave)}")
    print()

    underneath = stages_underneath(needs)
    print("holding up     : distinct stages that must already be running")
    for stage in sorted(underneath, key=lambda s: (-underneath[s], s)):
        print(f"  {underneath[stage]:2d}  {stage}")
    print()

    chain = longest_chain(needs)
    print(f"longest chain  : {len(chain)} stages, one after another")
    print(f"  {' -> '.join(chain)}")


def _straight_chain(length: int) -> dict[str, list[str]]:
    """A plan that is one stage deep, `length` stages long."""
    plan = {"stage-00000": []}
    for index in range(1, length):
        plan[f"stage-{index:05d}"] = [f"stage-{index - 1:05d}"]
    return plan


if __name__ == "__main__":
    print("=== restart plan: line 2, after the annual clean ===")
    print_report(NEEDS)
    print()

    print("=== the same audit on last year's typed-in-wrong plan ===")
    print_report(BROKEN_NEEDS)
    print()

    # The plant is fifteen stages deep at most. The scale check is the reason
    # every walk above uses an explicit stack anyway: twenty thousand stages in
    # a straight line is twenty times CPython's default 1000-frame limit, and a
    # recursive version of any of these functions dies on it.
    deep = _straight_chain(20_000)
    assert find_need_loop(deep) is None
    assert restart_order(deep)[:2] == ["stage-00000", "stage-00001"]
    assert len(restart_order(deep)) == 20_000
    assert len(restart_waves(deep)) == 20_000
    assert longest_chain(deep)[-1] == "stage-19999"

    assert find_need_loop({"a": ["a"]}) == ["a"]
    assert find_need_loop({}) is None
    assert restart_order({}) == []
    assert restart_waves({}) == []
    assert restart_order({"boiler": ["softener", "softener"]}) == ["softener", "boiler"]
    assert every_stage({"filler": ["capper"]}) == ["capper", "filler"]

    print("=== scale check ===")
    print("20000-stage chain: audited, ordered, waved, measured - no recursion used")
    print()
    print("all checks passed")
