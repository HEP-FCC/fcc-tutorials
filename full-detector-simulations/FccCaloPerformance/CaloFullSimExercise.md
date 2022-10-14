# Welcome to the Calorimeter Full Simulation Exercise!

In this tutorial, you will learn how to run the full simulation of the FCC-ee High Granularity Noble Liquid Calorimeter full simulation. Among other topics, this exercise covers:
* the **generation** of particle gun events with $\pi^0$'s and $\gamma$'s  
* the **reconstruction** of calorimeter data, including calibration, clustering and noise
* the energy resolution **performance evaluation** 

Let's get started!

## Setting up your environment

First, you have to log-in on LXPLUS, clone the repository if not already done, go to this exercise's folder and source the central KEY4hep environment script:

```bash
git clone https://github.com/HEP-FCC/fcc-tutorials
cd fcc-tutorials/full-detector-simulations/FccCaloPerformance/
git checkout fccswtuto2022
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```
Make sure your setup of the FCC software is working with:

```bash
which fccrun
```
which should print a path similar to `/cvmfs/sw.hsf.org/spackages6/fccsw/1.0pre06/x86_64-centos7-gcc11.2.0-opt/26ihv/bin/fccrun`.  Ask for help if it is not the case.

All good? Ok, let's do some physics then!

## Exercise 1: Get familiar with the detector geometry

The Geant4 detector geometry which is used for the full simulation is not written directly, but generated with the DD4hep library. The detector description in this library consists of two parts:
* a compiled C++ library that constructs the geometry: [ECalBarrelInclined_geo.cpp](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCChhECalInclined/src/ECalBarrelInclined_geo.cpp)   
* an xml file that sets parameters read by the C++ geometry builder to make the detector configurable without the need to recompile: [FCCee_ECalBarrel.xml](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml)

The idea is to set as parameters the quantities that will often change throughout the Detector R&D campaign (such as the geometrical extent or the material of a given component) and/or the one that have to be optimized. In order to build a complete detector, DD4hep also allows you to call multiple xml's corresponding to different sub-detectors which keeps things well factorized and provides a flexible plug-and-play approach. Even though we will deal only with calorimetric data in this exercise, the geometry we will use ([DetFCCeeIDEA-LAr](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml)) includes also a drift chamber, an HCAL, etc.

Take a few minutes to browse the above codes to get a glimpse of how things work.

The detector can also be visualized by running `python display_detector.py`.

Using either the prints from the above command or the xml files, try to answer the following questions:
* what is the thickness of the cryostat in front of the calorimeter?
* what is the type of noble liquid used?
* what are the absorbers made of?
* how many longitudinal layers has this calorimeter?

## Exercise 2: Run simple simulation and evaluate performance

FCCSW is based on the [Gaudi](https://gaudi-framework.readthedocs.io/en/latest/) framework. The different steps of your simulation are defined in a python configuration file where you arrange various Gaudi `Algorithms` and `Tools` to get the desired behavior. Open the file `runCaloSim.py` and briefly browse it to get familiar with the `Gaudi` syntax. Try to answer the following questions:
- how to modify the number of events?
-  how to change the type of particle you shoot in the detector?
- how to modify the sampling fraction?
- why is there one sampling fraction per longitudinal layers?
- how is the clustering algorithm called? 

NB: everything defined as a `Gaudi::Property` (e.g. `MomentumMin` from `MomentumRangeParticleGun`) can be set at run time in command line arguments. The complete list of parameters that can be modified at run time is displayed with `fccrun runCaloSim.py -h`.   

Let's run some simulations now! Execute the following commands:
```bash
fccrun runCaloSim.py
python plot_energy_resolution.py #FIXME
display #FIXME
```

This generated 200 events with 10 GeV photon gun, ran the calorimeter reconstruction on it and produced energy resolution plot.

- Assuming there is no noise nor constant term, derive the sampling term of this version of the calorimeter
:::{admonition} Hint
:class: toggle
$\frac{\sigma_E}{E} = \frac{a}{\sqrt E},  \sigma_E = 0.32 \text{ GeV}, E = 10 \text{ GeV}, a = ?$
:::

## Exercise 3: Change the geometry

In this exercise, we will run the same simulation but with liquid Krypton instead of liquid Argon. To do so, you will have to modify the detector geometry xml living in the `FCCDetectors` git repository:
```bash
cd ../../../
git clone https://github.com/HEP-FCC/FCCDetectors
vim FCCDetectors/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml
:102
:s/LAr/LKr/
:wq
```
In order to propagate this change you have to set the environment variable `FCCDETECTORS` to point to your local version. Check where it points now with `echo $FCCDETECTORS`. Change it with 
```bash
export FCCDETECTORS=$PWD/FCCDetectors
```
and check that it has correctly been modified with `echo $FCCDETECTORS`.

Now, let's go back to the tutorial repository and set the sampling fraction corresponding to the liquid Krypton scenario. For simplicity, the new sampling fractions are given to you but they can be derived for any new geometry with the Gaudi algorithm [SamplingFractionInLayers](https://github.com/HEP-FCC/k4SimGeant4/blob/main/Detector/DetStudies/src/components/SamplingFractionInLayers.h) by switching the absorbers as `sensitive` in [FCCee_ECalBarrel.xml](https://github.com/HEP-FCC/FCCDetectors/blob/main/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml). Run the following:
```bash
cd fcc-tutorials/full-detector-simulations/FccCaloPerformance/
sed runCaloSim.py #FIXME
```
Open `runCaloSim.py` and change the output root file name (`out.filename`) to avoid overwriting the previous sample (e.g. by adding `_LKr` before `.root`).

Run the simulation again, reproduce the performance plot and compare it to the one obtained with liquid Argon:
- how did the energy resolution change?
- can you explain why?
- compute again the sampling term assuming 0 noise and constant term

Before to move to the next exercise, roll back to the previous liquid argon set-up:
```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
git checkout runCaloSim.py
```

## Exercise 4: Apply energy corrections

As you may have noticed in the previous exercises, the reconstructed energy is, on average, below the generated energy. This is due to the fact that some energy is deposited in part of the detector which are not sensitive such as the cryostat walls. Hopefully, there is a strong correlation between the energy which is deposited before(after) the sensitive calorimeter and the energy we measure in the first(last) longitudinal layer. This correction is derived with #FIXME and applied with #FIXME.

Since you are now more familiar with the framework, no recipe will be provided for this exercise. Try to do the following to apply the dead material energy correction:

-  un-comment the code snippet corresponding to the cluster correction
- add this Gaudi algorithm to the `TopAlg` sequence (the order of the algorithms matters!)
- add a 

## Exercise #FIXME: prepare the next tutorial


