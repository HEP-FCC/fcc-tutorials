# Writing documentation for the FCC software

### Contents:

- Writing documentation for the FCC software
  - [Where to put documentation](#where-to-put-documentation)
  - [When and how is the documentation page updated](#when-and-where-is-the-documentation-page-updated)
  - [Running website generation locally](#running-website-generation-locally)
    - [For the impatient](#for-the-impatient)
    - [For the interested](#for-the-interested)
    - [About jekyll](#about-jekyll)
  - [Tricks for writing documentation](#tricks-for-writing-documentation)
    - [Getting the newest version name](#getting-the-newest-version-name)
    - [Using bootstrap](#using-bootstrap)


## Where to put documentation

- API documentation is done with Doxygen in the source code
- Slightly higher level documentation on usage of a piece of software is usually put directly in the corresponding repository
- Tutorials that introduce users to a piece of software belong in fcc-tutorials

> It is sometimes difficult to decide between the last two. In those cases either will be great.

## When and how is the documentation page updated?

The documentation page is updated automatically every night. That means that all markdown files are collected from the following
repositories and the site [fccsw.web.cern.ch/fccsw](fccsw.web.cern.ch/fccsw) is regenerated.

List of repositories from which we collect markdown files:

- HEP-FCC/FCCSW
- HEP-FCC/podio
- HEP-FCC/fcc-edm
- HEP-FCC/fcc-physics
- HEP-FCC/fcc-tutorials

## Running website generation locally

**This is meant for testing not to override the generated website!**

### For the impatient

Make sure you have the prerequisites installed as detailed in the fcc-spi [README](https://github.com/HEP-FCC/fcc-spi#prerequisites).
Then do:

```bash
git clone https://github.com/HEP-FCC/fcc-spi
cd fcc-spi
mkdir local-files
python collect_tutorials.py --savefiles local-files --savetree local-files/tree.pkl
# second run:
#python collect_tutorials.py --loadfiles local-files --loadtree local-files/tree.pkl
cd docpage
jekyll serve --baseurl=
```

Now you should be able to see the website at `localhost:4000`.

### For the interested

The `collect_tutorials.py` script fetches the trees of the above listed repositories and searches for
markdown files and images. The script has the options:
- `savetree`, the tree is saved to the given location.
- `loadtree`, load the tree.
- `savefiles`, the markdown and image files are saved to the given location. If you want to debug your markdown, it may
be smarter to clone the repositories and use them directly, see below.
- `loadfiles`, expects a folder containing all markdown and image files. You can create this structure either by using
the above option or by cloning all repositories in a common base directory (e.g. local-files/FCCSW, local-files/podio, etc.)

### About jekyll

We are using jekyll to build our website. If you are interested in extending the website have a look in
the [repository](https://github.com/HEP-FCC/fcc-spi/blob/master/docpage). Documentation of jekyll may be found
[elsewhere](https://jekyllrb.com/). In case of questions contact the fcc-experiments-sw-dev mailing list or Joschka Lingemann.

## Tricks for writing documentation

### Getting newest version name

Jekyll liquid allows us to get the name of the newest version of the software, add this to the beginning of your markdown:

```
{% for post in site.posts reversed limit:1 %}
{% assign latest_version=post.thisversion %}
{% endfor %}
```

In the following you can use `{{latest_version}}` and it will print the name of the latest FCC software version.

### Using bootstrap

We use bootstrap and you can mix your markdown with html to use any [bootstrap functionality](http://getbootstrap.com/).
