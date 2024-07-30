# import sphinx_rtd_theme

project = 'FCC Tutorials'
copyright = '2024, CERN'
html_logo = '_static/img/fcc-logo-light.png'
html_favicon = '_static/img/favicon.ico'
html_theme = 'sphinx_rtd_theme'

exclude_patterns = [
    'venv',
    '.github',
    'README.md',
    'archive'
]

html_theme = "sphinx_rtd_theme"

html_context = {
    'display_github': True,
    'github_user': 'HEP-FCC',
    'github_repo': 'fcc-tutorials',
    'github_version': 'main/',
}

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx_togglebutton',
    'sphinx_copybutton',
    'sphinx_multiversion',
]

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    'colon_fence',
    'html_admonition'
]

myst_heading_anchors = 3

html_static_path = [
    '_static'
]

html_css_files = [
    'css/custom-admonitions.css'
]

templates_path = [
    '_templates',
]

smv_tag_whitelist = r'^(?!(v0.1.0|v0.2.0))$'
smv_branch_whitelist = r'^(?!(HEAD|vvolkl-patch-|starterkit|gh-pages)).*$'
smv_remote_whitelist = r'^(origin)$'

linkcheck_ignore = [
    # FIXME: The URLs have changed
    r'https://research\.cs\.wisc\.edu/htcondor/.*',
]
