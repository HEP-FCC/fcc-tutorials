(contributing-lesson)=
# Contributing

[starterkit-lessons][repo] is an open source project, and we welcome contributions of all kinds:

* New lessons;
* Fixes to existing material;
* Bug reports; and
* Reviews of proposed changes.

By contributing, you are agreeing that we may redistribute your work under [these licenses][license].
You also agree to abide by our [contributor code of conduct][conduct].

## Getting Started

1.  We use the [fork and pull][gh-fork-pull] model to manage changes.
    More information about [forking a repository][gh-fork] and [making a Pull Request][gh-pull].

2.  For our lessons, you should branch from and submit pull requests against the `master` branch.

3.  When editing lesson pages, you need only commit changes to the Markdown source files.

4.  To build the lessons please follow the [instructions](#building-the-lessons).

5.  If you're looking for things to work on, please see [the list of issues for this repository][issues].
    Comments on issues and reviews of pull requests are equally welcome.

## Building the lessons

### Using `venv` (recommended)

#### Requirements
Make sure you have `venv` (virtual environment) in your working directory. It can be created with the following command:
```
$ python3 -m venv venv
```
Activate it in the shell and install the requirements, which are gathered in a file provided by the repository. 
```
$ source venv/bin/activate
pip3 install -r requirements.txt
```
After sourcing, your shell prompt will be augmented by the `(venv)` prefix, e.g.
```
(venv) mylaptop:~/fcc/fcc-tutorials
```

:::{admonition} Building `fcc-tutorials` in FCCSW stack
:class: solution

In case the Python from FCCSW stack is being used, it is necessary to clear
`PYTHONPATH` environment variable after sourcing of the stack
```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
unset PYTHONPATH
```

Sourcing of the FCCSW stack might be needed in cases when the Python provided by
the OS is too old, currently this is the case for CentOS 7 (`lxplus`).
:::

#### Building
The documentation pages are build by executing
```
$ sphinx-build -b html . build
```

#### Browsing the result
Open in your browser the file
```
$PWD/build/index.html
```

### Using `starterkit_ci`

#### Requirements

To build the lessons locally, install the following:

1. [starterkit-ci](https://pypi.org/project/starterkit-ci/)

#### Building
Build the pages:

```shell
$ starterkit_ci build --allow-warnings
$ starterkit_ci check --allow-warnings
```

#### Browsing the result
Start a web server to host them:

```shell
$ cd build
$ python -m http.server 8000
```
You can see your local version by using a web-browser to navigate to `http://localhost:8000` or wherever it says it's serving the book.

[conduct]: CONDUCT.md
[repo]: https://github.com/HEP-FCC/fcc-tutorials
[issues]: https://github.com/HEP-FCC/fcc-tutorials/issues
[license]: LICENSE.md
[pro-git-chapter]: http://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project
[gh-fork]: https://help.github.com/en/articles/fork-a-repo
[gh-pull]: https://help.github.com/en/articles/about-pull-requests
[gh-fork-pull]: https://reflectoring.io/github-fork-and-pull/


```{eval-rst}
.. toctree::
    :hidden:

    CONDUCT.md
    LICENSE.md
```
