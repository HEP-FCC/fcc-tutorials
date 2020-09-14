FCC: Getting started with the production and analysis of fast-simulated events
===================================================================================


## Overview

If you want to get started fast with the analysis of fast-simulated
events, you're at the right place.

Fast simulation is currently supported through the Delphes approach. Support for the Papas approach, initially used for FCC-ee, is
discontinued. 

An analysis ntuple will be produced with ROOT's RDataFrame, a simple modular event processing framework for high energy physics.

## Enabling FCCSW

* To configure your environment for the FCC software, just do:

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

Builds exist on CernVM-FS for CentOS7 (this is the system run on `lxplus`) using gcc8.

The `fccrun` steering application should be available at this point:

```bash
which fccrun
```

```
# the output might differ, but shouldn't be empty
/cvmfs/fcc.cern.ch/sw/views/releases/fccsw/0.13/LCG_97a_FCC_2/x86_64-centos7-gcc8-opt/scripts/fccrun
```

**You will need to source this script everytime you want to use the
software.**



## Generators

### Overview

The physics generators available for FCC typically come form the underlying LCG stack. However, any generator
able to generate events in one of the understood formats, e.g. HepMC or LHEf, can be used in standalone.
This pages intend to illustrate the use of a few general purpose generators available when enabling FCCSW:
pythia8, whizard, MadGraph5, Herwig.

###  Pythia8

Pythia8 is fully intergrated in FCCSW and it provides diverse functionality in addition to event generation,
including capability to read events in LHEF format.


###  Whizard

Whizard is available as standalone program:

```bash
which whizard
```

```
/cvmfs/fcc.cern.ch/sw/views/releases/fccsw/0.13/LCG_97a_FCC_2/x86_64-centos7-gcc8-opt/bin/whizard
```

Whizard is run as this:

```bash
whizard <process_config>.sin
```

Example of process configuration files are found under

``` bash
ls /cvmfs/fcc.cern.ch/sw/views/releases/fccsw/0.13/LCG_97a_FCC_2/x86_64-centos7-gcc8-opt/share/whizard/examples/
```

Some examples more specific to FCC can be found under

```bash
ls /eos/project-f/fccsw-web/www/share/gen/whizard/
```

It is advised to work in a separate directory for each process. For example, for Z_mumu, we have:

```bash
 mkdir test_whizard/Z_mumu; cd test_whizard/Z_mumu
 cp -rp /eos/project-f/fccsw-web/www/share/gen/whizard/Zpole/Z_mumu.sin .
 whizard Z_mumu.sin
 ```

 ```
| Writing log to 'whizard.log'
|=============================================================================|
|                                                                             |
|    WW             WW  WW   WW  WW  WWWWWW      WW      WWWWW    WWWW        |
|     WW    WW     WW   WW   WW  WW     WW      WWWW     WW  WW   WW  WW      |
|      WW  WW WW  WW    WWWWWWW  WW    WW      WW  WW    WWWWW    WW   WW     |
|       WWWW   WWWW     WW   WW  WW   WW      WWWWWWWW   WW  WW   WW  WW      |
|        WW     WW      WW   WW  WW  WWWWWW  WW      WW  WW   WW  WWWW        |
|                                                                             |
|                                                                             |

...

|=============================================================================|
|                               WHIZARD 2.8.2
|=============================================================================|
| Reading model file '/cvmfs/sft.cern.ch/lcg/releases/LCG_97a_FCC_2/MCGenerators/whizard/2.8.2/x86_64-centos7-gcc8-opt/share/whizard/models/SM.mdl'
| Preloaded model: SM
| Process library 'default_lib': initialized
| Preloaded library: default_lib
| Reading model file '/cvmfs/sft.cern.ch/lcg/releases/LCG_97a_FCC_2/MCGenerators/whizard/2.8.2/x86_64-centos7-gcc8-opt/share/whizard/models/SM_hadrons.mdl'
| Reading commands from file 'Z_mumu.sin'
| Switching to model 'SM', scheme 'default'

...

$description = "A WHIZARD 2.8 Example.
   Z -> mumu @ 91.2 events for FCC ee."
$y_label = "$N_{\textrm{events}}$"
$lhef_version = "3.0"
$sample = "z_mumu"
| Starting simulation for process 'zmumu'
| Simulate: using integration grids from file 'zmumu.m1.vg'
| RNG: Initializing TAO random-number generator
| RNG: Setting seed for random-number generator to 22345
| Simulation: requested number of events = 1000
|             corr. to luminosity [fb-1] =   6.6285E-04
| Events: writing to LHEF file 'z_mumu.lhe'
| Events: writing to raw file 'z_mumu.evx'
| Events: generating 1000 unweighted, unpolarized events ...
| Events: event normalization mode '1'
|         ... event sample complete.
| Events: actual unweighting efficiency =   1.16 %
Warning: Encountered events with excess weight: 6 events (  0.600 %)
| Maximum excess weight = 2.465E+00
| Average excess weight = 4.511E-03
| Events: closing LHEF file 'z_mumu.lhe'
| Events: closing raw file 'z_mumu.evx'
| There were no errors and    2 warning(s).
| WHIZARD run finished.
|=============================================================================|
```
The file `z_mumu.lhe` contains 100 e<sup>+</sup>e<sup>-</sup> &#8594; mu<sup>+</sup>mu<sup>-</sup>(gamma) events in LHEF 3.0 format .


###  MadGraph5

MadGraph5 is available as standalone program:

```bash
which mg5_aMC
```

```
/cvmfs/fcc.cern.ch/sw/views/releases/fccsw/0.13/LCG_97a_FCC_2/x86_64-centos7-gcc8-opt/bin/mg5_aMC
```


###  Herwig

Herwig is available as standalone program:

```bash
which Herwig
```

```
/cvmfs/fcc.cern.ch/sw/views/releases/fccsw/0.13/LCG_97a_FCC_2/x86_64-centos7-gcc8-opt/bin/Herwig
```

## Getting started with Delphes

In this tutorial, you will learn how to:

-   generate events with Pythia8, process them through Delphes with
    FCCSW and write them in the FCC EDM format.
-   read these events with RDataFrame to perfom basic selection and create an
    ntuple
-   read this ntuple with ROOT to make a few plots

### Run FCCSW with Pythia8+Delphes (FCC-hh)

Now you are ready to produce 100TeV ttbar events with Pythia, process them through Delphes and store them in the FCC-EDM:

```bash
fccrun FCCSW/Sim/SimDelphesInterface/options/PythiaDelphes_config.py --Filename FCCSW/Generation/data/Pythia_ttbar.cmd --DelphesCard FCCSW/Sim/SimDelphesInterface/data/FCChh_DelphesCard_Baseline_v01.tcl
```

you should obtain a file called `FCCDelphesOutput.root`.

Please ignore errors such as

```
Error in <TTree::Bronch>: Cannot find dictionary for class: HepMC::GenEvent
```

or

```
Error in <TList::Clear>: A list is accessing an object (0x35308a0) already deleted (list name = Browsables)
```

This example will run 100 events by default. To have more events for plotting purposes, you can increase this number or use files that have been already produced and stored on eos (see next section).


### Run FCCSW with Pythia8+Delphes (FCC-ee)

Let us now produce FCC-ee event with the IDEA delphes card. For that we use a different FCC configuration file than FCC-hh and a different detector parametrisation in Delphes.

```bash
fccrun  /eos/experiment/fcc/ee/utils/config/PythiaDelphes_config_v01.py --DelphesCard /eos/experiment/fcc/ee/utils/delphescards/fcc_v01/card.tcl --Filename FCCSW/Generation/data/ee_Z_ddbar.cmd --filename events.root -n 1000
```

### Run dataframe (FCC-ee)

Clone the repository and go in it

```bash
git clone https://github.com/HEP-FCC/FCCAnalyses.git
cd FCCAnalyses
```

Follow the installation instruction for dataframe in FCCAnalyses

```bash
source setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

then run the template analysis

```bash
python FCCeeAnalyses/Z_Zqq/dataframe/analysis.py  PATHTOTHEFILEPRODUCEBEFORE/events.root
```

