# FCC: Particle multiplicity

{% objectives "Learning Objectives" %}

This tutorial will teach you how to:

-   **Generate** Z events with **Pythia8** within FCCSW
-   Run a fast parametric **detector simulation** with **Delphes** within FCCSW
-   Plot the particle multiplicity

{% endobjectives %}

First login to to a fresh shell on lxplus, on OSG, or in one of the virtual machine that could be provided on open stack. Usage of bash shell is highly recommended. Create a working directory and go inside

```bash
mkdir mytutorial
cd mytutorial
```

Then, make sure your **setup of the FCC software** is working correctly. A quick check is that the executable `fccrun`, which allows you to run jobs in the Gaudi framework is available on the command line:


```bash
which fccrun
```

If the above command fails without printing a path like `/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.14/x86_64-centos7-gcc8-opt/scripts/fccrun`, you need to setup the FCC software stack 

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

- **Pythia_ee_Z_ecm91.cmd** 

```python
! File: Pythia_ee_Z_ecm91.cmd
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
```



```bash
fccrun $FCCSW/Sim/SimDelphesInterface/options/PythiaDelphes_config_IDEAtrkCov.py --Filename Pythia_ee_Z_ecm91.cmd --filename p8_ee_Z_ecm91.root -n 10000
```

```python
import ROOT as r
import sys

infile = sys.argv[1]

collections = ['efphotons','efcharged','efneutrals']
histo = r.TH2F('','',120,0,120,80,0,80)
f = r.TFile(infile)
tree = f.Get('events')
for entry in tree:
    tlv_tot = r.TLorentzVector()
    npart=0
    #loop over collections
    for c in collections:
        #loop over objects in collections
        coll=getattr(entry,'{}'.format(c))
        npart+=len(coll)
        for p in coll:
            tlv=r.TLorentzVector()
            tlv.SetXYZM(p.core.p4.px,p.core.p4.py,p.core.p4.pz,p.core.p4.mass)
            tlv_tot+=tlv

    histo.Fill(tlv_tot.M(),npart)
c=r.TCanvas()    
histo.Draw('E')
c.SaveAs('plot.png')
```
