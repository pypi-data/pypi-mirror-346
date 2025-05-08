
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'wavetools'
copyright = '2025, OIG@Coherent'
author = 'OIG@Coherent'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.autosummary', 'autoapi.extension']

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autoapi_dirs = ['../../src/wavetools']
autoapi_ignore = ['*/WaveAnalyzers/tests/*.*', '*/_WaveShapers/*.*']
autoapi_options = [ 'members', 'undoc-members', 'show-inheritance', 'show-module-summary', 'special-members', 'imported-members']
autoapi_type = "python"