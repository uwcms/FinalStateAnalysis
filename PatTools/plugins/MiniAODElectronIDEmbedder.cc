/*
 * Embeds the electron ID as recommended by EGamma POG (expected to be depreciated when IDs included by default).
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentificationRun2
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/HEEPElectronIdentificationRun2
 * Author: Devin N. Taylor, UW-Madison
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "EgammaAnalysis/ElectronTools/interface/EGammaMvaEleEstimatorCSA14.h"

#include <math.h>

// class declaration
class MiniAODElectronIDEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODElectronIDEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODElectronIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    bool cutBasedIDHelper(pat::Electron, double, double, double, double, double, double, double, double, int);
    edm::EDGetTokenT<pat::ElectronCollection> electronsCollection_;
    edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
    edm::EDGetTokenT<reco::ConversionCollection> convToken_;
    edm::EDGetTokenT<reco::BeamSpot> beamToken_;
    edm::InputTag MVAidCollection_;
    std::string bunchspacing_;
    EGammaMvaEleEstimatorCSA14* MVATrig_;
    EGammaMvaEleEstimatorCSA14* MVANonTrig_;
    reco::Vertex pv_;
    edm::Handle<reco::ConversionCollection> convs_;
    edm::Handle<reco::BeamSpot> thebs_;
};

// class member functions
MiniAODElectronIDEmbedder::MiniAODElectronIDEmbedder(const edm::ParameterSet& pset) {
  electronsCollection_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("src"));
  //  MVAidCollection_     = pset.getParameter<edm::InputTag>("MVAId");
  vtxToken_            = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vertices"));
  convToken_           = consumes<reco::ConversionCollection>(pset.getParameter<edm::InputTag>("convcollection"));
  beamToken_           = consumes<reco::BeamSpot>(pset.getParameter<edm::InputTag>("beamspot"));
  bunchspacing_        = pset.getUntrackedParameter<std::string>("bunchspacing","50ns");

  std::vector<std::string> myManualCatWeightsTrigXML;
  if (bunchspacing_ == "50ns"){
    myManualCatWeightsTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_50ns_EB_BDT.weights.xml");
    myManualCatWeightsTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_50ns_EE_BDT.weights.xml");
  }
  else{
    myManualCatWeightsTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EB_BDT.weights.xml");
    myManualCatWeightsTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EE_BDT.weights.xml");
  }
  
  vector<string> myManualCatWeightsTrig;
  string the_path;
  for (unsigned i  = 0 ; i < myManualCatWeightsTrigXML.size() ; i++){
    the_path = edm::FileInPath ( myManualCatWeightsTrigXML[i] ).fullPath();
    myManualCatWeightsTrig.push_back(the_path);
  }
  
  MVATrig_ = new EGammaMvaEleEstimatorCSA14();
  MVATrig_->initialize("BDT",
                       EGammaMvaEleEstimatorCSA14::kTrig,
                       true,
                       myManualCatWeightsTrig);

  std::vector<std::string> myManualCatWeightsNonTrigXML;
  // Should eventually be passed in as arguments, as they will change over time
  if (bunchspacing_ == "50ns"){
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EB_5_50ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EE_5_50ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EB_10_50ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EE_10_50ns_BDT.weights.xml");
  }
  else{
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EB_5_25ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EE_5_25ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EB_10_25ns_BDT.weights.xml");
    myManualCatWeightsNonTrigXML.push_back("EgammaAnalysis/ElectronTools/data/CSA14/EIDmva_EE_10_25ns_BDT.weights.xml");
  }
  
  vector<string> myManualCatWeightsNonTrig;
  for (unsigned i  = 0 ; i < myManualCatWeightsNonTrigXML.size() ; i++){
    the_path = edm::FileInPath ( myManualCatWeightsNonTrigXML[i] ).fullPath();
    myManualCatWeightsNonTrig.push_back(the_path);
  }
  
  MVANonTrig_ = new EGammaMvaEleEstimatorCSA14();
  MVANonTrig_->initialize("BDT",
                       EGammaMvaEleEstimatorCSA14::kNonTrig,
                       true,
                       myManualCatWeightsNonTrig);

  produces<pat::ElectronCollection>();
}

void MiniAODElectronIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<vector<pat::Electron>> electronsCollection;
  evt.getByToken(electronsCollection_ , electronsCollection);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vtxToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  pv_ = vertices->front();

  evt.getByToken(convToken_, convs_);
  evt.getByToken(beamToken_, thebs_);

  const vector<pat::Electron> * electrons = electronsCollection.product();

  unsigned int nbElectron =  electrons->size();

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(nbElectron);

  for(unsigned i = 0 ; i < nbElectron; i++){
    pat::Electron electron(electrons->at(i));

    // mva
    electron.addUserFloat("mvaTrigV0CSA14",MVATrig_->mvaValue(electrons->at(i),false));
    electron.addUserFloat("mvaNonTrigV0CSA14",MVANonTrig_->mvaValue(electrons->at(i),false));

    float mva = MVANonTrig_->mvaValue(electrons->at(i),false);
    float pt = electron.pt();
    float eta = electron.superCluster()->eta();
    int mvaidpass = 0;

    if (pt > 5.0 && pt < 10.0) {
      if ( (eta<0.8 && mva>0.47) || (eta>0.8 && eta<1.479 && mva>0.004) || (eta>1.479 && mva>0.295) )
        mvaidpass=1;
    }
    else if (pt > 10.0) {
      if ( (eta<0.8 && mva>-0.34) || (eta>0.8 && eta<1.479 && mva>-0.65) || (eta>1.479 && mva>0.6) )
        mvaidpass=1;
    }

    electron.addUserInt("mvaidwp",mvaidpass);

    if( thebs_.isValid() && convs_.isValid() ) {
       bool hasConversion = ConversionTools::hasMatchedConversion(electron,convs_,thebs_->position());
       electron.addUserFloat("hasConversion", hasConversion);
    }

    // cutbased id 
    float etaSC_ = electron.superCluster()->eta();
    bool veto25 = false, loose25 = false, medium25 = false, tight25 = false;
    bool veto50 = false, loose50 = false, medium50 = false, tight50 = false;
    if (abs(etaSC_) < 1.479){
      veto50 = cutBasedIDHelper(electron,0.021,0.25,0.012,0.24,0.031,0.5,0.32,0.24,2);
      loose50 = cutBasedIDHelper(electron,0.016,0.08,0.012,0.15,0.019,0.036,0.11,0.18,1);
      medium50 = cutBasedIDHelper(electron,0.015,0.051,0.01,0.10,0.012,0.030,0.053,0.14,1);
      tight50 = cutBasedIDHelper(electron,0.012,0.024,0.01,0.074,0.0091,0.017,0.026,0.10,1);
      veto25 = cutBasedIDHelper(electron,0.02,0.2579,0.0125,0.2564,0.025,0.5863,0.1508,0.3313,2);
      loose25 = cutBasedIDHelper(electron,0.0181,0.0936,0.0123,0.141,0.0166,0.54342,0.1353,0.24,1);
      medium25 = cutBasedIDHelper(electron,0.0106,0.0323,0.0107,0.067,0.0131,0.22310,0.1043,0.2179,1);
      tight25 = cutBasedIDHelper(electron,0.0091,0.031,0.0106,0.0532,0.0126,0.0116,0.0609,0.1649,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      veto50 = cutBasedIDHelper(electron,0.028,0.23,0.035,0.19,0.22,0.91,0.13,0.24,3);
      loose50 = cutBasedIDHelper(electron,0.025,0.097,0.032,0.12,0.099,0.88,0.11,0.21,1);
      medium50 = cutBasedIDHelper(electron,0.023,0.056,0.030,0.099,0.068,0.78,0.11,0.15,1);
      tight50 = cutBasedIDHelper(electron,0.019,0.043,0.029,0.08,0.037,0.065,0.076,0.14,1);
      veto25 = cutBasedIDHelper(electron,0.0141,0.2591,0.0371,0.1335,0.2232,0.9513,0.1542,0.3816,3);
      loose25 = cutBasedIDHelper(electron,0.0124,0.0642,0.035,0.1115,0.098,0.9187,0.1443,0.3529,1);
      medium25 = cutBasedIDHelper(electron,0.0108,0.0455,0.0318,0.097,0.0845,0.7523,0.1201,0.254,1);
      tight25 = cutBasedIDHelper(electron,0.0106,0.0359,0.0305,0.0835,0.0163,0.5999,0.1126,0.2075,1);
    }

    electron.addUserInt("cutBasedElectronID-CSA14-50ns-V1-standalone-veto",veto50);
    electron.addUserInt("cutBasedElectronID-CSA14-50ns-V1-standalone-loose",loose50);
    electron.addUserInt("cutBasedElectronID-CSA14-50ns-V1-standalone-medium",medium50);
    electron.addUserInt("cutBasedElectronID-CSA14-50ns-V1-standalone-tight",tight50);
    electron.addUserInt("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-veto",veto25);
    electron.addUserInt("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-loose",loose25);
    electron.addUserInt("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-medium",medium25);
    electron.addUserInt("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-tight",tight25);

    output->push_back(electron);
  }

  evt.put(output);
}

bool MiniAODElectronIDEmbedder::cutBasedIDHelper(pat::Electron el,  double dEtaIn, double dPhiIn,
    double full5x5_sigmaIetaIeta, double hOverE, double d0, double dz, double ooEmooP,
    double relIsoWithDBeta, int expectedMissingInnerHits){
  // What follows is from Lindsay's miniAOD code PR 5014
  float pt_ = el.pt();

  // ID and matching
  float dEtaIn_ = el.deltaEtaSuperClusterTrackAtVtx();
  float dPhiIn_ = el.deltaPhiSuperClusterTrackAtVtx();
  float hOverE_ = el.hcalOverEcal();
  float full5x5_sigmaIetaIeta_ = el.full5x5_sigmaIetaIeta();
  // |1/E-1/p| = |1/E - EoverPinner/E| is computed below
  // The if protects against ecalEnergy == inf or zero (always
  // the case for electrons below 5 GeV in miniAOD)
  float ooEmooP_ = 0;
  if( el.ecalEnergy() == 0 ){
    //printf("Electron energy is zero!\n");
    ooEmooP_ = 1e30;
  }else if( !std::isfinite(el.ecalEnergy())){
    //printf("Electron energy is not finite!\n");
    ooEmooP_ = 1e30;
  }else{
    ooEmooP_ = fabs(1.0/el.ecalEnergy() - el.eSuperClusterOverP()/el.ecalEnergy() );
  }

  // Isolation
  reco::GsfElectron::PflowIsolationVariables pfIso = el.pfIsolationVariables();
  // Compute isolation with delta beta correction for PU
  float absiso = pfIso.sumChargedHadronPt
    + std::max(0.0 , pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt );
  float relIsoWithDBeta_ = absiso/pt_;

  // Impact parameter
  float d0_ = (-1) * el.gsfTrack()->dxy(pv_.position() );
  float dz_ = el.gsfTrack()->dz( pv_.position() );

  // Conversion rejection
  int expectedMissingInnerHits_ = el.gsfTrack()->trackerExpectedHitsInner().numberOfHits();
  bool passConversionVeto_ = false;
  if( thebs_.isValid() && convs_.isValid() ) {
    passConversionVeto_ = !ConversionTools::hasMatchedConversion(el,convs_,
                                                         thebs_->position());
  }else{
    //printf("\n\nERROR!!! conversions not found!!!\n");
  }

  return (fabs(dEtaIn_) < dEtaIn\
          && fabs(dPhiIn_) < dPhiIn\
          && full5x5_sigmaIetaIeta_ < full5x5_sigmaIetaIeta\
          && hOverE_ < hOverE\
          && fabs(d0_) < d0\
          && fabs(dz_) < dz\
          && fabs(ooEmooP_) < ooEmooP\
          && relIsoWithDBeta_ < relIsoWithDBeta\
          && passConversionVeto_\
          && expectedMissingInnerHits_ < expectedMissingInnerHits);

}

// define plugin
DEFINE_FWK_MODULE(MiniAODElectronIDEmbedder);
