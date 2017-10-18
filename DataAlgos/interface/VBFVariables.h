/*
 * =====================================================================================
 *
 *       Filename:  VBFVariables.h
 *
 *    Description:  A simple container of VBF variables
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef VBFVARIABLES_ZNC5J0I
#define VBFVARIABLES_ZNC5J0I

namespace reco {
  class Candidate;
}

/*

1) mjj      -> the invariant mass of the two tag jets
2) dEta     -> the pseudorapidity difference between the two tag jets
3) dPhi     -> the phi difference between the two tag jets
4) ditau_pt -> the vector sum of the pT of the tau + electron/muon + MET
5) dijet_pt -> the vector sum of the pT of the two tag jets
6) dPhi_hj  -> the phi difference between the di-tau vector and the di-jet vector
8) C1       -> the pseudorapidity difference between the *visible* di-tau vector and the closest tag jet
9) C2       -> the *visible* pT of the di-tau

 */

class VBFVariables {
  public:
    const reco::Candidate* leadJet;
    const reco::Candidate* subleadJet;
    double mass;
    double deta;
    double dphi;
    double pt1;
    double pt2;
    double dijetpt;
    double ditaupt;
    double hrapidity;
    double dijetrapidity;
    double eta1;
    double eta2;

    double mass_JESDown;
    double deta_JESDown;
    double dphi_JESDown;
    double pt1_JESDown;
    double pt2_JESDown;
    double dijetpt_JESDown;
    double dijetrapidity_JESDown;
    double eta1_JESDown;
    double eta2_JESDown;
    unsigned int jets20_JESDown;
    unsigned int jets30_JESDown;

    double mass_JESUp;
    double deta_JESUp;
    double dphi_JESUp;
    double pt1_JESUp;
    double pt2_JESUp;
    double dijetpt_JESUp;
    double dijetrapidity_JESUp;
    double eta1_JESUp;
    double eta2_JESUp;
    unsigned int jets20_JESUp;
    unsigned int jets30_JESUp;

    double dphihj;
    double dphihj_nomet;
    double c1;
    double c2;
    double mva;
    unsigned int jets20;
    unsigned int jets30;
    unsigned int nJets; // Number of jets in event passing cut
};

#endif /* end of include guard: VBFVARIABLES_ZNC5J0I */
