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


class MiniAODBadMuonBadFilterEmbedder : public edm::stream::EDProducer<> {
  public:
    explicit MiniAODBadMuonBadFilterEmbedder(const edm::ParameterSet&);
    ~MiniAODBadMuonBadFilterEmbedder();

  private:

    typedef std::map<std::string, bool> filterFiredMapType;
    typedef edm::PtrVector<reco::Muon> muonPtrs;

    virtual void produce(edm::Event&, const edm::EventSetup&) override;

    // ----------member data ---------------------------

    edm::EDGetTokenT<muonPtrs> BadGlobalMuonFilterToken_;
    edm::EDGetTokenT<muonPtrs> CloneGlobalMuonFilterToken_;
    std::vector<std::string> filtersToCheck = {
      "badGlobalMuonFilter",
      "cloneGlobalMuonFilter",
    };
    muonPtrs filterbadGlobalMuon;
    muonPtrs filtercloneGlobalMuon;
    bool verbose_;
};


MiniAODBadMuonBadFilterEmbedder::MiniAODBadMuonBadFilterEmbedder(const edm::ParameterSet& pset)
{
  BadGlobalMuonFilterToken_ =  consumes<muonPtrs>(pset.getParameter<edm::InputTag>("badGlobalMuonTagger"));
  CloneGlobalMuonFilterToken_ =  consumes<muonPtrs>(pset.getParameter<edm::InputTag>("cloneGlobalMuonTagger"));
  verbose_ = pset.getUntrackedParameter<bool> ("verbose",false);

  produces< filterFiredMapType >();
  
}


MiniAODBadMuonBadFilterEmbedder::~MiniAODBadMuonBadFilterEmbedder()
{
}


void
MiniAODBadMuonBadFilterEmbedder::produce(edm::Event& evt, const edm::EventSetup& iSetup)
{
  std::auto_ptr< filterFiredMapType > output(new filterFiredMapType);
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

  if(verbose_) {
    for( std::string filter : filtersToCheck ) {
      printf("Map Loop: %s    val: %i\n", filter.c_str(), output->at( filter ));
    }
  } // end verbose


  evt.put(output);
 
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODBadMuonBadFilterEmbedder);



