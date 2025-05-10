# User guide

## Installation

```shell
pip install sloths
```

## Usage

The primary entrypoint to the library is the {class}`sloths.Stream` class.

### A contrived example

We create a lazy stream over the first 1B integers and then buffer it to
2048 chunks which we then forward directly to a map transform. We then
limit ourselves to the first 10:

```python
>>> from sloths import Stream
>>> source = iter(range(1_000_000_000))
>>> s = (
...     Stream(source)
...     .batch(2048)
...     .flatten()
...     .map(lambda x: x * 2)
...     .take(10)
... )
>>> list(s)
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

```

To confirm the stream is lazy, the source iterator should not have gone
past the first chunk, the memory ceiling is mostly dictated by that
buffer (and downstream processing):

```python
>>> next(source)
2048

```

Stream instances are valid iterators so can be used as such within comprehensions
or builtins once defined:

```python
>>> s = Stream(range(10)).take(10)
>>> sum(s)
45

```

An equivalent version using generators and {py:mod}`itertools`:

```python
>>> from sloths._utils import batch  # Similar to itertools.batched in more recent Python versions
>>> from itertools import islice, chain

>>> source = iter(range(1_000_000_000))
>>> list(
...     islice(
...         map(
...             lambda x: x * 2,
...             chain.from_iterable(
...                 batch(source, 2048),
...             ),
...         ),
...         10,
...     ),
... )
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
>>> next(source)
2048

```

The main difference here is that the generator version is defined from the
inside out: the outermost transformation is actually the last stage in the
pipeline while the stream version is flat. The lazyness aspect is applicable to
both spellings however.

Note that in both cases you could just pass in a list as the `source` value
(and any `Iterator` would work) however this would negate much of the lazyness
benefit from such pipelines.

### Chaining transforms

While the {class}`~sloths.Stream` class exposes many common operations, the
second core primitive  is iterator transforms which allow you to compose your
own operations with the {meth}`~sloths.Stream.pipe` method.

Transforms are simply functions which take an iterator  as input and return
another iterator. They should lazily consume the source iterator to maximise
their utility.

Taking the `add_2` example from above, it can be expressed as an iterator
transform like so:

```python
>>> def add_2(it):
...     for x in it:
...         yield x + 2

>>> Stream(range(10)).pipe(add_2).collect()
[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

```

Or using the {py:func}`itertools.cycle` function:

```python
>>> from sloths import Stream
>>> import itertools
>>> list(
...     Stream(range(2))
...     .pipe(itertools.cycle)
...     .take(5)
... )
[0, 1, 0, 1, 0]

```

Transforms can accept extra parameters (as long as the first positional
parameter is an iterator), for example with {py:func}`itertools.islice`:

```python
>>> from sloths import Stream
>>> import itertools
>>> list(
...     Stream(range(2))
...     .pipe(itertools.cycle)
...     .pipe(itertools.islice, 5)
... )
[0, 1, 0, 1, 0]

```

(This is how the {meth}`~sloths.Stream.take` method is implemented)

#### Transforms can hold state

As transforms work at the level of the iterator and are not element-wise they
can hold state, have side effects after the iteration, etc:

```python
>>> from sloths import Stream
>>> def track_bounds(gen):
...     m, M = 0, 0
...     for x in gen:
...         m, M = min(m, x), max(M, x)
...         yield x
...     print(f'Min {m}, Max {M}')
>>> s = Stream(range(10)).pipe(track_bounds)
>>> list(s)
Min 0, Max 9
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

```

### Lazyness and backpressure control

Streams by default are lazy and well-implemented transforms (i.e. generator
transforms) provide a few interesting properties to help control backpressure
as well as memory usage. The final transforms polls froms the last step which
essentially polls up the stack until any iterable yields data.

We can visualise this with the following constructed example:

```python
>>> def source():
...     # Could be any very large iterator, a network stream, a file, etc.
...     for x in range(100_000_000_000):
...         print('read >', x)
...         yield x
>>> (
...     Stream(source())
...     .map(lambda x: x * 2)
...     .inspect(lambda x: print('doubled > ', x))
...     .batch(10)
...     .inspect(lambda x: print('buffered > ', x))
...     .flatten()
...     .filter(lambda x: str(x).endswith('2'))
...     .inspect(lambda x: print('filtered > ', x))
...     .take(10)
... ).collect()
read > 0
doubled >  0
read > 1
doubled >  2
read > 2
doubled >  4
read > 3
doubled >  6
read > 4
doubled >  8
read > 5
doubled >  10
read > 6
doubled >  12
read > 7
doubled >  14
read > 8
doubled >  16
read > 9
doubled >  18
buffered >  (0, 2, 4, 6, 8, 10, 12, 14, 16, 18)
filtered >  2
filtered >  12
read > 10
doubled >  20
read > 11
doubled >  22
read > 12
doubled >  24
read > 13
doubled >  26
read > 14
doubled >  28
read > 15
doubled >  30
read > 16
doubled >  32
read > 17
doubled >  34
read > 18
doubled >  36
read > 19
doubled >  38
buffered >  (20, 22, 24, 26, 28, 30, 32, 34, 36, 38)
filtered >  22
filtered >  32
read > 20
doubled >  40
read > 21
doubled >  42
read > 22
doubled >  44
read > 23
doubled >  46
read > 24
doubled >  48
read > 25
doubled >  50
read > 26
doubled >  52
read > 27
doubled >  54
read > 28
doubled >  56
read > 29
doubled >  58
buffered >  (40, 42, 44, 46, 48, 50, 52, 54, 56, 58)
filtered >  42
filtered >  52
read > 30
doubled >  60
read > 31
doubled >  62
read > 32
doubled >  64
read > 33
doubled >  66
read > 34
doubled >  68
read > 35
doubled >  70
read > 36
doubled >  72
read > 37
doubled >  74
read > 38
doubled >  76
read > 39
doubled >  78
buffered >  (60, 62, 64, 66, 68, 70, 72, 74, 76, 78)
filtered >  62
filtered >  72
read > 40
doubled >  80
read > 41
doubled >  82
read > 42
doubled >  84
read > 43
doubled >  86
read > 44
doubled >  88
read > 45
doubled >  90
read > 46
doubled >  92
read > 47
doubled >  94
read > 48
doubled >  96
read > 49
doubled >  98
buffered >  (80, 82, 84, 86, 88, 90, 92, 94, 96, 98)
filtered >  82
filtered >  92
[2, 12, 22, 32, 42, 52, 62, 72, 82, 92]

```

The order of print statement shows that we're only pulling from the source as
needed and control buffering with the use `.batch` so there's only ever 10
integers read from the source and passing through the pipeline at any given time.

In practice this is mostly useful for:

- Controlling memory usage: when the source stream is very large you get
  explicit control of how many items can flow through the pipeline at any given
  time and thus control peak memory usage.
- Rate limiting as pipelines will poll only as fast as the slowest step
  allows it.
- Sampling.
- Dealing with infinite streams such as sockets or event streams.

:::{warning}
The lazyness can easily be lost by one bad transform. Be careful to never
consume the source iterator eagerly if you want the properties discussed
above to remain true.
:::

### Concurrent pipelines

While streams have no built in concurrency primitive and all transforms are
single threaded, the lazy polling behaviour make them well suited for concurrent
processing.

#### Concurrency inside a transform

Nothing prevents us from writing threaded code inside a transform; for example:

```python
>>> from concurrent.futures import ThreadPoolExecutor
>>> import time
>>> from sloths import Stream

>>> def heavy_io_fn(x):
...     time.sleep(0.01)
...     return x * 2

>>> def do_something_over_threads(gen):
...     with ThreadPoolExecutor(max_workers=4) as e:
...         yield from e.map(heavy_io_fn, gen)

>>> list(Stream(range(10)).pipe(do_something_over_threads))
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

```

The example above while short has one problem:
{py:meth}`concurrent.futures.Executor.map` (as well as
{py:func}`concurrent.futures.as_completed`) will consume the source iterator.

For convenience the library provides {func}`~sloths.ext.concurrent.threaded_map`
(and a few more generic helpers) which are lazy and can be used like so:

```python
>>> from sloths.ext.concurrent import threaded_map
>>> list(Stream(range(10)).pipe(threaded_map, heavy_io_fn, max_workers=4))
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

```

#### Using concurrent pipelines

Another common pattern is to run the full pipeline in a thread and feed it from
a {py:class}`queue.Queue`.

```python
>>> import threading, queue
>>> from sloths import Stream

>>> QUEUE, SENTINEL = queue.Queue(), object()

>>> def queue_to_gen(queue):
...     while True:
...         x = queue.get()
...         if x is SENTINEL:
...             queue.task_done()
...             return
...         yield x
...         queue.task_done()

>>> def process(x):
...     print('PROCESSING:', x)
...     return x * 2

>>> def worker():
...     Stream(queue_to_gen(QUEUE)).map(process).consume()
...     print("ALL DONE FROM THREAD")

>>> threading.Thread(target=worker, daemon=True).start()

>>> for item in range(10):
...     QUEUE.put(item)
>>> QUEUE.put(SENTINEL)

>>> QUEUE.join()
PROCESSING: 0
PROCESSING: 1
PROCESSING: 2
PROCESSING: 3
PROCESSING: 4
PROCESSING: 5
PROCESSING: 6
PROCESSING: 7
PROCESSING: 8
PROCESSING: 9
ALL DONE FROM THREAD

>>> print("ALL DONE")
ALL DONE

```

:::{warning}
In the example above if the queue was bounded (e.g. `Queue(10)`) the code
could deadlock as `put()` would block.
:::

Common versions of this pattern would be an main thread accepting data from a
socket distributing to one or more background processing threads or a chain of
streams running in individual threads (e.g. for branching).

### Error handling

By default - as with raw iterators - an exception will interrupt the entire
pipeline. For long running pipeline this is usually a blocker.

A common approach is to ignore and log errors (or send back to another queue to
be retried later). You can do this with {meth}`~sloths.Stream.try_map` or
{meth}`~sloths.Stream.try_`.

Another common approach if you need to carry errors through is to wrap the
computation in a result container (error tuples, result wrappers, etc.):

```python
>>> from sloths import Stream
>>> import collections

>>> class Result:
...     def __init__(self, val=None, err=None):
...         self.val, self.err = val, err

>>> def with_result(fn):
...     def wrapper(x):
...         if isinstance(x, Result):
...             if x.err:
...                 return x
...             x = x.val
...
...         try:
...             return Result(val=fn(x))
...         except Exception as e:
...             return Result(err=e)
...
...     return wrapper


>>> @with_result
... def faillible(x):
...     if x == 3:
...         raise ValueError("No 3!")
...     return x

>>> double = with_result(lambda x: x * 2)

>>> list(
...     Stream(range(5))
...     .map(faillible)
...     .map(double)
...     .map(lambda x: (x.val, str(x.err)))
... )
[(0, 'None'), (2, 'None'), (4, 'None'), (None, 'No 3!'), (8, 'None')]

```

A more practical use case here would be collecting the errors and saving the
successes while re-scheduling the failures for example.
