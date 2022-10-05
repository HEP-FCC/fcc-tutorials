# Finding data in the Bookkeeping

Knowing how data flows through the various Gaudi applications is crucial for 
knowing where to look for your data.

Data are catalogued in ‘the bookkeeping’, and are initially sorted in broad 
groups such as 'Delphes Events', ‘Full detector simulation’, and according to the FCC flavor (ee, hh or eh).
After this, a tree of various application and processing versions will 
eventually lead to the data you need.

:::{admonition} Learning Objectives
:class: objectives

* Find FCC data in the central storage
* Store FCC data in the central storage
:::

## Gaining access permissions

Read/write access to the shared filesystem is gained by subscribing to the relevant egroups [here](https://e-groups.cern.ch/e-groups/EgroupsSearchForm.do):

```
fcc-eos-read-hh
fcc-eos-read-ee
fcc-eos-read-eh

fcc-eos-write-hh
fcc-eos-write-ee
fcc-eos-write-eh
```

## Finding Data

Browse the fcc directory on `eos`, the shared filesystem used by CERN.

```bash
tree /eos/experiment/fcc/ -L 2
```

You should see an output similar to:

```
/eos/experiment/fcc/
├── ee
│   ├── accelerator
│   ├── analyses
│   ├── datasets
│   ├── generation
│   ├── mdi
│   ├── simulation
│   ├── tutorial
│   └── utils
├── eh
│   └── datasets
├── helhc
│   ├── analyses
│   ├── generation
│   ├── utils
│   └── YR_summary
├── hh
│   ├── analyses
│   ├── CDR_script
│   ├── generation
│   ├── hcal
│   ├── simulation
│   ├── tests
│   ├── testsamples
│   ├── tutorials
│   └── utils
```

The file paths on eos already give an indication where to find what kind of data. In some instances, the information is very detailed:

```bash

ls /eos/experiment/fcc/hh/simulation/samples/v03/physics/bjets/bFieldOn/etaTo1.5/1000GeV/simu/output_103747599.root
```

But not all datasets follow this exact format. In case of questions simply contact the software team.

On lxplus `eos` is mounted as a standard directory and you can use standard bash tools such as `ls`, `cp`, `mv` ... to manipulate the files - Also to write them provided you have the correct permissions.



However, using eos like this is not recommended to transfer actual data (we speak from experience) and also not possible on machines where eos has not been mounted. The right tool here is `xrdcp`, which uses the xrootd protocol. It works like   `cp` (minus some features) but all paths must be prefixed by the URL `root://eospublic.cern.ch/`.


:::{admonition} Write a file to the FCC eos directory
:class: challenge

To check that your permissions have been set up correctly, try to write a file
called `<user>.txt` to the test directory
`root://eospublic.cern.ch//eos/experiment/fcc/hh/tests/`
:::
