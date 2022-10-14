
# FCC: tracking and vertexing example using specific flavour decays


:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

-   run over a specific flavour decay in **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses** and reconstruct the specific decay chain
-   build your own algorithm for a specific flavour decay inside **FCCAnalyses**
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


## Builing a custom sub-package in FCCAnalyses

In order to add new code, we need to develop inside FCCAnalyses. For that we setup a dedicated area to work using this setup script.
```shell
source ./setupUserCode.sh myAnalysis
```

We now have a new directory ```myAnalysis``` that contains both include and source files ```myAnalysis/include/myAnalysis.h``` and ```myAnalysis/src/myAnalysis.cc``` within the ```myAnalysis``` namespace.

Now you need to write some code in the header and source file to describe the missing energy.

In the header file, the function should look like

```cpp
rv::RVec<float> get_missingEnergy(const rv::RVec<edm4hep::ReconstructedParticleData>& in);
```

and in the source file, the starting point is:

```cpp
rv::RVec<float> get_missingEnergy(const rv::RVec<edm4hep::ReconstructedParticleData>& in){
  rv::RVec<float> result;

  ...

  return result;
}
```

Do not forget to add the relevant ```edm4hep``` includes in case you are using other input collections!

In your python analysis, you can now call you newly defined function, don't forget it is inside a namespace!

:::{admonition} Suggested answer
:class: toggle
```python
.Define("missingEnergy","myAnalysis::get_missingEnergy(ReconstructedParticles)")
```
:::


Last thing, do not forget to compile before running.

```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```
