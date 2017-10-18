'''

Test of removing systematics

Reads in the M=120 WWW card from Moriond12.

Writes it out without the pdf_qqbar systematic.

'''

import unittest
from FinalStateAnalysis.StatTools.cardreader import read_card
import os

class TestSysRemover(unittest.TestCase):
    def test_closure(self):
        os.system('remove_systematics.py vh3l_120.txt "pdf_qqba*" > vh3l_nosys.txt')
        www_card_orig = read_card('vh3l_120.txt')
        www_card_nosys = read_card('vh3l_nosys.txt')

        self.assertTrue(
            'pdf_qqbar' in [x[0] for x in www_card_orig.systs]
        )
        self.assertTrue(
            'pdf_qqbar' not in [x[0] for x in www_card_nosys.systs]
        )

if __name__ == '__main__':
    unittest.main()
