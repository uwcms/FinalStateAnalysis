///////////
// imp of function getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfitLFV.h"
#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"
#include "TauAnalysis/SVfitStandaloneLFV/interface/SVfitStandaloneAlgorithmLFV.h"
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


namespace ApplySVfitLFV {

  // Caching and translation layer
  typedef std::map<size_t, double> SVLFVFitCache;
  static SVLFVFitCache theCacheLFV;
  static edm::EventID lastSVLFVfitEvent; // last processed event

  double getSVfitMassLFV(std::vector<reco::CandidatePtr>& cands,
                      const pat::MET& met, const ROOT::Math::SMatrix2D& covMET, unsigned int verbosity,
                      const edm::EventID& evtId, bool mutau) {


    // Check if this a new event
    if (evtId != lastSVLFVfitEvent) {
      theCacheLFV.clear();
    }
    lastSVLFVfitEvent = evtId;

    // Hash our candidates - NB cands will be sorted in place
    size_t hash = hashCandsByContent(cands);
    // std::cout << "EvtID: " << evtId << " Hash: " << hash << std::endl;

    // Check if we've already computed it
    SVLFVFitCache::const_iterator lookup = theCacheLFV.find(hash);
    if (lookup != theCacheLFV.end()) {
      return lookup->second;
    }

    // No pain no gain
    Vector measuredMET = met.momentum();
    std::vector<MeasuredTauLepton> measuredTauLeptons;

    int foundMuon=0, foundElectron=0, foundTau=0;
    for (size_t dau = 0; dau < cands.size(); ++dau) {
          int pdgId = std::abs(cands[dau]->pdgId()); 
          if (pdgId == 11) foundElectron++;
          if (pdgId == 13) foundMuon++;
          if (pdgId == 15) foundTau++;
    }

    int channel=0;
    if(foundTau+foundElectron+foundMuon>2) { /*This is not a LFV decay*/  return -1;}
    else if(foundTau >1) { /*This is not a LFV decay*/  return -1;}
    else if(foundMuon>1 || foundElectron>1) { /*This could be a LFV decay, but we cannot target this FS like this */  return -1;} 
    else if (foundMuon==1 && foundTau==1 && foundElectron==0) { channel=0;}
    else if (foundMuon==0 && foundTau==1 && foundElectron==1) { channel=1;}
    else if (foundMuon==1 && foundTau==0 && foundElectron==1) { if(mutau)channel=2; else channel=3;} 

    for (size_t dau = 0; dau < cands.size(); ++dau) {
      int pdgId = std::abs(cands[dau]->pdgId());
      if (pdgId == 11 && channel==1)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kPrompt,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      if (pdgId == 11 && channel==2)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToElecDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else if (pdgId == 13 && channel==0)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kPrompt,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else if (pdgId == 13 && channel==3)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToMuDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else if (pdgId == 15)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(svFitStandalone::kTauToHadDecay,cands[dau]->pt(),cands[dau]->eta(),cands[dau]->phi(),cands[dau]->mass()));
      else
         return 0;
    }

    SVfitStandaloneAlgorithmLFV algo(measuredTauLeptons, measuredMET, convert_matrix(covMET), 2);
    algo.addLogM(false);
    edm::FileInPath inputFileName_visPtResolution("TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root");
    TH1::AddDirectory(false);  
    TFile* inputFile_visPtResolution = new TFile(inputFileName_visPtResolution.fullPath().data());
    //algo.shiftVisPt(true, inputFile_visPtResolution);
    algo.integrateMarkovChain();
    double mass = algo.getMass(); // mass uncertainty not implemented yet

    delete inputFile_visPtResolution;

    theCacheLFV[hash] = mass;
    return mass;

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

} // namespace ApplySVfitLFV
