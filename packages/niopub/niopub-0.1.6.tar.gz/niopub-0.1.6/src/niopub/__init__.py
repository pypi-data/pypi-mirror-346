"""Niopub - Create quick army of context based agents on Niopub from your browser."""

try:
    from importlib.metadata import version
    __version__ = version("niopub")
except ImportError:
    __version__ = "0.0.1"  # fallback for Python < 3.8

from .server import main 