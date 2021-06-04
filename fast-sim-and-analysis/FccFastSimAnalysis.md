# FCC: Getting started with analysing simulated events


{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   apply an **event selection** on Delphes samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**
-   compare distributions produced with different generators

{% endobjectives %}



## Part II: Analyse with FCCAnalyses

We stay in the same directory where we have produced our samples with ```DelphesPythia8_EDM4HEP```.

For this part we start by making sure we can use FCCAnalyses by checking we can load the library correctly:

```bash
python
import ROOT
ROOT.gSystem.Load("libFCCAnalyses")

```

if no error message, it means we can load it.

Alternatively, you can check with spack, replacing ```<version>``` by the key4hep version you have set up.


```bash
spack find -p -d key4hep-stack@<version> | grep fccanalyses
```

create a file called ```analysis.py``` containing


```python
import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (self.df
               # define an alias for muon index collection
               .Alias("Muon0", "Muon#0.index")
               # define the muon collection
               .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               #select muons on pT
               .Define("selected_muons", "ReconstructedParticle::sel_pt(10.)(muons)")
               # create branch with muon transverse momentum
               .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)") 
               # create branch with muon rapidity
               .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)") 
               # create branch with muon total momentum
               .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
               # create branch with muon energy 
               .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
               # find zed candidates from  di-muon resonances  
               .Define("zed_leptonic",         "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
               # write branch with zed mass
               .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
               # write branch with zed transverse momenta
               .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
               # calculate recoil of zed_leptonic
               .Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
               # write branch with recoil mass
               .Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)") 

        )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_muons_pt",
                "selected_muons_y",
                "selected_muons_p",
                "selected_muons_e",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "zed_leptonic_recoil_m"               
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

    infile  = sys.argv[2]
    outfile = sys.argv[1]
    ncpus = 2
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()
```


And run the pre-selection on previously produced samples:

```bash
python analysis.py p8_ee_ZH_ecm240.root p8_ee_ZH_ecm240_edm4hep.root
python analysis.py p8_ee_ZZ_ecm240.root p8_ee_ZZ_ecm240_edm4hep.root
python analysis.py p8_ee_WW_ecm240.root p8_ee_WW_ecm240_edm4hep.root
```

this will produce small ntuples pre-selection files with only variables you are interested in.

lets now run the final selection on the pre-selection files:

```bash
python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
```
 this will produce 2 files for each sample and each selection, one with final tree with variables of interest, and one with histograms.
 
 Now we can produce plots:
 
```python
 python config/doPlots.py examples/FCCee/higgs/mH-recoil/mumu/plots.py
```

and look at them in `outputs/FCCee/higgs/mH-recoil/mumu/plots/`. 

Please note that the event statistics is not great because we only run on 10 000 events.


{% challenge "Exercises" %}

1) Modify `examples/FCCee/higgs/mH-recoil/mumu/plots.py` to include the muon tracks (look at the output file or to `examples/FCCee/higgs/mH-recoil/mumu/analysis.py` to check the name.

2) Add the track informations to the output files by modifying `examples/FCCee/higgs/mH-recoil/mumu/analysis.py` for the `efcharged` collection and produce plots with them as in 1)

3) Produce plots with larger statistics by re-running `fccrun` with more events.

4) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary** 
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php). 

```bash
 python examples/FCCee/higgs/mH-recoil/mumu/preSel.py
```

and as before run the final selection and plots:

```bash
python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
python config/doPlots.py examples/FCCee/higgs/mH-recoil/mumu/plots.py
```
and look at the new plots in `outputs/FCCee/higgs/mH-recoil/mumu/plots/`. 

To further increase the event statistics, increase the value (up to 1) of the parameter `fraction` in `examples/FCCee/higgs/mH-recoil/mumu/preSel.py`


{% endchallenge %}
<!--
## Part III: Compare two Monte-Carlo samples

In this part we will compare two generators at the Z-pole.
First, follow this tutorial to generate Z events with Whizard and produce a Les Houches Events file: [here](https://hep-fcc.github.io/fcc-tutorials/fast-sim-and-analysis/FccFastSimGeneration.html#whizard).

Once you have followed this tutorial, start from a clean shell, go to your tutorial directoty and run the setup

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

Then create a generic Pythia8 card for reading LHE files
- **Pythia_LHE.cmd** 

```python
! 1) Settings that will be used in a main program.
Main:numberOfEvents = 1            ! number of events to generate
Main:timesAllowErrors = 10        ! abort run after this many flawed events

! 2) Tell Pythia that LHEF input is used
Beams:frameType             = 4
Beams:setProductionScalesFromLHEF = off
Beams:LHEF = events.lhe

! 4) Settings for the event generation process in the Pythia8 library.
! PartonLevel:ISR = on               ! initial-state radiation
! PartonLevel:FSR = on               ! final-state radiation
```

Where `Beams:LHEF = events.lhe` points to the file you have produced with Whizard.
Then we shower with Pythia in FCCSW and run the Delphes detector parameterisation:

```bash
DelphesPythia8_EDM4HEP $DELPHES/cards/delphes_card_IDEA.tcl edm4hep.tcl Pythia_LHE.cmd wzp8_ee_Z_Zmumu_ecm91.root
```

- **Pythia_ee_Zmumu_ecm91.cmd** 

```python
! File: Pythia_ee_Zmumu_ecm91.cmd
Random:setSeed = on
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Next:numberCount = 100           ! print message every n events
Beams:idA = 11                   ! first beam, e- = 11
Beams:idB = -11                  ! second beam, e+ = -11

! 3) Hard process : Z->mumu, at 91.2 GeV
Beams:eCM = 91.2               ! CM energy of collision
WeakSingleBoson:ffbar2ffbar(s:gmZ) = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! Decays
!Z0
23:onMode = off
23:onIfAny = 13
!gamma
22:onMode = off
22:onIfAny = 13
```

and run fcc on it

```bash
DelphesPythia8_EDM4HEP $DELPHES/cards/delphes_card_IDEA.tcl edm4hep.tcl Pythia_ee_Zmumu_ecm91.cmd p8_ee_Z_Zmumu_ecm91.root
```

Now go to the `FCCAnalyses` repository you have cloned during Part II, and run the Z to mumu analysis on the files produced

```bash
python examples/FCCee/higgs/mH-recoil/mumu/analysis.py PATH_TO_FILES/wizhardp8_ee_Z_Zmumu_ecm91.root
python examples/FCCee/higgs/mH-recoil/mumu/analysis.py PATH_TO_FILES/p8_ee_Z_Zmumu_ecm91.root
```

Run the final selection:

```bash
python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
```

Now we can produce plots:
 
```python
 python config/doPlots.py examples/FCCee/higgs/mH-recoil/mumu/plots.py
```

and look at the new plots in `outputs/FCCee/higgs/mH-recoil/mumu/plots/`. 


{% challenge  "**Exercises**"  %} 

1) Whizard already contains ISR/FSR. To see this effect, rerun FCCSW on the Whizard LHE file by uncommenting the ISR/FSR in the Pythia card, and run the analysis to produce new plots and compare (move the old plots to an other directory as they will be overwritten) 

2) Modify ``` examples/FCCee/higgs/mH-recoil/mumu/analysis.py``` and ```examples/FCCee/higgs/mH-recoil/mumu/plots.py``` to include the muon tracks.

3) **For Experts** Produce the same process with madgraph, shower the LHE file produced with Ptyhia8 in FCCSW (together with Delphes) and compare the dimuon invariant mass distribution with Pythia and Whizard.

{% endchallenge %}
-->