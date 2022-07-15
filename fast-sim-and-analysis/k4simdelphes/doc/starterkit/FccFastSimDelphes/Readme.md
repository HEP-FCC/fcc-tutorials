
# FCC: Getting started with simulating events in Delphes

:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** with and without EvtGen
-   run a fast parametric **detector simulation** with **Delphes** in the EDM4Hep format
-   apply an **event selection** on those samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**
:::

First login to to a fresh shell on lxplus, on OSG, or in one of the virtual machine that could be provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `DelphesPythia8_EDM4HEP`, which allows you to run jobs in the EDM4Hep format is available on the command line:


```bash
which DelphesPythia8_EDM4HEP
```

If the above command fails without printing a path like `/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/edm4hep-master-kopc27l5fhxopkwfblet2xrwh6dbd322/bin/DelphesPythia8_EDM4HEP`, you need to setup the FCC software stack 

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

When sourcing the stack, you should see a message like:

```
 ...  Key4HEP release: key4hep-stack/2021-06-02
 ... Use the following command to reproduce the current environment: 
 ... 
         source /cvmfs/sw.hsf.org/spackages2/key4hep-stack/2021-06-02/x86_64-centos7-gcc8.3.0-opt/w6suthuzrwtg3mfan5xjglrv7pz6wvbc/setup.sh
 ... 
 ... done. 
```

this is telling that you have sourced the `key4hep-stack` version `2021-06-02`.

You can check all the packages associated to this release by using spack

```bash
source /cvmfs/sw.hsf.org/contrib/spack/share/spack/setup-env.sh 
spack find -p -d key4hep-stack@2021-06-02
```

for example to check the version of `k4simdelphes` installed in  version `2021-06-02`:

```bash
spack find -p -d key4hep-stack@2021-06-02 | grep k4simdelphes
```

of course, if you are setting up the lastest software, the version number has to be changed to the one you actually sourced.


## Part I: Generate and simulate Events with DelphesEDM4Hep

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z to mumu and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by downloading the official pythia cards for the various processes:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Generator/Pythia8/p8_noBES_ee_ZH_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Generator/Pythia8/p8_noBES_ee_ZZ_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Generator/Pythia8/p8_noBES_ee_WW_ecm240.cmd
```


The detector response of the the baseline FCC-ee IDEA detector configuration is estimated with Delphes.
Other detector cards can be found in the `$DELPHES_DIR/cards` directory, such as a ATLAS, CMS or ILD detector configurations:
`delphes_card_ATLAS.tcl`, `delphes_card_CMS.tcl` and `delphes_card_ILD.tcl`. 

But let's download the offical one:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Delphes/card_IDEA.tcl
```

To check the arguments ordering, please run the executable:

```
DelphesPythia8_EDM4HEP -h
```

it should produce the following message:

```
Usage: DelphesPythia8config_file output_config_file pythia_card output_file
config_file - configuration file in Tcl format,
output_config_file - configuration file steering the content of the edm4hep output in Tcl format,
pythia_card - Pythia8 configuration file,
output_file - output file in ROOT format.
```

where the first argument is the delphes card, the second argument the configuration file for the edm4hep output (see later) the third argument is the pythia card and last argument is the output file name.

Before running we need to define the collections that we want to write. The first name for example `GenParticleCollections` is the type of output collection in EDM4hep (in this case `GenParticleCollections` is of type `edm4hep::MCParticleCollection`) and the second argument for example `Particle` is the name of the collection in the Delphes card that will be used and stored in the EDM4Hep output file with the same name.


We also download the official version of this file:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Delphes/edm4hep_IDEA.tcl
```

The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_noBES_ee_ZH_ecm240.cmd p8_ee_ZH_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_noBES_ee_ZZ_ecm240.cmd p8_ee_ZZ_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_noBES_ee_WW_ecm240.cmd p8_ee_WW_ecm240_edm4hep.root
```
