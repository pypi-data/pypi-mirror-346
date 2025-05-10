from __future__ import annotations

import itertools
from collections import deque
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

from typing import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")


def batch(it: Iterable[T], by: int) -> Iterable[tuple[T, ...]]:
    """
    Chunk an iterable into tuples of a given size.

    >>> list(batch(range(11), 2))
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10,)]

    >>> list(batch([], 2))
    []
    """
    iterator = iter(it)
    while True:
        chunk = tuple(itertools.islice(iterator, by))
        if not chunk:
            break
        yield chunk


def window(it: Iterable[T], size: int) -> Iterable[tuple[T, ...]]:
    """
    Create a sliding window of a specified size over the iterable.

    Each window is a tuple containing 'size' elements from the iterable.
    The windows overlap, with each window shifted one element to the right
    from the previous window.

    >>> list(window(range(5), 3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    >>> list(window([1, 2], 3))
    []

    >>> list(window([], 2))
    []
    """
    if size <= 0:
        msg = "Window size must be positive"
        raise ValueError(msg)

    iterator = iter(it)
    win = deque(itertools.islice(iterator, size), maxlen=size)

    if len(win) < size:
        return

    yield tuple(win)

    for elem in iterator:
        win.append(elem)
        yield tuple(win)
