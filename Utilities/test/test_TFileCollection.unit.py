import ROOT
import tempfile
import FinalStateAnalysis.Utilities.TFileCollection as TFileCollection
import FinalStateAnalysis.Utilities.CachingTTree as CachingTTree
import os

import unittest
from test import test_support

class TestTFileCollection(unittest.TestCase):

    def test_histo_get(self):
        self.test_dir = os.path.join(
            os.environ['CMSSW_BASE'], 'src/FinalStateAnalysis/Utilities/test')
        self.src_file_path = os.path.join(self.test_dir, 'testCaseFile*.root')
        self.collection = TFileCollection.TFileCollection(
            self.src_file_path, reset=True)
        self.file1 = ROOT.TFile(os.path.join(self.test_dir, "testCaseFile.root"))
        self.file2 = ROOT.TFile(os.path.join(self.test_dir, "testCaseFile2.root"))

        intial_puts = self.collection.put_counter
        result = self.collection.Get("/emt/final/OS/Tau/TauPt")
        self.assertEqual(self.collection.put_counter, intial_puts + 1)
        histo1 = self.file1.Get("/emt/final/OS/Tau/TauPt")
        histo2 = self.file2.Get("/emt/final/OS/Tau/TauPt")
        clone = histo1.Clone()
        clone.Add(histo2)
        self.assertAlmostEqual(result.Integral(), clone.Integral())
        self.assertAlmostEqual(result.GetMean(), clone.GetMean())
        # Do it again. Make sure we don't get an extra put getting the same
        # thing.
        result = self.collection.Get("/emt/final/OS/Tau/TauPt")
        self.assertEqual(self.collection.put_counter, intial_puts + 1)
        self.collection.write()
        self.collection.cache_file.Close()
        self.file1.Close()
        self.file2.Close()

    def test_ntuple_get(self):
        self.test_dir = os.path.join(
            os.environ['CMSSW_BASE'], 'src/FinalStateAnalysis/Utilities/test')
        self.src_file_path = os.path.join(self.test_dir, 'testCaseFile*.root')
        self.collection = TFileCollection.TFileCollection(
            self.src_file_path, reset=False)
        self.tchain = ROOT.TChain("emt/final/Ntuple")
        self.tchain.Add("testCaseFile*.root")

        intial_puts = self.collection.put_counter
        ctree = self.collection.Get("/emt/final/Ntuple")
        self.assertTrue(isinstance(ctree, CachingTTree.CachingTTree))

        # Make sure we cached the chain
        self.assertEqual(self.collection.put_counter, intial_puts + 1)
        initial_tree_puts = ctree.put_counter
        myhisto = ctree.draw("ElecPt", "ElecCharge > 0 & ElecEta < 2.1")
        self.assertEqual(ctree.put_counter, initial_tree_puts + 1)
        # Check caching
        myhisto = ctree.draw("ElecPt", "ElecCharge > 0 & ElecEta < 2.1")
        self.assertEqual(ctree.put_counter, initial_tree_puts + 1)
        # Sanity check
        n_selected = self.tchain.GetEntries("ElecCharge > 0 & ElecEta < 2.1")
        self.assertAlmostEqual(myhisto.Integral(), n_selected)
        self.collection.write()
        self.collection.cache_file.Close()


def test_main():
    test_support.run_unittest(TestTFileCollection)

if __name__ == '__main__':
    test_main()
