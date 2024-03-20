# FCC-ee Full Sim General Overview

<!-- This version has been prepared for a 30 minutes tutorial at the Second US FCC Workshop (2024): https://indico.mit.edu/event/876/contributions/2893/ -->

Welcome to this general overview of the FCC-ee Full Simulation.
This tutorial aims at showing you how to run the state of the art full simulation of the various detector concepts currently under study for FCC-ee: CLD, ALLEGRO and IDEA. The DD4hep geometry descriptions of these detectors are hosted in the [k4geo](https://github.com/key4hep/k4geo/tree/main/FCCee) GitHub repository and made centrally available with the Key4hep stack under the `$K4GEO` environment variable.

<!-- Click on the k4geo link, show and explain the different existing CLD versions (the one starting by FCCee are legacy for reproducibility, the useful ones are CLD_...) and where they are documented -->

So, let's start playing with Full Sim!

## Towards Full Sim physics analyses with CLD

The CLD detector has a complete geometry description and reconstruction chain. It is thus a very good candidate to start full sim physics analyses. To illustrate that, we will process some physics events through its Geant4 simulation and reconstruction, look at automatically generated diagnostic plots and produce ourselves a higher level quantity plot.

### Running CLD simulation

Let's first run the CLD Geant4 simulation, through ddsim, for some e<sup>+</sup>e<sup>-</sup> &rarr;

<!-- Mention orally that ddsim can eat other formats (hepevt, hepmc3)-->

```bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

```

### Running CLD reconstruction

Inspect the ROOT file content with

<!-- Explain a bit the rootfile content -->

```
podio-dump wzp6_ee_mumuH_ecm240_edm4hep_recoed_edm4hep.root
```

### Analyzing the output

Let's now use the reconstructed sample to produce some physics quantities.

TOBEWRITTEN

If we had to analyze a large amount of events we would of course use FCCAnalyses or plain C++.

For a realistic analysis you would also need to access much more information than what is shown here. To understand what member can be called on a given edm4hep object, you can use this [Doxygen page](https://edm4hep.web.cern.ch/classedm4hep_1_1_reconstructed_particle-members.html)

## Optimizing a detector with Full Sim


## Running IDEA simulation with detailed Drift Chamber


## Detector visualization

Displaying detector geometries is very useful to understand what is actually being simulated without having to enter the code. One example of tool (out of many) is described here, chosen for its simplicity together with the particular feature of hosting the needed data locally, leading to smooth performance of the visualization.

Let's first generate the files containing the geometry that will be used by the display tool.

```bash
# connect to a machine with cvmfs mounted
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
wget https://fccsw.web.cern.ch/fccsw/tutorials/static/python/dd4hep2root
chmod +x dd4hep2root
./dd4hep2root -c $K4GEO/FCCee/CLD/compact/CLD_o2_v05/CLD_o2_v05.xml -o CLD_o2_v05_geom.root
echo $PWD/CLD_o2_v05_geom.root
```

Now, let's copy the file containing the geometry on your local machine:

```
scp USERNAME@HOSTNAME:ABSOLUTE_PATH_TO_GEOMETRY .
```

Load the file from your computer with the triple-dot button of this webpage: https://root.cern/js/latest/ .

From there, you can navigate the geometry hierarchy to see how volumes are nested, display all or parts of the detector (right click on a volume > Draw > all), play with the camera settings (right click on an empty space in the display window > Show Controls, Clipping > Enable X and Enable Y), etc. See the following picture for illustration:

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/MIT2024/pictures/JSROOT_Screenshot.png
:align: center
```

This tool is useful but not perfect and will not meet all the needs (especially if you want to overlay a physics event). To go further, other solutions are described in the dedicated [Visualization](https://hep-fcc.github.io/fcc-tutorials/master/full-detector-simulations/Visualization/Visualization.html) tutorial.


