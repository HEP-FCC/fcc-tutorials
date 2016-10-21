---
layout: site
thisversion: ""
---

FCC: Getting started with the production and analysis of fast-simulated events
===================================================================================


Contents:

-   [FCC: Getting started with the production and analysis of
    fast-simulated events](#FCC_Getting_started_with_the_pro)
    -   [Overview](#overview)
    -   [Installation](#installation)
        -   [Installing the FCC software on
            lxplus](#installing-the-fcc-software-on-l)
            -   [Optional : install FCCSW](#optional-install-fccsw)
            -   [Install heppy](#install-heppy)
        -   [Using the virtual machine](#using-the-virtual-machine)
            -   [Installing and running the
                machine](#installing-and-running-the-machi)
            -   [FAQ](#faq)
                -   [My keyboard is not correctly
                    recognized](#my-keyboard-is-not-correctly-rec)
                -   [How can I copy-paste on a mac with
                    a touchpad.](#how-can-i-copy-paste-on-a-mac-wi)
                -   [I'm getting messages about mouse and keyboard
                    capture](#i-m-getting-messages-about-mouse)
    -   [Getting started with papas (FCC-ee)](#getting-started-with-papas-fcc-ee)
        -   [Set up your working directory](#set-up-your-working-directory)
        -   [Generate events with pythia8](#generate-events-with-pythia8)
        -   [Run papas and the analysis in heppy](#run-papas-and-the-analysis-in-he)
        -   [Make plots](#make-plots)
        -   [Re-running the tutorial after logging out.](#re-running-the-tutorial-after-logging-out)
    -   [Getting started with Delphes (FCC-hh)](#getting-started-with-delphes-fcc-hh)
        -   [Set up your working directory](#set-up-your-working-directory)



Overview
-------------

If you want to get started fast with the analysis of fast-simulated
events, you're at the right place.

We currently support two different approaches for fast simulation, Papas
and Delphes. For now, FCC-ee users are encouraged to use Papas, while
FCC-hh and FCC-eh users should use Delphes. However, ultimately, all
users are encouraged to try both fast simulations and to compare the
results.

An analysis ntuple will be produced with heppy, a simple modular event
processing framework for high energy physics.

Installation
-----------------

If you have a full CERN account, the easiest is to follow the lxplus
installation instructions. If you only have a lightweight CERN account,
we provide a virtual machine with all the necessary software
preinstalled.

### Installing the FCC software on lxplus

Log to lxplus:

    ssh -Y your_username@lxplus.cern.ch

Create a base directory for the FCC software:

    mkdir FCC
    cd FCC
    export FCC=$PWD

Source the script for the definition of the FCC environment:

    source /afs/cern.ch/exp/fcc/sw/0.7/init_fcc_stack.sh

**You will need to source this script everytime you want to use the
software.**

#### Optional : install FCCSW

**If you do plan to use functionality of FCCSW (e.g. Pythia generator,
Delphes, etc.), follow this section, if not skip to [next section](#FccPhysicsAnalysisTools)**.

To get started, you are going to use [FCCSW](https://github.com/HEP-FCC/FCCSW) , the FCC full software
framework.

Get the code of FCCSW:

Tutorial branch - to follow the tutorial:

    git clone https://github.com/HEP-FCC/FCCSW.git -b tutorial
    cd FCCSW 

or the master branch - to proceed with a full version

    git clone https://github.com/HEP-FCC/FCCSW.git -b master
    cd FCCSW 

Follow [these instructions](https://github.com/HEP-FCC/FCCSW/blob/tutorial/README.md)
to compile and test [FCCSW](https://github.com/HEP-FCC/FCCSW). The simplest option is
below:

    cd ../
    export FCCBASE=$PWD
    export FCCSW=$FCCBASE/FCCSW
    cd $FCCSW
    make -j 12 

In case of problems, please do not proceed any further and contact J. Lingemann.

#### Install heppy


[heppy](https://github.com/HEP-FCC/heppy.git) is a python
framework for high-energy physics event processing.

Get the code:

    git clone https://github.com/HEP-FCC/heppy.git -b tutorial
    cd heppy

Follow [these instructions](https://github.com/HEP-FCC/heppy/blob/tutorial/README.md)
to set up and test [heppy](https://github.com/HEP-FCC/heppy.git).

In case of problems, please do not proceed any further and contact C.
Bernet

### Using the virtual machine

#### Installing and running the machine

A virtual machine is just like a real machine, except that the machine
hardware is emulated by software. The virtual machine, often called the
"guest", runs in a "host" operating system (OS).

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) .

Get the virtual machine, located at

    /afs/cern.ch/exp/fcc/vms/Ubuntu_14.04.3_LTS_4March16.ova

Import this virtual machine in [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (File menu,
then Import Appliance).

Start the machine, and open a terminal (black icon below the firefox
icon in the left tool bar).

#### FAQ

##### My keyboard is not correctly recognized

This virtual machine was prepared with a US keyboard. If you're using a
French or Swiss keyboard, just switch by clicking on "EN" at the top
right of the screen.

##### How can I copy-paste on a mac with a touchpad.

Assuming you have selected some text in a terminal of the ubuntu guest.

Solution 1 (only works in a terminal, not in an xterm)

-   click on your pad with two fingers, and select copy
-   click on your pad with two fingers, and select paste

Solution 2:

-   get an external mouse, and click the middle button

If you manage to emulate a middle click on the pad in the guest, please
tell Colin
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")

##### I'm getting messages about mouse and keyboard capture

You can safely ignore them, and google these messages if you want to
know more.

Getting started with papas (FCC-ee)
----------------------------------------

In this tutorial, you will learn how to:

-   generate events with pythia8 and write them in the FCC EDM format.
-   read these events with heppy to run the papas simulation and the
    analysis to create an ntuple
-   read this ntuple in a python ROOT macro to make basic plots

But first, you will set up a working directory for your analysis.

### Set up your working directory

Create a directory anywhere, e.g. in your FCC directory:

    cd $FCC
    mkdir Workdir
    cd Workdir

Get a pythia8 card file to generate ZH events. To download this file, on
linux, do:

    wget https://raw.githubusercontent.com/HEP-FCC/fcc-physics/tutorial/pythia8/ee_ZH_Zmumu_Hbb.txt

On MacOS, do:

    curl -O https://raw.githubusercontent.com/HEP-FCC/fcc-physics/tutorial/pythia8/ee_ZH_Zmumu_Hbb.txt

Get the [heppy](https://github.com/HEP-FCC/heppy.git) configuration file
for a ZH analysis:

    cp $FCC/heppy/test/analysis_ee_ZH_cfg.py .

### Generate events with pythia8

Here, we decide to use the standalone fcc-physics package to generate
events instead of FCCSW. The advantage of the fcc-physics package is
that it is supported for several operating systems, and in particular
for mac os X and linux while FCCSW only works on lxplus. In other words,
you could use fcc-physics to generate events on your notebook. That
being said, it is of course possible to generate events with FCCSW.

Generate ee to ZH events with Z to mumu and H to b bbar:

    fcc-pythia8-generate ee_ZH_Zmumu_Hbb.txt 

You should obtain a file `ee_ZH_Zmumu_Hbb.root` written in the
FCC EDM format. Let us open it and check the contents:

    root  ee_ZH_Zmumu_Hbb.root 
    events->Print()

You're getting a list of the available collections. You can use root to
draw the distribution of a variable. For example, the distribution of
the charge of the stable generated muons:

    events->Draw("GenParticle.Core.Charge", "abs(GenParticle.Core.Type)==13 && GenParticle.Core.Status==1")

exit root:

    .q

We are now going to run the papas simulation and to build an ntuple with
meaningful variables for the analysis.

### Run papas and the analysis in heppy

The ROOT file obtained in the previous section contains for each event
all generated particles produced by pythia.

In this section we will run an [heppy](https://github.com/HEP-FCC/heppy.git) job to:
-   run papas, a fast simulation that processes these generated
    particles to produce "reconstructed" particles;
-   process the papas reconstructed particles and compute various
    analysis variables;
-   store these variables in an ntuple written in an output root file.

The [heppy](https://github.com/HEP-FCC/heppy.git) configuration file
[analysis\_ee\_ZH\_cfg.py](https://github.com/HEP-FCC/heppy/blob/tutorial/test/analysis_ee_ZH_cfg.py)
describes these steps.

First, produce the display for the first event:

    ipython -i analysis_ee_ZH_cfg.py 0

You should get an event display. Move to the next event, and print the
event content:

    next()
    print loop.event

You should get a printout like:

```
    {   'eventWeight': 1,
        'gen_particles': [   Particle : pdgid =    25, status =  22, q =  0 pt =  55.4, e = 137.7, eta = -0.29, theta = -0.29, phi =  2.74, mass = 125.00,
                             Particle : pdgid =    25, status =  62, q =  0 pt =  55.4, e = 137.7, eta = -0.29, theta = -0.29, phi =  2.74, mass = 125.00,
                             Particle : pdgid =    11, status =   4, q = -1 pt =   0.0, e = 120.0, eta =   inf, theta =  1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =   -11, status =   4, q =  1 pt =   0.0, e = 120.0, eta =  -inf, theta = -1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =   -11, status =  61, q =  1 pt =   0.0, e = 120.0, eta =  -inf, theta = -1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =   -11, status =  21, q =  1 pt =   0.0, e = 120.0, eta =  -inf, theta = -1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =    11, status =  61, q = -1 pt =   0.0, e = 120.0, eta =   inf, theta =  1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =    11, status =  21, q = -1 pt =   0.0, e = 120.0, eta =   inf, theta =  1.57, phi =  0.00, mass =  0.00,
                             Particle : pdgid =    23, status =  22, q =  0 pt =  55.4, e = 102.3, eta =  0.29, theta =  0.29, phi = -0.40, mass = 84.50,
                             Particle : pdgid =    23, status =  62, q =  0 pt =  55.4, e = 102.3, eta =  0.29, theta =  0.29, phi = -0.40, mass = 84.50,
                             '...',
                             Particle : pdgid =    22, status =   1, q =  0 pt =   0.0, e =   0.0, eta =  -inf, theta = -1.57, phi =  0.00, mass =  0.00],
        'gen_particles_stable': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.1, e =  57.2, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                                    Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11,
                                    Particle : pdgid =    22, status =   1, q =  0 pt =  22.7, e =  23.4, eta =  0.24, theta =  0.24, phi =  2.75, mass =  0.00,
                                    Particle : pdgid =  -211, status =   1, q = -1 pt =  10.0, e =  10.1, eta =  0.15, theta =  0.14, phi =  2.80, mass =  0.14,
                                    Particle : pdgid =    22, status =   1, q =  0 pt =   8.3, e =   8.4, eta =  0.16, theta =  0.16, phi =  2.81, mass = -0.00,
                                    Particle : pdgid =    22, status =   1, q =  0 pt =   7.9, e =   8.1, eta =  0.25, theta =  0.25, phi =  2.75, mass = -0.00,
                                    Particle : pdgid =  -321, status =   1, q = -1 pt =   6.0, e =   7.5, eta = -0.70, theta = -0.65, phi = -0.21, mass =  0.49,
                                    Particle : pdgid =    22, status =   1, q =  0 pt =   7.3, e =   7.3, eta =  0.07, theta =  0.07, phi =  2.61, mass = -0.00,
                                    Particle : pdgid =   211, status =   1, q =  1 pt =   6.8, e =   6.9, eta =  0.19, theta =  0.19, phi =  2.90, mass =  0.14,
                                    Particle : pdgid =    22, status =   1, q =  0 pt =   4.6, e =   4.6, eta =  0.12, theta =  0.12, phi =  2.46, mass =  0.00,
                                    '...',
                                    Particle : pdgid =    22, status =   1, q =  0 pt =   0.1, e =   0.1, eta = -0.02, theta = -0.02, phi =  2.59, mass = -0.00],
        'higgses': [   Resonance2 : pdgid =    25, status =   3, q =  0 pt =  59.3, e = 131.7, eta = -0.20, theta = -0.19, phi =  2.74, mass = 117.08],
        'higgses_legs': [   Jet : pt =  89.4, e =  92.9, eta =  0.13, theta =  0.13, phi =  2.77, mass = 22.34, tags=,
                            Jet : pt =  30.1, e =  38.8, eta = -0.72, theta = -0.67, phi = -0.33, mass =  5.89, tags=],
        'iEv': 2,
        'jets': [   Jet : pt =  89.4, e =  92.9, eta =  0.13, theta =  0.13, phi =  2.77, mass = 22.34, tags=,
                    Jet : pt =  30.1, e =  38.8, eta = -0.72, theta = -0.67, phi = -0.33, mass =  5.89, tags=],
        'leptons': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.5, e =  57.7, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                       Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11],
        'leptons_true': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.1, e =  57.2, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                            Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11],
        'particles': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.1, e =  57.2, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                         Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11,
                         Particle : pdgid =    22, status =   1, q =  0 pt =  31.2, e =  32.1, eta =  0.24, theta =  0.24, phi =  2.75, mass = -0.00,
                         Particle : pdgid =  -211, status =   1, q = -1 pt =  10.1, e =  10.2, eta =  0.15, theta =  0.14, phi =  2.80, mass =  0.14,
                         Particle : pdgid =    22, status =   1, q =  0 pt =   9.3, e =   9.4, eta =  0.16, theta =  0.16, phi =  2.81, mass =  0.00,
                         Particle : pdgid =    22, status =   1, q =  0 pt =   7.7, e =   7.8, eta =  0.11, theta =  0.11, phi =  2.45, mass =  0.00,
                         Particle : pdgid =    22, status =   1, q =  0 pt =   7.6, e =   7.6, eta =  0.07, theta =  0.07, phi =  2.61, mass =  0.00,
                         Particle : pdgid =  -211, status =   1, q = -1 pt =   5.9, e =   7.4, eta = -0.70, theta = -0.65, phi = -0.21, mass =  0.14,
                         Particle : pdgid =   211, status =   1, q =  1 pt =   6.7, e =   6.8, eta =  0.19, theta =  0.19, phi =  2.90, mass =  0.14,
                         Particle : pdgid =  -211, status =   1, q = -1 pt =   4.4, e =   4.5, eta =  0.19, theta =  0.19, phi =  2.86, mass =  0.14,
                         '...',
                         Particle : pdgid =    22, status =   1, q =  0 pt =   0.3, e =   0.5, eta = -0.90, theta = -0.80, phi =  0.22, mass =  0.00],
        'particles_not_zed': [   Particle : pdgid =    22, status =   1, q =  0 pt =  31.2, e =  32.1, eta =  0.24, theta =  0.24, phi =  2.75, mass = -0.00,
                                 Particle : pdgid =  -211, status =   1, q = -1 pt =  10.1, e =  10.2, eta =  0.15, theta =  0.14, phi =  2.80, mass =  0.14,
                                 Particle : pdgid =    22, status =   1, q =  0 pt =   9.3, e =   9.4, eta =  0.16, theta =  0.16, phi =  2.81, mass =  0.00,
                                 Particle : pdgid =    22, status =   1, q =  0 pt =   7.7, e =   7.8, eta =  0.11, theta =  0.11, phi =  2.45, mass =  0.00,
                                 Particle : pdgid =    22, status =   1, q =  0 pt =   7.6, e =   7.6, eta =  0.07, theta =  0.07, phi =  2.61, mass =  0.00,
                                 Particle : pdgid =  -211, status =   1, q = -1 pt =   5.9, e =   7.4, eta = -0.70, theta = -0.65, phi = -0.21, mass =  0.14,
                                 Particle : pdgid =   211, status =   1, q =  1 pt =   6.7, e =   6.8, eta =  0.19, theta =  0.19, phi =  2.90, mass =  0.14,
                                 Particle : pdgid =  -211, status =   1, q = -1 pt =   4.4, e =   4.5, eta =  0.19, theta =  0.19, phi =  2.86, mass =  0.14,
                                 Particle : pdgid =  -211, status =   1, q = -1 pt =   3.2, e =   4.1, eta = -0.76, theta = -0.70, phi = -0.37, mass =  0.14,
                                 Particle : pdgid =  -211, status =   1, q = -1 pt =   3.1, e =   3.6, eta = -0.56, theta = -0.54, phi = -0.31, mass =  0.14,
                                 '...',
                                 Particle : pdgid =    22, status =   1, q =  0 pt =   0.3, e =   0.5, eta = -0.90, theta = -0.80, phi =  0.22, mass =  0.00],
        'recoil': Particle : pdgid =     0, status =   1, q =  0 pt =  55.6, e = 137.2, eta = -0.29, theta = -0.29, phi =  2.74, mass = 124.31,
        'sel_iso_leptons': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.5, e =  57.7, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                               Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11],
        'sim_particles': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.1, e =  57.2, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                             Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11,
                             Particle : pdgid =    22, status =   1, q =  0 pt =  22.7, e =  23.4, eta =  0.24, theta =  0.24, phi =  2.75, mass =  0.00,
                             Particle : pdgid =  -211, status =   1, q = -1 pt =  10.0, e =  10.1, eta =  0.15, theta =  0.14, phi =  2.80, mass =  0.14,
                             Particle : pdgid =    22, status =   1, q =  0 pt =   8.3, e =   8.4, eta =  0.16, theta =  0.16, phi =  2.81, mass = -0.00,
                             Particle : pdgid =    22, status =   1, q =  0 pt =   7.9, e =   8.1, eta =  0.25, theta =  0.25, phi =  2.75, mass = -0.00,
                             Particle : pdgid =  -321, status =   1, q = -1 pt =   6.0, e =   7.5, eta = -0.70, theta = -0.65, phi = -0.21, mass =  0.49,
                             Particle : pdgid =    22, status =   1, q =  0 pt =   7.3, e =   7.3, eta =  0.07, theta =  0.07, phi =  2.61, mass = -0.00,
                             Particle : pdgid =   211, status =   1, q =  1 pt =   6.8, e =   6.9, eta =  0.19, theta =  0.19, phi =  2.90, mass =  0.14,
                             Particle : pdgid =    22, status =   1, q =  0 pt =   4.6, e =   4.6, eta =  0.12, theta =  0.12, phi =  2.46, mass =  0.00,
                             '...',
                             Particle : pdgid =    22, status =   1, q =  0 pt =   0.1, e =   0.1, eta = -0.02, theta = -0.02, phi =  2.59, mass = -0.00],
        'simulator': ,
        'zeds': [   Resonance2 : pdgid =    23, status =   3, q =  0 pt =  55.6, e = 102.8, eta =  0.29, theta =  0.29, phi = -0.40, mass = 84.86],
        'zeds_legs': [   Particle : pdgid =    13, status =   1, q = -1 pt =  50.5, e =  57.7, eta =  0.53, theta =  0.50, phi =  0.44, mass =  0.11,
                         Particle : pdgid =   -13, status =   1, q =  1 pt =  43.7, e =  45.1, eta = -0.26, theta = -0.26, phi = -1.44, mass =  0.11]}

```

Locate the zed. If you have none, call `next()` and
`print loop.event` until you do. Check its mass. Then, locate the
recoil (momentum of the particles recoiling against the zed), and check
its mass.

Exit ipython:

    quit()

Process the whole input file:

    heppy_loop.py OutDir analysis_ee_ZH_cfg.py -N 1000

lxplus processes about 20 events/s, most of the time being spent in the
papas simulation modules. For your analysis, you will be able to use
parallel processing, either on a multicore machine or on the CERN lsf
cluster. Moreover, the papas computing performance still has to be
studied.

You get an output directory `OutDir` . Check its contents and the
contents of its subdirectories. In particular, the following directory
contains an ntuple with the variables we need:

    OutDir/example/heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root  

### Make plots

Open the root file containing the ntuple in root:

    root OutDir/example/heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root  

Make a few plots:

-   reconstructed Z mass:

        events->Draw("zed_m")

-   recoil mass:

        events->Draw("recoil_m", "zed_m>80")

-   dijet mass (note that jets have not been calibrated, using raw jets
    here):

        events->Draw("higgs_m", "zed_m>80")

### Re-running the tutorial after logging out.

You will need to follow these instructions to set up your environment
for this tutorial.

First go to your FCC directory.

Then:

    export FCC=$PWD 
    cd heppy/
    source ./init.sh
    cd $FCC/Workdir
    source /afs/cern.ch/exp/fcc/sw/0.7/init_fcc_stack.sh

Getting started with Delphes (FCC-hh)
------------------------------------------

In this tutorial, you will learn how to:

-   generate events with Pythia8, process them through Delphes with
    FCCSW and write them in the FCC EDM format.
-   read these events with heppy to perfom basic selection and create an
    ntuple
-   read this ntuple in a python ROOT macro to make basic plots

But first, you will set up a working directory for your analysis.

### Set up your working directory

Start by getting the master branch of
[FCCSW](/twiki/bin/view/FCC/FccSoftwareGettingStarted#Optional_install_FCCSW){.twikiCurrentTopicLink
.twikiAnchorLink} and proceed with installation. If not already in
%FCCSW%:

    cd $FCCSW

If %FCCSW% not initialized:

    source ./init.sh

Now you are ready to produce 100TeV ttbar events with Pythia, process
them through Delphes and store them in the FCC-EDM :

    ./run gaudirun.py Sim/SimDelphesInterface/options/PythiaDelphes_config.py 

you should obtain a file called `    FCCDelphesOutput.root   `

Install the [heppy
(https://github.com/HEP-FCC/heppy.git) package.

Edit the ttbar example:
     
    heppy/test/analysis_hh_ttbar_cfg.py

and link the file you produced running FCCSW previously
`    FCCDelphesOutput.root   ` in the `    files   ` list line 14. If
not the example will use files already produced and stored on eos, so
you will need to setup eos:

    export EOS_MGM_URL="root://eospublic.cern.ch"
    source /afs/cern.ch/project/eos/installation/client/etc/setup.sh

Now you are ready to run the ttbar example:
    cd test
    heppy_loop.py myoutput analysis_hh_ttbar_cfg.py

Look at the output files

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 2016-02-25

-   Set HEPPY = [heppy
    2"}](https://github.com/HEP-FCC/heppy.git)

