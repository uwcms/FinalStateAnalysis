'''

Test generation of stat. error shapes.

Reads in stat_test_shapes.root

'''


import unittest
import ROOT
import os
import math

class TestStatShapes(unittest.TestCase):
    def test_statshapes(self):
        os.system('rm -f stat_test_shapes_output.root')
        res = os.system('add_stat_shapes.py stat_shapes_test.root stat_test_shapes_output.root'
                  ' --filter "*fakes*"')
        self.assertTrue(res == 0)
        output = ROOT.TFile('stat_test_shapes_output.root', 'READ')
        fake_histo = output.Get('fakes')
        # No shape created for zero bin
        self.assertTrue(fake_histo.GetBinContent(1) == 0)
        self.assertFalse(output.Get('fakes_ss_bin_1_up'))

        self.assertAlmostEqual(fake_histo.GetBinContent(2), 1)
        self.assertTrue(output.Get('fakes_ss_bin_2_up'))
        self.assertTrue(output.Get('fakes_ss_bin_2_down'))

        bin2up = output.Get('fakes_ss_bin_2_up')
        bin2down = output.Get('fakes_ss_bin_2_down')
        self.assertAlmostEqual(bin2up.GetBinContent(2), 2)
        self.assertAlmostEqual(bin2down.GetBinContent(2), 0)
        # 3rd bin is unchanged
        self.assertAlmostEqual(bin2up.GetBinContent(3), fake_histo.GetBinContent(3))

        # Check higher stat bin
        self.assertAlmostEqual(fake_histo.GetBinContent(4), 3)
        bin4up = output.Get('fakes_ss_bin_4_up')
        self.assertAlmostEqual(bin4up.GetBinContent(4), 3 + math.sqrt(3), 5)

    def test_threshold(self):
        # Check we can increase the threshold to exclude some bins
        # sqrt(3)/3 = .577350269 should exclude bin 4
        os.system('rm -f stat_test_shapes_output_thresh.root')
        res = os.system('add_stat_shapes.py stat_shapes_test.root stat_test_shapes_output_thresh.root'
                  ' --filter "*fakes*" --threshold 0.6')
        output = ROOT.TFile('stat_test_shapes_output_thresh.root', 'READ')
        self.assertTrue(output.Get('fakes_ss_bin_2_up'))
        self.assertFalse(output.Get('fakes_ss_bin_4_up'))


if __name__ == '__main__':
    unittest.main()
