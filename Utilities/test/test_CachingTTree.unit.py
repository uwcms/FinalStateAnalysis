import ROOT
import tempfile
import FinalStateAnalysis.Utilities.CachingTTree as CachingTTree
import os

import unittest
from test import test_support

class TestCachingTTree(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        #self.cache_dir = tempfile.mkdtemp()
        self.cache_dir = '.'
        print self.cache_dir
        self.temp_file = os.path.join(self.cache_dir, "temp.root")
        self.cache_file = ROOT.TFile(self.temp_file, "UPDATE")
        self.test_dir = os.path.join(
            os.environ['CMSSW_BASE'], 'src/FinalStateAnalysis/Utilities/test')
        self.src_file_path = os.path.join(self.test_dir, 'testCaseFile.root')
        self.src_file = ROOT.TFile.Open(self.src_file_path, 'READ')
        self.ttree = self.src_file.Get("/emt/final/Ntuple")
        self.caching_ttree = \
                CachingTTree.CachingTTree(self.ttree, self.cache_file)

    def test_passing_functions(self):
        self.assertEqual(self.caching_ttree.GetEntries(), 966)

    def test_draw(self):
        result = self.caching_ttree.draw("ElecAbsEta", "")
        key = self.caching_ttree.key("ElecAbsEta", "")
        self.assertAlmostEqual(result.GetMean(), 0.8068, 4)
        self.assertTrue(self.cache_file.Get(key))
        cached_result = self.cache_file.Get(key)
        self.assertAlmostEqual(cached_result.GetMean(), 0.8068, 4)

    def tearDown(self):
        self.cache_file.ls()
        #self.cache_file.Write()

def test_main():
    test_support.run_unittest(TestCachingTTree)

if __name__ == '__main__':
    test_main()
