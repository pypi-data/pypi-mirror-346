Welcome to sloth's documentation!
=================================

:mod:`sloths` is a library providing a chainable interface to easily compose lazy
iterator pipelines in Python. The interface is largely inspired by Rust's
Iterator trait (although it's not a carbon copy).

The 2 primary goals of the library are:

- Provide an easy to use, chainable and typed API for composing iterator pipelines.
- Make it easy to control peak memory usage and throuhgput on large source datasets.

Documentation
-------------

.. toctree::
   :maxdepth: 4

   usage
   cookbook
