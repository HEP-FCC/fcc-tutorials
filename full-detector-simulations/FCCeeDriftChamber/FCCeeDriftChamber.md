
# FCCee: Full Simulation of IDEA Driftchamber


-   [Generate and Simulate Events](#generate-events)
-   [Analyze Events](#analyze-events)
-   [Plot events](#plot-events)
-   [Homework exercise](#homework-exercise)



{% objectives "Learning Objectives" %}


-   visualize and use the Driftchamber model in FCCSW
-   simulate the particle passage in Geant4
-   run digitization and get wire signal
-   run Hough Transform for a first track reconstruction
-   produce plots

{% endobjectives  %}

## Part I: Simulations with the IDEA detector model in  FCCSW
----------------------------------------------------

This tutorial is based on the FCC Note http://cds.cern.ch/record/2670936 and describes the use of the FCCee IDEA Driftchamber in the FCC software framework. First, setup the fcc software environment:

```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```


From the detector display or the command line, check to see the detector subsystems are there.


```bash
geoDisplay $FCCSWBASEDIR/share/FCCSW/Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml
```


```bash
fccrun $FCCSWBASEDIR/share/FCCSW/Examples/options/geant_fullsim_fccee_pgun.py --detectors $FCCSWBASEDIR/share/FCCSW/Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml --etaMin -3.5 --etaMax 3.5 -n 20000
```

You can see the created files:

```python
#!/bin/env python
import ROOT
f = ROOT.TFile("root://eospublic.cern.ch//eos/experiment/fcc/ee/tutorial/fccee_idea_pgun.root")
events = f.Get("events")

c = ROOT.TCanvas("c_positionedHits_DCH_xy", "", 700, 600)
# draw hits for first five events
events.Draw("positionedHits_DCH.position.x:positionedHits_DCH.position.y", "", "", 10, 0)
c.Draw()
```

This simulation configuration creates hits all along the particle trajectory. To obtain the hits on the wire it is necessary to merge them with [this configuration](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/master/full-detector-simulations/FCCeeDriftChamber/mergeDCHits.py)


```bash 
fccrun mergeDCHits.py
```

```bash
rootls -t mergedDCHits.root
```

By now, we have produced the two files `fccee_idea_pgun.root` and `mergedDCHits.root`.
You can try to put them in a "test" folder on the shared disk space on eos.
The files can already be found under the path `/eos/experiment/fcc/ee/tutorial`.
To use files on eos, you can simply prepend `root://eospublic.cern.ch//eos/experiment/fcc/ee/tutorial/`  when using TFile, or use `xrdcp root://eospublic.cern.ch/<path on eos> <local file name>`
And again, check that your files are present in your current directory:

```bash
xrdcp root://eospublic.cern.ch//eos/experiment/fcc/ee/tutorial/mergedDCHits.root mergedDCHits3.root
```

```python
#!/usr/bin/env python

import ROOT
f = ROOT.TFile("root://eospublic.cern.ch//eos/experiment/fcc/ee/tutorial/mergedDCHits.root")
events = f.Get("events")

# draw hits for first five events
events.Draw("DCHitInfo.hit_start.Perp():DCHitInfo.hit_start.z()", "DCHitInfo.layerId==5&&DCHitInfo.wireId==7", "")
c = ROOT.TCanvas("c_DCH_xy", "", 700, 600)
g = ROOT.TGraph(events.GetSelectedRows(), events.GetV2(), events.GetV1())
g.SetMarkerStyle(4)
g.SetTitle("DriftChamber Hits on one Wire;x;z")
g.Draw("AP")
c.Draw()
```

{% challenge "Driftchamber layers" %}

Using the simulation hits, find the number of wires in each layer.


{% endchallenge %}

```python
#!/usr/bin/env python
import ROOT
import numpy as np
f = ROOT.TFile("mergedDCHits.root")
events = f.Get("events")


c = ROOT.TCanvas("c_DCH_id", "", 700, 600)
events.Draw("DCHitInfo.hit_start.x():DCHitInfo.hit_start.y()", "", "")
dat_x = events.GetV1()
dat_y = events.GetV2()
x = []
y = []
for i in range(events.GetSelectedRows()):
    x.append(dat_x[i])
    y.append(dat_y[i])
    
events.Draw("DCHitInfo.hit_start.z():DCHitInfo.hit_start.z()", "", "")
dat_z = events.GetV1()

z = []
for i in range(events.GetSelectedRows()):
    z.append(dat_z[i])
    
events.Draw("DCHitInfo.wireId:DCHitInfo.layerId", "", "")
dat_wid = events.GetV1()
dat_lid = events.GetV2()
wid = []
lid = []
for i in range(events.GetSelectedRows()):
    lid.append(dat_lid[i])
    wid.append(dat_wid[i])

c.Draw()

lid = np.array(lid)
wid = np.array(wid)
x = np.array(x)
y = np.array(y)
z = np.array(z)

# draw with matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i  in range(500):
    cond = (lid ==1 )  * (wid == i)
    f_x = x[cond]
    f_y = y[cond]
    f_z = z[cond]
    ax.scatter(f_x, f_y, f_z)
plt.show()
```


## Part II User Task: Basic Reconstruction with a Hough-Transform

Go back to the note mentioned in the beginning: http://cds.cern.ch/record/2670936 It uses the Hough-Transform, a simple but very effective Reconstruction method for this type of detector. Some python codes implementing it can be found in this repository: https://github.com/HEP-FCC/HoughTransform
Try to reproduce the results. Background events stored on eos under `/eos/experiment/fcc/ee/generation/GUINEA-PIG/` can be read with this job options file: https://github.com/HEP-FCC/FCCSW/blob/master/Examples/options/geant_fullsim_fccee_hepevt.py.

