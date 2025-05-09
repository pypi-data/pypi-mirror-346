from __future__ import annotations

import datetime
import importlib.metadata as metadata
import os
import sys
from pathlib import Path
import os, sys
sys.path.insert(0, os.path.abspath('../../src'))


# -- Path setup --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# -- Project information -----------------------------------------------------
project = "DataGuy"
author = "István Magyary, Sára Viemann, Bálint Kristóf"
copyright = f"{datetime.datetime.now().year}, {author}"
release = metadata.version("dataguy") if "dataguy" in metadata.packages_distributions() else "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "myst_parser",
]

autosummary_generate = True
napoleon_numpy_docstring = True
napoleon_google_docstring = False
add_module_names = False

templates_path = ["_templates"]
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
