"""
dataguy package
=======

A lightweight toolkit for ingesting, inspecting and transforming
small‑to‑medium datasets or texts with the help of an LLM.

Import convenience::

    >>> from dataguy import DataGuy, validate_file_path
"""

from .core import DataGuy
from .context_manager import ContextManager
from .utils import validate_file_path

__all__: list[str] = ["DataGuy", "ContextManager", "validate_file_path"]

__version__: str = "0.1.0"

