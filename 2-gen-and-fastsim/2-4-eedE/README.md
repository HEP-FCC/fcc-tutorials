EDM4hep Event Data Explorer: eedE
===========================================

<!-- contributors:start -->
:::{admonition} Page contributors
:class: callout dropdown

Xunwu Zuo

Pablo Apausa
:::
<!-- contributors:end -->

The following section explains the usage of [eedE (EDM4hep event data explorer)](https://key4hep.github.io/eede/release/index.html), a web-based tool for visualizing the structure of EDM4hep events. 

Built in vanilla JavaScript with Pixi.js. It takes JSON files as inputs and renders the association between various objects such as Monte Carlo Particles. 

## 1. Generating JSON data from a Root EDM4hep file

### 1.1. Source a FCC software stack release

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
``` 

### 1.2. Convert Root event file to JSON

The `edm4hep2json` command converts the Root edm4hep file to JSON. An example output can be found at [example.edm4hep.json](https://fccsw.web.cern.ch/fccsw/tutorials/eede-tutorial/example_eedE_tutorial.edm4hep.json)

```
edm4hep2json [olenfvh] FILEPATH.edm4hep.root
```

| **Flag**            | **Description**                                                     |
| ------------------- | ------------------------------------------------------------------- |
| **-o/--out-file**   | output file path (default: "?.edm4hep.root" --> "?.edm4hep.json")   |
| **-l/--coll-list**  | comma separated list of collections to be converted                 |
| **-e/--events**     | comma separated list of events to be processed                      |
| **-n/--nevents**    | maximal number of events to be processed                            |
| **-f/--frame-name** | input frame name (default: "events")                                |
| **-v/--verbose**    | be more verbose                                                     |
| **-h/--help**       | show this help message                                              |
 
#### Example

One can call it with  ``edm4hep2json -l ReconstructedParticles,Particle,MCRecoAssociations -e 2,4 filename.edm4hep.root``. To save only ``ReconstructedParticles``, ``Particle`` and ``MCRecoAssociations`` object collections, keeping the 2nd and 4th events in the file.  

## 2. Using eedE

Once the data has been converted into a JSON format via edm4hep2json, one can then head to [eedE](https://key4hep.github.io/eede/release/index.html). After pressing the Start button, one is required to upload the EDM4hep json file via the Browse button. You can then select the type of association (`view`) to visualize.
```{image} eede_upload.png
:align: center
:width: 600px
```

### Visualizing the Monte Carlo Particle Tree

Here we take the MC Particle Tree as an example.
In the tree shown in the picture illustrates a collision at 91 GeV, where both the electron and positron emit a ISR photon before they merge into an on-shell Z boson, which decays into a pair of b quarks.
```{image} eede_Zbb_example.png
:align: center
:width: 400px
```
For each MC particle, values for `p`, `t`, `m`, `q` represents the momentum in lab frame, time of production, invariant mass, and charge, while `d` gives the displacement from the origin of lab frame (0,0,0) to the position where the particle is produced.