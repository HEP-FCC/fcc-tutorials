#ifndef HitAnalysis_h
#define HitAnalysis_h 1

#include "marlin/Processor.h"

#include <EVENT/LCCollection.h>
#include <EVENT/TrackerHit.h>
#include <EVENT/SimTrackerHit.h>
#include <EVENT/SimCalorimeterHit.h>
#include <EVENT/Track.h>
#include <EVENT/MCParticle.h>

#include <UTIL/LCRelationNavigator.h>

#include <UTIL/BitField64.h>
//#include <UTIL/ILDConf.h>

//#include "DD4hep/LCDD.h"
//#include "DD4hep/DD4hepUnits.h"
//#include "DDRec/SurfaceManager.h"

#include <TTree.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TGraph.h>
#include <TMath.h>
#include <vector>
#include "lcio.h"
#include <string>
#include <iostream>

using namespace lcio ;
using namespace marlin ;
//using namespace std ;


/**  Example processor for marlin.
 * 
 *  If compiled with MARLIN_USE_AIDA 
 *  it creates a histogram (cloud) of the MCParticle energies.
 * 
 *  <h4>Input - Prerequisites</h4>
 *  Needs the collection of MCParticles.
 *
 *  <h4>Output</h4> 
 *  A histogram.
 * 
 * @param CollectionName Name of the MCParticle collection
 * 
 * @author F. Gaede, DESY
 * @version $Id: HitAnalysis.h,v 1.4 2005/10/11 12:57:39 gaede Exp $ 
 */

class HitAnalysis : public Processor {
  
 public:
 
  //gSystem.Load("libPhysics.so") ;

  // declaration of trees


  virtual Processor*  newProcessor() { return new HitAnalysis ; }
  
  
  HitAnalysis() ;
  
  /** Called at the begin of the job before anything is read.
   * Use to initialize the processor, e.g. book histograms.
   */
  virtual void init();

  /** Called for every run.
   */
  virtual void processRunHeader( LCRunHeader* run ) ;
  
  /** Called for every event - the working horse.
   */
  virtual void processEvent( LCEvent * evt ) ; 
  
  
  virtual void check( LCEvent * evt ) ; 
  
  
  /** Called after data processing for clean up.
   */
  virtual void end() ;

  int getSubdetector(SimTrackerHit*, UTIL::BitField64&);
  int getLayer(SimTrackerHit*, UTIL::BitField64&);


 protected:

  /** Input collection name.
   */

  std::string _oteColName ;
  std::string _otbColName ;
  std::string _itbColName ;
  std::string _iteColName ;
  std::string _vxdBarrelColName ;
  std::string _vxdEndcapColName ;

  std::string _oteDigitColName ;
  std::string _otbDigitColName ;
  std::string _itbDigitColName ;
  std::string _iteDigitColName ;
  std::string _vxdBarrelDigitColName ;
  std::string _vxdEndcapDigitColName ;

  std::string _vxdTrkHitRelations ;
  std::string _vxdECTrkHitRelations ;
  std::string _itbTrkHitRelations ;
  std::string _iteTrkHitRelations ;
  std::string _otbTrkHitRelations ;
  std::string _oteTrkHitRelations ;

  std::string _lumicalColName ;

  std::string  _trackColName ;

  std::string _mcParticleCollectionName ;


  int nEvt= 0 ;
  int nmcp = 0 ;
  int EventWithPrimsAtVXD = 0 ;

  int vxd_hits_barrel = 0 ;
  int vxd_hits_endcaps = 0 ;
  int itb_hits_barrel = 0 ;
  int ite_hits_endcaps = 0 ;
  int otb_hits_barrel = 0 ;
  int ote_hits_endcaps = 0 ;

  int vxd_digits_barrel = 0 ;
  int vxd_digits_endcaps = 0 ;
  int itb_digits_barrel = 0 ;
  int ite_digits_endcaps = 0 ;
  int otb_digits_barrel = 0 ;
  int ote_digits_endcaps = 0 ;

  TH1F *gNoOfHits  ;
  TH1F *gNoOfDigits ;
  TH1F* JustHits ;
  //TGraph *gNoOfHits ;
  char const *ABC[6]={"VXDB","VXDE","ITB","ITE","OTB","OTE"};

  TCanvas *c1 ;

  TTree *hits;
  
  // declarations of leaves types
  //int vxd_hits;
  int event= 0 ;
  int sim_vxd_hits_barrel= 0 ;
  int sim_vxd_hits_endcaps= 0 ;
  int sim_itb_hits_barrel= 0 ;
  int sim_ite_hits_endcaps= 0 ;
  int sim_otb_hits_barrel= 0 ;
  int sim_ote_hits_endcaps= 0 ;
  int reco_vxd_digits_barrel= 0 ;
  int reco_vxd_digits_endcaps= 0 ;
  int reco_itb_digits_barrel= 0 ;
  int reco_ite_digits_endcaps= 0 ;
  int reco_otb_digits_barrel= 0 ;
  int reco_ote_digits_endcaps= 0 ;
  int pixel_vxd= 0 ;
  int fired_channels= 0 ;
  int NoOfTracks = 0 ;
  //double totalEnergy = 0 ;
  //int NoOfTPCHits;
  //int MCP_id;

  std::vector<double> X;
  std::vector<double> Y;
  std::vector<double> Z;
  std::vector<double> simX;
  std::vector<double> simY;
  std::vector<double> simZ;
  std::vector<double> lcalX;
  std::vector<double> lcalY;
  std::vector<double> lcalZ;
  std::vector<double> lcalNrg;
  std::vector<double> hitNrg;
  std::vector<double> simhitPx;
  std::vector<double> simhitPy;
  std::vector<double> simhitPz;
  std::vector<int>  simPDG ;
  std::vector<int>  simVXDPDG ;
  std::vector<double> vtxX;
  std::vector<double> vtxY;
  std::vector<double> vtxZ;
  std::vector<float> mcpPX;
  std::vector<float> mcpPY;
  std::vector<float> mcpPZ;
  std::vector<double> mcpE;
  std::vector<double> bs_true_vtx_X;
  std::vector<double> bs_true_vtx_Y;
  std::vector<double> bs_true_vtx_Z;
  std::vector<double> dir_true_vtx_X;
  std::vector<double> dir_true_vtx_Y;
  std::vector<double> dir_true_vtx_Z;
  std::vector<double> hitTime;
  std::vector<double> hitTimeVXD;
  std::vector<double> pathLength;
  std::vector<double> effPathLength;
  std::vector<double> simPathLength;
  std::vector<double> simEffPathLength;
  std::vector<double> ImpactAngle;
  std::vector<double> Zvtx;
  std::vector<bool> Secondary ;
  std::vector<int> genStat ;
  std::vector<int>  NoOfSimsPerDgt ;
  std::vector<double> dirX;
  std::vector<double> dirY;
  std::vector<double> dirZ;
  std::vector<double> bsX;
  std::vector<double> bsY;
  std::vector<double> bsZ;
  std::vector<double> vxdhitsX;
  std::vector<double> vxdhitsY;
  std::vector<double> vxdhitsZ;
  std::vector<double> digitsX;
  std::vector<double> digitsY;
  std::vector<double> digitsZ;
  std::vector<int> vxdlayer ;
  std::vector<int> layer ;
  std::vector<int> subdet ;
  std::vector<int> stave ;
  std::vector<int> sensor ;
  std::vector<float> RecoTrackPt ;
  std::vector<float> Z0 ;
  std::vector<double> AllMCP_px ;
  std::vector<double> AllMCP_py ;
  std::vector<double> AllMCP_pz ;
  std::vector<double> AllMCP_vtxx ;
  std::vector<double> AllMCP_vtxy ;
  std::vector<double> AllMCP_vtxz ;
  std::vector<double> AllMCP_E ;
  std::vector<int> AllMCP_PDG ;
  //std::vector<double>  PrimariesPhiAngle ;

} ;


#endif



