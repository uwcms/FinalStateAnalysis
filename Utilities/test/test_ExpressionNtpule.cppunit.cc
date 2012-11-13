#include "FinalStateAnalysis/Utilities/interface/ExpressionNtuple.h"
#include "TRandom.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>


class testExpressionNtuple: public CppUnit::TestFixture {
  typedef std::vector<reco::LeafCandidate> vLeafCandidate;
  CPPUNIT_TEST_SUITE(testExpressionNtuple);
  CPPUNIT_TEST(testBooking);
  CPPUNIT_TEST(testFilling);
  CPPUNIT_TEST_SUITE_END();
  public:
    void setUp();
    void tearDown(){}
    void testBooking();
    void testFilling();
  private:
    ExpressionNtuple<reco::LeafCandidate> * ntuple_;
    ExpressionNtuple<vLeafCandidate> * nfntuple_;
    fwlite::TFileService * fileService;
};


void testExpressionNtuple::setUp() {
  edm::ParameterSet pset;
  pset.addParameter<std::string>("pt", "pt");
  pset.addParameter<std::string>("eta", "eta");
  pset.addParameter<std::string>("abseta", "abs(eta)");
  pset.addParameter<std::string>("charge", "charge");
  fileService = new fwlite::TFileService("test_file.root");
  ntuple_ = new ExpressionNtuple<reco::LeafCandidate>(pset);
  ntuple_->initialize(*fileService);
  
  nfntuple_ = new ExpressionNtuple<vLeafCandidate>(pset);
  nfntuple_->initialize(*fileService);
}

void testExpressionNtuple::testBooking() {
  CPPUNIT_ASSERT(ntuple_);
  CPPUNIT_ASSERT(ntuple_->tree()->GetBranch("pt"));
  CPPUNIT_ASSERT(ntuple_->tree()->GetBranch("eta"));
  CPPUNIT_ASSERT(ntuple_->tree()->GetBranch("abseta"));
  CPPUNIT_ASSERT(ntuple_->tree()->GetBranch("charge"));
  // There is one additional branch, which is the IDX of each element.
  CPPUNIT_ASSERT(ntuple_->tree()->GetListOfBranches()->GetEntries() == 5);

  CPPUNIT_ASSERT(nfntuple_);
  CPPUNIT_ASSERT(nfntuple_->tree()->GetBranch("pt"));
  CPPUNIT_ASSERT(nfntuple_->tree()->GetBranch("eta"));
  CPPUNIT_ASSERT(nfntuple_->tree()->GetBranch("abseta"));
  CPPUNIT_ASSERT(nfntuple_->tree()->GetBranch("charge"));
  // There is one additional branch, which is the IDX of each element.
  CPPUNIT_ASSERT(nfntuple_->tree()->GetListOfBranches()->GetEntries() == 5);
}

void testExpressionNtuple::testFilling() {
  int nEntriesPtGt53 = 0;
  int nEntriesAbsEtaGt2 = 0;
  TRandom randy;
  for (int i = 0; i < 100; ++i) {
    double eta = randy.Rndm()*5 - 2.5;
    reco::LeafCandidate cand(i, math::PtEtaPhiMLorentzVector(i, eta, 0, 0));
    if (i > 53)
      nEntriesPtGt53++;
    if (std::abs(eta) > 2)
      nEntriesAbsEtaGt2++;
    ntuple_->fill(cand, i);
  }
  CPPUNIT_ASSERT(ntuple_->tree()->GetEntries() == 100);
  CPPUNIT_ASSERT(ntuple_->tree()->GetEntries("pt > 53") == nEntriesPtGt53);
  CPPUNIT_ASSERT(ntuple_->tree()->GetEntries("abs(eta) > 2.0") == nEntriesAbsEtaGt2);
  CPPUNIT_ASSERT(ntuple_->tree()->GetEntries("abseta > 2.0") == nEntriesAbsEtaGt2);
  CPPUNIT_ASSERT(ntuple_->tree()->GetEntries("idx == 1") == 1);  
}


CPPUNIT_TEST_SUITE_REGISTRATION(testExpressionNtuple);
