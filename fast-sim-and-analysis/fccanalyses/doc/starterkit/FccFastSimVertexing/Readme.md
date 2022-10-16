
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
fccanalysis run analysis_primary_vertex.py --test --nevents 1000 --output primary_Zuds.root
```

The resulting ntuple contains the MC event vertex (MC_PrimaryVertex), the reconstructed primary vertex (PrimaryVertex).
Snippet of analysis_primary_vertex.py:

```python
  # MC event primary vertex
  .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

  # Fit all tracks of the events to a common vertex  - here using a beam-spot constraint:

  # VertexObject_allTracks is an object of type VertexingUtils::FCCAnalysesVertex
  # It contains in particular :
  #  - an edm4hep::VertexData :
  #        std::int32_t primary{}; ///< boolean flag, if vertex is the primary vertex of the event
  #        float chi2{}; ///< chi-squared of the vertex fit
  #        ::edm4hep::Vector3f position{}; ///< [mm] position of the vertex.
  #        std::array<float, 6> covMatrix{}; ///< covariance matrix of the position 
  #           (stored as lower triangle matrix, i.e. cov(xx),cov(y,x),cov(z,x),cov(y,y),... )
  # - ROOT::VecOps::RVec<float> reco_chi2 : the contribution to the chi2 of all tracks used in the fit
  # - ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex : the post-fit (px, py, pz ) 
  #         of the tracks, at the vertex (and not at their d.c.a.)
  
  .Define("VertexObject_allTracks",  "VertexFitterSimple::VertexFitter_Tk ( 1, EFlowTrack_1, true, 4.5, 20e-3, 300)")

  # EFlowTrack_1 is the collection of all tracks (the fitting method can of course be applied to a subset of tracks (see later)).
  # "true" means that a beam-spot constraint is applied. Default is no BSC. Following args are the BS size and position, in mum :
  #                                   bool BeamSpotConstraint = false,
  #                                   double sigmax=0., double sigmay=0., double sigmaz=0.,
  #                                   double bsc_x=0., double bsc_y=0., double bsc_z=0. )  ;


  # This returns the  edm4hep::VertexData :
  .Define("Vertex_allTracks",  "VertexingUtils::get_VertexData( VertexObject_allTracks )")   # primary vertex, in mm


  # This is not a good estimate of the primary vertex: even in a Z -> uds event, there 
  # are displaced tracks (e.g. Ks, Lambdas), which would bias the fit.
  # Below, we determine the "primary tracks" using an iterative algorithm - cf LCFI+.
  .Define("RecoedPrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( VertexObject_allTracks, EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0., 0)")

  # Now we run again the vertex fit, but only on the primary tracks :
  .Define("PrimaryVertexObject",   "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ")
  .Define("PrimaryVertex",   "VertexingUtils::get_VertexData( PrimaryVertexObject )")

  # It is often useful to retrieve the secondary (i.e. non-primary) tracks, for example to search for secondary vertices. 
  # The method below simply "subtracts" the primary tracks from the full collection :
  .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1,  RecoedPrimaryTracks )")

```
Example plots: run the ROOT macro plots_primary_vertex.x
```shell
root
root [0] .x plots_primary_vertex.x
```
This shows the normalised chi2 of the primary vertex fit, the resolutions in x, y, z, and the pulls of the fitted vertex position.

### Exercises:
1. add the number of primary and secondary tracks into the ntuple
   - Solution:
```python
               # Number of primary and secondary tracks :
               .Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n( RecoedPrimaryTracks )")
               .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )
               # equivalent : (this is to show that a simple C++ statement can be included in a ".Define")
               .Define("n_SecondaryTracks_v2", " return ntracks - n_RecoedPrimaryTracks ; " )
```
and add them to the branches:
 ```python
         branchList = [
                #
                "MC_PrimaryVertex",
                "ntracks",
                "Vertex_allTracks",
                "PrimaryVertex",
                "n_RecoedPrimaryTracks",
                "n_SecondaryTracks",
                "n_SecondaryTracks_v2",
        ]
 ```
2. add the total pT that is carried by the primary tracks. This requires some simple analysis code to be written and compiled. Hint: use the "updated_track_momentum_at_vertex" that is contained in VertexingUtils::FCCAnalysesVertex (contains a TVector3 for each track used in the vertex fit).
      - solution : Create a file MyAnalysis.cc with :
```cpp
#include "FCCAnalyses/MyAnalysis.h"
#include <iostream>

namespace FCCAnalyses{

namespace MyAnalysis {

 double sum_momentum_tracks( const VertexingUtils::FCCAnalysesVertex&  vertex) {
   double sum = 0;
   ROOT::VecOps::RVec< TVector3 > momenta = vertex.updated_track_momentum_at_vertex ;
   int n = momenta.size();
   for (int i=0; i < n; i++) {
      TVector3 p = momenta[i];
      double px = p[0];
      double py = p[1];
      double pt = sqrt(pow(px,2)+pow(py,2)) ;
      sum += pt;
   }
  return sum;
 }
```
and a MyAnalysis.h :
```cpp
#ifndef  MYANALYSIS_ANALYZERS_H
#define  MYANALYSIS_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"

#include "VertexingUtils.h"

namespace FCCAnalyses{

namespace MyAnalysis {

 double sum_momentum_tracks( const VertexingUtils::FCCAnalysesVertex&  vertex );
}//end NS MyAnalysis

}//end NS FCCAnalyses

#endif
```
3. compare these distributions in Z -> uds events and in Z -> bb events: edit the file analysis_primary_vertex.py, search for "testFile" and replace the Zuds file by the Zbb file (currently commented).
4. To go beyond:
   - implementation of LCFI+ 


## Reconstruction of displaced vertices in an exclusive decay chain: starting example

Starting example: Z -> bb events. When a Bs is produced, it is forced to decay into J/Psi (mumu) Phi (K+ K-).
We want to reconstruct the Bs decay vertex and determine the resolution on the position of this vertex. Here, we use the MC-matching information to figure out which are the reconstructed tracks that are matched to the Bs decay products, and we fit these tracks to a common vertex. That means, we "seed" the vertex reconstruction using the MC-truth information.

```shell
fccanalysis run analysis_Bs2JpsiPhi_MCseeded.py  --test --nevents 1000 --output Bs2JpsiPhi_MCseeded.root
```

The ntuple contains the MC decay vertex of the Bs, and the reconstructed decay vertex. 

Snippet of the code:
```python
 # MC indices of the decay Bs (PDG = 531) -> mu+ (PDG = -13) mu- (PDG = 13) K+ (PDG = 321) K- (PDG = -321)
 # Retrieves a vector of int's which correspond to indices in the Particle block
 # vector[0] = the mother, and then the daughters in the order specified, i.e. here
 #       [1] = the mu+, [2] = the mu-, [3] = the K+, [4] = the K-
 # Boolean arguments :
 #        1st: stableDaughters. when set to true, the dsughters specified in the list are looked
 #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
 #             explored recursively if needed.
 #        2nd: chargeConjugateMother
 #        3rd: chargeConjugateDaughters
 #        4th: inclusiveDecay: when set to false, if a mother is found, that decays 
 #             into the particles specified in the list plus other particle(s), this decay is not selected.
 # If the event contains more than one such decays,only the first one is kept.
 .Define("Bs2MuMuKK_indices",  "MCParticle::get_indices( 531, {-13,13,321,-321}, true, true, true, false) ( Particle, Particle1)" )

 # select events for which the requested decay chain has been found:
 .Filter("Bs2MuMuKK_indices.size() > 0")

 # the mu+ (MCParticle) that comes from the Bs decay :
 .Define("MC_Muplus",  "return Particle.at(  Bs2MuMuKK_indices[1] ) ;")
 # Decay vertex (an edm4hep::Vector3d) of the Bs (MC) = production vertex of the muplus :
 .Define("BsMCDecayVertex",   " return  MC_Muplus.vertex ; ")

 # Returns the RecoParticles associated with the four  Bs decay products.
 # The size of this collection is always 4 provided that Bs2MuMuKK_indices is not empty,
 # possibly including "dummy" particles in case one of the legs did not make a RecoParticle
 # (e.g. because it is outsice the tracker acceptance).
 # This is done on purpose, in order to maintain the mapping with the indices - i.e. the 1st particle in 
 # the list BsRecoParticles is the mu+, then the mu-, etc.
 # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
 # hence the mother particle, which is the [0] element of the Bs2MuMuKK_indices vector).
 #
 # The matching between RecoParticles and MCParticles requires 4 collections. For more
 # detail, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics
 .Define("BsRecoParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( Bs2MuMuKK_indices,    
      MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

 # the corresponding tracks - here, dummy particles, if any, are removed, i.e. one may have < 4 tracks,
 # e.g. if one muon or kaon was emitted outside of the acceptance
 .Define("BsTracks",   "ReconstructedParticle2Track::getRP2TRK( BsRecoParticles, EFlowTrack_1)" )

 # number of tracks in this BsTracks collection ( = the #tracks used to reconstruct the Bs vertex)
 .Define("n_BsTracks", "ReconstructedParticle2Track::getTK_n( BsTracks )")

 # Fit the tracks to a common vertex. That would be a secondary vertex, hence we put
 # a "2" as the first argument of VertexFitter_Tk :
 #        First the full object, of type Vertexing::FCCAnalysesVertex
 .Define("BsVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, BsTracks)" )
 #        from which we extract the edm4hep::VertexData object, which contains the vertex positiob in mm
 .Define("BsVertex",  "VertexingUtils::get_VertexData( BsVertexObject )")

```
The root macro plots_Bs2JsiPhi.x produces various plots showing the vertex chi2, the vertex resolutions and the pulls of the vertex fit.



## Exercise: analysis of tau -> 3 mu

1. Start from analysis_Bs2JpsiPhi.py and adapt it to the decay tau -> 3 mu. 
```shell
cp analysis_Bs2JpsiPhi_MCseeded.py analysis_Tau3Mu_MCseeded.py
```
   - solution: one just need to retrieve properly the indices of the decay of interest:
 ```python
 .Define("indices",  "MCParticle::get_indices( 15, {-13,13,13}, true, true, true, false) ( Particle, Particle1)" )
 ```
 and replace subsequently "Bs2MuMuKK_indices" into "indices" - and, to have meaningful variable names, "Bsxxx" into "Tauxxx". The file can be found in the Exercises directory.
   
   
2. Add the reconstructed tau mass to the ntuple (you will need to write new code). Check that the mass resolution is improved when it is determined from the track momenta **at the tau decay vertex**, compared to a blunt 3-muon mass determined from the default track momenta (taken at theis distance of closest approach).
   - solution : This needs to be added to your MyAnalysis.cc :
```cpp
 double tau3mu_vertex_mass( const VertexingUtils::FCCAnalysesVertex& vertex ) {
   double muon_mass = 0.1056;
   TLorentzVector tau;
   ROOT::VecOps::RVec< TVector3 > momenta = vertex.updated_track_momentum_at_vertex ;
   int n = momenta.size();
   for (int ileg=0; ileg < n; ileg++) {
     TVector3 track_momentum = momenta[ ileg ];
     TLorentzVector leg;
     leg.SetXYZM( track_momentum[0], track_momentum[1], track_momentum[2], muon_mass ) ;
     tau += leg;
   }
  return tau.M();
 }

 double tau3mu_raw_mass( const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  legs ) {
  double muon_mass = 0.1056;
  TLorentzVector tau;
  int n = legs.size();
  for (int ileg=0; ileg < n; ileg++) {
     TLorentzVector leg;
     leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, muon_mass );
     tau += leg;
  }
  return tau.M();
 }
```
and update your MyAnalysis.h by adding the following includes:
```cpp
#include "TLorentzVector.h"
#include "edm4hep/ReconstructedParticleData.h"
```
and add this to your analysis_Tau3Mu_MCseeded.py:
```python
 # The reco'ed tau mass - from the post-VertxFit momenta, at the tau decay vertex :
.Define("TauMass",   "MyAnalysis::tau3mu_vertex_mass( TauVertexObject ) ")
 # The "raw" mass - using the track  momenta at their dca :
 .Define("RawMass",  "MyAnalysis::tau3mu_raw_mass( TauRecoParticles ) ")
```
and add the new variables to the list of branches.

4. So far, everything was done using "Monte-Carlo seeding", which gives the resolutions that we expect, in the absence of possible combinatoric issues. The next step is to write a new analysis.py which starts from the reconstructed muons.
   - select combinations of three muons with total charge = +/- 1
   - fit the three muons to a common vertex and reconstruct the tau mass
5. Look at the tau -> 3 pi nu background. 
  
        

