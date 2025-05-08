import ctao_sphinx_theme

project = "ctao-sphinx-theme"
copyright = "2024, CTAO"
author = "CTAO"
version = ctao_sphinx_theme.__version__

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_static_path = []

html_theme = "ctao"
# run python -m ctao_sphinx_theme to get a list of available branding options
html_theme_options = {
    # "branding": "acada",
    "logo": {
        "text": "Sphinx Theme",
    },
    "switcher": dict(
        json_url="http://cta-computing.gitlab-pages.cta-observatory.org/common/ctao-sphinx-theme/versions.json",  # noqa: E501
        version_match="latest" if ".dev" in version else f"v{version}",
    ),
    "navbar_center": ["version-switcher", "navbar-nav"],
}
