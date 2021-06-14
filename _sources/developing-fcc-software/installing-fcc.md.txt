# Installing the FCC software locally

## Overview

This page explains how to install the part of the FCC software that can be used locally on your laptop.
We encourage to use the [Virtual Machine](./FccVirtualMachine.md) or the centrally installed software.

## What can I use locally?

The packages that are supported for local usage are [fcc-physics](https://github.com/HEP-FCC/fcc-physics) and
[heppy](https://github.com/HEP-FCC/heppy). This allows you to do physics analysis on your laptop.

## Installing the latest version

### Setup a development area:

~~~{.sh}
mkdir FCC
cd FCC
export FCC=${PWD}
~~~

You need to install the **external** dependencies, check the [fcc-physics README](https://github.com/HEP-FCC/fcc-physics#installing-required-software):

> Set up as mentioned in the README (and set `CMAKE_PREFIX_PATH` accordingly) and also set the `PYTHIA8_DIR`.

### Install the latest version of the standalone FCC packages

You can copy the instructions below into a file and (after making it executable) execute it or copy paste them into a bash shell.

> Be sure to have set the `$FCC` environment variable before you execute.

~~~{.sh}
cd $FCC # your local development area
# get all the sources
declare -a repos=("podio" "fcc-edm" "fcc-physics" "heppy")
for r in "${repos[@]}"
do
  git clone https://github.com/HEP-FCC/$r
done
mkdir podio/build;mkdir fcc-edm/build;mkdir fcc-physics/build
mkdir fcc-install
# create a setup.sh file that you'll have to source every time
echo "export FCCEDM=$FCC/fcc-install;export PODIO=$FCC/fcc-install;export FCCPHYSICS=$FCC/fcc-install" > setup.sh
echo source $FCC/fcc-install/init_fcc_stack.sh >> setup.sh
curl https://raw.githubusercontent.com/HEP-FCC/fcc-spi/master/init_fcc_stack.sh -o $FCC/fcc-install/init_fcc_stack.sh
source setup.sh
~~~

Now you have all repository sources in your `$FCC` directory. If you do `ls` you should see them. To compile you need to
go through the list in this order:

1. podio
2. fcc-edm
3. fcc-physics

For each of them go into the build directory: `cd $FCC/<name>/build` and do:

~~~{.sh}
cmake -DCMAKE_INSTALL_PREFIX=$FCC/fcc-install/ ..
make install
~~~

If you encounter errors check the README of the corresponding repository.


## Using the local installation

The above lines created a setup script `setup.sh` in the folder `$FCC`. To use the software you'll have to source that file.
Additionally, make sure that the external software is also setup properly. In order to use heppy you need to also source the
`init.sh` script in the heppy folder.

For more information on usage, check the individual repositories or tutorial pages.
