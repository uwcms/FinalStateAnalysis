#ifdef HZZMELA // This should only be compiled if we actually want ME stuff

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODHZZCategoryEmbedder.cc                                          //
//                                                                          //
//   Finds the category of a 4l event based on the 2015 HZZ4l group	    //
//       rules and embeds it as a userFloat.				    //
//                                                                          //
//   Author: Nate Woods, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>
#include <unordered_map>
#include <utility> // contains std::pair

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"

// FSA includes
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"


class MiniAODHZZCategoryEmbedder : public edm::EDProducer {
 public:
  MiniAODHZZCategoryEmbedder(const edm::ParameterSet& pset);
  virtual ~MiniAODHZZCategoryEmbedder(){}
 private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Calculate the matrix element for fs under process hypothesis proc using calculator calc
  const unsigned int getHZZCategory(const PATFinalState& fs) const;

  // helper functions for use in getHZZCategory()
  // each assumes that the earlier categories have already been checked
  const bool isVBFTagged(const PATFinalState& fs) const;
  const bool isVHHadronicTagged(const PATFinalState& fs) const;
  const bool isVHLeptonicTagged(const PATFinalState& fs) const;
  const bool isTTHTagged(const PATFinalState& fs) const;
  const bool isHZZ1JetTagged(const PATFinalState& fs) const;
  // several of these need to check jet B tags
  bool isHZZBTagged(const pat::Jet& j) const;

  // Tag of final state collection
  edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;

  // Cut string to select tight leptons
  const std::string tightLepCut_;

  // B discriminator to use
  const std::string bDiscrimLabel_;

  // B discriminator cut
  const float bDiscrimCut_;
};


MiniAODHZZCategoryEmbedder::MiniAODHZZCategoryEmbedder(const edm::ParameterSet& iConfig) :
  srcToken_(consumes<edm::View<PATFinalState> >(iConfig.exists("src") ?
       iConfig.getParameter<edm::InputTag>("src") :
       edm::InputTag("finalStateeeee"))),
  tightLepCut_(iConfig.exists("tightLepCut") ?
	       iConfig.getParameter<std::string>("tightLepCut") :
	       std::string("userFloat(\"HZZ4lIDPassTight\") > 0.5 && userFloat(\"HZZ4lIsoPass\") > 0.5")),
  bDiscrimLabel_(iConfig.exists("bDiscriminator") ?
		 iConfig.getParameter<std::string>("bDiscriminator") :
		 std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags")),
  bDiscrimCut_(iConfig.exists("bDiscriminatorCut") ?
	       iConfig.getParameter<double>("bDiscriminatorCut") :
	       0.814)
{
  produces<PATFinalStateCollection>();
}


void MiniAODHZZCategoryEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  std::auto_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesIn;
  iEvent.getByToken(srcToken_, finalStatesIn);

  for (size_t iFS = 0; iFS < finalStatesIn->size(); ++iFS) 
    {
      PATFinalState* embedInto = finalStatesIn->ptrAt(iFS)->clone();

      const int cat = getHZZCategory(*embedInto); // meow

      embedInto->addUserFloat("HZZCategory", float(cat));

      output->push_back(embedInto); // takes ownership
    }

  iEvent.put(output);
}


// Get the event category for the 2015 H->ZZ->4l analysis
const unsigned int MiniAODHZZCategoryEmbedder::getHZZCategory(const PATFinalState& fs) const
{
  if(fs.numberOfDaughters() != 4)
    return 999;

  if(isVBFTagged(fs))
    return 2;

  if(isVHHadronicTagged(fs))
    return 4;

  if(isVHLeptonicTagged(fs))
    return 3;

  if(isTTHTagged(fs))
    return 5;

  if(isHZZ1JetTagged(fs))
    return 1;

  return 0;
}


// helper functions for use in getHZZCategory()
// each assumes that the earlier categories have already been checked
const bool MiniAODHZZCategoryEmbedder::isVBFTagged(const PATFinalState& fs) const
{
  // at least 2 jets
  if(fs.evt()->jets().size() < 2)
    return false;

  // at most one B-tagged jet
  uint nBTags = 0;
  for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
    {
      if(isHZZBTagged(fs.evt()->jets().at(j)))
        {
          nBTags++;
          if(nBTags > 1)
            return false;
        }
    }
  
  // Fisher discriminant > 0.5
  float D_jet = 0.18 * fabs(fs.evt()->jets().at(0).eta() - fs.evt()->jets().at(1).eta()) +
    0.000192 * fs.dijetMass(0,1);
  if(D_jet < 0.5)
    return false;

  // exactly 4 leptons
  if(fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0)
    return false;

  return true;
}

const bool MiniAODHZZCategoryEmbedder::isVHHadronicTagged(const PATFinalState& fs) const
{
  // all possibilities require at least 2 jets
  if(fs.evt()->jets().size() < 2)
    return false;

  // exactly 2 b-tagged jets
  bool twoBs = fs.evt()->jets().size() == 2;
  for(size_t j = 0; j < 2 && twoBs; ++j)
    twoBs &= isHZZBTagged(fs.evt()->jets().at(j));
  
  // OR at least 2 jets with |eta|<2.4, pt>40, 60<m_jj<120; and 4lpT>4lmass
  bool vJets = false;
  if(!twoBs)
    {
      for(size_t ijet = 0; ijet < fs.evt()->jets().size()-1 && !vJets; ++ijet) // safe because of 2 jet requirement
        {
          pat::Jet j1 = fs.evt()->jets().at(ijet);
          if(fabs(j1.eta()) > 2.4 || j1.pt() < 40.)
            continue;

          for(size_t jjet = ijet+1; jjet < fs.evt()->jets().size() && !vJets; ++jjet)
            {
              pat::Jet j2 = fs.evt()->jets().at(jjet);
              if(fabs(j2.eta()) > 2.4 || j2.pt() < 40.)
                continue;

              float mjj = (j1.p4() + j2.p4()).M();
              vJets |= (mjj > 60. && mjj < 120);
            }
        }
    }
  vJets &= (fs.mass() < fs.pt());

  if(! (twoBs || vJets))
    return false;

  // and exactly 4 leptons
  if(fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0)
    return false;

  return true;
}

const bool MiniAODHZZCategoryEmbedder::isVHLeptonicTagged(const PATFinalState& fs) const
{
  // no more than 2 jets
  if(fs.evt()->jets().size() > 2)
    return false;
  
  // no B-tagged jets
  for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
    if(isHZZBTagged(fs.evt()->jets().at(j)))
      return false;

  // at least 5 leptons
  return (fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0);
}

const bool MiniAODHZZCategoryEmbedder::isTTHTagged(const PATFinalState& fs) const
{
  // at least 3 jets, at least one of which is B tagged
  bool threeJ = (fs.evt()->jets().size() >= 3);
  bool oneB = false;
  if(threeJ)
    {
      for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
	{
	  if(isHZZBTagged(fs.evt()->jets().at(j)))
	    {
	      oneB = true;
	      break;
	    }
	}
    }
  
  if(threeJ && oneB)
    return true;

  // OR at least 5 leptons
  return (fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0);
}

const bool MiniAODHZZCategoryEmbedder::isHZZ1JetTagged(const PATFinalState& fs) const
{
  // at least 1 jet
  return bool(fs.evt()->jets().size());
}


bool MiniAODHZZCategoryEmbedder::isHZZBTagged(const pat::Jet& j) const
{
  return (j.bDiscriminator(bDiscrimLabel_) > bDiscrimCut_);
}



void MiniAODHZZCategoryEmbedder::beginJob(){}
void MiniAODHZZCategoryEmbedder::endJob(){}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODHZZCategoryEmbedder);



#endif // #ifdef HZZMELA
