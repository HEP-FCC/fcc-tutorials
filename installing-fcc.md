# Installing the FCC software locally

## Overview

This page explains how to install the part of the FCC software that can be used locally on your laptop.
We encourage to use the [Virtual Machine](./FccVirtualMachine.md) or the centrally installed software.

## What can I use locally?

The packages that are supported for local usage are [fcc-physics](https://github.com/HEP-FCC/fcc-physics) and
[heppy](https://github.com/HEP-FCC/heppy). This allows you to do physics analysis on your laptop.

## Installing the latest version

Setup a development area:

~~~{.sh}
mkdir FCC
cd FCC
export FCC=${PWD}
~~~

You need to install the **external** dependencies, check the [fcc-physics README](https://github.com/HEP-FCC/fcc-physics#installing-required-software):

- Either you set up as mentioned in the README (and set `CMAKE_PREFIX_PATH` accordingly) or
- Install all external packages in one directory `$FCC/externals` and do `export externals_prefix=$FCC/externals`

Install the latest version of the standalone FCC packages:

~~~{.sh}
cd $FCC # your local development area
git clone https://github.com/HEP-FCC/fcc-spi
cd fcc-spi
python ./build_latest.py $FCC
~~~

