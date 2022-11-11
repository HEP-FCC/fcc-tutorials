# FCCAnalyses getting started
Welcome to FCCAnalyses, a common framework to process large amount of samples and easily produce results. This framework allows one to write
full analysis, taking [EDM4hep](https://github.com/key4hep/EDM4hep) input ROOT files and producing the plots.

:::{admonition} Prerequisites
:class: prereq
As usual, if you aim at contributing to the repository, please fork it, develop your features and submit a pull requests.
 To have access to the common FCC samples, you need to be subscribed to one of the following e-groups (with owner approval) `fcc-eos-read`. For the time being, the configuration files are accessible on `fccsw` public AFS. This is not optimal and will be changed in the future with migration to DIRAC, thus you are also kindly asked to contact `emmanuel.perezATSPAMNOTcern.ch`, `gerardo.ganisATSPAMNOTcern.ch`, `clement.helsensATSPAMNOTcern.ch` and request access to `/afs/cern.ch/work/f/fccsw/public/FCCDicts/`.
:::

Detailed code documentation can be found [here](http://hep-fcc.github.io/FCCAnalyses/doc/latest/index.html).

## RootDataFrame based

Using ROOT dataframe allows to use modern, high-level interface and very quick processing time as it natively supports multithreading. In this documentation, everything from reading EDM4hep files on EOS and producing flat n-tuples, to running a final selection and plotting the results will be explained. This documentation does not aim at explaining ROOT dataframe, documentation on the topic is available [here](https://root.cern/doc/master/classROOT_1_1RDataFrame.html).


## Getting started

In order to use the FCC analysers within ROOT dataframe, a dictionary needs to be built and put into `LD_LIBRARY_PATH` (this happens in `setup.sh`). The following needs to be done when running local code and for developers.

```shell
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

:::{admonition} Nota Bene
:class: callout
Each time changes are made in the C++ code, for example in  `analyzers/dataframe/` please do not forget to re-compile such that you can use your modified code.
:::



## Generalities

Analyses in the FCCAnalyses framework usually follow standardized workflow, which consists of multiple files inside a single directory. Individual files denote steps in the analysis and have the following meaning:

1. `analysis.py` or `analysis_stage<num>`: In this file(s) the class of type
   `RDFanalysis` is used to define the list of analysers and filters to run on
   (`analysers` function) as well as the output variables (`output` function).
   It also contains the configuration parameters `processList`, `prodTag`,
   `outputDir`, `inputDir`, `nCPUS` and `runBatch`. User can define multiple
   stages of `analysis.py`. The first stage will most likely run on centrally
   produced EDM4hep events, thus the usage of `prodTag`. When running a second
   analysis stage, user points to the directory where the samples are
   located using `inputDir`. A skeleton can be seen below.

:::{admonition} FCCAnalyses initial stage code skeleton
   :class: toggle
```python
#List of processes, to run over official samples
processList = {
    'p8_ee_ZZ_ecm240':{},#Run the full statistics in one output file named <outputDir>/p8_ee_ZZ_ecm240.root
    'p8_ee_ZZ_ecm240':{},#Run the full statistics in one output file named <outputDir>/p8_ee_ZH_ecm240.root
}

#Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#output directory, default is local running directory
outputDir   = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"

# Mandatory: RDFanalysis class where the user defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    # Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
#Add your .Define("<name>","<alogorithm>") here
             )
       return df2

    #__________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
       branchList = [
#Add the branches <name> you want to save here
       ]
       return branchList
```
:::

2. `analysis_final.py`: This analysis file contains the final selections and it
   runs over the locally produced n-tuples from the various stages of
   `analysis.py`. It contains a link to the `procDict.json` such that the
   samples can be properly normalised by getting centrally produced cross
   sections. (this might be removed later to include everything in the yaml,
   closer to the sample). It also contains the list of processes (matching the
   standard names), the number of CPUs, the cut list, and the variables (that
   will be both written in a `TTree` and in the form of `TH1` properly
   normalised to an integrated luminosity of 1pb<sup>-1</sup>. A skeleton can be seen below.

:::{admonition} FCCAnalyses final stage code skeleton
:class: toggle
```python
#Input directory where the files produced at the pre-selection level are
inputDir  = "outputs/FCCee/higgs/mH-recoil/mumu/stage1/"

#Input directory where the files produced at the pre-selection level are
outputDir  = "outputs/FCCee/higgs/mH-recoil/mumu/final/"

processList = {
       'p8_ee_ZZ_ecm240':{},
       'p8_ee_ZH_ecm240':{}
   }

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
#Add here list of cuts like "<cutname>":"<CUTS>"
  }

#Dictionary for the ouput variable/hitograms.
histoList = {
#Add histograms like "<histoname>":{"name":"<branchname>","title:<histotitle>","bin":<number of bins>,"xmin":<x min>,"xmax":<x max>}
}
:::

3. `analysis_plots.py`: This analysis file is used to select the final
   selections from running `analysis_final.py` to plot. It usually contains
   information about how to merge processes, write some extra text, normalise
   to a given integrated luminosity etc... For the moment it is possible to
   only plot one signal at the time, but several backgrounds.

:::{admonition} FCCAnalyses code plot skeleton
:class: toggle
```python
import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = 'outputs/FCCee/higgs/mH-recoil/mumu/final/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'outputs/FCCee/higgs/mH-recoil/mumu/plots/'

variables = [#Add the histogram names
]

#Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = [#Add list of cut names
]

extralabel = {}
extralabel[<cutname>] = "My selection"

colors = {}
colors['ZH'] = ROOT.kRed
colors['ZZ'] = ROOT.kGreen+2

plots = {}
plots['ZH'] = {
  'signal':{'ZH':['p8_ee_ZH_ecm240']},
  'backgrounds':{'ZZ':['p8_ee_ZZ_ecm240']}
  }

legend = {}
legend['ZH'] = 'ZH'
legend['ZZ'] = 'ZZ'
```
:::

## Example analysis

To better explain the FCCAnalyses workflow let's run our example analysis. The
analysis should be located at `examples/FCCee/higgs/mH-recoil/mumu/`.


### Pre-selection

The pre-selection runs over already existing and properly registered FCCSW
EDM4hep events. The dataset names with the corresponding statistics can be found
[here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/spring2021/Delphesevents_IDEA.php)
for the IDEA spring 2021 campaign. The `processList` is a dictionary of
processes, each process having it's own dictionary of parameters. For example
```python
'p8_ee_ZH_ecm240':{'fraction':0.2, 'chunks':2, 'output':'p8_ee_ZH_ecm240_out'}
```
where `p8_ee_ZH_ecm240` should match an existing sample in the database,
`fraction` is the fraction of the sample you want to run on (default is 1),
`chunks` is the number of jobs to run (you will have the corresponding number
of output files) and `output` in case you need to change the name of the output
file (please note that then the sample will not be matched in the database for
`finalSel.py` histograms normalisation). The other parameters are explained in
[the example file](https://github.com/HEP-FCC/FCCAnalyses/tree/master/example/FCCee/higgs/mH-recoil/analysis_stage1.py).

To run the pre-selection stage of the example analysis run:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py
```

This will create the output files in the `ZH_mumu_recoil/stage1` subdirectory
of the output director specified with parameter `outDir` in the file.

You also have the possibility to bypass the samples specified in the
`processList` variable by using command line parameter `--output`, like so:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py \
      --output <myoutput.root> \
      --files-list <file.root or file1.root file2.root or file*.root>
```

The example analysis consists of two pre-selection stages, to run the second one
slightly alter the previous command:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage2.py
```


#### Pre-selection on batch (HTCondor)

It is also possible to run the pre-selection step on the batch. For that the
`runBatch` parameter needs to be set to true. Please make sure you select a
long enough `batchQueue` and that your computing group is properly set
`compGroup` (as you might not have the right to use the default one
`group_u_FCC.local_gen` as it request to be part of the FCC computing e-group
`fcc-experiments-comp`). When running on batch, you should use the `chunk`
parameter for each sample in your `processList` such that you benefit from high
parallelisation.


### Final selection

The final selection runs on the pre-selection files that were produced in the
[Pre-selection](#pre-selection) step. In the configuration file
`analysis_final.py` various cuts are defined to be run on and the final
variables to be stored in both a `TTree` and histograms. This is why the
variables needs extra fields like `title`, number of bins and range for the
histogram creation. In the example analysis it can be run like this:

```shell
fccanalysis final examples/FCCee/higgs/mH-recoil/mumu/analysis_final.py
```

This will create 2 files per selection `SAMPLENAME_SELECTIONNAME.root` for the
`TTree` and `SAMPLENAME_SELECTIONNAME_histo.root` for the histograms.
`SAMPLENAME` and `SELECTIONNAME` correspond to the name of the sample and
selection respectively in the configuration file.


### Plotting

The plotting analysis file `analysis_plots.py` contains not only details for
the rendering of the plots but also ways of combining samples for plotting.
In the example analysis it can be run in the following manner:

```shell
fccanalysis plots examples/FCCee/higgs/mH-recoil/mumu/analysis_plots.py
```

Resulting plots will be located the `outdir` defined in the analysis file.

### Experimental

In an attempt to ease the development of new physics case studies, such as for the [FCCee physics performance](https://github.com/HEP-FCC/FCCeePhysicsPerformance) cases, a new experimental analysis package creation tool is introduced.
[See here](case-studies/README.md) for more details.
