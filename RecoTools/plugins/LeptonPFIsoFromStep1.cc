#include <memory>
#include "Math/VectorUtil.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "TMath.h"

class LeptonPFIsoFromStep1 : public edm::EDProducer {
public:
  explicit LeptonPFIsoFromStep1(const edm::ParameterSet&);
  ~LeptonPFIsoFromStep1();

private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  edm::InputTag leptonLabel_;
  StringCutObjectSelector<reco::Candidate> endcapDefinition_;
  edm::InputTag pfLabel_;
  StringCutObjectSelector<reco::Candidate> pfSelection_;
  double deltaR_, deltaRself_, deltaZ_;
  double directional_;
  double vetoConeEndcaps_;
  bool   debug_;

};



LeptonPFIsoFromStep1::LeptonPFIsoFromStep1(const edm::ParameterSet& iConfig) :
  leptonLabel_(iConfig.getParameter<edm::InputTag>("leptonLabel")),
  endcapDefinition_(iConfig.existsAs<std::string>("endcapDefinition") ? iConfig.getParameter<std::string>("endcapDefinition") : "abs(eta) > 1.479", true),
  pfLabel_(iConfig.getParameter<edm::InputTag>("pfLabel")),
  pfSelection_(iConfig.getParameter<std::string>("pfSelection"), true),
  deltaR_(iConfig.getParameter<double>("deltaR")),
  deltaRself_(iConfig.getParameter<double>("deltaRself")),
  deltaZ_(iConfig.existsAs<double>("deltaZ") ? iConfig.getParameter<double>("deltaZ") : 0),
  directional_(iConfig.getParameter<bool>("directional")),
  vetoConeEndcaps_(iConfig.getParameter<double>("vetoConeEndcaps")),
  debug_(iConfig.getUntrackedParameter<bool>("debug",false))
{
  produces<edm::ValueMap<float> >().setBranchAlias("pfMuIso");
}

void LeptonPFIsoFromStep1::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  edm::Handle<reco::CandidateView> muH;
  iEvent.getByLabel(leptonLabel_,muH);

  edm::Handle<reco::CandidateView> pfH;
  iEvent.getByLabel(pfLabel_,pfH);

  std::vector<float> isoV;
  std::unique_ptr<edm::ValueMap<float> > isoM(new edm::ValueMap<float> ());
  edm::ValueMap<float>::Filler isoF(*isoM);

  if (debug_) std::cout << "Run " << iEvent.id().run() << ", Event " << iEvent.id().event() << std::endl;

  for(size_t i=0, n = muH->size(); i < n; ++i) {
    const reco::Candidate &mu = muH->at(i);
    if (debug_) std::cout << leptonLabel_.encode() << " with pt = " << mu.pt() << ", eta = " << mu.eta() << ", phi = " << mu.phi() << std::endl;

//     Double_t zLepton = 0.0;
//     if(mu.track().isNonnull()) zLepton = mu.track()->dz(vtxH->at(0).position());

    Double_t ptSum =0.;  
    math::XYZVector isoAngleSum;
    std::vector<math::XYZVector> coneParticles;

    for (size_t j=0; j<pfH->size();j++) {   
      const reco::Candidate &pf = pfH->at(j);

      double dr = deltaR(pf, mu) ;
      if (dr >= deltaR_) continue;
        
      if (!pfSelection_(pf)) continue; 

      if (debug_) std::cout << "   pfCandidate of pdgId " << pf.pdgId() << ", pt = " << pf.pt() << ", dr = " << dr << ", dz = " << (pf.vz() - mu.vz()) << " is in cone... " << std::endl;

      if (deltaZ_ > 0 && fabs(pf.vz() - mu.vz()) > deltaZ_) continue;

      if (deltaR(pf, mu) < deltaRself_) continue;

      // dR Veto for Gamma: no-one in EB, dR > 0.08 in EE
      if (vetoConeEndcaps_ > 0 && endcapDefinition_(mu) && dr < vetoConeEndcaps_) continue;

      if (debug_) std::cout << "          ...and passes all vetos, so it's added to the sum." << std::endl;
      // scalar sum
      ptSum += pf.pt();

      // directional sum
      math::XYZVector transverse( pf.eta() - mu.eta()
              , reco::deltaPhi(pf.phi(), mu.phi())
              , 0);
      transverse *= pf.pt() / transverse.rho();
      if (transverse.rho() > 0) {
          isoAngleSum += transverse;
          coneParticles.push_back(transverse);
      }

    }
    if (directional_) {
      double directionalPT = 0;
      for (unsigned int iPtcl = 0; iPtcl < coneParticles.size(); ++iPtcl)
        directionalPT += pow(TMath::ACos( coneParticles[iPtcl].Dot(isoAngleSum) / coneParticles[iPtcl].rho() / isoAngleSum.rho() ),2) * coneParticles[iPtcl].rho();
      isoV.push_back(directionalPT);
    } else isoV.push_back(ptSum);
  }

  isoF.insert(muH,isoV.begin(),isoV.end());

  isoF.fill();
  iEvent.put(std::move(isoM));

}

LeptonPFIsoFromStep1::~LeptonPFIsoFromStep1() { }
void LeptonPFIsoFromStep1::beginJob() { }
void LeptonPFIsoFromStep1::endJob() { }
DEFINE_FWK_MODULE(LeptonPFIsoFromStep1);

