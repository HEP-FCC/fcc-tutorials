[]() CMake guide for the FCC software
=====================================

Contents

-   [CMake guide for the FCC
    software](#cmake-guide-for-the-fcc-software)
    -   [Overview](#overview)
    -   [CMake example packages](#cmake-example-packages)
    -   [CMake in the FCC software
        framework](#cmake-in-the-fcc-software-framew)
        -   [Using an internal library](#using-an-internal-library)
        -   [Building a new Gaudi module](#building-a-new-gaudi-module)
        -   [Using an external library](#using-an-external-library)

[]() Overview
-------------

CMake is a tool for building software, which has become the de-facto
standard outside HEP. In HEP, it is for example used by the ILC/CLIC
communities and by the LHCb collaboration. For CMS people, CMake is the
equivalent of scram.

[]() CMake example packages
---------------------------

Colin provides [a few simple CMake
examples](https://github.com/cbernet/cmake-examples) independent from
the FCC software framework. They are helpful to understand the basics of
CMake.

Get these packages:

    git clone https://github.com/cbernet/cmake-examples.git
    cd cmake-examples

Follow the instructions in
[README.md](https://github.com/cbernet/cmake-examples/blob/master/README.md)
.

[]() CMake in the FCC software framework
----------------------------------------

The FCC software framework is split into single packages `  Generation`
, `  Examples` , `  Simulation` , .... Each of these packages contains
the file `  CMakeLists.txt` , defining its content. To build the entire
SW `  make` can be invoked. To rebuild a single package
`  make packagename` is sufficient.

When adding new source files to a package, the CMake build system needs
to be made aware of them. Usually `  CMakeLists.txt` contains a wildcard
expression that adds all implementation files in a subfolder, e.g.
`  src/*.cpp` , so there is no need to explicitly add the names of the
new files. To update the list of files, it is fastest to run
`  make configure` .

Note that when changing the name of a property of an algorithm or a
tool, `  make` (and not only `  make packagename` ) needs to be run for
Gaudi to be aware of the change.

### []() Using an internal library

### []() Building a new Gaudi module

### []() Using an external library

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 21 Sep 2014
