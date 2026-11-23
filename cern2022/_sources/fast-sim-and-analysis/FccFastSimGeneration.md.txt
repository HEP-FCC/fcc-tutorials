FCC: Getting started with event generation
===================================================================================


## Overview


## Enabling FCCSW

* To configure your environment for the FCC software, just do:

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```
:::{admonition} Nota Bene
:class: callout

For legacy reasons the following is still provided, fully equivalent to the above
```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```
:::

Builds exist on CernVM-FS for CentOS7 (this is the Operating System run on `lxplus`) using gcc11.

The `k4run` steering application should be available at this point:

```bash
which k4run
```

```
# The output might differ, but shouldn't be empty and the structure should be similar
/cvmfs/sw.hsf.org/spackages6/k4fwcore/1.0pre15/x86_64-centos7-gcc11.2.0-opt/2q37t/bin/k4run
```
The application `fccrun` is still provided, fully equivalent to `k4run`.

:::{admonition} Nota Bene
:class: callout

You will need to source the `/cvmfs/sw.hsf.org/key4hep/setup.sh` script everytime you want to use the software.
:::


## Generators

### Overview

The physics generators available for FCC typically come from the underlying stack. However, any generator
able to generate events in one of the understood formats, e.g. HepMC or EDM4hep or LHEf, can be used in standalone.
The recommended formats are `HepMC3` and `EDM4hep`.
This pages intend to illustrate the use of a few general purpose generators available when enabling FCCSW:
pythia8, whizard, MadGraph5, Herwig, KKMCee, BHLUMI, BabaYaga.

###  Pythia8

Pythia8 is fully intergrated in `Key4hep` software stack and it provides diverse functionality in addition to event generation,
including capability to read events in LHEF format.

To use Pythia8 we need a Gaudi steering file and a configuration file. Examples of configuration files can be obtained from the [FCC-config](https://github.com/HEP-FCC/FCC-config/tree/main/FCCee/Generator/Pythia8) repository.

The Gaudi steering file needs to activate the `GaudiAlgorithm` that runs Pythia8; the algorithm is available from the `k4Gen` repository and it is called [PythiaInterface](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/PythiaInterface.h).

An example of steering file can be found at [https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/options/pythia.py](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/options/pythia.py). The steering file runs the miniaml set of algorithms to run Pythia8 and produce an output in `EDM4hep` format:
```
$ wget https://raw.githubusercontent.com/HEP-FCC/k4Gen/main/k4Gen/options/pythia.py
$ k4run pythia.py -h
 -->  Pythia8 -->  HepMCToEDMConverter -->  StableParticles -->  out
...
  -n NUM_EVENTS, --num-events NUM_EVENTS
                        Number of events to run
...
  --out.filename [OUT.FILENAME], --filename.out [OUT.FILENAME]
                        Name of the file to create [PodioOutput]
...
  --Pythia8.PythiaInterface.pythiacard [PYTHIA8.PYTHIAINTERFACE.PYTHIACARD], --pythiacard.Pythia8.PythiaInterface [PYTHIA8.PYTHIAINTERFACE.PYTHIACARD]
                        [PythiaInterface]
...

```
For example, to generate 500  e<sup>+</sup>e<sup>-</sup> &#8594; mu<sup>+</sup>mu<sup>-</sup> at 91.2 GeV, we can do the following: download the configuration file:
```
$ wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_Zmumu_ecm91.cmd
```
and run
```
k4run pythia.py -n 500 --out.filename p8_mumu_500.e4h.root --Pythia8.PythiaInterface.pythiacard p8_ee_Zmumu_ecm91.cmd
```

###  Whizard

Whizard is available as standalone program:

```bash
which whizard
```

```
/cvmfs/sw.hsf.org/spackages6/whizard/3.0.1/x86_64-centos7-gcc11.2.0-opt/pmm4s/bin/whizard
```

Whizard is run as this:

```
whizard <process_config>.sin
```

Example of process configuration files are found under

``` bash
ls /cvmfs/sw.hsf.org/spackages6/whizard/3.0.1/x86_64-centos7-gcc11.2.0-opt/pmm4s/share/whizard/examples/
```
or at `https://gitlab.tp.nt.uni-siegen.de/whizard/public/-/tree/master/share/examples` .

Some examples more specific to FCC can be found under

```
ls /eos/project-f/fccsw-web/www/share/gen/whizard/
```
or browsing `https://fccsw.web.cern.ch/fccsw/share/gen/whizard/Zpole/`, if EOS is not available.


:::{admonition} Show dimuon example
:class: toggle

It is advised to work in a separate directory for each process. For example, for Z_mumu, we have:

```bash
 mkdir -p test_whizard/Z_mumu; cd test_whizard/Z_mumu
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
|                               WHIZARD 3.0.1
|=============================================================================|
| Reading model file '/cvmfs/sw.hsf.org/spackages6/whizard/3.0.1/x86_64-centos7-gcc11.2.0-opt/pmm4s/share/whizard/models/SM.mdl'
| Preloaded model: SM
| Process library 'default_lib': initialized
| Preloaded library: default_lib
| Reading model file '/cvmfs/sw.hsf.org/spackages6/whizard/3.0.1/x86_64-centos7-gcc11.2.0-opt/pmm4s/share/whizard/models/SM_hadrons.mdl'
| Reading commands from file 'Z_mumu.sin'
| Switching to model 'SM', scheme 'default'

...

$description = "A WHIZARD 3.0 Example.
   Z -> mumu @ 91.2 events for FCC ee."
$y_label = "$N_{\textrm{events}}$"
$sample = "z_mumu"
| Starting simulation for process 'zmumu'
| Simulate: using integration grids from file 'zmumu.m1.vg'
| RNG: Initializing TAO random-number generator
| RNG: Setting seed for random-number generator to 22345
| Simulation: requested number of events = 1000
|             corr. to luminosity [fb-1] =   6.6285E-04
| Events: writing to HepMC file 'z_mumu.hepmc'
| Events: writing to raw file 'z_mumu.evx'
| Events: generating 1000 unweighted, unpolarized events ...
| Events: event normalization mode '1'
|         ... event sample complete.
| Events: actual unweighting efficiency =   1.16 %
Warning: Encountered events with excess weight: 6 events (  0.600 %)
| Maximum excess weight = 2.465E+00
| Average excess weight = 4.511E-03
| Events: closing HepMC file 'z_mumu.hepmc'
| Events: closing raw file 'z_mumu.evx'
| There were no errors and    2 warning(s).
| WHIZARD run finished.
|=============================================================================|
```

:::

The file `z_mumu.hepmc` contains 100 e<sup>+</sup>e<sup>-</sup> &#8594; mu<sup>+</sup>mu<sup>-</sup>(gamma) events in HepMC 3 format .


###  MadGraph5

MadGraph5 is available as standalone program:

```bash
which mg5_aMC
```

```
/cvmfs/sw.hsf.org/spackages6/madgraph5amc/2.8.1/x86_64-centos7-gcc11.2.0-opt/3tclk/bin/mg5_aMC
```


###  Herwig

Herwig is available as standalone program:

```
which Herwig
```

```
/cvmfs/sw.hsf.org/spackages6/herwig3/7.2.3/x86_64-centos7-gcc11.2.0-opt/5d2cb/bin/Herwig
```

###  KKMCee

`KKMCee` is an adaptation of the `KKMC` Monte Carlo generator (the latest version of the `Koral` generators) to the
case of FCC-ee. 
KKMCee is available as standalone program when using the key4hep stack:

```bash
which KKMCee
```

```
/cvmfs/sw.hsf.org/spackages6/kkmcee/5.00.02/x86_64-centos7-gcc11.2.0-opt/eodg6/bin/KKMCee
```

A help function is available:

```
KKMCee -h
```

:::{admonition} Show help function output
:class: toggle

```
+++ Wrapper around the KKMCee executable  +++

Usage: \tKKMCee -f Mu|Tau|UDS|C|B|Hadrons -e Ecms -n Nevts -o output_file [-s initial_seed] [OPTIONS]
       \tKKMCee -c config_file [-s initial_seed]

Options:
  -c, --config file 		Path to configuration file
  -f, --flavour flavour 	Flavour to be generated (Mu|Tau|UDS|C|B|Hadrons)
  -e, --ecms energy 		Center of Mass energy in GeV
  -n, --nevts events 		Number of events to be generated
  -o, --outfile file 		File with the generated events in HEPMCv3 format [kkmcee.hepmc]
  -s, --initialseed 		Long number to be used for initial seeding (randomly generated, if missing)
  -b, --bessig bessig 		Beam-Energy-Spread of both beams (or of the first beam, if bessig2<0.)
                      		[fraction of Ecms/2, default -1. (no spread)]
  -g, --bessig2 bessig2 	Beam-Energy-Spread of the second beam if different from the first beam; fraction of Ecms/2.
                      		[fraction of Ecms/2, default -1. (no spread or equal to first beam)]
  -r, --besrho rho 		Beam-Energy-Spread correlation [default 0.]
  -d, --debug lvl 		 PrintOut Level 0,1,2 [default 1]

Special options for taus only:
  -t, --taudec t1*1000+t2 	decay channel for the first (t1) and second tau (t2)
                      		 0        Inclusive
                      		 1,2,3    electron,mu,pi
                      		 4,5,6,7  rho,a1,K,K*
                      		 8,9,10,11,12,13  3pip0,pi3pi0,3pi2pi0,5pi,5pip0,3pi3p0
                      		 14, ... (other rare decays see tauola++)
  --tauopt file 		File with tau options (see Tauola section in KKMCee_defaults)
                      		 the file is included as it is and overwrites other settings

Examples:
KKMCee -f Mu -e 91.2 -n 10000 -o kkmu_10000.hepmc -b 0.001
KKMCee -c kkmc_ditau.input
KKMCee -f B -e 91.2 -n 1000 -o kkbb_1000.hepmc

  NB: (1) This wrapper works only for KKMCee versions 5 or newer
      (2) Output is HEPMC v3
```

:::

Note that the BES (Beam Energy Spread) options are only available in version 4.32.01 and higher.

A configuration example file for taus is available under at

```
ls `dirname $( which KKMCee )`/../share/KKMCee/examples/kkmc-tauola.input
```

:::{admonition} Show dimuon example
:class: toggle

To generate a sample of dimuon events using the example files, do the following

```bash
KKMCee -f Mu -e 91.2 -n 1000 -o kkmu_1000.hepmc
```

The output should look something like this:

```
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

:::

and a file `kkmu_1000.hepmc` created.

`KKMCee` creates several files during its run. These are saved into a folder called `KKMCee-<date>-<time>`, for example `KKMCee-12Oct2022-191047`.
This folder contains the files:
```
$ ls KKMCee-12Oct2022-191047
DIZET-table1  TabMain77.output  TabMainC.output  mcgen.root  pro.input  pro.output  pro77.output
```
The file `pro.input` contains the configuration options and can be used to repeat the run
```bash
KKMCee -c KKMCee-12Oct2022-191047/pro.input
```
and, of course, as base configuration file example for further variations.

###  BHLUMI

`BHLUMI` is a Monte Carlo generator of Bhabha events used at LEP for luminosity studies.
BHLUMI is available as standalone program when using the key4hep stack:

```bash
which BHLUMI
```
```
/cvmfs/sw.hsf.org/spackages4/bhlumi/4.04-linuxLHE/x86_64-centos7-gcc8.3.0-opt/o7rmcus/bin/BHLUMI
```
A help function is available:

```
BHLUMI -h
```

:::{admonition} Show help function output
:class: toggle

```
+++ Wrapper around the BHLUMI.exe executable +++

Usage: 	BHLUMI -e Ecms -n Nevts -f Thmin -t Thmax -x epscms -o output_file [-s seed_file]
       	BHLUMI -c config_file [-s seed_file]

Switches:
  -c, --config file 		Path to configuration file
  -e, --ecms energy 		Center of Mass energy in GeV
  -n, --nevts energy 		Number of events to be generated
  -f, --Thmin theta 		Minimum theta [rad]
  -t, --Thmax theta 		Maximum theta [rad]
  -x, --epscms fraction 	Energy cut-off in  fraction of Ecms
  -o, --outfile file 		File with the generated events in LHE format
  -s, --seedfile file 		File to be used for seeding (randomly generated, if missing)

Examples:
BHLUMI -f 0.022 -t 0.082 -x 0.001 -e 91.2 -n 10000 -o kkmu_10000.LHE
BHLUMI -c bhlumi.input

Additional switches (for experts only):
  -k, --keyopt KEYOPT 		Technical parameters switch [default 3021]
  				KEYOPT = 1000*KEYGEN + 100*KEYREM + 10*KEYWGT + KEYRND
  -r, --keyrad KEYRAD 		Physics parameters switch [default 1021]
  				KEYRAD = 1000*KEYZET + 100*KEYUPD + 10*KEYMOD + KEYPIA
  (Contact BHLUMI authors for details, e.g. through https://github.com/KrakowHEPSoft/BHLUMI)
```

:::

###  BabaYaga

`BabaYaga` is a Monte Carlo generator of two-photons events used at LEP.
BabaYaga is available as standalone program when using the key4hep stack:

```bash
which babayaga
```
```
/cvmfs/sw.hsf.org/spackages4/babayaga/fcc-1.0.0/x86_64-centos7-gcc8.3.0-opt/jsgdir7/bin/babayaga
```
A help function is available:

```
babayaga -h
```

:::{admonition} Show help function output
:class: toggle

```

+++ Wrapper around the babayaga-fcc.exe executable +++

+++ Process: e+e- -> gamma gamma

Usage: 	babayaga -e Ecms -n Nevts -f Thmin -t Thmax -x epscms -o output_file [-s seed]
       	babayaga -c config_file [-s seed]

Switches:
  -c, --config file 		Path to configuration file
  -e, --ecms energy 		Center of Mass energy in GeV
  -n, --nevts energy 		Number of events to be generated
  -f, --Thmin angle 		Minimum theta [deg]
  -t, --Thmax angle 		Maximum theta [deg]
  -a, --acolmax angle 		Max acollinearity [deg]
  -m, --emin energy 		Min energy in GeV
  -x, --eps fraction 		Soft-photon cut-off
  -o, --outfile file 		File with the generated events in LHE format
  -w, --outdir path 		Path with working space (and residual files)
  -s, --seed number 		Number used for seeding (randomly generated, if missing)
  -d, --debug number 		Debug level (0, 1, 2, ...)

Examples:
babayaga -f 15. -t 165. -e 91.2 -n 10000 -o bbyg_10000.LHE
babayaga -c babayaga.input -o bbyg.LHE

```

:::

## Hands-on case study: ditau events with KKMCee, Pythia8 and Whizard

In this section we describe, with exercises, the generation of an equivalent sample of Monte Carlo events with three diffent generators,
`KKMCee`, `Pythia8` and `Whizard`. The process chosen is e<sup>-</sup>e<sup>+</sup> &rarr; tau<sup>-</sup>tau<sup>+</sup> (hereafter referred to as _ditaus_) at a centre of mass energy of 91.2 GeV. In the three cases 10000 will be generated and saved in `ROOT` files in `EDM4hep` format.

### Generating ditaus with KKMCee
As shown in the [KKMCee section](#kkmcee), event generation with the `KKMCee` is controlled through a configuration file. The interface available in `key4hep` allowed a generation of the configuration file through command line switches. Starting from the command line switches is therefore always a good option when no confguration file is available.

Currently, `KKMCee` does not have the option to save directly the events in `EDM4hep` format. In order to get there we need first to generate the events in `HepMC` format.

#### Generating `HepMC` events

What are the commands (options) to generate 10000 ditau events and saved them into the file kk_tautau_10000.hepmc ? 

:::{admonition} Suggested answer
:class: toggle

```bash
KKMCee -f Tau -e 91.2 -n 10000 -o kk_tautau_10000.hepmc
```

:::

:::{admonition} Expand to see the example of the produced `HepMC` output 
:class: toggle

The `HepMC` output is an ASCII format and can browsed with for example `more`:

```bash
$ more kk_tautau_10000.hepmc
HepMC::Version 3.02.04
HepMC::Asciiv3-START_EVENT_LISTING
E 0 4 11
U GEV MM
A 4 spin 0.056005 -0.954208 0.293856
A 5 spin 0.862823 0.105210 0.494436
P 1 0 11 0.0000000000000000e+00 0.0000000000000000e+00 4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 2 0 -11 0.0000000000000000e+00 0.0000000000000000e+00 -4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
V -1 0 [1,2]
P 3 -1 23 0.0000000000000000e+00 0.0000000000000000e+00 0.0000000000000000e+00 9.1200000000000003e+01 9.1200000000000003e+01 2
P 4 3 15 7.5634198134957833e+00 1.9208578260382165e+01 -4.0620528002933362e+01 4.5600000000000001e+01 1.7770499999998681e+00 2
P 5 3 -15 -7.5634198134957833e+00 -1.9208578260382165e+01 4.0620528002933362e+01 4.5600000000000001e+01 1.7770499999998681e+00 2
P 6 4 16 1.5520648658275604e-01 1.3736795186996460e+00 -3.0399644374847412e+00 3.3395311832427979e+00 0.0000000000000000e+00 1
P 7 4 13 3.3498418331146240e+00 7.8049712181091309e+00 -1.7384153366088867e+01 1.9348358154296875e+01 1.0565830000000000e-01 1
P 8 4 -14 4.0583715438842773e+00 1.0029928207397461e+01 -2.0196411132812500e+01 2.2912111282348633e+01 0.0000000000000000e+00 1
P 9 5 -16 -3.4257166385650635e+00 -9.4930477142333984e+00 2.1268466949462891e+01 2.3541477203369141e+01 0.0000000000000000e+00 1
P 10 5 211 -9.6522146463394165e-01 -2.8242239952087402e+00 5.9299035072326660e+00 6.6401152610778809e+00 1.3957587329547499e-01 1
P 11 5 111 -3.1724817752838135e+00 -6.8913059234619141e+00 1.3422157287597656e+01 1.5418406486511230e+01 1.3496067957561880e-01 1
E 0 7 22
U GEV MM
A 10 spin -0.526312 -0.653062 0.544523
A 11 spin 0.124883 0.876618 -0.464700
P 1 0 -11 0.0000000000000000e+00 0.0000000000000000e+00 -4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 2 1 -11 2.3989162307273351e-04 3.2683144961857383e-05 -4.5053509135514268e+01 4.5053509084747823e+01 -2.1524472631665264e-03 2
P 3 1 22 -2.3989162307273351e-04 -3.2683144961857383e-05 -5.4649086162257743e-01 5.4649091525218030e-01 -1.2904784139758924e-08 1
P 4 0 11 0.0000000000000000e+00 0.0000000000000000e+00 4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 5 4 11 -3.4272383325468539e-06 3.9756556219599252e-05 4.5471392649338441e+01 4.5471392646010933e+01 -5.5154828810563322e-04 2
P 6 4 22 3.4272383325468539e-06 -3.9756556219599252e-05 1.2860734779840696e-01 1.2860735398907067e-01 -3.2261960349397309e-09 1
P 7 2 -11 2.3978439291629699e-04 3.1121498922239849e-05 -4.4998932825148202e+01 4.4998932774359304e+01 -2.1515941974735880e-03 2
P 8 2 22 1.0723015643652809e-07 1.5616460396175375e-06 -5.4576310366068984e-02 5.4576310388516784e-02 -6.5854450798271929e-10 1
V -4 0 [5,7]
P 9 -4 23 2.3635715458375012e-04 7.0878055141839101e-05 4.7245982419023846e-01 9.0470325420370244e+01 9.0469091756916228e+01 2
P 10 9 15 -1.0567709246763060e+01 -4.0260638458492809e-01 4.4181853045814989e+01 4.5464630383293809e+01 1.7770500000003799e+00 2
P 11 9 -15 1.0567945603917645e+01 4.0267726264006992e-01 -4.3709393221624751e+01 4.5005695037076428e+01 1.7770500000001239e+00 2
P 12 10 16 -4.2494945526123047e+00 5.3450322151184082e-01 1.7407199859619141e+01 1.7926362991333008e+01 0.0000000000000000e+00 1
P 13 10 -211 -3.2984399795532227e+00 -2.7310401201248169e-01 1.5218788146972656e+01 1.5575150489807129e+01 1.3967110514153336e-01 1
P 14 10 111 -3.0197749137878418e+00 -6.6400557756423950e-01 1.1555866241455078e+01 1.1963118553161621e+01 1.3497032866486386e-01 1
P 15 11 -16 1.3823601500654497e+00 5.8997208178366942e-02 -6.8109338674845024e+00 6.9500518568222240e+00 0.0000000000000000e+00 1
P 16 11 211 1.1306452151024036e+00 9.9405550031272910e-02 -3.6136840095621445e+00 3.7903071607421510e+00 1.3955710658047393e-01 1
P 17 11 211 2.9148939828773184e+00 3.3597977559671632e-01 -1.0436451119833281e+01 1.0841977637941852e+01 1.3956283150401572e-01 1
P 18 11 -211 3.4269614119923486e+00 6.2251535093063998e-02 -1.5263612213083412e+01 1.5644337452123484e+01 1.3963076888122616e-01 1
P 19 11 111 1.5460559488251355e+00 -1.1916317312948667e-01 -6.7685473667467502e+00 6.9452098898073880e+00 1.3497443778768972e-01 1
P 20 11 22 1.3380509514620450e-04 -1.0323115492598167e-05 -3.8742519765868233e-04 4.1001055350006228e-04 0.0000000000000000e+00 1
P 21 11 22 6.4753176789756372e-05 3.6976379858981743e-06 -2.6864524513974572e-04 2.7636373526067825e-04 0.0000000000000000e+00 1
P 22 11 22 1.6683033237367961e-01 -3.4786968976788998e-02 -8.1550790025724251e-01 8.3312401741426301e-01 0.0000000000000000e+00 1
...
```
The detailed description of the ASCII `HepMC` output can be found in Section 3.4 of [HepMC3 writeup](https://arxiv.org/abs/1912.08005).
The first two line indicate the version of `HepMC` (here 3.02.04) and the type of output, i.e. `Asciiv3` (`HepMC` supports also binary formats as output).
The block for each event starts with a line `E`, indicating the event number, the number of vertices and the number of particles. The line staring with `U` gives the adopted units for energy and distances. The lines starting with `P` are the particle lines: the first integer is the particle number in the list, the second the particle number of the parent particle, the third the `PDG` particle ID, then we have the 3-momentum, the nergy and the mass; finally the status, with `status==1` labelling _stable_ particles entering leaving the interaction point and entering the detector. The lines starting with `A` indicate additional attributes: the can be per run, per event or per element of the listing. In this case they are used to provide helicity information for the two taus: the first number is the particle number, the second the name of the attribute, the rest the helicity information.  

Q: What can be conidered _strange_ in the above listing ? 

:::{admonition} Suggested answer
:class: toggle

A close-up look at the listing rasing two questions 
    1. The number of the second event is still 0. This is due to a bug in the `HepMC` interface of `KKMCee`; it has no influence
       in the following processing, since not really used.
    2. The number of vertices does not seem to correspond to what found in the listing. The number of vertices, for example 4 in the first listing, correponds to the collision plus the decays one: the collision one is indicated by `V`, the other 3 are not indicated explicitely, but can be infered by looking at the particles having the same non-null parent ID: the decays of the Z boson (PDG id = 23), of Tau- (  

:::

The remaining output files from the run are found in the `KKMCee-<date>-<time>` directory. In particular the file `pro.output` contains at the end information about the process cross-section. 

In this example 
```
$ tail -37 KKMCee-<date>-<time>/pro.output
   *****************************
   ****   KKMCee   Finalize ****
   *****************************
********************************************************************************
*                                                                              *
*                   ****************************************                   *
*                   ******      KKMCee::Finalize      ******                   *
*                   ****************************************                   *
*   f_NevGen =      10000 =                          No. of generated events   *
*   XsPrimPb =       2700.8373   =                   Primary from Foam [pb]    *
*  FoamInteg =       1713.9085   =                   Crude from FOAM   [pb]    *
*         +- =    0.0015374453   =                   error                     *
*                   ****************************************                   *
*   <WtMain> =       0.5480549   =                   average WtMain            *
*         +- =    0.0014250983   =                   error abs.                *
*     XsMain =       1480.2071   =                   Xsection main [pb]        *
*         +- =    0.0070229434   =                   error absolute            *
*         +- =    0.0026002838   =                   error relative            *
*                   ********** More from WtMainMonit *******                   *
*      AveWt =       0.5480549   =                   average <WtMain>          *
*      ERela =    0.0026002838   =                   relative error            *
*      sigma =      0.38497968   =                   dispersion of WtMain      *
*   DB_WTmax =               4   =                   input WTmax               *
*      WtMax =       4.2012103   =                   maximum  WTmain           *
*      WtMin =               0   =                   mainimum WTmain           *
*      AvUnd =               0   =                   underflow                 *
*      AvOve =   5.5091102e-06   =                   overflow                  *
* AvOve/<Wt> =   1.0052114e-05   =                   relative: AvOve/AveWt     *
*       Ntot =           72977   =                   Ntot primary events       *
*       Nacc =           10000   =                   accepted events           *
*  Nacc/Ntot =      0.13702948   =                   acceptance rate           *
*       Nneg =               0   =                   WT<0 events               *
*       Nove =               2   =                   WT>WTmax events           *
*  Nove/Ntot =   2.7405895e-05   =                   Nove/Ntot                 *
*       Nzer =            1201   =                   WT=0 events               *
*                                                                              *
********************************************************************************
```
i.e the total ditau cross-section at 91.2 GeV from `KKMCee` is 1480.2 +- 7.0 pb . 

#### `HepMC` to `EDM4hep` conversion

In order to get the events in `EDM4hep` format, we will use `Gaudi` and the tools available in [k4FWCore](https://github.com/key4hep/k4FWCore) and [k4Gen](https://github.com/HEP-FCC/k4Gen/). We need a Gaudi steering file that reads the `HepMC` file and writes out the `EDM4hep` file.
A minimal version of such a steering code is available on the tutorial reference page:
```
wget http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/hepmc2edm.py .
```
Let's see what it does: that is shown by the first line of the help function
```
$ k4run hepmc2edm.py -h
 -->  GenAlg  -->  HepMCToEDMConverter  -->  out
...
```

##### Dissection of `hepmc2edm.py`

:::{admonition} Expand
:class: toggle

The tool that we need is [HepMCFileReader](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/HepMCFileReader.h), which is a `GaudiTool`, not a `GaudiAlgorithm`, which is used as a signal provider (such as a Monte Carlo generator) within the [Generator Algorithm (GenAlg)](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/GenAlg.h). This is done in this part of the code:
```python
from Configurables import HepMCFileReader
hepmcreader = HepMCFileReader()

from Configurables import GenAlg
reader = GenAlg()
reader.SignalProvider = hepmcreader
reader.hepmc.Path = "hepmc"
ApplicationMgr().TopAlg += [reader]
```
Then we convert the event from `HepMC` to `EDM4hep` with the [HepMCToEDMConverter](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/HepMCToEDMConverter.h):
```
from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter()
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.GenParticles.Path = "GenParticles"
ApplicationMgr().TopAlg += [hepmc_converter]
```
Finally we write out the converted events into a file with the [PodioOutput](https://github.com/key4hep/k4FWCore/blob/master/k4FWCore/components/PodioOutput.h) algorithm:
```
from Configurables import PodioOutput
out = PodioOutput("out", filename = "hepmc2edm_output.root")
out.outputCommands = ["keep *"]
ApplicationMgr().TopAlg += [out]
```
:::

##### Running `hepmc2edm.py`

Among the `hepmc2edm` switches relevant for the purpose are those controling input an output files:
```
$ k4run hepmc2edm.py -h
...
  --GenAlg.HepMCFileReader.Filename [GENALG.HEPMCFILEREADER.FILENAME], --Filename.GenAlg.HepMCFileReader [GENALG.HEPMCFILEREADER.FILENAME]
                        Name of the HepMC file to read [HepMCFileReader]
...
  --out.filename [OUT.FILENAME], --filename.out [OUT.FILENAME]
                        Name of the file to create [PodioOutput]
...
```
We would like the output file to be called `kk_tautau_10000.e4h.root` . Which command should we use for that?

:::{admonition} Check answer
:class: toggle

```bash
k4run hepmc2edm.py -n 10000 --GenAlg.HepMCFileReader.Filename kk_tautau_10000.hepmc --out.filename kk_tautau_10000.e4h.root
```

:::

Q: Can you explain why we need to pass the `-n 10000` switch and how you could modify `hepmc2edm.py` to avoid that?

:::{admonition} Check answer
:class: toggle

Because `hepmc2edm.py` contains this piece of code:
```python
from Configurables import ApplicationMgr
ApplicationMgr(
               EvtSel='NONE',
               EvtMax=1,
               OutputLevel=INFO,
```
The setting `EvtMax=1` is overwritten by `-n <n_evts>`. To avoid this one could set `EvtMax=10000` inside `hepmc2edm.py` (try!)

:::

Note _en passant_ that the `EDM4hep` file is much smaller than the `HepMC` one:
```
$ ls -lt
total 43032
-rw-r--r-- 1 ganis vboxsf  3661630 Oct 18  2022 kk_tautau_10000.e4h.root
-rw-r--r-- 1 ganis vboxsf     1232 Oct 18  2022 hepmc2edm.py
drwxr-xr-x 1 ganis vboxsf      288 Oct 18 16:12 KKMCee-18Oct2022-161012
-rw-r--r-- 1 ganis vboxsf 19584017 Oct 18 16:12 kk_tautau_10000.hepmc
```

Q: Can you explain why?

:::{admonition} Check answer
:class: toggle

Because `kk_tautau_10000.e4h.root` is a `ROOT` file, which binary and compressed.

:::

### Generating ditaus with Pythia8

As explained in the dedicated [Pythia8 section](#pythia8), to use `Pythia8` we need a configuration file. To generate ditau events we will use the file
[p8_ee_Ztautau_ecm91.cmd](https://github.com/HEP-FCC/FCC-config/blob/main/FCCee/Generator/Pythia8/p8_ee_Ztautau_ecm91.cmd):
```
$ wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_Ztautau_ecm91.cmd
```
Q: How will we run it? (hint: check specific section)

:::{admonition} Answer
:class: toggle

```
k4run pythia.py -n 10000 --out.filename p8_tautau_10000.d4h.root --Pythia8.PythiaInterface.pythiacard p8_ee_Ztautau_ecm91.cmd
```

:::

Running will take a few minutes. Among the last lines of the output there should be the total cross-section for the process:
```
 *-------  PYTHIA Event and Cross Section Statistics  -------------------------------------------------------------*
 |                                                                                                                 |
 | Subprocess                                    Code |            Number of events       |      sigma +- delta    |
 |                                                    |       Tried   Selected   Accepted |     (estimated) (mb)   |
 |                                                    |                                   |                        |
 |-----------------------------------------------------------------------------------------------------------------|
 |                                                    |                                   |                        |
 | f fbar -> gamma*/Z0                            221 |      140682      10000      10000 |   1.458e-06  7.715e-09 |
 |                                                    |                                   |                        |
 | sum                                                |      140682      10000      10000 |   1.458e-06  7.715e-09 |
 |                                                                                                                 |
 *-------  End PYTHIA Event and Cross Section Statistics ----------------------------------------------------------*
```
i.e. 1458.0 +- 7.7 pb.

Q: How the cross-sections compare?

:::{admonition} Answer
:class: toggle

The differences of teh corss-section calculated by `KKMCee` and `Pythia8` is (1480.2 - 1458.0) pb = 22.2 pb ; the errors have a statistical and systematic component. Assuming half and half for statistical and systematics, and the systematics fully correlated, the error on the difference is about 8.5 pb, i.e. the two calculatons differ by 2.6 standard deviations. What would you check first?

:::


### Generating ditaus with Whizard

As explained in the dedicated [Whizard section](#whizard), to use `whizard` we need a `Sindarin` configuration file. To generate ditau events we will use the file
[Z_tautau.sin](http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/Z_tautau.sin):
```
$ wget http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/Z_tautau.sin
```
and run it in a dedicate directory to not pollute the working one withe the many files produced:
```
$ mkdir -p whizard/tautau; cd whizard/tautau;
$ whizard ../../Z_tautau.sin
```
The output created by `whizard` is `LHEf` (Les Houches Event format); this is because the curent build does not support writing `HepMC`; this may change in the future.

Exercise: look at produced `LHEf` file `z_tautau.lhe`: what di we notice?

:::{admonition} Answer
:class: toggle

The taus are not decayed. Investigate if a Sindarin option to decay taus exists.

:::

The first lines of the `LHEf` file give the total cross-section: 1502 +- 2 pb, which seems dfinetly higher than the othesr.

#### `LHEf` to `EDM4hep` conversion

In order to get the events in `EDM4hep` format, we eploit the fact that `Pythia` provides `LHEf` reader functionality. To activate that we will use `Gaudi` and special `.cmd` file the consider the input `LHEf` input file as a `Beam`. This special `.cmd` is called `Pythia_LHEinput.cmd` and it is available under the directory pointed by `$K4GEN`:
```
S cp -rp $K4GEN/Pythia_LHEinput.cmd
```
Please note the lines
```
! 4) Read-in Les Houches Event file - alternative beam and process selection.
Beams:frameType = 4                      ! read info from a LHEF
Beams:LHEF = Generation/data/events.lhe ! the LHEF to read from
```
This file needs to be edited to enter the exact locaton of the input file (it could also be a symlink to avoid always editng the file.

As steering we will use the file [lhe2edm.py](http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/lhe2edm.py) which run the following sequence:
```
$ wget http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/lhe2edm.py
$ k4run lhe2edm.py -h
 -->  Pythia8 -->  HepMCToEDMConverter -->  HepMCFileWriter -->  StableParticles -->  out
```
The `HepMCFileWriter` step is redundant and only serves at converting also in `HepMC` for controls.
The conversion is run by the usual comand:
```
$ k4run lhe2edm.py -n 10000 --out.filename wz_tautau_10000.e4h.root --HepMCFileWriter.Filename wz_tautau_10000.hepmc 
```

### Looking at the produced files: the MCParticle class

Despite being ROOT files, the `EDM4hep` files are not easily usable, beaue they contain information in EDM4hep classes.
A good practie is to use some helper function available in FCAnalyses to create `flat` ntuple, much more readable.

#### Creating flat ntuples with FCCAnalyses

To create flat ntuples using FCCAnalyses we need a `Python` script to be feed into the framework.
An example is available in [make_flat.py](http://fccsw.web.cern.ch/tutorials/october2020/tutorial1/make_flat.py).

You should have a lok and try to understand what it does. It adds a few event varialbe whihc would be useful to compare.

In order to run it with `FCCAnalyses` we have to call it like this:
```
fccanalysis run make_flat.py --test --output kk_tautau_10000.flat.root
```
and the same the other files.

Exercise: add a variable `invmass` with the invariant mass of the two taus.

:::{admonition} Hint
:class: toggle

Look at the the `scalarProdNorm`.

:::

#### Comparing distributions

This is the final exercise: write a `ROOT` macro, in `Python` or `C++`, to compare the global event variables `acol`, `n_charged`
and `cthetauminus`, and perhaps also `invmass`.

:::{admonition} Hint
:class: toggle

Look at the `ROOT` tutorials for `RDataFrame`, `TTree` and `Hist`.
:::

What can you say from the comparison?
