(contributing-lesson)=
# Contributing

[FCC Software][fcc-software] is an open source project, and we welcome
contributions of all kinds:

* New lessons;
* Fixes to existing material;
* Bug reports; and
* Reviews of proposed changes.

By contributing, you are agreeing that we may redistribute your work under
[these licenses][license].
You also agree to abide by our [contributor code of conduct][conduct].

## Getting Started

1.  We use the [fork and pull][gh-fork-pull] model to manage changes.
    More information about [forking a repository][gh-fork] and [making a Pull Request][gh-pull].

2.  For our lessons, you should branch from and submit pull requests against the `main` branch.

3.  When editing lesson pages, you need only commit changes to the Markdown source files.

4.  To build the lessons please follow the [instructions](#building-the-lessons).

5.  If you're looking for things to work on, please see [the list of issues for this repository][issues].
    Comments on issues and reviews of pull requests are equally welcome.


## Building the lessons

### Requirements

Make sure you have `venv` (virtual environment) in your working directory. It
can be created with the following command:
```shell
$ python3 -m venv venv
```
Activate it in your shell and install the requirements, which are gathered in a
file provided by the repository.
```shell
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
After sourcing, your shell prompt will be augmented by the `(venv)` prefix, e.g.
```shell
(venv) mylaptop:~/fcc/fcc-tutorials
```

:::{admonition} Building `fcc-tutorials` in FCC Software stack
:class: callout

In case the Python from the FCC Software stack is being used, it is necessary to
clear `PYTHONPATH` environment variable after sourcing of the stack
```shell
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
unset PYTHONPATH
```

Sourcing of the FCCSW stack might be needed in cases when the Python provided by
the OS is too old, currently this is the case for CentOS 7 (`lxplus7`).
:::

### Building

The documentation pages are build by executing
```shell
$ sphinx-build -b html . build
```

### Browsing the result

Start a web server to host the generated files from `build` directory
```shell
$ cd build
$ python -m http.server
```

You should be able to see your local version by opening a web-browser and
navigating to [http://localhost:8000](http://localhost:8000).


## How to Write Documentation

More information about how to write the documentation/tutorials for the FCC
Software visit
[](./developing-fcc-software/FccDocPage.md#writing-documentation-for-the-fcc-software).

## Legal

```{eval-rst}
.. toctree::

    CONDUCT.md
    LICENSE.md
```


[fcc-software]: https://fccsw.web.cern.ch/
[conduct]: CONDUCT.md
[license]: LICENSE.md
[issues]: https://github.com/HEP-FCC/fcc-tutorials/issues
[pro-git-chapter]: https://git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project
[gh-fork]: https://help.github.com/en/articles/fork-a-repo
[gh-pull]: https://help.github.com/en/articles/about-pull-requests
[gh-fork-pull]: https://reflectoring.io/github-fork-and-pull/
