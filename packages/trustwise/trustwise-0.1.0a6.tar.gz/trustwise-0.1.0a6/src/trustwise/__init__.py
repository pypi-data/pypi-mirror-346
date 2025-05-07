"""Trustwise SDK for evaluating AI-generated content."""

try:
    from importlib.metadata import version
    __version__ = version("trustwise")
except ImportError:
    # Fallback for Python < 3.8
    from pkg_resources import get_distribution
    __version__ = get_distribution("trustwise").version
