#include "FinalStateAnalysis/RecoTools/interface/PFMEtSignInterface.h"

#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <TMath.h>
#include <TVectorD.h>

PFMEtSignInterface::PFMEtSignInterface(const edm::ParameterSet& cfg)
  : PFMEtSignInterfaceBase(cfg.getParameter<edm::ParameterSet>("resolution"))
{
  srcPFJets_ = cfg.getParameter<edm::InputTag>("srcPFJets");
  srcPFCandidates_ = cfg.getParameter<edm::InputTag>("srcPFCandidates");

  dRoverlapPFJet_ = cfg.getParameter<double>("dRoverlapPFJet");
  dRoverlapPFCandidate_ = cfg.getParameter<double>("dRoverlapPFCandidate");

  verbosity_ = cfg.exists("verbosity") ?
    cfg.getParameter<int>("verbosity") : 0;
}

PFMEtSignInterface::~PFMEtSignInterface()
{
// nothing to be done yet...
}

template <typename T>
std::list<const T*> makeList(const std::vector<T>& collection)
{
  std::list<const T*> retVal;

  for ( typename std::vector<T>::const_iterator object = collection.begin();
	object != collection.end(); ++object ) {
    retVal.push_back(&(*object));
  }

  return retVal;
}

template <typename T>
void removePFCandidateOverlaps(std::list<const reco::PFCandidate*>& pfCandidates,
			       const std::list<const T*>& objectsNotToBeFiltered, double dRoverlap)
{
  std::list<const reco::PFCandidate*>::iterator pfCandidate = pfCandidates.begin();
  while ( pfCandidate != pfCandidates.end() ) {
    bool isOverlap = false;
    for ( typename std::list<const T*>::const_iterator objectNotToBeFiltered = objectsNotToBeFiltered.begin();
	  objectNotToBeFiltered != objectsNotToBeFiltered.end() && !isOverlap; ++objectNotToBeFiltered ) {
      if ( deltaR((*pfCandidate)->p4(), (*objectNotToBeFiltered)->p4()) < dRoverlap ) isOverlap = true;
    }

    if ( isOverlap ) pfCandidate = pfCandidates.erase(pfCandidate);
    else ++pfCandidate;
  }
}

void PFMEtSignInterface::beginEvent(const edm::Event& evt, const edm::EventSetup& es)
{
  edm::Handle<reco::PFJetCollection> pfJets;
  evt.getByLabel(srcPFJets_, pfJets);
  pfJetList_ = makeList<reco::PFJet>(*pfJets);

  edm::Handle<reco::PFCandidateCollection> pfCandidates;
  evt.getByLabel(srcPFCandidates_, pfCandidates);
  pfCandidateList_ = makeList<reco::PFCandidate>(*pfCandidates);

  std::list<const reco::PFCandidate*> pfJetConstituentList;
  for ( std::list<const reco::PFJet*>::const_iterator pfJet = pfJetList_.begin();
	pfJet != pfJetList_.end(); ++pfJet ) {
    const std::vector<reco::PFCandidatePtr> pfJetConstituents = (*pfJet)->getPFConstituents();
    for ( std::vector<reco::PFCandidatePtr>::const_iterator pfJetConstituent = pfJetConstituents.begin();
	  pfJetConstituent != pfJetConstituents.end(); ++pfJetConstituent ) {
      pfJetConstituentList.push_back(pfJetConstituent->get());
    }
  }

  removePFCandidateOverlaps(pfCandidateList_, pfJetConstituentList, dRoverlapPFCandidate_);
}

template <typename T>
void removePFJetOverlaps(std::list<const reco::PFJet*>& pfJets,
			 const std::list<const T*>& objectsNotToBeFiltered, double dRoverlapPFJet, double dRoverlapPFCandidate)
{
  std::list<const reco::PFJet*>::iterator pfJet = pfJets.begin();
  while ( pfJet != pfJets.end() ) {
    bool isOverlap = false;
    for ( typename std::list<const T*>::const_iterator objectNotToBeFiltered = objectsNotToBeFiltered.begin();
	  objectNotToBeFiltered != objectsNotToBeFiltered.end() && !isOverlap; ++objectNotToBeFiltered ) {
      if ( deltaR((*pfJet)->p4(), (*objectNotToBeFiltered)->p4()) < dRoverlapPFJet ) isOverlap = true;
    }

    const reco::Jet::Constituents pfJetConstituents = (*pfJet)->getJetConstituents();
    for ( reco::Jet::Constituents::const_iterator pfJetConstituent = pfJetConstituents.begin();
	  pfJetConstituent != pfJetConstituents.end() && !isOverlap; ++pfJetConstituent ) {
      for ( typename std::list<const T*>::const_iterator objectNotToBeFiltered = objectsNotToBeFiltered.begin();
	    objectNotToBeFiltered != objectsNotToBeFiltered.end(); ++objectNotToBeFiltered ) {
	if ( deltaR((*pfJetConstituent)->p4(), (*objectNotToBeFiltered)->p4()) < dRoverlapPFCandidate ) isOverlap = true;
      }
    }

    if ( isOverlap ) pfJet = pfJets.erase(pfJet);
    else ++pfJet;
  }
}

TMatrixD PFMEtSignInterface::operator()(const std::list<const reco::Candidate*>& patLeptonList) const
{
  if ( this->verbosity_ ) std::cout << "<PFMEtSignInterface::operator()>:" << std::endl;

  std::list<const reco::PFJet*> pfJetList_hypothesis = pfJetList_;
  removePFJetOverlaps(pfJetList_hypothesis, patLeptonList, dRoverlapPFJet_, dRoverlapPFCandidate_);

  std::list<const reco::PFCandidate*> pfCandidateList_hypothesis = pfCandidateList_;
  removePFCandidateOverlaps(pfCandidateList_hypothesis, patLeptonList, dRoverlapPFCandidate_);

  std::vector<metsig::SigInputObj> pfMEtSignObjects;
  addPFMEtSignObjects(pfMEtSignObjects, patLeptonList);
  addPFMEtSignObjects(pfMEtSignObjects, pfJetList_hypothesis);
  addPFMEtSignObjects(pfMEtSignObjects, pfCandidateList_hypothesis);

  return PFMEtSignInterfaceBase::operator()(pfMEtSignObjects);
}
