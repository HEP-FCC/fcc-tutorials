# FCC-ee Full Sim General Overview

<!-- This version has been prepared for the tutorial at the Second US FCC Workshop (2024): https://indico.mit.edu/event/876/contributions/2893/ -->

Welcome to this general overview of the FCC-ee Full Simulation.
This tutorial aims at showing you how to run the state of the art full simulation of the various detector concepts currently under study for FCC-ee: CLD, ALLEGRO and IDEA. The [DD4hep](https://dd4hep.web.cern.ch/dd4hep/usermanuals/DD4hepManual/DD4hepManual.pdf) geometry descriptions of these detectors are hosted in the [k4geo](https://github.com/key4hep/k4geo/tree/main/FCCee) GitHub repository and made centrally available with the Key4hep stack under the `$K4GEO` environment variable. This tutorial should work on any machine with `cvmfs` access and running an operating system supported by Key4hep (AlmaLinux 9 and Ubuntu 22).

<!-- Click on the k4geo link, show and explain the different existing CLD versions (the one starting by FCCee are legacy for reproducibility, the useful ones are CLD_...) and where they are documented -->

So, let's start playing with Full Sim!

## Setting-up the environment
```bash
# connect to a machine with cvmfs access and running an OS supported by Key4hep (Alma9 here)
ssh -X username@lxplus.cern.ch
# set-up the Key4hep environment, using the nightlies since we need the latest and greatest version of the packages
# (make sure you are in bash or zsh shell)
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# create a repository for the tutorial
mkdir FCC_Full_Sim_Tutorial
cd FCC_Full_Sim_Tutorial
git clone https://github.com/HEP-FCC/fcc-tutorials
```

## Towards Full Sim physics analyses with CLD

The CLD detector has a complete geometry description and reconstruction chain. It is thus a very good candidate to start full sim physics analyses. To illustrate that, we will process some physics events through its Geant4 simulation and reconstruction, look at automatically generated diagnostic plots and produce ourselves the Higgs recoil mass.

### Running CLD simulation

Let's first run the CLD Geant4 simulation, through ddsim, for some $e^{+}e^{-} \to Z(\mu\mu)H(\text{inclusive})$ events, taken from the generation used for Delphes simulation.
<!-- /eos/experiment/fcc/ee/generation/stdhep/wzp6_ee_mumuH_ecm240/events_057189088.stdhep.gz -->

```bash
# get the CLD config repository
git clone https://github.com/key4hep/CLDConfig.git
cd CLDConfig/CLDConfig
# retrieve Z(mumu)H(X) MC generator events
wget https://fccsw.web.cern.ch/fccsw/tutorials/MIT2024/wzp6_ee_mumuH_ecm240_GEN.stdhep.gz
gunzip wzp6_ee_mumuH_ecm240_GEN.stdhep.gz
# run the Geant4 simulation
ddsim -I wzp6_ee_mumuH_ecm240_GEN.stdhep -N 10 -O wzp6_ee_mumuH_ecm240_CLD_SIM.root --compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v05/CLD_o2_v07.xml --steeringFile cld_steer.py
# NB: we run only on 10 events (-N 10) here for the sake of time
# for such small amount of event the detector geometry construction step dominates, it takes about 5 seconds per event and the geometry loading takes 1min30s
```

While the code runs, you can browse the [k4geo](https://github.com/key4hep/k4geo/tree/main/FCCee) repository to see how the code is organized. This step produced an output file in edm4hep dataformat with Geant4 SIM hits that can then be fed to the reconstruction step. Note that ddsim can also digest other MC output format like `hepevt`, `hepmc`, `pairs` (GuineaPig output), ..., and of course also has particle gun**s** as we will see later. More information can be obtained with `ddsim -h`.

### Running CLD reconstruction

Let's now apply the CLD reconstruction (from ILCSoft through the Gaudi wrappers and data format converters) on top of the SIM step:

```
sed -i "s/DEBUG/INFO/" CLDReconstruction.py
k4run CLDReconstruction.py --inputFiles wzp6_ee_mumuH_ecm240_CLD_SIM.root --outputBasename wzp6_ee_mumuH_ecm240_CLD --num-events -1
# Do not forget to modify the geoservice.detectors variable if you do not use the central detector
```
<!-- takes 1m40s -->

This created an edm4hep ROOT file with a bunch of new DIGI/RECO level collections, including `edm4hep::ReconstructedParticle` from Particle Flow (PandoraPFA). You can inspect the ROOT file content with

```
podio-dump wzp6_ee_mumuH_ecm240_CLD_REC.edm4hep.root
```
<!-- Explain a bit the rootfile content -->

A detailed documentation on the collection content still has to be written.

NB: this step also produces a file named `wzp6_ee_mumuH_ecm240_CLD_aida.root` where you can find a lot of debugging distributions such as the pulls of the track fit.

### Plotting the Higgs recoil mass

Let's now use the reconstructed sample to produce some physics quantities. As an example, we will plot the Higgs recoil mass using the Python bindings of [PODIO](https://github.com/key4hep/key4hep-tutorials/blob/main/edm4hep_analysis/edm4hep_api_intro.md#reading-edm4hep-files). The following very simple script already does a decent job:

<!-- Explain a bit the script -->
```
import sys
from podio import root_io
import ROOT
ROOT.gROOT.SetBatch(True)

input_file_path = sys.argv[1]
podio_reader = root_io.Reader(input_file_path)

th1_recoil = ROOT.TH1F("Recoil Mass", "Recoil Mass", 100, 110, 160)

p_cm = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0, 0, 0, 240)
for event in podio_reader.get("events"):
    pfos = event.get("TightSelectedPandoraPFOs")
    n_good_muons = 0
    p_mumu = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
    for pfo in pfos:
        if abs(pfo.getPDG()) == 13 and pfo.getEnergy() > 20:
            n_good_muons += 1
            p_mumu += ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(pfo.getMomentum().x, pfo.getMomentum().y, pfo.getMomentum().z, pfo.getEnergy())
    if n_good_muons == 2:
        th1_recoil.Fill((p_cm - p_mumu).M())

canvas_recoil = ROOT.TCanvas("Recoil Mass", "Recoil Mass")
th1_recoil.Draw()
canvas_recoil.Print("recoil_mass.png")
```

The equivalent C++ ROOT macro looks like this:
```
#include "podio/ROOTFrameReader.h"
#include "podio/Frame.h"

#include "edm4hep/ReconstructedParticleCollection.h"

int plot_recoil_mass(std::string input_file_path) {
  auto reader = podio::ROOTFrameReader();
  reader.openFile(input_file_path);

  TH1* th1_recoil = new TH1F("Recoil Mass", "Recoil Mass", 100, 110., 160.);

  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>> p_cm(0., 0., 0., 240.);
  for (size_t i = 0; i < reader.getEntries("events"); ++i) {
    auto event = podio::Frame(reader.readNextEntry("events"));
    auto& pfos = event.get<edm4hep::ReconstructedParticleCollection>("TightSelectedPandoraPFOs");
    int n_good_muons = 0;
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>> p_mumu;
    for (const auto& pfo : pfos) {
      if (std::abs(pfo.getPDG()) == 13 and pfo.getEnergy() > 20.) {
        n_good_muons++;
        p_mumu += ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>>(pfo.getMomentum().x, pfo.getMomentum().y, pfo.getMomentum().z, pfo.getEnergy());
      }
    }
    if(n_good_muons == 2)
      th1_recoil->Fill((p_cm - p_mumu).M());
  }
  TCanvas* canvas_recoil = new TCanvas("Recoil Mass", "Recoil Mass");
  th1_recoil->Draw();
  canvas_recoil->Print("recoil_mass.png");
  return 0;
}
```
<!--
Let's get a similar sample but with more stat:
```
cd ../../fcc-tutorials/full-detector-simulations/FCCeeGeneralOverview/
wget https://fccsw.web.cern.ch/fccsw/tutorials/MIT2024/wzp6_ee_mumuH_ecm240_CLD_RECO_moreStat.root
```
and produce the simple Higgs recoil mass plot in Python:
``` 
python plot_recoil_mass.py wzp6_ee_mumuH_ecm240_CLD_RECO_moreStat.root
display recoil_mass.png
```

or in C++ with the ROOT interpreter:
```
root -b
.L plot_recoil_mass.C
plot_recoil_mass("wzp6_ee_mumuH_ecm240_CLD_RECO_moreStat.root")
.q
display recoil_mass.png
```
-->

To produce the Higgs recoil mass plot, copy the content of the above code in a file and run it.

In Python:
```
python plot_recoil_mass.py wzp6_ee_mumuH_ecm240_CLD_REC.edm4hep.root
display recoil_mass.png
```

or in C++ with the ROOT interpreter:
```
root -b
.L plot_recoil_mass.C
plot_recoil_mass("wzp6_ee_mumuH_ecm240_CLD_REC.edm4hep.root")
.q
display recoil_mass.png
```

This illustrates how easy it is already to do physics with Full Sim. Of course, if we had to do a realistic analysis, we would run on more events, properly select muons from the Z, include backgrounds, ..., and we would therefore use FCCAnalyses or plain C++ but it is not the topic of this tutorial. If you want to go further, the following [Doxygen page](https://edm4hep.web.cern.ch/classedm4hep_1_1_reconstructed_particle-members.html) will help you in understanding what members can be called on a given edm4hep object.

## Towards detector optimization with Full Sim: ALLEGRO ECAL

In this section we will learn how to run with a modified version of a detector (needed for optimization), taking the ALLEGRO ECAL as an example.

### Modifying the sub-detector content

So far we have been using the 'central' version of the detector, as directly provided by Key4hep. The first thing we have to do to run a modified version is to clone the repository where the DD4hep detector geometries are hosted and update the environment variable `$K4GEO` so that it points to your local folder:

```
# go in a 'clean' place i.e. outside of the git repository in which you were before
cd ../../../
git clone https://github.com/key4hep/k4geo
export K4GEO=$PWD/k4geo/
```
NB: a typical DD4hep detector implementation has a C++ detector builder where the shapes, volumes and placedVolumes are defined plus an xml "compact" file that configures the detector (e.g. setting the dimensions) and from which the C++ builder retrieves all the free parameters. When modifying the compact file nothing has to be recompiled, when touching the C++ detector builder, `k4geo` has to be recompiled and some more environment variables have to be set in order to use your local detector builder. This can be done as follows:
```
# No need to run this for the tutorial, it is just here for completeness
cd k4geo
# modify a detector builder, e.g. detector/calorimeter/ECalBarrel_NobleLiquid_InclinedTrapezoids_o1_v03_geo.cpp
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install -j 8
cd ..
k4_local_repo # this updates environment variables and PATHs such as LD_LIBRARY_PATH
cd ..
```
In the xml compact file, the detector builder to use is specified by the `type` keyword in the `detector` beacon (e.g. `<detector id=1 name="MyCoolDetectorName" type="MYCOOLDETECTOR" ... />`) and it should match the detector type defined in the C++ builder with the instruction `DECLARE_DETELEMENT(MYCOOLDETECTOR)`.

Now lets first modify the sub-detector content of ALLEGRO. Since we will deal with the calorimeter, let's remove the muon system to run faster.
For this, you just need to open the main detector "compact file" (`xml` file with detector parameters) with your favorite text editor and remove the import of the muon system, for instance:

```
# copy paste won't work here
vim $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml
:51
dd
:wq
```

### Running a first ALLEGRO ECAL simulation

Let's now run a first particle gun simulation and reconstruction by following the instructions [here](https://github.com/HEP-FCC/FCC-config/tree/main/FCCee/FullSim/ALLEGRO/ALLEGRO_o1_v03#instructions), outside of the tutorial repository.
Once done, copy the output rootfile to the tutorial repository `fcc-tutorials/full-detector-simulations/FCCeeGeneralOverview/` and go back there.

<!--
```bash
cd fcc-tutorials/full-detector-simulations/FCCeeGeneralOverview/
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --gun.thetaMin "55*degree" --gun.thetaMax "125*degree"  --numberOfEvents 100 --outputFile electron_gun_10GeV_ALLEGRO_SIM.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml
```

And apply the ALLEGRO reconstruction, including an MVA based calibration:
```
wget https://fccsw.web.cern.ch/fccsw/tutorials/MIT2024/lgbm_calibration-CaloClusters.onnx # needed for the MVA calibration
k4run run_ALLEGRO_RECO.py --EventDataSvc.input="electron_gun_10GeV_ALLEGRO_SIM.root" --out.filename="electron_gun_10GeV_ALLEGRO_RECO.root"
```
-->

Now let's plot the energy resolution for raw clusters and MVA calibrated clusters:

```bash
python plot_calo_energy_resolution.py RECO_FILE_NAME.root
display electron_gun_10GeV_ALLEGRO_RECO_clusterEnergyResolution.png
display electron_gun_10GeV_ALLEGRO_RECO_calibratedClusterEnergyResolution.png
```

Look at both distributions to see how the MVA calibration affects the distribution.

### Changing Liquid Argon to Liquid Krypton

In a sampling calorimeter, the ratio between the energy deposited in the dead absorbers and sensitive media (sampling fraction) is an important parameter for energy resolution: the more energy in the sensitive media the better. Liquid Krypton being denser than Liquid Argon, it is an appealing choice for the detector design. Though it is more expensive and difficult to procure in real life, testing this option in Full Sim is extremely cheap:

```
# make sure you properly followed the steps described in the exercise "Modifying the sub-detector content"
# i.e. called k4_local_repo in your local k4geo repository, so that $K4GEO points to your modified version
vim $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ECalBarrel_thetamodulemerged.xml
# change "LAr" to "LKr" everywhere
:%s/LAr/LKr/gc
```

You can now re-run the simulation and reconstruction with the same steps as in the previous exercise.
The cluster energy distribution will show you that, to accommodate the change to LKr, the sampling fraction should be updated.
This is typically done by experts but a central recipe is being prepared for this.


<!--
And to accomodate this change, we have to update the sampling fraction in the steering file:

```
vim run_ALLEGRO_RECO.py
# comment out line 105 and uncomment line 106
```
The derivation of new sampling fractions upon geometry change is out of scope for this tutorial.

Let's now re-run the simulation with the modified detector:
```bash
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --gun.thetaMin "55*degree" --gun.thetaMax "125*degree"  --numberOfEvents 100 --outputFile electron_gun_10GeV_ALLEGRO_LKr_SIM.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v02/ALLEGRO_o1_v02.xml
k4run run_ALLEGRO_RECO.py --EventDataSvc.input="electron_gun_10GeV_ALLEGRO_LKr_SIM.root" --out.filename="electron_gun_10GeV_ALLEGRO_LKr_RECO.root"
python plot_calo_energy_resolution.py electron_gun_10GeV_ALLEGRO_LKr_RECO.root
display electron_gun_10GeV_ALLEGRO_LKr_RECO_clusterEnergyResolution.png
```

See how the energy resolution improved with LKr. NB: here the MVA calibration should be retrainned to achieve good performance.

-->


## Towards IDEA tracking with the detailed Drift Chamber

A first version of the IDEA tracking system is now available. We can therefore start working on tracking algorithms implementation. In this exercise, we will produce a dataset containing Vertex, Drift Chamber and Silicon Wrapper digitized hits which can be used as a starting point to develop these tracking algorithms.

For this, let's run the IDEA simulation and digitization by following the recipe [here](https://github.com/HEP-FCC/FCC-config/tree/main/FCCee/FullSim/IDEA/IDEA_o1_v03#instructions) (outside of the tutorial repository).

<!--
```bash
# if you did not follow the entire tutorial sequencially, you have to do the following first
# git clone https://github.com/HEP-FCC/fcc-tutorials
# cd fcc-tutorials/full-detector-simulations/FCCeeGeneralOverview/
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile electron_gun_10GeV_IDEA_SIM.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/IDEA/compact/IDEA_o1_v02/IDEA_o1_v02.xml
k4run run_IDEA_DIGI.py --EventDataSvc.input="electron_gun_10GeV_IDEA_SIM.root" --out.filename="electron_gun_10GeV_IDEA_DIGI.root"
```
-->

The following collections are the one to use for tracking:
```cpp
VTXBDigis                             edm4hep::TrackerHit3D
VTXDDigis                             edm4hep::TrackerHit3D
DCH_DigiCollection                    extension::SenseWireHit
SiWrBDigis                            edm4hep::TrackerHit3D
SiWrDDigis                            edm4hep::TrackerHit3D

```

You can now play with the digitized hits:
```cpp
root electron_gun_10GeV_IDEA_DIGI.root
# to be ran one by one (no full copy paste)
events->Draw("DCH_DigiCollection.distanceToWire")
events->Draw("DCHCollection.eDep/DCHCollection.pathLength", "DCHCollection.eDep/DCHCollection.pathLength < 4e-7") // this shows the de/dx from the simHits
```

## Detector visualization

Displaying detector geometries is very useful to understand what is actually being simulated without having to enter the code. One example of tool (out of many) is described here, chosen for its simplicity together with the particular feature of hosting the needed data locally, leading to smooth performance of the visualization.

Let's first generate the files containing the geometry that will be used by the display tool.

```bash
wget https://fccsw.web.cern.ch/fccsw/tutorials/static/python/dd4hep2root
chmod +x dd4hep2root
./dd4hep2root -c $K4GEO/FCCee/CLD/compact/CLD_o2_v05/CLD_o2_v05.xml -o CLD_o2_v05_geom.root
echo $PWD/CLD_o2_v05_geom.root
```

Now, let's copy the file containing the geometry on your local machine:

```
scp USERNAME@HOSTNAME:ABSOLUTE_PATH_TO_GEOMETRY .
```

Load the file from your computer with the triple-dot button of this webpage: [https://root.cern/js/latest/](https://root.cern/js/latest/).

From there, you can navigate the geometry hierarchy to see how volumes are nested, display all or parts of the detector (right click on a volume > Draw > all), play with the camera settings (right click on an empty space in the display window > Show Controls, Clipping > Enable X and Enable Y), etc. See the following picture for illustration:

```{figure} https://fccsw.web.cern.ch/fccsw/tutorials/MIT2024/pictures/JSROOT_Screenshot.png
:align: center
```

This tool is useful but not perfect and will not meet all the needs (especially
if you want to overlay a physics event). To go further, other solutions are
described in the dedicated
[Visualization](../Visualization/Visualization.md#visualization)
tutorial.

## Additional Resources
 - [Key4hep tutorial](https://key4hep.github.io/key4hep-doc/setup-and-getting-started/README.html)
 - [FCC Full Sim webpage](https://fcc-ee-detector-full-sim.docs.cern.ch/)
 - Bi-weekly FCC Full Sim [working meeting](https://indico.cern.ch/category/16938/)
