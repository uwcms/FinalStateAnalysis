/*
  Embed into a PATObject ValueMap(s) result as user float. 
  Value maps are passed thrugh maps parameter as VPSet each 
  PSet contains and inputTag called src and a string 
  called label

  Author: Mauro Verzett (UZH)

  Plugins:
    PATElectronValueMapEmbedder
    PATMuonValueMapEmbedder
    PATTauValueMapEmbedder
    PATJetValueMapEmbedder
 */


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include <vector>
#include <string>
#include <iostream>
// class decleration
//
template <typename T>
class PATObjectValueMapEmbedder : public edm::EDProducer {

public:
  PATObjectValueMapEmbedder (const edm::ParameterSet& iConfig);
  ~PATObjectValueMapEmbedder() {}
  
  void produce(edm::Event& evt, const edm::EventSetup& es);

private:
  typedef std::vector<edm::ParameterSet> VPSet;
  typedef std::vector<T> TCollection;
  edm::InputTag src_;
  VPSet maps_;
};

template <typename T>
PATObjectValueMapEmbedder<T>::PATObjectValueMapEmbedder(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    maps_(iConfig.getParameter<VPSet>("maps"))
{
  produces< TCollection >();
}

template <typename T>
void PATObjectValueMapEmbedder<T>::produce(edm::Event& evt, const edm::EventSetup& es) 
{
  std::unique_ptr<TCollection> output(new TCollection);

  edm::Handle< edm::View<T> > inputs;
  evt.getByLabel(src_, inputs);

  // Build our output collection
  output->reserve(inputs->size());
  for (size_t iobj = 0; iobj < inputs->size(); ++iobj) {
    output->push_back(inputs->at(iobj));
  }

  // Embed map outputs (the ValueMap<float>s)
  for (VPSet::const_iterator imap_info = maps_.begin(); imap_info != maps_.end(); ++imap_info) {
    // Get the discriminator
    edm::InputTag map_name     = imap_info->getParameter<edm::InputTag>("src");
    std::string   ufloat_label = imap_info->getParameter<std::string>("label");

    edm::Handle<edm::ValueMap<float> > map;
    evt.getByLabel(map_name, map);

    // Embed in each pat jet
    for (size_t iobj = 0; iobj < inputs->size(); ++iobj) {
      //std::cout << "getting float value for jet " << iobj << " and value map: " << ufloat_label << std::endl;
      float map_result = (*map)[inputs->refAt(iobj)];
      output->at(iobj).addUserFloat(ufloat_label, map_result);
    }
  }

  // Store the jets in the event
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

typedef PATObjectValueMapEmbedder<pat::Muon>     PATMuonValueMapEmbedder;
typedef PATObjectValueMapEmbedder<pat::Tau>      PATTauValueMapEmbedder;
typedef PATObjectValueMapEmbedder<pat::Electron> PATElectronValueMapEmbedder;
typedef PATObjectValueMapEmbedder<pat::Jet>      PATJetValueMapEmbedder;

DEFINE_FWK_MODULE(PATMuonValueMapEmbedder);
DEFINE_FWK_MODULE(PATTauValueMapEmbedder);
DEFINE_FWK_MODULE(PATElectronValueMapEmbedder);
DEFINE_FWK_MODULE(PATJetValueMapEmbedder);
