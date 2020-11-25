# FCC: Getting started with simulating events in Delphes

{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** within FCCSW
-   run a fast parametric **detector simulation** with **Delphes** within FCCSW
-   apply an **event selection** on those samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**
-   compare distributions produced with different generators

{% endobjectives %}

First login to to a fresh shell on lxplus, on OSG, or in one of the virtual machine that could be provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```bash
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `fccrun`, which allows you to run jobs in the Gaudi framework is available on the command line:


```bash
which fccrun
```

If the above command fails without printing a path like `/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.14/x86_64-centos7-gcc8-opt/scripts/fccrun`, you need to setup the FCC software stack 

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

<!-- 
Please also add an environment varialbe for Delphes cards

```bash
export DELPHES_DIR='/cvmfs/sft.cern.ch/lcg/releases/delphes/3.4.3pre02-e4803/x86_64-centos7-gcc8-opt/'
```
-->

## Part I: Generate and simulate Events with FCCSW

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z to mumu and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by writing the pythia cards for the various processes.

- **Pythia_ee_ZH_Zmumu_ecm240.cmd** for the Higgs Strahlung signal

```python
! File: Pythia_ee_ZH_Zmumu_ecm240.cmd
Random:setSeed = on
Main:timesAllowErrors = 10          ! how many aborts before run stops

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

Both Pythia8 and Delphes are integrated in the Gaudi-based FCCSW framework as *Algorithms*. A job that runs the whole workflow consists of the following:

* `GenAlg` (Top level Generation Algorithm, with a `tool` that calls Pythia8)
* `HepMCConverter` (takes the HepMC output and translates it to the FCC event data model, understood by the Sim Algorithm)
* `DelphesSimulation`(Delphes integration, outputs reconstructed objects in the FCC event data model)
* `PodioOutput` (writes the event data to a root file on disk)

To run the code, a job options like the following is needed (**Note:** While the format of the configuration is a python file, it is not necessarily "pythonic". It can be used with GaudiPython, but we will only use it as to straightforwardly write down a job description for use with `fccrun` ) 

- **PythiaDelphes_config.py** for the FCCSW configuration file

```python
import sys, os
from Gaudi.Configuration import *

# Workflow Steering
from Configurables import ApplicationMgr
ApplicationMgr().EvtSel = 'NONE'
ApplicationMgr().EvtMax = 100

## Data event model based on Podio
from Configurables import FCCDataSvc
podioEvent = FCCDataSvc("EventDataSvc")
ApplicationMgr().ExtSvc += [podioEvent]
ApplicationMgr().OutputLevel = INFO


## Pythia generator
from Configurables import PythiaInterface
pythia8gentool = PythiaInterface()
pythia8gentool.Filename = os.path.join(os.environ.get("FCCSWSHAREDIR", ""),"Generation/data/ee_Z_ddbar.cmd")


## Write the HepMC::GenEvent to the data service
from Configurables import GenAlg
pythia8gen = GenAlg()
pythia8gen.SignalProvider = pythia8gentool
pythia8gen.hepmc.Path = "hepmc"
ApplicationMgr().TopAlg += [pythia8gen]


### Reads an HepMC::GenEvent from the data service and writes a collection of EDM Particles
from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path = "hepmc"
hepmc_converter.genparticles.Path = "genParticles"
hepmc_converter.genvertices.Path = "genVertices"
ApplicationMgr().TopAlg += [hepmc_converter]


# Define all output tools that convert the Delphes collections to FCC-EDM:

from Configurables import DelphesSaveChargedParticles

muonSaveTool = DelphesSaveChargedParticles("muons")
muonSaveTool.delphesArrayName = "MuonFilter/muons"
muonSaveTool.particles.Path      = "muons"
muonSaveTool.saveTrkCov = True
muonSaveTool.particles_trkCov.Path      = "muons_trkCov"
muonSaveTool.mcAssociations.Path = "muonsToMC"
muonSaveTool.isolationTags.Path  = "muonITags"

eleSaveTool = DelphesSaveChargedParticles("electrons")
eleSaveTool.delphesArrayName = "ElectronFilter/electrons"
eleSaveTool.particles.Path      = "electrons"
eleSaveTool.particles_trkCov.Path      = "electrons_trkCov"
eleSaveTool.mcAssociations.Path = "electronsToMC"
eleSaveTool.isolationTags.Path  = "electronITags"

chhadSaveTool = DelphesSaveChargedParticles("efcharged")
chhadSaveTool.delphesArrayName = "Calorimeter/eflowTracks"
chhadSaveTool.saveIsolation = False
chhadSaveTool.particles.Path      = "efcharged"
chhadSaveTool.particles_trkCov.Path      = "efcharged_trkCov"
chhadSaveTool.mcAssociations.Path = "efchargedToMC"


from Configurables import DelphesSaveNeutralParticles

# Particle-Flow Photons output tool
pfphotonsSaveTool = DelphesSaveNeutralParticles("efphotons")
pfphotonsSaveTool.delphesArrayName="Calorimeter/eflowPhotons"
pfphotonsSaveTool.saveIsolation=False
pfphotonsSaveTool.particles.Path      = "efphotons"
pfphotonsSaveTool.mcAssociations.Path = "efphotonsToMC"
pfphotonsSaveTool.isolationTags.Path  = "efphotonITags"

# Photons output tool
photonsSaveTool = DelphesSaveNeutralParticles("photons")
photonsSaveTool.delphesArrayName = "PhotonEfficiency/photons"
photonsSaveTool.particles.Path      = "photons"
photonsSaveTool.mcAssociations.Path = "photonsToMC"
photonsSaveTool.isolationTags.Path  = "photonITags"

# Particle-Flow Neutral Hadrons output tool
neuthadSaveTool = DelphesSaveNeutralParticles("efneutrals")
neuthadSaveTool.delphesArrayName = "Calorimeter/eflowNeutralHadrons"
neuthadSaveTool.saveIsolation = False
neuthadSaveTool.particles.Path      = "efneutrals"
neuthadSaveTool.mcAssociations.Path = "efneutralsToMC"


from Configurables import DelphesSaveGenJets

genJetSaveTool = DelphesSaveGenJets("genJets")
genJetSaveTool.delphesArrayName = "GenJetFinder/jets"
genJetSaveTool.genJets.Path             = "genJets"
genJetSaveTool.genJetsFlavorTagged.Path = "genJetsFlavor"


from Configurables import DelphesSaveJets

jetSaveTool = DelphesSaveJets("jets")
jetSaveTool.delphesArrayName = "JetEnergyScale/jets"
jetSaveTool.jets.Path             = "jets"
jetSaveTool.jetConstituents.Path  = "jetParts"
jetSaveTool.jetsFlavorTagged.Path = "jetsFlavor"
jetSaveTool.jetsBTagged.Path      = "bTags"
jetSaveTool.jetsCTagged.Path      = "cTags"
jetSaveTool.jetsTauTagged.Path    = "tauTags"


from Configurables import DelphesSaveMet

metSaveTool = DelphesSaveMet("met")
metSaveTool.delphesMETArrayName = "MissingET/momentum"
metSaveTool.delphesSHTArrayName = "ScalarHT/energy"
metSaveTool.missingEt.Path = "met"


## Delphes simulator -> define objects to be written out
from Configurables import DelphesSimulation
delphessim = DelphesSimulation()
## Define Delphes card
delphessim.DelphesCard = os.path.join(os.environ.get("DELPHES_DIR", ""), "cards/delphes_card_IDEAtrkCov.tcl")
delphessim.ROOTOutputFile = ""
delphessim.ApplyGenFilter = True
delphessim.outputs = [
                       "DelphesSaveChargedParticles/muons",
                       "DelphesSaveChargedParticles/electrons",
                       "DelphesSaveNeutralParticles/photons",
                       "DelphesSaveChargedParticles/efcharged",
                       "DelphesSaveNeutralParticles/efphotons",
                       "DelphesSaveNeutralParticles/efneutrals",
                       "DelphesSaveGenJets/genJets",
                       "DelphesSaveJets/jets",
                       "DelphesSaveMet/met",
                     ]
delphessim.hepmc.Path               = "hepmc"
delphessim.genParticles.Path        = "skimmedGenParticles"
delphessim.mcEventWeights.Path      = "mcEventWeights"
ApplicationMgr().TopAlg += [delphessim]


## FCC event-data model output -> define objects to be written out
from Configurables import PodioOutput
out = PodioOutput("out")
out.filename = "FCCDelphesOutput.root"
out.outputCommands = [
                       "keep *", 
                     ]
ApplicationMgr().TopAlg += [out]
```

The `fccrun` allows to change most `Properties` of the job on the command line. All possible arguments to fccrun  are listed with the command 

```bash
fccrun PythiaDelphes_config.py -h
```

Should return something like:

```
 -->  GenAlg
 -->  Converter
 -->  DelphesSimulation
 -->  out
 

usage: fccrun [-h] [--dry-run] [-v] [-n NUM_EVENTS] [-l] [--gdb]
              [--ncpus NCPUS] [--input [INPUT]] [--Blocking [BLOCKING]]
              [--PrintEmptyCounters [PRINTEMPTYCOUNTERS]]
              [--Filename [FILENAME]]
              [--printPythiaStatistics [PRINTPYTHIASTATISTICS]]
              [--doEvtGenDecays [DOEVTGENDECAYS]]
              [--EvtGenDecayFile [EVTGENDECAYFILE]]
              [--EvtGenParticleDataFile [EVTGENPARTICLEDATAFILE]]
              [--hepmcStatusList HEPMCSTATUSLIST [HEPMCSTATUSLIST ...]]
              [--DelphesCard [DELPHESCARD]]
              [--ROOTOutputFile [ROOTOUTPUTFILE]]
              [--outputs OUTPUTS [OUTPUTS ...]]
              [--ApplyGenFilter [APPLYGENFILTER]] [--filename [FILENAME]]
              [--outputCommands OUTPUTCOMMANDS [OUTPUTCOMMANDS ...]]
              [--filenameRemote [FILENAMEREMOTE]]
              [config_files [config_files ...]]

Run job in the FCC framework

positional arguments:
  config_files          Gaudi config (python) files describing the job

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             Do not actually run the job, just parse the config
                        files
  -v, --verbose         Run job with verbose output
  -n NUM_EVENTS, --num-events NUM_EVENTS
                        Number of events to run
  -l, --list            Print all the configurable components available in the
                        framework and exit
  --gdb                 Attach gdb debugger
  --ncpus NCPUS         Start Gaudi in parallel mode using NCPUS processes. 0
                        => serial mode (default), -1 => use all CPUs
  --input [INPUT]       Name of the file to read [unknown owner type]
  --Blocking [BLOCKING]
                        if algorithm invokes CPU-blocking system calls
                        (offloads computations to accelerators or quantum
                        processors, performs disk or network I/O, is bound by
                        resource synchronization, etc) [Gaudi::Algorithm]
  --PrintEmptyCounters [PRINTEMPTYCOUNTERS]
                        force printing of empty counters, otherwise only
                        printed in DEBUG mode [GaudiCommon<Algorithm>]
  --Filename [FILENAME]
                        [PythiaInterface]
  --printPythiaStatistics [PRINTPYTHIASTATISTICS]
                        Print Pythia Statistics [PythiaInterface]
  --doEvtGenDecays [DOEVTGENDECAYS]
                        Do decays with EvtGen [PythiaInterface]
  --EvtGenDecayFile [EVTGENDECAYFILE]
                        Name of the EvtGen Decay File [PythiaInterface]
  --EvtGenParticleDataFile [EVTGENPARTICLEDATAFILE]
                        Name of the EvtGen Particle Data File
                        [PythiaInterface]
  --hepmcStatusList HEPMCSTATUSLIST [HEPMCSTATUSLIST ...]
                        list of hepmc statuses to keep. An empty list means
                        all statuses will be kept [HepMCToEDMConverter]
  --DelphesCard [DELPHESCARD]
                        Name of Delphes tcl config file with detector and
                        simulation parameters [DelphesSimulation]
  --ROOTOutputFile [ROOTOUTPUTFILE]
                        Name of Delphes Root output file, if defined, the
                        Delphes standard tree write out (in addition to FCC-
                        EDM based output to transient data store)
                        [DelphesSimulation]
  --outputs OUTPUTS [OUTPUTS ...]
                        [DelphesSimulation]
  --ApplyGenFilter [APPLYGENFILTER]
                        only for debugging purposes. If entire MC particle
                        collection is needed, request in cfg file.
                        [DelphesSimulation]
  --filename [FILENAME]
                        Name of the file to create [PodioOutput]
  --outputCommands OUTPUTCOMMANDS [OUTPUTCOMMANDS ...]
                        A set of commands to declare which collections to keep
                        or drop. [PodioOutput]
  --filenameRemote [FILENAMEREMOTE]
                        An optional file path to copy the outputfile to.
                        [PodioOutput]

```


The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
fccrun PythiaDelphes_config.py --Filename Pythia_ee_ZH_Zmumu_ecm240.cmd --filename p8_ee_ZH_ecm240.root -n 10000
fccrun PythiaDelphes_config.py --Filename Pythia_ee_ZZ_ecm240.cmd --filename p8_ee_ZZ_ecm240.root -n 10000
fccrun PythiaDelphes_config.py --Filename Pythia_ee_WW_ecm240.cmd --filename p8_ee_WW_ecm240.root -n 10000
```

