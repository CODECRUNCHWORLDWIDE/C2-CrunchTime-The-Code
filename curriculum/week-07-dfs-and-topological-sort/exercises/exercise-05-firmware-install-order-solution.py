"""exercise-05-firmware-install-order-solution.py — install a rack's firmware in order.

Depth-first search, post-order. Finish a package, then append it. Because a
package is only appended once everything below it is already on the list, the
order is built bottom-up with no reversing and no waiting-count table.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
RACK: dict[str, list[str]] = {
    "analyzer-ui": ["chart-widgets", "measure-core"],
    "chart-widgets": ["render-gl"],
    "measure-core": ["bus-driver", "calibration-tables"],
    "logger": ["alarm-led", "measure-core", "storage-fs"],
    "storage-fs": ["bus-driver"],
}

# bus-driver requires sensor-io and sensor-io requires bus-driver. Neither can
# be installed first, so neither can be installed at all.
TANGLED: dict[str, list[str]] = {
    "bus-driver": ["sensor-io"],
    "sensor-io": ["bus-driver"],
}


# ---- Your task ----
def install_order(requires: dict[str, list[str]]) -> list[str]:
    """Return an order in which every package follows everything it requires.

    Args:
        requires: Maps a package to the packages that must already be
            installed. A package named only as a requirement, never as a key,
            is still a package and still appears in the order.

    Returns:
        Every package exactly once, each one after everything it requires.
        Top-level packages are entered in sorted order and each package's
        requirements are walked in sorted order, so the order is one specific
        list rather than any legal one. An empty manifest gives an empty list.

    Raises:
        ValueError: If the requirements contain a loop. The message spells the
            loop out, e.g. "requirement loop: a -> b -> a".
    """
    packages: set[str] = set(requires)
    for needed in requires.values():
        packages.update(needed)

    order: list[str] = []
    finished: set[str] = set()
    path: list[str] = []
    on_path: set[str] = set()

    def visit(package: str) -> None:
        """Install everything `package` needs, then record `package` itself."""
        if package in finished:
            return
        if package in on_path:
            trail = path[path.index(package) :] + [package]
            raise ValueError("requirement loop: " + " -> ".join(trail))
        path.append(package)
        on_path.add(package)
        for needed in sorted(requires.get(package, [])):
            visit(needed)
        on_path.discard(package)
        path.pop()
        finished.add(package)
        order.append(package)

    for package in sorted(packages):
        visit(package)
    return order


# ---- Self-check ----
if __name__ == "__main__":
    rack_order = install_order(RACK)
    print(f"empty manifest : {install_order({})}")
    print(f"one package    : {install_order({'bus-driver': []})}")
    print(f"rack order     : {rack_order}")
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        print(f"tangled rack   : {refusal}")

    assert install_order({}) == []
    assert install_order({"bus-driver": []}) == ["bus-driver"]
    assert install_order({"logger": ["storage-fs"]}) == ["storage-fs", "logger"]
    assert rack_order == [
        "alarm-led",
        "render-gl",
        "chart-widgets",
        "bus-driver",
        "calibration-tables",
        "measure-core",
        "analyzer-ui",
        "storage-fs",
        "logger",
    ]
    assert sorted(rack_order) == sorted(
        set(RACK) | {name for needed in RACK.values() for name in needed}
    )
    for package, needed_by_it in RACK.items():
        for needed in needed_by_it:
            assert rack_order.index(needed) < rack_order.index(package)
    try:
        install_order(TANGLED)
    except ValueError as refusal:
        assert str(refusal) == "requirement loop: bus-driver -> sensor-io -> bus-driver"
    else:
        raise AssertionError("a requirement loop should have been refused")
    print("All checks passed.")
