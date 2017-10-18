'''

Closure test on reading and writing cards.

Reads in the M=120 WWW card from Moriond12.

Writes it out, then reads it back in again.

'''

from FinalStateAnalysis.StatTools.cardreader import read_card
from FinalStateAnalysis.StatTools.cardwriter import write_card
from FinalStateAnalysis.StatTools.interpolator import interpolate_card
import unittest

class TestInterpolator(unittest.TestCase):
    def test_closure(self):
        new_120_file = open('vh3l_120_interpolated.txt', 'w')
        new_120 = interpolate_card(new_120_file,
                                   'vh3l_110.txt', 110,
                                   'vh3l_130.txt', 130,
                                   120, 'VHww', 'VHtt')
        new_120_file.close()
        new_120 = read_card('vh3l_120_interpolated.txt')


if __name__ == '__main__':
    unittest.main()
