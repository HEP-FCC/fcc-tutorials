# Writing documentation for the FCC software


## Where to put documentation

- API documentation of classes and functions is done with Doxygen notation in the source code.
- Slightly higher level documentation on usage of a piece of software is usually put directly in the corresponding repository.
- Long-form documentations  that introduce users to a piece of software belong in [fcc-tutorials](https://hep-fcc.github.io/fcc-tutorials/).

:::{admonition} Where to put documentation
:class: callout

It is sometimes difficult to decide between the last two. In those cases either will be great.
:::


## When and how is the documentation page updated?

There are both a main website (<https://cern.ch/fccsw>) and a readthedocs-style page for the tutorials (<https://hep-fcc.github.io/fcc-tutorials/>).

Both consists of a static website based on `github-pages`. The  main website points to EOS (`/eos/project/f/fccsw-web/www`), from where it is redirected to the github-pages site of FCCSW. Only members
of the corresponding e-group have write access. All markdown and configuration files are stored in the [`gh-pages`](https://github.com/HEP-FCC/FCCSW/tree/gh-pages) branch of the
FCCSW Github repository. All dependencies (jquery, bootstrap-sass) are included in the mentioned repository and any change should be automatically deployed to:

[http://hep-fcc.github.io/FCCSW/](http://hep-fcc.github.io/FCCSW/)


## Structure of the content of the main page

Folders can be added to aggregate markdown files by category:

- `computing`: FCC Computing Resources
- `presentations`: Selection of Publications and Presentations relating to FCC Software
...

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


## Custom Admonitions

The `fcc-tutorial` makes use of custom admonition classes:

* prereq
* callout
* challenge
* solution
* objectives
* keypoints
* discussion

Example of an admonition:
```markdown
:::{admonition} Custom admonition
:class: solution

Text of a custom admonition.
:::
```

:::{admonition} Custom admonition
:class: solution

Text of a custom admonition.
:::

To create collapsible admonition add additional classes:
* To create collapsible admonition closed by default add only `dropdown` class.
* To create collapsible admonition open by default add two classes `dropdown` and
  `toggle-shown`.

Example of collapsible admonition:
```markdown
:::{admonition} Collapsable admonition
:class: prereq dropdown toggle-shown

Text of a collapsable admonition.
:::
```

:::{admonition} Collapsable admonition
:class: prereq dropdown toggle-shown

Text of a collapsable admonition.
:::
