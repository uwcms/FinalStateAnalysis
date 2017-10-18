/*
 * =====================================================================================
 *
 *       Filename:  PATJetPUIDEmbedder.cc
 *
 *    Description:  Embeds PAT Jet PU ID
 *                  https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"

class PATJetPUIDEmbedder : public edm::EDProducer {
  public:
    PATJetPUIDEmbedder(const edm::ParameterSet& pset);
    virtual ~PATJetPUIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    typedef std::vector<edm::InputTag> VInputTag;
    edm::InputTag src_;
    VInputTag discriminants_;
    VInputTag ids_;

};
PATJetPUIDEmbedder::PATJetPUIDEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  discriminants_ = pset.getParameter<VInputTag>("discriminants");
  ids_ = pset.getParameter<VInputTag>("ids");
  produces<pat::JetCollection>();
}
void PATJetPUIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > inputs;
  evt.getByLabel(src_, inputs);

  // Build our output collection
  output->reserve(inputs->size());
  for (size_t ijet = 0; ijet < inputs->size(); ++ijet) {
    output->push_back(inputs->at(ijet));
  }

  /*  Stuff to embed (from twiki):
      edm::ValueMap<StoredPileupJetIdentifier> "puJetId" "" "PAT"
      edm::ValueMap<float> "puJetMva" "fullDiscriminant" "PAT"
      edm::ValueMap<float> "puJetMva" "cutbasedDiscriminant" "PAT"
      edm::ValueMap<float> "puJetMva" "simpleDiscriminant" "PAT"
      edm::ValueMap<int> "puJetMva" "fullId" "PAT"
      edm::ValueMap<int> "puJetMva" "cutbased" "PAT"
      edm::ValueMap<int> "puJetMva" "simpleId" "PAT"
   *  */

  // Embed MVA outputs (the ValueMap<float>s)
  for (size_t iMVA = 0; iMVA < discriminants_.size(); ++iMVA) {
    // Get the discriminator
    edm::Handle<edm::ValueMap<float> > disc;
    evt.getByLabel(discriminants_[iMVA], disc);
    const std::string& mvaName = discriminants_.at(iMVA).instance();

    // Embed in each pat jet
    for (size_t ijet = 0; ijet < inputs->size(); ++ijet) {
      float mva = (*disc)[inputs->refAt(ijet)->originalObjectRef()];
      output->at(ijet).addUserFloat(mvaName, mva);
    }
  }

  // Embed IDs - these come in loose, medium and tight
  for (size_t iDisc = 0; iDisc < ids_.size(); ++iDisc) {
    edm::Handle<edm::ValueMap<int> > id;
    evt.getByLabel(ids_[iDisc], id);
    const std::string& idName = ids_.at(iDisc).instance();

    // Embed in each pat jet
    for (size_t ijet = 0; ijet < inputs->size(); ++ijet) {
      int idflag = (*id)[inputs->refAt(ijet)->originalObjectRef()];
      bool passesLoose = PileupJetIdentifier::passJetId(
          idflag, PileupJetIdentifier::kLoose);
      bool passesMedium = PileupJetIdentifier::passJetId(
          idflag, PileupJetIdentifier::kMedium);
      bool passesTight = PileupJetIdentifier::passJetId(
          idflag, PileupJetIdentifier::kTight);
      output->at(ijet).addUserInt(idName, idflag);
      output->at(ijet).addUserInt(idName + "Loose", passesLoose);
      output->at(ijet).addUserInt(idName + "Medium", passesMedium);
      output->at(ijet).addUserInt(idName + "Tight", passesTight);
    }
  }

  // Store the jets in the event
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetPUIDEmbedder);

