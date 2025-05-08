ctao-sphinx-theme documentation
===============================

CTAO Sphinx theme version.

**Version**: |version| **Date**: |today|

Features
--------

- CTAO corporate design colors and fonts
- Logo branding support (e.g. ``branding = "acada"``)
- Light and dark mode thanks to ``pydata-sphinx-theme``


Usage
-----

.. code-block:: python

   html_theme = "ctao"
   # run python -m ctao_sphinx_theme to get a list of available branding options
   html_theme_options = {
       # "branding": "acada",
   }

This theme directly inherits from ``pydata-sphinx-theme`` and only applies styling changes
and sets up the logos.

See the `documentation of the pydata-sphinx-theme <https://pydata-sphinx-theme.readthedocs.io/>`_
for configuration options.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
