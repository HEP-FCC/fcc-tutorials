
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
and add the variable in your analyser:
```python
               # Total pT carried by the primary tracks:
               .Define("sum_pt_primaries",   "MyAnalysis::sum_momentum_tracks( PrimaryVertexObject )")
               ....
               branchList = [
                #
                ....
                "sum_pt_primaries",
                ]

```
3. compare these distributions in Z -> uds events and in Z -> bb events: edit the file analysis_primary_vertex.py, search for "testFile" and replace the Zuds file by the Zbb file (currently commented).
4. To go beyond:
   - The reconstruction of all secondary vertices following the LCFI+ has been implemented (Kunal Gautam, Armin Ilg). The Pull request is ready and will bemerged soon: https://github.com/HEP-FCC/FCCAnalyses/pull/206


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
and edit to change the testfile:
```python
testFile= "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu/events_189205650.root"
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

3. So far, everything was done using "Monte-Carlo seeding", which gives the resolutions that we expect, in the absence of possible combinatoric issues. The next step is to write a new analysis.py which starts from the reconstructed muons.
```shell
cp analysis_Tau3Mu_MCseeded.py  analysis_Tau3Mu.py
```
remove the "core" of the analyser:
```python
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
        )
        return df2
```
and insert:
```python
 # Use the "AllMuons" collection, which contains also non-isolated muons (in contrast to the "Muons" collection)
 #    Actually, "Muon" or ("AllMuon") just contain pointers (indices) to the RecoParticle collections,
 #    hence one needs to first retrieve the RecoParticles corresponding to these muons.
 #    ( for more detail about the collections, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics  )
 .Alias("Muon0", "AllMuon#0.index")
 .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
 .Define("n_muons",  "ReconstructedParticle::get_n( muons ) ")
```

We now want to write a method that builds muon triplets - actually, since the MC files produced for this tutorial only forced the decay of the tau-, we are interestedin triplets with total charge = -1.

**Exercise:** code a function in your MyAnalysis :
```cpp
  ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(
                        const   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  in , float total_charge) ;

```
that returns all combinations of 3-muons.

    - solution:
    
```cpp
    ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets
               ( const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in , float total_charge ) {

    ROOT::VecOps::RVec< ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> >  results;
    float charge =0;
    int n = in.size();
    if ( n < 3 ) return results;

    for (int i=0; i < n; i++) {
       edm4hep::ReconstructedParticleData pi = in[i];
       float charge_i = pi.charge ;

       for (int j=i+1; j < n; j++) {
        edm4hep::ReconstructedParticleData pj = in[j];
        float charge_j = pj.charge ;

        for (int k=j+1; k < n; k++) {
                edm4hep::ReconstructedParticleData pk = in[k];
                float charge_k = pk.charge ;
                float charge_tot = charge_i + charge_j + charge_k;
                if ( charge_tot == total_charge ) {
                    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_triplet;
                    a_triplet.push_back( pi );
                    a_triplet.push_back( pj );
                    a_triplet.push_back( pk );
                    results.push_back( a_triplet );
                }

        }

    }

 }
 return results;
}
```
    
 You can then use it in your analysis_Tau3Mu.py :
 ```python
  # Build triplets of muons.
  # We are interested in tau- -> mu- mu- mu+ (the MC files produced for this tutorial
  # only forced the decay of the tau- , not the tau+ ).
  # Hence we look for triples of total charge = -1 :
  .Define("triplets_m",  "MyAnalysis::build_triplets( muons, -1. )")   # returns a vector of triplets, i.e. of vectors of 3 RecoParticles
  .Define("n_triplets_m",  "return triplets_m.size() ; " )
  .Filter( "n_triplets_m > 0" )
 ```
 where the latter line will filter out events for which no triplet has been found.
 
 NB: the efficiency for having the three muons from the tau decay that fall within the tracker acceptance is about 95%. However, a track will reach the muon detector only if its momentum is larger than about 2 GeV (in Delphes, the efficiency for muons below 2 GeV is set to zero). When adding the requirement that the three muons have p > 2 GeV, the efficiency drops to about 75%. You can check that using the MC information, starting e.g. from analysis_Tau3Mu_MCseeded.py. Consequently: out of 1000 signal events, only ~ 750 events are selected by the above Filter.
 
 It is then simple to build a tau candidate from the first triplet that has been found, e.g. :
 ```python
  # ----------------------------------------------------
  # Simple: consider only the 1st triplet :

  .Define("the_muons_candidate_0",  "return triplets_m[0] ; ")  # the_muons_candidates = a vector of 3 RecoParticles

  # get the corresponding tracks:
  .Define("the_muontracks_candidate_0",  "ReconstructedParticle2Track::getRP2TRK( the_muons_candidate_0, EFlowTrack_1)")
  # and fit them to a common vertex :
  .Define("TauVertexObject_candidate_0",   "VertexFitterSimple::VertexFitter_Tk( 2, the_muontracks_candidate_0)" )
  # Now we can get the mass of this candidate, as before :
  .Define("TauMass_candidate_0",   "MyAnalysis::tau3mu_vertex_mass( TauVertexObject_candidate_0 )" )

 ```
 but we would like to retrieve all tau candidates.
 
 **Exercise:**  code the following methods in your MyAnalysis:
 ```cpp
   ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(
            const ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets,
            const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks ) ;

  ROOT::VecOps::RVec<  double > build_AllTauMasses( const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices ) ;

 ```
       - solution :
 ```cpp
       ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(
                        const ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets,
                        const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks )  {
      ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex >  results;
      int ntriplets = triplets.size();
      for (int i=0; i < ntriplets; i++) {
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = triplets[i];

          ROOT::VecOps::RVec<edm4hep::TrackState> the_tracks = ReconstructedParticle2Track::getRP2TRK( legs, allTracks );
          VertexingUtils::FCCAnalysesVertex vertex = VertexFitterSimple::VertexFitter_Tk( 2, the_tracks );
          results.push_back( vertex );
      }
 return results;
}


ROOT::VecOps::RVec<  double > build_AllTauMasses( const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices ) {
  ROOT::VecOps::RVec<  double >  results;
  for ( auto& v: vertices) {
     double mass =  tau3mu_vertex_mass( v );
     results.push_back( mass  );
  }
 return results;
}

 ```
 which you then use in your analyser:
 ```python
   # ----------------------------------------------------
   # Now consider all triplets :

   .Define("TauVertexObject_allCandidates",  "MyAnalysis::build_AllTauVertexObject( triplets_m , EFlowTrack_1 ) ")
   .Define("TauMass_allCandidates",   "MyAnalysis::build_AllTauMasses( TauVertexObject_allCandidates )" )

 ```
 and you add the mass of all candidates in your ntuple:
 ```python
   branchList = [
                "n_muons",
                "n_triplets_m",
                "TauMass_allCandidates"
  ]

 ```
 
4. We now want to look at the background. 
Copy your analysis_Tau3Mu.py:
```shell
cp analysis_Tau3Mu.py analysis_Tau3Mu_stage1.py

```
The main background is expected to come from tau -> 3 pi nu decays, when the charged pions are misidentified as muons. But there is no "fakes" in Delphes: all the "Muon" objects that you have on the edm4hep file do originate from genuine muons (which may, of course, come from a hadron decay). To alleviate this limitation, we first select the RecoParticles that are matched to a stable, charged hadron :
```python
 # -----------------------------------------
 # Add fake muons from pi -> mu

 # This selects the charged hadrons :
 .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
 .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 .Define("ChargedHadrons", "ReconstructedParticle2MC::selRP_ChargedHadrons( MCRecoAssociations0,
        MCRecoAssociations1,ReconstructedParticles,Particle)")
        
```
and further select the ones that are above 2 GeV - since only particles above 2 GeV will make it to the muon detector:
```python
  # Only the ones with  p > 2 GeV could be selected as muons :
  .Define("ChargedHadrons_pgt2",  "ReconstructedParticle::sel_p(2.) ( ChargedHadrons )")

```

Now we want to apply a "flat" fake rate, i.e. accept a random fraction of the above particles as muons.

**Exercise:** code a method in your MyAnalysis that does that :
```cpp
#include <random>
#include <chrono>
...
struct selRP_Fakes {
  selRP_Fakes( float arg_fakeRate, float arg_mass );
  float m_fakeRate = 1e-3;
  float m_mass = 0.106;  // muon mass
  std::default_random_engine m_generator;
  std::uniform_real_distribution<float> m_flat;
  std::vector<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};
```

     - solution:
     
```cpp
     
     selRP_Fakes::selRP_Fakes( float arg_fakeRate, float  arg_mass ) : m_fakeRate(arg_fakeRate), m_mass( arg_mass)  {
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::default_random_engine generator (seed);
        m_generator = generator;
        std::uniform_real_distribution<float> flatdis(0.,1.);
        m_flat.param( flatdis.param() );
     };

    std::vector<edm4hep::ReconstructedParticleData> selRP_Fakes::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
         std::vector<edm4hep::ReconstructedParticleData> result;
         for (size_t i = 0; i < in.size(); ++i) {
         auto & p = in[i];
         float arandom =  m_flat (m_generator );
         if ( arandom <= m_fakeRate) {
         edm4hep::ReconstructedParticleData reso = p;
         // overwrite the mass:
         reso.mass = m_mass;
         result.push_back( reso );
    }
  }
  return result;
}

 ```

We then use this method in the analyser :
```python
  # Build fake muons based on a flat fake rate (random selection) :
  .Define("fakeMuons_5em2", "MyAnalysis::selRP_Fakes( 5e-2, 0.106)(ChargedHadrons_pgt2)" )

  # Now we marge the collection of fake muons with the genuine muons :
  .Define("muons_with_fakes",  "ReconstructedParticle::merge( muons, fakeMuons_5em2 )")
  # and we use this collection later on, instead of "muons" :
  .Alias("theMuons", "muons_with_fakes")
  .Define("n_muons_withFakes",  "ReconstructedParticle::get_n( theMuons )")
  
```
and we just need to replace the muon collection when building the triplets :
```python
  .Define("triplets_m",  "MyAnalysis::build_triplets( theMuons, -1. )")   # returns a vector of triplets, i.e. of vectors of 3 RecoParticles

```

You can also add the total visible energy into your ntuple:

```python
             # Total visible energy in the event :
             .Define("RecoPartEnergies",  "ReconstructedParticle::get_e( ReconstructedParticles )")
             .Define("visible_energy",  "Sum( RecoPartEnergies )")
```

        
5. We now have a simple analyser that can be used to process the signal and background samples, and plot the mass of the tau -> 3mu candidates:
This produces flat ntuples:
```shell
fccanalysis run analysis_Tau3Mu_stage1.py --output-dir Tau3Mu
```
This produces histograms of selected variables, with some selection :
```shell
fccanalysis final analysis_Tau3Mu_final.py
```
and finally, this makes some plots :
```shell
fccanalysis plots analysis_Tau3Mu_plots.py
```



