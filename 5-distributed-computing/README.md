# Distributed Computing

<!-- contributors:start -->
:::{admonition} Page contributors
:class: callout dropdown

Gerardo Ganis, Juraj Smiesko, Michel Villanueva
:::
<!-- contributors:end -->


This chapter covers the tools used to run FCC simulation and analysis at scale: `EventProducer` and `DIRAC`. 

The first section is a primer on the [basic concepts of distributed computing](Concepts.md), written for readers who have never used grid computing in HEP.
It explains the vocabulary (Virtual Organization, job, sandbox, storage element logical file name, etc.) that the following pages use.
If you already familiar with the grid, you can skip it.

In addition, this chapter documents workflows based on the `DIRAC` Interware system through [iLCDirac][ilcdirac], the extension developed by the Linear Collider community and also used by CALICE. These tutorials provide concrete examples of running distributed workflows on grid resources, including job submission, production management, and output retrieval.

The setup procedure needed to use the FCC resources through DIRAC is described first. Additional information about the use of iLCDirac can be found in the [CLIC][wikiclic] and [ILC][wikiilc] dedicated Wiki pages.

Unless specified otherwise, in the remainder of this section the word `DIRAC` refers to the `iLCDirac` extension mentioned above.

The chapter closes with the `EventProducer` framework. It provides a lightweight and reproducible interface to define, submit, monitor, and manage centrally produced event samples. It integrates the different stages of the production chain from generator-level event creation to detector simulation and output handling.


[dirac]: https://dirac.readthedocs.io/en/latest/
[ilcdirac]: https://iopscience.iop.org/article/10.1088/1742-6596/513/3/032077/meta
[wikiclic]: https://twiki.cern.ch/twiki/bin/view/CLIC/DiracForUsers
[wikiilc]: https://flcwiki.desy.de/ILCDirac

```{eval-rst}
.. toctree::
    :maxdepth: 2
    :caption: Contents:

    ./Concepts.md
    ./RegisteringToFccVO.md
    ./Workflows.md
    ./OutputStructure.md
    ./EventProducer.md
```
