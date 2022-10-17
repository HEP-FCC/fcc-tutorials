
# FCC-ee photon/pi0 discrimination using noble liquid calorimeter

:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

* produce flat ntuples from full simulation samples using FCCAnalyses
* infer state of the art deep learning within FCCAnalyses
* produce discrimination **plots** single photons/pi0
:::

## Installation of FCCAnalyses
For this tutorial we will need to develop some code inside FCCAnalyses, thus we need to install it locally. If not already done, you need to clone and install it.
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

## First MVA evaluation

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

And let's run on a few events to check that everything is fine **NEED TO CHANGE THE INPUT FILE**.
To find the options to configure the code to run on a few (10) events using as input file ```pathtorootfile``` and to store an output file ```pion_MVA1.root``` using the command:

```shell
fccanalysis run --help
```

:::{admonition} Suggested answer
:class: toggle
```shell
fccanalysis run analysis_tutorial_mva.py --nevents 10 --output pions_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```
:::

Note that if you have already produced full simulation pions and photons with the calorimeter tutorial earlier this morning, you can change the file to point to your files.

Open the produced root file ```pions_MVA1.root``` and inspect it with ```Scan``` for example check that the index we have calculated indeed correspond to the clusters of maximum/minimum energy:

:::{admonition} Suggested answer
:class: toggle
```shell
root -l pions_MVA1.root
events->Scan("maxEnergyCluster_index:minEnergyCluster_index:clusters_n:clusters_energy")
```
:::

We now need to obtain the index of the first and last cells of the maximum energy cluster. For that we need to select the ```maxEnergyCluster_index``` in the ```CaloClusters``` collection and evaluate ```hits_begin``` and ```hits_end```:

:::{admonition} Suggested answer
:class: toggle
```python
.Define("maxEnergyCluster_firstCell_index", "CaloClusters[maxEnergyCluster_index].hits_begin")
.Define("maxEnergyCluster_lastCell_index", "CaloClusters[maxEnergyCluster_index].hits_end")
```
:::

Using the positions of the first and last cells in the ```PositionedCaloClusterCells``` collection we now need to create a sub-collection from the full collection between the two indices. To achieve this with the ROOT version in this tutorial, we need to declare some extra code at the beginning of our analysis file:

```python
import ROOT
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
fccanalysis run analysis_tutorial_mva.py --nevents 10 --output pions_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```
:::

Now we add the weaver part at the beginning of the ```analysers``` function:

**TO BE UPDATED WITH GENERIC INTERFACE**
```python
from ROOT import JetFlavourUtils
from os import getenv
test_inputs_path = getenv('TEST_INPUT_DATA_DIR', '/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX')
weaver = JetFlavourUtils.setup_weaver(test_inputs_path + '/fccee_flavtagging_dummy.onnx',
                                      test_inputs_path + '/preprocess.json',
                                      ('pfcand_e', 'pfcand_theta', 'pfcand_phi', 'pfcand_pid', 'pfcand_charge'))
```

and the evaluation after the definition of the variables:

```python
.Define("MVAVec", "JetFlavourUtils::get_weights(JC_e, JC_theta, JC_phi, JC_pid, JC_charge)")
```

and the get the weights:
```python
.Define("Jet_isG", "JetFlavourUtils::get_weight(MVAVec, 0)")
.Define("Jet_isQ", "JetFlavourUtils::get_weight(MVAVec, 1)")
.Define("Jet_isS", "JetFlavourUtils::get_weight(MVAVec, 2)")
.Define("Jet_isC", "JetFlavourUtils::get_weight(MVAVec, 3)")
.Define("Jet_isB", "JetFlavourUtils::get_weight(MVAVec, 4)")
```

Finally add the newly defined variable to the ```branchList``` in the ```output``` function and run over the full statistics

```shell
fccanalysis run analysis_tutorial_mva.py --output pions_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
fccanalysis run analysis_tutorial_mva.py --output photons_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_22_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```

Run a marco to make a plot to compare performance (NEED TO WRITE SOMETHING??)

## Removing the last layers

In this section we will remove the last layers of the calorimeter and evaluate the same MVA model with less layers. First let's have a look at one the output file and try to find how many layers we have in the calorimeter. For that plot the number of layers for a few events and look at the histogram

:::{admonition} Suggested answer
:class: toggle
```shell
events->Draw("maxEnergyCluster_cells_layer","","",10)
```
:::

Now you produce new file removing the last layer of the calorimeter adding a ```Filter``` after all the ```Define```

:::{admonition} Suggested answer
:class: toggle
```python
.Filter("maxEnergyCluster_cells_layer<11")
```
:::

:::{admonition} Suggested answer
:class: toggle
```shell
fccanalysis run analysis_tutorial_mva.py --output pions_MVA2.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
fccanalysis run analysis_tutorial_mva.py --output photons_MVA2.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_22_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```
:::

Compare the performance of the two MVAs and comment.
