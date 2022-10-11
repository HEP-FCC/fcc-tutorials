
# FCC-ee photon/pi0 discrimination using noble liquid calorimeter



:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

* produce flat ntuples from full simulation samples using FCCAnalyses
* infer state of the art deep learning within FCCAnalyses
* produce discrimination **plots** single photons/pi0
:::

## Installation of FCCAnalyses
For this tutorial we will need to develop some code inside FCCAnalyses, thus we need to install it locally.
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
#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

        ]
        return branchList
```

At the top of the file, define the special variables needed to load the DD4Hep geometry:

```python
geometryFile = "/afs/cern.ch/user/b/brfranco/work/public/Fellow/FCCSW/test_recipe_April2022/FCCDetectors/Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml"
readoutName  = "ECalBarrelPhiEta"
```

Let's now ```Define``` variables to the RootDataFrame object ```df2``` inside the function ```analysers``` of the class ```RDFanalysis```:

```python
.Define("maxEnergyInSecondLayer",               "CaloNtupleizer::getCaloCluster_maxEnergyInLayer(CaloClusters, ECalBarrelPositionedCells, 1)")
.Define("secondMaxEnergyInSecondLayer",         "CaloNtupleizer::getCaloCluster_secondMaxEnergyInLayer(CaloClusters, ECalBarrelPositionedCells, 1)")
.Define("energyInSecondLayerOverClusterEnergy", "CaloNtupleizer::getCaloCluster_energyInLayerOverClusterEnergy(CaloClusters, ECalBarrelPositionedCells, 1)")
.Define("distBetweenMaximaInSecondLayer",       "CaloNtupleizer::getCaloCluster_distBetweenMaximaInLayer(CaloClusters, ECalBarrelPositionedCells, 1)")
```

And add the variables to the ```branchList``` of the ```output``` function of the same ```RDFanalysis``` class:

```python
'maxEnergyInSecondLayer','secondMaxEnergyInSecondLayer','energyInSecondLayerOverClusterEnergy','distBetweenMaximaInSecondLayer'
```

And let's run to check that everything is fine:

```shell
fccanalysis run analysis_tutorial_mva.py --output pion_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```
Note that if you have already produced full simulation pions and photons with the calorimeter tutorial, you can change the file to point to yours

Now we add the weaver part at the begining of the ```analysers``` function:

TO BE UPDATED WITH GENERIC INTERFACE
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

Finally add the newly defined variable to the ```branchList``` in the ```output``` function and run:

```shell
fccanalysis run analysis_tutorial_mva.py --output pion_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_111_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
fccanalysis run analysis_tutorial_mva.py --output pion_MVA1.root --files-list /eos/experiment/fcc/ee/tutorial/pi0GammaLAr2022/edm4hepFormat/fccsw_output_pdgID_22_pMin_1000_pMax_100000_thetaMin_50_thetaMax_130.root
```

Run a marco to make a plot to compare performance (NEED TO WRITE SOMETHING??)

## Adding new variables

In order to add new variables, we need to develop inside FCCAnalyses. For that let us first define the output directory and properly add it to the environemnt variables

```shell
OUTPUT_DIR=${LOCAL_DIR}/tutorial_analysis
LD_LIBRARY_PATH=${LOCAL_DIR}/install:${LD_LIBRARY_PATH}
PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
PATH=${LOCAL_DIR}/bin:${LOCAL_DIR}:${PATH}
ROOT_INCLUDE_PATH=${LOCAL_DIR}/install:${ROOT_INCLUDE_PATH}
```

Now we set it up

```shell
fccanalysis init my_tutorial_analysis --output-dir ${OUTPUT_DIR} --standalone
```

We now have a new directory ```tutorial_analysis``` that contains a ```DummyAnalysis``` within ```my_tutorial_analysis``` namespace.

Now you need to add in ```tutorial_analysis/include/DummyAnalysis.h``` and ```tutorial_analysis/src/DummyAnalysis.cc``` the descriptions of the variables to be added to the MVA. You will also need to add them in the python (new ```Define```s) create a new weaver to evaluate with all the variables.

Last thing, do not forget to compile before

```
OLDPWD=${PWD}
mkdir -p ${OUTPUT_DIR}/build && cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${OLDPWD}
```

and run again

```
fccanalysis run caloanalysis.py --output photons_MVA1.root --files-list where the photons files are
fccanalysis run caloanalysis.py --output pi0_MVA1.root --files-list where the pi0s files are
```
