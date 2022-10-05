
# FCC: Getting started with analysing simulated events


:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

-   apply an **event selection** on Delphes samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**
-   compare distributions produced with different generators
:::


## Part II: Analyse with FCCAnalyses

We stay in the same directory where we have produced our samples with `DelphesPythia8_EDM4HEP`.

For this part we start by making sure we can use FCCAnalyses by checking we can load the library correctly:

```python
#!python
import ROOT
ROOT.gSystem.Load("libFCCAnalyses")

```

if no error message, it means we can load it.

Alternatively, you can check with spack, replacing `<version>` by the key4hep version you have set up.


```
spack find -p -d key4hep-stack@<version> | grep fccanalyses
```

create a file called `analysis_stage1.py` containing


```{python active="", eval=FALSE}
#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
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
            # create branch with zed mass
            .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
            # create branch with zed transverse momenta
            .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
            # calculate recoil of zed_leptonic
            .Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
            # create branch with recoil mass
            .Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)")
            # create branch with leptonic charge
            .Define("zed_leptonic_charge","ReconstructedParticle::get_charge(zed_leptonic)")
            # Filter at least one candidate
            .Filter("zed_leptonic_recoil_m.size()>0")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "zed_leptonic_pt",
            "zed_leptonic_m",
            "zed_leptonic_charge",
            "zed_leptonic_recoil_m"
        ]
        return branchList
```


And run the analysis stage 1 on previously produced samples:

```bash
# for testing purposes, take these from eos
TESTSAMPLEDIR=https://fccsw.web.cern.ch/testsamples/tutorial/
# if you want to use the previously produced samples, uncomment:
# TESTSAMPLEDIR=$PWD
fccanalysis run analysis_stage1.py --output p8_ee_ZH_ecm240.root --files-list $TESTSAMPLEDIR/p8_ee_ZH_ecm240_edm4hep.root
fccanalysis run analysis_stage1.py --output p8_ee_ZZ_ecm240.root --files-list $TESTSAMPLEDIR/p8_ee_ZZ_ecm240_edm4hep.root
fccanalysis run analysis_stage1.py --output p8_ee_WW_ecm240.root --files-list $TESTSAMPLEDIR/p8_ee_WW_ecm240_edm4hep.root
```

this will produce small ntuples pre-selection files with only variables you are interested in.

This first analysis stage usually runs on large samples on batch, and the idea is to produce small ntuples with less variables. From those small ntuples we could consider running a second analysis stage, for example let us create a file called `analysis_stage2.py` containing:

```{python active="", eval=FALSE}
processList = {
    'p8_ee_ZZ_ecm240':{},
    'p8_ee_WW_ecm240':{},
    'p8_ee_ZH_ecm240':{}
}

inputDir    = ""
outputDir   = "stage2"

#USER DEFINED CODE
import ROOT
ROOT.gInterpreter.Declare("""
bool myFilter(ROOT::VecOps::RVec<float> mass) {
    for (size_t i = 0; i < mass.size(); ++i) {
        if (mass.at(i)>80. && mass.at(i)<100.)
            return true;
    }
    return false;
}
""")
#END USER DEFINED CODE

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               #Filter to have exactly one Z candidate
               .Filter("zed_leptonic_m.size() == 1")
               #Define Z candidate mass
               .Define("Zcand_m","zed_leptonic_m[0]")
               #Define Z candidate recoil mass
               .Define("Zcand_recoil_m","zed_leptonic_recoil_m[0]")
               #Define Z candidate pt
               .Define("Zcand_pt","zed_leptonic_pt[0]")
               #Define Z candidate charge
               .Define("Zcand_q","zed_leptonic_charge[0]")
               #Define new var rdf entry (example)
               .Define("entry", "rdfentry_")
               #Define a weight based on entry (inline example of possible operations)
               .Define("weight", "return 1./(entry+1)")
               #Define a variable based on a custom filter
               .Define("MyFilter", "myFilter(zed_leptonic_m)")
               )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.
    def output():
        branchList = [
            "Zcand_m", "Zcand_pt", "Zcand_q","MyFilter","Zcand_recoil_m",
            "entry","weight"
        ]
        return branchList
```

And run the analysis stage 2 on previously produced samples in stage 1:

```bash
fccanalysis run analysis_stage2.py
```

lets now run the final selection on the pre-selection files, for that create a `analysis_final.py` file:

```{python active="", eval=FALSE}
#Input directory where the files produced at the pre-selection level are
inputDir  = "stage2"

#Input directory where the files produced at the pre-selection level are
outputDir  = "final"

processList = {
    'p8_ee_ZZ_ecm240':{},
    'p8_ee_WW_ecm240':{},
    'p8_ee_ZH_ecm240':{}
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee_procDict_spring2021_IDEA.json"

#produces ROOT TTrees, default is False
doTree = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"sel0":"Zcand_q == 0",
           "sel1":"Zcand_q == -1 || Zcand_q == 1",
           "sel2":"Zcand_m > 80 && Zcand_m < 100",
           "sel3":"MyFilter==true && (Zcand_m < 80 || Zcand_m > 100)"
            }


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mz":{"name":"Zcand_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom":{"name":"Zcand_m","title":"m_{Z} [GeV]","bin":40,"xmin":80,"xmax":100},
    "leptonic_recoil_m":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160},
    "leptonic_recoil_m_zoom1":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom2":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":400,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom4":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":800,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom5":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":2000,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom6":{"name":"Zcand_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":130.3,"xmax":132.5},
}
```

and run

```bash
fccanalysis final analysis_final.py
```

this will produce 2 files for each sample and each selection, one with final tree with variables of interest, and one with histograms.

Now we can write the code to produce plots, in `analysis_plots.py`:


```{python active="", eval=FALSE}
import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = 'final'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'plots/'

variables = ['mz','mz_zoom','leptonic_recoil_m','leptonic_recoil_m_zoom']

###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = ["sel0","sel1","sel2","sel3"]
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

Run the plotting script with the command:

```bash
fccanalysis plots analysis_plots.py
```


and look at them in `plots/`.

Please note that the event statistics is not great because we only produced on 10 000 events in the `k4SimDelphes` step.


:::{admonition} Exercises
:class: challenge

1) Modify `plots.py` to include the muon tracks (look at the output file `_edm4hep.root` or to `analysis.py` to check the name.

2) Add the track informations to the output files by modifying `analysis.py` for the `efcharged` collection and produce plots with them as in 1)

3) Produce plots with larger statistics by re-running `DelphesPythia8_EDM4HEP` with more events.

4) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary**
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php).
Add to your a `analysis_stage1.py` file

```{python active="", eval=FALSE}
processList = {
    'p8_ee_ZZ_ecm240':{'fraction':0.1},
    'p8_ee_WW_ecm240':{'fraction':0.1},
    'p8_ee_ZH_ecm240':{'fraction':0.1}
}
prodTag     = "FCCee/spring2021/IDEA/"
```

and run

```{bash active="", eval=FALSE}
fccanalysis run analysis_stage1.py
```

and as before run the stage 2, final selection and plots:

```{bash active="", eval=FALSE}
fccanalysis run analysis_stage2.py
fccanalysis final analysis_final.py
fccanalysis plots analysis_plots.py
```

and look at the new plots in `plots/`.

To further increase the event statistics, increase the value (up to 1) of the parameter `fraction` in `analysis_stage1` (no value mean 1)
:::
