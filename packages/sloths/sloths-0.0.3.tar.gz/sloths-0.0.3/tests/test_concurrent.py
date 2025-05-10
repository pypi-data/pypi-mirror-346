import random
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from typing import TypeVar

import pytest

from sloths import Stream
from sloths._utils import batch
from sloths.ext.concurrent import (
    imap_with_executor,
    imap_with_executor_as_completed,
    threaded_map,
)

T = TypeVar("T")


class Test_imap_with_executor:
    def test_empty(self):
        with ThreadPoolExecutor() as e:
            s: list[None] = []
            assert [] == list(imap_with_executor(s, lambda x: x, executor=e))

    def test_blocking(self):
        with ThreadPoolExecutor() as e:
            res = list(imap_with_executor(range(10), lambda x: x, executor=e))
        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == res

    def test_exception_interrupt(self):
        def fn(x: int) -> int:
            if x == 3:
                raise ValueError(3)
            return x

        source = iter(range(10))

        with pytest.raises(ValueError, match="3"), ThreadPoolExecutor() as e:
            list(imap_with_executor(source, fn, executor=e, prefetch=1))

        # With prefetch=1 we shouldn't be consuming the source iterator past the
        # exception trigger.
        assert next(source) == 4

    def test_yielding_enough_workers(self):
        done: list[int] = []

        def fn(x: int) -> int:
            time.sleep(0.1 - (x / 100))
            done.append(x)
            return x

        with ThreadPoolExecutor(max_workers=100) as e:
            res = list(imap_with_executor(range(10), fn, executor=e))

        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == res

        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary) despite yielding in order
        assert res != done

    def test_yielding_not_enough_workers(self):
        done: list[int] = []

        def fn(x: int) -> int:
            time.sleep(0.1 - (x / 100))
            done.append(x)
            return x

        with ThreadPoolExecutor(max_workers=2) as e:
            res = list(imap_with_executor(range(10), fn, executor=e))

        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == res

        # There's only ever 2 futures executing and we put them in order so the
        # reversing done by the sleep is staggered over pairs.
        assert [sorted(x) for x in batch(range(10), 2)] == (
            [sorted(x) for x in batch(done, 2)]
        )

        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary) despite yielding in order
        assert res != done

    def test_prefetch_only_fetches_required_count(self):
        done: list[int] = []

        def fn(x: int) -> int:
            # Modulo staggers the sleeps to better simulate our of order
            # execution
            time.sleep(0.1 - ((x % 10) / 100))
            done.append(x)
            return x

        it = iter(range(100))

        with ThreadPoolExecutor(max_workers=4) as e:
            res = list(
                islice(
                    imap_with_executor(
                        it,
                        fn,
                        executor=e,
                        prefetch=20,
                    ),
                    10,
                ),
            )

        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == res

        assert next(it) <= 30

        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary) despite yielding in order
        assert res != done

    def test_prefetch_greedy(self):
        done: list[int] = []

        def fn(x: int) -> int:
            # Modulo staggers the sleeps to better simulate our of order
            # execution
            time.sleep(0.1 - ((x % 10) / 100))
            done.append(x)
            return x

        it = iter(range(100))

        with ThreadPoolExecutor(max_workers=4) as e:
            res = list(
                islice(
                    imap_with_executor(
                        it,
                        fn,
                        executor=e,
                        prefetch=20,
                        greedy=True,
                    ),
                    10,
                ),
            )

        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == res

        # We should have fetched more than the previous test but still not
        # enough to consume the full source
        assert 30 < next(it) <= 40

        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary) despite yielding in order
        assert res != done


class Test_imap_with_executor_as_completed:
    def test_empty(self):
        with ThreadPoolExecutor() as e:
            s: list[None] = []
            assert [] == list(
                imap_with_executor_as_completed(
                    s,
                    lambda x: x,
                    executor=e,
                ),
            )

    def test_blocking(self):
        with ThreadPoolExecutor() as e:
            res = list(
                imap_with_executor_as_completed(
                    range(10),
                    lambda x: x,
                    executor=e,
                ),
            )
        # sorted() is important as even with a blocking function futures aren't
        # guaranteed to resolve in the order they are submitted.
        assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == sorted(res)

    def test_exception_interrupt(self):
        def fn(x: int) -> int:
            if x == 3:
                raise ValueError(3)
            return x

        source = iter(range(10))

        with pytest.raises(ValueError, match="3"), ThreadPoolExecutor() as e:
            list(
                imap_with_executor_as_completed(
                    source,
                    fn,
                    executor=e,
                    prefetch=1,
                ),
            )

        # With prefetch=1 we shouldn't be consuming the source iterator past the
        # exception trigger.
        assert next(source) is not None

    def test_yielding_enough_workers(self):
        done: list[int] = []

        def fn(x: int) -> int:
            time.sleep(0.1 - (x / 100))
            done.append(x)
            return x

        with ThreadPoolExecutor(max_workers=100) as e:
            res = list(
                imap_with_executor_as_completed(
                    range(10),
                    fn,
                    executor=e,
                ),
            )

        assert done == res
        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary)
        assert res != list(range(10))

    def test_yielding_not_enough_workers(self):
        done: list[int] = []

        def fn(x: int) -> int:
            time.sleep(0.1 - (x / 100))
            done.append(x)
            return x

        with ThreadPoolExecutor(max_workers=2) as e:
            res = list(
                imap_with_executor_as_completed(
                    range(10),
                    fn,
                    executor=e,
                ),
            )

        assert done == res
        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary)
        assert res != list(range(10))

    def test_prefetch_only_fetches_required_count(self):
        done: list[int] = []

        def fn(x: int) -> int:
            # Modulo staggers the sleeps to better simulate our of order
            # execution
            time.sleep(0.1 - ((x % 10) / 100))
            done.append(x)
            return x

        it = iter(range(100))

        with ThreadPoolExecutor(max_workers=4) as e:
            res = list(
                islice(
                    imap_with_executor_as_completed(
                        it,
                        fn,
                        executor=e,
                        prefetch=20,
                    ),
                    10,
                ),
            )

        assert len(res) == 10
        assert set(res).issubset(set(range(100)))
        assert next(it) <= 30

        # Check things resolved out of order (which the sleep should guarantee
        # although the exact order may vary)
        assert res != list(range(10))


# Needs to be here to be pickleable
def proc(x: int) -> int:
    time.sleep(random.randint(0, 100) / 10000)
    return x


def test_threaded_map_smoke():
    pipeline = Stream(range(100)).pipe(
        threaded_map,
        proc,
        max_workers=2,
        mode="ordered",
    )

    assert list(range(100)) == pipeline.collect()

    pipeline = Stream(range(100)).pipe(
        threaded_map,
        proc,
        max_workers=2,
        mode="as_completed",
    )

    assert list(range(100)) == sorted(pipeline.collect())
