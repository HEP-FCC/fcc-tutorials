# FCC: Getting started with simulating events and analysing them

{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** and **MadGraph** within FCCSW
-   run a fast parametric **detector simulation** with **Delphes** within FCCSW
-   apply an **event selection** on those samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**

{% endobjectives %}
First login to lxplus or one of the virtual machine provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```python
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `fccrun`, which allows you to run jobs in the Gaudi framework is available on the command line:


```python
which fccrun
```

If the above command fails without printing a path like `/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/scripts/fccrun`, you ned to setup the FCC software stack 

```python
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

Please also add an environment varialbe for Delphes cards

```python
export DELPHES_DIR='/cvmfs/sft.cern.ch/lcg/releases/delphes/3.4.3pre02-e4803/x86_64-centos7-gcc8-opt/'
```

## Part I: Generate and simulate Events with FCCSW

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z to mumu and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by writing the pythia cards for the various processes.

- **Pythia_ee_ZH_Zmumu_ecm240.cmd** for the Higgs Stralhung signal

```python
! File: Pythia_ee_ZH_Zmumu_ecm240.cmd
Random:setSeed = on
Main:timesAllowErrors = 10          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
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


```python
import os
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
pythia8gentool.Filename = os.path.join(os.environ.get("FCCSWSHAREDIR", ""),"Generation/data/Pythia_ttbar.cmd")

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
muonSaveTool.delphesArrayName = "MuonMomentumSmearing/muons"
muonSaveTool.particles.Path      = "muons"
muonSaveTool.mcAssociations.Path = "muonsToMC"
muonSaveTool.isolationTags.Path  = "muonITags"

eleSaveTool = DelphesSaveChargedParticles("electrons")
eleSaveTool.delphesArrayName = "ElectronFilter/electrons"
eleSaveTool.particles.Path      = "electrons"
eleSaveTool.mcAssociations.Path = "electronsToMC"
eleSaveTool.isolationTags.Path  = "electronITags"

chhadSaveTool = DelphesSaveChargedParticles("pfcharged")
chhadSaveTool.delphesArrayName = "ChargedHadronFilter/chargedHadrons"
chhadSaveTool.saveIsolation = False
chhadSaveTool.particles.Path      = "pfcharged"
chhadSaveTool.mcAssociations.Path = "pfchargedToMC"


from Configurables import DelphesSaveNeutralParticles

# Particle-Flow Neutral Hadrons output tool
neuthadSaveTool = DelphesSaveNeutralParticles("pfneutrals")
neuthadSaveTool.delphesArrayName = "HCal/eflowNeutralHadrons"
neuthadSaveTool.saveIsolation = False
neuthadSaveTool.particles.Path      = "pfneutrals"
neuthadSaveTool.mcAssociations.Path = "pfneutralsToMC"

# Particle-Flow Photons output tool
pfphotonsSaveTool = DelphesSaveNeutralParticles("pfphotons")
pfphotonsSaveTool.delphesArrayName="ECal/eflowPhotons"
pfphotonsSaveTool.saveIsolation=False
pfphotonsSaveTool.particles.Path      = "pfphotons"
pfphotonsSaveTool.mcAssociations.Path = "pfphotonsToMC"
pfphotonsSaveTool.isolationTags.Path  = "pfphotonITags"

# Photons output tool
photonsSaveTool = DelphesSaveNeutralParticles("photons")
photonsSaveTool.delphesArrayName = "PhotonEfficiency/photons"
photonsSaveTool.particles.Path      = "photons"
photonsSaveTool.mcAssociations.Path = "photonsToMC"
photonsSaveTool.isolationTags.Path  = "photonITags"


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

fatjetSaveTool = DelphesSaveJets("fatjets")
fatjetSaveTool.delphesArrayName = "FatJetFinder/jets"
fatjetSaveTool.saveSubstructure = True
fatjetSaveTool.jets.Path                        = "fatjets"
fatjetSaveTool.jetConstituents.Path             = "fatjetParts"
fatjetSaveTool.jetsOneSubJettinessTagged.Path   = "jetsOneSubJettiness"
fatjetSaveTool.jetsTwoSubJettinessTagged.Path   = "jetsTwoSubJettiness"
fatjetSaveTool.jetsThreeSubJettinessTagged.Path = "jetsThreeSubJettiness"
fatjetSaveTool.subjetsTrimmingTagged.Path       = "subjetsTrimmingTagged"
fatjetSaveTool.subjetsPruningTagged.Path        = "subjetsPruningTagged"
fatjetSaveTool.subjetsPruning.Path              = "subjetsPruning"
fatjetSaveTool.subjetsSoftDropTagged.Path       = "subjetsSoftDropTagged"
fatjetSaveTool.subjetsSoftDrop.Path             = "subjetsSoftDrop"
fatjetSaveTool.subjetsTrimming.Path             = "subjetsTrimming"

from Configurables import DelphesSaveMet
metSaveTool = DelphesSaveMet("met")
metSaveTool.delphesMETArrayName = "MissingET/momentum"
metSaveTool.delphesSHTArrayName = "ScalarHT/energy"
metSaveTool.missingEt.Path = "met"


## Delphes simulator -> define objects to be written out
from Configurables import DelphesSimulation
delphessim = DelphesSimulation()
## Define Delphes card
delphessim.DelphesCard = os.path.join(os.environ.get("FCCSWSHAREDIR", ""), "Sim/SimDelphesInterface/data/FCChh_DelphesCard_Baseline_v01.tcl")
delphessim.ROOTOutputFile = ""
delphessim.ApplyGenFilter = True
delphessim.outputs = [
                       "DelphesSaveChargedParticles/muons",
                       "DelphesSaveChargedParticles/electrons",
                       "DelphesSaveNeutralParticles/photons",
                       "DelphesSaveChargedParticles/pfcharged",
                       "DelphesSaveNeutralParticles/pfphotons",
                       "DelphesSaveNeutralParticles/pfneutrals",
                       "DelphesSaveGenJets/genJets",
                       "DelphesSaveJets/jets",
                       "DelphesSaveJets/fatjets",                                        
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

```python
!fccrun PythiaDelphes_config.py -h
```











## Getting started
Login to lxplus or one of the virtual machine provided on open stack.
Usage of bash shell is highly recommended.
Create a working directory ```mkdir mytutorial; cd mytutorial```
Setup FCC software stack ```source /cvmfs/fcc.cern.ch/sw/latest/setup.sh```

## Produce Delphes events with FCCSW

### From Pythia8 directly


### From LHE events showered with Pythia8
