
# FCC: tracking and vertexing example using specific flavour decays


:::{admonition} Learning Objectives
:class: objectives

This tutorial will teach you how to:

-   fit some tracks to a common vertex in **FCCAnalyses**, recontruct the primary vertex and the primary tracks
-   retrieve the tracks corresponding to a specific flavour decay in **FCCAnalyses**
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   build your own algorithm inside **FCCAnalyses**

For the vertex fitter, we make use of the code developed by Franco Bedeschi, [see this talk](https://indico.cern.ch/event/1003610/contributions/4214579/attachments/2187815/3696958/Bedeschi_Vertexing_Feb2021.pdf).
The [subsequent updates presented in July 2022](https://indico.cern.ch/event/1180976/contributions/4960968/attachments/2481467/4259924/Bedeschi_Vertexing_Jul2022.pdf) offer possibilities for complex reconstructions, but they are not yet ready to use in the public FCCAnalyses version (coming soon).

To reconstruct the primary vertex and the primary tracks, we follow the LCFI+ algorithm (T. Suehara,T. Tanabe), described in [arXiv:1506.08371](https://arxiv.org/pdf/1506.08371.pdf).

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


## Building a custom sub-package in FCCAnalyses

In order to add new code, we need to develop inside FCCAnalyses. For that we setup a dedicated area to work using this setup script.
```shell
source ./setupUserCode.sh myAnalysis
```

We now have a new directory `myAnalysis` that contains both include `myAnalysis/include/myAnalysis.h` and source `myAnalysis/src/myAnalysis.cc` files within the `myAnalysis` namespace. In the following of this tutorial, when new code needs to be added, it should be done in those two files. An example is given below:

```cpp
#in the header file
rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);

#in the source file
rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
  rv::RVec<float> output;
  for (size_t i = 0; i < parts.size(); ++i)
    output.emplace_back(parts.at(i).momentum.x);
  return output;
}
```

Finally, in your python analysis script, you can now call you newly defined function, don't forget it is inside a namespace!

```python
.Define("dummy_collection", "myAnalysis::dummy_collection(ReconstructedParticles)")
```

It takes as argument the collection named in our ROOT files `ReconstructedParticles`, which is a vector of `edm4hep::ReconstructedParticleData` [see here](https://edm4hep.web.cern.ch/classedm4hep_1_1_reconstructed_particle_data.html) and also add the newly defined column `dummy_collection` to the list of output variables, this can be seen in `myAnalysis/scripts/analysis_cfg.py`

Last thing, do not forget to compile before running to use your new code.

```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```



## Reconstruction of the primary vertex and of primary tracks

Let's start by running primary vertex reconstruction on a few events of one test file:

```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_primary_vertex.py --test --nevents 1000 --output primary_Zuds.root
```

Note: with the option `--test`, we process the file that is hard-coded under `testFile` inside `analysis_primary_vertex.py`. In this case, it is a file of $Z \rightarrow q \bar{q}$ with $q=u,d,s$.

The resulting ntuple `primary_Zuds.root` contains the MC event vertex `MC_PrimaryVertex`, and the reconstructed primary vertex `PrimaryVertex`.

:::{admonition} Snippet of `analysis_primary_vertex.py`
:class: toggle
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
:::


To produce some example plots, just run the ROOT macro ```examples/FCCee/tutorials/vertexing/plots_primary_vertex.x```

:::{admonition} Suggested answer
:class: toggle
```shell
root -l
.x examples/FCCee/tutorials/vertexing/plots_primary_vertex.x
```
:::

This produces normalised $\chi^2$ of the primary vertex fit, the resolutions in `x, y, z`, and the pulls of the fitted vertex position.

### Exercises:
1. add the number of primary and secondary tracks into the ntuple using the function `ReconstructedParticle2Track::getTK_n(ROOT::VecOps::RVec<edm4hep::TrackState> x)` [see here](https://github.com/HEP-FCC/FCCAnalyses/blob/master/analyzers/dataframe/FCCAnalyses/ReconstructedParticle2Track.h#L111)

:::{admonition} Suggested answer
:class: toggle
```python
# Number of primary and secondary tracks :
.Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n( RecoedPrimaryTracks )")
.Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )
# equivalent : (this is to show that a simple C++ statement can be included in a ".Define")
.Define("n_SecondaryTracks_v2", " return ntracks - n_RecoedPrimaryTracks ; " )
```
:::

and add the corresponding collection to the `branchList`:

:::{admonition} Suggested answer
:class: toggle
 ```python
branchList = [
  "MC_PrimaryVertex",
  "ntracks",
  "Vertex_allTracks",
  "PrimaryVertex",
  "n_RecoedPrimaryTracks",
  "n_SecondaryTracks",
  "n_SecondaryTracks_v2",
  ]
 ```
:::

2. Add the total $p_T$ that is carried by the primary tracks. This requires some simple analysis code to be written (in our `myAnalysis`) and compiled. Then, the python analyser file needs to be updated to include `analysesList = ['myAnalysis']`.

Hint: use the `updated_track_momentum_at_vertex` that is contained in `VertexingUtils::FCCAnalysesVertex` (contains a `TVector3` for each track used in the vertex fit) and use this function implementation:

```cpp
double sum_momentum_tracks(const VertexingUtils::FCCAnalysesVertex&  vertex);
```

:::{admonition} Suggested answer
:class: toggle
Add inside `myAnalysis/include/myAnalysis.h`
```cpp
...
#include "FCCAnalyses/VertexingUtils.h"
using namespace FCCAnalyses;
...
double sum_momentum_tracks(const VertexingUtils::FCCAnalysesVertex&  vertex);
```

Add inside `myAnalysis/src/myAnalysis.cc`
```cpp
 double sum_momentum_tracks(const VertexingUtils::FCCAnalysesVertex&  vertex) {
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

Compile as explained above:
```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```

Edit your `examples/FCCee/tutorials/vertexing/analysis_primary_vertex.py` and add at the very top :
```python
analysesList = ['myAnalysis']
```

and finally, add the variable in your analyser (both definition and in the branchList) `examples/FCCee/tutorials/vertexing/analysis_primary_vertex.py`
```python
# Total pT carried by the primary tracks:
.Define("sum_pt_primaries",   "myAnalysis::sum_momentum_tracks( PrimaryVertexObject )")
[...]
branchList = [
#
[...]
"sum_pt_primaries",
]
```
:::

3. Compare these distributions in $Z \rightarrow uds$ events and in $Z \rightarrow b\bar{b}$ events.

:::{admonition} Suggested answer
:class: toggle
Edit the file `examples/FCCee/tutorials/vertexing/analysis_primary_vertex.py`, search for `testFile` and replace the `Zuds` file by the `Zbb` file (currently commented).
:::

4. To go beyond:
The reconstruction of all secondary vertices following the LCFI+ algorithm has been implemented in **FCCAnalyses** by Kunal Gautam and Armin Ilg. The Pull request is ready and will be merged soon: [https://github.com/HEP-FCC/FCCAnalyses/pull/206](https://github.com/HEP-FCC/FCCAnalyses/pull/206). It contains an `analysis_SV.py` which:
  - reconstructs the primary vertex and primary tracks as done above
  - reconstructs jets using the Durham algorithm
  - reconstructs secondary vertices within all jets, and determines some properties of these secondary vertices
It is also possible to reconstruct all secondary vertices in an event, without reconstructing jets.



## Reconstruction of displaced vertices in an exclusive decay chain: starting example

We consider here $Z \rightarrow b \bar{b}$ events.
When a $B_s$ is produced, it is forced to decay into $J/\Psi \Phi$ with $J/\Psi \rightarrow \mu^+\mu^-$ and $\Phi \rightarrow K^+ K^-$.
We want to reconstruct the $B_s$ decay vertex and determine the resolution on the position of this vertex. Here, we use the MC-matching information to figure out which are the reconstructed tracks that are matched to the $B_s$ decay products, and we fit these tracks to a common vertex. That means, we "seed" the vertex reconstruction using the MC-truth information. Let's run the following:


```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_Bs2JpsiPhi_MCseeded.py  --test --nevents 1000 --output Bs2JpsiPhi_MCseeded.root
```

The ntuple `Bs2JpsiPhi_MCseeded.root` contains the MC decay vertex of the $B_s$, and the reconstructed decay vertex.

:::{admonition} Snippet of `analysis_Bs2JpsiPhi_MCseeded.py`
:class: toggle
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
:::

Run the root macro `examples/FCCee/tutorials/vertexing/plots_Bs2JsiPhi.x` produces various plots showing the vertex $\chi^2$, the vertex resolutions and the pulls of the vertex fit.

:::{admonition} Suggested answer
:class: toggle
```shell
root -l
.x examples/FCCee/tutorials/vertexing/plots_Bs2JsiPhi.x
```
:::


## Exercise: analysis of $\tau \rightarrow 3 \mu$

1. Start from `examples/FCCee/tutorials/vertexing/analysis_Bs2JpsiPhi.py` and adapt it to the decay $\tau \rightarrow 3 \mu$.

```shell
cp examples/FCCee/tutorials/vertexing/analysis_Bs2JpsiPhi_MCseeded.py examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_MCseeded.py
```

and edit to change the `testFile`:
```python
testFile= "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu/events_189205650.root"
```

and modify the call to `MCParticle::get_indices` to retrieve properly the indices of the decay of interest and replace subsequently `Bs2MuMuKK_indices` into the name you chose - and, to have meaningful variable names, `Bsxxx` into `Tauxxx`.


:::{admonition} Suggested answer
:class: toggle
 ```python
 .Define("indices",  "MCParticle::get_indices( 15, {-13,13,13}, true, true, true, false) ( Particle, Particle1)" )
 ```
 The full file can be found in  `examples/FCCee/tutorials/vertexing/Exercises/analysis_Tau3Mu_MCseeded_start.py`.
 :::



2. Add the reconstructed $\tau$ mass to the ntuple (you will need to write new code). Check that the mass resolution is improved when it is determined from the track momenta **at the tau decay vertex**, compared to a blunt 3-muon mass determined from the default track momenta (taken at the distance of closest approach).

Suggested implementation, to be added to your `myAnalysis/include/myAnalysis.h`:
```cpp
#include "TLorentzVector.h"
#include "edm4hep/ReconstructedParticleData.h"
[...]
double tau3mu_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex );
double tau3mu_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  legs);
```

:::{admonition} Suggested answer
:class: toggle
This needs to be added to your `myAnalysis/src/myAnalysis.cc` :
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

The local code needs to be recompiled:
```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```

Add the call to your `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_MCseeded.py`:
```python
 # The reco'ed tau mass - from the post-VertxFit momenta, at the tau decay vertex :
.Define("TauMass",   "myAnalysis::tau3mu_vertex_mass( TauVertexObject ) ")
 # The "raw" mass - using the track  momenta at their dca :
 .Define("RawMass",  "myAnalysis::tau3mu_raw_mass( TauRecoParticles ) ")
```
and add the new variables to the list of branches `branchList` as usual.
Moreover, in order to be able to run the local code from `myAnalysis`, don't forget to add
```python
analysesList = ['myAnalysis']
```
at the beggining of your `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_MCseeded.py`.

Run fccanalyses:
```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_MCseeded.py --test --nevents 1000 --output Tau3Mu_MCseeded.root
```

Plot the mass distributions in ROOT:
```shell
root -l Tau3Mu_MCseeded.root
TH1F* h1 = new TH1F("h1",";Tau Mass (GeV); a.u.",20, 1.75, 1.8) ;
events->Draw("TauMass >>h1");
TH1F* h2 = new TH1F("h2",";Raw Mass (GeV); a.u.", 20, 1.75, 1.8) ;
events->Draw("RawMass >>h2");
h1->SetLineColor(2);
h1->Draw("hist");
h2->Draw("same, hist");

```

:::


3. So far, everything was done using "Monte-Carlo seeding", which gives the resolutions that we expect, in the absence of possible combinatoric issues. The next step is to write a new `analysis.py` which starts from the reconstructed muons.

```shell
cp examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_MCseeded.py  examples/FCCee/tutorials/vertexing/analysis_Tau3Mu.py
```

and just keep the "core" of the `analysers` function such that you have something like:

```python
class RDFanalysis():
    def analysers(df):
        df2 = (
            df
        )
        return df2
```

clear out the `branchList`,
and insert new `Define`s:
```python
 # Use the "AllMuons" collection, which contains also non-isolated muons (in contrast to the "Muons" collection)
 #    Actually, "Muon" or ("AllMuon") just contain pointers (indices) to the RecoParticle collections,
 #    hence one needs to first retrieve the RecoParticles corresponding to these muons.
 #    ( for more detail about the collections, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics  )
 .Alias("Muon0", "AllMuon#0.index")
 .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
 .Define("n_muons",  "ReconstructedParticle::get_n( muons ) ")
```

We now want to write a method that builds muon triplets - actually, since the MC files produced for this tutorial only forced the decay of the $\tau^-$, we are interested in triplets with total charge = -1.

**Exercise:** code a function in your `myAnalysis` that builds such triplet

Hint, the function should take as input the `ReconstructedParticles` and the charge of the triplet, and should return all combinations of 3-muons in a vector of vector of `ReconstructedParticles`. It could be something like (to be added to `myAnalysis/include/myAnalysis.h`):

```cpp
ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(const   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>&  in , float total_charge);
```

:::{admonition} Suggested answer
:class: toggle
This needs to be added to your `myAnalysis/src/myAnalysis.cc` :
```cpp
ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> > build_triplets(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in , float total_charge) {

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
        }//end loop over k
      }//end loop over j
    }//end loop over i
 return results;
}
```


 You can then use it in your `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu.py` :
 ```python
  # Build triplets of muons.
  # We are interested in tau- -> mu- mu- mu+ (the MC files produced for this tutorial
  # only forced the decay of the tau- , not the tau+ ).
  # Hence we look for triples of total charge = -1 :
  .Define("triplets_m",  "myAnalysis::build_triplets( muons, -1. )")   # returns a vector of triplets, i.e. of vectors of 3 RecoParticles
  .Define("n_triplets_m",  "return triplets_m.size() ; " )
 ```

 NB: the efficiency for having the three muons from the tau decay that fall within the tracker acceptance is about 95%. However, a track will reach the muon detector only if its momentum is larger than about 2 GeV (in Delphes, the efficiency for muons below 2 GeV is set to zero). When adding the requirement that the three muons have p > 2 GeV, the efficiency drops to about 75%. You can check that using the MC information, starting e.g. from analysis_Tau3Mu_MCseeded.py. Consequently: out of 1000 signal events, only ~  a triplet is found in 750 events only.

 It is then simple to build a tau candidate from the first triplet that has been found, e.g. :
 ```python
  # ----------------------------------------------------
  # Simple: consider only the 1st triplet :

  #  .Define("the_muons_candidate_0",  "return triplets_m[0] ; ")  # the_muons_candidates = a vector of 3 RecoParticles

  # get the corresponding tracks:
  #   .Define("the_muontracks_candidate_0",  "ReconstructedParticle2Track::getRP2TRK( the_muons_candidate_0, EFlowTrack_1)")
  # and fit them to a common vertex :
  #   .Define("TauVertexObject_candidate_0",   "VertexFitterSimple::VertexFitter_Tk( 2, the_muontracks_candidate_0)" )
  # Now we can get the mass of this candidate, as before :
  #   .Define("TauMass_candidate_0",   "myAnalysis::tau3mu_vertex_mass( TauVertexObject_candidate_0 )" )

 ```
 but we would like to retrieve all tau candidates and decide later which one to use.
 :::

 **Exercise**: code a function in your `myAnalysis` to retrieve all tau candidates, and their corresponding tau mass.

Hint, the functions could be of type (to be added to `myAnalysis/include/myAnalysis.h`):

 ```cpp
 ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets, const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks) ;

ROOT::VecOps::RVec<  double > build_AllTauMasses(const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices) ;
 ```

:::{admonition} Suggested answer
:class: toggle
This needs to be added to your `myAnalysis/src/myAnalysis.cc`

 ```cpp
ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex > build_AllTauVertexObject(const ROOT::VecOps::RVec< ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> >&  triplets, const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks )  {
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


ROOT::VecOps::RVec<  double > build_AllTauMasses(const ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex>&  vertices) {
  ROOT::VecOps::RVec<  double >  results;
  for ( auto& v: vertices) {
     double mass =  tau3mu_vertex_mass( v );
     results.push_back( mass  );
  }
 return results;
}
 ```

and these includes must be added to `myAnalysis/include/myAnalysis.h` :
```cpp
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexFitterSimple.h"
```


The local code needs to be recompiled:
```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```


and you can then use in your analyser `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu.py` :
```python
   # ----------------------------------------------------
   # Now consider all triplets :

   .Define("TauVertexObject_allCandidates",  "myAnalysis::build_AllTauVertexObject( triplets_m , EFlowTrack_1 ) ")
   .Define("TauMass_allCandidates",   "myAnalysis::build_AllTauMasses( TauVertexObject_allCandidates )" )
```

and you add the mass of all candidates in your ntuple:
 ```python
   branchList = [
                "n_muons",
                "n_triplets_m",
                "TauMass_allCandidates"
                ]
 ```

Run fccanalyses:
```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_Tau3Mu.py --test --nevents 1000 --output Tau3Mu.root
```

and look at the ntuple:
```shell
root -l Tau3Mu.root
events -> Draw("TauMass_allCandidates")   // candidates at large mass pick up a muon from the "other" leg
events -> Draw("TauMass_allCandidates","TauMass_allCandidates < 2")   // the genuine tau to 3mu candidates
```

:::

4. We now want to look at the background.
Copy your analysis_Tau3Mu.py:
```shell
cp examples/FCCee/tutorials/vertexing/analysis_Tau3Mu.py examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py

```
The main background is expected to come from $\tau \rightarrow 3 \pi \nu$ decays, when the charged pions are misidentified as muons. But there is no "fakes" in Delphes: all the "Muon" objects that you have on the edm4hep file do originate from genuine muons (which may, of course, come from a hadron decay). To alleviate this limitation, we first select the `ReconstructedParticle`s that are matched to a stable, charged hadron. Edit your `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py` and add, after the `.Define("n_muons", ... )` :

```python
 # -----------------------------------------
 # Add fake muons from pi -> mu

 # This selects the charged hadrons :
 .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
 .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 .Define("ChargedHadrons","ReconstructedParticle2MC::selRP_ChargedHadrons(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
```

( As mentioned earlier, the matching between RecoParticles and MCParticles requires 4 collections. See [here](https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics) for more detail ).


and further select the ones that are above 2 GeV - since only particles above 2 GeV will make it to the muon detector:
```python
# Only the ones with  p > 2 GeV could be selected as muons :
.Define("ChargedHadrons_pgt2",  "ReconstructedParticle::sel_p(2.) ( ChargedHadrons )")
```

Now we want to apply a "flat" fake rate, i.e. accept a random fraction of the above particles as muons.

**Exercise:** code a method in your `myAnalysis` that does that.

Hint, in your header file `myAnalysis/include/myAnalysis.h` you need to define a `struct` and add few includes, like:
```cpp
#include <random>
#include <chrono>
...
struct selRP_Fakes {
  selRP_Fakes( float arg_fakeRate, float arg_mass );
  float m_fakeRate = 1e-3; //fake rate
  float m_mass = 0.106;  // muon mass
  std::default_random_engine m_generator;
  std::uniform_real_distribution<float> m_flat;
  std::vector<edm4hep::ReconstructedParticleData>  operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in);
};
```

:::{admonition} Suggested answer
:class: toggle

This needs to be added in your `myAnalysis/src/myAnalysis.cc`
```cpp
selRP_Fakes::selRP_Fakes( float arg_fakeRate, float  arg_mass ) : m_fakeRate(arg_fakeRate), m_mass( arg_mass)  {
  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  std::default_random_engine generator (seed);
  m_generator = generator;
  std::uniform_real_distribution<float> flatdis(0.,1.);
  m_flat.param( flatdis.param() );
};

std::vector<edm4hep::ReconstructedParticleData> selRP_Fakes::operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in) {
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

and compile:
```shell
cd ${OUTPUT_DIR}/build
cmake .. && make && make install
cd ${LOCAL_DIR}
```


We then use this method in the analyser `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py` :

```python
# Build fake muons based on a flat fake rate (random selection) - HUGE fake rate used on purpose here :
.Define("fakeMuons_5em2", ROOT.myAnalysis.selRP_Fakes(5e-2, 0.106), ["ChargedHadrons_pgt2"] )
# Now we marge the collection of fake muons with the genuine muons :
.Define("muons_with_fakes",  "ReconstructedParticle::merge( muons, fakeMuons_5em2 )")
# and we use this collection later on, instead of "muons" :
.Alias("theMuons", "muons_with_fakes")
.Define("n_muons_withFakes",  "ReconstructedParticle::get_n( theMuons )")
```

and we just need to replace the muon collection when building the triplets :
```python
.Define("triplets_m",  "myAnalysis::build_triplets( theMuons, -1. )")   # returns a vector of triplets, i.e. of vectors of 3 RecoParticles
```

Moreover, in order to pass the functor constructor of `selRP_Fakes` as above (`ROOT.myAnalysis.selRP_Fakes(5e-2, 0.106)`, not inside a string), we need to add
```python
import ROOT
```

at the top of `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py`.


You can also add the total visible energy into your ntuple:

```python
# Total visible energy in the event :
.Define("RecoPartEnergies",  "ReconstructedParticle::get_e( ReconstructedParticles )")
.Define("visible_energy",  "Sum( RecoPartEnergies )")
```

and add it to your `branchList` :
```python
        branchList = [
                "n_muons",
                "n_triplets_m",
                "TauMass_allCandidates",
                "visible_energy"
        ]

```

Run it again on the test signal file, in order to make sure that nothing is broken :

```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py --test --nevents 1000 --output Tau3Mu.root
```

:::

The files `analysis_Tau3Mu_stage1.py`, `myAnalysis.h` and `myAnalysis.cc` with all the changes discussed above can be found in the `examples/FCCee/tutorials/vertexing/Exercises/` directory of FCCAnalyses.

5. We now have a simple analyser that can be used to process the signal and background samples, and plot the mass of the $\tau \rightarrow 3\mu$ candidates. For that we need to process the full statistics. In order for you to have access to `/afs/cern.ch/work/f/fccsw/public/FCCDicts/`, we need to add you CERN login to an afs group. If not already provided, please do so.

All samples that have been centrally produced can be found [on this web page](http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/index.php). We use `spring2021` samples (in `Production tags`), and the files made with `IDEA`. If you enter `TauMinus2MuMuMu` and `TauMinus2PiPiPinus` in the search field, you will see the datasets produced for the signal anf the $\tau \rightarrow 3\pi \nu$ background. The first column shows the dataset names, in this case `p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu` and `p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu`.

To run fccanalyses over these datasets (and not anymore over one test file), the list of datasets to be processed should be inserted in your `examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py` :

```python
import ROOT

analysesList = ['myAnalysis']

processList = {
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu':{},
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu':{}
}
```

as well as
```python
#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"
```

and we tell `fccanalyses` to put all files into the `TauMu` directory :
```python
#Optional: output directory, default is local running directory
outputDir    = "Tau3Mu"

```

This produces flat ntuples:

```shell
fccanalysis run examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_stage1.py
```

After a few minutes, you will see two ntuples, one for the signal, the other for the background, in the `TauMu` directory.

Now that you have ntuples with the variables you need for your analysis, you may analyse them using the tools you prefer. As explained [here](https://github.com/HEP-FCC/FCCAnalyses), you can also use `fccanalysis` to produce histograms of some variables, with some sets of cuts, and to plot them. The normalisation is then taken care of by `fccanalyses`, thanks to a json file (`FCCee_procDict_spring2021_IDEA.json`) which contains the cross-section of the MC processes. To use these functionnalities :


This produces histograms of selected variables, with some selection :

```shell
fccanalysis final examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_final.py
```

:::{admonition} Snippet of `analysis_Tau3Mu_final.py`
:class: toggle
```python
###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"nocut": "true",
           "sel0":"n_triplets_m > 0",
           "sel1":"Min( TauMass_allCandidates ) < 3"
            }


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mTau":{"name":"TauMass_allCandidates","title":"m_{tau} [GeV]","bin":100,"xmin":0,"xmax":3},
    "mTau_zoom":{"name":"TauMass_allCandidates","title":"m_{tau} [GeV]","bin":100,"xmin":1.7,"xmax":1.9},
    "Evis":{"name":"visible_energy","title":"E_{vis} [GeV]","bin":100,"xmin":0,"xmax":91.2},

```
:::

This produces three histograms, for three sets of selections. The histogram files appear in the `TauMu/final` directory. There are now 6 files (2 processes, 3 sets of cuts). The histograms are normalised to a luminosity of one inverse pb.


Finally, this makes some plots :

```shell
fccanalysis plots examples/FCCee/tutorials/vertexing/analysis_Tau3Mu_plots.py
```

which appear in the `Tau3Mu/plots` directory. Look for example at the plot `mTaTau3Mu_nostack_log` in `Tau3Mu/plots/sel1`. The candidates in the background sample, corresponding to $\tau \rightarrow 3 \pi \nu$ decays, are reconstructed at a mass that is usually below the $\tau$ mass due to the presence of the neutrino. Note that the background sample corresponds to a very low statistics (50M have been produced, we expect 14B) and we see fluctuations. The signal cross-section used here correponds to $B( \tau \rightarrow 3 \mu) = 2 \times 10^{-8}$, which is roughly the current upper limit. The luminosity for these final plots is entered in analysis_Tau3Mu_plots.py.




6. To go beyond:

Interested in studying the FCC-ee sensitivity to $\tau \rightarrow 3 \mu$ ? Please contact <alberto.lusiani@pi.infn.it> and <monteil@in2p3.fr>.

Note that the samples used here are just low statistics, test samples. Larger samples that are more accurate (KKMC instead of Pythia) will be produced if someone is interested.
