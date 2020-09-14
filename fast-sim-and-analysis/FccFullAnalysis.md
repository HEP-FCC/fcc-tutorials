# FCC-hh: Pythia, Delphes, Heppy Analysis


{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** within FCCSW
-   run a fast parametric **detector simulation** with **Delphes** within FCCSW

{% endobjectives %}


But first, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `fccrun`, which allows you to run jobs in the Gaudi framework is available on the command line:



```bash
which fccrun
```



If the above command fails without printing a path like `/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.10/x86_64-centos7-gcc62-opt/scripts/fccrun` check [**the documentation page on FCC software setup**](https://github.com/HEP-FCC/fcc-tutorials/blob/master/FccSoftwareGettingStarted.md).

## Part I: Generate and simulate Events with FCCSW

For this tutorial we will consider the following **physics processes**:

-   p p -> H -> 4 l
-   p p -> Z/gamma Z/gamma -> 4 l

Pythia can be configured to hadronize previously generated hard scattering in the form of Les Houches event files (`.lhe`),
or generate the hard process itself and then run the parton shower and hadronization.
**In either case, the FCCSW takes as input a Pythia8 configuration file** (`.cmd`), and does not need to know which approach was used. 

For this tutorial, we are going to run Pythia8 on previously produced LHE files (with [MG5_aMCatNLO](https://launchpad.net/mg5amcnlo)).
Additional Pythia8 configurations can be found in `FCCSW/Generation/data`.


```
! File: Pythia_pp_h_4l.cmd
!
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.
! Names are case-insensitive  -  but spellings-sensitive!
! Adjusted from Pythia example: main42.cmnd

! 1) Settings that will be used in a main program.
Main:numberOfEvents = 1            ! number of events to generate
Main:timesAllowErrors = 3          ! abort run after this many flawed events
#Random:seed = 1234                ! initialize random generator with a seed


! 2) Settings related to output in init(), next() and stat() functions.
Init:showChangedSettings = on      ! list changed settings
Init:showAllSettings = off         ! list all settings
Init:showChangedParticleData = on  ! list changed particle data
Init:showAllParticleData = off     ! list all particle data
Next:numberCount = 10              ! print message every n events
Next:numberShowLHA = 1             ! print LHA information n times
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 1           ! print event record n times
Stat:showPartonLevel = off         ! additional statistics on MPI

! 3b) PDF settings. Default is to use internal PDFs
! some pdf sets examples: cteq61.LHpdf cteq61.LHgrid MRST2004nlo.LHgrid
#PDF:pSet = LHAPDF5:MRST2001lo.LHgrid
! Allow extrapolation of PDF's beyond x and Q2 boundaries, at own risk.
! Default behaviour is to freeze PDF's at boundaries.
#PDF:extrapolate = on

! 4) Read-in Les Houches Event file - alternative beam and process selection.
Beams:frameType = 4                      ! read info from a LHEF
Beams:LHEF = pp_h_4l.lhe

! 5) Other settings. Can be expanded as desired.
! Note: may overwrite some of the values above, so watch out.

```



The detector response of the the baseline FCC-hh detector configuration is calculated with Delphes.
Other detector cards can be found in the `$DELPHES_DIR/cards` directory, such as a ATLAS, CMS or ILD detector configurations:
`delphes_card_ATLAS.tcl`, `delphes_card_CMS.tcl` and `delphes_card_ILD.tcl`. Many of the questions you might have on Delphes Fast Simulation are probably answered
[here](https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook).

Both Pythia8 and Delphes are integrated in the Gaudi-based FCCSW framework as *Algorithms*. A job that runs the whole workflow consists of the following:

* `GenAlg` (Top level Generation Algorithm, with a `tool` that calls Pythia8)
* `HepMCConverter` (takes the HepMC output and translates it to the FCC event data model, understood by the Sim Algorithm)
* `DelphesSimulation`(Delphes integration, outputs reconstructed objects in the FCC event data model)
* `PodioOutput` (writes the event data to a root file on disk)

To run this job, a job options like the following is needed (**Note:** While the format of the configuration is a python file, it is not necessarily "pythonic". It can be used with GaudiPython, but we will only use it as to straightforwardly write down a job description for use with `fccrun` ) 


```python
#%%writefile PythiaDelphes_config.py
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
pythia8gentool.Filename = os.path.join(os.environ.get("FCCSWBASEDIR", ""),"share/FCCSW/Generation/data/Pythia_ttbar.cmd")

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
delphessim.DelphesCard = os.path.join(os.environ.get("FCCSWBASEDIR", ""), "share/FCCSW/Sim/SimDelphesInterface/data/FCChh_DelphesCard_Baseline_v01.tcl")
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

    Writing PythiaDelphes_config.py


The `fccrun` allows to change most `Properties` of the job on the command line. All possible arguments to fccrun  are listed with the command 


```bash
fccrun PythiaDelphes_config.py -h
```

     -->  GenAlg  -->  Converter  -->  DelphesSimulation  -->  out  
    
    usage: fccrun [-h] [--dry-run] [-v] [-n NUM_EVENTS] [-l] [--gdb]
                  [--ncpus NCPUS] [--ROOTOutputFile [ROOTOUTPUTFILE]]
                  [--ApplyGenFilter [APPLYGENFILTER]]
                  [--outputs OUTPUTS [OUTPUTS ...]] [--DelphesCard [DELPHESCARD]]
                  [--PrintEmptyCounters [PRINTEMPTYCOUNTERS]] [--input [INPUT]]
                  [--Filename [FILENAME]]
                  [--printPythiaStatistics [PRINTPYTHIASTATISTICS]]
                  [--outputCommands OUTPUTCOMMANDS [OUTPUTCOMMANDS ...]]
                  [--filename [FILENAME]]
                  [--hepmcStatusList HEPMCSTATUSLIST [HEPMCSTATUSLIST ...]]
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
      --ROOTOutputFile [ROOTOUTPUTFILE]
                            Name of Delphes Root output file, if defined, the
                            Delphes standard tree write out (in addition to FCC-
                            EDM based output to transient data store)
                            [DelphesSimulation]
      --ApplyGenFilter [APPLYGENFILTER]
                            only for debugging purposes. If entire MC particle
                            collection is needed, request in cfg file.
                            [DelphesSimulation]
      --outputs OUTPUTS [OUTPUTS ...]
                            [DelphesSimulation]
      --DelphesCard [DELPHESCARD]
                            Name of Delphes tcl config file with detector and
                            simulation parameters [DelphesSimulation]
      --PrintEmptyCounters [PRINTEMPTYCOUNTERS]
                            force printing of empty counters, otherwise only
                            printed in DEBUG mode [GaudiCommon<Algorithm>]
      --input [INPUT]       Name of the file to read [unknown owner type]
      --Filename [FILENAME]
                            [PythiaInterface]
      --printPythiaStatistics [PRINTPYTHIASTATISTICS]
                            Print Pythia Statistics [PythiaInterface]
      --outputCommands OUTPUTCOMMANDS [OUTPUTCOMMANDS ...]
                            A set of commands to declare which collections to keep
                            or drop. [PodioOutput]
      --filename [FILENAME]
                            Name of the file to create [PodioOutput]
      --hepmcStatusList HEPMCSTATUSLIST [HEPMCSTATUSLIST ...]
                            list of hepmc statuses to keep. An empty list means
                            all statuses will be kept [HepMCToEDMConverter]


Thus The following commands will run Pythia8 and Delphes and produce the relevant signal and background samples:


```bash
xrdcp root://eospublic.cern.ch//eos/experiment/fcc/hh/testsamples/pp_h_4l.lhe ./pp_h_4l.lhe
fccrun PythiaDelphes_config.py --Filename $FCCSWBASEDIR/share/FCCSW/Generation/data/Pythia_pp_h_4l.cmd --filename pp_h_4l.root -n 100
```


```bash
xrdcp root://eospublic.cern.ch//eos/experiment/fcc/hh/testsamples/pp_zgzg_4l.lhe ./pp_zgzg_4l.lhe
fccrun PythiaDelphes_config.py --Filename  $FCCSWBASEDIR/share/FCCSW/Generation/data/Pythia_pp_zgzg_4l.cmd --filename pp_zgzg_4l.root -n 100
```



For a complete discussion on the structure of configuration file, see [this page](https://github.com/HEP-FCC/FCCSW/blob/master/Sim/SimDelphesInterface/doc/FccPythiaDelphes.md).
Aside from I/O and number of events (which can be specified through command line),
for most use cases as a user you won't need to apply any change to the configuration file.

In addition to the **sequence of modules** to be executed, and which **output collections** to be stored in the output tree, the following
parameters can be specified via the configuration file:

The output is a ROOT file containing a tree in the FCC [Event Data Model structure](https://github.com/HEP-FCC/fcc-edm). It is browsable with ROOT:





```bash
rootls -t pp_h_4l.root
```

It contains the Generation-level particles (`skimmedGenParticles`) as well as the Reconstruction-level Delphes output (`muons`, `electrons` ...)


Plotting some basic quantities directly on this output is possible, although not very handy:


```python
import ROOT
c = ROOT.TCanvas()
f = ROOT.TFile("pp_h_4l.root")
# get event tree
events = f.Get("events")
events.Draw("sqrt(electrons[0].core.p4.px*electrons[0].core.p4.px + electrons[0].core.p4.py*electrons[0].core.p4.py)")
ROOT.gPad.SetLogy()
c.Draw()

```




![png](FCCFullAnalysis_files/FCCFullAnalysis_16_1.png)


To save time and computing power, more events with the same configuration can be taken from eos:


```bash
export EOS_MGM_URL="root://eospublic.cern.ch"
cp /eos/experiment/fcc/hh/tutorials/Higgs_4l/pp_h_4l.root .
cp /eos/experiment/fcc/hh/tutorials/Higgs_4l/pp_zgzg_4l.root .
```


## Other documentation

-   [FCCSW webpage](http://fccsw.web.cern.ch/fccsw/index.html)
-   [Pythia8 manual](http://home.thep.lu.se/~torbjorn/pythia81html/Welcome.html)
-   [Delphes website](https://cp3.irmp.ucl.ac.be/projects/delphes)































