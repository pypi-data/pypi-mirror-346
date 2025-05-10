import sys
from collections.abc import Iterable
from pathlib import Path


def compute_sequential(filename: str) -> int:
    """
    Given a file made of one integer per line read line by line and
    compute the sum of all lines.
    """
    from sloths import Stream

    with Path(filename).open() as f:
        return (
            Stream(f)
            .filter(lambda x: bool(x.strip()))
            .map(int)
            .fold(lambda x, y: x + y, 0)
        )


def part_sum(batch: Iterable[str]) -> int:
    """Parse and sum a batch of lines."""
    return sum(int(x.strip()) for x in batch if x.strip())


def compute_processpool(
    filename: str,
    batch_size: int = 16_000,
    workers: int = 4,
) -> int:
    """
    Given a file made of one integer per line read line by line and
    compute the sum of all lines across multiple processes by reading batches
    of lines and distributing the sum operation for the batches to individual
    processes.
    """
    from concurrent.futures import ProcessPoolExecutor

    from sloths import Stream
    from sloths.ext.concurrent import imap_with_executor_as_completed

    with (
        Path(filename).open() as f,
        ProcessPoolExecutor(max_workers=workers) as e,
    ):
        return (
            Stream(f)
            .batch(batch_size)
            .pipe(
                imap_with_executor_as_completed,
                part_sum,
                executor=e,
                prefetch=workers * 2,
            )
            .fold(lambda x, y: x + y, 0)
        )


if __name__ == "__main__":
    compute_processpool(sys.argv[-1])
