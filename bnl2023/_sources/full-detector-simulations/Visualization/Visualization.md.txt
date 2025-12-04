# Visualization

Visualization is of paramount importance in order to easily understand the behaviour of the detector and simulation. In this section, several tools of visualizing the detector geometry and the particle tracks are provided.

## Key4hep tool: geoDisplay

The tool `geoDisplay` is available as part of `Key4hep` project. To use it, first we need to source it from `LCG`

```shell
source /cvmfs/sft.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh 
```

To use it, just pass as first argument the `xml` file with the detector description, for example

```shell
geoDisplay $DD4hepINSTALL/DDDetectors/compact/SiD.xml
```

## Geant4 

The `Geant 4` visualization capabilities can be accesed as

```shell
source /cvmfs/sft.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh 
ddsim --compactFile $DD4hepINSTALL/DDDetectors/compact/SiD.xml --runType vis
```

This version of `Geant 4` is built with `Qt` interface, and can be explicitly called as

```shell
ddsim --compactFile $DD4hepINSTALL/DDDetectors/compact/SiD.xml --runType qt
```

As in the previous step, the `LCG` version of `Key4hep` was sourced.

## Phoenix@FCC

[Phoenix](https://github.com/HSF/phoenix) is a web based event display for High
Energy Physics. To visualize FCC events one needs to provide detector geometry
and generated events --- event data.

In this tutorial we will be working with files/programs stored on two computers. First
computer will be the one which can source FCCSW stack, e.g. `lxplus` and the
second one will be yours with the recent web browser. We will call the first
one the _remote machine_ and the second one the _local machine_.


### Event Data from CLD Reconstructed Events

Let's start with the visualization of the event data in the established detector
design CLD, which started its life as the detector designed for the CLIC linear
collider concept. The detectors in FCCSW are described in
[DD4hep](https://dd4hep.web.cern.ch/dd4hep/) compact files. The compact files
are written in XML and expose configuration options for the detector.

Example CLD compact file can be examined after sourcing of the FCCSW stack on
the remote machine
```sh
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```
like so
```sh
less ${FCCDETECTORS}/Detector/DetFCCeeCLD/compact/FCCee_o2_v02/FCCee_o2_v02.xml
```
This is a copy of the
[FCCDetectors](https://github.com/HEP-FCC/FCCDetectors/blob/main/doc/DD4hepInFCCSW.md#visualisation)
repository, which stores FCC detector designs.

The Phoenix web application already showcases the CLD detector
[here](https://fccsw.web.cern.ch/fccsw/phoenix/#/fccee-cld/) and we will
simulate few events in order to visualize them there.

On the remote machine we will need to clone the
[CLICPerformance](https://github.com/iLCSoft/CLICPerformance) repository
```sh
git clone https://github.com/iLCSoft/CLICPerformance.git
cd CLICPerformance/fcceeConfig
```

run the simulation
```sh
ddsim --compactFile $LCGEO/FCCee/compact/FCCee_o1_v04/FCCee_o1_v04.xml \
      --outputFile tops_edm4hep.root \
      --steeringFile fcc_steer.py \
      --inputFiles ../Tests/yyxyev_000.stdhep \
      --numberOfEvents 7
```

and after that, run the reconstruction with the help of
[this](https://fccsw.web.cern.ch/fccsw/tutorials/static/python/fccRec_e4h_input.py)
steering file
```sh
wget https://fccsw.web.cern.ch/fccsw/tutorials/static/python/fccRec_e4h_input.py
k4run fccRec_e4h_input.py
```

There should be a file called `tops_cld.root` inside of our working directory.

In order to visualize the events from this file we need co convert the
[EDM4hep](https://edm4hep.web.cern.ch/) ROOT file into intermediate JSON format
with the command:
```sh
edm4hep2json tops_cld.root
```

:::{admonition} EDM4hep Collections
:class: callout
One should specify a list collections to be exported with the `-l` flag. The
default ones are:
* `GenParticles`
* `BuildUpVertices`
* `SiTracks`
* `PandoraClusters`
* `VertexJets`
* `EventHeader`
:::

Now we download the obtained file from the remote machine into our local one.
Most easily done with `scp`
```sh
scp lxplus.cern.ch:CLICPerformance/fcceeConfig/tops_cld.edm4hep.json .
```

To upload the EDM4hep JSON file into the
[Phoenix](https://fccsw.web.cern.ch/fccsw/phoenix/#/fccee-cld/) use the upload
button in the lover right corner of the web page

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/phoenix_upload.png
:align: center
```

to bring up modal with our desired upload option

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/phoenix_upload_edm4hepjson.png
:align: center
:width: 300px
```

The detector and event data might look similar to this screenshot

```{figure} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/phoenix_cld.png
:align: center
:width: 600px

Example reconstructed event in CLD detector
```


:::{admonition} EDM4hep JSON File
:class: solution dropdown
The obtained EDM4hep JSON file should look similar to
[this one](https://fccsw.web.cern.ch/fccsw/tutorials/static/json/tops_cld.edm4hep.json) [Right click to download].
:::


### Event Data from Delphes Fast Simulation

Starting the same way as in [](delphesedm4hep) we will first generate few
events on the remote machine. One can reuse the files generated for that
exercise e.g. `p8_ee_ZH_ecm240_edm4hep.root` or quickly generate them with the
following steps.

First download Pythia card
```sh
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Generator/Pythia8/p8_noBES_ee_ZH_ecm240.cmd
```

and then Delphes cards. One for the detector response
```sh
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Delphes/card_IDEA.tcl
```

and the other for the [EDM4hep](https://edm4hep.web.cern.ch/) formated output
```sh
wget https://raw.githubusercontent.com/HEP-FCC/FCC-config/spring2021/FCCee/Delphes/edm4hep_IDEA.tcl
```

Finally, run the simulation with
```sh
DelphesPythia8_EDM4HEP card_IDEA.tcl edm4hep_IDEA.tcl p8_noBES_ee_ZH_ecm240.cmd p8_ee_ZH_ecm240_edm4hep.root
```

Produced EDM4hep ROOT file needs to be converted into intermediate JSON format
with the `edm4hep2json` converter. Let's look at the file more closely, so we
can decide what to keep/convert.

Start root with
```sh
root p8_ee_ZH_ecm240_edm4hep.root
```

and execute the `Show()` command on the `events` TTree
```
root [1] events->Show(2);
```

this will show you all trees and branches, similar to this example
```
MCRecoAssociations = (vector<edm4hep::MCRecoParticleAssociationData>*)0x5578924809e0
MCRecoAssociations.weight = 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
MCRecoAssociations#0 = (vector<podio::ObjectID>*)0x557890797c00
MCRecoAssociations#0.index = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
MCRecoAssociations#0.collectionID = 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14
MCRecoAssociations#1 = (vector<podio::ObjectID>*)0x5578925c1f00
MCRecoAssociations#1.index = 133, 118, 117, 152, 153, 115, 164, 155, 138, 224, 217, 228, 165, 227, 218, 90, 230, 122, 87, 88
MCRecoAssociations#1.collectionID = 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11
EFlowTrack      = (vector<edm4hep::TrackData>*)0x557892a7d3a0
EFlowTrack.type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
EFlowTrack.chi2 = 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
EFlowTrack.ndf  = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
EFlowTrack.dEdx = 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
EFlowTrack.dEdxError = 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
EFlowTrack.radiusOfInnermostHit = 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000, 320.000000, 655.494995, 17.000000, 655.494995, 320.000000, 17.000000, 17.000000, 17.000000, 17.000000, 17.000000
EFlowTrack.subDetectorHitNumbers_begin = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
EFlowTrack.subDetectorHitNumbers_end = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
EFlowTrack.trackStates_begin = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
EFlowTrack.trackStates_end = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
EFlowTrack.dxQuantities_begin = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
EFlowTrack.dxQuantities_end = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
EFlowTrack.trackerHits_begin = 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38
EFlowTrack.trackerHits_end = 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40
EFlowTrack.tracks_begin = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
EFlowTrack.tracks_end = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
```

We select desired collections with `-l` flag and limit number of converted
events to 10 with `-n` flag
```sh
edm4hep2json -l ReconstructedParticles,Jet,EFlowTrack,TrackerHits,Particle,MCRecoAssociations,MissingET -n 10 p8_ee_ZH_ecm240_edm4hep.root
```

The resulting EDM4hep JSON file can now be downloaded with `scp` to the local
machine and uploaded into
[Phoenix](https://fccsw.web.cern.ch/fccsw/phoenix/#/fccee-idea/) visualization
of the IDEA detector.

:::{admonition} EDM4hep JSON File
:class: solution dropdown
The obtained EDM4hep JSON file should look similar to
[this one](https://fccsw.web.cern.ch/fccsw/tutorials/static/json/p8_ee_ZH_ecm240_edm4hep.edm4hep.json) [Right click to download].
:::


### Detector Geometry

There are several ways how to import FCC detector geometry into Phoenix.
Currently the preferred method is to convert compact DD4hep file(s) to ROOT
files and from ROOT files to glTF files. The first conversion
(`.xml` -> `.root`) is straightforward and can be done using script like
[this](https://fccsw.web.cern.ch/fccsw/tutorials/static/python/dd4hep2root).
With the most important part being the building of the detector geometry from
the compact file

```python
import ROOT

ROOT.gSystem.Load('libDDCore')
description = ROOT.dd4hep.Detector.getInstance()
for cfile in compact_files:
    description.fromXML(cfile)

ROOT.gGeoManager.SetVisLevel(9)
ROOT.gGeoManager.SetVisOption(0)
ROOT.gGeoManager.Export(out_path)
```

We will try to convert FCCee Noble Liquid Calorimeter. On the remote machine
with FCCSW stack already sourced download the `dd4hep2root` script
```sh
wget https://fccsw.web.cern.ch/fccsw/tutorials/static/python/dd4hep2root
```
make it executable
```
chmod u+x dd4hep2root
```
and run the conversion with
```sh
./dd4hep2root -c ${FCCDETECTORS}/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectEmptyMaster.xml \
                 ${FCCDETECTORS}/Detector/DetFCCeeECalInclined/compact/FCCee_ECalBarrel.xml
              -o fccee_lar.root
```

The resulting file `fccee_lar.root` can already be visualized with ROOT. Let's
download it to the local machine with `scp` and then upload it into
[JSROOT](https://root.cern/js/latest/). This way we don't have to have ROOT
installed on our local machine.

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/jsroot_upload.png
:align: center
```

Resulting in the following visualization

```{figure} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/jsroot_lar.png
:align: center
:width: 600px

Noble Liquid Calorimeter visualized with JSROOT
```

Second conversion (`.root` -> `.gltf`) requires additional configuration and
can be done using the
[root_cern-To_gltf-Exporter](https://github.com/HSF/root_cern-To_gltf-Exporter).
We have to create menu items, suppress drawing of detector parts which are too
detailed or can affect the performance.

The
[root_cern-To_gltf-Exporter](https://github.com/HSF/root_cern-To_gltf-Exporter)
converter runs in the browser and is configured with an HTML page. It is
recommended to run the converter on the local machine, but it should be possible
to run it also on the remote machine over SSH with XWindowing enabled.

Let's start with cloning the converter repository
```sh
git clone https://github.com/HSF/root_cern-To_gltf-Exporter.git
cd root_cern-To_gltf-Exporter
```

then, we create new file `fccee_lar_conversion.html` and use, for example, the
following configuration for the FCCee Noble Liquid Calorimeter:
```html
<html>

  <head>
    <script src="https://unpkg.com/three@0.139.1/build/three.js"> </script>
    <script src="https://unpkg.com/three@0.139.1/examples/js/exporters/GLTFExporter.js"> </script>
    <script src="https://root.cern/js/latest/scripts/JSRoot.core.js"> </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/1.3.8/FileSaver.js"></script>
  </head>

<body>
  <script type="module">

    import { convertGeometry } from './phoenixExport.js';

    var hide_children = [
      "passive_",
      "active_",
      "PCB_"
    ];

    var subparts = {
        "Cryo Front" : [["ECAL_Cryo_front_0"], .8],
        "Cryo Back" : [["ECAL_Cryo_back_1"], .8],
        "Cryo Sides" : [["ECAL_Cryo_side_2"], .8],
        "Services Front" : [["services_front_3"], .6],
        "Services Back" : [["services_back_4"], .6],
        "Bath": [["LAr_bath_5"], true]
    }

    convertGeometry("./fccee_lar.root", "fccee_lar.gltf",
                    4, subparts, hide_children, "default", 120);
  </script>
</body>
```

Last missing peace is the ROOT file containing the detector geometry
`fccee_lar.root` which we should also copy into the converter directory.

To start the converter do
```sh
./run
```
which will start the web server and show URL to which we can connect through
the web browser
```
Started http server to serve requests at:
http://127.0.0.1:8000
```

In the web browser we should see directory listing similar to this one:

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/gltfconv.png
:align: center
```

clicking on the `fccee_lar_conversion.html` starts the conversion. At the end of
it the automatic download pop-up should appear in the browser window. The glTF
file can be uploaded into Playground section of the
[Phoenix](https://fccsw.web.cern.ch/fccsw/phoenix/#/playground) application by
selecting the correct geometry file format:

```{image} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/phoenix_playground_upload.png
:align: center
:width: 300px
```

The resulting visualization will be similar to the following screenshot

```{figure} https://fccsw.web.cern.ch/fccsw/tutorials/static/png/phoenix_playground_lar.png
:align: center
:width: 600px

Example reconstructed event in CLD detector
```

:::{admonition} glTF File
:class: solution dropdown
The obtained glTF file should look similar to
[this one](https://fccsw.web.cern.ch/fccsw/tutorials/static/gltf/fccee_lar.gltf) [Right click to download].
:::

:::{admonition} LAr Clusters
:class: challenge

Try to reconstruct calorimeter clusters in LAr Calorimeter and visualize them in
the Phoenix Playground alongside with the detector.

:::
