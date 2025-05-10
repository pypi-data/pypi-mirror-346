import sys
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import tqdm

from sloths import Stream
from sloths.ext.concurrent import imap_with_executor_as_completed


def part_sum(batch: Iterable[str]) -> int:
    """Parse and sum a batch of lines."""
    return sum(int(x.strip()) for x in batch if x.strip())


def compute(
    filename: str,
    batch_size: int = 16_000,
    workers: int = 4,
) -> int:
    with (
        Path(filename).open() as f,
        ProcessPoolExecutor(max_workers=workers) as e,
        tqdm.tqdm(desc="Lines read") as read_pb,
        tqdm.tqdm(desc="Batches ready") as batches_pb,
        tqdm.tqdm(desc="Batches summed") as summed_pb,
    ):
        return (
            Stream(f)
            .inspect(lambda _: read_pb.update(1))
            .batch(batch_size)
            .inspect(lambda _: batches_pb.update(1))
            .pipe(
                imap_with_executor_as_completed,
                part_sum,
                executor=e,
                prefetch=workers * 2,
            )
            .inspect(lambda _: summed_pb.update(1))
            .fold(lambda x, y: x + y, 0)
        )


if __name__ == "__main__":
    compute(sys.argv[-1])
