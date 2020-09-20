# FCC: Getting started with analysing simulated events


{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   apply an **event selection** on Delphes samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**
-   compare distributions produced with different generators

{% endobjectives %}



## Part II: Analyse with FCCAnalyses

For this part we start by cloning the FCCAnalyses GitHub repository

```bash
git clone https://github.com/HEP-FCC/FCCAnalyses.git
cd FCCAnalyses
```

and follow the compilation instructions [here](https://github.com/HEP-FCC/FCCAnalyses/#getting-started) to get started with **ONLY** the installation.
Once the code has been compiled, we can now run the pre-selection on previously produced samples:

```bash
python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py PATH_TO_FILES_PART_I/p8_ee_ZH_ecm240.root
python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py PATH_TO_FILES_PART_I/p8_ee_ZZ_ecm240.root
python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py PATH_TO_FILES_PART_I/p8_ee_WW_ecm240.root
```

this will produce small ntuples pre-selection files with only variables you are interested in.

lets now run the final selection on the pre-selection files:

```bash
python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py
```
 this will produce 2 files for each sample and each selection, one with final tree with variables of interest, and one with histograms.
 
 Now we can produce plots:
 
```python
 python bin/doPlots.py FCCeeAnalyses/ZH_Zmumu/dataframe/plots.py
```

and look at them in `FCCee/ZH_Zmumu/plots/`. 

Please note that the event statistics is not great because we only run on 10 000 events.


{% challenge "Exercises" %}

1) Modify `FCCeeAnalyses/ZH_Zmumu/dataframe/plots.py` to include the muon tracks (look at the output file or to `FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py` to check the name.

2) Add the track informations to the output files by modifying `FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py` for the `efcharged` collection and produce plots with them as in 1)

3) Produce plots with larger statistics by re-running `fccrun` with more events.

4) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary** 
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_v02.php). 

```bash
 python FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py
```

and as before run the final selection and plots:

```bash
python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py
python bin/doPlots.py FCCeeAnalyses/ZH_Zmumu/dataframe/plots.py
```
and look at the new plots in `FCCee/ZH_Zmumu/plots/`. 

To further increase the event statistics, increase the value (up to 1) of the parameter `fraction` in `FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py`


{% endchallenge %}

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
fccrun PythiaDelphes_config.py --Filename Pythia_LHE.cmd --filename wizhardp8_ee_Z_Zmumu_ecm91.root -n 10000
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
fccrun PythiaDelphes_config.py --Filename Pythia_ee_Zmumu_ecm91.cmd --filename p8_ee_Z_Zmumu_ecm91.root -n 10000
```

Now go to the `FCCAnalyses` repository you have cloned during Part II, and run the Z to mumu analysis on the files produced

```bash
python FCCeeAnalyses/Z_Zmumu/dataframe/analysis.py PATH_TO_FILES/wizhardp8_ee_Z_Zmumu_ecm91.root
python FCCeeAnalyses/Z_Zmumu/dataframe/analysis.py PATH_TO_FILES/p8_ee_Z_Zmumu_ecm91.root
```

Run the final selection:

```bash
python FCCeeAnalyses/Z_Zmumu/dataframe/finalSel.py
```

Now we can produce plots:
 
```python
 python bin/doPlots.py FCCeeAnalyses/Z_Zmumu/dataframe/plots.py
```

and look at the new plots in `FCCee/Z_Zmumu/plots/`. 


{% challenge  "**Exercises**"  %} 

1) Whizard already contains ISR/FSR. To see this effect, rerun FCCSW on the Whizard LHE file by uncommenting the ISR/FSR in the Pythia card, and run the analysis to produce new plots and compare (move the old plots to an other directory as they will be overwritten) 

2) Modify ```FCCeeAnalyses/Z_Zmumu/dataframe/analysis.py``` and ```FCCeeAnalyses/Z_Zmumu/dataframe/plots.py``` to include the muon tracks.

3) **For Experts** Produce the same process with madgraph, shower the LHE file produced with Ptyhia8 in FCCSW (together with Delphes) and compare the dimuon invariant mass distribution with Pythia and Whizard.

{% endchallenge %}
