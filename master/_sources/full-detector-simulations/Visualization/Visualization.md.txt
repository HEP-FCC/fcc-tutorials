# Visualization

Visualization is of paramount importance in order to easily understand the behavior of the detector and simulation. In this section, several tools of visualizing the detector geometry and the particle tracks are provided.

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

The `Geant 4` visualization capabilities can be accessed as

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

In this tutorial we will be working with files/programs stored on two computers.
First computer will be the one which can source Key4hep stack, e.g. `lxplus` and
the second one will be yours with the recent web browser. We will call the first
one the _remote machine_ and the second one the _local machine_.


### Event Data from CLD Reconstructed Events

Let's start with the visualization of the event data in the established detector
design -- CLD, which started its life as the detector designed for the linear
collider concept CLIC. The detectors in Key4hep are described using
[DD4hep](https://dd4hep.web.cern.ch/dd4hep/) compact files. The compact files
are written in XML and expose configuration options for the detector.

Example CLD compact file can be examined after sourcing of the Key4hep stack on
the remote machine
```sh
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```
like so
```sh
less ${K4GEO}/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml
```
This file is part part of the [k4geo](https://github.com/key4hep/k4geo/)
repository, which stores among other detector concepts integrated in Key4hep
also FCC-ee detector designs.

The Phoenix web application already showcases the CLD detector in different
options [here](https://fccsw.web.cern.ch/fccsw/phoenix/) and we will
simulate few events in order to visualize them there.

On the remote machine we will need to clone the
[CLDConfig](https://github.com/iLCSoft/CLICPerformance) repository
```sh
git clone https://github.com/key4hep/CLDConfig.git
cd CLDConfig/CLDConfig
```

run the simulation
```sh
ddsim --compactFile ${K4GEO}/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml \
      --steeringFile cld_steer.py \
      --inputFiles ../test/yyxyev_000.stdhep \
      --outputFile tops_cld_SIM_edm4hep.root \
      --numberOfEvents 5
```

and after that, run the reconstruction with the help of the
`CLDReconstruction.py` steering file
```sh
k4run CLDReconstruction.py --inputFiles tops_cld_SIM_edm4hep.root \
                           --outputBasename tops_cld \
                           --num-events -1
```

There should now be a file called `tops_cld_REC_edm4hep.root` inside our working
directory. More information about running of the CLD FullSim you can visit
[FCC-ee Detector Full Sim](https://fcc-ee-detector-full-sim.docs.cern.ch/CLD/)
page.

In order to visualize the events inside `tops_cld_REC_edm4hep.root` file we
need to convert the [EDM4hep](https://edm4hep.web.cern.ch/) ROOT file into
intermediate JSON representation with the command:
```sh
edm4hep2json -e 0 tops_cld_REC_edm4hep.root
```

:::{admonition} EDM4hep in JSON
:class: callout
Be careful when converting EDM4hep ROOT files into JSON files as JSON is very
ineffective in storing information leading to very large file size.

Always check size of your file to be around 200MB at maximum. One can check the
file size using `du` command
```bash
du -h tops_cld_REC.edm4hep.json
```

The `edm4hep2json` offers possibility to limit either number of events exported
or which collections. See `edm4hep2json -h` for more details.
:::

Now we download the obtained file from the remote machine into our local one.
Most easily done with `scp`
```sh
scp lxplus.cern.ch:CLDConfig/CLDConfig/tops_cld_REC.edm4hep.json .
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

Let's start by generating sample files using [](delphesedm4hep) tutorial section.

Produced EDM4hep ROOT file(s) needs to be converted into intermediate JSON
format with the `edm4hep2json` converter. Let's look at the file more closely,
so we can decide what to keep/convert.

Primary tool for inspecting EDM4hep files is `podio-dump`. This command can show
you list of all collections and also metadata stored in the file. To list the
collections in the default frame use
```sh
podio-dump p8_ee_ZH_ecm240_edm4hep.root
```

Alternatively, one can always use ROOT to inspect the file. Start by running
```sh
root p8_ee_ZH_ecm240_edm4hep.root
```
and execute the `Show()` command on the `events` TTree
```
root [1] events->Show(2);
```
this will show you all the branches which are by the PODIO reader to recreate
EDM4hep objects and their relations in memory.

Using `edm4hep2json` for converting the EDM4hep ROOT file into JSON we select
desired collections with `-l` flag and limit number of converted events to 10
with `-n` flag
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
