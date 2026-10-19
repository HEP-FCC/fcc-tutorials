# Getting Started with Fast Simulation in Delphes

<!-- contributors:start -->
:::{admonition} Page contributors
:class: callout dropdown

Clement Helsens, Valentin Volkl, Juraj Smiesko, Vasilisa, Aman Desai, Michele Selvaggi
:::
<!-- contributors:end -->

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

If the above command fails without printing a path like `/cvmfs/sw.hsf.org/key4hep/releases/2026-04-08/x86_64-almalinux9-gcc14.2.0-opt/k4simdelphes/00-07-06-36x4ef/bin/DelphesPythia8_EDM4HEP`, you need to setup the FCC software stack 

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

When sourcing the stack, you should see a message like:

```
Setting up the Key4hep software stack release latest-opt from CVMFS
Use the following command to reproduce the current environment: 

        source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2026-04-08
```

which means that the release `2026-04-08` of the Key4hep stack is sourced.


(delphesedm4hep)=
## Generate and Simulate Events with DelphesEDM4Hep

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by downloading the official pythia cards for the various processes:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_ZH_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_ZZ_ecm240.cmd
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_WW_ecm240.cmd
```


The detector response of the baseline FCC-ee IDEA detector configuration is estimated with Delphes.
Other detector cards can be found in the `$DELPHES_DIR/cards` directory, such as a ATLAS, CMS or ILD detector configurations:
`delphes_card_ATLAS.tcl`, `delphes_card_CMS.tcl` and `delphes_card_ILD.tcl`. 

But let's download the official one:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Delphes/card_IDEA.tcl
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
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Delphes/edm4hep_IDEA.tcl
```

The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_ZH_ecm240.cmd p8_ee_ZH_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_ZZ_ecm240.cmd p8_ee_ZZ_ecm240_edm4hep.root
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_ee_WW_ecm240.cmd p8_ee_WW_ecm240_edm4hep.root
```

## Sample Generation: Pythia8 + EvtGen

>
> Author: Vasilisa Guliaeva
>

This part explains how to produce FCC-ee samples with
[**Pythia8**](https://pythia.org/) and
[**EvtGen**](https://evtgen.hepforge.org), using the standard FCC configuration
files and **EDM4hep** output format.

[**EvtGen**](https://evtgen.hepforge.org/) is a decay generator specialized in
the simulation of hadronic decays of heavy-flavour particles with accurate
angular correlations and form-factor models. **EvtGen** is interfaced to
[**Pythia8**](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/PythiaInterface.h#L88-L97)
through **k4Gen**, so that events generated by **Pythia** can be decayed by
**EvtGen** before detector simulation.

We will generate a Monte Carlo sample of 1'000 events for $e^{+} e^{-} \;\rightarrow\; Z \;\rightarrow\; b\bar{b} \;\rightarrow\; B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$. All standard configuration files for FCC-ee Monte Carlo campaigns are provided in the [FCC-config repository](https://github.com/HEP-FCC/FCC-config); each production campaign has its own branch, and the `main` branch is used here.

Open a new lxplus session. Create a working directory and enter it:
```bash
mkdir tutorialGen
cd tutorialGen
```

Make sure you have the latest Key4hep release set up:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

**Event generation**

To generate events with Pythia8 + EvtGen, use the executable
`DelphesPythia8EvtGen_EDM4HEP_k4Interface`. Make sure your shell environment is
correctly set up by running:
```bash
which DelphesPythia8EvtGen_EDM4HEP_k4Interface
```
with a response similar to:
```
/cvmfs/sw.hsf.org/key4hep/releases/2026-04-08/x86_64-almalinux9-gcc14.2.0-opt/k4simdelphes/00-07-06-36x4ef/bin/DelphesPythia8EvtGen_EDM4HEP_k4Interface
```
(the output might differ, but shouldn't be empty and the structure should be similar).

The executable wrapper that connects Pythia8, EvtGen, and Delphes, and writes
output in EDM4hep format. You can inspect its expected argument order by
running:
```bash
DelphesPythia8EvtGen_EDM4HEP_k4Interface -h
```

:::{admonition} `DelphesPythia8EvtGen_EDM4HEP_k4Interface` CLI arguments
:class: callout toggle

The `DelphesPythia8EvtGen_EDM4HEP_k4Interface` takes the following CLI
arguments.

```
Usage: DelphesPythia8EvtGenconfig_file output_config_file pythia_card output_file DECAY.DEC evt.pdl user.dec

config_file - configuration file in Tcl format,  
output_config_file - configuration file steering the content of the edm4hep output in Tcl format,  
pythia_card - Pythia8 configuration file,  
output_file - output file in ROOT format,  
DECAY.DEC - EvtGen full decay file,  
evt.pdl - EvtGen particle list,  
user.dec - EvtGen user decay file.
```
:::

To start the sample generation, we need to download the configuration files.

We begin with the Pythia8 card that defines the hard process $e^{+} e^{-} \;\rightarrow\; Z \;\rightarrow\; b\bar{b}$ and enables the EvtGen interface for hadronic decays.

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.cmd
```

To limit the number of events for a local test, add:

```
Main:numberOfEvents = 1000
```

Next, we download the Delphes detector description and the EDM4hep steering file, which together define the IDEA detector geometry and how Delphes collections (tracks, jets, leptons, etc.) are translated into EDM4hep structures:

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Delphes/card_IDEA.tcl
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Delphes/edm4hep_IDEA.tcl
```

EvtGen requires a set of text files containing decay tables, particle properties, and our custom decay definition for $B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$ channel with a hadronic 3-prong tau decay  $\tau^{+} \;\rightarrow\; \pi^{+}\,\pi^{-}\,\pi^{+}\,\bar{\nu}_{\tau}$: 

```bash
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/EvtGen/DECAY.DEC
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/EvtGen/evt.pdl
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/EvtGen/Bu2TauNuTAUHADNU.dec
```

With all configuration files in place, we can now run the generation step using:

```
DelphesPythia8EvtGen_EDM4HEP_k4Interface card_IDEA.tcl edm4hep_IDEA.tcl \
p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.cmd Bu2TauNuTAUHADNU.root DECAY.DEC evt.pdl \
Bu2TauNuTAUHADNU.dec 521 Bu_SIGNAL 1
```

**Explanation of arguments:**

1. `Bu2TauNuTAUHADNU.root` — output EDM4hep file  
2. `521` — PDG code of B⁺, the PDG code of the particle whose decays you want to override
3. `Bu_SIGNAL` — a label for the signal process used for bookkeeping in campaign production 
4. `1` — force custom decay (use `0` to disable)

## Creating custom decay file

The custom decay file `Bu2TauNuTAUHADNU.dec` specifies the decay $B^{+} \;\rightarrow\; \tau^{+} \nu_{\tau} \;\rightarrow\; 3\pi$. EvtGen uses a flexible text-based format to define particle decays, allowing users to override or extend the default decay tables. To do this safely — without altering the global definitions in `DECAY.DEC` — we use **aliases**, which act as local copies of particles. Using **aliases** ensures that only the selected signal $B^+$ follow our custom decay chain, rather than forcing every $B^+$ in a $Z \rightarrow b\bar{b}$ event to decay the same way.

`Bu2TauNuTAUHADNU.dec` file:

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

- **TAUOLA** — precise $\tau$ decay simulation with polarization  
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

