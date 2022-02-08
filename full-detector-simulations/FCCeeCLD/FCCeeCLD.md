
# FCCee: Full Simulation of CLD, the adaptation of teh CLID detector to FCC-ee

An adaptation of the CLIC detector for FCC-ee has been implemented and made avaiable for tests.
The DD4hep description, initially implemented under [iLCSoft/lcgeo](https://github.com/iLCSoft/lcgeo/tree/master/FCCee/compact), is now
availble under [FCCDetecrors]() which serves as reference.
While it is possible to the detector through k4SimGeant4 for the Geant4-based full simulation ad produce a EDM4hep output,
to use the iLCSoft reconstruction tools it is still required to go through the SLCIO file format.
The easiest way to do that is to use DDSim for the full simulation.
In this chapter we illustrate how to achieve that.

