from __future__ import annotations

import enum
import functools
import itertools
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from typing import (
    Any,
    Concatenate,
    Generic,
    Literal,
    ParamSpec,
    TypeAlias,
    TypeVar,
    overload,
)

from ._utils import batch, window

T = TypeVar("T")
U = TypeVar("U")

P = ParamSpec("P")


class UNSET(enum.Enum):
    U = enum.auto()


Transform: TypeAlias = Callable[Concatenate[Iterable[T], P], Iterable[U]]


class Stream(Generic[T], Iterable[T]):
    """
    Typed interface to build lazy generator/coroutines pipelines.

    This technically works with any iterable but is primarily built to compose
    lazy-generator pipelines into a single iterator. When used with generators
    this provides good memory and throughput controls.

    None of this can't be achieved either by colocating everything in a single
    loop or composing generators outside-in by hand. This is a fairly light
    abstraction with almost no runtime cost and is provided mostly for
    ergonomics. The core benefits are:

    - flat-definition of the pipeline
    - stages defined in reading order instead of reverse order
    - type erasure and safety
    - composability

    The simplest stream just wraps and consumes an iterable:

    >>> s = Stream(range(10))
    >>> list(s)  # This will consume the iterator
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    But it becomes really useful when composing transformations. Taking a
    trivial example of outside-in composition:

    >>> def add_2(gen):
    ...     for x in gen:
    ...         yield x + 2
    ...
    >>> def drop_multiples_of_3(gen):
    ...     for x in gen:
    ...         if x % 3 > 0:
    ...             yield x
    ...
    >>> gen = drop_multiples_of_3(
    ...     add_2(
    ...         range(10),
    ...     ),
    ... )
    >>> list(gen)
    [2, 4, 5, 7, 8, 10, 11]

    The equivalent form with :class:`Stream` is:

    >>> stream = (
    ...     Stream(range(10))
    ...     .pipe(add_2)
    ...     .pipe(drop_multiples_of_3)
    ... )
    >>> list(stream)
    [2, 4, 5, 7, 8, 10, 11]

    Streams also provide a chainable API and convenience methods (largely
    inspired by Rust's iterator trait) to make it easy to compose readable
    pipelines without nesting.

    Streams are also lazy as long as the transforms are well implemented (i.e.
    they don't consume the entire source iterable in memory) and the pipeline
    will run from the last transform, polling up the stack as needed.

    For a simple example:

    >>> source = iter(range(100_000_000_000))  # Problematically large
    >>> (
    ...     Stream(source)
    ...     .pipe(add_2)
    ...     .batch(10)
    ...     .flatten()
    ...     .pipe(drop_multiples_of_3)
    ...     .inspect(print)
    ...     .take(20)
    ...     .fold(lambda x,y: x+y, 0)
    ... )
    2
    4
    5
    7
    8
    10
    11
    13
    14
    16
    17
    19
    20
    22
    23
    25
    26
    28
    29
    31
    330

    We can see that we haven't consumed too far into the source iterable:

    >>> next(source)
    30

    The print calls in the last example also illustrate the laziness of the
    streams. The final iterators polls from the last step which essentially
    polls up the stack until any iterable yields data. So in the example above
    there's only ever 10 integers passing through the pipeline at any given
    time. This is primarily useful with lazy generators in order to control
    peak memory usage.

    .. warning::
        Streams are *just* chained generators and don't provide any concurrency
        primitives (threads or async). Everything is executing linearly and
        behind the GIL. However nothing prevents a transform from using threads,
        processes or asyncio behind the scene.
    """

    def __init__(self, source: Iterable[T]) -> None:
        self._source = source

    @functools.cached_property
    def _iter(self) -> Iterator[T]:
        return iter(self._source)

    def __iter__(self) -> Iterator[T]:
        yield from self._iter

    def __next__(self) -> T:
        return next(self._iter)

    def __repr__(self) -> str:
        return f"Stream<{self._source!r}>"

    def chain(self, *others: Iterable[T]) -> Stream[T]:
        """
        Take two iterators and create a new iterator over both.

        Works with other streams:

        >>> Stream(range(10)).chain(
        ...     Stream(range(5)).map(lambda x: x + 20)
        ... ).collect()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24]

        And simple iterables:

        >>> Stream(range(2)).chain(range(3), range(2)).collect()
        [0, 1, 0, 1, 2, 0, 1]
        """
        return Stream(itertools.chain(self, *others))

    def pipe(
        self,
        fn: Transform[T, P, U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Pipe[T, P, U]:
        """
        Chain a transform to a stream and return the resulting stream.

        Transforms are the core composability primitive and are simply callables
        which take an iterable and return another iterable. Usually these are
        lazy generators.

        >>> def to_str(iterable: Iterable[int]) -> Iterable[str]:
        ...     for x in iterable:
        ...         yield str(x)
        ...
        >>> list(Stream(range(10)).pipe(to_str))
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        .. note::
            Type information of the source stream is preserved, so in the
            example above the first layer (``Stream(range(10))``) is a
            ``Stream[int, int]`` while the final stream is ``Stream[int, str]``
            which is also an ``Iterable[str]``.

        Transforms can also decide to short-circuit or selectively yield for
        control-flow:

        >>> def to_str_if_odd(iterable: Iterable[int]) -> Iterable[str]:
        ...     for x in iterable:
        ...         if x % 2:
        ...             yield str(x)
        ...
        >>> list(Stream(range(10)).pipe(to_str_if_odd))
        ['1', '3', '5', '7', '9']

        As transforms are just generator-factories they can hold state:

        >>> def track_bounds(gen: Iterable[int]) -> Iterable[int]:
        ...     m, M = 0, 0
        ...     for x in gen:
        ...         m, M = min(m, x), max(M, x)
        ...         yield x
        ...     print(f'Min {m}, Max {M}')
        >>> s = Stream(range(10)).pipe(track_bounds)
        >>> list(s)
        Min 0, Max 9
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        The flip-side of this being that streams are generally not safe to reuse
        once iterated upon.

        .. warning::
            When writing transforms be careful not to accidentally consume the
            iterable as this would negate much of the benefit of chaining
            generators in the first place.
        """
        return Pipe(self, fn, fn.__name__, *args, **kwargs)

    # Chained operations

    def inspect(self: Stream[T], cb: Callable[[T], Any]) -> Stream[T]:
        """
        Execute a function on each element without modifying it.

        This is mostly useful for debugging but could be used as the base for
        monitoring and metrics or any other side-effects.

        >>> Stream(range(4)).inspect(print).collect()
        0
        1
        2
        3
        [0, 1, 2, 3]
        """

        def inspect(gen: Iterable[T]) -> Iterable[T]:
            for x in gen:
                cb(x)
                yield x

        return Pipe(
            self,
            inspect,
            name=f"inspect<{getattr(cb, '__name__', None) or repr(cb)}>",
        )

    def enumerate(self: Stream[T]) -> Stream[tuple[int, T]]:
        """
        Python's ``enumerate`` as a transform.

        >>> Stream(range(5, 11)).enumerate().collect()
        [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10)]
        """
        return self.pipe(enumerate)

    def map(self, fn: Callable[[T], U]) -> Stream[U]:
        """
        Run an element-wise transform over the stream.

        >>> Stream(range(10)).map(lambda x: x * 2).collect()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        """

        def _map(gen: Iterable[T]) -> Iterable[U]:
            for x in gen:
                yield fn(x)

        return Pipe(self, _map, name=f"map({fn})")

    def try_map(
        self,
        fn: Callable[[T], U],
        exc_cls: tuple[type[Exception], ...] = (Exception,),
        *,
        cb: Callable[[Exception, T], None] | None = None,
    ) -> Stream[U]:
        """
        Run an element-wise transform over the stream and discard errors.

        >>> def no_2(x):
        ...     if x == 2:
        ...         raise ValueError(2)
        ...     return x

        >>> list(Stream(range(10)).map(no_2))
        Traceback (most recent call last):
            ...
        ValueError: 2

        >>> list(Stream(range(10)).try_map(no_2, (ValueError,)))
        [0, 1, 3, 4, 5, 6, 7, 8, 9]

        Optionally you can pass in a callback to handle errors out of band:

        >>> list(Stream(range(10)).try_map(no_2, (ValueError,), cb=print))
        2 2
        [0, 1, 3, 4, 5, 6, 7, 8, 9]
        """

        def _map_except(gen: Iterable[T]) -> Iterable[U]:
            for x in gen:
                try:
                    y = fn(x)
                except exc_cls as e:
                    if cb:
                        cb(e, x)
                    continue
                yield y

        return Pipe(
            self,
            _map_except,
            name=f"try_map({fn}, {exc_cls}, {cb})",
        )

    def try_(
        self,
        exc_cls: tuple[type[Exception], ...] = (Exception,),
        *,
        cb: Callable[[Exception], None] | None = None,
    ) -> Stream[T]:
        """
        Stop on the first exception and disacrd it.

        This is more generic than :meth:`try_map` and will catch error that
        happened when calling ``next()`` on the upstream transform but will stop
        iteration on the first exception.

        >>> def no_2(x):
        ...     if x == 2:
        ...         raise ValueError(2)
        ...     return x

        >>> list(Stream(range(10)).map(no_2))
        Traceback (most recent call last):
            ...
        ValueError: 2

        >>> list(Stream(range(10)).map(no_2).try_((ValueError,)))
        [0, 1]

        Optionally you can pass in a callback to handle errors out of band:

        >>> list(Stream(range(10)).map(no_2).try_((ValueError,), cb=print))
        2
        [0, 1]
        """

        def _try(gen: Iterable[T]) -> Iterable[T]:
            it = iter(gen)
            while True:
                try:
                    yield next(it)
                except StopIteration:  # noqa: PERF203
                    return
                except exc_cls as e:
                    if cb:
                        cb(e)
                    return

        return Pipe(
            self,
            _try,
            name=f"stop_on_exception({exc_cls}, {cb})",
        )

    def batch(self, by: int) -> Stream[Iterable[T]]:
        """
        Buffer the stream and provide groups to downstream consumers.

        .. warning::
            This partially unwinds the stream and will increase memory usage.
            Only buffer to amounts you're comfortable holding in memory at once.

        >>> Stream(range(11)).batch(by=2).collect()
        [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10,)]

        To simply buffer without exposing groups simply chain this with
        :meth:`flatten()` which will ensure at least `by` elements are ready
        before forwarding them downstream one by one:

        >>> list(Stream(range(11)).batch(by=2).flatten())
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Batches may not have the number of elements if the end of the stream
        doesn't have enough to fill a batch:

        >>> list(Stream(range(11)).batch(by=3))
        [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10)]
        """
        return Pipe(self, batch, name=f"batch(by={by})", by=by)

    def flatten(self: Stream[Iterable[U]]) -> Stream[U]:
        """
        Flatten iterators into their elements.

        This is usually most useful after a buffered operation.

        >>> Stream(range(11)).batch(by=2).flatten().collect()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        .. seealso:: :meth:`~Stream.flat_map`.
        """
        return Pipe(self, itertools.chain.from_iterable, name="flatten")

    def flat_map(self, fn: Callable[[T], Iterable[U]]) -> Stream[U]:
        """
        Run an element-wise transform over the stream and flatten results.

        >>> Stream(range(10)).flat_map(lambda x: [x] * 2).collect()
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        """

        def _flat_map(gen: Iterable[T]) -> Iterable[U]:
            for x in gen:
                yield from fn(x)

        return Pipe(self, _flat_map, name=f"flat_map({fn})")

    def filter(self, predicate: Callable[[T], bool]) -> Stream[T]:
        """
        Filter elements by running them through a predicate function.

        >>> Stream(range(10)).filter(lambda x: bool(x % 2)).collect()
        [1, 3, 5, 7, 9]
        """

        def _filter(gen: Iterable[T]) -> Iterable[T]:
            for x in gen:
                if predicate(x):
                    yield x

        return Pipe(self, _filter, name=f"filter({predicate})")

    def take(self, count: int) -> Stream[T]:
        """
        Take up to ``count`` element from the stream and interrupt.

        Upstream generators will not be polled once we've reached the requested
        number of elements so the source can be consumed to its end separately.

        >>> it = iter(range(10))
        >>> Stream(it).take(4).collect()
        [0, 1, 2, 3]
        >>> list(it)
        [4, 5, 6, 7, 8, 9]

        Taking more than the size in the iterator has no effect:

        >>> Stream(range(5)).take(10).collect()
        [0, 1, 2, 3, 4]
        """
        return Pipe(
            self,
            lambda x: itertools.islice(x, count),
            name=f"take({count})",
        )

    def skip(self, count: int) -> Stream[T]:
        """
        Skip over ``count`` element from the iterator.

        >>> list(Stream(range(10)).skip(4))
        [4, 5, 6, 7, 8, 9]
        """
        return Pipe(
            self,
            lambda x: itertools.islice(x, count, None),
            name=f"skip({count})",
        )

    def take_while(self, predicate: Callable[[T], bool]) -> Stream[T]:
        """
        Consume element from the stream until the predicate returns ``False``.

        >>> it = iter(range(10))
        >>> list(Stream(it).take_while(lambda x: x == 0 or x % 3 != 0))
        [0, 1, 2]

        Note that the first failing element of the iterator is consumed:

        >>> list(it)
        [4, 5, 6, 7, 8, 9]

        """
        return Pipe(
            self,
            lambda x: itertools.takewhile(predicate, x),
            name=f"take_while({predicate})",
        )

    def skip_while(self, predicate: Callable[[T], bool]) -> Stream[T]:
        """
        Skip elements until the predicate returns ``True``.

        >>> Stream(range(10)).skip_while(lambda x: x == 0 or x % 3 != 0)\
            .collect()
        [3, 4, 5, 6, 7, 8, 9]

        """
        return Pipe(
            self,
            lambda x: itertools.dropwhile(predicate, x),
            name=f"take_while({predicate})",
        )

    def step_by(self, step: int) -> Stream[T]:
        """
        Consume iterators by a given step size each iteration.

        This consumes elements after their predecessor has been consumed.

        >>> Stream(range(10)).step_by(2).collect()
        [0, 2, 4, 6, 8]
        """
        return Pipe(
            self,
            lambda x: itertools.islice(x, None, None, step),
            name=f"step_by({step})",
        )

    def window(self, size: int) -> Stream[tuple[T, ...]]:
        """
        Transform the stream into a stream of sliding windows.

        Each window is a tuple containing ``size`` consecutive elements from the
        stream. The windows overlap, with each window shifted one element
        forward
        from the previous window.

        If the stream contains fewer elements than the window size, an empty
        stream is returned.

        >>> Stream(range(5)).window(3).collect()
        [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

        >>> Stream([1, 2]).window(3).collect()
        []

        >>> Stream([]).window(2).collect()
        []
        """
        return Pipe(self, window, name=f"window(size={size})", size=size)

    def peekable(self) -> Peekable[T]:
        """
        Return a :class:`Peekable` version of the current stream.

        >>> s = Stream(range(100)).peekable()
        >>> s.peek()
        0
        """
        return Peekable(self)

    # Reducer / consuming methods

    def consume(self):
        """
        Consume the stream but discard the results.

        This is useful for infinite pipelines or processing pipelines where the
        results are not important.
        """
        for _ in iter(self):
            pass

    @overload
    def collect(self) -> list[T]: ...

    @overload
    def collect(self, collector: Callable[[Iterable[T]], U]) -> U: ...

    def collect(
        self,
        collector: Callable[[Iterable[T]], U] | None = None,
    ) -> U | list[T]:
        """
        Collect the iterator.

        By default this collects into a list, so this:

        >>> list(Stream(range(10)))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        Is equivalent to:

        >>> Stream(range(10)).collect()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        Custom collectors are also supported:

        >>> Stream(range(10)).collect(set)
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        """
        if collector is None:
            return list(self)
        return collector(self)

    def count(self) -> int:
        """
        Return the length of the stream after consuming it.

        ``__len__`` would implicitly consume the stream in various places so is
        unsafe to add.

        >>> Stream(range(100)).count()
        100
        """
        return sum(1 for _ in self)

    @overload
    def nth(self, nth: int) -> T: ...

    @overload
    def nth(self, nth: int, *, default: T) -> T: ...

    def nth(
        self,
        nth: int,
        *,
        default: U | Literal[UNSET.U] = UNSET.U,
    ) -> T | U:
        """
        Return the ``nth`` value.

        >>> Stream(range(10)).nth(0)
        0

        >>> Stream(range(10)).nth(6)
        6

        Raises ``IndexError`` if the stream is too short:

        >>> Stream(range(10)).nth(12)
        Traceback (most recent call last):
          ...
        IndexError: 12

        A ``default`` can be provided as a fallback:

        >>> Stream(range(10)).nth(12, default=42)
        42

        This short-cirtcuits so it won't consume the source iterator past the
        target element:

        >>> source = iter(range(10))
        >>> Stream(source).nth(3)
        3
        >>> list(source)
        [4, 5, 6, 7, 8, 9]
        """
        if default is not UNSET.U:
            return next(itertools.islice(self, nth, None), default)
        try:
            return next(itertools.islice(self, nth, None))
        except StopIteration:
            raise IndexError(nth) from None

    def find(self, predicate: Callable[[T], bool]) -> T | None:
        """
        Find the first elements that satisfies a predicate.

        >>> Stream(range(10)).find(lambda x: x == 3)
        3

        This short-cirtcuits so it won't consume the source iterator past the
        target element:

        >>> source = iter(range(10))
        >>> Stream(source).find(lambda x: x == 3)
        3
        >>> list(source)
        [4, 5, 6, 7, 8, 9]
        """
        return next(self.filter(predicate))

    def fold(self, fn: Callable[[U, T], U], acc: U) -> U:
        """
        Fold every element into an accumulator function.

        >>> Stream(range(10)).fold(lambda x,y: x + y, 0)
        45

        >>> Stream(range(10)).fold(lambda y, x: [x, *y], [])
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        """
        return functools.reduce(fn, self, acc)


class Pipe(Generic[T, P, U], Stream[U]):
    """
    A stream representing a source stream passed through a transform function.

    This should not be interacted with directly.

    .. seealso::
        :meth:`Stream.pipe`
    """

    def __init__(
        self,
        source: Iterable[T],
        fn: Transform[T, P, U],
        name: str | None = None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self._inner = source
        self._transform = fn
        self._name = name
        self._iterator: Iterator[U] | None = None
        self._args = args
        self._kwargs = kwargs

    @functools.cached_property
    def _iter(self) -> Iterator[U]:
        return iter(
            self._transform(
                iter(self._inner),
                *self._args,
                **self._kwargs,
            ),
        )

    def __str__(self) -> str:
        name = self._name or repr(self._transform)
        return f"{self._inner} | {name}({self._args}, {self._kwargs})"

    def __repr__(self) -> str:
        return f"Pipe<{self!s}>"


class Peekable(Stream[T]):
    """
    A :class:`Stream` with a :meth:`peek()` method.

    .. warning::
        This may have a memory impact as it will buffer elements up to the
        furthest index peeked at.
    """

    def __init__(self, source: Iterator[T]) -> None:
        self._source = source
        self._buffer: deque[T] = deque()

    @functools.cached_property
    def _iter(self) -> Iterator[T]:
        return iter(self._source)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._buffer:
            return self._buffer.popleft()
        return next(self._iter)

    def __repr__(self) -> str:
        return f"Peekable<{self._source!s}>"

    @overload
    def peek(self, n: int) -> T: ...

    @overload
    def peek(self, n: int, *, default: T) -> T: ...

    def peek(
        self,
        n: int = 1,
        *,
        default: U | Literal[UNSET.U] = UNSET.U,
    ) -> T | U:
        """
        Return the element n positions ahead without consuming the stream.

        >>> s = Stream(range(10)).peekable()
        >>> s.peek()
        0
        >>> next(s)
        0

        >>> s.peek(4)
        4
        >>> next(s)
        1

        Peeking past the stream raises ``IndexError``:

        >>> s.peek(20)
        Traceback (most recent call last):
          ...
        IndexError: 20

        Which can be avoided with a default value:

        >>> s.peek(20, default=None) is None
        True
        """
        if len(self._buffer) < (n + 1):
            self._buffer.extend(
                itertools.islice(
                    self._source,
                    n - len(self._buffer) + 1,
                ),
            )

        try:
            return self._buffer[n - 1]
        except IndexError:
            if default is not UNSET.U:
                return default
            raise IndexError(n) from None
