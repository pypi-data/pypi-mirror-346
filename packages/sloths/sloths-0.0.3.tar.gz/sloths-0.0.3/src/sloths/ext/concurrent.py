"""
Extensions to work with :py:mod:`concurrent.futures` executors.
"""

from __future__ import annotations

import contextlib
from collections import deque
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import islice
from time import perf_counter
from typing import TYPE_CHECKING, Literal, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from concurrent.futures import Executor, Future


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")


if TYPE_CHECKING:
    from collections.abc import Iterable


def imap_with_executor(
    iterable: Iterable[T],
    fn: Callable[[T], U],
    *,
    executor: Executor,
    timeout_seconds: float | None = None,
    prefetch: int = 128,
    greedy: bool = False,
) -> Iterable[U]:
    """
    Lazy version of :py:class:`concurrent.futures.Executor.map`.

    Execute an element-wise transform within an execurtor and return values in
    order.

    :py:class:`concurrent.futures.Executor.map` consumes the source iterator
    early which is not desirable when working with lazy iterator. This is a
    version which does not consume the entire source iterator at once and
    maintains the order of the source iterator.

    Exceptions will interrupt the iteration.

    :param iterable: The source iterable

    :param fn: The mapper function to apply element-wise.

    :param executor: The :py:class:`concurrent.futures.Executor` to use.

    :param timeout_seconds: The overall timeout for the entire operation.

    :param prefetch: Control the number of items to read from the source stream
        and feed into the executor on startup. Must be 1 or higher.

    :param greedy: Control whether we pull from the source iterable when any
        task completes or only when the head task completes.

        The latter means this will only consume the source up last completed
        task (or ``prefetch`` if it's higher) but risk keeping the executor
        idle if the head task is slower than average. The former will maximise
        keeping the executor fed but will possibly consume past the head task in
        case of short circuit.
    """
    from concurrent.futures import wait

    if timeout_seconds is not None:
        if timeout_seconds < 0:
            msg = "`timeout_seconds` must be at least 0"
            raise ValueError(msg)

        end_time = timeout_seconds + perf_counter()
    else:
        end_time = None

    if prefetch < 1:
        msg = "`prefetch` must be at least 1"
        raise ValueError(msg)

    args = iter(iterable)
    futures = deque(executor.submit(fn, x) for x in islice(args, prefetch))

    try:
        while True:
            if futures:
                if greedy:
                    # To keep the executor fed as much as possible at the cost
                    # of possibly consuming the source values while we may not
                    # need the results.
                    wait_timeout = (
                        end_time - perf_counter()
                        if end_time is not None
                        else None
                    )
                    done, _ = wait(
                        [*futures],
                        timeout=wait_timeout,
                        return_when="FIRST_COMPLETED",
                    )
                    with contextlib.suppress(StopIteration):
                        for x in islice(args, len(done)):
                            futures.append(executor.submit(fn, x))

                wait_timeout = (
                    end_time - perf_counter() if end_time is not None else None
                )
                yield futures.popleft().result(timeout=wait_timeout)

                if not greedy:
                    with contextlib.suppress(StopIteration):
                        # This may not be optimal in term of keeping the
                        # executor fed. We're only consuming from the source
                        # iterator one by one as we complete in order, so in the
                        # worse case where the first future resolves last we'd
                        # only feed the prefetch number into the executor and
                        # then wait.
                        futures.append(executor.submit(fn, next(args)))
            else:
                return
    finally:
        for f in futures:
            f.cancel()


def imap_with_executor_as_completed(
    iterable: Iterable[T],
    fn: Callable[[T], U],
    *,
    executor: Executor,
    timeout_seconds: float | None = None,
    prefetch: int = 128,
) -> Iterable[U]:
    """
    Lazy version of :py:func:`concurrent.futures.as_completed`.

    Execute an element-wise transform within an execurtor and return values as
    they complete.

    :py:func:`concurrent.futures.as_completed` consumes the source iterator
    early which is not desirable when working with lazy iterator. This is a
    version which does not consume the entire source iterator at once and
    also yields futures in the order they complete.

    Exceptions will interrupt the iteration.

    :param iterable: The source iterable

    :param fn: The mapper function to apply element-wise.

    :param executor: The :py:class:`concurrent.futures.Executor` to use.

    :param timeout_seconds: The overall timeout for the entire operation.

    :param prefetch: Control the number of items to read from the source stream
        and feed into the executor on startup. Must be 1 or higher.
    """
    from concurrent.futures import wait

    if timeout_seconds is not None:
        if timeout_seconds < 0:
            msg = "`timeout_seconds` must be at least 0"
            raise ValueError(msg)

        end_time = timeout_seconds + perf_counter()
    else:
        end_time = None

    if prefetch < 1:
        msg = "`prefetch` must be at least 1"
        raise ValueError(msg)

    args = iter(iterable)

    pending: set[Future[U]] = set()
    finished: list[Future[U]] = []

    def _submit(x: T) -> None:
        f = executor.submit(fn, x)
        pending.add(f)
        f.add_done_callback(finished.append)

    for x in islice(args, prefetch):
        _submit(x)

    try:
        while True:
            wait_timeout = (
                end_time - perf_counter() if end_time is not None else None
            )

            _, pending = wait(
                pending,
                timeout=wait_timeout,
                return_when="FIRST_COMPLETED",
            )
            done = [*finished]
            finished.clear()

            with contextlib.suppress(StopIteration):
                for x in islice(args, len(done)):
                    _submit(x)

            for x in done:
                yield x.result()

            if not pending:
                return
    finally:
        for f in pending:
            f.cancel()


def threaded_map(
    it: Iterable[T],
    fn: Callable[[T], U],
    max_workers: int,
    timeout_seconds: float | None = None,
    prefetch: int | None = None,
    mode: Literal["ordered", "as_completed"] = "ordered",
) -> Iterable[U]:
    """
    Threaded element-wise transform.

    This instantiates a :py:class:`~concurrent.futures.ThreadPoolExecutor`
    behind the scenes.

    :param iterable: The source iterable

    :param fn: The mapper function to apply element-wise.

    :param max_workers: The number of workers to use.

    :param timeout_seconds: The overall timeout for the entire operation.

    :param prefetch: Control the number of items to read from the source stream
        and feed into the executor on startup. Must be 1 or higher,
        defaults to ``max_workers``.

    :param ordered:
        If ``True`` (default) the the results will be returned in the order of
        the source iterator regardless of their order of execution by the
        threadpool.

        .. warning::
            If ``False`` then worst case scenario (first element resolves last)
            will buffer all results in memory which may not be acceptable. If
            this is likely to happen; consumer can chunk or rate limit their
            input to create  an implicit ceiling to the memory usage.

    Usage:

    >>> from sloths import Stream
    >>> def proc(n):
    ...     # Do something blocking
    ...     return n + 1
    >>> Stream(range(10)).pipe(threaded_map, proc, max_workers=4).collect()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    with ThreadPoolExecutor(max_workers=max_workers) as e:
        if mode == "ordered":
            yield from imap_with_executor(
                it,
                fn,
                timeout_seconds=timeout_seconds,
                executor=e,
                prefetch=prefetch or max_workers,
            )
        else:
            yield from imap_with_executor_as_completed(
                it,
                fn,
                timeout_seconds=timeout_seconds,
                executor=e,
                prefetch=prefetch or max_workers,
            )
