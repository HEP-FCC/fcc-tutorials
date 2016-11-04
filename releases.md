# How to do software releases of the FCC stack

## Overview

This page is a tutorial for admins of the FCC software and explains how a software release is done on AFS and CVMFS.

## Step 1: Externals

Currently we do not have a procedure to automatically install the external packages used in FCC software. That means we
currently need to install them before we actually push the "release button".

The only external package currently used is [Delphes](https://github.com/delphes/delphes). The location is explicitly set
in the [init script located in fcc-spi](https://github.com/HEP-FCC/fcc-spi/blob/master/init_fcc_stack.sh). Install Delphes
on AFS and CVMFS and set the `DELPHES_DIR` in that script to the correct location.

## Step 2: Tag the software

[Create the releases](https://help.github.com/articles/creating-releases/) in the repositories that need to be released.
Release notes written on github for the release are automatically picked up by the documentation web-site.

## Step 3: Launch the release job in Jenkins

[Go to Jenkins and launch a new release job](https://phsft-jenkins.cern.ch/view/FCC/job/FCC-release/build?delay=0sec).
You will be confronted with a form:

- `*_version` correspond to the tag-names you defined [step 2](#step-2-tag-the-software)
- `lcg_version` corresponds to the LCG release you want to use (e.g. `LCG_86`)
- `cvmfs_out` is an accesible directory (e.g. on AFS) where the CVMFS release is put to copy on CVMFS
    - Currently we cannot copy to CVMFS from the job but have to do that by hand
    - Also if you put an AFS path here, the release will be linked to CVMFS
- `release_name` a name for the release (e.g. `0.8`)

During the release, also the documentation website will be regenerated. If you are interested in learning how to
generate the website have a look at [this tutorial](FccDocPage.md)

## Step 4: Test the release

[Go to Jenkins and launch a new test job](https://phsft-jenkins.cern.ch/view/FCC/job/FCCSW-integration/build?delay=0sec).
