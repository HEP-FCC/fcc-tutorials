# You should normally never do wildcard imports
# Here it is useful to allow the configuration to be maintained elsewhere
from starterkit_ci.sphinx_config import *  # NOQA

project = 'FCC Starterkit Lessons'
copyright = '2020, FCC Starterkit'
author = 'FCC Starterkit'
html_logo = 'starterkit.png'

exclude_patterns += [
    'archive',
    'README.md',
]

html_context = {
    'display_github': True,
    'github_user': 'HEP-FCC',
    'github_repo': 'fcc-tutorials',
    'github_version': 'master',
    'conf_py_path': '/',
}

extensions = [
    'sphinx_copybutton',
    'recommonmark',
]

html_static_path += [
    f'_static',
]

linkcheck_ignore += [
    # FIXME: The URLs have changed
    r'https://research\.cs\.wisc\.edu/htcondor/.*',
]

def starterkit_ci_setup(app):
    app.add_stylesheet('starterkit.css')

setup.extra_setup_funcs += [starterkit_ci_setup]
