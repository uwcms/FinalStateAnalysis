// A slight revision of the bare RochesterCorrection code...
// Modifications from L. Gray

#ifndef __ROCHESTER_CORRECTIONS_2011_H__
#define __ROCHESTER_CORRECTIONS_2011_H__

#include <iostream>
#include <TChain.h>
#include <TClonesArray.h>
#include <TString.h>
#include <map>

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"

#include <TSystem.h>
#include <TROOT.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include <TRandom3.h>

namespace rochcor {

  class RochesterCorrections2011 {
  public:
    RochesterCorrections2011(bool central_value);    
    ~RochesterCorrections2011();
    
    void momcor_mc(TLorentzVector&, float, float, int);
    void momcor_data(TLorentzVector&, float, float, int);
    
    void musclefit_data(TLorentzVector& , TLorentzVector&);
    
    float zptcor(float);
    int etabin(float);
    int phibin(float);
    
  private:
    
    edm::Service<edm::RandomNumberGenerator> rng;

    //TRandom3 eran;
    //TRandom3 sran;
    
    
    //  static float netabin[9] = {-2.4,-2.1,-1.4,-0.7,0.0,0.7,1.4,2.1,2.4};
    static constexpr double pi = 3.14159265358979323846;
    static const float netabin[9];
    
    static constexpr float genm_smr = 9.09956e+01; //gen mass peak with eta dependent gaussian smearing => better match in Z mass profile vs. eta/phi
    static constexpr float genm = 91.06; //gen mass peak without smearing => Z mass profile vs. eta/phi in CMS note
    
    static constexpr float recmA = 9.10062e+01; //rec mass peak in MC (2011A)
    static constexpr float drecmA = 9.09285e+01; //rec mass peak in data (2011A)
    static constexpr float mgsclA_stat = 0.0001; //stat. error of global factor for mass peak in MC (2011A)  
    static constexpr float mgsclA_syst = 0.0006; //syst. error of global factor for mass peak in MC (2011A)  
    static constexpr float dgsclA_stat = 0.0001; //stat. error of global factor for mass peak in data (2011A)
    static constexpr float dgsclA_syst = 0.0008; //syst. error of global factor for mass peak in data (2011A)
    static constexpr float recmB = 9.10210e+01; //rec mass peak in MC (2011B)
    static constexpr float drecmB = 9.09469e+01; //rec mass peak in data (2011B)
    static constexpr float mgsclB_stat = 0.0001; //stat. error of global factor for mass peak in MC (2011B)  
    static constexpr float mgsclB_syst = 0.0006; //syst. error of global factor for mass peak in MC (2011B)  
    static constexpr float dgsclB_stat = 0.0001; //stat. error of global factor for mass peak in data (2011B)
    static constexpr float dgsclB_syst = 0.0008; //syst. error of global factor for mass peak in data (2011B)
    
    //iteration2 after FSR : after Z Pt correction
    static constexpr float deltaA = -2.85242e-06;
    static constexpr float deltaA_stat = 7.74389e-07;
    static constexpr float deltaA_syst = 6.992e-07;
    
    static constexpr float sfA = 44.6463;
    static constexpr float sfA_stat = 1.92224;
    static constexpr float sfA_syst = 9.29;
    
    static constexpr float deltaB = -5.68463e-06;
    static constexpr float deltaB_stat = 8.21406e-07;
    static constexpr float deltaB_syst = 1.4268e-06;
    
    static constexpr float sfB = 23.8652;
    static constexpr float sfB_stat = 0.941748;
    static constexpr float sfB_syst = 4.86;
    
    static constexpr float apar = 1.0; //+- 0.002
    static constexpr float bpar = -5.03313e-06; //+- 1.57968e-06
    static constexpr float cpar = -4.41463e-05; //+- 1.92775e-06
    static constexpr float d0par = -0.000148871; //+- 3.16301e-06
    static constexpr float e0par = 1.59501; //+- 0.0249021
    static constexpr float d1par = 7.95495e-05; //+- 1.12386e-05
    static constexpr float e1par = -0.364823; //+- 0.17896
    static constexpr float d2par = 0.000152032; //+- 5.68386e-06
    static constexpr float e2par = 0.410195; //+- 0.0431732
    
    //---------------------------------------------------------------------------------------------
    
    static const float dcor_bfA[8][8];  
    static const float dcor_maA[8][8];
    static const float mcor_bfA[8][8];
    static const float mcor_maA[8][8];
    static const float dcor_bfAer[8][8];  
    static const float dcor_maAer[8][8];
    static const float mcor_bfAer[8][8];
    static const float mcor_maAer[8][8];
    
    static const float dcor_bfB[8][8];  
    static const float dcor_maB[8][8];
    static const float mcor_bfB[8][8];
    static const float mcor_maB[8][8];
    static const float dcor_bfBer[8][8];  
    static const float dcor_maBer[8][8];
    static const float mcor_bfBer[8][8];
    static const float mcor_maBer[8][8];
    
    //=======================================================================================================
    
    static const float dmavgA[8][8];  
    static const float dpavgA[8][8];  
    static const float mmavgA[8][8];  
    static const float mpavgA[8][8];
    
    static const float dmavgB[8][8];  
    static const float dpavgB[8][8];  
    static const float mmavgB[8][8];  
    static const float mpavgB[8][8];
    
    //===============================================================================================
    //parameters for Z pt correction
    static const int nptbins=84;
    static const float ptlow[85];    
    
    static const float zptscl[84];
    static const float zptscler[84];
    
    float mptsys_mc_dm[8][8];
    float mptsys_mc_da[8][8];
    float mptsys_da_dm[8][8];
    float mptsys_da_da[8][8];
    
  };

}// namespace rochcor

#endif  
