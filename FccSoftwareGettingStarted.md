{% for post in site.posts reversed limit:1 %}
{% assign latest_version=post.thisversion %}
{% endfor %}

# Getting started with FCC software

The FCC software is the common software for the FCC detector design study. We support the whole chain starting
from event generation through parameterized and full detector simulation, reconstruction and data analysis.

<div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">
        <span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
        Prerequisites
    </h3></div>
    <div class="panel-body">
     <p>You should be familiar with basics of <code class="highlighter-rouge">bash</code> and know something about either python or C++ programming. If you are not, there are excellent material on the web.</p>
     <p>New to CERN? Get to know the lxplus system <a href="http://information-technology.web.cern.ch/book/lxplus-service/lxplus-guide/lxplus-aliases">here</a>, <a href="http://information-technology.web.cern.ch/services/lxplus-service">here</a>, and <a href="https://twiki.cern.ch/twiki/bin/view/LHCb/RemoteLxplusConsoleHowTo">here</a>. Log in with the standard standard <code class="highlighter-rouge">ssh</code> command, if you are on Windows, look at <a href="http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">PuTTY</a>.  </p>
    </div>
</div>

## Where do I start?

Depending on what you want to do, there are different starting points in the FCC software stack. The following flow
chart should get you to the point where you know where to start and what you need to setup:

![flow-chart getting started](http://fccsw.web.cern.ch/fccsw/static_files/flow_chart_starting.png)

## Setting up the FCC environment

This will set up the pre-installed software on SLC6 machines:

```bash
source /cvmfs/fcc.cern.ch/sw/{{latest_version}}/setup.sh
```

<div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">
        <span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
        Important
    </h3></div>
    <div class="panel-body">
    <em>Note</em>: This has to  be done every time you start a new session (i.e. when you log into your machine).
    </div>
</div>

> We recommend to newcomers to use the central installation, but some of the software (heppy and fcc-physics)
> can also be used standalone on your laptop. See the  [virtual machine](./FccVirtualMachine) and
> [installation](./installing-fcc.md) tutorials.

## Where do I go from here?

The chart hopefully let you select the starting point for what you want to do. If not, feel free to contact our
mailing list: fcc-experiments-sw-devATSPAMNOTcern.ch

### FCCSW

- [Getting started with FCCSW](./FccSoftwareFramework.md)
- Getting started with simulation:
    - [Using parametric Delphes simulation](./FccPythiaDelphes.md)
    - [Geant 4 full (and fast) simulation](https://github.com/HEP-FCC/FCCSW/tree/master/Sim/doc/README.md)
- [Getting started with detector description](https://github.com/HEP-FCC/FCCSW/tree/master/Detector/doc/DD4hepInFCCSW.md)

### fcc-physics

- [Generating events](FccSoftwareGettingStartedFastSim.md)
- Writing analyses with fcc-physics

### heppy

- [Getting started with parametric PAPAS simulation](FccSoftwareGettingStartedFastSim.md)
- Writing analyses with HEPPY

Additional information is to be found in the [index](README.md)
