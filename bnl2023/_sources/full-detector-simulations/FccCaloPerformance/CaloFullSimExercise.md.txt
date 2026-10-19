# Noble Liquid Calorimeter Full Simulation Exercise

:::{admonition} Learning Objectives
In this tutorial, you will learn how to run the full simulation of the FCC-ee High Granularity Noble Liquid Calorimeter. Among other topics, this exercise covers:
* the **generation** of particle gun events with $\pi^0$'s and $\gamma$'s  
* the **reconstruction** of calorimeter data, including calibration, clustering and noise
* the energy resolution **performance evaluation** 
* the modification of the **detector geometry**
:::
Let's get started!

## Setting up your environment

First, you have to log-in on LXPLUS (or any machine with cvmfs mounted), clone the repository if not already done, go to this exercise's folder and source the central Key4hep environment:

```bash
git clone https://github.com/HEP-FCC/fcc-tutorials
cd fcc-tutorials/full-detector-simulations/FccCaloPerformance/
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```
Make sure your setup of the FCC software is working with:

```bash
which fccrun
```
which should print a path similar to `/cvmfs/sw.hsf.org/spackages7/fccsw/1.0pre07/x86_64-centos7-gcc11.2.0-opt/gvetc/bin/fccrun`. Ask for help if it is not the case.

All good? Ok, let's do some physics then!

## Getting familiar with the detector geometry

The Geant4 detector geometry which is used for the full simulation is generated with the DD4hep framework. The detector description in this framework consists of two parts:
* a compiled C++ library that constructs the geometry: [ECalBarrelInclined_geo.cpp](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCChhECalInclined/src/ECalBarrelInclined_geo.cpp)   
* an xml file that sets parameters read by the C++ geometry builder to make the detector configurable without the need to recompile: [FCCee_ECalBarrel.xml](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml)

The idea is to set as parameters the quantities that will often change throughout the Detector R&D campaign (such as the geometrical extent or the material of a given component) and/or the one that have to be optimized. In order to build a complete detector, DD4hep also allows you to call multiple xml's corresponding to different sub-detectors which keeps things well factorized and provides a flexible plug-and-play approach. Even though we will deal only with calorimetric data in this exercise, the geometry we will use ([DetFCCeeIDEA-LAr](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml)) includes also a drift chamber, an HCAL, etc.

Take a few minutes to browse the above codes to get a glimpse of how things work.

Looking at [FCCee_ECalBarrel.xml](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml), try to answer the following questions:
* what is the thickness of readout electrodes?
:::{admonition} Answer
:class: toggle
This is defined by the variable `readout_thickness`: **1.2 mm**
:::
* how many longitudinal layers (i.e. radial segmentation) has this calorimeter?
:::{admonition} Answer
:class: toggle
The radial extent of each layer is set under the `layer` tag (mind that a layer can be 'repeated'): **12**
:::

## Running simple simulation and evaluating performance

Let's now run some simulation. The various FCCSW components are orchestrated with the [Gaudi](https://gaudi-framework.readthedocs.io/en/latest/) framework. 
The different steps of your simulation are defined in a python configuration (aka 'steering') file where you arrange various Gaudi `Algorithms` and `Tools` to get the desired behavior. 
Open the file `runCaloSim.py` and briefly browse it to get familiar with the `Gaudi` syntax. 
NB: everything defined as a `Gaudi::Property` in the C++ implementation (e.g. `MomentumMin` from `MomentumRangeParticleGun`) can be set at run time in command line arguments. 
The complete list of parameters that can be modified is displayed with `fccrun runCaloSim.py -h`.   

Run the simulation with  `fccrun runCaloSim.py` (you can safely ignore the warnings and the error about HistogramSvc). While this command runs, try to answer the following questions by browsing [runCaloSim.py](https://github.com/HEP-FCC/fcc-tutorials/blob/master/full-detector-simulations/FccCaloPerformance/runCaloSim.py):

- how to change the type of particle you shoot in the detector?
:::{admonition} Answer
:class: toggle
This is a particle gun property which is set by a parameter at the beginning of the file `pgun.PdgCodes = [pdgCode]`. NB: a mixture of particles can be used (it is a list).
:::
- how to modify the number of events that are generated?
:::{admonition} Answer
:class: toggle
This is defined by the `EvtMax` parameter of the `ApplicationMgr`
:::
- how many different values do we have for the sampling fraction? Why is that (physics-wise)?
:::{admonition} Answer
:class: toggle
We have 12 values for the sampling fraction, one per longitudinal layer. This is due to the geometry: the absorbers have a rectangular shape and the circumference is smaller at the inner radius than at the outer radius. The sensitive media is thus wider (compared to the non-sensitive media) when going to higher radius which is why the sampling fraction grows. Note that the first layer, called the pre-sampler, has a large sampling fraction because the absorbers are made of a material way lighter than Lead there. We do this to improve the quality of the upstream material correction discussed later.
:::

The above command generated 200 events with 10 GeV photon gun and ran the calorimeter reconstruction on it.
- Looking at the end of prompt output when running `runCaloSim.py`, what algorithm takes most of the computing time? What do you think this algorithm does?
:::{admonition} Answer
:class: toggle
The algorithm taking most of the computation time is `SimG4Alg:Execute`. It deals with the propagation of particles through matter and is especially dominated by the development of the electromagnetic shower which features a lot of secondary particles. NB: an alternative to this 'first principle' approach would be to develop the shower from a more empirical point of view through e.g. machine learning but this is not easy and goes beyond the scope of this tutorial. 
:::

Produce the energy resolution plot with `python plot_energy_resolution.py output_caloFullSim_10GeV_pdgId_22_noiseFalse.root` and display it with `display output_caloFullSim_10GeV_pdgId_22_noiseFalse_energyResolution.png`.
- Assuming there is no noise nor constant term, derive the sampling term of this version of the calorimeter based on the width of the Gaussian fit from the plot.
:::{admonition} Hint
:class: toggle
$\frac{\sigma_E}{E} = \frac{a}{\sqrt E},  \sigma_E = 0.28 \text{ GeV}, E = 10 \text{ GeV}, a = ?$
:::
:::{admonition} Answer
:class: toggle
$a = 0.09 \text{ Gev}^\frac{1}{2}$
NB: this is of course not the exact value of the sampling term since the noise and constant term should be considered and a fit on a large energy spectrum should be performed, see e.g. [here](https://indico.desy.de/event/33640/contributions/128389/attachments/77680/100499/20221006_Brieuc_Francois_Noble_Liquid_Calorimetry_forFCCee_ECFA_Workshop_DESY.pdf#page=3).
:::

## Changing the geometry

In this exercise, we will run the same simulation but with liquid Krypton instead of liquid Argon. To do so, you will have to modify the detector geometry xml living in the `FCCDetectors` git repository:
```bash
cd ../../../
git clone https://github.com/HEP-FCC/FCCDetectors
```
Open `FCCDetectors/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml` with your favorite editor and modify line 143 to fill the calorimeter with liquid Krypton (`LKr`) instead of liquid Argon (`LAr`).
Open `FCCDetectors/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml` with your favorite editor and delete line 42 (just because this detector needs constructor not available centrally yet).

In order to make sure `fccrun` uses your local version of the geometry you have to set the environment variable `FCCDETECTORS` so that it points to the right location (but first, we will save the current path so that we can re-use it later). 
```bash
export CENTRALFCCDETECTORS=$FCCDETECTORS
export FCCDETECTORS=$PWD/FCCDetectors
```

Now, let's go back to the tutorial repository and set the sampling fraction corresponding to the liquid Krypton scenario (liquid Krypton is denser than liquid Argon). NB: for simplicity, the new sampling fractions are given to you but they can be derived for any new geometry with the Gaudi algorithm [SamplingFractionInLayers](https://github.com/HEP-FCC/k4SimGeant4/blob/main/Detector/DetStudies/src/components/SamplingFractionInLayers.h) by switching the absorbers as `sensitive` in [FCCee_ECalBarrel.xml](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml). 

Run the following:
```bash
cd fcc-tutorials/full-detector-simulations/FccCaloPerformance/
# this sed command will change the sampling fraction to match the LKr scenario
sed -i 's/samplingFraction =.*,/samplingFraction = [0.43409357593, 0.1547424461, 0.193381391453, 0.217112491538, 0.232641970166, 0.243824523984, 0.252601621016, 0.259608181095, 0.266145090772, 0.270853520501, 0.275895174626, 0.308837752573],/' runCaloSim.py
```
Open `runCaloSim.py` and change the output root file name (`out.filename`) to avoid overwriting the previous sample (e.g. by adding `_LKr` before `.root`).

Run the simulation again, reproduce the performance plot using the new sample and look at the width of the Gaussian:

- How did the energy resolution change? Can you explain this behavior?
:::{admonition} Answer
:class: toggle
The energy resolution improved because we have now a higher ratio between sensitive and non-sensitive material budget. 
:::
- compute again the sampling term assuming a null noise and constant term
:::{admonition} Answer
:class: toggle
 $a = 0.07 \text{ Gev}^\frac{1}{2}$
 NB: this is of course not the exact value of the sampling term since the noise and constant term should be considered and a fit on a large energy spectrum should be performed, see e.g. [here](https://indico.desy.de/event/33640/contributions/128389/attachments/77680/100499/20221006_Brieuc_Francois_Noble_Liquid_Calorimetry_forFCCee_ECFA_Workshop_DESY.pdf#page=4).
:::

Before to move to the next exercise, roll back to the previous liquid Argon set-up:
```bash
git checkout runCaloSim.py
export FCCDETECTORS=$CENTRALFCCDETECTORS
```

## Adding noise

A further important step in having an accurate description of the detector response is to add electronics noise (pile-up noise can safely be ignored at FCC-ee). Generally speaking, the noise can depend on many factors such as the detector cell capacitance (and every cell can potentially have different shapes) or the readout channel it corresponds to. The noise tools foresee thus the possibility to have a single noise value per cell. For simplicity, we provided a Gaudi config with a flag to easily switch on the noise:
- revert to the version of the code without upstream energy correction: `git checkout runCaloSim.py`, `git checkout plot_energy_resolution.py`
- switch `addNoise` to True in `runCaloSim.py`
- remove cell collections from the output (`ECalBarrelPositionedCells` and `PositionedCaloClusterCells`) to keep the weight of the rootfile small 
- run the simulation. Simulating with noise takes longer (every single cell now has an energy deposit), jump thus now to the other exercises and do the following once the simulation is over.  
- produce the performance plot and compare it to the one without noise
- what do you observe?
:::{admonition} Answer
:class: toggle 
The resolution barely changed. This is partially due to the lack of statistics but also to the fact that the noise impact is small because this version of the calorimeter has been optimized to feature a low noise and at 10 GeV we are already dominated by the sampling term. 
:::

## Preparing for the next tutorial

Open a new terminal, go to the Full Sim tutorial repository `fcc-tutorials/full-detector-simulations/FccCaloPerformance/`, set your environment with `source /cvmfs/sw.hsf.org/key4hep/setup.sh`, revert to the original config version with `git checkout runCaloSim.py`, set `pgun.PhiMax` to `0` (for technical reasons) and launch a production of 1000 photons events (you have to change `EvtMax`). Open another terminal, and launch another 1000 events with neutral pions (you have to set the `pdgCode` to `111` and don't forget to also source the environment in this new terminal). 

## Bonus exercise


Write a macro that plots the longitudinal profile of the electromagnetic shower energy deposits and run it on both the photon and neutral pion samples.
:::{admonition} Hint
:class: toggle
- use a TProfile
- the radial extent of the sensitive calorimeter is 2160 mm to 2560 mm
- there are 12 longitudinal layers, the first one is 15 mm thick while the other ones are 35 mm thick 
- radius can be obtained from $\sqrt{x^2 + y^2}$, $x$ and $y$ are obtained with `PositionedCaloClusterCells.position.x` and `PositionedCaloClusterCells.position.y`, in mm
- For each event, sum the energy from cells in a given layer and normalize it to the cluster energy
:::

Compare the longitudinal shower profile for photons and neutral pions.
- What do you observe?
:::{admonition} Answer
:class: toggle
For a given cluster energy, the single photon showers deposit their energy deeper in the calorimeter than the showers from neutral pions. This is due to the fact that the latter correspond to two close-by photon showers with smaller energy. 
:::
