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

First login to a fresh shell on lxplus, on OSG, or in one of the virtual machines that could be provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `DelphesPythia8_EDM4HEP`, which allows you to run jobs in the EDM4Hep format is available on the command line:


```bash
which DelphesPythia8_EDM4HEP
```

If the above command fails without printing a path like `/cvmfs/sw.hsf.org/spackages7/k4simdelphes/00-03-01/x86_64-centos7-gcc11.2.0-opt/7he4m/bin/DelphesPythia8_EDM4HEP`, you need to setup the FCC software stack 

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

When sourcing the stack, you should see a message like:

```
 ...  Key4HEP release: key4hep-stack/2023-04-08
 ... Use the following command to reproduce the current environment: 
 ...
         source /cvmfs/sw.hsf.org/spackages7/key4hep-stack/2023-04-08/x86_64-centos7-gcc11.2.0-opt/urwcv/setup.sh
 ...
 ... done.
```

which means that the version `2023-04-08` of `key4hep-stack` is sourced.


(delphesedm4hep)=
## Generate and Simulate Events with DelphesEDM4Hep

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by downloading the official pythia cards for the various processes:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/Pythia8/p8_ee_ZH_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/Pythia8/p8_ee_ZZ_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/Pythia8/p8_ee_WW_ecm240.cmd
```


The detector response of the baseline FCC-ee IDEA detector configuration is estimated with Delphes.
Other detector cards can be found in the `$DELPHES_DIR/cards` directory, such as a ATLAS, CMS or ILD detector configurations:
`delphes_card_ATLAS.tcl`, `delphes_card_CMS.tcl` and `delphes_card_ILD.tcl`. 

But let's download the official one:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Delphes/card_IDEA.tcl
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

where the first argument is the delphes card, the second argument the configuration file for the edm4hep output (see later), the third argument is the pythia card and the last argument is the output file name.

Before running we need to define the collections that we want to write. The first name for example `GenParticleCollections` is the type of output collection in EDM4hep (in this case `GenParticleCollections` is of type `edm4hep::MCParticleCollection`) and the second argument for example `Particle` is the name of the collection in the Delphes card that will be used and stored in the EDM4Hep output file with the same name.


We also download the official version of this file:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Delphes/edm4hep_IDEA.tcl
```

The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_ZH_ecm240.cmd p8_ee_ZH_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_ZZ_ecm240.cmd p8_ee_ZZ_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_WW_ecm240.cmd p8_ee_WW_ecm240_edm4hep.root
```

## Sample Generation: Pythia8 + EvtGen

This part explains how to produce FCC-ee samples with **Pythia8** and **EvtGen**, using the standard FCC configuration files and **EDM4hep** output format.  
It is based on the setup used for the **Winter 2023 MC campaigns**.

**EvtGen** is a decay generator specialized in the simulation of hadronic decays of heavy-flavour particles with accurate angular correlations and form-factor models.  
**EvtGen** is interfaced to [**Pythia8**](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/PythiaInterface.h#L88-L97) through **k4Gen**,  
so that events generated by **Pythia** can be decayed by **EvtGen** before detector simulation.

### Environment setup

EvtGen support is already integrated in the Key4HEP stack, but depending on the campaign version you need to choose between the **Winter 2023** or **Latest** environment.

- Use this setup if you want to reproduce results from the `winter2023` MC campaign:

```bash
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh
```

- Use this setup if you want to run the latest compatible versions of the FCC software:

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh 
```

- You can check the active version with:

```bash
echo $KEY4HEP_STACK
```

### Hands-on case study Pythia8 + EvtGen

We will generate a Monte Carlo sample for  
$e^{+} e^{-} \;\rightarrow\; Z \;\rightarrow\; b\bar{b} \;\rightarrow\; B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$,  
where one of the b-quarks hadronizes into a B-meson decaying via  $B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$.  
The centre-of-mass energy is 91.2 GeV. We will produce 1'000 events and save them in **EDM4hep** format.

All standard configuration files for FCC-ee Monte Carlo campaigns are provided in the  
[FCC-config repository (winter2023 branch)](https://github.com/HEP-FCC/FCC-config/tree/winter2023).

**Pythia8 configuration file**

This file `p8_ee_Zbb_ecm91_EVTGEN.cmd` defines the hard process $e^{+} e^{-} \;\rightarrow\; Z \;\rightarrow\; b\bar{b}$
and enables the **EvtGen** interface for hadronic decays.

```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/Pythia8/p8_ee_Zbb_ecm91_EVTGEN.cmd
```

To limit the number of events for a local test, add:

```
Main:numberOfEvents = 1000
```
**Detector cards**

These files define the detector geometry and simulation parameters for **Delphes**.

1. The Delphes detector card:
```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Delphes/card_IDEA.tcl
```
2. The EDM4hep output card describing how Delphes output collections (tracks, jets, leptons, etc.) are mapped to EDM4hep data structures:
```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Delphes/edm4hep_IDEA.tcl
```

**EvtGen decay files**

EvtGen needs several text files to describe decays, particle data and custom modes:

1. The main EvtGen decay table listing all standard decay channels and branching fractions for hadrons and leptons: 

```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/EvtGen/DECAY.DEC
```
2. The EvtGen particle data list (PDL) defining particle masses, lifetimes, and PDG codes:
```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/EvtGen/evt.pdl
```
3. The custom decay card defining the $B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$ channel with a hadronic 3-prong tau decay  $\tau^{+} \;\rightarrow\; \pi^{+}\,\pi^{-}\,\pi^{+}\,\bar{\nu}_{\tau}$: 

```
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/winter2023/FCCee/Generator/EvtGen/Bu2TauNuTAUHADNU.dec
```

**Event generation**

To generate events with Pythia8 + EvtGen, use the executable ```DelphesPythia8EvtGen_EDM4HEP_k4Interface```. The executable wrapper that connects Pythia8, EvtGen, and Delphes, and writes output in EDM4hep format.

Run the sample generation using:

```
DelphesPythia8EvtGen_EDM4HEP_k4Interface card_IDEA.tcl edm4hep_IDEA.tcl \
p8_ee_Zbb_ecm91_EVTGEN.cmd Bu2TauNuTAUHADNU.root DECAY.DEC evt.pdl \
Bu2TauNuTAUHADNU.dec 521 Bu_SIGNAL 1
```

**Explanation of arguments:**

1. `Bu2TauNuTAUHADNU.root` — output EDM4hep file  
2. `521` — PDG code of B⁺, the PDG code of the particle whose decays you want to override
3. `Bu_SIGNAL` — a label for the signal process used for bookkeeping in campaign production 
4. `1` — force custom decay (use `0` to disable)

## Creating custom decay file

We define a **custom EvtGen decay file** to describe $B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$.  
EvtGen uses a flexible text-based format to define particle decays, allowing users to override or extend the default decay tables. To do this safely — without altering the global definitions in `DECAY.DEC` — we use **aliases**, which act as local copies of particles.

Example `.dec` file:

```
Alias   Bu_SIGNAL   B+
Alias   Bubar_SIGNAL   B-
ChargeConj   Bu_SIGNAL   Bubar_SIGNAL
#
Alias   MyTau+   tau+
Alias   MyTau-   tau-
ChargeConj   MyTau+   MyTau-
#
Decay Bu_SIGNAL
    1.0   MyTau+   nu_tau   SLN;
Enddecay
CDecay   Bubar_SIGNAL
#
Decay MyTau-
    1.0   pi-   pi-   pi+   nu_tau   TAUHADNU -0.108 0.775 0.149 1.364 0.400 1.23 0.4;
Enddecay
CDecay MyTau+
#
End
```

**Using TAUOLA and PHOTOS in EvtGen**

EvtGen can interface with two optional external packages:

- **TAUOLA** — precise tau decay simulation with polarization  
- **PHOTOS** — adds QED final-state radiation

Both are included in the Key4HEP build of EvtGen.

To enable **TAUOLA**:

```
Decay MyTau-
    1.0   pi-   pi-   pi+   nu_tau   TAUOLA;
Enddecay
```

To enable **PHOTOS**:

```
Decay Bu_SIGNAL
    1.0   MyTau+   nu_tau   SLN PHOTOS;
Enddecay
```

