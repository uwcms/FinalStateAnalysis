// -*- C++ -*-
//
// Package:   FinalStateAnalysis/PatTools
// Class:    MiniAODBadMuonBadFilterEmbedder
// 
/**\class MiniAODBadMuonBadFilterEmbedder MiniAODBadMuonBadFilterEmbedder.cc FinalStateAnalysis/PatTools/plugins/MiniAODBadMuonBadFilterEmbedder.cc

 Description: [Take filters and turn them into tagged events]

 Implementation:
    [Notes on implementation]
*/
//
// Original Author:  Tyler Henry Ruggles
//      Created:  Tue, 07 Feb 2017 10:02:01 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

//Trigger Files
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

class MiniAODBadMuonBadFilterEmbedder : public edm::stream::EDProducer<> {
  public:
    explicit MiniAODBadMuonBadFilterEmbedder(const edm::ParameterSet&);
    ~MiniAODBadMuonBadFilterEmbedder();

  private:

    typedef std::map<std::string, bool> filterFiredMapType;
    typedef std::map<std::string, bool>::iterator map_iter;
    typedef edm::PtrVector<reco::Muon> muonPtrs;

    virtual void produce(edm::Event&, const edm::EventSetup&) override;

    // ----------member data ---------------------------

    // Bad Muon Filters
    edm::EDGetTokenT<muonPtrs> BadGlobalMuonFilterToken_;
    edm::EDGetTokenT<muonPtrs> CloneGlobalMuonFilterToken_;
    std::vector<std::string> filtersToCheck = {
      "badGlobalMuonFilter",
      "cloneGlobalMuonFilter",
      "BadChargedCandidateFilter",
      "BadPFMuonFilter",
    };
    muonPtrs filterbadGlobalMuon;
    muonPtrs filtercloneGlobalMuon;

    // MET Filters
    edm::EDGetTokenT<bool> BadChCandFilterToken_;
    edm::EDGetTokenT<bool> BadPFMuonFilterToken_;
    edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
    std::vector<std::string> metFilterPaths_;
    edm::EDGetTokenT< bool >ecalBadCalibFilterUpdate_token ;

    bool verbose_;
};


MiniAODBadMuonBadFilterEmbedder::MiniAODBadMuonBadFilterEmbedder(const edm::ParameterSet& pset)
{
  BadGlobalMuonFilterToken_ =  consumes<muonPtrs>(pset.getParameter<edm::InputTag>("badGlobalMuonTagger"));
  CloneGlobalMuonFilterToken_ =  consumes<muonPtrs>(pset.getParameter<edm::InputTag>("cloneGlobalMuonTagger"));
  BadChCandFilterToken_ = consumes<bool>(pset.getParameter<edm::InputTag>("BadChargedCandidateFilter"));
  BadPFMuonFilterToken_ = consumes<bool>(pset.getParameter<edm::InputTag>("BadPFMuonFilter"));
  triggerToken_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("triggerSrc"));
  metFilterPaths_ = pset.getParameter<std::vector<std::string> >("metFilterPaths");
  verbose_ = pset.getUntrackedParameter<bool> ("verbose",false);
  ecalBadCalibFilterUpdate_token= consumes< bool >(edm::InputTag("ecalBadCalibReducedMINIAODFilter"));

  produces< filterFiredMapType >();
  
}


MiniAODBadMuonBadFilterEmbedder::~MiniAODBadMuonBadFilterEmbedder()
{
}


void
MiniAODBadMuonBadFilterEmbedder::produce(edm::Event& evt, const edm::EventSetup& iSetup)
{
  std::unique_ptr< filterFiredMapType > output(new filterFiredMapType);
  // Add Bad Muon Filters
  for( std::string filter : filtersToCheck ) {
    output->insert( std::make_pair(filter, false) );
  } // end reset filters to false

  edm::Handle<muonPtrs> ifilterbadGlobalMuon;
  evt.getByToken(BadGlobalMuonFilterToken_, ifilterbadGlobalMuon);
  filterbadGlobalMuon = *ifilterbadGlobalMuon;

  edm::Handle<muonPtrs> ifiltercloneGlobalMuon;
  evt.getByToken(CloneGlobalMuonFilterToken_, ifiltercloneGlobalMuon);
  filtercloneGlobalMuon = *ifiltercloneGlobalMuon;

  // Count our bad objects and set our outMap
  int nCloneMuon = filtercloneGlobalMuon.size();
  int nBadMuon = filterbadGlobalMuon.size();
  if(nBadMuon)   output->at("badGlobalMuonFilter") = true;
  if(nCloneMuon) output->at("cloneGlobalMuonFilter") = true;

  // MET Filters
  // non-trigger style filters first
  edm::Handle<bool> badChCandHandle;
  edm::Handle<bool> badPFMuonHandle;
  evt.getByToken(BadChCandFilterToken_, badChCandHandle);
  evt.getByToken(BadPFMuonFilterToken_, badPFMuonHandle);
  bool badChCand = * badChCandHandle;
  bool badPFMuon = * badPFMuonHandle;
  if(!badChCand)  output->at("BadChargedCandidateFilter") = true;
  if(!badPFMuon)  output->at("BadPFMuonFilter") = true;


  // trigger style filters second
  edm::Handle<edm::TriggerResults> triggerBits;
  evt.getByToken(triggerToken_, triggerBits);
  //get the names of the triggers
  const edm::TriggerNames &names = evt.triggerNames(*triggerBits);

  for(unsigned int i=0;i<metFilterPaths_.size();++i) {
    bool fired_t=false;
    //std::cout<<"Find a Trigger Path: "<<metFilterPaths_[i]<<std::endl;
    for(unsigned int j=0 ,  n = triggerBits->size(); j < n && fired_t == false; ++j) {
      size_t trigPath = names.triggerName(j).find(metFilterPaths_.at(i));
      if ( trigPath == 0) {
        //std::cout<<"Found a Trigger Name!: "<<names.triggerName(j)<<std::endl;
        // If flag == true for good vertices, there are good vertices, so we take inverse
        bool fired = !(triggerBits->accept(j)); 
        output->insert( std::make_pair(metFilterPaths_.at(i), fired) );
      } // end found trigger result
    } // end trigger bits
  } // end MET path 

  edm::Handle< bool > passecalBadCalibFilterUpdate ;
  evt.getByToken(ecalBadCalibFilterUpdate_token,passecalBadCalibFilterUpdate);
  bool    _passecalBadCalibFilterUpdate =  !(*passecalBadCalibFilterUpdate );
  output->insert( std::make_pair("Flag_ecalBadCalibReducedMINIAODFilter", _passecalBadCalibFilterUpdate) );

  if(verbose_) {
    for(map_iter pair = output->begin(); pair != output->end(); pair++) {
      printf("Map Loop: %50s    val: %5i\n", pair->first.c_str(), pair->second );
    }
  } // end verbose


    evt.put(std::move(output));
 
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODBadMuonBadFilterEmbedder);



