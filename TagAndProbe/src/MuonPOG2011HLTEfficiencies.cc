// Taken from:
// https://twiki.cern.ch/twiki/pub/CMS/MuonHLT/efficiencyFunctions.C
// on https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT#DoubleMu_Efficiency

#include "FinalStateAnalysis/TagAndProbe/interface/MuonPOG2011HLTEfficiencies.h"

Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATA(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.683784;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.783309;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.797219;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.802663;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.802375;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.81108;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.775747;
    else if( eta2>=-0.2 && eta2<0) return 0.809198;
    else if( eta2>=0 && eta2<0.2) return 0.810635;
    else if( eta2>=0.2 && eta2<0.3) return 0.783068;
    else if( eta2>=0.3 && eta2<0.6) return 0.808557;
    else if( eta2>=0.6 && eta2<0.9) return 0.803173;
    else if( eta2>=0.9 && eta2<1.2) return 0.800397;
    else if( eta2>=1.2 && eta2<1.6) return 0.794997;
    else if( eta2>=1.6 && eta2<2.1) return 0.787449;
    else if( eta2>=2.1 && eta2<=2.4) return 0.742006;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.783309;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.897;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.912839;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.919061;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.918718;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.928674;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.888225;
    else if( eta2>=-0.2 && eta2<0) return 0.926524;
    else if( eta2>=0 && eta2<0.2) return 0.928164;
    else if( eta2>=0.2 && eta2<0.3) return 0.896602;
    else if( eta2>=0.3 && eta2<0.6) return 0.925783;
    else if( eta2>=0.6 && eta2<0.9) return 0.919631;
    else if( eta2>=0.9 && eta2<1.2) return 0.916467;
    else if( eta2>=1.2 && eta2<1.6) return 0.910305;
    else if( eta2>=1.6 && eta2<2.1) return 0.901755;
    else if( eta2>=2.1 && eta2<=2.4) return 0.849978;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.797219;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.912839;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.928934;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.935262;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.93491;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.945037;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.903878;
    else if( eta2>=-0.2 && eta2<0) return 0.942851;
    else if( eta2>=0 && eta2<0.2) return 0.944518;
    else if( eta2>=0.2 && eta2<0.3) return 0.912401;
    else if( eta2>=0.3 && eta2<0.6) return 0.942095;
    else if( eta2>=0.6 && eta2<0.9) return 0.935838;
    else if( eta2>=0.9 && eta2<1.2) return 0.932622;
    else if( eta2>=1.2 && eta2<1.6) return 0.926358;
    else if( eta2>=1.6 && eta2<2.1) return 0.917683;
    else if( eta2>=2.1 && eta2<=2.4) return 0.865065;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.802663;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.919061;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.935262;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.941632;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941278;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.951473;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.910034;
    else if( eta2>=-0.2 && eta2<0) return 0.949273;
    else if( eta2>=0 && eta2<0.2) return 0.950951;
    else if( eta2>=0.2 && eta2<0.3) return 0.918615;
    else if( eta2>=0.3 && eta2<0.6) return 0.948511;
    else if( eta2>=0.6 && eta2<0.9) return 0.942212;
    else if( eta2>=0.9 && eta2<1.2) return 0.938975;
    else if( eta2>=1.2 && eta2<1.6) return 0.932669;
    else if( eta2>=1.6 && eta2<2.1) return 0.923938;
    else if( eta2>=2.1 && eta2<=2.4) return 0.87097;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.802375;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.918718;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.93491;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.941278;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.940922;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.951114;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.909691;
    else if( eta2>=-0.2 && eta2<0) return 0.948914;
    else if( eta2>=0 && eta2<0.2) return 0.950591;
    else if( eta2>=0.2 && eta2<0.3) return 0.918268;
    else if( eta2>=0.3 && eta2<0.6) return 0.948152;
    else if( eta2>=0.6 && eta2<0.9) return 0.941856;
    else if( eta2>=0.9 && eta2<1.2) return 0.938621;
    else if( eta2>=1.2 && eta2<1.6) return 0.932318;
    else if( eta2>=1.6 && eta2<2.1) return 0.923594;
    else if( eta2>=2.1 && eta2<=2.4) return 0.870657;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.81108;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.928674;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.945037;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951473;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.951114;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.961415;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.919544;
    else if( eta2>=-0.2 && eta2<0) return 0.959192;
    else if( eta2>=0 && eta2<0.2) return 0.960887;
    else if( eta2>=0.2 && eta2<0.3) return 0.928214;
    else if( eta2>=0.3 && eta2<0.6) return 0.958422;
    else if( eta2>=0.6 && eta2<0.9) return 0.952058;
    else if( eta2>=0.9 && eta2<1.2) return 0.948788;
    else if( eta2>=1.2 && eta2<1.6) return 0.942418;
    else if( eta2>=1.6 && eta2<2.1) return 0.933603;
    else if( eta2>=2.1 && eta2<=2.4) return 0.880102;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.775747;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.888225;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.903878;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.910034;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.909691;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.919544;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.879496;
    else if( eta2>=-0.2 && eta2<0) return 0.917417;
    else if( eta2>=0 && eta2<0.2) return 0.919038;
    else if( eta2>=0.2 && eta2<0.3) return 0.887788;
    else if( eta2>=0.3 && eta2<0.6) return 0.916681;
    else if( eta2>=0.6 && eta2<0.9) return 0.910594;
    else if( eta2>=0.9 && eta2<1.2) return 0.907466;
    else if( eta2>=1.2 && eta2<1.6) return 0.901373;
    else if( eta2>=1.6 && eta2<2.1) return 0.89294;
    else if( eta2>=2.1 && eta2<=2.4) return 0.841763;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.809198;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.926524;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.942851;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.949273;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.948914;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.959192;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.917417;
    else if( eta2>=-0.2 && eta2<0) return 0.956974;
    else if( eta2>=0 && eta2<0.2) return 0.958665;
    else if( eta2>=0.2 && eta2<0.3) return 0.926067;
    else if( eta2>=0.3 && eta2<0.6) return 0.956205;
    else if( eta2>=0.6 && eta2<0.9) return 0.949856;
    else if( eta2>=0.9 && eta2<1.2) return 0.946593;
    else if( eta2>=1.2 && eta2<1.6) return 0.940237;
    else if( eta2>=1.6 && eta2<2.1) return 0.931441;
    else if( eta2>=2.1 && eta2<=2.4) return 0.87806;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.810635;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.928164;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.944518;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.950951;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950591;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.960887;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.919038;
    else if( eta2>=-0.2 && eta2<0) return 0.958665;
    else if( eta2>=0 && eta2<0.2) return 0.960359;
    else if( eta2>=0.2 && eta2<0.3) return 0.927704;
    else if( eta2>=0.3 && eta2<0.6) return 0.957895;
    else if( eta2>=0.6 && eta2<0.9) return 0.951535;
    else if( eta2>=0.9 && eta2<1.2) return 0.948266;
    else if( eta2>=1.2 && eta2<1.6) return 0.9419;
    else if( eta2>=1.6 && eta2<2.1) return 0.93309;
    else if( eta2>=2.1 && eta2<=2.4) return 0.879619;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.783068;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.896602;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.912401;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.918615;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.918268;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.928214;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.887788;
    else if( eta2>=-0.2 && eta2<0) return 0.926067;
    else if( eta2>=0 && eta2<0.2) return 0.927704;
    else if( eta2>=0.2 && eta2<0.3) return 0.896159;
    else if( eta2>=0.3 && eta2<0.6) return 0.925324;
    else if( eta2>=0.6 && eta2<0.9) return 0.919179;
    else if( eta2>=0.9 && eta2<1.2) return 0.916022;
    else if( eta2>=1.2 && eta2<1.6) return 0.909872;
    else if( eta2>=1.6 && eta2<2.1) return 0.901361;
    else if( eta2>=2.1 && eta2<=2.4) return 0.849706;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.808557;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.925783;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.942095;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.948511;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.948152;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.958422;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.916681;
    else if( eta2>=-0.2 && eta2<0) return 0.956205;
    else if( eta2>=0 && eta2<0.2) return 0.957895;
    else if( eta2>=0.2 && eta2<0.3) return 0.925324;
    else if( eta2>=0.3 && eta2<0.6) return 0.955438;
    else if( eta2>=0.6 && eta2<0.9) return 0.949094;
    else if( eta2>=0.9 && eta2<1.2) return 0.945834;
    else if( eta2>=1.2 && eta2<1.6) return 0.939484;
    else if( eta2>=1.6 && eta2<2.1) return 0.930697;
    else if( eta2>=2.1 && eta2<=2.4) return 0.877364;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.803173;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.919631;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.935838;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.942212;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941856;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.952058;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.910594;
    else if( eta2>=-0.2 && eta2<0) return 0.949856;
    else if( eta2>=0 && eta2<0.2) return 0.951535;
    else if( eta2>=0.2 && eta2<0.3) return 0.919179;
    else if( eta2>=0.3 && eta2<0.6) return 0.949094;
    else if( eta2>=0.6 && eta2<0.9) return 0.942791;
    else if( eta2>=0.9 && eta2<1.2) return 0.939553;
    else if( eta2>=1.2 && eta2<1.6) return 0.933244;
    else if( eta2>=1.6 && eta2<2.1) return 0.924512;
    else if( eta2>=2.1 && eta2<=2.4) return 0.871523;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.800397;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.916467;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.932622;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.938975;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.938621;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.948788;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.907466;
    else if( eta2>=-0.2 && eta2<0) return 0.946593;
    else if( eta2>=0 && eta2<0.2) return 0.948266;
    else if( eta2>=0.2 && eta2<0.3) return 0.916022;
    else if( eta2>=0.3 && eta2<0.6) return 0.945834;
    else if( eta2>=0.6 && eta2<0.9) return 0.939553;
    else if( eta2>=0.9 && eta2<1.2) return 0.936324;
    else if( eta2>=1.2 && eta2<1.6) return 0.930036;
    else if( eta2>=1.6 && eta2<2.1) return 0.92133;
    else if( eta2>=2.1 && eta2<=2.4) return 0.868512;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.794997;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.910305;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.926358;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.932669;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.932318;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.942418;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.901373;
    else if( eta2>=-0.2 && eta2<0) return 0.940237;
    else if( eta2>=0 && eta2<0.2) return 0.9419;
    else if( eta2>=0.2 && eta2<0.3) return 0.909872;
    else if( eta2>=0.3 && eta2<0.6) return 0.939484;
    else if( eta2>=0.6 && eta2<0.9) return 0.933244;
    else if( eta2>=0.9 && eta2<1.2) return 0.930036;
    else if( eta2>=1.2 && eta2<1.6) return 0.923789;
    else if( eta2>=1.6 && eta2<2.1) return 0.915135;
    else if( eta2>=2.1 && eta2<=2.4) return 0.862654;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.787449;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.901755;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.917683;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.923938;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.923594;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.933603;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.89294;
    else if( eta2>=-0.2 && eta2<0) return 0.931441;
    else if( eta2>=0 && eta2<0.2) return 0.93309;
    else if( eta2>=0.2 && eta2<0.3) return 0.901361;
    else if( eta2>=0.3 && eta2<0.6) return 0.930697;
    else if( eta2>=0.6 && eta2<0.9) return 0.924512;
    else if( eta2>=0.9 && eta2<1.2) return 0.92133;
    else if( eta2>=1.2 && eta2<1.6) return 0.915135;
    else if( eta2>=1.6 && eta2<2.1) return 0.906535;
    else if( eta2>=2.1 && eta2<=2.4) return 0.854471;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.742006;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.849978;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.865065;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.87097;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.870657;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.880102;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.841763;
    else if( eta2>=-0.2 && eta2<0) return 0.87806;
    else if( eta2>=0 && eta2<0.2) return 0.879619;
    else if( eta2>=0.2 && eta2<0.3) return 0.849706;
    else if( eta2>=0.3 && eta2<0.6) return 0.877364;
    else if( eta2>=0.6 && eta2<0.9) return 0.871523;
    else if( eta2>=0.9 && eta2<1.2) return 0.868512;
    else if( eta2>=1.2 && eta2<1.6) return 0.862654;
    else if( eta2>=1.6 && eta2<2.1) return 0.854471;
    else if( eta2>=2.1 && eta2<=2.4) return 0.805183;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_MC(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.846754;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.885084;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.897003;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.900219;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.899382;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.909829;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.887239;
    else if( eta2>=-0.2 && eta2<0) return 0.907034;
    else if( eta2>=0 && eta2<0.2) return 0.907328;
    else if( eta2>=0.2 && eta2<0.3) return 0.886891;
    else if( eta2>=0.3 && eta2<0.6) return 0.9095;
    else if( eta2>=0.6 && eta2<0.9) return 0.895609;
    else if( eta2>=0.9 && eta2<1.2) return 0.899687;
    else if( eta2>=1.2 && eta2<1.6) return 0.895219;
    else if( eta2>=1.6 && eta2<2.1) return 0.880775;
    else if( eta2>=2.1 && eta2<=2.4) return 0.839747;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.885084;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.924877;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.937255;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.940608;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.939722;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.950636;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.927034;
    else if( eta2>=-0.2 && eta2<0) return 0.947716;
    else if( eta2>=0 && eta2<0.2) return 0.948023;
    else if( eta2>=0.2 && eta2<0.3) return 0.926671;
    else if( eta2>=0.3 && eta2<0.6) return 0.950294;
    else if( eta2>=0.6 && eta2<0.9) return 0.935782;
    else if( eta2>=0.9 && eta2<1.2) return 0.940055;
    else if( eta2>=1.2 && eta2<1.6) return 0.935392;
    else if( eta2>=1.6 && eta2<2.1) return 0.920386;
    else if( eta2>=2.1 && eta2<=2.4) return 0.877763;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.897003;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.937255;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.949777;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.953173;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.952272;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.963331;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.939414;
    else if( eta2>=-0.2 && eta2<0) return 0.960372;
    else if( eta2>=0 && eta2<0.2) return 0.960683;
    else if( eta2>=0.2 && eta2<0.3) return 0.939046;
    else if( eta2>=0.3 && eta2<0.6) return 0.962984;
    else if( eta2>=0.6 && eta2<0.9) return 0.948279;
    else if( eta2>=0.9 && eta2<1.2) return 0.952613;
    else if( eta2>=1.2 && eta2<1.6) return 0.947889;
    else if( eta2>=1.6 && eta2<2.1) return 0.932707;
    else if( eta2>=2.1 && eta2<=2.4) return 0.889585;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.900219;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.940608;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.953173;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.956581;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.955676;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.966775;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.942773;
    else if( eta2>=-0.2 && eta2<0) return 0.963805;
    else if( eta2>=0 && eta2<0.2) return 0.964117;
    else if( eta2>=0.2 && eta2<0.3) return 0.942404;
    else if( eta2>=0.3 && eta2<0.6) return 0.966427;
    else if( eta2>=0.6 && eta2<0.9) return 0.951669;
    else if( eta2>=0.9 && eta2<1.2) return 0.956019;
    else if( eta2>=1.2 && eta2<1.6) return 0.951278;
    else if( eta2>=1.6 && eta2<2.1) return 0.936045;
    else if( eta2>=2.1 && eta2<=2.4) return 0.892774;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.899382;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.939722;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.952272;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.955676;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.954772;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.96586;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.941881;
    else if( eta2>=-0.2 && eta2<0) return 0.962893;
    else if( eta2>=0 && eta2<0.2) return 0.963205;
    else if( eta2>=0.2 && eta2<0.3) return 0.941512;
    else if( eta2>=0.3 && eta2<0.6) return 0.965513;
    else if( eta2>=0.6 && eta2<0.9) return 0.950769;
    else if( eta2>=0.9 && eta2<1.2) return 0.955115;
    else if( eta2>=1.2 && eta2<1.6) return 0.950379;
    else if( eta2>=1.6 && eta2<2.1) return 0.935163;
    else if( eta2>=2.1 && eta2<=2.4) return 0.891944;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.909829;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.950636;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.963331;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.966775;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.96586;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.977077;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.952819;
    else if( eta2>=-0.2 && eta2<0) return 0.974076;
    else if( eta2>=0 && eta2<0.2) return 0.974391;
    else if( eta2>=0.2 && eta2<0.3) return 0.952446;
    else if( eta2>=0.3 && eta2<0.6) return 0.976725;
    else if( eta2>=0.6 && eta2<0.9) return 0.96181;
    else if( eta2>=0.9 && eta2<1.2) return 0.966207;
    else if( eta2>=1.2 && eta2<1.6) return 0.961416;
    else if( eta2>=1.6 && eta2<2.1) return 0.946024;
    else if( eta2>=2.1 && eta2<=2.4) return 0.902305;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.887239;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.927034;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.939414;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.942773;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941881;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.952819;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.929164;
    else if( eta2>=-0.2 && eta2<0) return 0.949892;
    else if( eta2>=0 && eta2<0.2) return 0.9502;
    else if( eta2>=0.2 && eta2<0.3) return 0.9288;
    else if( eta2>=0.3 && eta2<0.6) return 0.952476;
    else if( eta2>=0.6 && eta2<0.9) return 0.937932;
    else if( eta2>=0.9 && eta2<1.2) return 0.942219;
    else if( eta2>=1.2 && eta2<1.6) return 0.937547;
    else if( eta2>=1.6 && eta2<2.1) return 0.922537;
    else if( eta2>=2.1 && eta2<=2.4) return 0.879902;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.907034;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.947716;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.960372;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.963805;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.962893;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.974076;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.949892;
    else if( eta2>=-0.2 && eta2<0) return 0.971084;
    else if( eta2>=0 && eta2<0.2) return 0.971398;
    else if( eta2>=0.2 && eta2<0.3) return 0.94952;
    else if( eta2>=0.3 && eta2<0.6) return 0.973725;
    else if( eta2>=0.6 && eta2<0.9) return 0.958856;
    else if( eta2>=0.9 && eta2<1.2) return 0.963239;
    else if( eta2>=1.2 && eta2<1.6) return 0.958463;
    else if( eta2>=1.6 && eta2<2.1) return 0.943118;
    else if( eta2>=2.1 && eta2<=2.4) return 0.899534;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.907328;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.948023;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.960683;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.964117;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.963205;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.974391;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.9502;
    else if( eta2>=-0.2 && eta2<0) return 0.971398;
    else if( eta2>=0 && eta2<0.2) return 0.971713;
    else if( eta2>=0.2 && eta2<0.3) return 0.949828;
    else if( eta2>=0.3 && eta2<0.6) return 0.974041;
    else if( eta2>=0.6 && eta2<0.9) return 0.959166;
    else if( eta2>=0.9 && eta2<1.2) return 0.963551;
    else if( eta2>=1.2 && eta2<1.6) return 0.958773;
    else if( eta2>=1.6 && eta2<2.1) return 0.943424;
    else if( eta2>=2.1 && eta2<=2.4) return 0.899825;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.886891;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.926671;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.939046;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.942404;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941512;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.952446;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.9288;
    else if( eta2>=-0.2 && eta2<0) return 0.94952;
    else if( eta2>=0 && eta2<0.2) return 0.949828;
    else if( eta2>=0.2 && eta2<0.3) return 0.928436;
    else if( eta2>=0.3 && eta2<0.6) return 0.952103;
    else if( eta2>=0.6 && eta2<0.9) return 0.937564;
    else if( eta2>=0.9 && eta2<1.2) return 0.94185;
    else if( eta2>=1.2 && eta2<1.6) return 0.93718;
    else if( eta2>=1.6 && eta2<2.1) return 0.922175;
    else if( eta2>=2.1 && eta2<=2.4) return 0.879557;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.9095;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.950294;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.962984;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.966427;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.965513;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.976725;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.952476;
    else if( eta2>=-0.2 && eta2<0) return 0.973725;
    else if( eta2>=0 && eta2<0.2) return 0.974041;
    else if( eta2>=0.2 && eta2<0.3) return 0.952103;
    else if( eta2>=0.3 && eta2<0.6) return 0.976374;
    else if( eta2>=0.6 && eta2<0.9) return 0.961464;
    else if( eta2>=0.9 && eta2<1.2) return 0.965859;
    else if( eta2>=1.2 && eta2<1.6) return 0.96107;
    else if( eta2>=1.6 && eta2<2.1) return 0.945683;
    else if( eta2>=2.1 && eta2<=2.4) return 0.901979;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.895609;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.935782;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.948279;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951669;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950769;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.96181;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.937932;
    else if( eta2>=-0.2 && eta2<0) return 0.958856;
    else if( eta2>=0 && eta2<0.2) return 0.959166;
    else if( eta2>=0.2 && eta2<0.3) return 0.937564;
    else if( eta2>=0.3 && eta2<0.6) return 0.961464;
    else if( eta2>=0.6 && eta2<0.9) return 0.946782;
    else if( eta2>=0.9 && eta2<1.2) return 0.95111;
    else if( eta2>=1.2 && eta2<1.6) return 0.946394;
    else if( eta2>=1.6 && eta2<2.1) return 0.931242;
    else if( eta2>=2.1 && eta2<=2.4) return 0.888203;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.899687;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.940055;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.952613;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.956019;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.955115;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.966207;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.942219;
    else if( eta2>=-0.2 && eta2<0) return 0.963239;
    else if( eta2>=0 && eta2<0.2) return 0.963551;
    else if( eta2>=0.2 && eta2<0.3) return 0.94185;
    else if( eta2>=0.3 && eta2<0.6) return 0.965859;
    else if( eta2>=0.6 && eta2<0.9) return 0.95111;
    else if( eta2>=0.9 && eta2<1.2) return 0.955457;
    else if( eta2>=1.2 && eta2<1.6) return 0.950719;
    else if( eta2>=1.6 && eta2<2.1) return 0.935493;
    else if( eta2>=2.1 && eta2<=2.4) return 0.892246;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.895219;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.935392;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.947889;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951278;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950379;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.961416;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.937547;
    else if( eta2>=-0.2 && eta2<0) return 0.958463;
    else if( eta2>=0 && eta2<0.2) return 0.958773;
    else if( eta2>=0.2 && eta2<0.3) return 0.93718;
    else if( eta2>=0.3 && eta2<0.6) return 0.96107;
    else if( eta2>=0.6 && eta2<0.9) return 0.946394;
    else if( eta2>=0.9 && eta2<1.2) return 0.950719;
    else if( eta2>=1.2 && eta2<1.6) return 0.946005;
    else if( eta2>=1.6 && eta2<2.1) return 0.930853;
    else if( eta2>=2.1 && eta2<=2.4) return 0.887816;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.880775;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.920386;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.932707;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.936045;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.935163;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.946024;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.922537;
    else if( eta2>=-0.2 && eta2<0) return 0.943118;
    else if( eta2>=0 && eta2<0.2) return 0.943424;
    else if( eta2>=0.2 && eta2<0.3) return 0.922175;
    else if( eta2>=0.3 && eta2<0.6) return 0.945683;
    else if( eta2>=0.6 && eta2<0.9) return 0.931242;
    else if( eta2>=0.9 && eta2<1.2) return 0.935493;
    else if( eta2>=1.2 && eta2<1.6) return 0.930853;
    else if( eta2>=1.6 && eta2<2.1) return 0.915916;
    else if( eta2>=2.1 && eta2<=2.4) return 0.87349;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.839747;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.877763;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.889585;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.892774;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.891944;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.902305;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.879902;
    else if( eta2>=-0.2 && eta2<0) return 0.899534;
    else if( eta2>=0 && eta2<0.2) return 0.899825;
    else if( eta2>=0.2 && eta2<0.3) return 0.879557;
    else if( eta2>=0.3 && eta2<0.6) return 0.901979;
    else if( eta2>=0.6 && eta2<0.9) return 0.888203;
    else if( eta2>=0.9 && eta2<1.2) return 0.892246;
    else if( eta2>=1.2 && eta2<1.6) return 0.887816;
    else if( eta2>=1.6 && eta2<2.1) return 0.87349;
    else if( eta2>=2.1 && eta2<=2.4) return 0.832798;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


Double_t Eff_HLT_Mu13_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.807536;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.885011;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.888759;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.89163;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.892141;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.891464;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.874339;
    else if( eta2>=-0.2 && eta2<0) return 0.892135;
    else if( eta2>=0 && eta2<0.2) return 0.893432;
    else if( eta2>=0.2 && eta2<0.3) return 0.882935;
    else if( eta2>=0.3 && eta2<0.6) return 0.889012;
    else if( eta2>=0.6 && eta2<0.9) return 0.896789;
    else if( eta2>=0.9 && eta2<1.2) return 0.88964;
    else if( eta2>=1.2 && eta2<1.6) return 0.888047;
    else if( eta2>=1.6 && eta2<2.1) return 0.894041;
    else if( eta2>=2.1 && eta2<=2.4) return 0.883607;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.885011;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.969858;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.97395;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.977092;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.977649;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.976897;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.958137;
    else if( eta2>=-0.2 && eta2<0) return 0.977639;
    else if( eta2>=0 && eta2<0.2) return 0.979052;
    else if( eta2>=0.2 && eta2<0.3) return 0.967551;
    else if( eta2>=0.3 && eta2<0.6) return 0.974207;
    else if( eta2>=0.6 && eta2<0.9) return 0.982741;
    else if( eta2>=0.9 && eta2<1.2) return 0.974908;
    else if( eta2>=1.2 && eta2<1.6) return 0.97318;
    else if( eta2>=1.6 && eta2<2.1) return 0.979757;
    else if( eta2>=2.1 && eta2<=2.4) return 0.968346;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.888759;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.97395;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.978055;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.981209;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.981768;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98101;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.962172;
    else if( eta2>=-0.2 && eta2<0) return 0.981756;
    else if( eta2>=0 && eta2<0.2) return 0.983173;
    else if( eta2>=0.2 && eta2<0.3) return 0.971625;
    else if( eta2>=0.3 && eta2<0.6) return 0.978308;
    else if( eta2>=0.6 && eta2<0.9) return 0.98688;
    else if( eta2>=0.9 && eta2<1.2) return 0.979015;
    else if( eta2>=1.2 && eta2<1.6) return 0.977285;
    else if( eta2>=1.6 && eta2<2.1) return 0.983892;
    else if( eta2>=2.1 && eta2<=2.4) return 0.972436;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.89163;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.977092;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.981209;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.984373;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.984933;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.984173;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965274;
    else if( eta2>=-0.2 && eta2<0) return 0.984921;
    else if( eta2>=0 && eta2<0.2) return 0.986343;
    else if( eta2>=0.2 && eta2<0.3) return 0.974758;
    else if( eta2>=0.3 && eta2<0.6) return 0.981462;
    else if( eta2>=0.6 && eta2<0.9) return 0.990062;
    else if( eta2>=0.9 && eta2<1.2) return 0.982172;
    else if( eta2>=1.2 && eta2<1.6) return 0.980437;
    else if( eta2>=1.6 && eta2<2.1) return 0.987066;
    else if( eta2>=2.1 && eta2<=2.4) return 0.975577;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.892141;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.977649;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.981768;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.984933;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.985494;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.984732;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965824;
    else if( eta2>=-0.2 && eta2<0) return 0.985482;
    else if( eta2>=0 && eta2<0.2) return 0.986904;
    else if( eta2>=0.2 && eta2<0.3) return 0.975312;
    else if( eta2>=0.3 && eta2<0.6) return 0.98202;
    else if( eta2>=0.6 && eta2<0.9) return 0.990626;
    else if( eta2>=0.9 && eta2<1.2) return 0.982731;
    else if( eta2>=1.2 && eta2<1.6) return 0.980996;
    else if( eta2>=1.6 && eta2<2.1) return 0.987629;
    else if( eta2>=2.1 && eta2<=2.4) return 0.976134;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.891464;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.976897;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.98101;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.984173;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.984732;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.983971;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965077;
    else if( eta2>=-0.2 && eta2<0) return 0.98472;
    else if( eta2>=0 && eta2<0.2) return 0.986141;
    else if( eta2>=0.2 && eta2<0.3) return 0.974558;
    else if( eta2>=0.3 && eta2<0.6) return 0.98126;
    else if( eta2>=0.6 && eta2<0.9) return 0.98986;
    else if( eta2>=0.9 && eta2<1.2) return 0.981972;
    else if( eta2>=1.2 && eta2<1.6) return 0.980239;
    else if( eta2>=1.6 && eta2<2.1) return 0.98687;
    else if( eta2>=2.1 && eta2<=2.4) return 0.975393;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.874339;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.958137;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.962172;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.965274;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.965824;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.965077;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.946546;
    else if( eta2>=-0.2 && eta2<0) return 0.965812;
    else if( eta2>=0 && eta2<0.2) return 0.967205;
    else if( eta2>=0.2 && eta2<0.3) return 0.955845;
    else if( eta2>=0.3 && eta2<0.6) return 0.962418;
    else if( eta2>=0.6 && eta2<0.9) return 0.970853;
    else if( eta2>=0.9 && eta2<1.2) return 0.963116;
    else if( eta2>=1.2 && eta2<1.6) return 0.961416;
    else if( eta2>=1.6 && eta2<2.1) return 0.967918;
    else if( eta2>=2.1 && eta2<=2.4) return 0.956656;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.892135;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.977639;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.981756;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.984921;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.985482;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98472;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965812;
    else if( eta2>=-0.2 && eta2<0) return 0.98547;
    else if( eta2>=0 && eta2<0.2) return 0.986892;
    else if( eta2>=0.2 && eta2<0.3) return 0.9753;
    else if( eta2>=0.3 && eta2<0.6) return 0.982007;
    else if( eta2>=0.6 && eta2<0.9) return 0.990614;
    else if( eta2>=0.9 && eta2<1.2) return 0.982719;
    else if( eta2>=1.2 && eta2<1.6) return 0.980984;
    else if( eta2>=1.6 && eta2<2.1) return 0.987619;
    else if( eta2>=2.1 && eta2<=2.4) return 0.976128;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.893432;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.979052;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.983173;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.986343;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.986904;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.986141;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.967205;
    else if( eta2>=-0.2 && eta2<0) return 0.986892;
    else if( eta2>=0 && eta2<0.2) return 0.988315;
    else if( eta2>=0.2 && eta2<0.3) return 0.976707;
    else if( eta2>=0.3 && eta2<0.6) return 0.983424;
    else if( eta2>=0.6 && eta2<0.9) return 0.992043;
    else if( eta2>=0.9 && eta2<1.2) return 0.984137;
    else if( eta2>=1.2 && eta2<1.6) return 0.982401;
    else if( eta2>=1.6 && eta2<2.1) return 0.989047;
    else if( eta2>=2.1 && eta2<=2.4) return 0.977545;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.882935;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.967551;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.971625;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.974758;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.975312;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.974558;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.955845;
    else if( eta2>=-0.2 && eta2<0) return 0.9753;
    else if( eta2>=0 && eta2<0.2) return 0.976707;
    else if( eta2>=0.2 && eta2<0.3) return 0.965235;
    else if( eta2>=0.3 && eta2<0.6) return 0.971873;
    else if( eta2>=0.6 && eta2<0.9) return 0.980391;
    else if( eta2>=0.9 && eta2<1.2) return 0.972578;
    else if( eta2>=1.2 && eta2<1.6) return 0.970862;
    else if( eta2>=1.6 && eta2<2.1) return 0.977429;
    else if( eta2>=2.1 && eta2<=2.4) return 0.966061;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.889012;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.974207;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.978308;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.981462;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.98202;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98126;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.962418;
    else if( eta2>=-0.2 && eta2<0) return 0.982007;
    else if( eta2>=0 && eta2<0.2) return 0.983424;
    else if( eta2>=0.2 && eta2<0.3) return 0.971873;
    else if( eta2>=0.3 && eta2<0.6) return 0.978557;
    else if( eta2>=0.6 && eta2<0.9) return 0.987134;
    else if( eta2>=0.9 && eta2<1.2) return 0.979267;
    else if( eta2>=1.2 && eta2<1.6) return 0.977539;
    else if( eta2>=1.6 && eta2<2.1) return 0.984153;
    else if( eta2>=2.1 && eta2<=2.4) return 0.97271;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.896789;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.982741;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.98688;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.990062;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.990626;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98986;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.970853;
    else if( eta2>=-0.2 && eta2<0) return 0.990614;
    else if( eta2>=0 && eta2<0.2) return 0.992043;
    else if( eta2>=0.2 && eta2<0.3) return 0.980391;
    else if( eta2>=0.3 && eta2<0.6) return 0.987134;
    else if( eta2>=0.6 && eta2<0.9) return 0.995785;
    else if( eta2>=0.9 && eta2<1.2) return 0.987849;
    else if( eta2>=1.2 && eta2<1.6) return 0.986105;
    else if( eta2>=1.6 && eta2<2.1) return 0.992773;
    else if( eta2>=2.1 && eta2<=2.4) return 0.98122;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.88964;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.974908;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.979015;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.982172;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.982731;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.981972;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.963116;
    else if( eta2>=-0.2 && eta2<0) return 0.982719;
    else if( eta2>=0 && eta2<0.2) return 0.984137;
    else if( eta2>=0.2 && eta2<0.3) return 0.972578;
    else if( eta2>=0.3 && eta2<0.6) return 0.979267;
    else if( eta2>=0.6 && eta2<0.9) return 0.987849;
    else if( eta2>=0.9 && eta2<1.2) return 0.979976;
    else if( eta2>=1.2 && eta2<1.6) return 0.978245;
    else if( eta2>=1.6 && eta2<2.1) return 0.98486;
    else if( eta2>=2.1 && eta2<=2.4) return 0.973399;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.888047;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.97318;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.977285;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.980437;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.980996;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.980239;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.961416;
    else if( eta2>=-0.2 && eta2<0) return 0.980984;
    else if( eta2>=0 && eta2<0.2) return 0.982401;
    else if( eta2>=0.2 && eta2<0.3) return 0.970862;
    else if( eta2>=0.3 && eta2<0.6) return 0.977539;
    else if( eta2>=0.6 && eta2<0.9) return 0.986105;
    else if( eta2>=0.9 && eta2<1.2) return 0.978245;
    else if( eta2>=1.2 && eta2<1.6) return 0.976515;
    else if( eta2>=1.6 && eta2<2.1) return 0.983114;
    else if( eta2>=2.1 && eta2<=2.4) return 0.971658;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.894041;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.979757;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.983892;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.987066;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.987629;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98687;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.967918;
    else if( eta2>=-0.2 && eta2<0) return 0.987619;
    else if( eta2>=0 && eta2<0.2) return 0.989047;
    else if( eta2>=0.2 && eta2<0.3) return 0.977429;
    else if( eta2>=0.3 && eta2<0.6) return 0.984153;
    else if( eta2>=0.6 && eta2<0.9) return 0.992773;
    else if( eta2>=0.9 && eta2<1.2) return 0.98486;
    else if( eta2>=1.2 && eta2<1.6) return 0.983114;
    else if( eta2>=1.6 && eta2<2.1) return 0.989757;
    else if( eta2>=2.1 && eta2<=2.4) return 0.978227;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.883607;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.968346;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.972436;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.975577;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.976134;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.975393;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.956656;
    else if( eta2>=-0.2 && eta2<0) return 0.976128;
    else if( eta2>=0 && eta2<0.2) return 0.977545;
    else if( eta2>=0.2 && eta2<0.3) return 0.966061;
    else if( eta2>=0.3 && eta2<0.6) return 0.97271;
    else if( eta2>=0.6 && eta2<0.9) return 0.98122;
    else if( eta2>=0.9 && eta2<1.2) return 0.973399;
    else if( eta2>=1.2 && eta2<1.6) return 0.971658;
    else if( eta2>=1.6 && eta2<2.1) return 0.978227;
    else if( eta2>=2.1 && eta2<=2.4) return 0.966841;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATA(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.814586;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.854611;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.86971;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.875898;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.875702;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.8851;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.846657;
    else if( eta2>=-0.2 && eta2<0) return 0.883122;
    else if( eta2>=0 && eta2<0.2) return 0.884678;
    else if( eta2>=0.2 && eta2<0.3) return 0.854316;
    else if( eta2>=0.3 && eta2<0.6) return 0.882569;
    else if( eta2>=0.6 && eta2<0.9) return 0.876532;
    else if( eta2>=0.9 && eta2<1.2) return 0.873346;
    else if( eta2>=1.2 && eta2<1.6) return 0.867453;
    else if( eta2>=1.6 && eta2<2.1) return 0.859233;
    else if( eta2>=2.1 && eta2<=2.4) return 0.812599;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.854611;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.896249;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.912003;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.918465;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.918238;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.928077;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.887775;
    else if( eta2>=-0.2 && eta2<0) return 0.926008;
    else if( eta2>=0 && eta2<0.2) return 0.927634;
    else if( eta2>=0.2 && eta2<0.3) return 0.895801;
    else if( eta2>=0.3 && eta2<0.6) return 0.925424;
    else if( eta2>=0.6 && eta2<0.9) return 0.919108;
    else if( eta2>=0.9 && eta2<1.2) return 0.915799;
    else if( eta2>=1.2 && eta2<1.6) return 0.909644;
    else if( eta2>=1.6 && eta2<2.1) return 0.901108;
    else if( eta2>=2.1 && eta2<=2.4) return 0.8525;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.86971;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.912003;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.928013;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.934583;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.934348;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.944355;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.903349;
    else if( eta2>=-0.2 && eta2<0) return 0.942251;
    else if( eta2>=0 && eta2<0.2) return 0.943905;
    else if( eta2>=0.2 && eta2<0.3) return 0.911514;
    else if( eta2>=0.3 && eta2<0.6) return 0.941656;
    else if( eta2>=0.6 && eta2<0.9) return 0.935232;
    else if( eta2>=0.9 && eta2<1.2) return 0.931873;
    else if( eta2>=1.2 && eta2<1.6) return 0.925616;
    else if( eta2>=1.6 && eta2<2.1) return 0.916949;
    else if( eta2>=2.1 && eta2<=2.4) return 0.867556;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.875898;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.918465;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.934583;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.941198;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.940959;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.951036;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.90974;
    else if( eta2>=-0.2 && eta2<0) return 0.948918;
    else if( eta2>=0 && eta2<0.2) return 0.950582;
    else if( eta2>=0.2 && eta2<0.3) return 0.917963;
    else if( eta2>=0.3 && eta2<0.6) return 0.948318;
    else if( eta2>=0.6 && eta2<0.9) return 0.941849;
    else if( eta2>=0.9 && eta2<1.2) return 0.938469;
    else if( eta2>=1.2 && eta2<1.6) return 0.932169;
    else if( eta2>=1.6 && eta2<2.1) return 0.923447;
    else if( eta2>=2.1 && eta2<=2.4) return 0.873727;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.875702;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.918238;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.934348;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.940959;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.940719;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.950792;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.909507;
    else if( eta2>=-0.2 && eta2<0) return 0.948675;
    else if( eta2>=0 && eta2<0.2) return 0.950339;
    else if( eta2>=0.2 && eta2<0.3) return 0.917728;
    else if( eta2>=0.3 && eta2<0.6) return 0.948075;
    else if( eta2>=0.6 && eta2<0.9) return 0.941609;
    else if( eta2>=0.9 && eta2<1.2) return 0.938231;
    else if( eta2>=1.2 && eta2<1.6) return 0.931935;
    else if( eta2>=1.6 && eta2<2.1) return 0.92322;
    else if( eta2>=2.1 && eta2<=2.4) return 0.873529;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.8851;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.928077;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.944355;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951036;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950792;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.960973;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.919246;
    else if( eta2>=-0.2 && eta2<0) return 0.958833;
    else if( eta2>=0 && eta2<0.2) return 0.960515;
    else if( eta2>=0.2 && eta2<0.3) return 0.927555;
    else if( eta2>=0.3 && eta2<0.6) return 0.958226;
    else if( eta2>=0.6 && eta2<0.9) return 0.951692;
    else if( eta2>=0.9 && eta2<1.2) return 0.94828;
    else if( eta2>=1.2 && eta2<1.6) return 0.941917;
    else if( eta2>=1.6 && eta2<2.1) return 0.933112;
    else if( eta2>=2.1 && eta2<=2.4) return 0.882904;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.846657;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.887775;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.903349;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.90974;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.909507;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.919246;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.879331;
    else if( eta2>=-0.2 && eta2<0) return 0.917199;
    else if( eta2>=0 && eta2<0.2) return 0.918808;
    else if( eta2>=0.2 && eta2<0.3) return 0.887279;
    else if( eta2>=0.3 && eta2<0.6) return 0.916619;
    else if( eta2>=0.6 && eta2<0.9) return 0.910368;
    else if( eta2>=0.9 && eta2<1.2) return 0.907103;
    else if( eta2>=1.2 && eta2<1.6) return 0.901016;
    else if( eta2>=1.6 && eta2<2.1) return 0.892592;
    else if( eta2>=2.1 && eta2<=2.4) return 0.844556;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.883122;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.926008;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.942251;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.948918;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.948675;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.958833;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.917199;
    else if( eta2>=-0.2 && eta2<0) return 0.956698;
    else if( eta2>=0 && eta2<0.2) return 0.958376;
    else if( eta2>=0.2 && eta2<0.3) return 0.925489;
    else if( eta2>=0.3 && eta2<0.6) return 0.956093;
    else if( eta2>=0.6 && eta2<0.9) return 0.949573;
    else if( eta2>=0.9 && eta2<1.2) return 0.946167;
    else if( eta2>=1.2 && eta2<1.6) return 0.939818;
    else if( eta2>=1.6 && eta2<2.1) return 0.931032;
    else if( eta2>=2.1 && eta2<=2.4) return 0.880931;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.884678;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.927634;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.943905;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.950582;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950339;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.960515;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.918808;
    else if( eta2>=-0.2 && eta2<0) return 0.958376;
    else if( eta2>=0 && eta2<0.2) return 0.960057;
    else if( eta2>=0.2 && eta2<0.3) return 0.927112;
    else if( eta2>=0.3 && eta2<0.6) return 0.957769;
    else if( eta2>=0.6 && eta2<0.9) return 0.951238;
    else if( eta2>=0.9 && eta2<1.2) return 0.947827;
    else if( eta2>=1.2 && eta2<1.6) return 0.941468;
    else if( eta2>=1.6 && eta2<2.1) return 0.932667;
    else if( eta2>=2.1 && eta2<=2.4) return 0.882482;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.854316;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.895801;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.911514;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.917963;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.917728;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.927555;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.887279;
    else if( eta2>=-0.2 && eta2<0) return 0.925489;
    else if( eta2>=0 && eta2<0.2) return 0.927112;
    else if( eta2>=0.2 && eta2<0.3) return 0.895298;
    else if( eta2>=0.3 && eta2<0.6) return 0.924903;
    else if( eta2>=0.6 && eta2<0.9) return 0.918596;
    else if( eta2>=0.9 && eta2<1.2) return 0.915302;
    else if( eta2>=1.2 && eta2<1.6) return 0.90916;
    else if( eta2>=1.6 && eta2<2.1) return 0.900661;
    else if( eta2>=2.1 && eta2<=2.4) return 0.852196;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.882569;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.925424;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.941656;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.948318;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.948075;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.958226;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.916619;
    else if( eta2>=-0.2 && eta2<0) return 0.956093;
    else if( eta2>=0 && eta2<0.2) return 0.957769;
    else if( eta2>=0.2 && eta2<0.3) return 0.924903;
    else if( eta2>=0.3 && eta2<0.6) return 0.955488;
    else if( eta2>=0.6 && eta2<0.9) return 0.948972;
    else if( eta2>=0.9 && eta2<1.2) return 0.945569;
    else if( eta2>=1.2 && eta2<1.6) return 0.939225;
    else if( eta2>=1.6 && eta2<2.1) return 0.930445;
    else if( eta2>=2.1 && eta2<=2.4) return 0.880379;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.876532;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.919108;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.935232;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.941849;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941609;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.951692;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.910368;
    else if( eta2>=-0.2 && eta2<0) return 0.949573;
    else if( eta2>=0 && eta2<0.2) return 0.951238;
    else if( eta2>=0.2 && eta2<0.3) return 0.918596;
    else if( eta2>=0.3 && eta2<0.6) return 0.948972;
    else if( eta2>=0.6 && eta2<0.9) return 0.9425;
    else if( eta2>=0.9 && eta2<1.2) return 0.939119;
    else if( eta2>=1.2 && eta2<1.6) return 0.932817;
    else if( eta2>=1.6 && eta2<2.1) return 0.924094;
    else if( eta2>=2.1 && eta2<=2.4) return 0.874358;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.873346;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.915799;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.931873;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.938469;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.938231;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.94828;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.907103;
    else if( eta2>=-0.2 && eta2<0) return 0.946167;
    else if( eta2>=0 && eta2<0.2) return 0.947827;
    else if( eta2>=0.2 && eta2<0.3) return 0.915302;
    else if( eta2>=0.3 && eta2<0.6) return 0.945569;
    else if( eta2>=0.6 && eta2<0.9) return 0.939119;
    else if( eta2>=0.9 && eta2<1.2) return 0.935747;
    else if( eta2>=1.2 && eta2<1.6) return 0.929465;
    else if( eta2>=1.6 && eta2<2.1) return 0.920766;
    else if( eta2>=2.1 && eta2<=2.4) return 0.871181;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.867453;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.909644;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.925616;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.932169;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.931935;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.941917;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.901016;
    else if( eta2>=-0.2 && eta2<0) return 0.939818;
    else if( eta2>=0 && eta2<0.2) return 0.941468;
    else if( eta2>=0.2 && eta2<0.3) return 0.90916;
    else if( eta2>=0.3 && eta2<0.6) return 0.939225;
    else if( eta2>=0.6 && eta2<0.9) return 0.932817;
    else if( eta2>=0.9 && eta2<1.2) return 0.929465;
    else if( eta2>=1.2 && eta2<1.6) return 0.923224;
    else if( eta2>=1.6 && eta2<2.1) return 0.914577;
    else if( eta2>=2.1 && eta2<=2.4) return 0.865305;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.859233;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.901108;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.916949;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.923447;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.92322;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.933112;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.892592;
    else if( eta2>=-0.2 && eta2<0) return 0.931032;
    else if( eta2>=0 && eta2<0.2) return 0.932667;
    else if( eta2>=0.2 && eta2<0.3) return 0.900661;
    else if( eta2>=0.3 && eta2<0.6) return 0.930445;
    else if( eta2>=0.6 && eta2<0.9) return 0.924094;
    else if( eta2>=0.9 && eta2<1.2) return 0.920766;
    else if( eta2>=1.2 && eta2<1.6) return 0.914577;
    else if( eta2>=1.6 && eta2<2.1) return 0.905992;
    else if( eta2>=2.1 && eta2<=2.4) return 0.857112;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.812599;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.8525;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.867556;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.873727;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.873529;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.882904;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.844556;
    else if( eta2>=-0.2 && eta2<0) return 0.880931;
    else if( eta2>=0 && eta2<0.2) return 0.882482;
    else if( eta2>=0.2 && eta2<0.3) return 0.852196;
    else if( eta2>=0.3 && eta2<0.6) return 0.880379;
    else if( eta2>=0.6 && eta2<0.9) return 0.874358;
    else if( eta2>=0.9 && eta2<1.2) return 0.871181;
    else if( eta2>=1.2 && eta2<1.6) return 0.865305;
    else if( eta2>=1.6 && eta2<2.1) return 0.857112;
    else if( eta2>=2.1 && eta2<=2.4) return 0.810614;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_MC(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.846665;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.885059;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.896988;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.900202;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.899378;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.909826;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.887235;
    else if( eta2>=-0.2 && eta2<0) return 0.907031;
    else if( eta2>=0 && eta2<0.2) return 0.907324;
    else if( eta2>=0.2 && eta2<0.3) return 0.886888;
    else if( eta2>=0.3 && eta2<0.6) return 0.909496;
    else if( eta2>=0.6 && eta2<0.9) return 0.895606;
    else if( eta2>=0.9 && eta2<1.2) return 0.899665;
    else if( eta2>=1.2 && eta2<1.6) return 0.8952;
    else if( eta2>=1.6 && eta2<2.1) return 0.880749;
    else if( eta2>=2.1 && eta2<=2.4) return 0.839691;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.885059;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.92487;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.937251;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.940604;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.939721;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.950636;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.927033;
    else if( eta2>=-0.2 && eta2<0) return 0.947715;
    else if( eta2>=0 && eta2<0.2) return 0.948022;
    else if( eta2>=0.2 && eta2<0.3) return 0.92667;
    else if( eta2>=0.3 && eta2<0.6) return 0.950293;
    else if( eta2>=0.6 && eta2<0.9) return 0.935781;
    else if( eta2>=0.9 && eta2<1.2) return 0.940049;
    else if( eta2>=1.2 && eta2<1.6) return 0.935387;
    else if( eta2>=1.6 && eta2<2.1) return 0.920379;
    else if( eta2>=2.1 && eta2<=2.4) return 0.877748;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.896988;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.937251;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.949775;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.953171;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.952271;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.963331;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.939414;
    else if( eta2>=-0.2 && eta2<0) return 0.960372;
    else if( eta2>=0 && eta2<0.2) return 0.960683;
    else if( eta2>=0.2 && eta2<0.3) return 0.939046;
    else if( eta2>=0.3 && eta2<0.6) return 0.962984;
    else if( eta2>=0.6 && eta2<0.9) return 0.948279;
    else if( eta2>=0.9 && eta2<1.2) return 0.952611;
    else if( eta2>=1.2 && eta2<1.6) return 0.947887;
    else if( eta2>=1.6 && eta2<2.1) return 0.932703;
    else if( eta2>=2.1 && eta2<=2.4) return 0.889573;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.900202;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.940604;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.953171;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.956579;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.955676;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.966775;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.942773;
    else if( eta2>=-0.2 && eta2<0) return 0.963805;
    else if( eta2>=0 && eta2<0.2) return 0.964117;
    else if( eta2>=0.2 && eta2<0.3) return 0.942403;
    else if( eta2>=0.3 && eta2<0.6) return 0.966427;
    else if( eta2>=0.6 && eta2<0.9) return 0.951669;
    else if( eta2>=0.9 && eta2<1.2) return 0.956017;
    else if( eta2>=1.2 && eta2<1.6) return 0.951276;
    else if( eta2>=1.6 && eta2<2.1) return 0.936039;
    else if( eta2>=2.1 && eta2<=2.4) return 0.892759;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.899378;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.939721;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.952271;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.955676;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.954772;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.96586;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.941881;
    else if( eta2>=-0.2 && eta2<0) return 0.962893;
    else if( eta2>=0 && eta2<0.2) return 0.963205;
    else if( eta2>=0.2 && eta2<0.3) return 0.941512;
    else if( eta2>=0.3 && eta2<0.6) return 0.965512;
    else if( eta2>=0.6 && eta2<0.9) return 0.950769;
    else if( eta2>=0.9 && eta2<1.2) return 0.955114;
    else if( eta2>=1.2 && eta2<1.6) return 0.950379;
    else if( eta2>=1.6 && eta2<2.1) return 0.935162;
    else if( eta2>=2.1 && eta2<=2.4) return 0.891941;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.909826;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.950636;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.963331;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.966775;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.96586;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.977077;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.952819;
    else if( eta2>=-0.2 && eta2<0) return 0.974076;
    else if( eta2>=0 && eta2<0.2) return 0.974391;
    else if( eta2>=0.2 && eta2<0.3) return 0.952446;
    else if( eta2>=0.3 && eta2<0.6) return 0.976725;
    else if( eta2>=0.6 && eta2<0.9) return 0.96181;
    else if( eta2>=0.9 && eta2<1.2) return 0.966207;
    else if( eta2>=1.2 && eta2<1.6) return 0.961416;
    else if( eta2>=1.6 && eta2<2.1) return 0.946024;
    else if( eta2>=2.1 && eta2<=2.4) return 0.902303;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.887235;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.927033;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.939414;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.942773;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941881;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.952819;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.929164;
    else if( eta2>=-0.2 && eta2<0) return 0.949892;
    else if( eta2>=0 && eta2<0.2) return 0.9502;
    else if( eta2>=0.2 && eta2<0.3) return 0.9288;
    else if( eta2>=0.3 && eta2<0.6) return 0.952476;
    else if( eta2>=0.6 && eta2<0.9) return 0.937932;
    else if( eta2>=0.9 && eta2<1.2) return 0.942218;
    else if( eta2>=1.2 && eta2<1.6) return 0.937547;
    else if( eta2>=1.6 && eta2<2.1) return 0.922536;
    else if( eta2>=2.1 && eta2<=2.4) return 0.879899;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.907031;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.947715;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.960372;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.963805;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.962893;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.974076;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.949892;
    else if( eta2>=-0.2 && eta2<0) return 0.971084;
    else if( eta2>=0 && eta2<0.2) return 0.971398;
    else if( eta2>=0.2 && eta2<0.3) return 0.94952;
    else if( eta2>=0.3 && eta2<0.6) return 0.973725;
    else if( eta2>=0.6 && eta2<0.9) return 0.958856;
    else if( eta2>=0.9 && eta2<1.2) return 0.963239;
    else if( eta2>=1.2 && eta2<1.6) return 0.958463;
    else if( eta2>=1.6 && eta2<2.1) return 0.943117;
    else if( eta2>=2.1 && eta2<=2.4) return 0.89953;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.907324;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.948022;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.960683;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.964117;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.963205;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.974391;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.9502;
    else if( eta2>=-0.2 && eta2<0) return 0.971398;
    else if( eta2>=0 && eta2<0.2) return 0.971713;
    else if( eta2>=0.2 && eta2<0.3) return 0.949828;
    else if( eta2>=0.3 && eta2<0.6) return 0.97404;
    else if( eta2>=0.6 && eta2<0.9) return 0.959166;
    else if( eta2>=0.9 && eta2<1.2) return 0.963551;
    else if( eta2>=1.2 && eta2<1.6) return 0.958773;
    else if( eta2>=1.6 && eta2<2.1) return 0.943423;
    else if( eta2>=2.1 && eta2<=2.4) return 0.899822;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.886888;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.92667;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.939046;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.942403;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.941512;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.952446;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.9288;
    else if( eta2>=-0.2 && eta2<0) return 0.94952;
    else if( eta2>=0 && eta2<0.2) return 0.949828;
    else if( eta2>=0.2 && eta2<0.3) return 0.928436;
    else if( eta2>=0.3 && eta2<0.6) return 0.952103;
    else if( eta2>=0.6 && eta2<0.9) return 0.937564;
    else if( eta2>=0.9 && eta2<1.2) return 0.941849;
    else if( eta2>=1.2 && eta2<1.6) return 0.93718;
    else if( eta2>=1.6 && eta2<2.1) return 0.922174;
    else if( eta2>=2.1 && eta2<=2.4) return 0.879554;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.909496;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.950293;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.962984;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.966427;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.965512;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.976725;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.952476;
    else if( eta2>=-0.2 && eta2<0) return 0.973725;
    else if( eta2>=0 && eta2<0.2) return 0.97404;
    else if( eta2>=0.2 && eta2<0.3) return 0.952103;
    else if( eta2>=0.3 && eta2<0.6) return 0.976374;
    else if( eta2>=0.6 && eta2<0.9) return 0.961464;
    else if( eta2>=0.9 && eta2<1.2) return 0.965859;
    else if( eta2>=1.2 && eta2<1.6) return 0.96107;
    else if( eta2>=1.6 && eta2<2.1) return 0.945682;
    else if( eta2>=2.1 && eta2<=2.4) return 0.901975;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.895606;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.935781;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.948279;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951669;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950769;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.96181;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.937932;
    else if( eta2>=-0.2 && eta2<0) return 0.958856;
    else if( eta2>=0 && eta2<0.2) return 0.959166;
    else if( eta2>=0.2 && eta2<0.3) return 0.937564;
    else if( eta2>=0.3 && eta2<0.6) return 0.961464;
    else if( eta2>=0.6 && eta2<0.9) return 0.946782;
    else if( eta2>=0.9 && eta2<1.2) return 0.951109;
    else if( eta2>=1.2 && eta2<1.6) return 0.946394;
    else if( eta2>=1.6 && eta2<2.1) return 0.931241;
    else if( eta2>=2.1 && eta2<=2.4) return 0.8882;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.899665;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.940049;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.952611;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.956017;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.955114;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.966207;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.942218;
    else if( eta2>=-0.2 && eta2<0) return 0.963239;
    else if( eta2>=0 && eta2<0.2) return 0.963551;
    else if( eta2>=0.2 && eta2<0.3) return 0.941849;
    else if( eta2>=0.3 && eta2<0.6) return 0.965859;
    else if( eta2>=0.6 && eta2<0.9) return 0.951109;
    else if( eta2>=0.9 && eta2<1.2) return 0.955454;
    else if( eta2>=1.2 && eta2<1.6) return 0.950717;
    else if( eta2>=1.6 && eta2<2.1) return 0.935487;
    else if( eta2>=2.1 && eta2<=2.4) return 0.892228;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.8952;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.935387;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.947887;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.951276;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.950379;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.961416;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.937547;
    else if( eta2>=-0.2 && eta2<0) return 0.958463;
    else if( eta2>=0 && eta2<0.2) return 0.958773;
    else if( eta2>=0.2 && eta2<0.3) return 0.93718;
    else if( eta2>=0.3 && eta2<0.6) return 0.96107;
    else if( eta2>=0.6 && eta2<0.9) return 0.946394;
    else if( eta2>=0.9 && eta2<1.2) return 0.950717;
    else if( eta2>=1.2 && eta2<1.6) return 0.946003;
    else if( eta2>=1.6 && eta2<2.1) return 0.930847;
    else if( eta2>=2.1 && eta2<=2.4) return 0.8878;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.880749;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.920379;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.932703;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.936039;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.935162;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.946024;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.922536;
    else if( eta2>=-0.2 && eta2<0) return 0.943117;
    else if( eta2>=0 && eta2<0.2) return 0.943423;
    else if( eta2>=0.2 && eta2<0.3) return 0.922174;
    else if( eta2>=0.3 && eta2<0.6) return 0.945682;
    else if( eta2>=0.6 && eta2<0.9) return 0.931241;
    else if( eta2>=0.9 && eta2<1.2) return 0.935487;
    else if( eta2>=1.2 && eta2<1.6) return 0.930847;
    else if( eta2>=1.6 && eta2<2.1) return 0.915909;
    else if( eta2>=2.1 && eta2<=2.4) return 0.873474;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.839691;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.877748;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.889573;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.892759;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.891941;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.902303;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.879899;
    else if( eta2>=-0.2 && eta2<0) return 0.89953;
    else if( eta2>=0 && eta2<0.2) return 0.899822;
    else if( eta2>=0.2 && eta2<0.3) return 0.879554;
    else if( eta2>=0.3 && eta2<0.6) return 0.901975;
    else if( eta2>=0.6 && eta2<0.9) return 0.8882;
    else if( eta2>=0.9 && eta2<1.2) return 0.892228;
    else if( eta2>=1.2 && eta2<1.6) return 0.8878;
    else if( eta2>=1.6 && eta2<2.1) return 0.873474;
    else if( eta2>=2.1 && eta2<=2.4) return 0.832773;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


Double_t Eff_HLT_Mu17_Mu8_2011_TPfit_RunAB_EtaEta_DATAoverMC(Double_t eta1, Double_t eta2) {
  if( eta1>=-2.4 && eta1<-2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.962112;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.965597;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.96959;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.973002;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.973675;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.972823;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.954265;
    else if( eta2>=-0.2 && eta2<0) return 0.973641;
    else if( eta2>=0 && eta2<0.2) return 0.97504;
    else if( eta2>=0.2 && eta2<0.3) return 0.963274;
    else if( eta2>=0.3 && eta2<0.6) return 0.970394;
    else if( eta2>=0.6 && eta2<0.9) return 0.978703;
    else if( eta2>=0.9 && eta2<1.2) return 0.970745;
    else if( eta2>=1.2 && eta2<1.6) return 0.969005;
    else if( eta2>=1.6 && eta2<2.1) return 0.975571;
    else if( eta2>=2.1 && eta2<=2.4) return 0.967735;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-2.1 && eta1<-1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.965597;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.969054;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.973061;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.976463;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.977139;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.97627;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.957652;
    else if( eta2>=-0.2 && eta2<0) return 0.977096;
    else if( eta2>=0 && eta2<0.2) return 0.978494;
    else if( eta2>=0.2 && eta2<0.3) return 0.966688;
    else if( eta2>=0.3 && eta2<0.6) return 0.973831;
    else if( eta2>=0.6 && eta2<0.9) return 0.982183;
    else if( eta2>=0.9 && eta2<1.2) return 0.974204;
    else if( eta2>=1.2 && eta2<1.6) return 0.972479;
    else if( eta2>=1.6 && eta2<2.1) return 0.979062;
    else if( eta2>=2.1 && eta2<=2.4) return 0.971235;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.6 && eta1<-1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.96959;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.973061;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.977087;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.980499;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.981178;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.980302;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.961609;
    else if( eta2>=-0.2 && eta2<0) return 0.981132;
    else if( eta2>=0 && eta2<0.2) return 0.982535;
    else if( eta2>=0.2 && eta2<0.3) return 0.970681;
    else if( eta2>=0.3 && eta2<0.6) return 0.977852;
    else if( eta2>=0.6 && eta2<0.9) return 0.986242;
    else if( eta2>=0.9 && eta2<1.2) return 0.978231;
    else if( eta2>=1.2 && eta2<1.6) return 0.976504;
    else if( eta2>=1.6 && eta2<2.1) return 0.98311;
    else if( eta2>=2.1 && eta2<=2.4) return 0.975251;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-1.2 && eta1<-0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.973002;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.976463;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.980499;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.98392;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.9846;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98372;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.964962;
    else if( eta2>=-0.2 && eta2<0) return 0.984554;
    else if( eta2>=0 && eta2<0.2) return 0.985961;
    else if( eta2>=0.2 && eta2<0.3) return 0.974066;
    else if( eta2>=0.3 && eta2<0.6) return 0.981262;
    else if( eta2>=0.6 && eta2<0.9) return 0.989682;
    else if( eta2>=0.9 && eta2<1.2) return 0.981645;
    else if( eta2>=1.2 && eta2<1.6) return 0.979914;
    else if( eta2>=1.6 && eta2<2.1) return 0.986547;
    else if( eta2>=2.1 && eta2<=2.4) return 0.978681;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.9 && eta1<-0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.973675;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.977139;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.981178;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.9846;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.985281;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.9844;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965629;
    else if( eta2>=-0.2 && eta2<0) return 0.985234;
    else if( eta2>=0 && eta2<0.2) return 0.986642;
    else if( eta2>=0.2 && eta2<0.3) return 0.974739;
    else if( eta2>=0.3 && eta2<0.6) return 0.98194;
    else if( eta2>=0.6 && eta2<0.9) return 0.990366;
    else if( eta2>=0.9 && eta2<1.2) return 0.982324;
    else if( eta2>=1.2 && eta2<1.6) return 0.980593;
    else if( eta2>=1.6 && eta2<2.1) return 0.98723;
    else if( eta2>=2.1 && eta2<=2.4) return 0.979358;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.6 && eta1<-0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.972823;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.97627;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.980302;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.98372;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.9844;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.983518;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.964765;
    else if( eta2>=-0.2 && eta2<0) return 0.984352;
    else if( eta2>=0 && eta2<0.2) return 0.985759;
    else if( eta2>=0.2 && eta2<0.3) return 0.973866;
    else if( eta2>=0.3 && eta2<0.6) return 0.98106;
    else if( eta2>=0.6 && eta2<0.9) return 0.98948;
    else if( eta2>=0.9 && eta2<1.2) return 0.981446;
    else if( eta2>=1.2 && eta2<1.6) return 0.979718;
    else if( eta2>=1.6 && eta2<2.1) return 0.986352;
    else if( eta2>=2.1 && eta2<=2.4) return 0.9785;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.3 && eta1<-0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.954265;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.957652;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.961609;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.964962;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.965629;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.964765;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.946369;
    else if( eta2>=-0.2 && eta2<0) return 0.965582;
    else if( eta2>=0 && eta2<0.2) return 0.966963;
    else if( eta2>=0.2 && eta2<0.3) return 0.955296;
    else if( eta2>=0.3 && eta2<0.6) return 0.962354;
    else if( eta2>=0.6 && eta2<0.9) return 0.970612;
    else if( eta2>=0.9 && eta2<1.2) return 0.962731;
    else if( eta2>=1.2 && eta2<1.6) return 0.961036;
    else if( eta2>=1.6 && eta2<2.1) return 0.967542;
    else if( eta2>=2.1 && eta2<=2.4) return 0.959834;
    else return 0.;
    return 0.;
  }
  else if( eta1>=-0.2 && eta1<0) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.973641;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.977096;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.981132;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.984554;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.985234;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.984352;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.965582;
    else if( eta2>=-0.2 && eta2<0) return 0.985186;
    else if( eta2>=0 && eta2<0.2) return 0.986594;
    else if( eta2>=0.2 && eta2<0.3) return 0.974691;
    else if( eta2>=0.3 && eta2<0.6) return 0.981892;
    else if( eta2>=0.6 && eta2<0.9) return 0.990318;
    else if( eta2>=0.9 && eta2<1.2) return 0.982277;
    else if( eta2>=1.2 && eta2<1.6) return 0.980548;
    else if( eta2>=1.6 && eta2<2.1) return 0.987186;
    else if( eta2>=2.1 && eta2<=2.4) return 0.979323;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0 && eta1<0.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.97504;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.978494;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.982535;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.985961;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.986642;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.985759;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.966963;
    else if( eta2>=-0.2 && eta2<0) return 0.986594;
    else if( eta2>=0 && eta2<0.2) return 0.988005;
    else if( eta2>=0.2 && eta2<0.3) return 0.976085;
    else if( eta2>=0.3 && eta2<0.6) return 0.983295;
    else if( eta2>=0.6 && eta2<0.9) return 0.991734;
    else if( eta2>=0.9 && eta2<1.2) return 0.983682;
    else if( eta2>=1.2 && eta2<1.6) return 0.98195;
    else if( eta2>=1.6 && eta2<2.1) return 0.9886;
    else if( eta2>=2.1 && eta2<=2.4) return 0.98073;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.2 && eta1<0.3) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.963274;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.966688;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.970681;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.974066;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.974739;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.973866;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.955296;
    else if( eta2>=-0.2 && eta2<0) return 0.974691;
    else if( eta2>=0 && eta2<0.2) return 0.976085;
    else if( eta2>=0.2 && eta2<0.3) return 0.964308;
    else if( eta2>=0.3 && eta2<0.6) return 0.971432;
    else if( eta2>=0.6 && eta2<0.9) return 0.979769;
    else if( eta2>=0.9 && eta2<1.2) return 0.971814;
    else if( eta2>=1.2 && eta2<1.6) return 0.970103;
    else if( eta2>=1.6 && eta2<2.1) return 0.976671;
    else if( eta2>=2.1 && eta2<=2.4) return 0.968895;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.3 && eta1<0.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.970394;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.973831;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.977852;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.981262;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.98194;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98106;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.962354;
    else if( eta2>=-0.2 && eta2<0) return 0.981892;
    else if( eta2>=0 && eta2<0.2) return 0.983295;
    else if( eta2>=0.2 && eta2<0.3) return 0.971432;
    else if( eta2>=0.3 && eta2<0.6) return 0.978608;
    else if( eta2>=0.6 && eta2<0.9) return 0.987007;
    else if( eta2>=0.9 && eta2<1.2) return 0.978993;
    else if( eta2>=1.2 && eta2<1.6) return 0.97727;
    else if( eta2>=1.6 && eta2<2.1) return 0.983888;
    else if( eta2>=2.1 && eta2<=2.4) return 0.976057;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.6 && eta1<0.9) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.978703;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.982183;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.986242;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.989682;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.990366;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.98948;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.970612;
    else if( eta2>=-0.2 && eta2<0) return 0.990318;
    else if( eta2>=0 && eta2<0.2) return 0.991734;
    else if( eta2>=0.2 && eta2<0.3) return 0.979769;
    else if( eta2>=0.3 && eta2<0.6) return 0.987007;
    else if( eta2>=0.6 && eta2<0.9) return 0.995477;
    else if( eta2>=0.9 && eta2<1.2) return 0.987393;
    else if( eta2>=1.2 && eta2<1.6) return 0.985654;
    else if( eta2>=1.6 && eta2<2.1) return 0.992326;
    else if( eta2>=2.1 && eta2<=2.4) return 0.984415;
    else return 0.;
    return 0.;
  }
  else if( eta1>=0.9 && eta1<1.2) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.970745;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.974204;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.978231;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.981645;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.982324;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.981446;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.962731;
    else if( eta2>=-0.2 && eta2<0) return 0.982277;
    else if( eta2>=0 && eta2<0.2) return 0.983682;
    else if( eta2>=0.2 && eta2<0.3) return 0.971814;
    else if( eta2>=0.3 && eta2<0.6) return 0.978993;
    else if( eta2>=0.6 && eta2<0.9) return 0.987393;
    else if( eta2>=0.9 && eta2<1.2) return 0.979374;
    else if( eta2>=1.2 && eta2<1.6) return 0.977647;
    else if( eta2>=1.6 && eta2<2.1) return 0.984264;
    else if( eta2>=2.1 && eta2<=2.4) return 0.976411;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.2 && eta1<1.6) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.969005;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.972479;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.976504;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.979914;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.980593;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.979718;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.961036;
    else if( eta2>=-0.2 && eta2<0) return 0.980548;
    else if( eta2>=0 && eta2<0.2) return 0.98195;
    else if( eta2>=0.2 && eta2<0.3) return 0.970103;
    else if( eta2>=0.3 && eta2<0.6) return 0.97727;
    else if( eta2>=0.6 && eta2<0.9) return 0.985654;
    else if( eta2>=0.9 && eta2<1.2) return 0.977647;
    else if( eta2>=1.2 && eta2<1.6) return 0.975921;
    else if( eta2>=1.6 && eta2<2.1) return 0.982521;
    else if( eta2>=2.1 && eta2<=2.4) return 0.974662;
    else return 0.;
    return 0.;
  }
  else if( eta1>=1.6 && eta1<2.1) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.975571;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.979062;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.98311;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.986547;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.98723;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.986352;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.967542;
    else if( eta2>=-0.2 && eta2<0) return 0.987186;
    else if( eta2>=0 && eta2<0.2) return 0.9886;
    else if( eta2>=0.2 && eta2<0.3) return 0.976671;
    else if( eta2>=0.3 && eta2<0.6) return 0.983888;
    else if( eta2>=0.6 && eta2<0.9) return 0.992326;
    else if( eta2>=0.9 && eta2<1.2) return 0.984264;
    else if( eta2>=1.2 && eta2<1.6) return 0.982521;
    else if( eta2>=1.6 && eta2<2.1) return 0.989173;
    else if( eta2>=2.1 && eta2<=2.4) return 0.981267;
    else return 0.;
    return 0.;
  }
  else if( eta1>=2.1 && eta1<=2.4) {
    if( eta2>=-2.4 && eta2<-2.1) return 0.967735;
    else if( eta2>=-2.1 && eta2<-1.6) return 0.971235;
    else if( eta2>=-1.6 && eta2<-1.2) return 0.975251;
    else if( eta2>=-1.2 && eta2<-0.9) return 0.978681;
    else if( eta2>=-0.9 && eta2<-0.6) return 0.979358;
    else if( eta2>=-0.6 && eta2<-0.3) return 0.9785;
    else if( eta2>=-0.3 && eta2<-0.2) return 0.959834;
    else if( eta2>=-0.2 && eta2<0) return 0.979323;
    else if( eta2>=0 && eta2<0.2) return 0.98073;
    else if( eta2>=0.2 && eta2<0.3) return 0.968895;
    else if( eta2>=0.3 && eta2<0.6) return 0.976057;
    else if( eta2>=0.6 && eta2<0.9) return 0.984415;
    else if( eta2>=0.9 && eta2<1.2) return 0.976411;
    else if( eta2>=1.2 && eta2<1.6) return 0.974662;
    else if( eta2>=1.6 && eta2<2.1) return 0.981267;
    else if( eta2>=2.1 && eta2<=2.4) return 0.973391;
    else return 0.;
    return 0.;
  }
  else return 0.;
  return 0.;
}


