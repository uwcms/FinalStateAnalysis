/*
 * Test the SmartTrigger object
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>
#include <vector>

#include "FinalStateAnalysis/DataFormats/interface/SmartTrigger.h"

class testSmartTrigger: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testSmartTrigger);
  CPPUNIT_TEST(testGroupSelect);
  CPPUNIT_TEST(testMissingTrigger);
  CPPUNIT_TEST(testAllMissingTrigger);
  CPPUNIT_TEST(testOR);
  CPPUNIT_TEST(testORDifferentPrescales);
  CPPUNIT_TEST_SUITE_END();
  typedef std::vector<unsigned int>  VInt;
  typedef std::vector<VInt> VVInt;
  public:
  void testGroupSelect();
  void testMissingTrigger();
  void testAllMissingTrigger();
  void testORDifferentPrescales();
  void testOR();

};

void testSmartTrigger::testGroupSelect() {
  // The first, lowest prescaled trigger should be selected.  Group 3
  VInt groupA;
  groupA.push_back(20);
  VInt groupB;
  groupB.push_back(20);
  VInt groupC;
  groupC.push_back(5);
  VInt groupD;
  groupD.push_back(5);
  VVInt prescales;
  prescales.push_back(groupA);
  prescales.push_back(groupB);
  prescales.push_back(groupC);
  prescales.push_back(groupD);

  VInt resultA;
  resultA.push_back(0);
  VInt resultB;
  resultB.push_back(0);
  VInt resultC;
  resultC.push_back(1);
  VInt resultD;
  resultD.push_back(0);
  VVInt results;
  results.push_back(resultA);
  results.push_back(resultB);
  results.push_back(resultC);
  results.push_back(resultD);

  SmartTriggerResult result = makeDecision(prescales, results);

  // Group C
  CPPUNIT_ASSERT(result.group == 2);

  // Prescale & Result from C
  CPPUNIT_ASSERT(result.prescale == 5);
  CPPUNIT_ASSERT(result.passed == 1);
}

void testSmartTrigger::testMissingTrigger() {
  // Missing triggers should be skipped.  i.e. group C was run in this Run
  VInt groupA;
  groupA.push_back(20);
  VInt groupB;
  groupB.push_back(20);
  VInt groupC;
  groupC.push_back(0);
  VInt groupD;
  groupD.push_back(69);
  VVInt prescales;
  prescales.push_back(groupA);
  prescales.push_back(groupB);
  prescales.push_back(groupC);
  prescales.push_back(groupD);

  VInt resultA;
  resultA.push_back(0);
  VInt resultB;
  resultB.push_back(0);
  VInt resultC;
  resultC.push_back(0);
  VInt resultD;
  resultD.push_back(10);
  VVInt results;
  results.push_back(resultA);
  results.push_back(resultB);
  results.push_back(resultC);
  results.push_back(resultD);

  SmartTriggerResult result = makeDecision(prescales, results);

  // Group D
  CPPUNIT_ASSERT(result.group == 3);

  // Prescale & Result from D
  CPPUNIT_ASSERT(result.prescale == 69);
  CPPUNIT_ASSERT(result.passed == 10);
}

// If everything is missing, return group = nGroups
void testSmartTrigger::testAllMissingTrigger() {
  // Missing triggers should be skipped.  i.e. group C was run in this Run
  VInt groupA;
  groupA.push_back(0);
  VInt groupB;
  groupB.push_back(0);
  VInt groupC;
  groupC.push_back(0);
  VInt groupD;
  groupD.push_back(0);
  VVInt prescales;
  prescales.push_back(groupA);
  prescales.push_back(groupB);
  prescales.push_back(groupC);
  prescales.push_back(groupD);

  VInt resultA;
  resultA.push_back(0);
  VInt resultB;
  resultB.push_back(0);
  VInt resultC;
  resultC.push_back(0);
  VInt resultD;
  resultD.push_back(10);
  VVInt results;
  results.push_back(resultA);
  results.push_back(resultB);
  results.push_back(resultC);
  results.push_back(resultD);

  SmartTriggerResult result = makeDecision(prescales, results);

  // Group D
  CPPUNIT_ASSERT(result.group == 4);

  // Prescale & Result from D
  CPPUNIT_ASSERT(result.prescale == 0);
  CPPUNIT_ASSERT(result.passed == 0);
}

// You can OR triggers.
void testSmartTrigger::testOR() {
  VInt groupA;
  groupA.push_back(10);
  VInt groupB;
  groupB.push_back(5);
  VInt groupC;
  groupC.push_back(4); // C is OR of two triggers
  groupC.push_back(4);
  VInt groupD;
  groupD.push_back(4);
  VVInt prescales;
  prescales.push_back(groupA);
  prescales.push_back(groupB);
  prescales.push_back(groupC);
  prescales.push_back(groupD);

  {
    VInt resultA;
    resultA.push_back(0);
    VInt resultB;
    resultB.push_back(0);
    VInt resultC;
    resultC.push_back(1);
    resultC.push_back(1);
    VInt resultD;
    resultD.push_back(10);
    VVInt results;
    results.push_back(resultA);
    results.push_back(resultB);
    results.push_back(resultC);
    results.push_back(resultD);

    SmartTriggerResult result = makeDecision(prescales, results);

    // Group C
    CPPUNIT_ASSERT(result.group == 2);

    // Prescale & Result from C
    CPPUNIT_ASSERT(result.prescale == 4);
    CPPUNIT_ASSERT(result.passed == 1);
  }

  {
    // Check if one fails
    VInt resultA;
    resultA.push_back(0);
    VInt resultB;
    resultB.push_back(0);
    VInt resultC;
    resultC.push_back(1);
    resultC.push_back(0);
    VInt resultD;
    resultD.push_back(10);
    VVInt results;
    results.push_back(resultA);
    results.push_back(resultB);
    results.push_back(resultC);
    results.push_back(resultD);

    SmartTriggerResult result = makeDecision(prescales, results);

    // Group C
    CPPUNIT_ASSERT(result.group == 2);

    // Prescale & Result from C
    CPPUNIT_ASSERT(result.prescale == 4);
    CPPUNIT_ASSERT(result.passed == 1);
  }

  {
    // Check if both fails
    VInt resultA;
    resultA.push_back(0);
    VInt resultB;
    resultB.push_back(0);
    VInt resultC;
    resultC.push_back(0);
    resultC.push_back(0);
    VInt resultD;
    resultD.push_back(10);
    VVInt results;
    results.push_back(resultA);
    results.push_back(resultB);
    results.push_back(resultC);
    results.push_back(resultD);

    SmartTriggerResult result = makeDecision(prescales, results);

    // Group C
    CPPUNIT_ASSERT(result.group == 2);

    // Prescale & Result from C
    CPPUNIT_ASSERT(result.prescale == 4);
    CPPUNIT_ASSERT(result.passed == 0);
  }
}

// If the ORed triggers, have different prescales, always skip them.
void testSmartTrigger::testORDifferentPrescales() {
  VInt groupA;
  groupA.push_back(10);
  VInt groupB;
  groupB.push_back(7);
  VInt groupC;
  groupC.push_back(1); // C is OR of two triggers
  groupC.push_back(4);
  VInt groupD;
  groupD.push_back(5);
  VVInt prescales;
  prescales.push_back(groupA);
  prescales.push_back(groupB);
  prescales.push_back(groupC);
  prescales.push_back(groupD);

  VInt resultA;
  resultA.push_back(0);
  VInt resultB;
  resultB.push_back(0);
  VInt resultC;
  resultC.push_back(1);
  resultC.push_back(1);
  VInt resultD;
  resultD.push_back(10);
  VVInt results;
  results.push_back(resultA);
  results.push_back(resultB);
  results.push_back(resultC);
  results.push_back(resultD);

  SmartTriggerResult result = makeDecision(prescales, results);

  // Group D - C has different prescales
  CPPUNIT_ASSERT(result.group == 3);

  // Prescale & Result from D
  CPPUNIT_ASSERT(result.prescale == 5);
  CPPUNIT_ASSERT(result.passed == 10);
}

CPPUNIT_TEST_SUITE_REGISTRATION(testSmartTrigger);
