
import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project   = 'PyUmlDiagrams'
copyright = '2023, Humberto A. Sanchez II'
author    = 'Humberto A. Sanchez II'
version   = '2.50.0'

sys.path.insert(0, os.path.abspath('../'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Mappings for sphinx.ext.intersphinx. Projects have to have Sphinx-generated doc! (.inv file)
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# extensions = ["myst_parser"]
# extensions = []
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'autoapi.extension',
]

autoapi_dirs = ['../pyumldiagrams']
autoapi_options = [ 'members', 'undoc-members', 'show-inheritance', 'show-module-summary', 'imported-members', 'show-inheritance-diagram',]
autoapi_python_class_content = 'both'

templates_path   = ['_templates']
exclude_patterns = []
todo_include_todos=True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme       = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo        = 'PyUmlDiagram.png'
