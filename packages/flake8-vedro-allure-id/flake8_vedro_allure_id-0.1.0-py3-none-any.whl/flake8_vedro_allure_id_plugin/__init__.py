"""Flake8 plugin to enforce @allure.id() decorator for Vedro Scenario classes."""

# Make plugin available to flake8
from .plugin import AllureIdPlugin  # noqa

__version__ = "0.1.0"
