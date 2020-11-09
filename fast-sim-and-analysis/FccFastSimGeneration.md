FCC: Getting started with event generation
===================================================================================


## Overview


## Enabling FCCSW

* To configure your environment for the FCC software, just do:

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

for the Spack installed version or

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup-lcg.sh
```

for the LCG stack installed version.
While the version should be equivalent in most of the aspects, some packages may be available only 
in one of the builds. This ill be highlighted when relevant.

Builds exist on CernVM-FS for CentOS7 (this is the system run on `lxplus`) using gcc8. LCG buils exist also
for Ubuntu 20.04 LTS.

The `fccrun` steering application should be available at this point:

```bash
which fccrun
```

```
# the output might differ, but shouldn't be empty
/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/fccsw-develop-q57ahua7lm65fvxnzekozih4mgvzptlx/scripts/fccrun
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
/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/whizard-2.8.4-nxnm6ntaaduopm5ff22xr6p35r23euz6/bin/whizard
```

Whizard is run as this:

```bash
whizard <process_config>.sin
```

Example of process configuration files are found under

``` bash
ls /cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/whizard-2.8.4-nxnm6ntaaduopm5ff22xr6p35r23euz6/share/whizard/examples/
```
or at `https://gitlab.tp.nt.uni-siegen.de/whizard/public/-/tree/master/share/examples` .

Some examples more specific to FCC can be found under

```bash
ls /eos/project-f/fccsw-web/www/share/gen/whizard/
```
or browsing `https://fccsw.web.cern.ch/fccsw/share/gen/whizard/Zpole/`, if EOS is not available.

It is advised to work in a separate directory for each process. For example, for Z_mumu, we have:

```bash
 mkdir test_whizard/Z_mumu; cd test_whizard/Z_mumu
 wget https://fccsw.web.cern.ch/fccsw/share/gen/whizard/Zpole/Z_mumu.sin
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

###  KKMCee

`KKMCee` is an adaptation of the `KKMC` Monte Carlo generator (the latest version of the `Koral` generetors) to the
case of FCC-ee. 
KKMCee is available as standalone program when using the `LCG` installaton of FCCSW version 0.15 or higher:

```bash
which KKMCee
```

```
/cvmfs/sft.cern.ch/lcg/views/LCG_97a_FCC_4/x86_64-centos7-gcc8-opt/bin/KKMCee
```
An help function is available

```bash
KKMCee -h

+++ Wrapper around the KKMCee/ProdMC.exe executable +++

Usage: \tKKMCee -f Mu|Tau|Hadrons -e Ecms -n Nevts -o output_file [-s seed_file] [OPTIONS]
       \tKKMCee -c config_file [-s seed_file]

Options:
  -c, --config file 		Path to configuration file
  -f, --flavour flavour 	Flavour to be generated (Mu|Tau|Hadrons)
  -e, --ecms energy 		Center of Mass energy in GeV
  -n, --nevts energy 		Number of events to be generated
  -o, --outfile file 		File with the generated events in LHE format
  -s, --seedfile file 		File to be used for seeding (randomly generated, if missing)

Examples:
KKMCee -f Mu -e 91.2 -n 10000 -o kkmu_10000.LHE
KKMCee -c kkmc_ditau.input
```

Configuration example files are available under

```bash
$ ls /cvmfs/sft.cern.ch/lcg/views/LCG_97a_FCC_4/x86_64-centos7-gcc8-opt/share/KKMCee/examples/
Beast.input  Bottom.input  Down.input  Inclusive.input  Mu.input  Tau.input  Up.input
```

To generate a sample of dimuon events using the example files, do the following

```bash
KKMCee -c /cvmfs/sft.cern.ch/lcg/views/LCG_97a_FCC_4/x86_64-centos7-gcc8-opt/share/KKMCee/examples/Mu.input
```
The out should somethign like this

```bash
Seeds: 29318493 48191772
  29318493      IJKLIN= 29318493  48191772
         0      NTOTIN= 0
         0      NTOT2N= 0
  ------- starting from the scratch ----------
ranmar initialized: ij,kl,ijkl,ntot,ntot2=       974     18625  29318493         0         0
        1000  requested events
 ---------------
 ****************************
 *    KK2f_ReaDataX Starts  *
 ****************************
 ---------------
 ---------------
 ---------------
 ---------------
 ---------------
BeginX
********************************************************************************
*               ACTUAL DATA FOR THIS PARTICULAR RUN
********************************************************************************
*indx_____data______ccccccccc0ccccccccc0ccccccccc0ccccccccc0ccccccccc0ccccccccc0
*     Center-of-mass energy [GeV]
    1    91.0000         CMSene =xpar( 1) Average Center of mass energy [GeV]
********************************************************************************
*     Define process
  413    1.00000          KFfin, muon
  100    1.00000          store lhe file to (LHE_OUT.LHE)
 ---------------          26          36 LHE_OUT.LHE
************************* one can change the lhf file name between brackets
********************************************************************************
EndX
 **************************
 *   KK2f_ReaDataX Ends   *
 **************************
 Tables are READ from DiskFile  dizet/table.down
amz,amh,amtop,swsq,gammz,amw,gammw=
     =  91.1876000 125.1000000 173.0000000   0.2234020   2.4953766  80.3588894   2.0898788
 
 ...
 
 

                            Event listing (summary)

    I particle/jet KS     KF  orig    p_x      p_y      p_z       E        m

    1 !e-!         21      11    0    0.000    0.000   45.500   45.500    0.001
    2 !e+!         21     -11    0    0.000    0.000  -45.500   45.500    0.001
    3 (Z0)         11      23    1    0.039    0.001    0.115   90.879   90.879
    4 gamma         1      22    1    0.000    0.000   -0.001    0.001    0.000
    5 gamma         1      22    1   -0.039   -0.001   -0.114    0.120    0.000
    6 mu-           1      13    3   14.678    0.229   43.067   45.500    0.106
    7 mu+           1     -13    3  -14.639   -0.229  -42.952   45.379    0.106
                   sum:  0.00         0.000    0.000    0.000   91.000   91.000
 iev=          501
  generation finished
  xSecPb, xErrPb =   1442.5021729176829        13.903134156944603
++++++++++++++++++++++++++++++++++++++++++++++++++++++
++    GLK_PRINT: bmin.eq.bmax, id=     50004 ++
++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++
++    GLK_PRINT: bmin.eq.bmax, id=     50005 ++
++++++++++++++++++++++++++++++++++++++++++++++++++++++

real	0m4.043s
user	0m3.777s
sys	0m0.085s
```

and a file `LHE_OUT.LHE` created.

The same can be obtained on the command line:

```bash
KKMCee -f Mu -e 91.2 -n 1000 -o LHE_OUT_1.LHE
```

