/** \class PATJetSmearEmbedder
 *
 * Based on PhysicsTools/PatUtils/interface/SmearedJetProducerT.h
 *
 * Produce collection of "smeared" jets.
 * The aim of this correction is to account for the difference in jet energy resolution
 * between Monte Carlo simulation and Data.
 * The jet energy resolutions have been measured in QCD di-jet and gamma + jets events selected in 2010 data,
 * as documented in the PAS JME-10-014.
 *
 * \author Christian Veelken, LLR
 *
 * \version $Revision: 1.3 $
 *
 * $Id: SmearedJetProducerT.h,v 1.3 2011/11/01 14:11:55 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <TMath.h>
#include <TFile.h>
#include <TH2.h>

namespace {
  template <typename T>
  class GenJetMatcherT
  {
    public:

     GenJetMatcherT(const edm::ParameterSet& cfg)
       : srcGenJets_(cfg.getParameter<edm::InputTag>("srcGenJets")),
         dRmaxGenJetMatch_(cfg.getParameter<double>("dRmaxGenJetMatch"))
     {}
     ~GenJetMatcherT() {}

     const reco::GenJet* operator()(const T& jet, edm::Event* evt = 0) const
     {
       assert(evt);

       edm::Handle<reco::GenJetCollection> genJets;
       evt->getByLabel(srcGenJets_, genJets);

       const reco::GenJet* retVal = 0;

       double dRbestMatch = dRmaxGenJetMatch_;
       for ( reco::GenJetCollection::const_iterator genJet = genJets->begin();
	     genJet != genJets->end(); ++genJet ) {
	 double dR = deltaR(jet.p4(), genJet->p4());
	 if ( dR < dRbestMatch ) {
	   retVal = &(*genJet);
	   dRbestMatch = dR;
	 }
       }

       return retVal;
     }

    private:

//--- configuration parameter
     edm::InputTag srcGenJets_;

     double dRmaxGenJetMatch_;
  };
}

class PATJetSmearEmbedder : public edm::EDProducer
{
  typedef pat::JetCollection JetCollection;
  typedef pat::Jet T;
  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef reco::CandidatePtr CandidatePtr;
  typedef reco::Candidate::LorentzVector LorentzVector;

 public:

  explicit PATJetSmearEmbedder(const edm::ParameterSet& cfg)
    : moduleLabel_(cfg.getParameter<std::string>("@module_label")),
      genJetMatcher_(cfg)
  {
    src_ = cfg.getParameter<edm::InputTag>("src");

    edm::FileInPath inputFileName = cfg.getParameter<edm::FileInPath>("inputFileName");
    std::string lutName = cfg.getParameter<std::string>("lutName");
    if ( inputFileName.location() != edm::FileInPath::Local )
      throw cms::Exception("JetMETsmearInputProducer")
        << " Failed to find File = " << inputFileName << " !!\n";

    inputFile_ = new TFile(inputFileName.fullPath().data());
    lut_ = dynamic_cast<TH2*>(inputFile_->Get(lutName.data()));
    if ( !lut_ )
      throw cms::Exception("SmearedJetProducer")
        << " Failed to load LUT = " << lutName.data() << " from file = " << inputFileName.fullPath().data() << " !!\n";

    smearBy_ = ( cfg.exists("smearBy") ) ? cfg.getParameter<double>("smearBy") : 1.0;


    produces<ShiftedCandCollection>("smearedCands");
    produces<ShiftedCandCollection>("smearUpCands");
    produces<ShiftedCandCollection>("smearDownCands");
    produces<JetCollection>();
  }
  ~PATJetSmearEmbedder()
  {
    // nothing to be done yet...
  }

 private:

  virtual void produce(edm::Event& evt, const edm::EventSetup& es)
  {
    //std::cout << "<SmearedJetProducer::produce>:" << std::endl;
    //std::cout << " moduleLabel = " << moduleLabel_ << std::endl;

    std::unique_ptr<JetCollection> outputJets(new JetCollection);

    std::unique_ptr<ShiftedCandCollection> smearedCands(new ShiftedCandCollection);
    std::unique_ptr<ShiftedCandCollection> smearUpCands(new ShiftedCandCollection);
    std::unique_ptr<ShiftedCandCollection> smearDownCands(new ShiftedCandCollection);

    edm::Handle<JetCollection> jets;
    evt.getByLabel(src_, jets);

    for (JetCollection::const_iterator jet = jets->begin();
	  jet != jets->end(); ++jet ) {
      reco::Candidate::LorentzVector jetP4 = jet->p4();

      T outputJet = (*jet);

      reco::Candidate::LorentzVector smearedP4 = jetP4;
      reco::Candidate::LorentzVector smearUpP4 = jetP4;
      reco::Candidate::LorentzVector smearDownP4 = jetP4;

      ShiftedCand smearedCand = outputJet;
      ShiftedCand smearUpCand = outputJet;
      ShiftedCand smearDownCand = outputJet;

      // Only smear MC
      if (!evt.isRealData()) {
        const reco::GenJet* genJet = genJetMatcher_(*jet, &evt);
        if ( genJet ) {
          int binIndex = lut_->FindBin(TMath::Abs(jetP4.eta()), jetP4.pt());
          double smearFactor = lut_->GetBinContent(binIndex);
          double smearFactorErr = lut_->GetBinError(binIndex);

          smearFactor = TMath::Power(smearFactor, smearBy_);

          smearedP4 = jet->p4() - genJet->p4();
          smearedP4 *= smearFactor;
          smearedP4 += genJet->p4();

          double smearFactorUp = smearFactor + 3*smearFactorErr;
          smearUpP4 = jet->p4() - genJet->p4();
          smearUpP4 *= smearFactorUp;
          smearUpP4 += genJet->p4();

          double smearFactorDown = smearFactor - 3*smearFactorErr;
          smearDownP4 = jet->p4() - genJet->p4();
          smearDownP4 *= smearFactorDown;
          smearDownP4 += genJet->p4();

        }
      }
      outputJets->push_back(outputJet);

      smearedCand.setP4(smearedP4);
      smearUpCand.setP4(smearUpP4);
      smearDownCand.setP4(smearDownP4);

      smearedCands->push_back(smearedCand);
      smearUpCands->push_back(smearUpCand);
      smearDownCands->push_back(smearDownCand);
    }

    typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
      PutHandle smearedCandsH = evt.put(std::move(smearedCands), "smearedCands");
      PutHandle smearUpCandsH = evt.put(std::move(smearUpCands), "smearUpCands");
      PutHandle smearDownCandsH = evt.put(std::move(smearDownCands), "smearDownCands");

    //--- add collection of "smeared" jets to the event
    for (size_t i = 0; i < outputJets->size(); ++i) {
      pat::Jet& jet = outputJets->at(i);
      jet.addUserCand("smeared", CandidatePtr(smearedCandsH, i));
      jet.addUserCand("smear+", CandidatePtr(smearUpCandsH, i));
      jet.addUserCand("smear-", CandidatePtr(smearDownCandsH, i));
    }
      evt.put(std::move(outputJets));
  }

  std::string moduleLabel_;

  GenJetMatcherT<T> genJetMatcher_;

//--- configuration parameters

  // collection of pat::Jets (with L2L3/L2L3Residual corrections applied)
  edm::InputTag src_;

  TFile* inputFile_;
  TH2* lut_;

  double smearBy_; // option to "smear" jet energy by N standard-deviations, useful for template morphing

};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetSmearEmbedder);
