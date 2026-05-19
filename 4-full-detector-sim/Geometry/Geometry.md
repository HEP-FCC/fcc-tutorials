# Changing geometry 

The description of the componentes of a particle detector can be extremely complex. `DD4hep` exploits the properties of `xml` file format to store hierarchically the geometry and materials of each component of a given detector. Thus the detector description is given in one or more `xml` files.

 In this section, the following topics are covered:
* how tow to simulate the existing detector model of the `CLD` detector
* modify its XML files
* check for overlaps with Geant4
* get a better understanding of what DD4hep does under the hood
* Write your own C++ detector constructor and run with it

This section is adapted from the [talk given by Andre Sailer](https://indico.cern.ch/event/1182767/contributions/5093486/attachments/2532164/4356996/221020_soft_tutorial_dd4hep.pdf) in the *FCC Software Tutorial 2022*.

## Setup

The first step is to set up a CentOS 7 machine with CVMFS. It can be a local machine, a remote machine (e.g. [lxplus.cern.ch](https://lxplusdoc.web.cern.ch/)), a virtual machine (e.g. [CernVM](https://cernvm.cern.ch/appliance/)) or a containerized system (e.g. [Docker](https://linux.web.cern.ch/dockerimages/), or Apptainer). 

Then, the stack with the FCC software can be sourced as 

```shell
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh 
```

The following step is to create a working directory,

```shell
mkdir mydd4heptutorial
cd mydd4heptutorial
```

Then, copy the CLD detector description into the working directory,

```shell
cp -r $LCGEO/FCCee/compact/FCCee_o1_v05 .
```

In order to plot the histograms in the terminal, the histoprint python package is used and it can be installed with the following command

```shell
pip install --user histoprint
```

If everything goes as expected, the contents of your working directory shall look this:

```shell
ls -ltra
total 8
drwxr-xr-x. 28 sailer zf 4096 Oct 14 11:29 ..
drwxr-xr-x. 3 sailer zf 26 Oct 14 11:30 .
drwxr-xr-x. 2 sailer zf 4096 Oct 14 11:30 FCCee_o1_v05
```

Another ingredient is a script to plot some information after the simulations to show that the geometry really did change. The `showPlots.py` script plots the per hit energy deposition and position along Z axis in the ECal endcap. The histograms are printed in the terminal to avoid the use of a graphical interface. If a graphical system is available, one can also visualize the geometry with `geoDisplay` or the Geant4 visualizations.

<details>

<summary><b>Click to show the code of the python script <code>showPlots.py</code> </b></summary>

```python
#!/bin/env python
import sys, ROOT
from histoprint import print_hist

ROOT.gROOT.SetBatch(True)

if len(sys.argv) < 2:
    print("Please specify input file"); sys.exit(1)
inputFile = sys.argv[1]; print("Reading:", inputFile)

tfile = ROOT.TFile.Open(inputFile)
myTree = tfile.Get("events")
myTree.Draw("ECalEndcapCollection.position.z>>zHist(100, 2300, 2510)",
            "ECalEndcapCollection.position.z > 0")
myTree.Draw("ECalEndcapCollection.energy>>eHist(30, 0, 0.002)")

print_hist(tfile.Get("zHist"), title="Hits per Layer")
print_hist(tfile.Get("eHist"), title="Energy per Hit")
```

</details>

<br/>


In this section, the detector geometry will be changed in every step. The geometry can be visualized using different tools, as it is explained in the next section. 


## Modify an existing XML file

The detector geometry is complex, and takes a while to be built. To speed up the following steps, the Silicon Tracker can be removed. To do so, 

1. Open `FCCee_o1_v05/FCCee_o1_v05.xml`
2. Find the following lines in the file, and delete/comment them

```xml
<include ref="InnerTracker_o2_v06_02.xml"/>
<include ref="OuterTracker_o2_v06_02.xml"/>
```

Remember that a comment in `xml` looks like `<!-- blablabla -->`.

3. Comment out the plugins section `<plugins> ... </plugins>` in the same file. 

To simulate the interaction of 100 muons with the CLD detector, the following command is used inside the directory `mydd4heptutorial`. It takes some minutes to build the geometry and run the actual simulation.

```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --enableGun \
      --gun.distribution uniform \
      --gun.energy "10*GeV" \
      --gun.particle mu- \
      --numberOfEvents 100 \
      --outputFile Step1_edm4hep.root
```

And now plot the distribution with `showPlots.py`

```shell
python showPlots.py Step1_edm4hep.root
```


The simulation runs 20 times faster than the full geometry simulation and the distributions do not change.

## Overlap checking

Whenever you change the geometry in a non-trivial way there are the possibilities of overlaps and the following things should be kept in mind

1. There are no trivial changes
2. See point 1
3. Run the overlap check

Geant4 can perform the overlap check of a given geometry. This action is available for `ddsim`. A macro file with the Geant4 instructions has to be provided to `ddsim`. To do so, create a file named as *overlap.mac* and write these commands inside

```
/geometry/test/run
exit
```

And then we run `ddsim` with this macro file, and dump the output to a text file for easy browsing:

```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --runType run \
      --macroFile overlap.mac > overlapDump &
```

With the full detector model including the tracker this would take about 30 minutes. The output shows some exceptions:

* The exceptions about the VertexEndcapModule are due to a too small envelope, and could be
easily fixed

* The exceptions about the Boolean Volume are more vexing, let’s ignore those for now. The HOMAbsorber include can be dropped as well to silent these errors.

## Modifying the ECAL

In this section, it is shown how to change the number of layers and silicon thicknesses of the ECal Endcap. To do so,

1. Open the file `FCCee_o1_v05/ECalEndcap_o2_v01_03.xml`
2. Find this block:
```xml
<layer repeat="40" vis="ECalLayerVis">
    <slice material = "TungstenDens24" thickness = "1.90*mm" vis="ECalAbsorberVis" radiator="yes"/>
    <slice material = "G10" thickness = "0.15*mm" vis="InvisibleNoDaughters"/>
    <slice material = "GroundOrHVMix" thickness = "0.10*mm" vis="ECalAbsorberVis"/>
    <slice material = "Silicon" thickness = "0.50*mm" sensitive="yes" limits="cal_limits"
    vis="ECalSensitiveVis"/>
    <slice material = "Air" thickness = "0.10*mm" vis="InvisibleNoDaughters"/>
    <slice material = "siPCBMix" thickness = "1.30*mm" vis="ECalAbsorberVis"/>
    <slice material = "Air" thickness = "0.25*mm" vis="InvisibleNoDaughters"/>
    <slice material = "G10" thickness = "0.75*mm" vis="InvisibleNoDaughters"/>
</layer>
```
3. Change the number of layers from **40** to **20**, and the silicon thickness from `0.50*mm` to `1.00*mm`. 

<details>

<summary><b>Click to show that piece of code from <code>FCCee_o1_v05/ECalEndcap_o2_v01_03.xml</code> after the change </b></summary>

```xml
<layer repeat="20" vis="ECalLayerVis">
    <slice material = "TungstenDens24" thickness = "1.90*mm" vis="ECalAbsorberVis" radiator="yes"/>
    <slice material = "G10" thickness = "0.15*mm" vis="InvisibleNoDaughters"/>
    <slice material = "GroundOrHVMix" thickness = "0.10*mm" vis="ECalAbsorberVis"/>
    <slice material = "Silicon" thickness = "1.00*mm" sensitive="yes" limits="cal_limits"
    vis="ECalSensitiveVis"/>
    <slice material = "Air" thickness = "0.10*mm" vis="InvisibleNoDaughters"/>
    <slice material = "siPCBMix" thickness = "1.30*mm" vis="ECalAbsorberVis"/>
    <slice material = "Air" thickness = "0.25*mm" vis="InvisibleNoDaughters"/>
    <slice material = "G10" thickness = "0.75*mm" vis="InvisibleNoDaughters"/>
</layer>
```

</details>

<br/>


Simulate again with the new ECal,

```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --enableGun \
      --gun.distribution uniform \
      --gun.energy "10*GeV" \
      --gun.particle mu- \
      --numberOfEvents 100 \
      --outputFile Step2_edm4hep.root
```

Compare the histograms produced from `Step1_edm4hep.root` and `Step2_edm4hep.root`.

## Geometry driver modifications

The type attribute of the detector tag tells DD4hep which detector constructor to load

```xml
<detector name="ECalEndcap"
          type="GenericCalEndcap_o1_v01"
          id="DetID_ECal_Endcap"
          readout="ECalEndcapCollection"
          vis="ECALVis" >
</detector>
```
DD4hep’s plugin service will look in the `*.components` files it finds via the `LD_LIBRARY_PATH` (or `DD4HEP_LIBRARY_PATH` on macOS because of SIP) environment variables, and load the library on-demand, and then instantiate the function.

For example, to know which library contains the GenericCalEndcap plugin


```shell
for DIR in $(echo $LD_LIBRARY_PATH | tr ":" " ") ; do 
    grep GenericCalEndcap $DIR/*.components 2> /dev/null; 
done
```
Usually we would add our detector to an existing project, but because overwriting existing libraries in the environment requires some work, we start with a new project. This requires two main steps, first creating a new detector constructor, and second creating the detector description in a **xml file**. Start by executing the following code inside the directory `mydd4heptutorial`, in order to create the detector constructor project

```shell
mkdir MyFirstDetector
cd MyFirstDetector
touch CMakeLists.txt
mkdir src
touch src/MyFirstDetector.cpp
```

The `CMakeLists.txt` file has to contain the following code

```cmake
cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
set(PackageName MyFirstDetector)
project(${PackageName})
find_package(DD4hep REQUIRED COMPONENTS DDG4)
# our sources
set(sources ./src/MyFirstDetector.cpp)
# create our library and make the components file
add_dd4hep_plugin(${PackageName} SHARED ${sources})
# link it with DDCore, or whatever you need
target_link_libraries(${PackageName} DD4hep::DDCore)
# Create this_package.sh file, and install
dd4hep_instantiate_package(${PackageName})
```

And the `MyFirstDetector.cpp` file has to contain the following code

```cpp
#include "DD4hep/DetFactoryHelper.h"
#include "XML/Layering.h"
#include "XML/Utilities.h"
#include "DDRec/DetectorData.h"
static dd4hep::Ref_t create_detector(
    dd4hep::Detector &theDetector,
    xml_h entities,
    dd4hep::SensitiveDetector sens)
{
    // XML Detector Element (confusingly also XML::DetElement)
    xml_det_t x_det = entities;
    // DetElement of our detector instance, attach additional information, sub-elements...
    // uses name of detector and ID number as defined in the XML detector tag
    std::string detName = x_det.nameStr();
    sens.setType("calorimeter");
    dd4hep::DetElement sdet(detName, x_det.id());
    // get the dimensions tag
    xml_dim_t dim = x_det.dimensions();
    // read its attributes
    double rmin = dim.rmin();
    double rmax = dim.rmax();
    double zmax = dim.zmax();
    // Make a Cylinder
    dd4hep::Tube envelope(rmin, rmax, zmax);
    dd4hep::Material air = theDetector.air();
    dd4hep::Volume envelopeVol(detName + "_envelope",
                               envelope,
                               air);
    dd4hep::PlacedVolume physvol =
        theDetector.pickMotherVolume(sdet).placeVolume(envelopeVol);
    // add system ID and identify as barrel (as opposed to endcap +/-1)
    physvol.addPhysVolID("system", sdet.id()).addPhysVolID(_U(side), 0);
    sdet.setPlacement(physvol);
    return sdet;
}
DECLARE_DETELEMENT(MyFirstDetector, create_detector)
```



Still inside the `MyFirstDetector` directory, execute the following shell commands,

```shell
mkdir build install
cd build
cmake -D CMAKE_INSTALL_PREFIX=$PWD/../install ..
make install
source ../install/bin/thisMyFirstDetector.sh
```

Look at `$PWD/../install` and note the content of the `bin` and `lib` directories, have a look at the `libMyFirstDetector.components` file.

After creating the detector constructor project, a detector description has to be given as a `xml` file. In the `FCCee_o1_v05` directory, create a `mydetector.xml` file with the following content

<details>

<summary><b>Click to show the code of <code>mydetector.xml</code> </b></summary>


```xml
<lccdd>

    <define>
        <constant name="ECal_cell_size" value="5.1*mm" />
    </define>

    <readouts>
        <readout name="MyReadout">
            <segmentation type="GridRPhiEta"
                grid_size_eta="ECal_cell_size" phi_bins="360"
                offset_r="ECalBarrel_inner_radius"
                grid_size_r="1*cm" />
            <id>system:5,side:2,module:8,stave:4,layer:9,submodule:4,r:32:10,eta:-11,phi:-11</id>
        </readout>
    </readouts>

    <display>
        <vis name="MyVis" alpha="0.1"
            r="0.1" g=".5" b=".5"
            showDaughters="true"
            visible="false" />
    </display>

    <detectors>
        <detector name="MyDetectorName"
            type="MyFirstDetector"
            id="1234"
            readout="MyReadout"
            vis="MyVis">
            <dimensions
                zmax="ECalBarrel_half_length"
                rmin="ECalBarrel_inner_radius"
                rmax="ECalBarrel_outer_radius" />
        </detector>
    </detectors>
    
</lccdd>
```

</details>

<br/>



Now, modify the `FCCee_o1_v05/FCCee_o1_v05.xml` and replace the include for the `ECalBarrel`
with `mydetector.xml`. After every change in the geometry, the overlap check must be run inside `FCCee_o1_v05` directory 

```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --runType run \
      --macroFile overlap.mac  > overlapDump2 &
```

If there are no exceptions, we can continue. Now, we add some layers to the detector. First, we add a `layer` component inside the `<detector> ... </detector>` section of `FCCee_o1_v05/mydetector.xml` detector description file.

<details>

<summary><b>Click to show the code of <code>mydetector.xml</code> </b></summary>

```xml
<lccdd>
    <define>
        <constant name="ECal_cell_size" value="5.1*mm" />
    </define>
    <readouts>
        <readout name="MyReadout">
            <segmentation type="GridRPhiEta"
                grid_size_eta="ECal_cell_size" phi_bins="360"
                offset_r="ECalBarrel_inner_radius"
                grid_size_r="1*cm" />
            <id>system:5,side:2,module:8,stave:4,layer:9,submodule:4,r:32:10,eta:-11,phi:-11</id>
        </readout>
    </readouts>
    <display>
        <vis name="MyVis" alpha="0.1"
            r="0.1" g=".5" b=".5"
            showDaughters="true"
            visible="false" />
    </display>
    <detectors>
        <detector name="MyDetectorName"
            type="MyFirstDetector"
            id="1234"
            readout="MyReadout"
            vis="MyVis">
            <dimensions
                zmax="ECalBarrel_half_length"
                rmin="ECalBarrel_inner_radius"
                rmax="ECalBarrel_outer_radius" />

            <layer repeat="10" vis="MyVis">
                <slice material="Iron" thickness="1*cm" />
                <slice material="G10" thickness="1*mm" />
                <slice material="Silicon" thickness="1*mm" sensitive="true" />
                <slice material="G10" thickness="1*mm" />
            </layer>

        </detector>
    </detectors>
</lccdd>
```

</details>

<br/>


In order to actually build the layers that were included in the detector description, we have to add the corresponding interpretation in the detector constructor defined in `MyFirstDetector.cpp`, which should look like the following:

<details>

<summary><b>Click to show the code of <code>MyFirstDetector.cpp</code> </b></summary>

```cpp
#include "DD4hep/DetFactoryHelper.h"
#include "DDRec/DetectorData.h"
#include "XML/Layering.h"
#include "XML/Utilities.h"
static dd4hep::Ref_t create_detector(dd4hep::Detector &theDetector,
                                     xml_h entities,
                                     dd4hep::SensitiveDetector sens) {

  // XML Detector Element (confusingly also XML::DetElement)
  xml_det_t x_det = entities;
  // DetElement of our detector instance, attach additional information,
  // sub-elements... uses name of detector and ID number as defined in the XML
  // detector tag
  std::string detName = x_det.nameStr();
  sens.setType("calorimeter");
  dd4hep::DetElement sdet(detName, x_det.id());

  // get the dimensions tag
  xml_dim_t dim = x_det.dimensions();
  // read its attributes
  double rmin = dim.rmin();
  double rmax = dim.rmax();
  double zmax = dim.zmax();
  // Make a Cylinder
  dd4hep::Tube envelope(rmin, rmax, zmax);
  dd4hep::Material air = theDetector.air();
  dd4hep::Volume envelopeVol(detName + "_envelope", envelope, air);
  dd4hep::PlacedVolume physvol =
      theDetector.pickMotherVolume(sdet).placeVolume(envelopeVol);
  // add system ID and identify as barrel (as opposed to endcap +/-1)
  physvol.addPhysVolID("system", sdet.id()).addPhysVolID(_U(side), 0);
  sdet.setPlacement(physvol);

  // Interpretation of layers: 
  double currentInnerRadius = rmin; // running inner radius
  dd4hep::Layering layering(x_det); // convenience class
  int layerNum = 0;
  for (xml_coll_t c(x_det, _U(layer)); c; ++c, ++layerNum) {
    xml_comp_t x_layer = c;
    const dd4hep::Layer *lay =
        layering.layer(layerNum); // Get the layer from the layering engine.
    const double layerThickness = lay->thickness();
    // loop over the number of repetitions
    for (int i = 0, repeat = x_layer.repeat(); i < repeat; ++i, ++layerNum) {
      std::string layerName = detName + dd4hep::_toString(layerNum, "_layer%d");
      // make a volume for the layer
      dd4hep::Tube layerTube(currentInnerRadius,
                             currentInnerRadius + layerThickness, zmax);
      dd4hep::Volume layerVol(layerName, layerTube, air);
      dd4hep::DetElement layerElement(sdet, layerName, layerNum);
      dd4hep::PlacedVolume layerVolPlaced = envelopeVol.placeVolume(layerVol);
      layerVolPlaced.addPhysVolID("layer", layerNum);
      int sliceNum = 0;
      for (xml_coll_t slice(x_layer, _U(slice)); slice; ++slice, ++sliceNum) {
        xml_comp_t x_slice = slice;
        double sliceThickness = x_slice.thickness();
        dd4hep::Material sliceMat = theDetector.material(x_slice.materialStr());
        std::string sliceName =
            layerName + dd4hep::_toString(sliceNum, "slice%d");
        dd4hep::Tube sliceTube(currentInnerRadius,
                               currentInnerRadius + sliceThickness, zmax);
        dd4hep::Volume sliceVol(sliceName, sliceTube, sliceMat);
        if (x_slice.isSensitive()) {
          sliceVol.setSensitiveDetector(sens);
        }
        // place the slice in the layer
        layerVol.placeVolume(sliceVol);
        currentInnerRadius += sliceThickness;
      } // slices
    }   // repetitions
  }     // layers

  return sdet;
}
DECLARE_DETELEMENT(MyFirstDetector, create_detector)
```

</details>

<br/>


To take effect, the code has to be recompiled,


```shell
cd MyFirstDetector/build
make install
```

After every change in the geometry, the overlap check must be run. To do so, go to the top working directory and run it as before


```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --runType run \
      --macroFile overlap.mac  > overlapDump3 &
```

The number of checks now increased, and if everything is done properly, no overlaps are found. Now the geometry is ready to go for a simulation. As it was done previously, we use `ddsim` to run a simulation of 100 muons in the geometry that has just been defined, as in the previous steps

```shell
ddsim --compactFile FCCee_o1_v05/FCCee_o1_v05.xml \
      --enableGun \
      --gun.distribution uniform \
      --gun.energy "10*GeV" \
      --gun.particle mu- \
      --numberOfEvents 100 \
      --outputFile Step3_edm4hep.root
```

Modify `showPlots.py` to display properties from this collection (MyReadout).


<details>

<summary><b>Click to show the code of the python script <code>showPlots.py</code> </b></summary>

```python
#!/bin/env python
import sys, ROOT
from histoprint import print_hist
ROOT.gROOT.SetBatch(True)
if len(sys.argv) < 2:
  print("Please specify input file"); sys.exit(1)
inputFile = sys.argv[1]; print("Reading:", inputFile)
tfile = ROOT.TFile.Open(inputFile)
myTree = tfile.Get("events")
myTree.Draw("sqrt(MyReadout.position.x*MyReadout.position.x+MyReadout.position.y*MyReadout.position.y)>>rHist(100, 2150, 2352)")
myTree.Draw("MyReadout.energy>>eHist(30, 0, 0.002)")
print_hist(tfile.Get("rHist"), title="Hits per Layer")
print_hist(tfile.Get("eHist"), title="Energy per Hit")

```

</details>

<br/>

## Final note

Changing geometries with DD4hep can range from trivial to sophisticated. The overlap checker shall be run after every change. 

Check the following links for further information and support:

1. Browse the [DD4hep documentation](https://dd4hep.web.cern.ch/dd4hep/) and [beginners guide](https://dd4hep.web.cern.ch/dd4hep/page/beginners-guide/)
2. Ask at [https://github.com/aidasoft/dd4hep](https://github.com/aidasoft/dd4hep)
3. Post your questions or suggestions at FCC software [forum](https://fccsw-forum.web.cern.ch/) or [Mattermost channel](https://mattermost.web.cern.ch/fccsw/)

<br/>
