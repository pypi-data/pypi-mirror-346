sloths
======

Lazy iterator pipelines for Python.

`sloths` is a library providing a chainable interface to easily compose lazy iterator pipelines in Python. The interface is largely inspired by Rust's Iterator trait (although it's not a carbon copy).

The 2 primary goals of the library are:

- Provide an easy to use, chainable and typed API for composing generator pipelines.
- Make it easy to control peak memory usage and throuhgput on large source datasets or long running input streams.

```python
>>> from sloths import Stream
>>> Stream(range(100_000)).enumerate().filter(lambda x: x[1] % 3 == 0).skip(3).take(5).collect()
[(9, 9), (12, 12), (15, 15), (18, 18), (21, 21)]

```

For more examples see doctests within the code or [`usage.md`](./docs/usage.md).

Installation
------------

The project is released [on PyPI](https://pypi.org/project/sloths/).

```shell
pip install sloths
```
