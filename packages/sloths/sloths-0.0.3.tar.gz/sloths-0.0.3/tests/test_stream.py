import dataclasses
from collections.abc import Iterable
from unittest import mock

from sloths import Stream


def test_lazy_polling():
    class MaxTracker:
        def __init__(self) -> None:
            self.current = 0

        def __call__(self, x: int) -> None:
            self.current = max(self.current, x)

    tracker = MaxTracker()
    stream = Stream(range(10)).inspect(tracker).map(lambda _: tracker.current)

    # As we poll one by one the max should always be the current value.
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == list(stream)

    # If we force consume / unwind in an intermediate step:
    tracker = MaxTracker()
    stream = (
        Stream(range(10))
        .inspect(tracker)
        .batch(3)
        .flatten()
        .map(lambda _: tracker.current)
    )

    assert [2, 2, 2, 5, 5, 5, 8, 8, 8, 9] == list(stream)


def test_unwinding_order():
    # Stages can also define post-processing which only runs once the pipeline
    # has unwinded. Note that while useful this can be tricky to reason about in
    # case of buffering and inline unwinding.

    @dataclasses.dataclass
    class Entry:
        before: int
        after: int | None = None

    log = mock.Mock()

    def before(gen: Iterable[int]) -> Iterable[Entry]:
        for x in gen:
            yield Entry(before=x, after=None)

    def logger(gen: Iterable[Entry]) -> Iterable[Entry]:
        for x in gen:
            log(">> enter", x.before, x.after)
            yield x
            log("<< exit", x.before, x.after)

    def after(gen: Iterable[Entry]) -> Iterable[int]:
        for x in gen:
            x.after = x.before
            yield x.before

    pipeline = Stream(range(10)).pipe(before).pipe(logger).pipe(after)

    values = list(pipeline)
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == values

    assert [
        mock.call(">> enter", 0, None),
        mock.call("<< exit", 0, 0),
        mock.call(">> enter", 1, None),
        mock.call("<< exit", 1, 1),
        mock.call(">> enter", 2, None),
        mock.call("<< exit", 2, 2),
        mock.call(">> enter", 3, None),
        mock.call("<< exit", 3, 3),
        mock.call(">> enter", 4, None),
        mock.call("<< exit", 4, 4),
        mock.call(">> enter", 5, None),
        mock.call("<< exit", 5, 5),
        mock.call(">> enter", 6, None),
        mock.call("<< exit", 6, 6),
        mock.call(">> enter", 7, None),
        mock.call("<< exit", 7, 7),
        mock.call(">> enter", 8, None),
        mock.call("<< exit", 8, 8),
        mock.call(">> enter", 9, None),
        mock.call("<< exit", 9, 9),
    ] == log.call_args_list


def test_ack():
    # A slightly more useful example of unwinding with buffering for ACK type
    # behaviours.

    committed: list[list[int]] = []

    def mark_committed_on_backpropagation(gen: Iterable[Iterable[int]]):
        for x in gen:
            yield x
            # This runs after the yield which is essentially acknowledging
            # when the downstream consumers are starved and need to pool
            # back up.
            # This can act as a confirmation that the input has been fully
            # processed by the pipeline. For more complex case you could
            # pass through a mutable context and update flags through the
            # stages.
            # WARN: further buffering downstream might skew this as we'll
            # need to consume inputs to fill buffer and values will come
            # back up until the next buffer is full. The guarantees only
            # hold until the next unwinding and should be used carefully as
            # it is highly dependent on the pipeline's purpose.
            committed.append(list(x))

    pipeline = (
        Stream(range(100))
        # Create 10 lazy chunks, i.e. buffer the input
        .batch(10)
        # ACK chunks as they come back up the stack
        .pipe(mark_committed_on_backpropagation)
        # Downstream we only care about individual values
        .flatten()
        # This ensure we'll only partially consume the third chunk and as a
        # result only the first 2 chunks should be marked as committed.
        .take(25)
    )

    result = list(pipeline)

    assert list(range(25)) == result

    assert [list(range(10)), list(range(10, 20))] == committed
