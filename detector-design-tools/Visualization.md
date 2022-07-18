# Visualization

## Phoenix@FCC

[Phoenix](https://github.com/HSF/phoenix) is a web based event display for High
Energy Physics. To visualize FCC events one needs to provide detector geometry
and generated events.


### Detector Geometry

There are several ways how to import FCC detector geometry into Phoenix.
Currently the most preferred method is to convert compact DD4hep file(s) to
ROOT files and from ROOT files to GLtf files. The first conversion
(`.xml` -> `.root`) is straightforward and can be done using script like this:

```python
#!/usr/bin/env python3

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert detector')
    parser.add_argument('-c', '--compact', help='Compact file location(s)',
                        required=True, type=str, nargs='+')
    parser.add_argument('-o', '--out', help='Converted file path',
                        default='detector.root', type=str)
    args = vars(parser.parse_args())

    convert(args['compact'], args['out'])


def convert(compact_files, out_path):
    print('INFO: Converting following compact file(s):')
    for cfile in compact_files:
        print('      ' + cfile)

    import ROOT

    ROOT.gSystem.Load('libDDCore')
    description = ROOT.dd4hep.Detector.getInstance()
    for cfile in compact_files:
        description.fromXML(cfile)

    ROOT.gGeoManager.SetVisLevel(9)
    ROOT.gGeoManager.SetVisOption(0)
    ROOT.gGeoManager.Export(out_path)


if __name__ == '__main__':
    main()

```

Second conversion (`.root` -> `.gltf`) requires inclusion of additional
information about the geometry and is done using the
[root_cern-To_gltf-Exporter](https://github.com/HSF/root_cern-To_gltf-Exporter).
One can create hierarchy menu, suppress drawing of volumes which are too small
and so on. The example for FCCee Lar Calo:

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

    // for each level of hierarchy in the phoenix menu, tell which parts of the geometry to
    // use and whether they are initially visible or not.
    var subparts = {
        "Cryo > Front" : [["ECAL_Cryo_front_0"], .8],
        "Cryo > Back" : [["ECAL_Cryo_back_1"], .8],
        "Cryo > Sides" : [["ECAL_Cryo_side_2"], .8],
        "Services > _Front" : [["services_front_3"], .6],
        "Services > _Back" : [["services_back_4"], .6],
        "Bath": [["LAr_bath_5"], true]
    }

    convertGeometry("./fccee-lar-ecal.root", "fccee-lar-ecal.gltf",
                    4, subparts, hide_children, "default", 120);

  </script>
</body>
```

Already converted geometry for the FCCee LAr Calorimeter imported into Phoenix
application can be found [here](https://kjvbrt.github.io/fcc-viewer/).


## [WIP] Event data

First one needs to have some events generated:
```
fccrun Reconstruction/RecFCCeeCalorimeter/options/runCaloSim.py  \
       --filename fccee_LAr_idea_pgun.root \
       -n 10
```

and then using `edm4hep2json` converter convert EDM4hep `.root` file into
`.json` file which can be uploaded to the Phoenix application. Converter is
WIP and is currently hosted in the EDM4hep fork
[here](https://github.com/kjvbrt/EDM4hep/tree/edm4hep2json). After compilation
of the `edm4hep2json` branch you should be able to run the converter using
```
./build/tools/edm4hep2json -i input_edm4hep.root
```

After successful conversion one can use upload button in Phoenix interface and
upload event data to be displayed.
