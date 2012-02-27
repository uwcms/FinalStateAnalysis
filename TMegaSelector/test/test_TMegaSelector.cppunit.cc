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
#include "TFile.h"
#include <stdexcept>

class testMegaSelector: public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(testMegaSelector);
  CPPUNIT_TEST(testOperatorSelections);
  CPPUNIT_TEST(testUnknownOperator);
  CPPUNIT_TEST(testBadBranchType);
  CPPUNIT_TEST(testBadBranchName);
  CPPUNIT_TEST(testSelectionSet);
  CPPUNIT_TEST(testSelectionCaching);
  // The full chain
  CPPUNIT_TEST(testSelector);

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
    /// Test caching functionality
    void testSelectionCaching();

    /// Test main selector code
    void testSelector();

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

  // Save the output file for later
  TFile outfile("test_file.root", "recreate");
  TTree* copy = testTree_->CopyTree("");
  outfile.cd();
  copy->Write();
  outfile.Close();
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

void testMegaSelector::testSelectionCaching() {
  TMegaSelectionFactory factory(director_);
  testTree_->GetEntry(5);
  director_->SetReadEntry(5);

  std::auto_ptr<TMegaSelection> intCut = factory.MakeIntCut("intBranch", ">", -12);

  TMegaSelection* intPointer = intCut.get();  // keep track of this guy for testing

  TMegaSelectionSet selectionSet("aSet", "aSet");
  selectionSet.AddSelection(intCut);

  Long_t entry = 5;

  selectionSet.SetCachePointers(&testTree_, &entry);

  // emit change should return true, whenever the entry or tree changes
  CPPUNIT_ASSERT(selectionSet.emitChanged() && intPointer->emitChanged());

  // emit change should now be false until we change the entry or tree
  CPPUNIT_ASSERT(!selectionSet.emitChanged());
  CPPUNIT_ASSERT(!intPointer->emitChanged());

  entry = 6;

  CPPUNIT_ASSERT(selectionSet.emitChanged() && intPointer->emitChanged());
  CPPUNIT_ASSERT(!selectionSet.emitChanged());
  CPPUNIT_ASSERT(!intPointer->emitChanged());

  TTree* currentTreePtr = testTree_;  // save to restore state
  testTree_ = NULL;

  CPPUNIT_ASSERT(selectionSet.emitChanged() && intPointer->emitChanged());
  CPPUNIT_ASSERT(!selectionSet.emitChanged());
  CPPUNIT_ASSERT(!intPointer->emitChanged());

  testTree_ = currentTreePtr;  // restore state
}

class TMegaTester : public TMegaSelector {
  public:
    TMegaTester(TTree* tree=0):TMegaSelector(tree) {
      this->AddToSelection("tester",
          this->factory()->MakeIntCut("intBranch", ">", -12));
      this->AddToSelection("tester",
          this->factory()->MakeFloatCut("floatBranch", "<", 10));
      count = 0;
      testSelectCount = 0;
      tree_ = tree;
    }
    void MegaBegin() {
    }
    Bool_t MegaProcess(Long64_t entry) {
      count += 1;
      //std::cout << entry << std::endl;
      TMegaSelectionSet* tester = this->GetSelectionSet("tester");
      //std::cout << tester << std::endl;
      if (tester->Select()) {
        //std::cout << "select" << std::endl;
        testSelectCount += 1;
      }

      return true;
    }
    void MegaTerminate() {
    }

    Long64_t count;
    Long64_t testSelectCount;
    TTree* tree_;
};

void testMegaSelector::testSelector() {

  TMegaTester megaTester(testTree_);
  testTree_->Process(&megaTester);
  int expected = testTree_->GetEntries("intBranch > -12 && floatBranch < 10");

  CPPUNIT_ASSERT_EQUAL(testTree_->GetEntries(), megaTester.count);
  CPPUNIT_ASSERT(megaTester.testSelectCount == expected);

  // Try it with the filter
  TMegaTester megaTester2(testTree_);
  megaTester2.SetFilterSelection("tester");
  testTree_->Process(&megaTester2);
  CPPUNIT_ASSERT(megaTester2.testSelectCount == megaTester2.count);
  CPPUNIT_ASSERT(megaTester2.testSelectCount == expected);
}


CPPUNIT_TEST_SUITE_REGISTRATION(testMegaSelector);
