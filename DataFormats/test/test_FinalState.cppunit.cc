/*
 * Test the PATFinalState object
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>
#include <vector>

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiLeptonFinalStates.h"
#include "FinalStateAnalysis/DataFormats/interface/PATTriLeptonFinalStates.h"

#include "DataFormats/Math/interface/Vector3D.h"

#include "DataFormats/Common/interface/EDProductGetter.h"
#include "DataFormats/Common/interface/OrphanHandle.h"
#include "DataFormats/Common/interface/Wrapper.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/MET.h"

using namespace edm;

class testFinalState: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testFinalState);
  CPPUNIT_TEST(checkSetup);
  CPPUNIT_TEST(testDiLepton);
  CPPUNIT_TEST(testTriLepton);
  CPPUNIT_TEST(testOverlaps);
  CPPUNIT_TEST(testIndexGetter);
  CPPUNIT_TEST_SUITE_END();
  public:
    void setUp();
    void tearDown(){}

    void checkSetup();

    void testDiLepton();
    void testTriLepton();
    void testOverlaps();
    void testIndexGetter();

    ProductID electronPID;
    std::vector<pat::Electron> mockElectronColl_;
    edm::Ptr<pat::Electron> mockElectronPtr_;

    ProductID muonPID;
    std::vector<pat::Muon> mockMuonColl_;
    edm::Ptr<pat::Muon> mockMuonPtr1_;
    edm::Ptr<pat::Muon> mockMuonPtr2_;

    ProductID userCandPID;
    std::vector<reco::LeafCandidate> mockUserCandColl_;
    edm::Ptr<reco::LeafCandidate> mockUserCandPtr1_;
    edm::Ptr<reco::LeafCandidate> mockUserCandPtr2_;

    ProductID metPID;
    std::vector<pat::MET> mockMETColl_;
    edm::Ptr<pat::MET> mockMETPtr_;

    ProductID eventPID;
    std::vector<PATFinalStateEvent> mockEventColl_;
    edm::Ptr<PATFinalStateEvent> mockEventPtr_;

    edm::Ptr<reco::Vertex> nullVtx_;

    ProductID jetPID;
    std::vector<reco::LeafCandidate> mockJetColl_;
    edm::PtrVector<reco::LeafCandidate> mockJetEdmPtrVector_;
    std::vector<edm::Ptr<reco::Candidate> > mockJetPtrVector_;
};

void testFinalState::setUp() {
  // fake electron @ phi = 0 eta = 0, pt = 10
  pat::Electron electron;
  electron.setCharge(1);
  electron.setPdgId(1);
  electron.setP4(math::PtEtaPhiMLorentzVector(10, 0, 0, 0));
  mockElectronColl_.push_back(electron);
  electronPID = ProductID(1,1);
  TestHandle<std::vector<pat::Electron> > elecHandle(&mockElectronColl_, electronPID);
  mockElectronPtr_ = Ptr<pat::Electron>(elecHandle, 0);

  reco::LeafCandidate userCand1;
  userCand1.setCharge(-1);
  userCand1.setP4(math::PtEtaPhiMLorentzVector(15, 1, 1, 0));
  mockUserCandColl_.push_back(userCand1);

  reco::LeafCandidate userCand2;
  userCand2.setCharge(-1);
  userCand2.setP4(math::PtEtaPhiMLorentzVector(15, 1, -1, 0));
  mockUserCandColl_.push_back(userCand2);

  userCandPID = ProductID(1,3);
  TestHandle<std::vector<reco::LeafCandidate> > userHandle(&mockUserCandColl_, userCandPID);
  mockUserCandPtr1_ = Ptr<reco::LeafCandidate>(userHandle, 0);
  mockUserCandPtr2_ = Ptr<reco::LeafCandidate>(userHandle, 1);

  mockElectronColl_[0].addUserCand("aUserCand1", mockUserCandPtr1_);

  pat::Muon muon;
  muon.setCharge(-1);
  muon.setPdgId(-2);
  muon.setP4(math::PtEtaPhiMLorentzVector(11, 1, 0, 0));
  muon.addUserCand("aUserCand2", mockUserCandPtr2_);
  mockMuonColl_.push_back(muon);
  pat::Muon muon2(muon);
  muon2.setP4(math::PtEtaPhiMLorentzVector(12, -1, 0, 0));
  mockMuonColl_.push_back(muon2);

  muonPID = ProductID(1,2);
  TestHandle<std::vector<pat::Muon> > muonHandle(&mockMuonColl_, muonPID);
  mockMuonPtr1_ = Ptr<pat::Muon>(muonHandle, 0);
  mockMuonPtr2_ = Ptr<pat::Muon>(muonHandle, 1);

  metPID = ProductID(1,3);
  pat::MET met;
  met.setP4(math::PtEtaPhiMLorentzVector(20, 0, -1, 0));
  mockMETColl_.push_back(met);
  TestHandle<std::vector<pat::MET> > metHandle(&mockMETColl_, metPID);
  mockMETPtr_ = Ptr<pat::MET>(metHandle, 0);

  PATFinalStateEvent mockEvent(nullVtx_, mockMETPtr_);
  mockEventColl_.push_back(mockEvent);
  TestHandle<std::vector<PATFinalStateEvent> > eventHandle(&mockEventColl_, eventPID);
  mockEventPtr_ = Ptr<PATFinalStateEvent>(eventHandle, 0);

  for (size_t i = 10; i < 100; i += 10) {
    reco::LeafCandidate cand;
    cand.setP4(math::PtEtaPhiMLorentzVector(i, 0, 0, 0));
    mockJetColl_.push_back(cand);
  }
  jetPID = ProductID(1, 4);
  TestHandle<std::vector<reco::LeafCandidate> > jetHandle(&mockJetColl_, jetPID);
  for (size_t i = 0; i < mockJetColl_.size(); ++i) {
    mockJetEdmPtrVector_.push_back(Ptr<reco::LeafCandidate>(jetHandle, i));
    mockJetPtrVector_.push_back(Ptr<reco::Candidate>(jetHandle, i));
  }
}

void testFinalState::checkSetup() {
  // check things are set up okay
  CPPUNIT_ASSERT(mockElectronPtr_.isAvailable());
  CPPUNIT_ASSERT(mockElectronPtr_.isNonnull());
  CPPUNIT_ASSERT(mockElectronPtr_.get() == &mockElectronColl_[0]);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockElectronPtr_->eta(), 0, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockElectronPtr_->phi(), 0, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockElectronPtr_->pt(), 10, 1e-6);
  CPPUNIT_ASSERT(mockElectronPtr_->hasUserCand("aUserCand1"));

  CPPUNIT_ASSERT(mockMuonPtr1_.isAvailable());
  CPPUNIT_ASSERT(mockMuonPtr1_.isNonnull());
  CPPUNIT_ASSERT(mockMuonPtr1_.get() == &mockMuonColl_[0]);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr1_->eta(), 1, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr1_->phi(), 0, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr1_->pt(), 11, 1e-6);
  CPPUNIT_ASSERT(mockMuonPtr1_->hasUserCand("aUserCand2"));
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr1_->userCand("aUserCand2")->pt(), 15, 1e-6);

  CPPUNIT_ASSERT(mockMuonPtr2_.isAvailable());
  CPPUNIT_ASSERT(mockMuonPtr2_.isNonnull());
  CPPUNIT_ASSERT(mockMuonPtr2_.get() == &mockMuonColl_[1]);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr2_->eta(), -1, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr2_->phi(), 0, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr2_->pt(), 12, 1e-6);
  CPPUNIT_ASSERT(mockMuonPtr2_->hasUserCand("aUserCand2"));
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMuonPtr2_->userCand("aUserCand2")->pt(), 15, 1e-6);

  CPPUNIT_ASSERT(mockMETPtr_.isAvailable());
  CPPUNIT_ASSERT(mockMETPtr_.isNonnull());
  CPPUNIT_ASSERT(mockMETPtr_.get() == &mockMETColl_[0]);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMETPtr_->eta(), 0, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMETPtr_->phi(), -1, 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(mockMETPtr_->pt(), 20, 1e-6);
}

void testFinalState::testDiLepton() {
  edm::Ptr<reco::Vertex> nullVtx_;


  // Explicitly check that all the methods are const
  const PATElecMuFinalState finalState(mockElectronPtr_, mockMuonPtr1_,
      mockEventPtr_);

  // Check charge defintion
  CPPUNIT_ASSERT(finalState.charge() == 0);

  // Check p4 definition
  reco::Candidate::LorentzVector expectP4 = mockElectronPtr_->p4() + mockMuonPtr1_->p4();
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.pt(), expectP4.pt(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.phi(), expectP4.phi(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.eta(), expectP4.eta(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.mass(), expectP4.mass(), 1e-6);

  // Check assignment of variables
  CPPUNIT_ASSERT(finalState.met() == mockMETPtr_);
  CPPUNIT_ASSERT(finalState.vertexObject() == nullVtx_);

  // Check daughter getters via ptr
  CPPUNIT_ASSERT(finalState.daughter(0) == mockElectronPtr_.get());
  CPPUNIT_ASSERT(finalState.daughter(1) == mockMuonPtr1_.get());
  CPPUNIT_ASSERT(finalState.numberOfDaughters() == 2);

  // Check undefined daughter throws
  CPPUNIT_ASSERT_THROW(finalState.daughter(2), cms::Exception);

  // Getters of Ptrs
  CPPUNIT_ASSERT(finalState.daughterPtr(0) == reco::CandidatePtr(mockElectronPtr_));
  CPPUNIT_ASSERT(finalState.daughterPtr(1) == reco::CandidatePtr(mockMuonPtr1_));
  // Check undefined daughter throws
  CPPUNIT_ASSERT_THROW(finalState.daughterPtr(2), cms::Exception);
  CPPUNIT_ASSERT_THROW(finalState.daughterPtr(-2), cms::Exception);

  std::vector<const reco::Candidate*> theDaughters = finalState.daughters();
  CPPUNIT_ASSERT(theDaughters[0] == mockElectronPtr_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockMuonPtr1_.get());

  // Check ability to get arbitrary systags
  theDaughters = finalState.daughters("aUserCand1,aUserCand2");
  CPPUNIT_ASSERT(theDaughters[0] == mockUserCandPtr1_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockUserCandPtr2_.get());

  // Check syntax for ommitting daughters
  theDaughters = finalState.daughters("#,aUserCand2");
  CPPUNIT_ASSERT(theDaughters.size() == 1);
  CPPUNIT_ASSERT(theDaughters[0] == mockUserCandPtr2_.get());

  // Check syntax for including daughters
  theDaughters = finalState.daughters("@,aUserCand2");
  CPPUNIT_ASSERT(theDaughters.size() == 2);
  CPPUNIT_ASSERT(theDaughters[0] == mockElectronPtr_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockUserCandPtr2_.get());

  std::vector<reco::CandidatePtr> daughterPtrs = finalState.daughterPtrs("@,aUserCand2");
  CPPUNIT_ASSERT(daughterPtrs.size() == 2);
  reco::CandidatePtr dauPtr0 = daughterPtrs[0];
  reco::CandidatePtr dauPtr1 = daughterPtrs[1];
  CPPUNIT_ASSERT(dauPtr0 == reco::CandidatePtr(mockElectronPtr_));
  CPPUNIT_ASSERT(dauPtr1 == reco::CandidatePtr(mockUserCandPtr2_));

  // IF the sys tag is blank (or @), get the regular daughter
  theDaughters = finalState.daughters(",aUserCand2");
  CPPUNIT_ASSERT(theDaughters[0] == mockElectronPtr_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockUserCandPtr2_.get());

  // Check no problems parsing the string with spaces
  theDaughters = finalState.daughters("   aUserCand1 ,  aUserCand2  ");
  CPPUNIT_ASSERT(theDaughters[0] == mockUserCandPtr1_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockUserCandPtr2_.get());
  theDaughters = finalState.daughters("   ,aUserCand2");
  CPPUNIT_ASSERT(theDaughters[0] == mockElectronPtr_.get());
  CPPUNIT_ASSERT(theDaughters[1] == mockUserCandPtr2_.get());

  // Check throws on missing userCand
  CPPUNIT_ASSERT_THROW(
      finalState.daughters(" notARealUserCand  ,aUserCand2"), cms::Exception);

  // Check userCand tester
  CPPUNIT_ASSERT(finalState.daughterHasUserCand(0, "aUserCand1"));
  CPPUNIT_ASSERT(!finalState.daughterHasUserCand(0, "aUserCand2"));

  // Check userCand getter
  CPPUNIT_ASSERT(finalState.daughterUserCand(0, "aUserCand1") == reco::CandidatePtr(mockUserCandPtr1_));
  CPPUNIT_ASSERT(finalState.daughterUserCand(1, "aUserCand2") == reco::CandidatePtr(mockUserCandPtr2_));
  // Check userCand getter throws on bad name
  CPPUNIT_ASSERT_THROW(finalState.daughterUserCand(0, "aasdf"), cms::Exception);

  // Check userCand P4 getter
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.daughterUserCandP4(0, "aUserCand1").pt(),
      mockUserCandPtr1_->pt(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.daughterUserCandP4(0, "aUserCand1").eta(),
      mockUserCandPtr1_->eta(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.daughterUserCandP4(0, "aUserCand1").phi(),
      mockUserCandPtr1_->phi(), 1e-6);

  // Check getting as specific types
  CPPUNIT_ASSERT(finalState.daughterAsElectron(0) == mockElectronPtr_);
  // Check that asking for the wrong type doesn't work
  // fixme
  //CPPUNIT_ASSERT(finalState.daughterAsElectron(1).isNull());
  //CPPUNIT_ASSERT(finalState.daughterAsMuon(1).isNonnull());

  // Check visP4 getter.  The regular one shoudl be same as the whole final
  // state
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4().pt(),  finalState.pt(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4().eta(),  finalState.eta(), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4().phi(),  finalState.phi(), 1e-6);

  {
    reco::Candidate::LorentzVector expectWithTags = mockElectronPtr_->p4() +
      mockUserCandPtr2_->p4();
    CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4(",aUserCand2").pt(), expectWithTags.pt(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4(",aUserCand2").eta(), expectWithTags.eta(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.visP4(",aUserCand2").phi(), expectWithTags.phi(), 1e-6);
  }

  {
    reco::Candidate::LorentzVector metP4 = mockMETPtr_->p4();
    reco::Candidate::LorentzVector totalP4 = finalState.totalP4();
    reco::Candidate::LorentzVector expectTotalP4 = finalState.visP4() + metP4;
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.pt(), totalP4.pt(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.eta(), totalP4.eta(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.phi(), totalP4.phi(), 1e-6);
  }

  {
    reco::Candidate::LorentzVector metP4 = mockMETPtr_->p4();
    reco::Candidate::LorentzVector totalP4 = finalState.totalP4("aUserCand1,", "");
    reco::Candidate::LorentzVector expectTotalP4 = finalState.visP4("aUserCand1,") + metP4;
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.pt(), totalP4.pt(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.eta(), totalP4.eta(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(expectTotalP4.phi(), totalP4.phi(), 1e-6);
  }

  // Test deltaPhi
  {
    double deltaPhi = reco::deltaPhi(mockElectronPtr_->phi(), mockMuonPtr1_->phi());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaPhi, finalState.dPhi(0,1), 1e-6);
    // For di-lepton this should always be true
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaPhi, finalState.smallestDeltaPhi(), 1e-6);

    deltaPhi = reco::deltaPhi(mockUserCandPtr1_->phi(), mockMuonPtr1_->phi());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaPhi, finalState.dPhi(0,"aUserCand1", 1, ""), 1e-6);
  }

  // Test deltaR
  {
    double deltaR = reco::deltaR(mockElectronPtr_->p4(), mockMuonPtr1_->p4());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaR, finalState.dR(0,1), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaR, finalState.smallestDeltaR(), 1e-6);

    deltaR = reco::deltaR(mockUserCandPtr1_->p4(), mockMuonPtr1_->p4());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaR, finalState.dR(0,"aUserCand1", 1, ""), 1e-6);
  }

  // Test delta phi to MET
  {
    double deltaPhi = reco::deltaPhi(mockElectronPtr_->phi(), mockMETPtr_->phi());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaPhi, finalState.deltaPhiToMEt(0), 1e-6);
    deltaPhi = reco::deltaPhi(mockMuonPtr1_->phi(), mockMETPtr_->phi());
    CPPUNIT_ASSERT_DOUBLES_EQUAL(deltaPhi, finalState.deltaPhiToMEt(1), 1e-6);
  }

  // TODO test MT

  {
    double ht = mockElectronPtr_->pt() + mockMuonPtr1_->pt();
    CPPUNIT_ASSERT_DOUBLES_EQUAL(ht, finalState.ht(), 1e-6);
    ht = mockUserCandPtr1_->pt() + mockUserCandPtr2_->pt();
    CPPUNIT_ASSERT_DOUBLES_EQUAL(ht, finalState.ht("aUserCand1,aUserCand2"), 1e-6);
  }

  // everything else lets use the trilepton
}

void testFinalState::testTriLepton() {
  const PATElecMuMuFinalState finalState(mockElectronPtr_, mockMuonPtr1_, mockMuonPtr2_,
      mockEventPtr_);

  CPPUNIT_ASSERT(finalState.daughter(0) == mockElectronPtr_.get());
  CPPUNIT_ASSERT(finalState.daughter(1) == mockMuonPtr1_.get());
  CPPUNIT_ASSERT(finalState.daughter(2) == mockMuonPtr2_.get());
  CPPUNIT_ASSERT(finalState.met() == mockMETPtr_);
  CPPUNIT_ASSERT(finalState.vertexObject() == nullVtx_);

  {
    PATFinalStateProxy subcand = finalState.subcand(1, 2);
    reco::Candidate::LorentzVector expectP4 = mockMuonPtr1_->p4() + mockMuonPtr2_->p4();
    int nDaughters = subcand->numberOfDaughters();
    CPPUNIT_ASSERT_EQUAL(2, nDaughters);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(subcand->pt(), expectP4.pt(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(subcand->phi(), expectP4.phi(), 1e-6);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(subcand->eta(), expectP4.eta(), 1e-6);
    CPPUNIT_ASSERT(subcand->charge() == -2);
  }


  CPPUNIT_ASSERT(finalState.daughter(0)->charge() == 1);
  CPPUNIT_ASSERT(finalState.daughter(2)->charge() == -1);

  CPPUNIT_ASSERT(!finalState.likeSigned(0, 2));
  CPPUNIT_ASSERT(finalState.likeSigned(1, 2));
  CPPUNIT_ASSERT(finalState.likeFlavor(1, 2));
  CPPUNIT_ASSERT(!finalState.likeFlavor(0, 2));

  // Test eval
  {
    CPPUNIT_ASSERT_DOUBLES_EQUAL(finalState.eval("daughter(1).pt"), mockMuonPtr1_->pt(), 1e-6);
    CPPUNIT_ASSERT(finalState.filter("daughter(1).pt > 5"));
    CPPUNIT_ASSERT(!finalState.filter("daughter(1).pt < 5"));
  }
}

void testFinalState::testOverlaps() {
  PATElecMuMuFinalState finalStateNonConst(mockElectronPtr_, mockMuonPtr1_, mockMuonPtr2_,
      mockEventPtr_);
  finalStateNonConst.setOverlaps("jets", mockJetEdmPtrVector_);
  const PATElecMuMuFinalState finalState(finalStateNonConst);
  CPPUNIT_ASSERT(finalState.hasOverlaps("jets"));
  CPPUNIT_ASSERT(finalState.overlaps("jets") == mockJetEdmPtrVector_);
  // No filter
  CPPUNIT_ASSERT(finalState.extras("jets", "") == mockJetPtrVector_);
  size_t actual = 0;
  reco::Candidate::LorentzVector p4Total;
  for (size_t i = 0; i < mockJetPtrVector_.size(); ++i) {
    if (mockJetPtrVector_[i]->pt() > 43.2) {
      actual++;
      p4Total += mockJetPtrVector_[i]->p4();
    }
  }
  // Test filter is working
  CPPUNIT_ASSERT(finalState.extras("jets", "pt > 43.2").size() == actual);

  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.eval("extras('jets', 'pt > 43.2').size()"),
      actual, 1e-6);

  // Test overlap subcandidate creation
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.subcand("#,#,#", "jets", "pt > 43.2")->pt(),
      p4Total.pt(), 1e-6);

  p4Total += mockElectronPtr_->p4();
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.subcand("@,#,#", "jets", "pt > 43.2")->pt(),
      p4Total.pt(), 1e-6);

  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.eval("subcand('@,#,#').get.pt - daughter(0).pt"), 0, 1e-6);
}

void testFinalState::testIndexGetter() {
  PATElecMuMuFinalState finalStateNonConst(mockElectronPtr_, mockMuonPtr1_, mockMuonPtr2_,
      mockEventPtr_);
  const PATElecMuMuFinalState& finalState = finalStateNonConst;
  CPPUNIT_ASSERT(mockMuonPtr2_->pt() > mockMuonPtr1_->pt());
  CPPUNIT_ASSERT(mockMuonPtr1_->pt() > mockElectronPtr_->pt());
  std::vector<size_t> indices = finalState.indicesByPt();
  CPPUNIT_ASSERT(indices.size() == 3);
  CPPUNIT_ASSERT(indices[0] == 2);
  CPPUNIT_ASSERT(indices[1] == 1);
  CPPUNIT_ASSERT(indices[2] == 0);
  indices = finalState.indicesByPt("aUserCand1,@,@");
  CPPUNIT_ASSERT(indices.size() == 3);
  CPPUNIT_ASSERT(indices[0] == 0);
  CPPUNIT_ASSERT(indices[1] == 2);
  CPPUNIT_ASSERT(indices[2] == 1);
  CPPUNIT_ASSERT(!finalState.ptOrdered(0, 1));
  CPPUNIT_ASSERT(finalState.ptOrdered(1, 0));
  CPPUNIT_ASSERT(finalState.ptOrdered(2, 0));
  // Doesn't compile :(
//  CPPUNIT_ASSERT_DOUBLES_EQUAL(
//      finalState.eval("daughter(indicesByPt()[0]).pt - daughter(2).pt"),
//      0.0, 1e-6);
  std::vector<const reco::Candidate*> daus = finalState.daughtersByPt();
  CPPUNIT_ASSERT(daus[0] == mockMuonPtr2_.get());
  CPPUNIT_ASSERT(daus[1] == mockMuonPtr1_.get());
  CPPUNIT_ASSERT(daus[2] == mockElectronPtr_.get());
  CPPUNIT_ASSERT_DOUBLES_EQUAL(
      finalState.eval( "abs(deltaPhi(daughterByPt(0).phi, daughterByPt(1).phi))"),
      //finalState.eval( "daughtersByPt()[0].phi"),
      reco::deltaPhi(finalState.daughtersByPt()[0]->phi(), finalState.daughtersByPt()[1]->phi()),
      1e-6
      );

}

CPPUNIT_TEST_SUITE_REGISTRATION(testFinalState);
