"""problem-05-rolling-error-rate-solution.py — a window over time, not over a list.

The algorithmic sliding window moves over positions in a list. A production
alerting system moves a window over the clock: "what fraction of the last
sixty seconds of requests failed?" Same idea, different axis, and the same two
rules — add on the right, drop on the left, keep the totals rather than
recounting.

The state here is a queue of one-second buckets plus two running integers. A
bucket that falls out of the sixty-second horizon is popped and subtracted, so
answering "what is the rate right now" is a division, not a scan.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import deque


class RollingRate:
    """A failure rate over the most recent `horizon` seconds of traffic."""

    def __init__(self, horizon: int) -> None:
        """Create an empty window.

        Args:
            horizon: How many seconds of traffic the window covers.
        """
        self.horizon = horizon
        self.buckets: deque[list[int]] = deque()  # [second, requests, failures]
        self.requests = 0
        self.failures = 0

    def record(self, second: int, requests: int, failures: int) -> None:
        """Fold one second of traffic into the window.

        Args:
            second: The whole second the traffic belongs to, non-decreasing
                across calls.
            requests: How many requests that second served.
            failures: How many of them failed.
        """
        self.buckets.append([second, requests, failures])
        self.requests += requests
        self.failures += failures
        self._drop_stale(second)

    def _drop_stale(self, now: int) -> None:
        """Remove buckets that have fallen out of the horizon.

        Args:
            now: The current second.
        """
        while self.buckets and self.buckets[0][0] <= now - self.horizon:
            _, requests, failures = self.buckets.popleft()
            self.requests -= requests
            self.failures -= failures

    def rate(self) -> float:
        """Return the failure rate over the window, as a fraction of one.

        Returns:
            failures / requests, or 0.0 when the window saw no requests.
        """
        if self.requests == 0:
            return 0.0
        return self.failures / self.requests


def first_alert(
    traffic: list[tuple[int, int, int]],
    horizon: int = 60,
    threshold: float = 0.01,
    minimum_requests: int = 100,
) -> tuple[int, float] | None:
    """Return the first second at which the rolling failure rate trips.

    Args:
        traffic: (second, requests, failures) triples, in time order.
        horizon: How many seconds the window covers.
        threshold: The failure rate that must be exceeded, as a fraction.
        minimum_requests: How many requests the window needs before the rate
            is trusted. Without this, one failed request out of one is a
            hundred per cent and every quiet minute pages somebody.

    Returns:
        (second, rate) for the first second whose window is over threshold, or
        None when the window never trips.
    """
    window = RollingRate(horizon)
    for second, requests, failures in traffic:
        window.record(second, requests, failures)
        if window.requests >= minimum_requests and window.rate() > threshold:
            return (second, window.rate())
    return None


def scripted_traffic() -> list[tuple[int, int, int]]:
    """Return five minutes of made-up but entirely predictable traffic.

    Forty requests a second throughout. For the first three minutes one
    request fails every twenty-five seconds — background noise, well under
    one per cent. From second 180 a bad deploy fails two requests a second,
    which is five per cent, and the rolling window has to notice.

    Returns:
        (second, requests, failures) triples for seconds 0 to 299.
    """
    traffic = []
    for second in range(300):
        if second >= 180:
            failures = 2
        elif second % 25 == 0:
            failures = 1
        else:
            failures = 0
        traffic.append((second, 40, failures))
    return traffic


# ---- Self-check ----
if __name__ == "__main__":
    traffic = scripted_traffic()
    alert = first_alert(traffic)
    second, rate = alert

    print("five minutes of traffic, 40 requests a second")
    print("  bad deploy starts at second 180, failing 2 requests a second")
    print(f"  first alert at second {second}, rolling rate {rate * 100:.2f}%")
    print(f"  that is {second - 180} seconds after the deploy went out")
    print()

    quiet = RollingRate(60)
    for tick in range(120):
        quiet.record(tick, 40, 0)
    print(f"a clean window holds {quiet.requests} requests and reports {quiet.rate() * 100:.2f}%")
    print(f"buckets kept in memory: {len(quiet.buckets)}, not {120}")
    print()

    assert alert == (191, 26 / 2400)
    assert first_alert(traffic[:180]) is None
    assert first_alert([]) is None
    # One failure out of one request is 100%, and must not page anyone.
    assert first_alert([(0, 1, 1)]) is None
    # The same burst with the minimum lowered does trip, immediately.
    assert first_alert([(0, 1, 1)], minimum_requests=1) == (0, 1.0)

    # The window really only ever holds `horizon` buckets.
    assert len(quiet.buckets) == 60
    assert quiet.requests == 60 * 40
    assert quiet.rate() == 0.0

    # Running totals agree with a from-scratch count of the buckets kept.
    window = RollingRate(60)
    for row in traffic[:250]:
        window.record(*row)
    assert window.requests == sum(bucket[1] for bucket in window.buckets)
    assert window.failures == sum(bucket[2] for bucket in window.buckets)

    print("All checks passed.")
