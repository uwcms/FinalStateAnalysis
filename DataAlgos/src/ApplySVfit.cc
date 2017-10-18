///////////
// imp of function getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"
#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"
#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include <iostream>
#include <iomanip>
#include <map>
#include <stdio.h>
#include <string>


namespace ApplySVfit {

  // Caching and translation layer
  typedef std::map<size_t, std::vector<double> > SVFitCache;
  static SVFitCache theCache;
  static edm::EventID lastSVfitEvent; // last processed event

  std::vector<double> getSVfitMass(std::vector<reco::CandidatePtr>& cands,
                      const pat::MET& met, const ROOT::Math::SMatrix2D& covMET, unsigned int verbosity,
                      const edm::EventID& evtId) {


    std::vector<double> returnVector;

    // Check if this a new event
    if (evtId != lastSVfitEvent) {
      theCache.clear();
    }
    lastSVfitEvent = evtId;

    // Hash our candidates - NB cands will be sorted in place
    size_t hash = hashCandsByContent(cands);
    // std::cout << "EvtID: " << evtId << " Hash: " << hash << std::endl;

    // Check if we've already computed it
    SVFitCache::const_iterator lookup = theCache.find(hash);
    if (lookup != theCache.end()) {
      return lookup->second;
    }

    // No pain no gain
    Vector measuredMET = met.momentum();
    std::vector<MeasuredTauLepton> measuredTauLeptons;

    for (size_t dau = 0; dau < cands.size(); ++dau) {
      int pdgId = std::abs(cands[dau]->pdgId());
      if (pdgId == 11)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToElecDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else if (pdgId == 13)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToMuDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else if (pdgId == 15)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToHadDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else
        throw cms::Exception("BadPdgId") << "I don't understand PDG id: "
          << pdgId << ", sorry." << std::endl;
    }

    SVfitStandaloneAlgorithm algo(measuredTauLeptons, measuredMET.x(), measuredMET.y(), 
                                  convert_matrix(covMET), verbosity);
    algo.addLogM(false);
    edm::FileInPath inputFileName_visPtResolution("TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root");
    TH1::AddDirectory(false);  
    TFile* inputFile_visPtResolution = new TFile(inputFileName_visPtResolution.fullPath().data());
    //algo.shiftVisPt(true, inputFile_visPtResolution);
    algo.integrateMarkovChain();
    //double mass = algo.getMass(); // mass uncertainty not implemented yet

    delete inputFile_visPtResolution;

    returnVector.push_back( algo.mass() );
    returnVector.push_back( algo.pt() );
    returnVector.push_back( algo.eta() );
    returnVector.push_back( algo.phi() );
    returnVector.push_back( algo.fittedMET().Rho() );

    theCache[hash] = returnVector;
    return returnVector;

  }

  TMatrixD convert_matrix(const ROOT::Math::SMatrix2D& mat)
  {
    const TMatrixD output = TMatrixD(mat.kRows, mat.kCols, mat.Array());
    return output;
  }

  TMatrixD convert_matrix(const TMatrixD& mat) 
  {
    return mat;
  }

} // namespace ApplySVfit
