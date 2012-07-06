#include <memory>
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#include <TFile.h>

#include "FinalStateAnalysis/DataAlgos/interface/VBFMVA.h"
#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"

namespace vbf {

  void VBFMVA::Initialize( std::string Weights ) {

    fIsInitialized = kTRUE;

    fTMVAReader = new TMVA::Reader( "!Color:!Silent:Error" );
    vbfvars.resize(8);
    fTMVAReader->AddVariable("mjj", &vbfvars[0]);
    fTMVAReader->AddVariable("dEta", &vbfvars[1]);
    fTMVAReader->AddVariable("dPhi", &vbfvars[2]);
    fTMVAReader->AddVariable("ditau_pt", &vbfvars[3]);
    fTMVAReader->AddVariable("dijet_pt", &vbfvars[4]);
    fTMVAReader->AddVariable("dPhi_hj", &vbfvars[5]);
    fTMVAReader->AddVariable("C1", &vbfvars[6]);
    fTMVAReader->AddVariable("C2", &vbfvars[7]);

    fTMVAReader->BookMVA("BDTG", Weights);

  }

  //--------------------------------------------------------------------------------------------------
  Double_t VBFMVA::calcVBFMVA(Double_t mjj,
      Double_t dEta,
      Double_t dPhi,
      Double_t diTau_pt,
      Double_t diJet_pt,
      Double_t dPhi_hj,
      Double_t C1,
      Double_t C2) {

    if (!fIsInitialized) {
      std::cout << "Error: VBFMVA not properly initialized.\n";
      return -9999;
    }

    //set all input variables
    vbfvars[0] = mjj;
    vbfvars[1] = dEta;
    vbfvars[2] = dPhi;
    vbfvars[3] = diTau_pt;
    vbfvars[4] = diJet_pt;
    vbfvars[5] = dPhi_hj;
    vbfvars[6] = C1;
    vbfvars[7] = C2;

    // Evaluate MVA
    float mva = fTMVAReader->EvaluateMVA( vbfvars, "BDTG");

    return mva;

  }

  void VBFMVA::applyMVA(VBFVariables& vars) {
    double mva = this->calcVBFMVA(
        vars.mass,
        vars.deta,
        vars.dphi,
        vars.ditaupt,
        vars.dijetpt,
        vars.dphihj,
        vars.c1,
        vars.c2);
    vars.mva = mva;
  }
}
