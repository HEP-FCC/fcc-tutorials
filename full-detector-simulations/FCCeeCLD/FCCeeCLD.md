
# FCCee: Full Simulation of CLD, the CLID detector for FCC

An adaptation of the CLIC detector for FCC-ee has been implemented and made available for tests at the times of the CDR
(see, for example, [N. Bacchetta et al., CLD -- A Detector Concept for the FCC-ee](https://arxiv.org/abs/1911.12230))
The DD4hep description, initially implemented under [iLCSoft/lcgeo](https://github.com/iLCSoft/lcgeo/tree/master/FCCee/compact), is now
availble under [FCCDetectors](https://github.com/HEP-FCC/FCCDetectors/tree/main/Detector/DetFCCeeCLD) which serves as reference.

While it is possible to the detector through `k4SimGeant4` for the Geant4-based full simulation and produce a `EDM4hep` output,
to use the iLCSoft reconstruction tools it is still required to go through the `SLCIO` file format.
The easiest way to do that is to use `DDSim` for the full simulation.
In this chapter we illustrate how to run this workflow.

## Setting up the environment

The solution described in this chapter is still in preview mode. Therefore we need the latest version of the software

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

## Generate some signal to process: taus from the particle gun

To illustrate this workflow we use a simple but significat example: single taus generated with the particle gun.
We generate this with `k4run` and we save the result in `stdHEP` format for later processing in `DDSim`. 
