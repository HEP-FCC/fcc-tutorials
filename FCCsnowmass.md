#FCC: Getting started with simulating events and analysing them

{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **generate** signal and background samples with **Pythia8** and **MadGraph** within FCCSW
-   run a fast parametric **detector simulation** with **Delphes** within FCCSW
-   apply an **event selection** on those samples with **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with **FCCAnalyses**

{% endobjectives %}
First login to lxplus or one of the virtual machine provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```python
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `fccrun`, which allows you to run jobs in the Gaudi framework is available on the command line:


```python
which fccrun
```

If the above command fails without printing a path like `/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.12/x86_64-centos7-gcc8-opt/scripts/fccrun`, you ned to setup the FCC software stack 

```python
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```


## Part I: Generate and simulate Events with FCCSW

For this tutorial we will consider the following **physics processes**:

-   e+ e- -> ZH -> Z to mumu and H to anything
-   e+ e- -> ZZ -> Z to anything
-   e+ e- -> WW -> W to anything


Let's start by writing the pythia cards for the various processes.

- **Pythia_ee_ZH_Zmumu_ecm240.cmd*** for the Higgs Stralhung signal

```python
! File: Pythia_ee_ZH_Zmumu_ecm240.cmd
Random:setSeed = on
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

Beams:idA = 11                     ! first beam, e+ = 11
Beams:idB = -11                    ! second beam, e- = -11

! 3) Hard process : ZH at 240 GeV
Beams:eCM = 240  ! CM energy of collision
HiggsSM:ffbar2HZ = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! 5) Non-standard settings; exemplifies tuning possibilities.
25:m0        = 125.0               ! Higgs mass
23:onMode    = off		   ! switch off Z boson decays
23:onIfAny   = 13		   ! switch on Z boson decay to muons
```



```python
export $DELPHES_DIR='/cvmfs/sft.cern.ch/lcg/releases/delphes/3.4.3pre02-e4803/x86_64-centos7-gcc8-opt/'
```







## Getting started
Login to lxplus or one of the virtual machine provided on open stack.
Usage of bash shell is highly recommended.
Create a working directory ```mkdir mytutorial; cd mytutorial```
Setup FCC software stack ```source /cvmfs/fcc.cern.ch/sw/latest/setup.sh```

## Produce Delphes events with FCCSW

### From Pythia8 directly


### From LHE events showered with Pythia8