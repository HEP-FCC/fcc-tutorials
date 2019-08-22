# FCC Calorimeter Performance Studies Workflow

## Overview

This tutorial will teach you how to:

* **simulate** the single particle response of the calorimeter detector system
* **reconstruct** physics object from raw signals
* produce **plots** of energy resolutions and other quantities.

First, make sure your setup of the FCC software is working. 
You can check that the command to run jobs in the Gaudi framework is available on the command line:

```python
!which fccrun
```
If you don't see a valid path like `/usr/local/bin/fccrun`  you should consult [the documentation page on FCCSW setup](https://github.com/vvolkl/fcc-tutorials/blob/master/FccSoftwareGettingStarted.md)

## Using the DD4hep detector model in FCC Software.

The Geant4 geometry is used for the full simulation of the detector is not written directly, but generated using the DD4hep library.
The detector description in this library consists of two parts:
A compiled C++ library that constructs the geometry, and a set of xml files that contain parameters that can are parsed by the library at runtime and make the detector geometry (somewhat) configurable.
In the framework, the geometry is available to all components via the service `GeoSvc`.
One of the simplest jobs is to write the geometry to a `.gdml` file:

```python
%% writefile dumpGeo_fccee.py

import os
from Gaudi.Configuration import *
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
geoservice.detectors=[
	os.path.join(os.environ["FCC_DETECTORS"], 'Detector/DetFCCeeIDEA/compact/FCCee_DectEmptyMaster.xml'),
  os.path.join(os.environ["FCC_DETECTORS"], 'Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml'),
                                         ]

from Configurables import SimG4Svc
geantservice = SimG4Svc("SimG4Svc")

from Configurables import GeoToGdmlDumpSvc
geodumpservice = GeoToGdmlDumpSvc("GeoDump") 
geodumpservice.gdml="FCCee_IDEA.gdml"

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [], 
                EvtSel = 'NONE',
                EvtMax   = 1,
                # order is important, as GeoSvc is needed by SimG4Svc
                ExtSvc = [geoservice, geantservice, geodumpservice],
                OutputLevel=DEBUG
 )

```

A job with this configuration can be executed with 

```python
!fccrun dumpGeo_fccee.py
```

Note the printout of the GeoSvc and make sure the information is as expected. If there is something unclear or missing make sure to open an [issue](https://github.com/HEP-FCC/FCCSW/issues)!
Take a look at the resulting gdml file. Although it is text-based it is not really human-readable for a geometry of this size, but you can check the number of lines and volume names if you are familiar with the geometry.

```python
!tail FCCee_IDEA.gdml
```

## Running Geant4 within the FCC Software Framework

To run Geant4, a number of additional components are required, foremost the `SimG4Alg` and `SimG4Svc`.
The simplest way to generate a particle to simulate is to use one of the particle guns (`GenAlg` with the `MomentumRangeParticleGun` tool for example).
This algorithm produces a particles with energies from a flat probability distribution in HepMC format.
To use them as input they first need to be converted to the FCC event data model (`HepMCToEDMConverter`) and piped into the Geant4 interface via the `SimG4PrimariesFromEdmTool`.

A configuration that runs all of this is distributed with FCCSW


```
!fccrun  $FCCSWBASEDIR/Reconstruction/RecFCCeeCalorimeter/options/runCaloSim.py --filename fccee_idea_LAr_pgun.root -n 500 
```

The output of this job is `fccee_idea_LAr_pgun.root`, a ROOT file containing the simulation products of 500 single particle events (5 Gev e-) in the FCC event data model.
Check for example that the distribution of the input particles is as you expect:

```python
import ROOT
f = ROOT.TFile("fccee_idea_LAr_pgun.root")
events = f.Get("events")
c = ROOT.TCanvas()
events.Draw("sqrt(pow(GenParticles.core.p4.px,2) + pow(GenParticles.core.p4.py,2) +pow(GenParticles.core.p4.pz,2))")


```

The exact position of the energy deposit is available too:

```python

import ROOT
f = ROOT.TFile("fccee_idea_LAr_pgun.root")
events = f.Get("events")
c = ROOT.TCanvas()
events.Draw("ECalBarrelPositions.position.y:ECalBarrelPositions.position.x", "", "", 5, 0)
```


### Obtaining and Plotting the Energy Resolution

Now that the detector response is simulated, it is time to reconstruct the signals. FCCSW includes another configuration to run a Sliding Window reconstruction:

```python
!fccrun $FCCSWBASEDIR/Reconstruction/RecFCCeeCalorimeter/options/runFullCaloSystem_ReconstructionSW_noiseFromFile.py --inputs fcc_idea_LAr_pgun.root -n 500
```

This configuration inludes electronics noise especially calculated for this detector geometry.

TODO: Plotting scripts

### Further Topics: Calculating the Sampling Fraction and using it in Simulation

TODO









