# Writing documentation for the FCC software

**Contents:**

<!-- TOC -->

- [Writing documentation for the FCC software](#writing-documentation-for-the-fcc-software)
    - [Where to put documentation](#where-to-put-documentation)
    - [When and how is the documentation page updated?](#when-and-how-is-the-documentation-page-updated)
    - [Running website generation locally](#running-website-generation-locally)
        - [For the impatient](#for-the-impatient)
        - [For the interested](#for-the-interested)
        - [About jekyll](#about-jekyll)
    - [Tricks for writing documentation](#tricks-for-writing-documentation)
        - [Getting newest version name](#getting-newest-version-name)
        - [Using bootstrap](#using-bootstrap)
        - [Linking to other resources](#linking-to-other-resources)
    - [For website admins](#for-website-admins)

<!-- /TOC -->

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

In order to check the formatting of files, you should modify the files in the `loadfiles` directory and re-run the
`collect_tutorials` script again. The script also modifies the tutorials: Links are changed and the jekyll front matter
is added (se below).

### About jekyll

We are using jekyll to build our website. If you are interested in extending the website have a look in
the [repository](https://github.com/HEP-FCC/fcc-spi/blob/master/docpage). Documentation of jekyll may be found
[elsewhere](https://jekyllrb.com/). In case of questions contact the fcc-experiments-sw-dev mailing list or Joschka Lingemann.

## Tricks for writing documentation

### Getting newest version name

Jekyll liquid allows us to get the name of the newest version of the software, add this to the beginning of your markdown:

```
{% raw "do not paste this, this is to escape" %}
{% for post in site.posts reversed limit:1 %}
{% assign latest_version=post.thisversion %}
{% endfor %}
{% endraw "do not paste this, this is to escape" %}
```

In the following you can use {% raw "do not paste this, this is to escape" %}`{{latest_version}}`{% endraw "do not paste this, this is to escape" %} and it will print the name of the latest FCC software version.

### Using bootstrap

We use bootstrap and you can mix your markdown with html to use any [bootstrap functionality](http://getbootstrap.com/).

### Linking to other resources

In general you don't have to take a lot of care how you link. If you link to other content within this repository, just
use relative paths. If you want to link to something in another repository, use the full URL. In the latter case, during
the markdown collection, the links are modified to point to the generated websites in case it is a markdown file.

## For website admins

Administrators controlling access to the webspace need to be members of the e-group `cernbox-project-fccsw-web-admins`.

If you want to have write-access you need to request membership in
`cernbox-project-fccsw-web-writers`. If you are the main responsible for these activities, you should own the service account `fccsweos` that has admin rights for both the physics data EOS space and the web EOS space.
