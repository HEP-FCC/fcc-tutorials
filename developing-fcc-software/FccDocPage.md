# Writing documentation for the FCC Software


## Where to put documentation

- API documentation of classes and functions should be done using Doxygen
    notation directly in the source code.
- Slightly higher level documentation on usage of a piece of software is
    usually put directly in the corresponding repository.
- Long-form documentations that introduces users to a piece of software belongs
    into [fcc-tutorials](https://hep-fcc.github.io/fcc-tutorials/).

:::{admonition} Where to put documentation
:class: callout

It is sometimes difficult to decide between the last two. In those cases either
will be great.
:::


## How to write Mardown

This tutorial website is generated with [Sphinx](https://www.sphinx-doc.org/)
machinery using [Read the Docs](https://readthedocs.org/) theme. Specific
parser of Mardown we use is [MyST](https://myst-parser.readthedocs.io).


## Custom Admonitions

The `fcc-tutorial` makes use of the following custom admonition classes
inherited from [LHCb Starterkit](https://lhcb.github.io/starterkit-lessons/):

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


## When and how is the tutorials page updated?

This tutorials page is hosted at <https://hep-fcc.github.io/fcc-tutorials/> and
the edits are managed using Github pull requests. Once the pull request is
merged the change to the tutorials page will happen within few minutes.


## For website admins

Administrators controlling access to the webspace need to be members of the
`cernbox-project-fccsw-web-admins` e-group.

If you want to have write-access you need to request membership in
`cernbox-project-fccsw-web-writers`. If you are the main responsible for these
activities, you should own the service account `fccsweos` that has admin rights
for both the physics data EOS space and the web EOS space.
