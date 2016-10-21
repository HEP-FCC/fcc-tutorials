---
layout: site
---
[]() FCC Event Data Model
=========================

Contents

-   [FCC Event Data Model](#fcc-event-data-model)
    -   [Overview](#overview)
    -   [Albers](#albers)
        -   [Installation](#installation)
        -   [PODs, handles, collections](#pods-handles-collections)
        -   [Exercise 1: Writing a
            collection](#exercise-1-writing-a-collection)
        -   [Exercise 2: Modifying the
            EDM](#exercise-2-modifying-the-edm)
    -   [The FCC event data model](#the-fcc-event-data-model)
        -   [Installation](#installation-an1)
        -   [Exercise 1](#exercise-1)
        -   [Exercise 2](#exercise-2)
    -   [Event analysis in C++](#event-analysis-in-c)
        -   [Installation](#installation-an2)
        -   [Exercise 1](#exercise-1-an1)
        -   [Exercise 2](#exercise-2-an1)
    -   [Event analysis in python](#event-analysis-in-python)
    -   [Standalone applications based on the FCC
        EDM](#standalone-applications-based-on)
        -   [Exercise 1: Set up a standalone pythia8 + FCC
            EDM application.](#exercise-1-set-up-a-standalone-p)
            -   [Step 1: Set up the
                new package.](#step-1-set-up-the-new-package)
            -   [Step 2: Plug pythia](#step-2-plug-pythia)
            -   [Step 3 : Use pythia](#step-3-use-pythia)
            -   [Step 4: A more complex event
                content](#step-4-a-more-complex-event-cont)

[]() Overview
-------------

The FCC event data model is based on simple C++ classes called POD
structs (Plain Old Data structures). A POD struct can be thought of as a
basic C struct.

This page presents the following packages:

-   albers-core: a standalone library containing the tools necessary to
    define an EDM based on PODs, and to write and read events based on
    this EDM.
-   fcc-edm: the official FCC event data model, based on albers-core
-   analysis-cpp: example analysis code showing how to read FCC
    EDM events.

**Create an FCC directory on your computer (either lxplus6 or a mac),
and keep track of this directory:**

    mkdir FCC
    cd FCC
    export FCC=$PWD

[]() Albers
-----------

Albers is a standalone library used to:

-   define complex event data models in a simple way
-   write and read edm events.

### []() Installation

The code of Albers is available on
[HEP-FCC/albers-core.git](https://github.com/HEP-FCC/albers-core) .

Clone this repository in your FCC directory:

    cd $FCC
    git clone git@github.com:HEP-FCC/albers-core.git
    cd albers-core
    git checkout -t origin/tutorial 

And follow the instructions in the
[README.md](https://github.com/HEP-FCC/albers-core/blob/tutorial/README.md)
. Make sure the tests work before proceeding to the next sections.

### []() PODs, handles, collections

Albers comes with a very simple test EDM, described in
[example\_edm.yaml](https://github.com/HEP-FCC/albers-core/blob/tutorial/examples/example_edm.yaml)
. A code generation script takes this yaml file in input to produce all
classes in the
[datamodel/datamodel/](https://github.com/HEP-FCC/albers-core/tree/tutorial/datamodel/datamodel)
directory.

For each datatype in the yaml file, three classes are generated:

-   the POD itself, e.g.
    [Particle.h](https://github.com/HEP-FCC/albers-core/blob/tutorial/datamodel/datamodel/Particle.h) .
-   a Handle to the POD, e.g.
    [ParticleHandle.h](https://github.com/HEP-FCC/albers-core/blob/tutorial/datamodel/datamodel/ParticleHandle.h) .
-   a collection of Handles, e.g.
    [ParticleCollection.h](https://github.com/HEP-FCC/albers-core/blob/tutorial/datamodel/datamodel/ParticleCollection.h) .

PODs are used as simple structs, for example:

    Particle ptc;
    ptc.P4 = LorentzVector{pt, eta, phi, m}; //mind the { !
    ptc.ID = 25
    ptc.Status = 3
    std::cout << ptc.Status << std::endl;

A Handle contains a pointer to an existing POD. If you have a handle,
you can get a readable reference to the corresponding POD by doing:

    const Particle& ptc = ptchandle.read();
    std::cout << ptc.Status << std::endl;
    ptc.Status = 1; // ERROR! CANNOT MODIFY THE POD

In case you wish to modify a POD, you can instead do:

    Particle& ptc = ptchandle.mod();
    ptc.Status = 1; // That works :-)
    std::cout << ptc.Status << std::endl;

Handles can be stored in a POD, as a reference to another POD. They are
also used to manipulate PODs stored in the event.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
if you are not allowed to modify a POD, the compiler will let you know.

<span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
**if your goal is just to read a POD, call read(). Only call mod() when
you need to modify the POD.**

The [yaml
file](https://github.com/HEP-FCC/albers-core/blob/tutorial/examples/example_edm.yaml)
also contains "components". Components are PODs that can be used as
building blocks in other PODs. For each component, the code generation
script only produces the POD class, meaning that components cannot be
pointed to by a Handle, and cannot be stored in a Collection.

### []() Exercise 1: Writing a collection

Modify
[write.cc](https://github.com/HEP-FCC/albers-core/blob/tutorial/examples/write.cc)
to write a second collection in the event, containing Particles.

**As usual, compile and run your code, and check the output root file.**

Tips:

-   Get inspiration from the code writing the <span
    class="twikiNewLink"> EventInfo </span> collection. The only
    conceptual difference here is that you are going to store several
    Particles in your particle collection. For each event, you will
    create two Particles in the Particle collection.
-   For each of the two Particles, create a handle in a similar way as
    for the <span class="twikiNewLink"> EventInfo </span> . Mofidy the
    Particle POD corresponding to the handle, setting its attributes to
    dummy values of your choice.
-   To check the output, open the resulting root file in root, and look
    at the events TTree. Plot the Particle attributes and make sure they
    correspond to what you have written.

### []() Exercise 2: Modifying the EDM

Modify
[example\_edm.yaml](https://github.com/HEP-FCC/albers-core/blob/tutorial/examples/example_edm.yaml)
to add a new datatype of your own.

Run the code generator:

    cd $ALBERS/..
    python python/albers_class_generator.py  examples/example_edm.yaml datamodel datamodel

Check that the classes for your new datatype have been created in
`  datamodel/datamodel/` .

Remove the `  build/` directory, run CMake again, and compile as
explained in the
[README.md](https://github.com/HEP-FCC/albers-core/blob/tutorial/README.md)
.

Modify
[write.cc](https://github.com/HEP-FCC/albers-core/blob/tutorial/examples/write.cc)
to write another collection in the event, containing objects of your new
datatype.

Compile again, run, and check the output root file with root to make
sure that your objects have been written correctly.

[]() The FCC event data model
-----------------------------

fcc-edm is a library based on Albers, defining the FCC event data model.

### []() Installation

The code of is available on
[HEP-FCC/fcc-edm.git](https://github.com/HEP-FCC/fcc-edm) .

Clone this repository in your FCC directory:

    cd $FCC
    git clone git@github.com:HEP-FCC/fcc-edm.git
    cd fcc-edm
    git checkout -t origin/tutorial

And follow the instructions in the
[README.md](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/README.md)
. Make sure the tests work before proceeding to the next sections.

### []() Exercise 1

The file
[edm\_1.yaml](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/edm_1.yaml)
describes the whole FCC data model.

Read this file, and make sure you understand all data types. In
particular, you should be able to make the difference between a POD that
refers to another POD (through a Handle) and a POD that contains another
POD (a component).

### []() Exercise 2

Can you find a missing datatype or a missing attribute in an existing
POD?

If that is the case:

-   add it to the yaml file.
-   run the code generator, **this time from the fcc-edm package, not
    from albers-core!** .
-   compile and run the tests.
-   contact Colin to discuss the change.

[]() Event analysis in C++
--------------------------

analysis-cpp is a package showing how to create analysis code based on
the albers and fcc-edm libraries, so that the analysis code is able to
understand the FCC event data model.

### []() Installation

The code of is available on
[HEP-FCC/analysis-cpp.git](https://github.com/HEP-FCC/analysis-cpp) .

Clone this repository in your FCC directory:

    cd $FCC
    git clone git@github.com:HEP-FCC/analysis-cpp.git
    cd analysis-cpp
    git checkout -t origin/tutorial

And follow the instructions in the
[README.md](https://github.com/HEP-FCC/analysis-cpp/blob/tutorial/README.md)
. Make sure the tests work before proceeding to the next sections.

### []() Exercise 1

Add a new histogram to the <span class="twikiNewLink"> MyAnalysis
</span> class showing the event number. Make sure it is filled, and
display it in the macro.

### []() Exercise 2

Fire up root and open the example file

    root
    TFile f("example.root")

You should see a lot of warnings from TClass which indicate that no
dictionary is present for the various EDM classes. The dictionary is
necessary for root to understand the classes stored in the events tree
of `  example.root` .

The dictionary is stored in the fcc-edm shared library,
`  libdatamodel.so` (libdatamodel.dylib) on Linux (on MacOs).

Quit root.

Open it again, load the fcc-edm shared library, and open the file:

    root
    gSystem.Load("libdatamodel")
    TFile f("example.root")

Note that the warnings have disappeared.

ROOT is able to find this library because it is in one of the
directories present in your LD\_LIBRARY\_PATH (DYLD\_LIBRARY\_PATH on
MacOs). Quit root and print this environment variable:

on Linux:

    echo $LD_LIBRARY_PATH

on MacOs:

    echo $DYLD_LIBRARY_PATH

list the contents of each of the directories, until you find
`  libdatamodel.so` in the `  fcc-edm` package, e.g.:

    ls /Users/HEP-FCC/Code/FCC/fcc-edm/install/lib

[]() Event analysis in python
-----------------------------

See [FccSoftwareHeppy](./FccSoftwareHeppy){.twikiLink}

[]() Standalone applications based on the FCC EDM
-------------------------------------------------

The FCC Event Data Model can easily be used in standalone applications.
For example, one could generate events with pythia and write the
particles in the FCC EDM format, so that these particles can be analyzed
transparently later on using analysis-cpp or heppy. That is precisely
the subject of the exercise below.

### []() Exercise 1: Set up a standalone pythia8 + FCC EDM application.

This exercise is not for the faint of heart :-).

#### []() Step 1: Set up the new package.

Copy analysis-cpp and name it differently, e.g. pythiafcc. In the
package, grep for all occurences of analysis-cpp or analysiscpp and
replace by pythiafcc. To do the replacement in one command, you could
use a combination of the find and sed commands like, on Mac OS:

    find . -type f | grep -v /.git/ | xargs sed -i '' 's/analysiscpp/pythiafcc/g'

**Note that the command is different on linux, google for more
information.**

Remove the contents of the `  build/` directory, run cmake, compile, and
check that all tests are running.

Copy `  example/read.cc` into `  example/generate.cc` . Modify all <span
class="twikiNewLink"> CMakeLists </span> so that you create an
executable called pythiafcc-generate out of this file.

Remove the contents of the `  build/` directory, run cmake, compile, and
run the new executable.

#### []() Step 2: Plug pythia

Our application will use pythia8.

First, install pythia8. Remember which install prefix you have used for
pythia.

We must make sure that the pythia headers and libraries can be found.
This is done by modifying the <span class="twikiNewLink"> CMakeLists
</span> .txt file. This file contains find\_package commands:

    # Make sure we find the Find*.cmake functions distributed with this package
    set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
    set(CMAKE_PREFIX_PATH $ENV{ALBERS} $ENV{FCCEDM})
    find_package(alberscore REQUIRED)
    find_package(fccedm REQUIRED)
    find_package(ROOT REQUIRED)

We want to add a find\_package call for Pythia8:

    find_package(Pythia8)

This command in fact calls a function in a cmake module called <span
class="twikiNewLink"> FindPythia8 </span> .cmake. With google again, you
can easily find such a function. Here is what I got:

    # Find the Pythia8 includes and library.
    #
    # This module defines
    # PYTHIA8_INCLUDE_DIR   where to locate Pythia.h file
    # PYTHIA8_LIBRARY       where to find the libpythia8 library
    # PYTHIA8__LIBRARY Addicional libraries
    # PYTHIA8_LIBRARIES     (not cached) the libraries to link against to use Pythia8
    # PYTHIA8_FOUND         if false, you cannot build anything that requires Pythia8
    # PYTHIA8_VERSION       version of Pythia8 if found

    set(_pythia8dirs ${PYTHIA8_DIR} $ENV{PYTHIA8_DIR} /usr /opt/pythia8)

    find_path(PYTHIA8_INCLUDE_DIR
              NAMES Pythia.h Pythia8/Pythia.h
              HINTS ${_pythia8dirs}
              PATH_SUFFIXES include
              DOC "Specify the directory containing Pythia.h.")

    find_library(PYTHIA8_LIBRARY
                 NAMES pythia8 Pythia8
                 HINTS ${_pythia8dirs}
                 PATH_SUFFIXES lib
                 DOC "Specify the Pythia8 library here.")

    find_library(PYTHIA8_hepmcinterface_LIBRARY
                 NAMES hepmcinterface pythia8tohepmc
                 HINTS ${_pythia8dirs}
                 PATH_SUFFIXES lib)

    find_library(PYTHIA8_lhapdfdummy_LIBRARY
                 NAMES lhapdfdummy
                 HINTS ${_pythia8dirs}
                 PATH_SUFFIXES lib)

    foreach(_lib PYTHIA8_LIBRARY PYTHIA8_hepmcinterface_LIBRARY PYTHIA8_lhapdfdummy_LIBRARY)
      if(${_lib})
        set(PYTHIA8_LIBRARIES ${PYTHIA8_LIBRARIES} ${${_lib}})
      endif()
    endforeach()
    set(PYTHIA8_INCLUDE_DIRS ${PYTHIA8_INCLUDE_DIR} ${PYTHIA8_INCLUDE_DIR}/Pythia8 )

    # handle the QUIETLY and REQUIRED arguments and set PYTHIA8_FOUND to TRUE if
    # all listed variables are TRUE

    include(FindPackageHandleStandardArgs)
    find_package_handle_standard_args(Pythia8 DEFAULT_MSG PYTHIA8_INCLUDE_DIR PYTHIA8_LIBRARY)
    mark_as_advanced(PYTHIA8_INCLUDE_DIR PYTHIA8_LIBRARY PYTHIA8_hepmcinterface_LIBRARY PYTHIA8_lhapdfdummy_LIBRARY)

Put it in the cmake/ directory, where you can also find the <span
class="twikiNewLink"> FindROOT </span> .cmake function.

You don't need to understand everything in this function, but you still
need to understand:

-   which variables this function relies upon for finding pythia. For
    example, we see that it is enough to have an environment variable
    called `    PYTHIA8_DIR   ` set to the installation directory
    of pythia. Inside this directory, cmake will look for an
    `    include/   ` subdirectory containing `    Pythia.h   ` and
    `    Pythia8/Pythia.h   ` .
-   which cmake variables this function is setting. You can see that it
    sets `    PYTHIA8_LIBRARIES   ` and `    PYTHIA8_INCLUDE_DIRS   ` .
    You will need to make use of these variables in your
    `    CMakeLists.txt   ` files.

Set the `  PYTHIA8_DIR` environment variable:

    export PYTHIA8_DIR=the_installation_path_of_pythia_on_your_computer

Modify `  pythiafcc/CMakeLists.txt` to:

-   add the find\_package call for pythia8
-   add the pythia include directories to the list of
    include\_directories

Modify `  pythiafcc/example` to add the pythia8 libraries to the list of
libraries linked with the executable.

Run cmake in the usual way, making sure that pythia8 is found. In
`  pythiafcc/CMakeLists.txt` , write at the end:

    message(${PYTHIA8_INCLUDE_DIRS})
    message(${PYTHIA8_LIBRARIES})

Run cmake again and check the value of these variables. You should see
something like this:

    /Users/cbernet/local/include/Users/cbernet/local/include/Pythia8
    /Users/cbernet/local/lib/libpythia8.a

Check that this directory and this static library are indeed there.

**If everything's alright, you may keep going. If not, you need to sort
that out.**

#### []() Step 3 : Use pythia

In this step, we are finally going to modify `  example/generate.cc` to
use pythia. At each step, make sure your code compiles and runs as
expected before going further.

You will need only the `  main` function, so remove the rest.

At the beginning of the `  main` , perform the initialization of pythia.
Look for some inspiration and code in one of the many example
executables distributed with pythia8. You should see the pythia
initialization message when you run your executable.

Generate some events. You should see pythia event printouts.

For each event, access the particles generated by pythia, convert them
to FCC MCParticles, and write them to an output root file. Some example
code is available in [the fcc-edm
simplewrite.cc](https://github.com/HEP-FCC/fcc-edm/blob/tutorial/examples/simplewrite.cc)
.

#### []() Step 4: A more complex event content

In the previous step, we have stored MCParticles to the ROOT file. In
this step:

-   add the <span class="twikiNewLink"> GenVertex </span> collection
-   keep track of the production and end vertex of each particle in the
    MCParticle

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 2014-12-15
