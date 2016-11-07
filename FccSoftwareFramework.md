FCCSW
==

Contents:

-   [FCCSW](#fccsw)
    -   [Overview](#overview)
    -   [Git guide for FCC](#git-guide-for-fcc)
    -   [CMake](#cmake)
    -   [Installation](#installation)
    -   [Example process](#example-process)
    -   [Exercises](#exercises)
        -   [1- Modifying an existing
            algorithm](#1-modifying-an-existing-algorith)
        -   [2- Changing an algorithm
            parameter](#2-changing-an-algorithm-paramete)
        -   [3- Adding a filtering
            algorithm](#3-adding-a-filtering-algorithm)

Overview
--

The FCC software framework is based on Gaudi, with a simple event data
model (EDM) library called PODIO (Plain Old Data Input / Output). The
code is managed with Git, and built using CMake.

Git guide for FCC
--

The code for both the FCC software and Gaudi is managed on Git
repositories. We have set up a short [Git guide](./FccSoftwareGit) for
people who are not familar with Git, and where we explain the
recommended way to contribute code to the FCC software.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
All new developers should read this guide.

CMake
--

The build process of the FCC software is managed with CMake. Here is a
[short CMake guide](./FccCMakeGuide.md) for FCC developers.

Installation
--

Log in an lxplus6 machine and follow [these
instructions](https://github.com/HEP-FCC/FCCSW), also see the [getting started instructions](./FccSoftwareGettingStarted.md).

Example process
--

An example configuration file is provided in
[simple\_workflow.py](https://github.com/HEP-FCC/FCCSW/blob/tutorial/simple_workflow.py). This configuration file allows to execute the following tasks for each
event:

-   read an [HepMC](http://lcgapp.cern.ch/project/simu/HepMC/20400/html/classHepMC_1_1GenEvent.html) text file
-   convert the HepMC particles to a collection of EDM
    [ParticleCollection](http://fccsw.web.cern.ch/fccsw/fcc-edm/d5/d95/classfcc_1_1_m_c_particle_collection.html)
-   read the EDM
    [Particles](http://fccsw.web.cern.ch/fccsw/fcc-edm/0.4/de/d22/classfcc_1_1_m_c_particle.html)
    and use fastjet to cluster them into EDM [Jets](http://fccsw.web.cern.ch/fccsw/fcc-edm/0.4/d9/dd7/classfcc_1_1_gen_jet.html) .
-   write an EDM root file


Run Gaudi on the example HepMC source text file (1000 Z production events in an e+e- collider at sqrt(s) = 91 GeV) using this configuration file:

```bash
    ./run gaudirun.py Examples/options/simple_workflow.py
```

Please have a detailed look at [simple\_workflow.py](https://github.com/HEP-FCC/FCCSW/blob/master/Examples/options/simple_workflow.py).
.

Exercises
--

### 1- Modifying an existing algorithm

-   locate the C++ code of the jet clustering algorithm (maybe do a
    recursive grep for jet or clustering?)
-   add a printout for the reconstructed jets in the `execute`
    function of the jet clustering algorithm.
-   recompile and run again:

~~~{.sh}
# in the FCCSW directory:
make
~~~

Note how the total energy is generally way too high. It is due to the
fact that both stable and unstable particles are clustered into jets,
hence a double counting of the energy. In exercise 3, we will see how to
filter the generated particles to send only the stables ones to jet
clustering.

### 2- Changing an algorithm parameter

Open [JetClustering.cpp](https://github.com/HEP-FCC/FCCSW/blob/master/Reconstruction/src/JetClustering.cpp), and have a look at the constructor of the class. Several properties
are declared.

Properties can be set in the configuration file.

Change the configuration of the JetClustering algorithm in the following
way:

~~~{.py}
    genjet_clustering = JetClustering_MCParticleCollection_GenJetCollection_(
        "GenJetClustering",
        ptMin = 30.,
        )
~~~

And check the results.

### 3- Adding a filtering algorithm

The goal of this exercise is to fix the energy double counting obersved
in exercise 1. The current algorithm sequence contains three algorithms:
`[reader, hepmc_converter, genjet_clustering]`. We want to insert a
new algorithm in the sequence, which would become:
`[reader, hepmc_converter, genp_filter, genjet_clustering]`.

The new algorithm, `genp_filter`, will:

-   read in input the genparticles created by the `hepmc_converter`
-   write in output a copy of all the stable gen particles (status 1),
    discarding the other particles.

Go to the `Generation/` directory.

~~~{.sh}
cd Generation/src/components
~~~

Take the HepMCConverter as a base, and make a GenParticleFilter
algorithm:

~~~{.sh}
cp ReadTestConsumer.cpp MyGenParticleFilter.cpp
~~~

Since you created new files, next time you compile, you will need to do
the following so that your files are detected by the build system:

~~~{.sh}
cd ../../../ # go to the FCCSW root directory
make configure
make -j 4
~~~

When you just edit existing files, don't reconfigure, and just do:

~~~{.sh}
make -j 4
~~~

**Edit the GenParticleFilter** so that:

-   the class name matches your file name (also note the `DECLARE_COMPONENT` at the end of the file)
-   it creates as output a MCParticleCollection (see [HepMCConverter](https://github.com/HEP-FCC/FCCSW/blob/master/Generation/src/HepMCConverter.cpp))
-   it copies only the particles with status 1 to the output collection
    (see the [MCParticle.h](http://fccsw.web.cern.ch/fccsw/fcc-edm/0.4/de/d22/classfcc_1_1_m_c_particle.html)
    and [BareParticle.h](http://fccsw.web.cern.ch/fccsw/fcc-edm/0.4/d2/df9/classfcc_1_1_bare_particle.html)
    classes to see which data members are available)

Finally, insert the new algorithm in the sequence in the configuration
file, and run again. Check the printout and make sure that the jet
energy is now what you would expect (around 45 GeV).
