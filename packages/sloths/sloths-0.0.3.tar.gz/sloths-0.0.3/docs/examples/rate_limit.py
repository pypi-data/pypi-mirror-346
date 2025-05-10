from __future__ import annotations

import sys
from collections.abc import Iterable
from time import perf_counter, sleep
from typing import TypeVar

from sloths import Stream

T = TypeVar("T")


def rate_limit(it: Iterable[T], *, interval_seconds: float) -> Iterable[T]:
    """
    A very basic rate limiting transform which allows at most one item per
    ``interval_seconds`` interval.
    """
    iterator = iter(it)

    try:
        last_yield = perf_counter()
        yield next(iterator)
    except StopIteration:
        return

    while True:
        since_last_yield = perf_counter() - last_yield
        if since_last_yield < interval_seconds:
            # This technically adds some tiny wall time over the rate
            # limit which is acceptable in most cases.
            #
            # Putting the sleep before the yield also means we'll poll upstream
            # at most once per interval, we could move it after the yield to
            # only make values available within the limit but poll as fast as we
            # can.
            sleep(interval_seconds - since_last_yield)
        try:
            last_yield = perf_counter()
            yield next(iterator)
        except StopIteration:
            return


if __name__ == "__main__":
    start = perf_counter()

    size = int(sys.argv[-2])
    limit = float(sys.argv[-1])

    Stream(range(size)).inspect(lambda x: print(">", x)).pipe(
        rate_limit,
        interval_seconds=limit,
    ).inspect(lambda x: print("<", x)).consume()

    assert perf_counter() - start >= limit * size
