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

```python
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

lets now run the final selection on the pre-selection files, for that create a ```finalSel.py``` file:
```python
import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "outputs/FCCee/higgs/mH-recoil/mumu/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee_procDict_spring2021_IDEA.json"
process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"zed_leptonic_m.size() == 1",
            "sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "mz"                    :{"name":"zed_leptonic_m"       ,"title":"m_{Z} [GeV]"            ,"bin":125,"xmin":0 ,"xmax":250},
    "mz_zoom"               :{"name":"zed_leptonic_m"       ,"title":"m_{Z} [GeV]"            ,"bin":40 ,"xmin":80,"xmax":100},
    "leptonic_recoil_m"     :{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0 ,"xmax":200},
    "leptonic_recoil_m_zoom":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160}
}

###Number of CPUs to use
NUM_CPUS = 2

###Produce TTrees
DO_TREE=True

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS, doTree=DO_TREE)
```

and run 
```bash
python finalSel.py
```


this will produce 2 files for each sample and each selection, one with final tree with variables of interest, and one with histograms.
 
Now we can write the code to produce plots, in ```plots.py```:


```python
import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = ''
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'plots/'

variables = ['mz','mz_zoom','leptonic_recoil_m','leptonic_recoil_m_zoom']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = ["sel0","sel1"]
selections['ZH_2'] = ["sel0","sel1"]

extralabel = {}
extralabel['sel0'] = "Selection: N_{Z} = 1"
extralabel['sel1'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV"

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['VV'] = ROOT.kGreen+3

plots = {}
plots['ZH'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
               'backgrounds':{'WW':['p8_ee_WW_ecm240'],
                              'ZZ':['p8_ee_ZZ_ecm240']}
           }


plots['ZH_2'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
                 'backgrounds':{'VV':['p8_ee_WW_ecm240','p8_ee_ZZ_ecm240']}
             }

legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['VV'] = 'VV boson'
```

And run the plots (the line below is temporary, will be updated once we properly link the env var) 
```bash
python /cvmfs/sw.hsf.org/spackages/linux-centos7-x86_64/gcc-8.3.0/fccanalyses-0.3.1-7adsdbjfcz7glgzdm7emtbbcn5eiia7f/python/config/doPlots.py plots.py 
```


and look at them in `plots/`. 

Please note that the event statistics is not great because we only produced on 10 000 events in the ```k4SimDelphes``` step.


{% challenge "Exercises" %}

1) Modify `plots.py` to include the muon tracks (look at the output file ```_edm4hep.root``` or to `analysis.py` to check the name.

2) Add the track informations to the output files by modifying `analysis.py` for the `efcharged` collection and produce plots with them as in 1)

3) Produce plots with larger statistics by re-running ```DelphesPythia8_EDM4HEP``` with more events.

4) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary** 
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php). 
create a ```preSel.py``` file

```python
basedir="https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee/yaml/FCCee/spring2021/IDEA/"
outdir="output_spring2021"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)

process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']
fraction=0.1

import config.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)
```

```python
 python preSel.py
```

and as before run the final selection and plots:

```bash
python finalSel.py
python /cvmfs/sw.hsf.org/spackages/linux-centos7-x86_64/gcc-8.3.0/fccanalyses-0.3.1-7adsdbjfcz7glgzdm7emtbbcn5eiia7f/python/config/doPlots.py examples/FCCee/higgs/mH-recoil/mumu/plots.py
```
and look at the new plots in `plots/`. 

To further increase the event statistics, increase the value (up to 1) of the parameter `fraction` in `preSel.py`


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
