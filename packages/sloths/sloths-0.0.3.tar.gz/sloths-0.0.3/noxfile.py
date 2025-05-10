#!/usr/bin/env uv run --frozen --all-groups nox --no-venv -f
# /// script
# dependencies = ["nox[toml]>=2025.5.1"]
# ///
"""
Development commands.

Run a task with `nox -s <name>`, list all tasks with `nox -l`.
"""

import contextlib
import functools
import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterator

import nox

pyproject = nox.project.load_toml("pyproject.toml")

# Don't select any session by default.
nox.options.sessions = ()
nox.options.default_venv_backend = "uv"

SUPPORTED_PYTHON = nox.project.python_versions(pyproject)
DEFAULT_PYTHON = (max(SUPPORTED_PYTHON),)


# Export uv's lock file in a format that nox can use.
# Ideally this can go away soon with the new lockfile format stabilisation.
@functools.cache
def _requirements() -> str:
    return subprocess.run(
        [
            "uv",
            "export",
            "--no-emit-project",
            "--all-groups",
            "--all-extras",
            "--frozen",
            "--no-hashes",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


@functools.cache
def _constraints() -> str:
    return "\n".join(
        x for x in _requirements().split("\n") if not x.startswith("-e")
    )


@contextlib.contextmanager
def _file(contents: str) -> Iterator[str]:
    with tempfile.NamedTemporaryFile("w") as f:
        f.write(contents)
        f.flush()  # Force write
        yield f.name


def _install_with_constraints(session: nox.Session, *args: str) -> None:
    if session.venv_backend == "none":
        return

    with _file(_constraints()) as constraints:
        session.install(*args, "--constraint", constraints)


# Development tasks from here
# ===========================================================================


@nox.session(tags=["check"], python=SUPPORTED_PYTHON)
def lint(session: nox.Session) -> None:
    _install_with_constraints(session, "ruff")
    session.run("ruff", "check", "src", "tests")


@nox.session(python=DEFAULT_PYTHON)
def fmt(session: nox.Session) -> None:
    _install_with_constraints(session, "ruff")
    session.run("ruff", "format", "src", "tests")


@nox.session(tags=["check"], python=SUPPORTED_PYTHON)
def typecheck(session: nox.Session) -> None:
    _install_with_constraints(
        session,
        "-e",
        ".",
        *nox.project.dependency_groups(pyproject, "dev"),
        *nox.project.dependency_groups(pyproject, "examples"),
    )
    session.run("pyright", "src", "tests", "docs/examples")


@nox.session(tags=["check"], python=SUPPORTED_PYTHON)
def test(session: nox.Session) -> None:
    _install_with_constraints(
        session,
        "-e",
        ".",
        *nox.project.dependency_groups(pyproject, "dev"),
        *nox.project.dependency_groups(pyproject, "examples"),
    )

    opts = ["-vvls"]

    if junit := os.environ.get("PYTEST_JUNIT_XML"):
        opts.append(f"--junit-xml={junit}")

    session.run(
        "coverage",
        "run",
        "--include=src/**/*.py",
        "-m",
        "pytest",
        *opts,
        *session.posargs,
    )


@nox.session(tags=["check"], python=DEFAULT_PYTHON)
def coverage(session: nox.Session) -> None:
    _install_with_constraints(session, "-e", ".", "coverage")
    session.run("coverage", "combine")
    session.run("coverage", "report")
    session.run("coverage", "html")


@nox.session(tags=["check"], python=DEFAULT_PYTHON)
def spellcheck(session: nox.Session) -> None:
    _install_with_constraints(
        session,
        "-e",
        ".",
        *nox.project.dependency_groups(pyproject, "docs"),
    )
    session.run("codespell", "src", "tests", "docs/**/*.md", "docs/examples/")


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    _install_with_constraints(
        session,
        "-e",
        ".",
        *nox.project.dependency_groups(pyproject, "docs"),
    )
    shutil.rmtree("./docs/_build", ignore_errors=True)
    session.run("sphinx-build", "-M", "html", "docs/", "docs/_build")


@nox.session(venv_backend="none")
def build(session: nox.Session) -> None:
    session.run("uv", "build")
