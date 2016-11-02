CMake guide for the FCC software
=====================================

-   [CMake guide for the FCC
    software](#cmake-guide-for-the-fcc-software)
    -   [Overview](#overview)
    -   [CMake example packages](#cmake-example-packages)
    -   [CMake in the FCC software
        framework](#cmake-in-the-fcc-software-framew)
        -   [Using an internal library](#using-an-internal-library)
        -   [Building a new Gaudi module](#building-a-new-gaudi-module)
        -   [Using an external library](#using-an-external-library)

Overview
-------------

CMake is a tool for building software, which has become the de-facto
standard outside HEP. In HEP, it is for example used by the ILC/CLIC
communities and by the LHCb collaboration. For CMS people, CMake is the
equivalent of scram. In FCCSW, CMake is used mainly via Gaudi macros, which are however fairly similar to plain CMake commands in syntax.

CMake example packages
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

CMake in the FCC software framework
----------------------------------------

The FCC software framework is split into single packages `  Generation`
, `  Examples` , `  Simulation` , .... Each of these packages contains
the file `  CMakeLists.txt` , defining its content. To build the entire
SW, a Makefile is provided in the top level directory, so `  make` can be invoked there to build FCCSW. To rebuild a single package
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

### CTest in FCCSW

FCCSW also uses the cmake for integration tests.
This is described in detail in `doc/AddingTestsToFCCSW.md`.

### Using an internal library

Once Gaudi is notified that a certain subdirectory is needed by invoking `gaudi_depends_on_subdir`, internal libraries defined in this subdirectory can be used by simply adding them to the list of `INCLUDE_DIRS` and `LINK_LIBRARIES`. An example would be the way the internal library `DetCommon` is used by the module `Test/TestGeometryPlugins` in FCCSW.



### Building a new Gaudi module

The best way is to look at existing modules in FCCSW for inspiration. The syntax to declare the module `TestGeometryPlugins`, for example, is:

```
gaudi_add_module(TestGeometryPlugins
                 src/components/*.cpp
                 INCLUDE_DIRS Geant4 FWCore SimG4Interface SimG4Common DetInterface DetCommon TestGeometry
                 LINK_LIBRARIES GaudiKernel FWCore Geant4 DetCommon TestGeometry)

```

### Using an external library

This can be done using the standard cmake command [find_package](https://cmake.org/cmake/help/v3.0/command/find_package.html). See [Colins CMake examples](https://github.com/cbernet/cmake-examples) for details.

Sometimes external libraries require special treatment, and their documentation needs to be consulted. One known case is DD4hep, for which in some cases the CMake variable `${DD4hep_COMPONENT_LIBRARIES}` needs to be used in the `LINK_LIBRARIES` line (if the DDRec or DDSegmentation package is used). Example:

```
gaudi_add_library(DetCommon
                 src/*.cpp
                 INCLUDE_DIRS DD4hep ROOT Geant4 DetSegmentation
                 LINK_LIBRARIES GaudiKernel DD4hep ROOT Geant4 DetSegmentation ${DD4hep_COMPONENT_LIBRARIES}
                 PUBLIC_HEADERS DetCommon)

```

