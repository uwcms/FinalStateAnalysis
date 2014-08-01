//
// $Id: PATPFParticleProducerUser.h,v 1.8 2012/05/26 10:42:53 gpetrucc Exp $
//

#ifndef UWAnalysis_RecoTools_PATPFPaticleProducerUser_h
#define UWAnalysis_RecoTools_PATPFPaticleProducerUser_h

/**
  \class    pat::PATPFParticleProducerUser PATPFParticleProducerUser.h "PhysicsTools/PatAlgos/interface/PATPFParticleProducerUser.h"
  \brief    Produces pat::PFParticle's

   The PATPFParticleProducerUser produces analysis-level pat::PFParticle's starting from
   a collection of objects of reco::PFCandidate.

  \author   Steven Lowette, Roger Wolf
  \version  $Id: PATPFParticleProducerUser.h,v 1.8 2012/05/26 10:42:53 gpetrucc Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "CommonTools/Utils/interface/PtComparator.h"

#include "DataFormats/PatCandidates/interface/PFParticle.h"

#include "PhysicsTools/PatAlgos/interface/MultiIsolator.h"
#include "PhysicsTools/PatAlgos/interface/EfficiencyLoader.h"
#include "PhysicsTools/PatAlgos/interface/KinResolutionsLoader.h"

#include "DataFormats/PatCandidates/interface/UserData.h"
#include "PhysicsTools/PatAlgos/interface/PATUserDataHelper.h"

#include <string>


namespace pat {

  class LeptonLRCalc;

  class PATPFParticleProducerUser : public edm::EDProducer {

    public:

      explicit PATPFParticleProducerUser(const edm::ParameterSet & iConfig);
      ~PATPFParticleProducerUser();

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

    private:
      void 
    fetchCandidateCollection(edm::Handle< edm::View<reco::PFCandidate> >& c, 
                 const edm::InputTag& tag, 
                 const edm::Event& iSetup) const;

      // configurables
      edm::InputTag pfCandidateSrc_;
      bool          embedPFCandidate_;
      bool          addGenMatch_;
      bool          embedGenMatch_;
      std::vector<edm::InputTag> genMatchSrc_;
      // tools
      GreaterByPt<PFParticle>      pTComparator_;

      bool addEfficiencies_;
      pat::helper::EfficiencyLoader efficiencyLoader_;
      
      bool addResolutions_;
      pat::helper::KinResolutionsLoader resolutionLoader_;

      bool useUserData_;
      pat::PATUserDataHelper<pat::PFParticle> userDataHelper_;

 
  };


}

#endif
