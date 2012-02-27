/*
 * Test the TMegaSelector object
 */

#include <cppunit/extensions/HelperMacros.h>
#include <Utilities/Testing/interface/CppUnit_testdriver.icpp>

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelector.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionFactory.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionSet.h"

#include "TTree.h"
#include <stdexcept>

class testMegaSelector: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testMegaSelector);
  CPPUNIT_TEST(testOperatorSelections);
  CPPUNIT_TEST(testUnknownOperator);
  CPPUNIT_TEST(testBadBranchType);
  CPPUNIT_TEST(testBadBranchName);
  CPPUNIT_TEST(testSelectionSet);
  CPPUNIT_TEST_SUITE_END();
  public:
    void setUp();
    void tearDown();

    /// Test operator based selections on a branch
    void testOperatorSelections();
    /// Test we throw and exception on an unknown op code type
    void testUnknownOperator();
    /// Test we throw when the declared branch type (int/float) isn't correct
    void testBadBranchType();
    /// Test we throw when the branch name doesn't exist
    void testBadBranchName();
    /// Test selection set functionality
    void testSelectionSet();

  private:
    TTree* testTree_;
    ROOT::TBranchProxyDirector* director_;
    Int_t intBranch_;
    Float_t floatBranch_;
    Double_t doubleBranch_;
};

void testMegaSelector::setUp() {
  testTree_ = new TTree("TestTree", "TestTree");
  director_ = new ROOT::TBranchProxyDirector(testTree_, -1);
  testTree_->Branch("intBranch", &intBranch_);
  testTree_->Branch("floatBranch", &floatBranch_);
  testTree_->Branch("doubleBranch", &doubleBranch_);
  // 41 entries, from -20 to 20
  for (int i = -20; i < 21; ++i) {
    intBranch_ = i;
    floatBranch_ = i;
    doubleBranch_ = i;
    testTree_->Fill();
  }
}

void testMegaSelector::tearDown() {
  delete testTree_;
  delete director_;
}

void testMegaSelector::testOperatorSelections() {
  TMegaSelectionFactory factory(director_);

  testTree_->GetEntry(10);
  director_->SetReadEntry(10);
  CPPUNIT_ASSERT(intBranch_ == -10);

  std::auto_ptr<TMegaSelection> intCut = factory.MakeIntCut(
      "intBranch", ">", -11);

  CPPUNIT_ASSERT(intCut->Select());

  testTree_->GetEntry(5);
  director_->SetReadEntry(5);
  CPPUNIT_ASSERT(intBranch_ == -15);

  // Check to make sure now it fails
  CPPUNIT_ASSERT_EQUAL(false, intCut->Select());

  // Now try different operators first GEQ
  intCut = factory.MakeIntCut("intBranch", ">=", -11);
  CPPUNIT_ASSERT_EQUAL(false, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", ">=", -15);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", ">=", -16);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());

  // Now try different operators first LEQ
  intCut = factory.MakeIntCut("intBranch", "<=", -11);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", "<=", -15);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", "<=", -16);
  CPPUNIT_ASSERT_EQUAL(false, intCut->Select());

  intCut = factory.MakeIntCut("intBranch", "==", -15);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", "==", -16);
  CPPUNIT_ASSERT_EQUAL(false, intCut->Select());

  intCut = factory.MakeIntCut("intBranch", "!=", -16);
  CPPUNIT_ASSERT_EQUAL(true, intCut->Select());
  intCut = factory.MakeIntCut("intBranch", "!=", -15);
  CPPUNIT_ASSERT_EQUAL(false, intCut->Select());
}

void testMegaSelector::testUnknownOperator() {
  TMegaSelectionFactory factory(director_);
  CPPUNIT_ASSERT_THROW(
      factory.MakeIntCut("intBranch", "I'm WRONG", -11),
      std::runtime_error
      );
}

void testMegaSelector::testBadBranchType() {
//  TMegaSelectionFactory factory(director_);
////  CPPUNIT_ASSERT_THROW(
////      factory.MakeFloatCut("intBranch", "==", -11),
////      std::runtime_error
////      );
//  testTree_->GetEntry(5);
//  director_->SetReadEntry(5);
//  CPPUNIT_ASSERT(intBranch_ == -15);
//  std::auto_ptr<TMegaSelection> cut = factory.MakeFloatCut("intBranch", ">", -12);
//  CPPUNIT_ASSERT(cut->Select());
}

void testMegaSelector::testBadBranchName() {
  TMegaSelectionFactory factory(director_);
  testTree_->GetEntry(5);
  director_->SetReadEntry(5);
  std::auto_ptr<TMegaSelection> cut = factory.MakeFloatCut("HELLO", ">", -12);
  CPPUNIT_ASSERT_THROW( cut->Select(), std::runtime_error);
}

void testMegaSelector::testSelectionSet() {
  TMegaSelectionFactory factory(director_);
  testTree_->GetEntry(5);
  director_->SetReadEntry(5);

  TMegaSelectionSet selectionSet("aSet", "aSet");

  selectionSet.AddSelection(factory.MakeIntCut("intBranch", ">", -12));
  selectionSet.AddSelection(factory.MakeFloatCut("floatBranch", "<", 10));

  std::auto_ptr<TMegaSelection> intCut = factory.MakeIntCut("intBranch", ">", -12);
  std::auto_ptr<TMegaSelection> floatCut = factory.MakeFloatCut("floatBranch", "<", 10);

  for (int i = 0; i < testTree_->GetEntries(); ++i) {
    testTree_->GetEntry(i);
    director_->SetReadEntry(i);
    bool expect = intCut->Select() && floatCut->Select();
    bool got = selectionSet.Select();
    CPPUNIT_ASSERT_EQUAL(expect, got);
  }

  // Test nested selection sets
  TMegaSelectionSet superSet("superSet", "superSet");
  superSet.AddSelection(selectionSet);
  superSet.AddSelection(factory.MakeDoubleCut("doubleBranch", "<", 5));
  std::auto_ptr<TMegaSelection> doubleCut = factory.MakeDoubleCut("doubleBranch", "<", 5);

  for (int i = 0; i < testTree_->GetEntries(); ++i) {
    testTree_->GetEntry(i);
    director_->SetReadEntry(i);
    CPPUNIT_ASSERT_EQUAL(
        intCut->Select() && floatCut->Select() && doubleCut->Select(),
        superSet.Select());
  }
}

CPPUNIT_TEST_SUITE_REGISTRATION(testMegaSelector);
