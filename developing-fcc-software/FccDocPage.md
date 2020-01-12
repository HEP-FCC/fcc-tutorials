# Writing documentation for the FCC software


## Where to put documentation

- API documentation is done with Doxygen in the source code
- Slightly higher level documentation on usage of a piece of software is usually put directly in the corresponding repository
- Tutorials that introduce users to a piece of software belong in fcc-tutorials

{% callout "Where to put documentation" %}

 It is sometimes difficult to decide between the last two. In those cases either will be great.

{% endcallout %}

## When and how is the documentation page updated?

The documentation page consists of a static website based on `github-pages`. The content of the website is hosted in EOS (`/eos/project/f/fccsw-web/www`). Only members
of the corresponding e-group have write access. All markdown and configuration files are stored in the [`gh-pages`](https://github.com/HEP-FCC/FCCSW/tree/gh-pages) branch of the
FCCSW Github repository. All dependencies (jquery, bootstrap-sass) are included in the mentioned repository and any change should be automatically deployed to:

[http://hep-fcc.github.io/FCCSW/](http://hep-fcc.github.io/FCCSW/)

The old URL [http://cern.ch/fccsw](http://cern.ch/fccsw) now redirects to [http://hep-fcc.github.io/FCCSW/](http://hep-fcc.github.io/FCCSW/).

## Structure of the content

There are four main folder which aggregate markdown files by category:

- `computing`: FCC Computing Resources
- `presentations`: Selection of Publications and Presentations relating to FCC Software
- `stack`: Main pieces of software that compose the FCC Software stack
- `tutorials`: Different how-to guides for getting started with the different FCC Software packages

The rest of folders and files are mainly configuration files to generate the website itself with [Jekyll](https://jekyllrb.com/):

- `_data`: Contains `permalinks.yaml` YAML file with the links shown on the website
- `_includes`: HTML files to define the structure of the website (header, footer, ...)
- `_layouts`: HTML Structure for those part that are commonly used (posts, sites, title headers, ...)
- `css`: Define the style of the website
- `geo`: Geometry visualization
- `node_modules`: Contains Javascript installed dependencies
- `Gemfile`: Define Ruby dependencies
- `package.json`: Define Javascript dependencies
- `_config`: General configuration file with metadata used by Jekyll


## Running website generation locally

**This is meant for testing not to override the generated website!**

Modify the content and serve the page with:

```bash
jekyll serve --baseurl=
```

Now you should be able to see the website at `localhost:4000`.


### About jekyll

We are using jekyll to build our website. If you are interested in extending the website have a look in
the [repository](https://github.com/HEP-FCC/FCCSW/tree/gh-pages). Documentation of jekyll may be found
[elsewhere](https://jekyllrb.com/). In case of questions contact the fcc-experiments-sw-dev mailing list.


## For website admins

Administrators controlling access to the webspace need to be members of the e-group `cernbox-project-fccsw-web-admins`.

If you want to have write-access you need to request membership in
`cernbox-project-fccsw-web-writers`. If you are the main responsible for these activities, you should own the service account `fccsweos` that has admin rights for both the physics data EOS space and the web EOS space.
