Heppy : a mini framework for HEP event processing in python
================================================================

Contents:

-   Heppy : a mini framework for HEP event processing in python
    -   [Prerequisites](#prerequisites)
    -   [Reference guide](#reference-guide)
    -   [A short description of the analysis system](#a-short-description-of-the-analysis-system)
        -   [The ntuplizer](#the-ntuplizer)
    -   [Installation](#installation)
    -   [Generating an EDM root file with pythia](#generating-an-edm-root-file-with)
    -   [Exercises](#exercises)
        -   [1- Understanding the configuration file](#1--understanding-the-configuration-file)
        -   [2- Finding existing analysis code](#2--finding-existing-analysis-code)
        -   [3- Running interactively on one component](#3--running-interactively-on-one-component)
        -   [4- Multiprocessing on a single machine](#4--multiprocessing-on-a-single-machine)
        -   [5- Using PAPAS, the particle flow simulation](#5--using-papas-the-particle-flow)

Prerequisites
------------------

**You must follow [FccSoftwareEDM](./FccSoftwareEDM){.twikiLink} first**
.

**You should be familiar with python to follow this tutorial** .

I strongly advise to carefully follow [the python tutorial](http://docs.python.org/tutorial/index.html) if not yet done.
It will take you a few hours now, but will gain you many days in the
future.

Why python? In short:

-   fast learning curve: python is the most easy-to-learn language
-   high productivity: coding in python is about 10 times faster than in
    C++
-   high flexibility: code can be easily reused, refactored, extended.
-   dynamic typing (similar to C++ template features, without the pain
    in the neck): if you do an analysis for e.g. the muon channel, it is
    going to work for the electron channel with only minor modifications
    related to lepton identification. If your analysis reads a certain
    kind of particle-like objects, it will probably work on other kinds
    of particle-like objects.
-   very large and easy-to-use standard library

Reference guide
--------------------

-   [Reference guide](http://fcc-support-heppy.web.cern.ch/fcc-support-heppy/) :
    documentation automatically generated with pydoc

A short description of the analysis system
-----------------------------------------------

### The ntuplizer

This goal of the ntuplizer system is to produce a flat tree for each of
the datasets (also called "components") used in the analysis. Any
operation requiring a user-written loop on the events can be done while
producing the flat tree, so that the resulting trees can be used with
simple TTree.Draw or TTree.Project commands.

For example, the ntuplizer makes it possible to:

-   read events from an albers root file produced using the FCC
    software framework.
-   create python physics objects to hold the C++ objects from the
    albers root file. These objects have the exact same interface as the
    C++ objects, and can be extended with more information. For example,
    you could write your own muon ID function for your python Muon
    object, or add attributes to your python Muons along the processing
    flow, like the 4-momentum of the closest jet or the closest
    generated muon.
-   create new python objects, e.g. a Z object containing two leptons.
-   compute event-by-event weights
-   select a trigger path, and match to the corresponding trigger
    objects
-   define and write simple flat trees

It is up to you to define what you want to do, possibly re-using
existing code from other analyses or writing your own.

An analysis typically consists in several tenth of samples, or
"components": data samples, standard model backgrounds, signal. The
ntuplizer is built in such a way that it takes one command to either:

-   run interactively on a single component
-   run several processes in parallel on your multiprocessor machine
-   run hundreds of processes as separate jobs on LSF, the CERN
    batch cluster.

If you decide to run several processes, you can split a single component
in as many chunks as input ROOT files for this component. For example,
you could run in parallel:

-   6 chunks from the DYJet component, using 6 processors of your local
    machine, assuming you have more than 6 input DYJet ROOT files.
-   200 chunks from the DYJet component, 300 from your 5 data components
    altogether, and 300 jobs from all the remaing components (e.g.
    di-boson, TTJets, ...) on LSF.

The ntuplizer is based on python, pyroot, and the albers event data
model (EDM). It could have been written as a simple python macro based
on ROOT and albers. Instead, it was decided to keep the design of
typical high-energy physics software frameworks (e.g. CMSSW, Athena,
FCCSW), and to implement it in python. This design boils down to:

-   a python configuration system, similar to the one we use in HEP full
    frameworks like Gaudi.
-   a Looper accessing the albers EDM events and running a sequence of
    analyzers on each event.
-   a common python event, created at the beginning of the processing of
    each albers EDM event, and read/modified by the analyzers.

the python event allows you to build the information you want into your
event, and allows the analyzers to communicate. At the end of the
processing of a given EDM event, the python event can be filled into a
flat tree using a specific kind of analyzer [like this one](https://github.com/HEP-FCC/heppy/blob/tutorial/analyzers/SimpleTreeProducer.py)
.

**The code consists of two packages:**

[The core package](https://github.com/HEP-FCC/heppy/tree/tutorial)
contains the following packages:

-   [framework](https://github.com/HEP-FCC/heppy/tree/tutorial/framework)
    : Core modules: python configuration system, the looper, the python
    event, etc.
-   [analyzers](https://github.com/HEP-FCC/heppy/tree/tutorial/analyzers)
    : Generic analyzers
-   [statistics](https://github.com/HEP-FCC/heppy/tree/tutorial/statistics)
    : Modules for counting and averaging, histogramming,
    tree production.
-   [utils](https://github.com/HEP-FCC/heppy/tree/tutorial/utils) :
    Miscellaneous utilities, like deltaR matching tools.

It also contains a
[scripts](https://github.com/HEP-FCC/heppy/tree/tutorial/scripts)
directory.

[The FCC-specific
package](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial) contains
the following packages:

-   [analyzers](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial/analyzers)
    : FCC-specific analyzers;
-   [particles](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial/particles)
    : python physics objects;
-   [fastsim](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial/fastsim)
    : PAPAS fast simulation;
-   [display](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial/fastsim)
    : event display;
-   [tools](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial/tools) :
    various tools, like generated particle history analysis.

The code is documented. To get more information on a given class, use
the python docstring functionality, for example:

    python
    import math
    help(math)

Installation
-----------------

Install the following three packages

-   [podio](https://github.com/HEP-FCC/podio/blob/master/README.md)
-   [fcc-edm](https://github.com/HEP-FCC/fcc-edm/blob/master/README.md)
-   [fcc-physics](https://github.com/HEP-FCC/fcc-physics/blob/master/README.md)

For this tutorial, these three packages are all needed.

First, make sure the `FCC` environment variable is set properly. Do:

    echo $FCC

If the command returns the path to the directory containing the 3
packages described above, you're all set. Otherwise, go to this
directory and do:

    export FCC=$PWD

We will now install the two heppy packages and a pythia inferface to the
FCC EDM:

-   [heppy](https://github.com/HEP-FCC/heppy/tree/tutorial)
-   [heppy\_fcc](https://github.com/HEP-FCC/heppy_fcc/tree/tutorial)
-   [pythiafcc](https://github.com/HEP-FCC/pythiafcc/tree/tutorial)

Go back to your base directory and install the core heppy package:

    cd $FCC
    git clone git@github.com:HEP-FCC/heppy.git
    cd heppy
    git checkout -t origin/tutorial

Follow the instructions in the README.md file.

Go back to your base directory and install the specific heppy\_fcc
package:

    cd $FCC
    git clone git@github.com:HEP-FCC/heppy_fcc.git
    cd heppy_fcc
    git checkout -t origin/tutorial

Follow the installation instructions in the README.md file, **but do not
try to run yet** .

Go back to your base directory and install the pythiafcc package:

    cd $FCC
    git clone git@github.com:HEP-FCC/pythiafcc.git
    cd pythiafcc
    git checkout -t origin/tutorial

Follow the installation instructions in the README.md file.

Generating an EDM root file with pythia
--------------------------------------------

[pythiafcc](https://github.com/HEP-FCC/pythiafcc/tree/tutorial) is a
pythia8 executable that writes all generated particles and vertices to
an FCC EDM root file.

It is currently set to produce inclusive gamma star/Z events at the Z
pole, decaying into d dbar. Later on you can modify the pythia8 cards in
[generate.cc](https://github.com/HEP-FCC/pythiafcc/blob/tutorial/example/generate.cc)
and recompile if you want a different kind of events.

For now, just do:

    cd $HEPPY_FCC/test
    pythiafcc-generate

You should get a file called `  example.root` that are going to read in
the following exercises.

Exercises
--------------

### 1- Understanding the configuration file

Have a detailed look at the configuration file,
[simple\_analysis\_cfg.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/test/simple_analysis_cfg.py)
.

**For these exercises, we use ipython, an enhanced python interpreter.
If you don't have ipython, just use python instead.**

Load it in python:

    ipython -i simple_analysis_cfg.py

Print the component:

    print selectedComponents[0]

    ->
    Component: example
            dataset_entries:   0
            files          :   ['example.root']
            isData         :   False
            isEmbed        :   False
            isMC           :   False
            tree_name      :   None
            triggers       :   None

Print the sequence of analyzers:

    print sequence

    ->
    0 :
    Analyzer: heppy_fcc.analyzers.FCCReader.FCCReader_1
            class_object   :
            instance_label :   1
            verbose        :   False :
    1 :
    Analyzer: heppy_fcc.analyzers.Recoil.Recoil_gen
            class_object   :
            instance_label :   gen
            particles      :   gen_particles_stable
            sqrts          :   91.0
            verbose        :   False :
    2 :
    Analyzer: heppy_fcc.analyzers.JetClusterizer.JetClusterizer_gen
            class_object   :
            instance_label :   gen
            particles      :   gen_particles_stable
            verbose        :   False :
    3 :
    Analyzer: heppy_fcc.analyzers.SimpleTreeProducer.SimpleTreeProducer_1
            class_object   :
            instance_label :   1
            verbose        :   False :

Now quit ipython.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
all objects created in this cfg file are just configuration objects.
These configuration objects will be passed to the actual analyzers that
contain your analysis code.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
In the future, when you use this event processing system in your
analysis, always make sure that all ingredients (components, analyzers)
are defined correctly by loading your configuration in python before
even trying to run.

### 2- Finding existing analysis code

Open
[simple\_analysis\_cfg.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/test/simple_analysis_cfg.py)
.

The configuration fragments for the analyzers look like:

    from heppy_fcc.analyzers.Recoil import Recoil
    gen_recoil = cfg.Analyzer(
        Recoil,
        instance_label = 'gen',
        sqrts = 91.,
        particles = 'gen_particles_stable'
    )

The first argument is a class object coming from
[Recoil.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/analyzers/Recoil.py)
. The framework will use this class object to create an instance of this
class.

The second argument, `  instance_label` , is an instance label. This
argument is optional, and is useful in case several analyzers of the
same class are requested.

Have a look at the
[Recoil.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/analyzers/Recoil.py)
module, and study the code. In particular, note how the analyzer reads
from the event and writes to it, and how it makes use of the parameters
defined in its configuration fragment.

Then study the code of the base class in
[analyzer.py](https://github.com/HEP-FCC/heppy/blob/tutorial/framework/analyzer.py)
to see which methods are available in analyzers. You may also simply
have a look at the documentation of this class:

    ipython
    from heppy_fcc.analyzers.Recoil import Recoil
    help(Recoil)

### 3- Running interactively on one component

Run:

    heppy_loop.py Out simple_analysis_cfg.py -N 1000

You should see a healhy printout with, towards the end:

    number of events processed: 1000

In the ouput `  Out` directory, you can find a component directory,
`  example` . Investigate the contents of this component directory, and
of all directories within. Have a look at the text files, but ignore the
`  .pck` files

Fire up root (here we choose to use ipython + pyroot), and check the
main output tree:

    ipython
    from ROOT import TFile
    f = TFile('Out/example/heppy_fcc.analyzers.SimpleTreeProducer.SimpleTreeProducer_1/tree.root')
    f.ls()
    t = f.Get('events')
    t.Print()
    t.Draw('recoil_visible_gen_m')

### 4- Multiprocessing on a single machine

Copy your input file:

    cp example.root example_2.root

Edit
[simple\_analysis\_cfg.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/test/simple_analysis_cfg.py)
and add the following lines, after the creation of the `  comp`
component object.

    comp.files.append('example_2.root')
    comp.splitFactor = 2  # splitting the component in 2 chunks

As usual, load the configutation script in python, and print the
`  config` object. You should be able to see that the component now has
two input files and a splitFactor equal to 2.

Run again:

    heppy_loop.py Multi simple_analysis_cfg.py -N 1000

In the `  Multi` output directory, you have chunks. Each of these chunks
correspond to one of the threads you have run We're going to add
everything up:

    cd Multi
    heppy_check.py *
    heppy_hadd.py .

The first command checks that all chunks terminated correctly. The
second command adds the root files (with hadd), the cut-flow counters,
and the averages.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
To do multiprocessing, you can also define several components
corresponding to the samples you need to process. Each of these
components can have its own split factor.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
Check the number of processors on your machine ( `  cat /proc/cpuinfo`
), and define the number of threads accordingly.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
When debugging your code, make sure to have only one thread.

### 5- Using PAPAS, the particle flow simulation

PAPAS (PAramatrized PArticle Simulation) is a simulation of the particle
flow. It propagates stable generated particles through a simple detector
model.

In the tracker, charged particles may be detected as tracks, taking into
account the acceptance, efficiency, and momentum resolution of this
detector.

In the calorimeters, particles are detected as energy deposits. The
energy deposits are modelled by taking into account the following
detector properties: energy resolution, acceptance, energy thresholds,
and characteristic size. The latter is defined as the distance between
two clusters below which the two clusters cannot be resolved and are
considered as a single cluster.

A particle flow algorithm then runs over the simulated tracks and
clusters to identify and reconstruct charged hadrons, photons, and
neutral hadrons. These particles can then be used as an input to
higher-level algorithms like jet clustering, or directly in the
analysis.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
**Electrons and muons are passed through PAPAS without any modification,
and the user is responsible for applying is own efficiency and
resolution models. The hadronic decay products of tau leptons are
simulated just like other hadrons and photons.**

A
[CMS-like](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/fastsim/detectors/CMS.py)
detector model is provided as an example, and used in
[simple\_papas\_cfg.py](https://github.com/HEP-FCC/heppy_fcc/blob/tutorial/test/simple_papas_cfg.py)
. Please inspect both modules carefully.

To run this confirguration file, do:

    heppy_loop.py Papas simple_papas_cfg.py -N 1000

Then, check the output jet tree:

    ipython
    from ROOT import TFile
    f = TFile('Papas/example/heppy_fcc.analyzers.JetTreeProducer.JetTreeProducer_papas/jet_tree.root')
    f.ls()
    t = f.Get('events')
    t.Print()
    t.Draw('jet1_e/jet1_gen_e>>h(40, 0, 2)', 'jet1_gen_e>10 && abs(jet1_gen_eta)<3.')

This jet response plot is characteristic of what is to be expected with
particle flow. It is quite close from what would be obtained with the
CMS full simulation.

If you want to see an event display of event 10, do:

    ipython
    %run simple_papas_cfg.py 10
    # and for next events:
    next()
    next()
    # and so on

If you see nothing, it could be because the Z boson decayed into
neutrinos. In that case, just proceed to next event.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
This exercise shows how to run papas to produce a collection of
reconstructed particles. You can then build on this example to add
analysis modules and customized tree producers.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
A full documentation for PAPAS will be provided sometime this autumn.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
**PAPAS is still in an experimental phase! No guarantee whatsoever,
please report bugs to Colin.**

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 08 Oct 2014
