
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

```
git clone https://github.com/HEP-FCC/FCCAnalyses.git
```

Go inside the directory and run

```
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

## First MVA evaluation

Here we evaluate the so called sub-optimal.
Need to add the defines from calo ntupleizer here, and point to weaver example to implement the first MVA with basic variables
https://github.com/HEP-FCC/FCCAnalyses/blob/master/examples/FCCee/test/weaver_inference.py

User need to create his own ```analysis.py``` with the basic variables and output the mva score

```
fccanalysis run caloanalysis.py --output photons_MVA1.root --files-list where the photons files are
fccanalysis run caloanalysis.py --output pi0_MVA1.root --files-list where the pi0s files are
```

Run a marco to make a plot to compare performance

## Adding new variables

In order to add new variables, we need to develop inside FCCAnalyses. For that let us create a dedicated working directory:

```
fccanalysis init --standalone --output-dir tutorial tutorialAnalysis
```
