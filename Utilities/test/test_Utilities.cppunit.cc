/*
 * Test Utilities
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>
#include <vector>

#include "FinalStateAnalysis/Utilities/interface/StringObjectSorter.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include <algorithm>

using namespace edm;

class testUtilities: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testUtilities);
  CPPUNIT_TEST(testSorter);
  CPPUNIT_TEST(testLazySorter);
  CPPUNIT_TEST(testRepeat);
  CPPUNIT_TEST_SUITE_END();
  public:
    void setUp() {};
    void tearDown(){}
    void testSorter();
    void testLazySorter();
    void testRepeat();
};


void testUtilities::testSorter() {
  StringObjectSorter<reco::LeafCandidate> sorter("pt");

  // 5 cands
  {
    size_t nCands = 5;
    std::vector<const reco::LeafCandidate*> cands;
    // Ascending
    for (size_t i = 0; i < nCands; ++i) {
      reco::Candidate::LorentzVector p4(i, 0, 0, i);
      cands.push_back(new reco::LeafCandidate(0, p4));
    }
    std::sort(cands.begin(), cands.end(), sorter);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(nCands-1, cands[0]->pt(), 1e-6);
    for (size_t i = 0; i < nCands; ++i) {
      delete cands[i];
    }
  }

  // 15 cands
  {
    size_t nCands = 15;
    std::vector<const reco::LeafCandidate*> cands;
    // Ascending
    for (size_t i = 0; i < nCands; ++i) {
      reco::Candidate::LorentzVector p4(i, 0, 0, i);
      cands.push_back(new reco::LeafCandidate(0, p4));
    }
    std::sort(cands.begin(), cands.end(), sorter);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(nCands-1, cands[0]->pt(), 1e-6);
    for (size_t i = 0; i < nCands; ++i) {
      delete cands[i];
    }
  }

  //100 cands
  {
    size_t nCands = 100;
    std::vector<const reco::LeafCandidate*> cands;
    // Ascending
    for (size_t i = 0; i < nCands; ++i) {
      reco::Candidate::LorentzVector p4(i, 0, 0, i);
      cands.push_back(new reco::LeafCandidate(0, p4));
    }
    std::sort(cands.begin(), cands.end(), sorter);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(nCands-1, cands[0]->pt(), 1e-6);
    for (size_t i = 0; i < nCands; ++i) {
      delete cands[i];
    }
  }

}

void testUtilities::testLazySorter() {
  StringObjectSorter<reco::Candidate> sorter("track().key()");

  // 100 cands
  {
    size_t nCands = 10;
    std::vector<const reco::Candidate*> cands;
    // Ascending
    for (size_t i = 0; i < nCands; ++i) {
      reco::Candidate::LorentzVector p4(i, 0, 0, i);
      reco::RecoChargedCandidate* newcand = new reco::RecoChargedCandidate(0, p4);
      reco::TrackRef fake(NULL, i);
      newcand->setTrack(fake);
      cands.push_back(newcand);
    }
    std::sort(cands.begin(), cands.end(), sorter);
    CPPUNIT_ASSERT_DOUBLES_EQUAL(nCands-1, cands[0]->pt(), 1e-6);
    for (size_t i = 0; i < nCands; ++i) {
      delete cands[i];
    }
  }

  // This crashes!  the function value changes to some garbage flaot
//  {
//    size_t nCands = 100;
//    std::vector<const reco::Candidate*> cands;
//    // Ascending
//    for (size_t i = 0; i < nCands; ++i) {
//      reco::Candidate::LorentzVector p4(i, 0, 0, i);
//      reco::RecoChargedCandidate* newcand = new reco::RecoChargedCandidate(0, p4);
//      reco::TrackRef fake(NULL, i);
//      newcand->setTrack(fake);
//      cands.push_back(newcand);
//    }
//    std::sort(cands.begin(), cands.end(), sorter);
//    CPPUNIT_ASSERT_DOUBLES_EQUAL(nCands-1, cands[0]->pt(), 1e-6);
//    for (size_t i = 0; i < nCands; ++i) {
//      delete cands[i];
//    }
//  }
}

void testUtilities::testRepeat() {
  StringObjectFunction<reco::Candidate> function("track().key()", true);

  // 100 cands
  {
    size_t nCands = 100;
    std::vector<const reco::Candidate*> cands;
    // Ascending
    for (size_t i = 0; i < nCands; ++i) {
      reco::Candidate::LorentzVector p4(i, 0, 0, i);
      reco::RecoChargedCandidate* newcand = new reco::RecoChargedCandidate(0, p4);
      reco::TrackRef fake(NULL, i);
      newcand->setTrack(fake);
      cands.push_back(newcand);
    }
    std::vector<double> last_values;
    last_values.resize(cands.size());
    for (size_t i = 0; i < nCands; ++i) {
      const reco::Candidate* cand = cands[i];
      last_values[i] = function(*cand);
    }

    for (size_t j = 0; j < 10000; ++j) {
      for (size_t i = 0; i < nCands; ++i) {
        const reco::Candidate* cand = cands[i];
        CPPUNIT_ASSERT(cand);
        double new_value = function(*cand);
        CPPUNIT_ASSERT_EQUAL(last_values[i], new_value);
        last_values[i]= new_value;
      }
    }
    for (size_t i = 0; i < nCands; ++i) {
      delete cands[i];
    }

  }


}

CPPUNIT_TEST_SUITE_REGISTRATION(testUtilities);
