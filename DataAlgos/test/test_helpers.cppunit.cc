/*
 * Test the fshelpers functions
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>
#include <vector>

#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"

using namespace fshelpers;

class testHelpers: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testHelpers);
  CPPUNIT_TEST(testxySignificance);
  CPPUNIT_TEST_SUITE_END();
  public:
  void testxySignificance();

};

void testHelpers::testxySignificance() {
  reco::Candidate::Vector xOnly(1, 0, 0);
  reco::Candidate::Vector yOnly(0, 1, 0);
  TMatrixD cov(2,2);
  cov(0, 0) = 2*2;
  cov(1, 1) = 3*3;
  // no off diagonal elements
  cov(0, 1) = 0;
  cov(1, 0) = 0;

  CPPUNIT_ASSERT_DOUBLES_EQUAL(1/2., xySignficance(xOnly, cov), 1e-6);
  CPPUNIT_ASSERT_DOUBLES_EQUAL(1/3., xySignficance(yOnly, cov), 1e-6);
}


CPPUNIT_TEST_SUITE_REGISTRATION(testHelpers);
