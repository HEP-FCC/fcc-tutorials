
# FCC-ee photon/pi0 discrimination using noble liquid calorimeter

:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

* produce flat ntuples from full simulation samples using FCCAnalyses
* infer state of the art deep learning within FCCAnalyses
* produce discrimination **plots** single photons/pi0
:::

## Installation of FCCAnalyses
For this tutorial we will need to use FCCAnalyses. We can either use it from the stack, or if you have it installed locally use it. If you want to install it, you need to clone and install it.
Go inside the area that you have setup for the tutorials and get the FCCAnalyses code:

```shell
git clone https://github.com/HEP-FCC/FCCAnalyses.git
```

Go inside the directory and run

```shell
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

## Build FCCAnalyses skeleton

We start by creating a file named ```analysis_tutorial_mva.py``` (or any other name you prefer to use) with the following information.

```python
# Mandatory: RDFanalysis class where the user defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    # Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

              )
        return df2

    #__________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

        ]
        return branchList
```

At the top of the file, we need to define special variables needed to load the DD4Hep geometry, but first we need to get the path where they are located from the python code:

```python
# get the environment variable FCCDETECTORS
from os import getenv
FCCDETECTORS = getenv("FCCDETECTORS")
# define geometryFile and readoutName to load a DD4Hep detector and readout
geometryFile = FCCDETECTORS + "/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml"
readoutName  = "ECalBarrelPhiEta"
```

At the top of the file, also add `tesFile=` to point to where your files are located from the calorimeter full simulation tutorial. If you do not have those files, you can use those two:

```shell
testFile='/eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat_smallSampleNotUsedForTraining/output_caloFullSim_10GeV_pdgId_22_noiseFalse.root'
#testFile='/eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat_smallSampleNotUsedForTraining/output_caloFullSim_10GeV_pdgId_111_noiseFalse.root'
```

## Get the highest energetic cluster

Let's now define new columns to the RootDataFrame object ```df2``` inside the function ```analysers``` of the class ```RDFanalysis```. We start by defining the index in the collection ```CaloClusters``` which is of type [ClusterData](https://edm4hep.web.cern.ch/_cluster_data_8h_source.html) of the cluster with maximum energy:

```python
.Define("maxEnergyCluster_index", "std::distance(CaloClusters.energy.begin(), std::max_element(CaloClusters.energy.begin(), CaloClusters.energy.end()))")
```

Similarly, define the index in the collection ```CaloClusters``` of the cluster with minimum energy, the total number of clusters in the event and the cluster energy.

:::{admonition} Suggested answer
:class: toggle
```python
.Define("minEnergyCluster_index", "std::distance(CaloClusters.energy.begin(), std::min_element(CaloClusters.energy.begin(), CaloClusters.energy.end()))")
.Define("clusters_n", "CaloClusters.energy.size()")
.Define("clusters_energy", "CaloClusters.energy")
```
:::

Now we need to add all the variables that we have defined to the ```branchList``` of the ```output``` function of the same ```RDFanalysis``` class.

:::{admonition} Suggested answer
:class: toggle
```python
"maxEnergyCluster_index", "minEnergyCluster_index", "clusters_n", "clusters_energy"
```
:::

And let's run on a few events to check that everything is fine.
To find the options to configure the code to run on a few (10) events using as input file the test file in the python `testFile` and to store an output file ```photons.root``` using the command:

```shell
fccanalysis run --help
```

:::{admonition} Suggested answer
:class: toggle
```shell
fccanalysis run analysis_tutorial_mva.py --nevents 10 --output photons.root --test
```
:::

Open the produced root file ```photons.root``` and inspect it with ```Scan``` for example check that the index we have calculated indeed correspond to the clusters of maximum/minimum energy:

:::{admonition} Suggested answer
:class: toggle
```shell
root -l photons.root
events->Scan("maxEnergyCluster_index:minEnergyCluster_index:clusters_n:clusters_energy")
```
:::

## Get the list of cells from the cluster

We now need to obtain the index of the first and last cells of the maximum energy cluster. For that we need to select the ```maxEnergyCluster_index``` in the ```CaloClusters``` collection and evaluate ```hits_begin``` and ```hits_end```:

:::{admonition} Suggested answer
:class: toggle
```python
.Define("maxEnergyCluster_firstCell_index", "CaloClusters[maxEnergyCluster_index].hits_begin")
.Define("maxEnergyCluster_lastCell_index",  "CaloClusters[maxEnergyCluster_index].hits_end")
```
:::

## Create sub-collection of cells

Using the positions of the first and last cells in the ```PositionedCaloClusterCells``` collection we now need to create a sub-collection from the full collection between the two indices. To achieve this with the ROOT version in this tutorial, we need to declare some extra code after the definition of the `analysers` function:

```python
ROOT.gInterpreter.Declare("""
template<typename T>
ROOT::VecOps::RVec<T> myRange(ROOT::VecOps::RVec<T>& vec, std::size_t begin, std::size_t end)
{
   ROOT::VecOps::RVec<T> ret;
   ret.reserve(end - begin);
   for (auto i = begin; i < end; ++i)
      ret.push_back(vec[i]);
   return ret;
}
""")
```

Note, With the root version used for this tutorial (```ROOT v6.26```) it is not possible to do this inline, while from ```ROOT v6.28``` it will be possible using ```Take``` and ```Range```:

```python
Take(vec, Range(id_end - id_begin) + id_begin)
```

Now you can create the sub-collection ```maxEnergyCluster_Cells``` from the input collection ```PositionedCaloClusterCells``` from ```maxEnergyCluster_firstCell_index``` to ```maxEnergyCluster_lastCell_index``` using the newly defined ```myRange``` function:

:::{admonition} Suggested answer
:class: toggle
```python
.Define("maxEnergyCluster_cells", "myRange(PositionedCaloClusterCells, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
```
:::

## Create collection of cells observables

Using the newly defined collection ```maxEnergyCluster_cells```, create new variables of their energies, phi, theta, layer and number of cells, using functions like [here](https://github.com/HEP-FCC/FCCAnalyses/blob/master/analyzers/dataframe/FCCAnalyses/CaloNtupleizer.h#L23#L33)

:::{admonition} Suggested answer
:class: toggle
```python
.Define("maxEnergyCluster_cells_energy", "CaloNtupleizer::getCaloHit_energy(maxEnergyCluster_cells)" )
.Define("maxEnergyCluster_cells_phi",    "CaloNtupleizer::getCaloHit_phi(maxEnergyCluster_cells)" )
.Define("maxEnergyCluster_cells_theta",  "CaloNtupleizer::getCaloHit_theta(maxEnergyCluster_cells)" )
.Define("maxEnergyCluster_cells_layer" , "CaloNtupleizer::getCaloHit_layer(maxEnergyCluster_cells)" )
.Define("maxEnergyCluster_cells_n" ,     "maxEnergyCluster_cells.size()" )
```
:::

The last variable to add is the radius of the cell position, you can compute it inline defining first collections ```maxEnergyCluster_cells_x``` and ```maxEnergyCluster_cells_y```. Hint you need to use the ```myRange``` function ```PositionedCaloClusterCells``` and the ```position``` attribute of the collection which is of type ```edm4hep::CalorimeterHitData``` [see here](https://edm4hep.web.cern.ch/classedm4hep_1_1_calorimeter_hit_data.html) and you need to calculate the radius as usual with ```x``` and ```y```.


:::{admonition} Suggested answer
:class: toggle
```python
.Define("maxEnergyCluster_cells_x", "myRange(PositionedCaloClusterCells.position.x, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
.Define("maxEnergyCluster_cells_y", "myRange(PositionedCaloClusterCells.position.y, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
.Define("maxEnergyCluster_cells_radius", "sqrt(pow(maxEnergyCluster_cells_x,2)+pow(maxEnergyCluster_cells_y,2))")
```
:::

Do not forget to add all the newly defined variables to the output ```branchList```.

:::{admonition} Suggested answer
:class: toggle
```python
"maxEnergyCluster_cells_energy","maxEnergyCluster_cells_phi","maxEnergyCluster_cells_theta","maxEnergyCluster_cells_layer","maxEnergyCluster_cells_n","maxEnergyCluster_cells_radius"
```
:::

Let's give it a try on a few events as last time.

:::{admonition} Suggested answer
:class: toggle
```shell
fccanalysis run analysis_tutorial_mva.py --nevents 10 --output photons.root --test
```
:::

## Adding the MVA inference

Now we add the weaver part at the beginning of the ```analysers``` function:


```python
from ROOT import WeaverUtils
from os import getenv
test_inputs_path = getenv('TEST_INPUT_DATA_DIR', '/eos/experiment/fcc/ee/tutorial/PNet_pi0Gamma/v1')
weaver = WeaverUtils.setup_weaver(test_inputs_path + '/fccee_pi_vs_gamma_v1.onnx',
                                      test_inputs_path + '/preprocess_fccee_pi_vs_gamma_v1.json',
                                      ('recocells_e', 'recocells_theta', 'recocells_phi', 'recocells_radius', 'recocells_layer'))

```

We need to transform our collection of cells observables in a vector as we might want to evaluate several cluster in the same event:

```python
# retrieve all information about jet constituents for each jet in collection
.Define("cells_e",         "Utils::as_vector(maxEnergyCluster_cells_energy)")
.Define("cells_theta",     "Utils::as_vector(maxEnergyCluster_cells_theta)")
.Define("cells_phi",       "Utils::as_vector(maxEnergyCluster_cells_phi)")
.Define("cells_radius",    "Utils::as_vector(maxEnergyCluster_cells_radius)")
.Define("cells_layer",     "Utils::as_vector(maxEnergyCluster_cells_layer)")
```

Then we evaluate the network:
```python
 .Define("MVAVec", "WeaverUtils::get_weights(cells_e, cells_theta, cells_phi, cells_radius, cells_layer)")
```

and retrieve the weights

```python
 .Define("Cluster_isPhoton", "WeaverUtils::get_weight(MVAVec, 0)")
 .Define("Cluster_isPi0",    "WeaverUtils::get_weight(MVAVec, 1)")

```

Finally add the newly defined variable to the ```branchList``` in the ```output``` function and run over the full statistics. Do not forget to change the `testFile` when switching pi0, photon

```shell
fccanalysis run analysis_tutorial_mva.py --output pi0s.root --test
fccanalysis run analysis_tutorial_mva.py --output photons.root --test
```

## Removing the last layers

In this section we will remove the last layers of the calorimeter and evaluate the same MVA model with less layers. First let's have a look at one the output file and try to find how many layers we have in the calorimeter. For that plot the number of layers for a few events and look at the histogram

:::{admonition} Suggested answer
:class: toggle
```shell
events->Draw("maxEnergyCluster_cells_layer","","",10)
```
:::

Now you produce new file removing the last 2 layers of the calorimeter adding a filter on the cells.
Need to comment one the definition of the cells collection and add the two lines below


```python
#.Define("maxEnergyCluster_cells", "myRange(PositionedCaloClusterCells, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
.Define("maxEnergyCluster_cellsFull", "myRange(PositionedCaloClusterCells, maxEnergyCluster_firstCell_index, maxEnergyCluster_lastCell_index)")
.Define("maxEnergyCluster_cells", ROOT.CaloNtupleizer.sel_layers(0, 10),["maxEnergyCluster_cellsFull"])
```

and we run again (don't forget to switch the testFile)
:::{admonition} Suggested answer
:class: toggle
```shell
fccanalysis run analysis_tutorial_mva.py --output pi0s_10layers.root --test
fccanalysis run analysis_tutorial_mva.py --output photons_10layers.root --test
```
:::

## Compare the performance

We get the following plotting scripts
```shell
wget https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/master/full-detector-simulations/FCCeeCaloPhotonPi0Discrimination/draw_rocCurve_pi0_gamma_GNN.py
wget https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/master/full-detector-simulations/FCCeeCaloPhotonPi0Discrimination/rocCurveFacility.py
```

Edit `draw_rocCurve_pi0_gamma_GNN.py` and edit the following:
```python
#Where your files are
input_file_path = ""
#name of your files
pi0_file = os.path.join(input_file_path, "pi0s.root")
photon_file = os.path.join(input_file_path, "photons.root")
#output name
output_string_suffix = ""
```

and run first with the full layers
```shell
python draw_rocCurve_pi0_gamma_GNN.py
```

change the name to use the 10 layers files
```python
#name of your files
pi0_file = os.path.join(input_file_path, "pi0s_10layers.root")
photon_file = os.path.join(input_file_path, "photons_10layers.root")
#output name
output_string_suffix = "_10layers"
```

and run again with only 10 layers
```shell
python draw_rocCurve_pi0_gamma_GNN.py
```

look at the produced plot and compare the performance.
