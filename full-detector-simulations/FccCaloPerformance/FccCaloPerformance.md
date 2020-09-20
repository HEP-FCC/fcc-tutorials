
# FCC Calorimeter Performance Studies Workflow


{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

* **simulate** the single particle response of the calorimeter detector system
* **reconstruct** physics object from raw signals
* produce **plots** of energy resolutions and other quantities.

{% endobjectives %}

First, make sure your setup of the FCC software is working. 
You can check that the command to run jobs in the Gaudi framework is available on the command line:

```bash
which fccrun
```
If you don't see a valid path like `/usr/local/bin/fccrun`  you should consult [the documentation page on FCCSW setup](https://github.com/vvolkl/fcc-tutorials/blob/master/FccSoftwareGettingStarted.md)

## Using the DD4hep detector model in FCC Software.

The Geant4 geometry is used for the full simulation of the detector is not written directly, but generated using the DD4hep library.
The detector description in this library consists of two parts:
A compiled C++ library that constructs the geometry, and a set of xml files that contain parameters that can are parsed by the library at runtime and make the detector geometry (somewhat) configurable.
In the framework, the geometry is available to all components via the service `GeoSvc`.
One of the simplest jobs is to write the geometry to a `.gdml` file:

```python

# write to dumpGeo_fccee.py
import os
from Gaudi.Configuration import *
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
geoservice.detectors=[
  "/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/share/FCCSW/Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml",
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
                OutputLevel=INFO
 )

```

A job with this configuration can be executed with 

```bash
fccrun dumpGeo_fccee.py
```

Note the printout of the GeoSvc and make sure the information is as expected. If there is something unclear or missing make sure to open an [issue](https://github.com/HEP-FCC/FCCSW/issues)!
Take a look at the resulting gdml file. Although it is text-based it is not really human-readable for a geometry of this size, but you can check the number of lines and volume names if you are familiar with the geometry.

```bash
tail FCCee_IDEA.gdml
```

```bash
# count occurences of "physvol"
grep -c "<physvol" FCCee_IDEA.gdml
```

## Running Geant4 within the FCC Software Framework

To run Geant4, a number of additional components are required, foremost the `SimG4Alg` and `SimG4Svc`.
The simplest way to generate a particle to simulate is to use one of the particle guns (`GenAlg` with the `MomentumRangeParticleGun` tool for example).
This algorithm produces a particles with energies from a flat probability distribution in HepMC format.
To use them as input they first need to be converted to the FCC event data model (`HepMCToEDMConverter`) and piped into the Geant4 interface via the `SimG4PrimariesFromEdmTool`.

A configuration that runs all of this is distributed with FCCSW and can be run with the following command:

(This simulates the response of 5GeV electrons which makes for modest shower sizes and should produce 500 events in around 2 minutes)


```bash
 fccrun  $FCCSWBASEDIR/share/FCCSW/RecFCCeeCalorimeter/options/runCaloSim.py  \
          --filename fccee_idea_LAr_pgun.root \
          -n 500 
```

The output of this job is `fccee_idea_LAr_pgun.root`, a ROOT file containing the simulation products of 500 single particle events (5 Gev e-) in the FCC event data model.
Check for example that the distribution of the input particles is as you expect:

```python
import ROOT
f = ROOT.TFile("fccee_idea_LAr_pgun.root")
events = f.Get("events")
c = ROOT.TCanvas("canvas1", "",600, 400)
h = ROOT.TH1F("h_GenParticles_P", ";Primary particle Momentum P; Events", 100, 0 ,100)
events.Draw("sqrt(pow(GenParticles.core.p4.px,2) + pow(GenParticles.core.p4.py,2) +pow(GenParticles.core.p4.pz,2))>>h_GenParticles_P")
c.Draw()

```

The exact position of the energy deposit is available too (Note that this collection, which is MCTruth-level information is not usually saved on disk to save space):

```python
import ROOT
f = ROOT.TFile("fccee_idea_LAr_pgun.root")
events = f.Get("events")

c = ROOT.TCanvas("c_ECalBarrelPositions_xy", "", 700, 600)
# draw hits for first five events
events.Draw("ECalBarrelPositions.position.y:ECalBarrelPositions.position.x", "", "", 5, 0)
c.Draw()
```


### Obtaining and Plotting the Energy Resolution

Now that the detector response is simulated, it is time to reconstruct the signals. FCCSW includes another configuration to run a Sliding Window reconstruction:

```bash
fccrun $FCCSWBASEDIR/share/FCCSW/RecFCCeeCalorimeter/options/runFullCaloSystem_ReconstructionSW_noiseFromFile.py \
       -n 100 \
       --input fccee_idea_LAr_pgun.root \
       --noiseFileName http://fccsw.web.cern.ch/fccsw/testsamples/elecNoise_ecalBarrelFCCee_50Ohm_traces1_4shieldWidth.root \
       --filename output_allCalo_reco_noise.root
```

This configuration inludes electronics noise especially calculated for this detector geometry. which is overlayed on the branch `ECalBarrelCells` containing information on all cells in the ECal Barrel.
First, let's visualize the impact of the noise:

```python
import ROOT
f = ROOT.TFile("output_allCalo_reco_noise.root")
events = f.Get("events")

c = ROOT.TCanvas("c_ECalBarrelCellsNoise_energy", "", 700, 600)

h = ROOT.TH1F("h_ECalBarrelCells_energy", ";ECal Barrel Cells Energy [GeV]; Cells", 80, -0.2 ,1)
events.Draw("ECalBarrelCells.core.energy >> h_ECalBarrelCells_energy", "", "", 10, 0)
h.GetYaxis().SetRangeUser(0.2, 8*10**6)



c.SetLogy()
c.Draw()

c2 = ROOT.TCanvas("c_ECalBarrelCells_energy", "", 700, 600)
#h2 = ROOT.TH1F("h_ECalBarrelCellsNoise_energy", ";ECall Barrel Cells Energy with Noise [GeV]; Events", 80, -0.2 ,1)
h2 = h.Clone("h_ECalBarrelCellsNoise_energy")
h2.SetTitle(";ECal Barrel Cells Energy with Noise [GeV]; Cells")
events.Draw("ECalBarrelCellsNoise.core.energy>> h_ECalBarrelCellsNoise_energy", "", "", 10, 0)
h2.GetYaxis().SetRangeUser(0.2, 8*10**6)
h2.SetLineColor(ROOT.kBlack)


c2.SetLogy()
c2.Draw()
```

From these plots the impact of the noise becomes clear. Note that the branch `EcalBarrelCellsNoise` is much larger than `ECalBarrelCells`, as all cells that did not record a signal can no longer be ignored, but have to be saved as well due to the presence of noise.


### Extracting and Plotting the Resolution

The root file created by FCCSW also contains the output of the Sliding Window reconstruction in the branch "CaloClusters". Again, we first check the contents:

```python
import ROOT
f = ROOT.TFile("output_allCalo_reco_noise.root")
events = f.Get("events")

c = ROOT.TCanvas("c_CaloClusters_energy", "", 700, 600)
hEn = ROOT.TH1F("h_CaloClusters_energy", ";ECal Calo Cluster Energy [GeV]; # Clusters", 120, 0 ,8)
events.Draw("CaloClusters.core.energy >> h_CaloClusters_energy")

c.Draw()

```

To extract the Calorimeter Performance, we have to fit the reco energy distribution:

```python

import ROOT
f = ROOT.TFile("output_allCalo_reco_noise.root")
events = f.Get("events")

c = ROOT.TCanvas("c_CaloClusters_energyFit", "", 700, 600)
hEn = ROOT.TH1F("h_CaloClusters_energy", ";ECal Calo Cluster Energy [GeV]; # Clusters", 120, 0 ,8)
events.Draw("CaloClusters.core.energy >> h_CaloClusters_energy")

fitPre = ROOT.TF1("fitPre","gaus", hEn.GetMean() - 1. * hEn.GetRMS(), hEn.GetMean() + 1. * hEn.GetRMS())
resultPre = hEn.Fit(fitPre, "SQRN")
fit = ROOT.TF1("fit","gaus", resultPre.Get().Parameter(1) - 2. * resultPre.Get().Parameter(2), resultPre.Get().Parameter(1) + 2. * resultPre.Get().Parameter(2))
result = hEn.Fit(fit, "SQRN")
mean = result.Get().Parameter(1)
sigma = result.Get().Parameter(2)
dMean = result.Get().Error(1)
dSigma = result.Get().Error(2)
print "mean:", round(mean,2), "[GeV]"
print "sigma:", round(sigma  ,2), "[GeV]"
fit.Draw("SAME")
c.Draw()

```


### Further Topics: Parametrizing the Energy Resolution 

We are of course interested in the Calorimeter response not only at one energy, but over a range of energies,
and in particular in the usual parametrisation of the resolution:



`$  {\sigma_E \over E} =  { a \over \sqrt{E}} \oplus  {b \over E} \oplus c  $`,

where a is the "stochastic term", b the "noise term" and c the "constant term" 

This requires a somewhat more complex script. The FCC Calo Group maintains one here: https://github.com/faltovaj/FCC_calo_analysis_cpp/blob/master/scripts/plot_enResolution.py

TODO: Install a modified version of this script that can run on pre-produced samples on eos?





### Further Topics: Calculating the Sampling Fraction and using it in Simulation

As you can see in https://github.com/HEP-FCC/FCCSW/blob/master/Reconstruction/RecFCCeeCalorimeter/options/runCaloSim.py#L112, the simulation already corrected for the sampling fraction of our calorimeter.
These values themselves are taken from simulation and in case you change the geometry they need to be recalculated and updated.

TODO: This will be part of another tutorial. Add link.
