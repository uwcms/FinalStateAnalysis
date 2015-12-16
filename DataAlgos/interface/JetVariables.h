
#ifndef JETVARIABLES_ZNC5J0I
#define JETVARIABLES_ZNC5J0I

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

class JetVariables {
  public:
    const reco::Candidate* leadJet;
    const reco::Candidate* subleadJet;
    double pt1;
    double pt2;
    double eta1;
    double eta2;
    double phi1;
    double phi2;
    double pumva1;
    double pumva2;
    double id1;
    double id2;
    double csv1;
    double csv2;
};

#endif /* end of include guard: JETVARIABLES_ZNC5J0I */
