# Inspecting an FCC data file

:::{admonition} Learning Objectives
:class: objectives

* Get to know FCC data files and the tools to inspect them
:::


## The `events` tree

FCC Data is generally stored in ROOT files. The layout of the file is determined by the "Event Data Model", which describes conceptually how the data is structured, and technically what branches are written in the final file.

The implementation of the event data model uses simple structs in order to keep the resulting file simple - it already has a "flat tree" structure.
The definition of the structs can be found in the [`fcc-edm` repository](https://github.com/HEP-FCC/fcc-edm/blob/master/edm.yaml).
You will see that the FCC ROOT files contain a branch for every member of theses structs. So  they can either be processed individually, or as a complete struct. The event data model also allows to store pointers to other objects - to use these it is best to use the provided [code](https://github.com/cbernet/fcc-edm/blob/master/examples/simplewrite.cc)



In configuring jobs with the FCC software framework, users can choose the Branch names in the produced file. Mostly, they will be one of the following:

* `GenParticles`:  Particles from either a generator like Pythia8 or a particle gun
* `GenParticlesFiltered`: The same collection, but filtered according to some criteria (mostly used to select stable particles that are seen in the detector)
* `SimTrackerHits`: Geant information  on energy deposits in the tracker
* `SimTrackerHitsPositions`: The same, but including the MC truth information on the exact coordinates of the deposits
* `SimCaloHits`: Geant information on energy deposits in the calorimeter
* `SimCaloHitsPositions`: The same, but including the MC truth information on the exact coordinates of the deposits
* `SimParticles`: MC truth information about the particles in Geant simulations
* `RecTrackStates`: Helix parameters as reconstructed by the software 
* `RecParticles` Full particle information after Reconstruction




:::{admonition} Inspecting a [ROOT file](https://root.cern/manual/storing_root_objects/)
:class: challenge

Let's take a look at an example: `root://eospublic.cern.ch//eos/experiment/fcc/hh/tutorials/fccee_idea_pgun.root`. 
(For machines without eos access, this is mirrored at <https://fccsw.web.cern.ch/fccsw/testsamples/tutorial/fccee_idea_pgun.root>)
This file
contains simulated data of a single particle passing through the detector and hits from the detector simulation.
Open the file with ROOT and determine:

* How many events does it contain?
* What particle type is being simulated?
* What is the energy of the primary particle?
* How many hits were recorded (averaged over the run) in the Tracker? And in the calorimeter? What is the event with the maximum number of hits?
:::


## The `metadata` tree

FCC data files contain another tree called `metadata`.
As the name suggests, this information is mostly used to process the actual data in the `events` tree.
However, files produced with newer (>0.11) versions of FCCSW
will store the information of the job options file here, so that they can be reproduced (using the same versions of the software). FCCSW provides a script `fcc_dump_joboptions` that can easily access this information.

```bash
k4-print-joboptions https://fccsw.web.cern.ch/fccsw/testsamples/tutorial/fccee_idea_pgun.root 
```


```
EventDataSvc.input = "";

GeoSvc.OutputLevel = 3;
GeoSvc.detectors = ['/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/share/FCCSW/Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml'];

SimG4Alg.eventProvider = "SimG4SingleParticleGeneratorTool/GeantinoGun";
SimG4Alg.outputs = ['SimG4SaveParticleHistory/saveHistory', 'SimG4SaveTrackerHits/saveTrackerHits_Barrel', 'SimG4SaveTrackerHits/saveTrackerHits_Endcap', 'SimG4SaveTrackerHits/saveTrackerHits_DCH'];

SimG4Alg.GeantinoGun.energyMax = "2400.0";
SimG4Alg.GeantinoGun.energyMin = "2400.0";
SimG4Alg.GeantinoGun.etaMax = "3.5";
SimG4Alg.GeantinoGun.etaMin = "-3.5";
SimG4Alg.GeantinoGun.particleName = "mu-";
SimG4Alg.GeantinoGun.phiMax = "360.0";
SimG4Alg.GeantinoGun.phiMin = "0.0";
SimG4Alg.GeantinoGun.saveEdm = False;
SimG4Alg.GeantinoGun.vertexX = "0.0";
SimG4Alg.GeantinoGun.vertexY = "0.0";
SimG4Alg.GeantinoGun.vertexZ = "0.0";
...
```

The output can be redirected to a new job options file that can be run with `fccrun`, provided that all the paths to the detector xmls etc. are still valid.

Note that some older files on eos may not contain the metadata information.


