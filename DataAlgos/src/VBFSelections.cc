#include "FinalStateAnalysis/DataAlgos/interface/VBFSelections.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "FinalStateAnalysis/DataAlgos/interface/VBFMVA.h"

// internal VBFMVA object
namespace {

static vbf::VBFMVA mva = vbf::VBFMVA();

vbf::VBFMVA* getMVA() {
  if (!mva.IsInitialized()) {
    edm::FileInPath thePath(
        "UserCode/MitHtt/data/VBFMVA/MuTau/VBFMVA_BDTG.weights.xml");
    mva.Initialize(thePath.fullPath());
  }
  return &mva;
}

}

VBFVariables computeVBFInfo(
    const std::vector<const reco::Candidate*>& hardScatter,
    const reco::Candidate::LorentzVector& metp4,
    const std::vector<const reco::Candidate*>& jets) {
  VBFVariables output;

  // number of initial jets
  output.nJets = jets.size();

  // Not enough jets
  if (output.nJets < 2)
    return output;

  assert(jets[0]->pt() > jets[1]->pt());

  output.leadJet = jets[0];
  output.subleadJet = jets[1];

  // Get 4vectors of two highest jets
  reco::Candidate::LorentzVector leadJet(jets[0]->p4());
  reco::Candidate::LorentzVector subleadJet(jets[1]->p4());

  reco::Candidate::LorentzVector dijet = leadJet + subleadJet;

  reco::Candidate::LorentzVector ditauvis;
  for (size_t i = 0; i < hardScatter.size(); ++i) {
    ditauvis += hardScatter[i]->p4();
  }

  // ditau = hard scatter + MET
  reco::Candidate::LorentzVector ditau = metp4 + ditauvis;

  output.mass = dijet.mass();
  output.deta = std::abs(leadJet.eta() - subleadJet.eta());
  output.dphi = std::abs(reco::deltaPhi(leadJet.phi(), subleadJet.phi()));
  output.pt1 = leadJet.pt();
  output.pt2 = subleadJet.pt();
  output.dijetpt = dijet.pt();
  output.ditaupt = ditau.pt();
  output.eta1 = leadJet.eta();
  output.eta2 = subleadJet.eta();
  output.dphihj = std::abs(reco::deltaPhi(dijet.phi(), ditau.phi()));
  output.c1 = std::min(
      std::abs(ditauvis.eta() - leadJet.eta()),
      std::abs(ditauvis.eta() - subleadJet.eta()));
  output.c2 = ditauvis.pt();

  // Figure out the central gap area
  float maxEta = std::max(leadJet.eta(), subleadJet.eta());
  float minEta = std::min(leadJet.eta(), subleadJet.eta());

  output.jets20 = 0;
  output.jets30 = 0;

  // Figure out central jet veto counts
  for (size_t k = 2; k < jets.size(); ++k) {
    // Check if central
    if(jets.at(k)->eta() > minEta && jets.at(k)->eta() < maxEta) {
      double pt = jets.at(k)->pt();
      if (pt > 20)
        output.jets20++;
      if (pt > 30)
        output.jets30++;
    }
  }

  // apply MVA
  getMVA()->applyMVA(output);

  return output;
}
