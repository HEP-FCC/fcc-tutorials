
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

In order to add new code, we need to develop inside FCCAnalyses. For that let us first define the output directory and properly add it to the environment variables

```shell
OUTPUT_DIR=${LOCAL_DIR}/tutorial_analysis
LD_LIBRARY_PATH=${LOCAL_DIR}/install:${LD_LIBRARY_PATH}
PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
PATH=${LOCAL_DIR}/bin:${LOCAL_DIR}:${PATH}
ROOT_INCLUDE_PATH=${LOCAL_DIR}/install:${ROOT_INCLUDE_PATH}
OLDPWD=${PWD}
mkdir -p ${OUTPUT_DIR}/build
```

Now we set it up

```shell
fccanalysis init my_tutorial_analysis --output-dir ${OUTPUT_DIR} --name myAnalysis --standalone
```

We now have a new directory ```tutorial_analysis``` that contains a ```myAnalysis``` within ```my_tutorial_analysis``` namespace.

Now you need to add in ```tutorial_analysis/include/myAnalysis.h``` and ```tutorial_analysis/src/myAnalysis.cc``` the description of the missing energy variable

In the header file, the function should look like

```cpp
rv::RVec<float> get_missingEnergy(const rv::RVec<edm4hep::ReconstructedParticleData>& in);
```

Do not forget to add the relevant ```edm4hep``` includes!

and in the source file, the starting point is:

```cpp
rv::RVec<float> get_missingEnergy(const rv::RVec<edm4hep::ReconstructedParticleData>& in){
  rv::RVec<float> result;

  ...

  return result;
}
```

In your python analysis, you can now call you newly defined function, don't forget it is inside a namespace!

:::{admonition} Suggested answer
:class: toggle
```python
.Define("missingEnergy","my_tutorial_analysis::get_missingEnergy(ReconstructedParticle)")
```
:::


Last thing, do not forget to compile before

```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${OLDPWD}
```

## Generalities and references

## Reconstruction of the primary vertex and of primary tracks

```shell
fccanalysis run examples/tutorial2022_vertexing/analysis_primary_vertex.py --test --nevents 1000 --output primary_Zuds.root
```

The resulting ntuple contains the MC event vertex (MC_PrimaryVertex), the reconstructed primary vertex (FinalVertex), and vectors of booleans that tell whether a track was flagged as a primary track when using the MC-truth information (IsPrimary_based_on_MC), or when using the algorithm (IsPrimary_based_on_reco).
Example plots: run the ROOT macro plots_primary_vertex.x

### Exercises:
- add variables to the ntuple: the number of primary and secondary tracks, obtained when matching the tracks to the MC-truth, and obtained from the algorithm
- add the total p or pT that is carried by the primary and secondary tracks. This requires some simple analysis code to be written and compiled.
- compare these distributions in Z -> uds events and in Z -> bb events


## Reconstruction of displaced vertices in an exclusive decay chain

Starting example: Z -> bb events where one b leg hadronizes to Bs, and the Bs is forced to decay into J/Psi (mumu) Phi (K+ K-).

```shell
fccanalysis run analysis_Bs2JpsiPhi.py  --test --nevents 1000 --output Bs2JpsiPhi_MCseeded.root
```

( NB: I need to reproduce the example file. This one is old, was done with the older evtgen, events were not forced to hadronise to a Bs )

The ntuple contains the MC decay vertex of the Bs, and the reconstructed decay vertex. The root macro plots_Bs2JsiPhi.x produces various plots showing the vertex chi2, the vertex resolutions and the pulls of the vertex fit.

## Exercise: analysis of tau -> 3 mu

1. Start from analysis_Bs2JpsiPhi.py and adapt it to the decay tau -> 3 mu.  (example file to be produced )
2. Add the reconstructed tau mass to the ntuple (you will need to write new code). You can check that the mass resolution is improved when it is determined from the track momenta **at the tau decay vertex**, compared to a blunt 3-muon mass determined from the default track momenta (taken at theis distance of closest approach).
3. So far, everything was done using "Monte-Carlo seeding", which gives the resolutions that we expect, in the absence of possible combinatoric issues. The next step is to write a new analysis.py which starts from the reconstructed muons.
   - select combinations of three muons with total charge = +/- 1
   - fit the three muons to a common vertex and reconstruct the tau mass
4. Look at the tau -> 3 pi nu background. 
  
        

