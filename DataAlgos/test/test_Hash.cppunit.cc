/*
 * Test the fshelpers functions
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>
#include <vector>

#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

using namespace edm;

class testHash: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testHash);
  CPPUNIT_TEST(testPID);
  CPPUNIT_TEST(testCandPtr);
  CPPUNIT_TEST(testOrdering);
  CPPUNIT_TEST_SUITE_END();
  public:
  void testPID();
  void testCandPtr();
  void testOrdering();
};

void testHash::testPID() {
  edm::ProductID pid1(1, 1);
  edm::ProductID pid2(1, 2);
  CPPUNIT_ASSERT(hash_value(pid1) != hash_value(pid2));
  edm::ProductID pid3(3, 1);
  edm::ProductID pid4(4, 1);
  CPPUNIT_ASSERT(hash_value(pid3) != hash_value(pid4));
  edm::ProductID pid5(5, 1);
  edm::ProductID pid6(5, 1);
  CPPUNIT_ASSERT(hash_value(pid5) == hash_value(pid6));
}

void testHash::testCandPtr() {
  edm::ProductID pid1(1, 1);
  edm::ProductID pid2(1, 2);
  reco::CandidateCollection mockCands1;
  reco::CandidateCollection mockCands2;
  for (size_t i = 0; i < 3; ++i) {
    mockCands1.push_back(new reco::LeafCandidate());
    mockCands2.push_back(new reco::LeafCandidate());
  }

  TestHandle<reco::CandidateCollection> mockHandle1(&mockCands1, pid1);
  TestHandle<reco::CandidateCollection> mockHandle2(&mockCands2, pid2);

  reco::CandidatePtr cand_1_1(mockHandle1, 1);
  reco::CandidatePtr cand_1_2(mockHandle1, 2);

  reco::CandidatePtr cand_2_1(mockHandle2, 1);
  reco::CandidatePtr cand_2_1_b(mockHandle2, 1);

  CPPUNIT_ASSERT(hash_value(cand_1_1) != hash_value(cand_1_2));
  CPPUNIT_ASSERT(hash_value(cand_1_1) != hash_value(cand_2_1));
  CPPUNIT_ASSERT(hash_value(cand_2_1) == hash_value(cand_2_1_b));
}

void testHash::testOrdering() {
  edm::ProductID pid1(1, 1);
  edm::ProductID pid2(1, 2);
  reco::CandidateCollection mockCands1;
  reco::CandidateCollection mockCands2;
  for (size_t i = 0; i < 3; ++i) {
    mockCands1.push_back(new reco::LeafCandidate());
    mockCands2.push_back(new reco::LeafCandidate());
  }

  TestHandle<reco::CandidateCollection> mockHandle1(&mockCands1, pid1);
  TestHandle<reco::CandidateCollection> mockHandle2(&mockCands2, pid2);

  reco::CandidatePtr cand_1_1(mockHandle1, 1);
  reco::CandidatePtr cand_1_2(mockHandle1, 2);

  reco::CandidatePtr cand_2_1(mockHandle2, 1);
  reco::CandidatePtr cand_2_1_b(mockHandle2, 1);

  std::vector<reco::CandidatePtr> vec_a;
  vec_a.push_back(cand_1_1);
  vec_a.push_back(cand_1_2);
  vec_a.push_back(cand_2_1);

  std::vector<reco::CandidatePtr> vec_a_copy;
  vec_a_copy.push_back(cand_1_1);
  vec_a_copy.push_back(cand_1_2);
  vec_a_copy.push_back(cand_2_1);

  const std::vector<reco::CandidatePtr> vec_a_const(vec_a);

  CPPUNIT_ASSERT(hash_value(vec_a_const) == hash_value(vec_a));
  // const correctness
  CPPUNIT_ASSERT(hash_value(vec_a_const) == hash_value(vec_a));
  CPPUNIT_ASSERT(hash_value(vec_a) == hash_value(vec_a_copy));

  std::vector<reco::CandidatePtr> vec_a_extra;
  vec_a_extra.push_back(cand_1_1);
  vec_a_extra.push_back(cand_1_2);

  CPPUNIT_ASSERT(hash_value(vec_a_extra) != hash_value(vec_a));

  // Same as A, but different order
  std::vector<reco::CandidatePtr> vec_b;
  vec_b.push_back(cand_1_1);
  vec_b.push_back(cand_2_1);
  vec_b.push_back(cand_1_2);

  CPPUNIT_ASSERT(hash_value(vec_a) != hash_value(vec_b));

  CPPUNIT_ASSERT(hashCandsByContent(vec_a) == hashCandsByContent(vec_b));

  // B has been sorted in place, so now it's equal to A
  CPPUNIT_ASSERT(vec_a == vec_b);
}

CPPUNIT_TEST_SUITE_REGISTRATION(testHash);
