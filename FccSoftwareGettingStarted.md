{% for post in site.posts reversed limit:1 %}
{% assign latest_version=post.thisversion %}
{% endfor %}

# Getting started with FCC software

The FCC software is the common software for the FCC detector design study. We support the whole chain starting
from event generation through parameterized and full detector simulation and data analysis.

## Prerequisites

> You should be familiar with basics of `bash` and know something about either python or C++ programming.
> If you are not, there are excellent material on the web.

## Where do I start?

Depending on what you want to do, there are different starting points in the FCC software stack. The following flow
chart should get you to the point where you know where to start and what you need to setup:

![flow-chart getting started](http://fccsw.web.cern.ch/fccsw/static_files/flow_chart_starting.png)

## Setting up the FCC environment

This will set up the pre-installed software on SLC6 machines:

```bash
source /cvmfs/fcc.cern.ch/sw/{{latest_version}}/setup.sh
```

> **Note**: This has to  be done every time you start a new session (i.e. when you log into your machine).

> We recommend to newcomers to use the central installation, but some of the software (heppy and fcc-physics)
> can also be used standalone on your laptop. See the  [virtual machine](./FccVirtualMachine) and
> [installation](./installing-fcc.md) tutorials.

## Where do I go from here?

The chart hopefully let you select the starting point for what you want to do. If not, feel free to contact our
mailing list: fcc-experiments-sw-devATSPAMNOTcern.ch

### FCCSW

- Getting started with FCCSW
- Getting started with simulation:
    - [Using parametric Delphes simulation](./FccPythiaDelphes.md)
    - [Geant 4 full (and fast) simulation](../FCCSW/Sim/README.md)
- [Getting started with detector description](../FCCSW/Detector/DD4hepInFCCSW.md)

### fcc-physics

- Generating events
- Writing analyses with fcc-physics

### heppy

- Getting started with parametric PAPAS simulation
- Writing analyses with HEPPY

If you know where to start, have a look at the [index page](./README.md) to see the documentation of the end-point where you landed in
the flow chart. There should be sub-chapters on the specific topics that will get you started.
