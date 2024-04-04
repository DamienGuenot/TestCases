from sphinx_mdolab_theme.config import *  # noqa: F403 F401

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------
project = "MACH tutorial"

# Extract private tokens from environment variables
PYTACS_TOKEN = os.environ.get("PYTACS_TOKEN")
PRIVATE_DOCS_TOKEN = os.environ.get("PRIVATE_DOCS_TOKEN")
PYAEROSTRUCTURE_TOKEN = os.environ.get("PYAEROSTRUCTURE_TOKEN")

# Specify the baseurls for the projects I want to link to
intersphinx_mapping = {
    "baseclasses": ("https://mdolab-baseclasses.readthedocs-hosted.com", None),
    "pyspline": ("https://mdolab-pyspline.readthedocs-hosted.com/en/latest", None),
    "pygeo": ("https://mdolab-pygeo.readthedocs-hosted.com/en/latest", None),
    "idwarp": ("https://mdolab-idwarp.readthedocs-hosted.com/en/latest", None),
    "adflow": ("https://mdolab-adflow.readthedocs-hosted.com/en/latest", None),
    "pyoptsparse": ("https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest", None),
    "mach-aero": ("https://mdolab-mach-aero.readthedocs-hosted.com/en/latest", None),
    "multipoint": ("https://mdolab-multipoint.readthedocs-hosted.com/en/latest", None),
    "pytacs": ("https://{PYTACS_TOKEN}:@mdolab-pytacs.readthedocs-hosted.com/en/latest", None),
    "private-docs": ("https://{PRIVATE_DOCS_TOKEN}:@mdolab-private-docs.readthedocs-hosted.com/en/latest", None),
    "pyaerostructure": (
        "https://{PYAEROSTRUCTURE_TOKEN}:@mdolab-pyaerostructure.readthedocs-hosted.com/en/latest",
        None,
    ),
}
