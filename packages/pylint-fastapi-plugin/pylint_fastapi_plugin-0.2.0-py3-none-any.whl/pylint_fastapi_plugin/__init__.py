"""Pylint plugin for FastAPI."""

from typing import TYPE_CHECKING

from .checker import FastAPIChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter

def register(linter: "PyLinter") -> None:
    """Register the FastAPI checker with Pylint."""
    linter.register_checker(FastAPIChecker(linter))
