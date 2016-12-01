# How to do software releases of the FCC stack

## Overview

This page is a tutorial for admins of the FCC software and explains how a software release is done on AFS and CVMFS.

## How to do a release

### Step 1: Externals

Currently we do not have a procedure to automatically install the external packages used in FCC software. That means we
currently need to install them before we actually push the "release button".

The only external packages that are not in the LCG releases currently are [Delphes](https://github.com/delphes/delphes)
and [ACTS](http://acts.web.cern.ch/). The location is explicitly set in the
[init script located in fcc-spi](https://github.com/HEP-FCC/fcc-spi/blob/master/init_fcc_stack.sh).

Install on AFS and CVMFS and set the `*_DIR` in that script to the correct location.

### Step 2: Tag the software

[Create the releases](https://help.github.com/articles/creating-releases/) in the repositories that need to be released.
Release notes written on github for the release are automatically picked up by the documentation web-site.

To generate the change-logs, have a look at this [github-changelog-generator](https://github.com/skywinder/github-changelog-generator).

### Step 3: Launch the release job in Jenkins

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

### Step 4: Test the release

[Go to Jenkins and launch a new test job](https://phsft-jenkins.cern.ch/view/FCC/job/FCCSW-integration/build?delay=0sec).

## Modifying the build and init scripts

### Adding a dependency

For external dependencies as mentioned above, you will need to modify the [init_fcc_stack.sh](https://github.com/HEP-FCC/fcc-spi/blob/master/init_fcc_stack.sh)
to properly set the needed `PATH` variables.

For *internal* dependencies, i.e. software that is part of the release (at the moment everything that is located under
[HEP-FCC](https://github.com/HEP-FCC)) you need to modify both the init and the build scripts:

- Adding the new dependency to the build script - look at how the versions for e.g. `podio` are set with the environment
  variable `podio_version`. You need to define it in the script and echo it into the `setup.sh` script. Also add it to the
  packages that are built at the end of the script. For setting the version also in Jenkins, you need to add the option to the release job.

- Adding the new dependency to the init script - again have a look at how `podio` is handled and add the corresponding
  statements for the new package: once `export MYPACKAGE=/the/path` and then adding it at the end of the script:
  `add_to_path CMAKE_PREFIX_PATH $MYPACKAGE` (look at the other `PATH` variables and decide what you need.)
