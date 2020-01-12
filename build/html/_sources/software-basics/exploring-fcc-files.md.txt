# Inspecting an FCC data file

{% objectives "Learning Objectives" %}

* Get to know FCC data files and the tools to inspect them

{% endobjectives %} 

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




{% challenge "Inspecting a ROOT file" %}

Let's take a look at an example: `root://eospublic.cern.ch//eos/experiment/fcc/hh/tutorials/output_708223617.root`. 
This file
contains simulated data of a single particle passing through the detector and hits from the detector simulation.
Open the file with ROOT and determine:

* How many events does it contain?
* What particle type is being simulated?
* What is the energy of the primary particle?
* How many hits were recorded (averaged over the run) in the Tracker? And in the calorimeter? What is the event with the maximum number of hits?


{% endchallenge %}

## The `metadata` tree

FCC data files contain another tree called `metadata`.
As the name suggests, this information is mostly used to process the actual data in the `events` tree.
However, files produced with newer (>0.11) versions of FCCSW
will store the information of the job options file here, so that they can be reproduced (using the same versions of the software). FCCSW provides a script `fcc_dump_joboptions` that can easily access this information. Unfortunately our example file is too old: 

```bash
    fcc_dump_joboptions root://eospublic.cern.ch//eos/experiment/fcc/hh/tutorials/output_708223617.root
    Traceback (most recent call last):
      File "/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/scripts/fcc_dump_joboptions", line 63, in <module>
          dump_joboptions(args.filename)
            File "/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/scripts/fcc_dump_joboptions", line 53, in dump_joboptions
                s =  event.gaudiConfigOptions
                AttributeError: 'TTree' object has no attribute 'gaudiConfigOptions'
```
It does not contain the job information.


