FCC-ee: Getting started with analysing simulated physics events
===================================================================================



Contents:

  * [FCC-ee: Getting started with analysing simulated physics events](#getting-started-with-analysing-simulated-physics-events)
    * [Overview](#overview)
    * [Installation](#installation)
 

## Overview

The FCC software is the common software for the FCC detector design study. We support the whole chain starting
from event generation through parameterized and full detector simulation, reconstruction and data analysis.
In this tutorial 


## Installation

For this tutorial the software needs to be locally installed. Create a directory for this tutorial and go there:
```
mkdir FCCeePhysics
cd FCCeePhysics
```

Clone the repository and go there:

```
git clone git@github.com:HEP-FCC/FlatTreeAnalyzer.git
cd FlatTreeAnalyzer
```

then initialize:
```
source ./init.sh
```


Analyses are run the following way:

```
./bin/analyze.py -n [analysis_name_in_heppy] -c [heppy_cfg] -t [heppy_tree_location] -o [output_dir] -p [analysis_parameters] -j [proc_dict]
```

The example we will run here for the ZH with Z to electrons is:

```
./bin/analyze.py -n ZH_Zee -c /afs/cern.ch/work/h/helsens/public/FCCSW_WS/heppy/ZH_Zee/analysis.py -t /afs/cern.ch/work/h/helsens/public/FCCSW_WS/data/ZH_Zee/ -o outputs/ZH_zee_ecm240_recoil/ -p templates/FCCee/zh_zee_ecm240_recoil.py -j /afs/cern.ch/work/h/helsens/public/FCCSW_WS/dict/FCCee_procDict_fcc_v01.json --nev 50000 -m
```

The example we will run here for the ZH with Z to muons is:

```
./bin/analyze.py -n ZH_Zmumu -c /afs/cern.ch/work/h/helsens/public/FCCSW_WS/heppy/ZH_Zmumu/analysis.py -t /afs/cern.ch/work/h/helsens/public/FCCSW_WS/data/ZH_Zmumu/ -o outputs/ZH_zmumu_ecm240_recoil/ -p templates/FCCee/zh_zmumu_ecm240_recoil.py -j /afs/cern.ch/work/h/helsens/public/FCCSW_WS/dict/FCCee_procDict_fcc_v01.json --nev 50000 -m
```

The files that will need to be edited are  ```templates/FCCee/zh_zee_ecm240_recoil.p``` for the Z boson decaying to electrons and ```
templates/FCCee/zh_mumu_ecm240_recoil.py``` for the Z boson decaying to muons.

Different selections are alrready implemented at the end of the files: ```selbase``` with no cut, ```selopt``` that tries to optimise based on some variables, ```selbb``` that only selects events with exactly 2 b-jets in the recoil, ```seltautau``` that only selects events with exactly 2 tau-jets in the recoil, ```selWhadWhad```  that only selects events with exactly 4 jets in the recoil, ```selWhadWlep```  that only selects events with exactly 2 jets and one lepton in the recoil, ```selWlepWlep``` that only selects events with exactly 2 leptons in the recoil and ```selWW``` that is a logical or between the various W boson selections.

