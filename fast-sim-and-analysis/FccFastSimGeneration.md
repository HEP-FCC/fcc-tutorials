FCC: Getting started with event generation
===================================================================================


## Overview


## Enabling FCCSW

The FCC software `FCCSW` is fully embedded in the `key4hep` software stack or ecosystem, which means that the components providing the framework and those FCC specific are all available in `key4hep`. To configure your environment for the FCC software is therefore sufficient to initialise `key4hep`:

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```
:::{admonition} Nota Bene
:class: callout

For legacy reasons the following is still provided, fully equivalent to the above
```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```
Note however that not all the `cvmfs` tier-1 centers replicate the `fcc.cern.ch`, so this may lead to slowdowns or even failures.
:::

Builds exist on CernVM-FS for `CentOS7` (this is the Operating System run on `lxplus`) using as compiler `Gcc 11` (currently gcc version `11.2.0`).

:::{admonition} Nota Bene
:class: callout

The combination of old `glibc` version available on `CentOS7` with the backward compatibility attributes of glibc makes the provided stack in principle working for newer OSes, such as `CentOS8`, `AlmaLinux9` or `Fedora37`. This in general holds, though less core aspects, such graphics, might still be OS specific.
:::

The `gaudimain` steering application here is called `k4run` which should be available at this point:

```bash
$ which k4run
/cvmfs/sw.hsf.org/spackages7/k4fwcore/1.0pre16/x86_64-centos7-gcc11.2.0-opt/tp4u6/bin/k4run
```
(The output might differ, but shouldn't be empty and the structure should be similar).

The application `fccrun` is still provided, fully equivalent to `k4run`.

:::{admonition} Nota Bene
:class: callout

You will need to source the `/cvmfs/sw.hsf.org/key4hep/setup.sh` script everytime you want to use the software.
:::


## Generators

### Overview

The physics generators available for FCC usually come from `key4hep`. However, any generator
able to generate events in one of the understood formats, e.g. HepMC or EDM4hep or LHEf, can be used in standalone.
Following the discussion at the [1st ECFA workshop on Generators](https://indico.cern.ch/event/1078675/), the recommended formats are `HepMC3` and `EDM4hep`; `LHEf` is still much in use though.
This pages intend to illustrate the use of a few general purpose generators available when enabling FCCSW:
pythia8, whizard, MadGraph5, Herwig, KKMCee, BHLUMI, BabaYaga.

###  Pythia8

Pythia8 is fully intergrated in `Key4hep` software stack and it provides diverse functionality in addition to event generation, including capability to read events in `LHEf` format.

To use Pythia8 we need a Gaudi steering file and a Pythia8 configuration file, usually having extension `.cmd`. Examples of these `.cmd` files are available from the [FCC-config](https://github.com/HEP-FCC/FCC-config/tree/main/FCCee/Generator/Pythia8) repository.

The Gaudi steering file needs to activate the `GaudiTool` that interfaces `Pythia8`, available from the `k4Gen` repository under the name [PythiaInterface](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/src/components/PythiaInterface.h).

An example of steering file can be found at [pythia.py](https://raw.githubusercontent.com/HEP-FCC/k4Gen/main/k4Gen/options/pythia.py). The steering file runs the minimal set of algorithms to run Pythia8 and produce an output in `EDM4hep` format:
```
$ wget https://raw.githubusercontent.com/HEP-FCC/k4Gen/main/k4Gen/options/pythia.py
$ k4run pythia.py -h | head -n 1
 -->  Pythia8 -->  HepMCToEDMConverter -->  StableParticles -->  out
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
$ which whizard
/cvmfs/sw.hsf.org/spackages6/whizard/3.0.3/x86_64-centos7-gcc11.2.0-opt/yy7yk/bin/whizard
```

Whizard is run as this:

```
whizard <process_config>.sin
```

Example of Sindarin configuration files are found under

``` bash
ls /cvmfs/sw.hsf.org/spackages6/whizard/3.0.3/x86_64-centos7-gcc11.2.0-opt/yy7yk/share/whizard/examples/
```
or at [https://gitlab.tp.nt.uni-siegen.de/whizard/public/-/tree/master/share/examples](https://gitlab.tp.nt.uni-siegen.de/whizard/public/-/tree/master/share/examples).

Some examples more specific to FCC can be found at [https://fccsw.web.cern.ch/fccsw/share/gen/whizard/Zpole/](https://fccsw.web.cern.ch/fccsw/share/gen/whizard/Zpole/)`.


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

:::{admonition} Nota Bene
:class: callout
Note that, due to a mangling issue internal to KKMCee, the channel numbering for decays channel with pions is not the one shown by the help function. The numbering follows the relative order found in the file pro77.output produced by a KKMMee run. In particular, the single pion channel is numbered 159.  
A next version will address this issue.
:::


:::{admonition} Show channel numbering
:class: toggle
```

  Most common decays

  #    Default BR                       Channel
   1   0.17865208                      TAU-  -->   E-
   2   0.17355204                      TAU-  -->  MU-
 159   0.11084167                      TAU-  --> PI-
  88   0.25375551                      TAU-  --> RHO- -> PI- PI0
  77   0.91783553E-01                  TAU-  --> PI0  PI0  PI-
   4   0.12619076E-01                  TAU-  --> 3PI0,        PI-
  78   0.91783553E-01                  TAU-  --> PI-  PI-  PI+
   3   0.43654263E-01                  TAU-  --> 2PI-,  PI+,  PI0
  35   0.50110305E-02                  TAU-  --> 2PI-, PI+, 2PI0 old
  56   0.78900479E-03                  TAU-  --> 3PI-, 2PI+,
  57   0.18300110E-03                  TAU-  --> 3PI-, 2PI+,  PI0
  58   0.25100150E-03                  TAU-  --> 2PI-,  PI+, 3PI0
 
  All decays

  #    Default BR                       Channel
   1   0.17865208                      TAU-  -->   E-
   2   0.17355204                      TAU-  -->  MU-
   3   0.43654263E-01                  TAU-  --> 2PI-,  PI+,  PI0
   4   0.12619076E-01                  TAU-  --> 3PI0,        PI-
   5    0.0000000                      TAU-  --> nu_e e- e- e+
   6    0.0000000                      TAU-  --> nu_mu mu- mu- mu+
   7    0.0000000                      TAU-  --> nu_e e- mu- mu+
   8    0.0000000                      TAU-  --> nu_mu mu- e- e+
   9    0.0000000                      TAU-  --> K- 3PI0
  10    0.0000000                      TAU-  --> 2PI0 ETA K-
  11    0.0000000                      TAU-  --> 2PI0 K0  PI-
  12    0.0000000                      TAU-  --> PI0  K0  ETA PI-
  13    0.0000000                      TAU-  --> PI0  PI- PI+ K-
  14    0.0000000                      TAU-  --> K0   PI- PI+ PI-
  15    0.0000000                      TAU-  --> 2PI0 ETA PI-
  16    0.0000000                      TAU-  --> K0 K0B ETA PI-
  17    0.0000000                      TAU-  --> K0 K0B PI0 PI-
  18    0.0000000                      TAU-  --> K0 K0B K0  PI-
  19    0.0000000                      TAU-  --> K0 PI0 PI0 K-
  20    0.0000000                      TAU-  --> K0 K0B PI0 K-
  21    0.0000000                      TAU-  --> PI0  K0  ETA K-
  22    0.0000000                      TAU-  --> PI-PI+PI-  ETA
  23    0.0000000                      TAU-  --> PI-K+ K-   PI0
  24    0.0000000                      TAU-  --> K- K+ K-   PI0
  25    0.0000000                      TAU-  --> K- K+ K-   K0
  26    0.0000000                      TAU-  --> K- PI+PI-  K0
  27    0.0000000                      TAU-  --> K- K+ PI-  K0
  28    0.0000000                      TAU-  --> PI-PI+PI-  OMEGA
  29    0.0000000                      reserved
  30    0.0000000                      reserved
  31    0.0000000                      reserved
  32    0.0000000                      reserved
  33    0.0000000                      reserved
  34    0.0000000                      reserved
  35   0.50110305E-02                  TAU-  --> 2PI-, PI+, 2PI0 old
  36    0.0000000                      TAU-  --> a1 --> rho omega
  37    0.0000000                      TAU-  --> benchmark curr
  38    0.0000000                      TAU-  --> 2PI- PI+ 2PI0 app08
  39    0.0000000                      TAU-  --> PI- 4PI0  app08
  40    0.0000000                      TAU-  --> 3PI- 2PI+ app08
  41    0.0000000                      TAU-  --> 2PI- 2PI+  K-
  42    0.0000000                      TAU-  --> 2PI- PI+ PI0 K0
  43    0.0000000                      TAU-  --> PI- 4PI0
  44    0.0000000                      reserved
  45    0.0000000                      reserved
  46    0.0000000                      reserved
  47    0.0000000                      reserved
  48    0.0000000                      reserved
  49    0.0000000                      reserved
  50    0.0000000                      reserved
  51    0.0000000                      reserved
  52    0.0000000                      reserved
  53    0.0000000                      reserved
  54    0.0000000                      reserved
  55    0.0000000                      reserved
  56   0.78900479E-03                  TAU-  --> 3PI-, 2PI+,
  57   0.18300110E-03                  TAU-  --> 3PI-, 2PI+,  PI0
  58   0.25100150E-03                  TAU-  --> 2PI-,  PI+, 3PI0
  59    0.0000000                      TAU-  --> 3pi- 2pi+ 2pi0
  60    0.0000000                      TAU-  --> 4PI- 3PI+
  61    0.0000000                      TAU-  --> 4PI- 3PI+  PI0
  62    0.0000000                      TAU-  --> 2PI- 2PI+ K- PI0
  63    0.0000000                      reserved
  64    0.0000000                      reserved
  65    0.0000000                      reserved
  66    0.0000000                      reserved
  67    0.0000000                      reserved
  68    0.0000000                      reserved
  69   0.15900095E-02                  TAU-  -->  K-, PI-,  K+
  70   0.16720101E-02                  TAU-  -->  K0, PI-, K0B
  71   0.15360093E-02                  TAU-  -->  K-,  PI0, K0
  72   0.68000407E-03                  TAU-  --> PI0  PI0   K-
  73   0.30090183E-02                  TAU-  -->  K-  PI-  PI+
  74   0.37670226E-02                  TAU-  --> PI-  K0B  PI0
  75   0.18300110E-02                  TAU-  --> ETA  PI-  PI0
  76   0.80200483E-03                  TAU-  --> PI-  PI0  GAM
  77   0.91783553E-01                  TAU-  --> PI0  PI0  PI-
  78   0.91783553E-01                  TAU-  --> PI-  PI-  PI+
  79    0.0000000                      TAU-  --> K-    K-   K+
  80    0.0000000                      TAU-  --> K-    K0   K0
  81    0.0000000                      TAU-  --> K-   ETA  PI0
  82    0.0000000                      TAU-  --> K0   ETA  PI-
  83    0.0000000                      TAU-  --> K-   K0   RHO0
  84    0.0000000                      TAU-  --> PI-  PHI  PI0
  85    0.0000000                      TAU-  --> K-   PHI  PI0
  86    0.0000000                      TAU-  --> K0   ETA  K-
  87    0.0000000                      reserved
  88   0.25375551                      TAU-  -->  RHO- -> PI- PI0
  89   0.90931449E-02                  TAU-  -->  PI- K0
  90   0.45479368E-02                  TAU-  -->  K-  PI0
  91   0.16510099E-02                  TAU-  -->  K-  K0
  92    0.0000000                      TAU-  -->  mu-mu-mu+ !nu_tau
  93    0.0000000                      TAU-  --> mu- mu- e+ !nu_tau
  94    0.0000000                      TAU-  --> mu- e- mu+ !nu_tau
  95    0.0000000                      TAU-  --> mu- e- e+  !nu_tau
  96    0.0000000                      TAU-  --> mu+ e- e-  !nu_tau
  97    0.0000000                      TAU-  --> e- e- e+   !nu_tau
  98    0.0000000                      TAU-  --> e-pi+pi-  !nu_tau
  99    0.0000000                      TAU-  --> mu-pi+pi-  !nu_tau
 100    0.0000000                      TAU-  --> e-pi+K-  !nu_tau
 101    0.0000000                      TAU-  --> mu-pi+K-  !nu_tau
 102    0.0000000                      TAU-  --> e-pi-K+  !nu_tau
 103    0.0000000                      TAU-  --> mu-pi-K+  !nu_tau
 104    0.0000000                      TAU-  --> e-K-K+  !nu_tau
 105    0.0000000                      TAU-  --> mu-K-K+  !nu_tau
 106    0.0000000                      TAU-  --> e-K0K0  !nu_tau
 107    0.0000000                      TAU-  --> mu-K0K0  !nu_tau
 108    0.0000000                      TAU-  --> e+pi-pi-  !nu_tau
 109    0.0000000                      TAU-  --> mu+pi-pi-  !nu_tau
 110    0.0000000                      TAU-  --> e+pi-K-  !nu_tau
 111    0.0000000                      TAU-  --> mu+pi-K-  !nu_tau
 112    0.0000000                      TAU-  --> e+K-K-  !nu_tau
 113    0.0000000                      TAU-  --> mu+K-K-  !nu_tau
 114    0.0000000                      TAU-  --> mu-mu- p+  !nu_tau
 115    0.0000000                      TAU-  --> mu-mu+ p-  !nu_tau
 116    0.0000000                      TAU-  -->  e - e- p+ !nu_tau
 117    0.0000000                      TAU-  -->  e - e+ p- !nu_tau
 118    0.0000000                      TAU-  --> eta k-
 119    0.0000000                      TAU-  --> eta pi-
 120    0.0000000                      TAU-  --> PI-  PHI
 121    0.0000000                      TAU-  -->  K-  PHI
 122    0.0000000                      TAU-  -->  PI- OMEGA
 123    0.0000000                      TAU-  -->  K-  OMEGA
 124    0.0000000                      TAU-  -->  PI- ETAprm
 125    0.0000000                      TAU-  -->  K-  ETAprm
 126    0.0000000                      TAU-  -->  e- mu+ p- !nu_tau
 127    0.0000000                      TAU-  -->  e+ mu- p- !nu_tau
 128    0.0000000                      TAU-  -->  e- mu- p+ !nu_tau
 129    0.0000000                      TAU-  --> e- PI0 PI0  !nu_tau
 130    0.0000000                      TAU-  --> mu- PI0 PI0 !nu_tau
 131    0.0000000                      TAU-  --> e- PI0 eta !nu_tau
 132    0.0000000                      TAU-  --> mu- PI0 eta !nu_tau
 133    0.0000000                      TAU-  -->  e- PI0 eta_p !nu_t
 134    0.0000000                      TAU-  --> mu- PI0 eta_p !nu_t
 135    0.0000000                      TAU-  --> e- eta eta  !nu_tau
 136    0.0000000                      TAU-  --> mu- eta eta !nu_tau
 137    0.0000000                      TAU-  --> e- eta eta_p !nu_t
 138    0.0000000                      TAU-  --> mu- eta eta_p !nu_t
 139    0.0000000                      TAU-  --> e- PI0 Ks  !nu_tau
 140    0.0000000                      TAU-  --> mu- PI0 Ks !nu_tau
 141    0.0000000                      TAU-  --> e- eta  Ks !nu_tau
 142    0.0000000                      TAU-  --> mu- eta Ks !nu_tau
 143    0.0000000                      TAU-  --> e- eta_p Ks !nu_tau
 144    0.0000000                      TAU-  --> mu- eta_p Ks !nu_t
 145    0.0000000                      TAU-  --> p- pi+ K- !nu_tau
 146    0.0000000                      TAU-  --> p+ pi- K-  !nu_tau
 147    0.0000000                      TAU-  --> p- K+ pi- !nu_tau
 148    0.0000000                      TAU-  --> p- pi0 pi0 !nu_tau
 149    0.0000000                      TAU-  --> p- pi0 eta !nu_tau
 150    0.0000000                      TAU-  --> p- pi0 Ks !nu_tau
 151    0.0000000                      reserved
 152    0.0000000                      reserved
 153    0.0000000                      reserved
 154    0.0000000                      reserved
 155    0.0000000                      reserved
 156    0.0000000                      reserved
 157    0.0000000                      reserved
 158    0.0000000                      reserved
 159   0.11084167                      TAU-  --> PI-
 160   0.69460417E-02                  TAU-  --> K-
 161    0.0000000                      TAU-  --> gamma e-   !nu_tau
 162    0.0000000                      TAU-  --> gamma mu-  !nu_tau
 163    0.0000000                      TAU-  --> PI0 e-     !nu_tau
 164    0.0000000                      TAU-  --> PI0 mu-    !nu_tau
 165    0.0000000                      TAU-  --> eta e-     !nu_tau
 166    0.0000000                      TAU-  --> eta mu-    !nu_tau
 167    0.0000000                      TAU-  --> e-  K0     !nu_tau
 168    0.0000000                      TAU-  --> mu- K0     !nu_tau
 169    0.0000000                      TAU-  --> e-  omega  !nu_tau
 170    0.0000000                      TAU-  --> mu- omega  !nu_tau
 171    0.0000000                      TAU-  --> e-  phi    !nu_tau
 172    0.0000000                      TAU-  --> mu- phi    !nu_tau
 173    0.0000000                      TAU-  --> e- rho0    !nu_tau
 174    0.0000000                      TAU-  --> mu- rho0   !nu_tau
 175    0.0000000                      TAU-  --> A0-
 176    0.0000000                      TAU-  --> B1-
 177    0.0000000                      TAU-  --> e- K0    !nu_tau
 178    0.0000000                      TAU-  --> mu- K0    !nu_tau
 179    0.0000000                      TAU-  -->  p gamma  !nu_tau
 180    0.0000000                      TAU-  --> p pi0     !nu_tau
 181    0.0000000                      TAU-  --> p eta    !nu_tau
 182    0.0000000                      TAU-  -->  p K0   !nu_tau
 183    0.0000000                      TAU-  --> e- eta_p  !nu_tau
 184    0.0000000                      TAU-  --> mu- eta_p !nu_tau
 185    0.0000000                      TAU-  --> pi- lambda !nu_tau
 186    0.0000000                      TAU-  --> pi- lmb_br !nu_tau
 187    0.0000000                      TAU-  --> K- lambda  !nu_tau
 188    0.0000000                      TAU-  --> K- lmb_bar !nu_tau
 189    0.0000000                      TAU-  --> e-  K*  !nu_tau
 190    0.0000000                      TAU-  --> e-  K*_bar !nu_tau
 191    0.0000000                      TAU-  --> mu- K*_bar !nu_tau
 192    0.0000000                      TAU-  --> mu-  K*  !nu_tau
 193    0.0000000                      TAU-  --> e- a0(980) !nu_tau
 194    0.0000000                      TAU-  --> mu- a0(980) !nu_tau
 195    0.0000000                      TAU-  --> e-  f0(980) !nu_tau
 196    0.0000000                      TAU-  --> mu- f0(980) !nu_tau
 197    0.0000000                      reserved
 198    0.0000000                      reserved
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


###  Herwig

`Herwig` is another historical LEP generator providing a difefrent approach to hadronization wrt `Pythia8`. It is available as standalone program:

```
$ which Herwig
/cvmfs/sw.hsf.org/spackages7/herwig3/7.2.3/x86_64-centos7-gcc11.2.0-opt/q3pxd/bin/Herwig
```


###  MadGraph5

`MadGraph5` was developed for `LHC` but it is reality general purpose and can be used also for `FCC-ee`. It is available as standalone program:

```bash
$ which mg5_aMC
/cvmfs/sw.hsf.org/spackages7/madgraph5amc/2.8.1/x86_64-centos7-gcc11.2.0-opt/nlauf/bin/mg5_aMC
```

## Hands-on case study: ditau events with Pythia8, Whizard and KKMCee

In this section we describe, with exercises, the generation of an equivalent sample of Monte Carlo events with three diffent generators: `Pythia8`, `Whizard` and `KKMCee`. The process chosen is $e^{-}e^{+} \rightarrow \tau^{-}\tau^{+}$
 (hereafter referred to as _ditaus_), with both _taus_ decaying leptonically with a _muon_ in the final state. The centre of mass energy of 91.2 GeV. In the three cases 10000 will be generated and saved in `ROOT` files in `EDM4hep` format: the steps to arrive at this results are however different.

### Generating ditaus with Pythia8

As explained in the dedicated [Pythia8 section](#pythia8), we need a `Pythia8` configuration file and a `Gaudi` configuration file.
For the former, to generate ditau events we will use the file
[p8_ee_Ztautau_mumu_ecm91.cmd](https://github.com/HEP-FCC/FCC-config/blob/main/FCCee/Generator/Pythia8/p8_ee_Ztautau_mumu_ecm91.cmd). We create a sub-directory `cards` and we retrieve in it the file:
```
$ mkdir cards; cd cards
$ wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/main/FCCee/Generator/Pythia8/p8_ee_Ztautau_mumu_ecm91.cmd
```
For the second, we create a sub-directory `config` and we retrieve in it the `pythia.py` file:
```
$ mkdir config; cd config
$ wget https://raw.githubusercontent.com/HEP-FCC/k4Gen/main/k4Gen/options/pythia.py
```

Before running it, we also create sub-directories `gen/<generator_tag>_tautau_ecm91` for the generator files in format `edm4hep`.

:::{admonition} Nota Bene
:class: callout

The sub-directory structure here is not mandatory but copes with the dataset structure suggested by `FCCAnalyses`, as we can see later.
:::

Now: how will we run it? (hint: check specific section)

:::{admonition} Answer
:class: toggle

```
k4run config/pythia.py -n 10000 --out.filename gen/p8_tautau_ecm91/events_1.root --Pythia8.PythiaInterface.pythiacard cards/p8_ee_Ztautau_mumu_ecm91.cmd
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


### Generating ditaus with Whizard

As explained in the dedicated [Whizard section](#whizard), to use `whizard` we need a `Sindarin` configuration file. To generate ditau events we will use the file
[Z_tautau.sin](http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/Z_tautau.sin):
```
$ wget http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/Z_tautau.sin
```
and run it in a dedicate directory to not pollute the working one with the many files produced:
```
$ mkdir -p whizard; cd whizard;
$ whizard ../Z_tautau.sin
```
The output created by `whizard` is `LHEf` (Les Houches Event format); this is because the current build does not support writing `HepMC`; this may change in the future.

Exercise: look at produced `LHEf` file `z_tautau.lhe`: what did we notice?

:::{admonition} Answer
:class: toggle

The taus are not decayed. We need another solution for that.

:::

The first lines of the `LHEf` file give the total cross-section: 1.508 +- 2 pb, which seems definitely higher than the others.

#### `LHEf` to `EDM4hep` conversion

In order to get the events in `EDM4hep` format, we exploit the fact that `Pythia` provides `LHEf` reader functionality. To activate that we will use `Gaudi` and special `.cmd` file the consider the input `LHEf` input file as a `Beam`. This special `.cmd` is called `p8_lhereader.cmd` and it is available on the web:
```
S cd ../cards
wget http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/p8_lhereader.cmd
```
Please note the lines
```
! 4) Read-in Les Houches Event file - alternative beam and process selection.
Beams:frameType = 4                      ! read info from a LHEF
Beams:LHEF = z_tautau.lhe                ! the LHEF to read from
```
This file needs to be edited to enter the exact locaton of the input file (it could also be a symlink to avoid always editng the file.

Also note the lines:
```
! Tau decays to mu nu_tau nu_mu (from pythia8)
15:onMode = off
15:onIfAny = 14
```
which will make decay the taus in `pythia8`

As steering we will use the file `pythia.py`.

Q: how will we run it from the whizard sub-directory? (hint: think of the conversion file)

:::{admonition} Answer
:class: toggle

```
$ cd whizard
$ k4run ../config/pythia.py -n 10000 --out.filename ../gen/wz_tautau_ecm91/events_1.root --Pythia8.PythiaInterface.pythiacard ../cards/p8_lhereader.cmd | tee wz_ee_Ztautau_mumu_ecm91.log
```
:::


### Generating ditaus with KKMCee
As shown in the [KKMCee section](#kkmcee), event generation with the `KKMCee` is controlled through a configuration file. The interface available in `key4hep` allowed a generation of the configuration file through command line switches. Starting from the command line switches is therefore always a good option when no confguration file is available.

Currently, `KKMCee` does not have the option to save directly the events in `EDM4hep` format. In order to get there we need first to generate the events in `HepMC` format.

#### Generating `HepMC` events

What are the commands (options) to generate 10000 ditau events and saved them into the file gen/kk_ee_Ztautau_mumu_ecm91_10000.hepmc ? 

:::{admonition} Suggested answer
:class: toggle

```bash
KKMCee -f Tau -e 91.2 -n 10000 -o kk_ee_Zautau_mumu_10000.hepmc -t 2002
```
:::

:::{admonition} Expand to see the example of the produced `HepMC` output 
:class: toggle

The `HepMC` output is an ASCII format and can browsed with for example `more`:

```bash
$ more kk_ee_Ztautau_mumu_10000.hepmc
HepMC::Version 3.02.05
HepMC::Asciiv3-START_EVENT_LISTING
E 0 5 13
U GEV MM
A 6 spin 0.008477 -0.585915 -0.810328
A 7 spin 0.895044 -0.441222 0.064956
P 1 0 -11 0.0000000000000000e+00 0.0000000000000000e+00 -4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 2 1 -11 2.2399816427048513e-07 1.2760500083922739e-07 -4.5594392324226938e+01 4.5594392327084165e+01 5.1043808629749475e-04 2
P 3 1 22 -2.2399816427048513e-07 -1.2760500083922739e-07 -5.6076729099135154e-03 5.6076729158391651e-03 0.0000000000000000e+00 1
P 4 0 11 0.0000000000000000e+00 0.0000000000000000e+00 4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
V -2 0 [2,4]
P 5 -2 23 2.2399816427048513e-07 1.2760500083922739e-07 5.6076729099103773e-03 9.1194392327084159e+01 9.1194392154672272e+01 2
P 6 5 15 7.1885962308218696e+00 -4.4991780056897120e+01 -9.8145772963693700e-02 4.5597189910708785e+01 1.7770500000001239e+00 2
P 7 5 -15 -7.1885960068237056e+00 4.4991780184502126e+01 1.0375344587360721e-01 4.5597202416375396e+01 1.7770499999998681e+00 2
P 8 6 16 3.6528532505035400e+00 -2.5398200988769531e+01 4.4600862264633179e-01 2.5663415908813477e+01 0.0000000000000000e+00 1
P 9 6 13 2.9088804721832275e+00 -1.4574359893798828e+01 -6.1780035495758057e-01 1.4875025749206543e+01 1.0565830000000000e-01 1
P 10 6 -14 6.2686276435852051e-01 -5.0192222595214844e+00 7.3646016418933868e-02 5.0587520599365234e+00 0.0000000000000000e+00 1
P 11 7 -16 -1.4101594686508179e+00 1.0276637077331543e+01 1.8954864144325256e-01 1.0374669075012207e+01 0.0000000000000000e+00 1
P 12 7 -13 -5.2335274219512939e-01 1.9895267486572266e+00 2.5705483555793762e-01 2.0758986473083496e+00 1.0565830000000000e-01 1
P 13 7 14 -5.2550840377807617e+00 3.2725616455078125e+01 -3.4285002946853638e-01 3.3146636962890625e+01 0.0000000000000000e+00 1
E 0 7 17
U GEV MM
A 8 spin -0.961817 0.224045 0.157199
A 9 spin -0.961817 0.224045 0.157199
A 11 spin -0.790568 -0.498846 -0.355182
P 1 0 -11 0.0000000000000000e+00 0.0000000000000000e+00 -4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 2 1 -11 1.3608988909162606e-03 -7.0797770900342773e-04 -4.5535420867045751e+01 4.5535402652364432e+01 -4.0757567471711616e-02 2
P 3 1 22 -1.3608988909162606e-03 7.0797770900342773e-04 -6.4579130091094755e-02 6.4597347635566904e-02 -1.6130980174698654e-09 1
P 4 0 11 0.0000000000000000e+00 0.0000000000000000e+00 4.5599999997136848e+01 4.5600000000000001e+01 5.1099859770630950e-04 4
P 5 4 11 -6.9206286709266992e-06 1.4913930365122828e-04 4.5598536086585199e+01 4.5598528495827317e+01 -2.6311159737751326e-02 2
P 6 4 22 6.9206286709266992e-06 -1.4913930365122828e-04 1.4639105516485410e-03 1.4715041726827383e-03 2.0579515874459978e-11 1
V -3 0 [2,5]
P 7 -3 23 1.3539782622453340e-03 -5.5883840535219948e-04 6.3115219539447764e-02 9.1133931148191749e+01 9.1133909281051146e+01 2
P 8 7 -15 3.9415751172627040e+01 2.1813196014962450e+01 6.5533728999791174e+00 4.5585978851090765e+01 2.3911943786087866e+00 2
P 9 8 -15 3.9337461622363861e+01 2.1673662453262313e+01 6.5670154262523361e+00 4.5425401807139110e+01 1.7770499999996121e+00 2
P 10 8 22 7.8289550263179436e-02 1.3953356170013725e-01 -1.3642526273218885e-02 1.6057704395165695e-01 -2.6341780319308772e-09 1
P 11 7 15 -3.9414397194364788e+01 -2.1813754853367801e+01 -6.4902576804396714e+00 4.5547952297100949e+01 1.7770499999997402e+00 2
P 12 11 16 -2.1019369125366211e+01 -1.1058233261108398e+01 -3.3810205459594727e+00 2.3990200042724609e+01 0.0000000000000000e+00 1
P 13 11 13 -1.0991277694702148e+00 -4.3037441372871399e-01 -7.9439476132392883e-02 1.1877619028091431e+00 1.0565830000000000e-01 1
P 14 11 -14 -1.7295900344848633e+01 -1.0325146675109863e+01 -3.0297973155975342e+00 2.0369989395141602e+01 0.0000000000000000e+00 1
P 15 9 -16 3.7669422626495361e+00 2.1739947795867920e+00 1.1482763290405273e+00 4.4982938766479492e+00 0.0000000000000000e+00 1
P 16 9 -13 2.2649795532226562e+01 1.2544136047363281e+01 3.6078701019287109e+00 2.6141853332519531e+01 1.0565830000000000e-01 1
P 17 9 14 1.2920722961425781e+01 6.9555315971374512e+00 1.8108688592910767e+00 1.4785254478454590e+01 0.0000000000000000e+00 1
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
$ tail -37 kk/KKMCee-24Apr2023-060444/pro.output
   *****************************
   ****   KKMCee   Finalize ****
   *****************************
********************************************************************************
*                                                                              *
*                   ****************************************                   *
*                   ******      KKMCee::Finalize      ******                   *
*                   ****************************************                   *
*   f_NevGen =      10000 =                          No. of generated events   *
*   XsPrimPb =       2700.8551   =                   Primary from Foam [pb]    *
*  FoamInteg =       1714.1189   =                   Crude from FOAM   [pb]    *
*         +- =    0.0015340174   =                   error                     *
*                   ****************************************                   *
*   <WtMain> =      0.54999872   =                   average WtMain            *
*         +- =    0.0014270066   =                   error abs.                *
*     XsMain =       1485.4669   =                   Xsection main [pb]        *
*         +- =    0.0070075399   =                   error absolute            *
*         +- =    0.0025945634   =                   error relative            *
*                   ********** More from WtMainMonit *******                   *
*      AveWt =      0.54999872   =                   average <WtMain>          *
*      ERela =    0.0025945634   =                   relative error            *
*      sigma =      0.38656078   =                   dispersion of WtMain      *
*   DB_WTmax =               4   =                   input WTmax               *
*      WtMax =       5.6197178   =                   maximum  WTmain           *
*      WtMin =               0   =                   mainimum WTmain           *
*      AvUnd =               0   =                   underflow                 *
*      AvOve =   3.8040121e-05   =                   overflow                  *
* AvOve/<Wt> =   6.9164016e-05   =                   relative: AvOve/AveWt     *
*       Ntot =           73381   =                   Ntot primary events       *
*       Nacc =           10000   =                   accepted events           *
*  Nacc/Ntot =      0.13627506   =                   acceptance rate           *
*       Nneg =               0   =                   WT<0 events               *
*       Nove =               2   =                   WT>WTmax events           *
*  Nove/Ntot =   2.7255012e-05   =                   Nove/Ntot                 *
*       Nzer =            1209   =                   WT=0 events               *
*                                                                              *
********************************************************************************

```
i.e the total ditau cross-section at 91.2 GeV from `KKMCee` is 1485.5 +- 0.007 pb . 

#### `HepMC` to `EDM4hep` conversion

In order to get the events in `EDM4hep` format, we will use `Gaudi` and the tools available in [k4FWCore](https://github.com/key4hep/k4FWCore) and [k4Gen](https://github.com/HEP-FCC/k4Gen/). We need a Gaudi steering file that reads the `HepMC` file and writes out the `EDM4hep` file.
A minimal version of such a steering code is available on the tutorial reference page:
```
wget http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/hepmc2edm.py
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
We would like the output file to be called `kk_Ztautau_mumu_10000.e4h.root` . Which command should we use for that?

:::{admonition} Check answer
:class: toggle

```bash
k4run config/hepmc2edm.py -n 10000 --GenAlg.HepMCFileReader.Filename kk/kk_tautau_10000.hepmc --out.filename gen/kk_tautau_ecm91/events_1.root
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


Q: How the cross-sections compare?

:::{admonition} Answer
:class: toggle

The differences of the cross-section calculated by `KKMCee` and `Pythia8` is (1485.5 - 1467.0) pb = 18.5 pb ; the errors have a statistical and systematic component. Assuming half and half for statistical and systematics, and the systematics fully correlated, the error on the difference is about 8.5 pb, i.e. the two calculatons differ by 2.6 standard deviations. What would you check first?

:::


### Looking at the produced files. Comparing distributions

The idea here is to look at some distributions, typically key for generators (angles, momenta). We take as example: acollinearity (of the initial taus, of the decaying products), momenta and cosinus of polar angles of the final 1-prompt products. 

#### Looking the MCParticle class

Despite being ROOT files and the information stored in `POD` (Plain Old Data), the `EDM4hep` files are not easily usable, because interpreting the PODs requires the higher level PODIO / EDM4hep classes.
This is what the helper functions available in FCCAnalyses, which depend of `EDM4hep`, do. They can be used to create `flat` ntuples, to be used for the analysis later on.

#### Building FCCAnalyses

`FCCAnalyses` is avaibale at [https://github.com/HEP-FCC/FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses). `FCCAnalysis`, which is based on ROOT DataFrame, changes regularly, almost daily.
Therefore it is always good to rebuild the latest version. It is advised to do it in a separate directory,
for example `../FCCAnalyses`.

```
$ cd ..
$ git clone https://github.com/HEP-FCC/FCCAnalyses.git
$ cd FCCAnalyses; mkdir {build,install}; cd build
$ cmake -DCMAKE_INSTALL_PREFIX=../install ..
$ make -j4 install
$ cd ..
$ source setup.sh
$ cd ../tutorials1
```
It is mandatory to run setup after the build in the source directory. 

Now we are ready to go.

#### Creating histograms with FCCAnalyses
At this purpose we will use the recently introduced `build_graph` attribute. The example is availble at 
[histmaker_ttmm.py](http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/histmaker_ttmm.py).

##### Dissection of `histmaker_ttmm.py`

:::{admonition} Expand
:class: toggle

The files need to be organised in a special way: directories need to be called as the process, files below need to be called `events_<num>`, when `<num>` is any number. So in the current case we have
```
$ ls -lt gen
total 0
drwxr-xr-x. 2 ganis sf 26 Apr 24 07:38 wz_tautau_ecm91
drwxr-xr-x. 2 ganis sf 26 Apr 24 07:37 p8_tautau_ecm91
drwxr-xr-x. 2 ganis sf 26 Apr 24 07:37 kk_tautau_ecm91
```
translating in the following `processList`:
```
# list of processes (mandatory)
processList = {
    'p8_tautau_ecm91':    {'fraction':1},
    'wz_tautau_ecm91':    {'fraction':1},
    'kk_tautau_ecm91':    {'fraction':1},
}
```

Then we need to define where the files are and where they will to go:
```
# Define the input dir (optional)
inputDir    = "gen/"

#Optional: output directory, default is local running directory
outputDir   = "outputs"
```

Define some binning for histograms:
```
# define some binning for various histograms
bins_p_l = (100, 0, 50) # 0.5 GeV bins
bins_cosTheta = (50, -1, 1)
bins_acol = (50, -1, -.9)
```

Now we come to the `build_graph`: here the input is the `RDataFrame` called `df` and the output a list of histograms called `results`.
We can use the built-in functions to extract the information, or define our own as in here
```
    import ROOT
    ROOT.gInterpreter.Declare("""

       #ifndef funDone
       #define funDone

       float cosTheta(const edm4hep::Vector3f& in){
          return (in.z/sqrt(pow(in.x,2)+pow(in.y,2)+pow(in.z,2)));
       };

       float scalarProductNorm(const edm4hep::Vector3f& in1, const edm4hep::Vector3f& in2 ){
          return ((in1.x*in2.x + in1.y*in2.y + in1.z*in2.z)/sqrt(pow(in1.x,2)+pow(in1.y,2)+pow(in1.z,2))/sqrt(pow(in2.x,2)+pow(in2.y,2)+pow(in2.z,2) ));
       };

       float momP(const edm4hep::Vector3f& in ){
          return (sqrt(pow(in.x,2)+pow(in.y,2)+pow(in.z,2)));
       };

       #endif
    """)
```
which will need for the acollinearity and 1-prompt momentum and cos(theta).
The histograms are defined in here
```
    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("P_mup", "", *bins_p_l), "muplus_p"))
    results.append(df.Histo1D(("P_mum", "", *bins_p_l), "muminus_p"))
    results.append(df.Histo1D(("CosTheta_taup", "", *bins_cosTheta), "cthetaup"))
    results.append(df.Histo1D(("CosTheta_mup", "", *bins_cosTheta), "cthemup"))
    results.append(df.Histo1D(("AcolTau", "", *bins_acol), "acoltau"))
    results.append(df.Histo1D(("AcolMu", "", *bins_acol), "acolmu"))
```
:::

##### Running `histmaker_ttmm.py`

The `build_graph` is part of the `fccanalyses run`:
```
$ fccanalysis run histmaker_ttmm.py
```
This should produce `ROTO` files with the histograms in `./outputs`:
```
 $ ls -lt outputs/
total 24
-rw-r--r--. 1 ganis sf 7386 Apr 24 18:01 kk_tautau_ecm91.root
-rw-r--r--. 1 ganis sf 7384 Apr 24 18:01 wz_tautau_ecm91.root
-rw-r--r--. 1 ganis sf 7399 Apr 24 18:01 p8_tautau_ecm91.root
```

#### Comparing distributions

FCCAnalyses provides the `plots` option to prepare some plots. A possible way to plot the histos is available at
[plots_ttmm.py](http://fccsw.web.cern.ch/tutorials/apr2023/tutorial1/plots_ttmm.py), which can run as
```
$ fccanalysis plots plots_ttmm.py
```
with results available under `plots`.

Example of a result are: [positive muon momentum](images/p_mup.png), [positive muon cosine theta](images/costheta_mup.png), [acollinearity of muons](images/acolmu.png).

#### Possible conclusion of the exercise

Think of your own. Expand for a possible one.

:::{admonition} Hint
:class: toggle

The distributions show a lot of similarities, which means that for detector optimisation studies the choice of the generator probably won't matter. However, the total cross-section is significantly different, so for studies where exact calculations matter more, the `KKMCee` seems the choice to go, because it is the only one giving the total cross-section compatible with experiment (ALEPH at 91.197 GeV gave 1.4771 ± 0.0066± 0.0027 pb). 
:::
