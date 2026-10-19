# CMake guide for the FCC software

## Overview

CMake is a tool for building software, which has become the de-facto
standard outside HEP. In HEP, it is for example used by the ILC/CLIC
communities and by the LHCb collaboration. For CMS people, CMake is the
equivalent of scram. In FCCSW, CMake is used mainly via Gaudi macros, which are however fairly similar to plain CMake commands in syntax.

This [LHCb Twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/GaudiCMakeConfiguration) has some additional information on
various Gaudi CMake functions.



## Quick start into building FCCSW

### Set up the environment

In case you are unsure, it is best to use the `init.sh` script provided with FCCSW:

```
source ./init.sh`
```

Note that mixing setup scripts (from another package, for example) may or may not work as intended - more likely not.
For any requests to changes in the environment, feel free to contact the software team on the mailing list or any other channels.
Developers may also look into `spack` to have more fine-grained control over the build dependencies.

### Using the top-level Makefile


- The software can be compiled in the root directory with `make -j8`.
- After adding new files, do `make configure`
- Building single packages: `make packagename`
- Cleaning up (rebuild from scratch): `make purge`
- To change the build-type (e.g. Release or Debug), set the `BUILDTYPE` variable (e.g. `BUILDTYPE=Debug make`)

### Using plain CMake

The steps that the top-level Makefile does can also be done manually:

* Create a build directory: `mkdir build; cd build`
* Run CMake in the build directory: `cmake .. `
* Change any cmake options by rerunning cmake. For example: `cmake .. -DCMAKE_INSTALL_PREFIX=install`. Tools like ccmake may also be useful: `ccmake ..`
* Compile the software, using all the cpus available:    ```make -j `getconf _NPROCESSORS_ONLN` ```  
* Install by running `make install`
* In case any dependency is changed, most likely you need to remove all the contents of the build folder and rerun cmake and the compilation.



## CMake example packages

Colin provides [a few simple CMake
examples](https://github.com/cbernet/cmake-examples) independent from
the FCC software framework. They are helpful to understand the basics of
CMake.

Get these packages:

    git clone https://github.com/cbernet/cmake-examples.git
    cd cmake-examples

Follow the instructions in
[README.md](https://github.com/cbernet/cmake-examples/blob/master/README.md).

## CMake in the FCC software framework

The FCC software framework is split into single packages `Generation`, `Examples`, `Simulation` , .... Each of these packages contains
the file `CMakeLists.txt`, defining its content. To build the entire
SW, a Makefile is provided in the top level directory, so `make` can be invoked there to build FCCSW. To rebuild a single package
`make packagename` is sufficient.

Note that single subdirectory cannot be installed individually at the moment.
If you need to install, it is best to compile everything in the beginning (which may take a while), and then work with the build folder. Any changes should only lead to the changed subdirectories being recompiled. 


When adding new source files to a package, the CMake build system needs
to be made aware of them. Usually `CMakeLists.txt` contains a wildcard
expression that adds all implementation files in a subfolder, e.g.
`src/*.cpp` , so there is no need to explicitly add the names of the
new files. To update the list of files, it is fastest to run
`make configure` .

Note that when changing the name of a property of an algorithm or a
tool, `make` (and not only `make packagename` ) needs to be run for
Gaudi to be aware of the change.

The `make` command creates a directory `build.xxxx` where `xxxx` depends on your platform and compiler. All build files
are writtin in that directory. There are situations where you need to clean this build folder before you can
successfully build the software:

- The FCCSW environment changed (version change)
- Fetching changes from other users or the HEP-FCC repository with deleted files

In those cases you'll need to do `make purge` (this target deletes the build and install directories) and rebuild the
entire software.


### Runtime Environment

FCCSW consists of executables, headers, scripts, dynamic libraries, xmls  and special files describing gaudi components.
In order to use these, some environment variables need to be set.
FCCSW includes a setup script that is installed automatically and can be sourced to set up the required variables.

Gaudi also offers the possibility to set up the environment via the `xenv` command. This is done by simply prefixing the command you want to run with the `run` script in the top level directory of FCCSW, or directly in the build directory.

```bash
./build/run fccrun Examples/options/pythia.py
```

Sometimes it is convenient to run FCCSW directly from the binaries in the build directory without installing them.
This can be done by using the `run` script in the build directory, or setting the environment variables as in `setup.sh` for the build folder.
Note that the directories in the  build folder differ a bit. Mostly it is important the the LD_LIBRARY_PATH is pre-fixed with the library directories. The fccrun command should pick up the components from the build folder then.



## CTest in FCCSW

FCCSW also uses the cmake for integration tests.
This is described in detail in the documentation page on [adding tests to FCCSW](https://github.com/HEP-FCC/FCCSW/blob/master/doc/AddingTestsToFCCSW.md).

## Using an internal library

Libraries are the main tool to avoid code duplication, i.e. make pieces of code available in other parts of the framework.
Once Gaudi is notified that a certain subdirectory is needed by invoking `gaudi_depends_on_subdir`, internal libraries defined in this subdirectory can be used by simply adding them to the list of `INCLUDE_DIRS` and `LINK_LIBRARIES`. An example would be the way the internal library `DetCommon` is used by the module  [`Test/TestGeometryPlugins`](https://github.com/HEP-FCC/FCCSW/blob/master/Test/TestGeometry/CMakeLists.txt)  in FCCSW.
The required changes to use the `DetCommon` library are
* declare the dependency on the subdirectory `Detector/DetCommon`
* add the `DetCommon` headers by adding `DetCommon` to the `INCLUDE_DIRS` line
* link the `DetCommon` libraries by adding `DetCommon` to the `LINK_LIBRARIES` line.


## Building a new Gaudi module

A more general introduction to Gaudi modules and the differences with respect to libraries can be found in the [LHCb twiki](https://twiki.cern.ch/twiki/bin/view/LHCb/GaudiCMakeConfiguration#Building_a_Module_AKA_component).
The best way is to look at existing modules in FCCSW for inspiration. The syntax to declare the module [`TestGeometryPlugins`](https://github.com/HEP-FCC/FCCSW/blob/master/Test/TestGeometry/CMakeLists.txt), for example, is:

```cmake
gaudi_add_module(TestGeometryPlugins
                 src/components/*.cpp
                 INCLUDE_DIRS Geant4 FWCore SimG4Interface SimG4Common DetInterface DetCommon TestGeometry
                 LINK_LIBRARIES GaudiKernel FWCore Geant4 DetCommon TestGeometry)

```

## Using an external library

This can be done using the standard cmake command [find_package](https://cmake.org/cmake/help/v3.0/command/find_package.html). See [Colins CMake examples](https://github.com/cbernet/cmake-examples) for details.

Sometimes external libraries require special treatment, and their documentation needs to be consulted. One known case is DD4hep, for which in some cases the CMake variable `${DD4hep_COMPONENT_LIBRARIES}` needs to be used in the `LINK_LIBRARIES` line (if the DDRec or DDSegmentation package is used). Example:

```cmake
gaudi_add_library(DetCommon
                 src/*.cpp
                 INCLUDE_DIRS DD4hep ROOT Geant4 DetSegmentation
                 LINK_LIBRARIES GaudiKernel DD4hep ROOT Geant4 DetSegmentation ${DD4hep_COMPONENT_LIBRARIES}
                 PUBLIC_HEADERS DetCommon)

```

ROOT is needed in many modules of FCCSW. More information how to use it in a CMake-based project is available on the [ROOT website](https://root.cern.ch/how/integrate-root-my-project-cmake).

### Customizing how CMake is run

An environment variable is used to forward command line arguments to the cmake command, for example to run cmake with the `trace` option:

```
CMAKEFLAGS='--trace' make
```

:::{admonition} How do I check compilation flags?
:class: callout

Instead of running `make`, run:

```shell
make VERBOSE=1
```
:::
