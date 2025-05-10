Development
-----------

Development uses [`uv`](https://docs.astral.sh/uv/) and [`nox`](https://nox.thea.codes), we also provide a `mise.toml` file with the relevant versions (see [mise-en-place](https://mise.jdx.dev)).

For linting we use [`ruff`](https://docs.astral.sh/ruff) and [`pyright`](https://github.com/microsoft/pyright) for typechecking. [`pre-commit`](https://pre-commit.com) is used locally.

With `mise` setup globally you should be able to run `mise bootstrap` after which virtualenv should be setup, the tools available and `pre-commit` setup. All manual dev tasks are run through `nox`, common tasks include:

- `nox -l` will list all available dev tasks
- `nox -t checks` will run all checks (lints, typechecks, tests, ...) against all supported Python versions
- `nox -e coverage` will run the tests and generate coverage reports
- `nox -e docs` will build the docs

The bare minimum checks are also setup as a [GitHub action](./.github/workflows/checks.yml).

Publishing is manual for now.

TODO
----

Things I'd like to add:

- [ ] Async I/O extension and `Stream` class variant
- [ ] Concurrent variant that work in no GIL world
- [ ] Cythonize to see if that provides any decent benefit
- [ ] Monitoring recipes, progress bars, maybe some form of middleware
- [ ] Prevent adding transforms to a started stream
