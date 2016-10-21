---
layout: site
---
[]() FCCSW
==========

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

[]() Overview
-------------

The FCC software framework is based on Gaudi, with a simple event data
model (EDM) library called PODIO (Plain Old Data Input / Output). The
code is managed with Git, and built using CMake.

[]() Git guide for FCC
----------------------

The code for both the FCC software and Gaudi is managed on Git
repositories. We have set up a short [Git guide](./FccSoftwareGit) for
people who are not familar with Git, and where we explain the
recommended way to contribute code to the FCC software.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
All new developers should read this guide.

[]() CMake
----------

The build process of the FCC software is managed with CMake. Here is a
[short CMake guide](./FccCMakeGuide){.twikiLink} for FCC developers.

[]() Installation
-----------------

Log in an lxplus6 machine and follow [these
instructions](https://github.com/HEP-FCC/FCCSW) .

[]() Example process
--------------------

An example configuration file is provided in
[simple\_workflow.py](https://github.com/HEP-FCC/FCCSW/blob/tutorial/simple_workflow.py)
. This configuration file allows to execute the following tasks for each
event:

-   read an
    [HepMC](http://lcgapp.cern.ch/project/simu/HepMC/20400/html/classHepMC_1_1GenEvent.html)
    text file
-   convert the <span class="twikiNewLink"> HepMC </span> particles to a
    collection of EDM
    [ParticleCollection](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/datamodel/datamodel/MCParticleCollection.h)
    (also see the <span class="twikiNewLink"> MCParticleCollection
    </span>
    [doxygen](http://fccsw.web.cern.ch/fccsw/fcc-edm/d5/d95/classfcc_1_1_m_c_particle_collection.html) )
-   read the EDM
    [Particles](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/datamodel/datamodel/MCParticle.h)
    (also see the MCParticle
    [doxygen](http://fccsw.web.cern.ch/fccsw/fcc-edm/de/d22/classfcc_1_1_m_c_particle.html) )
    and use fastjet to cluster them into EDM
    [Jets](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/datamodel/datamodel/GenJet.h) .
-   write an EDM root file

Get a source <span class="twikiNewLink"> HepMC </span> text file (1000 Z
production events in an e+e- collider at sqrt(s) = 91 <span
class="twikiNewLink"> GeV </span> ):

    cp /afs/cern.ch/user/c/cbern/public/pythia_Z_91_hepmc.dat example_MyPythia.dat

Run Gaudi on this configuration file:

    ./run gaudirun.py simple_workflow.py

Please have a detailed look at
[simple\_workflow.py](https://github.com/HEP-FCC/FCCSW/blob/tutorial/simple_workflow.py)
.

[]() Exercises
--------------

### []() 1- Modifying an existing algorithm

-   locate the C++ code of the jet clustering algorithm (maybe do a
    recursive grep for jet or clustering?)
-   add a printout for the reconstructed jets in the `    execute   `
    function of the jet clustering algorithm.
-   recompile and run again:

           cd $FCCSW
           make 

Note how the total energy is generally way too high. It is due to the
fact that both stable and unstable particles are clustered into jets,
hence a double counting of the energy. In exercise 3, we will see how to
filter the generated particles to send only the stables ones to jet
clustering.

### []() 2- Changing an algorithm parameter

Open
[JetClustering.cpp](https://github.com/HEP-FCC/FCCSW/blob/tutorial/Reconstruction/src/JetClustering.cpp)
, and have a look at the constructor of the class. Several properties
are declared.

Properties can be set in the configuration file.

Change the configuration of the JetClustering algorithm in the following
way:

    genjet_clustering = JetClustering_MCParticleCollection_GenJetCollection_(
        "GenJetClustering",
        ptMin = 30.,
        )

And check the results.

### []() 3- Adding a filtering algorithm

The goal of this exercise is to fix the energy double counting obersved
in exercise 1. The current algorithm sequence contains three algorithms:
`  [reader, hepmc_converter, genjet_clustering]` . We want to insert a
new algorithm in the sequence, which would become:
`  [reader, hepmc_converter, genp_filter, genjet_clustering]` .

The new algorithm, `  genp_filter` , will:

-   read in input the genparticles created by the
    `    hepmc_converter   `
-   write in output a copy of all the stable gen particles (status 1),
    discarding the other particles.

Go to the `  Generation/` directory.

     
    cd Generation/src

Take the HepMCConverter as a base, and make a GenParticleFilter
algorithm:

    cp HepMCConverter.h GenParticleFilter.h
    cp HepMCConverter.cpp GenParticleFilter.cpp

Since you created new files, next time you compile, you will need to do
the following so that your files are detected by the build system:

    cd $FCCSW
    rm build.x86_64-slc6-gcc48-opt/CMakeCache.txt 
    make -j 4

When you just edit existing files, don't remove the `  CMakeCache.txt`
file, and just do:

    cd $FCCSW
    make -j 4 

**Edit the GenParticleFilter** so that:

-   it takes in input a <span class="twikiNewLink"> MCParticleCollection
    </span>
-   it creates in output a <span class="twikiNewLink">
    MCParticleCollection </span> (see
    [HepMCConverter.cpp](https://github.com/HEP-FCC/FCCSW/blob/tutorial/Generation/src/HepMCConverter.cpp) )
-   it copies only the particles with status 1 to the output collection
    (see the
    [MCParticle.h](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/datamodel/datamodel/MCParticle.h)
    and \[
    [BareParticle.h](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/datamodel/datamodel/BareParticle.h)
    classes to see which data members are available)

Finally, insert the new algorithm in the sequence in the configuration
file, and run again. Check the printout and make sure that the jet
energy is now what you would expect (around 45 <span
class="twikiNewLink"> GeV </span> ).

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 11 December
2014
