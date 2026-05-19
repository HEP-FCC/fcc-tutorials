# Getting Started: Higgs Mass Analysis with FCCAnalyses

>
> Original author: Michele Selvaggi
>

Let's first clone and build `FCCAnalyses` with the following commands:
```bash
git clone --branch master https://github.com/HEP-FCC/FCCAnalyses.git
cd FCCAnalyses
source ./setup.sh
fccanalysis build -j 8
```
and create a directory containing this tutorial:
```bash
cd ..
mkdir tutorial && cd tutorial
```

Copy the necessary files, either from the web or from some location where the
files were produced locally

```bash
mkdir localSamples && cd localSamples
mkdir  p8_ee_WW_mumu_ecm240 && cd p8_ee_WW_mumu_ecm240
wget https://fccsw.web.cern.ch/tutorials/ana-sim-evt/p8_ee_WW_mumu_ecm240/p8_ee_WW_mumu_ecm240_edm4hep.root
cd ..
mkdir p8_ee_ZZ_mumubb_ecm240 && cd p8_ee_ZZ_mumubb_ecm240
wget https://fccsw.web.cern.ch/tutorials/ana-sim-evt/p8_ee_ZZ_mumubb_ecm240/p8_ee_ZZ_mumubb_ecm240_edm4hep.root
cd ..
mkdir p8_ee_ZH_Zmumu_ecm240  && cd p8_ee_ZH_Zmumu_ecm240
wget https://fccsw.web.cern.ch/tutorials/ana-sim-evt/p8_ee_ZH_Zmumu_ecm240/p8_ee_ZH_Zmumu_ecm240_edm4hep.root
cd ../..
```

This tutorial consists in two parts. Both parts will make use of ee->ZH (Z->mumu)events, with its relevant backgrounds ee->WW and ee->ZZ:

- in **Part I** you will construct the recoil mass observable and apply a list of pre-selection cuts.
- in **Part II** you will learn how to run an exclusive jet clustering algorithm, evaluate the various jet flavor probabilities and use them to select H->bb events.

:::{admonition} Learning Objectives
:class: objectives

In this first example, you will learn how to: 

-   read the **edm4hep** data format and construct physics observable (such as the recoil mass)
-  define C++ helper functions in a separate that will be compiled at run time 
-   apply an **event selection** and **fill histograms** in a single iteration using the **histmaker** option.
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with the **plot** option. 
:::

## Part I - Recoil Mass: Analysis and Histograms in a Single Step

Start by downloading this file called [functions.h](functions.h). This contains C++ helper functions that you will need to compute observables with RDataframe.

Next, download the [histmaker_recoil.py](histmaker_recoil.py) script, which processes the previously produced ROOT samples, reconstructs muon and Z candidates, applies a sequence of event-selection cuts, and produces a set of histograms. 

The script first defines the input/output paths, luminosity scaling, and histogram binning. The main analysis logic is implemented in the ```build_graph``` function: reconstructed muons are selected and isolated muons with ```p > 20 GeV``` are retained. The analysis then applies successive cuts, including opposite-sign muon selection, Z-boson candidate reconstruction, Z mass and momentum requirements, missing-energy selection, and finally a recoil-mass window to suppress background processes.

Before running the script, update the ```inputDir``` variable so it points to the directory containing your local samples; the output histograms will be written to ```outputDir```. Finally, run the histmaker script using the fccanalysis ```run``` parameter to generate a ROOT file containing the resulting TH1 histograms:

```bash
fccanalysis run histmaker_recoil.py
```

Now download the the plotting script [plots_recoil.py](plots_recoil.py) and run it using the fccanalysis ```plots``` parameter:


```bash
fccanalysis plots plots_recoil.py
```

Please note that the event statistics is not great because we only produced on 10 000 events in the `Delphes Fast Simulation` step.


## Part II - Jet Flavor: Producing a flat ntuple tree before creating histograms and plots

:::{admonition} Learning Objectives
:class: objectives

In this second example, you will learn how to: 

-  read the **edm4hep** data format, produce jet collections and evaluate the ParticleNet jet tagger score and apply an an event **preselection**
-  produce **flat ntuples** with observables of interest with **FCCAnalyses**
-  apply an **event selection** and **fill histograms** in a single iteration using the **histmaker** option.
-   produce plots with the **plot** option. 
:::


This first analysis stage usually runs on large samples on batch, and the idea is to produce small ntuples with less variables. Also, jet inference of the jet tagger is pretty slow, and usually has to be performed only once. In this exercise we will run the **histmaker** in a separate, second stage. 

Download this analysis script [treemaker_flavor.py](treemaker_flavor.py) and run

```bash
fccanalysis run treemaker_flavor.py
```

This will produce a root file for every process containing a flat tree `events` containing high-level variables. In addition to selecting muons as done in the previous example, this script create a new collection of `ReconstructedParticles` without the two high energy muons, and runs the jet clustering algorithm in exclusive N=2 mode of the new collection. In such a way, the two clustered jets form the H->jj jet candidates. The jet flavour algorithm is then evaluated on these two jets and the relevant scores are stored in the output tree.   

Now we can download a dedicated [histmaker_flavor.py](histmaker_flavor.py) script, that runs this time on the just created flat ntuples files instead of the edm4hep format.

Run it as before: 

```bash
fccanalysis run histmaker_flavor.py
```

This script takes the ntuples produced in the previous step, applies a similar selection as in the previous examples, but requires the jets to have a high probability to be B-like. 

To compare the results between the flavor and recoil approaches, we again produce plots using a dedicated [plots_flavor.py](plots_flavor.py) script and run it:

```bash
fccanalysis plots plots_flavor.py
```

:::{admonition} Exercises
:class: challenge

## Simple

1) Modify `histmaker_flavor.py` to require the two jets individually to be B-like, i.e requiring the B score is greater 0.5 for each jet. 

2) Selecting gluon-like jets instead. You will need to modify both the  `treemaker_flavor.py` and `histmaker_flavor.py` for this.)

3) Produce plots with larger statistics by re-running `DelphesPythia8_EDM4HEP` with more events. In particular produce a ZZ inclusive sample using to include all Z decays. Rerun all the examples above.

## Advanced

1) To evaluate the impact of detector performance, smear the neutral hadron resolution in the `ReconstructedParticlesNoMuons` collection and check the impact on the dijet invariant mass resolution. An example can be found [here] (https://github.com/HEP-FCC/FCCAnalyses/blob/master/examples/FCCee/smearing/smear_jets.py):

2) Now smear the impact parameter resolution and evaluate the imapct on the efficiency of selecting two B-tagged jets or two C-tagged jets. 

3) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary**
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](https://fcc-physics-events.web.cern.ch/FCCee/spring2021/Delphesevents_IDEA.php).
Add to your a `analysis_stage1.py` file

```python
processList = {
    'p8_ee_ZZ_ecm240':{'fraction':0.1},
    'p8_ee_WW_ecm240':{'fraction':0.1},
    'p8_ee_ZH_ecm240':{'fraction':0.1}
}
prodTag     = "FCCee/winter2023/IDEA/"
:::
