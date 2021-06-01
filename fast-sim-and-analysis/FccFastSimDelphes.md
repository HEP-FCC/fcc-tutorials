# FCC: Getting started with simulating events in Delphes

{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** with and without EvtGen
-   run a fast parametric **detector simulation** with **Delphes** in the EDM4Hep format
-   apply an **event selection** on those samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**

{% endobjectives %}

First login to to a fresh shell on lxplus, on OSG, or in one of the virtual machine that could be provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```bash
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `DelphesPythia8_EDM4HEP`, which allows you to run jobs in the EDM4Hep format is available on the command line:


```bash
which DelphesPythia8_EDM4HEP
```

If the above command fails without printing a path like `/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/edm4hep-master-kopc27l5fhxopkwfblet2xrwh6dbd322/bin/DelphesPythia8_EDM4HEP`, you need to setup the FCC software stack 

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```


## Part I: Generate and simulate Events with DelphesEDM4Hep

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z to mumu and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by writing the pythia cards for the various processes.

- **Pythia_ee_ZH_Zmumu_ecm240.cmd** for the Higgs Strahlung signal

```python
! File: Pythia_ee_ZH_Zmumu_ecm240.cmd
Random:setSeed = on
Main:numberOfEvents = 10000        ! number of events to generate
Main:timesAllowErrors = 10         ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Next:numberCount = 100             ! print message every n events
Beams:idA = 11                     ! first beam, e+ = 11
Beams:idB = -11                    ! second beam, e- = -11

! 3) Hard process : ZH at 240 GeV
Beams:eCM = 240  ! CM energy of collision
HiggsSM:ffbar2HZ = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! 5) Non-standard settings; exemplifies tuning possibilities.
25:m0        = 125.0               ! Higgs mass
23:onMode    = off		   ! switch off Z boson decays
23:onIfAny   = 13		   ! switch on Z boson decay to muons
```


- **Pythia_ee_ZZ_ecm240.cmd** for the ZZ background

```python
! File: Pythia_ee_ZZ_ecm240.cmd
Random:setSeed = on
Main:numberOfEvents = 10000        ! number of events to generate
Main:timesAllowErrors = 10         ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Next:numberCount = 100             ! print message every n events
Beams:idA = 11                     ! first beam, e+ = 11
Beams:idB = -11                    ! second beam, e- = -11

! 3) Hard process : ZZ at 240 GeV
Beams:eCM = 240  ! CM energy of collision
WeakDoubleBoson:ffbar2gmZgmZ = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation
```

- **Pythia_ee_WW_ecm240.cmd** for the WW background

```python
! File: Pythia_ee_WW_ecm240.cmd
Random:setSeed = on
Main:numberOfEvents = 10000        ! number of events to generate
Main:timesAllowErrors = 10         ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Next:numberCount = 100             ! print message every n events
Beams:idA = 11                     ! first beam, e+ = 11
Beams:idB = -11                    ! second beam, e- = -11

! 3) Hard process : WW at 240 GeV
Beams:eCM = 240  ! CM energy of collision
WeakDoubleBoson:ffbar2WW = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation
```

The detector response of the the baseline FCC-ee IDEA detector configuration is estimated with Delphes.
Other detector cards can be found in the `$DELPHES_DIR/cards` directory, such as a ATLAS, CMS or ILD detector configurations:
`delphes_card_ATLAS.tcl`, `delphes_card_CMS.tcl` and `delphes_card_ILD.tcl`. 

To check the arguments ordering, please run the executable:


```bash
DelphesPythia8_EDM4HEP
```

it should produce the following message:

```bash
Usage: DelphesPythia8config_file output_config_file pythia_card output_file
config_file - configuration file in Tcl format,
output_config_file - configuration file steering the content of the edm4hep output in Tcl format,
pythia_card - Pythia8 configuration file,
output_file - output file in ROOT format.
```

where the first argument is the delphes card, the second argument the configuration file for the edm4hep output (see later) the third argument is the pythia card and last argument is the output file name.

Before running we need to define the collections that we want to write. The first name for example ```GenParticleCollections``` is the type of output collection in EDM4hep (in this case ```GenParticleCollections``` is of type ```edm4hep::MCParticleCollection```) and the second argument for example ```Particle``` is the name of the collection in the Delphes card that will be used and stored in the EDM4Hep output file with the same name.

- **edm4hep.tcl** 
```python
module EDM4HepOutput EDM4HepOutput {
    add ReconstructedParticleCollections EFlowTrack EFlowPhoton EFlowNeutralHadron
    add GenParticleCollections           Particle
    add JetCollections                   Jet
    add MuonCollections                  Muon
    add ElectronCollections              Electron
    add PhotonCollections                Photon
    add MissingETCollections             MissingET
    add ScalarHTCollections              ScalarHT
    set RecoParticleCollectionName       ReconstructedParticles
    set MCRecoAssociationCollectionName  MCRecoAssociations
 }
```

The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
DelphesPythia8_EDM4HEP $DELPHES/cards/delphes_card_IDEA.tcl edm4hep.tcl Pythia_ee_ZH_Zmumu_ecm240.cmd p8_ee_ZH_ecm240.root
DelphesPythia8_EDM4HEP $DELPHES/cards/delphes_card_IDEA.tcl edm4hep.tcl Pythia_ee_ZZ_ecm240.cmd p8_ee_ZZ_ecm240.root
DelphesPythia8_EDM4HEP $DELPHES/cards/delphes_card_IDEA.tcl edm4hep.tcl Pythia_ee_WW_ecm240.cmd p8_ee_WW_ecm240.root
```

