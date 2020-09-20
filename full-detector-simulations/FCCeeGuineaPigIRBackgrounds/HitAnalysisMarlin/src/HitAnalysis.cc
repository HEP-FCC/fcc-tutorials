#include "HitAnalysis.h"
#include <iostream>

#include <IMPL/LCCollectionVec.h>
#include <IMPL/TrackerHitImpl.h>

#include <UTIL/CellIDDecoder.h>
#include <UTIL/CellIDEncoder.h>
#include "UTIL/LCTrackerConf.h"
#include <UTIL/BitSet32.h>

#include <marlin/Exceptions.h>

#ifdef MARLIN_USE_AIDA
#include <marlin/AIDAProcessor.h>

// ----- include for verbosity dependend logging ---------
#include "marlin/VerbosityLevels.h"
#endif

HitAnalysis aHitAnalysis ;


HitAnalysis::HitAnalysis() : Processor("HitAnalysis") {
  
  // modify processor description
  _description = "HitAnalysis does whatever it does ..." ;
  

  // register steering parameters: name, description, class-variable, default value
  

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "VTXBarrelCollectionName" , 
                           "Name of the VTX barrel SimTrackerHit collection"  ,
                           _vxdBarrelColName ,
                           std::string("VertexBarrelCollection") ) ;

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "VTXEndcapCollectionName" , 
                           "Name of the VTX endcaps SimTrackerHit collection"  ,
                           _vxdEndcapColName ,
                           std::string("VertexEndcapCollection") ) ;

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "InnerTrackerBarrelCollectionName" , 
                           "Name of the inner tracker barrel SimTrackerHit collection"  ,
                           _itbColName ,
                           std::string("InnerTrackerBarrelCollection") ) ;

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "InnerTrackerEndcapCollectionName" , 
                           "Name of the inner tracker endcaps SimTrackerHit collection"  ,
                           _iteColName ,
                           std::string("InnerTrackerEndcapCollection") ) ;

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "OuterTrackerBarrelCollectionName" , 
                           "Name of the outer tracker barrel SimTrackerHit collection"  ,
                           _otbColName ,
                           std::string("OuterTrackerBarrelCollection") ) ;

  registerInputCollection( LCIO::SIMTRACKERHIT,
                           "OuterTrackerEndcapCollectionName" , 
                           "Name of the outer tracker endcaps SimTrackerHit collection"  ,
                           _oteColName ,
                           std::string("OuterTrackerEndcapCollection") ) ;



  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "VXDTrackerHitsName" , 
                           "Name of the VTX barrel digits collection"  ,
                           _vxdBarrelDigitColName ,
                           std::string("VXDTrackerHits") ) ;

  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "VXDEndcapTrackerHitsName" , 
                           "Name of the VTX endcaps digits collection"  ,
                           _vxdEndcapDigitColName ,
                           std::string("VXDEndcapTrackerHits") ) ;

  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "ITrackerHitsName" , 
                           "Name of the inner tracker barrel digits collection"  ,
                           _itbDigitColName ,
                           std::string("ITrackerHits") ) ;

  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "ITrackerEndcapHitsName" , 
                           "Name of the inner tracker endcaps digits collection"  ,
                           _iteDigitColName ,
                           std::string("ITrackerEndcapHits") ) ;

  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "OTrackerHitsName" , 
                           "Name of the outer tracker barrel digits collection"  ,
                           _otbDigitColName ,
                           std::string("OTrackerHits") ) ;

  registerInputCollection( LCIO::TRACKERHITPLANE,
                           "OTrackerEndcapHitsName" , 
                           "Name of the outer tracker endcaps digits collection"  ,
                           _oteDigitColName ,
                           std::string("OTrackerEndcapHits") ) ;

  registerInputCollection( LCIO::LCRELATION,
			   "VXDTrackerHitRelations" , 
			   "VXD tracker hits relation to sim hits"  ,
			   _vxdTrkHitRelations,
			   std::string("VXDTrackerHitRelations") ) ;

  registerInputCollection( LCIO::LCRELATION,
			   "VXDEndcapTrackerHitRelations" , 
			   "VXD Endcap tracker relation hits to sim hits"  ,
			   _vxdECTrkHitRelations,
			   std::string("VXDEndcapTrackerHitRelations") ) ;


  registerInputCollection( LCIO::LCRELATION,
			   "InnerTrackerBarrelHitsRelations" , 
			   "ITB tracker hits relation to sim hits"  ,
			   _itbTrkHitRelations,
			   std::string("InnerTrackerBarrelHitsRelations") ) ;

  registerInputCollection( LCIO::LCRELATION,
			   "InnerTrackerEndcapHitsRelations" , 
			   "ITE tracker hits relation to sim hits"  ,
			   _iteTrkHitRelations,
			   std::string("InnerTrackerEndcapHitsRelations") ) ;

  registerInputCollection( LCIO::LCRELATION,
			   "OuterTrackerBarrelHitsRelations" , 
			   "OTB tracker hits relation to sim hits"  ,
			   _otbTrkHitRelations,
			   std::string("OuterTrackerBarrelHitsRelations") ) ;

  registerInputCollection( LCIO::LCRELATION,
			   "OuterTrackerEndcapHitsRelations" , 
			   "OTE tracker hits relation to sim hits"  ,
			   _oteTrkHitRelations ,
			   std::string("OuterTrackerEndcapHitsRelations") ) ;

  registerInputCollection( LCIO::TRACK,
			   "StudiedTracks" , 
			   "Name of the track collection"  ,
			   _trackColName ,
			   std::string("SiTracks") ) ; 

  registerInputCollection( LCIO::SIMCALORIMETERHIT,
			   "LumiCalCollectionName" , 
			   "Name of the LumiCal hit collection"  ,
			   _lumicalColName ,
			   std::string("LumiCalCollection") ) ;  

  registerInputCollection( LCIO::MCPARTICLE,
			   "MCParticleCollection" , 
			   "Name of the MCParticle input collection"  ,
			   _mcParticleCollectionName ,
			   std::string("MCParticle") ) ;

  }


void HitAnalysis::init() { 

  streamlog_out(DEBUG) << "   init called  " 
		       << std::endl ;

  // usually a good idea to
  printParameters() ;

  nEvt = 0;

  vxd_hits_barrel = 0;
  vxd_hits_endcaps  = 0;
  itb_hits_barrel  = 0;
  ite_hits_endcaps  = 0;
  otb_hits_barrel  = 0;
  ote_hits_endcaps  = 0;

  vxd_digits_barrel = 0;
  vxd_digits_endcaps  = 0;
  itb_digits_barrel  = 0;
  ite_digits_endcaps  = 0;
  otb_digits_barrel  = 0;
  ote_digits_endcaps  = 0;

  pixel_vxd = 0 ;
  fired_channels = 0 ;


}

void HitAnalysis::processRunHeader( LCRunHeader* run) { 


} 

void HitAnalysis::processEvent( LCEvent * evt ) { 

  
  // this gets called for every event 
  // usually the working horse ...

  //#ifdef MARLIN_USE_AIDA
  
  // this part of codes has a purpose to skip events that no hits are registered in the VXD/tracker
  // Can reduce significantly the time/size needed to process SR simulated data
  const StringVec*  colNames = evt->getCollectionNames() ;
  UTIL::BitField64 m_encoder( lcio::LCTrackerCellID::encoding_string() ) ;
  int sim_vxd_hits_barrel2 = 0 ; int sim_vxd_hits_endcaps2 =0 ; int sim_itb_hits_barrel2 =0 ; int sim_ite_hits_endcaps2 =0 ; int sim_otb_hits_barrel2 = 0 ; int  sim_ote_hits_endcaps2 = 0;
  for( StringVec::const_iterator it = colNames->begin() ; it != colNames->end() ; it++ ){
    //std::cout << " Available collection name " << *it << std::endl;
    
    if(  _vxdBarrelColName ==  *it ){
      sim_vxd_hits_barrel2 = evt->getCollection( *it )->getNumberOfElements();
    }
    if(  _vxdEndcapColName ==  *it ){
      sim_vxd_hits_endcaps2 = evt->getCollection( *it )->getNumberOfElements();
    }
    if( _itbColName  ==  *it ){
      sim_itb_hits_barrel2 = evt->getCollection( *it )->getNumberOfElements();
    }
    if( _iteColName  ==  *it ){
      sim_ite_hits_endcaps2  = evt->getCollection( *it )->getNumberOfElements();
    }
    if( _otbColName  ==  *it ){
      sim_otb_hits_barrel2 = evt->getCollection( *it )->getNumberOfElements();
    }
    if( _oteColName  ==  *it ){
      sim_ote_hits_endcaps2 = evt->getCollection( *it )->getNumberOfElements();
    }
  }
  if (sim_vxd_hits_barrel2==0 && sim_vxd_hits_endcaps2==0 && sim_itb_hits_barrel2==0 && sim_ite_hits_endcaps2 == 0 && sim_otb_hits_barrel2==0 && sim_ote_hits_endcaps2 == 0) 
    // evt->removeCollection(_mcParticleCollectionName) ;
    throw marlin::SkipEventException(this);


  if( isFirstEvent() ) {
      
    hits = new TTree("hits","hits") ;
    hits->Branch("sim_vxd_hits_barrel",&sim_vxd_hits_barrel,"sim_vxd_hits_barrel/I") ;
    hits->Branch("sim_vxd_hits_endcaps",&sim_vxd_hits_endcaps,"sim_vxd_hits_endcaps/I") ;
    hits->Branch("sim_itb_hits_barrel",&sim_itb_hits_barrel,"sim_itb_hits_barrel/I") ;
    hits->Branch("sim_ite_hits_endcaps",&sim_ite_hits_endcaps,"sim_ite_hits_endcaps/I") ;
    hits->Branch("sim_otb_hits_barrel",&sim_otb_hits_barrel,"sim_otb_hits_barrel/I") ;
    hits->Branch("sim_ote_hits_endcaps",&sim_ote_hits_endcaps,"sim_ote_hits_endcaps/I") ;
    hits->Branch("reco_vxd_digits_barrel",&reco_vxd_digits_barrel,"reco_vxd_digits_barrel/I") ;
    hits->Branch("reco_vxd_digits_endcaps",&reco_vxd_digits_endcaps,"reco_vxd_digits_endcaps/I") ;
    hits->Branch("reco_itb_digits_barrel",&reco_itb_digits_barrel,"reco_itb_digits_barrel/I") ;
    hits->Branch("reco_ite_digits_endcaps",&reco_ite_digits_endcaps,"reco_ite_digits_endcaps/I") ;
    hits->Branch("reco_otb_digits_barrel",&reco_otb_digits_barrel,"reco_otb_digits_barrel/I") ;
    hits->Branch("reco_ote_digits_endcaps",&reco_ote_digits_endcaps,"reco_ote_digits_endcaps/I") ;
    hits->Branch("event",&event,"event/I") ;
    hits->Branch("NoOfTracks",&NoOfTracks,"NoOfTracks/I") ;
    //hits->Branch("vxd_hits",&vxd_hits,"vxd_hits/I") ;
    hits->Branch("nEvt",&nEvt,"nEvt/I") ;
    hits->Branch("X",&X) ;
    hits->Branch("Y",&Y) ;
    hits->Branch("Z",&Z) ;
    hits->Branch("hitTime",&hitTime) ;
    hits->Branch("hitTimeVXD",&hitTimeVXD) ;
    hits->Branch("pathLength",&pathLength) ;
    hits->Branch("ImpactAngle",&ImpactAngle) ;
    hits->Branch("effPathLength",&effPathLength) ;
    hits->Branch("simPathLength",&simPathLength) ;
    hits->Branch("simEffPathLength",&simEffPathLength) ;
    hits->Branch("Zvtx",&Zvtx) ;
    hits->Branch("simX",&simX) ;
    hits->Branch("simY",&simY) ;
    hits->Branch("simZ",&simZ) ;
    hits->Branch("lcalX",&lcalX) ;
    hits->Branch("lcalY",&lcalY) ;
    hits->Branch("lcalZ",&lcalZ) ;
    hits->Branch("lcalNrg",&lcalNrg) ;
    hits->Branch("hitNrg",&hitNrg) ;
    hits->Branch("simhitPX",&simhitPx) ;
    hits->Branch("simhitPY",&simhitPy) ;
    hits->Branch("simhitPZ",&simhitPz) ;
    hits->Branch("simPDG",&simPDG) ;
    hits->Branch("simVXDPDG",&simPDG) ;
    hits->Branch("vtxX",&vtxX) ;
    hits->Branch("vtxY",&vtxY) ;
    hits->Branch("vtxZ",&vtxZ) ;
    hits->Branch("mcpPX",&mcpPX) ;
    hits->Branch("mcpPY",&mcpPY) ;
    hits->Branch("mcpPZ",&mcpPZ) ;
    hits->Branch("mcpE",&mcpE) ;
    hits->Branch("Secondary",&Secondary) ;
    hits->Branch("genStat",&genStat) ;
    hits->Branch("NoOfSimsPerDgt",&NoOfSimsPerDgt) ;
    hits->Branch("vxdlayer",&vxdlayer) ;
    hits->Branch("layer",&layer) ;
    hits->Branch("subdet",&subdet) ;
    hits->Branch("stave",&stave) ;
    hits->Branch("sensor",&sensor) ;
    hits->Branch("bsX",&bsX) ;
    hits->Branch("bsY",&bsY) ;
    hits->Branch("bsZ",&bsZ) ;
    hits->Branch("bs_true_vtx_X",&bs_true_vtx_X) ;
    hits->Branch("bs_true_vtx_Y",&bs_true_vtx_Y) ;
    hits->Branch("bs_true_vtx_Z",&bs_true_vtx_Z) ;
    hits->Branch("dirX",&dirX) ;
    hits->Branch("dirY",&dirY) ;
    hits->Branch("dirZ",&dirZ) ;
    hits->Branch("dir_true_vtx_X",&dir_true_vtx_X) ;
    hits->Branch("dir_true_vtx_Y",&dir_true_vtx_Y) ;
    hits->Branch("dir_true_vtx_Z",&dir_true_vtx_Z) ;
    hits->Branch("vxdhitsX",&vxdhitsX) ;
    hits->Branch("vxdhitsY",&vxdhitsY) ;
    hits->Branch("vxdhitsZ",&vxdhitsZ) ;
    hits->Branch("digitsX",&digitsX) ;
    hits->Branch("digitsY",&digitsY) ;
    hits->Branch("digitsZ",&digitsZ) ;
    hits->Branch("RecoTrackPt",&RecoTrackPt) ;
    hits->Branch("Z0",&Z0) ;
    hits->Branch("AllMCP_px",&AllMCP_px);
    hits->Branch("AllMCP_py",&AllMCP_py);
    hits->Branch("AllMCP_pz",&AllMCP_pz);
    hits->Branch("AllMCP_E",&AllMCP_E);
    hits->Branch("AllMCP_PDG",&AllMCP_PDG);
    hits->Branch("AllMCP_vtxx",&AllMCP_vtxx);
    hits->Branch("AllMCP_vtxy",&AllMCP_vtxy);
    hits->Branch("AllMCP_vtxz",&AllMCP_vtxz);
    hits->Branch("nmcp",&nmcp,"nmcp/I") ;
    hits->Branch("EventWithPrimsAtVXD",&EventWithPrimsAtVXD,"EventWithPrimsAtVXD/I") ;
    //hits->Branch("totalEnergy",&totalEnergy,"totalEnergy/D") ;
    //hits->Branch("PrimariesPhiAngle",&PrimariesPhiAngle) ;

    gNoOfHits = new TH1F("gNoOfHits","hits/event",6,0,6) ;
    gNoOfHits->SetMinimum(0.01);
    JustHits = new TH1F("JustHits","hits/event",6,0,6) ;
    JustHits->SetMinimum(0.01);
    gNoOfDigits = new TH1F("gNoOfDigits","hits/event",6,0,6) ;
    c1 = new TCanvas("c1", "c1",11,43,700,500);
    c1->SetLogy();
  }


  X.clear(); Y.clear();  Z.clear();
  simX.clear();  simY.clear();  simZ.clear();
  lcalX.clear();  lcalY.clear();  lcalZ.clear();
  simhitPx.clear();  simhitPy.clear();  simhitPz.clear();
  simPDG.clear();  simVXDPDG.clear();
  dirX.clear();  dirY.clear();  dirZ.clear();
  digitsX.clear();  digitsY.clear();  digitsZ.clear();
  vxdhitsX.clear();  vxdhitsY.clear();  vxdhitsZ.clear();
  bsX.clear();  bsY.clear();  bsZ.clear();
  vtxX.clear();  vtxY.clear();  vtxZ.clear();
  mcpPX.clear();  mcpPY.clear();  mcpPZ.clear(); mcpE.clear();
  bs_true_vtx_X.clear();  bs_true_vtx_Y.clear();  bs_true_vtx_Z.clear();
  dir_true_vtx_X.clear();  dir_true_vtx_Y.clear();  dir_true_vtx_Z.clear();
  hitTime.clear();  Zvtx.clear();  pathLength.clear(); hitTimeVXD.clear(); effPathLength.clear(); ImpactAngle.clear();
  simPathLength.clear();      simEffPathLength.clear();
  Secondary.clear(); vxdlayer.clear();   layer.clear();
  NoOfSimsPerDgt.clear();   lcalNrg.clear();  hitNrg.clear();
  RecoTrackPt.clear();   subdet.clear();   Z0.clear(); stave.clear();  sensor.clear();
  AllMCP_px.clear();  AllMCP_py.clear();  AllMCP_pz.clear(); AllMCP_E.clear(); AllMCP_PDG.clear(); 
  AllMCP_vtxx.clear();  AllMCP_vtxy.clear();  AllMCP_vtxz.clear();
  genStat.clear();
  //totalEnergy = 0 ;
  //PrimariesPhiAngle.clear();

  event = nEvt;

  std::cout << " EVENT : " << nEvt << std::endl ;

  /*
  int flagVXDBarrel = 0 ;    int flagVXDEndcaps = 0 ;
  int flagITBarrel = 0 ;     int flagITEndcaps = 0 ; 
  int flagOTBarrel = 0 ;     int flagOTEndcaps = 0 ; 
  */
  // MCParticle Loop
  // Below we register information for all MC particles, and not only the ones that create a hit in the detector
  LCCollection* MonteCarlo = evt->getCollection( _mcParticleCollectionName );
  nmcp = MonteCarlo->getNumberOfElements();

  double EnergyCounter = 0 ;
  EventWithPrimsAtVXD = 0 ;
  
  for (int i = 0 ; i < nmcp ; i++ ){
    MCParticle *mcp = (MCParticle*) MonteCarlo->getElementAt( i ) ;
    AllMCP_px.push_back( mcp->getMomentum()[0]);
    AllMCP_py.push_back( mcp->getMomentum()[1]);
    AllMCP_pz.push_back( mcp->getMomentum()[2]);
    AllMCP_vtxx.push_back( mcp->getVertex()[0]);
    AllMCP_vtxy.push_back( mcp->getVertex()[1]);
    AllMCP_vtxz.push_back( mcp->getVertex()[2]);
    genStat.push_back(mcp->getGeneratorStatus());
    AllMCP_E.push_back( mcp->getEnergy());
    if ( mcp->getEnergy() > 100){
      std::cout << " OOOP, ti paizetai sto gegonos " << nEvt << std::endl ;
    }
    AllMCP_PDG.push_back( mcp->getPDG());
  }

  for( StringVec::const_iterator it = colNames->begin() ; it != colNames->end() ; it++ ){
    //std::cout << " Available collection name " << *it << std::endl;
    
    if(  _vxdBarrelColName ==  *it ){
      //flagVXDBarrel = 1 ;
      sim_vxd_hits_barrel = evt->getCollection( *it )->getNumberOfElements();
      vxd_hits_barrel = vxd_hits_barrel + sim_vxd_hits_barrel ;
    }
    if(  _vxdEndcapColName ==  *it ){
      //flagVXDEndcaps = 1 ;
      sim_vxd_hits_endcaps = evt->getCollection( *it )->getNumberOfElements();
      vxd_hits_endcaps = vxd_hits_endcaps + sim_vxd_hits_endcaps ;
    }
    if( _itbColName  ==  *it ){
      sim_itb_hits_barrel = evt->getCollection( *it )->getNumberOfElements();
      //flagITBarrel = 1 ;
      itb_hits_barrel = itb_hits_barrel + sim_itb_hits_barrel ;
    }
    if( _iteColName  ==  *it ){
      sim_ite_hits_endcaps  = evt->getCollection( *it )->getNumberOfElements();
      //flagITEndcaps = 1 ;
      ite_hits_endcaps = ite_hits_endcaps + sim_ite_hits_endcaps ; 
    }
    if( _otbColName  ==  *it ){
      sim_otb_hits_barrel = evt->getCollection( *it )->getNumberOfElements();
      //flagOTBarrel = 1 ;
      otb_hits_barrel = otb_hits_barrel + sim_otb_hits_barrel ;
    }
    if( _oteColName  ==  *it ){
      sim_ote_hits_endcaps = evt->getCollection( *it )->getNumberOfElements();
      //flagOTEndcaps = 1 ;   
      ote_hits_endcaps = ote_hits_endcaps + sim_ote_hits_endcaps ;
    }


    if(  _vxdBarrelDigitColName ==  *it ){
      reco_vxd_digits_barrel = evt->getCollection( *it )->getNumberOfElements();
      vxd_digits_barrel = vxd_digits_barrel + reco_vxd_digits_barrel;
    }
    if(  _vxdEndcapDigitColName ==  *it ){
      reco_vxd_digits_endcaps = evt->getCollection( *it )->getNumberOfElements();
      vxd_digits_endcaps = vxd_digits_endcaps + reco_vxd_digits_endcaps ;
    }
    if( _itbDigitColName  ==  *it ){
      reco_itb_digits_barrel = evt->getCollection( *it )->getNumberOfElements();
      itb_digits_barrel = itb_digits_barrel + reco_itb_digits_barrel; 
    }
    if( _iteDigitColName  ==  *it ){
      reco_ite_digits_endcaps  = evt->getCollection( *it )->getNumberOfElements();
      ite_digits_endcaps = ite_digits_endcaps + reco_ite_digits_endcaps ; 
    }
    if( _otbDigitColName  ==  *it ){
      reco_otb_digits_barrel = evt->getCollection( *it )->getNumberOfElements();
      otb_digits_barrel = otb_digits_barrel + reco_otb_digits_barrel; 
    }
    if( _oteDigitColName  ==  *it ){
      reco_ote_digits_endcaps = evt->getCollection( *it )->getNumberOfElements();
      ote_digits_endcaps = ote_digits_endcaps + reco_ote_digits_endcaps ;
    }

    // Relevant only if run track reconstruction, commented out for the moment
    /*
    if( _trackColName  ==  *it ){   
    
      LCCollection* StudiedTracks = evt->getCollection( _trackColName );
      NoOfTracks = StudiedTracks->getNumberOfElements();
      
      for ( int ii = 0; ii < NoOfTracks; ii++ ) {
	
	Track *RecoTrack = dynamic_cast<Track*>( StudiedTracks->getElementAt( ii ) ) ;
	float recoPt = fabs(((3.0/10000.0)*2.0)/(RecoTrack->getOmega())) ;
	RecoTrackPt.push_back(recoPt) ;
	float recoZ0  = RecoTrack->getZ0();
	Z0.push_back(recoZ0);
      }
    }
    */

    LCCollection* Col = evt->getCollection( *it ) ;

      
    if (*it == _vxdBarrelColName || *it == _vxdEndcapColName || *it == _itbColName  || *it == _iteColName || *it == _otbColName || *it == _oteColName ){

      int simhits = Col->getNumberOfElements();
      CellIDDecoder<SimTrackerHit> cellid_decoder( Col) ;
      for (int i=0;i<simhits;i++){
	
	SimTrackerHit* simhit = dynamic_cast<SimTrackerHit*>( Col->getElementAt( i ) ) ;
	std::cout << " Tracker hit " << simhit << std::endl ;
	if (simhit){
	  simX.push_back(simhit->getPosition()[0]);
	  simY.push_back(simhit->getPosition()[1]);
	  simZ.push_back(simhit->getPosition()[2]);

	  hitTime.push_back(simhit->getTime());
	  hitNrg.push_back(simhit->getEDep() );

	  simhitPx.push_back(simhit->getMomentum()[0]);
	  simhitPy.push_back(simhit->getMomentum()[1]);
	  simhitPz.push_back(simhit->getMomentum()[2]);

	  int Layer = getLayer(simhit,m_encoder);
	  int SubDet = getSubdetector(simhit,m_encoder);
	  layer.push_back(Layer);
	  subdet.push_back(SubDet);

	  // information from the MCParticle that made the hit
	  MCParticle *mcp = simhit->getMCParticle() ;
	  if (mcp){
	    vtxX.push_back(mcp->getVertex()[0]);
	    vtxY.push_back(mcp->getVertex()[1]);
	    vtxZ.push_back(mcp->getVertex()[2]);

	    simPDG.push_back(mcp->getPDG()) ;

	    mcpPX.push_back(mcp->getMomentum()[0]);
	    mcpPY.push_back(mcp->getMomentum()[1]);
	    mcpPZ.push_back(mcp->getMomentum()[2]);

	    mcpE.push_back(mcp->getEnergy());
	    Secondary.push_back(mcp->isCreatedInSimulation() );
	  }

	  simPathLength.push_back(simhit->getPathLength());
	  double simcosa = (simhit->getMomentum()[2]) / (sqrt(simhit->getMomentum()[0]*simhit->getMomentum()[0] +  simhit->getMomentum()[1]*simhit->getMomentum()[1] + simhit->getMomentum()[2]*simhit->getMomentum()[2] )) ;
	  
	  double sim_eff_path_length = fabs((simhit->getPathLength()) * simcosa) ;
	  simEffPathLength.push_back( sim_eff_path_length ) ;
	  // gives the number of pixels fired, given a pitch of 20μm. FIX ME: the pitch should be a processor parameter. The formula also is ad hoc. 
	  fired_channels = fired_channels + (int(sim_eff_path_length/0.02) + 1)*3+2 ;
	}
      }
    }


    if (*it == _vxdBarrelDigitColName || *it == _vxdEndcapDigitColName || *it == _itbDigitColName  || *it == _iteDigitColName || *it == _otbDigitColName || *it == _oteDigitColName ){


      //std::cout << " Taking digitised collection " << *it << " with number of elements " << evt->getCollection( *it )->getNumberOfElements() << std::endl;
    
      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){
	  X.push_back(digit->getPosition()[0]);
	  Y.push_back(digit->getPosition()[1]);
	  Z.push_back(digit->getPosition()[2]);

	}
      }
    }

    /*
    if (*it == _vxdEndcapDigitColName ){

      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* VTXEdgtsToSimhits = evt->getCollection( _vxdECTrkHitRelations ) ;
	  LCRelationNavigator navDtH( VTXEdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  //NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);
	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }




    if (*it == _itbDigitColName ){

      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* ITBdgtsToSimhits = evt->getCollection( _itbTrkHitRelations ) ;
	  LCRelationNavigator navDtH( ITBdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  //NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);
	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }



    if (*it == _iteDigitColName ){

      int digits = Col->getNumberOfElements();

      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* ITEdgtsToSimhits = evt->getCollection( _iteTrkHitRelations ) ;
	  LCRelationNavigator navDtH( ITEdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  //NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);
	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }




    if (*it == _otbDigitColName ){

      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* OTBdgtsToSimhits = evt->getCollection( _otbTrkHitRelations ) ;
	  LCRelationNavigator navDtH( OTBdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  //NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);
	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }





    if (*it == _oteDigitColName ){

      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* OTEdgtsToSimhits = evt->getCollection( _oteTrkHitRelations ) ;
	  LCRelationNavigator navDtH( OTEdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  //NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);
	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }








    if (*it == _vxdBarrelDigitColName ){

      int digits = Col->getNumberOfElements();
      for (int i=0;i<digits;i++){
	
	TrackerHit* digit = dynamic_cast<TrackerHit*>( Col->getElementAt( i ) ) ;
	if (digit){

	  vxdhitsX.push_back(digit->getPosition()[0]);
	  vxdhitsY.push_back(digit->getPosition()[1]);
	  vxdhitsZ.push_back(digit->getPosition()[2]);
	  digitsX.push_back(digit->getPosition()[0]);
	  digitsY.push_back(digit->getPosition()[1]);
	  digitsZ.push_back(digit->getPosition()[2]);

	  LCCollection* VTXBdgtsToSimhits = evt->getCollection( _vxdTrkHitRelations ) ;
	  LCRelationNavigator navDtH( VTXBdgtsToSimhits ) ;

	  const EVENT::LCObjectVec& relsimhits = navDtH.getRelatedToObjects(digit);
	  NoOfSimsPerDgt.push_back(relsimhits.size());
	  for(unsigned k = 0; k < relsimhits.size(); k++){
	    SimTrackerHit* rawHit = dynamic_cast< SimTrackerHit* >(relsimhits[k]);

	    hitTimeVXD.push_back(rawHit->getTime());
	    pathLength.push_back(rawHit->getPathLength());

	    double Px = rawHit->getMomentum()[0];
	    double Py = rawHit->getMomentum()[1];
	    double Pz = rawHit->getMomentum()[2];

	    double cosa = Pz / (sqrt(Px*Px + Py*Py + Pz*Pz)) ;

	    ImpactAngle.push_back(cosa);

	    double eff_path_length = fabs((rawHit->getPathLength()) * cosa) ;
	    effPathLength.push_back( eff_path_length ) ;

	    pixel_vxd = pixel_vxd + (int(eff_path_length/0.02) + 1)*3+2 ;
	    simVXDPDG.push_back(rawHit->getMCParticle()->getPDG());

	    if (rawHit->getMCParticle()->isCreatedInSimulation()){
	      //dgtFromSecondaries.push_back(digit);
	      bsX.push_back(digit->getPosition()[0]);
	      bsY.push_back(digit->getPosition()[1]);
	      bsZ.push_back(digit->getPosition()[2]);
	      bs_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      bs_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      bs_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	    else{
	      //directDgts.push_back(digit);
	      dirX.push_back(digit->getPosition()[0]);
	      dirY.push_back(digit->getPosition()[1]);
	      dirZ.push_back(digit->getPosition()[2]);
	      dir_true_vtx_X.push_back(rawHit->getMCParticle()->getVertex()[0]);
	      dir_true_vtx_Y.push_back(rawHit->getMCParticle()->getVertex()[1]);
	      dir_true_vtx_Z.push_back(rawHit->getMCParticle()->getVertex()[2]);

	    }
	  }
	}
      }
    }
    */
    //-----------------------------------------------------------------------------------------------
    // -- Lumical simhits study ---------------------------------------------------------------------
    //-----------------------------------------------------------------------------------------------
    if (*it == _lumicalColName ){
      LCCollection *LCCol = evt->getCollection( _lumicalColName ) ;
      int LumiHits = LCCol->getNumberOfElements() ;
      
      for ( int kk = 0 ; kk < LumiHits ; kk ++) {
	
	SimCalorimeterHit* lcalhit = dynamic_cast<SimCalorimeterHit*>( LCCol->getElementAt( kk) ) ;
	
	if (lcalhit){
	  lcalX.push_back(lcalhit->getPosition()[0]);
	  lcalY.push_back(lcalhit->getPosition()[1]);
	  lcalZ.push_back(lcalhit->getPosition()[2]);
	  lcalNrg.push_back(lcalhit->getEnergy());

	  //std::cout << "adding hit at Z " << lcalhit->getPosition()[2] << " and radius " << sqrt((lcalhit->getPosition()[0]*lcalhit->getPosition()[0]) + (lcalhit->getPosition()[1]*lcalhit->getPosition()[1])) <<   " with energy " << lcalhit->getEnergy() << std::endl ;

	}
      }
    }
    
    
  }  // end of loop on collections

  totalEnergy = EnergyCounter ;

  hits->Fill();
  nEvt++; 
  //#endif


  



    
}



void HitAnalysis::check( LCEvent * evt ) { 
  // nothing to check here - could be used to fill checkplots in reconstruction processor
}


void HitAnalysis::end(){ 

  //std::cout << " total number of simulated hits : VXD barrel " << vxd_hits_barrel << " VXD endcap " << vxd_hits_endcaps << " Inner tracker barrel " << itb_hits_barrel << " Inner tracker endcaps " << ite_hits_endcaps << " Outer tracker barrel " << otb_hits_barrel << " outer barrel endcaps " << ote_hits_endcaps << " total number of reconstructed hits : VXD barrel " << vxd_digits_barrel << " VXD endcap " << vxd_digits_endcaps << " Inner tracker barrel " << itb_digits_barrel << " Inner tracker endcaps " << ite_digits_endcaps << " Outer tracker barrel " << otb_digits_barrel << " outer barrel endcaps " << ote_digits_endcaps << std::endl ;

  // simulated hits
  //double HitsPerEvt[6] = {vxd_hits_barrel*1./(nEvt*100000.),vxd_hits_endcaps*1./(nEvt*100000.),itb_hits_barrel*1./(nEvt*100000.),ite_hits_endcaps*1./(nEvt*100000.),otb_hits_barrel*1./(nEvt*100000.),ote_hits_endcaps*1./(nEvt*100000.) };
  double HitsPerEvt[6] = {vxd_hits_barrel*1./(nEvt*1.),vxd_hits_endcaps*1./(nEvt*1.),itb_hits_barrel*1./(nEvt*1.),ite_hits_endcaps*1./(nEvt*1.),otb_hits_barrel*1./(nEvt*1.),ote_hits_endcaps*1./(nEvt*1.) };

  if (gNoOfHits){

  for (int i=0; i<6; i++){
    gNoOfHits->GetXaxis()->SetBinLabel(i+1,ABC[i]);
    gNoOfHits->SetBinContent(i+1,HitsPerEvt[i]);
  } 
  gNoOfHits->Write();
  }
  /*
  // just hits, no normalised per BX
  c1->cd();
  gPad->SetLogy() ;
  double TotalHits[6] = {2*vxd_hits_barrel,2*vxd_hits_endcaps,2*itb_hits_barrel,2*ite_hits_endcaps,2*otb_hits_barrel,2*ote_hits_endcaps };
  for (int i=0; i<6; i++){
    JustHits->GetXaxis()->SetBinLabel(i+1,ABC[i]);
    JustHits->SetBinContent(i+1,TotalHits[i]);
  } 
  JustHits->Draw();
  JustHits->Write();
  */

  // reconstructed digits
  /*
  double DigitsPerEvt[6] = {vxd_digits_barrel*1./nEvt*1.,vxd_digits_endcaps*1./nEvt*1.,itb_digits_barrel*1./nEvt*1.,ite_digits_endcaps*1./nEvt*1.,otb_digits_barrel*1./nEvt*1.,ote_digits_endcaps*1./nEvt*1., };
  
  for (int i=0; i<6; i++){
    gNoOfDigits->GetXaxis()->SetBinLabel(i+1,ABC[i]);
    gNoOfDigits->SetBinContent(i+1,DigitsPerEvt[i]);
  } 
  gNoOfDigits->Write();
  */
  /*
  int FiringPixels = pixel_vxd*1. / nEvt*1. ;
  int FiringChannels = fired_channels*1. / nEvt*1. ;
  std::cout << " firing pixels / event " << FiringPixels << std::endl ;
  std::cout << " firing channels / event " << FiringChannels << std::endl ;
  */
}

int HitAnalysis::getSubdetector(SimTrackerHit* hit, UTIL::BitField64 &encoder){
  const int celId = hit->getCellID0() ;
  encoder.reset();
  encoder.setValue(celId) ;
  int subdetector = encoder[lcio::LCTrackerCellID::subdet()];
  return subdetector;
}

int HitAnalysis::getLayer(SimTrackerHit* hit, UTIL::BitField64 &encoder){
  const int celId = hit->getCellID0() ;
  encoder.reset();
  encoder.setValue(celId) ;
  int Layer = encoder[lcio::LCTrackerCellID::layer()];
  //std::cout << " Layer = " << Layer << std::endl;
  return Layer;
}
